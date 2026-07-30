# Claude Skills Observatory

Open-source technical observatory for Claude Skills, MCP servers, APIs, prompts, benchmarks, papers, datasets and practical AI documentation.

## Entrega 10

This repository package integrates:

- a responsive MkDocs Material portal;
- an executive dashboard built with vanilla JavaScript;
- a searchable Skills catalog;
- the validated Skills catalog from Entrega 09;
- the reproducible benchmark system from Entrega 08;
- English and Portuguese entry points;
- GitHub Actions for validation and GitHub Pages deployment.

## Local development

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
mkdocs serve
```

Open `http://127.0.0.1:8000`.

## Validation

```bash
python scripts/catalog/validate_skills.py
python scripts/benchmark/validate_results.py
python scripts/portal/build_portal_data.py
mkdocs build --strict
```

## Deployment

Push the repository to GitHub and set **Settings → Pages → Source** to **GitHub Actions**. The workflow in `.github/workflows/deploy.yml` builds and publishes the portal.

## Stack

Only free and open-source technologies are used:

- GitHub and GitHub Pages;
- MkDocs Material;
- Markdown and Mermaid;
- Python;
- HTML5, CSS3 and JavaScript;
- GitHub Actions.

## License

The portal code and original documentation are released under the MIT License. Third-party catalog entries remain subject to their upstream licenses and terms.

## Author

Ramon Ribeiro Fontes
