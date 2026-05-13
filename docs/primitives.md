# CTI Primitives — The Evaluable Cognitive Event

> *The atomic unit of measurement under the CTI protocol.*

**Status:** Stable since v3.1.0
**Closes:** Q1.3 (open-questions.md)

---

## Why a Primitive

v3.0.0 of CTI used the word **decision** as the unit of measurement under both metric specifications. This worked as prose but failed as engineering:

- "Decision" is polysemic. In an LLM, is a decision a token, a response, a tool-call, a reasoning step?
- "Decision" has no type signature. Two implementations cannot agree on $\Delta D$ without a separate negotiation.
- "Decision" cannot be validated by a machine. A validator needs structure, not vocabulary.

v3.1.0 replaces **decision** with a formal primitive: the **Evaluable Cognitive Event** (ECE). Specifications 1 and 2 are now defined over ECEs, not decisions. The change is breaking but unavoidable.

---

## Definition

An **Evaluable Cognitive Event (ECE)** is the atomic unit observed and measured under the CTI protocol. Every ECE carries five required fields:

```
ECE := { trigger, output, validator, cost, latency }
```

| Field | Type | Required | Semantics |
|---|---|---|---|
| `trigger` | structured value | ✅ | The input, prompt, state, or signal that initiated the event. Establishes causal antecedent. |
| `output` | structured value | ✅ | The result produced by the event. Must be inspectable. |
| `validator` | function `(trigger, output) → score` | ✅ | A pure function returning a validation score. Score domain is defined per implementation. Minimum: boolean (`valid` / `not valid`). Extended: scalar in `[0, 1]` or rubric vector. |
| `cost` | non-negative scalar | ✅ | Computational cost incurred to produce `output` from `trigger`. Unit defined per implementation (tokens, FLOPs, monetary cost, composite). |
| `latency` | non-negative scalar | ✅ | Wall-clock duration between trigger receipt and output emission. Unit: seconds (recommended). |

An ECE is **only valid as a unit of CTI measurement when all five fields are populated**. Missing any field disqualifies the event from contributing to $I_t$ or $E_c$.

---

## Type Signatures

### TypeScript

```typescript
type ECE<TTrigger = unknown, TOutput = unknown> = {
  trigger: TTrigger;
  output: TOutput;
  validator: (trigger: TTrigger, output: TOutput) => number | boolean;
  cost: number;     // non-negative
  latency: number;  // non-negative, seconds
};
```

### JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "EvaluableCognitiveEvent",
  "type": "object",
  "required": ["trigger", "output", "validator_ref", "cost", "latency"],
  "properties": {
    "trigger": { "description": "Causal antecedent of the event" },
    "output": { "description": "Result produced by the event" },
    "validator_ref": {
      "type": "string",
      "description": "Identifier of the validator function applied to (trigger, output)"
    },
    "cost": { "type": "number", "minimum": 0 },
    "latency": { "type": "number", "minimum": 0 }
  }
}
```

> When serialized, `validator` is replaced by `validator_ref` — a stable identifier that points to the validator definition. Functions are not serializable; references are.

### Python (dataclass)

```python
from dataclasses import dataclass
from typing import Any, Callable, Union

@dataclass
class ECE:
    trigger: Any
    output: Any
    validator: Callable[[Any, Any], Union[bool, float]]
    cost: float          # non-negative
    latency: float       # non-negative, seconds

    def is_valid(self) -> bool:
        result = self.validator(self.trigger, self.output)
        return bool(result) if isinstance(result, bool) else result > 0
```

---

## Field Semantics

### `trigger`

The causal antecedent. May be:

- A prompt or message (LLM systems)
- A state observation (RL agents)
- An event from a queue (orchestrated systems)
- A function call with arguments (tool-using agents)

The trigger establishes the **what came before** of the event. Without it, the event has no observable causal context.

### `output`

The result of the event. Must be inspectable by the validator. Common forms:

- A generated text completion
- A chosen action from an action space
- A tool invocation with arguments
- A structured response (JSON, function call, etc.)

### `validator`

The most important field. A pure function with signature:

```
validator: (trigger, output) → score
```

The score domain is implementation-defined. CTI specifies three canonical forms:

| Form | Score Type | When to Use |
|---|---|---|
| **Boolean** | `bool` | Binary validity (passes/fails) |
| **Scalar** | `float ∈ [0, 1]` | Rubric-scored quality |
| **Vector** | `float[] ∈ [0, 1]^n` | Multi-dimensional rubric |

For Specification 1 ($I_t = \Delta D / \Delta T$), an ECE contributes to $\Delta D$ if and only if its validator returns a truthy / non-zero / non-empty score.

For Specification 2 ($E_c = Q / (C \cdot T)$), the validator score **is** $Q$ (scalar form) or a function over the score vector (vector form).

### `cost`

Non-negative scalar representing the computational cost incurred. CTI does not mandate a unit, but recommends:

- **For LLM systems:** total token count (input + output), or monetary cost in fixed currency
- **For RL agents:** wall-clock compute time or FLOPs
- **For hybrid systems:** composite weighted by stakeholder priorities

The chosen unit must be **consistent within a measurement context** for cross-system comparison to be meaningful.

### `latency`

Wall-clock duration in seconds from trigger receipt to output emission. This is the operational latency observed by the system using the cognitive component, not internal microbenchmarks.

---

## Relationship to Specifications 1 and 2

With ECEs as the primitive, the metric definitions become:

### Specification 1 — Throughput Metric (revised)

$$I_t = \frac{\Delta D}{\Delta T}$$

Where:

$$\Delta D = \left| \{\, e \in \text{ECE}_{[t, t+\Delta T]} : \text{validator}(e) \text{ truthy} \,\} \right|$$

In words: $\Delta D$ is the count of ECEs in the measurement window whose validator returned a truthy score.

### Specification 2 — Efficiency Metric (revised)

For a set of ECEs $E = \{e_1, e_2, \ldots, e_n\}$ in a measurement window:

$$E_c = \frac{\sum_{e \in E} Q(e)}{\sum_{e \in E} \text{cost}(e) \cdot \text{latency}(e)}$$

Where $Q(e)$ is the validator score of event $e$ in scalar form, and $\text{cost}(e)$, $\text{latency}(e)$ are the corresponding fields.

This formulation makes the metrics directly computable from any sequence of well-formed ECEs.

---

## Examples

### Example 1 — LLM tool-using agent

```python
ECE(
  trigger = {"user_message": "Get weather for Tokyo and book a meeting room"},
  output  = [
    {"tool": "get_weather", "args": {"city": "Tokyo"}},
    {"tool": "book_room",   "args": {"room": "A1", "time": "14:00"}}
  ],
  validator = lambda t, o: all(call["tool"] in REGISTERED_TOOLS for call in o),
  cost    = 1432,    # tokens consumed
  latency = 2.341    # seconds
)
```

### Example 2 — RL agent action

```python
ECE(
  trigger = observation_vector,
  output  = action_choice,
  validator = lambda obs, act: env_simulator.step(obs, act).reward,
  cost    = 0.012,   # GPU-seconds
  latency = 0.008    # seconds
)
```

### Example 3 — Information retrieval

```python
ECE(
  trigger = {"query": "What is bounded rationality?"},
  output  = retrieved_documents,
  validator = lambda q, docs: relevance_rubric(q, docs),  # returns float in [0,1]
  cost    = 0.04,    # USD
  latency = 0.156    # seconds
)
```

In all three examples, the same five-field structure makes the events directly comparable under Specifications 1 and 2, even though the underlying systems differ entirely.

---

## What This Primitive Does Not Capture

ECE is the **minimum** structure required for CTI measurement. It deliberately does **not** include:

| Excluded Field | Reason |
|---|---|
| `agent_id` | Multi-agent attribution is the subject of a future RFC |
| `parent_event_id` | Causal chains and dependencies are an extension |
| `confidence` | Self-reported confidence is not part of the validation contract |
| `intermediate_states` | CTI is behavioral, not introspective (see philosophy.md) |
| `metadata` | Implementation-specific; not part of the core protocol |

Extensions adding optional fields will be specified through the RFC process and must not break the five required fields.

---

## On the Word "Decision"

The word **decision** has not been banned from CTI prose. It remains useful as informal vocabulary. But under the protocol, the **measurable unit** is an Evaluable Cognitive Event. When precision matters — in implementation, telemetry, comparison, or RFC discussion — use **ECE**.

A decision under CTI is an ECE whose validator returned a truthy score. Nothing more, nothing less.

---

## Closing Q1.3

This document closes the open question Q1.3 from `research/open-questions.md`:

> *"What is the baseline unit of a 'decision'?"*

The answer: an Evaluable Cognitive Event, with the type signature specified above.

---

## Related Documents

- [`/docs/protocol.md`](./protocol.md) — Specifications 1 and 2, revised over ECEs
- [`/docs/formal-model.md`](./formal-model.md) — Bounded-rationality model in ECE terms
- [`/research/open-questions.md`](../research/open-questions.md) — Q1.3 marked closed
- [`/rfcs/RFC-0001-template.md`](../rfcs/RFC-0001-template.md) — Propose ECE extensions here

---

*The primitive is stable. Extensions are versioned.*
[primitives.md](https://github.com/user-attachments/files/27735817/primitives.md)
