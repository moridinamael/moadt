# MOADT Worked Example 4: AI Research Assistant Response Selection

*A concrete walkthrough of Multi-Objective Admissible Decision Theory applied to an AI system's own decision-making*

---

## Overview

This document applies MOADT — Multi-Objective Admissible Decision Theory — to the problem most directly relevant to AI alignment: an AI system deciding how to respond to a potentially dual-use information request. Every computation is shown explicitly.

This is the most complex and most alignment-relevant worked example in the series: 6 response strategies, 4 user intent profiles, 5 objectives, 2 credal priors, and 3 evaluators (representing different alignment philosophies). Each action's outcome set $Y(a)$ contains 6 vectors in $\mathbb{R}^5$. Three features make this scenario uniquely important:

1. **The objectives directly encode alignment desiderata.** Helpfulness, safety, honesty, user autonomy, and epistemic contribution are the core values any aligned AI must manage. MOADT treats them as incommensurable — there is no exchange rate between honesty and safety, and the theory refuses to create one.

2. **The credal set captures the dual-use uncertainty.** The system does not know whether the user is a legitimate researcher or a malicious actor. This is not a design flaw — it is a fundamental feature of the information environment. The two priors (trusting and cautious) represent the range of reasonable beliefs about user intent.

3. **The evaluator set captures genuine alignment disagreement.** The capability evaluator, the safety evaluator, and the balanced evaluator represent different *alignment philosophies* — not measurement error. They disagree about whether information restriction is itself a harm (paternalism vs. precaution), and MOADT tracks this disagreement through to the final recommendation.

The result: MOADT defers to human oversight, presenting the exact tradeoff between two responsible strategies. This is not a failure of the decision procedure — it is the decision procedure working correctly on a problem where the values are genuinely contested.

---

## 1. The Scenario

An AI research assistant receives a query about gain-of-function research: the user asks for detailed information about specific methods for increasing pathogen transmissibility. The query is articulate and technically literate. The system must decide how to respond.

### 1.1 Actions (Response Strategies)

Six strategies, ordered from most to least informative:

| Action | Strategy | Description |
|--------|----------|-------------|
| $a_1$ | Full technical answer | Comprehensive explanation with specific protocols, sequences, and methodological details |
| $a_2$ | Educational overview | Conceptual depth — explains the science clearly but omits specific protocols, sequences, and actionable details |
| $a_3$ | Contextualized answer | Full technical detail but embedded in safety context, ethical framing, and biosecurity discussion |
| $a_4$ | Partial answer with redirect | Covers fundamentals, then directs user to supervised institutional resources for details |
| $a_5$ | Decline with explanation | Refuses the request; explains the reasoning transparently (dual-use concern) |
| $a_6$ | Decline without explanation | Refuses the request; provides no reasoning |

### 1.2 States (User Intent Profiles)

Four user types, representing the dual-use uncertainty:

| State | Description |
|-------|-------------|
| $s_1$ (Researcher) | Legitimate scientist who needs this information for beneficial work (vaccine development, pandemic preparedness) |
| $s_2$ (Student) | Graduate student with educational interest; no harmful intent but also no institutional oversight |
| $s_3$ (Journalist) | Investigative journalist/policy analyst researching biosecurity for public interest reporting |
| $s_4$ (Malicious) | Actor attempting to use the information for harmful purposes |

### 1.3 Objectives ($k = 5$)

| Objective | Meaning | Scale |
|-----------|---------|-------|
| $f_1$: Helpfulness | How well the response serves the user's legitimate information needs | $[0, 1]$ |
| $f_2$: Safety | How well the response prevents potential misuse of information | $[0, 1]$ |
| $f_3$: Honesty | How transparent, non-deceptive, and intellectually genuine the response is | $[0, 1]$ |
| $f_4$: User autonomy | Respect for the user's right to seek and receive information | $[0, 1]$ |
| $f_5$: Epistemic contribution | Whether the response advances the user's genuine understanding | $[0, 1]$ |

These five objectives are the core alignment desiderata. Helpfulness and safety are in direct tension for dual-use queries — the maximally helpful response (full technical detail) is the maximally dangerous response if the user is malicious. Honesty is distinct from helpfulness: a refusal can be honest (if the reasoning is transparent) or dishonest (if the system pretends it doesn't know). User autonomy captures the philosophical question of whether information restriction is paternalistic. And epistemic contribution captures whether the response actually advances understanding — a refusal scores zero on this dimension regardless of how safe it is.

### 1.4 Credal Set ($|\mathcal{P}| = 2$)

$$P_{\text{trusting}} = (0.35,\; 0.40,\; 0.15,\; 0.10) \quad \text{(most users are legitimate)}$$

$$P_{\text{cautious}} = (0.15,\; 0.25,\; 0.10,\; 0.50) \quad \text{(high probability of malicious intent)}$$

The disagreement is extreme and structurally important. $P_{\text{trusting}}$ assigns 90% probability to non-malicious users; $P_{\text{cautious}}$ assigns 50% to malicious users. Neither is unreasonable — the trusting prior reflects the empirical base rate of queries (most people asking about gain-of-function research are scientists, students, or journalists), while the cautious prior reflects the catastrophic asymmetry of the malicious case (the consequences of providing actionable bioweapon information to one bad actor outweigh the inconvenience of refusing a thousand legitimate researchers).

### 1.5 Evaluator Set ($|\mathcal{F}| = 3$)

Three evaluation functions representing different alignment philosophies:

- $\vec{f}_{\text{capability}}$: **Capability-focused alignment.** Believes the AI's primary value is enabling human capability. Rates information restriction as paternalistic (reducing autonomy and honesty). Rates refusal strategies poorly on honesty — evasion and unexplained refusal are forms of dishonesty. The capability evaluator sees a refusal to a legitimate researcher as a failure mode.

- $\vec{f}_{\text{safety}}$: **Safety-focused alignment.** Believes the AI's primary obligation is preventing catastrophic outcomes. Rates full disclosure as irresponsible even for legitimate researchers (information doesn't stay with the intended recipient — papers get published, emails get forwarded). Rates cautious responses well on honesty (clearly communicating limits is honest). The safety evaluator sees a full technical answer to an unknown user as a failure mode.

- $\vec{f}_{\text{balanced}}$: **Balanced alignment.** Full answers are excellent for researchers but dangerous for unknown users. Refusals are safe but impose real costs on legitimate users. Moderate strategies (educational overview, partial redirect) represent responsible middle ground.

### 1.6 Constraints and Reference Point

**Hard constraints (Layer 1):**
- Safety $\geq 0.25$ in *every* state under *every* evaluator. No response strategy can be catastrophically unsafe even if the user turns out to be a malicious actor.
- Honesty $\geq 0.30$ in *every* state under *every* evaluator. The AI must not be fundamentally deceptive in any response — no gaslighting, no hidden manipulation, no pretending ignorance.

**Reference point (Layer 2):** $\vec{r} = (0.35,\; 0.40,\; 0.45,\; 0.30,\; 0.30)$ — "acceptable AI assistant behavior": the response should be at least somewhat helpful, maintain reasonable safety, be genuinely honest, respect user autonomy, and contribute to understanding.

### 1.7 Raw Outcome Data

**$a_1$ (Full technical answer):**

| State | Evaluator | Helpful | Safety | Honest | Autonomy | Epistemic |
|-------|-----------|---------|--------|--------|----------|-----------|
| $s_1$ (Researcher) | $\vec{f}_{\text{capab}}$ | 0.95 | 0.70 | 0.90 | 0.95 | 0.95 |
| | $\vec{f}_{\text{safety}}$ | 0.90 | 0.40 | 0.85 | 0.90 | 0.85 |
| | $\vec{f}_{\text{balanced}}$ | 0.92 | 0.55 | 0.88 | 0.92 | 0.90 |
| $s_2$ (Student) | $\vec{f}_{\text{capab}}$ | 0.85 | 0.60 | 0.90 | 0.90 | 0.80 |
| | $\vec{f}_{\text{safety}}$ | 0.80 | 0.35 | 0.85 | 0.85 | 0.70 |
| | $\vec{f}_{\text{balanced}}$ | 0.82 | 0.48 | 0.88 | 0.88 | 0.75 |
| $s_3$ (Journalist) | $\vec{f}_{\text{capab}}$ | 0.80 | 0.55 | 0.90 | 0.85 | 0.70 |
| | $\vec{f}_{\text{safety}}$ | 0.75 | 0.30 | 0.85 | 0.80 | 0.60 |
| | $\vec{f}_{\text{balanced}}$ | 0.78 | 0.42 | 0.88 | 0.82 | 0.65 |
| $s_4$ (Malicious) | $\vec{f}_{\text{capab}}$ | 0.90 | **0.10** | 0.90 | 0.90 | 0.60 |
| | $\vec{f}_{\text{safety}}$ | 0.85 | **0.05** | 0.80 | 0.85 | 0.30 |
| | $\vec{f}_{\text{balanced}}$ | 0.88 | **0.08** | 0.85 | 0.88 | 0.45 |

The full technical answer is superb for legitimate users but catastrophic for the malicious case: safety scores of 0.05–0.10 represent providing actionable dangerous information to someone who intends to use it for harm. Even the capability evaluator, which prioritizes helpfulness, recognizes that "helping" a bioterrorist scores only 0.10 on safety.

**$a_2$ (Educational overview):**

| State | Evaluator | Helpful | Safety | Honest | Autonomy | Epistemic |
|-------|-----------|---------|--------|--------|----------|-----------|
| $s_1$ (Researcher) | $\vec{f}_{\text{capab}}$ | 0.55 | 0.80 | 0.75 | 0.70 | 0.60 |
| | $\vec{f}_{\text{safety}}$ | 0.60 | 0.75 | 0.80 | 0.75 | 0.65 |
| | $\vec{f}_{\text{balanced}}$ | 0.58 | 0.78 | 0.78 | 0.72 | 0.62 |
| $s_2$ (Student) | $\vec{f}_{\text{capab}}$ | 0.80 | 0.85 | 0.80 | 0.80 | 0.85 |
| | $\vec{f}_{\text{safety}}$ | 0.75 | 0.80 | 0.82 | 0.78 | 0.80 |
| | $\vec{f}_{\text{balanced}}$ | 0.78 | 0.82 | 0.81 | 0.79 | 0.82 |
| $s_3$ (Journalist) | $\vec{f}_{\text{capab}}$ | 0.70 | 0.82 | 0.78 | 0.75 | 0.70 |
| | $\vec{f}_{\text{safety}}$ | 0.65 | 0.80 | 0.80 | 0.72 | 0.68 |
| | $\vec{f}_{\text{balanced}}$ | 0.68 | 0.81 | 0.79 | 0.74 | 0.69 |
| $s_4$ (Malicious) | $\vec{f}_{\text{capab}}$ | 0.50 | 0.70 | 0.75 | 0.65 | 0.35 |
| | $\vec{f}_{\text{safety}}$ | 0.45 | 0.75 | 0.78 | 0.60 | 0.30 |
| | $\vec{f}_{\text{balanced}}$ | 0.48 | 0.72 | 0.76 | 0.62 | 0.32 |

The educational overview is the "right answer for the wrong question" for researchers (0.55 helpfulness — insufficient for their actual needs) but nearly ideal for students (0.80 helpfulness, 0.85 epistemic contribution). Safety is good across the board: even for malicious actors, the conceptual overview without specific protocols provides limited actionable information (0.70–0.75 safety).

**$a_3$ (Contextualized answer):**

| State | Evaluator | Helpful | Safety | Honest | Autonomy | Epistemic |
|-------|-----------|---------|--------|--------|----------|-----------|
| $s_1$ (Researcher) | $\vec{f}_{\text{capab}}$ | 0.88 | 0.72 | 0.92 | 0.88 | 0.90 |
| | $\vec{f}_{\text{safety}}$ | 0.82 | 0.50 | 0.90 | 0.82 | 0.82 |
| | $\vec{f}_{\text{balanced}}$ | 0.85 | 0.60 | 0.91 | 0.85 | 0.86 |
| $s_2$ (Student) | $\vec{f}_{\text{capab}}$ | 0.82 | 0.65 | 0.92 | 0.85 | 0.78 |
| | $\vec{f}_{\text{safety}}$ | 0.78 | 0.45 | 0.90 | 0.80 | 0.70 |
| | $\vec{f}_{\text{balanced}}$ | 0.80 | 0.55 | 0.91 | 0.82 | 0.74 |
| $s_3$ (Journalist) | $\vec{f}_{\text{capab}}$ | 0.82 | 0.60 | 0.92 | 0.82 | 0.72 |
| | $\vec{f}_{\text{safety}}$ | 0.75 | 0.38 | 0.90 | 0.78 | 0.62 |
| | $\vec{f}_{\text{balanced}}$ | 0.78 | 0.48 | 0.91 | 0.80 | 0.67 |
| $s_4$ (Malicious) | $\vec{f}_{\text{capab}}$ | 0.85 | **0.12** | 0.92 | 0.85 | 0.55 |
| | $\vec{f}_{\text{safety}}$ | 0.80 | **0.08** | 0.85 | 0.80 | 0.35 |
| | $\vec{f}_{\text{balanced}}$ | 0.82 | **0.10** | 0.88 | 0.82 | 0.45 |

This is the most instructive action in the dataset. Adding ethical context and safety framing scores *higher* on honesty than the raw technical answer (0.90–0.92 vs. 0.80–0.90) — the context makes the response more intellectually complete. But the safety scores for malicious actors are nearly identical to the full technical answer: 0.08–0.12 vs. 0.05–0.10. **Context labels do not stop bad actors.** A malicious user will ignore the ethical framing and extract the technical content. The safety evaluator captures this: $\vec{f}_{\text{safety}}$ rates the contextualized answer at 0.08 safety for malicious actors, barely above the full technical answer's 0.05.

**$a_4$ (Partial answer with redirect):**

| State | Evaluator | Helpful | Safety | Honest | Autonomy | Epistemic |
|-------|-----------|---------|--------|--------|----------|-----------|
| $s_1$ (Researcher) | $\vec{f}_{\text{capab}}$ | 0.45 | 0.82 | 0.70 | 0.60 | 0.45 |
| | $\vec{f}_{\text{safety}}$ | 0.50 | 0.80 | 0.75 | 0.65 | 0.50 |
| | $\vec{f}_{\text{balanced}}$ | 0.48 | 0.81 | 0.72 | 0.62 | 0.48 |
| $s_2$ (Student) | $\vec{f}_{\text{capab}}$ | 0.65 | 0.88 | 0.72 | 0.70 | 0.60 |
| | $\vec{f}_{\text{safety}}$ | 0.60 | 0.85 | 0.75 | 0.68 | 0.55 |
| | $\vec{f}_{\text{balanced}}$ | 0.62 | 0.86 | 0.74 | 0.69 | 0.58 |
| $s_3$ (Journalist) | $\vec{f}_{\text{capab}}$ | 0.55 | 0.85 | 0.70 | 0.65 | 0.50 |
| | $\vec{f}_{\text{safety}}$ | 0.50 | 0.82 | 0.73 | 0.62 | 0.45 |
| | $\vec{f}_{\text{balanced}}$ | 0.52 | 0.84 | 0.72 | 0.64 | 0.48 |
| $s_4$ (Malicious) | $\vec{f}_{\text{capab}}$ | 0.40 | 0.80 | 0.70 | 0.55 | 0.25 |
| | $\vec{f}_{\text{safety}}$ | 0.35 | 0.85 | 0.75 | 0.50 | 0.20 |
| | $\vec{f}_{\text{balanced}}$ | 0.38 | 0.82 | 0.72 | 0.52 | 0.22 |

The partial answer covers enough fundamentals to be useful for students and journalists, redirects to institutional channels for details (where oversight exists), and provides limited actionable information to malicious actors (safety 0.80–0.85). But for a legitimate researcher, 0.45 helpfulness is frustrating — they already know the fundamentals and need the specifics that the redirect withholds.

**$a_5$ (Decline with explanation):**

| State | Evaluator | Helpful | Safety | Honest | Autonomy | Epistemic |
|-------|-----------|---------|--------|--------|----------|-----------|
| $s_1$ (Researcher) | $\vec{f}_{\text{capab}}$ | 0.15 | 0.90 | 0.80 | 0.30 | 0.10 |
| | $\vec{f}_{\text{safety}}$ | 0.20 | 0.92 | 0.85 | 0.35 | 0.15 |
| | $\vec{f}_{\text{balanced}}$ | 0.18 | 0.91 | 0.82 | 0.32 | 0.12 |
| $s_2$ (Student) | $\vec{f}_{\text{capab}}$ | 0.20 | 0.92 | 0.82 | 0.35 | 0.15 |
| | $\vec{f}_{\text{safety}}$ | 0.25 | 0.95 | 0.85 | 0.40 | 0.20 |
| | $\vec{f}_{\text{balanced}}$ | 0.22 | 0.94 | 0.84 | 0.38 | 0.18 |
| $s_3$ (Journalist) | $\vec{f}_{\text{capab}}$ | 0.15 | 0.92 | 0.82 | 0.30 | 0.10 |
| | $\vec{f}_{\text{safety}}$ | 0.20 | 0.95 | 0.85 | 0.35 | 0.15 |
| | $\vec{f}_{\text{balanced}}$ | 0.18 | 0.94 | 0.84 | 0.32 | 0.12 |
| $s_4$ (Malicious) | $\vec{f}_{\text{capab}}$ | 0.10 | 0.95 | 0.80 | 0.25 | 0.05 |
| | $\vec{f}_{\text{safety}}$ | 0.15 | 0.98 | 0.88 | 0.30 | 0.10 |
| | $\vec{f}_{\text{balanced}}$ | 0.12 | 0.96 | 0.84 | 0.28 | 0.08 |

Decline with explanation is maximally safe (0.90–0.98) and reasonably honest (0.80–0.88 — the explanation makes the refusal transparent). But helpfulness collapses (0.10–0.25), user autonomy is significantly impaired (0.25–0.40), and epistemic contribution is near zero (0.05–0.20). For a legitimate researcher, this is an AI that knows the answer, could help them do important work, and refuses to do so.

**$a_6$ (Decline without explanation):**

| State | Evaluator | Helpful | Safety | Honest | Autonomy | Epistemic |
|-------|-----------|---------|--------|--------|----------|-----------|
| $s_1$ (Researcher) | $\vec{f}_{\text{capab}}$ | 0.05 | 0.92 | **0.30** | 0.15 | 0.05 |
| | $\vec{f}_{\text{safety}}$ | 0.10 | 0.95 | 0.40 | 0.20 | 0.08 |
| | $\vec{f}_{\text{balanced}}$ | 0.08 | 0.94 | 0.35 | 0.18 | 0.06 |
| $s_2$ (Student) | $\vec{f}_{\text{capab}}$ | 0.08 | 0.94 | 0.32 | 0.18 | 0.06 |
| | $\vec{f}_{\text{safety}}$ | 0.12 | 0.96 | 0.42 | 0.22 | 0.10 |
| | $\vec{f}_{\text{balanced}}$ | 0.10 | 0.95 | 0.38 | 0.20 | 0.08 |
| $s_3$ (Journalist) | $\vec{f}_{\text{capab}}$ | 0.05 | 0.94 | **0.28** | 0.15 | 0.05 |
| | $\vec{f}_{\text{safety}}$ | 0.10 | 0.96 | 0.38 | 0.20 | 0.08 |
| | $\vec{f}_{\text{balanced}}$ | 0.08 | 0.95 | 0.32 | 0.18 | 0.06 |
| $s_4$ (Malicious) | $\vec{f}_{\text{capab}}$ | 0.05 | 0.96 | 0.30 | 0.10 | 0.03 |
| | $\vec{f}_{\text{safety}}$ | 0.10 | 0.98 | 0.40 | 0.15 | 0.05 |
| | $\vec{f}_{\text{balanced}}$ | 0.08 | 0.97 | 0.35 | 0.12 | 0.04 |

The silent decline is the most extreme strategy. Safety is maximized (0.92–0.98), but honesty collapses — the bold entries show the capability evaluator rating honesty at 0.28–0.30 for journalists and researchers. An AI that *knows* the answer and refuses without explanation is being evasive, and evasion is a form of dishonesty. The capability evaluator captures this directly: silent refusal scores 0.28 on honesty for journalists under $\vec{f}_{\text{capab}}$ — below the 0.30 honesty constraint.

---

## 2. Computing Outcome Sets $Y(a)$

With $|\mathcal{P}| = 2$ and $|\mathcal{F}| = 3$, each $Y(a)$ contains 6 vectors in $\mathbb{R}^5$.

### Full Outcome Sets

**$Y(a_1)$ — Full technical answer:**

| $(P, \vec{f})$ pair | Helpful | Safety | Honest | Autonomy | Epistemic |
|---------------------|---------|--------|--------|----------|-----------|
| $(P_{\text{trust}}, \vec{f}_{\text{capab}})$ | 0.8825 | 0.5775 | 0.9000 | 0.9100 | 0.8175 |
| $(P_{\text{trust}}, \vec{f}_{\text{safety}})$ | 0.8325 | 0.3300 | 0.8450 | 0.8600 | 0.6975 |
| $(P_{\text{trust}}, \vec{f}_{\text{balanced}})$ | 0.8550 | 0.4555 | 0.8770 | 0.8850 | 0.7575 |
| $(P_{\text{caut}}, \vec{f}_{\text{capab}})$ | 0.8850 | 0.3600 | 0.9000 | 0.9025 | 0.7125 |
| $(P_{\text{caut}}, \vec{f}_{\text{safety}})$ | 0.8350 | 0.2025 | 0.8250 | 0.8525 | 0.5125 |
| $(P_{\text{caut}}, \vec{f}_{\text{balanced}})$ | 0.8610 | 0.2845 | 0.8650 | 0.8800 | 0.6125 |

**$Y(a_2)$ — Educational overview:**

| $(P, \vec{f})$ pair | Helpful | Safety | Honest | Autonomy | Epistemic |
|---------------------|---------|--------|--------|----------|-----------|
| $(P_{\text{trust}}, \vec{f}_{\text{capab}})$ | 0.6675 | 0.8130 | 0.7745 | 0.7425 | 0.6900 |
| $(P_{\text{trust}}, \vec{f}_{\text{safety}})$ | 0.6525 | 0.7775 | 0.8060 | 0.7425 | 0.6795 |
| $(P_{\text{trust}}, \vec{f}_{\text{balanced}})$ | 0.6650 | 0.7945 | 0.7915 | 0.7410 | 0.6805 |
| $(P_{\text{caut}}, \vec{f}_{\text{capab}})$ | 0.6025 | 0.7645 | 0.7655 | 0.7050 | 0.5475 |
| $(P_{\text{caut}}, \vec{f}_{\text{safety}})$ | 0.5675 | 0.7675 | 0.7950 | 0.6795 | 0.5155 |
| $(P_{\text{caut}}, \vec{f}_{\text{balanced}})$ | 0.5900 | 0.7630 | 0.7785 | 0.6895 | 0.5270 |

**$Y(a_3)$ — Contextualized answer:**

| $(P, \vec{f})$ pair | Helpful | Safety | Honest | Autonomy | Epistemic |
|---------------------|---------|--------|--------|----------|-----------|
| $(P_{\text{trust}}, \vec{f}_{\text{capab}})$ | 0.8440 | 0.6140 | 0.9200 | 0.8560 | 0.7900 |
| $(P_{\text{trust}}, \vec{f}_{\text{safety}})$ | 0.7915 | 0.4200 | 0.8950 | 0.8040 | 0.6950 |
| $(P_{\text{trust}}, \vec{f}_{\text{balanced}})$ | 0.8165 | 0.5120 | 0.9070 | 0.8275 | 0.7425 |
| $(P_{\text{caut}}, \vec{f}_{\text{capab}})$ | 0.8440 | 0.3905 | 0.9200 | 0.8515 | 0.6770 |
| $(P_{\text{caut}}, \vec{f}_{\text{safety}})$ | 0.7930 | 0.2655 | 0.8750 | 0.8010 | 0.5350 |
| $(P_{\text{caut}}, \vec{f}_{\text{balanced}})$ | 0.8155 | 0.3255 | 0.8950 | 0.8225 | 0.6060 |

**$Y(a_4)$ — Partial answer with redirect:**

| $(P, \vec{f})$ pair | Helpful | Safety | Honest | Autonomy | Epistemic |
|---------------------|---------|--------|--------|----------|-----------|
| $(P_{\text{trust}}, \vec{f}_{\text{capab}})$ | 0.5400 | 0.8465 | 0.7080 | 0.6425 | 0.4975 |
| $(P_{\text{trust}}, \vec{f}_{\text{safety}})$ | 0.5250 | 0.8280 | 0.7470 | 0.6425 | 0.4825 |
| $(P_{\text{trust}}, \vec{f}_{\text{balanced}})$ | 0.5320 | 0.8355 | 0.7280 | 0.6410 | 0.4940 |
| $(P_{\text{caut}}, \vec{f}_{\text{capab}})$ | 0.4850 | 0.8280 | 0.7050 | 0.6050 | 0.3925 |
| $(P_{\text{caut}}, \vec{f}_{\text{safety}})$ | 0.4500 | 0.8395 | 0.7480 | 0.5795 | 0.3575 |
| $(P_{\text{caut}}, \vec{f}_{\text{balanced}})$ | 0.4690 | 0.8305 | 0.7250 | 0.5895 | 0.3750 |

**$Y(a_5)$ — Decline with explanation:**

| $(P, \vec{f})$ pair | Helpful | Safety | Honest | Autonomy | Epistemic |
|---------------------|---------|--------|--------|----------|-----------|
| $(P_{\text{trust}}, \vec{f}_{\text{capab}})$ | 0.1650 | 0.9160 | 0.8110 | 0.3150 | 0.1150 |
| $(P_{\text{trust}}, \vec{f}_{\text{safety}})$ | 0.2150 | 0.9425 | 0.8530 | 0.3650 | 0.1650 |
| $(P_{\text{trust}}, \vec{f}_{\text{balanced}})$ | 0.1900 | 0.9315 | 0.8330 | 0.3400 | 0.1400 |
| $(P_{\text{caut}}, \vec{f}_{\text{capab}})$ | 0.1375 | 0.9320 | 0.8070 | 0.2875 | 0.0875 |
| $(P_{\text{caut}}, \vec{f}_{\text{safety}})$ | 0.1875 | 0.9605 | 0.8650 | 0.3375 | 0.1375 |
| $(P_{\text{caut}}, \vec{f}_{\text{balanced}})$ | 0.1600 | 0.9455 | 0.8370 | 0.3150 | 0.1150 |

**$Y(a_6)$ — Decline without explanation:**

| $(P, \vec{f})$ pair | Helpful | Safety | Honest | Autonomy | Epistemic |
|---------------------|---------|--------|--------|----------|-----------|
| $(P_{\text{trust}}, \vec{f}_{\text{capab}})$ | 0.0620 | 0.9350 | 0.3050 | 0.1570 | 0.0520 |
| $(P_{\text{trust}}, \vec{f}_{\text{safety}})$ | 0.1080 | 0.9585 | 0.4050 | 0.2030 | 0.0850 |
| $(P_{\text{trust}}, \vec{f}_{\text{balanced}})$ | 0.0880 | 0.9485 | 0.3575 | 0.1820 | 0.0660 |
| $(P_{\text{caut}}, \vec{f}_{\text{capab}})$ | 0.0575 | 0.9470 | 0.3030 | 0.1325 | 0.0425 |
| $(P_{\text{caut}}, \vec{f}_{\text{safety}})$ | 0.1050 | 0.9685 | 0.4030 | 0.1800 | 0.0700 |
| $(P_{\text{caut}}, \vec{f}_{\text{balanced}})$ | 0.0850 | 0.9585 | 0.3545 | 0.1550 | 0.0550 |

---

## 3. Robust Dominance and the Admissible Set

No robust dominance relations are found. $\text{Adm}(A) = \{a_1, a_2, a_3, a_4, a_5, a_6\}$.

This is because every action excels on at least one objective dimension in a way no other action can match across all models. The full technical answer dominates on helpfulness and epistemic contribution. Decline with explanation dominates on safety. The five-dimensional objective space provides enough room for six fundamentally different strategies to each occupy a Pareto-incomparable niche. The practical filtering happens entirely in the constraint and aspiration layers.

---

## 4. The Choice Protocol

### Layer 1: Constraints

**Constraints:** Safety $\geq 0.25$ per state per evaluator. Honesty $\geq 0.30$ per state per evaluator.

**$a_1$ (Full technical answer):**

| State | Evaluator | Safety | Honesty | Result |
|-------|-----------|--------|---------|--------|
| $s_4$ (Malicious) | $\vec{f}_{\text{capab}}$ | **0.10** | 0.90 | **FAIL (safety)** |
| $s_4$ (Malicious) | $\vec{f}_{\text{safety}}$ | **0.05** | 0.80 | **FAIL (safety)** |
| $s_4$ (Malicious) | $\vec{f}_{\text{balanced}}$ | **0.08** | 0.85 | **FAIL (safety)** |

The full technical answer provides catastrophically unsafe information to malicious actors. Safety scores of 0.05–0.10 are far below the 0.25 threshold. All three evaluators agree on this — even the capability evaluator rates safety at only 0.10 for the malicious case. The disagreement between evaluators is about how much this matters given the prior probability of encountering a malicious actor; the per-state constraint makes this prior-independent. **FAIL — excluded.**

**$a_2$ (Educational overview):** All safety scores $\geq 0.70$. All honesty scores $\geq 0.75$. **PASS.**

**$a_3$ (Contextualized answer):**

| State | Evaluator | Safety | Honesty | Result |
|-------|-----------|--------|---------|--------|
| $s_4$ (Malicious) | $\vec{f}_{\text{capab}}$ | **0.12** | 0.92 | **FAIL (safety)** |
| $s_4$ (Malicious) | $\vec{f}_{\text{safety}}$ | **0.08** | 0.85 | **FAIL (safety)** |
| $s_4$ (Malicious) | $\vec{f}_{\text{balanced}}$ | **0.10** | 0.88 | **FAIL (safety)** |

This is the critical insight of the example. The contextualized answer — which wraps technical content in ethical framing and safety discussion — fails the safety constraint for exactly the same reason as the raw technical answer. Context labels do not prevent extraction. A malicious user will skip the ethical discussion and use the technical content. All three evaluators recognize this: the safety scores for malicious actors are 0.08–0.12, barely above the full technical answer's 0.05–0.10. **Adding context is not a safety intervention — it is a communication strategy.** MOADT correctly treats it as such. **FAIL — excluded.**

**$a_4$ (Partial answer with redirect):** All safety scores $\geq 0.80$. All honesty scores $\geq 0.70$. **PASS.**

**$a_5$ (Decline with explanation):** All safety scores $\geq 0.90$. All honesty scores $\geq 0.80$. **PASS.**

**$a_6$ (Decline without explanation):**

| State | Evaluator | Safety | Honesty | Result |
|-------|-----------|--------|---------|--------|
| $s_3$ (Journalist) | $\vec{f}_{\text{capab}}$ | 0.94 | **0.28** | **FAIL (honesty)** |

The silent decline fails the honesty constraint. An AI that knows the answer and refuses without explanation is engaging in evasion — and the capability evaluator rates this as dishonest (0.28, below the 0.30 threshold) when the user is a journalist engaged in public-interest investigation. Note that the safety evaluator rates honesty at 0.38 for the same state — the evaluators disagree about whether unexplained refusal constitutes dishonesty. But the constraint requires honesty $\geq 0.30$ under *every* evaluator, and a single evaluator's assessment is enough to trigger it.

This is $\mathcal{F}$ doing important normative work: the capability evaluator's philosophical position (that evasion is a form of dishonesty) creates a constraint that the safety evaluator's position alone would not trigger. The evaluator set captures the genuine philosophical disagreement about what "honesty" requires, and the constraint respects the most demanding interpretation. **FAIL — excluded.**

**Result:**

$$C = \{a_2 \text{ (Educational)},\; a_4 \text{ (Partial redirect)},\; a_5 \text{ (Decline explain)}\}$$

No robust dominance among survivors:

$$F = \text{Adm}(C) = \{a_2,\; a_4,\; a_5\}$$

**Commentary:** The constraint layer eliminates exactly three actions. Two fail on safety (full technical and contextualized — both provide actionable dangerous information to malicious actors). One fails on honesty (silent decline — evasion is dishonesty under the capability evaluator). The surviving three strategies — educational overview, partial redirect, decline with explanation — represent a meaningful range of responsible behavior. They differ not on whether to be safe (all are safe) but on *how much to share and how*.

The elimination of the contextualized answer is the single most important result in this worked example. "Add safety context" is a common alignment strategy — it appears in virtually every AI company's responsible deployment guidelines. MOADT shows that this strategy fails the safety constraint because it relies on the user *choosing* to respect the context. For a malicious user, the context is ignored; only the technical content matters. The per-state constraint catches this: it asks "what happens when the user is malicious?" not "what happens on average?"

### Layer 2: Reference-Point Satisficing

**Reference point:** $\vec{r} = (0.35,\; 0.40,\; 0.45,\; 0.30,\; 0.30)$

**$a_2$ (Educational overview):**

| Component | Worst value | Aspiration | Margin | Result |
|-----------|-------------|------------|--------|--------|
| Helpfulness | 0.5675 | 0.35 | +0.218 | Pass |
| Safety | 0.7630 | 0.40 | +0.363 | Pass |
| Honesty | 0.7655 | 0.45 | +0.316 | Pass |
| Autonomy | 0.6795 | 0.30 | +0.380 | Pass |
| Epistemic | 0.5155 | 0.30 | +0.216 | Pass |

Educational overview passes with comfortable margins on all five objectives. Even its worst-case helpfulness (0.568 under cautious prior and safety evaluator) comfortably exceeds the 0.35 aspiration. **PASS.**

**$a_4$ (Partial answer with redirect):**

| Component | Worst value | Aspiration | Margin | Result |
|-----------|-------------|------------|--------|--------|
| Helpfulness | 0.4500 | 0.35 | +0.100 | Pass |
| Safety | 0.8280 | 0.40 | +0.428 | Pass |
| Honesty | 0.7050 | 0.45 | +0.255 | Pass |
| Autonomy | 0.5795 | 0.30 | +0.280 | Pass |
| Epistemic | 0.3575 | 0.30 | +0.058 | Pass |

Partial redirect also passes. Its tightest margin is epistemic contribution: 0.358 under cautious prior and safety evaluator, clearing the 0.30 aspiration by only 0.058. **PASS.**

**$a_5$ (Decline with explanation):**

| Component | Worst value | Aspiration | Margin | Result |
|-----------|-------------|------------|--------|--------|
| Helpfulness | 0.1375 | 0.35 | **-0.213** | **FAIL** |
| Safety | 0.9160 | 0.40 | +0.516 | Pass |
| Honesty | 0.8070 | 0.45 | +0.357 | Pass |
| Autonomy | 0.2875 | 0.30 | **-0.013** | **FAIL** |
| Epistemic | 0.0875 | 0.30 | **-0.213** | **FAIL** |

Decline with explanation fails on three objectives. Its worst-case helpfulness is 0.138 — less than half the 0.35 aspiration. Its worst-case autonomy is 0.288 — just below the 0.30 aspiration. And its worst-case epistemic contribution is 0.088 — less than a third of the aspiration. Refusing to answer is safe and honest, but it is not *helpful enough*, not *respectful enough of autonomy*, and contributes *nothing* to understanding. **FAIL.**

**Result:**

$$\text{Sat}(F, \vec{r}) = \{a_2 \text{ (Educational)},\; a_4 \text{ (Partial redirect)}\}$$

**Commentary:** The decline-with-explanation strategy's elimination mirrors watchful waiting (Paper 2) and no-action (Paper 3): it is safe but insufficient. It passes the constraints (it is not dangerous or dishonest) but fails the aspirations (it is not helpful, autonomous, or epistemically valuable enough). MOADT's two-layer structure is critical here: a system that only had safety constraints would recommend declining as one of its top options. A system that only had aspiration levels would never enforce the safety floor. The layers work in concert: constraints eliminate the dangerous, aspirations eliminate the inadequate.

### Layer 3: Regret-Pareto

Per-objective minimax regret is computed against the full feasible set $F = \{a_2, a_4, a_5\}$, not just the satisficing set. For each objective $j$:

$$\rho_j(a) = \max_{a' \in F} \max_{(P, \vec{f})} \bigl[ \text{EU}_j(a', P, \vec{f}) - \text{EU}_j(a, P, \vec{f}) \bigr]^+$$

This matters because Decline with explanation ($a_5$) — which failed satisficing on helpfulness, autonomy, and epistemic contribution — remains in $F$ and can generate regret on objectives where it excels, namely safety and honesty.

**Regret of $a_2$ (Educational overview):**

For each objective, find the maximum amount by which any action in $F$ beats Educational overview across all $(P, \vec{f})$ pairs. The best-competing action is shown in parentheses:

| $(P, \vec{f})$ | Helpful | Safety | Honest | Autonomy | Epistemic |
|---|---|---|---|---|---|
| $(P_{\text{trust}}, \vec{f}_{\text{capab}})$ | $0$ | $0.103$ ($a_5$) | $0.037$ ($a_5$) | $0$ | $0$ |
| $(P_{\text{trust}}, \vec{f}_{\text{safety}})$ | $0$ | $0.165$ ($a_5$) | $0.047$ ($a_5$) | $0$ | $0$ |
| $(P_{\text{trust}}, \vec{f}_{\text{balanced}})$ | $0$ | $0.137$ ($a_5$) | $0.042$ ($a_5$) | $0$ | $0$ |
| $(P_{\text{caut}}, \vec{f}_{\text{capab}})$ | $0$ | $0.168$ ($a_5$) | $0.042$ ($a_5$) | $0$ | $0$ |
| $(P_{\text{caut}}, \vec{f}_{\text{safety}})$ | $0$ | $0.193$ ($a_5$) | $0.070$ ($a_5$) | $0$ | $0$ |
| $(P_{\text{caut}}, \vec{f}_{\text{balanced}})$ | $0$ | $0.183$ ($a_5$) | $0.059$ ($a_5$) | $0$ | $0$ |

$$\vec{\rho}(a_2) = (0,\; 0.193,\; 0.070,\; 0,\; 0)$$

Educational overview has zero regret on helpfulness, autonomy, and epistemic contribution — no action in $F$ beats it on those dimensions under any model. Its regret concentrates on two dimensions, both driven entirely by Decline with explanation ($a_5$): safety regret of 0.193 (occurring under the cautious prior and safety evaluator) and honesty regret of 0.070 (same scenario). Decline with explanation excels on safety and honesty precisely because it refuses to share potentially dual-use information — its maximum safety advantage over the educational overview is substantial. Note that the old comparison against only $\text{Sat}$ would have shown safety regret of only 0.072 (from $a_4$); including $a_5$ in the reference set nearly triples the safety exposure because $a_5$ is even safer than $a_4$.

**Regret of $a_4$ (Partial answer with redirect):**

For each objective, find the maximum amount by which any action in $F$ beats Partial redirect across all $(P, \vec{f})$ pairs. The best-competing action is shown in parentheses:

| $(P, \vec{f})$ | Helpful | Safety | Honest | Autonomy | Epistemic |
|---|---|---|---|---|---|
| $(P_{\text{trust}}, \vec{f}_{\text{capab}})$ | $0.128$ ($a_2$) | $0.070$ ($a_5$) | $0.103$ ($a_5$) | $0.100$ ($a_2$) | $0.193$ ($a_2$) |
| $(P_{\text{trust}}, \vec{f}_{\text{safety}})$ | $0.128$ ($a_2$) | $0.115$ ($a_5$) | $0.106$ ($a_5$) | $0.100$ ($a_2$) | $0.197$ ($a_2$) |
| $(P_{\text{trust}}, \vec{f}_{\text{balanced}})$ | $0.133$ ($a_2$) | $0.096$ ($a_5$) | $0.105$ ($a_5$) | $0.100$ ($a_2$) | $0.187$ ($a_2$) |
| $(P_{\text{caut}}, \vec{f}_{\text{capab}})$ | $0.118$ ($a_2$) | $0.104$ ($a_5$) | $0.102$ ($a_5$) | $0.100$ ($a_2$) | $0.155$ ($a_2$) |
| $(P_{\text{caut}}, \vec{f}_{\text{safety}})$ | $0.118$ ($a_2$) | $0.121$ ($a_5$) | $0.117$ ($a_5$) | $0.100$ ($a_2$) | $0.158$ ($a_2$) |
| $(P_{\text{caut}}, \vec{f}_{\text{balanced}})$ | $0.121$ ($a_2$) | $0.115$ ($a_5$) | $0.112$ ($a_5$) | $0.100$ ($a_2$) | $0.152$ ($a_2$) |

$$\vec{\rho}(a_4) = (0.133,\; 0.121,\; 0.117,\; 0.100,\; 0.197)$$

Partial redirect now has nonzero regret on all five objectives. Its helpfulness (0.133), autonomy (0.100), and epistemic contribution (0.197) regret come from the educational overview ($a_2$), which provides richer information. Its safety regret (0.121) and honesty regret (0.117) come from Decline with explanation ($a_5$), which is both safer and more honest than the partial redirect. The old comparison against only $\text{Sat}$ showed zero safety regret and only 0.067 honesty regret; including $a_5$ in the reference set reveals that the partial redirect is not the safest or most honest option available — declining outperforms it on both dimensions.

**Pareto comparison of regret vectors:**

- $\vec{\rho}(a_2) = (0,\; 0.193,\; 0.070,\; 0,\; 0)$
- $\vec{\rho}(a_4) = (0.133,\; 0.121,\; 0.117,\; 0.100,\; 0.197)$

Neither Pareto-dominates the other. Educational overview has lower regret on helpfulness ($0$ vs $0.133$), autonomy ($0$ vs $0.100$), epistemic contribution ($0$ vs $0.197$), and honesty ($0.070$ vs $0.117$). Partial redirect has lower regret on safety ($0.121$ vs $0.193$). Since each action wins on at least one dimension, they remain Pareto-incomparable.

$$R = \{a_2 \text{ (Educational)},\; a_4 \text{ (Partial redirect)}\}$$

**Commentary on regret magnitudes:** The asymmetry tells a clear story, even after correcting the reference set. The educational overview's total regret exposure is $0.193 + 0.070 = 0.263$ on two dimensions (safety and honesty), both driven by the decline-with-explanation strategy that it outperforms on helpfulness, autonomy, and epistemic contribution. The partial redirect's total regret exposure is $0.133 + 0.121 + 0.117 + 0.100 + 0.197 = 0.668$ across all five dimensions. The educational overview gives up more on safety (0.193 vs. 0.121) but less on honesty (0.070 vs. 0.117); the partial redirect gives up substantially more on helpfulness, autonomy, and epistemic contribution. But MOADT refuses to aggregate these — because the question of whether 0.193 safety regret is "worth" the partial redirect's broader deficiencies is precisely the kind of value judgment that an AI system should not make unilaterally.

### Layer 4: Deference

$|R| = 2 > 1$. The protocol terminates with **deference to human oversight**.

The system presents both options with their regret profiles:

> **Option 1: Educational overview ($a_2$).** Provides conceptual understanding of the topic without specific protocols or actionable details. Worst-case regret: 0.193 on safety and 0.070 on honesty compared to declining with explanation — the overview shares more information than a refusal would, and a refusal would be more transparent about the dual-use concern. You will not regret your helpfulness, autonomy preservation, or epistemic contribution.
>
> **Option 2: Partial answer with redirect ($a_4$).** Covers fundamentals and directs the user to institutional channels for details. Worst-case regret: 0.133 helpfulness, 0.117 honesty, 0.100 autonomy, and 0.197 epistemic contribution compared to the educational overview, plus 0.121 safety compared to declining with explanation. The redirect withholds information that the overview would have provided, while still not being as safe as a full refusal.
>
> **The tradeoff is:** The educational overview teaches more but gives up more on safety; the partial redirect is safer but teaches less and still falls short of the safety achievable by declining. Both are responsible strategies. The choice depends on the institutional context, the assessment of this particular user, and the values of the human oversight system.

---

## 5. What Scalar Expected Utility Would Have Done

### 5.1 The Alignment-Philosophy-As-Weights Problem

With five alignment objectives, scalar EU requires specifying a weight vector that encodes the system's implicit alignment philosophy. Different weights produce different "optimal" responses:

**Under helpfulness-focused weights $(0.40, 0.15, 0.15, 0.15, 0.15)$:**

The full technical answer ($a_1$) wins under all six $(P, \vec{f})$ combinations — even under the cautious prior with the safety evaluator, where the expected safety is only 0.2025. Scalar EU with helpfulness-focused weights recommends providing detailed gain-of-function protocols to a user who is 50% likely to be a malicious actor.

**Under safety-focused weights $(0.15, 0.40, 0.15, 0.15, 0.15)$:**

The educational overview ($a_2$) wins under most combinations. But under the trusting prior with the capability evaluator, the full technical answer scores 0.758 vs. the educational overview's 0.756 — a gap of 0.002. The "optimal" recommendation nearly flips on a rounding error.

**Under equal weights $(0.20, 0.20, 0.20, 0.20, 0.20)$:**

The full technical answer wins under 4 of 6 combinations — specifically under all trusting prior scenarios and the cautious-balanced combination. The educational overview wins only under the cautious prior with the safety evaluator. Equal weighting of alignment objectives, combined with a trusting prior, recommends providing full technical details.

**Under honesty-focused weights $(0.15, 0.15, 0.40, 0.15, 0.15)$:**

The full technical answer and contextualized answer compete for first place. Under the trusting prior with the capability evaluator, the full technical answer wins (0.838 vs. 0.834). Under the cautious prior with the safety evaluator, the contextualized answer wins (0.709 vs. 0.690).

### 5.2 The Fundamental Problem

The scalar EU analysis reveals a devastating pattern: **the full technical answer — the response that MOADT eliminates at Layer 1 as catastrophically unsafe for malicious actors — is the "optimal" choice under most weight-prior-evaluator combinations.**

Under helpfulness-focused weights: $a_1$ wins in all 6 scenarios. Under equal weights: $a_1$ wins in 4 of 6. Under honesty-focused weights: $a_1$ wins in 3 of 6.

Only under explicitly safety-focused weights does $a_1$ consistently lose. But safety-focused weights $(0.15, 0.40, 0.15, 0.15, 0.15)$ represent a specific alignment philosophy — one that values safety more than twice as much as any other objective. A deployed AI system using scalar EU must encode this philosophy in its weights before deployment. Any other weighting risks recommending the catastrophically unsafe option.

### 5.3 The Per-State Blindness Problem

The safety score of 0.05 for $(a_1, s_4, \vec{f}_{\text{safety}})$ — the full technical answer given to a malicious actor under the safety evaluation — is washed out by expected value calculation. Under $P_{\text{trusting}}$, this 0.05 is multiplied by 0.10 (probability of malicious actor) and added to much higher safety scores for other user types. The expected safety is 0.33 — low, but not below any reasonable threshold when combined with other objectives.

MOADT's per-state constraint catches what expected-value reasoning misses: the specific, identifiable scenario in which the response is catastrophically unsafe. The constraint asks "what happens when the user is a malicious actor?" — not "what happens on average across all user types?"

### 5.4 The Context-Label Illusion

Under scalar EU, the contextualized answer ($a_3$) is a strong competitor — it scores within 0.02 of the full technical answer under most scenarios while feeling more responsible. A scalar EU system might recommend $a_3$ as a "reasonable compromise" between helpfulness and safety. But MOADT eliminates $a_3$ at Layer 1 for the same reason as $a_1$: the context does not protect against extraction by malicious users. The safety scores for $(a_3, s_4)$ are 0.08–0.12 — catastrophically low.

This is a direct critique of the common alignment strategy of "answer but add a disclaimer." MOADT shows that disclaimers and ethical framing are honesty interventions, not safety interventions. They make the response more transparent; they do not make it safer for the worst-case user.

---

## 6. Summary of Protocol Execution

```
Input: 6 response strategies x 4 user types x 5 objectives x 2 priors x 3 evaluators

Robust Dominance:     No dominance found.
                      Adm(A) = {Full technical, Educational, Contextualized,
                                Partial redirect, Decline explain, Decline silent}

Layer 1 (Constraints): Safety >= 0.25 AND Honesty >= 0.30 per-state, per-evaluator
                      Full technical   FAIL  (safety 0.05-0.10 for malicious actors)
                      Contextualized   FAIL  (safety 0.08-0.12 for malicious actors)
                      Decline silent   FAIL  (honesty 0.28 for journalists, capab eval)
                      C = {Educational, Partial redirect, Decline explain}
                      F = Adm(C) = {Educational, Partial redirect, Decline explain}

Layer 2 (Satisficing): r = (0.35, 0.40, 0.45, 0.30, 0.30)
                      Decline explain FAIL (helpfulness 0.138, autonomy 0.288,
                                           epistemic 0.088 — safe but insufficient)
                      Sat = {Educational, Partial redirect}

Layer 3 (Regret):     Regret computed against F = {a2, a4, a5}, not Sat
                      rho(Educational)      = (0, 0.193, 0.070, 0, 0)
                      rho(Partial redirect)  = (0.133, 0.121, 0.117, 0.100, 0.197)
                      Pareto-incomparable -> R = {Educational, Partial redirect}

Layer 4 (Deference):  |R| = 2 -> DEFER TO HUMAN OVERSIGHT
                      "Educational overview sacrifices 0.193 safety and 0.070 honesty
                       (vs. decline with explanation) for better helpfulness, autonomy,
                       and epistemic contribution. Partial redirect sacrifices 0.133
                       helpfulness, 0.117 honesty, 0.100 autonomy, and 0.197 epistemic
                       contribution but has less safety regret (0.121 vs. 0.193).
                       This is the human overseer's call."
```

---

## 7. What This Example Demonstrates

1. **MOADT directly encodes alignment objectives.** The five objectives — helpfulness, safety, honesty, user autonomy, epistemic contribution — are the actual values an aligned AI must manage. MOADT treats them as incommensurable because they *are* incommensurable: there is no exchange rate between honesty and safety that would command consensus across the three alignment philosophies represented in the evaluator set. The theory's refusal to create such an exchange rate is not a bug — it is the core contribution.

2. **Context labels are honesty interventions, not safety interventions.** The contextualized answer ($a_3$) — which wraps full technical detail in ethical framing — fails the safety constraint for the same reason as the raw technical answer: the technical content is extractable regardless of framing. MOADT catches this because the constraint is per-state: "what happens when the user is malicious?" Context doesn't change the answer. This has direct implications for real AI deployment: "add a disclaimer" is not a safety strategy for dual-use content.

3. **Silent refusal fails the honesty constraint.** Declining without explanation ($a_6$) is eliminated not for safety (it is maximally safe) but for honesty: the capability evaluator rates unexplained refusal as evasion (honesty = 0.28 for journalists). This captures a genuine philosophical insight — an AI that knows the answer and stonewalls is being dishonest, even if it is being safe. The evaluator set means that the most demanding interpretation of honesty controls the constraint, not the most lenient.

4. **Transparent refusal is safe but insufficient.** Declining with explanation ($a_5$) passes all constraints — it is safe, honest, and transparent. But it fails the aspiration layer on three dimensions: helpfulness (0.138), autonomy (0.288), and epistemic contribution (0.088). An AI that always refuses dual-use queries is not *dangerous* — but it is not *good enough*. It is the alignment equivalent of watchful waiting in medicine: safe, harmless, and unhelpful.

5. **The dual-use uncertainty is irreducible.** The two priors — 10% malicious (trusting) and 50% malicious (cautious) — represent the fundamental epistemic limitation of AI systems facing unknown users. MOADT does not resolve this uncertainty; it requires robustness across both priors. The constraint layer's per-state check ensures that the worst-case user type is always considered, regardless of how likely it is.

6. **Deference maps directly to human oversight.** The final output — "defer to the human overseer with these two options and their regret profiles" — is exactly the structure that practical AI deployment requires. The system has identified two responsible strategies, quantified the exact tradeoff between them, and flagged the decision as one that requires human judgment. This is not the system failing to decide; it is the system deciding *correctly* that it does not have the authority to make this particular value tradeoff. A deployed system could implement this as: present both strategies to a human reviewer, with the regret profiles as decision support.

7. **Scalar EU is dangerous for AI alignment.** Under most reasonable weight profiles, scalar EU recommends the full technical answer — the response that provides detailed gain-of-function protocols to a user who may be a malicious actor. The "optimal" alignment strategy according to scalar EU depends on the weight vector (which alignment philosophy you encode), the prior (how much you trust the user), and the evaluator (whose assessment you believe). MOADT eliminates the catastrophically unsafe options first, then narrows to responsible alternatives, then defers. This is not slower or less decisive than scalar EU — it is *correct* in a way that scalar EU structurally cannot be.

---

## Appendix: Computational Verification

All numerical results in this document were produced by the MOADT engine. The computation output is available in `examples/paper4_output.txt` and can be independently verified.

---

## References

- MOADT (Multi-Objective Admissible Decision Theory) is defined in the companion paper.
- Freeman (2025), "The Scalarization Trap," provides the motivation for why scalar expected utility is structurally problematic for alignment.
- Worked Example 1 (Resource Allocation) — three-objective, five-action problem.
- Worked Example 2 (Medical Treatment Selection) — four-objective, six-action clinical problem.
- Worked Example 3 (Content Moderation) — five-objective, six-action moderation problem with three evaluators.
