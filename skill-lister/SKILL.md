---
name: skill-lister
description: Skill responsável por listar todas as outras skills disponíveis no projeto. Use-a quando o usuário perguntar "quais skills você tem?" ou "o que você pode fazer?".
---

# Skill: Skill Lister

Esta skill permite ao agente descobrir dinamicamente quais ferramentas (skills) estão instaladas no projeto SandecoClaw.

## Como usar
Quando ativada, o agente deve:
1. Ler o diretório `.agents/skills/`.
2. Identificar subpastas que contenham um arquivo `SKILL.md`.
3. Extrair o nome e a descrição de cada skill.
4. Apresentar uma lista formatada para o usuário.

## Regras
- Sempre liste o nome exato da skill e seu propósito.
- Se houver sub-skills (como no caso de `superpowers` ou `youtube-optimization-skills`), liste-as de forma hierárquica.
- Nunca invente skills que não foram encontradas no diretório.
