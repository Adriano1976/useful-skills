---
name: youtube-thumbnail-downloader
description: >
  Faz download das imagens de thumbnail (capa) de vídeos do YouTube a partir de um arquivo
  contendo links do YouTube. Use esta skill SEMPRE que o usuário quiser: baixar thumbnails
  de vídeos do YouTube, fazer download de capas de vídeos do YouTube, obter imagens de
  miniatura de uma lista de links do YouTube, ou qualquer combinação de YouTube + thumbnail
  + download/baixar/capas/imagens/miniaturas.
  Ative também para frases como: "baixa as thumbnails", "faz download das capas",
  "quero as imagens dos vídeos", "pega as thumbnails desses links", "baixar thumbnail
  do YouTube", "download das miniaturas", "salvar capas de vídeos YouTube", "get youtube
  thumbnails", "download youtube video images". Funciona com arquivos .txt contendo
  links no formato youtube.com/watch?v=ID, youtu.be/ID, ou qualquer URL válida do YouTube.
---

# YouTube Thumbnail Downloader

Faz download das imagens de thumbnail (maxresdefault.jpg) de vídeos do YouTube a partir
de um arquivo com links — um link por linha.

## Fluxo de execução

### 1. Identificar o arquivo de links

O usuário vai indicar um caminho para uma pasta ou arquivo com os links do YouTube.

- Se o usuário indicar uma **pasta**: procure por arquivos `.txt` dentro dela e use o primeiro encontrado (ou pergunte qual usar se houver mais de um)
- Se o usuário indicar um **arquivo diretamente**: use esse arquivo

Confirme com o usuário o caminho encontrado antes de prosseguir, se houver ambiguidade.

### 2. Definir pasta de saída

- Por padrão, salve as thumbnails em uma subpasta chamada `thumbnails/` dentro da mesma pasta do arquivo de links
- Se o usuário especificar outro destino, use-o
- Crie a pasta de saída se ela não existir

### 3. Executar o script de download

Use o script Python incluído nesta skill para processar os links e fazer os downloads:

```bash
python3 <caminho-desta-skill>/scripts/download_thumbnails.py \
  --links <arquivo-de-links> \
  --output <pasta-de-saida>
```

O script:
- Lê cada linha do arquivo de links (ignora linhas em branco e comentários com `#`)
- Extrai o ID do vídeo de qualquer formato de URL do YouTube
- Tenta baixar `maxresdefault.jpg` (maior resolução disponível)
- Se `maxresdefault.jpg` não existir (vídeos antigos ou privados), tenta `hqdefault.jpg`
- Salva cada imagem com o nome `<video_id>.jpg`
- Exibe um resumo ao final: quantos foram baixados com sucesso, quais falharam

### 4. Reportar resultados

Após o download, informe ao usuário:
- Total de links processados
- Quantos thumbnails foram baixados com sucesso
- Quais links falharam (se houver), com o motivo
- Caminho da pasta onde as imagens foram salvas
- Use o `present_files` tool se disponível para mostrar as imagens baixadas

## Formatos de URL suportados

O script reconhece os seguintes formatos de URL do YouTube:

| Formato | Exemplo |
|---------|---------|
| URL padrão | `https://www.youtube.com/watch?v=dQw4w9WgXcQ` |
| URL curta | `https://youtu.be/dQw4w9WgXcQ` |
| URL de embed | `https://www.youtube.com/embed/dQw4w9WgXcQ` |
| URL sem protocolo | `youtube.com/watch?v=dQw4w9WgXcQ` |
| Apenas o ID | `dQw4w9WgXcQ` (11 caracteres alfanuméricos) |

## Notas importantes

- Não é necessária API key do YouTube — as thumbnails são públicas
- A URL de download usada é: `https://img.youtube.com/vi/<ID>/maxresdefault.jpg`
- Vídeos muito antigos ou com configurações específicas podem não ter `maxresdefault.jpg`, nesse caso o script usa `hqdefault.jpg` como fallback
- Vídeos privados ou removidos não terão thumbnail disponível
