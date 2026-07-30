from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/skills/skills.json"
DASHBOARD_OUTPUT = ROOT / "dashboards/skills/data/skills-catalog.json"


def load() -> dict:
    with SOURCE.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> None:
    document = load()
    skills = document["skills"]

    by_category: dict[str, list[str]] = defaultdict(list)
    for skill in skills:
        by_category[skill["category"]].append(skill["id"])

    dashboard = {
        "schema_version": document["schema_version"],
        "generated_on": document["generated_on"],
        "total_skills": len(skills),
        "verified_skills": sum(
            skill["status"] == "verified" for skill in skills
        ),
        "categories": [
            {
                "id": category,
                "count": len(ids),
                "skill_ids": sorted(ids),
            }
            for category, ids in sorted(by_category.items())
        ],
        "skills": skills,
    }

    DASHBOARD_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    DASHBOARD_OUTPUT.write_text(
        json.dumps(dashboard, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Wrote {DASHBOARD_OUTPUT}")


if __name__ == "__main__":
    main()
