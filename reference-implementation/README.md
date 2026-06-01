# Reference Implementation

Empirical reference implementation of **CTI Specification 1 — Throughput** ($I_t = \Delta D / \Delta T$), instantiating the roadmap item **v3.2.0**.

This directory does not redefine the protocol. It demonstrates that Spec 1 is operationally measurable on real, unrelated substrates, and reports the results.

## Mapping to the protocol

The implementations here predate the v3.1 ECE primitive but map onto it cleanly. Each decision the systems make is an **Evaluable Cognitive Event (ECE)**:

| ECE field | Energy substrate (dispatch) | Retrieval substrate (IRIS) |
|-----------|------------------------------|-----------------------------|
| `trigger` | New interval price signal | User query |
| `output` | Dispatch / battery action | Ranked result above cosine floor |
| `validator` | Cost-aware policy outcome | Cosine ≥ 0.15 + full-listen confirmation |
| `cost` | $/MWh exposure of the action | Compute of the query |
| `latency` | Interval decision time | Query→render, ms |

**ΔD** is then the count of *validated* ECEs in an interval, exactly as Spec 1 defines it. **ΔT** is the interval duration. No redefinition — only an instantiation.

## Two substrates

- **`energy/`** — a CAISO day-ahead dispatch simulator and the decision motors. Full code, data, and results here.
- **Retrieval** — lives in its own repo, [iris](https://github.com/nickhashira12/iris), as a shippable Chrome extension. Linked rather than vendored because it is also a product.

The point of two unrelated substrates is to test whether Spec 1 is substrate-independent. The paper states this as an open, empirically-supported conjecture — not a proven invariance.

## Contents

```
reference-implementation/
├── paper/     The technical paper (PDF, Markdown source, HTML render)
├── energy/
│   ├── src/       Decision motors + reproduction scripts
│   ├── data/      Real CAISO LMP days (6) with provenance
│   └── results/   Output CSVs reproducing the paper's tables
└── LICENSE        MIT — applies to code in this directory only
```

## Empirical results (summary)

- **Movement 1 — baselines.** Full loop beats an industry-competent time-of-use scheduler by a mean **+78.5%** in cost savings over 6 real CAISO days. **r(ΔD, savings) = +0.877**, 95% CI [+0.36, +0.98], N=6.
- **Movement 2 — ablation.** Five capability-nested variants; monotonicity holds 6/6 days; value decomposes mainly to battery dispatch (+46.4%) and price awareness (+34.8%).

Two results proved formally (Ablation Monotonicity; Decomposition of Value Capture). Six falsifiable predictions stated. See `paper/`.

## Reproduce

```bash
pip install -r energy/requirements.txt
python energy/src/run_movement1.py    # → energy/results/movement1_results.csv
python energy/src/run_movement2.py    # → energy/results/movement2_ablations.csv
```

## Licensing

The CTI protocol, docs, and the paper text remain under the repository's **CC BY 4.0**. The **source code in this directory** (`energy/src/`) is additionally released under the **MIT License** (see [`LICENSE`](./LICENSE)) so it can be run, modified, and reused as software. Attribution under CC BY 4.0 still applies to the framework and paper.
