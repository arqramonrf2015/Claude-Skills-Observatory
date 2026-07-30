# Release Candidate v0.1.0

## Objetivo

Primeira versão pública funcional do Claude Skills Observatory.

## Incluído

- portal MkDocs Material;
- documentação bilíngue inicial;
- catálogo estruturado de Claude Skills;
- arquitetura reproduzível de benchmarks;
- dashboards estáticos;
- busca;
- modo claro e escuro;
- publicação pelo GitHub Pages;
- automações de validação;
- scripts para publicação, auditoria e preview local.

## Critérios de aceite

- [ ] `python scripts/qa/audit_project.py` conclui sem erros.
- [ ] `mkdocs build --strict` conclui sem erros.
- [ ] A página inicial abre no desktop e no smartphone.
- [ ] Busca retorna páginas do catálogo.
- [ ] Alternância de tema funciona.
- [ ] Links internos não apresentam erro 404.
- [ ] Workflow de Pages fica verde.
- [ ] Dados sintéticos permanecem claramente identificados.
- [ ] Nenhum segredo, token ou Client ID está versionado.
- [ ] Licenças e procedência dos conteúdos estão visíveis.

## Tag recomendada

```text
v0.1.0
```

## Commit recomendado

```text
release: publish Claude Skills Observatory v0.1.0
```
