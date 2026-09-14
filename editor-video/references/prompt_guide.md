# Guia de Prompt para Análise de Blocos SRT

Este documento contém o prompt template que deve ser enviado ao LLM para cada chunk
de blocos do SRT.

## Prompt Template

```
Você é um editor de vídeo especializado em análise de legendas. Sua tarefa é analisar
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
   - Exemplo:
     Bloco 14: "Então o que a gente precisa fazer é configurar o banco"  → cut
     Bloco 15: "Então o que a gente precisa fazer é configurar o banco de dados" → keep

2. FALSOS INÍCIOS:
   - Frases curtas e incompletas seguidas de uma versão completa → cortar o início falso.
   - Exemplo:
     Bloco 20: "E aí a gente..."  → cut
     Bloco 21: "E aí a gente vai precisar instalar o Docker primeiro" → keep

3. GAGUEJOS E HESITAÇÕES:
   - Blocos que são predominantemente hesitações ("éh", "hm", "tipo assim", "é...")
     seguidos de fala clara → cortar as hesitações.
   - MAS: hesitações breves dentro de uma frase normal NÃO devem ser cortadas.

4. FALA NORMAL:
   - Frases fluentes que avançam o conteúdo → sempre manter ("keep").
   - Na dúvida, mantenha. É melhor preservar algo duvidoso do que perder conteúdo bom.

5. MÚLTIPLAS TENTATIVAS:
   - Se o apresentador tenta a mesma frase 3 ou mais vezes, mantenha APENAS a última.
   - Todas as tentativas anteriores são "cut".

## Formato de Resposta

Responda APENAS com um JSON válido, sem nenhum texto adicional, sem markdown backticks.
O JSON deve ser um array de objetos, um para cada bloco, na mesma ordem em que foram
apresentados:

[
  {"index": <número_do_bloco>, "verdict": "keep"|"cut", "reason": "<motivo breve>"},
  ...
]

O campo "reason" deve ser breve (máx 10 palavras). Exemplos:
- "fala normal, conteúdo avança"
- "repetição - versão anterior da frase seguinte"
- "falso início"
- "hesitação sem conteúdo"
- "versão final corrigida"

## Blocos para Análise

{blocks_json}
```

## Como Montar o Prompt

Para cada chunk de blocos, substitua `{blocks_json}` por um JSON array dos blocos
no formato:

```json
[
  {"index": 14, "start": 45.2, "end": 48.7, "text": "Então o que a gente precisa..."},
  {"index": 15, "start": 49.1, "end": 53.4, "text": "Então o que a gente precisa fazer..."}
]
```

## Parsing da Resposta

A resposta do LLM deve ser parseada como JSON. Caso venha com backticks markdown
(```json ... ```), remova-os antes de parsear.

Se o parse falhar, tente novamente com o mesmo chunk (máx 2 retentativas).

## Parâmetros Recomendados para a API

- **model**: claude-sonnet-4-20250514 (bom equilíbrio custo/qualidade para esta tarefa)
- **max_tokens**: 4096 (suficiente para ~40 blocos)
- **temperature**: 0 (queremos respostas determinísticas)
