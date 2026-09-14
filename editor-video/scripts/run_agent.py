#!/usr/bin/env python3
"""
SRT Video Cutter - Script Orquestrador Principal

Pipeline completo:
1. Parse do SRT
2. Chunking com janela deslizante
3. Análise por chunk via LLM (Claude API)
4. Merge e geração do JSON final de cortes

Uso:
    python run_agent.py <arquivo.srt> --api-key <ANTHROPIC_API_KEY>
    
    Ou com variável de ambiente:
    export ANTHROPIC_API_KEY=sk-...
    python run_agent.py <arquivo.srt>

Parâmetros opcionais:
    --silence-threshold  Gap mínimo para silêncio (default: 1.0s)
    --chunk-size         Blocos por chunk (default: 40)
    --overlap            Blocos de overlap (default: 5)
    --model              Modelo Claude a usar (default: claude-sonnet-4-20250514)
    --output             Caminho do JSON de saída (default: <arquivo>_cuts.json)
    --dry-run            Apenas parse e chunking, sem chamar LLM
    --verbose            Mostra detalhes do processamento
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

# Importa módulos locais
sys.path.insert(0, str(Path(__file__).parent))
from parse_srt import parse_srt, create_chunks
from merge_cuts import build_verdicts_map, merge_keeps, generate_report


# ============================================================
# Prompt Template (carregado inline para simplicidade)
# ============================================================

ANALYSIS_PROMPT = """Você é um editor de vídeo especializado em análise de legendas. Sua tarefa é analisar
os blocos de legenda abaixo e decidir quais trechos devem ser MANTIDOS e quais devem
ser CORTADOS do vídeo final.

## Contexto
- Estes são blocos de legenda de um vídeo educativo sobre Inteligência Artificial em PT-BR.
- O apresentador grava sozinho e comete erros de fala naturais.
- Quando erra, ele para e repete a mesma frase (com pequenas variações).
- O padrão típico é: frase com erro → pausa → mesma frase corrigida.
- Às vezes ele repete mais de 2 vezes antes de acertar.

## Regras de Decisão

1. REPETIÇÕES CONSECUTIVAS:
   - Quando duas ou mais frases consecutivas dizem essencialmente a mesma coisa,
     mantenha APENAS A ÚLTIMA versão (que é a corrigida).
   - Marque todas as versões anteriores como "cut".

2. FALSOS INÍCIOS:
   - Frases curtas e incompletas seguidas de uma versão completa → cortar o início falso.

3. GAGUEJOS E HESITAÇÕES:
   - Blocos que são predominantemente hesitações ("éh", "hm", "tipo assim", "é...")
     seguidos de fala clara → cortar as hesitações.
   - MAS: hesitações breves dentro de uma frase normal NÃO devem ser cortadas.

4. FALA NORMAL:
   - Frases fluentes que avançam o conteúdo → sempre manter ("keep").
   - Na dúvida, mantenha. É melhor preservar algo duvidoso do que perder conteúdo bom.

5. MÚLTIPLAS TENTATIVAS:
   - Se o apresentador tenta a mesma frase 3 ou mais vezes, mantenha APENAS a última.

## Formato de Resposta

Responda APENAS com um JSON válido, sem nenhum texto adicional, sem markdown backticks.
O JSON deve ser um array de objetos, um para cada bloco:

[
  {"index": <número_do_bloco>, "verdict": "keep" ou "cut", "reason": "<motivo breve>"}
]

## Blocos para Análise

"""


def call_claude_api(
    prompt: str,
    api_key: str,
    model: str = "claude-sonnet-4-20250514",
    max_tokens: int = 4096,
    max_retries: int = 3,
    verbose: bool = False
) -> Optional[str]:
    """
    Chama a API do Claude para analisar um chunk.
    
    Usa urllib para evitar dependência do anthropic SDK.
    """
    import urllib.request
    import urllib.error
    
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01"
    }
    
    body = json.dumps({
        "model": model,
        "max_tokens": max_tokens,
        "temperature": 0,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }).encode("utf-8")
    
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, data=body, headers=headers, method="POST")
            
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                
                # Extrai texto da resposta
                text = ""
                for block in result.get("content", []):
                    if block.get("type") == "text":
                        text += block["text"]
                
                if verbose:
                    usage = result.get("usage", {})
                    print(f"    Tokens: input={usage.get('input_tokens', '?')}, "
                          f"output={usage.get('output_tokens', '?')}")
                
                return text
                
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else ""
            if e.code == 429:
                # Rate limit — espera e tenta novamente
                wait = (attempt + 1) * 10
                print(f"    ⚠ Rate limit atingido. Aguardando {wait}s...")
                time.sleep(wait)
            elif e.code == 529:
                # Overloaded
                wait = (attempt + 1) * 15
                print(f"    ⚠ API sobrecarregada. Aguardando {wait}s...")
                time.sleep(wait)
            else:
                print(f"    ✗ Erro HTTP {e.code}: {error_body[:200]}")
                if attempt == max_retries - 1:
                    return None
                time.sleep(5)
                
        except Exception as e:
            print(f"    ✗ Erro: {e}")
            if attempt == max_retries - 1:
                return None
            time.sleep(5)
    
    return None


def parse_llm_response(response: str) -> Optional[List[Dict]]:
    """
    Parseia a resposta do LLM como JSON.
    Remove backticks markdown se presentes.
    """
    if not response:
        return None
    
    # Remove backticks markdown
    text = response.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()
    
    try:
        result = json.loads(text)
        if isinstance(result, list):
            return result
        return None
    except json.JSONDecodeError as e:
        print(f"    ✗ Erro ao parsear JSON: {e}")
        print(f"    Resposta (primeiros 200 chars): {text[:200]}")
        return None


def analyze_chunk(
    chunk: Dict,
    api_key: str,
    model: str,
    verbose: bool = False
) -> Optional[Dict]:
    """
    Analisa um chunk de blocos via LLM.
    
    Returns:
        Dict com chunk_id, verdicts e overlap_start_indices
    """
    blocks_json = json.dumps(chunk["blocks"], ensure_ascii=False, indent=2)
    prompt = ANALYSIS_PROMPT + blocks_json
    
    if verbose:
        block_range = f"{chunk['blocks'][0]['index']}-{chunk['blocks'][-1]['index']}"
        print(f"  → Chunk {chunk['chunk_id']}: blocos {block_range} "
              f"({len(chunk['blocks'])} blocos)")
    
    response = call_claude_api(prompt, api_key, model=model, verbose=verbose)
    
    if not response:
        print(f"    ✗ Falha ao obter resposta para chunk {chunk['chunk_id']}")
        return None
    
    verdicts = parse_llm_response(response)
    
    if not verdicts:
        # Tenta uma segunda vez
        if verbose:
            print(f"    ↻ Tentando novamente...")
        response = call_claude_api(prompt, api_key, model=model, verbose=verbose)
        verdicts = parse_llm_response(response)
    
    if not verdicts:
        print(f"    ✗ Falha ao parsear resposta do chunk {chunk['chunk_id']}")
        # Fallback: marca todos como "keep" (conservador)
        verdicts = [
            {"index": b["index"], "verdict": "keep", "reason": "fallback - erro no LLM"}
            for b in chunk["blocks"]
        ]
    
    return {
        "chunk_id": chunk["chunk_id"],
        "verdicts": verdicts,
        "overlap_start_indices": chunk.get("overlap_start_indices", [])
    }


def run_pipeline(
    srt_path: str,
    api_key: str,
    silence_threshold: float = 1.0,
    chunk_size: int = 40,
    overlap: int = 5,
    model: str = "claude-sonnet-4-20250514",
    output_path: Optional[str] = None,
    dry_run: bool = False,
    verbose: bool = False
) -> List[Dict[str, float]]:
    """
    Executa o pipeline completo.
    
    Returns:
        Lista de cortes [{start, end}]
    """
    print("=" * 60)
    print("SRT Video Cutter Agent")
    print("=" * 60)
    
    # --- Etapa 1: Parse ---
    print(f"\n📄 Etapa 1: Parse do SRT")
    print(f"   Arquivo: {srt_path}")
    
    result = parse_srt(srt_path, silence_threshold=silence_threshold)
    blocks = result["blocks"]
    silences = result["silences"]
    
    print(f"   ✓ {result['total_blocks']} blocos extraídos")
    print(f"   ✓ {result['total_silences']} silêncios detectados (>{silence_threshold}s)")
    print(f"   ✓ Duração: {result['total_duration']:.1f}s ({result['total_duration']/60:.1f} min)")
    
    # --- Etapa 2: Chunking ---
    print(f"\n📦 Etapa 2: Chunking (size={chunk_size}, overlap={overlap})")
    
    chunks = create_chunks(blocks, chunk_size=chunk_size, overlap=overlap)
    print(f"   ✓ {len(chunks)} chunks criados")
    
    if dry_run:
        print("\n🛑 Dry run — parando antes da análise LLM")
        print(f"\n   Chunks:")
        for chunk in chunks:
            block_range = f"{chunk['blocks'][0]['index']}-{chunk['blocks'][-1]['index']}"
            print(f"   Chunk {chunk['chunk_id']}: blocos {block_range} ({len(chunk['blocks'])} blocos)")
        return []
    
    # --- Etapa 3: Análise via LLM ---
    print(f"\n🤖 Etapa 3: Análise via LLM ({model})")
    print(f"   Processando {len(chunks)} chunks...")
    
    chunk_results = []
    for i, chunk in enumerate(chunks):
        print(f"\n   [{i+1}/{len(chunks)}]", end="")
        
        result_chunk = analyze_chunk(chunk, api_key, model, verbose=verbose)
        
        if result_chunk:
            chunk_results.append(result_chunk)
            
            # Estatísticas do chunk
            keeps = sum(1 for v in result_chunk["verdicts"] if v.get("verdict") == "keep")
            cuts = sum(1 for v in result_chunk["verdicts"] if v.get("verdict") == "cut")
            print(f"    ✓ keep={keeps}, cut={cuts}")
        else:
            print(f"    ✗ Falhou")
        
        # Pequeno delay entre chunks para evitar rate limit
        if i < len(chunks) - 1:
            time.sleep(1)
    
    # --- Etapa 4: Merge ---
    print(f"\n🔧 Etapa 4: Merge dos resultados")
    
    verdicts = build_verdicts_map(chunk_results)
    keeps = merge_keeps(blocks, verdicts, silences)
    
    # Relatório
    report = generate_report(blocks, verdicts, keeps)
    print(f"\n{report}")
    
    # Salva output
    if not output_path:
        output_path = str(Path(srt_path).with_suffix('')) + "_keeps.json"
    
    Path(output_path).write_text(json.dumps(keeps, ensure_ascii=False, indent=2))
    print(f"\n✅ JSON de trechos a manter salvo em: {output_path}")
    
    # Salva também o relatório detalhado
    report_path = str(Path(output_path).with_suffix('')) + "_report.txt"
    Path(report_path).write_text(report)
    print(f"📊 Relatório salvo em: {report_path}")
    
    # Salva verdicts completos para debug
    verdicts_path = str(Path(output_path).with_suffix('')) + "_verdicts.json"
    verdicts_list = [verdicts[k] for k in sorted(verdicts.keys())]
    Path(verdicts_path).write_text(json.dumps(verdicts_list, ensure_ascii=False, indent=2))
    print(f"🔍 Vereditos detalhados: {verdicts_path}")
    
    return keeps


def main():
    parser = argparse.ArgumentParser(
        description="SRT Video Cutter - Edição automática de vídeo via análise de legendas SRT"
    )
    parser.add_argument("srt_file", help="Caminho para o arquivo .srt")
    parser.add_argument("--api-key", help="Anthropic API key (ou use ANTHROPIC_API_KEY env var)")
    parser.add_argument("--silence-threshold", type=float, default=1.0,
                       help="Gap mínimo para silêncio em segundos (default: 1.0)")
    parser.add_argument("--chunk-size", type=int, default=40,
                       help="Número de blocos por chunk (default: 40)")
    parser.add_argument("--overlap", type=int, default=5,
                       help="Blocos de overlap entre chunks (default: 5)")
    parser.add_argument("--model", default="claude-sonnet-4-20250514",
                       help="Modelo Claude (default: claude-sonnet-4-20250514)")
    parser.add_argument("--output", help="Caminho do JSON de saída")
    parser.add_argument("--dry-run", action="store_true",
                       help="Apenas parse e chunking, sem chamar LLM")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Mostra detalhes do processamento")
    
    args = parser.parse_args()
    
    # API key
    api_key = args.api_key or os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key and not args.dry_run:
        print("❌ Erro: forneça a API key via --api-key ou ANTHROPIC_API_KEY env var")
        sys.exit(1)
    
    # Valida arquivo
    if not Path(args.srt_file).exists():
        print(f"❌ Erro: arquivo não encontrado: {args.srt_file}")
        sys.exit(1)
    
    # Executa
    cuts = run_pipeline(
        srt_path=args.srt_file,
        api_key=api_key,
        silence_threshold=args.silence_threshold,
        chunk_size=args.chunk_size,
        overlap=args.overlap,
        model=args.model,
        output_path=args.output,
        dry_run=args.dry_run,
        verbose=args.verbose
    )
    
    print(f"\n{'='*60}")
    print(f"Total de cortes: {len(cuts)}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
