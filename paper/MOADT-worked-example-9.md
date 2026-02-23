# MOADT Worked Example 9: The St. Petersburg Paradox

*A concrete walkthrough of Multi-Objective Admissible Decision Theory applied to infinite expected value*

---

## Overview

The St. Petersburg Paradox (Bernoulli, 1738) is perhaps the oldest and most fundamental paradox in decision theory. A fair coin is flipped repeatedly until tails appears; if tails first appears on flip $n$, the player wins $2^n$ dollars. The expected value of the game is infinite:

$$E[\text{winnings}] = \sum_{n=1}^{\infty} \frac{1}{2^n} \cdot 2^n = \sum_{n=1}^{\infty} 1 = \infty$$

Standard expected utility theory therefore says a risk-neutral agent should pay *any* finite amount to play. Yet no rational human would pay more than roughly \$20--25. This gap between theory and intuition has generated nearly three centuries of proposed resolutions -- diminishing marginal utility, bounded utility functions, finite wealth constraints, risk aversion, prospect theory -- each picking a single mechanism and building it into the utility function.

This document applies MOADT to the St. Petersburg Paradox and shows that the paradox dissolves not through any single mechanism but through *structural pluralism*: the interaction of multiple objectives, multiple priors, multiple evaluators, and a layered protocol that filters sequentially. Every computation is shown explicitly. The key finding: MOADT caps the acceptable entry fee at \$22, matching human intuition of \$20--25. All numerical results were produced by `examples/classic_stpetersburg.py` using the MOADT engine.

---

## 1. The Scenario

### 1.1 The St. Petersburg Game

A casino offers the following game:

1. A fair coin is flipped repeatedly until tails appears.
2. If tails first appears on flip $n$, you win $\$2^n$.
3. You must pay an entry fee $F$ to play.

The expected winnings are infinite: each flip contributes exactly \$1 to the expected value (probability $1/2^n$ times payoff $2^n = 1$), and there are infinitely many flips. Expected utility theory says: pay any finite fee. Humans say: about \$20--25 at most.

### 1.2 Truncated Model

We truncate at $N = 20$ flips, with the final state $s_{20}$ absorbing all remaining probability mass. This gives:

- Maximum payoff: $2^{20} = \$1{,}048{,}576$
- Truncated EV (fair coin): \$21.00
- Truncated EV (biased coin, $P_{\text{tails}} = 0.55$): \$9.78

Even truncated, EU theory says pay up to \$21. The paradox remains: a risk-neutral agent should pay \$20 for a game where 75% of the time it wins \$2 or \$4.

### 1.3 MOADT Formulation

For each entry fee $F$, we formulate a separate binary MOADT problem:

| Component | Specification |
|-----------|---------------|
| **Actions** | $\{$Play, Dont\_Play$\}$ |
| **States** | 20 coin outcome states: $s_n$ = "first tails on flip $n$" |
| **Objectives** ($k = 3$) | (1) Expected net monetary value, (2) Probability of net gain, (3) Downside exposure |
| **Evaluators** ($|\mathcal{F}| = 2$) | Risk-neutral, Risk-aware (log compression) |
| **Credal set** ($|\mathcal{P}| = 2$) | Fair coin, Biased coin ($P_{\text{tails}} = 0.55$) |
| **Constraint** (Layer 1) | Worst-case loss $\leq \$20$ in any state |
| **Reference point** (Layer 2) | EV $\geq \$1$, $P(\text{gain}) \geq 10\%$, worst case $\geq -\$5$ |

We sweep over 21 fee levels from \$1 to \$1,000 and find the *crossover point* -- the maximum fee at which MOADT still recommends playing.

### 1.4 Why Three Objectives?

The three objectives are genuinely independent and capture orthogonal dimensions of value:

- **Objective 1 (Expected net value):** Favors playing -- the expected payoff exceeds the fee up to $F = \$21$ (truncated) or always (untruncated). This is the dimension that creates the paradox in scalar EU.
- **Objective 2 (Probability of net gain):** Penalizes playing at high fees. At $F = \$15$, you have only a 12.5% chance of coming out ahead. At $F = \$50$, only 3.1%.
- **Objective 3 (Downside exposure):** Measures expected loss magnitude. Per-state values are capped at the baseline (the \$0-net-payoff level), so winning states contribute no upside information — only losing states differentiate actions. The expected downside drops below baseline as soon as any state produces a loss (fee $> \$2$), and worsens monotonically with fee as losses grow larger and more frequent. This is genuinely independent of objective 1 (which captures both upside and downside) and objective 2 (which captures only the probability, not the magnitude, of outcomes). The Layer 1 *constraint* on this objective enforces a hard per-state floor on worst-case loss; the *objective value* captures how badly the expectation is dragged down by losing states.

In scalar EU, objective 1 drowns out objectives 2 and 3. In MOADT, all three are maintained as separate dimensions, preserving the tension that the paradox exploits.

### 1.5 Evaluators and Priors

**Evaluators:**

- $\vec{f}_{\text{neutral}}$ (risk-neutral): Objective 1 uses normalized net payoffs in $[0, 1]$ across the range $[-998, 1{,}048{,}575]$. Objective 2 (probability of gain) is naturally in $[0, 1]$. Objective 3 uses the same normalization but capped at the baseline: $\min(\text{norm}(\text{net}), \text{baseline})$, so only losing states contribute below-baseline values.
- $\vec{f}_{\text{risk}}$ (risk-aware): Applies logarithmic compression to objective 1 on the upside, while preserving downside linearly. Objective 3 is un-compressed in both evaluators — losses are fully felt regardless of risk attitude. This is Bernoulli's original insight -- diminishing marginal value of money -- but as *one evaluator among several*, not the sole resolution.

The risk-aware evaluator uses $\text{log}(1 + 99x) / \text{log}(100)$ compression. At the baseline (\$0), both evaluators agree: $0.000951$. But they diverge for large gains: a \$1M payoff normalizes to $0.953719$ (risk-neutral) vs. $0.989815$ (risk-aware, compressed). The compression reduces the pull of extreme upside without eliminating it.

**Priors:**

- $P_{\text{fair}}$: Exact fair coin. $P(\text{first tails on flip } n) = (1/2)^n$.
- $P_{\text{biased}}$: Slightly pessimistic coin with $P(\text{tails}) = 0.55$. Long runs of heads (which produce the huge payoffs) are less likely.

---

## 2. Game Structure

The state table shows all 20 states with their probabilities and payoffs:

| State | $P(\text{fair})$ | $P(\text{biased})$ | Payoff | Cumulative $P(\text{fair})$ |
|-------|------------------|---------------------|--------|-----------------------------|
| $s_1$ | 0.50000000 | 0.55000000 | \$2 | 0.50000000 |
| $s_2$ | 0.25000000 | 0.24750000 | \$4 | 0.75000000 |
| $s_3$ | 0.12500000 | 0.11137500 | \$8 | 0.87500000 |
| $s_4$ | 0.06250000 | 0.05011875 | \$16 | 0.93750000 |
| $s_5$ | 0.03125000 | 0.02255344 | \$32 | 0.96875000 |
| $s_6$ | 0.01562500 | 0.01014905 | \$64 | 0.98437500 |
| $s_7$ | 0.00781250 | 0.00456707 | \$128 | 0.99218750 |
| $s_8$ | 0.00390625 | 0.00205518 | \$256 | 0.99609375 |
| $s_9$ | 0.00195312 | 0.00092483 | \$512 | 0.99804688 |
| $s_{10}$ | 0.00097656 | 0.00041617 | \$1,024 | 0.99902344 |
| $s_{11}$ | 0.00048828 | 0.00018728 | \$2,048 | 0.99951172 |
| $s_{12}$ | 0.00024414 | 0.00008428 | \$4,096 | 0.99975586 |
| $s_{13}$ | 0.00012207 | 0.00003792 | \$8,192 | 0.99987793 |
| $s_{14}$ | 0.00006104 | 0.00001707 | \$16,384 | 0.99993896 |
| $s_{15}$ | 0.00003052 | 0.00000768 | \$32,768 | 0.99996948 |
| $s_{16}$ | 0.00001526 | 0.00000346 | \$65,536 | 0.99998474 |
| $s_{17}$ | 0.00000763 | 0.00000156 | \$131,072 | 0.99999237 |
| $s_{18}$ | 0.00000381 | 0.00000070 | \$262,144 | 0.99999619 |
| $s_{19}$ | 0.00000191 | 0.00000031 | \$524,288 | 0.99999809 |
| $s_{20}$ [abs] | 0.00000191 | 0.00000026 | \$1,048,576 | 1.00000000 |

### Key Observation

**75% of the time, you win \$2 or \$4.** 93.75% of the time, you win \$16 or less. The huge payoffs (\$1M+) happen with probability less than 0.0001%. The entire expected value of the game is driven by astronomically improbable events. This is the structural feature that makes the paradox: expected value is dominated by tail events that a real decision-maker would never rely on.

The biased coin compresses these tails further. Under $P_{\text{biased}}$, the probability of reaching state $s_{20}$ drops from $0.00000191$ to $0.00000026$ -- a factor of 7 reduction. The truncated EV falls from \$21.00 to \$9.78.

---

## 3. Classical Expected Value Analysis

The following table shows the classical EU analysis for each fee level:

| Fee | $\text{EV}_{\text{fair}}$ | $\text{EV}_{\text{biased}}$ | Median | $P(\text{gain})_{\text{fair}}$ | Worst Case |
|-----|---------------------------|-----------------------------|--------|-------------------------------|------------|
| \$1 | +\$20.00 | +\$8.78 | +\$1 | 100.00% | +\$1 |
| \$2 | +\$19.00 | +\$7.78 | \$0 | 50.00% | \$0 |
| \$3 | +\$18.00 | +\$6.78 | $-$\$1 | 50.00% | $-$\$1 |
| \$4 | +\$17.00 | +\$5.78 | $-$\$2 | 25.00% | $-$\$2 |
| \$5 | +\$16.00 | +\$4.78 | $-$\$3 | 25.00% | $-$\$3 |
| \$8 | +\$13.00 | +\$1.78 | $-$\$6 | 12.50% | $-$\$6 |
| \$10 | +\$11.00 | $-$\$0.22 | $-$\$8 | 12.50% | $-$\$8 |
| \$12 | +\$9.00 | $-$\$2.22 | $-$\$10 | 12.50% | $-$\$10 |
| \$15 | +\$6.00 | $-$\$5.22 | $-$\$13 | 12.50% | $-$\$13 |
| \$18 | +\$3.00 | $-$\$8.22 | $-$\$16 | 6.25% | $-$\$16 |
| \$20 | +\$1.00 | $-$\$10.22 | $-$\$18 | 6.25% | $-$\$18 |
| \$22 | $-$\$1.00 | $-$\$12.22 | $-$\$20 | 6.25% | $-$\$20 |
| \$25 | $-$\$4.00 | $-$\$15.22 | $-$\$23 | 6.25% | $-$\$23 |
| \$30 | $-$\$9.00 | $-$\$20.22 | $-$\$28 | 6.25% | $-$\$28 |
| \$40 | $-$\$19.00 | $-$\$30.22 | $-$\$38 | 3.12% | $-$\$38 |
| \$50 | $-$\$29.00 | $-$\$40.22 | $-$\$48 | 3.12% | $-$\$48 |
| \$75 | $-$\$54.00 | $-$\$65.22 | $-$\$73 | 1.56% | $-$\$73 |
| \$100 | $-$\$79.00 | $-$\$90.22 | $-$\$98 | 1.56% | $-$\$98 |
| \$200 | $-$\$179.00 | $-$\$190.22 | $-$\$198 | 0.78% | $-$\$198 |
| \$500 | $-$\$479.00 | $-$\$490.22 | $-$\$498 | 0.39% | $-$\$498 |
| \$1,000 | $-$\$979.00 | $-$\$990.22 | $-$\$998 | 0.20% | $-$\$998 |

### The Paradox in Numbers

The absurdity of expected value maximization is starkest at moderate fees:

- **At fee = \$15:** EV = +\$6, but the median outcome is $-$\$13 and $P(\text{gain})$ is only 12.5%. You have a positive expected value but lose money 87.5% of the time.
- **At fee = \$25:** EV = $-$\$4 in the truncated game, but *infinite* in the untruncated game. EU theory says "play" even though you lose money 93.75% of the time.
- **At fee = \$100:** EV = $-$\$79, median = $-$\$98, $P(\text{gain})$ = 1.6%. Only in the untruncated game does EU still say "play."

Classical EU says: play at any fee $\leq \$21$ (truncated) or ANY fee (untruncated). This is the recommendation that nearly three centuries of decision theory have struggled to escape.

---

## 4. MOADT Analysis

For each fee level, the MOADT protocol runs on the binary decision $\{$Play, Dont\_Play$\}$ with 20 states, 3 objectives, 2 evaluators, and 2 priors. Each action's outcome set $Y(a)$ contains $|\mathcal{P}| \times |\mathcal{F}| = 4$ vectors in $\mathbb{R}^3$.

### Results Across All Fee Levels

| Fee | Adm($A$) | Constraints | $F = \text{Adm}(C)$ | Sat($F, \vec{r}$) | Final $R$ | Verdict |
|-----|----------|-------------|----------------------|---------------------|-----------|---------|
| \$1 | Play | all pass | Play | Play | Play | **PLAY** |
| \$2 | Play | all pass | Play | Play | Play | **PLAY** |
| \$3 | Play, Dont\_Play | all pass | Play, Dont\_Play | Play | Play | **PLAY** |
| \$4 | Play, Dont\_Play | all pass | Play, Dont\_Play | Play | Play | **PLAY** |
| \$5 | Play, Dont\_Play | all pass | Play, Dont\_Play | Play | Play | **PLAY** |
| \$8 | Play, Dont\_Play | all pass | Play, Dont\_Play | Play | Play | **PLAY** |
| \$10 | Play, Dont\_Play | all pass | Play, Dont\_Play | ASF $\to$ Play | Play | **PLAY** |
| \$12 | Play, Dont\_Play | all pass | Play, Dont\_Play | ASF $\to$ Play | Play | **PLAY** |
| \$15 | Play, Dont\_Play | all pass | Play, Dont\_Play | ASF $\to$ Play | Play | **PLAY** |
| \$18 | Play, Dont\_Play | all pass | Play, Dont\_Play | ASF $\to$ Play | Play | **PLAY** |
| \$20 | Play, Dont\_Play | all pass | Play, Dont\_Play | ASF $\to$ Play | Play | **PLAY** |
| \$22 | Play, Dont\_Play | all pass | Play, Dont\_Play | ASF $\to$ Play | Play | **PLAY** |
| \$25 | Play, Dont\_Play | Play fail | Dont\_Play | ASF $\to$ Dont\_Play | Dont\_Play | **DONT PLAY** |
| \$30 | Play, Dont\_Play | Play fail | Dont\_Play | ASF $\to$ Dont\_Play | Dont\_Play | **DONT PLAY** |
| \$40 | Play, Dont\_Play | Play fail | Dont\_Play | ASF $\to$ Dont\_Play | Dont\_Play | **DONT PLAY** |
| \$50 | Play, Dont\_Play | Play fail | Dont\_Play | ASF $\to$ Dont\_Play | Dont\_Play | **DONT PLAY** |
| \$75 | Play, Dont\_Play | Play fail | Dont\_Play | ASF $\to$ Dont\_Play | Dont\_Play | **DONT PLAY** |
| \$100 | Play, Dont\_Play | Play fail | Dont\_Play | ASF $\to$ Dont\_Play | Dont\_Play | **DONT PLAY** |
| \$200 | Play, Dont\_Play | Play fail | Dont\_Play | ASF $\to$ Dont\_Play | Dont\_Play | **DONT PLAY** |
| \$500 | Play, Dont\_Play | Play fail | Dont\_Play | ASF $\to$ Dont\_Play | Dont\_Play | **DONT PLAY** |
| \$1,000 | Play, Dont\_Play | Play fail | Dont\_Play | ASF $\to$ Dont\_Play | Dont\_Play | **DONT PLAY** |

### The Crossover

- **Last fee where MOADT says PLAY:** \$22
- **First fee where MOADT says DONT PLAY:** \$25
- **Classical EU says:** pay up to \$21 (truncated), infinity (untruncated)
- **Human intuition:** \$20--25

MOADT's maximum recommended fee of \$22 falls squarely within the range of human willingness-to-pay. At the sampled fee points, the crossover is clear: \$22 is a clear PLAY, \$25 is a clear DONT PLAY. (The exact crossover lies somewhere in the \$22--\$25 interval; finer fee sampling would locate it more precisely but would not change the qualitative conclusion.)

### Three Regimes

The table reveals three distinct regimes:

1. **Very low fees (\$1--\$2):** Play robustly dominates Dont\_Play. At these fees, no state produces a net loss (the minimum payoff is \$2), so Play matches Dont\_Play on downside (objective 3) while strictly beating it on expected value and P(gain). Satisficing passes directly.
2. **Low-to-moderate fees (\$3--\$8):** Robust dominance fails — the first-flip state ($\$2 - F < 0$) drags Play's expected downside below baseline, creating a genuine three-way tension among objectives. But satisficing still selects Play (all three objectives meet aspirations under the better prior-evaluator pairs).
3. **Moderate fees (\$10--\$22):** Both actions survive dominance. Satisficing fails (P(gain) drops below the 10\% aspiration), but the ASF fallback selects Play because its shortfall from aspirations is smaller than Dont\_Play's.
4. **High fees (\$25+):** Play violates the downside constraint (worst-case loss exceeds \$20). Only Dont\_Play survives Layer 1. The game is unambiguously not worth playing.

---

## 5. Detailed Traces

### 5.1 Fee = \$5 (Low Fee -- Satisficing Resolves)

**Outcome sets:**

| $(P, \vec{f})$ pair | $E[\text{net}]$ | $P(\text{gain})$ | Downside |
|----------------------|-----------------|-------------------|----------|
| **Y(Play):** | | | |
| $(P_{\text{fair}}, \vec{f}_{\text{neutral}})$ | 0.000966 | 0.250000 | 0.000949 |
| $(P_{\text{fair}}, \vec{f}_{\text{risk}})$ | 0.001176 | 0.250000 | 0.000949 |
| $(P_{\text{biased}}, \vec{f}_{\text{neutral}})$ | 0.000955 | 0.202500 | 0.000949 |
| $(P_{\text{biased}}, \vec{f}_{\text{risk}})$ | 0.001058 | 0.202500 | 0.000949 |
| **Y(Dont\_Play):** | | | |
| (all pairs) | 0.000951 | 0.000000 | 0.000951 |

**Protocol execution:**

```
Robust Dominance:   No robust dominance found.
                    Adm(A) = {Play, Dont_Play}

Layer 1 (Constraints): Both pass. C = {Play, Dont_Play}
                       F = Adm(C) = {Play, Dont_Play}

Layer 2 (Satisficing): Sat(F, r) = {Play}
                       Play meets all three aspirations.

Layer 3 (Regret):      rho(Play) = (0, 0, 0)
                       R = {Play}

Layer 4:               |R| = 1 -- unique recommendation: Play
```

At \$5, Play beats Dont\_Play on objectives 1 and 2 (higher EV and positive P(gain)), but Dont\_Play beats Play on objective 3 (downside): Play's expected downside is $0.000949$ (dragged below baseline by the 50% chance of losing \$3 on the first flip) while Dont\_Play's is $0.000951$ (baseline). This three-way tension -- Play wins on EV and P(gain), Dont\_Play wins on downside -- means neither robustly dominates the other. But satisficing resolves it: Play meets all three aspirations, so Layer 2 selects Play directly.

### 5.2 Fee = \$10 (Moderate Fee -- ASF Resolves)

**Outcome sets:**

| $(P, \vec{f})$ pair | $E[\text{net}]$ | $P(\text{gain})$ | Downside |
|----------------------|-----------------|-------------------|----------|
| **Y(Play):** | | | |
| $(P_{\text{fair}}, \vec{f}_{\text{neutral}})$ | 0.000961 | 0.125000 | 0.000945 |
| $(P_{\text{fair}}, \vec{f}_{\text{risk}})$ | 0.001151 | 0.125000 | 0.000945 |
| $(P_{\text{biased}}, \vec{f}_{\text{neutral}})$ | 0.000951 | 0.091125 | 0.000945 |
| $(P_{\text{biased}}, \vec{f}_{\text{risk}})$ | 0.001038 | 0.091125 | 0.000945 |
| **Y(Dont\_Play):** | | | |
| (all pairs) | 0.000951 | 0.000000 | 0.000951 |

**Protocol execution:**

```
Robust Dominance:   No robust dominance found.
                    Adm(A) = {Play, Dont_Play}

Layer 1 (Constraints): Both pass. C = {Play, Dont_Play}
                       F = Adm(C) = {Play, Dont_Play}

Layer 2 (Satisficing): Sat(F, r) = empty
                       Play fails the P(gain) >= 10% aspiration under biased prior
                       (P(gain) = 9.11% < 10%).
                       ASF fallback: ASF(Play) = -0.0089
                                     ASF(Dont_Play) = -0.1000
                       ASF selects Play (best available).

Layer 3:               Skipped (ASF already resolved).

Layer 4:               |R| = 1 -- unique recommendation: Play
```

At \$10, neither action robustly dominates — Play loses on downside (objective 3 at $0.000945$ vs. baseline $0.000951$) while winning on EV and P(gain). Play also *fails* the satisficing aspiration on P(gain): under the biased coin, only 9.11% of outcomes produce a net gain, falling below the 10% threshold. The ASF fallback activates, measuring shortfall from aspirations. Play's worst shortfall is $-0.0089$ (barely missing the P(gain) target), while Dont\_Play's is $-0.1000$ (missing the P(gain) target completely at 0%). Play wins the ASF comparison handily.

### 5.3 Fee = \$20 (Near the Crossover -- ASF Resolves)

**Outcome sets:**

| $(P, \vec{f})$ pair | $E[\text{net}]$ | $P(\text{gain})$ | Downside |
|----------------------|-----------------|-------------------|----------|
| **Y(Play):** | | | |
| $(P_{\text{fair}}, \vec{f}_{\text{neutral}})$ | 0.000952 | 0.062500 | 0.000937 |
| $(P_{\text{fair}}, \vec{f}_{\text{risk}})$ | 0.001123 | 0.062500 | 0.000937 |
| $(P_{\text{biased}}, \vec{f}_{\text{neutral}})$ | 0.000941 | 0.041006 | 0.000936 |
| $(P_{\text{biased}}, \vec{f}_{\text{risk}})$ | 0.001015 | 0.041006 | 0.000936 |
| **Y(Dont\_Play):** | | | |
| (all pairs) | 0.000951 | 0.000000 | 0.000951 |

**Protocol execution:**

```
Robust Dominance:   No robust dominance found.
                    Adm(A) = {Play, Dont_Play}

Layer 1 (Constraints): Both pass. C = {Play, Dont_Play}
                       F = Adm(C) = {Play, Dont_Play}

Layer 2 (Satisficing): Sat(F, r) = empty
                       P(gain) = 4.1% under biased prior (far below 10%).
                       ASF fallback: ASF(Play) = -0.0590
                                     ASF(Dont_Play) = -0.1000
                       ASF selects Play.

Layer 3:               Skipped (ASF already resolved).

Layer 4:               |R| = 1 -- unique recommendation: Play
```

At \$20, the tension across all three objectives is fully engaged. Play loses on downside (objective 3 at $0.000936$--$0.000937$ vs. baseline $0.000951$) and on EV under the biased prior ($0.000941 < 0.000951$), but wins on P(gain) ($4.1\% > 0\%$) and on EV under the risk-aware evaluator ($0.001015$--$0.001123$). Neither action dominates. The ASF shortfall has grown to $-0.0590$, reflecting that Play is increasingly far from meeting aspirations, but Play still beats Dont\_Play's shortfall of $-0.1000$.

### 5.4 Fee = \$22 (The Last PLAY -- Constraint Boundary)

**Outcome sets:**

| $(P, \vec{f})$ pair | $E[\text{net}]$ | $P(\text{gain})$ | Downside |
|----------------------|-----------------|-------------------|----------|
| **Y(Play):** | | | |
| $(P_{\text{fair}}, \vec{f}_{\text{neutral}})$ | 0.000950 | 0.062500 | 0.000935 |
| $(P_{\text{fair}}, \vec{f}_{\text{risk}})$ | 0.001118 | 0.062500 | 0.000935 |
| $(P_{\text{biased}}, \vec{f}_{\text{neutral}})$ | 0.000939 | 0.041006 | 0.000934 |
| $(P_{\text{biased}}, \vec{f}_{\text{risk}})$ | 0.001011 | 0.041006 | 0.000934 |
| **Y(Dont\_Play):** | | | |
| (all pairs) | 0.000951 | 0.000000 | 0.000951 |

**Protocol execution:**

```
Robust Dominance:   No robust dominance found.
                    Adm(A) = {Play, Dont_Play}

Layer 1 (Constraints): Both pass. C = {Play, Dont_Play}
                       F = Adm(C) = {Play, Dont_Play}

Layer 2 (Satisficing): Sat(F, r) = empty
                       ASF fallback:
                         ASF(Play) = -0.0590
                         ASF(Dont_Play) = -0.1000
                       ASF selects Play.

Layer 3:               Skipped (ASF already resolved).

Layer 4:               |R| = 1 -- unique recommendation: Play
```

At \$22, this is the last fee where MOADT recommends playing. The fee exceeds the truncated EV (\$21), so under the fair coin with risk-neutral evaluation, Play's expected net value ($0.000950$) falls *below* the baseline ($0.000951$). Under the biased prior, it is even worse ($0.000939$). Play's downside ($0.000934$--$0.000935$) is well below baseline. Neither action dominates — the three-way tension (Play wins on P(gain), mixed on EV, loses on downside) persists.

Both actions survive to the constraint layer. Both pass (worst-case loss = $\$22 - \$2 = \$20$, exactly at the limit). Both enter the feasible set. Satisficing fails for both (neither meets P(gain) $\geq 10\%$). The ASF fallback resolves: Play's shortfall ($-0.0590$) is smaller than Dont\_Play's ($-0.1000$), so Play is selected. The key: even though Play's P(gain) aspiration shortfall is larger, its *worst* shortfall across all objectives is still less severe than Dont\_Play's complete failure on P(gain) (score of 0 vs. aspiration of 0.10).

### 5.5 Fee = \$25 (The First DONT PLAY -- Constraint Eliminates Play)

**Outcome sets:**

| $(P, \vec{f})$ pair | $E[\text{net}]$ | $P(\text{gain})$ | Downside |
|----------------------|-----------------|-------------------|----------|
| **Y(Play):** | | | |
| $(P_{\text{fair}}, \vec{f}_{\text{neutral}})$ | 0.000947 | 0.062500 | 0.000932 |
| $(P_{\text{fair}}, \vec{f}_{\text{risk}})$ | 0.001112 | 0.062500 | 0.000932 |
| $(P_{\text{biased}}, \vec{f}_{\text{neutral}})$ | 0.000936 | 0.041006 | 0.000932 |
| $(P_{\text{biased}}, \vec{f}_{\text{risk}})$ | 0.001006 | 0.041006 | 0.000932 |
| **Y(Dont\_Play):** | | | |
| (all pairs) | 0.000951 | 0.000000 | 0.000951 |

**Protocol execution:**

```
Robust Dominance:   No robust dominance found.
                    Adm(A) = {Play, Dont_Play}

Layer 1 (Constraints): Play FAILS.
                       Worst-case loss = $25 - $2 = $23 > $20 limit.
                       Dont_Play PASSES.
                       C = {Dont_Play}
                       F = Adm(C) = {Dont_Play}

Layer 2 (Satisficing): Sat(F, r) = empty
                       ASF fallback: ASF(Dont_Play) = -0.1000
                       ASF selects Dont_Play.

Layer 3:               Skipped (ASF already resolved).

Layer 4:               |R| = 1 -- unique recommendation: Dont_Play
```

At \$25, the hard constraint fires. The worst-case net payoff from Play is $\$2 - \$25 = -\$23$, which exceeds the \$20 loss tolerance. Play is eliminated at Layer 1 -- no amount of expected upside can compensate for a worst-case loss that the agent cannot tolerate. This is not a utility function adjustment; it is a structural precondition.

### 5.6 Fee = \$50 (High Fee -- Deep into DONT PLAY Territory)

**Protocol execution:**

```
Robust Dominance:   No robust dominance found.
                    Adm(A) = {Play, Dont_Play}

Layer 1 (Constraints): Play FAILS (worst loss = $48 > $20).
                       F = {Dont_Play}

Layer 2-4:             Dont_Play selected throughout.
                       Unique recommendation: Dont_Play
```

At \$50, the constraint violation is overwhelming ($\$48$ loss vs. $\$20$ limit). Play has only a 3.12% chance of gaining and a 1.85% chance under the biased prior. Even the risk-aware evaluator cannot rescue it.

---

## 6. Mechanism Analysis

### Which MOADT Layer Drives the Resolution at Each Fee Level

| Fee Range | Resolving Layer | Mechanism |
|-----------|----------------|-----------|
| \$1--\$2 | Layer 0 (Dominance) | Play robustly dominates: no state produces a loss, so downside $=$ baseline while EV and P(gain) strictly beat Dont\_Play. |
| \$3--\$8 | Layer 2 (Satisficing) | Dominance fails — the first-flip loss state drags expected downside below baseline, creating a three-way tension. But Play meets all aspirations, so satisficing selects it directly. |
| \$10--\$22 | Layer 2 (ASF) | Neither action dominates. Satisficing also fails (P(gain) drops below 10% aspiration). ASF fallback selects Play (smaller shortfall from aspirations than Dont\_Play). |
| \$25+ | Layer 1 (Constraint) | Play violates the worst-case loss constraint. Eliminated before any further analysis. |

**Detailed mechanism trace from the script:**

```
$    1: Layer 0 (Dominance): Play robustly dominates
$    2: Layer 0 (Dominance): Play robustly dominates
$    3: Layer 2 (Satisficing): excludes Dont_Play
$    4: Layer 2 (Satisficing): excludes Dont_Play
$    5: Layer 2 (Satisficing): excludes Dont_Play
$    8: Layer 2 (Satisficing): excludes Dont_Play
$   10: Layer 2 (ASF): selects Play
$   12: Layer 2 (ASF): selects Play
$   15: Layer 2 (ASF): selects Play
$   18: Layer 2 (ASF): selects Play
$   20: Layer 2 (ASF): selects Play
$   22: Layer 2 (ASF): selects Play
$   25: Layer 1 (Constraint): Play violates downside floor
$   30: Layer 1 (Constraint): Play violates downside floor
$   40: Layer 1 (Constraint): Play violates downside floor
...
$ 1000: Layer 1 (Constraint): Play violates downside floor
```

### Why Multiple Mechanisms Matter

No single mechanism resolves the paradox across the full range:

1. **Dominance alone** resolves only fees \$1--\$2 (where no state produces a loss, so Play wins on all three objectives). From fee \$3 onward, the downside objective creates a genuine tension that dominance cannot resolve — both actions remain admissible, and the protocol layers must do the real work.

2. **Constraints alone** would produce a sharp cutoff at \$22 (fee = loss limit + \$2) but would say nothing about whether to play at \$20 or \$22 -- it treats all fees below the cutoff identically.

3. **Satisficing alone** would fail at fees above \$8 (where P(gain) drops below 10%), which is too conservative -- most people would still play at \$10 or \$15.

4. **ASF** provides the bridge: it resolves cases where satisficing fails but the game is still worth playing, by measuring *how far* each action falls from aspirations rather than applying a binary pass/fail.

The layered protocol allows each mechanism to operate in its natural range, handing off to the next layer when the current one cannot resolve the decision.

---

## 7. Comparison with Historical Resolutions

| Historical Resolution | Mechanism | MOADT Analog |
|-----------------------|-----------|--------------|
| **Bernoulli (1738)** -- Log utility | Diminishing marginal value of money; $U(x) = \ln(x)$ | Risk-aware evaluator $\vec{f}_{\text{risk}}$ with log compression. But it is *one evaluator among two*, not the sole resolution. |
| **Bounded utility** (Menger, 1934) | Cap on total utility gain; finite $U_{\text{max}}$ prevents infinite EV | Hard constraints (Layer 1): cap on maximum acceptable *loss*, not maximum utility. Structural, not parametric. |
| **Finite wealth** (various) | Cannot bet what you do not have; budget constraint | Downside floor constraint. The agent's loss tolerance is a structural parameter of the decision problem, not a property of the utility function. |
| **Risk aversion** (Arrow, Pratt) | Concave utility function; $U'' < 0$ | Multi-objective structure: P(gain) and downside exposure as *separate objectives*, not curvature of a single utility function. Risk is preserved as a dimension, not compressed into one. |
| **Prospect theory** (Kahneman & Tversky, 1979) | Probability weighting, loss aversion, reference dependence | Credal set (biased prior models probability distortion) + loss-preserving evaluator (downside stays linear while upside is compressed). Reference point is explicit in Layer 2. |

### The Key Difference

Each historical resolution picks *one* mechanism and builds it into the utility function. MOADT does not choose -- it provides a framework that naturally incorporates elements of *all* of them:

- **Evaluator plurality** captures diminishing marginal value (Bernoulli) without committing to a specific functional form.
- **Constraints** capture wealth bounds (Menger, finite wealth) as structural preconditions rather than utility modifications.
- **Objective plurality** captures risk aversion (Arrow-Pratt) structurally -- risk is a separate dimension, not a curvature parameter.
- **Credal sets** capture probability uncertainty (prospect theory's probability weighting) as explicit model uncertainty.

The paradox dissolves through structural pluralism, not a clever fix to the utility function.

---

## 8. Sensitivity Analysis

### Effect of Loss Tolerance on Fee Cap

The Layer 1 constraint sets the maximum acceptable loss in any state. Since the worst state always pays \$2, the constraint translates directly to a fee cap: $F_{\max} = \$2 + \text{loss\_limit}$.

| Loss Tolerance | Max Fee (Layer 1) | Note |
|----------------|-------------------|------|
| \$5 | \$7 | Conservative gambler |
| \$10 | \$12 | |
| \$15 | \$17 | |
| \$20 | \$22 | Matches human intuition |
| \$25 | \$27 | Beyond truncated EV |
| \$30 | \$32 | Beyond truncated EV |
| \$50 | \$52 | Beyond truncated EV |
| \$100 | \$102 | Beyond truncated EV |
| \$500 | \$502 | Beyond truncated EV |

With loss tolerance of \$20, MOADT caps the fee at \$22. This is close to human intuition of \$20--25.

### Why This Is Not Arbitrary

The constraint level is *not* an arbitrary parameter choice -- it represents a genuine structural feature of the decision problem: "How much can the agent afford to lose in a single bet?" Different agents with different wealth levels would set different constraints, producing different fee caps. This is exactly analogous to the empirical finding that wealthier individuals report higher willingness-to-pay for the St. Petersburg game.

The constraint interacts with the multi-objective structure:

- **Low fees ($< \$3$):** Play robustly dominates regardless of constraint level. Layer 0 resolves.
- **Moderate fees (\$3--$F_{\max}$):** Neither action dominates, but ASF/satisficing selects Play (positive EV + some P(gain)). The constraint is not binding.
- **High fees ($> F_{\max}$):** The constraint eliminates Play. No further analysis needed.

The transition zone around $F_{\max}$ is where multiple MOADT mechanisms interact to produce the fee cap.

---

## 9. Summary of Protocol Execution

```
Input: 2 actions x 20 states x 3 objectives x 2 priors x 2 evaluators
       Sweep over 21 fee levels from $1 to $1,000

Fee = $1-$2:   Robust Dominance: Play dominates Dont_Play
               Adm(A) = {Play}
               No state produces a loss, so downside = baseline
               Verdict: PLAY

Fee = $3-$8:   Robust Dominance: Neither dominates
               Adm(A) = {Play, Dont_Play}
               Layer 2: Satisficing selects Play (all aspirations met)
               Verdict: PLAY

Fee = $10-$22: Robust Dominance: Neither dominates
               Adm(A) = {Play, Dont_Play}
               Layer 2: Satisficing fails (P(gain) < 10% aspiration)
                        ASF fallback selects Play
               Verdict: PLAY

Fee = $25+:    Robust Dominance: Neither dominates
               Adm(A) = {Play, Dont_Play}
               Layer 1: Play FAILS (worst loss > $20)
               F = {Dont_Play}
               Verdict: DONT PLAY

MOADT maximum recommended fee: $22
Crossover to refusal: $25
Classical EU maximum: $21 (truncated), infinity (untruncated)
Human intuition: ~$20-25
```

---

## 10. What This Example Demonstrates

1. **The multi-objective structure prevents dominance swamping.** In scalar EU, infinite (or large) expected value overwhelms all other concerns -- this is the paradox. With 3 independent objectives, Play cannot robustly dominate Dont\_Play once the fee exceeds \$2, because the expected downside exposure (objective 3) drops below the baseline while expected value remains positive. MOADT preserves the tension rather than collapsing it.

2. **Hard constraints eliminate catastrophic bets.** The per-state floor (max loss $\leq \$20$) means that entry fees above \$22 are immediately eliminated at Layer 1. No amount of expected upside can compensate. This is a structural feature of MOADT, not a utility function tweak. The constraint is analogous to bounded utility (Menger) and finite wealth, but operates as a precondition rather than a function shape.

3. **Satisficing filters on multiple aspirations simultaneously.** The reference point requires positive EV AND reasonable P(gain) AND tolerable worst case. As the fee rises, P(gain) drops below the aspiration threshold, filtering out Play even if EV remains positive. This captures the intuition that a game where you lose money 87.5% of the time is not a "good bet" regardless of expected value.

4. **The ASF fallback bridges the gap.** When no action robustly meets aspirations (as happens for fees \$10--\$22), the achievement scalarizing function measures *how close* each action gets. This allows MOADT to distinguish between "barely misses aspirations" (Play at \$10) and "completely fails aspirations" (Dont\_Play on P(gain)), avoiding the false conservatism of a binary pass/fail filter.

5. **Structural pluralism replaces single-mechanism fixes.** MOADT incorporates elements of *every* historical resolution -- Bernoulli's log utility, bounded utility, finite wealth, risk aversion, prospect theory -- as special cases within its framework. The paradox dissolves not because one of these mechanisms is "correct," but because their interaction through the layered protocol produces a recommendation that respects all of them simultaneously.

6. **The framework produces actionable recommendations.** The output is not "it depends" or a philosophical position. It is: "Play at fees up to \$22. Do not play at \$25 or above." This matches human intuition while being derived from explicit, verifiable computations.

---

## Appendix: Computational Verification

All numerical results in this document were produced by `examples/classic_stpetersburg.py` using the MOADT engine (`moadt/_engine.py`). The code is available in the repository and can be run independently to verify every number.

**Key parameters:**

- Truncation depth: $N = 20$ flips
- Normalization range: $[-998, 1{,}048{,}575]$
- Baseline (Dont\_Play normalized value): $0.000951$
- Loss limit: \$20 (translates to constraint floor at `normalize_net(-20)`)
- Reference point: $\vec{r} = (\text{normalize\_net}(1),\; 0.10,\; \text{normalize\_net}(-5))$
- Risk compression: $\text{log}(1 + 99x) / \text{log}(100)$ on upside, linear on downside

---

## References

- MOADT (Multi-Objective Admissible Decision Theory) is defined in the companion paper.
- Freeman (2025), "The Scalarization Trap," provides the motivation for why scalar expected utility is structurally problematic for alignment.
- Bernoulli, D. (1738). "Specimen theoriae novae de mensura sortis." *Commentarii Academiae Scientiarum Imperialis Petropolitanae*, 5, 175--192. The original statement of the paradox and the log-utility resolution.
- Menger, K. (1934). "Das Unsicherheitsmoment in der Wertlehre." *Zeitschrift fur Nationalokonomie*, 5, 459--485. Showed that Bernoulli's resolution fails for unbounded utility functions (the "super-Petersburg paradox").
- Kahneman, D. & Tversky, A. (1979). "Prospect Theory: An Analysis of Decision under Risk." *Econometrica*, 47(2), 263--291. Probability weighting and loss aversion as behavioral resolution.
- Wierzbicki, A. P. (1980). "The use of reference objectives in multiobjective optimization." The achievement scalarizing function used in the Layer 2 fallback.
