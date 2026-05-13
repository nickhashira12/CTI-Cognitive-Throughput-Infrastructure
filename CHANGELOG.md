# Changelog

All notable changes to CTI will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
CTI uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.0.0] — 2026

### Breaking Changes
- **Removed "Law" framing.** The previous "First Law / Second Law" presentation has been retired. The two formulas are definitions of metrics, not physical laws. They are now presented as **Specification 1 (Throughput Metric)** and **Specification 2 (Efficiency Metric)**.
- **Repositioned CTI as a measurement protocol**, not an operational theory of cognition. The underlying mathematics and philosophical boundary are unchanged; the positioning is corrected.
- **Renamed `/docs/laws.md` → `/docs/protocol.md`**.
- **File extensions normalized.** Previously extensionless files (`MANIFIESTO`, `CHANGELOG`, `CONTRIBUTING`, `CITATION`, `LICENSE`, `docs/*`, `research/*`, `rfcs/*`) now use `.md` (or `.cff` for `CITATION.cff`) to render correctly on GitHub.
- **Naming standardized to `MANIFESTO.md`** (English spelling) for consistency with internal references.
- **Directory casing normalized** to lowercase: `research/`, `rfcs/`.

### Added
- Explicit comparison of CTI metrics to existing benchmarks (tokens/sec, latency, accuracy) in README and MANIFESTO.
- Explicit prior-art acknowledgment: Simon (1955), constrained MDPs, operationalism, AI observability stack (LangSmith, Helicone, Arize, Langfuse, AgentOps), agent benchmarks (AgentBench, GAIA, SWE-bench).
- Roadmap section in README and MANIFESTO covering v3.1 through v3.3.
- New research category **Q7 — Empirical Validation** in `open-questions.md`, with three concrete questions targeting reference implementation and falsifiable claims.

### Changed
- README and MANIFESTO rewritten with protocol framing throughout.
- `docs/protocol.md` (formerly `docs/laws.md`) reframes Specifications 1 & 2 as definitions and operationalization requirements rather than physical laws.
- `docs/formal-model.md` adds explicit prior-art attribution to bounded rationality (Simon, 1955) and constrained MDPs.
- `docs/philosophy.md` adds a section on the v2→v3 frame shift, explaining the retraction of "Law" language.

### Roadmap
- **v3.1.0** — Replace "decision" primitive with **evaluable cognitive event** carrying type signature `{trigger, output, validator, cost, latency}`. Closes Q1.3.
- **v3.2.0** — Reference implementation: compute $I_t$ and $E_c$ across LangGraph, CrewAI, OpenAI Agents SDK, AutoGen. Converts CTI from manifesto to instrument.
- **v3.3.0** — One falsifiable empirical claim regarding $E_c$ scaling under model size in agentic tool-use tasks.

---

## [2.0.0] — 2025

### Added
- First public release of the CTI framework in English
- Full formal manifesto
- First Law: The Cognitive Throughput Axiom ($I_t = \Delta D / \Delta T$)
- Second Law: The Cognitive Efficiency Principle ($E_c = Q / (C \cdot T)$)
- Formal Model of Cognitive Decision (contextual optimization under constraints)
- Operational definition of a valid decision
- Philosophical boundary declaration
- Open research directions
- RFC contribution system
- Documentation structure (`/docs`)
- Open research questions

### Philosophy
- Explicit epistemological limit established: CTI measures operational cognition, not metaphysical truth
- Conscious rejection of claims about consciousness, phenomenology, and absolute truth

### Deprecated in v3.0.0
- "Law" framing of the two metrics
- "Axiom" and "Principle" terminology

---

## [1.0.0] — Internal

- Initial conception of the Cognitive Throughput Layer
- First formulations of throughput and efficiency metrics (Spanish, internal draft)

---

*To propose changes, see [`CONTRIBUTING.md`](./CONTRIBUTING.md).*
