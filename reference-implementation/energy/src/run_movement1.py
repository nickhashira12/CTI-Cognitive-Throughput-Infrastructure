"""
Run Movement 1 — Competitive Baselines
Reproduces Table 1 from the CTI paper.
Output: energy/results/movement1_results.csv
"""
import pandas as pd
import numpy as np
from pathlib import Path
from baselines import (load_day, simulate_naive, simulate_throttle_at_peak,
                       simulate_tou_aware, simulate_cti_full)

DATA_DIR = Path(__file__).parent.parent / "data"
RESULTS_DIR = Path(__file__).parent.parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

DAYS = [
    "2025-03-10", "2025-03-17", "2025-04-07",
    "2025-04-15", "2025-04-21", "2025-05-05"
]

rows = []
for date in DAYS:
    df = load_day(DATA_DIR / f"caiso_{date}.csv")
    mean_lmp = df['lmp_usd_mwh'].mean()

    cost_naive, d_naive = simulate_naive(df)
    cost_throttle, d_throttle = simulate_throttle_at_peak(df)
    cost_tou, d_tou = simulate_tou_aware(df)
    cost_cti, d_cti = simulate_cti_full(df)

    def savings_pct(baseline, cti):
        return round((baseline - cti) / abs(baseline) * 100, 1) if baseline != 0 else 0

    rows.append({
        "date": date,
        "mean_lmp_usd_mwh": round(mean_lmp, 2),
        "cost_naive": round(cost_naive, 4),
        "cost_throttle": round(cost_throttle, 4),
        "cost_tou": round(cost_tou, 4),
        "cost_cti_full": round(cost_cti, 4),
        "delta_d_cti": d_cti,
        "savings_vs_naive_pct": savings_pct(cost_naive, cost_cti),
        "savings_vs_throttle_pct": savings_pct(cost_throttle, cost_cti),
        "savings_vs_tou_pct": savings_pct(cost_tou, cost_cti),
    })

results = pd.DataFrame(rows)
out = RESULTS_DIR / "movement1_results.csv"
results.to_csv(out, index=False)

print("=== Movement 1 Results ===")
print(results[["date", "mean_lmp_usd_mwh", "savings_vs_naive_pct",
               "savings_vs_throttle_pct", "savings_vs_tou_pct"]].to_string(index=False))
print(f"\nMean savings vs NAIVE:    {results['savings_vs_naive_pct'].mean():.1f}%")
print(f"Mean savings vs THROTTLE: {results['savings_vs_throttle_pct'].mean():.1f}%")
print(f"Mean savings vs ToU:      {results['savings_vs_tou_pct'].mean():.1f}%")

r = np.corrcoef(results['delta_d_cti'], results['savings_vs_tou_pct'])[0,1]
print(f"r(ΔD, savings_vs_tou):    {r:.3f}")
print(f"\nSaved to: {out}")
