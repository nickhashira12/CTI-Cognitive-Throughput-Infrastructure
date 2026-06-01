"""
CTI Energy Reference — Movement 1: Competitive Baselines
Four dispatch policies of increasing competence over real CAISO LMP days.
Maps to CTI Specification 1: I_t = ΔD / ΔT
"""

import pandas as pd
import numpy as np
from pathlib import Path

BATTERY_CAPACITY_KWH = 100.0
BATTERY_MAX_KW = 25.0
SOLAR_MAX_KW = 30.0
SITE_LOAD_KW = 20.0

def load_day(csv_path):
    df = pd.read_csv(csv_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def simulate_naive(df):
    """NAIVE: flat 65% compute, no price awareness."""
    cost = 0.0
    decisions = 0
    for _, row in df.iterrows():
        load = SITE_LOAD_KW * 0.65
        net = load - row['solar_kw']
        if net > 0:
            cost += net * row['lmp_usd_mwh'] / 1000
        decisions += 1
    return cost, decisions

def simulate_throttle_at_peak(df, threshold_pct=90):
    """THROTTLE_AT_PEAK: cut to 30% compute when price > 90th percentile."""
    p90 = np.percentile(df['lmp_usd_mwh'], threshold_pct)
    cost = 0.0
    decisions = 0
    for _, row in df.iterrows():
        if row['lmp_usd_mwh'] > p90:
            load = SITE_LOAD_KW * 0.30
        else:
            load = SITE_LOAD_KW * 0.65
        net = load - row['solar_kw']
        if net > 0:
            cost += net * row['lmp_usd_mwh'] / 1000
        decisions += 1
    return cost, decisions

def simulate_tou_aware(df):
    """ToU_AWARE: industry-standard time-of-use scheduling."""
    cost = 0.0
    decisions = 0
    for _, row in df.iterrows():
        hour = row['timestamp'].hour
        # Peak: 16-21, Off-peak: 22-06, Shoulder: rest
        if 16 <= hour <= 21:
            load = SITE_LOAD_KW * 0.20
        elif hour <= 6 or hour >= 22:
            load = SITE_LOAD_KW * 0.90
        else:
            load = SITE_LOAD_KW * 0.65
        net = load - row['solar_kw']
        if net > 0:
            cost += net * row['lmp_usd_mwh'] / 1000
        decisions += 1
    return cost, decisions

def simulate_cti_full(df):
    """CTI_FULL: full sense-decide-act loop with battery dispatch."""
    cost = 0.0
    decisions = 0
    battery_soc = BATTERY_CAPACITY_KWH * 0.5
    p25 = np.percentile(df['lmp_usd_mwh'], 25)
    p75 = np.percentile(df['lmp_usd_mwh'], 75)

    for _, row in df.iterrows():
        lmp = row['lmp_usd_mwh']
        solar = row['solar_kw']
        hour = row['timestamp'].hour

        # Negative price soak
        if lmp < 0:
            charge = min(BATTERY_MAX_KW, BATTERY_CAPACITY_KWH - battery_soc)
            battery_soc += charge
            load = SITE_LOAD_KW * 0.30
            net = load - solar - charge
            if net > 0:
                cost += net * lmp / 1000
            decisions += 1
            continue

        # High price: discharge battery
        if lmp > p75 and battery_soc > 10:
            discharge = min(BATTERY_MAX_KW, battery_soc - 10)
            battery_soc -= discharge
            load = SITE_LOAD_KW * 0.20
            net = max(0, load - solar - discharge)
            cost += net * lmp / 1000
            decisions += 1
            continue

        # Low price: charge battery
        if lmp < p25 and battery_soc < BATTERY_CAPACITY_KWH - 5:
            charge = min(BATTERY_MAX_KW, BATTERY_CAPACITY_KWH - battery_soc)
            battery_soc += charge
            load = SITE_LOAD_KW * 0.65
            net = load - solar + charge
            if net > 0:
                cost += net * lmp / 1000
            decisions += 1
            continue

        # Default: moderate load
        load = SITE_LOAD_KW * 0.50
        net = max(0, load - solar)
        cost += net * lmp / 1000
        decisions += 1

    return cost, decisions

if __name__ == "__main__":
    print("baselines.py loaded. Run via run_movement1.py")
