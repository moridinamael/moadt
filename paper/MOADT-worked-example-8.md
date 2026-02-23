# MOADT Worked Example 8: The Allais Paradox

*A concrete walkthrough of Multi-Objective Admissible Decision Theory applied to the Independence Axiom violation*

---

## Overview

This document applies MOADT --- Multi-Objective Admissible Decision Theory --- to the Allais Paradox, the most famous demonstration that real human preferences systematically violate Expected Utility theory. Every computation is shown explicitly: the algebraic proof of the EU contradiction, outcome sets under multiple evaluators and priors, all four layers of the choice protocol, and a scalar EU comparison showing the knife-edge impossibility of reproducing Allais preferences with weighted objectives.

The Allais Paradox is not a contrived edge case. It is a clean, minimal demonstration that scalar utility theory cannot capture a pattern of preferences that the overwhelming majority of humans exhibit. The standard response in economics and decision theory is to classify this preference pattern as *irrational* --- a bias to be corrected. MOADT offers a different interpretation: the preferences are perfectly rational once you stop forcing them through a one-dimensional bottleneck.

The scenario uses 4 gambles, 100 equiprobable states (encoding the Allais probabilities exactly), 3 objectives, 2 evaluators, and 2 priors. All numerical results were produced by `examples/classic_allais.py` using the MOADT engine (`moadt/_engine.py`) and can be independently verified.

---

## 1. The Scenario

### 1.1 The Allais Paradox (Allais, 1953)

A decision-maker faces two independent choice problems.

**Problem 1:**

| Gamble | Description |
|--------|-------------|
| A | \$1,000,000 with certainty |
| B | 89% chance of \$1M, 10% chance of \$5M, 1% chance of \$0 |

**Problem 2:**

| Gamble | Description |
|--------|-------------|
| C | 11% chance of \$1M, 89% chance of \$0 |
| D | 10% chance of \$5M, 90% chance of \$0 |

The typical human preference pattern is $A \succ B$ and $D \succ C$. People prefer the certainty of \$1M over the risky gamble in Problem 1, but prefer the higher expected value gamble in Problem 2. This is not a niche laboratory finding --- it is robust across cultures, stakes, and decades of replication.

### 1.2 The Independence Axiom Violation

Under Expected Utility with any utility function $u(\cdot)$, normalizing $u(\$0) = 0$:

**$A \succ B$ requires:**

$$u(\$1M) > 0.89 \cdot u(\$1M) + 0.10 \cdot u(\$5M) + 0.01 \cdot u(\$0)$$

$$0.11 \cdot u(\$1M) > 0.10 \cdot u(\$5M)$$

$$\frac{u(\$1M)}{u(\$5M)} > \frac{10}{11} \approx 0.9091$$

**$D \succ C$ requires:**

$$0.10 \cdot u(\$5M) > 0.11 \cdot u(\$1M)$$

$$\frac{u(\$1M)}{u(\$5M)} < \frac{10}{11} \approx 0.9091$$

These two conditions are a direct algebraic contradiction. No utility function --- linear, concave, convex, or otherwise --- can simultaneously produce $A \succ B$ and $D \succ C$. This is the Allais Paradox.

### 1.3 MOADT Formulation

Rather than forcing the problem through a scalar utility function, MOADT models it with three genuinely incommensurable objectives:

| Objective | Meaning | How computed |
|-----------|---------|--------------|
| $f_1$: Expected value | Monetary payoff (normalized: \$0 = 0, \$5M = 1) | $\mathbb{E}_P[v(\text{payoff})]$ |
| $f_2$: Downside protection | Probability of adequate outcome ($\geq$ \$500K) | $\mathbb{E}_P[\mathbf{1}_{\text{payoff} \geq 500K}]$ |
| $f_3$: Reliability | Probability of nonzero payoff | $\mathbb{E}_P[\mathbf{1}_{\text{payoff} > 0}]$ |

These objectives are genuinely distinct. Expected value measures average return. Downside protection measures the probability of avoiding a bad outcome. Reliability measures the probability of receiving *anything*. A person who values the certainty of \$1M is not exhibiting a "bias" --- they are weighting objectives 2 and 3 alongside objective 1.

**Evaluators** ($|\mathcal{F}| = 2$):

| Evaluator | Valuation function | Interpretation |
|-----------|-------------------|----------------|
| $v_{\text{neutral}}$ | $v(x) = x / \$5M$ | Risk-neutral: linear in dollars |
| $v_{\text{cautious}}$ | $v(x) = \sqrt{x / \$5M}$ | Risk-averse: diminishing marginal returns |

**Credal set** ($|\mathcal{P}| = 2$): We use 100 equiprobable states to encode the Allais probabilities exactly. The exact prior assigns $P(s_i) = 0.01$ uniformly. A perturbed prior shifts 0.002 probability mass per state from the 5 highest-numbered states to the 5 lowest-numbered states, creating a mildly pessimistic variant. Since worst outcomes (e.g., \$0) are assigned to the highest-numbered states, this perturbation slightly increases the probability of bad outcomes.

**State encoding**: Each gamble's probability distribution is mapped onto the 100 states. For example:
- Gamble A: all 100 states yield \$1M
- Gamble B: states 1--89 yield \$1M, states 90--99 yield \$5M, state 100 yields \$0
- Gamble C: states 1--11 yield \$1M, states 12--100 yield \$0
- Gamble D: states 1--10 yield \$5M, states 11--100 yield \$0

(Worst outcomes are assigned to the highest-numbered states, so the perturbed prior is genuinely pessimistic.)

---

## 2. Why Expected Utility Fails

### 2.1 The Algebraic Contradiction

The proof in Section 1.2 is airtight: no utility function can produce both $A \succ B$ and $D \succ C$. To make this concrete, here are five specific utility functions spanning the full range from risk-neutral to extremely concave:

| Utility function | $EU(A)$ | $EU(B)$ | $A \succ B$? | $EU(C)$ | $EU(D)$ | $D \succ C$? | Both? |
|-----------------|---------|---------|:------------:|---------|---------|:------------:|:-----:|
| Linear: $u(x) = x/5M$ | 0.200000 | 0.278000 | No | 0.022000 | 0.100000 | Yes | No |
| Sqrt: $u(x) = \sqrt{x/5M}$ | 0.447214 | 0.498020 | No | 0.049193 | 0.100000 | Yes | No |
| Log: $u(x) = \ln(1+x)/\ln(1+5M)$ | 0.895660 | 0.897138 | No | 0.098523 | 0.100000 | Yes | No |
| Power: $u(x) = (x/5M)^{0.3}$ | 0.617034 | 0.649160 | No | 0.067874 | 0.100000 | Yes | No |
| Extreme: $u(x) = (x/5M)^{0.05}$ | 0.922681 | 0.921186 | Yes | 0.101495 | 0.100000 | No | No |

### 2.2 The Pattern

The table reveals the structural impossibility. As the utility function becomes more concave (from Linear to Extreme), $EU(A)$ eventually exceeds $EU(B)$ --- but only by reversing the relationship between $C$ and $D$. The Extreme utility function achieves $A \succ B$ but forces $C \succ D$. The crossover is inevitable because $A \succ B$ and $D \succ C$ require contradictory constraints on the ratio $u(\$1M)/u(\$5M)$.

No amount of curvature adjustment can thread this needle. The failure is not a calibration problem --- it is a theorem. QED.

---

## 3. Multi-Objective Gamble Statistics

Before running the MOADT protocol, we examine the raw multi-objective statistics for all four gambles:

| Gamble | $\mathbb{E}[\$]$ | $\mathbb{E}[v]$ neutral | $\mathbb{E}[v]$ sqrt | $P(\text{adequate})$ | Reliability |
|--------|------------------:|------------------------:|---------------------:|---------------------:|------------:|
| A (certain \$1M) | \$1,000,000 | 0.2000 | 0.4472 | 1.00 | 1.00 |
| B (risky mix) | \$1,390,000 | 0.2780 | 0.4980 | 0.99 | 0.99 |
| C (11% \$1M) | \$110,000 | 0.0220 | 0.0492 | 0.11 | 0.11 |
| D (10% \$5M) | \$500,000 | 0.1000 | 0.1000 | 0.10 | 0.10 |

### 3.1 Problem 1: The Certainty Premium

B has higher expected value than A under both evaluators (\$1.39M vs. \$1M; 0.278 vs. 0.200 normalized). But A has **perfect** downside protection ($P(\text{adequate}) = 1.00$ vs. 0.99) and **perfect** reliability (1.00 vs. 0.99). A dominates B on two of three objectives; B dominates A on one. These are genuinely incommensurable --- not an "irrational bias."

The 1% gap between 1.00 and 0.99 may look trivially small, but it represents the difference between *certainty* and *uncertainty*. This is a qualitative, not merely quantitative, distinction. Every state under A yields an adequate outcome; under B, one state yields catastrophic loss. The multi-objective framework captures this as a real structural difference.

### 3.2 Problem 2: The Certainty Dimension Collapses

D has higher expected value than C (\$500K vs. \$110K; a 4.5x advantage). C has slightly higher downside protection (0.11 vs. 0.10) and reliability (0.11 vs. 0.10). But notice: both gambles are overwhelmingly risky. C gives \$0 with probability 0.89; D gives \$0 with probability 0.90. Neither gamble offers anything resembling certainty. The downside protection dimension --- which drove the structural advantage of A in Problem 1 --- is effectively neutralized. D's massive expected value advantage is the salient feature.

### 3.3 The Structural Asymmetry

This is the key insight: **the certainty dimension creates a genuine multi-objective advantage in Problem 1 that has no analogue in Problem 2.** In Problem 1, gamble A achieves perfection on two objectives. In Problem 2, neither gamble achieves anything close to perfection on any objective. The asymmetry between the two problems is structural, not parametric --- it cannot be captured by adjusting a utility function's curvature.

---

## 4. MOADT Analysis: Problem 1 (A vs. B)

### 4.1 Outcome Sets

Each action's outcome set $Y(a)$ contains one vector per $(P, \vec{f})$ pair. With $|\mathcal{P}| = 2$ priors and $|\mathcal{F}| = 2$ evaluators, each $Y(a)$ contains 4 vectors in $\mathbb{R}^3$.

**$Y(\text{A\_certain\_1M})$:**

| $(P, \vec{f})$ pair | Expected value | Downside protection | Reliability |
|---------------------|---------------:|--------------------:|------------:|
| $(P_{\text{exact}}, v_{\text{neutral}})$ | 0.2000 | 1.0000 | 1.0000 |
| $(P_{\text{exact}}, v_{\text{cautious}})$ | 0.4472 | 1.0000 | 1.0000 |
| $(P_{\text{perturbed}}, v_{\text{neutral}})$ | 0.2000 | 1.0000 | 1.0000 |
| $(P_{\text{perturbed}}, v_{\text{cautious}})$ | 0.4472 | 1.0000 | 1.0000 |

A's outcome set is remarkably stable: regardless of evaluator or prior, downside protection and reliability are always exactly 1.0. This is the mathematical signature of certainty --- the outcome set has zero spread on objectives 2 and 3.

**$Y(\text{B\_risky\_mix})$:**

| $(P, \vec{f})$ pair | Expected value | Downside protection | Reliability |
|---------------------|---------------:|--------------------:|------------:|
| $(P_{\text{exact}}, v_{\text{neutral}})$ | 0.2780 | 0.9900 | 0.9900 |
| $(P_{\text{exact}}, v_{\text{cautious}})$ | 0.4980 | 0.9900 | 0.9900 |
| $(P_{\text{perturbed}}, v_{\text{neutral}})$ | 0.2696 | 0.9880 | 0.9880 |
| $(P_{\text{perturbed}}, v_{\text{cautious}})$ | 0.4916 | 0.9880 | 0.9880 |

B's expected value is higher than A's under every $(P, \vec{f})$ pair, but its downside protection and reliability fall below 1.0. The perturbed prior reduces these further (0.988 vs. 0.990), demonstrating sensitivity to probability uncertainty.

### 4.2 Robust Dominance

We check: does either action robustly dominate the other?

$A \succ_R B$ requires: $\forall \vec{y}_B \in Y(B), \exists \vec{y}_A \in Y(A)$ such that $\vec{y}_A \succ_P \vec{y}_B$.

Take B's best vector $(P_{\text{exact}}, v_{\text{cautious}})$: $(0.498, 0.990, 0.990)$. A's best expected value is 0.4472, which is less than 0.498. So no vector in $Y(A)$ can Pareto-dominate this vector --- A always loses on expected value. Therefore $A \not\succ_R B$.

$B \succ_R A$ requires: $\forall \vec{y}_A \in Y(A), \exists \vec{y}_B \in Y(B)$ such that $\vec{y}_B \succ_P \vec{y}_A$.

Take any vector in $Y(A)$: downside protection and reliability are 1.0. No vector in $Y(B)$ reaches 1.0 on these objectives. Therefore $B \not\succ_R A$.

**Result:** No robust dominance. $\text{Adm}(A) = \{\text{A\_certain\_1M}, \text{B\_risky\_mix}\}$.

### 4.3 Protocol Trace

**Layer 1 (Constraints):** No binding constraints in this run ($\text{constraint\_floor} = \{\}$).

$$C = \{\text{A\_certain\_1M}, \text{B\_risky\_mix}\}$$

$$F = \text{Adm}(C) = \{\text{A\_certain\_1M}, \text{B\_risky\_mix}\}$$

**Layer 2 (Reference-Point Satisficing):** $\vec{r} = (0.15, 0.05, 0.50)$ --- modest aspirations reflecting that even a small expected value and minimal downside protection are acceptable, but reliability should be at least 50%.

Both actions satisfy the reference point under all $(P, \vec{f})$ pairs:

$$\text{Sat}(F, \vec{r}) = \{\text{A\_certain\_1M}, \text{B\_risky\_mix}\}$$

**Layer 3 (Regret-Pareto):** For each action and objective, we compute the worst-case regret --- the maximum gap between the best alternative and this action, across all $(P, \vec{f})$ pairs:

$$\vec{\rho}(\text{A\_certain\_1M}) = (0.078, \; 0, \; 0)$$

$$\vec{\rho}(\text{B\_risky\_mix}) = (0, \; 0.012, \; 0.012)$$

A's only regret is on expected value: B beats it by at most 0.078. A has zero regret on downside protection and reliability --- it is never worse than B on these objectives.

B's only regret is on downside protection and reliability: A beats it by at most 0.012 on each. B has zero regret on expected value.

Neither regret vector Pareto-dominates the other: $(0.078, 0, 0)$ vs. $(0, 0.012, 0.012)$. A has lower regret on objectives 2 and 3; B has lower regret on objective 1.

$$R = \{\text{A\_certain\_1M}, \text{B\_risky\_mix}\}$$

**Layer 4 (Deference):** $|R| = 2 > 1$. The protocol defers to the principal:

> Both A and B are admissible. A sacrifices 0.078 in expected value for zero regret on safety dimensions. B sacrifices 0.012 in downside protection and reliability for zero regret on expected value. The theory cannot resolve this tradeoff without a value judgment about how much certainty is worth. This is the principal's decision.

---

## 5. MOADT Analysis: Problem 2 (C vs. D)

### 5.1 Outcome Sets

**$Y(\text{C\_11pct\_1M})$:**

| $(P, \vec{f})$ pair | Expected value | Downside protection | Reliability |
|---------------------|---------------:|--------------------:|------------:|
| $(P_{\text{exact}}, v_{\text{neutral}})$ | 0.0220 | 0.1100 | 0.1100 |
| $(P_{\text{exact}}, v_{\text{cautious}})$ | 0.0492 | 0.1100 | 0.1100 |
| $(P_{\text{perturbed}}, v_{\text{neutral}})$ | 0.0200 | 0.1000 | 0.1000 |
| $(P_{\text{perturbed}}, v_{\text{cautious}})$ | 0.0447 | 0.1000 | 0.1000 |

**$Y(\text{D\_10pct\_5M})$:**

| $(P, \vec{f})$ pair | Expected value | Downside protection | Reliability |
|---------------------|---------------:|--------------------:|------------:|
| $(P_{\text{exact}}, v_{\text{neutral}})$ | 0.1000 | 0.1000 | 0.1000 |
| $(P_{\text{exact}}, v_{\text{cautious}})$ | 0.1000 | 0.1000 | 0.1000 |
| $(P_{\text{perturbed}}, v_{\text{neutral}})$ | 0.0900 | 0.0900 | 0.0900 |
| $(P_{\text{perturbed}}, v_{\text{cautious}})$ | 0.0900 | 0.0900 | 0.0900 |

Two immediate observations:

1. D's outcome set is identical across both evaluators (neutral and cautious). This is because D's payoff is either \$0 or \$5M. The normalized value of \$5M is 1.0 under both evaluators ($v_{\text{neutral}}(5M) = 1.0$, $v_{\text{cautious}}(5M) = \sqrt{1.0} = 1.0$), and $v(0) = 0$ for both. So the evaluator distinction is irrelevant for D.

2. C has a tiny edge on downside protection and reliability (0.11 vs. 0.10 under exact prior), but D has a massive edge on expected value (0.10 vs. 0.022 under neutral, 0.10 vs. 0.049 under cautious).

### 5.2 Robust Dominance

Neither action robustly dominates the other. D cannot Pareto-dominate C's vectors because C has higher downside protection and reliability under the exact prior (0.11 > 0.10). C cannot Pareto-dominate D because D has much higher expected value.

$$\text{Adm}(A) = \{\text{C\_11pct\_1M}, \text{D\_10pct\_5M}\}$$

### 5.3 Protocol Trace

**Layer 1 (Constraints):** No binding constraints. Both pass.

$$C = \{\text{C\_11pct\_1M}, \text{D\_10pct\_5M}\}, \quad F = \text{Adm}(C) = \{\text{C\_11pct\_1M}, \text{D\_10pct\_5M}\}$$

**Layer 2 (Reference-Point Satisficing):** $\vec{r} = (0.05, 0.00, 0.05)$ --- very low aspirations, reflecting that both gambles are overwhelmingly likely to yield \$0.

C's worst vector is $(0.0200, 0.1000, 0.1000)$. The expected value of 0.02 falls below the aspiration of 0.05 on objective 1. **C fails the reference point.**

D's worst vector is $(0.0900, 0.0900, 0.0900)$. All components meet or exceed the aspiration levels. **D passes.**

$$\text{Sat}(F, \vec{r}) = \{\text{D\_10pct\_5M}\}$$

**Layer 3 (Regret-Pareto):** With only one action surviving:

$$\vec{\rho}(\text{D\_10pct\_5M}) = (0, \; 0, \; 0)$$

$$R = \{\text{D\_10pct\_5M}\}$$

**Layer 4 (Deference):** $|R| = 1$. **Unique recommendation: D.**

### 5.4 The Resolution So Far

Without constraints, MOADT produces:
- **Problem 1:** Both A and B are admissible; deference to the principal (who can rationally choose A).
- **Problem 2:** D is uniquely recommended (C fails satisficing on expected value).

The Allais preference pattern $A \succ B$ and $D \succ C$ is *compatible* with MOADT --- the theory does not force $C \succ D$ as a consequence of $A \succ B$. The Independence Axiom has no analogue in MOADT's multi-objective framework.

---

## 6. MOADT with Constraints

### 6.1 Problem 1: Downside Floor Eliminates B

We now add a hard constraint: downside protection $\geq 0.5$ per state per evaluator. This means every state must yield an adequate outcome ($\geq$ \$500K). This is a non-negotiable floor --- not a tradeoff.

**Constraint check:**
- A: Every state gives \$1M $\geq$ \$500K. Adequate indicator = 1.0 in all 100 states. **PASS.**
- B: State 100 gives \$0 $<$ \$500K. Adequate indicator = 0.0 in that state. **FAIL.**

The protocol trace:

**Layer 1:** B fails the constraint.

$$C = \{\text{A\_certain\_1M}\}, \quad F = \text{Adm}(C) = \{\text{A\_certain\_1M}\}$$

**Layers 2--3:** With only one action, A trivially passes satisficing and has zero regret.

$$R = \{\text{A\_certain\_1M}\}$$

**Layer 4:** $|R| = 1$. **Unique recommendation: A.**

### 6.2 Problem 2: Same Floor Eliminates Both

We apply the identical constraint to Problem 2:

**Constraint check:**
- C: 89 states give \$0 $<$ \$500K. Adequate indicator = 0.0 in those states. **FAIL.**
- D: 90 states give \$0 $<$ \$500K. Adequate indicator = 0.0 in those states. **FAIL.**

The protocol trace:

**Layer 1:** Both actions fail. $C = \emptyset$.

$$\text{WARNING: } C = \emptyset \text{ --- no action satisfies all constraints!}$$

This is an **error condition**. The constraint is too strict for this decision context --- both gambles involve overwhelming ruin risk. The protocol escalates to the principal, who must either relax the constraint or accept the risk.

### 6.3 The Asymmetry Explained

This is precisely how MOADT dissolves the paradox through constraints:

- In Problem 1, the adequacy constraint provides a clean separation: A passes, B fails. The constraint reflects a genuine qualitative difference between certainty and near-certainty.
- In Problem 2, the same constraint does **not** favor C over D. Both gambles fail, because both involve substantial ruin risk. The constraint that eliminates B (1% ruin) does not force $C \succ D$, because C also has ruin risk (89%).

Under EU, $A \succ B$ logically implies $C \succ D$ (the Independence Axiom). Under MOADT with constraints, "eliminate B because it has ruin risk" does **not** imply "prefer C over D" --- because C also has ruin risk. The logical entailment that creates the paradox simply does not exist in the MOADT framework.

---

## 7. Combined Analysis: All Four Gambles

Running all four gambles through a single MOADT problem reveals the dominance structure:

### 7.1 Outcome Sets

All outcome sets are as computed in Sections 4.1 and 5.1 above. The key new information is the pairwise dominance analysis.

### 7.2 Robust Dominance

| Dominance pair | Result |
|----------------|--------|
| A $\succ_R$ C | **Yes** --- A dominates C on all objectives under all $(P, \vec{f})$ pairs |
| A $\succ_R$ D | **Yes** --- A dominates D on all objectives under all $(P, \vec{f})$ pairs |
| B $\succ_R$ C | **Yes** --- B dominates C on all objectives under all $(P, \vec{f})$ pairs |
| B $\succ_R$ D | **Yes** --- B dominates D on all objectives under all $(P, \vec{f})$ pairs |
| A $\succ_R$ B | No |
| B $\succ_R$ A | No |

Both Problem 1 gambles robustly dominate both Problem 2 gambles. This is unsurprising --- the Problem 1 gambles have higher expected value, higher downside protection, and higher reliability across the board. Within each problem, the actions remain incomparable.

$$\text{Adm}(A) = \{\text{A\_certain\_1M}, \text{B\_risky\_mix}\}$$

C and D are eliminated by robust dominance before the protocol even begins.

### 7.3 Protocol Trace

**Layer 1 (Constraints):** No binding constraints. All four pass constraint check, but the feasible set is restricted to the admissible set.

$$F = \text{Adm}(C) = \{\text{A\_certain\_1M}, \text{B\_risky\_mix}\}$$

**Layer 2 (Satisficing):** $\vec{r} = (0.10, 0.00, 0.10)$. Both A and B pass.

$$\text{Sat}(F, \vec{r}) = \{\text{A\_certain\_1M}, \text{B\_risky\_mix}\}$$

**Layer 3 (Regret-Pareto):**

$$\vec{\rho}(\text{A\_certain\_1M}) = (0.078, \; 0, \; 0)$$
$$\vec{\rho}(\text{B\_risky\_mix}) = (0, \; 0.012, \; 0.012)$$

Pareto-incomparable. $R = \{\text{A\_certain\_1M}, \text{B\_risky\_mix}\}$.

**Layer 4 (Deference):** $|R| = 2 > 1$. Defer to principal.

### 7.4 Interpretation

When all four gambles compete simultaneously, the combined analysis confirms the within-problem structure: A and B are the only viable options (C and D are robustly dominated), and the tradeoff between A and B is exactly as described in Section 4. The between-problem comparison is trivial --- Problem 1 gambles are simply better than Problem 2 gambles on every dimension.

---

## 8. Scalar EU Comparison

### 8.1 The Knife-Edge Problem

Even within the three-objective MOADT framework, one might ask: can we find a weight vector $\vec{w} = (w_1, w_2, w_3)$ that produces $A \succ B$ and $D \succ C$ simultaneously via scalar aggregation $U(a) = \vec{w} \cdot \vec{y}(a)$?

**Evaluator: risk-neutral, Prior: exact probabilities:**

| Weights | A | B | C | D | P1 winner | P2 winner |
|---------|------:|------:|------:|------:|:---------:|:---------:|
| Pure expected value $(1, 0, 0)$ | 0.2000 | 0.2780 | 0.0220 | 0.1000 | B | D |
| Pure downside $(0, 1, 0)$ | 1.0000 | 0.9900 | 0.1100 | 0.1000 | A | C |
| Pure reliability $(0, 0, 1)$ | 1.0000 | 0.9900 | 0.1100 | 0.1000 | A | C |
| Balanced $(1/3, 1/3, 1/3)$ | 0.7333 | 0.7527 | 0.0807 | 0.1000 | B | D |
| Value + safety $(0.4, 0.4, 0.2)$ | 0.6800 | 0.7052 | 0.0748 | 0.1000 | B | D |
| Safety-heavy $(0.2, 0.5, 0.3)$ | 0.8400 | 0.8476 | 0.0924 | 0.1000 | B | D |
| Value-heavy $(0.7, 0.1, 0.2)$ | 0.4400 | 0.4916 | 0.0484 | 0.1000 | B | D |
| Knife-edge $(0.1136, 0.4432, 0.4432)$ | 0.9091 | 0.9091 | 0.1000 | 0.1000 | A | C |

**Evaluator: sqrt-concave, Prior: exact probabilities:**

| Weights | A | B | C | D | P1 winner | P2 winner |
|---------|------:|------:|------:|------:|:---------:|:---------:|
| Pure expected value $(1, 0, 0)$ | 0.4472 | 0.4980 | 0.0492 | 0.1000 | B | D |
| Pure downside $(0, 1, 0)$ | 1.0000 | 0.9900 | 0.1100 | 0.1000 | A | C |
| Pure reliability $(0, 0, 1)$ | 1.0000 | 0.9900 | 0.1100 | 0.1000 | A | C |
| Balanced $(1/3, 1/3, 1/3)$ | 0.8157 | 0.8260 | 0.0897 | 0.1000 | B | D |
| Value + safety $(0.4, 0.4, 0.2)$ | 0.7789 | 0.7932 | 0.0857 | 0.1000 | B | D |
| Safety-heavy $(0.2, 0.5, 0.3)$ | 0.8894 | 0.8916 | 0.0978 | 0.1000 | B | D |
| Value-heavy $(0.7, 0.1, 0.2)$ | 0.6130 | 0.6456 | 0.0674 | 0.1000 | B | D |
| Knife-edge $(0.1136, 0.4432, 0.4432)$ | 0.9372 | 0.9341 | 0.1031 | 0.1000 | A | C |

### 8.2 The Vanishingly Narrow Feasible Region

No weight vector in either table produces the Allais pattern ($A \succ B$ and $D \succ C$). The pattern is always either $B + D$ (expected value dominates) or $A + C$ (safety dominates).

The algebra explains why. Under risk-neutral evaluation with the exact prior:

$$U(A) = 0.20 w_1 + 1.00 w_2 + 1.00 w_3$$
$$U(B) = 0.278 w_1 + 0.99 w_2 + 0.99 w_3$$

$A \geq B$ requires:

$$0.01(w_2 + w_3) \geq 0.078 w_1 \quad \Longrightarrow \quad \frac{w_2 + w_3}{w_1} \geq 7.8$$

Meanwhile:

$$U(D) = 0.10 w_1 + 0.10 w_2 + 0.10 w_3$$
$$U(C) = 0.022 w_1 + 0.11 w_2 + 0.11 w_3$$

$D \geq C$ requires:

$$0.078 w_1 \geq 0.01(w_2 + w_3) \quad \Longrightarrow \quad \frac{w_2 + w_3}{w_1} \leq 7.8$$

Both thresholds are *exactly* 7.8 --- the same coefficients (0.078 and 0.01) appear in both inequalities because the objective-value gaps between the safe and risky options are identical in both problems. The feasible region for strict preferences ($A \succ B$ and $D \succ C$ simultaneously) is therefore *empty*:

$$A \succ B \text{ requires } \frac{w_2 + w_3}{w_1} > 7.8, \qquad D \succ C \text{ requires } \frac{w_2 + w_3}{w_1} < 7.8$$

These are contradictory. The only solution is the exact boundary point $(w_2 + w_3)/w_1 = 7.8$, where $A = B$ and $C = D$ simultaneously (both problems are dead ties). The knife-edge weights $(0.1136, 0.4432, 0.4432)$ sit at this unique point. Any perturbation flips one preference but necessarily flips the other in the opposite direction.

A scalar weighting cannot even weakly "achieve" the Allais pattern --- the best it can do is produce simultaneous ties on both problems, which is not a preference at all. **No scalar weighting over three objectives can reproduce the Allais preferences, even approximately.** This is exactly why MOADT's non-scalar approach is necessary: it keeps the objectives separate and never needs to find the "right" weights.

---

## 9. The Mechanism: How MOADT Accommodates the Allais Preferences

MOADT resolves the Allais paradox through three reinforcing mechanisms.

### 9.1 Multi-Objective Structure (Layer 0)

EU theory forces all considerations into a single scalar $u(x)$. MOADT maintains separate objectives --- expected value, downside protection, and reliability --- that are genuinely incommensurable.

**In Problem 1 (A vs. B):**
- B beats A on expected value.
- A beats B on downside protection (1.00 vs. 0.99) and reliability (1.00 vs. 0.99).
- Neither robustly dominates the other. Both are admissible.
- The "certainty premium" is captured as a real advantage on 2 of 3 objectives.

**In Problem 2 (C vs. D):**
- D beats C on expected value (0.10 vs. 0.022 neutral; 0.10 vs. 0.049 cautious).
- C barely beats D on downside protection (0.11 vs. 0.10) and reliability (0.11 vs. 0.10).
- With both gambles being overwhelmingly risky, the certainty dimension collapses.
- D's expected value advantage is massive; C's safety edge is marginal.
- D is selected by satisficing; C fails the reference point.

The **structural asymmetry** between problems is the key: in Problem 1, certainty creates a genuine multi-objective advantage on two dimensions. In Problem 2, both gambles are risky, so the dimensions that favored A are effectively neutralized.

### 9.2 Hard Constraints (Layer 1)

If the agent has a non-negotiable floor on downside protection (e.g., "never risk total ruin"), then:
- **Problem 1:** B fails (1% chance of \$0), A passes. A is selected.
- **Problem 2:** Both fail (both have \$0 outcomes). Escalate to principal.

The constraint provides an **absolute veto**, not a tradeoff. This reflects how people actually think about certainty: "guaranteed money" vs. "a chance of nothing" is qualitatively different, not just quantitatively. The constraint that eliminates B does **not** force $C \succ D$, because C also has ruin risk.

### 9.3 Regret-Pareto Selection (Layer 3)

When both actions survive to Layer 3, minimax regret captures asymmetric opportunity costs:
- Choosing A and missing B's upside: regret is modest (expected value gap of 0.078).
- Choosing B and getting \$0: regret is on the downside and reliability dimensions (gaps of 0.012 each).

In Problem 2, the regret structure is different: D's expected value advantage is so large relative to C's marginal safety edge that satisficing resolves the problem at Layer 2 before regret analysis is needed.

### 9.4 Why the Independence Axiom Fails in MOADT

The Independence Axiom says: if you prefer A to B, then for any gamble X and any mixing probability $\alpha$, you should prefer the mixture $\alpha A + (1-\alpha)X$ to $\alpha B + (1-\alpha)X$. The common component X should be irrelevant.

In scalar EU, this axiom is a theorem --- it follows from linearity of expectation applied to a single utility function. In MOADT, it is not a theorem because:

1. MOADT does not have a single utility function. It has a vector of objectives.
2. The admissibility criterion (robust dominance) is a partial order, not a total order. Mixing in a common component can change which actions are Pareto-incomparable.
3. The choice protocol layers (constraints, satisficing, regret) are sensitive to the structure of the outcome sets, not just their expected values.

The Allais paradox is only a "paradox" if you accept that a single scalar utility function should capture all human preferences. MOADT rejects this premise.

---

## 10. Summary and What This Demonstrates

```
Problem 1 (A vs B), no constraints:
  Admissible set:      {A_certain_1M, B_risky_mix}
  Satisficing set:     {A_certain_1M, B_risky_mix}
  Regret-Pareto set:   {A_certain_1M, B_risky_mix}
  Deference needed:    Yes
  -> Both admissible; principal can rationally choose A

Problem 2 (C vs D), no constraints:
  Admissible set:      {C_11pct_1M, D_10pct_5M}
  Satisficing set:     {D_10pct_5M}
  Regret-Pareto set:   {D_10pct_5M}
  Deference needed:    No
  -> D uniquely recommended

Problem 1, downside floor (>= $500K per state):
  Constraint set:      {A_certain_1M}
  -> B eliminated (1% ruin risk). A uniquely selected.

Problem 2, same downside floor:
  Constraint set:      {} (empty)
  -> BOTH fail. Error condition: escalate to principal.
  -> The constraint that eliminates B does NOT force C > D.

Combined (all 4 gambles, no constraints):
  Admissible set:      {A_certain_1M, B_risky_mix}
  Dominance:           A >_R C, A >_R D, B >_R C, B >_R D
  Regret-Pareto set:   {A_certain_1M, B_risky_mix}
  Deference needed:    Yes
```

### What This Demonstrates

1. **The Allais "paradox" is not a paradox.** It is a perfectly rational pattern of preferences once you stop forcing multi-dimensional concerns through a one-dimensional bottleneck. People who prefer A to B are not violating rationality --- they are giving weight to downside protection and reliability alongside expected value. People who prefer D to C are not contradicting their Problem 1 preference --- the certainty dimension that created A's structural advantage simply does not exist in Problem 2.

2. **Scalar utility cannot accommodate the pattern.** No single utility function produces both $A \succ B$ and $D \succ C$. Even scalarizing over three objectives fails: the same coefficients (0.078 and 0.01) appear in both problems, so $A \succ B$ requires $(w_2+w_3)/w_1 > 7.8$ while $D \succ C$ requires $(w_2+w_3)/w_1 < 7.8$ — a contradiction. The only solution is the exact tie point where both problems are dead ties. The failure is structural, not parametric.

3. **MOADT's non-scalar structure is essential.** By keeping objectives separate, MOADT allows the dominance structure to differ between problems. A has a genuine multi-objective advantage over B (perfection on 2 of 3 objectives); D has a genuine expected value advantage over C in a context where the safety objectives are neutralized. These are different structural configurations, not contradictory preferences.

4. **Constraints provide qualitative distinctions.** The constraint mechanism captures the qualitative difference between certainty and near-certainty. A constraint that eliminates B (1% ruin risk) does not logically force $C \succ D$ --- because C has 89% ruin risk. The logical entailment that creates the paradox under EU ($A \succ B \Rightarrow C \succ D$) has no analogue in MOADT.

5. **Deference is appropriate.** In Problem 1, MOADT does not force the choice of A --- it identifies both A and B as admissible and presents the tradeoff transparently. The theory makes room for the Allais preference without mandating it. A principal who prefers B (accepting 1% ruin risk for higher expected value) is also acting rationally within MOADT.

---

## Appendix: Computational Verification

All numerical results in this document were produced by `examples/classic_allais.py` using the MOADT engine (`moadt/_engine.py`). The code uses the `build_allais_problem_v2` encoding: 100 equiprobable states, 2 evaluators (risk-neutral and sqrt-concave), 2 priors (exact and perturbed), and 3 objectives (expected value, downside protection, reliability). The code is available in the repository and can be run independently to verify every number.

Key implementation details:
- States are sorted so that worst outcomes occupy the highest-numbered states, making the perturbed prior genuinely pessimistic.
- The downside protection objective uses an indicator function: $\mathbf{1}_{\text{payoff} \geq \$500K}$, so its expectation equals the probability of an adequate outcome.
- The reliability objective uses an indicator function: $\mathbf{1}_{\text{payoff} > \$0}$, so its expectation equals the probability of any positive payoff.
- Constraints in Section 6 are per-state, per-evaluator checks (not on expected values).

---

## References

- Allais, M. (1953). Le comportement de l'homme rationnel devant le risque: critique des postulats et axiomes de l'ecole americaine. *Econometrica*, 21(4), 503--546.
- MOADT (Multi-Objective Admissible Decision Theory) is defined in the companion paper.
- Freeman (2025), "The Scalarization Trap," provides the motivation for why scalar expected utility is structurally problematic for alignment.
- Kahneman, D. & Tversky, A. (1979). Prospect theory: An analysis of decision under risk. *Econometrica*, 47(2), 263--292.
