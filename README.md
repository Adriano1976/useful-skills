# useful-skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Coleção abrangente de skills para agentes Claude/Anthropic, projetadas para automatizar fluxos de trabalho de engenharia, criação de conteúdo, marketing e design.

## Visão Geral

O **useful-skills** é um repositório de skills modulares para agentes de IA (especificamente Claude/Anthropic) que cobrem diversas áreas do desenvolvimento de software e criação de conteúdo. Cada skill é um guia especializado com instruções detalhadas, scripts auxiliares e referências para executar tarefas específicas de forma autônoma e eficiente.

### Por que usar?

- **Automação inteligente**: Skills que entendem contexto e executam fluxos completos
- **Modularidade**: Cada skill é independente e pode ser usada separadamente
- **Padronizado**: Estrutura consistente com `SKILL.md`, scripts e referências
- **Foco em produtividade**: Reduz tempo de tarefas repetitivas e complexas

---

## Technology Stack

| Componente | Tecnologia |
|------------|------------|
| **Plataforma** | Claude/Anthropic Agents |
| **Formato** | Markdown (SKILL.md) |
| **Scripts** | Python 3.x |
| **Visualização** | Mermaid.js, D3.js, Highcharts.js |
| **Templates** | HTML/Tailwind CSS |
| **Versionamento** | Git |
| **Empacotamento** | .skill (formato nativo) |

---

## Project Architecture

```
useful-skills/
├── 📁 academic/                    # Skills acadêmicas
│   ├── academic-paper-summarizer/  # Resumo de papers
│   └── escritor-academico/         # Escritor LaTeX
│
├── 📁 apresentacao-cards/          # Apresentações HTML em cards
│
├── 📁 design/                      # Skills de design e visualização
│   ├── d3-image-animator/          # Animações D3.js
│   ├── especialista-d3/            # Especialista D3.js
│   ├── highcharts-visualizer/      # Gráficos Highcharts
│   └── image-prompt-json/          # Prompts para geração de imagens
│
├── 📁 design-system/               # Extração de Design System
│
├── 📁 editor-video/                # Edição de vídeo via SRT
│
├── 📁 escritor-linkedin/           # Escritor de conteúdo LinkedIn
│
├── 📁 escritor-medium/             # Escritor de artigos Medium
│
├── 📁 files/                       # Arquivos auxiliares
│
├── 📁 find-skills/                 # Descobrir e instalar skills
│
├── 📁 gerador-slides/              # Geração de apresentações
│
├── 📁 git-naming-conventions/      # Convenções de nomenclatura Git
│
├── 📁 marketing/                   # 26 skills de marketing
│   ├── copywriting/
│   ├── seo-audit/
│   ├── email-sequence/
│   ├── paid-ads/
│   └── ... (26 subdiretórios)
│
├── 📁 paper-extrator/              # Extração de papers arXiv
│
├── 📁 prd-manager/                 # Gerenciamento de PRD
│
├── 📁 python-docstring-generator/  # Geração de docstrings Python
│
├── 📁 readme-blueprint-generator/  # Geração de README
│
├── 📁 reversa-bubble-graph/        # Gráficos de bolhas arquiteturais
│
├── 📁 revisor-gramatical/          # Revisão gramatical PT-BR
│
├── 📁 sandeco-maestro/             # Orquestração multi-agente
│
├── 📁 sdd-spec/                    # Spec-Driven Development
│
├── 📁 security-code-audit/         # Auditoria de segurança
│
├── 📁 skill-creator/               # Criação e melhoria de skills
│
├── 📁 skill-injection-auditor/     # Auditoria de segurança de skills
│
├── 📁 skill-lister/                # Listar skills disponíveis
│
├── 📁 software-architecture/       # Arquitetura de software
│
├── 📁 superpowers/                 # 13 skills de desenvolvimento
│   ├── dispatching-parallel-agents/
│   ├── executing-plans/
│   ├── finishing-a-development-branch/
│   ├── receiving-code-review/
│   ├── requesting-code-review/
│   ├── subagent-driven-development/
│   ├── systematic-debugging/
│   ├── test-driven-development/
│   ├── using-git-worktrees/
│   ├── using-superpowers/
│   ├── verification-before-completion/
│   ├── writing-plans/
│   └── writing-skills/
│
├── 📁 youtube-creative/            # 6 skills criativas YouTube
│   ├── storytelling-roteiro/
│   ├── youtube-ganchos/
│   ├── youtube-pesquisa/
│   ├── youtube-roteiro/
│   ├── youtube-step-extractor/
│   └── youtube-thumbnail-downloader/
│
├── 📁 youtube-optimization-skills/ # 4 skills de otimização YouTube
│   ├── youtube-descricoes/
│   ├── youtube-manager/
│   ├── youtube-tags/
│   └── youtube-titulos/
│
├── LICENSE
└── README.md
```

---

## Getting Started

### Pré-requisitos

- **Claude/Anthropic Agent** (Claude Code, Claude.ai, ou ambiente similar)
- **Python 3.8+** (para scripts auxiliares)
- **Git** (para versionamento)

### Instalação

1. **Clonar o repositório:**
   ```bash
   git clone https://github.com/Adriano1976/useful-skills.git
   cd useful-skills
   ```

2. **Instalar skills globalmente (opcional):**
   ```bash
   npx skills add Adriano1976/useful-skills@skill-name -g -y
   ```

3. **Ou copiar skills manualmente:**
   - Copie a pasta desejada para `~/.claude/skills/` ou `~/.agents/skills/`

### Uso Básico

As skills são ativadas automaticamente pelo agente Claude quando detectam palavras-chave relevantes. Por exemplo:

- `escritor-linkedin` → Ativada ao pedir para escrever posts para LinkedIn
- `security-code-audit` → Ativada ao pedir auditoria de segurança
- `skill-creator` → Ativada ao querer criar ou melhorar uma skill

---

## Key Features

### 🛠️ Skills de Engenharia

| Skill | Descrição |
|-------|-----------|
| `software-architecture` | Cria, avalia e moderniza arquiteturas de software |
| `security-code-audit` | Audita código em 5 categorias de vulnerabilidade |
| `sdd-spec` | Desenvolvimento orientado a especificações |
| `prd-manager` | Gerencia Product Requirements Documents |
| `git-naming-conventions` | Convenções de nomenclatura para Git |

### 🔧 Superpowers (13 skills)

| Skill | Descrição |
|-------|-----------|
| `test-driven-development` | TDD com ciclo Red-Green-Refactor |
| `systematic-debugging` | Debugging sistemático com 4 fases |
| `subagent-driven-development` | Execução com sub-agentes |
| `writing-plans` | Criação de planos de implementação |
| `using-git-worktrees` | Worktrees isolados |
| `verification-before-completion` | Verificação antes de completar |
| `requesting-code-review` | Solicitação de code review |
| `receiving-code-review` | Recebimento de feedback |
| `finishing-a-development-branch` | Finalização de branches |
| `executing-plans` | Execução de planos |
| `dispatching-parallel-agents` | Agentes paralelos |
| `using-superpowers` | Ativação de skills |
| `writing-skills` | Criação de skills |

### 📝 Skills de Conteúdo

| Skill | Descrição |
|-------|-----------|
| `escritor-linkedin` | Posts otimizados para LinkedIn |
| `escritor-medium` | Artigos para Medium |
| `revisor-gramatical` | Revisão gramatical PT-BR |
| `python-docstring-generator` | Docstrings no padrão Google |
| `prd-manager` | Criação e análise de PRDs |

### 🎬 YouTube (10 skills)

| Skill | Descrição |
|-------|-----------|
| `youtube-manager` | Orquestrador mestre |
| `youtube-titulos` | Títulos otimizados |
| `youtube-descricoes` | Descrições com hooks |
| `youtube-tags` | Tags SEO |
| `youtube-roteiro` | Roteiros para gravação |
| `youtube-ganchos` | Ganchos de 30 segundos |
| `editor-video` | Edição via legendas SRT |

### 🎨 Design (7 skills)

| Skill | Descrição |
|-------|-----------|
| `design-system` | Extração de Design System |
| `highcharts-visualizer` | Gráficos interativos |
| `d3-image-animator` | Animações D3.js |
| `apresentacao-cards` | Apresentações HTML |
| `gerador-slides` | Roteiros de slides |

### 📈 Marketing (26 skills)

| Categoria | Exemplos |
|-----------|----------|
| **Copywriting** | `copywriting`, `copy-editing` |
| **SEO** | `seo-audit`, `programmatic-seo` |
| **CRO** | `page-cro`, `signup-flow-cro`, `popup-cro` |
| **Email** | `email-sequence` |
| **Ads** | `paid-ads` |
| ** Conteúdo** | `social-content`, `content-strategy` |

---

## Project Structure

### Padronização de Skills

Cada skill segue esta estrutura:

```
skill-name/
├── SKILL.md              # Arquivo principal (obrigatório)
│   ├── YAML frontmatter  # name, description
│   └── Instruções        # Fluxo de trabalho detalhado
│
├── references/           # Documentação de referência (opcional)
│   ├── api-core.md
│   └── patterns.md
│
├── scripts/              # Scripts executáveis (opcional)
│   ├── helper.py
│   └── process.sh
│
└── assets/               # Templates e recursos (opcional)
    ├── template.html
    └── schema.json
```

### Formato do SKILL.md

```markdown
---
name: skill-name
description: >
  Descrição de quando ativar esta skill.
  Use palavras-chave que o agente pode detectar.
---

# Nome da Skill

## Visão Geral
Descrição breve do propósito.

## Quando Usar
- Caso de uso 1
- Caso de uso 2

## Fluxo de Trabalho
1. Passo 1
2. Passo 2

## Exemplos
Código ou exemplos práticos.
```

---

## Development Workflow

### Criando uma Nova Skill

1. **Use o `skill-creator`** para guiar o processo:
   ```
   "Quero criar uma skill para [descrever o objetivo]"
   ```

2. **Siga o ciclo TDD:**
   - **RED**: Teste sem a skill (baseline)
   - **GREEN**: Escreva a skill
   - **REFACTOR**: Feche lacunas

3. **Teste com cenários de pressão:**
   - Questões acadêmicas
   - Cenários com pressão de tempo
   - Combinações de pressões

4. **Valide antes de implantar:**
   ```bash
   python scripts/spec_scorer.py --spec caminho/para/spec.md
   ```

### Melhorando Skills Existentes

1. **Analise o comportamento atual:**
   - Execute a skill sem alterações
   - Documente falhas e racionalizações

2. **Identifique padrões:**
   - Quais pressões causam violações?
   - Quais racionalizações são usadas?

3. **Implemente melhorias:**
   - Adicione contadores explícitos
   - Feche lacunas identificadas

4. **Re-teste:**
   - Execute os mesmos cenários
   - Verifique conformidade

---

## Coding Standards

### Convenções de Nomenclatura

| Tipo | Formato | Exemplo |
|------|---------|---------|
| **Branches** | `prefixo/descricao-kebab-case` | `feat/login-social` |
| **Commits** | Conventional Commits | `feat(auth): implement JWT` |
| **PRs** | Título descritivo | `feat: Add user authentication` |

### Prefixos de Branch

| Prefixo | Uso |
|---------|-----|
| `feat/` | Nova funcionalidade |
| `fix/` | Correção de bug |
| `refactor/` | Refatoração |
| `chore/` | Manutenção |
| `docs/` | Documentação |
| `test/` | Testes |
| `perf/` | Performance |
| `ci/` | CI/CD |

### Formatação

- **Markdown**: Use formatação padrão GitHub
- **Código**: Siga o padrão da linguagem (PEP 8 para Python, etc.)
- **Comentários**: Em português quando aplicável
- **Links**: Use referências relativas quando possível

---

## Testing

### Estratégia de Teste

1. **Testes de Unidade:**
   - Cada skill deve ter testes que verifiquem comportamento esperado
   - Use scripts Python para testes automatizados

2. **Testes de Integração:**
   - Teste skills em conjunto quando aplicável
   - Verifique fluxos completos

3. **Testes de Pressão:**
   - Cenários com múltiplas pressões
   - Verifique resistência a racionalizações

### Comandos de Teste

```bash
# Testar uma skill específica
python scripts/test_skill.py --skill skill-name

# Executar todos os testes
python -m pytest tests/

# Verificar cobertura
python -m pytest --cov=skills tests/
```

### Estrutura de Testes

```
tests/
├── test_skill_name/
│   ├── test_basic.py
│   ├── test_edge_cases.py
│   └── test_pressure.py
└── conftest.py
```

---

## Contributing

### Diretrizes

1. ** Leia o `skill-creator`** antes de contribuir
2. **Siga o padrão TDD**: Teste antes de implementar
3. **Mantenha consistência**: Use a estrutura padrão
4. **Documente**: Explique o porquê das mudanças
5. **Teste**: Valide antes de submeter

### Processo

1. Fork o repositório
2. Crie uma branch (`git checkout -b feat/nova-skill`)
3. Implemente suas mudanças
4. Adicione testes
5. Execute os testes
6. Faça commit (`git commit -m 'feat: add nova-skill'`)
7. Push para a branch (`git push origin feat/nova-skill`)
8. Abra um Pull Request

### Checklist de PR

- [ ] Skill segue a estrutura padrão
- [ ] `SKILL.md` tem frontmatter completo
- [ ] Testes passam
- [ ] Documentação atualizada
- [ ] Não quebra skills existentes
- [ ] Scripts são executáveis
- [ ] Referências estão corretas

---

## Skills em Destaque

### 🔐 Security Code Audit

Audita projetos em 5 categorias de vulnerabilidade:
1. Isolamento de dados ausente (RLS)
2. Permissão validada só no frontend
3. IDOR (Insecure Direct Object Reference)
4. Chaves/segredos expostos
5. Inputs sem tratamento (XSS)

**Gera:** Relatório PDF/Markdown + issues GitHub prontas

### 🏗️ Software Architecture

Quatro modos de operação:
- **CRIAR**: Projetar arquitetura do zero
- **AVALIAR**: Analisar arquitetura existente
- **UPGRADE**: Propor modernização
- **EXTRAIR**: Gerar `architecture.md` a partir de specs

**Entrega:** Diagramas Mermaid renderizáveis

### 📝 PRD Manager

Gerencia Product Requirements Documents:
- **CRIAR**: Gerar PRD completo
- **ANALISAR**: Avaliar PRD existente
- **MELHORAR**: Reescrever seções fracas
- **DESCOBERTA**: Extrair requisitos

**Template:** 10 seções estruturadas

### 🎯 Spec-Driven Development (SDD)

Metodologia completa:
1. **Entrevista Estruturada**: Extrair contexto
2. **Redigir Spec**: Usar template padrão
3. **Avaliação Automática**: Score 0-100
4. **Iteração**: Melhorar até ≥80 pontos

**Entrega:** Spec completa + relatório de avaliação

---

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

```
MIT License

Copyright (c) 2026 Adriano Santos

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Contato

**Adriano Santos**
- GitHub: [@Adriano1976](https://github.com/Adriano1976)
- Especialidades: IA, Ciência de Dados, Engenharia de Software

---

<div align="center">

**Feito com ❤️ para a comunidade de agentes Claude**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Adriano1976)

</div>

##
 
<br><br>

<div align="center">
  <p><b><h3> Contagem de visitantes </h3></b></p>  
  <img src="https://vbr.nathanchung.dev/badge?page_id=Adriano1976/useful-skills" style="height: 30px;" />
   <br>
  <img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=87CEFA&height=120&section=footer"/>
</div>
