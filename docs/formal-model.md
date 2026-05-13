# Formal Model of Cognitive Decision

---

## Overview

CTI models a valid decision as a **contextual optimization problem under bounded rationality.**

This model is the mathematical foundation underlying both metric specifications and the operational definition of a valid decision. It is a direct application of Simon's bounded-rationality framework (1955) and is structurally familiar from constrained Markov Decision Processes (MDPs) in reinforcement learning. CTI claims no originality on the model itself; it claims correctness in adopting it as the foundation under Specifications 1 and 2.

---

## Decision Flow

```mermaid
flowchart LR
    I[Information I] --> OPT
    C[Context C] --> OPT
    R[Resources R] --> OPT
    OPT{"Bounded Optimization<br/>argmax expected U of e<br/>subject to R_c &lt; R_max"} --> E["Cognitive Event e<br/>{trigger, output, validator,<br/>cost, latency}"]
    E --> EFF[Causal effect on system state]
    EFF --> V{validator e<br/>truthy?}
    V -->|yes| VALID[Validated ECE under CTI]
    V -->|no| INVALID[Unvalidated event]
    style OPT fill:#0a0a0a,stroke:#00d9ff,color:#ffffff,stroke-width:2px
    style E fill:#1a1a1a,stroke:#ffffff,color:#ffffff
    style VALID fill:#0a3d2e,stroke:#10b981,color:#ffffff
    style INVALID fill:#3d0a0a,stroke:#ef4444,color:#ffffff
    style V fill:#1a1a1a,stroke:#ffffff,color:#ffffff
    style I fill:#f5f5f5,stroke:#1a1a1a,color:#1a1a1a
    style C fill:#f5f5f5,stroke:#1a1a1a,color:#1a1a1a
    style R fill:#f5f5f5,stroke:#1a1a1a,color:#1a1a1a
    style EFF fill:#f5f5f5,stroke:#1a1a1a,color:#1a1a1a
```

A cognitive event flows from three inputs (information, context, resources) through a bounded optimization that respects cost constraints, produces a structured event $e = \{trigger, output, validator, cost, latency\}$, and is then evaluated by its own attached `validator`. Only events whose `validator` returns a truthy score qualify as **validated** under CTI.

See [`primitives.md`](./primitives.md) for the full specification of the Evaluable Cognitive Event.

---

## The Optimization Problem

A validated cognitive event is defined as:

> *"A state-transition operator that maximizes expected contextual utility under limited constraints of information and compute, and whose attached `validator` returns a truthy score."*

**Formally:**

$$\underset{e}{\arg\max} \; \mathbb{E}[U(e) \mid I, C, R]$$

**Subject to:**

$$R_c < R_{max}$$

---

## Variables

| Variable | Type | Meaning |
|----------|------|---------|
| $e$ | ECE | The cognitive event being evaluated (see [`primitives.md`](./primitives.md)) |
| $U(e)$ | Function | Expected contextual utility of event $e$ |
| $I$ | Context | Available information at event time |
| $C$ | Context | Operational context (goals, environment, state) |
| $R$ | Constraint | Resource constraints (time, compute, memory) |
| $R_c$ | Scalar | Actual computational cost incurred (corresponds to the `cost` field of $e$) |
| $R_{max}$ | Scalar | Maximum allowable resource cost |

---

## Key Properties

### 1. Bounded Rationality

The constraint $R_c < R_{max}$ explicitly encodes **bounded rationality**. The model assumes that no system operates with unlimited resources or perfect information.

This means:

- Optimal cognition under CTI is **not** perfect cognition
- It is **adaptively efficient** given available resources
- An event made with limited information that maximizes $\mathbb{E}[U(e) \mid I, C, R]$ within $R_{max}$ — and whose `validator` returns truthy — is a **validated ECE** under the protocol

### 2. Contextual Utility

$U(e)$ is **context-dependent**. Utility is not absolute. An event is evaluated by its effect within a specific operational context $C$, not by abstract standards.

### 3. Causal Grounding

A validated ECE must produce a **causal effect** that advances a defined objective. An event with no measurable effect on system state does not qualify as validated under CTI.

---

## Operational Definition of a Validated ECE

CTI defines a validated Evaluable Cognitive Event as:

> *"A cognitive event $e = \{trigger, output, validator, cost, latency\}$ whose causal effect advances a defined objective within an observable operational context, and whose `validator(trigger, output)` returns a truthy score."*

This definition is deliberately:

- **Free of metaphysical claims** — no appeal to absolute truth or consciousness
- **Free of domain-specific semantics** — applicable across reasoning systems, agents, and pipelines
- **Anchored to observability** — non-observable transformations are out of scope
- **Type-checked** — the event has a formal signature, not a vocabulary

> **Closed in v3.1.** The polysemy of "decision" identified in Q1.3 is now resolved by the **Evaluable Cognitive Event** primitive in [`primitives.md`](./primitives.md).

---

## Relationship to the Two Specifications

The formal model underpins both metric specifications:

- **Specification 1** ($I_t = \Delta D / \Delta T$): $\Delta D$ counts ECEs that satisfy $\arg\max_e \mathbb{E}[U(e) \mid I, C, R]$ within $R_c < R_{max}$ **and** whose `validator` returns truthy
- **Specification 2** ($E_c = \sum Q(e) / \sum (\text{cost}(e) \cdot \text{latency}(e))$): $Q(e)$ corresponds to the validator score of $e$; $\text{cost}(e)$ and $\text{latency}(e)$ are fields of $e$, corresponding to $R_c$ and the temporal component respectively

---

## Prior Art

This model is not new. It is the standard form of:

- Bounded rationality (Simon, 1955)
- Constrained MDPs in reinforcement learning
- Decision-theoretic agent models in classical AI
- Cost-aware planning in operations research

CTI's contribution is not the model. CTI's contribution is the **explicit adoption** of this model as the foundation for a vendor-neutral measurement protocol on AI decision systems.

---

## Open Questions

1. How is $U(e)$ specified across domains? (See Q2.1)
2. How is $R_{max}$ set in practice — statically, adaptively, by the operator, by the system? (See Q2.2)
3. What is the minimum information $I$ for an event to qualify as validated? (See Q2.3)
4. How does the model extend to multi-agent settings where events interact? (See Q2.4)
5. Can the model be implemented as a real-time monitoring layer without measurement-induced latency? (See Q1.4 and Q3.1)

---

*Propose extensions or challenges via the [RFC process](../rfcs/RFC-0001-template.md).*
[formal-model.md](https://github.com/user-attachments/files/27735948/formal-model.md)

