# Data provenance

The six CAISO trading days used in Movements 1 and 2.

| File | Date | Notes |
|------|------|-------|
| `caiso_2025-03-10.csv` | 2025-03-10 | |
| `caiso_2025-03-17.csv` | 2025-03-17 | |
| `caiso_2025-04-07.csv` | 2025-04-07 | Lowest mean price ($14.99/MWh) → lowest savings (44.4%). Read as evidence value scales with volatility. |
| `caiso_2025-04-15.csv` | 2025-04-15 | |
| `caiso_2025-04-21.csv` | 2025-04-21 | |
| `caiso_2025-05-05.csv` | 2025-05-05 | |

## Real vs. modeled — read before drawing conclusions

- **Price (LMP) — REAL.** Real CAISO day-ahead market data for the listed dates.
- **Solar — MODELED.** A modeled curve, not measured plant output.
- **Demand — MODELED.** A modeled profile, not measured load.

The decision loop acts on the *real price signal*, which is the variable the value claim depends on. Replacing the modeled solar/demand columns with measured data is the entirety of the deferred Movement 1B. This limitation is stated in the paper.

## Schema

Hourly (or sub-hourly where noted):

- `timestamp` — interval start, local CAISO time
- `lmp_usd_mwh` — locational marginal price, USD/MWh (REAL)
- `solar_kw` — modeled available solar, kW (MODELED)
- `demand_kw` — modeled site demand, kW (MODELED)
