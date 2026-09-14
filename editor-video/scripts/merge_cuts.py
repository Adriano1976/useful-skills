#!/usr/bin/env python3
"""
Merge dos resultados de análise por chunks.
Consolida os vereditos do LLM e gera o JSON final com trechos a MANTER no vídeo.
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional


def resolve_overlap(
    verdicts: Dict[int, Dict],
    chunk_results: List[Dict],
) -> Dict[int, Dict]:
    """
    Resolve conflitos no overlap entre chunks.
    Regra: prevalece a decisão da segunda janela (onde o bloco está mais centralizado).
    """
    for i in range(1, len(chunk_results)):
        chunk = chunk_results[i]
        overlap_indices = chunk.get("overlap_start_indices", [])
        
        for block_verdict in chunk["verdicts"]:
            idx = block_verdict["index"]
            if idx in [oi for oi in overlap_indices]:
                verdicts[idx] = block_verdict
            elif idx not in verdicts:
                verdicts[idx] = block_verdict
    
    return verdicts


def build_verdicts_map(chunk_results: List[Dict]) -> Dict[int, Dict]:
    """
    Constrói mapa completo de vereditos a partir dos resultados dos chunks.
    """
    verdicts = {}
    
    if chunk_results:
        for v in chunk_results[0]["verdicts"]:
            verdicts[v["index"]] = v
    
    verdicts = resolve_overlap(verdicts, chunk_results)
    
    return verdicts


def merge_keeps(
    blocks: List[Dict],
    verdicts: Dict[int, Dict],
    silences: List[Dict],
    transition_gap: float = 0.3,
    silence_threshold: float = 1.0
) -> List[Dict[str, float]]:
    """
    Gera a lista final de trechos a serem MANTIDOS no vídeo.
    
    Agrupa blocos consecutivos "keep" em segmentos contínuos.
    Silêncios > silence_threshold entre dois keeps quebram o segmento
    (removendo o silêncio excessivo).
    
    Args:
        blocks: Lista de blocos do SRT [{index, start, end, text}]
        verdicts: Mapa de vereditos {index: {verdict: "keep"|"cut", ...}}
        silences: Lista de silêncios detectados [{start, end, duration, after_block}]
        transition_gap: Margem (em segundos) para transições suaves
        silence_threshold: Limiar de silêncio em segundos
    
    Returns:
        Lista de trechos a MANTER: [{start: float, end: float}]
    """
    # Identifica blocos keep
    keep_indices = set()
    for idx, v in verdicts.items():
        if v.get("verdict") == "keep":
            keep_indices.add(idx)
    
    # Mapeia blocos por index
    block_map = {b["index"]: b for b in blocks}
    sorted_indices = sorted(block_map.keys())
    
    # Set de blocos "after" que têm silêncio longo
    silence_after = set()
    for s in silences:
        if s["duration"] > silence_threshold:
            silence_after.add(s["after_block"])
    
    # Agrupa blocos consecutivos "keep" em segmentos
    keeps: List[Dict[str, float]] = []
    current_start = None
    current_end = None
    prev_idx = None
    
    for idx in sorted_indices:
        if idx not in keep_indices:
            # Bloco é "cut" — fecha o segmento atual se existir
            if current_start is not None:
                keeps.append({
                    "start": round(current_start, 2),
                    "end": round(current_end, 2)
                })
                current_start = None
                current_end = None
                prev_idx = None
            continue
        
        block = block_map[idx]
        
        if current_start is None:
            # Início de novo segmento keep
            current_start = block["start"]
            current_end = block["end"]
            prev_idx = idx
        else:
            # Verifica se há silêncio longo entre o bloco anterior e este
            if prev_idx is not None and prev_idx in silence_after:
                # Silêncio longo entre dois keeps — quebra o segmento
                # Fecha o segmento anterior (com pequena margem)
                keeps.append({
                    "start": round(current_start, 2),
                    "end": round(current_end + transition_gap, 2)
                })
                # Inicia novo segmento (com pequena margem antes)
                current_start = block["start"] - transition_gap
                current_start = max(current_start, current_end)  # não sobrepor
                current_end = block["end"]
            else:
                # Continuação normal — expande o segmento
                current_end = block["end"]
            
            prev_idx = idx
    
    # Fecha o último segmento
    if current_start is not None:
        keeps.append({
            "start": round(current_start, 2),
            "end": round(current_end, 2)
        })
    
    return keeps


def generate_report(
    blocks: List[Dict],
    verdicts: Dict[int, Dict],
    keeps: List[Dict[str, float]]
) -> str:
    """Gera um relatório legível do processamento."""
    total = len(blocks)
    kept = sum(1 for v in verdicts.values() if v.get("verdict") == "keep")
    cut = sum(1 for v in verdicts.values() if v.get("verdict") == "cut")
    
    total_duration = blocks[-1]["end"] if blocks else 0
    keep_duration = sum(k["end"] - k["start"] for k in keeps)
    cut_duration = total_duration - keep_duration
    
    report = []
    report.append("=" * 60)
    report.append("RELATÓRIO DE ANÁLISE - SRT Video Cutter")
    report.append("=" * 60)
    report.append(f"Total de blocos analisados: {total}")
    report.append(f"Blocos mantidos (keep):     {kept} ({kept/total*100:.1f}%)")
    report.append(f"Blocos removidos (cut):     {cut} ({cut/total*100:.1f}%)")
    report.append(f"")
    report.append(f"Duração total estimada:     {total_duration:.1f}s ({total_duration/60:.1f} min)")
    report.append(f"Tempo mantido:              {keep_duration:.1f}s ({keep_duration/60:.1f} min)")
    report.append(f"Tempo removido:             {cut_duration:.1f}s ({cut_duration/60:.1f} min)")
    report.append(f"Redução:                    {cut_duration/total_duration*100:.1f}%")
    report.append(f"")
    report.append(f"Segmentos a manter:         {len(keeps)}")
    report.append("=" * 60)
    
    # Detalhes dos segmentos mantidos
    report.append("\nSEGMENTOS MANTIDOS:")
    report.append("-" * 60)
    for i, k in enumerate(keeps):
        duration = k["end"] - k["start"]
        report.append(f"  Segmento {i+1:3d}: {k['start']:8.2f}s - {k['end']:8.2f}s ({duration:.1f}s)")
    
    # Detalhes dos blocos cortados
    report.append("\nDETALHES DOS BLOCOS CORTADOS:")
    report.append("-" * 60)
    for idx in sorted(verdicts.keys()):
        v = verdicts[idx]
        if v.get("verdict") == "cut":
            block = next((b for b in blocks if b["index"] == idx), None)
            if block:
                report.append(
                    f"  [{idx:4d}] {block['start']:8.2f}s - {block['end']:8.2f}s | "
                    f"{v.get('reason', 'sem motivo')}"
                )
                report.append(f"          \"{block['text'][:80]}...\"" 
                            if len(block['text']) > 80 
                            else f"          \"{block['text']}\"")
    
    return "\n".join(report)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python merge_cuts.py --from-combined <combined_results.json>")
        sys.exit(1)
    
    if sys.argv[1] == "--from-combined":
        combined_path = sys.argv[2]
        with open(combined_path) as f:
            data = json.load(f)
        
        blocks = data["blocks"]
        silences = data.get("silences", [])
        chunk_results = data["chunk_results"]
        
        verdicts = build_verdicts_map(chunk_results)
        keeps = merge_keeps(blocks, verdicts, silences)
        
        report = generate_report(blocks, verdicts, keeps)
        print(report)
        
        output_path = Path(combined_path).parent / "keeps_final.json"
        output_path.write_text(json.dumps(keeps, ensure_ascii=False, indent=2))
        print(f"\nJSON de trechos a manter salvo em: {output_path}")
        
    else:
        print("Use: python merge_cuts.py --from-combined <combined_results.json>")
        sys.exit(1)
