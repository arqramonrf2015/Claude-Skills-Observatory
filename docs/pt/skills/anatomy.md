---
title: Anatomia de uma Agent Skill
language: pt
translation_key: skill-anatomy
translation_status: complete
---

# Anatomia de uma Agent Skill

Uma Skill requer um arquivo `SKILL.md`. Ela também pode incluir scripts, referências e recursos visuais.

```text
nome-da-skill/
├── SKILL.md
├── scripts/
├── references/
└── assets/
```

## Metadados obrigatórios

O front matter YAML deve conter pelo menos:

```yaml
---
name: nome-da-skill
description: O que a Skill faz e quando deve ser utilizada.
---
```

## Divulgação progressiva

1. Nome e descrição permitem a descoberta.
2. O corpo do `SKILL.md` fornece o fluxo principal.
3. Recursos adicionais são carregados ou executados somente quando necessários.

## Evidências do catálogo

O Observatório também registra procedência, versão verificada, licença, categoria, capacidades e data de verificação.
