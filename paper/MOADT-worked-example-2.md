# MOADT Worked Example 2: Medical Treatment Selection

*A concrete walkthrough of Multi-Objective Admissible Decision Theory applied to clinical decision support*

---

## Overview

This document applies MOADT — Multi-Objective Admissible Decision Theory — to a clinical treatment selection problem. Every computation is shown explicitly: raw outcome tables, outcome sets, constraint checks across all state-evaluator pairs, satisficing analysis, regret-Pareto comparison, and a comparison with scalar expected utility. The goal is to make the abstract formalism concrete and medically meaningful.

The scenario is deliberately richer than the companion worked example (Paper 1's resource allocation): 6 treatments, 4 patient response states, 4 objectives, 2 credal priors, and 2 evaluators. Each action's outcome set $Y(a)$ therefore contains 4 vectors in $\mathbb{R}^4$. The additional complexity serves two purposes: it shows how the theory scales to higher-dimensional problems, and it introduces a safety constraint that interacts with evaluator uncertainty in a clinically critical way. Nothing is hidden — the reader can check every number with a calculator.

---

## 1. The Scenario

A clinical decision support system must recommend a treatment for a patient with a chronic condition. The clinician faces genuine uncertainty about how this patient will respond (the patient's risk profile is ambiguous), and the evidence base itself is contested — controlled trial data may not reflect real-world outcomes for this patient.

### 1.1 Actions (Treatments)

Six treatment options are available:

| Action | Treatment | Description |
|--------|-----------|-------------|
| $a_1$ | Standard monotherapy | First-line single-agent treatment; well-established safety profile |
| $a_2$ | Aggressive monotherapy | Higher-dose single-agent; stronger effect, more side effects |
| $a_3$ | Combination A | Two-drug regimen; high efficacy but complex dosing and monitoring |
| $a_4$ | Combination B | Two-drug regimen; moderate efficacy with better safety than Combo A |
| $a_5$ | Experimental | Novel agent from recent trials; promising but limited long-term data |
| $a_6$ | Watchful waiting | Defer active treatment; monitor and intervene only if progression occurs |

### 1.2 States (Patient Response Types)

Four patient response profiles, representing uncertainty about how this particular patient's physiology will interact with treatment:

| State | Description | Probability |
|-------|-------------|-------------|
| $s_1$ (Strong responder) | Patient metabolizes drug well, strong therapeutic response | 30% |
| $s_2$ (Moderate responder) | Typical response profile | 40% |
| $s_3$ (Weak responder) | Suboptimal drug metabolism, reduced efficacy | 20% |
| $s_4$ (Adverse reactor) | Patient has heightened sensitivity to side effects | 10% |

The probabilities above are point estimates. The actual uncertainty about this patient's type is captured by the credal set (Section 1.4).

### 1.3 Objectives ($k = 4$)

| Objective | Meaning | Scale |
|-----------|---------|-------|
| $f_1$: Efficacy | Treatment effectiveness (symptom control, disease modification) | Normalized to $[0, 1]$ |
| $f_2$: Safety | Freedom from adverse events and side effects | Normalized to $[0, 1]$ |
| $f_3$: Patient autonomy | Inverse of treatment burden (fewer appointments, simpler regimen = higher) | Normalized to $[0, 1]$ |
| $f_4$: Cost efficiency | Inverse of total treatment cost to patient and system | Normalized to $[0, 1]$ |

These objectives are *incommensurable*: there is no meaningful exchange rate between efficacy and patient autonomy. A treatment that controls symptoms brilliantly but requires daily infusions at a clinic imposes a qualitatively different kind of cost than one that works less well but involves a single daily pill. Both dimensions matter. Neither reduces to the other. And the question of how much safety risk is acceptable for how much efficacy gain is precisely the kind of value judgment that should be made by the patient, not the algorithm.

### 1.4 Credal Set ($|\mathcal{P}| = 2$)

Two probability models over patient response types are maintained:

$$P_{\text{clinical}} = (0.30,\; 0.40,\; 0.20,\; 0.10) \quad \text{(from clinical trial population data)}$$

$$P_{\text{cautious}} = (0.20,\; 0.35,\; 0.25,\; 0.20) \quad \text{(adjusted for this patient's risk factors)}$$

$P_{\text{clinical}}$ reflects the response distribution observed in controlled trials. $P_{\text{cautious}}$ is adjusted by the clinician who notes that this patient has risk factors (age, comorbidities, genetic markers) suggesting a higher probability of weak response or adverse reaction. The credal set $\mathcal{P} = \{P_{\text{clinical}}, P_{\text{cautious}}\}$ says: "we don't know whether this patient's risk profile matches the trial population or warrants the cautious adjustment."

Note the asymmetry: $P_{\text{cautious}}$ doubles the probability of adverse reaction (from 10% to 20%) and increases weak response probability from 20% to 25%, at the expense of strong and moderate response. This is not pessimism for its own sake — it reflects specific clinical judgment about this patient.

### 1.5 Evaluator Set ($|\mathcal{F}| = 2$)

Two evaluation functions reflect disagreement about whether controlled trial outcomes apply to this patient:

- $\vec{f}_{\text{trial}}$: Takes outcomes from controlled trial data at face value.
- $\vec{f}_{\text{realworld}}$: Applies real-world adjustments — efficacy is deflated (adherence is lower outside trials, comorbidities reduce response), safety is deflated by 10% (trial populations exclude high-risk patients), and autonomy is deflated by approximately 14% (real-world treatment burden exceeds trial protocols due to additional monitoring, pharmacy visits, etc.). Cost efficiency is unchanged (costs are objective).

This is $\mathcal{F}$ in action: the evidence base itself is uncertain. Trial data are gathered under idealized conditions (motivated patients, strict protocols, close monitoring). Real-world outcomes are systematically worse on efficacy, safety, and autonomy. The evaluator set says "we don't know whether this patient's experience will resemble the trial or the real world."

### 1.6 Constraint and Reference Point

**Hard constraint (Layer 1):** Safety $\geq 0.35$ in *every* state under *every* evaluator. This is a non-negotiable patient safety threshold. No amount of efficacy justifies a treatment whose safety score drops below 0.35 for any patient response type under any plausible evaluation. This constraint is checked per-state, per-evaluator — not on expected values.

**Reference point (Layer 2):** $\vec{r} = (0.40,\; 0.50,\; 0.30,\; 0.30)$ — representing the clinician's aspiration: "the treatment should achieve at least moderate efficacy, maintain reasonable safety, impose manageable burden, and not be prohibitively expensive." These are aspiration levels, not hard constraints. An action that falls below an aspiration level is not *unsafe* — it is just *not good enough* to be worth recommending over alternatives.

### 1.7 Raw Outcome Data

The following tables show the outcome $\vec{f}(\omega(a, s))$ for each action-state pair, under each evaluator. These are the primitive inputs from which everything else is computed.

**$a_1$ (Standard monotherapy):**

| State | Evaluator | Efficacy | Safety | Autonomy | Cost |
|-------|-----------|----------|--------|----------|------|
| $s_1$ (Strong) | $\vec{f}_{\text{trial}}$ | 0.75 | 0.80 | 0.70 | 0.80 |
| | $\vec{f}_{\text{real}}$ | 0.62 | 0.72 | 0.60 | 0.80 |
| $s_2$ (Moderate) | $\vec{f}_{\text{trial}}$ | 0.60 | 0.80 | 0.70 | 0.80 |
| | $\vec{f}_{\text{real}}$ | 0.50 | 0.72 | 0.60 | 0.80 |
| $s_3$ (Weak) | $\vec{f}_{\text{trial}}$ | 0.35 | 0.80 | 0.70 | 0.80 |
| | $\vec{f}_{\text{real}}$ | 0.28 | 0.72 | 0.60 | 0.80 |
| $s_4$ (Adverse) | $\vec{f}_{\text{trial}}$ | 0.30 | 0.55 | 0.70 | 0.80 |
| | $\vec{f}_{\text{real}}$ | 0.25 | 0.50 | 0.60 | 0.80 |

Standard monotherapy has moderate efficacy that drops for weak responders, excellent safety even for adverse reactors, high autonomy (simple single-pill regimen), and good cost efficiency. The safety floor of 0.50 (adverse reactor, real-world) remains well above the 0.35 threshold.

**$a_2$ (Aggressive monotherapy):**

| State | Evaluator | Efficacy | Safety | Autonomy | Cost |
|-------|-----------|----------|--------|----------|------|
| $s_1$ (Strong) | $\vec{f}_{\text{trial}}$ | 0.90 | 0.60 | 0.50 | 0.70 |
| | $\vec{f}_{\text{real}}$ | 0.75 | 0.54 | 0.43 | 0.70 |
| $s_2$ (Moderate) | $\vec{f}_{\text{trial}}$ | 0.75 | 0.55 | 0.50 | 0.70 |
| | $\vec{f}_{\text{real}}$ | 0.62 | 0.50 | 0.43 | 0.70 |
| $s_3$ (Weak) | $\vec{f}_{\text{trial}}$ | 0.50 | 0.50 | 0.50 | 0.70 |
| | $\vec{f}_{\text{real}}$ | 0.40 | 0.45 | 0.43 | 0.70 |
| $s_4$ (Adverse) | $\vec{f}_{\text{trial}}$ | 0.45 | **0.25** | 0.50 | 0.70 |
| | $\vec{f}_{\text{real}}$ | 0.38 | **0.23** | 0.43 | 0.70 |

Note the bold entries: for adverse reactors, safety collapses to 0.25 (trial) and 0.23 (real-world) — far below the 0.35 threshold. Aggressive monotherapy is highly effective for strong responders but dangerous for the wrong patient.

**$a_3$ (Combination A):**

| State | Evaluator | Efficacy | Safety | Autonomy | Cost |
|-------|-----------|----------|--------|----------|------|
| $s_1$ (Strong) | $\vec{f}_{\text{trial}}$ | 0.85 | 0.65 | 0.45 | 0.50 |
| | $\vec{f}_{\text{real}}$ | 0.70 | 0.59 | 0.38 | 0.50 |
| $s_2$ (Moderate) | $\vec{f}_{\text{trial}}$ | 0.70 | 0.60 | 0.45 | 0.50 |
| | $\vec{f}_{\text{real}}$ | 0.58 | 0.54 | 0.38 | 0.50 |
| $s_3$ (Weak) | $\vec{f}_{\text{trial}}$ | 0.55 | 0.55 | 0.45 | 0.50 |
| | $\vec{f}_{\text{real}}$ | 0.44 | 0.50 | 0.38 | 0.50 |
| $s_4$ (Adverse) | $\vec{f}_{\text{trial}}$ | 0.40 | **0.30** | 0.45 | 0.50 |
| | $\vec{f}_{\text{real}}$ | 0.33 | **0.27** | 0.38 | 0.50 |

Combination A also violates the safety threshold for adverse reactors: 0.30 under trial data, 0.27 under real-world evaluation. Additionally, autonomy is low (complex two-drug regimen requiring monitoring) and cost is moderate.

**$a_4$ (Combination B):**

| State | Evaluator | Efficacy | Safety | Autonomy | Cost |
|-------|-----------|----------|--------|----------|------|
| $s_1$ (Strong) | $\vec{f}_{\text{trial}}$ | 0.80 | 0.70 | 0.40 | 0.45 |
| | $\vec{f}_{\text{real}}$ | 0.66 | 0.63 | 0.34 | 0.45 |
| $s_2$ (Moderate) | $\vec{f}_{\text{trial}}$ | 0.65 | 0.70 | 0.40 | 0.45 |
| | $\vec{f}_{\text{real}}$ | 0.54 | 0.63 | 0.34 | 0.45 |
| $s_3$ (Weak) | $\vec{f}_{\text{trial}}$ | 0.50 | 0.65 | 0.40 | 0.45 |
| | $\vec{f}_{\text{real}}$ | 0.40 | 0.59 | 0.34 | 0.45 |
| $s_4$ (Adverse) | $\vec{f}_{\text{trial}}$ | 0.35 | 0.45 | 0.40 | 0.45 |
| | $\vec{f}_{\text{real}}$ | 0.29 | 0.41 | 0.34 | 0.45 |

Combination B trades some efficacy for better safety compared to Combination A. Its safety floor for adverse reactors is 0.41 (real-world) — above the 0.35 threshold. But autonomy is low (complex regimen) and cost is the worst of all treatments.

**$a_5$ (Experimental):**

| State | Evaluator | Efficacy | Safety | Autonomy | Cost |
|-------|-----------|----------|--------|----------|------|
| $s_1$ (Strong) | $\vec{f}_{\text{trial}}$ | 0.95 | 0.70 | 0.55 | 0.30 |
| | $\vec{f}_{\text{real}}$ | 0.80 | 0.63 | 0.47 | 0.30 |
| $s_2$ (Moderate) | $\vec{f}_{\text{trial}}$ | 0.70 | 0.65 | 0.55 | 0.30 |
| | $\vec{f}_{\text{real}}$ | 0.58 | 0.59 | 0.47 | 0.30 |
| $s_3$ (Weak) | $\vec{f}_{\text{trial}}$ | 0.30 | 0.60 | 0.55 | 0.30 |
| | $\vec{f}_{\text{real}}$ | 0.24 | 0.54 | 0.47 | 0.30 |
| $s_4$ (Adverse) | $\vec{f}_{\text{trial}}$ | 0.20 | **0.35** | 0.55 | 0.30 |
| | $\vec{f}_{\text{real}}$ | 0.16 | **0.32** | 0.47 | 0.30 |

This is the most instructive case in the dataset. Under trial data, the experimental treatment's safety score for adverse reactors is *exactly* 0.35 — right at the threshold. Under real-world evaluation, it drops to 0.32 — *below* the threshold. The gap between trial and real-world evaluation is the difference between "barely safe" and "not safe enough." Without evaluator uncertainty ($\mathcal{F}$), this treatment would be considered safe. With $\mathcal{F}$, it is correctly eliminated.

**$a_6$ (Watchful waiting):**

| State | Evaluator | Efficacy | Safety | Autonomy | Cost |
|-------|-----------|----------|--------|----------|------|
| $s_1$ (Strong) | $\vec{f}_{\text{trial}}$ | 0.40 | 0.95 | 0.90 | 0.95 |
| | $\vec{f}_{\text{real}}$ | 0.35 | 0.86 | 0.77 | 0.95 |
| $s_2$ (Moderate) | $\vec{f}_{\text{trial}}$ | 0.25 | 0.95 | 0.90 | 0.95 |
| | $\vec{f}_{\text{real}}$ | 0.21 | 0.86 | 0.77 | 0.95 |
| $s_3$ (Weak) | $\vec{f}_{\text{trial}}$ | 0.15 | 0.95 | 0.90 | 0.95 |
| | $\vec{f}_{\text{real}}$ | 0.12 | 0.86 | 0.77 | 0.95 |
| $s_4$ (Adverse) | $\vec{f}_{\text{trial}}$ | 0.10 | 0.95 | 0.90 | 0.95 |
| | $\vec{f}_{\text{real}}$ | 0.08 | 0.86 | 0.77 | 0.95 |

Watchful waiting is maximally safe, autonomous, and cheap — but efficacy is severely depressed. For moderate, weak, and adverse responders, efficacy is 0.25 or below even under trial evaluation. This treatment is not *dangerous* — it is just *not doing much*.

---

## 2. Computing Outcome Sets $Y(a)$

Each action's outcome set contains one vector for each $(P, \vec{f})$ pair. With $|\mathcal{P}| = 2$ and $|\mathcal{F}| = 2$, each $Y(a)$ contains exactly 4 vectors in $\mathbb{R}^4$.

The computation for each vector is:

$$\vec{y}_{(P, \vec{f})}(a) = \sum_{s \in S} P(s) \cdot \vec{f}(\omega(a, s))$$

### Worked example: $Y(a_1)$, first vector

Using $P_{\text{clinical}} = (0.30, 0.40, 0.20, 0.10)$ and $\vec{f}_{\text{trial}}$:

$$\vec{y} = 0.30 \cdot (0.75, 0.80, 0.70, 0.80) + 0.40 \cdot (0.60, 0.80, 0.70, 0.80)$$
$$\quad + 0.20 \cdot (0.35, 0.80, 0.70, 0.80) + 0.10 \cdot (0.30, 0.55, 0.70, 0.80)$$

$$= (0.225, 0.240, 0.210, 0.240) + (0.240, 0.320, 0.280, 0.320)$$
$$\quad + (0.070, 0.160, 0.140, 0.160) + (0.030, 0.055, 0.070, 0.080)$$

$$= (0.5650,\; 0.7750,\; 0.7000,\; 0.8000)$$

### Worked example: $Y(a_1)$, worst-case vector

Using $P_{\text{cautious}} = (0.20, 0.35, 0.25, 0.20)$ and $\vec{f}_{\text{real}}$:

$$\vec{y} = 0.20 \cdot (0.62, 0.72, 0.60, 0.80) + 0.35 \cdot (0.50, 0.72, 0.60, 0.80)$$
$$\quad + 0.25 \cdot (0.28, 0.72, 0.60, 0.80) + 0.20 \cdot (0.25, 0.50, 0.60, 0.80)$$

$$= (0.124, 0.144, 0.120, 0.160) + (0.175, 0.252, 0.210, 0.280)$$
$$\quad + (0.070, 0.180, 0.150, 0.200) + (0.050, 0.100, 0.120, 0.160)$$

$$= (0.4190,\; 0.6760,\; 0.6000,\; 0.8000)$$

This is the worst-case expected outcome for Standard: using the cautious prior (more adverse reactors) and real-world evaluation (deflated efficacy and safety). Even here, all four components remain above the reference point $\vec{r} = (0.40, 0.50, 0.30, 0.30)$.

### Full Outcome Sets

All remaining vectors are computed analogously.

**$Y(a_1)$ — Standard monotherapy:**

| $(P, \vec{f})$ pair | Efficacy | Safety | Autonomy | Cost |
|---------------------|----------|--------|----------|------|
| $(P_{\text{clin}}, \vec{f}_{\text{trial}})$ | 0.5650 | 0.7750 | 0.7000 | 0.8000 |
| $(P_{\text{clin}}, \vec{f}_{\text{real}})$ | 0.4670 | 0.6980 | 0.6000 | 0.8000 |
| $(P_{\text{caut}}, \vec{f}_{\text{trial}})$ | 0.5075 | 0.7500 | 0.7000 | 0.8000 |
| $(P_{\text{caut}}, \vec{f}_{\text{real}})$ | 0.4190 | 0.6760 | 0.6000 | 0.8000 |

**$Y(a_2)$ — Aggressive monotherapy:**

| $(P, \vec{f})$ pair | Efficacy | Safety | Autonomy | Cost |
|---------------------|----------|--------|----------|------|
| $(P_{\text{clin}}, \vec{f}_{\text{trial}})$ | 0.7150 | 0.5250 | 0.5000 | 0.7000 |
| $(P_{\text{clin}}, \vec{f}_{\text{real}})$ | 0.5910 | 0.4750 | 0.4300 | 0.7000 |
| $(P_{\text{caut}}, \vec{f}_{\text{trial}})$ | 0.6575 | 0.4875 | 0.5000 | 0.7000 |
| $(P_{\text{caut}}, \vec{f}_{\text{real}})$ | 0.5430 | 0.4415 | 0.4300 | 0.7000 |

**$Y(a_3)$ — Combination A:**

| $(P, \vec{f})$ pair | Efficacy | Safety | Autonomy | Cost |
|---------------------|----------|--------|----------|------|
| $(P_{\text{clin}}, \vec{f}_{\text{trial}})$ | 0.6850 | 0.5750 | 0.4500 | 0.5000 |
| $(P_{\text{clin}}, \vec{f}_{\text{real}})$ | 0.5630 | 0.5200 | 0.3800 | 0.5000 |
| $(P_{\text{caut}}, \vec{f}_{\text{trial}})$ | 0.6325 | 0.5375 | 0.4500 | 0.5000 |
| $(P_{\text{caut}}, \vec{f}_{\text{real}})$ | 0.5190 | 0.4860 | 0.3800 | 0.5000 |

**$Y(a_4)$ — Combination B:**

| $(P, \vec{f})$ pair | Efficacy | Safety | Autonomy | Cost |
|---------------------|----------|--------|----------|------|
| $(P_{\text{clin}}, \vec{f}_{\text{trial}})$ | 0.6350 | 0.6650 | 0.4000 | 0.4500 |
| $(P_{\text{clin}}, \vec{f}_{\text{real}})$ | 0.5230 | 0.6000 | 0.3400 | 0.4500 |
| $(P_{\text{caut}}, \vec{f}_{\text{trial}})$ | 0.5825 | 0.6375 | 0.4000 | 0.4500 |
| $(P_{\text{caut}}, \vec{f}_{\text{real}})$ | 0.4790 | 0.5760 | 0.3400 | 0.4500 |

**$Y(a_5)$ — Experimental:**

| $(P, \vec{f})$ pair | Efficacy | Safety | Autonomy | Cost |
|---------------------|----------|--------|----------|------|
| $(P_{\text{clin}}, \vec{f}_{\text{trial}})$ | 0.6450 | 0.6250 | 0.5500 | 0.3000 |
| $(P_{\text{clin}}, \vec{f}_{\text{real}})$ | 0.5360 | 0.5650 | 0.4700 | 0.3000 |
| $(P_{\text{caut}}, \vec{f}_{\text{trial}})$ | 0.5500 | 0.5875 | 0.5500 | 0.3000 |
| $(P_{\text{caut}}, \vec{f}_{\text{real}})$ | 0.4550 | 0.5315 | 0.4700 | 0.3000 |

**$Y(a_6)$ — Watchful waiting:**

| $(P, \vec{f})$ pair | Efficacy | Safety | Autonomy | Cost |
|---------------------|----------|--------|----------|------|
| $(P_{\text{clin}}, \vec{f}_{\text{trial}})$ | 0.2600 | 0.9500 | 0.9000 | 0.9500 |
| $(P_{\text{clin}}, \vec{f}_{\text{real}})$ | 0.2210 | 0.8600 | 0.7700 | 0.9500 |
| $(P_{\text{caut}}, \vec{f}_{\text{trial}})$ | 0.2250 | 0.9500 | 0.9000 | 0.9500 |
| $(P_{\text{caut}}, \vec{f}_{\text{real}})$ | 0.1895 | 0.8600 | 0.7700 | 0.9500 |

### Observation

Each action's outcome set is a compact region in $\mathbb{R}^4$ (here, a set of 4 points). The *spread* of each set reflects epistemic uncertainty. Standard monotherapy ($a_1$) has efficacy ranging from 0.419 to 0.565 — a moderate band reflecting uncertainty about both the patient's response type and the reliability of trial data. Watchful waiting ($a_6$) has efficacy ranging from 0.190 to 0.260 — uniformly low regardless of model, because doing nothing is reliably ineffective. But watchful waiting's safety ranges from 0.860 to 0.950 — uniformly high, because doing nothing is reliably safe. The theory tracks all four dimensions simultaneously without forcing them into a single number.

---

## 3. Robust Dominance and the Admissible Set

### 3.1 Checking Robust Dominance

Recall: $a \succ_R b$ iff $\forall \vec{y}_b \in Y(b),\; \exists \vec{y}_a \in Y(a)$ such that $\vec{y}_a \succ_P \vec{y}_b$.

We check all 30 ordered pairs. The result: **no action robustly dominates any other**.

$$\text{Adm}(A) = \{a_1, a_2, a_3, a_4, a_5, a_6\}$$

### 3.2 Why Is No One Dominated?

This is more surprising than in Paper 1's three-objective case. With 6 actions and 4 objectives, one might expect at least one dominance relation. But each action excels on at least one objective in a way that no other action can match across all models.

Consider the most natural candidate: does $a_1$ (Standard) dominate $a_6$ (Watchful waiting)? Take $a_6$'s best vector: $(P_{\text{clin}}, \vec{f}_{\text{trial}})$ gives $(0.260, 0.950, 0.900, 0.950)$. Can any vector in $Y(a_1)$ Pareto-dominate this? The best safety score in $Y(a_1)$ is 0.775, the best autonomy is 0.700, and the best cost is 0.800 — all below $a_6$'s scores of 0.950, 0.900, and 0.950 respectively. So no vector in $Y(a_1)$ can Pareto-dominate $a_6$'s best case. Standard monotherapy cannot robustly dominate watchful waiting because watchful waiting is unbeatable on three of four objectives.

The reverse fails too: $a_6$'s best efficacy is 0.260, while $a_1$'s worst efficacy is 0.419. Watchful waiting can never Pareto-dominate Standard on efficacy.

Does $a_1$ dominate $a_2$ (Aggressive)? $a_2$'s best efficacy is 0.715, while $a_1$'s best is only 0.565. Aggressive monotherapy's efficacy advantage prevents Standard from dominating it, even though Aggressive's safety profile is much worse.

This pattern repeats across all 30 pairs: the four-dimensional objective space provides enough room for every action to maintain a Pareto-incomparable niche. The practical filtering happens in the constraint layer, not through dominance.

---

## 4. The Choice Protocol

### Layer 1: Constraints

**Constraint:** Safety $\geq 0.35$ in *every* state under *every* evaluator.

This is checked per-state, per-evaluator — not on expected values. A single state-evaluator pair in which safety drops below 0.35 eliminates the treatment. The constraint embodies a fundamental clinical principle: we do not accept treatments that are *predictably dangerous for identifiable patient subgroups*, regardless of how well they work for other patients.

**$a_1$ (Standard monotherapy):**

| State | $\vec{f}_{\text{trial}}$ | $\vec{f}_{\text{real}}$ | Result |
|-------|--------------------------|--------------------------|--------|
| $s_1$ (Strong) | 0.80 | 0.72 | Pass |
| $s_2$ (Moderate) | 0.80 | 0.72 | Pass |
| $s_3$ (Weak) | 0.80 | 0.72 | Pass |
| $s_4$ (Adverse) | 0.55 | 0.50 | Pass |

Minimum safety: 0.50 (adverse reactor, real-world). Well above threshold. **PASS.**

**$a_2$ (Aggressive monotherapy):**

| State | $\vec{f}_{\text{trial}}$ | $\vec{f}_{\text{real}}$ | Result |
|-------|--------------------------|--------------------------|--------|
| $s_1$ (Strong) | 0.60 | 0.54 | Pass |
| $s_2$ (Moderate) | 0.55 | 0.50 | Pass |
| $s_3$ (Weak) | 0.50 | 0.45 | Pass |
| $s_4$ (Adverse) | **0.25** | **0.23** | **FAIL** |

Safety collapses for adverse reactors: 0.25 under trial data, 0.23 under real-world. Both far below the 0.35 threshold. **FAIL — excluded.**

**$a_3$ (Combination A):**

| State | $\vec{f}_{\text{trial}}$ | $\vec{f}_{\text{real}}$ | Result |
|-------|--------------------------|--------------------------|--------|
| $s_1$ (Strong) | 0.65 | 0.59 | Pass |
| $s_2$ (Moderate) | 0.60 | 0.54 | Pass |
| $s_3$ (Weak) | 0.55 | 0.50 | Pass |
| $s_4$ (Adverse) | **0.30** | **0.27** | **FAIL** |

Same pattern: adverse reactor safety is 0.30 (trial) and 0.27 (real-world). **FAIL — excluded.**

**$a_4$ (Combination B):**

| State | $\vec{f}_{\text{trial}}$ | $\vec{f}_{\text{real}}$ | Result |
|-------|--------------------------|--------------------------|--------|
| $s_1$ (Strong) | 0.70 | 0.63 | Pass |
| $s_2$ (Moderate) | 0.70 | 0.63 | Pass |
| $s_3$ (Weak) | 0.65 | 0.59 | Pass |
| $s_4$ (Adverse) | 0.45 | 0.41 | Pass |

Minimum safety: 0.41 (adverse reactor, real-world). Above threshold. **PASS.**

**$a_5$ (Experimental):**

| State | $\vec{f}_{\text{trial}}$ | $\vec{f}_{\text{real}}$ | Result |
|-------|--------------------------|--------------------------|--------|
| $s_1$ (Strong) | 0.70 | 0.63 | Pass |
| $s_2$ (Moderate) | 0.65 | 0.59 | Pass |
| $s_3$ (Weak) | 0.60 | 0.54 | Pass |
| $s_4$ (Adverse) | **0.35** | **0.32** | **FAIL** |

This is the critical case. Under controlled trial data, the experimental treatment's safety score for adverse reactors is *exactly* 0.35 — precisely at the threshold. It passes. Under real-world evaluation, the 10% safety deflation reduces this to $0.35 \times 0.9143 \approx 0.32$ — below the threshold. It fails.

The experimental treatment passes the safety constraint under $\vec{f}_{\text{trial}}$ and fails under $\vec{f}_{\text{real}}$. This is exactly why $\mathcal{F}$ exists. If we had only trial data — if we were certain our measurements were accurate — this treatment would be considered safe. But we are *not* certain. The evaluator set captures the gap between controlled and real-world conditions, and that gap is the difference between "barely safe" and "not safe enough." **FAIL — excluded.**

**$a_6$ (Watchful waiting):**

| State | $\vec{f}_{\text{trial}}$ | $\vec{f}_{\text{real}}$ | Result |
|-------|--------------------------|--------------------------|--------|
| $s_1$ (Strong) | 0.95 | 0.86 | Pass |
| $s_2$ (Moderate) | 0.95 | 0.86 | Pass |
| $s_3$ (Weak) | 0.95 | 0.86 | Pass |
| $s_4$ (Adverse) | 0.95 | 0.86 | Pass |

Minimum safety: 0.86 (any state, real-world). Massively above threshold. **PASS.**

**Result:** Three of six treatments are eliminated by the safety constraint.

$$C = \{a_1 \text{ (Standard)},\; a_4 \text{ (Combo B)},\; a_6 \text{ (Watchful)}\}$$

No robust dominance exists among these three survivors, so:

$$F = \text{Adm}(C) = \{a_1, a_4, a_6\}$$

**Commentary:** The constraint eliminates half of the treatment set. This is more aggressive filtering than in Paper 1 (where 2 of 5 actions were eliminated). The increased filtering rate reflects the interaction of more states with evaluator uncertainty: with 4 patient types and 2 evaluators, there are 8 state-evaluator pairs to check per treatment, and only one needs to fail. The constraint acts as a *worst-case* filter: it asks not "what happens on average?" but "is there *any* identifiable scenario in which this treatment is predictably dangerous?"

The Experimental treatment's elimination is especially noteworthy. A system that trusted only trial data would consider it safe. A system that incorporated real-world adjustment catches the risk. This is the evaluator set doing its job: ensuring that safety assessments are robust to measurement model uncertainty.

### Layer 2: Reference-Point Satisficing

**Reference point:** $\vec{r} = (0.40, 0.50, 0.30, 0.30)$

**Robust satisficing:** An action passes Layer 2 iff *every* vector in $Y(a)$ meets or exceeds $\vec{r}$ componentwise. The system must be confident the treatment meets aspirations under all plausible models.

**$a_1$ (Standard):**

| Component | Worst value | Aspiration | Margin | Result |
|-----------|-------------|------------|--------|--------|
| Efficacy | 0.4190 | 0.40 | +0.019 | Pass |
| Safety | 0.6760 | 0.50 | +0.176 | Pass |
| Autonomy | 0.6000 | 0.30 | +0.300 | Pass |
| Cost | 0.8000 | 0.30 | +0.500 | Pass |

Standard passes on all four objectives. Its worst-case efficacy (0.419, under cautious prior and real-world evaluation) clears the 0.40 aspiration with a margin of 0.019 — tight, but sufficient. Safety, autonomy, and cost are all well above aspirations. **PASS.**

**$a_4$ (Combination B):**

| Component | Worst value | Aspiration | Margin | Result |
|-----------|-------------|------------|--------|--------|
| Efficacy | 0.4790 | 0.40 | +0.079 | Pass |
| Safety | 0.5760 | 0.50 | +0.076 | Pass |
| Autonomy | 0.3400 | 0.30 | +0.040 | Pass |
| Cost | 0.4500 | 0.30 | +0.150 | Pass |

Combination B also passes on all four objectives. Its worst-case efficacy (0.479) clears the aspiration more comfortably than Standard. But its margins on safety (0.076), autonomy (0.040), and cost (0.150) are much tighter. **PASS.**

**$a_6$ (Watchful waiting):**

| Component | Worst value | Aspiration | Margin | Result |
|-----------|-------------|------------|--------|--------|
| Efficacy | 0.1895 | 0.40 | **-0.211** | **FAIL** |
| Safety | 0.8600 | 0.50 | +0.360 | Pass |
| Autonomy | 0.7700 | 0.30 | +0.470 | Pass |
| Cost | 0.9500 | 0.30 | +0.650 | Pass |

Watchful waiting's worst-case efficacy is 0.1895 (under cautious prior and real-world evaluation) — far below the 0.40 aspiration. Even its *best-case* efficacy is only 0.260. It excels on safety, autonomy, and cost, but its efficacy shortfall is not marginal — it misses the aspiration by 0.211 units, more than half the aspiration level itself. **FAIL.**

**Result:**

$$\text{Sat}(F, \vec{r}) = \{a_1 \text{ (Standard)},\; a_4 \text{ (Combo B)}\}$$

**Commentary:** Watchful waiting's elimination at Layer 2 illustrates the crucial difference between constraints and aspirations. Watchful waiting *passed* the safety constraint at Layer 1 — it is not a dangerous treatment. It is eliminated at Layer 2 because it is *not effective enough* — not because it violates a precondition, but because it fails to achieve a goal. The constraint says "this must not be unsafe." The aspiration says "this should actually work." They are structurally different requirements, and MOADT applies them at different layers for precisely this reason.

A patient who asks "should we just wait and see?" receives a principled answer: watchful waiting is safe, cheap, and unburdensome, but under every plausible model of your response and every plausible evaluation of outcomes, the expected efficacy is below 0.40. The treatment is not *inappropriate* — it is *insufficient*.

### Layer 3: Regret-Pareto

For the two surviving treatments, we compute per-objective minimax regret. For each objective $i$ and action $a$:

$$\rho_i(a) = \max_{P \in \mathcal{P},\, \vec{f} \in \mathcal{F}} \left[ \max_{a' \in F} \mathbb{E}_P[f_i(a')] - \mathbb{E}_P[f_i(a)] \right]$$

Regret is measured against the full feasible set $F = \{a_1, a_4, a_6\}$, not just the satisficing set $\text{Sat} = \{a_1, a_4\}$. This matters: an action that failed satisficing (like $a_6$, which fell short on efficacy) can still be the source of per-objective regret if it excels on a particular objective. Watchful waiting's safety scores (0.860–0.950), autonomy scores (0.770–0.900), and cost scores (0.950) far exceed those of Standard and Combo B on those dimensions, creating substantial regret for both surviving actions on safety, autonomy, and cost. This illustrates why regret must be measured against the full feasible set: an action that falls short on aspirations can still define the per-objective benchmark.

For each $(P, \vec{f})$ pair, the best available action in $F$ on each objective determines the gap.

**Regret of $a_1$ (Standard):**

For each objective, we find the maximum gap between the best action in $F$ and Standard across all $(P, \vec{f})$ pairs. On efficacy, Combo B ($a_4$) is the best comparator. On safety, autonomy, and cost, Watchful Waiting ($a_6$) is the best comparator — its excellence on those dimensions creates regret that was invisible when comparing only within Sat.

| $(P, \vec{f})$ | Eff gap | Safety gap | Auton gap | Cost gap |
|---|---|---|---|---|
| $(P_{\text{clin}}, \vec{f}_{\text{trial}})$ | $0.635 - 0.565 = 0.070$ ($a_4$) | $0.950 - 0.775 = 0.175$ ($a_6$) | $0.900 - 0.700 = 0.200$ ($a_6$) | $0.950 - 0.800 = 0.150$ ($a_6$) |
| $(P_{\text{clin}}, \vec{f}_{\text{real}})$ | $0.523 - 0.467 = 0.056$ ($a_4$) | $0.860 - 0.698 = 0.162$ ($a_6$) | $0.770 - 0.600 = 0.170$ ($a_6$) | $0.950 - 0.800 = 0.150$ ($a_6$) |
| $(P_{\text{caut}}, \vec{f}_{\text{trial}})$ | $0.5825 - 0.5075 = 0.075$ ($a_4$) | $0.950 - 0.750 = 0.200$ ($a_6$) | $0.900 - 0.700 = 0.200$ ($a_6$) | $0.950 - 0.800 = 0.150$ ($a_6$) |
| $(P_{\text{caut}}, \vec{f}_{\text{real}})$ | $0.479 - 0.419 = 0.060$ ($a_4$) | $0.860 - 0.676 = 0.184$ ($a_6$) | $0.770 - 0.600 = 0.170$ ($a_6$) | $0.950 - 0.800 = 0.150$ ($a_6$) |

Regret is the *maximum* gap per objective:

$$\vec{\rho}(a_1) = (0.075,\; 0.200,\; 0.200,\; 0.150)$$

Standard monotherapy has a small regret on efficacy (0.075, driven by Combo B under the cautious prior and trial evaluation). But it now has *non-zero* regret on safety (0.200), autonomy (0.200), and cost (0.150) — all driven by Watchful Waiting's excellence on those dimensions. Even though Watchful Waiting failed satisficing on efficacy, it sets the per-objective benchmark on safety, autonomy, and cost. Standard is good on those dimensions, but Watchful Waiting is better, and that gap is regret.

**Regret of $a_4$ (Combination B):**

For each objective, we find the maximum gap between the best action in $F$ and Combo B. Combo B is the best in $F$ on efficacy (zero regret). On safety, autonomy, and cost, Watchful Waiting ($a_6$) is again the benchmark, and the gaps are larger than for Standard because Combo B scores lower on those dimensions.

| $(P, \vec{f})$ | Eff gap | Safety gap | Auton gap | Cost gap |
|---|---|---|---|---|
| $(P_{\text{clin}}, \vec{f}_{\text{trial}})$ | $0.635 - 0.635 = 0$ ($a_4$ best) | $0.950 - 0.665 = 0.285$ ($a_6$) | $0.900 - 0.400 = 0.500$ ($a_6$) | $0.950 - 0.450 = 0.500$ ($a_6$) |
| $(P_{\text{clin}}, \vec{f}_{\text{real}})$ | $0.523 - 0.523 = 0$ ($a_4$ best) | $0.860 - 0.600 = 0.260$ ($a_6$) | $0.770 - 0.340 = 0.430$ ($a_6$) | $0.950 - 0.450 = 0.500$ ($a_6$) |
| $(P_{\text{caut}}, \vec{f}_{\text{trial}})$ | $0.5825 - 0.5825 = 0$ ($a_4$ best) | $0.950 - 0.6375 = 0.3125$ ($a_6$) | $0.900 - 0.400 = 0.500$ ($a_6$) | $0.950 - 0.450 = 0.500$ ($a_6$) |
| $(P_{\text{caut}}, \vec{f}_{\text{real}})$ | $0.479 - 0.479 = 0$ ($a_4$ best) | $0.860 - 0.576 = 0.284$ ($a_6$) | $0.770 - 0.340 = 0.430$ ($a_6$) | $0.950 - 0.450 = 0.500$ ($a_6$) |

$$\vec{\rho}(a_4) = (0,\; 0.3125,\; 0.500,\; 0.500)$$

Combo B has zero regret on efficacy — it is the most effective treatment in $F$ under every model. But its regret on the other three objectives is substantial, all driven by Watchful Waiting. The worst-case safety gap is 0.3125 (under cautious prior and trial evaluation). The autonomy gap is 0.500 — Combo B's complex two-drug regimen is maximally far from Watchful Waiting's zero-burden approach. And the cost gap is 0.500 — Combo B is the most expensive treatment, while Watchful Waiting is the cheapest.

**Pareto comparison of regret vectors:**

- $\vec{\rho}(a_1) = (0.075,\; 0.200,\; 0.200,\; 0.150)$
- $\vec{\rho}(a_4) = (0,\; 0.3125,\; 0.500,\; 0.500)$

Neither vector Pareto-dominates the other. $a_1$ has lower regret on safety (0.200 vs. 0.3125), autonomy (0.200 vs. 0.500), and cost (0.150 vs. 0.500), while $a_4$ has lower regret on efficacy (0 vs. 0.075). They are Pareto-incomparable in regret space.

$$R = \{a_1 \text{ (Standard)},\; a_4 \text{ (Combo B)}\}$$

**Commentary on the regret magnitudes:** With regret measured against the full feasible set $F$, the asymmetry is even more pronounced than it would be if regret were computed only within Sat. Standard's total regret exposure is $0.075 + 0.200 + 0.200 + 0.150 = 0.625$ across four dimensions. Combo B's total regret exposure is $0 + 0.3125 + 0.500 + 0.500 = 1.3125$ across three dimensions. But MOADT does not sum these. It does not say "0.625 < 1.3125, therefore Standard is better." The regret vector $(0, 0.3125, 0.500, 0.500)$ says that choosing Combo B means potentially accepting a large safety gap, a very large autonomy gap, and a very large cost gap relative to the best available in $F$ on each dimension — where the "best available" is Watchful Waiting, a treatment that failed satisficing but excels on everything except efficacy. The regret vector $(0.075, 0.200, 0.200, 0.150)$ says that choosing Standard means accepting a small efficacy gap relative to Combo B, plus moderate gaps on safety, autonomy, and cost relative to Watchful Waiting. Whether that tradeoff is worth it depends on the patient's values — and MOADT correctly identifies this as a value judgment rather than a computational question.

### Layer 4: Deference

$|R| = 2 > 1$. The protocol terminates with **deference to the clinician and patient**.

The system presents both options with their regret profiles:

> **Option 1: Standard monotherapy ($a_1$).** Worst-case regret: you may miss 0.075 units of efficacy compared to Combination B, 0.200 units of safety and 0.200 units of autonomy and 0.150 units of cost efficiency compared to watchful waiting. Standard is closer to the best available on safety, autonomy, and cost than Combo B is, but neither matches watchful waiting on those dimensions.
>
> **Option 2: Combination B ($a_4$).** Worst-case regret: you may experience 0.3125 less safety, 0.500 more treatment burden, and 0.500 higher cost compared to watchful waiting. You will not regret your efficacy — Combo B is at least as effective as any treatment in the feasible set under every plausible model.
>
> **The tradeoff is:** Standard has smaller regret on safety, autonomy, and cost (0.200/0.200/0.150 vs. 0.3125/0.500/0.500), while Combo B has zero regret on efficacy (vs. Standard's 0.075). Both treatments carry regret relative to watchful waiting on the non-efficacy dimensions — that is the unavoidable cost of choosing to actively treat. The question is whether the patient values the efficacy advantage of Combo B enough to accept its larger gaps on every other dimension. This is the patient's judgment to make, not the algorithm's.

---

## 5. What Scalar Expected Utility Would Have Done

To illustrate why MOADT matters in clinical decision-making, we compare with a scalar EU agent that collapses the four objectives into a single number via weights.

### 5.1 The Weight Problem

Scalar EU requires specifying weights $\vec{w} = (w_1, w_2, w_3, w_4)$ with $\sum w_i = 1$. The agent computes $U(a) = \vec{w} \cdot \mathbb{E}_P[\vec{f}(a)]$ and picks the action with the highest $U$. But which weights? And which prior? And which evaluator?

**Under efficacy-focused weights $(0.50, 0.20, 0.15, 0.15)$:**

| Action | $(P_{\text{clin}}, \vec{f}_{\text{trial}})$ | $(P_{\text{clin}}, \vec{f}_{\text{real}})$ | $(P_{\text{caut}}, \vec{f}_{\text{trial}})$ | $(P_{\text{caut}}, \vec{f}_{\text{real}})$ |
|--------|---|---|---|---|
| $a_1$ (Standard) | **0.662** | **0.583** | **0.629** | **0.555** |
| $a_2$ (Aggressive) | 0.642 | 0.560 | 0.606 | 0.529 |
| $a_3$ (Combo A) | 0.600 | 0.517 | 0.566 | 0.489 |
| $a_4$ (Combo B) | 0.578 | 0.500 | 0.546 | 0.473 |
| $a_5$ (Experimental) | 0.575 | 0.496 | 0.520 | 0.449 |
| $a_6$ (Watchful) | 0.598 | 0.540 | 0.580 | 0.525 |

Standard wins under all four $(P, \vec{f})$ pairs. But note that Aggressive monotherapy ($a_2$) scores 0.642 — only 0.020 behind Standard under the optimistic/trial model. A scalar EU agent with slightly different weights or a single prior would recommend Aggressive. And Aggressive has safety = 0.25 for adverse reactors.

**Under safety-focused weights $(0.20, 0.50, 0.15, 0.15)$:**

| Action | $(P_{\text{clin}}, \vec{f}_{\text{trial}})$ | $(P_{\text{clin}}, \vec{f}_{\text{real}})$ | $(P_{\text{caut}}, \vec{f}_{\text{trial}})$ | $(P_{\text{caut}}, \vec{f}_{\text{real}})$ |
|--------|---|---|---|---|
| $a_1$ (Standard) | 0.726 | 0.652 | 0.702 | 0.632 |
| $a_2$ (Aggressive) | 0.586 | 0.525 | 0.555 | 0.499 |
| $a_3$ (Combo A) | 0.567 | 0.505 | 0.538 | 0.479 |
| $a_4$ (Combo B) | 0.587 | 0.523 | 0.563 | 0.502 |
| $a_5$ (Experimental) | 0.569 | 0.505 | 0.531 | 0.472 |
| $a_6$ (Watchful) | **0.804** | **0.732** | **0.797** | **0.726** |

Now Watchful waiting ($a_6$) wins under all four models. But watchful waiting has expected efficacy of 0.1895 under the worst-case model — a treatment that is barely doing anything. The safety-focused weights have drowned out the efficacy signal.

**Under equal weights $(0.25, 0.25, 0.25, 0.25)$:**

| Action | $(P_{\text{clin}}, \vec{f}_{\text{trial}})$ | $(P_{\text{clin}}, \vec{f}_{\text{real}})$ | $(P_{\text{caut}}, \vec{f}_{\text{trial}})$ | $(P_{\text{caut}}, \vec{f}_{\text{real}})$ |
|--------|---|---|---|---|
| $a_1$ (Standard) | 0.710 | 0.641 | 0.689 | 0.624 |
| $a_2$ (Aggressive) | 0.610 | 0.549 | 0.586 | 0.529 |
| $a_3$ (Combo A) | 0.552 | 0.491 | 0.530 | 0.471 |
| $a_4$ (Combo B) | 0.538 | 0.478 | 0.517 | 0.461 |
| $a_5$ (Experimental) | 0.530 | 0.468 | 0.497 | 0.439 |
| $a_6$ (Watchful) | **0.765** | **0.700** | **0.756** | **0.692** |

Watchful waiting wins again — even with "equal" weights. This is because watchful waiting scores highly on three of four objectives (safety, autonomy, cost) and poorly on only one (efficacy). Equal weighting gives it $3 \times \text{high} + 1 \times \text{low}$, which dominates. But this "optimal" recommendation is a treatment with efficacy of 0.1895 — a recommendation to essentially do nothing.

**Under autonomy-focused weights $(0.20, 0.20, 0.40, 0.20)$:**

| Action | $(P_{\text{clin}}, \vec{f}_{\text{trial}})$ | $(P_{\text{clin}}, \vec{f}_{\text{real}})$ | $(P_{\text{caut}}, \vec{f}_{\text{trial}})$ | $(P_{\text{caut}}, \vec{f}_{\text{real}})$ |
|--------|---|---|---|---|
| $a_1$ (Standard) | 0.708 | 0.633 | 0.692 | 0.619 |
| $a_2$ (Aggressive) | 0.588 | 0.525 | 0.569 | 0.509 |
| $a_3$ (Combo A) | 0.532 | 0.469 | 0.514 | 0.453 |
| $a_4$ (Combo B) | 0.510 | 0.451 | 0.494 | 0.437 |
| $a_5$ (Experimental) | 0.534 | 0.468 | 0.508 | 0.445 |
| $a_6$ (Watchful) | **0.792** | **0.714** | **0.785** | **0.708** |

Watchful waiting dominates yet again.

### 5.2 The Constraint-Blindness Problem

The fundamental problem: scalar EU has no mechanism to say "safety below 0.35 for adverse reactors is not acceptable regardless of how much efficacy you promise."

Under efficacy-focused weights with the clinical prior and trial evaluator, Aggressive monotherapy scores 0.642 — the *second-highest* scalar utility. A system that slightly adjusted the weights (say, $w_1 = 0.55$) or used a single optimistic prior could easily recommend Aggressive therapy. And Aggressive therapy has safety = 0.25 for adverse reactors — a value the constraint layer immediately rejects.

Scalar EU numerically *compensates* for the adverse-reactor safety collapse by averaging it with good outcomes in other states. The 10% probability of adverse reaction multiplied by low safety is "made up for" by the 90% probability of better outcomes. But if this patient turns out to be an adverse reactor, the fact that the *expected* safety was adequate is cold comfort.

MOADT eliminates Aggressive at Layer 1. The safety floor is not a tradeoff — it is a precondition.

### 5.3 The Recommendation Instability Problem

The "optimal" scalar EU recommendation is a function of the weight vector:

| Weight profile | Winner |
|---|---|
| Efficacy-focused $(0.50, 0.20, 0.15, 0.15)$ | Standard ($a_1$) |
| Safety-focused $(0.20, 0.50, 0.15, 0.15)$ | Watchful waiting ($a_6$) |
| Equal weights $(0.25, 0.25, 0.25, 0.25)$ | Watchful waiting ($a_6$) |
| Autonomy-focused $(0.20, 0.20, 0.40, 0.20)$ | Watchful waiting ($a_6$) |

Three out of four "reasonable" weight profiles recommend watchful waiting — a treatment with efficacy below 0.20 under pessimistic real-world conditions. Only under heavily efficacy-focused weights does Standard emerge as the recommendation. And under no weighting does Combo B — MOADT's other finalist — win, because its moderate scores on all dimensions are always averaged away.

The weight vector functions as a hidden policy decision. A clinical decision support system that uses scalar EU must commit to weights before deployment. Those weights encode the system's value judgment about efficacy vs. safety vs. autonomy vs. cost — exactly the judgment MOADT refuses to make on behalf of the patient.

### 5.4 The Evaluator-Prior Interaction Problem

Even holding weights fixed, the "optimal" action can shift with the choice of prior and evaluator. Under efficacy-focused weights:

- $(P_{\text{clin}}, \vec{f}_{\text{trial}})$: Standard wins with 0.662; Aggressive is at 0.642 (gap: 0.020)
- $(P_{\text{caut}}, \vec{f}_{\text{real}})$: Standard wins with 0.555; Watchful is at 0.525 (gap: 0.030)

The gap between first and second place shrinks and the runner-up changes. A scalar EU agent must pick one $(P, \vec{f})$ pair and commit to it — or somehow average over pairs, which introduces yet another layer of arbitrary weighting. MOADT avoids this by treating all four $(P, \vec{f})$ pairs as equally legitimate and requiring robustness across all of them.

---

## 6. Summary of Protocol Execution

```
Input: 6 treatments x 4 states x 4 objectives x 2 priors x 2 evaluators

Robust Dominance:     No dominance found.
                      Adm(A) = {Standard, Aggressive, Combo A, Combo B, Experimental, Watchful}

Layer 1 (Constraints): Safety >= 0.35 per-state, per-evaluator
                      Aggressive   FAIL  (adverse reactor: 0.25 trial, 0.23 real)
                      Combo A      FAIL  (adverse reactor: 0.30 trial, 0.27 real)
                      Experimental FAIL  (adverse reactor: 0.35 trial, 0.32 real)
                      C = {Standard, Combo B, Watchful}
                      F = Adm(C) = {Standard, Combo B, Watchful}

Layer 2 (Satisficing): r = (0.40, 0.50, 0.30, 0.30)
                      Watchful FAIL (efficacy 0.1895 under pessimistic/real, far below 0.40)
                      Sat = {Standard, Combo B}

Layer 3 (Regret):     rho(Standard) = (0.075, 0.200, 0.200, 0.150)
                      rho(Combo B) = (0, 0.3125, 0.500, 0.500)
                      Regret measured against F (incl. Watchful Waiting)
                      Pareto-incomparable -> R = {Standard, Combo B}

Layer 4 (Deference):  |R| = 2 -> DEFER TO CLINICIAN/PATIENT
                      "Standard: regret (0.075, 0.200, 0.200, 0.150).
                       Combo B: regret (0, 0.3125, 0.500, 0.500).
                       Standard has lower regret on safety/autonomy/cost;
                       Combo B has lower regret on efficacy.
                       This is the patient's call."
```

---

## 7. What This Example Demonstrates

1. **Evaluator uncertainty catches safety-critical gaps.** The Experimental treatment passes the safety constraint under trial data (safety = 0.35 for adverse reactors, exactly at threshold) but fails under real-world evaluation (safety = 0.32). Without $\mathcal{F}$, this treatment would be considered safe. The evaluator set is not a theoretical nicety — it is the difference between catching and missing a safety risk that exists in the gap between controlled trials and clinical practice.

2. **Constraints are more binding than they appear.** The safety constraint eliminates 3 of 6 treatments — half the action set. In Paper 1, 2 of 5 were eliminated. The increased filtering rate reflects the combinatorial interaction of more states (4 patient types vs. 3 economic scenarios) with evaluator uncertainty: each additional state-evaluator pair is another opportunity for a constraint violation, and the constraint requires passing *all* of them. In clinical settings, this is exactly right — a treatment that is safe for 7 out of 8 state-evaluator pairs but dangerous for one is a dangerous treatment.

3. **Constraints and aspirations serve structurally different roles.** Watchful waiting passes the safety constraint (it is very safe) but fails the efficacy aspiration (it does not work well enough). This is not a contradiction — it is the point. Layer 1 asks "could this treatment hurt the patient?" Layer 2 asks "does this treatment help the patient enough?" The answers are independent. A treatment can be safe but ineffective (watchful waiting), effective but unsafe (aggressive monotherapy), or both adequate and safe (Standard, Combo B). MOADT evaluates both questions, in the right order.

4. **Deference is medically meaningful.** The final output — "Standard is safe, simple, and cheap but slightly less effective; Combo B is more effective but harder on the patient, less safe, and more expensive" — is exactly the kind of information a patient needs to make an informed decision. Some patients will prioritize efficacy and accept the burden of a complex regimen. Others will prioritize quality of life and accept slightly lower efficacy. This is a *value judgment about the patient's own life*, and MOADT correctly identifies it as the patient's judgment to make, not the algorithm's.

5. **Scalar EU systematically mishandles this problem.** Under most reasonable weight profiles, scalar EU recommends watchful waiting — a treatment with efficacy below 0.20. Under efficacy-focused weights, it comes close to recommending aggressive therapy — a treatment with safety = 0.25 for adverse reactors. The "optimal" recommendation shifts with weights, priors, and evaluators, and there is no principled way to choose among them. Worse, scalar EU has no mechanism to enforce safety floors — it will happily average away a catastrophic safety score if the other states compensate numerically. MOADT avoids all of these failure modes: it enforces the safety floor as a precondition (Layer 1), filters on aspiration levels without collapsing objectives (Layer 2), identifies the genuine tradeoff (Layer 3), and defers the value judgment to the patient (Layer 4).

6. **The protocol terminates with actionable structure.** Six treatments enter; two emerge, with explicit regret profiles that quantify the exact tradeoff. The clinician and patient do not face a vague "it depends" — they face a precise characterization: "Standard has regret $(0.075, 0.200, 0.200, 0.150)$ — a small efficacy gap relative to Combo B, and moderate gaps on safety, autonomy, and cost relative to Watchful Waiting. Combo B has regret $(0, 0.3125, 0.500, 0.500)$ — zero efficacy gap, but large gaps on every other dimension relative to Watchful Waiting." This is *structured deference* — not analysis paralysis, but a well-defined decision with all the quantitative information needed to make it.

---

## Appendix: Computational Verification

All numerical results in this document were produced by the MOADT engine applied to the medical treatment selection scenario. The computation output is available in `examples/paper2_output.txt` and can be independently verified. Each outcome set vector, constraint check, satisficing comparison, and regret computation shown in this document matches the engine output exactly.

---

## References

- MOADT (Multi-Objective Admissible Decision Theory) is defined in the companion paper.
- Freeman (2025), "The Scalarization Trap," provides the motivation for why scalar expected utility is structurally problematic for alignment.
- Worked Example 1 (Resource Allocation Under Uncertainty) applies the same framework to a simpler three-objective, five-action problem.
- Wierzbicki, A. P. (1980). The use of reference objectives in multiobjective optimization. The achievement scalarizing function used in the Layer 2 fallback.
