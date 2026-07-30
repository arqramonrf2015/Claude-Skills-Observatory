from __future__ import annotations

from datetime import date
from pathlib import Path
from urllib.parse import urlparse
import sys

from common import ROOT, load_json


DATA_DIR = ROOT / "benchmarks/data"

REQUIRED_FIELDS = {
    "id", "benchmark_id", "benchmark_version", "category",
    "metric_id", "metric_direction", "score", "unit",
    "model_id", "model_version", "evaluation_date",
    "provenance", "source", "reproducibility"
}
DIRECTIONS = {"higher_is_better", "lower_is_better"}
PROVENANCE = {"independent", "official", "community", "synthetic", "estimated"}
REPRODUCIBILITY = {"not_attempted", "partial", "reproduced", "failed"}


def validate_iso_date(value: str) -> bool:
    try:
        date.fromisoformat(value)
        return True
    except (TypeError, ValueError):
        return False


def validate_file(path: Path) -> list[str]:
    document = load_json(path)
    errors: list[str] = []

    if not isinstance(document.get("results"), list):
        return [f"{path}: `results` must be an array."]

    seen_ids: set[str] = set()

    for index, result in enumerate(document["results"]):
        location = f"{path}: results[{index}]"
        missing = REQUIRED_FIELDS - set(result)
        if missing:
            errors.append(f"{location}: missing fields: {sorted(missing)}")
            continue

        if result["id"] in seen_ids:
            errors.append(f"{location}: duplicate id `{result['id']}`")
        seen_ids.add(result["id"])

        if result["metric_direction"] not in DIRECTIONS:
            errors.append(f"{location}: invalid metric direction")
        if result["provenance"] not in PROVENANCE:
            errors.append(f"{location}: invalid provenance")
        if not isinstance(result["score"], (int, float)):
            errors.append(f"{location}: score must be numeric")
        if not validate_iso_date(result["evaluation_date"]):
            errors.append(f"{location}: invalid evaluation date")

        source = result.get("source", {})
        parsed = urlparse(source.get("url", ""))
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            errors.append(f"{location}: invalid source URL")

        repro = result.get("reproducibility", {})
        if repro.get("status") not in REPRODUCIBILITY:
            errors.append(f"{location}: invalid reproducibility status")

    return errors


def main() -> int:
    files = sorted(DATA_DIR.glob("*results*.json"))
    if not files:
        print("No result files found.")
        return 1

    all_errors: list[str] = []
    for path in files:
        all_errors.extend(validate_file(path))

    if all_errors:
        print("\n".join(all_errors))
        return 1

    print(f"Validated {len(files)} benchmark result file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
