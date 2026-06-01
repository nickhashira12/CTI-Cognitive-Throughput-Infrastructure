"""
Run Movement 2 — Causal Identification by Ablation
Reproduces the ablation table from the CTI paper.
Output: energy/results/movement2_ablations.csv
"""
import pandas as pd
import numpy as np
from pathlib import Path
from baselines import load_day
from ablations import (simulate_static, simulate_price_only,
                       simulate_no_battery, simulate_no_soak, simulate_full)

DATA_DIR = Path(__file__).parent.parent / "data"
RESULTS_DIR = Path(__file__).parent.parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

DAYS = [
    "2025-03-10", "2025-03-17", "2025-04-07",
    "2025-04-15", "2025-04-21", "2025-05-05"
]

VARIANTS = [
    ("STATIC",      simulate_static),
    ("PRICE_ONLY",  simulate_price_only),
    ("NO_BATTERY",  simulate_no_battery),
    ("NO_SOAK",     simulate_no_soak),
    ("FULL",        simulate_full),
]

rows = []
for date in DAYS:
    df = load_day(DATA_DIR / f"caiso_{date}.csv")
    day_row = {"date": date}
    prev_cost = None
    for name, fn in VARIANTS:
        cost, d = fn(df)
        day_row[f"cost_{name}"] = round(cost, 4)
        day_row[f"delta_d_{name}"] = d
        if prev_cost is not None:
            improvement = round((prev_cost - cost) / abs(prev_cost) * 100, 1) if prev_cost != 0 else 0
            day_row[f"gain_{name}_pct"] = improvement
        prev_cost = cost
    rows.append(day_row)

results = pd.DataFrame(rows)
out = RESULTS_DIR / "movement2_ablations.csv"
results.to_csv(out, index=False)

print("=== Movement 2 — Ablation Results ===")
cost_cols = [f"cost_{n}" for n, _ in VARIANTS]
print(results[["date"] + cost_cols].to_string(index=False))

print("\n=== Monotonicity check (cost should decrease left→right) ===")
for _, row in results.iterrows():
    costs = [row[c] for c in cost_cols]
    mono = all(costs[i] >= costs[i+1] for i in range(len(costs)-1))
    print(f"  {row['date']}: {'✓ monotone' if mono else '✗ VIOLATED'}")

print(f"\nSaved to: {out}")
