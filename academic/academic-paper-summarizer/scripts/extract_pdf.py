#!/usr/bin/env python3
"""
Extrai texto de um arquivo PDF.
Tenta pdfplumber primeiro; se o texto for muito curto (PDF escaneado),
faz fallback para OCR com pytesseract + pdf2image.

Uso:
    python extract_pdf.py <caminho_do_pdf> [--output <caminho_saida.txt>]

Saída:
    Texto extraído impresso em stdout (ou salvo em arquivo se --output).
"""

import sys
import argparse


def extract_with_pdfplumber(pdf_path: str) -> str:
    """Extrai texto usando pdfplumber (melhor para PDFs com texto nativo)."""
    import pdfplumber

    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                full_text += f"\n--- Página {i + 1} ---\n{text}"
    return full_text.strip()


def extract_with_ocr(pdf_path: str) -> str:
    """Extrai texto via OCR para PDFs escaneados."""
    import pytesseract
    from pdf2image import convert_from_path

    images = convert_from_path(pdf_path)
    full_text = ""
    for i, img in enumerate(images):
        text = pytesseract.image_to_string(img, lang="eng+por")
        if text.strip():
            full_text += f"\n--- Página {i + 1} ---\n{text}"
    return full_text.strip()


def extract_text(pdf_path: str, min_chars: int = 200) -> tuple[str, str]:
    """
    Extrai texto do PDF. Retorna (texto, método_usado).
    Se pdfplumber retornar menos que min_chars, tenta OCR.
    """
    # Tentar pdfplumber primeiro
    try:
        text = extract_with_pdfplumber(pdf_path)
        if len(text) >= min_chars:
            return text, "pdfplumber"
    except Exception as e:
        print(f"[AVISO] pdfplumber falhou: {e}", file=sys.stderr)

    # Fallback para OCR
    try:
        print("[INFO] Texto insuficiente via pdfplumber. Tentando OCR...", file=sys.stderr)
        text = extract_with_ocr(pdf_path)
        if text:
            return text, "ocr"
    except Exception as e:
        print(f"[AVISO] OCR falhou: {e}", file=sys.stderr)

    return "", "nenhum"


def main():
    parser = argparse.ArgumentParser(description="Extrai texto de PDF")
    parser.add_argument("pdf_path", help="Caminho do arquivo PDF")
    parser.add_argument("--output", "-o", help="Salvar texto em arquivo (opcional)")
    parser.add_argument(
        "--min-chars",
        type=int,
        default=200,
        help="Mínimo de caracteres para considerar extração bem-sucedida (default: 200)",
    )
    args = parser.parse_args()

    text, method = extract_text(args.pdf_path, args.min_chars)

    if not text:
        print("[ERRO] Não foi possível extrair texto do PDF.", file=sys.stderr)
        print("Sugestões:", file=sys.stderr)
        print("  - Verifique se o PDF não está protegido por senha", file=sys.stderr)
        print("  - Tente enviar uma versão com texto selecionável", file=sys.stderr)
        sys.exit(1)

    print(f"[INFO] Texto extraído com sucesso via {method} ({len(text)} caracteres)", file=sys.stderr)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[INFO] Texto salvo em: {args.output}", file=sys.stderr)
    else:
        print(text)


if __name__ == "__main__":
    main()
