# Entrega 10 — Portal Inicial Integrado

## Conteúdo

- portal MkDocs Material responsivo;
- landing page bilíngue;
- dashboard executivo em JavaScript puro;
- catálogo interativo de Skills;
- integração da Entrega 08 — Benchmarks;
- integração da Entrega 09 — Catálogo de Skills;
- modo claro e escuro;
- diagramas Mermaid;
- GitHub Actions para qualidade e GitHub Pages;
- documentação em inglês e português;
- scripts sem backend e sem serviços pagos.

## Testes

```bash
python scripts/catalog/validate_skills.py
python scripts/benchmark/validate_results.py
python scripts/benchmark/generate_rankings.py
python scripts/benchmark/export_dashboard_data.py
python scripts/portal/build_portal_data.py
mkdocs build --strict
```

## Publicação

No GitHub, abra **Settings → Pages** e selecione **GitHub Actions** como fonte. Em seguida, envie os arquivos para a branch `main`.

## Observação

Os dados de benchmark incluídos permanecem sintéticos e servem exclusivamente para validar o pipeline e o dashboard.
