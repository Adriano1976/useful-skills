#!/usr/bin/env python3
"""
Resolve o caminho de saída para o resumo estendido.

Prioridade:
  1. Pasta indicada pelo usuário (--user-path)
  2. Mesma pasta do PDF de origem (--pdf)
  3. Fallback para /mnt/user-data/outputs/

Uso:
    python resolve_output.py --pdf <caminho_pdf> --name <nome_artigo>
    python resolve_output.py --user-path /home/user/docs --name <nome_artigo>
    python resolve_output.py --name <nome_artigo>

Saída:
    Caminho completo do arquivo de saída impresso em stdout.
"""

import os
import re
import argparse


def sanitize_filename(name: str) -> str:
    """Remove caracteres inválidos e normaliza o nome do arquivo."""
    # Substituir caracteres especiais por underscore
    name = re.sub(r'[^\w\s-]', '_', name.lower())
    # Substituir espaços por underscore
    name = re.sub(r'[\s]+', '_', name)
    # Remover underscores duplicados
    name = re.sub(r'_+', '_', name).strip('_')
    # Limitar tamanho
    return name[:80] if len(name) > 80 else name


def resolve_output_path(
    pdf_path: str | None = None,
    user_path: str | None = None,
    article_name: str = "artigo",
) -> str:
    """Determina onde salvar o resumo."""
    filename = f"resumo_estendido_{sanitize_filename(article_name)}.md"

    # 1. Pasta indicada pelo usuário
    if user_path:
        os.makedirs(user_path, exist_ok=True)
        return os.path.join(user_path, filename)

    # 2. Mesma pasta do PDF
    if pdf_path:
        pdf_dir = os.path.dirname(os.path.abspath(pdf_path))
        if os.access(pdf_dir, os.W_OK):
            return os.path.join(pdf_dir, filename)

    # 3. Fallback
    fallback = "/mnt/user-data/outputs"
    os.makedirs(fallback, exist_ok=True)
    return os.path.join(fallback, filename)


def main():
    parser = argparse.ArgumentParser(description="Resolve caminho de saída do resumo")
    parser.add_argument("--pdf", help="Caminho do PDF de origem")
    parser.add_argument("--user-path", help="Pasta indicada pelo usuário")
    parser.add_argument("--name", default="artigo", help="Nome do artigo para o arquivo")
    args = parser.parse_args()

    output_path = resolve_output_path(
        pdf_path=args.pdf,
        user_path=args.user_path,
        article_name=args.name,
    )
    print(output_path)


if __name__ == "__main__":
    main()
