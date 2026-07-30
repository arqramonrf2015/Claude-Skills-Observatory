from __future__ import annotations

from common import ROOT, load_json, write_json


SOURCE = ROOT / "benchmarks/generated/rankings.json"
TARGET = ROOT / "dashboards/benchmarks/data/benchmark-dashboard.json"


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(
            "Rankings file not found. Run "
            "`python scripts/benchmark/generate_rankings.py` first."
        )

    rankings = load_json(SOURCE)
    cards = []

    for category_id, category in rankings["categories"].items():
        leader = category["rankings"][0] if category["rankings"] else None
        cards.append(
            {
                "category_id": category_id,
                "category_label": category["label"],
                "leader": leader,
                "ranked_models": len(category["rankings"]),
            }
        )

    payload = {
        "schema_version": "1.0.0",
        "generated_at": rankings["generated_at"],
        "data_notice": rankings.get("data_notice"),
        "cards": cards,
        "categories": rankings["categories"],
    }
    write_json(TARGET, payload)
    print(f"Wrote {TARGET}")


if __name__ == "__main__":
    main()
