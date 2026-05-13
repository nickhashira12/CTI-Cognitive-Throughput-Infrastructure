# CTI v3 — Cognitive Throughput Infrastructure

## A Measurement Protocol for Operational Cognition

**Version:** 3.1.0 &nbsp;|&nbsp; **Status:** Open Specification &nbsp;|&nbsp; **License:** CC BY 4.0

---

## Introduction

Modern artificial intelligence is benchmarked on tokens per second, latency, FLOPS, and accuracy. None of these measure what matters most for agentic and reasoning systems: **the rate and efficiency of validated decisions produced under real operational constraints.**

CTI emerges as a response to that gap.

CTI is a **measurement protocol**. It is not a theory of intelligence, a model of consciousness, or a physical law. v2 of this document used "Law/Axiom/Principle" framing inherited from physics-style manifestos. v3 explicitly removes that framing. What remains is a specification — falsifiable, revisable, and implementable.

---

## What CTI Specifies

CTI proposes a new operational layer: the **Cognitive Throughput Layer** — situated above models, tools, frameworks, and multi-agent systems.

```mermaid
flowchart TB
    A[Applications]
    B[Agents / Orchestration]
    C["★ Cognitive Throughput Layer ★"]
    D[Models / Compute]
    A --- B
    B --- C
    C --- D
    style A fill:#f5f5f5,stroke:#1a1a1a,color:#1a1a1a
    style B fill:#f5f5f5,stroke:#1a1a1a,color:#1a1a1a
    style C fill:#0a0a0a,stroke:#00d9ff,color:#ffffff,stroke-width:3px
    style D fill:#f5f5f5,stroke:#1a1a1a,color:#1a1a1a
```

This layer is a measurement plane. CTI specifies:

- A definition of **throughput** ($I_t$) for decision systems
- A definition of **efficiency** ($E_c$) for decision systems
- A formal model of **bounded-rational decision-making** as the underlying optimization problem
- A philosophical boundary that limits CTI to operationally observable behavior

CTI does not specify which agents, models, or runtimes implement the protocol. It specifies what they must expose to be measured.

---

## The Frame Shift

Previous versions presented CTI as a set of "Laws" — a framing borrowed from physics. This was incorrect on three counts:

1. **The two formulas are definitions, not laws.** A law makes a non-trivial prediction about the world. $I_t = \Delta D / \Delta T$ defines a rate. $E_c = Q / (C \cdot T)$ defines a quality-adjusted productivity measure. Neither predicts anything that could be falsified independently of the definition itself.
2. **Borrowing physics rhetoric weakens credibility with technical reviewers.** Calling a definition a "law" invites attack on the dressing rather than evaluation of the substance.
3. **A protocol is what AI infrastructure actually needs.** TCP/IP, HTTP, and OpenTelemetry shape ecosystems precisely because they are protocols and not theories.

v3 removes the "Law" framing entirely. The same fundamentals remain, now positioned as what they are: **a measurement specification**.

---

## Foundational Stance

CTI commits to an explicit epistemological limit:

> *"CTI measures operationally verifiable cognitive transformations, not metaphysical truth."*

CTI does not attempt to prove consciousness, define absolute intelligence, or claim to understand subjective experience. CTI specifies how to measure observable cognitive behavior within operational systems.

---

## Specification 1 — Throughput Metric

**Definition.** The throughput of a decision system is the rate of validated decisions per unit time.

$$I_t = \frac{\Delta D}{\Delta T}$$

| Variable | Definition | Unit |
|---|---|---|
| $I_t$ | Throughput | events / time |
| $\Delta D$ | Count of validated Evaluable Cognitive Events in interval | count |
| $\Delta T$ | Interval duration | time |

**Operational consequence.** Under CTI, a system's measured cognition is the rate at which it produces decisions that pass a domain-specific validator — not the rate at which it produces outputs.

```
"Did it produce output?" → "Did it produce validated decisions, and how fast?"
```

**What CTI does not claim.** That $I_t$ is the only measure of cognition that matters, that throughput correlates with intelligence in any deep sense, or that any specific value of $I_t$ is universally good.

**What CTI does claim.** That $I_t$ is operationally definable, measurable in production, and useful for cross-system comparison once $\Delta D$ is operationalized per domain.

---

## Specification 2 — Efficiency Metric

**Definition.** The efficiency of a decision system is decision quality per unit cost per unit time, computed over a set of Evaluable Cognitive Events.

For a set of ECEs $E = \{e_1, \ldots, e_n\}$ in a measurement window:

$$E_c = \frac{\sum_{e \in E} Q(e)}{\sum_{e \in E} \text{cost}(e) \cdot \text{latency}(e)}$$

| Variable | Definition |
|---|---|
| $E_c$ | Efficiency |
| $Q(e)$ | Quality score of ECE $e$ (validator output, scalar form) |
| $\text{cost}(e)$ | The `cost` field of ECE $e$ |
| $\text{latency}(e)$ | The `latency` field of ECE $e$ |

**Operational consequence.** An efficient system maximizes decision quality while minimizing cost and latency. A system that produces more low-quality decisions does not improve $E_c$; a system that produces fewer high-quality decisions at low cost does.

**Relationship to $I_t$.** Specification 1 measures rate. Specification 2 measures quality-adjusted efficiency. Together they describe cognitive performance along two axes — how fast does a system decide, and how efficiently does it decide well.

---

## Primitive — The Evaluable Cognitive Event

**New in v3.1.** Specifications 1 and 2 operate over a formal primitive: the **Evaluable Cognitive Event (ECE)**.

$$\text{ECE} := \{\, \text{trigger}, \;\text{output}, \;\text{validator}, \;\text{cost}, \;\text{latency} \,\}$$

| Field | Required | Role |
|---|---|---|
| `trigger` | ✅ | The causal antecedent of the event |
| `output` | ✅ | The result produced |
| `validator` | ✅ | A function `(trigger, output) → score` that evaluates the output |
| `cost` | ✅ | Non-negative scalar — computational cost |
| `latency` | ✅ | Non-negative scalar — wall-clock duration |

An ECE is **only valid as a unit of CTI measurement when all five fields are populated**. The metric definitions are now:

- **Specification 1:** $\Delta D$ = count of ECEs in the window whose `validator` returned a truthy score
- **Specification 2:** $E_c$ = sum of validator scores divided by sum of `cost · latency` across ECEs

This primitive **closes Q1.3** ("What is the baseline unit of a decision?") — a question deliberately left open in v3.0.

The full type signature in TypeScript, JSON Schema, and Python, with examples across LLM, RL, and retrieval systems, is specified in [`/docs/primitives.md`](./docs/primitives.md).

### Why a Primitive

v3.0 used the word **decision** as the measurement unit. This worked as prose but failed as engineering:

- Polysemic: in an LLM, is a decision a token, a response, a tool-call, a reasoning step?
- Untyped: two implementations could not agree on $\Delta D$ without separate negotiation
- Unvalidatable: a validator needs structure, not vocabulary

The ECE has structure. Two implementations agreeing on the ECE schema agree on what is being measured.

### What Changes for Implementers

A system claiming CTI compliance must emit ECEs with all five fields. From a stream of ECEs, the protocol's measurement layer derives $I_t$ and $E_c$ directly. There is no separate "decision counter" to maintain.

The word **decision** remains valid informal vocabulary. Under the protocol, the measurable unit is the ECE.

---

## Formal Model of Cognition

CTI models a validated ECE as a contextual optimization problem under bounded rationality:

$$\underset{e}{\arg\max} \; \mathbb{E}[U(e) \mid I, C, R]$$

Subject to:

$$R_c < R_{max}$$

| Variable | Meaning |
|---|---|
| $U(e)$ | Expected contextual utility |
| $I$ | Available information |
| $C$ | Operational context |
| $R$ | Resource constraints |
| $R_c$ | Computational cost (corresponds to ECE `cost` field) |
| $R_{max}$ | Maximum allowable cost |

This is the bounded-rationality optimization familiar from Simon (1955) and standard in constrained MDPs. CTI does not claim originality on the formal model. CTI uses it as the foundation under Specifications 1 and 2, with explicit attribution.

Optimal cognition under CTI is **not** perfect cognition. It is **adaptively efficient under constraints**.

---

## Operational Definition of a Validated ECE

CTI defines a validated Evaluable Cognitive Event as:

> *"A cognitive event $e = \{trigger, output, validator, cost, latency\}$ whose causal effect advances a defined objective within an observable operational context, and whose `validator(trigger, output)` returns a truthy score."*

This definition is deliberately:

- **Causally grounded** — an ECE with no observable effect on system state is not validated under CTI
- **Operationally observable** — events that cannot be logged or measured are outside scope
- **Contextual** — utility is defined relative to a stated objective, not in the abstract
- **Type-checked** — the event has a formal signature, not a vocabulary

> *Closed in v3.1: the polysemy of "decision" identified in Q1.3 of v3.0 is resolved by the ECE primitive. See [`/docs/primitives.md`](./docs/primitives.md).*

---

## Philosophical Boundary

CTI explicitly excludes claims about consciousness, phenomenology, metaphysical intelligence, sentience, and absolute truth. CTI evaluates only observable operational behavior, measurable decision transformations, and reasoning systems under constraints.

| Domain | CTI Scope |
|---|---|
| Cognitive throughput | ✅ |
| Decision efficiency | ✅ |
| Operational validation | ✅ |
| Cognitive observability | ✅ |
| Consciousness | ❌ |
| Subjective experience | ❌ |
| Absolute truth | ❌ |

These exclusions are statements about what CTI is qualified to measure — not statements about what exists.

---

## The Conceptual Shift

**Traditional AI evaluation:**

```
input → output (correct/incorrect)
```

**Under CTI:**

```
state → cognitive transformation → contextual utility (measured operationally)
```

---

## What CTI Is Not

CTI is not a foundation model, an agent, a runtime, a prompt wrapper, a dashboard, or a benchmark suite.

## What CTI Is

- A **measurement specification** for AI decision systems
- An **open standard** governed by RFCs
- A **reference vocabulary** for cross-system comparison
- A **revisable protocol** — versioned, falsifiable, and adoption-driven

---

## Relationship to Prior Work

CTI is positioned alongside, and explicitly draws from:

- **Bounded rationality** (Simon, 1955) — the formal model is a direct application
- **Operationalism** in philosophy of science — define concepts by how they are measured
- **Rational analysis** (Anderson) — task-relative evaluation of cognition
- **AI observability infrastructure** — LangSmith, Helicone, Arize, Langfuse, AgentOps already occupy parts of the measurement plane CTI specifies; CTI proposes a vendor-neutral standard above them
- **Agent benchmarks** — AgentBench, GAIA, SWE-bench evaluate static performance; CTI is complementary, focused on runtime throughput and efficiency under real constraints

CTI does not claim originality on any of these foundations. CTI claims originality on the specific composition: a vendor-neutral protocol for runtime decision throughput and efficiency, with explicit philosophical boundaries.

---

## Open System Philosophy

CTI is an open specification, governed by RFCs. The goal is not proprietary control. The goal is to enable contribution from researchers, engineers, mathematicians, philosophers, cognitive scientists, systems architects, and open-source communities.

---

## Why This Matters

The next generation of AI systems will be evaluated less on raw capability and more on:

- Rate of useful decisions under real constraints
- Quality-adjusted cost efficiency
- Operational observability across heterogeneous stacks

CTI specifies how to measure all three.

---

## Roadmap

| Version | Focus | Status |
|---|---|---|
| v2.0.0 | "Laws" framing (deprecated) | Archived |
| v3.0.0 | Reframe as protocol; remove "Law" language | Released |
| **v3.1.0** | **Replace "decision" primitive with evaluable cognitive event** | **Current** |
| v3.2.0 | Reference implementation: $I_t$, $E_c$ across agentic LLM stacks | Planned |
| v3.3.0 | One falsifiable empirical claim on $E_c$ scaling | Planned |

---

## Open Research Directions

CTI opens multiple research lines:

1. Cognitive observability standards
2. Throughput metrics under heterogeneous architectures
3. Multi-agent optimization and attribution
4. Reasoning under constraints
5. Cognitive routing
6. Operational efficiency benchmarks
7. Contextual validation methodologies
8. Adaptive decision systems

→ See [`/research/open-questions.md`](./research/open-questions.md) for the full inventory.

---

## Open Invitation

CTI is designed to evolve publicly. Researchers, engineers, mathematicians, philosophers, cognitive scientists, systems architects, and open-source contributors are invited to **question, attack, improve, and extend** this specification.

---

## Closing Statement

CTI does not claim to be a theory of intelligence. It claims to be a measurement protocol — useful, falsifiable, and revisable.

v3.0.0 removed the "Law" framing. v3.1.0 replaces the informal "decision" with a typed primitive — the Evaluable Cognitive Event. Subsequent versions will add a reference implementation and at least one falsifiable empirical claim.

This is the beginning of a specification, not the end of a manifesto.

---

*CTI v3.1.0 — Licensed under [CC BY 4.0](./LICENSE)*
ding MANIFESTO.md…]()
