#!/usr/bin/env python3
"""
YouTube Thumbnail Downloader
Faz download de thumbnails de vídeos do YouTube a partir de um arquivo com links.
Uso: python3 download_thumbnails.py --links <arquivo> --output <pasta>
"""

import argparse
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path


# Padrões para extrair o ID do vídeo do YouTube de diferentes formatos de URL
YOUTUBE_ID_PATTERNS = [
    # youtube.com/watch?v=ID ou youtube.com/watch?v=ID&...
    r'(?:youtube\.com/watch\?(?:.*&)?v=)([a-zA-Z0-9_-]{11})',
    # youtu.be/ID
    r'(?:youtu\.be/)([a-zA-Z0-9_-]{11})',
    # youtube.com/embed/ID
    r'(?:youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
    # youtube.com/v/ID
    r'(?:youtube\.com/v/)([a-zA-Z0-9_-]{11})',
    # youtube.com/shorts/ID
    r'(?:youtube\.com/shorts/)([a-zA-Z0-9_-]{11})',
    # ID puro (11 caracteres alfanuméricos + _ e -)
    r'^([a-zA-Z0-9_-]{11})$',
]

THUMBNAIL_QUALITIES = [
    'maxresdefault',  # 1280x720 (melhor qualidade)
    'hqdefault',      # 480x360 (fallback)
    'mqdefault',      # 320x180 (segundo fallback)
    'default',        # 120x90 (última opção)
]


def extract_video_id(line: str) -> str | None:
    """Extrai o ID do vídeo YouTube de uma URL ou string."""
    line = line.strip()
    if not line:
        return None

    for pattern in YOUTUBE_ID_PATTERNS:
        match = re.search(pattern, line)
        if match:
            return match.group(1)

    return None


def download_thumbnail(video_id: str, output_dir: Path) -> tuple[bool, str]:
    """
    Tenta baixar a thumbnail em maxresdefault, depois fallbacks.
    Retorna (sucesso, mensagem).
    """
    output_path = output_dir / f"{video_id}.jpg"

    # Não baixa novamente se já existir
    if output_path.exists():
        return True, f"já existe: {output_path.name}"

    for quality in THUMBNAIL_QUALITIES:
        url = f"https://img.youtube.com/vi/{video_id}/{quality}.jpg"
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; ThumbnailDownloader/1.0)'
            }
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request, timeout=15) as response:
                if response.status != 200:
                    continue

                content = response.read()

                # Thumbnails inválidas (vídeo não existe) geralmente têm < 1KB
                if len(content) < 1000:
                    continue

                output_path.write_bytes(content)
                size_kb = len(content) / 1024
                return True, f"baixado ({quality}, {size_kb:.0f}KB)"

        except urllib.error.HTTPError as e:
            if e.code == 404:
                continue  # Tenta próxima qualidade
            return False, f"erro HTTP {e.code}"
        except urllib.error.URLError as e:
            return False, f"erro de conexão: {e.reason}"
        except Exception as e:
            return False, f"erro inesperado: {str(e)}"

    return False, "thumbnail não disponível (vídeo privado, removido ou ID inválido)"


def process_links_file(links_file: Path, output_dir: Path) -> dict:
    """Processa o arquivo de links e faz os downloads. Retorna estatísticas."""
    results = {
        'total_lines': 0,
        'valid_ids': 0,
        'success': 0,
        'failed': 0,
        'skipped': 0,  # linhas em branco ou comentários
        'details': []
    }

    lines = links_file.read_text(encoding='utf-8').splitlines()
    results['total_lines'] = len(lines)

    for i, line in enumerate(lines, 1):
        line = line.strip()

        # Ignora linhas em branco e comentários
        if not line or line.startswith('#'):
            results['skipped'] += 1
            continue

        video_id = extract_video_id(line)

        if not video_id:
            results['failed'] += 1
            results['details'].append({
                'line': i,
                'input': line[:60],
                'status': 'falhou',
                'message': 'não foi possível extrair ID do YouTube'
            })
            print(f"  ✗ Linha {i}: ID não encontrado em '{line[:60]}'")
            continue

        results['valid_ids'] += 1
        success, message = download_thumbnail(video_id, output_dir)

        if success:
            results['success'] += 1
            status = 'sucesso'
        else:
            results['failed'] += 1
            status = 'falhou'

        results['details'].append({
            'line': i,
            'input': line[:60],
            'video_id': video_id,
            'status': status,
            'message': message
        })

        icon = '✓' if success else '✗'
        print(f"  {icon} [{video_id}] {message}")

    return results


def main():
    parser = argparse.ArgumentParser(
        description='Faz download de thumbnails de vídeos do YouTube'
    )
    parser.add_argument(
        '--links', '-l',
        required=True,
        help='Caminho para o arquivo com links do YouTube (um por linha)'
    )
    parser.add_argument(
        '--output', '-o',
        help='Pasta de destino para as thumbnails (padrão: thumbnails/ ao lado do arquivo)'
    )
    args = parser.parse_args()

    # Valida arquivo de links
    links_file = Path(args.links)
    if not links_file.exists():
        print(f"ERRO: Arquivo não encontrado: {links_file}", file=sys.stderr)
        sys.exit(1)
    if not links_file.is_file():
        print(f"ERRO: '{links_file}' não é um arquivo", file=sys.stderr)
        sys.exit(1)

    # Define pasta de saída
    if args.output:
        output_dir = Path(args.output)
    else:
        output_dir = links_file.parent / 'thumbnails'

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n🎬 YouTube Thumbnail Downloader")
    print(f"   Arquivo de links : {links_file}")
    print(f"   Pasta de saída   : {output_dir}")
    print(f"   Processando...\n")

    results = process_links_file(links_file, output_dir)

    # Resumo final
    print(f"\n{'='*50}")
    print(f"📊 Resumo:")
    print(f"   Total de linhas   : {results['total_lines']}")
    print(f"   IDs válidos       : {results['valid_ids']}")
    print(f"   ✓ Sucesso         : {results['success']}")
    print(f"   ✗ Falhas          : {results['failed']}")
    print(f"   Pasta de saída    : {output_dir.resolve()}")

    if results['failed'] > 0:
        print(f"\n⚠️  Links com falha:")
        for detail in results['details']:
            if detail['status'] == 'falhou':
                print(f"   Linha {detail['line']}: {detail['input']}")
                print(f"   → {detail['message']}")

    print(f"\n✅ Concluído!")

    # Saída estruturada para facilitar parsing pelo Claude
    print(f"\n__RESULT__")
    print(f"success_count={results['success']}")
    print(f"failed_count={results['failed']}")
    print(f"output_dir={output_dir.resolve()}")


if __name__ == '__main__':
    main()
