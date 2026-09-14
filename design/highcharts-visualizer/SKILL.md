---
name: highcharts-visualizer
description: >
  Cria visualizações de dados interativas e profissionais usando Highcharts.js, gerando
  HTML standalone com gráficos animados, responsivos e acessíveis. Use este skill sempre que
  o usuário pedir para criar gráficos, charts, dashboards, visualizações de dados, ou qualquer
  representação visual de dados numéricos/categóricos. Deve ser usado quando o usuário mencionar
  termos como "gráfico", "chart", "dashboard", "highcharts", "visualização de dados",
  "gráfico de linhas", "barras", "pizza", "scatter", "heatmap", "treemap", "gauge", "stock chart",
  "mapa", "gantt", "sankey", "funnel", ou quando fornecer dados (CSV, JSON, tabela, planilha)
  pedindo representação visual. Também deve ser ativado quando o usuário pedir gráficos bonitos,
  interativos, animados, com tooltip, drill-down, ou exportáveis. Funciona com dados inline,
  CSV, JSON, e arquivos de dados. Sempre gera HTML standalone completo e funcional.
---

# Highcharts Visualizer

Cria visualizações de dados profissionais usando Highcharts.js. Gera sempre **HTML standalone**
(arquivo único, self-contained) com gráficos interativos, animados, responsivos e acessíveis.

## Fluxo de Trabalho

### 1. Receber os Dados

Os dados podem vir de:

- **Inline na conversa** → Usuário cola dados, tabela, lista de valores
- **CSV/JSON enviado** → Analise o conteúdo usando `view_file` e injete os dados diretamente no HTML gerado. Nunca crie scripts em Python.
- **Planilha Excel** → Extraia os dados das tabelas e injete-os no HTML. Não use Python.
- **Dados de exemplo** → Quando o usuário quer explorar um tipo de gráfico sem dados reais
- **URL de dados** → Usar `web_fetch` para buscar dados remotos

### 2. Analisar os Dados

Antes de gerar o gráfico, entender a natureza dos dados:

- **Dimensões**: quantas séries? Quantas categorias? Temporal ou categórico?
- **Escala**: range dos valores, outliers, distribuição
- **Relações**: comparação, composição, distribuição, tendência, correlação
- **Volume**: poucos pontos (<100), médio (100-10K), grande (>10K — usar boost module)

Analise os dados internamente após a leitura e injete as tags via string. Não crie programas Python intermediários.

### 3. Escolher o Tipo de Gráfico

Consultar `references/CHART_CATALOG.md` para o catálogo completo de 40+ tipos de gráfico,
com orientação de quando usar cada um.

**Regra de decisão rápida:**

| Objetivo | Tipos recomendados |
|----------|-------------------|
| Tendência ao longo do tempo | line, area, spline, areaspline |
| Comparação entre categorias | column, bar, lollipop, bullet |
| Composição / proporção | pie, donut, stacked column, stacked area, treemap, sunburst |
| Distribuição | histogram, box plot, scatter, bell curve |
| Correlação | scatter, bubble, heatmap |
| Fluxo / processo | sankey, dependency wheel, network graph |
| Hierarquia | treemap, sunburst, organization chart |
| Geográfico | map (Highcharts Maps module) |
| Financeiro / timeline | stock chart (candlestick, OHLC, flags) |
| Progresso / KPI | gauge, solid gauge, activity gauge |
| Projeto / planejamento | gantt chart |
| Funil / conversão | funnel, pyramid |

Se o usuário não especificou o tipo, sugerir 2-3 opções que melhor representam os dados.

### 4. Gerar o Código

Consultar `references/HIGHCHARTS_PATTERNS.md` para padrões de código testados.

**Regras fundamentais:**

1. **HTML standalone** — Arquivo único `.html` com Highcharts via CDN
2. **CDN versão estável** — Usar `https://code.highcharts.com/highcharts.js` (core)
3. **Módulos por demanda** — Só incluir scripts extras quando necessário (ver tabela de módulos)
4. **Accessibility sempre** — Sempre incluir `modules/accessibility.js`
5. **Exporting sempre** — Sempre incluir `modules/exporting.js` + `modules/export-data.js`
6. **Responsivo** — O gráfico deve se adaptar ao container/viewport
7. **Tema consistente** — Aplicar cores coesas e tipografia profissional
8. **Animação** — Habilitar animações de entrada e transições suaves
9. **Tooltips ricos** — Tooltips formatados, com unidades e contexto
10. **Dados grandes** — Para >10K pontos, incluir `modules/boost.js`

**Módulos CDN necessários por tipo de gráfico:**

| Recurso | Script CDN |
|---------|-----------|
| Core (obrigatório) | `highcharts.js` |
| Accessibility (obrigatório) | `modules/accessibility.js` |
| Exporting (obrigatório) | `modules/exporting.js` |
| Export Data | `modules/export-data.js` |
| Tipos avançados (gauge, polar, etc.) | `highcharts-more.js` |
| 3D | `highcharts-3d.js` |
| Solid Gauge | `modules/solid-gauge.js` |
| Treemap | `modules/treemap.js` |
| Sunburst | `modules/sunburst.js` |
| Sankey | `modules/sankey.js` |
| Heatmap | `modules/heatmap.js` |
| Funnel | `modules/funnel.js` |
| Dependency Wheel | `modules/dependency-wheel.js` |
| Network Graph | `modules/networkgraph.js` |
| Organization | `modules/organization.js` |
| Histogram/Bellcurve | `modules/histogram-bellcurve.js` |
| Bullet | `modules/bullet.js` |
| Timeline | `modules/timeline.js` |
| Wordcloud | `modules/wordcloud.js` |
| Venn | `modules/venn.js` |
| Drilldown | `modules/drilldown.js` |
| Annotations | `modules/annotations.js` |
| Boost (dados grandes) | `modules/boost.js` |
| Offline Exporting | `modules/offline-exporting.js` |
| Stock (candlestick, OHLC) | `/stock/highstock.js` (substitui highcharts.js) |
| Maps | `/maps/highmaps.js` (substitui highcharts.js) |
| Gantt | `/gantt/highcharts-gantt.js` (substitui highcharts.js) |

Todos os CDN no formato: `https://code.highcharts.com/{path}`

### 5. Salvar e Entregar

Salvar o HTML gerado diretamente na pasta de destino usando `write_to_file`. Sempre gere o arquivo HTML puro com todos os dados processados e injetados nas variáveis `<script>`. Não use trechos de Python.

## Diretrizes de Qualidade

- **Estética profissional**: cores coesas (usar paletas Highcharts ou custom), tipografia limpa, espaçamentos adequados
- **Dados formatados**: números com separadores de milhar, datas localizadas, unidades nos eixos
- **Legendas claras**: nomes de séries descritivos, posição que não obstrui os dados
- **Interatividade rica**: hover highlights, tooltips contextuais, zoom quando aplicável
- **Dark mode**: quando apropriado, oferecer versão dark com `backgroundColor: '#1a1a2e'`
- **Múltiplos gráficos**: para dashboards, organizar em grid CSS responsivo
- **Código comentado**: comentários em português explicando cada seção

## Tratamento de Erros

Consultar `references/ERRORS.md` para cenários de erro e soluções.
