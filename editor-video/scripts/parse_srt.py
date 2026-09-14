#!/usr/bin/env python3
"""
Parser de arquivos SRT.
Extrai blocos de legenda com timestamps em segundos (float) e texto.
Também detecta silêncios entre blocos.
"""

import re
import json
import sys
from pathlib import Path
from typing import List, Dict, Any


def timestamp_to_seconds(ts: str) -> float:
    """
    Converte timestamp SRT para segundos float.
    
    Aceita múltiplos formatos gerados pelo Whisper:
      - HH:MM:SS,mmm        (padrão SRT)
      - HH:MM:SS.mmm        (variante com ponto)
      - H:MM:SS,mmmmmm      (Whisper: hora 1 dígito, ms 6 dígitos)
      - H:MM:SS.mmmmmm      (variante)
      - H:MM:SS              (sem milissegundos)
      - HH:MM:SS             (sem milissegundos)
    """
    ts = ts.strip()
    
    # Padrão flexível: 1-2 dígitos hora, 2 dígitos min/seg, 0-6 dígitos ms (opcional)
    match = re.match(r'(\d{1,2}):(\d{2}):(\d{2})(?:[,.](\d{1,6}))?', ts)
    if not match:
        raise ValueError(f"Timestamp inválido: {ts}")
    
    h, m, s = int(match.group(1)), int(match.group(2)), int(match.group(3))
    
    ms_str = match.group(4)
    if ms_str:
        # Normaliza para milissegundos (3 dígitos)
        # Se 6 dígitos (microsegundos do Whisper), converte para ms
        if len(ms_str) <= 3:
            ms = int(ms_str.ljust(3, '0'))  # pad right com zeros
        else:
            ms = int(ms_str[:3])  # trunca para 3 dígitos (ignora microsegundos)
    else:
        ms = 0
    
    return h * 3600 + m * 60 + s + ms / 1000


def parse_srt(filepath: str, silence_threshold: float = 1.0) -> Dict[str, Any]:
    """
    Parse de um arquivo SRT.
    
    Args:
        filepath: Caminho para o arquivo .srt
        silence_threshold: Gap mínimo (em segundos) para considerar silêncio. Default: 1.0s
    
    Returns:
        Dict com:
          - blocks: lista de blocos {index, start, end, text}
          - silences: lista de silêncios {start, end, duration, after_block}
          - total_duration: duração total estimada do vídeo
          - total_blocks: número total de blocos
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
    
    # Tenta múltiplos encodings comuns
    content = None
    for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']:
        try:
            content = path.read_text(encoding=encoding)
            break
        except UnicodeDecodeError:
            continue
    
    if content is None:
        raise ValueError(f"Não foi possível decodificar o arquivo: {filepath}")
    
    # Remove BOM se presente
    content = content.lstrip('\ufeff')
    
    # Parse dos blocos SRT
    # Padrão flexível para timestamps do Whisper (1-2 dígitos hora, 3-6 dígitos ms ou sem ms)
    pattern = re.compile(
        r'(\d+)\s*\n'
        r'(\d{1,2}:\d{2}:\d{2}(?:[,.]\d{1,6})?)\s*-->\s*(\d{1,2}:\d{2}:\d{2}(?:[,.]\d{1,6})?)\s*\n'
        r'((?:(?!\d+\s*\n\d{1,2}:\d{2}:\d{2}).+\n?)*)',
        re.MULTILINE
    )
    
    blocks: List[Dict[str, Any]] = []
    
    for match in pattern.finditer(content):
        index = int(match.group(1))
        start = timestamp_to_seconds(match.group(2))
        end = timestamp_to_seconds(match.group(3))
        text = match.group(4).strip()
        
        # Remove tags HTML/formatting do Whisper (ex: <font>, <i>)
        text = re.sub(r'<[^>]+>', '', text)
        
        # Junta linhas múltiplas em uma só
        text = ' '.join(text.split('\n')).strip()
        
        if text:  # Ignora blocos vazios
            blocks.append({
                "index": index,
                "start": round(start, 2),
                "end": round(end, 2),
                "text": text
            })
    
    # Detecta silêncios
    silences: List[Dict[str, Any]] = []
    for i in range(len(blocks) - 1):
        gap = blocks[i + 1]["start"] - blocks[i]["end"]
        if gap > silence_threshold:
            silences.append({
                "start": round(blocks[i]["end"], 2),
                "end": round(blocks[i + 1]["start"], 2),
                "duration": round(gap, 2),
                "after_block": blocks[i]["index"]
            })
    
    total_duration = blocks[-1]["end"] if blocks else 0.0
    
    return {
        "blocks": blocks,
        "silences": silences,
        "total_duration": round(total_duration, 2),
        "total_blocks": len(blocks),
        "total_silences": len(silences),
        "silence_threshold": silence_threshold
    }


def create_chunks(blocks: List[Dict], chunk_size: int = 40, overlap: int = 5) -> List[Dict]:
    """
    Divide os blocos em chunks com overlap para processamento por janela deslizante.
    
    Args:
        blocks: Lista de blocos do SRT
        chunk_size: Número de blocos por chunk
        overlap: Número de blocos de overlap entre chunks consecutivos
    
    Returns:
        Lista de chunks, cada um com:
          - chunk_id: índice do chunk
          - blocks: blocos deste chunk
          - overlap_start: índice do primeiro bloco de overlap (do chunk anterior)
          - overlap_end: índice do último bloco de overlap (para o próximo chunk)
          - is_first: se é o primeiro chunk
          - is_last: se é o último chunk
    """
    if not blocks:
        return []
    
    if len(blocks) <= chunk_size:
        return [{
            "chunk_id": 0,
            "blocks": blocks,
            "overlap_start": None,
            "overlap_end": None,
            "is_first": True,
            "is_last": True
        }]
    
    chunks = []
    step = chunk_size - overlap
    total = len(blocks)
    
    for i, start_idx in enumerate(range(0, total, step)):
        end_idx = min(start_idx + chunk_size, total)
        chunk_blocks = blocks[start_idx:end_idx]
        
        chunk = {
            "chunk_id": i,
            "blocks": chunk_blocks,
            "is_first": start_idx == 0,
            "is_last": end_idx >= total,
            "start_block_index": blocks[start_idx]["index"],
            "end_block_index": blocks[end_idx - 1]["index"],
        }
        
        # Marcar região de overlap
        if start_idx > 0:
            chunk["overlap_start_indices"] = [
                b["index"] for b in chunk_blocks[:overlap]
            ]
        else:
            chunk["overlap_start_indices"] = []
        
        chunks.append(chunk)
        
        if end_idx >= total:
            break
    
    return chunks


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python parse_srt.py <arquivo.srt> [silence_threshold]")
        print("  silence_threshold: gap mínimo em segundos (default: 1.0)")
        sys.exit(1)
    
    filepath = sys.argv[1]
    threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
    
    result = parse_srt(filepath, silence_threshold=threshold)
    
    print(f"\n=== Resumo do SRT ===")
    print(f"Total de blocos: {result['total_blocks']}")
    print(f"Total de silêncios (>{threshold}s): {result['total_silences']}")
    print(f"Duração estimada: {result['total_duration']:.1f}s "
          f"({result['total_duration']/60:.1f} min)")
    
    # Cria chunks
    chunks = create_chunks(result["blocks"])
    print(f"Chunks para processamento: {len(chunks)}")
    
    # Salva output
    output = {
        **result,
        "chunks": chunks
    }
    
    output_path = Path(filepath).with_suffix('.parsed.json')
    output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2))
    print(f"\nOutput salvo em: {output_path}")
