---
title: Anatomy of an Agent Skill
language: en
translation_key: skill-anatomy
translation_status: complete
---

# Anatomy of an Agent Skill

A Skill requires a `SKILL.md` file. It may also include scripts, references and assets.

```text
skill-name/
├── SKILL.md
├── scripts/
├── references/
└── assets/
```

## Required metadata

The YAML front matter should contain at least:

```yaml
---
name: skill-name
description: What the skill does and when it should be used.
---
```

## Progressive disclosure

1. The name and description support discovery.
2. The `SKILL.md` body supplies the core workflow.
3. Bundled resources are loaded or executed only when required.

## Catalog evidence

The Observatory additionally records source provenance, version evidence, license information, category, capabilities and verification date.
