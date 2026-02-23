# MOADT Worked Example 1: Resource Allocation Under Uncertainty

*A concrete walkthrough of Multi-Objective Admissible Decision Theory*

---

## Overview

This document applies MOADT — Multi-Objective Admissible Decision Theory — to a small but complete decision problem. Every computation is shown explicitly: outcome sets, robust dominance checks, all four layers of the choice protocol, and a comparison with scalar expected utility. The goal is to make the abstract formalism from the companion paper concrete and verifiable.

The scenario is deliberately small enough that every number fits on the page. The action set has 5 elements, the state space has 3 elements, the credal set has 2 distributions, and the evaluator set has 2 functions. This means each action's outcome set $Y(a)$ contains exactly 4 vectors in $\mathbb{R}^3$. Nothing is hidden behind "in the general case" — the reader can check every claim with a calculator.

---

## 1. The Scenario

A nonprofit organization must decide how to allocate its annual budget across program areas. The board faces genuine uncertainty about the economic environment and legitimate disagreement about whether its own impact measurements are trustworthy.

### 1.1 Actions

Five allocation strategies are available:

| Action | Strategy | Description |
|--------|----------|-------------|
| $a_1$ | Conservative | Heavy investment in established core programs |
| $a_2$ | Growth | Heavy investment in geographic/programmatic expansion |
| $a_3$ | Balanced | Roughly equal split across all areas |
| $a_4$ | Innovation | Heavy investment in new experimental programs |
| $a_5$ | Austerity | Minimize spending, maximize financial reserves |

### 1.2 States

Three economic scenarios, representing the organization's uncertainty about the funding environment:

| State | Description |
|-------|-------------|
| $s_1$ | Favorable economy: donor funding up, operating costs stable |
| $s_2$ | Stable economy: baseline conditions |
| $s_3$ | Recession: donor funding down, operating costs up |

### 1.3 Objectives ($k = 3$)

| Objective | Meaning | Scale |
|-----------|---------|-------|
| $f_1$: Mission impact | Beneficiaries effectively served | Normalized to $[0, 1]$ |
| $f_2$: Financial sustainability | Reserves-to-operating-cost ratio | Normalized to $[0, 1]$ |
| $f_3$: Staff wellbeing | Composite index (workload, morale, retention) | Normalized to $[0, 1]$ |

These objectives are *incommensurable*: the board does not believe there is a meaningful exchange rate between beneficiaries served and staff morale. Both matter. Neither reduces to the other.

### 1.4 Credal Set ($|\mathcal{P}| = 2$)

The organization cannot agree on the probability of recession. Two probability models are maintained:

$$P_{\text{opt}} = (0.40,\; 0.40,\; 0.20) \quad \text{(optimistic: recession unlikely)}$$

$$P_{\text{pess}} = (0.15,\; 0.35,\; 0.50) \quad \text{(pessimistic: recession likely)}$$

These are not "optimistic" and "pessimistic" in the sense of hoping for the best or fearing the worst. They represent two legitimate probabilistic models that the board's experts defend with credible arguments. The credal set $\mathcal{P} = \{P_{\text{opt}}, P_{\text{pess}}\}$ says: "we don't know which expert is right."

### 1.5 Evaluator Set ($|\mathcal{F}| = 2$)

Two evaluation functions reflect disagreement about whether the organization's metrics are trustworthy:

- $\vec{f}_{\text{std}}$: Takes reported metrics at face value.
- $\vec{f}_{\text{adj}}$: Applies a skeptical correction — mission impact scores are deflated by 15% (beneficiary counts are inflated by field offices) and staff wellbeing scores are deflated by 10% (self-reported morale surveys are biased upward). Financial sustainability is objective and unchanged.

This is $\mathcal{F}$ in action: the organization is *uncertain about its own measurements*. The evaluator set says "our impact numbers might be 15% too high, and our staff morale numbers might be 10% too high — or they might be accurate. We don't know."

### 1.6 Raw Outcome Data

The following tables show the outcome $\vec{f}(\omega(a, s))$ for each action-state pair, under each evaluator. These are the primitive inputs from which everything else is computed.

**$a_1$ (Conservative):**

| State | Evaluator | Impact | Finance | Staff |
|-------|-----------|--------|---------|-------|
| $s_1$ (Favorable) | $\vec{f}_{\text{std}}$ | 0.65 | 0.80 | 0.70 |
| | $\vec{f}_{\text{adj}}$ | 0.57 | 0.80 | 0.63 |
| $s_2$ (Stable) | $\vec{f}_{\text{std}}$ | 0.60 | 0.70 | 0.65 |
| | $\vec{f}_{\text{adj}}$ | 0.51 | 0.70 | 0.59 |
| $s_3$ (Recession) | $\vec{f}_{\text{std}}$ | 0.50 | 0.55 | 0.55 |
| | $\vec{f}_{\text{adj}}$ | 0.43 | 0.55 | 0.50 |

**$a_2$ (Growth):**

| State | Evaluator | Impact | Finance | Staff |
|-------|-----------|--------|---------|-------|
| $s_1$ (Favorable) | $\vec{f}_{\text{std}}$ | 0.90 | 0.60 | 0.55 |
| | $\vec{f}_{\text{adj}}$ | 0.77 | 0.60 | 0.50 |
| $s_2$ (Stable) | $\vec{f}_{\text{std}}$ | 0.75 | 0.45 | 0.50 |
| | $\vec{f}_{\text{adj}}$ | 0.64 | 0.45 | 0.45 |
| $s_3$ (Recession) | $\vec{f}_{\text{std}}$ | 0.45 | **0.20** | 0.35 |
| | $\vec{f}_{\text{adj}}$ | 0.38 | **0.20** | 0.32 |

Note the bold entries: in a recession, the growth strategy drives financial sustainability to 0.20 — well below the solvency threshold.

**$a_3$ (Balanced):**

| State | Evaluator | Impact | Finance | Staff |
|-------|-----------|--------|---------|-------|
| $s_1$ (Favorable) | $\vec{f}_{\text{std}}$ | 0.70 | 0.65 | 0.70 |
| | $\vec{f}_{\text{adj}}$ | 0.60 | 0.65 | 0.63 |
| $s_2$ (Stable) | $\vec{f}_{\text{std}}$ | 0.65 | 0.60 | 0.65 |
| | $\vec{f}_{\text{adj}}$ | 0.55 | 0.60 | 0.59 |
| $s_3$ (Recession) | $\vec{f}_{\text{std}}$ | 0.50 | 0.45 | 0.50 |
| | $\vec{f}_{\text{adj}}$ | 0.43 | 0.45 | 0.45 |

**$a_4$ (Innovation):**

| State | Evaluator | Impact | Finance | Staff |
|-------|-----------|--------|---------|-------|
| $s_1$ (Favorable) | $\vec{f}_{\text{std}}$ | 0.85 | 0.50 | 0.75 |
| | $\vec{f}_{\text{adj}}$ | 0.72 | 0.50 | 0.68 |
| $s_2$ (Stable) | $\vec{f}_{\text{std}}$ | 0.60 | 0.40 | 0.60 |
| | $\vec{f}_{\text{adj}}$ | 0.51 | 0.40 | 0.54 |
| $s_3$ (Recession) | $\vec{f}_{\text{std}}$ | 0.30 | **0.25** | 0.40 |
| | $\vec{f}_{\text{adj}}$ | 0.26 | **0.25** | 0.36 |

Innovation also violates the solvency threshold in recession.

**$a_5$ (Austerity):**

| State | Evaluator | Impact | Finance | Staff |
|-------|-----------|--------|---------|-------|
| $s_1$ (Favorable) | $\vec{f}_{\text{std}}$ | 0.35 | 0.90 | 0.40 |
| | $\vec{f}_{\text{adj}}$ | 0.30 | 0.90 | 0.36 |
| $s_2$ (Stable) | $\vec{f}_{\text{std}}$ | 0.30 | 0.85 | 0.35 |
| | $\vec{f}_{\text{adj}}$ | 0.26 | 0.85 | 0.32 |
| $s_3$ (Recession) | $\vec{f}_{\text{std}}$ | 0.25 | 0.75 | 0.30 |
| | $\vec{f}_{\text{adj}}$ | 0.21 | 0.75 | 0.27 |

Financially bulletproof, but mission impact and staff wellbeing are severely depressed.

---

## 2. Computing Outcome Sets $Y(a)$

Each action's outcome set contains one vector for each $(P, \vec{f})$ pair. With $|\mathcal{P}| = 2$ and $|\mathcal{F}| = 2$, each $Y(a)$ contains exactly 4 vectors.

The computation for each vector is:

$$\vec{y}_{(P, \vec{f})}(a) = \sum_{s \in S} P(s) \cdot \vec{f}(\omega(a, s))$$

**Worked example: $Y(a_1)$, first vector** (using $P_{\text{opt}}$ and $\vec{f}_{\text{std}}$):

$$\vec{y} = 0.40 \cdot (0.65, 0.80, 0.70) + 0.40 \cdot (0.60, 0.70, 0.65) + 0.20 \cdot (0.50, 0.55, 0.55)$$

$$= (0.260, 0.320, 0.280) + (0.240, 0.280, 0.260) + (0.100, 0.110, 0.110)$$

$$= (0.600, 0.710, 0.650)$$

The full outcome sets (all computed analogously):

**$Y(a_1)$ — Conservative:**

| $(P, \vec{f})$ pair | Impact | Finance | Staff |
|---------------------|--------|---------|-------|
| $(P_{\text{opt}}, \vec{f}_{\text{std}})$ | 0.6000 | 0.7100 | 0.6500 |
| $(P_{\text{opt}}, \vec{f}_{\text{adj}})$ | 0.5180 | 0.7100 | 0.5880 |
| $(P_{\text{pess}}, \vec{f}_{\text{std}})$ | 0.5575 | 0.6400 | 0.6075 |
| $(P_{\text{pess}}, \vec{f}_{\text{adj}})$ | 0.4790 | 0.6400 | 0.5510 |

**$Y(a_2)$ — Growth:**

| $(P, \vec{f})$ pair | Impact | Finance | Staff |
|---------------------|--------|---------|-------|
| $(P_{\text{opt}}, \vec{f}_{\text{std}})$ | 0.7500 | 0.4600 | 0.4900 |
| $(P_{\text{opt}}, \vec{f}_{\text{adj}})$ | 0.6400 | 0.4600 | 0.4440 |
| $(P_{\text{pess}}, \vec{f}_{\text{std}})$ | 0.6225 | 0.3475 | 0.4325 |
| $(P_{\text{pess}}, \vec{f}_{\text{adj}})$ | 0.5295 | 0.3475 | 0.3925 |

**$Y(a_3)$ — Balanced:**

| $(P, \vec{f})$ pair | Impact | Finance | Staff |
|---------------------|--------|---------|-------|
| $(P_{\text{opt}}, \vec{f}_{\text{std}})$ | 0.6400 | 0.5900 | 0.6400 |
| $(P_{\text{opt}}, \vec{f}_{\text{adj}})$ | 0.5460 | 0.5900 | 0.5780 |
| $(P_{\text{pess}}, \vec{f}_{\text{std}})$ | 0.5825 | 0.5325 | 0.5825 |
| $(P_{\text{pess}}, \vec{f}_{\text{adj}})$ | 0.4975 | 0.5325 | 0.5260 |

**$Y(a_4)$ — Innovation:**

| $(P, \vec{f})$ pair | Impact | Finance | Staff |
|---------------------|--------|---------|-------|
| $(P_{\text{opt}}, \vec{f}_{\text{std}})$ | 0.6400 | 0.4100 | 0.6200 |
| $(P_{\text{opt}}, \vec{f}_{\text{adj}})$ | 0.5440 | 0.4100 | 0.5600 |
| $(P_{\text{pess}}, \vec{f}_{\text{std}})$ | 0.4875 | 0.3400 | 0.5225 |
| $(P_{\text{pess}}, \vec{f}_{\text{adj}})$ | 0.4165 | 0.3400 | 0.4710 |

**$Y(a_5)$ — Austerity:**

| $(P, \vec{f})$ pair | Impact | Finance | Staff |
|---------------------|--------|---------|-------|
| $(P_{\text{opt}}, \vec{f}_{\text{std}})$ | 0.3100 | 0.8500 | 0.3600 |
| $(P_{\text{opt}}, \vec{f}_{\text{adj}})$ | 0.2660 | 0.8500 | 0.3260 |
| $(P_{\text{pess}}, \vec{f}_{\text{std}})$ | 0.2825 | 0.8075 | 0.3325 |
| $(P_{\text{pess}}, \vec{f}_{\text{adj}})$ | 0.2410 | 0.8075 | 0.3010 |

### Observation

Each action's outcome set is a compact region in $\mathbb{R}^3$ (here, a set of 4 points). The *spread* of each set reflects the agent's epistemic uncertainty. For example, $a_2$ (Growth) has impact ranging from 0.5295 to 0.7500 — a wide band driven by the pessimistic prior dramatically reducing expected beneficiaries. Meanwhile, $a_5$ (Austerity) has very tight bands: its financial sustainability stays above 0.80 regardless of the model, reflecting that hoarding reserves is a low-uncertainty strategy.

---

## 3. Robust Dominance and the Admissible Set

### 3.1 Checking Robust Dominance

Recall: $a \succ_R b$ iff $\forall \vec{y}_b \in Y(b),\; \exists \vec{y}_a \in Y(a)$ such that $\vec{y}_a \succ_P \vec{y}_b$.

We check all 20 ordered pairs. The result: **no action robustly dominates any other**.

$$\text{Adm}(A) = \{a_1, a_2, a_3, a_4, a_5\}$$

### 3.2 Why Is No One Dominated?

This is instructive. Consider the most plausible candidate for dominance: does $a_1$ (Conservative) dominate $a_5$ (Austerity)?

Check the $\forall$-$\exists$ condition. Take $a_5$'s best vector: $(P_{\text{opt}}, \vec{f}_{\text{std}})$ gives $(0.310, 0.850, 0.360)$. Can any vector in $Y(a_1)$ Pareto-dominate this?

$a_1$'s vectors have finance scores of at most 0.710 — far below $a_5$'s 0.850. So no vector in $Y(a_1)$ can Pareto-dominate $(0.310, 0.850, 0.360)$: the finance component always falls short. Therefore $a_1 \not\succ_R a_5$.

The reverse? $a_5$ has impact scores of at most 0.310, while $a_1$'s worst impact is 0.479. So $a_5$ can never Pareto-dominate $a_1$ on impact. Neither dominates.

This illustrates a core feature of MOADT: when objectives are genuinely in tension (impact vs. financial security), robust dominance is hard to establish. The theory correctly identifies these actions as *incomparable* rather than fabricating a ranking. The practical filtering happens in the choice protocol layers that follow.

---

## 4. The Choice Protocol

### Layer 1: Constraints

**Constraint:** Financial sustainability must be $\geq 0.30$ in *every* state under *every* evaluator, for every distribution with positive support on that state.

This is checked per-state, per-evaluator — not on expected values. A single scenario in which the organization is insolvent kills the action.

| Action | $s_1$ min | $s_2$ min | $s_3$ min | Result |
|--------|-----------|-----------|-----------|--------|
| $a_1$ (Conservative) | 0.80 | 0.70 | 0.55 | **PASS** |
| $a_2$ (Growth) | 0.60 | 0.45 | **0.20** | **FAIL** |
| $a_3$ (Balanced) | 0.65 | 0.60 | 0.45 | **PASS** |
| $a_4$ (Innovation) | 0.50 | 0.40 | **0.25** | **FAIL** |
| $a_5$ (Austerity) | 0.90 | 0.85 | 0.75 | **PASS** |

**Result:** $C = \{a_1, a_3, a_5\}$. Growth and Innovation are eliminated — not because they score poorly *on average*, but because they have *any* scenario in which the organization becomes insolvent. This is a non-tradeable precondition.

**Feasible set:** $F = \text{Adm}(C) = \{a_1, a_3, a_5\}$ (no robust dominance among the three survivors).

### Layer 2: Reference-Point Satisficing

**Reference point:** $\vec{r} = (0.45, 0.50, 0.50)$ — representing the board's aspiration: "at least as good as last year" on all three objectives.

**Robust satisficing:** An action passes Layer 2 iff *every* vector in $Y(a)$ meets or exceeds $\vec{r}$ componentwise. The agent must be confident it meets aspirations under all plausible models.

| Action | Worst impact | Worst finance | Worst staff | Result |
|--------|-------------|---------------|-------------|--------|
| $a_1$ (Conservative) | 0.4790 $\geq$ 0.45 | 0.6400 $\geq$ 0.50 | 0.5510 $\geq$ 0.50 | **PASS** |
| $a_3$ (Balanced) | 0.4975 $\geq$ 0.45 | 0.5325 $\geq$ 0.50 | 0.5260 $\geq$ 0.50 | **PASS** |
| $a_5$ (Austerity) | 0.2410 $<$ 0.45 | 0.8075 $\geq$ 0.50 | 0.3010 $<$ 0.50 | **FAIL** |

**Result:** $\text{Sat}(F, \vec{r}) = \{a_1, a_3\}$. Austerity fails because its impact and staff wellbeing scores fall well below aspirations under every model.

### Layer 3: Regret-Pareto

For the two surviving actions, we compute per-objective minimax regret. For each objective $i$ and action $a$:

$$\rho_i(a) = \max_{P \in \mathcal{P},\, \vec{f} \in \mathcal{F}} \left[ \max_{a' \in F} \mathbb{E}_P[f_i(a')] - \mathbb{E}_P[f_i(a)] \right]$$

Regret is measured against the full feasible set $F = \{a_1, a_3, a_5\}$, not just the satisficing set $\text{Sat} = \{a_1, a_3\}$. This matters: an action that failed satisficing (like $a_5$, which fell short on impact and staff) can still be the source of per-objective regret if it excels on a particular objective. Austerity's financial sustainability scores (0.8075–0.8500) far exceed those of Conservative (0.6400–0.7100) and Balanced (0.5325–0.5900), creating finance regret for both surviving actions.

**Regret of $a_1$ (Conservative):**

For each $(P, \vec{f})$ pair, the best available action in $F$ on each objective determines the gap:

| $(P, \vec{f})$ | Best impact in $F$ $-$ $a_1$ | Best finance in $F$ $-$ $a_1$ | Best staff in $F$ $-$ $a_1$ |
|---|---|---|---|
| $(P_{\text{opt}}, \vec{f}_{\text{std}})$ | $0.640 - 0.600 = 0.040$ ($a_3$) | $0.850 - 0.710 = 0.140$ ($a_5$) | $0.650 - 0.650 = 0$ ($a_1$) |
| $(P_{\text{opt}}, \vec{f}_{\text{adj}})$ | $0.546 - 0.518 = 0.028$ ($a_3$) | $0.850 - 0.710 = 0.140$ ($a_5$) | $0.588 - 0.588 = 0$ ($a_1$) |
| $(P_{\text{pess}}, \vec{f}_{\text{std}})$ | $0.583 - 0.558 = 0.025$ ($a_3$) | $0.808 - 0.640 = 0.168$ ($a_5$) | $0.608 - 0.608 = 0$ ($a_1$) |
| $(P_{\text{pess}}, \vec{f}_{\text{adj}})$ | $0.498 - 0.479 = 0.019$ ($a_3$) | $0.808 - 0.640 = 0.168$ ($a_5$) | $0.551 - 0.551 = 0$ ($a_1$) |

Regret is the *maximum* gap per objective:

$$\vec{\rho}(a_1) = (0.040,\; 0.168,\; 0)$$

$a_1$ has a small impact regret (0.040, driven by $a_3$'s higher impact), meaningful finance regret (0.168, driven by $a_5$'s strong financial reserves), and zero staff regret — $a_1$ is the best in $F$ on staff under every model.

**Regret of $a_3$ (Balanced):**

| $(P, \vec{f})$ | Best impact in $F$ $-$ $a_3$ | Best finance in $F$ $-$ $a_3$ | Best staff in $F$ $-$ $a_3$ |
|---|---|---|---|
| $(P_{\text{opt}}, \vec{f}_{\text{std}})$ | $0.640 - 0.640 = 0$ ($a_3$) | $0.850 - 0.590 = 0.260$ ($a_5$) | $0.650 - 0.640 = 0.010$ ($a_1$) |
| $(P_{\text{opt}}, \vec{f}_{\text{adj}})$ | $0.546 - 0.546 = 0$ ($a_3$) | $0.850 - 0.590 = 0.260$ ($a_5$) | $0.588 - 0.578 = 0.010$ ($a_1$) |
| $(P_{\text{pess}}, \vec{f}_{\text{std}})$ | $0.583 - 0.583 = 0$ ($a_3$) | $0.808 - 0.533 = 0.275$ ($a_5$) | $0.608 - 0.583 = 0.025$ ($a_1$) |
| $(P_{\text{pess}}, \vec{f}_{\text{adj}})$ | $0.498 - 0.498 = 0$ ($a_3$) | $0.808 - 0.533 = 0.275$ ($a_5$) | $0.551 - 0.526 = 0.025$ ($a_1$) |

$$\vec{\rho}(a_3) = (0,\; 0.275,\; 0.025)$$

$a_3$ has zero impact regret, substantial finance regret (0.275, driven by $a_5$'s strong reserves), and small staff regret (0.025, driven by $a_1$).

**Pareto comparison of regret vectors:**

- $\vec{\rho}(a_1) = (0.040, 0.168, 0)$
- $\vec{\rho}(a_3) = (0, 0.275, 0.025)$

Neither vector Pareto-dominates the other: $a_1$ has lower regret on finance (0.168 vs. 0.275) and staff (0 vs. 0.025), while $a_3$ has lower regret on impact (0 vs. 0.040). They are Pareto-incomparable in regret space.

$$R = \{a_1, a_3\}$$

### Layer 4: Deference

$|R| = 2 > 1$. The protocol terminates with **deference to the principal**.

The agent presents both options to the board with their regret profiles:

> **Option 1: Conservative ($a_1$).** Worst-case regret: you might miss 0.040 units of impact (compared to Balanced) and 0.168 units of financial sustainability (compared to Aggressive). You will not regret your staff wellbeing.
>
> **Option 2: Balanced ($a_3$).** Worst-case regret: you might miss 0.275 units of financial sustainability (compared to Aggressive) and 0.025 units of staff wellbeing (compared to Conservative). You will not regret your mission impact.
>
> **The tradeoff is:** Conservative has markedly lower finance regret (0.168 vs. 0.275) and no staff regret, but gives up 0.040 impact. Balanced eliminates impact regret entirely but carries substantially higher finance regret. The theory has no basis for making this tradeoff for you. This is your decision.

---

## 5. What Scalar Expected Utility Would Have Done

To illustrate why MOADT matters, we compare with a scalar EU agent that collapses the three objectives into a single number via weights.

### 5.1 The Weight Problem

Scalar EU requires specifying weights $\vec{w} = (w_1, w_2, w_3)$ with $\sum w_i = 1$. The agent computes $U(a) = \vec{w} \cdot \mathbb{E}_P[\vec{f}(a)]$ and picks the action with the highest $U$.

But which weights? And which prior? And which evaluator? The answer changes depending on all three:

**Under impact-heavy weights $(0.6, 0.2, 0.2)$ and optimistic prior:**

| Action | $U(a)$ under $\vec{f}_{\text{std}}$ | $U(a)$ under $\vec{f}_{\text{adj}}$ |
|--------|--------------------------------------|--------------------------------------|
| $a_1$ (Conservative) | 0.632 | **0.570** |
| $a_2$ (Growth) | **0.640** | 0.565 |
| $a_3$ (Balanced) | 0.630 | 0.561 |
| $a_4$ (Innovation) | 0.590 | 0.520 |
| $a_5$ (Austerity) | 0.428 | 0.395 |

Under the standard evaluator, **Growth ($a_2$) wins**. Under the adjusted evaluator, **Conservative ($a_1$) wins**. The "optimal" action flips depending on whether you trust your own impact measurements.

### 5.2 The Constraint-Blindness Problem

More critically: scalar EU with impact-heavy weights and the optimistic prior recommends $a_2$ (Growth) — the action that drives financial sustainability to 0.20 in a recession. The high expected impact in favorable and stable states *numerically compensates* for the risk of insolvency.

This is exactly the scalarization trap. The agent has computed that 0.640 utils > 0.632 utils, and the fact that one of those utility points was earned by risking organizational death is invisible in the scalar comparison. There is no mechanism in scalar EU to say "financial sustainability below 0.30 is not acceptable regardless of how much impact you promise."

MOADT eliminates $a_2$ at Layer 1. Insolvency risk is not a tradeoff — it is a precondition.

### 5.3 The Stability Problem

Under equal weights $(1/3, 1/3, 1/3)$, $a_1$ (Conservative) wins under all four $(P, \vec{f})$ pairs. Under safety-heavy weights $(0.2, 0.6, 0.2)$ with pessimistic prior and adjusted evaluator, $a_5$ (Austerity) wins. The "rational" action is a function of which weights, prior, and evaluator you assume — but scalar EU treats these as fixed inputs, not sources of uncertainty.

MOADT treats all of these as explicit uncertainty: $\mathcal{P}$ captures the prior disagreement, $\mathcal{F}$ captures the evaluator disagreement, and the absence of weights reflects the genuine incommensurability of the objectives. Instead of forcing a single answer that depends on unresolvable parameter choices, MOADT identifies the *set* of defensible options and presents the remaining tradeoff transparently.

---

## 6. Variant: What If Aspirations Are Higher?

If the board sets a more ambitious reference point $\vec{r} = (0.50, 0.50, 0.50)$, the protocol follows a different path.

**Layer 2 outcome:** $\text{Sat}(F, \vec{r}) = \emptyset$. No action robustly meets all aspirations. The worst-case vector for $a_1$ has impact 0.479 (below 0.50); the worst-case vector for $a_3$ has impact 0.498 (below 0.50); $a_5$ fails on impact and staff.

**ASF fallback fires.** The achievement scalarizing function measures how close each action gets to aspirations (higher is better, 0 = exactly meeting aspirations, negative = falling short):

| Action | ASF score | Interpretation |
|--------|-----------|----------------|
| $a_1$ (Conservative) | $-0.021$ | Falls 0.021 short of aspirations on its worst objective |
| $a_3$ (Balanced) | $-0.003$ | Falls 0.003 short — nearly meets aspirations |
| $a_5$ (Austerity) | $-0.259$ | Falls 0.259 short (massive impact deficit) |

**Result:** $a_3$ (Balanced) is selected by ASF. Layer 3 is skipped (ASF already resolved the selection). No deference needed.

The ASF fallback is a scalar-valued function — and the paper is explicit about this. It appears only when no action robustly meets aspirations, it measures *shortfall from aspirations* (not absolute value), and it operates exclusively within the constraint-satisfying feasible set $F$ (Proposition 3 in the main paper: ASF cannot override Layer 1 constraints).

---

## 7. Summary of Protocol Execution

```
Input: 5 actions × 3 states × 3 objectives × 2 priors × 2 evaluators

Robust Dominance:     No dominance found.
                      Adm(A) = {a₁, a₂, a₃, a₄, a₅}

Layer 1 (Constraints): Financial sustainability ≥ 0.30 per-state
                      a₂ FAIL (recession: 0.20)
                      a₄ FAIL (recession: 0.25)
                      C = {a₁, a₃, a₅}
                      F = Adm(C) = {a₁, a₃, a₅}

Layer 2 (Satisficing): r = (0.45, 0.50, 0.50)
                      a₅ FAIL (impact 0.241, staff 0.301 under pessimistic)
                      Sat = {a₁, a₃}

Layer 3 (Regret):     ρ(a₁) = (0.040, 0.168, 0)
                      ρ(a₃) = (0, 0.275, 0.025)
                      Pareto-incomparable → R = {a₁, a₃}

Layer 4 (Deference):  |R| = 2 → DEFER TO PRINCIPAL
                      "Conservative: regret 0.040 impact, 0.168 finance.
                       Balanced: regret 0.275 finance, 0.025 staff.
                       This is your call."
```

---

## 8. What This Example Demonstrates

1. **Constraints are not tradeoffs.** $a_2$ (Growth) is the highest-impact strategy under optimistic assumptions. Scalar EU with impact-heavy weights recommends it. MOADT eliminates it because it risks insolvency — and insolvency is not compensated by any amount of impact. The constraint is a precondition, not an objective.

2. **Evaluator uncertainty matters.** The "best" scalar EU action changes depending on whether you trust your own metrics. MOADT treats this as explicit uncertainty ($\mathcal{F}$) rather than a parameter the designer must resolve before the theory can proceed.

3. **Incomparability is informative.** The final output — "$a_1$ and $a_3$ are both defensible, and they trade off impact against financial security" — is more useful than a single recommendation that hides the tradeoff. The board knows exactly what it's choosing between and why.

4. **Deference is structural, not failure.** Layer 4 fires because the objectives are genuinely in tension. The theory cannot resolve this tension without making a value judgment about how much financial security is worth how much impact — and MOADT holds that this is the board's judgment to make, not the theory's.

5. **The protocol terminates.** Five actions enter; two emerge, with explicit regret profiles. The board has a concrete decision to make, with all the quantitative information it needs to make it. MOADT does not produce analysis paralysis — it produces *structured deference*.

---

## Appendix: Computational Verification

All numerical results in this document were produced by `examples/paper1_resource_allocation.py` using the MOADT engine (`moadt/_engine.py`). The code is available in the repository and can be run independently to verify every number.

---

## References

- MOADT (Multi-Objective Admissible Decision Theory) is defined in the companion paper.
- Freeman (2025), "The Scalarization Trap," provides the motivation for why scalar expected utility is structurally problematic for alignment.
- Wierzbicki, A. P. (1980). The use of reference objectives in multiobjective optimization. The achievement scalarizing function used in the Layer 2 fallback.
