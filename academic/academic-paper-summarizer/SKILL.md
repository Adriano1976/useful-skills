---
name: academic-paper-summarizer
description: >
  Lê artigos científicos (PDF ou link da web) e gera um resumo estendido em português brasileiro
  com os pontos mais importantes. Use este skill sempre que o usuário pedir para resumir, analisar,
  sintetizar ou explicar um artigo científico, paper acadêmico, preprint ou publicação de pesquisa.
  Também deve ser usado quando o usuário mencionar termos como "paper", "artigo", "publicação",
  "preprint", "arxiv", "resumo estendido", "resumo científico", "pontos principais de um artigo",
  ou quando fornecer um PDF ou link de site acadêmico (arxiv.org, scholar.google.com, sciencedirect,
  ieee, acm, springer, nature, science, plos, etc.) pedindo análise ou resumo. Funciona tanto com
  PDFs enviados pelo usuário quanto com links diretos para artigos online.
---

# Academic Paper Summarizer

Gera resumos estendidos de artigos científicos em pt-BR. Aceita PDF, link direto ou referência textual.

## Fluxo de Trabalho

### 1. Identificar a Fonte

- **PDF enviado** → arquivo em `/mnt/user-data/uploads/`. Usar o script `scripts/extract_pdf.py` para extrair texto.
- **Link direto** → usar `web_fetch` para buscar conteúdo. Se for link de PDF, baixar e processar como PDF.
- **Referência textual** (título ou DOI) → usar `web_search` para localizar, depois seguir o fluxo de link.

### 2. Extrair Texto

Executar o script de extração:

```bash
python scripts/extract_pdf.py <caminho_do_pdf>
```

O script tenta `pdfplumber` primeiro. Se o texto extraído for muito curto (PDF escaneado), tenta OCR com `pytesseract`. Ver detalhes em `scripts/extract_pdf.py`.

### 3. Identificar Seções

Após obter o texto, identificar as seções padrão: Título/Autores, Abstract, Introdução, Trabalhos Relacionados, Metodologia, Resultados, Discussão, Conclusão, Referências. Adaptar conforme o artigo real.

### 4. Gerar o Resumo Estendido

Seguir o template e as diretrizes de qualidade em `references/TEMPLATE.md`. O resumo deve ter entre 800 e 2000 palavras, proporcionalmente à complexidade do artigo.

### 5. Salvar o Resultado

A lógica de salvamento segue esta prioridade:

1. **Pasta indicada pelo usuário** — se especificou um caminho, usar esse caminho.
2. **Mesma pasta do PDF de origem** — se enviou PDF e não indicou pasta, salvar junto do PDF.
3. **Fallback** — `/mnt/user-data/outputs/` apenas se não for possível determinar a pasta.

Executar o script auxiliar para resolver o caminho:

```bash
python scripts/resolve_output.py --pdf <caminho_pdf> --user-path <caminho_usuario> --name <nome_artigo>
```

Antes de salvar, confirmar com o usuário se ele deseja alterar o local. Se o artigo veio de link (sem PDF local), perguntar onde salvar.

Usar `present_files` para entregar o arquivo ao usuário. Se preferir DOCX ou PDF, converter com o skill apropriado.

## Tratamento de Erros

Consultar `references/ERRORS.md` para a lista completa de cenários de erro e como tratá-los.
