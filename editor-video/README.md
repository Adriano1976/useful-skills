# SRT Video Cutter Agent 🎬✂️

Agente de edição automática de vídeo que analisa legendas SRT (geradas pelo Whisper)
para identificar e remover automaticamente erros de fala, repetições e silêncios.

## Como Funciona

```
Arquivo .srt → Parse → Chunking → Análise LLM (Claude) → JSON de cortes
```

O agente:
1. Lê o arquivo SRT e extrai blocos com timestamps
2. Detecta silêncios (gaps > 1s entre blocos)
3. Divide em chunks para processar arquivos grandes progressivamente
4. Envia cada chunk ao Claude para identificar repetições e erros de fala
5. Gera um JSON com os trechos a serem removidos

## Instalação

Não requer dependências externas além do Python 3.8+. A comunicação com a API
do Claude é feita via `urllib` (stdlib).

```bash
git clone <repo>
cd srt-video-cutter
```

## Uso

### Modo básico

```bash
export ANTHROPIC_API_KEY=sk-ant-...
python scripts/run_agent.py meu_video.srt
```

### Com parâmetros

```bash
python scripts/run_agent.py meu_video.srt \
  --api-key sk-ant-... \
  --silence-threshold 1.0 \
  --chunk-size 40 \
  --overlap 5 \
  --model claude-sonnet-4-20250514 \
  --output cortes.json \
  --verbose
```

### Dry run (sem chamar a API)

```bash
python scripts/run_agent.py meu_video.srt --dry-run
```

## Output

O agente gera 3 arquivos:

1. **`*_cuts.json`** — JSON com trechos a remover:
```json
[
  {"start": 13.52, "end": 21.26},
  {"start": 37.48, "end": 43.30}
]
```

2. **`*_report.txt`** — Relatório com estatísticas do processamento

3. **`*_verdicts.json`** — Vereditos detalhados para cada bloco (debug)

## Parâmetros

| Parâmetro | Default | Descrição |
|-----------|---------|-----------|
| `--silence-threshold` | 1.0 | Gap mínimo (segundos) para considerar silêncio |
| `--chunk-size` | 40 | Blocos por chunk na janela deslizante |
| `--overlap` | 5 | Blocos de overlap entre chunks consecutivos |
| `--model` | claude-sonnet-4-20250514 | Modelo Claude a usar |

## Estrutura do Projeto

```
srt-video-cutter/
├── SKILL.md                    # Instruções do agente (skill format)
├── README.md                   # Este arquivo
├── scripts/
│   ├── run_agent.py            # Orquestrador principal
│   ├── parse_srt.py            # Parser de arquivos SRT
│   └── merge_cuts.py           # Merge de resultados e geração do JSON final
├── references/
│   └── prompt_guide.md         # Template do prompt para o LLM
└── tests/
    └── sample.srt              # SRT de exemplo para testes
```

## Custo Estimado por Vídeo

Para um vídeo de ~30 min com ~300 blocos SRT:
- ~8 chunks de 40 blocos
- ~8 chamadas à API Claude Sonnet
- Custo estimado: ~$0.05-0.10 USD por vídeo

## Integração com seu Código de Corte

O JSON gerado é compatível diretamente com seu código existente:

```python
import json

with open("meu_video_cuts.json") as f:
    cuts = json.load(f)

# cuts = [{"start": 13.52, "end": 21.26}, ...]
# Passe para seu código de corte FFmpeg
```
