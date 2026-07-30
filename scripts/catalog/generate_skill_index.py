from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/skills/skills.json"
EN_OUTPUT = ROOT / "docs/en/skills/catalog.md"
PT_OUTPUT = ROOT / "docs/pt/skills/catalog.md"
DASHBOARD_OUTPUT = ROOT / "dashboards/skills/data/skills-catalog.json"


def load() -> dict:
    with SOURCE.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def table_rows(skills: list[dict], language: str) -> list[str]:
    summary_key = f"summary_{language}"
    rows = []
    for skill in sorted(skills, key=lambda item: (item["category"], item["display_name"].lower())):
        rows.append(
            f'| `{skill["name"]}` | {skill["display_name"]} | {skill["category"]} | '
            f'{skill["origin"]} | {skill["status"]} | {skill[summary_key]} | '
            f'[Source]({skill["source_url"]}) |'
        )
    return rows


def build_en(document: dict) -> str:
    skills = document["skills"]
    categories = Counter(skill["category"] for skill in skills)
    lines = [
        "---", "title: Skills Catalog", "language: en",
        "translation_key: skills-catalog", "translation_status: complete", "---", "",
        "# Skills Catalog", "",
        f'Verified starter records: **{len(skills)}**.', '',
        "> Third-party skills remain governed by upstream licenses and terms.", "",
        "## Category summary", "",
        "| Category | Records |", "|---|---:|",
    ]
    for category, count in sorted(categories.items()):
        lines.append(f"| {category} | {count} |")
    lines += [
        "", "## Records", "",
        "| Name | Display name | Category | Origin | Status | Summary | Upstream |",
        "|---|---|---|---|---|---|---|",
        *table_rows(skills, "en"), "",
        "## Verification model", "",
        "Each verified record includes the upstream repository, path, blob SHA and verification date.",
    ]
    return "\n".join(lines)


def build_pt(document: dict) -> str:
    skills = document["skills"]
    categories = Counter(skill["category"] for skill in skills)
    lines = [
        "---", "title: Catálogo de Skills", "language: pt",
        "translation_key: skills-catalog", "translation_status: complete", "---", "",
        "# Catálogo de Skills", "",
        f'Registros iniciais verificados: **{len(skills)}**.', '',
        "> Skills de terceiros permanecem sujeitas às licenças e condições das fontes originais.", "",
        "## Resumo por categoria", "",
        "| Categoria | Registros |", "|---|---:|",
    ]
    for category, count in sorted(categories.items()):
        lines.append(f"| {category} | {count} |")
    lines += [
        "", "## Registros", "",
        "| Nome | Nome exibido | Categoria | Origem | Estado | Resumo | Fonte |",
        "|---|---|---|---|---|---|---|",
        *table_rows(skills, "pt"), "",
        "## Modelo de verificação", "",
        "Cada registro verificado inclui repositório, caminho, hash do arquivo e data de verificação.",
    ]
    return "\n".join(lines)


def main() -> None:
    document = load()
    skills = document["skills"]
    write(EN_OUTPUT, build_en(document))
    write(PT_OUTPUT, build_pt(document))

    by_category: dict[str, list[str]] = defaultdict(list)
    for skill in skills:
        by_category[skill["category"]].append(skill["id"])

    dashboard = {
        "schema_version": document["schema_version"],
        "generated_on": document["generated_on"],
        "total_skills": len(skills),
        "verified_skills": sum(skill["status"] == "verified" for skill in skills),
        "categories": [
            {"id": category, "count": len(ids), "skill_ids": sorted(ids)}
            for category, ids in sorted(by_category.items())
        ],
        "skills": skills,
    }
    DASHBOARD_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    DASHBOARD_OUTPUT.write_text(json.dumps(dashboard, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {EN_OUTPUT}")
    print(f"Wrote {PT_OUTPUT}")
    print(f"Wrote {DASHBOARD_OUTPUT}")


if __name__ == "__main__":
    main()
