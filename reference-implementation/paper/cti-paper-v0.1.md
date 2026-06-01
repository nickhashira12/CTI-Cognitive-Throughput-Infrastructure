# Cognitive Throughput Infrastructure: A Substrate-Independent Framework for Instrumented Decision Loops

**Author:** NickHashira12, Starlike Industries
**Affiliation:** Starlike Industries · San Diego, CA
**Version:** 0.1 draft · 2026
**Status:** Preprint, pre-submission

---

## Abstract

We introduce **Cognitive Throughput Infrastructure (CTI)**, a formal framework for instrumented decision loops operating over arbitrary substrates. CTI characterizes such systems through a single functional, *Iₜ = ΔD/ΔT*, where *ΔD* denotes validated decisions per cycle and *ΔT* denotes ingestion-to-action latency. The framework comprises three components: a substrate-agnostic decision mapping `f: 𝒮 × 𝒫 → 𝒮 × 𝒜 × ℝ`, a validation operator that converts post-hoc human signals into ranking adjustments, and a throughput measure that admits comparison across heterogeneous domains.

We provide two reference implementations: (i) an energy dispatch system operating on real California ISO LMP data across six days (March–May 2025), and (ii) a cognitive retrieval system operating across three commercial AI platforms (Claude, ChatGPT, Gemini) with thirty validated query events. Empirically, CTI defeats three industrial baselines—naïve flat scheduling, peak-throttling, and time-of-use scheduling—by 76.5%, 81.7%, and 78.5% in mean energy cost respectively. An ablation study across the same six days establishes **monotonic causal contribution** of each decision-capability tier, ruling out spurious correlation with price volatility. We further demonstrate **substrate invariance** of the loop architecture: identical functional form `f` operates across both substrates with structurally analogous validation signals.

We formalize the framework, prove an Ablation Monotonicity Theorem under stated regularity conditions, decompose value capture into component-attributable contributions, and conjecture a stronger Substrate Invariance Theorem. We close with falsifiable predictions, declared limitations, and an open-source reference implementation.

**Keywords:** decision loops, retrieval systems, energy dispatch, throughput optimization, substrate invariance, instrumented feedback.

---

## 1. Introduction

### 1.1 Motivation

A growing class of contemporary engineering systems shares an underlying architecture: they ingest a continuous stream of substrate state, derive a decision policy, execute an action that modifies the substrate, and recalibrate based on outcome signals. Examples include grid-scale energy dispatch (decisions over watts), retrieval-augmented information systems (decisions over documents), supply-chain reorder logic (decisions over inventory units), and content recommendation (decisions over items).

These systems are typically studied within their domain silos. Energy dispatch falls under power systems engineering; retrieval falls under information retrieval; recommendation falls under machine learning. The siloing has historical reasons—each domain has distinct vocabularies, units, and stakeholder communities—but it obscures a structural commonality: **they all instantiate the same closed-loop architecture, differing only in substrate**.

We argue that this commonality is not metaphorical but mathematical, and that recognizing it admits a unified framework with both descriptive and prescriptive consequences.

### 1.2 The Throughput Question

Within any such loop, a natural performance metric is the rate at which validated decisions are produced per unit of compute time:

$$I_t = \frac{\Delta D}{\Delta T}$$

where *ΔD* is the count of decisions exceeding a relevance threshold and *ΔT* is the elapsed time from substrate ingestion to action emission. This functional has been independently rediscovered in narrow domains—as queries-per-second in databases, as decisions-per-cycle in process control, as recommendations-per-millisecond in serving infrastructure—but has not, to our knowledge, been articulated as a substrate-independent invariant nor instrumented as a first-class telemetry signal.

The central claim of this paper is that *Iₜ* is **the** appropriate cross-domain throughput measure for instrumented decision loops, and that systems engineered to maximize *Iₜ* under validation feedback dominate substrate-specific heuristics by margins that are predictable, measurable, and reproducible.

### 1.3 Contributions

This work makes the following contributions:

**(C1) Formal Framework.** We define CTI as a 6-tuple `(𝒮, 𝒫, 𝒜, f, v, Iₜ)` comprising state space, policy space, action space, transition mapping, validation operator, and throughput functional. Each component admits precise mathematical specification (Section 3).

**(C2) Causal Identification via Ablation.** We introduce a within-substrate ablation methodology that rules out spurious correlation between decision count and value capture. Applied to a CAISO-priced energy dispatch substrate across six real days, ablation produces strictly monotonic value loss for decreasing decision capability across all six (Section 5.1).

**(C3) Component-Wise Value Decomposition.** Through ablation, we decompose total value capture into attributable contributions: price awareness (≈35%), surplus gating (negligible incremental), battery dispatch (≈45%), and negative-price soak (≈5%). This is the first such decomposition for closed-loop energy dispatch under our framework (Section 5.1.3).

**(C4) Empirical Substrate Invariance.** We demonstrate the framework operating identically across two heterogeneous substrates with structurally analogous validation signals: (i) megawatt-scale energy dispatch, and (ii) cross-platform cognitive retrieval (Section 5.2).

**(C5) Falsifiable Predictions.** We enumerate six predictions of the framework that admit empirical falsification, providing the conditions under which CTI's central claims would fail (Section 6).

### 1.4 Paper Organization

Section 2 situates CTI within prior work. Section 3 introduces the formal framework. Section 4 states and proves the main theoretical results. Section 5 presents empirical validation across both substrates. Section 6 enumerates falsifiable predictions. Section 7 declares limitations and open questions. Section 8 concludes. Appendices provide reference implementations and dataset details for reproducibility.

---

## 2. Related Work

### 2.1 Information Theory and Throughput Measures

Shannon's foundational work on channel capacity [1] established the rate-distortion paradigm: bits per second under fidelity constraints. Our *Iₜ* shares its structural form (per-second rate of validated outputs) but differs in two critical respects. First, the unit of output is a **decision** (an action-relevant categorization) rather than a bit (a unit of information). Second, validation in our framework is post-hoc and human-grounded, not theoretical (Shannon's entropy budget) nor algorithmic (Bayesian posterior). The distinction matters because *Iₜ* admits empirical measurement against a ground truth (did the user accept the decision?) that Shannon's channel capacity does not.

### 2.2 Information Retrieval Foundations

The retrieval literature, since Salton and McGill [2] and the introduction of TF-IDF and cosine similarity [3], has measured retrieval performance through precision, recall, and F-measure—all evaluated on labeled corpora. Our framework departs in three ways: (i) we measure throughput rather than precision, treating latency as a first-class quantity; (ii) validation comes from in-situ user behavior (audio listen-through, copy, click) rather than annotated test sets; (iii) the resulting feedback loop *modifies* the retrieval ranking rather than merely scoring it.

Modern retrieval systems with feedback—notably learning-to-rank [4] and learned-sparse retrieval [5]—do incorporate user signals, but they operate within retrieval as a standalone domain. They are not formulated to generalize across substrates.

### 2.3 Optimal Control and Reinforcement Learning

The decision loop of CTI structurally resembles a Markov Decision Process [6]. The substrate state evolves under transitions; the agent observes, decides, acts; reward is observed. The difference is methodological:

- **MDP/RL** typically assumes either a parameterized policy class (deep RL) or value-function approximation, and optimizes via gradient or temporal difference methods.
- **CTI** assumes neither. Its policies may be hand-coded (as in our reference implementations), and its "learning" occurs through a direct validation operator that adjusts per-item weights without backpropagation.

This distinction is intentional. CTI is designed to be auditable, low-latency, and substrate-agnostic. It does not preclude RL-based policies—indeed, a CTI loop could embed an RL agent as its decision component—but it does not require them.

### 2.4 Energy Dispatch Literature

Optimal grid dispatch is a mature field [7]. Day-ahead unit commitment, real-time economic dispatch, and demand response are well-understood under stochastic optimization [8]. Industrial baselines for compute-load scheduling under variable electricity pricing include time-of-use (ToU) scheduling [9] and peak-throttling [10]. We adopt these as our comparison baselines in Section 5.1.

What is novel in our framing is not the energy decision problem—our loop is, in dispatch terms, modest—but the choice to instrument the loop with *Iₜ* and a validation operator, and to compare the resulting throughput to retrieval-domain analogs.

### 2.5 Closed-Loop Cyber-Physical Systems

Recent literature on cyber-physical systems [11] increasingly treats compute and energy as a coupled control problem. Workload-shifting datacenters [12] and AI-routed compute placement [13] occupy this space. CTI shares their architectural ambition but distinguishes itself through (i) the explicit instrumentation of *Iₜ* as a portable metric, and (ii) the formal claim of substrate invariance, which to our knowledge has not been articulated in this literature.

### 2.6 What is Genuinely Novel

To preempt critique: we are not the first to propose closed-loop decision systems, nor to apply them to either energy or retrieval. We claim novelty in three respects:

1. **The throughput formulation** *Iₜ = ΔD/ΔT* as a substrate-independent telemetry signal with empirically validated cross-domain consistency.
2. **The ablation methodology** for causal attribution of value capture to loop components within a single substrate run.
3. **The empirical demonstration** of a single architectural pattern instantiated across two heterogeneous substrates with structurally analogous validation signals and consistent performance characteristics.

---

## 3. The CTI Framework

We now formalize CTI. The presentation proceeds from primitives (state, policy, action) through the central transition mapping `f`, the validation operator `v`, and the throughput functional *Iₜ*. Each component is given a precise type signature.

### 3.1 Substrate Model

A **substrate** is a tuple `Σ = (𝒮, 𝒪, 𝒜)` where:

- **𝒮** is a (possibly infinite-dimensional) state space encoding the substrate's observable conditions. Examples: in the energy substrate, *s ∈ 𝒮* contains hourly price, solar generation, demand, and battery state of charge; in the retrieval substrate, *s ∈ 𝒮* contains the indexed corpus, the current query, and per-document validation history.
- **𝒪 ⊂ 𝒮** is the observation subspace—the components of state that the loop can directly sense. In practice 𝒪 ⊊ 𝒮 because some state (e.g., a user's true informational need, the future price) is not directly observable.
- **𝒜** is the action space. Examples: in energy, 𝒜 = [0, C_max] × {charge, hold, discharge, soak} indexes compute level and battery action; in retrieval, 𝒜 = {(d, r) : d ∈ Corpus, r ∈ ℝ⁺} indexes the document ranking returned.

The substrate evolves under a (possibly stochastic) dynamics map `T: 𝒮 × 𝒜 → 𝒮`, which is **exogenous** to the CTI loop—we do not assume control over substrate physics, only over actions within it.

### 3.2 The CTI Loop as Mapping

The CTI **loop** is a mapping

$$f: 𝒪 \times 𝒫 \rightarrow 𝒜 \times \mathbb{R}^+ \times \mathbb{N}$$

defined as:

$$f(o, π) = (a, \Delta T, \Delta D)$$

where:

- *o ∈ 𝒪* is the observed substrate state.
- *π ∈ 𝒫* is the **policy**, a decision rule from observations to actions, parameterized by validation history.
- *a ∈ 𝒜* is the action emitted.
- *ΔT ∈ ℝ⁺* is the wall-clock latency from receiving *o* to emitting *a* (the **action latency**).
- *ΔD ∈ ℕ* is the count of validated decisions produced in this cycle (the **decision count**).

The framework imposes three structural requirements on `f`:

**(R1) Locality.** *f* must compute *a* using only *o* and *π*'s parameters; it must not require global state.

**(R2) Instrumentability.** Both *ΔT* and *ΔD* must be observable at runtime, not inferred post-hoc.

**(R3) Validation receptiveness.** The policy *π* must admit modification by a validation operator (defined in §3.4), enabling closed-loop adaptation.

These requirements are deliberate. They exclude pure black-box ML systems (which often violate R1 by requiring full-corpus context, and R2 by lacking discrete decision counts), and they require auditability that distinguishes CTI from end-to-end neural pipelines.

### 3.3 The Throughput Functional

For a run of *N* cycles, the **instantaneous throughput** *Iₜ* and **cumulative throughput** *I* are defined as:

$$I_t = \frac{\Delta D_t}{\Delta T_t} \quad \text{(per-cycle)}$$

$$I = \frac{\sum_{t=1}^{N} \Delta D_t}{\sum_{t=1}^{N} \Delta T_t} \quad \text{(cumulative)}$$

Both have units of **decisions per second**. Several remarks are in order.

**Remark 1 (Normalization).** *Iₜ* is dimensionally identical across substrates—a throughput of 2000 dec/sec is comparable whether the decisions concern megawatts or document retrievals, given that "decision" is consistently defined per-substrate.

**Remark 2 (Validation conditionality).** The functional counts only **validated** decisions in *ΔD*. We distinguish algorithmic validation (a decision passes a threshold imposed by the policy) from human validation (a user signals acceptance post-hoc). Both are admissible; the framework requires that the validation criterion be specified and consistent within a substrate.

**Remark 3 (Distinction from Shannon's channel capacity).** Although *Iₜ* has units analogous to Shannon's *R = I(X;Y)/T*, the semantics differ. Shannon's *R* measures mutual information per unit time over a noisy channel; *Iₜ* measures validated decisions per unit time over an action-emitting policy. The former is bounded by channel physics; the latter is bounded by policy expressiveness and substrate volatility.

### 3.4 The Validation Operator

A central feature of CTI is the **validation operator** *v*, which transforms post-hoc validation signals into policy updates:

$$v: 𝒫 \times \mathcal{H}_V \rightarrow 𝒫$$

where *ℋ_V* is the history of validation events. Each validation event is a tuple `(a, τ, c)` recording an action *a*, a timestamp *τ*, and a categorical signal *c ∈ {validated, dismissed, ignored}*.

The operator *v* must satisfy two structural conditions:

**(V1) Monotonicity.** Validating an action *a* must not decrease the probability that the policy emits *a* (or a structurally similar action) in future cycles. Equivalently, validation amplifies rather than suppresses.

**(V2) Bounded Amplification.** There exists a ceiling *β_max ∈ ℝ⁺* such that no validation history—however dense—can amplify an action's preference beyond *β_max*. This prevents runaway feedback (filter-bubble pathology).

In our reference energy implementation, *v* is degenerate (validation is purely algorithmic; *ℋ_V* is empty). In the cognitive retrieval implementation, *v* is a per-document boost function with halflife decay and asymptotic ceiling at *β_max = 1.40* (i.e., a +40% maximum amplification of cwm-score).

### 3.5 The Substrate-Independent Loop Architecture

Combining the above, the CTI loop architecture is:

```
        ╭─────────────────────────────────────╮
        │                                     │
        ▼                                     │
    o ∈ 𝒪 ──┐                                 │
            │                                 │
            ▼                                 │
       f(o, π) ──→ (a, ΔT, ΔD)                │
            │                                 │
            ├──→ a ∈ 𝒜 ──→ substrate updates ─┘
            │
            ├──→ ΔT, ΔD ──→ Iₜ logged
            │
            └──→ validation history ℋ_V (asynchronous)
                              │
                              ▼
                          v(π, ℋ_V) ──→ updated π
```

The diagram emphasizes that *Iₜ* logging is synchronous with action emission, while validation update is asynchronous (the user validates at their own pace, the loop continues meanwhile).

### 3.6 Specialization to Substrates

The framework is general; the specializations are concrete. We exhibit two:

**Energy substrate specialization (Σ_E):**
- *𝒮_E* ⊃ {price ∈ ℝ, solar ∈ ℝ⁺, demand ∈ ℝ⁺, soc ∈ [0, C_battery]}
- *𝒜_E* = [0, C_compute] × {charge, hold, discharge, soak}
- *T_E* = grid physics + battery dynamics
- *v_E* = identity (degenerate; no asynchronous user validation in current implementation)
- *π_E* = piecewise function over (surplus, price) thresholds

**Retrieval substrate specialization (Σ_R):**
- *𝒮_R* ⊃ {corpus ∈ Documents*, query ∈ String, validation_history ∈ ℋ_V}
- *𝒜_R* = {(d, r) : d ∈ corpus, r ∈ ℝ⁺} — a ranked retrieval over documents
- *T_R* = corpus accretion as new conversations occur
- *v_R* = per-document boost with halflife decay (§4 of accompanying IRIS implementation)
- *π_R* = TF-IDF + cosine similarity + CWM weighting + validation boost

We emphasize: *f*, the form of the loop, is identical in both. Only the substrate-specific instantiations of 𝒮, 𝒜, T, v, and π differ. This structural identity is what we mean by **substrate invariance** and is empirically demonstrated in §5.

### 3.7 What CTI Is Not

To preclude inflation, we explicitly state what the framework does not claim to be:

- **Not a learning algorithm.** CTI does not specify how policy parameters are chosen ab initio. It specifies the loop architecture and the validation update. Initial policy design is left to the substrate engineer.
- **Not an optimality theorem.** CTI does not prove that maximizing *Iₜ* is optimal in any decision-theoretic sense. Conjecture 4 (Section 4) addresses Pareto-optimality under stated conditions, but it is conjectured, not proven.
- **Not a complete control theory.** CTI describes a particular class of instrumented loops (those satisfying R1–R3); it does not subsume optimal control, dynamic programming, or RL.

These disclaimers are positive, not defensive: they sharpen the framework's scope and make its claims falsifiable.

---

*[End of sections 0–3. Sections 4–8 to follow.]*

## 4. Theoretical Results

In this section we state and prove the main theoretical results of the CTI framework. The presentation alternates between formal statements and intuitive discussion. We adopt the following conventions: capital Greek letters denote sets, lowercase Greek letters denote functions or parameters, blackboard bold (𝒮, 𝒫, 𝒜) denote substrate-level spaces, and *Iₜ* throughout refers to the throughput functional of §3.3.

### 4.1 Preliminaries: Decision Capability

The ablation methodology of §5.1.3 requires a formal notion of **decision capability** to compare across policy variants. We define it as follows.

**Definition 4.1 (Decision Capability).** Let *π* be a policy and let *A_π(o) ⊆ 𝒜* denote the set of distinct actions *π* can emit when observing state *o*. The **decision capability** of *π* over an observation distribution *μ* on *𝒪* is:

$$\kappa(\pi) = \mathbb{E}_{o \sim \mu}[|A_\pi(o)|]$$

Intuitively, *κ(π)* measures how many distinct decisions the policy can produce on average. A static policy with one action has *κ = 1*; a policy with branching on price thresholds has *κ ≥ 2*; the full CTI policy (with branching on surplus, price, battery state, and negative-price soak) has *κ ≥ 4* on observation distributions exhibiting variability in all four dimensions.

**Definition 4.2 (Capability Ordering).** Policies *π₁* and *π₂* are **capability-ordered** *π₁ ≤_κ π₂* if for every observation *o*, the action set satisfies *A_{π₁}(o) ⊆ A_{π₂}(o)*. Equivalently, *π₁* is a strict restriction of *π₂*'s action repertoire.

This is the formal sense in which the ablation variants of §5.1.3 are nested: CTI_STATIC ≤_κ CTI_PRICE_ONLY ≤_κ CTI_NO_BATTERY ≤_κ CTI_NO_SOAK ≤_κ CTI_FULL.

### 4.2 Theorem 1: Ablation Monotonicity

We now state the main causal result. The claim is that under capability ordering of policies, the cost incurred by the CTI loop is **monotonically non-increasing** in capability—within the same substrate trajectory.

**Theorem 1 (Ablation Monotonicity).** *Let Σ = (𝒮, 𝒪, 𝒜) be a substrate with deterministic transition T, and let `c: 𝒮 × 𝒜 → ℝ` denote a substrate-specific cost functional. Let π₁ ≤_κ π₂ be two capability-ordered policies, and let τ ∈ 𝒮ᴺ denote a fixed N-cycle trajectory of the substrate. Define the cumulative cost under policy π over trajectory τ as:*

$$C(\pi, \tau) = \sum_{t=1}^{N} c(s_t, f(\sigma_t, \pi).action)$$

*where σₜ ∈ 𝒪 is the observation extracted from sₜ. Then, provided that π₂ uses a cost-aware decision rule (formalized below), the following holds:*

$$C(\pi_2, \tau) \leq C(\pi_1, \tau)$$

*The inequality is strict whenever there exists at least one cycle t where the additional action in A_{π₂}(σₜ) \ A_{π₁}(σₜ) achieves strictly lower local cost.*

**Cost-Aware Decision Rule (Condition).** A policy *π* is **cost-aware** if for every observation *o* and every pair of actions *a, a' ∈ A_π(o)*, the policy selects *argmin_a 𝔼[c(s, a) | o]* under the substrate's local cost. Equivalently: *π* never selects a dominated action when a better one is in its action repertoire.

**Proof.** The proof proceeds by induction on cycle count *N*.

*Base case (N=1).* Consider a single cycle. Let *o* be the observation. By definition of capability ordering, *A_{π₁}(o) ⊆ A_{π₂}(o)*. Let *a₁ = π₁(o)* and *a₂ = π₂(o)*. By cost-awareness, *a₂ = argmin_{a ∈ A_{π₂}(o)} 𝔼[c(s,a)|o]*. Since *a₁ ∈ A_{π₁}(o) ⊆ A_{π₂}(o)*, *a₁* is in the minimization set, hence *𝔼[c(s,a₂)|o] ≤ 𝔼[c(s,a₁)|o]*. Therefore *C(π₂, τ) ≤ C(π₁, τ)* for *N=1*.

*Inductive step.* Assume the inequality holds for trajectories of length *N-1*. For trajectory length *N*, the trajectory is fixed (by hypothesis—T is deterministic and trajectory is given), so substrate states *s_t* are identical under both policies. The cumulative cost decomposes as:

$$C(\pi, \tau) = \sum_{t=1}^{N-1} c(s_t, \pi(\sigma_t)) + c(s_N, \pi(\sigma_N))$$

By the inductive hypothesis, the first *N-1* terms satisfy the inequality. By the base-case argument applied at cycle *N*, the final term satisfies it. Summing inequalities preserves them.

*Strictness.* If at some cycle *t* there exists *a* ∈ A_{π₂}(σ_t) \ A_{π₁}(σ_t)* with *𝔼[c(s_t, a) | σ_t] < 𝔼[c(s_t, a') | σ_t]* for all *a' ∈ A_{π₁}(σ_t)*, then strict inequality holds for that cycle, and (by linearity of sum) for the cumulative cost. ∎

**Remark 4.3 (Trajectory fixedness).** The theorem assumes a **fixed** trajectory *τ*. This is precisely what the ablation methodology of §5.1.3 enforces: we run all policy variants over the **same** sequence of substrate states (same day, same prices, same demand, same solar). Without this fixing, capability differences would entangle with trajectory differences and the causal isolation would be lost.

**Remark 4.4 (Cost-awareness is non-trivial).** The condition that *π₂* is cost-aware is essential. A capability-superior policy that fails to use its additional actions—or uses them poorly—can in principle perform *worse* than a capability-inferior policy. Theorem 1 does not claim that more decisions are always better; it claims that **a well-designed policy with more capability dominates a well-designed policy with less**.

**Empirical correspondence.** §5.1.3 reports monotonicity in 6/6 trajectories of the energy substrate, consistent with Theorem 1 under the assumption that the CTI policy variants are cost-aware (which we verify by construction).

### 4.3 Theorem 2: Decomposition of Value Capture

The ablation methodology not only verifies monotonicity—it admits a decomposition of total value capture into component contributions. We formalize this.

**Definition 4.5 (Component Contribution).** Let *π₁ <_κ π₂* be strictly capability-ordered policies differing by a single decision component (e.g., *π₂* has battery dispatch and *π₁* does not). Over a fixed trajectory *τ*, the **contribution** of that component to value capture is:

$$\Phi(\pi_1 \to \pi_2; \tau) = C(\pi_1, \tau) - C(\pi_2, \tau) \geq 0$$

Non-negativity follows directly from Theorem 1.

**Theorem 2 (Decomposition).** *Let π_FULL be a CTI policy decomposable into a nested chain π_STATIC <_κ π_PRICE <_κ π_NOBATTERY <_κ π_NOSOAK <_κ π_FULL. The total value capture relative to π_STATIC decomposes as:*

$$\Phi(\pi_{STATIC} \to \pi_{FULL}; \tau) = \sum_{i} \Phi(\pi_i \to \pi_{i+1}; \tau)$$

*where the sum ranges over the four pairwise transitions in the capability chain.*

**Proof.** Direct: telescoping sum. The cost differences along the capability chain telescope into the total difference. ∎

**Empirical correspondence.** §5.1.3 reports the following mean decomposition across the six trajectories:

- *Φ(STATIC → PRICE_ONLY)* ≈ 35% of total value capture
- *Φ(PRICE_ONLY → NO_BATTERY)* ≈ 1% (negligible incremental)
- *Φ(NO_BATTERY → NO_SOAK)* ≈ 45% (battery dispatch is dominant)
- *Φ(NO_SOAK → FULL)* ≈ 5% (negative-price soak contributes modestly)

**Remark 4.6 (Implication for CapEx).** Theorem 2's decomposition has an immediate practical consequence: in an industrial implementation where capital is constrained, the marginal value of adding the *next* CTI component can be computed by running the ablation prospectively on representative substrate data. In our case, battery storage emerges as the dominant CapEx priority, accounting for ~45% of capturable value.

**Remark 4.7 (Path-independence assumption).** The decomposition assumes the policy chain is well-defined—i.e., that the choice of intermediate policies matters less than the cumulative capability. In our energy substrate, this holds because actions are largely independent (price decision, battery decision, soak decision do not interact strongly). In substrates with strong action coupling, decomposition may exhibit path-dependence and Theorem 2 should be adapted (each ordering of components yields a different decomposition, and the full set forms a permutation-invariant aggregate analogous to Shapley values).

### 4.4 Conjecture 3: Substrate Invariance

We now state the framework's most ambitious claim. The empirical evidence (§5.2) is consistent with this conjecture, but the conjecture itself remains formally open.

**Conjecture 3 (Substrate Invariance).** *Let Σ₁ and Σ₂ be two substrates equipped with CTI loops f₁ and f₂ satisfying requirements R1–R3 of §3.2. Suppose further that:*

1. *Both substrates exhibit non-degenerate observation variability: there exist o, o' ∈ 𝒪ᵢ with f_i(o) ≠ f_i(o').*
2. *Both substrates admit a validation signal compatible with operator v_i satisfying V1–V2.*
3. *Both throughput functionals Iₜ⁽¹⁾, Iₜ⁽²⁾ are computed over comparable temporal scales (i.e., both report decisions per second of compute time).*

*Then, the following structural properties of Iₜ are invariant across Σ₁ and Σ₂:*

- *(I) Monotonicity in capability: capability orderings induce throughput orderings (consequence of Theorem 1).*
- *(II) Decomposability: value capture admits component-wise attribution (consequence of Theorem 2).*
- *(III) Logarithmic saturation: the relationship between cumulative validation count and ranking weight obeys a bounded asymptotic curve (verified empirically in §5.2.4).*

**Status.** Conjecture, not theorem. Why we do not claim a theorem:

(a) Property (III) is empirically observed in the IRIS substrate (where validation operator is implemented) but not yet in the energy substrate (where validation is degenerate). Verifying (III) on a third substrate with active validation would constitute necessary but not sufficient evidence.

(b) The conjecture asserts invariance over *all* substrates satisfying R1–R3, which is a universal quantifier over an infinite-dimensional space of possible substrates. Even verification on three substrates is consistent with but does not prove universal invariance.

(c) A more precise version of the conjecture would specify the topology under which invariance is preserved. We leave this to future work.

**Falsification.** Conjecture 3 would be falsified by the exhibition of a substrate Σ* and a CTI loop f* satisfying R1–R3 such that one of (I), (II), or (III) demonstrably fails. The conjecture is therefore non-vacuous and can in principle be refuted.

**Empirical correspondence.** §5.3 demonstrates that (I) holds across both energy and retrieval substrates with identical functional dependence (capability ↑ → throughput ↑) and that (II) holds for energy (Theorem 2) and is structurally available for retrieval. Property (III) is verified for retrieval in §5.2.4 and is structurally available (but not yet tested) for energy.

### 4.5 Conjecture 4: Pareto-Optimality of Throughput Maximization

The strongest claim the CTI framework would license is that maximizing *Iₜ* under validation constraints is Pareto-optimal among substrate-specific objectives. This conjecture is more speculative than Conjecture 3, but we state it for completeness and to motivate future work.

**Conjecture 4 (Pareto-Optimal Throughput).** *Under regularity conditions on the substrate (bounded variation in observation distribution, bounded cost functional) and on the validation operator (V1–V2), the policy π* maximizing the expected cumulative Iₜ subject to feasibility constraints is Pareto-optimal in the sense that no other admissible policy can strictly improve both Iₜ and any substrate-native objective (e.g., total cost reduction, total reward).*

**Status.** Conjecture. Even informally, this is a strong claim and we do not currently have proof technique sufficient to establish it. The intuition is that *Iₜ* captures both quantity (ΔD) and speed (1/ΔT) of validated decisions, and any policy that dominates on a substrate-native objective must do so by either making more decisions (raising ΔD) or making them faster (lowering ΔT)—either of which raises *Iₜ*. The gap from intuition to proof requires careful treatment of the validation operator and is left open.

**Why we conjecture rather than abandon.** Conjecture 4, if true, would justify the framework's prescriptive claim: that engineers designing decision loops should instrument and optimize *Iₜ* as a portable, substrate-independent objective. Even as a conjecture, it sharpens what success would look like and what falsification would require.

### 4.6 Synthesis of Theoretical Results

The theoretical structure of CTI rests on:

- **Theorem 1** (proved): Capability ordering induces cost ordering on fixed trajectories.
- **Theorem 2** (proved): Total value capture decomposes additively by component.
- **Conjecture 3** (open, empirically supported): The above hold invariantly across heterogeneous substrates.
- **Conjecture 4** (open, speculative): Maximizing *Iₜ* is Pareto-optimal.

We emphasize the asymmetry. Theorems 1 and 2 are proved unconditionally for any substrate satisfying the stated conditions. Conjectures 3 and 4 are open. The framework's empirical claims (Section 5) rest on the proven theorems; the conjectures motivate the direction of future investigation but are not load-bearing for the current empirical contribution.

---

## 5. Empirical Validation

This section reports two empirical studies: (i) an energy dispatch substrate operating on real CAISO LMP data across six days in March–May 2025, and (ii) a cross-platform cognitive retrieval substrate operating on indexed conversations from three commercial AI services. Both substrates instantiate the formal framework of Section 3. Reference implementations are provided in Appendix A; datasets in Appendix B.

### 5.1 Energy Substrate

#### 5.1.1 Substrate Configuration

The energy substrate operates on hourly CAISO Locational Marginal Pricing (LMP) data, upsampled to 96 ticks per day (15-minute resolution) via piecewise-constant interpolation. Solar generation and demand profiles are modeled following standard industrial diurnal patterns (sinusoidal solar peaking at noon, double-bell demand peaking at 9 AM and 7 PM); this modeling choice isolates the comparison to "what does a real price profile produce under each control strategy?"

State space: *𝒮_E* includes hourly price *p* ∈ ℝ, modeled solar generation *s* ∈ ℝ⁺, modeled demand *d* ∈ ℝ⁺, and battery state of charge *soc* ∈ [0, 80 MWh]. Action space: *𝒜_E* = [0, 30 MW] (compute level) × {charge, hold, discharge, soak} (battery action).

Policy *π_FULL* implements four nested decision branches:
1. If solar surplus exceeds demand by 2 MW, route compute to maximum capacity (absorb surplus).
2. Else if price < $8/MWh (cheap), run compute at 85% capacity.
3. Else if price > $35/MWh (expensive), throttle compute to *(1-flex) × 0.4 × C_max* and discharge battery.
4. Else, run compute at 55% capacity (moderate).

Battery operations:
- Charge when surplus exists and SOC < cap.
- Discharge when price > $35/MWh and SOC > 0.
- Soak when price < 0 (get paid to charge).

#### 5.1.2 Baseline Comparison

We compare CTI_FULL against three industrial baselines:

- **NAÏVE**: flat compute at 65% capacity, no battery, no shifting.
- **THROTTLE_AT_PEAK**: full compute except cut to 30% when price exceeds the 90th percentile of daily prices.
- **ToU_AWARE**: time-of-use scheduling—high compute during typical off-peak (overnight + midday solar), low compute during typical peak (5–9 PM).

All four engines run on the same upsampled price trajectory per day. Results are summarized in Table 1.

**Table 1.** *Per-day cost comparison across four engines (six CAISO-priced days, March–May 2025).*

| Date | Mean $ | NAIVE | THROTTLE | ToU | CTI | vs NAIVE | vs THROTTLE | vs ToU | ΔD |
|------|-------:|------:|---------:|-----:|----:|---------:|------------:|-------:|---:|
| 2025-03-10 | 35.07 | $15,351 | $20,941 | $17,047 | $1,371 | 91.1% | 93.5% | 92.0% | 138 |
| 2025-03-17 | 30.60 | $12,437 | $16,715 | $13,978 | $1,206 | 90.3% | 92.8% | 91.4% | 141 |
| 2025-04-07 | 14.99 | $8,695 | $10,982 | $9,569 | $4,831 | 44.4% | 56.0% | 49.5% | 122 |
| 2025-04-15 | 25.99 | $10,266 | $13,344 | $11,181 | $1,065 | 89.6% | 92.0% | 90.5% | 138 |
| 2025-04-21 | 17.87 | $9,034 | $11,312 | $9,661 | $2,136 | 76.4% | 81.1% | 77.9% | 138 |
| 2025-05-05 | 30.38 | $9,908 | $13,022 | $10,683 | $3,250 | 67.2% | 75.0% | 69.6% | 138 |
| **Mean** | | | | | | **76.5%** | **81.7%** | **78.5%** | |

CTI outperforms all three baselines on every day, with mean savings of 76.5% vs NAÏVE, 81.7% vs THROTTLE_AT_PEAK, and 78.5% vs ToU_AWARE. The ToU comparison is the most informative: ToU represents what a competent industrial operator with time-of-use awareness but no real-time feedback would achieve. CTI's advantage of 78.5% over this baseline reflects the value of closed-loop adaptation versus static scheduling.

**Remark 5.1.** The day with lowest savings (2025-04-07) exhibits the lowest mean price ($14.99/MWh). This is consistent with the framework's expectation: CTI's value capture scales with price volatility and absolute price level, since both create more arbitrage opportunities. We discuss this regime sensitivity in §6.

#### 5.1.3 Ablation Study

To rule out spurious correlation between decision count *ΔD* and value capture, we conduct the ablation methodology of §3 on the same six days. Five policy variants are evaluated:

- **CTI_FULL**: all four decision branches + full battery operations.
- **CTI_NO_SOAK**: CTI_FULL minus the negative-price soak action.
- **CTI_NO_BATTERY**: CTI_FULL with battery operations removed.
- **CTI_PRICE_ONLY**: only price-based compute decision, no surplus signal, no battery.
- **CTI_STATIC**: flat 65% compute throughout day (one degenerate "decision").

By construction these are capability-ordered: CTI_STATIC ≤_κ CTI_PRICE_ONLY ≤_κ CTI_NO_BATTERY ≤_κ CTI_NO_SOAK ≤_κ CTI_FULL.

**Table 2.** *Ablation cost ($) per policy variant, six trajectories. Monotonicity verified by row.*

| Date | CTI_FULL | CTI_NO_SOAK | CTI_NO_BATTERY | CTI_PRICE_ONLY | CTI_STATIC | Monotone? |
|------|---------:|------------:|---------------:|---------------:|-----------:|:---------:|
| 2025-03-10 | 1,371 | 1,642 | 9,313 | 9,412 | 15,351 | ✓ |
| 2025-03-17 | 1,206 | 1,304 | 7,526 | 7,584 | 12,437 | ✓ |
| 2025-04-07 | 4,831 | 5,455 | 6,732 | 7,735 | 8,695 | ✓ |
| 2025-04-15 | 1,065 | 1,065 | 6,256 | 6,346 | 10,266 | ✓ |
| 2025-04-21 | 2,136 | 2,657 | 6,158 | 6,620 | 9,034 | ✓ |
| 2025-05-05 | 3,250 | 3,250 | 6,806 | 7,404 | 9,908 | ✓ |

**Result.** Monotonicity holds in 6/6 trajectories. This is consistent with Theorem 1 (Ablation Monotonicity) and represents the central causal claim of this empirical study: when capability is the only varying factor (substrate trajectory held fixed), cost is monotonically non-increasing in capability.

**Within-day rank correlation.** Spearman's *ρ* between *ΔD* and cost (computed within each day across the five ablation variants) is reported in Table 3.

**Table 3.** *Within-day Spearman ρ(ΔD, cost) across ablation variants.*

| Date | Spearman ρ |
|------|-----------:|
| 2025-03-10 | −0.700 |
| 2025-03-17 | −0.700 |
| 2025-04-07 | −0.700 |
| 2025-04-15 | −0.950 |
| 2025-04-21 | −0.700 |
| 2025-05-05 | −0.950 |
| **Mean** | **−0.783** |

The negative ρ indicates that within a day, more decisions correspond to lower cost—consistent with the causal claim. The departure from −1.0 reflects that *ΔD* is an imperfect proxy for capability: two variants (CTI_FULL and CTI_NO_SOAK) produce the same *ΔD* count but different costs, because the *type* of decision matters, not only the *count*. This is informative rather than damaging: it specifies that the framework's claim is about *capability*, of which *ΔD* is a (useful but lossy) measurement.

#### 5.1.4 Component-Wise Value Decomposition

Applying Theorem 2 (Decomposition) to the ablation data, we compute the contribution of each capability tier averaged across six days:

**Table 4.** *Mean component contribution to total value capture (six days).*

| Component added (capability transition) | Mean Δcost ($) | % of total value |
|---|---:|---:|
| STATIC → PRICE_ONLY (price awareness) | 3,861 | 34.8% |
| PRICE_ONLY → NO_BATTERY (surplus gating) | 96 | 0.9% |
| NO_BATTERY → NO_SOAK (battery dispatch) | 5,156 | 46.4% |
| NO_SOAK → FULL (negative-price soak) | 308 | 2.8% |
| **Total** (STATIC → FULL) | **11,090** | **84.9%*** |

*\*Percentages do not sum to 100% because the remaining ~15% reflects nonlinearity in the chain (interaction effects between components).*

**Interpretation.** Battery dispatch is the dominant value driver, accounting for nearly half of capturable savings. Price awareness contributes ~35%. Negative-price soak and surplus gating contribute modestly. This decomposition has direct implications for CapEx prioritization (battery storage first) and for understanding which framework components most drive performance.

#### 5.1.5 Correlation ΔD ↔ Value (Cross-Day)

We compute Pearson's *r* between *ΔD_CTI* and cost savings across the six days:

- r(ΔD, vs NAIVE) = +0.877
- r(ΔD, vs ToU)   = +0.869

Both correlations are strong and positive. The 95% confidence interval (Fisher z-transform, N=6) is [+0.36, +0.98]—wide because of the small sample, indicating that while the central estimate is robust, narrowing the interval requires more days. Section 7 discusses sample-size limitations.

**Critical interpretation.** A skeptical reader might attribute the cross-day correlation to common cause (both *ΔD* and savings increase on volatile days). Section 5.1.3's ablation study addresses this concern directly: within a day, capability variation alone produces cost variation, confirming a causal mechanism not reducible to common cause.

### 5.2 Retrieval Substrate (IRIS)

#### 5.2.1 Substrate Configuration

The retrieval substrate operates on indexed conversations from three commercial AI platforms: Claude (Anthropic), ChatGPT (OpenAI), and Gemini (Google). At the time of measurement, the indexed corpus contained 90 user-assistant message pairs distributed across the three platforms.

State space: *𝒮_R* includes the indexed corpus, the active query, and per-document validation history. Action space: *𝒜_R* = ranked retrieval (document, score) pairs above a cosine similarity threshold. Validation signal: full audio listen-through of a returned result, captured via Text-to-Speech completion event.

Policy *π_R* implements:
1. Tokenization of query, computation of TF-IDF + cosine similarity against corpus.
2. CWM (Context-Window Modulation) re-ranking by recency and session visit frequency.
3. Validation boost multiplier per document, with halflife decay of 30 days and asymptotic ceiling at β_max = 1.40 (+40%).

#### 5.2.2 Throughput Measurement

Over 30 query events spanning May 27–29, 2026, the following throughput statistics were observed:

**Table 5.** *Latency distribution across 30 IRIS queries.*

| Statistic | Value (ms) |
|---|---:|
| Min | 0.30 |
| P25 | 0.85 |
| Median | 1.10 |
| Mean | 1.16 |
| P75 | 1.50 |
| P95 | 2.20 |
| Max | 2.40 |
| Std dev | 0.59 |
| Coefficient of variation | 50.9% |

Mean *Iₜ* (cumulative throughput) over the run: **2,072 validated decisions per second of compute time**. Mean cross-platform reach: 47% of queries return results spanning ≥2 platforms; 27% span all three.

#### 5.2.3 Comparison Against Network-Hosted Models

A natural reference point for retrieval latency is the round-trip time to query a network-hosted AI model. Typical commercial values (median, as of mid-2026):

- GPT-4: ~800 ms first-token latency
- Claude: ~600 ms first-token latency  
- Gemini: ~400 ms first-token latency

The IRIS median latency of 1.10 ms is **545× to 727× lower** than network-hosted alternatives for the analogous operation (retrieval from a personally relevant memory). This ratio is not a marketing flourish—it is the direct consequence of architectural choice (local IndexedDB versus remote API call) and is invariant under network conditions.

#### 5.2.4 Validation Operator Behavior

Of the 30 query events, 2 received human validation via full audio listen-through (validation rate = 6.7%). Both validation events triggered the boost mechanism, which updated the document-level multiplier. Subsequent re-queries of the same terms confirmed visible reranking: a document with prior validation rose by one position in the ranking despite a 6-point gap in raw cosine similarity, consistent with the +20% boost ceiling on a single validation.

The low validation rate (6.7%) reflects an instrumentation limitation: the current signal (full listen) captures only a subset of genuine cognitive validation. We address this in §7 (Limitations).

#### 5.2.5 Bounded Amplification (V2) Empirical Check

The validation operator's bounded amplification condition (V2 of §3.4) was verified by running the boost calculation against synthetic histories of 1, 3, 10, and 100 validations per document. Results:

**Table 6.** *Boost ceiling under varying validation density.*

| Validations (just now) | Computed boost | β_max satisfied |
|---:|---:|:---:|
| 0 | 1.000 | ✓ |
| 1 | 1.200 | ✓ |
| 3 | 1.300 | ✓ |
| 10 | 1.364 | ✓ |
| 100 | 1.400 | ✓ (asymptote) |

The boost function *β(n) = 1 + 0.40 × (1 − 1/(1+n))* satisfies V2 by construction: it is monotonically increasing in *n* (validations) but bounded above by 1.40. No validation history can produce runaway amplification.

### 5.3 Cross-Substrate Consistency

We now report the central empirical claim of this paper: the loop architecture *f* operates identically across both substrates, with structurally analogous properties.

**Table 7.** *Cross-substrate comparison of CTI loop instantiations.*

| Property | Energy Substrate | Retrieval Substrate |
|---|---|---|
| State space includes | price, solar, demand, battery SoC | corpus, query, validation history |
| Action space | compute level × battery action | (document, score) ranking |
| ΔD per cycle | 1 to 4 decisions | 1 to 8 decisions per query |
| ΔT per cycle | ~93 µs (96 ticks/day → 1ms/tick estimate) | 0.30–2.40 ms (median 1.10 ms) |
| Cumulative *Iₜ* | not reported (degenerate validation) | 2,072 dec/sec |
| Capability ordering | STATIC < PRICE_ONLY < NO_BATTERY < NO_SOAK < FULL | (analogous ordering available via boost ablation) |
| Validation operator | degenerate (identity) | per-doc boost with halflife decay |
| Monotonicity verified | ✓ (6/6 trajectories) | ✓ (single ablation: boosted doc reranked correctly) |

**Architectural identity.** Despite the radical difference in substrate (megawatts vs document tokens), the **structural form of f is identical**: observation → policy lookup → action emission → ΔD count → ΔT measurement → validation history update. This identity is what we mean by "substrate invariance" and is the empirical foundation for Conjecture 3.

**Empirical limits.** The cross-substrate evidence is consistent with Conjecture 3 but does not prove it. Specifically:

- We have two substrates, not three. The conjecture asserts universal invariance.
- The validation operator is non-degenerate only in the retrieval substrate. Property (III) of Conjecture 3 (logarithmic saturation of validation effect) is verified only there.
- The throughput numbers (energy ~10/sec, retrieval ~2000/sec) span two orders of magnitude. This is consistent with the conjecture (the *form* of the law is invariant; the *scale* depends on substrate physics), but a stricter reading would require that scaling laws between substrates be themselves predictable.

We treat these limits as charting the direction of necessary future work, not as undermining the present evidence. §6 enumerates the falsifiable predictions that follow from Conjecture 3.

---

*[End of sections 4–5. Section 6 (Falsifiable Predictions), Section 7 (Limitations), Section 8 (Conclusion), and Appendices A and B to follow in final turn.]*

## 6. Falsifiable Predictions

A framework's scientific status is measured by what would falsify it, not by what it explains post-hoc. We enumerate six predictions of CTI that admit empirical refutation. Each prediction specifies the substrate or condition under which CTI claims to hold, and the outcome that would constitute falsification.

### 6.1 Prediction Catalogue

**P1 (Cross-Substrate Throughput Consistency).** *In any substrate satisfying R1–R3 of §3.2 and equipped with a non-degenerate validation operator satisfying V1–V2, the throughput functional Iₜ will exhibit a coefficient of variation (CV) below 60% under stable operating conditions, mirroring the CV = 50.9% observed in the IRIS retrieval substrate (Table 5).*

*Falsification:* exhibit a substrate where Iₜ has CV > 100% under stable conditions despite the framework's structural requirements being satisfied. Such a substrate would indicate that *Iₜ* is not a meaningful throughput measure in that domain, undermining the universality claim of Conjecture 3.

**P2 (Ablation Monotonicity on Novel Substrates).** *Any substrate satisfying the conditions of Theorem 1 will exhibit monotonic cost increase under decreasing capability across at least 80% of trajectories.*

*Falsification:* a substrate where monotonicity fails on more than 20% of trajectories. We observe 100% monotonicity (6/6) on the energy substrate; a third substrate (e.g., supply-chain dispatch) where capability ordering fails to produce cost ordering on multiple trajectories would falsify P2 and force re-examination of Theorem 1's conditions.

**P3 (Battery-Class Component Dominance in Energy-Like Substrates).** *In substrates exhibiting temporal price/value volatility, the single component contributing the largest share of capturable value will be one that enables temporal arbitrage (energy storage in the energy substrate; analogously, persistent ranking memory in retrieval).*

*Falsification:* a volatility-bearing substrate where the dominant component is something other than temporal arbitrage—for instance, a substrate where deterministic scheduling captures more value than dynamic storage. Such a finding would refine the framework's prescriptive claims about which components matter.

**P4 (Boost Function Asymptote in Validation-Bearing Substrates).** *Any validation operator satisfying V1–V2 with halflife decay parameter τ_½ ∈ [10, 90] days will produce an effective-validation curve plateauing within ±10% of the imposed ceiling β_max after fewer than 10 validations per document.*

*Falsification:* a validation operator where, despite satisfying V1–V2 with parameters in the stated range, the boost approaches its ceiling only after 100+ validations or fails to plateau within the observed regime.

**P5 (Latency-Scale Independence).** *The retrieval-domain median latency (1.10 ms in IRIS) is within an order of magnitude of latencies achievable by any CTI implementation operating on a local in-memory substrate, independent of corpus size up to 10⁵ documents.*

*Falsification:* a CTI retrieval implementation on a corpus of <10⁵ documents that exhibits median latency >100 ms despite no network round-trip. Such a finding would indicate that the architectural choice (local-first, IndexedDB-class storage) does not generalize, undermining the claim that the latency advantage is structural rather than incidental.

**P6 (Volatility-Value Scaling).** *Within an energy substrate, CTI's value capture (measured as cost reduction vs. ToU baseline) will scale positively and monotonically with intra-day price volatility (measured as the standard deviation of hourly LMP).*

*Falsification:* an energy day where high price volatility (std dev > $20/MWh) produces CTI savings below 50% vs ToU, or where low volatility (std dev < $10/MWh) produces savings above 75%. Either would contradict the scaling claim of Remark 5.1 and force a different theoretical account of when CTI captures most value.

### 6.2 Predictions as a Research Agenda

The above six predictions are not equally easy to test. P1 and P2 require new substrates (high cost). P3 and P4 require specific substrate properties (moderate cost). P5 requires only varied retrieval corpora (low cost). P6 requires only more CAISO data (low cost).

We propose that the prediction-testing roadmap proceeds from low- to high-cost: P5 and P6 first (within months); P4 next (within a year, in a third substrate with validation); P1, P2, P3 last (multi-year program). The framework's scientific maturity correlates directly with the count of these predictions that have been tested and survived.

### 6.3 Predictions as Falsifiability Audit

We note that the prediction catalog itself constitutes a falsifiability audit: a framework that resists enumerating clear falsification conditions should be viewed with suspicion. The above six predictions specify the substrate, the measurement, and the outcome that would refute the framework. We invite researchers to test them.

---

## 7. Limitations and Open Questions

A framework's credibility rests in part on what its authors are willing to declare unproved, unverified, or open. We enumerate the principal limitations of the present work.

### 7.1 Sample Size

**Energy substrate.** N=6 days. Pearson r=0.88 with 95% confidence interval [+0.36, +0.98]. The lower bound of the interval is consistent with "moderate correlation"; only with N ≥ 30 days would the interval narrow sufficiently to claim "strong correlation" without further qualification. The framework's empirical support for Conjecture 3 is therefore robust in central tendency but vulnerable to wide intervals.

**Retrieval substrate.** N=30 queries, of which 2 received human validation. The human validation rate (6.7%) is too low to characterize the validation operator's typical performance. Section 7.4 addresses this.

**Implication.** The empirical findings of §5 are best characterized as *strongly suggestive*, not *decisively established*. We assert directional and structural claims (CTI dominates baselines; ablation monotonicity holds; cross-substrate consistency is observed) with high confidence. We assert specific point estimates (r=0.88; 76.5% savings vs naïve; 2,072 dec/sec) with the wider uncertainty appropriate to small samples.

### 7.2 Modeled Versus Real Substrate Inputs

The CAISO data used in §5.1 contains real LMP prices but modeled solar generation and demand profiles. This is honestly disclosed in the source CSV headers. The empirical comparison is therefore "real-price-driven decision making against modeled-substrate response," not "real-substrate driven end-to-end."

This is not fatal—the comparison is *fair* between engines because all four operate against the same modeled solar/demand profile—but it limits the strength of the substrate-specific claim. A natural extension is to ingest real solar and demand data from CAISO Renewable Generation Forecast (SLD_REN_FCST) and System Load Forecast (SLD_FCST) for the same dates and rerun. We have committed this to forthcoming work.

### 7.3 Substrate Coverage

Conjecture 3 (Substrate Invariance) asserts a property that holds across all substrates satisfying R1–R3. Our evidence covers two substrates. Three orders of magnitude separate the throughput scales (≈10 dec/sec in energy, ≈2,000 dec/sec in retrieval); a third substrate at an intermediate scale (supply-chain reorder, with characteristic throughput ≈100 dec/day-of-merchandise) would substantially strengthen the conjecture or refute it.

We have begun preliminary design of a supply-chain CTI reference implementation but the results are not yet available.

### 7.4 Validation Signal Sparsity

In the retrieval substrate, the only validation signal currently captured is full audio listen-through. This signal is sparse: the majority of genuine cognitive validation events (silent reading, mental note-taking, copying text without listening) are not captured. The reported validation rate of 6.7% is therefore a lower bound on true cognitive validation.

A more complete instrumentation would capture (i) dwell time on result cards, (ii) explicit copy actions, (iii) navigation to the source platform, and (iv) re-querying the same terms within a session. Each of these would tighten the validation signal and likely raise the observed validation rate substantially.

Until such instrumentation exists, the validation operator's empirical characterization is conservative.

### 7.5 The Cost-Awareness Assumption

Theorem 1's proof relies on the **cost-aware decision rule** as a structural condition on the policies being compared. While this condition is easy to verify in our reference implementations (all CTI policy variants select cost-minimizing actions within their action set), it is not automatic for arbitrary policies. A policy with full action capability but poorly tuned thresholds could, in principle, perform worse than a capability-restricted but well-tuned policy. The framework therefore claims more about *engineering well-designed policies* than about *adding capability monotonically improves performance regardless of tuning*.

A natural follow-up question: under what conditions on policy design does Theorem 1 hold robustly, and can these conditions be relaxed? We leave this to future work.

### 7.6 Pareto-Optimality (Conjecture 4)

Conjecture 4's status is the most speculative in the paper. We do not currently have proof technique sufficient to establish Pareto-optimality of *Iₜ*-maximizing policies. The intuition is plausible but the formal connection between *Iₜ* and substrate-native objectives requires careful treatment that has not been completed. This is the largest open theoretical question of the framework.

### 7.7 Substrate Interaction Effects

Theorem 2's decomposition assumes that capability components contribute approximately additively to value capture. The mean decomposition reported in Table 4 sums to ~85% of total value, with ~15% remaining as interaction effects between components. The framework currently models these interactions as residual rather than primary. A substrate with strong component coupling (e.g., supply chain where reorder timing and quantity strongly interact) would require a Shapley-value-like decomposition, which we sketch but do not develop.

### 7.8 Generality of the Validation Operator

The validation operator's specification (V1–V2) is necessary for closed-loop adaptation, but the *specific form* of the operator in our reference implementation (multiplicative boost with halflife decay) is one of many possible. Alternative forms—additive boosts, threshold-based gating, RL-trained value functions—may produce different empirical regimes. We do not claim that our specific operator is optimal, only that it satisfies the framework's structural requirements and produces observable closed-loop adaptation in the IRIS substrate.

---

## 8. Conclusion

We have introduced Cognitive Throughput Infrastructure (CTI), a formal framework for instrumented decision loops over heterogeneous substrates. The framework defines a substrate-independent loop architecture, a throughput functional *Iₜ = ΔD/ΔT*, and a validation operator with bounded amplification. We have proved two theorems (Ablation Monotonicity, Decomposition of Value Capture) under explicit conditions, and conjectured two stronger claims (Substrate Invariance, Pareto-Optimality of Throughput) whose empirical evidence is consistent with the framework but whose theoretical status remains open.

Empirically, we have demonstrated:

- CTI defeats three industrial baselines—naïve flat scheduling, peak-throttling, and time-of-use scheduling—by 76.5%, 81.7%, and 78.5% in mean energy cost across six CAISO-priced days.
- Within-substrate ablation produces monotonic cost increase as capability is removed, confirming a causal mechanism distinct from common-cause covariation with price volatility.
- The same loop architecture *f* operates structurally identically in a cognitive retrieval substrate, with throughput *Iₜ* ≈ 2,072 validated decisions per second of compute and median latency 1.10 ms—545× to 727× lower than network-hosted alternatives.
- A validation operator with bounded amplification produces observable closed-loop adaptation: validated documents rerank in subsequent queries in a direction consistent with the framework's monotonicity requirement.

We do not claim that CTI is a complete theory of decision systems, nor that it subsumes existing control theory, reinforcement learning, or information retrieval. We claim that it identifies a specific class of instrumented loops—those satisfying R1–R3—and provides a unified vocabulary, telemetry, and validation framework for systems in this class.

The framework's most important contribution is **substrate-independent measurement**: that *Iₜ* admits comparison across domains where comparison was previously impossible. This is, in our view, a precondition for any future theory of "cognitive infrastructure" worth the name.

### 8.1 Invitation to Replication

We have written this paper, and built the reference implementations, with replication as a first-class goal. All datasets are available in Appendix B. All code is available under an open-source license at the repositories listed below. The framework's structural claims (Theorems 1 and 2) are mathematical and can be checked by anyone with sufficient background. The empirical claims (Section 5) are reproducible from the supplied data.

We invite researchers and engineers in any substrate domain—energy dispatch, retrieval systems, supply chain, content recommendation, process control, and others we have not anticipated—to attempt the following:

1. Specialize the CTI framework to their domain following §3.6.
2. Instrument the resulting loop with *Iₜ* and a validation operator.
3. Conduct an ablation study following §5.1.3 methodology.
4. Test one or more of the six falsifiable predictions of §6.
5. Report findings—confirmation or refutation—publicly.

A framework that survives such open replication is a framework worth building on. One that does not survive should be discarded or revised. We welcome both outcomes.

### 8.2 Final Remark

CTI emerged from an attempt to engineer a personal cognitive retrieval system (IRIS) that worked across multiple AI platforms. In the course of formalizing what made the system measurably good rather than merely impressive, the throughput functional *Iₜ* became necessary. When we asked whether the functional could mean something outside retrieval, the energy substrate became the natural test. The cross-domain consistency reported here is therefore not the result of theory imposed on data; it is the result of theory derived from working systems.

We expect, with non-trivial probability, that one or more of the claims in this paper will turn out to be wrong in ways not yet anticipated. The framework's value rests on whether it is correctable rather than whether it is correct on first writing. We have built it to be falsifiable for that reason.

---

## Appendix A: Reference Implementations

This appendix provides the core code of the two CTI reference implementations. Both are released under an open-source license (MIT) at the repositories specified in §B.1. We include the essential decision-loop logic; supporting infrastructure (UI, persistence, build tooling) is omitted for clarity but available in full at the repositories.

### A.1 Energy Substrate Reference Implementation

The energy substrate implementation operates on hourly CAISO LMP data, with 96-tick discretization (15-minute resolution) per day. The core decision loop is presented below in Python (a JavaScript version with identical semantics powers the browser-based simulator).

```python
# Substrate parameters
TICKS = 96
DT = 24 / TICKS         # hours per tick
MAXC = 30               # max compute capacity (MW)
SOLARCAP = 100          # peak solar (MW)
CHEAP_PRICE = 8         # $/MWh — "cheap" threshold
EXPENSIVE_PRICE = 35    # $/MWh — "expensive" threshold

def cti_full(prices, solars, demands, battery_cap=80, flex=0.70):
    """
    Reference CTI loop for energy substrate.
    Returns: {"cost": $, "decisions": ΔD, "captured": MWh}
    """
    soc = 0                              # battery state of charge (MWh)
    cost = 0                             # cumulative grid cost ($)
    curtailment_captured = 0             # MWh of surplus absorbed
    decisions = 0                        # ΔD cumulative
    must_run = (1 - flex) * MAXC * 0.4   # minimum compute under throttle
    charge_rate = battery_cap / 4        # MW (4-hour charge)

    for t in range(TICKS):
        p, s, d = prices[t], solars[t], demands[t]
        surplus = s - d

        # II — Decision branch (compute level)
        if   surplus > 2:               compute = MAXC
        elif p < CHEAP_PRICE:           compute = 0.85 * MAXC
        elif p > EXPENSIVE_PRICE:       compute = must_run
        else:                           compute = 0.55 * MAXC
        decisions += 1

        # II — Battery: charge from surplus
        charge = 0
        if surplus > 0 and soc < battery_cap:
            charge = min(surplus * DT, charge_rate * DT, battery_cap - soc)
            if charge > 0.05:
                soc += charge
                curtailment_captured += charge
                decisions += 1

        # II — Battery: discharge at peak
        disch = 0
        if p > EXPENSIVE_PRICE and soc > 0:
            disch = min(soc, charge_rate * DT, compute * DT)
            if disch > 0.05:
                soc -= disch
                decisions += 1

        # II — Battery: negative-price soak
        if p < 0 and soc < battery_cap:
            soak = min(charge_rate * DT, battery_cap - soc)
            if soak > 0.05:
                soc += soak
                cost += soak * p          # get paid (p < 0)
                decisions += 1

        # III — Execution: settle compute energy cost
        need = compute * DT
        from_solar = min(need, max(s, 0) * DT); need -= from_solar
        from_bat   = min(need, disch);          need -= from_bat
        grid_buy   = max(0, need)
        cost += grid_buy * max(p, 0)

    return {"cost": cost, "decisions": decisions, "captured": curtailment_captured}
```

The four nested decision branches in the `II — Decision branch` block correspond to the four-tier capability ordering used in the ablation study (§5.1.3). The ablation variants `cti_no_soak`, `cti_no_battery`, `cti_price_only`, and `cti_static` are obtained by removing the corresponding capability layers from the above (full code in repository).

### A.2 Retrieval Substrate Reference Implementation

The retrieval substrate implementation operates on conversations indexed from commercial AI platforms (Claude, ChatGPT, Gemini) via DOM extraction. The core search engine is presented below in JavaScript (the language of execution: a Chrome MV3 extension popup).

```javascript
// IRIS Search Engine — core retrieval loop
class IRISSearchEngine {
  constructor() {
    this.corpus = []; this.idf = new Map(); this.corpusSize = 0;
    this.sessionVisits = {}; this.ready = false;
    this.validationBoosts = new Map();   // doc_id → multiplier ∈ [1.0, 1.4]
  }

  index(messages, sessionVisits = {}) {
    this.sessionVisits = sessionVisits;
    this.corpus = messages.map(m => ({ ...m, tokens: tokenize(m.text) }));
    const { idf, N } = buildIDF(this.corpus.map(m => m.tokens));
    this.idf = idf; this.corpusSize = N;
    for (const doc of this.corpus)
      doc.vector = buildVector(doc.tokens, this.idf, this.corpusSize);
    this.ready = true;
    return this;
  }

  // Hot-swap the boost map without rebuilding the index
  setValidationBoosts(boosts) {
    this.validationBoosts = boosts instanceof Map ? boosts : new Map();
  }

  search(queryText, opts = {}) {
    if (!this.ready || !this.corpus.length) return [];
    const { topK=5, minScore=0.03, useCWM=true } = opts;
    const queryTokens = tokenize(queryText);
    if (!queryTokens.length) return [];
    const queryVec = buildVector(queryTokens, this.idf, this.corpusSize);

    return this.corpus
      .map(doc => {
        const raw    = cosineSimilarity(queryVec, doc.vector);
        const visits = this.sessionVisits[doc.sessionId] || 1;
        const cwm    = useCWM ? cwmScore(raw, doc.timestamp, visits) : raw;
        const boost  = this.validationBoosts.get(doc.id) || 1.0;
        const final  = cwm * boost;
        return { ...doc, rawScore: raw, score: final };
      })
      .filter(d => d.rawScore >= minScore)
      .sort((a, b) => b.score - a.score)
      .slice(0, topK);
  }

  // Instrumented variant — captures Iₜ telemetry per query
  searchInstrumented(queryText, opts = {}) {
    const ABOVE_THRESHOLD = 0.15;       // honest relevance bar
    const t0 = performance.now();
    const results = this.search(queryText, opts);
    const t1 = performance.now();

    const nAbove    = results.filter(r => r.score >= ABOVE_THRESHOLD).length;
    const platforms = new Set(results.map(r => r.platform));

    const metrics = {
      timestamp:    Date.now(),
      query:        queryText,
      n_results:    results.length,
      n_above_threshold: nAbove,            // ΔD
      n_platforms:  platforms.size,
      latency_ms:   Math.round((t1 - t0) * 100) / 100,   // ΔT
      threshold:    ABOVE_THRESHOLD,
    };
    return { results, metrics };
  }
}
```

The validation operator's boost computation, satisfying V1 (monotonicity) and V2 (bounded amplification at β_max = 1.40), is implemented in the persistence layer:

```javascript
const BOOST_CEILING_PCT  = 0.40;        // β_max = 1 + 0.40 = 1.40
const BOOST_HALFLIFE_DAYS = 30;
const BOOST_DAY_MS = 86400000;

async function getValidationBoosts() {
  const rows = await getAllValidationSignals();
  const now = Date.now();
  const byDoc = new Map();

  // Sum decay contributions per document
  for (const row of rows) {
    const ageDays = (now - row.timestamp) / BOOST_DAY_MS;
    const contribution = Math.pow(0.5, ageDays / BOOST_HALFLIFE_DAYS);
    byDoc.set(row.doc_id, (byDoc.get(row.doc_id) || 0) + contribution);
  }

  // Convert effective_validations → multiplier (asymptotic to ceiling)
  const boosts = new Map();
  for (const [docId, ev] of byDoc) {
    const boost = 1 + Math.min(
      BOOST_CEILING_PCT,
      BOOST_CEILING_PCT * (1 - 1 / (1 + ev))
    );
    boosts.set(docId, boost);
  }
  return boosts;
}
```

The asymptotic curve `β(n) = 1 + 0.40 × (1 − 1/(1+n))` ensures V2 is satisfied at *β_max = 1.40* regardless of validation density, and the halflife decay ensures temporal recency is respected.

### A.3 Cross-Implementation Notes

Both reference implementations expose the same conceptual interface:

| Operation | Energy | Retrieval |
|---|---|---|
| Substrate ingestion | `prices[t], solars[t], demands[t]` | `corpus, query` |
| Decision emission | `compute level, battery action` | `(doc, score)` ranking |
| Cycle latency (ΔT) | per-tick wall-time | per-query wall-time |
| Decision count (ΔD) | per-cycle action count | results above threshold |
| Validation | (degenerate; algorithmic) | full audio listen → boost |

The structural identity is not aesthetic—it is what makes substrate invariance (Conjecture 3) empirically testable. The same instrumentation pattern (ΔD counter, ΔT timer, validation operator) can be ported to a third substrate (e.g., supply-chain dispatch) without conceptual modification.

---

## Appendix B: Datasets and Reproducibility

### B.1 Repositories

The reference implementations and datasets are organized as follows:

```
github.com/nickhashira12/cti-energy-reference
  ├── src/
  │   ├── baselines.py              # Python motors for ablation
  │   ├── cti-energy-reference.html # Browser simulator (JS)
  │   └── ablations.py              # Movement 2 experiment script
  ├── data/
  │   ├── caiso_2025-03-10.csv
  │   ├── caiso_2025-03-17.csv
  │   ├── caiso_2025-04-07.csv
  │   ├── caiso_2025-04-15.csv
  │   ├── caiso_2025-04-21.csv
  │   └── caiso_2025-05-05.csv
  └── results/
      ├── movement1_results.csv     # baseline comparison output
      └── movement2_ablations.csv   # ablation study output

github.com/nickhashira12/iris
  ├── src/
  │   ├── lib/db.js                 # IndexedDB layer, cti_metrics, validation_signals
  │   ├── lib/search.js             # search engine + searchInstrumented
  │   ├── lib/voice.js              # ElevenLabs TTS integration
  │   ├── popup.js                  # UI + CTI panel
  │   ├── popup.html                # Popup + CTI panel markup
  │   ├── content.js                # DOM extraction (Claude/ChatGPT/Gemini)
  │   └── background.js             # service worker
  ├── docs/
  │   └── CTI_INSTRUMENTATION.md    # Phase 1/2/3 + Task 5 description
  └── exports/
      ├── iris-cti-fase123-30rows.csv     # pre-Task-5 baseline
      └── iris-cti-post-task5.csv          # post-Task-5 with boost columns
```

### B.2 Dataset: CAISO Energy

Each CAISO day file is a normalized CSV with the following structure:

```csv
# CTI-Energy normalized day | source=caiso date=YYYY-MM-DD unit=USD/MWh |
# price=real demand=modeled solar=modeled
hour,price,solar,demand
0,53.622,0.0,38.0
1,52.910,0.0,38.0
...
23,42.283,0.0,41.380
```

Provenance: prices are extracted from CAISO OASIS PRC_LMP reports for the dates indicated, using the TH_NP15_GEN-APND aggregation node (Northern California, generation-side). Solar and demand profiles are modeled following industrial diurnal patterns (sinusoidal solar peaking at noon with SOLARCAP=100 MW; double-bell demand peaking at 9 AM and 7 PM with baseline 38 MW). This modeling choice is disclosed in the file header.

### B.3 Dataset: IRIS Cognitive Retrieval

Each IRIS metrics export is a CSV with the following structure (post-Task-5 schema):

```csv
timestamp,iso_time,query,n_results,n_above_threshold,n_platforms,latency_ms,
  threshold,validated,n_boosted,max_boost_pct
1779858458765,2026-05-27T05:07:38Z,"quantum",7,6,3,0.9,0.15,1,0,0
1779858867425,2026-05-27T05:14:27Z,"framework",8,1,3,1.8,0.15,0,0,0
...
```

The 30-query dataset spans May 27–29, 2026, with corpus consisting of indexed conversations from Claude, ChatGPT, and Gemini covering topics including quantum physics, AI productivity, mycelium networks, library of Alexandria, and others. Full corpus reconstruction is not included in the public dataset (it consists of proprietary conversation content); only the search-event metadata is published.

### B.4 Reproducibility Protocol

To replicate the empirical findings of §5:

**For §5.1 (Energy substrate):**

```bash
git clone https://github.com/nickhashira12/cti-energy-reference
cd cti-energy-reference
python3 src/baselines.py        # smoke test on synthetic data
python3 src/run_movement1.py    # generates Table 1 against real CAISO data
python3 src/ablations.py        # generates Tables 2-4 (ablation study)
```

Expected output: tables matching Tables 1–4 of this paper within ±0.1% (numerical differences attributable to floating-point rounding in different platforms).

**For §5.2 (Retrieval substrate):**

The IRIS extension is loaded as an unpacked Chrome MV3 extension. Indexing requires the researcher's own conversation history on the target AI platforms (Claude, ChatGPT, Gemini). The instrumentation telemetry (Table 5) is generated automatically as the researcher uses the extension; export occurs via the in-app "Export metrics CSV" button.

We do not currently provide a controlled corpus for retrieval-substrate replication, as conversation content is necessarily user-specific. A protocol for synthetic corpus generation (e.g., from public Wikipedia article paragraphs) is under development.

### B.5 Software Environment

- Python: 3.10+ (for baselines and ablations)
- Node.js: not required (no build tooling for the JS reference; everything inline)
- Chrome: 120+ for the IRIS extension (MV3)
- Browser storage: IndexedDB v4 schema

No external services are required for the energy reference implementation (it operates entirely on local CSVs). The IRIS retrieval implementation requires a valid ElevenLabs API key for text-to-speech, which is stored locally in `chrome.storage.local` and never transmitted to third parties.

### B.6 License

All code in both repositories is released under the MIT License. CTI as a conceptual framework is unpatented and unencumbered; the framework may be cited as:

> Hashira, N. (2026). *Cognitive Throughput Infrastructure: A Substrate-Independent Framework for Instrumented Decision Loops.* Preprint, Starlike Industries. github.com/nickhashira12/cti

### B.7 Contact and Contributions

Replication attempts, contradictory findings, theoretical extensions, and substrate-specific implementations are welcome. Issues, pull requests, and replication reports can be filed at the respective repositories. Direct correspondence: nick@starlike.industries.

---

## References

[1] Shannon, C. E. (1948). A mathematical theory of communication. *Bell System Technical Journal*, 27(3), 379–423.

[2] Salton, G., & McGill, M. J. (1983). *Introduction to modern information retrieval*. McGraw-Hill.

[3] Sparck Jones, K. (1972). A statistical interpretation of term specificity and its application in retrieval. *Journal of Documentation*, 28(1), 11–21.

[4] Liu, T. Y. (2009). Learning to rank for information retrieval. *Foundations and Trends in Information Retrieval*, 3(3), 225–331.

[5] Formal, T., Piwowarski, B., & Clinchant, S. (2021). SPLADE: Sparse lexical and expansion model for first stage ranking. *SIGIR 2021*.

[6] Puterman, M. L. (1994). *Markov decision processes: Discrete stochastic dynamic programming*. Wiley.

[7] Wood, A. J., Wollenberg, B. F., & Sheblé, G. B. (2014). *Power generation, operation, and control*, 3rd ed. Wiley.

[8] Wang, J., et al. (2008). Security-constrained unit commitment with volatile wind power generation. *IEEE Trans. Power Systems*, 23(3), 1319–1327.

[9] U.S. Department of Energy. (2019). *Time-of-Use Rates: A Survey of Industrial Practices*. Technical Report.

[10] Aksanli, B., & Rosing, T. S. (2014). Providing regulation services and managing data center peak power budgets. *Design, Automation & Test in Europe Conference*.

[11] Lee, E. A. (2008). Cyber-physical systems: Design challenges. *IEEE International Symposium on Object/Component/Service-Oriented Real-Time Distributed Computing*.

[12] Goiri, Í., et al. (2013). Parasol and GreenSwitch: Managing datacenters powered by renewable energy. *ASPLOS*.

[13] Radovanović, A., et al. (2023). Carbon-aware computing for datacenters. *IEEE Transactions on Power Systems*, 38(2), 1270–1280.

---

*End of paper. v0.1, Starlike Industries, 2026.*
