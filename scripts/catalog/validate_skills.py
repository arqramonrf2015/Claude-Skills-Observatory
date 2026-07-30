from __future__ import annotations

from datetime import date
from pathlib import Path
from urllib.parse import urlparse
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "data/skills/skills.json"
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
SHA_RE = re.compile(r"^[a-f0-9]{40}$")
VALID_ORIGINS = {"official", "partner", "community", "custom", "research"}
VALID_STATUSES = {"verified", "review", "draft", "deprecated", "archived"}
VALID_LICENSE_CLASSES = {"open-source", "source-available", "upstream-specific", "unknown"}

REQUIRED = {
    "id", "name", "display_name", "summary_en", "summary_pt", "origin",
    "publisher", "category", "subcategory", "status", "source_repository",
    "source_path", "source_url", "source_blob_sha", "license", "license_class",
    "required_files", "bundled_resources", "capabilities", "tags", "verified_on"
}


def load_catalog() -> dict:
    with CATALOG.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def valid_date(value: str) -> bool:
    try:
        date.fromisoformat(value)
        return True
    except (TypeError, ValueError):
        return False


def main() -> int:
    catalog = load_catalog()
    errors: list[str] = []
    skills = catalog.get("skills")

    if not isinstance(skills, list):
        print("Catalog field `skills` must be an array.")
        return 1

    if catalog.get("record_count") != len(skills):
        errors.append("record_count does not match the number of skills")

    seen_ids: set[str] = set()
    seen_sources: set[tuple[str, str]] = set()

    for index, skill in enumerate(skills):
        location = f"skills[{index}]"
        missing = REQUIRED - set(skill)
        if missing:
            errors.append(f"{location}: missing {sorted(missing)}")
            continue

        if not ID_RE.fullmatch(skill["id"]):
            errors.append(f"{location}: invalid id")
        if not ID_RE.fullmatch(skill["name"]):
            errors.append(f"{location}: invalid name")
        if skill["id"] in seen_ids:
            errors.append(f"{location}: duplicate id")
        seen_ids.add(skill["id"])

        source_key = (skill["source_repository"], skill["source_path"])
        if source_key in seen_sources:
            errors.append(f"{location}: duplicate source path")
        seen_sources.add(source_key)

        if skill["origin"] not in VALID_ORIGINS:
            errors.append(f"{location}: invalid origin")
        if skill["status"] not in VALID_STATUSES:
            errors.append(f"{location}: invalid status")
        if skill["license_class"] not in VALID_LICENSE_CLASSES:
            errors.append(f"{location}: invalid license class")
        if not SHA_RE.fullmatch(skill["source_blob_sha"]):
            errors.append(f"{location}: invalid blob SHA")
        if not valid_date(skill["verified_on"]):
            errors.append(f"{location}: invalid verification date")

        parsed = urlparse(skill["source_url"])
        if parsed.scheme != "https" or not parsed.netloc:
            errors.append(f"{location}: source_url must be HTTPS")

        for field in ("required_files", "capabilities", "tags"):
            value = skill[field]
            if not isinstance(value, list) or not value:
                errors.append(f"{location}: {field} must be a non-empty array")

    if errors:
        print("\n".join(errors))
        return 1

    print(f"Validated {len(skills)} skill records.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
