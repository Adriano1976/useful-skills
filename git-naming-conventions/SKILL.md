---
name: git-naming-conventions
description: Diretrizes para nomeação estrita de branches, commits e Pull Requests usando o padrão Conventional Commits e Git Flow.
---

# Convenção de Nomenclatura para Git (Branches, Commits e PRs)

Esta habilidade instrui a IA a gerar, revisar ou validar nomes de branches, mensagens de commit e títulos de Pull Requests seguindo as boas práticas do setor.

## Nomenclaturas Principais (Core)

Sempre priorize estes quatro prefixos para as tarefas mais comuns:

* **`feat/`**: Nova funcionalidade ou recurso para o usuário.
  * *Exemplo:* `feat/login-social`
* **`fix/`**: Correção de bug ou comportamento inesperado em código existente.
  * *Exemplo:* `fix/overflow-calculo`
* **`refactor/`**: Mudança no código que não altera o comportamento externo nem corrige bugs (melhoria de arquitetura, clareza ou estrutura).
  * *Exemplo:* `refactor/auth-middleware`
* **`chore/`**: Tarefas de manutenção, atualização de dependências ou configurações de infraestrutura que não alteram o código de produção.
  * *Exemplo:* `chore/atualiza-deps`

---

## Nomenclaturas Secundárias e Especializadas

Utilize estas opções quando a tarefa for específica:

* **`docs/`**: Alterações exclusivamente em documentações (ex: `README.md`, Swagger, manuais).
  * *Exemplo:* `docs/api-endpoints`
* **`style/`**: Ajustes de formatação de código (lint, espaços, ponto e vírgula) ou alterações puramente visuais de UI/CSS que não alteram regras de negócio.
  * *Exemplo:* `style/dark-mode-colors`
* **`test/`**: Adição, remoção ou ajuste de testes automatizados (unitários, integração ou E2E).
  * *Exemplo:* `test/login-unit`
* **`perf/`**: Mudanças focadas especificamente em otimização de desempenho e performance de execução.
  * *Exemplo:* `perf/otimiza-query`
* **`build/`**: Alterações que afetam o sistema de build, empacotamento ou dependências de compilação.
  * *Exemplo:* `build/webpack-config`
* **`ci/`**: Alterações em pipelines de Integração/Entrega Contínua (GitHub Actions, GitLab CI, etc.).
  * *Exemplo:* `ci/github-actions`
* **`revert/`**: Reversão de um commit ou funcionalidade anterior.
  * *Exemplo:* `revert/feat-login`
* **`hotfix/`**: Correção crítica e urgente aplicada diretamente para o ambiente de produção.
  * *Exemplo:* `hotfix/corrigi-vazamento-memoria`

---

## Regras de Formatação

1. **Estrutura do Nome**: `<prefixo>/<descricao-kebab-case>`
2. **Letras Minúsculas**: Use sempre caracteres minúsculos no prefixo e na descrição.
3. **Kebab-case**: Separe palavras por hífens (`-`), sem espaços ou caracteres especiais/acentos.
4. **Verbo no Presente ou Substantivo Claro**: Descreva de forma concisa o objetivo principal da alteração.