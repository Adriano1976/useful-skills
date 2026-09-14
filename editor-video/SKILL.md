---
name: srt-video-cutter
description: >
  Agente de edição automática de vídeo via análise de legendas SRT. Use esta skill sempre que
  o usuário quiser limpar, editar ou cortar um vídeo removendo erros de fala, repetições e
  silêncios. Triggers incluem: upload de arquivo .srt, menções a "cortar vídeo", "editar vídeo",
  "remover erros de fala", "limpar legenda", "repetições no vídeo", "silêncios", ou qualquer
  pedido para analisar legendas e gerar pontos de corte. Também use quando o usuário mencionar
  "edição automática", "cortes automáticos", ou quiser processar legendas do Whisper para
  identificar trechos ruins. O output é sempre um JSON com timestamps dos trechos a remover.
---

# SRT Video Cutter Agent

Agente que analisa arquivos de legenda SRT (gerados pelo Whisper, em PT-BR) para identificar
automaticamente trechos que devem ser removidos de um vídeo: erros de fala, repetições
semânticas e silêncios longos.

## Visão Geral do Pipeline

```
[Arquivo .srt] → [Parse] → [Chunking] → [Análise LLM por chunk] → [Merge] → [JSON de cortes]
```

## Etapa 1 — Parse do SRT

Execute o script `scripts/parse_srt.py` para extrair os blocos do SRT.

```bash
python scripts/parse_srt.py <caminho_do_arquivo.srt>
```

O script retorna um JSON com a lista de blocos:
```json
[
  {"index": 1, "start": 0.0, "end": 3.52, "text": "Olá pessoal, tudo bem?"},
  {"index": 2, "start": 4.10, "end": 8.30, "text": "Hoje vamos falar sobre..."}
]
```

## Etapa 2 — Detecção de Silêncios

Silêncios são detectados automaticamente pelo script de parse. Um silêncio é definido como
um gap > 1.0 segundo entre o `end` de um bloco e o `start` do próximo. O script já marca
esses gaps no output.

## Etapa 3 — Análise por Chunks via LLM

Esta é a etapa principal. O arquivo SRT pode ser muito grande, então processamos em chunks
usando janela deslizante.

### Parâmetros de Chunking
- **Tamanho do chunk**: 40 blocos por vez
- **Overlap**: 5 blocos (para não perder repetições na fronteira)
- **Resolução de conflitos no overlap**: prevalece a decisão da janela onde o bloco
  estava mais centralizado (ou seja, a segunda janela que o analisa)

### Prompt para o LLM

Para cada chunk, envie os blocos ao LLM com o seguinte prompt. Leia o arquivo
`references/prompt_guide.md` para o prompt completo e detalhado.

O LLM deve retornar, para cada bloco, um veredito:
- `"keep"` — trecho bom, manter no vídeo
- `"cut"` — trecho ruim (erro, repetição, falso início), remover

### Regras de Decisão

1. **Repetições consecutivas**: quando duas ou mais frases consecutivas são muito similares,
   manter apenas a ÚLTIMA (a versão mais completa/correta). Marcar as anteriores como `"cut"`.
2. **Falsos inícios**: frases curtas e incompletas seguidas de uma versão completa da mesma
   ideia → marcar o falso início como `"cut"`.
3. **Gaguejos e hesitações**: blocos com muitas hesitações ("éh", "hm", "tipo assim") que
   são seguidos de uma versão limpa → marcar como `"cut"`.
4. **Trechos normais**: fala fluente sem repetição → `"keep"`.

## Etapa 4 — Montagem do JSON Final

Execute o script `scripts/merge_cuts.py` para consolidar os resultados de todos os chunks
e gerar o JSON final.

```bash
python scripts/merge_cuts.py <diretorio_dos_resultados_dos_chunks>
```

O JSON final contém os trechos a serem **mantidos** no vídeo (os trechos bons):

```json
[
  {"start": 7.66, "end": 16.88},
  {"start": 20.88, "end": 30.74},
  {"start": 41.92, "end": 57.82}
]
```

### Regras de Merge

1. Blocos consecutivos marcados como `"keep"` são fundidos em um único segmento contínuo.
2. Silêncios > 1.0s entre dois blocos `"keep"` quebram o segmento (removem o silêncio
   excessivo, mantendo ~0.3s de margem para transição natural).
3. Os timestamps do JSON final usam segundos com decimais (float), não o formato HH:MM:SS.
4. O último tempo do JSON que será retornado (tempo final do último trecho válido) deve receber 2 segundos de acréscimo para não ter um fim abrupto no vídeo.

## Fluxo Completo (passo a passo)

1. Receba o arquivo .srt do usuário
2. Execute `parse_srt.py` para extrair os blocos
3. Divida os blocos em chunks de 40 com overlap de 5
4. Para cada chunk, monte o prompt (veja `references/prompt_guide.md`) e envie ao LLM
5. Colete os vereditos de cada chunk
6. Resolva conflitos no overlap (prevalece a segunda janela)
7. Execute `merge_cuts.py` para gerar o JSON final
8. Retorne o JSON ao usuário

## Notas Importantes

- O SRT é gerado pelo Whisper, então os timestamps são confiáveis.
- O idioma é sempre PT-BR.
- O contexto é de vídeos educativos sobre IA (canal do YouTube).
- O apresentador é sempre a mesma pessoa (uma única voz).
- Erros de fala seguem um padrão previsível: erro → pausa curta → repetição corrigida.
- Em caso de dúvida, prefira NÃO cortar (é melhor manter algo duvidoso do que cortar
  conteúdo bom).
