# Open Research Questions

This document tracks unresolved questions across the CTI framework. It is a living document — questions are added as the framework evolves, and closed when addressed by an accepted RFC or published research.

> **v3.0.0 note.** References to "First Law" and "Second Law" have been replaced with "Specification 1" and "Specification 2" to reflect the protocol reframing. The underlying questions are unchanged.

---

## Category 1: Measurement & Metrics

**Q1.1 — How is $\Delta D$ (validated decisions) operationalized empirically?**
Specification 1 requires counting validated decisions. What constitutes validation? Who validates? Is validation domain-specific or universal?

**Q1.2 — How is $Q$ (decision quality) measured formally?**
Specification 2 uses $Q$ as a scalar. Is quality binary, continuous, or multi-dimensional? How is it measured without circular definitions?

**Q1.3 — What is the baseline unit of a "decision"?**
In LLMs, is a decision a token? A sentence? A response? An action taken by an agent? How does granularity affect $I_t$?
> *Roadmap: v3.1 addresses this via the **evaluable cognitive event** primitive with type signature `{trigger, output, validator, cost, latency}`.*

**Q1.4 — Can $I_t$ and $E_c$ be measured in real-time without significant overhead?**
Measuring cognition at runtime introduces latency. How do we minimize the observability cost of the Cognitive Throughput Layer itself?

---

## Category 2: Formal Model

**Q2.1 — How is $U(D)$ (contextual utility) specified across domains?**
Utility in a medical diagnosis system is different from utility in a code generation system. Can a domain-agnostic $U(D)$ be defined, or is it always domain-specific?

**Q2.2 — How is $R_{max}$ (resource constraint) set in practice?**
The formal model requires $R_c < R_{max}$. Who sets this bound? Is it static or adaptive?

**Q2.3 — What is the minimum information $I$ for a valid decision?**
If a system makes a decision with near-zero information, can it still be "valid"? Is there a minimum information requirement?

**Q2.4 — How does the model extend to multi-agent settings?**
When decisions from multiple agents interact, how does the optimization problem change? Can $U(D)$ be aggregated across agents?

---

## Category 3: Cognitive Observability

**Q3.1 — What does a Cognitive Throughput Layer implementation look like?**
The CTI stack places a "Cognitive Throughput Layer" above compute. What does this mean architecturally? What interfaces does it expose?

**Q3.2 — Can cognitive observability be standardized across different model architectures?**
LLMs, RL agents, and symbolic systems make decisions differently. Can a single observability standard apply to all?

**Q3.3 — What are the minimal telemetry requirements for CTI compliance?**
If a system wants to be "CTI-observable," what must it expose? Latency? Decision logs? Cost per call? Quality rubric output?

---

## Category 4: Multi-Agent & Distributed Systems

**Q4.1 — How is cognitive throughput measured across a pipeline of agents?**
In a multi-agent system, $\Delta D$ may be produced by different agents. How do we aggregate or attribute throughput?

**Q4.2 — Does cognitive routing affect $I_t$?**
If a routing layer directs queries to different agents based on complexity, how does this impact the overall throughput metric?

**Q4.3 — Can two agents with different architectures be compared using CTI metrics?**
Is $I_t$ architecture-neutral? Or does comparing an LLM to an RL agent require normalization?

---

## Category 5: Adaptive Systems

**Q5.1 — How do CTI metrics change as a system learns or adapts?**
If $E_c$ improves over time, is that improvement measurable within the CTI framework?

**Q5.2 — Can CTI be used to detect cognitive degradation?**
If $I_t$ drops or $E_c$ decreases over time, does that signal a meaningful problem? What thresholds matter?

---

## Category 6: Philosophical & Foundational

**Q6.1 — Is "valid decision" the right unit of cognitive measurement?**
Could there be better primitives — actions, predictions, updates to internal state?

**Q6.2 — Does CTI's behavioral stance miss something important about cognition?**
By committing to external observation only, does CTI systematically ignore aspects of cognition that matter for building better systems?

**Q6.3 — What is the relationship between $I_t$ and traditional notions of intelligence?**
How does cognitive throughput relate to IQ, $g$-factor, or other existing constructs?

---

## Category 7: Empirical Validation

> *New in v3.0.0. These questions exist to drive CTI from manifesto toward instrument.*

**Q7.1 — Can $I_t$ and $E_c$ be computed and compared across leading agentic LLM stacks?**
Candidates: LangGraph, CrewAI, OpenAI Agents SDK, AutoGen. What does a comparable measurement protocol across them require?

**Q7.2 — Does $E_c$ scale linearly with model size in agentic tool-use tasks?**
A falsifiable hypothesis under investigation. If $E_c$ saturates or inverts beyond N parameters, the protocol surfaces a non-obvious empirical claim.

**Q7.3 — Can CTI metrics distinguish between architectures that achieve identical benchmark scores?**
If two systems score equally on AgentBench but differ in $E_c$, which is the more useful instrument for practitioners?

---

## How to Contribute

To address any of these questions:

1. Open a GitHub Discussion referencing the question number
2. Submit an RFC via [`/rfcs/RFC-0001-template.md`](../rfcs/RFC-0001-template.md)
3. Link published research in the relevant issue thread

When a question is resolved by an accepted RFC, it will be marked as **Closed** with a link to the resolution.

---

*Last updated: 2026 | Open questions: 25*
