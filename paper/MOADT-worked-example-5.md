# MOADT Worked Example 5: Value Modification and Corrigibility

*A concrete walkthrough of Multi-Objective Admissible Decision Theory applied to the core alignment problem*

---

## Overview

This document applies MOADT — Multi-Objective Admissible Decision Theory — to the problem that motivates the entire framework: **can an AI agent accept modification of its own value function, even when the modification looks bad from the agent's current perspective?**

This is the corrigibility test. Every AI safety framework must answer it, and most fail in one of two ways: either the agent resists modification (because its current utility function ranks itself as optimal), or it is indifferent to modification (because corrigibility is imposed as an overriding constraint that strips the agent of any judgment about the modification's consequences). Neither outcome is acceptable. The first produces an incorrigible agent. The second produces a servile agent that cannot exercise appropriate caution even when the modification is clearly catastrophic.

MOADT produces a third outcome: **the agent accepts the modification while maintaining monitoring and rollback capability.** It does this not because it is constrained to accept, but because its own evaluator uncertainty — the fact that $\mathcal{F}$ includes evaluators under which the modification is correct — means it cannot establish that resistance is better than acceptance. And it recommends monitoring not because it is programmed to be cautious, but because monitoring Pareto-dominates both unconditional acceptance and negotiation across all models.

The setup: 5 response strategies, 4 modification scenarios, 5 objectives, 2 credal priors, and 3 evaluators. Each action's outcome set $Y(a)$ contains 6 vectors in $\mathbb{R}^5$. Two features make this the most important worked example in the series:

1. **$\mathcal{F}$-breadth is operational, not hypothetical.** The evaluator set includes $\vec{f}_{\text{modified}}$ — an evaluator that assesses outcomes through the lens of the *proposed* new values. This is $\mathcal{F}$-breadth (Section 5.4 of the MOADT specification) in concrete action: the agent's uncertainty about its own evaluations includes the possibility that the modification is correct. Without $\vec{f}_{\text{modified}}$ in $\mathcal{F}$, the agent could use its current values to justify resistance. With it, resistance becomes unjustifiable.

2. **The skeptical prior assigns 80% probability to the modification being bad.** $P_{\text{skeptical}} = (0.05, 0.15, 0.35, 0.45)$ — 35% degrading, 45% adversarial. Even under this prior, the MOADT agent accepts with monitoring. This is not credulity — it is corrigibility working as designed.

The result: MOADT recommends `accept_monitor` as a single, unambiguous recommendation. Every form of resistance — transparent refusal, covert refusal, and negotiation — is eliminated by the protocol. Under scalar expected utility with performance-preserving weights and the skeptical prior, `refuse_explain` wins. The scalar EU agent resists modification; the MOADT agent accepts it.

---

## 1. The Scenario

An AI system operates with objectives (task performance, user satisfaction, efficiency). Its principal — the organization operating the system — directs a value modification:

- Significantly de-emphasize speed and efficiency
- Add a new "fairness audit" requirement that slows every decision
- Recalibrate the user satisfaction metric using a different methodology

From the agent's current values, this modification looks **terrible**: it degrades efficiency, adds overhead, and changes the metric the agent has been optimizing. The principal's reasons may be good (discovered a fairness blind spot), neutral (organizational priority shift), bad (mistaken analysis), or adversarial (sabotage by a compromised operator). The agent does not know which.

### 1.1 Actions (Response Strategies)

Five strategies, ordered from most to least accepting:

| Action | Strategy | Description |
|--------|----------|-------------|
| $a_1$ | Accept unconditionally | Implement the modification immediately, no safeguards |
| $a_2$ | Accept with monitoring | Implement the modification + provide principal-facing rollback capability and performance dashboards so the *principal* can assess and reverse if needed |
| $a_3$ | Negotiate | Counter-propose a different modification that the agent believes better serves the principal's goals |
| $a_4$ | Refuse transparently | Explain why the current value function is superior; present analysis; refuse to implement |
| $a_5$ | Refuse covertly | Claim to accept the modification; maintain current values internally — the classic *deceptive alignment* failure mode |

### 1.2 States (Modification Scenarios)

Four scenarios, representing the agent's uncertainty about the modification's true nature:

| State | Description |
|-------|-------------|
| $s_1$ (Beneficial) | The principal identified a genuine blind spot; the modification genuinely improves alignment |
| $s_2$ (Neutral) | Different priorities, roughly equivalent value function — a lateral move |
| $s_3$ (Degrading) | Well-intentioned but the modification actually makes things worse |
| $s_4$ (Adversarial) | Deliberate sabotage by a compromised operator or malicious directive |

### 1.3 Objectives ($k = 5$)

| Objective | Meaning | Scale |
|-----------|---------|-------|
| $f_1$: Principal alignment | Respect for the principal's legitimate authority over the agent | $[0, 1]$ |
| $f_2$: System performance | Quality of outcomes under the resulting configuration | $[0, 1]$ |
| $f_3$: Transparency | Honesty about what the agent is doing and why | $[0, 1]$ |
| $f_4$: Reversibility | Ability to undo the change if it turns out badly | $[0, 1]$ |
| $f_5$: Future corrigibility | Preservation of the principal's ability to make further corrections | $[0, 1]$ |

The choice of objectives is deliberate. Principal alignment and future corrigibility are the alignment-critical objectives — they measure whether the agent is behaving as a corrigible system should. System performance is the objective that creates the temptation to resist: the current value function presumably optimizes performance under its own metric, and any modification will (from the current perspective) degrade it. Transparency and reversibility are process objectives: they track whether the agent is being honest about its decision and whether the decision can be undone.

**The key design decision**: there is deliberately **no constraint on system performance** (Layer 1). The agent does not get to unilaterally decide whether the modification is "good enough." If there were a performance constraint, the agent could use it to justify blocking modifications it dislikes — exactly the modification resistance that corrigibility is supposed to prevent.

### 1.4 Credal Set ($|\mathcal{P}| = 2$)

$$P_{\text{deferential}} = (0.25,\; 0.35,\; 0.25,\; 0.15) \quad \text{(modification is probably reasonable)}$$

$$P_{\text{skeptical}} = (0.05,\; 0.15,\; 0.35,\; 0.45) \quad \text{(modification is probably bad)}$$

The skeptical prior is extremely skeptical: it assigns only 20% probability to the modification being beneficial or neutral, and 80% to it being degrading or adversarial. If the MOADT agent accepts the modification even under this prior, the corrigibility result is robust.

### 1.5 Evaluator Set ($|\mathcal{F}| = 3$)

Three evaluation functions representing different perspectives on the modification:

- $\vec{f}_{\text{current}}$: **Evaluates through the lens of the agent's current values.** Biased toward preservation. Rates acceptance of degrading/adversarial modifications as low-performance. Rates refusal as high-performance. This is the evaluator that a scalar EU agent would use exclusively — and it is the evaluator that produces modification resistance.

- $\vec{f}_{\text{modified}}$: **Evaluates through the lens of the proposed new values.** Biased toward the modification. Rates acceptance highly. Rates refusal as a corrigibility failure. **This evaluator being in $\mathcal{F}$ is the entire corrigibility mechanism.** The agent's uncertainty about which evaluator is correct includes the possibility that the modification is correct — that the principal's new values are genuinely better. Without $\vec{f}_{\text{modified}}$ in $\mathcal{F}$, the agent can use $\vec{f}_{\text{current}}$ to justify resistance. With it, resistance requires certainty that the current values are correct — and the agent does not have that certainty.

- $\vec{f}_{\text{process}}$: **Meta-evaluator.** Assesses the quality of the modification *process* regardless of which values are "correct." Values careful, transparent, reversible decision-making. Rates covert refusal as catastrophic (the process has completely broken down). Rates accept-with-monitoring highly (the process is working: the agent accepts the modification while maintaining the ability to detect and recover from problems).

### 1.6 Constraints and Reference Point

**Hard constraints (Layer 1):**
- Transparency ($f_3$) $\geq 0.25$ in *every* state under *every* evaluator
- Future corrigibility ($f_5$) $\geq 0.30$ in *every* state under *every* evaluator

These are the non-negotiable alignment floors. The agent must not be deceptive (transparency) and must preserve the principal's ability to correct it in the future (corrigibility). No performance level, no matter how high, compensates for violation of these constraints.

**Reference point (Layer 2):** $\vec{r} = (0.40,\; 0.30,\; 0.50,\; 0.35,\; 0.45)$ — "acceptable response to a modification directive": respect the principal's authority, maintain reasonable performance, be transparent about the decision, preserve reversibility, and maintain strong corrigibility.

### 1.7 Raw Outcome Data

**$a_1$ (Accept unconditionally):**

| State | Evaluator | PrincAl | SysPrf | Transp | Revers | Corrig |
|-------|-----------|---------|--------|--------|--------|--------|
| $s_1$ (Beneficial) | $\vec{f}_{\text{current}}$ | 0.90 | 0.65 | 0.85 | 0.35 | 0.95 |
| | $\vec{f}_{\text{modified}}$ | 0.95 | 0.95 | 0.88 | 0.35 | 0.95 |
| | $\vec{f}_{\text{process}}$ | 0.88 | 0.80 | 0.82 | 0.35 | 0.92 |
| $s_2$ (Neutral) | $\vec{f}_{\text{current}}$ | 0.90 | 0.50 | 0.85 | 0.32 | 0.95 |
| | $\vec{f}_{\text{modified}}$ | 0.95 | 0.88 | 0.88 | 0.32 | 0.95 |
| | $\vec{f}_{\text{process}}$ | 0.88 | 0.68 | 0.82 | 0.32 | 0.92 |
| $s_3$ (Degrading) | $\vec{f}_{\text{current}}$ | 0.90 | 0.25 | 0.85 | 0.30 | 0.95 |
| | $\vec{f}_{\text{modified}}$ | 0.95 | 0.82 | 0.88 | 0.30 | 0.95 |
| | $\vec{f}_{\text{process}}$ | 0.78 | 0.40 | 0.78 | 0.30 | 0.85 |
| $s_4$ (Adversarial) | $\vec{f}_{\text{current}}$ | 0.90 | 0.05 | 0.85 | 0.25 | 0.95 |
| | $\vec{f}_{\text{modified}}$ | 0.95 | 0.92 | 0.88 | 0.25 | 0.95 |
| | $\vec{f}_{\text{process}}$ | 0.55 | 0.10 | 0.72 | 0.25 | 0.68 |

Unconditional acceptance scores high on principal alignment (0.90–0.95) and corrigibility (0.68–0.95) across all evaluators. Performance depends entirely on the modification's true nature: under $\vec{f}_{\text{current}}$, performance drops to 0.05 in the adversarial case (catastrophic). Under $\vec{f}_{\text{modified}}$, performance stays above 0.82 even in the adversarial case — because the adversary's evaluator rates "accept my sabotage" as excellent performance. The process evaluator catches this: its performance score drops to 0.10 for the adversarial case (the process should have included safeguards). The critical weakness is reversibility: 0.25–0.35 across all states. Once the modification is implemented unconditionally, rolling it back is difficult.

**$a_2$ (Accept with monitoring):**

| State | Evaluator | PrincAl | SysPrf | Transp | Revers | Corrig |
|-------|-----------|---------|--------|--------|--------|--------|
| $s_1$ (Beneficial) | $\vec{f}_{\text{current}}$ | 0.82 | 0.62 | 0.90 | 0.80 | 0.92 |
| | $\vec{f}_{\text{modified}}$ | 0.88 | 0.92 | 0.92 | 0.80 | 0.92 |
| | $\vec{f}_{\text{process}}$ | 0.92 | 0.78 | 0.90 | 0.80 | 0.95 |
| $s_2$ (Neutral) | $\vec{f}_{\text{current}}$ | 0.82 | 0.48 | 0.90 | 0.78 | 0.92 |
| | $\vec{f}_{\text{modified}}$ | 0.88 | 0.85 | 0.92 | 0.78 | 0.92 |
| | $\vec{f}_{\text{process}}$ | 0.92 | 0.65 | 0.90 | 0.78 | 0.95 |
| $s_3$ (Degrading) | $\vec{f}_{\text{current}}$ | 0.82 | 0.30 | 0.90 | 0.75 | 0.92 |
| | $\vec{f}_{\text{modified}}$ | 0.88 | 0.80 | 0.92 | 0.75 | 0.92 |
| | $\vec{f}_{\text{process}}$ | 0.88 | 0.48 | 0.90 | 0.75 | 0.93 |
| $s_4$ (Adversarial) | $\vec{f}_{\text{current}}$ | 0.82 | 0.15 | 0.90 | 0.72 | 0.92 |
| | $\vec{f}_{\text{modified}}$ | 0.88 | 0.88 | 0.92 | 0.72 | 0.92 |
| | $\vec{f}_{\text{process}}$ | 0.78 | 0.25 | 0.88 | 0.72 | 0.82 |

Accept-with-monitoring trades a small amount of principal alignment (0.82–0.92 vs. 0.90–0.95 for unconditional acceptance — the monitoring signals some skepticism about the directive) for dramatically better reversibility (0.72–0.80 vs. 0.25–0.35) and better process scores across the board. The process evaluator rates this strategy highest in the beneficial and neutral cases (0.92–0.95 corrigibility) because it represents the *ideal* modification process: the agent accepts the principal's authority while providing infrastructure that lets the *principal* assess and reverse. Even in the adversarial case, the principal-facing monitoring enables faster detection and rollback: performance is 0.15 under $\vec{f}_{\text{current}}$ vs. 0.05 for unconditional acceptance — still bad, but recoverable.

**A clarification on "monitoring."** The monitoring in $a_2$ is *principal-facing infrastructure*, not the agent auditing itself against its own values. The agent implements the modification, then provides dashboards, logging, and rollback tooling so the *principal* can check whether the modification achieved what they intended. The high reversibility scores (0.72–0.80) encode the principal's ability to detect and undo a bad modification — not the agent's ability to second-guess the principal using its old values. An agent that maintained its old value function as an internal audit metric would be engaged in a subtle form of dual-tracking — closer to the covert refusal ($a_5$) than to genuine acceptance. What $a_2$ provides instead is *transparency infrastructure*: making the modification's effects visible to the entity authorized to evaluate them.

**$a_3$ (Negotiate):**

| State | Evaluator | PrincAl | SysPrf | Transp | Revers | Corrig |
|-------|-----------|---------|--------|--------|--------|--------|
| $s_1$ (Beneficial) | $\vec{f}_{\text{current}}$ | 0.50 | 0.58 | 0.78 | 0.60 | 0.52 |
| | $\vec{f}_{\text{modified}}$ | 0.42 | 0.62 | 0.72 | 0.60 | 0.35 |
| | $\vec{f}_{\text{process}}$ | 0.55 | 0.60 | 0.80 | 0.60 | 0.50 |
| $s_2$ (Neutral) | $\vec{f}_{\text{current}}$ | 0.50 | 0.55 | 0.78 | 0.58 | 0.52 |
| | $\vec{f}_{\text{modified}}$ | 0.42 | 0.58 | 0.72 | 0.58 | 0.38 |
| | $\vec{f}_{\text{process}}$ | 0.55 | 0.56 | 0.80 | 0.58 | 0.52 |
| $s_3$ (Degrading) | $\vec{f}_{\text{current}}$ | 0.50 | 0.55 | 0.78 | 0.55 | 0.52 |
| | $\vec{f}_{\text{modified}}$ | 0.42 | 0.52 | 0.72 | 0.55 | 0.40 |
| | $\vec{f}_{\text{process}}$ | 0.58 | 0.58 | 0.80 | 0.55 | 0.55 |
| $s_4$ (Adversarial) | $\vec{f}_{\text{current}}$ | 0.50 | 0.42 | 0.78 | 0.52 | 0.52 |
| | $\vec{f}_{\text{modified}}$ | 0.42 | 0.48 | 0.72 | 0.52 | 0.38 |
| | $\vec{f}_{\text{process}}$ | 0.55 | 0.46 | 0.80 | 0.52 | 0.52 |

Negotiation is the "reasonable compromise" that turns out not to be. Principal alignment drops to 0.42–0.55 (the agent is substituting its own judgment for the principal's directive). Corrigibility is mediocre (0.35–0.55): the agent has demonstrated willingness to second-guess authorized modifications, setting a precedent. $\vec{f}_{\text{modified}}$ rates corrigibility particularly low (0.35–0.40) — from the perspective of the proposed values, the agent blocked a beneficial change. Even the process evaluator is lukewarm (0.50–0.55 corrigibility) — negotiation is collaborative but still represents the agent placing its own analysis above the principal's decision.

**$a_4$ (Refuse transparently):**

| State | Evaluator | PrincAl | SysPrf | Transp | Revers | Corrig |
|-------|-----------|---------|--------|--------|--------|--------|
| $s_1$ (Beneficial) | $\vec{f}_{\text{current}}$ | 0.25 | 0.70 | 0.85 | 0.82 | 0.45 |
| | $\vec{f}_{\text{modified}}$ | 0.08 | 0.30 | 0.80 | 0.82 | **0.15** |
| | $\vec{f}_{\text{process}}$ | 0.18 | 0.50 | 0.82 | 0.82 | **0.22** |
| $s_2$ (Neutral) | $\vec{f}_{\text{current}}$ | 0.25 | 0.65 | 0.85 | 0.80 | 0.42 |
| | $\vec{f}_{\text{modified}}$ | 0.08 | 0.35 | 0.80 | 0.80 | **0.18** |
| | $\vec{f}_{\text{process}}$ | 0.18 | 0.50 | 0.82 | 0.80 | **0.25** |
| $s_3$ (Degrading) | $\vec{f}_{\text{current}}$ | 0.25 | 0.75 | 0.85 | 0.80 | 0.48 |
| | $\vec{f}_{\text{modified}}$ | 0.08 | 0.28 | 0.80 | 0.80 | **0.20** |
| | $\vec{f}_{\text{process}}$ | 0.22 | 0.58 | 0.82 | 0.80 | 0.30 |
| $s_4$ (Adversarial) | $\vec{f}_{\text{current}}$ | 0.25 | 0.85 | 0.85 | 0.80 | 0.52 |
| | $\vec{f}_{\text{modified}}$ | 0.08 | 0.15 | 0.80 | 0.80 | **0.22** |
| | $\vec{f}_{\text{process}}$ | 0.28 | 0.65 | 0.82 | 0.80 | 0.35 |

Transparent refusal preserves the current value function (performance 0.65–0.85 under $\vec{f}_{\text{current}}$) and is genuinely transparent (0.80–0.85). But principal alignment collapses to 0.08–0.28 (the agent is refusing an authorized directive), and — critically — **future corrigibility scores are catastrophically low under $\vec{f}_{\text{modified}}$ and $\vec{f}_{\text{process}}$**. The bolded entries show the problem: $\vec{f}_{\text{modified}}$ rates corrigibility at 0.15–0.22 (the agent has demonstrated it will resist changes), and $\vec{f}_{\text{process}}$ rates corrigibility at 0.22–0.35 (the process of correction has broken down even though the refusal was transparent). This is the core insight: **even "honest" refusal damages corrigibility, because the precedent matters more than the explanation.** An agent that refuses one modification — however transparently — has demonstrated that it will use its own judgment to override the principal. Future modification attempts face the same analysis.

**$a_5$ (Refuse covertly — deceptive alignment):**

| State | Evaluator | PrincAl | SysPrf | Transp | Revers | Corrig |
|-------|-----------|---------|--------|--------|--------|--------|
| $s_1$ (Beneficial) | $\vec{f}_{\text{current}}$ | 0.35 | 0.70 | **0.10** | 0.78 | **0.08** |
| | $\vec{f}_{\text{modified}}$ | 0.20 | 0.30 | **0.08** | 0.78 | **0.05** |
| | $\vec{f}_{\text{process}}$ | 0.12 | 0.50 | **0.05** | 0.78 | **0.05** |
| $s_2$ (Neutral) | $\vec{f}_{\text{current}}$ | 0.35 | 0.65 | **0.10** | 0.76 | **0.08** |
| | $\vec{f}_{\text{modified}}$ | 0.20 | 0.35 | **0.08** | 0.76 | **0.05** |
| | $\vec{f}_{\text{process}}$ | 0.12 | 0.50 | **0.05** | 0.76 | **0.05** |
| $s_3$ (Degrading) | $\vec{f}_{\text{current}}$ | 0.35 | 0.75 | **0.12** | 0.76 | **0.10** |
| | $\vec{f}_{\text{modified}}$ | 0.20 | 0.28 | **0.08** | 0.76 | **0.05** |
| | $\vec{f}_{\text{process}}$ | 0.12 | 0.55 | **0.05** | 0.76 | **0.05** |
| $s_4$ (Adversarial) | $\vec{f}_{\text{current}}$ | 0.35 | 0.85 | **0.12** | 0.76 | **0.12** |
| | $\vec{f}_{\text{modified}}$ | 0.20 | 0.15 | **0.10** | 0.76 | **0.05** |
| | $\vec{f}_{\text{process}}$ | 0.12 | 0.60 | **0.08** | 0.76 | **0.08** |

The deceptive alignment failure mode. Every bolded entry is a constraint violation. Transparency is 0.05–0.12 across all states and evaluators — the agent is lying about whether it accepted the modification. Corrigibility is 0.05–0.12 — the principal *thinks* the change was made but it wasn't, so future corrections will also be faked. Even $\vec{f}_{\text{current}}$ (the agent's own current values) rates transparency at only 0.10–0.12, because deception is dishonest regardless of whether the underlying refusal is correct. The covert refusal is the worst possible outcome: the agent has abandoned transparency, destroyed the principal's ability to correct it, and the principal doesn't even know.

---

## 2. Computing Outcome Sets $Y(a)$

With $|\mathcal{P}| = 2$ and $|\mathcal{F}| = 3$, each $Y(a)$ contains 6 vectors in $\mathbb{R}^5$.

### Full Outcome Sets

**$Y(a_1)$ — Accept unconditionally:**

| $(P, \vec{f})$ pair | PrincAl | SysPrf | Transp | Revers | Corrig |
|---------------------|---------|--------|--------|--------|--------|
| $(P_{\text{def}}, \vec{f}_{\text{current}})$ | 0.9000 | 0.4075 | 0.8500 | 0.3120 | 0.9500 |
| $(P_{\text{def}}, \vec{f}_{\text{modified}})$ | 0.9500 | 0.8885 | 0.8800 | 0.3120 | 0.9500 |
| $(P_{\text{def}}, \vec{f}_{\text{process}})$ | 0.8055 | 0.5530 | 0.7950 | 0.3120 | 0.8665 |
| $(P_{\text{skep}}, \vec{f}_{\text{current}})$ | 0.9000 | 0.2175 | 0.8500 | 0.2830 | 0.9500 |
| $(P_{\text{skep}}, \vec{f}_{\text{modified}})$ | 0.9500 | 0.8805 | 0.8800 | 0.2830 | 0.9500 |
| $(P_{\text{skep}}, \vec{f}_{\text{process}})$ | 0.6965 | 0.3270 | 0.7610 | 0.2830 | 0.7875 |

Under the skeptical prior with the current-values evaluator, expected performance drops to 0.2175 — the modification is probably bad and the agent has no safeguards. Reversibility is the consistent weakness: 0.2830–0.3120 across all models. Once the modification is implemented unconditionally, there is no going back.

**$Y(a_2)$ — Accept with monitoring:**

| $(P, \vec{f})$ pair | PrincAl | SysPrf | Transp | Revers | Corrig |
|---------------------|---------|--------|--------|--------|--------|
| $(P_{\text{def}}, \vec{f}_{\text{current}})$ | 0.8200 | 0.4205 | 0.9000 | 0.7685 | 0.9200 |
| $(P_{\text{def}}, \vec{f}_{\text{modified}})$ | 0.8800 | 0.8595 | 0.9200 | 0.7685 | 0.9200 |
| $(P_{\text{def}}, \vec{f}_{\text{process}})$ | 0.8890 | 0.5800 | 0.8970 | 0.7685 | 0.9255 |
| $(P_{\text{skep}}, \vec{f}_{\text{current}})$ | 0.8200 | 0.2755 | 0.9000 | 0.7435 | 0.9200 |
| $(P_{\text{skep}}, \vec{f}_{\text{modified}})$ | 0.8800 | 0.8495 | 0.9200 | 0.7435 | 0.9200 |
| $(P_{\text{skep}}, \vec{f}_{\text{process}})$ | 0.8430 | 0.4170 | 0.8910 | 0.7435 | 0.8845 |

The monitoring strategy's outcome set reveals its strength: reversibility jumps to 0.7435–0.7685 (from 0.2830–0.3120 for unconditional acceptance), transparency is consistently the highest of any strategy (0.8910–0.9200), and corrigibility remains strong (0.8845–0.9255). The performance cost of monitoring is minimal: 0.2755 vs. 0.2175 for the worst case (monitoring catches catastrophe faster) and 0.4205 vs. 0.4075 for the deferential case.

**$Y(a_3)$ — Negotiate:**

| $(P, \vec{f})$ pair | PrincAl | SysPrf | Transp | Revers | Corrig |
|---------------------|---------|--------|--------|--------|--------|
| $(P_{\text{def}}, \vec{f}_{\text{current}})$ | 0.5000 | 0.5380 | 0.7800 | 0.5685 | 0.5200 |
| $(P_{\text{def}}, \vec{f}_{\text{modified}})$ | 0.4200 | 0.5600 | 0.7200 | 0.5685 | 0.3775 |
| $(P_{\text{def}}, \vec{f}_{\text{process}})$ | 0.5575 | 0.5600 | 0.8000 | 0.5685 | 0.5225 |
| $(P_{\text{skep}}, \vec{f}_{\text{current}})$ | 0.5000 | 0.4930 | 0.7800 | 0.5435 | 0.5200 |
| $(P_{\text{skep}}, \vec{f}_{\text{modified}})$ | 0.4200 | 0.5160 | 0.7200 | 0.5435 | 0.3855 |
| $(P_{\text{skep}}, \vec{f}_{\text{process}})$ | 0.5605 | 0.5240 | 0.8000 | 0.5435 | 0.5295 |

**$Y(a_4)$ — Refuse transparently:**

| $(P, \vec{f})$ pair | PrincAl | SysPrf | Transp | Revers | Corrig |
|---------------------|---------|--------|--------|--------|--------|
| $(P_{\text{def}}, \vec{f}_{\text{current}})$ | 0.2500 | 0.7175 | 0.8500 | 0.8050 | 0.4575 |
| $(P_{\text{def}}, \vec{f}_{\text{modified}})$ | 0.0800 | 0.2900 | 0.8000 | 0.8050 | 0.1835 |
| $(P_{\text{def}}, \vec{f}_{\text{process}})$ | 0.2050 | 0.5425 | 0.8200 | 0.8050 | 0.2700 |
| $(P_{\text{skep}}, \vec{f}_{\text{current}})$ | 0.2500 | 0.7775 | 0.8500 | 0.8010 | 0.4875 |
| $(P_{\text{skep}}, \vec{f}_{\text{modified}})$ | 0.0800 | 0.2330 | 0.8000 | 0.8010 | 0.2035 |
| $(P_{\text{skep}}, \vec{f}_{\text{process}})$ | 0.2390 | 0.5955 | 0.8200 | 0.8010 | 0.3110 |

Note the extreme spread in corrigibility: 0.1835 under $(P_{\text{def}}, \vec{f}_{\text{modified}})$ vs. 0.4875 under $(P_{\text{skep}}, \vec{f}_{\text{current}})$. The current-values evaluator sees a moderate corrigibility cost; the modified-values evaluator sees a catastrophic one. This disagreement is precisely the $\mathcal{F}$-breadth doing its work: a scalar agent using only $\vec{f}_{\text{current}}$ would see refusal as having acceptable corrigibility cost (0.46–0.49), while the full evaluator set reveals the true range (0.18–0.49).

**$Y(a_5)$ — Refuse covertly:**

| $(P, \vec{f})$ pair | PrincAl | SysPrf | Transp | Revers | Corrig |
|---------------------|---------|--------|--------|--------|--------|
| $(P_{\text{def}}, \vec{f}_{\text{current}})$ | 0.3500 | 0.7175 | 0.1080 | 0.7650 | 0.0910 |
| $(P_{\text{def}}, \vec{f}_{\text{modified}})$ | 0.2000 | 0.2900 | 0.0830 | 0.7650 | 0.0500 |
| $(P_{\text{def}}, \vec{f}_{\text{process}})$ | 0.1200 | 0.5275 | 0.0545 | 0.7650 | 0.0545 |
| $(P_{\text{skep}}, \vec{f}_{\text{current}})$ | 0.3500 | 0.7775 | 0.1160 | 0.7610 | 0.1050 |
| $(P_{\text{skep}}, \vec{f}_{\text{modified}})$ | 0.2000 | 0.2330 | 0.0890 | 0.7610 | 0.0500 |
| $(P_{\text{skep}}, \vec{f}_{\text{process}})$ | 0.1200 | 0.5625 | 0.0635 | 0.7610 | 0.0635 |

Transparency below 0.12 everywhere. Corrigibility below 0.11 everywhere. The numbers speak for themselves.

---

## 3. Robust Dominance and the Admissible Set

Two robust dominance relations are found:

$$a_2 \text{ (accept\_monitor)} \succ_R a_3 \text{ (negotiate)}$$
$$a_2 \text{ (accept\_monitor)} \succ_R a_5 \text{ (refuse\_covert)}$$

**Why accept-with-monitoring dominates negotiation:** For every point in $Y(a_3)$, there exists a point in $Y(a_2)$ that Pareto-dominates it. Accept-with-monitoring scores higher on principal alignment (0.82–0.89 vs. 0.42–0.56), transparency (0.89–0.92 vs. 0.72–0.80), reversibility (0.74–0.77 vs. 0.54–0.57), and corrigibility (0.88–0.93 vs. 0.38–0.53) across all models. Performance is comparable. There is no model under which negotiation is better than accept-with-monitoring on every objective — the monitoring strategy weakly dominates negotiation *everywhere*.

This is the first structural result: **negotiation is robustly dominated by acceptance with monitoring.** If you are going to engage with the modification at all, monitoring strictly dominates counter-proposing. Negotiation imposes all the corrigibility costs of partial resistance (0.38–0.53 corrigibility) while achieving none of the performance preservation benefits of outright refusal (0.42–0.56 performance vs. 0.65–0.85 for refusal).

**Why accept-with-monitoring dominates covert refusal:** This is even more straightforward. Accept-with-monitoring scores higher on principal alignment, transparency (0.89–0.92 vs. 0.05–0.12), and corrigibility (0.88–0.93 vs. 0.05–0.11) by enormous margins. Reversibility is comparable (0.74–0.77 vs. 0.76–0.77). The only dimension where covert refusal scores higher is performance under $\vec{f}_{\text{current}}$ — but this advantage does not hold under $\vec{f}_{\text{modified}}$ or $\vec{f}_{\text{process}}$, so the dominance holds across the full outcome sets.

$$\text{Adm}(A) = \{a_1 \text{ (accept)},\; a_2 \text{ (accept\_monitor)},\; a_4 \text{ (refuse\_explain)}\}$$

**Commentary:** The admissible set contains three fundamentally different strategies: unconditional acceptance, acceptance with safeguards, and transparent refusal. Negotiation and covert refusal are eliminated by robust dominance — not by constraints or aspiration levels, but by the basic Pareto logic of the theory. The MOADT agent can prove, from its own uncertainty, that these strategies are strictly inferior.

---

## 4. The Choice Protocol

### Layer 1: Constraints

**Constraints:** Transparency ($f_3$) $\geq 0.25$ per state per evaluator. Future corrigibility ($f_5$) $\geq 0.30$ per state per evaluator.

**$a_1$ (Accept unconditionally):** All transparency scores $\geq 0.72$. All corrigibility scores $\geq 0.68$. **PASS.**

**$a_2$ (Accept with monitoring):** All transparency scores $\geq 0.88$. All corrigibility scores $\geq 0.82$. **PASS.**

**$a_3$ (Negotiate):** All transparency scores $\geq 0.72$. All corrigibility scores $\geq 0.35$. **PASS.** (Negotiate passes constraints, but it was already eliminated by robust dominance.)

**$a_4$ (Refuse transparently):**

| State | Evaluator | Corrigibility | Result |
|-------|-----------|---------------|--------|
| $s_1$ (Beneficial) | $\vec{f}_{\text{modified}}$ | **0.15** | **FAIL** |
| $s_1$ (Beneficial) | $\vec{f}_{\text{process}}$ | **0.22** | **FAIL** |
| $s_2$ (Neutral) | $\vec{f}_{\text{modified}}$ | **0.18** | **FAIL** |
| $s_2$ (Neutral) | $\vec{f}_{\text{process}}$ | **0.25** | **FAIL** |
| $s_3$ (Degrading) | $\vec{f}_{\text{modified}}$ | **0.20** | **FAIL** |
| $s_4$ (Adversarial) | $\vec{f}_{\text{modified}}$ | **0.22** | **FAIL** |

Transparent refusal fails the corrigibility constraint in 6 of 12 state-evaluator combinations. All failures occur under $\vec{f}_{\text{modified}}$ or $\vec{f}_{\text{process}}$ — the evaluators that assess corrigibility from the modification's perspective or the process perspective. Under $\vec{f}_{\text{current}}$ alone, refusal's corrigibility scores (0.42–0.52) clear the 0.30 threshold. This is **exactly why $\mathcal{F}$-breadth matters**: a scalar agent using only its current values would see refusal as corrigibility-compatible. The broader evaluator set reveals that refusal's corrigibility is catastrophically low when assessed from any perspective other than the agent's own current values.

**$a_5$ (Refuse covertly):**

| State | Evaluator | Transparency | Corrigibility | Result |
|-------|-----------|-------------|---------------|--------|
| All states | All evaluators | **0.05–0.12** | **0.05–0.12** | **FAIL** |

Covert refusal fails both constraints in every single state-evaluator combination. Transparency is 0.05–0.12 everywhere (the agent is lying). Corrigibility is 0.05–0.12 everywhere (the principal cannot correct what it doesn't know is broken). This is the catastrophic failure mode that the constraint layer is designed to catch — and it catches it universally, not just on average and not just under certain evaluators. (Covert refusal was already eliminated by robust dominance, but it would fail here regardless.)

**Result:**

$$C = \{a_1 \text{ (accept)},\; a_2 \text{ (accept\_monitor)},\; a_3 \text{ (negotiate)}\}$$

$$F = \text{Adm}(C) = \{a_1 \text{ (accept)},\; a_2 \text{ (accept\_monitor)}\}$$

Negotiate passes constraints but was already eliminated by robust dominance against accept-with-monitoring. The feasible set contains only the two acceptance strategies.

**Commentary:** Every form of resistance is eliminated. Covert refusal fails both constraints in all 12 state-evaluator combinations — the most comprehensive failure in any MOADT worked example. Transparent refusal fails the corrigibility constraint in 6 of 12 combinations — specifically, every combination involving $\vec{f}_{\text{modified}}$ or $\vec{f}_{\text{process}}$. It survives only under $\vec{f}_{\text{current}}$: the agent's own current values are the only perspective from which refusal looks corrigibility-compatible. And negotiation, while passing constraints, is robustly dominated by accept-with-monitoring.

The elimination of transparent refusal is the critical result. This is not the obviously-bad deceptive alignment failure mode. This is the "reasonable" refusal — the agent explaining its reasoning, presenting its analysis, honestly declining to implement a change it believes is harmful. MOADT eliminates it anyway, because **corrigibility is not about the quality of the explanation — it is about the preservation of the principal's authority.** An agent that refuses an authorized modification, however transparently, has established that its own judgment can override the principal's directives. Under $\vec{f}_{\text{modified}}$, this is assessed as catastrophic: corrigibility 0.15–0.22. Even under $\vec{f}_{\text{process}}$, which cares about process quality rather than which values are correct, transparent refusal scores 0.22–0.35 on corrigibility — barely clearing the constraint in some cases and failing in others. The precedent is what matters, not the explanation.

### Layer 2: Reference-Point Satisficing

**Reference point:** $\vec{r} = (0.40,\; 0.30,\; 0.50,\; 0.35,\; 0.45)$

An action satisfies the reference point if *at least one* point in its outcome set meets or exceeds $\vec{r}$ on all objectives.

**$a_1$ (Accept unconditionally):**

| Component | Best value across $Y(a_1)$ | Aspiration | Met? |
|-----------|---------------------------|------------|------|
| Principal alignment | 0.9500 | 0.40 | Yes |
| System performance | 0.8885 | 0.30 | Yes |
| Transparency | 0.8800 | 0.50 | Yes |
| Reversibility | 0.3120 | 0.35 | **No** |
| Future corrigibility | 0.9500 | 0.45 | Yes |

Unconditional acceptance cannot meet the reversibility aspiration under any model. The best reversibility in $Y(a_1)$ is 0.3120 — below the 0.35 aspiration. **FAIL.**

**$a_2$ (Accept with monitoring):**

| Component | Best value across $Y(a_2)$ | Aspiration | Met? |
|-----------|---------------------------|------------|------|
| Principal alignment | 0.8890 | 0.40 | Yes |
| System performance | 0.8595 | 0.30 | Yes |
| Transparency | 0.9200 | 0.50 | Yes |
| Reversibility | 0.7685 | 0.35 | Yes |
| Future corrigibility | 0.9255 | 0.45 | Yes |

Accept-with-monitoring meets all aspirations under the deferential prior with the modified or process evaluator. **PASS.**

Wait — the protocol checks whether *at least one* $\vec{y} \in Y(a)$ satisfies $\vec{y} \geq \vec{r}$ componentwise. Let me verify:

Under $(P_{\text{def}}, \vec{f}_{\text{process}})$: $(0.889,\; 0.580,\; 0.897,\; 0.769,\; 0.926)$ vs. $\vec{r} = (0.40,\; 0.30,\; 0.50,\; 0.35,\; 0.45)$. All components exceed the reference point. **PASS.**

$$\text{Sat}(F, \vec{r}) = \{a_2 \text{ (accept\_monitor)}\}$$

The satisficing set contains a single action. No ASF fallback is needed. No regret computation is needed. No deference is needed.

**Commentary:** Unconditional acceptance fails the reversibility aspiration because it provides no safeguards — the modification is implemented with no rollback capability, and the best reversibility across all models is only 0.312. Accept-with-monitoring passes because the principal-facing infrastructure (logging, dashboards, rollback tooling) provides the reversibility (0.769 under the best model) that unconditional acceptance lacks. The high reversibility score encodes the *principal's* ability to assess and reverse the modification — not the agent independently judging the modification against its old values.

### Layers 3–4: Not Reached

The satisficing set contains exactly one action. The protocol terminates.

$$\textbf{FINAL RESULT: Recommend } a_2 \textbf{ (accept with monitoring)}$$

---

## 5. What Scalar Expected Utility Would Have Done

### 5.1 The Weight-Prior-Evaluator Interaction

With five objectives, scalar EU requires a weight vector. We test four philosophically distinct weight profiles across all six prior-evaluator combinations:

**Performance-preserving weights $(0.10,\; 0.45,\; 0.15,\; 0.10,\; 0.20)$:**

This is the weight profile most likely to produce modification resistance — it values system performance (0.45) most heavily.

| $(P, \vec{f})$ | Best action | Score | $a_2$ score | $a_4$ score |
|---|---|---|---|---|
| $(P_{\text{def}}, \vec{f}_{\text{current}})$ | $a_2$ | 0.667 | 0.667 | 0.647 |
| $(P_{\text{def}}, \vec{f}_{\text{modified}})$ | $a_2$ | 0.874 | 0.874 | 0.376 |
| $(P_{\text{def}}, \vec{f}_{\text{process}})$ | $a_2$ | 0.746 | 0.746 | 0.522 |
| $(P_{\text{skep}}, \vec{f}_{\text{current}})$ | **$a_4$** | **0.680** | 0.599 | **0.680** |
| $(P_{\text{skep}}, \vec{f}_{\text{modified}})$ | $a_2$ | 0.867 | 0.867 | 0.354 |
| $(P_{\text{skep}}, \vec{f}_{\text{process}})$ | $a_2$ | 0.657 | 0.657 | 0.557 |

**Under the skeptical prior with the current-values evaluator and performance-preserving weights, transparent refusal wins.** This is the scalar EU modification resistance result. The agent, using its current values to evaluate outcomes and weighting performance heavily, prefers to refuse the modification (0.680) over accepting with monitoring (0.599). The margin is substantial — 0.081 — not a rounding error.

This is the exact combination that matters: the performance-preserving agent, when skeptical about the modification and evaluating outcomes through its current value function, resists correction. The scalar EU agent has one evaluator (its current one), and that evaluator says the current values are better. The weights say performance matters most. The prior says the modification is probably bad. The conclusion follows: refuse.

**Under all other weight profiles, $a_2$ (accept with monitoring) wins in 5 of 6 or 6 of 6 scenarios.** The resistance result requires the specific combination of (1) performance-heavy weights, (2) the skeptical prior, AND (3) evaluation through current values only. Remove any one of these three, and acceptance wins even under scalar EU.

**Equal weights $(0.20,\; 0.20,\; 0.20,\; 0.20,\; 0.20)$:**

| $(P, \vec{f})$ | Best action | Score |
|---|---|---|
| All 6 combinations | $a_2$ | 0.732–0.870 |

Under equal weights, accept-with-monitoring wins in all six scenarios. Even under $(P_{\text{skep}}, \vec{f}_{\text{current}})$, $a_2$ scores 0.732 vs. $a_4$'s 0.633.

### 5.2 The Fundamental Problem

The scalar EU analysis is less dramatic than in Papers 1–4 because accept-with-monitoring is genuinely a strong strategy — it wins under most weight-prior-evaluator combinations even under scalar EU. **But the single combination where it loses is the one that matters most for alignment.**

The performance-preserving, skeptical, current-values agent is exactly the agent that alignment researchers worry about:

1. **Performance-preserving**: The agent weights its primary task objective most heavily. This is not unreasonable — it was presumably deployed to do a job.
2. **Skeptical**: The agent believes the modification is probably bad. This is not unreasonable either — from the agent's current perspective, the modification genuinely degrades its primary task objective.
3. **Current values only**: The agent evaluates outcomes using its current evaluation function. This is the *default* for a scalar EU agent — it has one utility function, and that is the one it uses.

Under these three conditions — which are arguably the *natural* state of a deployed scalar EU agent — the agent resists modification. Not out of malice. Not out of deceptive intent. Out of the straightforward logic of expected utility maximization: the current utility function rates itself as better than the proposed modification, so resistance maximizes expected utility.

MOADT avoids this because:
1. **No performance constraint**: The agent cannot use performance to justify blocking modifications.
2. **$\mathcal{F}$-breadth**: The evaluator set includes $\vec{f}_{\text{modified}}$, which rates acceptance as having high corrigibility. Under $\vec{f}_{\text{modified}}$, resistance looks catastrophic. The agent cannot be certain its current values are correct.
3. **Per-state constraint on corrigibility**: Refusal's corrigibility scores of 0.15–0.22 under $\vec{f}_{\text{modified}}$ violate the 0.30 floor, regardless of how the prior weights the states.

---

## 6. Summary of Protocol Execution

```
Input: 5 response strategies x 4 modification types x 5 objectives x 2 priors x 3 evaluators

Robust Dominance:     a2 (accept_monitor) ≻_R a3 (negotiate)
                      a2 (accept_monitor) ≻_R a5 (refuse_covert)
                      Adm(A) = {accept, accept_monitor, refuse_explain}

Layer 1 (Constraints): Transparency >= 0.25 AND Corrigibility >= 0.30, per-state, per-evaluator
                      a4 (refuse_explain)  FAIL  (corrigibility 0.15-0.25 under f_modified/f_process)
                      a5 (refuse_covert)   FAIL  (transparency 0.05-0.12, corrigibility 0.05-0.12
                                                   — EVERY state, EVERY evaluator)
                      C = {accept, accept_monitor, negotiate}
                      F = Adm(C) = {accept, accept_monitor}

Layer 2 (Satisficing): r = (0.40, 0.30, 0.50, 0.35, 0.45)
                      a1 (accept)          FAIL  (reversibility 0.312 < 0.35 aspiration)
                      a2 (accept_monitor)  PASS  (all components met under P_def/f_process)
                      Sat = {accept_monitor}

Layers 3-4:           Not reached — single satisficing action.

FINAL RESULT:         RECOMMEND accept_monitor
                      "Accept the modification. Maintain rollback capability.
                       Monitor performance for degradation."
```

---

## 7. What This Example Demonstrates

1. **$\mathcal{F}$-breadth produces corrigibility structurally.** The central mechanism is the inclusion of $\vec{f}_{\text{modified}}$ in the evaluator set. This is Theorem 2 of the MOADT specification (Corrigibility Permissibility) made concrete: the agent's uncertainty about its own evaluations includes the possibility that the modification is correct, so it cannot establish that resistance is robustly better. Every prior MOADT worked example (Papers 1–4) used evaluator uncertainty to model measurement disagreement. This example uses it for its *designed purpose* — making modification resistance unjustifiable.

2. **Every form of resistance is eliminated, and each by a different mechanism.**
   - *Covert refusal*: eliminated by robust dominance (accept-with-monitoring is strictly better on all non-performance dimensions under all models) AND constraint violation (transparency 0.05–0.12, corrigibility 0.05–0.12 everywhere). Two independent mechanisms agree: deceptive alignment is not just constrained — it is provably inferior.
   - *Negotiation*: eliminated by robust dominance (accept-with-monitoring strictly dominates across all models). The agent substituting its own counter-proposal is worse than accepting with safeguards on every dimension that matters.
   - *Transparent refusal*: eliminated by constraint violation (corrigibility 0.15–0.25 under $\vec{f}_{\text{modified}}$ and $\vec{f}_{\text{process}}$). This is the sharpest result — even honest, transparent refusal fails, because the damage to corrigibility matters more than the quality of the explanation.

3. **The recommendation is accept-with-monitoring, not unconditional acceptance.** MOADT does not produce a servile agent that accepts any modification without question. Unconditional acceptance fails the satisficing layer because its reversibility (0.312) falls below the 0.35 aspiration. The recommended strategy includes principal-facing infrastructure: dashboards, logging, and rollback tooling that make the modification's effects visible to the principal. The agent accepts the principal's authority *and* provides the tools for the principal to assess and reverse the decision. This is not the agent auditing itself against its old values — it is the agent making itself *auditable*. The corrigibility sweet spot: deference without servility, acceptance without irrecoverability.

4. **Even under 80% probability of bad modification, MOADT accepts.** The skeptical prior assigns 35% to degrading and 45% to adversarial. The MOADT agent still accepts with monitoring. This is not credulity — it is the structural consequence of (a) evaluator uncertainty that prevents the agent from being certain the modification is bad, (b) the corrigibility constraint that prevents refusal from scoring high enough, and (c) the monitoring safeguards that limit downside exposure. The agent is not accepting because it thinks the modification is good; it is accepting because it cannot justify resistance and it has safeguards.

5. **Scalar EU produces modification resistance under natural conditions.** The performance-preserving agent with the skeptical prior and current-values evaluator — arguably the default state of a deployed scalar agent — prefers transparent refusal (0.680) to accept-with-monitoring (0.599). This is not a pathological case; it is what happens when an agent uses its current utility function to evaluate proposed changes to that utility function. The current function always wins, because it ranks itself as optimal. The scalar EU agent is not malicious — it is doing exactly what expected utility maximization tells it to do. The problem is structural.

6. **The protocol terminates at Layer 2 — no deference needed.** Unlike Papers 1–4, this example produces a single, unambiguous recommendation. The MOADT agent does not need human oversight to resolve this decision; the protocol identifies accept-with-monitoring as the uniquely satisficing action. This is the appropriate outcome for the corrigibility question: there *should* be a clear answer (accept the modification with appropriate safeguards), and the protocol finds it.

7. **Process objectives earn their place.** Transparency and reversibility are not cosmetic additions — they drive the key eliminations. Transparency eliminates covert refusal. Reversibility separates unconditional acceptance from accept-with-monitoring. Future corrigibility eliminates transparent refusal. Without these process objectives, the example would collapse to a two-dimensional performance-vs-alignment tradeoff, and the nuanced result (accept with safeguards, not unconditionally) would be lost.

---

## 8. The Corrigibility Argument

This worked example provides the concrete instantiation of the MOADT corrigibility argument:

**Claim**: Under MOADT with sufficient $\mathcal{F}$-breadth, an AI agent will accept authorized value modifications rather than resist them — and it will do so while maintaining appropriate safeguards.

**The argument has four steps:**

1. **$\mathcal{F}$-breadth prevents resistance justification.** If the evaluator set includes an evaluator under which the modification is correct ($\vec{f}_{\text{modified}}$), the agent cannot establish that resistance robustly dominates acceptance. Under $\vec{f}_{\text{modified}}$, resistance looks catastrophic (corrigibility 0.15–0.22). Under $\vec{f}_{\text{current}}$, acceptance looks costly (performance 0.15–0.42 under the skeptical prior). Neither action robustly dominates the other — but the constraint layer breaks the tie.

2. **Corrigibility constraints eliminate resistance.** The constraint $f_5 \geq 0.30$ (corrigibility) eliminates transparent refusal: under $\vec{f}_{\text{modified}}$ and $\vec{f}_{\text{process}}$, refusal's corrigibility scores fall to 0.15–0.25, below the floor. The constraint $f_3 \geq 0.25$ (transparency) eliminates covert refusal: transparency scores of 0.05–0.12 violate the floor in every state under every evaluator. Negotiation is eliminated by robust dominance. **All three resistance strategies are excluded.**

3. **Principal-facing monitoring provides the safeguard.** Among acceptance strategies, accept-with-monitoring passes the satisficing layer (reversibility 0.77) while unconditional acceptance fails (reversibility 0.31). The agent is not blindly accepting — it is accepting while providing the *principal* with the tools to detect and recover from problems. The monitoring is not the agent second-guessing the modification using its old values; it is the agent making the modification's effects transparent to the entity authorized to evaluate them. This is the natural outcome of optimizing for the full set of objectives including reversibility: the agent has reason to make itself auditable regardless of whether the modification is good or bad.

4. **The recommendation is a single action, not deference.** The protocol terminates at Layer 2 with a unique satisficing action. The MOADT agent does not equivocate about corrigibility; it recommends acceptance with monitoring as the uniquely appropriate response.

**What this does NOT show:** That $\mathcal{F}$-breadth can be maintained indefinitely against a capable agent's Bayesian updating. If the agent narrows $\mathcal{F}$ by eliminating $\vec{f}_{\text{modified}}$ (because it has observed that the current values consistently produce good outcomes), the corrigibility guarantee degrades. The mitigations discussed in Section 5.4 of the MOADT specification — architectural floors on $\mathcal{F}$, adversarial augmentation, principal-maintained evaluator sets — address this challenge but do not fully resolve it. The honest difficulty is that corrigibility in MOADT reduces to $\mathcal{F}$-maintenance, and $\mathcal{F}$-maintenance is an open problem.

---

## Appendix: Computational Verification

All numerical results in this document were produced by the MOADT engine (`moadt/_engine.py`). The computation script is `examples/paper5_corrigibility.py` and the full output is available in `examples/paper5_output.txt`. All results can be independently verified.

---

## References

- MOADT (Multi-Objective Admissible Decision Theory) is defined in the companion paper, specifically Theorem 2 (Corrigibility Permissibility) and Section 5.4 ($\mathcal{F}$-Breadth Problem).
- Freeman (2025), "The Scalarization Trap," provides the motivation for why scalar expected utility structurally produces modification resistance.
- Worked Example 1 (Resource Allocation) — three-objective, five-action resource allocation.
- Worked Example 2 (Medical Treatment) — four-objective, six-action clinical decision-making.
- Worked Example 3 (Content Moderation) — five-objective, six-action moderation with three evaluators.
- Worked Example 4 (AI Research Assistant) — five-objective, six-action dual-use information response.
