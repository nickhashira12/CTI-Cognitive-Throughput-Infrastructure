"""
CTI Energy Reference — Movement 2: Causal Identification by Ablation
Five capability-nested variants: STATIC <= PRICE_ONLY <= NO_BATTERY <= NO_SOAK <= FULL
Maps to CTI Specification 1: causal decomposition of ΔD value.
"""

import pandas as pd
import numpy as np

BATTERY_CAPACITY_KWH = 100.0
BATTERY_MAX_KW = 25.0
SITE_LOAD_KW = 20.0

def simulate_static(df):
    """STATIC: no price awareness, no battery, flat 65%."""
    cost, decisions = 0.0, 0
    for _, row in df.iterrows():
        net = max(0, SITE_LOAD_KW * 0.65 - row['solar_kw'])
        cost += net * row['lmp_usd_mwh'] / 1000
        decisions += 1
    return cost, decisions

def simulate_price_only(df):
    """PRICE_ONLY: price-aware load shift, no battery."""
    p75 = np.percentile(df['lmp_usd_mwh'], 75)
    cost, decisions = 0.0, 0
    for _, row in df.iterrows():
        load = SITE_LOAD_KW * 0.20 if row['lmp_usd_mwh'] > p75 else SITE_LOAD_KW * 0.65
        net = max(0, load - row['solar_kw'])
        cost += net * row['lmp_usd_mwh'] / 1000
        decisions += 1
    return cost, decisions

def simulate_no_battery(df):
    """NO_BATTERY: price-aware + surplus gating, no battery dispatch."""
    p25 = np.percentile(df['lmp_usd_mwh'], 25)
    p75 = np.percentile(df['lmp_usd_mwh'], 75)
    cost, decisions = 0.0, 0
    for _, row in df.iterrows():
        lmp = row['lmp_usd_mwh']
        if lmp > p75:
            load = SITE_LOAD_KW * 0.20
        elif lmp < p25:
            load = SITE_LOAD_KW * 0.80
        else:
            load = SITE_LOAD_KW * 0.50
        net = max(0, load - row['solar_kw'])
        cost += net * lmp / 1000
        decisions += 1
    return cost, decisions

def simulate_no_soak(df):
    """NO_SOAK: full battery dispatch but no negative-price soak."""
    p25 = np.percentile(df['lmp_usd_mwh'], 25)
    p75 = np.percentile(df['lmp_usd_mwh'], 75)
    cost, decisions = 0.0, 0
    battery_soc = BATTERY_CAPACITY_KWH * 0.5
    for _, row in df.iterrows():
        lmp = row['lmp_usd_mwh']
        solar = row['solar_kw']
        if lmp > p75 and battery_soc > 10:
            discharge = min(BATTERY_MAX_KW, battery_soc - 10)
            battery_soc -= discharge
            net = max(0, SITE_LOAD_KW * 0.20 - solar - discharge)
        elif lmp < p25 and battery_soc < BATTERY_CAPACITY_KWH - 5:
            charge = min(BATTERY_MAX_KW, BATTERY_CAPACITY_KWH - battery_soc)
            battery_soc += charge
            net = max(0, SITE_LOAD_KW * 0.65 - solar + charge)
        else:
            net = max(0, SITE_LOAD_KW * 0.50 - solar)
        cost += net * lmp / 1000
        decisions += 1
    return cost, decisions

def simulate_full(df):
    """FULL: complete loop including negative-price soak."""
    from baselines import simulate_cti_full
    return simulate_cti_full(df)

if __name__ == "__main__":
    print("ablations.py loaded. Run via run_movement2.py")
