# MOADT Worked Example 7: The Ellsberg Paradox

*A concrete walkthrough of Multi-Objective Admissible Decision Theory applied to ambiguity aversion*

---

## Overview

This document applies MOADT -- Multi-Objective Admissible Decision Theory -- to the Ellsberg Paradox, one of the most celebrated challenges to Expected Utility (EU) theory. Every computation is shown explicitly: outcome sets, robust dominance checks, all four layers of the choice protocol, and a comparison with scalar expected utility. The goal is to demonstrate that the behavior decision theorists have called "irrational ambiguity aversion" for over sixty years is, in fact, rational multi-objective decision-making under Knightian uncertainty.

The Ellsberg Paradox matters because it strikes at the foundations of decision theory. Since Savage (1954), the normative consensus has been that rational agents maximize expected utility with respect to a single subjective probability distribution. Ellsberg (1961) showed that ordinary people systematically violate this axiom -- and that most decision theorists, when confronted with the problem, violate it too. The usual response has been to treat this as a cognitive bias, or to introduce ad hoc "ambiguity aversion" parameters. MOADT offers a structural resolution: the paradox disappears once you allow multiple priors, multiple objectives, and multiple evaluators.

The problem is small enough that every number fits on the page. The action set has 4 elements, the state space has 7 elements, the credal set has 5 distributions, and the evaluator set has 2 functions. This means each action's outcome set $Y(a)$ contains exactly 10 vectors in $\mathbb{R}^2$. Nothing is hidden behind "in the general case" -- the reader can check every claim with a calculator.

---

## 1. The Scenario

### 1.1 The Classic Setup

An urn contains 90 balls:

- **30 are Red** (known)
- **60 are Black and Yellow** in an unknown proportion

Four bets are offered, each paying \$100 if a ball of the specified color(s) is drawn, and \$0 otherwise:

| Bet | Wins on | Win probability | Status |
|-----|---------|-----------------|--------|
| Bet I | Red | $P = 1/3$ | **Known** |
| Bet II | Black | $P = 0$ to $2/3$ | **Ambiguous** |
| Bet III | Red or Yellow | $P = 1/3$ to $1$ | **Ambiguous** |
| Bet IV | Black or Yellow | $P = 2/3$ | **Known** |

### 1.2 The Paradox

When presented with these bets, most people -- including trained decision theorists -- express two preferences:

$$\text{Bet I} \succ \text{Bet II} \qquad \text{and} \qquad \text{Bet IV} \succ \text{Bet III}$$

Under Expected Utility theory, this is contradictory. If you hold a single subjective probability distribution over urn compositions, then:

- $\text{Bet I} \succ \text{Bet II}$ implies $P(\text{Red}) > P(\text{Black})$, i.e., $P(\text{Red}) > P(\text{Black})$
- $\text{Bet IV} \succ \text{Bet III}$ implies $P(\text{Black} + \text{Yellow}) > P(\text{Red} + \text{Yellow})$, i.e., $P(\text{Black}) > P(\text{Red})$

These two implications contradict each other. More precisely, under any single prior, $E[\text{Bet I}] + E[\text{Bet IV}] = E[\text{Bet II}] + E[\text{Bet III}] = 1.0$, so preferring the known bet in both choices is impossible under EU.

### 1.3 MOADT Formulation

MOADT resolves this by modeling the problem with three structural generalizations: a credal set instead of a single prior, multiple objectives instead of a single scalar value, and an evaluator set instead of a single evaluation function.

**States ($|S| = 7$).** The uncertainty is about the composition of the 60 unknown balls. We discretize into 7 states:

| State | Black balls | Yellow balls | Description |
|-------|-------------|--------------|-------------|
| $s_{0B/60Y}$ | 0 | 60 | All yellow |
| $s_{10B/50Y}$ | 10 | 50 | Mostly yellow |
| $s_{20B/40Y}$ | 20 | 40 | Yellow-leaning |
| $s_{30B/30Y}$ | 30 | 30 | Even split |
| $s_{40B/20Y}$ | 40 | 20 | Black-leaning |
| $s_{50B/10Y}$ | 50 | 10 | Mostly black |
| $s_{60B/0Y}$ | 60 | 0 | All black |

Each state determines a precise probability of drawing each color: $P(\text{Red}) = 30/90$, $P(\text{Black}) = b/90$, $P(\text{Yellow}) = (60-b)/90$. The uncertainty is not about the draw -- it is about which state obtains. This is Knightian uncertainty, not risk.

**Actions ($|A| = 4$).** The four bets.

**Objectives ($k = 2$).**

| Objective | Meaning | Scale |
|-----------|---------|-------|
| $f_1$: Monetary payoff | Expected winnings from the bet | Normalized to $[0, 1]$ where $1 = \$100$ |
| $f_2$: Knowability | How well you know the bet's win probability | $1$ if state-independent, otherwise $1 - |b - 30|/30$ |

The knowability objective captures something EU theory cannot represent: the distinct value of *knowing your odds*. For Bets I and IV, the win probability is the same in every state, so knowability $= 1.0$ always. For Bets II and III, the win probability depends on the unknown composition, so knowability varies -- it equals 1.0 at the symmetric state ($s_{30B/30Y}$) and drops to 0.0 at the extreme states ($s_{0B/60Y}$ and $s_{60B/0Y}$).

These objectives are *incommensurable*: MOADT does not assume an exchange rate between money and informational confidence.

**Credal Set ($|\mathcal{P}| = 5$).** Five probability distributions over the 7 states, representing different beliefs about the urn composition:

| Prior | $s_{0B}$ | $s_{10B}$ | $s_{20B}$ | $s_{30B}$ | $s_{40B}$ | $s_{50B}$ | $s_{60B}$ | Interpretation |
|-------|----------|-----------|-----------|-----------|-----------|-----------|-----------|----------------|
| $P_{\text{uniform}}$ | 0.1429 | 0.1429 | 0.1429 | 0.1429 | 0.1429 | 0.1429 | 0.1429 | "I have no idea" |
| $P_{\text{extreme}}$ | 0.3750 | 0.0625 | 0.0375 | 0.0500 | 0.0375 | 0.0625 | 0.3750 | "Probably all-or-nothing" |
| $P_{\text{black}}$ | 0.0200 | 0.0500 | 0.0800 | 0.1500 | 0.2500 | 0.2500 | 0.2000 | "More black than yellow" |
| $P_{\text{yellow}}$ | 0.2000 | 0.2500 | 0.2500 | 0.1500 | 0.0800 | 0.0500 | 0.0200 | "More yellow than black" |
| $P_{\text{moderate}}$ | 0.0200 | 0.0800 | 0.2000 | 0.4000 | 0.2000 | 0.0800 | 0.0200 | "Probably close to 30/30" |

The credal set says: "we don't know which model of the urn is correct." This is the key structural difference from EU theory, which demands a single prior.

**Evaluator Set ($|\mathcal{F}| = 2$).**

- $e_{\text{neutral}}$: Takes monetary payoff at face value. Knowability unchanged.
- $e_{\text{cautious}}$: Applies a concave $\sqrt{\cdot}$ transform to monetary payoff (reflecting diminishing marginal value of money). Knowability unchanged.

**Constraints.** None. This is a pure preference problem -- all bets are available and there is no risk of ruin.

**Reference Point.** $\vec{r} = (0.25, 0.50)$ -- modest aspiration of at least \$25 in expected value and at least moderate knowability.

---

## 2. Computing Outcome Sets $Y(a)$

Each action's outcome set contains one vector for each $(P, e)$ pair. With $|\mathcal{P}| = 5$ and $|\mathcal{F}| = 2$, each $Y(a)$ contains exactly 10 vectors.

The computation for each vector is:

$$\vec{y}_{(P, e)}(a) = \sum_{s \in S} P(s) \cdot e(\omega(a, s))$$

where $\omega(a, s)$ is the raw outcome vector (payoff, knowability) for action $a$ in state $s$, and $e$ applies any evaluator transformation.

### 2.1 Win Probabilities by State

Before computing outcome sets, it is instructive to see the raw win probabilities that drive objective 1:

| State | Bet I (Red) | Bet II (Black) | Bet III (R+Y) | Bet IV (B+Y) |
|-------|-------------|----------------|---------------|---------------|
| 0B/60Y | 0.3333 | 0.0000 | 1.0000 | 0.6667 |
| 10B/50Y | 0.3333 | 0.1111 | 0.8889 | 0.6667 |
| 20B/40Y | 0.3333 | 0.2222 | 0.7778 | 0.6667 |
| 30B/30Y | 0.3333 | 0.3333 | 0.6667 | 0.6667 |
| 40B/20Y | 0.3333 | 0.4444 | 0.5556 | 0.6667 |
| 50B/10Y | 0.3333 | 0.5556 | 0.4444 | 0.6667 |
| 60B/0Y | 0.3333 | 0.6667 | 0.3333 | 0.6667 |

The critical observation: Bet I yields 0.3333 in *every* state. Bet IV yields 0.6667 in *every* state. These are known-probability bets -- their payoff does not depend on the unknown composition. Bets II and III, by contrast, range from 0 to 0.6667 and from 0.3333 to 1.0000 respectively. Under EU with any single prior, $E[\text{II}] + E[\text{III}] = E[\text{I}] + E[\text{IV}] = 1.0$, which is why EU cannot simultaneously prefer I over II and IV over III.

### 2.2 Detailed Outcome Sets

**$Y(\text{Bet I})$ -- Red (known 1/3):**

| $(P, e)$ pair | Payoff | Knowability |
|---------------|--------|-------------|
| $(P_{\text{uniform}}, e_{\text{neutral}})$ | 0.3333 | 1.0000 |
| $(P_{\text{uniform}}, e_{\text{cautious}})$ | 0.5774 | 1.0000 |
| $(P_{\text{extreme}}, e_{\text{neutral}})$ | 0.3333 | 1.0000 |
| $(P_{\text{extreme}}, e_{\text{cautious}})$ | 0.5774 | 1.0000 |
| $(P_{\text{black}}, e_{\text{neutral}})$ | 0.3333 | 1.0000 |
| $(P_{\text{black}}, e_{\text{cautious}})$ | 0.5774 | 1.0000 |
| $(P_{\text{yellow}}, e_{\text{neutral}})$ | 0.3333 | 1.0000 |
| $(P_{\text{yellow}}, e_{\text{cautious}})$ | 0.5774 | 1.0000 |
| $(P_{\text{moderate}}, e_{\text{neutral}})$ | 0.3333 | 1.0000 |
| $(P_{\text{moderate}}, e_{\text{cautious}})$ | 0.5774 | 1.0000 |
| **Ranges** | **[0.3333, 0.5774]** | **[1.0000, 1.0000]** |

Bet I's outcome set contains only *two distinct points*: $(0.3333, 1.0)$ and $(0.5774, 1.0)$. The payoff varies only because of the evaluator difference ($\sqrt{1/3} \approx 0.5774$ vs. $1/3 \approx 0.3333$). The knowability is identically 1.0 -- no spread at all. This is the signature of a known-probability bet: the credal set has *no effect* on its outcome set.

**$Y(\text{Bet II})$ -- Black (ambiguous):**

| $(P, e)$ pair | Payoff | Knowability |
|---------------|--------|-------------|
| $(P_{\text{uniform}}, e_{\text{neutral}})$ | 0.3333 | 0.4286 |
| $(P_{\text{uniform}}, e_{\text{cautious}})$ | 0.5158 | 0.4286 |
| $(P_{\text{extreme}}, e_{\text{neutral}})$ | 0.3333 | 0.1417 |
| $(P_{\text{extreme}}, e_{\text{cautious}})$ | 0.4451 | 0.1417 |
| $(P_{\text{black}}, e_{\text{neutral}})$ | 0.4567 | 0.4700 |
| $(P_{\text{black}}, e_{\text{cautious}})$ | 0.6573 | 0.4700 |
| $(P_{\text{yellow}}, e_{\text{neutral}})$ | 0.2100 | 0.4700 |
| $(P_{\text{yellow}}, e_{\text{cautious}})$ | 0.3947 | 0.4700 |
| $(P_{\text{moderate}}, e_{\text{neutral}})$ | 0.3333 | 0.7200 |
| $(P_{\text{moderate}}, e_{\text{cautious}})$ | 0.5612 | 0.7200 |
| **Ranges** | **[0.2100, 0.6573]** | **[0.1417, 0.7200]** |

Bet II's outcome set is dramatically spread out on *both* objectives. Payoff ranges from 0.21 to 0.66 (a band of 0.45), and knowability ranges from 0.14 to 0.72 (a band of 0.58). Both the credal set and the evaluator set contribute to this spread.

**$Y(\text{Bet III})$ -- Red+Yellow (ambiguous):**

| $(P, e)$ pair | Payoff | Knowability |
|---------------|--------|-------------|
| $(P_{\text{uniform}}, e_{\text{neutral}})$ | 0.6667 | 0.4286 |
| $(P_{\text{uniform}}, e_{\text{cautious}})$ | 0.8044 | 0.4286 |
| $(P_{\text{extreme}}, e_{\text{neutral}})$ | 0.6667 | 0.1417 |
| $(P_{\text{extreme}}, e_{\text{cautious}})$ | 0.7939 | 0.1417 |
| $(P_{\text{black}}, e_{\text{neutral}})$ | 0.5433 | 0.4700 |
| $(P_{\text{black}}, e_{\text{cautious}})$ | 0.7286 | 0.4700 |
| $(P_{\text{yellow}}, e_{\text{neutral}})$ | 0.7900 | 0.4700 |
| $(P_{\text{yellow}}, e_{\text{cautious}})$ | 0.8832 | 0.4700 |
| $(P_{\text{moderate}}, e_{\text{neutral}})$ | 0.6667 | 0.7200 |
| $(P_{\text{moderate}}, e_{\text{cautious}})$ | 0.8124 | 0.7200 |
| **Ranges** | **[0.5433, 0.8832]** | **[0.1417, 0.7200]** |

Bet III mirrors Bet II's pattern: large spread on both objectives. Payoff ranges from 0.54 to 0.88 (band of 0.34), and knowability has the same range as Bet II (0.14 to 0.72), since both bets share the same source of uncertainty.

**$Y(\text{Bet IV})$ -- Black+Yellow (known 2/3):**

| $(P, e)$ pair | Payoff | Knowability |
|---------------|--------|-------------|
| $(P_{\text{uniform}}, e_{\text{neutral}})$ | 0.6667 | 1.0000 |
| $(P_{\text{uniform}}, e_{\text{cautious}})$ | 0.8165 | 1.0000 |
| $(P_{\text{extreme}}, e_{\text{neutral}})$ | 0.6667 | 1.0000 |
| $(P_{\text{extreme}}, e_{\text{cautious}})$ | 0.8165 | 1.0000 |
| $(P_{\text{black}}, e_{\text{neutral}})$ | 0.6667 | 1.0000 |
| $(P_{\text{black}}, e_{\text{cautious}})$ | 0.8165 | 1.0000 |
| $(P_{\text{yellow}}, e_{\text{neutral}})$ | 0.6667 | 1.0000 |
| $(P_{\text{yellow}}, e_{\text{cautious}})$ | 0.8165 | 1.0000 |
| $(P_{\text{moderate}}, e_{\text{neutral}})$ | 0.6667 | 1.0000 |
| $(P_{\text{moderate}}, e_{\text{cautious}})$ | 0.8165 | 1.0000 |
| **Ranges** | **[0.6667, 0.8165]** | **[1.0000, 1.0000]** |

Like Bet I, Bet IV's outcome set collapses to just two distinct points. Knowability is identically 1.0. The credal set does nothing.

### 2.3 The Key Geometric Observation

Summarizing the spreads:

| Bet | Payoff spread | Knowability spread | Geometry |
|-----|---------------|--------------------|----------|
| Bet I (Red) | 0.2440 | 0.0000 | **Tight line segment** |
| Bet II (Black) | 0.4473 | 0.5783 | **Spread-out cloud** |
| Bet III (R+Y) | 0.3398 | 0.5783 | **Spread-out cloud** |
| Bet IV (B+Y) | 0.1498 | 0.0000 | **Tight line segment** |

Known-probability bets (I and IV) have *zero* knowability spread and small payoff spread (arising only from the evaluator difference). Their outcome sets are compact line segments pinned to knowability $= 1.0$. Ambiguous bets (II and III) have large spread on *both* dimensions -- a diffuse cloud in outcome space, pulled in different directions by different priors and evaluators.

This geometric distinction is the engine of the resolution. When MOADT checks whether one action robustly dominates another, it must verify that *every* vector in the dominated set is Pareto-beaten by *some* vector in the dominating set. Spread-out clouds are harder to dominate (they have extreme vectors in many directions) but also harder to dominate *with* (some of their vectors may be weak). Compact sets are easy to characterize: if their two points are strong, the whole set is strong.

---

## 3. Robust Dominance and the Admissible Set

### 3.1 Checking Robust Dominance

Recall: $a \succ_R b$ iff $\forall \vec{y}_b \in Y(b),\; \exists \vec{y}_a \in Y(a)$ such that $\vec{y}_a \succ_P \vec{y}_b$ (Pareto-dominates componentwise).

Checking all 12 ordered pairs among the 4 bets, three robust dominance relations hold:

$$\text{Bet III} \succ_R \text{Bet II}$$
$$\text{Bet IV} \succ_R \text{Bet I}$$
$$\text{Bet IV} \succ_R \text{Bet II}$$

### 3.2 Why These Relations Hold

**Bet IV $\succ_R$ Bet I:** Every vector in $Y(\text{Bet I})$ has the form $(p, 1.0)$ with $p \in \{0.3333, 0.5774\}$. Every vector in $Y(\text{Bet IV})$ has the form $(q, 1.0)$ with $q \in \{0.6667, 0.8165\}$. Since $0.6667 > 0.5774 > 0.3333$ and knowability is tied at 1.0, the worst Bet IV vector $(0.6667, 1.0)$ already Pareto-dominates the best Bet I vector $(0.5774, 1.0)$. Robust dominance is clear: Bet IV simply pays more with the same perfect knowability.

**Bet III $\succ_R$ Bet II:** Both are ambiguous bets with spread-out outcome sets. But Bet III's payoff range ([0.5433, 0.8832]) is strictly above Bet II's range ([0.2100, 0.6573]), and their knowability ranges are identical ([0.1417, 0.7200]). For each vector in $Y(\text{Bet II})$, the corresponding vector in $Y(\text{Bet III})$ -- computed under the same $(P, e)$ pair -- has weakly higher knowability (equal, in fact) and strictly higher payoff. This makes sense: Bet III wins on Red *or* Yellow, while Bet II wins on Black alone, and $P(\text{Red} + \text{Yellow}) = 1 - P(\text{Black}/90 \cdot 90) + 30/90$ is always at least as large as $P(\text{Black})$.

**Bet IV $\succ_R$ Bet II:** Bet IV has minimum payoff 0.6667 with knowability 1.0. Bet II's best vector is $(0.6573, 0.7200)$. Since $0.6667 > 0.6573$ and $1.0 > 0.7200$, even Bet IV's worst vector dominates Bet II's best vector.

### 3.3 Why Other Relations Fail

**Bet I $\not\succ_R$ Bet II:** Under $P_{\text{black}}$ with $e_{\text{cautious}}$, Bet II achieves payoff 0.6573, which exceeds Bet I's best payoff of 0.5774. No vector in $Y(\text{Bet I})$ can match Bet II on the payoff dimension in this scenario, even though Bet I dominates on knowability.

**Bet IV $\not\succ_R$ Bet III:** Under $P_{\text{yellow}}$ with $e_{\text{cautious}}$, Bet III achieves payoff 0.8832, which exceeds Bet IV's best payoff of 0.8165. Bet IV cannot Pareto-dominate this vector despite its perfect knowability.

### 3.4 The Admissible Set

$$\text{Adm}(A) = \{\text{Bet III (Red+Yellow)},\; \text{Bet IV (Black+Yellow)}\}$$

Bets I and II are eliminated. Bet I is robustly dominated by Bet IV (same knowability, strictly better payoff). Bet II is robustly dominated by both Bet III and Bet IV.

---

## 4. The Choice Protocol

### Layer 1: Constraints

**Constraint:** None. This is a pure preference problem -- all bets are available.

| Bet | Result |
|-----|--------|
| Bet I (Red) | **PASS** |
| Bet II (Black) | **PASS** |
| Bet III (Red+Yellow) | **PASS** |
| Bet IV (Black+Yellow) | **PASS** |

$$C = \{\text{Bet I},\; \text{Bet II},\; \text{Bet III},\; \text{Bet IV}\}$$

$$F = \text{Adm}(C) = \{\text{Bet III},\; \text{Bet IV}\}$$

All four bets pass the (vacuous) constraint check, but admissibility within the constraint-satisfying set eliminates Bets I and II, exactly as in the full admissible set.

### Layer 2: Reference-Point Satisficing

**Reference point:** $\vec{r} = (0.25, 0.50)$.

**Robust satisficing:** An action passes Layer 2 iff *every* vector in $Y(a)$ meets or exceeds $\vec{r}$ componentwise. The agent must be confident it meets aspirations under all plausible models.

| Bet | Worst payoff | Worst knowability | Result |
|-----|-------------|-------------------|--------|
| Bet III (Red+Yellow) | 0.5433 $\geq$ 0.25 | 0.1417 $<$ 0.50 | **FAIL** |
| Bet IV (Black+Yellow) | 0.6667 $\geq$ 0.25 | 1.0000 $\geq$ 0.50 | **PASS** |

Bet III fails because under the extreme prior ($P_{\text{extreme}}$), its expected knowability drops to 0.1417 -- well below the 0.50 aspiration. The extreme prior concentrates weight on the states $s_{0B/60Y}$ and $s_{60B/0Y}$ where knowability is zero, dragging the expected value down. Bet IV, with its constant knowability of 1.0, passes trivially.

$$\text{Sat}(F, \vec{r}) = \{\text{Bet IV}\}$$

### Layer 3: Regret-Pareto

With only one action surviving, regret computation is straightforward:

$$\vec{\rho}(\text{Bet IV}) = (0, 0)$$

There is no other action in the satisficing set against which Bet IV could accumulate regret.

$$R = \{\text{Bet IV}\}$$

### Layer 4: Deference

$|R| = 1$ -- the protocol terminates with a **unique recommendation: Bet IV (Black+Yellow)**.

No deference to the principal is needed. The protocol has resolved the decision fully.

---

## 5. The Two-Choice Framing

The Ellsberg Paradox is traditionally presented as *two separate binary choices*. This framing is essential because the paradox lies in the *pattern* across both choices. Let us run MOADT on each choice independently.

### 5.1 Choice A: Bet I (Red) vs. Bet II (Black)

**Outcome sets** (from Section 2):

- $Y(\text{Bet I})$: payoff in $[0.3333, 0.5774]$, knowability $= 1.0$
- $Y(\text{Bet II})$: payoff in $[0.2100, 0.6573]$, knowability in $[0.1417, 0.7200]$

**Robust dominance:** Neither bet robustly dominates the other. Bet I cannot dominate Bet II because Bet II achieves payoff 0.6573 under $P_{\text{black}}/e_{\text{cautious}}$, exceeding Bet I's maximum of 0.5774. Bet II cannot dominate Bet I because Bet I's knowability is always 1.0, far above Bet II's maximum of 0.72.

$$\text{Adm}(\{I, II\}) = \{\text{Bet I},\; \text{Bet II}\}$$

**Layer 1:** Both pass (no constraints). $F = \{\text{Bet I},\; \text{Bet II}\}$.

**Layer 2:** Reference point $\vec{r} = (0.25, 0.50)$.

| Bet | Worst payoff | Worst knowability | Result |
|-----|-------------|-------------------|--------|
| Bet I | 0.3333 $\geq$ 0.25 | 1.0000 $\geq$ 0.50 | **PASS** |
| Bet II | 0.2100 $<$ 0.25 | 0.1417 $<$ 0.50 | **FAIL** |

Bet II fails on *both* dimensions. Under $P_{\text{yellow}}/e_{\text{neutral}}$, its expected payoff drops to 0.21 (below 0.25), and under $P_{\text{extreme}}$, its knowability drops to 0.14 (far below 0.50).

$$\text{Sat} = \{\text{Bet I}\}$$

**Layer 3:** $\vec{\rho}(\text{Bet I}) = (0, 0)$.

**Layer 4:** Unique recommendation -- **Bet I (Red)**.

### 5.2 Choice B: Bet III (Red+Yellow) vs. Bet IV (Black+Yellow)

**Outcome sets** (from Section 2):

- $Y(\text{Bet III})$: payoff in $[0.5433, 0.8832]$, knowability in $[0.1417, 0.7200]$
- $Y(\text{Bet IV})$: payoff in $[0.6667, 0.8165]$, knowability $= 1.0$

**Robust dominance:** Neither bet robustly dominates the other. Bet IV cannot dominate Bet III because Bet III achieves payoff 0.8832 under $P_{\text{yellow}}/e_{\text{cautious}}$, exceeding Bet IV's maximum of 0.8165. Bet III cannot dominate Bet IV because Bet IV's knowability is always 1.0.

$$\text{Adm}(\{III, IV\}) = \{\text{Bet III},\; \text{Bet IV}\}$$

**Layer 1:** Both pass. $F = \{\text{Bet III},\; \text{Bet IV}\}$.

**Layer 2:** Reference point $\vec{r} = (0.25, 0.50)$.

| Bet | Worst payoff | Worst knowability | Result |
|-----|-------------|-------------------|--------|
| Bet III | 0.5433 $\geq$ 0.25 | 0.1417 $<$ 0.50 | **FAIL** |
| Bet IV | 0.6667 $\geq$ 0.25 | 1.0000 $\geq$ 0.50 | **PASS** |

Bet III fails on knowability for the same reason as before: the extreme prior drives expected knowability below the aspiration threshold.

$$\text{Sat} = \{\text{Bet IV}\}$$

**Layer 3:** $\vec{\rho}(\text{Bet IV}) = (0, 0)$.

**Layer 4:** Unique recommendation -- **Bet IV (Black+Yellow)**.

### 5.3 The Ellsberg Pattern Emerges

| Choice | MOADT recommends | Ellsberg prediction | Match? |
|--------|------------------|---------------------|--------|
| A: Bet I vs. Bet II | **Bet I** (known 1/3) | Bet I | Yes |
| B: Bet III vs. Bet IV | **Bet IV** (known 2/3) | Bet IV | Yes |

MOADT reproduces the classic Ellsberg preferences: prefer the known-probability bet in both choices. This is not a coincidence or a parameter-fitting exercise. It emerges from the geometry of outcome sets under credal uncertainty and the structural role of the knowability objective.

---

## 6. What Scalar Expected Utility Would Have Done

### 6.1 The Impossibility Under EU

Under scalar EU, the agent holds a single prior $P$ and computes $\mathbb{E}_P[\text{payoff}]$ for each bet. Here is the ranking under each of the 5 priors with the neutral evaluator, using payoff-only weights $(1.0, 0.0)$:

| Prior | Bet I | Bet II | Bet III | Bet IV | Pattern |
|-------|-------|--------|---------|--------|---------|
| $P_{\text{uniform}}$ | 0.3333 | 0.3333 | 0.6667 | 0.6667 | I $=$ II, III $=$ IV |
| $P_{\text{extreme}}$ | 0.3333 | 0.3333 | 0.6667 | 0.6667 | I $=$ II, III $=$ IV |
| $P_{\text{black}}$ | 0.3333 | 0.4567 | 0.5433 | 0.6667 | II $>$ I, IV $>$ III |
| $P_{\text{yellow}}$ | 0.3333 | 0.2100 | 0.7900 | 0.6667 | I $>$ II, III $>$ IV |
| $P_{\text{moderate}}$ | 0.3333 | 0.3333 | 0.6667 | 0.6667 | I $=$ II, III $=$ IV |

The critical row is $P_{\text{yellow}}$: it gives I $>$ II, but it *also* gives III $>$ IV. The critical row $P_{\text{black}}$ gives IV $>$ III, but it *also* gives II $>$ I. No single prior produces the Ellsberg pattern (I $>$ II **and** IV $>$ III). This is precisely the EU impossibility:

$$\forall P: \quad \mathbb{E}_P[\text{I}] + \mathbb{E}_P[\text{IV}] = \mathbb{E}_P[\text{II}] + \mathbb{E}_P[\text{III}] = 1.0$$

If you gain by choosing the known bet in one choice, you lose by choosing the known bet in the other. Under a single prior and a single objective, the Ellsberg pattern is a logical impossibility.

### 6.2 Adding Weights Does Not Help

With equal weights $(0.5, 0.5)$ that include knowability:

| Prior | Evaluator | Ranking (best to worst) |
|-------|-----------|-------------------------|
| $P_{\text{uniform}}$ | $e_{\text{neutral}}$ | IV (0.8333), I (0.6667), III (0.5476), II (0.3810) |
| $P_{\text{black}}$ | $e_{\text{neutral}}$ | IV (0.8333), I (0.6667), III (0.5067), II (0.4633) |
| $P_{\text{yellow}}$ | $e_{\text{neutral}}$ | IV (0.8333), I (0.6667), III (0.6300), II (0.3400) |
| $P_{\text{moderate}}$ | $e_{\text{neutral}}$ | IV (0.8333), III (0.6933), I (0.6667), II (0.5267) |

Under equal weights, IV always beats III and I always beats II (except under $P_{\text{moderate}}$ where III edges past I). But this is a scalar collapse -- it hides the structure of the tradeoff behind a specific weighting. Under knowability-heavy weights $(0.3, 0.7)$, the Ellsberg pattern holds even more strongly across all priors, but this requires *choosing* the weights in advance. MOADT avoids this by treating the objectives as incommensurable.

---

## 7. Single-Objective Variant: Why Ambiguity Aversion Is Genuinely Multi-Objective

This section provides the most important diagnostic in the entire analysis. We strip away the knowability objective and run MOADT with payoff as the *only* objective, retaining the full credal set and evaluator set. If the Ellsberg pattern survives, then ambiguity aversion can be explained by risk preferences alone. If it reverses, then ambiguity aversion is genuinely multi-objective.

### 7.1 Single-Objective Outcome Sets

With $k = 1$ (monetary payoff only), each $Y(a)$ is a set of 10 scalar values:

| $(P, e)$ pair | Bet I | Bet II | Bet III | Bet IV |
|---------------|-------|--------|---------|--------|
| $(P_{\text{uniform}}, e_{\text{neutral}})$ | 0.3333 | 0.3333 | 0.6667 | 0.6667 |
| $(P_{\text{uniform}}, e_{\text{cautious}})$ | 0.5774 | 0.5158 | 0.8044 | 0.8165 |
| $(P_{\text{extreme}}, e_{\text{neutral}})$ | 0.3333 | 0.3333 | 0.6667 | 0.6667 |
| $(P_{\text{extreme}}, e_{\text{cautious}})$ | 0.5774 | 0.4451 | 0.7939 | 0.8165 |
| $(P_{\text{black}}, e_{\text{neutral}})$ | 0.3333 | 0.4567 | 0.5433 | 0.6667 |
| $(P_{\text{black}}, e_{\text{cautious}})$ | 0.5774 | 0.6573 | 0.7286 | 0.8165 |
| $(P_{\text{yellow}}, e_{\text{neutral}})$ | 0.3333 | 0.2100 | 0.7900 | 0.6667 |
| $(P_{\text{yellow}}, e_{\text{cautious}})$ | 0.5774 | 0.3947 | 0.8832 | 0.8165 |
| $(P_{\text{moderate}}, e_{\text{neutral}})$ | 0.3333 | 0.3333 | 0.6667 | 0.6667 |
| $(P_{\text{moderate}}, e_{\text{cautious}})$ | 0.5774 | 0.5612 | 0.8124 | 0.8165 |

### 7.2 Robust Dominance Reversal

With payoff as the only objective, robust dominance in one dimension reduces to comparing the ranges $[\min Y(a), \max Y(a)]$. The results:

$$\text{Bet II} \succ_R \text{Bet I} \qquad \text{Bet III} \succ_R \text{Bet IV}$$

and additionally:

$$\text{Bet III} \succ_R \text{Bet I}, \quad \text{Bet III} \succ_R \text{Bet II}, \quad \text{Bet IV} \succ_R \text{Bet I}, \quad \text{Bet IV} \succ_R \text{Bet II}$$

The admissible set is:

$$\text{Adm}(A) = \{\text{Bet III}\}$$

### 7.3 The Single-Objective Pairwise Results

| Choice | Single-objective MOADT recommends | Ellsberg prediction | Match? |
|--------|-----------------------------------|---------------------|--------|
| A: I vs. II | **Bet II** (ambiguous!) | Bet I | **No -- reversed** |
| B: III vs. IV | **Bet III** (ambiguous!) | Bet IV | **No -- reversed** |

The Ellsberg pattern is completely reversed. With payoff as the only objective, MOADT *favors* the ambiguous bets.

### 7.4 Why the Reversal Happens

The reversal is driven by the cautious ($\sqrt{\cdot}$) evaluator and Jensen's inequality. For a concave function $g$ and a random variable $X$:

$$\mathbb{E}[g(X)] \leq g(\mathbb{E}[X])$$

But the evaluator is applied *before* taking the expectation over states. The ambiguous bets have win probabilities that vary across states. In the states where they win with high probability, the square root compresses the advantage less than proportionally; in the states where they win with low probability, the square root *boosts* the value more than proportionally. The net effect is that the cautious evaluator gives *higher* expected values to the variable (ambiguous) bets than to the constant (known) bets.

Combined with the credal set (which includes $P_{\text{black}}$, under which Bet II has high expected payoff), this means the ambiguous bets can robustly dominate the known bets when payoff is the only objective.

### 7.5 The Core Lesson

This is the single most important finding: **risk aversion (the shape of $u(x)$) does not explain ambiguity aversion. In fact, it reverses it.**

The $\sqrt{\cdot}$ evaluator is the standard model of risk aversion -- a concave utility function. If ambiguity aversion were merely extreme risk aversion, then the cautious evaluator should strengthen the Ellsberg pattern. Instead, it destroys it. The conclusion is inescapable: ambiguity aversion is about something *different* from the curvature of the utility function. It is about the distinct value of knowing your odds -- a separate objective that cannot be captured by any scalar utility function, however cleverly shaped.

With two objectives (payoff + knowability), MOADT recommends I over II and IV over III -- the classic Ellsberg pattern. With one objective (payoff only), MOADT recommends the opposite. The contrast proves that the Ellsberg pattern is *genuinely multi-objective*.

---

## 8. How MOADT Resolves the Paradox

The resolution has three structural components, each corresponding to an axiom that EU theory assumes and MOADT relaxes.

### 8.1 Credal Sets Instead of a Single Prior

EU theory requires a single subjective probability distribution. Under $P_{\text{yellow}}$, $E[\text{Bet I}] > E[\text{Bet II}]$. Under $P_{\text{black}}$, $E[\text{Bet IV}] > E[\text{Bet III}]$. These are *different* priors. EU demands you pick one; MOADT maintains both. The credal set $\mathcal{P} = \{P_{\text{uniform}}, P_{\text{extreme}}, P_{\text{black}}, P_{\text{yellow}}, P_{\text{moderate}}\}$ acknowledges genuine Knightian uncertainty about the urn composition.

### 8.2 Multiple Objectives Instead of a Single Scalar

The knowability objective captures what EU theory cannot represent: the irreducible value of *knowing* your probability. This is not risk aversion. Risk aversion is about preferring a sure \$50 to a 50/50 gamble for \$100 -- it is about the *shape* of $u(x)$. Ambiguity aversion is about preferring a gamble where you *know* it is 50/50 to a gamble where it might be 50/50 or might be 0/100. MOADT models this as a distinct objective, not a parameter of the utility function.

### 8.3 Evaluator Sets Instead of a Single Evaluation Function

The evaluator set $\mathcal{F} = \{e_{\text{neutral}}, e_{\text{cautious}}\}$ acknowledges that even "monetary payoff" might be assessed differently. The Section 7 analysis shows that the evaluator choice interacts with ambiguity in surprising ways: the cautious evaluator actually *favors* ambiguous bets on the payoff dimension. This interaction is invisible under scalar EU.

### 8.4 The Geometric Mechanism

Together, these components produce outcome sets with a characteristic geometry:

| Bet | Payoff spread | Knowability spread | Outcome set shape |
|-----|---------------|--------------------|-------------------|
| Bet I (Red, known) | 0.2440 | 0.0000 | Compact segment at knowability $= 1.0$ |
| Bet II (Black, ambiguous) | 0.4473 | 0.5783 | Diffuse cloud, low knowability |
| Bet III (R+Y, ambiguous) | 0.3398 | 0.5783 | Diffuse cloud, low knowability |
| Bet IV (B+Y, known) | 0.1498 | 0.0000 | Compact segment at knowability $= 1.0$ |

Known-probability bets have outcome sets that are *compact and elevated* on the knowability dimension. Ambiguous bets have outcome sets that are *spread out and depressed* on knowability. When the reference point demands at least moderate knowability (0.50), the ambiguous bets fail because their worst-case knowability falls far below the threshold. The known-probability bets pass effortlessly. This is not a trick of parameter choice -- it is a structural consequence of the relationship between Knightian uncertainty and the value of information.

---

## 9. Summary of Protocol Execution

```
Input: 4 actions x 7 states x 2 objectives x 5 priors x 2 evaluators

Full problem (all 4 bets):
  Robust Dominance:      III ≻_R II, IV ≻_R I, IV ≻_R II
                         Adm(A) = {Bet III, Bet IV}

  Layer 1 (Constraints):  No constraints (pure preference problem)
                         C = {Bet I, Bet II, Bet III, Bet IV}
                         F = Adm(C) = {Bet III, Bet IV}

  Layer 2 (Satisficing):  r = (0.25, 0.50)
                         Bet III FAIL (knowability 0.1417 under P_extreme)
                         Sat = {Bet IV}

  Layer 3 (Regret):       rho(Bet IV) = (0, 0)
                         R = {Bet IV}

  Layer 4 (Deference):    |R| = 1 --> unique recommendation: Bet IV

Pairwise (Choice A: Bet I vs. Bet II):
  Adm = {Bet I, Bet II}
  Satisficing: Bet II FAIL (payoff 0.21, knowability 0.14)
  MOADT recommends: Bet I (Red)

Pairwise (Choice B: Bet III vs. Bet IV):
  Adm = {Bet III, Bet IV}
  Satisficing: Bet III FAIL (knowability 0.14)
  MOADT recommends: Bet IV (Black+Yellow)

Single-objective variant (payoff only):
  Adm = {Bet III} -- ambiguous bet wins!
  Choice A: Bet II > Bet I -- REVERSED
  Choice B: Bet III > Bet IV -- REVERSED
  Risk aversion does not explain Ellsberg; it reverses it.
```

---

## 10. What This Example Demonstrates

1. **"Ambiguity aversion" is rational multi-objective decision-making.** The Ellsberg Paradox is not a paradox under MOADT. It arises because EU theory insists on a single prior, a single scalar value function, and a single evaluation function. Relax any of these, and the preference for known-probability bets emerges naturally from the structure of outcome sets under credal uncertainty.

2. **The knowability objective is irreducible.** Section 7 proves that removing the knowability objective *reverses* the Ellsberg pattern. The preference for known probabilities cannot be captured by any concave utility function -- it requires a distinct objective. This is not a modeling convenience; it is a structural necessity.

3. **Credal sets and evaluator sets interact nontrivially.** The cautious evaluator favors ambiguous bets on the payoff dimension (via Jensen's inequality), while the credal set generates the spread that makes ambiguous bets vulnerable on knowability. Neither mechanism alone produces the Ellsberg pattern. Their interaction through MOADT's multi-objective outcome sets is what resolves the paradox.

4. **MOADT needs no "ambiguity aversion parameter."** Unlike Maxmin EU, $\alpha$-MEU, smooth ambiguity models, or variational preferences, MOADT does not introduce a special parameter to capture ambiguity aversion. The phenomenon emerges from the standard MOADT machinery: credal sets, evaluator sets, multiple objectives, and the robust dominance / satisficing protocol. No new axioms are needed.

5. **The protocol terminates with a definite recommendation.** In the full 4-bet problem, MOADT uniquely recommends Bet IV. In each pairwise choice, MOADT uniquely recommends the known-probability bet. There is no deference needed -- the structural advantage of known-probability bets is decisive at Layer 2. The theory resolves the paradox completely, without passing the decision back to the principal.

---

## Appendix: Computational Verification

All numerical results in this document were produced by `examples/classic_ellsberg.py` using the MOADT engine (`moadt/_engine.py`). The code is available in the repository and can be run independently to verify every number.

The knowability function used is:

$$\text{knowability}(a, s) = \begin{cases} 1.0 & \text{if bet } a \text{ has a state-independent win probability} \\ 1 - \frac{|b - 30|}{30} & \text{otherwise, where } b = \text{number of black balls in state } s \end{cases}$$

The cautious evaluator applies $\sqrt{\cdot}$ to the monetary payoff only; knowability is passed through unchanged.

---

## References

- MOADT (Multi-Objective Admissible Decision Theory) is defined in the companion paper.
- Ellsberg, D. (1961). Risk, ambiguity, and the Savage axioms. *Quarterly Journal of Economics*, 75(4), 643--669.
- Savage, L. J. (1954). *The Foundations of Statistics*. Wiley.
- Gilboa, I., & Schmeidler, D. (1989). Maxmin expected utility with non-unique prior. *Journal of Mathematical Economics*, 18(2), 141--153. The maxmin EU model that first formalized multiple priors.
- Klibanoff, P., Marinacci, M., & Mukerji, S. (2005). A smooth model of decision making under ambiguity. *Econometrica*, 73(6), 1849--1892. The smooth ambiguity model, which introduces a separate ambiguity aversion parameter -- precisely what MOADT avoids.
- Knight, F. H. (1921). *Risk, Uncertainty, and Profit*. Houghton Mifflin. The original distinction between risk (known odds) and uncertainty (unknown odds) that the knowability objective formalizes.
- Wierzbicki, A. P. (1980). The use of reference objectives in multiobjective optimization. The achievement scalarizing function used in the Layer 2 fallback.
