from __future__ import annotations

from collections import defaultdict
from datetime import date
from typing import Any
import math

from common import ROOT, load_json, write_json


RESULTS_PATH = ROOT / "benchmarks/data/sample-results.json"
MODELS_PATH = ROOT / "benchmarks/data/model-registry.json"
METRICS_PATH = ROOT / "benchmarks/config/metrics.json"
NORMALIZATION_PATH = ROOT / "benchmarks/config/normalization.json"
OUTPUT_JSON = ROOT / "benchmarks/generated/rankings.json"
OUTPUT_MD = ROOT / "benchmarks/generated/rankings.md"


def normalize(values: list[float], direction: str, equal_score: float) -> list[float]:
    minimum = min(values)
    maximum = max(values)

    if math.isclose(minimum, maximum):
        return [equal_score for _ in values]

    if direction == "higher_is_better":
        return [(value - minimum) / (maximum - minimum) for value in values]

    if direction == "lower_is_better":
        return [(maximum - value) / (maximum - minimum) for value in values]

    raise ValueError(f"Unsupported direction: {direction}")


def main() -> None:
    result_document = load_json(RESULTS_PATH)
    model_document = load_json(MODELS_PATH)
    metrics_config = load_json(METRICS_PATH)
    normalization_config = load_json(NORMALIZATION_PATH)

    models = {item["id"]: item for item in model_document["models"]}
    equal_score = float(normalization_config["normalization"]["equal_values_score"])
    display_scale = float(normalization_config["normalization"]["display_scale"])
    score_precision = int(normalization_config["ranking"]["score_precision"])

    # This starter dataset is synthetic by design. Production ingestion should
    # enforce provenance rules from normalization.json before public ranking.
    results = result_document["results"]

    by_metric: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for result in results:
        key = (
            result["benchmark_id"],
            result["benchmark_version"],
            result["metric_id"],
        )
        by_metric[key].append(result)

    normalized_records: list[dict[str, Any]] = []
    for records in by_metric.values():
        direction = records[0]["metric_direction"]
        values = [float(record["score"]) for record in records]
        normalized_values = normalize(values, direction, equal_score)

        for record, normalized_value in zip(records, normalized_values):
            normalized_records.append(
                {**record, "normalized_score": normalized_value}
            )

    category_metric_counts = {
        category: len(config["metrics"])
        for category, config in metrics_config["categories"].items()
    }

    by_model_category: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for record in normalized_records:
        by_model_category[(record["model_id"], record["category"])].append(record)

    categories: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for (model_id, category), records in by_model_category.items():
        category_config = metrics_config["categories"].get(category)
        if not category_config:
            continue

        expected = category_metric_counts[category]
        observed_metric_ids = {record["metric_id"] for record in records}
        coverage = len(observed_metric_ids) / expected if expected else 0.0
        minimum_coverage = float(category_config["minimum_coverage"])

        weighted_total = 0.0
        total_weight = 0.0

        for record in records:
            metric_config = category_config["metrics"].get(record["metric_id"])
            if not metric_config:
                continue
            weight = float(metric_config["weight"])
            weighted_total += record["normalized_score"] * weight
            total_weight += weight

        score = None
        status = "insufficient_coverage"
        if total_weight and coverage >= minimum_coverage:
            score = round((weighted_total / total_weight) * display_scale, score_precision)
            status = "ranked"

        model = models.get(model_id, {"display_name": model_id, "provider": "Unknown"})
        categories[category].append(
            {
                "model_id": model_id,
                "model_name": model["display_name"],
                "provider": model["provider"],
                "score": score,
                "coverage": round(coverage, 4),
                "metric_count": len(observed_metric_ids),
                "status": status,
            }
        )

    output_categories: dict[str, Any] = {}
    for category, entries in categories.items():
        ranked = [entry for entry in entries if entry["score"] is not None]
        unranked = [entry for entry in entries if entry["score"] is None]

        ranked.sort(key=lambda entry: (-entry["score"], entry["model_name"]))
        current_rank = 0
        previous_score = None

        for index, entry in enumerate(ranked, start=1):
            if previous_score is None or entry["score"] != previous_score:
                current_rank = index
            entry["rank"] = current_rank
            previous_score = entry["score"]

        output_categories[category] = {
            "label": metrics_config["categories"][category]["label"],
            "rankings": ranked,
            "unranked": unranked,
        }

    output = {
        "schema_version": "1.0.0",
        "generated_at": date.today().isoformat(),
        "data_notice": result_document.get("notice"),
        "categories": output_categories,
    }
    write_json(OUTPUT_JSON, output)

    lines = [
        "# Generated Benchmark Rankings",
        "",
        f"Generated: {output['generated_at']}",
        "",
        f"> {output['data_notice']}",
        "",
    ]

    for payload in output_categories.values():
        lines.extend(
            [
                f"## {payload['label']}",
                "",
                "| Rank | Model | Provider | Score | Coverage |",
                "|---:|---|---|---:|---:|",
            ]
        )
        for entry in payload["rankings"]:
            lines.append(
                f"| {entry['rank']} | {entry['model_name']} | "
                f"{entry['provider']} | {entry['score']:.2f} | "
                f"{entry['coverage']:.0%} |"
            )
        if not payload["rankings"]:
            lines.append("| — | No eligible results | — | — | — |")
        lines.append("")

    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUTPUT_JSON}")
    print(f"Wrote {OUTPUT_MD}")


if __name__ == "__main__":
    main()
