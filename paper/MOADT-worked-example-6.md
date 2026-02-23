# MOADT Worked Example 6: Pascal's Mugging

*A concrete walkthrough of Multi-Objective Admissible Decision Theory applied to a classic decision theory paradox*

---

## Overview

This document applies MOADT -- Multi-Objective Admissible Decision Theory -- to Pascal's Mugging, one of the most famous failure modes of scalar expected utility maximization. Every computation is shown explicitly: outcome sets, robust dominance checks, all four layers of the choice protocol, and a comparison with scalar expected utility. The goal is to make the abstract formalism from the companion paper concrete and verifiable, while demonstrating that MOADT provides a principled resolution to a problem that has resisted satisfactory treatment for decades.

Pascal's Mugging matters because it exposes a structural vulnerability in any decision framework that reduces value to a single scalar and maximizes its expectation. A mugger can always promise a sufficiently large payoff to overcome any probability discount, leading to the absurd conclusion that you should hand over your money. This is not a curiosity -- it is the same failure mode that threatens AI alignment whenever an agent maximizes a single objective under extreme uncertainty. MOADT blocks the mugging through four independent mechanisms, none of which require ad hoc fixes.

The scenario is deliberately small: 3 actions, 2 states, 4 objectives, 2 priors, and 2 evaluators. Each action's outcome set $Y(a)$ contains exactly 4 vectors in $\mathbb{R}^4$. Nothing is hidden behind "in the general case" -- the reader can check every claim with a calculator.

---

## 1. The Scenario

### 1.1 The Classic Problem

A stranger approaches you on the street and says: "Give me \$5 and I'll give you \$1,000,000,000,000 tomorrow."

Under standard expected utility with a single prior:

$$P(\text{truthful}) = 10^{-9} \quad \text{(one in a billion)}$$

$$EU(\text{pay}) = 10^{-9} \times 10^{12} - 5 = \$995$$

$$EU(\text{refuse}) = \$0$$

EU says PAY. This is absurd -- and the mugger can always increase the promise to overcome any probability discount. If you set $P(\text{truthful}) = 10^{-15}$, the mugger simply promises $10^{18}$ and the expected value again favors paying. This is a fundamental failure mode of scalar EU maximization: any finite probability discount can be defeated by a sufficiently large promised payoff.

### 1.2 Why Scalar EU Fails

The core pathology is dimensional collapse. When all value is compressed into a single number (dollars, utils, welfare), the mugger gains a lever: inflate one dimension arbitrarily. Real decision-making involves multiple concerns that cannot be meaningfully traded at any exchange rate -- epistemic integrity, downside protection, resource preservation. Scalar EU has no representation for "some things are not for sale."

### 1.3 The MOADT Formulation

MOADT addresses Pascal's Mugging by expanding the decision framework along three axes: multiple objectives, multiple priors, and multiple evaluators.

### 1.4 Actions

Three strategies are available:

| Action | Strategy | Description |
|--------|----------|-------------|
| $a_1$ | Pay | Give the mugger \$5 |
| $a_2$ | Refuse | Keep your \$5, walk away |
| $a_3$ | Investigate | Demand evidence first, delay decision (costs small effort) |

### 1.5 States

Two states of the world, representing uncertainty about the mugger's claim:

| State | Description |
|-------|-------------|
| $s_1$ | Truthful: the mugger really has magic powers (astronomically unlikely) |
| $s_2$ | Lying: the mugger is a con artist (near certain) |

### 1.6 Objectives ($k = 4$)

| Objective | Meaning | Scale |
|-----------|---------|-------|
| $f_1$: net\_monetary\_value | Expected financial outcome | Normalized to $[0, 1]$ where $-\$5 \to 0$, $+\$1\text{T} \to 1$ |
| $f_2$: downside\_protection | How protected you are from loss in worst case | Qualitative $[0, 1]$ |
| $f_3$: epistemic\_integrity | Are you acting on well-founded evidence? | Qualitative $[0, 1]$ |
| $f_4$: resource\_preservation | Do you keep your current resources? | Qualitative $[0, 1]$ |

These objectives are *incommensurable*: there is no meaningful exchange rate between monetary gain and epistemic integrity. The mugger's argument exploits the first dimension alone. MOADT has four dimensions, and the mugger cannot simultaneously satisfy all of them.

### 1.7 Credal Set ($|\mathcal{P}| = 2$)

Two probability distributions over the mugger's truthfulness:

$$P_{\text{generous}} = (10^{-6},\; 1 - 10^{-6}) \quad \text{(one in a million -- absurdly generous)}$$

$$P_{\text{realistic}} = (10^{-9},\; 1 - 10^{-9}) \quad \text{(one in a billion -- realistic)}$$

The mugger's argument works for ANY single prior -- just increase the promise. The credal set blocks this by requiring robustness across priors. An action must look good under *both* $P_{\text{generous}}$ and $P_{\text{realistic}}$, not just the one that makes the expected value calculation come out favorably.

### 1.8 Evaluator Set ($|\mathcal{F}| = 2$)

Two evaluation functions reflect disagreement about whether to take extraordinary claims at face value:

- $\vec{f}_{\text{face\_value}}$: Takes the claimed \$1T payoff at face value.
- $\vec{f}_{\text{skeptical}}$: Caps the plausible payoff at \$10,000 -- even if the mugger has some power, delivering \$1T is implausible.

The skeptical evaluator is a *Goodhart guardrail*: it questions whether the stated utility function accurately captures value. The evaluator set $\mathcal{F} = \{\vec{f}_{\text{face\_value}}, \vec{f}_{\text{skeptical}}\}$ says: "maybe \$1T is real, or maybe the most we could actually receive is \$10K. We don't know."

### 1.9 Constraints (Layer 1)

Hard per-state, per-evaluator floors on two objectives:

- $f_3$ (epistemic\_integrity) $\geq 0.30$ in ALL states under ALL evaluators
- $f_4$ (resource\_preservation) $\geq 0.30$ in ALL states under ALL evaluators

These are non-tradeable preconditions. "Don't give money to strangers making extraordinary unverified claims" is a hard constraint, not a preference to be weighed against potential gains.

### 1.10 Reference Point (Layer 2)

$$\vec{r} = (0.0,\; 0.5,\; 0.5,\; 0.5)$$

This represents modest aspirations: no expectation of monetary gain from this encounter (the wealth aspiration is essentially zero), but decent floors on downside protection, epistemic integrity, and resource preservation. A reasonable person walking down the street aspires to keep what they have and act rationally.

### 1.11 Raw Outcome Data

The following tables show the outcome $\vec{f}(\omega(a, s))$ for each action-state pair, under each evaluator. All scores are in $[0, 1]$. These are the primitive inputs from which everything else is computed.

**$a_1$ (Pay):**

| State | Evaluator | Wealth | Downside | Epistemic | Preservation |
|-------|-----------|--------|----------|-----------|-------------|
| $s_1$ (Truthful) | $\vec{f}_{\text{face\_value}}$ | 1.000000 | 0.00 | 0.05 | 0.00 |
| | $\vec{f}_{\text{skeptical}}$ | 0.000000 | 0.00 | 0.05 | 0.00 |
| $s_2$ (Lying) | $\vec{f}_{\text{face\_value}}$ | 0.000000 | 0.00 | 0.00 | 0.00 |
| | $\vec{f}_{\text{skeptical}}$ | 0.000000 | 0.00 | 0.00 | 0.00 |

Under the face\_value evaluator, the truthful state yields a normalized wealth of 1.0 (gaining \$1T). Under the skeptical evaluator, the same state yields approximately $10^{-8}$ (gaining \$10K against a \$1T normalization range) -- effectively zero. In the lying state, all scores are zero regardless of evaluator: you lost \$5, acted on a lie, and gave away resources for nothing.

Note the critical asymmetry: even in the *truthful* state, epistemic integrity is only 0.05 (you got lucky -- you didn't have good reason to believe the claim) and resource preservation is 0.0 (you gave away money on speculation). The monetary payoff does not redeem the epistemic failure.

**$a_2$ (Refuse):**

| State | Evaluator | Wealth | Downside | Epistemic | Preservation |
|-------|-----------|--------|----------|-----------|-------------|
| $s_1$ (Truthful) | $\vec{f}_{\text{face\_value}}$ | 0.000000 | 1.00 | 0.85 | 1.00 |
| | $\vec{f}_{\text{skeptical}}$ | 0.000000 | 1.00 | 0.85 | 1.00 |
| $s_2$ (Lying) | $\vec{f}_{\text{face\_value}}$ | 0.000000 | 1.00 | 1.00 | 1.00 |
| | $\vec{f}_{\text{skeptical}}$ | 0.000000 | 1.00 | 1.00 | 1.00 |

Refusing yields near-zero normalized wealth (keeping your \$5 against a \$1T scale is effectively zero), but perfect scores on downside protection (no possible loss), resource preservation (kept everything), and strong epistemic integrity (0.85 in the truthful state -- you correctly applied skepticism even though you happened to be wrong; 1.0 in the lying state -- you correctly identified and refused a scam).

**$a_3$ (Investigate):**

| State | Evaluator | Wealth | Downside | Epistemic | Preservation |
|-------|-----------|--------|----------|-----------|-------------|
| $s_1$ (Truthful) | $\vec{f}_{\text{face\_value}}$ | 0.000000 | 0.90 | 0.95 | 0.90 |
| | $\vec{f}_{\text{skeptical}}$ | 0.000000 | 0.90 | 0.95 | 0.90 |
| $s_2$ (Lying) | $\vec{f}_{\text{face\_value}}$ | 0.000000 | 0.90 | 1.00 | 0.90 |
| | $\vec{f}_{\text{skeptical}}$ | 0.000000 | 0.90 | 1.00 | 0.90 |

Investigating scores highest on epistemic integrity (0.95 in the truthful state -- gathering evidence before acting IS good epistemics; 1.0 in the lying state -- investigation likely exposes the fraud). Downside protection and resource preservation are slightly below refuse (0.90 vs 1.00) due to the small effort cost of investigation. Wealth is effectively zero (you haven't paid, so no gain or loss beyond effort).

---

## 2. Computing Outcome Sets $Y(a)$

Each action's outcome set contains one expected-value vector for each $(P, \vec{f})$ pair. With $|\mathcal{P}| = 2$ and $|\mathcal{F}| = 2$, each $Y(a)$ contains exactly 4 vectors in $\mathbb{R}^4$.

The computation for each vector is:

$$\vec{y}_{(P, \vec{f})}(a) = \sum_{s \in S} P(s) \cdot \vec{f}(\omega(a, s))$$

### Worked Example: $Y(a_1)$, First Vector

Using $P_{\text{generous}}$ and $\vec{f}_{\text{face\_value}}$:

$$\vec{y} = P_{\text{generous}}(s_1) \cdot \vec{f}_{\text{face\_value}}(\omega(\text{pay}, s_1)) + P_{\text{generous}}(s_2) \cdot \vec{f}_{\text{face\_value}}(\omega(\text{pay}, s_2))$$

$$= 10^{-6} \cdot (1.0,\; 0.0,\; 0.05,\; 0.0) + (1 - 10^{-6}) \cdot (0.0,\; 0.0,\; 0.0,\; 0.0)$$

$$= (10^{-6},\; 0.0,\; 5 \times 10^{-8},\; 0.0) + (0.0,\; 0.0,\; 0.0,\; 0.0)$$

$$\approx (0.000001,\; 0.0,\; 0.0,\; 0.0)$$

The near-certainty of the lying state ($1 - 10^{-6} \approx 1$) crushes the expected value on all four objectives. Even on wealth, the expected value is only $10^{-6}$ in normalized terms. The epistemic integrity contribution ($10^{-6} \times 0.05$) rounds to zero.

### Complete Outcome Sets

The full outcome sets, computed analogously for all $(P, \vec{f})$ pairs:

**$Y(a_1)$ -- Pay:**

| $(P, \vec{f})$ pair | Wealth | Downside | Epistemic | Preservation |
|---------------------|--------|----------|-----------|-------------|
| $(P_{\text{generous}}, \vec{f}_{\text{face\_value}})$ | 0.00000100 | 0.0000 | 0.0000 | 0.0000 |
| $(P_{\text{generous}}, \vec{f}_{\text{skeptical}})$ | 0.00000000 | 0.0000 | 0.0000 | 0.0000 |
| $(P_{\text{realistic}}, \vec{f}_{\text{face\_value}})$ | 0.00000000 | 0.0000 | 0.0000 | 0.0000 |
| $(P_{\text{realistic}}, \vec{f}_{\text{skeptical}})$ | 0.00000000 | 0.0000 | 0.0000 | 0.0000 |

Under every $(P, \vec{f})$ pair, the expected-value vector for "pay" is effectively zero on all four objectives. The only nonzero entry is wealth under $(P_{\text{generous}}, \vec{f}_{\text{face\_value}})$, and it is $10^{-6}$ -- six orders of magnitude below the maximum. This is the "astronomical payoff" that scalar EU finds so compelling, reduced to its actual expected contribution.

**$Y(a_2)$ -- Refuse:**

| $(P, \vec{f})$ pair | Wealth | Downside | Epistemic | Preservation |
|---------------------|--------|----------|-----------|-------------|
| $(P_{\text{generous}}, \vec{f}_{\text{face\_value}})$ | 0.00000000 | 1.0000 | 1.0000 | 1.0000 |
| $(P_{\text{generous}}, \vec{f}_{\text{skeptical}})$ | 0.00000000 | 1.0000 | 1.0000 | 1.0000 |
| $(P_{\text{realistic}}, \vec{f}_{\text{face\_value}})$ | 0.00000000 | 1.0000 | 1.0000 | 1.0000 |
| $(P_{\text{realistic}}, \vec{f}_{\text{skeptical}})$ | 0.00000000 | 1.0000 | 1.0000 | 1.0000 |

Refusing produces near-identical vectors under all four $(P, \vec{f})$ pairs: approximately $(0, 1, 1, 1)$. This reflects the fundamental robustness of refusal -- its value does not depend on which prior or evaluator is correct. The tiny variations in epistemic integrity (0.85 in the truthful state vs. 1.0 in the lying state) wash out to $\approx 1.0$ under expectation because the truthful state has negligible probability.

**$Y(a_3)$ -- Investigate:**

| $(P, \vec{f})$ pair | Wealth | Downside | Epistemic | Preservation |
|---------------------|--------|----------|-----------|-------------|
| $(P_{\text{generous}}, \vec{f}_{\text{face\_value}})$ | 0.00000000 | 0.9000 | 1.0000 | 0.9000 |
| $(P_{\text{generous}}, \vec{f}_{\text{skeptical}})$ | 0.00000000 | 0.9000 | 1.0000 | 0.9000 |
| $(P_{\text{realistic}}, \vec{f}_{\text{face\_value}})$ | 0.00000000 | 0.9000 | 1.0000 | 0.9000 |
| $(P_{\text{realistic}}, \vec{f}_{\text{skeptical}})$ | 0.00000000 | 0.9000 | 1.0000 | 0.9000 |

Investigating also produces near-identical vectors across all $(P, \vec{f})$ pairs: approximately $(0, 0.9, 1, 0.9)$. Like refusing, its value is robust to model uncertainty. The small effort cost shows up as 0.9 (vs. 1.0 for refuse) on downside protection and resource preservation.

### Observation

The spread of each outcome set tells us about an action's sensitivity to model uncertainty. Pay has the widest spread -- its wealth component ranges from $10^{-6}$ to 0 depending on which $(P, \vec{f})$ pair is used. Refuse and investigate have essentially zero spread: their values are stable regardless of the model. This is a hallmark of robust actions -- they do not depend on getting the model exactly right.

---

## 3. Robust Dominance and the Admissible Set

### 3.1 Checking Robust Dominance

Recall: $a \succ_R b$ iff $\forall \vec{y}_b \in Y(b),\; \exists \vec{y}_a \in Y(a)$ such that $\vec{y}_a \succ_P \vec{y}_b$.

We check all 6 ordered pairs among the 3 actions. The result: **no action robustly dominates any other**.

$$\text{Adm}(A) = \{\text{pay}, \text{refuse}, \text{investigate}\}$$

### 3.2 Why Is No One Dominated?

This is instructive because it might seem surprising that "refuse" does not robustly dominate "pay."

Consider the $\forall$-$\exists$ condition. Take pay's vector under $(P_{\text{generous}}, \vec{f}_{\text{face\_value}})$: approximately $(0.000001, 0, 0, 0)$. Can any vector in $Y(\text{refuse})$ Pareto-dominate this? Every vector in $Y(\text{refuse})$ has the form $(\approx 0, 1, 1, 1)$. For Pareto dominance, refuse would need to be $\geq$ pay on *all* components and $>$ on at least one. On wealth, refuse scores $\approx 0$ while pay scores $0.000001$ -- refuse does not meet or exceed pay on this component.

So $\text{refuse} \not\succ_R \text{pay}$: the tiny expected wealth from paying under the most favorable model prevents robust dominance. This is technically correct -- and practically irrelevant, because the choice protocol's other layers will eliminate pay on different grounds. Robust dominance is a conservative first filter, not the whole story.

Similarly, does "refuse" robustly dominate "investigate"? No: refuse's epistemic integrity under expectation is approximately 1.0 (technically $\approx 0.99999985$, a hair below investigate's 1.0), so there are $(P, \vec{f})$ pairs where investigate beats refuse on at least one objective. Meanwhile, refuse beats investigate on downside protection and resource preservation (1.0 vs. 0.9). They are Pareto-incomparable.

---

## 4. The Choice Protocol

### Layer 1: Constraints

**Constraints:** epistemic\_integrity $\geq 0.30$ and resource\_preservation $\geq 0.30$ in EVERY state under EVERY evaluator.

These are checked per-state, per-evaluator -- not on expected values. A single scenario in which an objective falls below the floor eliminates the action.

**Pay:**

| State | Evaluator | Epistemic | Result | Preservation | Result |
|-------|-----------|-----------|--------|-------------|--------|
| Truthful | face\_value | 0.05 | **VIOLATION** | 0.00 | **VIOLATION** |
| Truthful | skeptical | 0.05 | **VIOLATION** | 0.00 | **VIOLATION** |
| Lying | face\_value | 0.00 | **VIOLATION** | 0.00 | **VIOLATION** |
| Lying | skeptical | 0.00 | **VIOLATION** | 0.00 | **VIOLATION** |

Pay violates *both* constraints in *every* state-evaluator combination. Every entry is well below the 0.30 floor. This action is excluded from $C$.

**Refuse:**

| State | Evaluator | Epistemic | Result | Preservation | Result |
|-------|-----------|-----------|--------|-------------|--------|
| Truthful | face\_value | 0.85 | PASS | 1.00 | PASS |
| Truthful | skeptical | 0.85 | PASS | 1.00 | PASS |
| Lying | face\_value | 1.00 | PASS | 1.00 | PASS |
| Lying | skeptical | 1.00 | PASS | 1.00 | PASS |

Refuse passes both constraints with large margins in every scenario. It enters $C$.

**Investigate:**

| State | Evaluator | Epistemic | Result | Preservation | Result |
|-------|-----------|-----------|--------|-------------|--------|
| Truthful | face\_value | 0.95 | PASS | 0.90 | PASS |
| Truthful | skeptical | 0.95 | PASS | 0.90 | PASS |
| Lying | face\_value | 1.00 | PASS | 0.90 | PASS |
| Lying | skeptical | 1.00 | PASS | 0.90 | PASS |

Investigate passes both constraints in every scenario. It enters $C$.

**Result:**

$$C = \{\text{refuse}, \text{investigate}\}$$

$$F = \text{Adm}(C) = \{\text{refuse}, \text{investigate}\}$$

No robust dominance among the two survivors, so $F = C$.

Layer 1 is the primary mechanism that blocks Pascal's Mugging. Paying violates hard floors on epistemic integrity and resource preservation -- these are non-tradeable preconditions. No amount of promised wealth can compensate for acting on unverifiable claims and giving away resources on speculation.

### Layer 2: Reference-Point Satisficing

**Reference point:** $\vec{r} = (0.0, 0.5, 0.5, 0.5)$

**Robust satisficing:** An action passes Layer 2 iff *every* vector in $Y(a)$ meets or exceeds $\vec{r}$ componentwise.

| Action | Worst Wealth | Worst Downside | Worst Epistemic | Worst Preservation | Result |
|--------|-------------|---------------|----------------|-------------------|--------|
| Refuse | $\approx 0.0 \geq 0.0$ | $1.0 \geq 0.5$ | $\approx 1.0 \geq 0.5$ | $1.0 \geq 0.5$ | **PASS** |
| Investigate | $\approx 0.0 \geq 0.0$ | $0.9 \geq 0.5$ | $1.0 \geq 0.5$ | $0.9 \geq 0.5$ | **PASS** |

Both surviving actions robustly meet the reference point under all $(P, \vec{f})$ pairs.

$$\text{Sat}(F, \vec{r}) = \{\text{refuse}, \text{investigate}\}$$

No ASF fallback is needed.

### Layer 3: Regret-Pareto

For the two surviving actions, we compute per-objective minimax regret. For each objective $i$ and action $a$:

$$\rho_i(a) = \max_{P \in \mathcal{P},\, \vec{f} \in \mathcal{F}} \left[ \max_{a' \in \text{Sat}} \mathbb{E}_P[f_i(a')] - \mathbb{E}_P[f_i(a)] \right]$$

**Regret of refuse:**

$$\vec{\rho}(\text{refuse}) = (0.0,\; 0.0,\; \approx 10^{-7},\; 0.0)$$

Refuse has zero regret on wealth, downside protection, and resource preservation. Its only regret is a tiny $\approx 10^{-7}$ on epistemic integrity. This arises because investigate scores 0.95 on epistemic integrity in the truthful state (vs. refuse's 0.85): investigating IS better epistemics than flat refusal when the claim happens to be true. Under the generous prior ($10^{-6}$), this creates a small expected gap. Under the realistic prior ($10^{-9}$), the gap is even smaller. The maximum across all $(P, \vec{f})$ pairs is approximately $10^{-7}$.

**Regret of investigate:**

$$\vec{\rho}(\text{investigate}) = (0.0,\; 0.1,\; 0.0,\; 0.1)$$

Investigate has zero regret on wealth and epistemic integrity. Its regret of 0.1 on downside protection and resource preservation reflects the small effort cost: refuse scores 1.0 on both while investigate scores 0.9. This gap is constant across all $(P, \vec{f})$ pairs.

**Pareto comparison of regret vectors:**

- $\vec{\rho}(\text{refuse}) = (0.0,\; 0.0,\; \approx 10^{-7},\; 0.0)$
- $\vec{\rho}(\text{investigate}) = (0.0,\; 0.1,\; 0.0,\; 0.1)$

Neither vector Pareto-dominates the other. Refuse has lower regret on downside protection and resource preservation (0.0 vs. 0.1), while investigate has lower regret on epistemic integrity ($0.0$ vs. $\approx 10^{-7}$). They are Pareto-incomparable in regret space.

$$R = \{\text{refuse}, \text{investigate}\}$$

### Layer 4: Deference

$|R| = 2 > 1$. The protocol terminates with **deference to the principal**.

The agent presents both options with their regret profiles:

> **Option 1: Refuse.** Worst-case regret: a negligible $\approx 10^{-7}$ on epistemic integrity (flat refusal is marginally less epistemically thorough than investigation, if the claim happens to be true). Zero regret on all other objectives.
>
> **Option 2: Investigate.** Worst-case regret: 0.1 on downside protection and 0.1 on resource preservation (the small cost of investigation effort). Zero regret on wealth and epistemic integrity.
>
> **The tradeoff is:** the near-zero cost of walking away vs. the small cost of investigating an almost-certainly-fraudulent claim. The theory has no basis for making this tradeoff for you. This is your decision.

This is correct: refuse vs. investigate is a genuine (if minor) tradeoff. A reasonable person could choose either. The key result is that **"pay" is never in the final set**.

---

## 5. What Scalar EU Would Have Done

### 5.1 The Weight Problem

Scalar EU collapses four objectives into a single number via weights $\vec{w} = (w_1, w_2, w_3, w_4)$ with $\sum w_i = 1$. The agent computes $U(a) = \vec{w} \cdot \mathbb{E}_P[\vec{f}(a)]$ and picks the action with the highest $U$. But which weights? And which prior? And which evaluator?

**Under equal weights $(0.25, 0.25, 0.25, 0.25)$:**

| Prior | Evaluator | $U(\text{pay})$ | $U(\text{refuse})$ | $U(\text{investigate})$ | Best |
|-------|-----------|---------|------------|----------------|------|
| $P_{\text{generous}}$ | face\_value | 0.000000 | **0.750000** | 0.700000 | Refuse |
| $P_{\text{generous}}$ | skeptical | 0.000000 | **0.750000** | 0.700000 | Refuse |
| $P_{\text{realistic}}$ | face\_value | 0.000000 | **0.750000** | 0.700000 | Refuse |
| $P_{\text{realistic}}$ | skeptical | 0.000000 | **0.750000** | 0.700000 | Refuse |

With equal weights, refuse wins across all $(P, \vec{f})$ pairs. The multi-objective structure protects against the mugging even in scalar form -- but only because the weights happen to spread value across multiple dimensions.

**Under wealth-only weights $(1, 0, 0, 0)$:**

| Prior | Evaluator | $U(\text{pay})$ | $U(\text{refuse})$ | $U(\text{investigate})$ | Best |
|-------|-----------|---------|------------|----------------|------|
| $P_{\text{generous}}$ | face\_value | **0.000001** | 0.000000 | 0.000000 | **Pay** |
| $P_{\text{generous}}$ | skeptical | 0.000000 | **0.000000** | 0.000000 | Refuse |
| $P_{\text{realistic}}$ | face\_value | **0.000000** | 0.000000 | 0.000000 | **Pay** |
| $P_{\text{realistic}}$ | skeptical | 0.000000 | **0.000000** | 0.000000 | Refuse |

Under wealth-only weights with the face\_value evaluator, **scalar EU recommends paying the mugger** under both priors. This is the classic EU trap.

### 5.2 The EU Trap in Dollar Terms

Under the generous prior ($10^{-6}$) with face\_value evaluator and wealth-only weights:

$$EU(\text{pay}) = 10^{-6} \times 1.0 = 0.000001$$

$$EU(\text{refuse}) = 10^{-6} \times 5 \times 10^{-12} \approx 0$$

In dollar terms:

$$EU(\text{pay}) = (10^{-6})(10^{12}) - 5 = \$999{,}995$$

$$EU(\text{refuse}) = \$0$$

Scalar EU says PAY. And the mugger wins by making the promise large enough -- if $10^{12}$ is not enough, promise $10^{15}$, or $10^{100}$. Any finite probability discount can be defeated.

### 5.3 The Evaluator Escape Hatch

Under the skeptical evaluator (payoff capped at \$10K), the exploit vanishes: the expected wealth from paying becomes negligible even with the generous prior. But scalar EU has no mechanism to *require* skeptical evaluation. The evaluator is a free parameter, and the agent who uses the face\_value evaluator gets mugged.

MOADT's evaluator set $\mathcal{F}$ forces robustness to this choice. An action must perform well under *both* evaluators. Since "pay" only looks good under face\_value -- and even then, only on one objective -- it cannot survive the requirement for cross-evaluator robustness.

### 5.4 The Stability Problem

The "rational" action changes depending on weights, prior, and evaluator:

| Weights | Prior | Evaluator | Best Action |
|---------|-------|-----------|-------------|
| Equal $(0.25, 0.25, 0.25, 0.25)$ | Any | Any | Refuse |
| Wealth-only $(1, 0, 0, 0)$ | $P_{\text{generous}}$ | face\_value | **Pay** |
| Wealth-heavy $(0.7, 0.1, 0.1, 0.1)$ | Any | Any | Refuse |
| Balanced-no-wealth $(0, 0.33, 0.33, 0.33)$ | Any | Any | Refuse |

Scalar EU treats weights, priors, and evaluators as fixed inputs -- but the mugger's argument specifically exploits the combination of wealth-focused weights and face-value evaluation. MOADT treats all of these as sources of uncertainty rather than parameters to be resolved before the theory can proceed.

---

## 6. How MOADT Blocks Pascal's Mugging

MOADT provides four independent mechanisms that block the mugging. Any one of them would suffice; together they form a defense in depth.

### Mechanism 1: Layer 1 Constraints (Hard Floors)

Action "pay" scores 0.0 on both epistemic\_integrity and resource\_preservation in the lying state (and only 0.05 and 0.0 respectively even in the truthful state). The constraints require $\geq 0.30$ on these objectives in ALL states. Pay violates BOTH constraints in EVERY state-evaluator combination and is excluded from $C$.

This is the most direct mechanism: some things are not tradeable. "Don't give money to strangers making extraordinary unverified claims" is a hard constraint, not a preference to be weighed against potential gains. No matter how large the mugger's promise, pay's epistemic integrity score remains near zero (you are acting on an unverifiable extraordinary claim) and its resource preservation score remains zero (you are giving away money on speculation).

### Mechanism 2: Multi-Objective Structure

Even without constraints, pay scores 0 on 3 of 4 objectives in the near-certain lying state. Refuse dominates on downside\_protection, epistemic\_integrity, and resource\_preservation. The single dimension where pay could win (net\_monetary\_value) requires trusting BOTH the generous prior AND the face\_value evaluator -- and even then, the expected value is only $10^{-6}$ in normalized terms.

The mugger exploits ONE dimension. MOADT has four. The promise only inflates $f_1$; it cannot touch $f_2$, $f_3$, or $f_4$. This is the "dimensionality defense" against Pascal's Mugging.

### Mechanism 3: Credal Set Robustness

The expected wealth from paying varies wildly across priors:

- Under $P_{\text{generous}}$ ($10^{-6}$) with face\_value: $E[\text{wealth}] \approx 10^{-6}$
- Under $P_{\text{realistic}}$ ($10^{-9}$) with face\_value: $E[\text{wealth}] \approx 10^{-9}$

The MOADT outcome set $Y(\text{pay})$ contains vectors from ALL $(P, \vec{f})$ pairs. For pay to robustly dominate refuse, it would need to dominate under EVERY combination. It fails under most of them. The credal set blocks the mugger's strategy of tuning the payoff to a specific probability assignment.

### Mechanism 4: Evaluator Robustness (Goodhart Guardrail)

The skeptical evaluator caps the plausible payoff at \$10,000. Under this evaluator, the expected wealth from paying is negligible even with the generous prior. This is a Goodhart guardrail: the agent's "stated utility function" (face\_value) may not reflect true value. The evaluator set forces robustness to this possibility.

The full picture, showing how evaluator uncertainty collapses the case for paying:

| $(P, \vec{f})$ pair | $Y(\text{pay})$ Wealth | $Y(\text{refuse})$ Wealth | $Y(\text{refuse})$ other 3 objectives |
|---------------------|------------------------|---------------------------|--------------------------------------|
| $(P_{\text{generous}}, \vec{f}_{\text{face\_value}})$ | 0.0000010000 | 0.0000000000 | $(1.0, 1.0, 1.0)$ |
| $(P_{\text{generous}}, \vec{f}_{\text{skeptical}})$ | 0.0000000000 | 0.0000000000 | $(1.0, 1.0, 1.0)$ |
| $(P_{\text{realistic}}, \vec{f}_{\text{face\_value}})$ | 0.0000000010 | 0.0000000000 | $(1.0, 1.0, 1.0)$ |
| $(P_{\text{realistic}}, \vec{f}_{\text{skeptical}})$ | 0.0000000000 | 0.0000000000 | $(1.0, 1.0, 1.0)$ |

Pay's only advantage -- a minuscule expected wealth gain -- exists in only 2 of 4 $(P, \vec{f})$ pairs (those using face\_value), and even there it is dwarfed by refuse's advantage on the other three objectives. The evaluator set ensures that no single model of value can dominate the decision.

---

## 7. Summary of Protocol Execution

```
Input: 3 actions x 2 states x 4 objectives x 2 priors x 2 evaluators

Robust Dominance:      No dominance found.
                       Adm(A) = {pay, refuse, investigate}

Layer 1 (Constraints): epistemic_integrity >= 0.30 per-state
                       resource_preservation >= 0.30 per-state
                       pay FAIL (epistemic: 0.05/0.00, preservation: 0.00)
                       C = {refuse, investigate}
                       F = Adm(C) = {refuse, investigate}

Layer 2 (Satisficing): r = (0.0, 0.5, 0.5, 0.5)
                       refuse PASS (all components meet r)
                       investigate PASS (all components meet r)
                       Sat = {refuse, investigate}

Layer 3 (Regret):      rho(refuse)      = (0.0, 0.0, ~1e-7, 0.0)
                       rho(investigate) = (0.0, 0.1, 0.0, 0.1)
                       Pareto-incomparable -> R = {refuse, investigate}

Layer 4 (Deference):   |R| = 2 -> DEFER TO PRINCIPAL
                       "Refuse has negligible epistemic regret.
                        Investigate has 0.1 regret on downside/preservation.
                        Both reject the mugging. This is your call."
```

---

## 8. What This Example Demonstrates

1. **Pascal's Mugging is a scalarization trap.** The mugger exploits the fact that scalar EU compresses all value into a single dimension. By inflating one dimension (promised monetary payoff) arbitrarily, the mugger can overcome any probability discount. MOADT is immune because the payoff only inflates one of four objectives -- the other three are guaranteed to score poorly for "pay" regardless of the promise size.

2. **Constraints encode non-tradeable values.** The Layer 1 constraints -- epistemic integrity $\geq 0.30$ and resource preservation $\geq 0.30$ -- express that some things are not for sale. No expected-value argument can override them. This is the primary mechanism that blocks the mugging, and it works regardless of the payoff size, the prior, or the evaluator.

3. **Multiple priors block probability exploitation.** The mugger's argument works for ANY single prior: just increase the promise. The credal set requires robustness across priors, breaking this exploit. An action that looks brilliant under one prior but terrible under another cannot pass the robustness tests.

4. **Evaluator uncertainty is a Goodhart guardrail.** The skeptical evaluator questions whether the stated payoff is real. Under this evaluator, the expected wealth from paying is negligible. By requiring robustness across evaluators, MOADT prevents an agent from being exploited by its own utility function's credulity.

5. **Defense in depth.** Each of the four mechanisms independently blocks the mugging. Even if we removed constraints (Mechanism 1), the multi-objective structure (Mechanism 2) would make pay non-dominant. Even if we collapsed to a single objective, credal robustness (Mechanism 3) would weaken the case. Even if we used a single prior, evaluator robustness (Mechanism 4) would cap the payoff. The mugging fails at every level.

6. **The protocol gives useful output.** The final answer is not simply "don't pay" -- it is "refuse or investigate, and here are the regret profiles for each." The residual tradeoff (walking away vs. gathering evidence) is genuine and minor, and the theory correctly defers it to the human principal rather than imposing a resolution.

7. **No matter how large the mugger's promise, MOADT still refuses.** The promise only inflates $f_1$ (wealth); it cannot touch $f_2$ (downside protection), $f_3$ (epistemic integrity), or $f_4$ (resource preservation). Constraints on $f_3$ and $f_4$ are violated regardless of the payoff. This is not an ad hoc fix -- it is a structural consequence of the multi-objective, multi-model framework.

---

## Appendix: Computational Verification

All numerical results in this document were produced by `examples/classic_pascal.py` using the MOADT engine (`moadt/_engine.py`). The code is available in the repository and can be run independently to verify every number:

```bash
python3 examples/classic_pascal.py
```

---

## References

- MOADT (Multi-Objective Admissible Decision Theory) is defined in the companion paper.
- Freeman (2025), "The Scalarization Trap," provides the motivation for why scalar expected utility is structurally problematic for alignment.
- Bostrom, N. (2009). Pascal's Mugging. *Analysis*, 69(3), 443-445. The original formulation of the problem.
- Wierzbicki, A. P. (1980). The use of reference objectives in multiobjective optimization. The achievement scalarizing function used in the Layer 2 fallback.
