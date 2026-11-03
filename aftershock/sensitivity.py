"""Reproduce the negative control: legitimate clients use a 'sensitive' path."""
from copy import deepcopy
import csv
from pathlib import Path
from .engine import evaluate
from .scenarios import scenario


def run(destination="output/sensitivity.csv"):
    rows = []
    for count in (0, 5, 10, 18, 19, 30, 50, 100):
        case = scenario("shared-nat")
        for i in range(count):
            request = deepcopy(case["requests"][0])
            request.update(id=f"sensitivity-{i}", path="/.env", service="store")
            case["requests"].append(request)
        result = evaluate(case, case["initial_state"], "narrow_control")
        rows.append({"added_legitimate_sensitive_requests": count,
                     "attack_denied": result["newly_denied"]["attack"],
                     "benign_denied": result["newly_denied"]["benign"],
                     "benign_baseline": result["baseline_allowed"]["benign"],
                     "collateral_pct": result["collateral_pct"], "eligible": result["eligible"]})
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Eight sensitivity experiments saved: {path}")


if __name__ == "__main__":
    run()
