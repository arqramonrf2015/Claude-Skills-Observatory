from __future__ import annotations

from pathlib import Path
import json
import shutil

ROOT = Path(__file__).resolve().parents[2]

SOURCES = {
    ROOT / "dashboards/skills/data/skills-catalog.json": ROOT / "docs/assets/data/skills.json",
    ROOT / "dashboards/benchmarks/data/benchmark-dashboard.json": ROOT / "docs/assets/data/benchmarks.json",
}


def validate_json(path: Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        json.load(handle)


def main() -> None:
    for source, target in SOURCES.items():
        if not source.exists():
            raise SystemExit(f"Missing portal data source: {source}")
        validate_json(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        print(f"Synced {source.relative_to(ROOT)} -> {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
