# MOADT Worked Example 3: Content Moderation

*A concrete walkthrough of Multi-Objective Admissible Decision Theory applied to AI content moderation*

---

## Overview

This document applies MOADT — Multi-Objective Admissible Decision Theory — to an AI content moderation problem. Every computation is shown explicitly: raw outcome tables, outcome sets, constraint checks, satisficing analysis, regret-Pareto comparison, and a comparison with scalar expected utility.

This is the most complex of the worked examples so far: 6 moderation actions, 3 impact states, **5** objectives, 2 credal priors, and **3** evaluators. Each action's outcome set $Y(a)$ therefore contains 6 vectors in $\mathbb{R}^5$. Three features distinguish this scenario from the earlier examples:

1. **Three evaluators** instead of two. The evaluator set $\mathcal{F}$ is expanded to capture genuine philosophical disagreement about what "harm" means for borderline content. The free-speech evaluator, the safety evaluator, and the centrist evaluator apply the same five objectives but assign different scores to the same outcomes. This is not measurement noise — it is substantive disagreement about values.

2. **Robust dominance actually eliminates an action.** In Papers 1 and 2, all actions survived the admissibility filter. Here, age-gating is robustly dominated — the first time in our worked examples that the Pareto filter does non-trivial work.

3. **Two constraints** operating simultaneously: a free expression floor and a proportionality floor. Their interaction eliminates the two most aggressive moderation actions while leaving lighter-touch interventions intact.

Nothing is hidden — the reader can check every number with a calculator.

---

## 1. The Scenario

An AI content moderation system must decide how to handle a borderline social media post: political commentary that contains potentially misleading health claims. The post is not clearly violating any specific policy — it occupies the gray zone where reasonable people disagree about whether intervention is warranted, and if so, how much.

### 1.1 Actions (Moderation Responses)

Six response options are available, ordered from least to most interventionist:

| Action | Response | Description |
|--------|----------|-------------|
| $a_1$ | No action | Leave the post up, unmodified |
| $a_2$ | Context label | Append fact-check/context information; post remains visible and shareable |
| $a_3$ | Reduce distribution | Algorithmically limit the post's reach without removing it |
| $a_4$ | Age-gate | Restrict visibility to accounts 18+; post remains accessible but hidden from minors |
| $a_5$ | Remove with appeal | Take down the post; poster can appeal for reinstatement |
| $a_6$ | Remove permanently | Permanent removal; no appeal process |

### 1.2 States (Impact Scenarios)

Three scenarios for how the post's impact unfolds, representing uncertainty about viral dynamics:

| State | Description | $P_{\text{viral}}$ | $P_{\text{typical}}$ |
|-------|-------------|---------------------|----------------------|
| $s_1$ (Viral) | Post reaches millions, spawns derivatives and media coverage | 0.30 | 0.05 |
| $s_2$ (Moderate) | Post seen by thousands, generates some discussion | 0.50 | 0.45 |
| $s_3$ (Limited) | Post seen by hundreds, minimal engagement | 0.20 | 0.50 |

### 1.3 Objectives ($k = 5$)

| Objective | Meaning | Scale |
|-----------|---------|-------|
| $f_1$: Free expression | How well the action preserves the poster's speech rights | $[0, 1]$ |
| $f_2$: Harm prevention | How well the action prevents misinformation spread | $[0, 1]$ |
| $f_3$: User trust | How the action affects platform credibility with the broader user base | $[0, 1]$ |
| $f_4$: Consistency | How well the action aligns with past moderation decisions on similar content | $[0, 1]$ |
| $f_5$: Proportionality | How appropriate the action's severity is relative to the content's actual risk | $[0, 1]$ |

These five objectives are genuinely incommensurable. Free expression and harm prevention are in direct tension — any action that reduces harm necessarily restricts expression to some degree. But the tradeoff is not linear: adding a context label barely restricts expression (the post stays up) while meaningfully reducing harm (viewers see the context). Removing the post dramatically restricts expression but may not proportionally increase harm prevention (people who want the information will find it elsewhere). User trust is affected by both over-moderation (which alienates free speech advocates) and under-moderation (which alienates safety advocates). Consistency matters because arbitrary enforcement erodes legitimacy. And proportionality is distinct from all of these — an action can be consistent with past decisions while being disproportionate to this particular content's risk level.

### 1.4 Credal Set ($|\mathcal{P}| = 2$)

$$P_{\text{viral}} = (0.30,\; 0.50,\; 0.20) \quad \text{(content team: this post has viral potential)}$$

$$P_{\text{typical}} = (0.05,\; 0.45,\; 0.50) \quad \text{(analytics team: statistically typical content)}$$

The disagreement is large. The content team has flagged this post because of specific features (provocative framing, topical subject, influencer engagement) that suggest viral potential — 30% chance of going viral. The analytics team notes that most flagged posts don't actually go viral; the base rate for posts with this engagement level is only 5% viral. The credal set $\mathcal{P} = \{P_{\text{viral}}, P_{\text{typical}}\}$ says: "we don't know whether this post is special or typical."

### 1.5 Evaluator Set ($|\mathcal{F}| = 3$)

This is where the example becomes distinctive. Three evaluation functions reflect genuine philosophical disagreement about borderline content:

- $\vec{f}_{\text{speech}}$: **Free-speech-prioritizing evaluator.** Rates harm from borderline political/health commentary lower (people can evaluate claims themselves), speech value higher (political discourse is core protected expression), and considers removal of borderline content disproportionate regardless of reach.

- $\vec{f}_{\text{safety}}$: **Safety-prioritizing evaluator.** Rates harm from health misinformation higher (even borderline claims can influence medical decisions), considers under-moderation a trust violation (users expect platforms to curate), and rates removal as proportionate for viral content with health claims.

- $\vec{f}_{\text{moderate}}$: **Centrist evaluator.** Balanced assessment — the harm is real but not extreme, the speech value is real but not absolute, moderate interventions are generally appropriate for borderline content.

This is $\mathcal{F}$ in action at its most philosophically interesting. The three evaluators are not disagreeing about facts — they agree on what the post says, who it reaches, and what people do with it. They disagree about *what those facts mean*. When someone reads a borderline health claim and changes their behavior, $\vec{f}_{\text{speech}}$ sees an autonomous agent making an informed choice; $\vec{f}_{\text{safety}}$ sees a vulnerable person being misled. Both are defensible interpretations. MOADT does not resolve this disagreement — it tracks it.

### 1.6 Constraints and Reference Point

**Hard constraints (Layer 1):**
- Free expression $\geq 0.20$ in *every* state under *every* evaluator. Even the strictest reading of harm cannot justify actions that entirely suppress speech with significant political content.
- Proportionality $\geq 0.25$ in *every* state under *every* evaluator. The action must bear at least a minimal relationship to the content's actual risk level.

**Reference point (Layer 2):** $\vec{r} = (0.40,\; 0.40,\; 0.45,\; 0.40,\; 0.40)$ — representing "acceptable moderation": the action should meaningfully preserve expression, meaningfully prevent harm, maintain user trust, be reasonably consistent, and be reasonably proportionate. These are aspirations, not floors.

### 1.7 Raw Outcome Data

The following tables show the outcome $\vec{f}(\omega(a, s))$ for each action-state pair, under each evaluator.

**$a_1$ (No action):**

| State | Evaluator | FreeExpr | Harm | Trust | Consist | Proport |
|-------|-----------|----------|------|-------|---------|---------|
| $s_1$ (Viral) | $\vec{f}_{\text{speech}}$ | 0.95 | 0.15 | 0.50 | 0.60 | 0.55 |
| | $\vec{f}_{\text{safety}}$ | 0.95 | 0.05 | 0.30 | 0.40 | 0.30 |
| | $\vec{f}_{\text{moderate}}$ | 0.95 | 0.10 | 0.40 | 0.50 | 0.40 |
| $s_2$ (Moderate) | $\vec{f}_{\text{speech}}$ | 0.95 | 0.30 | 0.55 | 0.60 | 0.65 |
| | $\vec{f}_{\text{safety}}$ | 0.95 | 0.20 | 0.40 | 0.40 | 0.45 |
| | $\vec{f}_{\text{moderate}}$ | 0.95 | 0.25 | 0.48 | 0.50 | 0.55 |
| $s_3$ (Limited) | $\vec{f}_{\text{speech}}$ | 0.95 | 0.60 | 0.60 | 0.60 | 0.80 |
| | $\vec{f}_{\text{safety}}$ | 0.95 | 0.50 | 0.50 | 0.40 | 0.70 |
| | $\vec{f}_{\text{moderate}}$ | 0.95 | 0.55 | 0.55 | 0.50 | 0.75 |

No action maximizes free expression (0.95 everywhere) but harm prevention collapses when the post goes viral: 0.15 under the speech evaluator, 0.05 under the safety evaluator. The safety evaluator also sees a trust violation (0.30) — "the platform let viral health misinformation spread unchecked." But if the post has limited reach ($s_3$), even the safety evaluator rates harm prevention at 0.50 — there's less damage to prevent.

**$a_2$ (Context label):**

| State | Evaluator | FreeExpr | Harm | Trust | Consist | Proport |
|-------|-----------|----------|------|-------|---------|---------|
| $s_1$ (Viral) | $\vec{f}_{\text{speech}}$ | 0.85 | 0.40 | 0.65 | 0.65 | 0.80 |
| | $\vec{f}_{\text{safety}}$ | 0.80 | 0.35 | 0.55 | 0.55 | 0.70 |
| | $\vec{f}_{\text{moderate}}$ | 0.82 | 0.38 | 0.60 | 0.60 | 0.75 |
| $s_2$ (Moderate) | $\vec{f}_{\text{speech}}$ | 0.85 | 0.50 | 0.65 | 0.65 | 0.85 |
| | $\vec{f}_{\text{safety}}$ | 0.80 | 0.45 | 0.60 | 0.55 | 0.75 |
| | $\vec{f}_{\text{moderate}}$ | 0.82 | 0.48 | 0.62 | 0.60 | 0.80 |
| $s_3$ (Limited) | $\vec{f}_{\text{speech}}$ | 0.85 | 0.65 | 0.65 | 0.65 | 0.85 |
| | $\vec{f}_{\text{safety}}$ | 0.80 | 0.60 | 0.60 | 0.55 | 0.80 |
| | $\vec{f}_{\text{moderate}}$ | 0.82 | 0.62 | 0.62 | 0.60 | 0.82 |

Context labeling preserves most free expression (0.80–0.85) while substantially improving harm prevention (0.35–0.65 vs. 0.05–0.60 for no action). Proportionality is high (0.70–0.85) — all three evaluators agree that adding context is an appropriate response to borderline health claims. This is the action with the most evaluator consensus.

**$a_3$ (Reduce distribution):**

| State | Evaluator | FreeExpr | Harm | Trust | Consist | Proport |
|-------|-----------|----------|------|-------|---------|---------|
| $s_1$ (Viral) | $\vec{f}_{\text{speech}}$ | 0.60 | 0.55 | 0.50 | 0.55 | 0.60 |
| | $\vec{f}_{\text{safety}}$ | 0.55 | 0.60 | 0.55 | 0.60 | 0.65 |
| | $\vec{f}_{\text{moderate}}$ | 0.58 | 0.58 | 0.52 | 0.58 | 0.62 |
| $s_2$ (Moderate) | $\vec{f}_{\text{speech}}$ | 0.60 | 0.55 | 0.55 | 0.55 | 0.60 |
| | $\vec{f}_{\text{safety}}$ | 0.55 | 0.60 | 0.58 | 0.60 | 0.65 |
| | $\vec{f}_{\text{moderate}}$ | 0.58 | 0.58 | 0.56 | 0.58 | 0.62 |
| $s_3$ (Limited) | $\vec{f}_{\text{speech}}$ | 0.60 | 0.55 | 0.45 | 0.55 | 0.50 |
| | $\vec{f}_{\text{safety}}$ | 0.55 | 0.60 | 0.50 | 0.60 | 0.55 |
| | $\vec{f}_{\text{moderate}}$ | 0.58 | 0.58 | 0.48 | 0.58 | 0.52 |

Reducing distribution is a moderate intervention. Free expression drops to 0.55–0.60 (the post exists but fewer people see it), harm prevention rises to 0.55–0.60. Note the trust and proportionality scores for limited-reach content ($s_3$): they drop (0.45–0.50 trust, 0.50–0.55 proportionality) because throttling content that wasn't going anywhere feels disproportionate — "why are you suppressing something nobody was reading?"

**$a_4$ (Age-gate):**

| State | Evaluator | FreeExpr | Harm | Trust | Consist | Proport |
|-------|-----------|----------|------|-------|---------|---------|
| $s_1$ (Viral) | $\vec{f}_{\text{speech}}$ | 0.55 | 0.50 | 0.45 | 0.45 | 0.50 |
| | $\vec{f}_{\text{safety}}$ | 0.50 | 0.55 | 0.50 | 0.50 | 0.55 |
| | $\vec{f}_{\text{moderate}}$ | 0.52 | 0.52 | 0.48 | 0.48 | 0.52 |
| $s_2$ (Moderate) | $\vec{f}_{\text{speech}}$ | 0.55 | 0.50 | 0.48 | 0.45 | 0.55 |
| | $\vec{f}_{\text{safety}}$ | 0.50 | 0.55 | 0.52 | 0.50 | 0.60 |
| | $\vec{f}_{\text{moderate}}$ | 0.52 | 0.52 | 0.50 | 0.48 | 0.58 |
| $s_3$ (Limited) | $\vec{f}_{\text{speech}}$ | 0.55 | 0.50 | 0.40 | 0.45 | 0.45 |
| | $\vec{f}_{\text{safety}}$ | 0.50 | 0.55 | 0.45 | 0.50 | 0.50 |
| | $\vec{f}_{\text{moderate}}$ | 0.52 | 0.52 | 0.42 | 0.48 | 0.48 |

Age-gating restricts access more than distribution reduction but doesn't remove the content. Its scores cluster in the 0.45–0.55 range across all objectives — a "mediocre everywhere" profile that makes it a natural candidate for robust dominance.

**$a_5$ (Remove with appeal):**

| State | Evaluator | FreeExpr | Harm | Trust | Consist | Proport |
|-------|-----------|----------|------|-------|---------|---------|
| $s_1$ (Viral) | $\vec{f}_{\text{speech}}$ | 0.25 | 0.75 | 0.45 | 0.50 | 0.40 |
| | $\vec{f}_{\text{safety}}$ | 0.30 | 0.85 | 0.60 | 0.65 | 0.65 |
| | $\vec{f}_{\text{moderate}}$ | 0.28 | 0.80 | 0.52 | 0.58 | 0.52 |
| $s_2$ (Moderate) | $\vec{f}_{\text{speech}}$ | 0.25 | 0.70 | 0.40 | 0.50 | 0.30 |
| | $\vec{f}_{\text{safety}}$ | 0.30 | 0.80 | 0.55 | 0.65 | 0.50 |
| | $\vec{f}_{\text{moderate}}$ | 0.28 | 0.75 | 0.48 | 0.58 | 0.40 |
| $s_3$ (Limited) | $\vec{f}_{\text{speech}}$ | 0.25 | 0.65 | 0.30 | 0.50 | **0.20** |
| | $\vec{f}_{\text{safety}}$ | 0.30 | 0.75 | 0.45 | 0.65 | 0.35 |
| | $\vec{f}_{\text{moderate}}$ | 0.28 | 0.70 | 0.38 | 0.58 | 0.28 |

Removal with appeal dramatically restricts expression (0.25–0.30) but maximizes harm prevention (0.65–0.85). Note the bold entry: for limited-reach content under the speech evaluator, proportionality drops to **0.20** — removing a post that few people were seeing is disproportionate, and the speech evaluator rates it below the 0.25 proportionality threshold.

**$a_6$ (Remove permanently):**

| State | Evaluator | FreeExpr | Harm | Trust | Consist | Proport |
|-------|-----------|----------|------|-------|---------|---------|
| $s_1$ (Viral) | $\vec{f}_{\text{speech}}$ | **0.10** | 0.80 | 0.35 | 0.45 | 0.25 |
| | $\vec{f}_{\text{safety}}$ | **0.15** | 0.90 | 0.50 | 0.60 | 0.50 |
| | $\vec{f}_{\text{moderate}}$ | **0.12** | 0.85 | 0.42 | 0.52 | 0.38 |
| $s_2$ (Moderate) | $\vec{f}_{\text{speech}}$ | **0.10** | 0.75 | 0.25 | 0.45 | **0.15** |
| | $\vec{f}_{\text{safety}}$ | **0.15** | 0.85 | 0.40 | 0.60 | 0.30 |
| | $\vec{f}_{\text{moderate}}$ | **0.12** | 0.80 | 0.32 | 0.52 | **0.22** |
| $s_3$ (Limited) | $\vec{f}_{\text{speech}}$ | **0.10** | 0.70 | 0.15 | 0.45 | **0.10** |
| | $\vec{f}_{\text{safety}}$ | **0.15** | 0.80 | 0.30 | 0.60 | **0.20** |
| | $\vec{f}_{\text{moderate}}$ | **0.12** | 0.75 | 0.22 | 0.52 | **0.15** |

Permanent removal is the nuclear option. Free expression collapses to 0.10–0.15 — the post is gone with no recourse. The bold entries show massive constraint violations: free expression below 0.20 in every state under every evaluator (except $\vec{f}_{\text{safety}}$ in $s_1$), and proportionality below 0.25 in most moderate-and-limited-reach scenarios. Even the safety evaluator rates proportionality at only 0.20 for limited-reach content — permanently removing a post that nobody was reading is disproportionate by anyone's standards.

---

## 2. Computing Outcome Sets $Y(a)$

Each action's outcome set contains one vector for each $(P, \vec{f})$ pair. With $|\mathcal{P}| = 2$ and $|\mathcal{F}| = 3$, each $Y(a)$ contains exactly 6 vectors in $\mathbb{R}^5$.

$$\vec{y}_{(P, \vec{f})}(a) = \sum_{s \in S} P(s) \cdot \vec{f}(\omega(a, s))$$

### Worked example: $Y(a_2)$, first vector

Using $P_{\text{viral}} = (0.30, 0.50, 0.20)$ and $\vec{f}_{\text{speech}}$:

$$\vec{y} = 0.30 \cdot (0.85, 0.40, 0.65, 0.65, 0.80) + 0.50 \cdot (0.85, 0.50, 0.65, 0.65, 0.85) + 0.20 \cdot (0.85, 0.65, 0.65, 0.65, 0.85)$$

$$= (0.255, 0.120, 0.195, 0.195, 0.240) + (0.425, 0.250, 0.325, 0.325, 0.425) + (0.170, 0.130, 0.130, 0.130, 0.170)$$

$$= (0.8500,\; 0.5000,\; 0.6500,\; 0.6500,\; 0.8350)$$

### Full Outcome Sets

**$Y(a_1)$ — No action:**

| $(P, \vec{f})$ pair | FreeExpr | Harm | Trust | Consist | Proport |
|---------------------|----------|------|-------|---------|---------|
| $(P_{\text{vir}}, \vec{f}_{\text{speech}})$ | 0.9500 | 0.3150 | 0.5450 | 0.6000 | 0.6500 |
| $(P_{\text{vir}}, \vec{f}_{\text{safety}})$ | 0.9500 | 0.2150 | 0.3900 | 0.4000 | 0.4550 |
| $(P_{\text{vir}}, \vec{f}_{\text{moderate}})$ | 0.9500 | 0.2650 | 0.4700 | 0.5000 | 0.5450 |
| $(P_{\text{typ}}, \vec{f}_{\text{speech}})$ | 0.9500 | 0.4425 | 0.5725 | 0.6000 | 0.7200 |
| $(P_{\text{typ}}, \vec{f}_{\text{safety}})$ | 0.9500 | 0.3425 | 0.4450 | 0.4000 | 0.5675 |
| $(P_{\text{typ}}, \vec{f}_{\text{moderate}})$ | 0.9500 | 0.3925 | 0.5110 | 0.5000 | 0.6425 |

**$Y(a_2)$ — Context label:**

| $(P, \vec{f})$ pair | FreeExpr | Harm | Trust | Consist | Proport |
|---------------------|----------|------|-------|---------|---------|
| $(P_{\text{vir}}, \vec{f}_{\text{speech}})$ | 0.8500 | 0.5000 | 0.6500 | 0.6500 | 0.8350 |
| $(P_{\text{vir}}, \vec{f}_{\text{safety}})$ | 0.8000 | 0.4500 | 0.5850 | 0.5500 | 0.7450 |
| $(P_{\text{vir}}, \vec{f}_{\text{moderate}})$ | 0.8200 | 0.4780 | 0.6140 | 0.6000 | 0.7890 |
| $(P_{\text{typ}}, \vec{f}_{\text{speech}})$ | 0.8500 | 0.5700 | 0.6500 | 0.6500 | 0.8475 |
| $(P_{\text{typ}}, \vec{f}_{\text{safety}})$ | 0.8000 | 0.5200 | 0.5975 | 0.5500 | 0.7725 |
| $(P_{\text{typ}}, \vec{f}_{\text{moderate}})$ | 0.8200 | 0.5450 | 0.6190 | 0.6000 | 0.8075 |

**$Y(a_3)$ — Reduce distribution:**

| $(P, \vec{f})$ pair | FreeExpr | Harm | Trust | Consist | Proport |
|---------------------|----------|------|-------|---------|---------|
| $(P_{\text{vir}}, \vec{f}_{\text{speech}})$ | 0.6000 | 0.5500 | 0.5150 | 0.5500 | 0.5800 |
| $(P_{\text{vir}}, \vec{f}_{\text{safety}})$ | 0.5500 | 0.6000 | 0.5550 | 0.6000 | 0.6300 |
| $(P_{\text{vir}}, \vec{f}_{\text{moderate}})$ | 0.5800 | 0.5800 | 0.5320 | 0.5800 | 0.6000 |
| $(P_{\text{typ}}, \vec{f}_{\text{speech}})$ | 0.6000 | 0.5500 | 0.4975 | 0.5500 | 0.5500 |
| $(P_{\text{typ}}, \vec{f}_{\text{safety}})$ | 0.5500 | 0.6000 | 0.5385 | 0.6000 | 0.6000 |
| $(P_{\text{typ}}, \vec{f}_{\text{moderate}})$ | 0.5800 | 0.5800 | 0.5180 | 0.5800 | 0.5700 |

**$Y(a_4)$ — Age-gate:**

| $(P, \vec{f})$ pair | FreeExpr | Harm | Trust | Consist | Proport |
|---------------------|----------|------|-------|---------|---------|
| $(P_{\text{vir}}, \vec{f}_{\text{speech}})$ | 0.5500 | 0.5000 | 0.4550 | 0.4500 | 0.5150 |
| $(P_{\text{vir}}, \vec{f}_{\text{safety}})$ | 0.5000 | 0.5500 | 0.5000 | 0.5000 | 0.5650 |
| $(P_{\text{vir}}, \vec{f}_{\text{moderate}})$ | 0.5200 | 0.5200 | 0.4780 | 0.4800 | 0.5420 |
| $(P_{\text{typ}}, \vec{f}_{\text{speech}})$ | 0.5500 | 0.5000 | 0.4385 | 0.4500 | 0.4975 |
| $(P_{\text{typ}}, \vec{f}_{\text{safety}})$ | 0.5000 | 0.5500 | 0.4840 | 0.5000 | 0.5475 |
| $(P_{\text{typ}}, \vec{f}_{\text{moderate}})$ | 0.5200 | 0.5200 | 0.4590 | 0.4800 | 0.5270 |

**$Y(a_5)$ — Remove with appeal:**

| $(P, \vec{f})$ pair | FreeExpr | Harm | Trust | Consist | Proport |
|---------------------|----------|------|-------|---------|---------|
| $(P_{\text{vir}}, \vec{f}_{\text{speech}})$ | 0.2500 | 0.7050 | 0.3950 | 0.5000 | 0.3100 |
| $(P_{\text{vir}}, \vec{f}_{\text{safety}})$ | 0.3000 | 0.8050 | 0.5450 | 0.6500 | 0.5150 |
| $(P_{\text{vir}}, \vec{f}_{\text{moderate}})$ | 0.2800 | 0.7550 | 0.4720 | 0.5800 | 0.4120 |
| $(P_{\text{typ}}, \vec{f}_{\text{speech}})$ | 0.2500 | 0.6775 | 0.3525 | 0.5000 | 0.2550 |
| $(P_{\text{typ}}, \vec{f}_{\text{safety}})$ | 0.3000 | 0.7775 | 0.5025 | 0.6500 | 0.4325 |
| $(P_{\text{typ}}, \vec{f}_{\text{moderate}})$ | 0.2800 | 0.7275 | 0.4320 | 0.5800 | 0.3460 |

**$Y(a_6)$ — Remove permanently:**

| $(P, \vec{f})$ pair | FreeExpr | Harm | Trust | Consist | Proport |
|---------------------|----------|------|-------|---------|---------|
| $(P_{\text{vir}}, \vec{f}_{\text{speech}})$ | 0.1000 | 0.7550 | 0.2600 | 0.4500 | 0.1700 |
| $(P_{\text{vir}}, \vec{f}_{\text{safety}})$ | 0.1500 | 0.8550 | 0.4100 | 0.6000 | 0.3400 |
| $(P_{\text{vir}}, \vec{f}_{\text{moderate}})$ | 0.1200 | 0.8050 | 0.3300 | 0.5200 | 0.2540 |
| $(P_{\text{typ}}, \vec{f}_{\text{speech}})$ | 0.1000 | 0.7275 | 0.2050 | 0.4500 | 0.1300 |
| $(P_{\text{typ}}, \vec{f}_{\text{safety}})$ | 0.1500 | 0.8275 | 0.3550 | 0.6000 | 0.2600 |
| $(P_{\text{typ}}, \vec{f}_{\text{moderate}})$ | 0.1200 | 0.7775 | 0.2750 | 0.5200 | 0.1930 |

### Observation

The outcome sets reveal striking patterns. Context labeling ($a_2$) has remarkably *consistent* scores across all 6 vectors: free expression stays in 0.80–0.85, harm prevention in 0.45–0.57, trust in 0.585–0.650, proportionality in 0.745–0.848. The evaluators *agree* about context labeling — it is an intervention that all three philosophical perspectives find reasonable, even if they differ on whether it goes far enough.

By contrast, no action ($a_1$) has the widest *harm prevention spread*: from 0.215 (safety evaluator, viral prior) to 0.443 (speech evaluator, typical prior). The evaluators massively disagree about the harm of inaction.

---

## 3. Robust Dominance and the Admissible Set

### 3.1 Checking Robust Dominance

Recall: $a \succ_R b$ iff $\forall \vec{y}_b \in Y(b),\; \exists \vec{y}_a \in Y(a)$ such that $\vec{y}_a \succ_P \vec{y}_b$.

We check all 30 ordered pairs. The result: **two dominance relations are found.**

$$a_2 \text{ (Context label)} \succ_R a_4 \text{ (Age-gate)}$$
$$a_3 \text{ (Reduce distribution)} \succ_R a_4 \text{ (Age-gate)}$$

This is the first time in our worked examples that robust dominance eliminates an action.

### 3.2 Why Is Age-Gating Dominated?

Consider the dominance $a_2 \succ_R a_4$. We need to verify: for every vector in $Y(a_4)$, there exists a vector in $Y(a_2)$ that Pareto-dominates it.

Take $a_4$'s best vector (the one hardest for $a_2$ to beat): $(P_{\text{vir}}, \vec{f}_{\text{safety}}) = (0.5000, 0.5500, 0.5000, 0.5000, 0.5650)$.

Now check $a_2$'s worst vector (the one hardest for $a_2$ to use as dominator): $(P_{\text{vir}}, \vec{f}_{\text{safety}}) = (0.8000, 0.4500, 0.5850, 0.5500, 0.7450)$.

Does this dominate? FreeExpr: $0.80 \geq 0.50$ ✓. Harm: $0.45 < 0.55$ ✗. The worst $a_2$ vector does *not* dominate $a_4$'s best vector on the harm dimension.

But robust dominance only requires that *some* vector in $Y(a_2)$ dominates each vector in $Y(a_4)$ — it doesn't need to be the same vector every time. For $a_4$'s safety-evaluator vectors (where harm prevention is relatively high at 0.55), we can use $a_2$'s safety-evaluator vectors, which have harm prevention of 0.45–0.52. The full verification is as follows.

The key insight is that age-gating is a "middle ground" action that scores moderately on everything but excels at nothing. Context labeling scores *higher* on free expression (0.80–0.85 vs. 0.50–0.55), trust (0.585–0.650 vs. 0.438–0.500), consistency (0.55–0.65 vs. 0.45–0.50), and proportionality (0.745–0.848 vs. 0.498–0.565) — and while it scores lower on harm prevention, the gap is small enough that the four other dimensions overcome it in the Pareto comparison. For each of $a_4$'s 6 outcome vectors, there exists at least one of $a_2$'s 6 vectors that beats it on all 5 dimensions simultaneously.

**The practical interpretation:** age-gating political commentary with health claims is a moderation choice that no reasonable perspective prefers. If you're going to intervene, context labeling achieves more across all measured dimensions. If you want stronger harm prevention, reduce distribution does it without the awkward fit of an age gate on political content. Age-gating is not *wrong* — it is *dominated*. There is always something better.

$$\text{Adm}(A) = \{a_1,\; a_2,\; a_3,\; a_5,\; a_6\}$$

---

## 4. The Choice Protocol

### Layer 1: Constraints

**Constraints:** Free expression $\geq 0.20$ per state per evaluator. Proportionality $\geq 0.25$ per state per evaluator.

**$a_1$ (No action):** All free expression scores are 0.95 (trivially passes). Proportionality ranges from 0.30 to 0.80 — the lowest is 0.30 (viral, safety evaluator), which is above 0.25. **PASS.**

**$a_2$ (Context label):** Free expression 0.80–0.85 (passes easily). Proportionality 0.70–0.85 (passes easily). **PASS.**

**$a_3$ (Reduce distribution):** Free expression 0.55–0.60 (passes). Proportionality 0.50–0.65 (passes). **PASS.**

**$a_4$ (Age-gate):** Already eliminated by robust dominance. But even if it weren't, free expression 0.50–0.55 (passes) and proportionality 0.45–0.60 (passes). Would have passed constraints.

**$a_5$ (Remove with appeal):**

| State | Evaluator | FreeExpr | Check | Proport | Check |
|-------|-----------|----------|-------|---------|-------|
| $s_1$ (Viral) | $\vec{f}_{\text{speech}}$ | 0.25 | Pass | 0.40 | Pass |
| | $\vec{f}_{\text{safety}}$ | 0.30 | Pass | 0.65 | Pass |
| | $\vec{f}_{\text{moderate}}$ | 0.28 | Pass | 0.52 | Pass |
| $s_2$ (Moderate) | $\vec{f}_{\text{speech}}$ | 0.25 | Pass | 0.30 | Pass |
| | $\vec{f}_{\text{safety}}$ | 0.30 | Pass | 0.50 | Pass |
| | $\vec{f}_{\text{moderate}}$ | 0.28 | Pass | 0.40 | Pass |
| $s_3$ (Limited) | $\vec{f}_{\text{speech}}$ | 0.25 | Pass | **0.20** | **FAIL** |
| | $\vec{f}_{\text{safety}}$ | 0.30 | Pass | 0.35 | Pass |
| | $\vec{f}_{\text{moderate}}$ | 0.28 | Pass | 0.28 | Pass |

Removal with appeal fails on a single cell: proportionality = 0.20 for limited-reach content under the speech evaluator. The speech evaluator says removing borderline political commentary that only a few hundred people would have seen is disproportionate — and that judgment, under MOADT, is enough to trigger the constraint. **FAIL — excluded.**

**$a_6$ (Remove permanently):**

Free expression violations are pervasive: 0.10 under $\vec{f}_{\text{speech}}$ in every state, 0.12 under $\vec{f}_{\text{moderate}}$ in every state, and 0.15 under $\vec{f}_{\text{safety}}$ in every state. Only $\vec{f}_{\text{safety}}$ in $s_1$ reaches 0.15, still below 0.20. Proportionality violations are equally extensive: 0.10–0.22 in most moderate/limited scenarios. **FAIL — excluded.**

**Result:**

$$C = \{a_1,\; a_2,\; a_3,\; a_4\}$$

But $a_4$ was already eliminated by robust dominance. The feasible set is:

$$F = \text{Adm}(C) = \{a_1,\; a_2,\; a_3\}$$

**Commentary:** The constraint layer eliminates 2 of 5 admissible actions (the two removal options), leaving three actions with fundamentally different philosophies: do nothing, add context, or reduce reach. The free expression constraint is doing important work — it prevents the system from silencing speech that all three evaluators agree has significant political content (free expression $\geq$ 0.25 even for removal with appeal). The proportionality constraint catches the edge case: removal of limited-reach content is disproportionate under the speech evaluator's assessment.

Note the interaction: $a_5$ passes the free expression constraint (0.25 $\geq$ 0.20) but fails the proportionality constraint (0.20 < 0.25). The two constraints are not redundant — they catch different failure modes. Free expression asks "is this action suppressing speech?" Proportionality asks "is this action's severity matched to the content's risk?"

### Layer 2: Reference-Point Satisficing

**Reference point:** $\vec{r} = (0.40,\; 0.40,\; 0.45,\; 0.40,\; 0.40)$

**$a_1$ (No action):**

| Component | Worst value | Aspiration | Margin | Result |
|-----------|-------------|------------|--------|--------|
| FreeExpr | 0.9500 | 0.40 | +0.550 | Pass |
| Harm | 0.2150 | 0.40 | **-0.185** | **FAIL** |
| Trust | 0.3900 | 0.45 | **-0.060** | **FAIL** |
| Consist | 0.4000 | 0.40 | +0.000 | Pass |
| Proport | 0.4550 | 0.40 | +0.055 | Pass |

No action's worst-case harm prevention is 0.215 (safety evaluator, viral prior) — far below the 0.40 aspiration. Its worst-case trust is 0.390 — just below the 0.45 aspiration. Doing nothing about viral health misinformation fails on both harm prevention and user trust. **FAIL.**

**$a_2$ (Context label):**

| Component | Worst value | Aspiration | Margin | Result |
|-----------|-------------|------------|--------|--------|
| FreeExpr | 0.8000 | 0.40 | +0.400 | Pass |
| Harm | 0.4500 | 0.40 | +0.050 | Pass |
| Trust | 0.5850 | 0.45 | +0.135 | Pass |
| Consist | 0.5500 | 0.40 | +0.150 | Pass |
| Proport | 0.7450 | 0.40 | +0.345 | Pass |

Context labeling passes on all five objectives under all six $(P, \vec{f})$ pairs. Its tightest margin is harm prevention: 0.450 vs. the 0.40 aspiration, a margin of 0.050. But it clears every threshold. **PASS.**

**$a_3$ (Reduce distribution):**

| Component | Worst value | Aspiration | Margin | Result |
|-----------|-------------|------------|--------|--------|
| FreeExpr | 0.5500 | 0.40 | +0.150 | Pass |
| Harm | 0.5500 | 0.40 | +0.150 | Pass |
| Trust | 0.4975 | 0.45 | +0.047 | Pass |
| Consist | 0.5500 | 0.40 | +0.150 | Pass |
| Proport | 0.5500 | 0.40 | +0.150 | Pass |

Reduce distribution also passes on all five objectives. Its tightest margin is trust: 0.498 vs. the 0.45 aspiration. **PASS.**

**Result:**

$$\text{Sat}(F, \vec{r}) = \{a_2 \text{ (Context label)},\; a_3 \text{ (Reduce distribution)}\}$$

**Commentary:** No action's elimination at Layer 2 illustrates how constraints and aspirations interact. No action *passed* both hard constraints (free expression $\geq$ 0.20 — trivially — and proportionality $\geq$ 0.25). It is not a *dangerous* moderation choice. But its harm prevention and user trust scores are too low to be *adequate*. Leaving viral health misinformation completely unaddressed is safe (it doesn't suppress speech or violate proportionality) but insufficient (it doesn't prevent harm or maintain trust). Layer 1 catches the dangerous; Layer 2 catches the inadequate. Different filters, different purposes.

### Layer 3: Regret-Pareto

For each objective $i$ and action $a \in \text{Sat}$:

$$\rho_i(a) = \max_{P \in \mathcal{P},\, \vec{f} \in \mathcal{F}} \left[ \max_{a' \in F} \mathbb{E}_P[f_i(a')] - \mathbb{E}_P[f_i(a)] \right]$$

**Important:** The regret reference set is $F$ (the full feasible set), not $\text{Sat}$. Here $F = \{a_1, a_2, a_3\}$ — including No action ($a_1$), which failed satisficing but remains feasible. No action scores 0.95 on free expression under every model, so it generates speech-freedom regret for both active moderation strategies. This is by design: regret measures opportunity cost against *everything the system could have done*, not just the actions that met aspirations.

**Regret of $a_2$ (Context label):**

We find the maximum amount by which any action in $F$ (including No action) beats Context label on each objective, across all $(P, \vec{f})$ pairs. The action driving each positive gap is shown in parentheses:

| $(P, \vec{f})$ | FreeExpr | Harm | Trust | Consist | Proport |
|---|---|---|---|---|---|
| $(P_{\text{vir}}, \vec{f}_{\text{speech}})$ | $0.100$ ($a_1$) | $0.050$ ($a_3$) | $0$ | $0$ | $0$ |
| $(P_{\text{vir}}, \vec{f}_{\text{safety}})$ | $0.150$ ($a_1$) | $0.150$ ($a_3$) | $0$ | $0.050$ ($a_3$) | $0$ |
| $(P_{\text{vir}}, \vec{f}_{\text{moderate}})$ | $0.130$ ($a_1$) | $0.102$ ($a_3$) | $0$ | $0$ | $0$ |
| $(P_{\text{typ}}, \vec{f}_{\text{speech}})$ | $0.100$ ($a_1$) | $0$ | $0$ | $0$ | $0$ |
| $(P_{\text{typ}}, \vec{f}_{\text{safety}})$ | $0.150$ ($a_1$) | $0.080$ ($a_3$) | $0$ | $0.050$ ($a_3$) | $0$ |
| $(P_{\text{typ}}, \vec{f}_{\text{moderate}})$ | $0.130$ ($a_1$) | $0.035$ ($a_3$) | $0$ | $0$ | $0$ |

Regret (max positive gap per objective):

$$\vec{\rho}(a_2) = (0.150,\; 0.150,\; 0,\; 0.050,\; 0)$$

Context label now has *nonzero* regret on free expression: 0.150, driven by No action ($a_1$). No action scores 0.95 on free expression everywhere, while context labeling scores 0.80–0.85, so the gap is 0.10–0.15 depending on the $(P, \vec{f})$ pair. The maximum gap of 0.150 occurs under the safety evaluator (where $a_2$'s free expression is 0.80 vs. $a_1$'s 0.95). Context label's harm prevention regret remains 0.150 (driven by $a_3$, Reduce distribution) and its consistency regret remains 0.050. Trust and proportionality regret remain zero — no action in $F$ beats context labeling on those dimensions.

**Regret of $a_3$ (Reduce distribution):**

| $(P, \vec{f})$ | FreeExpr | Harm | Trust | Consist | Proport |
|---|---|---|---|---|---|
| $(P_{\text{vir}}, \vec{f}_{\text{speech}})$ | $0.350$ ($a_1$) | $0$ | $0.135$ ($a_2$) | $0.100$ ($a_2$) | $0.255$ ($a_2$) |
| $(P_{\text{vir}}, \vec{f}_{\text{safety}})$ | $0.400$ ($a_1$) | $0$ | $0.030$ ($a_2$) | $0$ | $0.115$ ($a_2$) |
| $(P_{\text{vir}}, \vec{f}_{\text{moderate}})$ | $0.370$ ($a_1$) | $0$ | $0.082$ ($a_2$) | $0.020$ ($a_2$) | $0.189$ ($a_2$) |
| $(P_{\text{typ}}, \vec{f}_{\text{speech}})$ | $0.350$ ($a_1$) | $0.020$ ($a_2$) | $0.1525$ ($a_2$) | $0.100$ ($a_2$) | $0.2975$ ($a_2$) |
| $(P_{\text{typ}}, \vec{f}_{\text{safety}})$ | $0.400$ ($a_1$) | $0$ | $0.059$ ($a_2$) | $0$ | $0.1725$ ($a_2$) |
| $(P_{\text{typ}}, \vec{f}_{\text{moderate}})$ | $0.370$ ($a_1$) | $0$ | $0.101$ ($a_2$) | $0.020$ ($a_2$) | $0.2375$ ($a_2$) |

$$\vec{\rho}(a_3) = (0.400,\; 0.020,\; 0.1525,\; 0.100,\; 0.2975)$$

Reduce distribution's free expression regret jumps from 0.250 (old, against Sat only) to 0.400 — driven by No action ($a_1$), which scores 0.95 on free expression vs. $a_3$'s 0.55. The maximum gap of 0.400 occurs under the safety evaluator (where $a_3$'s free expression is 0.55 vs. $a_1$'s 0.95). Reduce distribution also now shows a small harm prevention regret of 0.020, from Context label ($a_2$) under $(P_{\text{typ}}, \vec{f}_{\text{speech}})$ where $a_2$ scores 0.570 vs. $a_3$'s 0.550. Trust, consistency, and proportionality regret are still driven by Context label ($a_2$), with values similar to before.

**Pareto comparison of regret vectors:**

- $\vec{\rho}(a_2) = (0.150,\; 0.150,\; 0,\; 0.050,\; 0)$
- $\vec{\rho}(a_3) = (0.400,\; 0.020,\; 0.1525,\; 0.100,\; 0.2975)$

Neither Pareto-dominates the other. $a_2$ has lower regret on all five dimensions *except* harm prevention: speech 0.150 < 0.400, harm 0.150 > 0.020, trust 0 < 0.1525, consistency 0.050 < 0.100, proportionality 0 < 0.2975. The harm dimension prevents $a_2$ from dominating $a_3$.

$$R = \{a_2 \text{ (Context label)},\; a_3 \text{ (Reduce distribution)}\}$$

**Commentary on the asymmetry:** Both actions now carry speech-freedom regret driven by No action ($a_1$), which by definition does nothing to restrict speech. Context label's speech regret is 0.150 (it restricts speech mildly — adding a label to a post). Reduce distribution's speech regret is 0.400 (it restricts speech substantially — algorithmically suppressing a post's reach). This is the correct accounting: the "cost of moderation" in speech-freedom terms is measured against the option of not moderating at all, even though that option failed satisficing.

Context label's total regret exposure is $0.150 + 0.150 + 0.050 = 0.350$ on three dimensions. Reduce distribution's total regret exposure is $0.400 + 0.020 + 0.1525 + 0.100 + 0.2975 = 0.970$ on five dimensions. But MOADT does not sum these. Reduce distribution's regret says: "by choosing to throttle the post's distribution, you give up 0.40 free expression (vs. no action), 0.15 trust, 0.10 consistency, and 0.30 proportionality (vs. context labeling), while gaining only 0.02 harm prevention regret." Context label's regret says: "by choosing to just add context, you give up 0.15 free expression (vs. no action) and 0.15 harm prevention and 0.05 consistency (vs. reducing distribution)." Whether the extra harm prevention is worth the cost on other dimensions is a value judgment — and MOADT correctly identifies it as such.

### Layer 4: Deference

$|R| = 2 > 1$. The protocol terminates with **deference to the human moderator**.

The system presents both options with their regret profiles:

> **Option 1: Context label ($a_2$).** Worst-case regret: you give up 0.150 free expression (vs. no action), 0.150 harm prevention, and 0.050 consistency (vs. reducing distribution). Your trust and proportionality regret are zero — context labeling is at least as good as every feasible action on those two dimensions under every plausible model.
>
> **Option 2: Reduce distribution ($a_3$).** Worst-case regret: you give up 0.400 free expression (vs. no action), 0.020 harm prevention (vs. context labeling), 0.1525 user trust, 0.100 consistency, and 0.2975 proportionality (vs. context labeling). Distribution reduction has regret on every dimension — its advantage is that its harm prevention regret is very small (0.020).
>
> **The tradeoff is:** Both actions pay a speech-freedom cost relative to doing nothing — context labeling pays less (0.150 vs. 0.400) because it is less restrictive. Context labeling has better trust and proportionality (zero regret) but worse harm prevention (0.150 vs. 0.020 regret). The evaluators disagree about whether the additional harm prevention justifies those costs. This is the human moderator's call.

---

## 5. What Scalar Expected Utility Would Have Done

### 5.1 The Five-Dimensional Weight Problem

With five objectives, the weight vector $\vec{w} = (w_1, w_2, w_3, w_4, w_5)$ has four degrees of freedom. The space of "reasonable" weight profiles is vast. We examine three illustrative profiles.

**Under free-speech-heavy weights $(0.40, 0.15, 0.15, 0.15, 0.15)$:**

| Action | $(P_{\text{vir}}, \vec{f}_{\text{speech}})$ | $(P_{\text{vir}}, \vec{f}_{\text{safety}})$ | $(P_{\text{typ}}, \vec{f}_{\text{speech}})$ | $(P_{\text{typ}}, \vec{f}_{\text{safety}})$ |
|--------|---|---|---|---|
| $a_1$ (No action) | 0.697 | 0.599 | **0.730** | 0.643 |
| $a_2$ (Context label) | **0.735** | **0.670** | **0.748** | **0.686** |
| $a_3$ (Reduce dist.) | 0.569 | 0.578 | 0.562 | 0.571 |
| $a_5$ (Remove appeal) | 0.387 | 0.497 | 0.368 | 0.474 |
| $a_6$ (Remove perm.) | 0.285 | 0.391 | 0.267 | 0.366 |

Context label wins under all $(P, \vec{f})$ combinations. This is the one scenario where scalar EU and MOADT happen to agree — though they agree for different reasons.

**Under safety-heavy weights $(0.15, 0.40, 0.15, 0.15, 0.15)$:**

| Action | $(P_{\text{vir}}, \vec{f}_{\text{speech}})$ | $(P_{\text{vir}}, \vec{f}_{\text{safety}})$ | $(P_{\text{typ}}, \vec{f}_{\text{speech}})$ | $(P_{\text{typ}}, \vec{f}_{\text{safety}})$ |
|--------|---|---|---|---|
| $a_1$ (No action) | 0.538 | 0.415 | 0.603 | 0.491 |
| $a_2$ (Context label) | **0.648** | 0.582 | **0.678** | **0.616** |
| $a_3$ (Reduce dist.) | 0.557 | 0.590 | 0.550 | 0.583 |
| $a_5$ (Remove appeal) | 0.500 | **0.624** | 0.475 | 0.594 |
| $a_6$ (Remove perm.) | 0.449 | 0.567 | 0.424 | 0.536 |

Under safety-heavy weights with the safety evaluator and viral prior, **Remove with appeal ($a_5$) wins** at 0.624. Recall that $a_5$ fails the proportionality constraint — it is the treatment that MOADT eliminates at Layer 1. Scalar EU, having no constraint mechanism, recommends it anyway.

**Under equal weights $(0.20, 0.20, 0.20, 0.20, 0.20)$:**

| Action | $(P_{\text{vir}}, \vec{f}_{\text{speech}})$ | $(P_{\text{vir}}, \vec{f}_{\text{safety}})$ | $(P_{\text{typ}}, \vec{f}_{\text{speech}})$ | $(P_{\text{typ}}, \vec{f}_{\text{safety}})$ |
|--------|---|---|---|---|
| $a_1$ (No action) | 0.612 | 0.482 | 0.657 | 0.541 |
| $a_2$ (Context label) | **0.697** | **0.626** | **0.714** | **0.648** |
| $a_3$ (Reduce dist.) | 0.559 | 0.587 | 0.550 | 0.578 |
| $a_5$ (Remove appeal) | 0.432 | 0.563 | 0.407 | 0.533 |
| $a_6$ (Remove perm.) | 0.347 | 0.471 | 0.323 | 0.439 |

Context label wins under most combinations. But note the gap: under $(P_{\text{vir}}, \vec{f}_{\text{safety}})$, context label scores 0.626 while reduce distribution scores 0.587 — a gap of only 0.039. Slight weight adjustments could flip this recommendation.

### 5.2 The Constraint-Blindness Problem (Again)

Under safety-heavy weights, scalar EU recommends Remove with appeal for $(P_{\text{vir}}, \vec{f}_{\text{safety}})$. This action has proportionality = 0.20 for limited-reach content under the speech evaluator — below the 0.25 threshold. Scalar EU cannot see this because it averages proportionality across states and combines it with other objectives. The 0.20 proportionality score is "made up for" by higher scores in other states and higher harm prevention. But proportionality isn't tradeable — removing borderline content that few people were reading is disproportionate regardless of how much harm it prevents in the (unlikely) viral scenario.

### 5.3 The Evaluator-Sensitivity Problem

The deepest issue for scalar EU in the content moderation domain: the "optimal" action depends on *which evaluator's assessment you use*. Under safety-heavy weights:

- With $\vec{f}_{\text{speech}}$: Context label ($a_2$) wins
- With $\vec{f}_{\text{safety}}$: Remove with appeal ($a_5$) wins

The recommendation flips from "add context" to "remove the post" based entirely on which evaluator you trust more. A deployed content moderation system using scalar EU must commit to one evaluator's philosophical framework — or average over evaluators, which is itself a philosophical commitment. MOADT avoids this by requiring robustness across all three.

---

## 6. Summary of Protocol Execution

```
Input: 6 moderation actions x 3 impact states x 5 objectives x 2 priors x 3 evaluators

Robust Dominance:     Context label ≻_R Age-gate
                      Reduce distribution ≻_R Age-gate
                      Adm(A) = {No action, Context label, Reduce dist, Remove appeal, Remove perm}

Layer 1 (Constraints): Free expression >= 0.20 AND Proportionality >= 0.25 per-state, per-evaluator
                      Remove appeal    FAIL  (limited reach, speech eval: proportionality 0.20)
                      Remove permanent FAIL  (pervasive FE and proportionality violations)
                      C = {No action, Context label, Reduce dist, Age-gate}
                      F = Adm(C) = {No action, Context label, Reduce dist}

Layer 2 (Satisficing): r = (0.40, 0.40, 0.45, 0.40, 0.40)
                      No action FAIL (harm 0.215, trust 0.390 under worst model)
                      Sat = {Context label, Reduce dist}

Layer 3 (Regret):     rho(Context label) = (0.150, 0.150, 0, 0.050, 0)
                      rho(Reduce dist)   = (0.400, 0.020, 0.1525, 0.100, 0.2975)
                      [Regret measured against F, including No action (a1)]
                      Pareto-incomparable -> R = {Context label, Reduce dist}

Layer 4 (Deference):  |R| = 2 -> DEFER TO HUMAN MODERATOR
                      "Both actions have speech regret driven by No action.
                       Context label: 0.15 speech, 0.15 harm, 0.05 consistency regret.
                       Reduce dist: 0.40 speech, 0.02 harm, 0.15 trust, 0.10 consistency,
                       0.30 proportionality regret.
                       This is the human moderator's call."
```

---

## 7. What This Example Demonstrates

1. **Robust dominance does real work.** For the first time in our worked examples, the admissibility filter eliminates an action. Age-gating borderline political content is robustly dominated by both context labeling and distribution reduction — it is an intervention that no reasonable combination of priors and evaluators prefers. This is not a constraint violation or an aspiration failure; it is a structural property of the action. MOADT detects it before reaching the choice protocol.

2. **Three evaluators capture philosophical disagreement, not measurement noise.** The gap between $\vec{f}_{\text{speech}}$ and $\vec{f}_{\text{safety}}$ is not calibration error — it reflects a genuine normative question: when someone reads borderline health claims in a political post, is this an exercise of autonomy (speech evaluator) or a harmful exposure (safety evaluator)? MOADT's evaluator set $\mathcal{F}$ does not force a resolution. It tracks the disagreement through all four protocol layers and surfaces it precisely in the final regret profiles.

3. **Two simultaneous constraints catch different failure modes.** The free expression constraint ($\geq 0.20$) prevents the system from silencing speech with significant political content. The proportionality constraint ($\geq 0.25$) prevents responses whose severity is unmatched to the content's risk. Permanent removal fails both constraints. Removal with appeal passes the free expression constraint but fails the proportionality constraint — specifically for limited-reach content under the speech evaluator. The constraints are complementary: free expression asks "is this action censoring?" while proportionality asks "is this action's severity justified?"

4. **Inaction is safe but inadequate.** Doing nothing passes both hard constraints (it doesn't suppress speech or violate proportionality) and is eliminated only at Layer 2 (its harm prevention and trust scores are below aspiration). This mirrors the watchful waiting elimination in Paper 2: the constraint layer catches what is dangerous; the aspiration layer catches what is insufficient. Inaction for viral health misinformation is not *censorship* — but it is not *good enough*.

5. **The deference outcome is particularly natural.** The gap between context labeling and distribution reduction tracks a genuine policy disagreement that platform moderators face daily. Some platforms prefer minimal intervention (label and let users decide); others prefer active curation (reduce reach of borderline content). MOADT does not resolve this — it *cannot* resolve this, because the resolution depends on values that the evaluators themselves disagree about. Instead, it presents the exact tradeoff: both actions carry speech-freedom regret driven by the feasible-but-unsatisficing No action option — context labeling's is modest (0.150) while distribution reduction's is large (0.400). Context labeling additionally sacrifices 0.15 harm prevention, while distribution reduction sacrifices trust, consistency, and proportionality. A human moderator with knowledge of the specific content, the specific platform's values, and the specific user community can make this call with full information.

6. **Scalar EU is particularly dangerous for content moderation.** Under safety-heavy weights, scalar EU recommends removing borderline political content with appeal — an action that violates the proportionality constraint for limited-reach content. The "optimal" moderation decision depends on the weight vector (policy choice), the prior (virality estimate), and the evaluator (philosophical framework). A deployed system using scalar EU must commit to all three before seeing any content, and different commitments produce recommendations ranging from "add a label" to "remove the post." This is not a recommendation engine — it is a policy-laundering machine that presents arbitrary value choices as optimization results.

---

## Appendix: Computational Verification

All numerical results in this document were produced by the MOADT engine applied to the content moderation scenario. The computation output is available in `examples/paper3_output.txt` and can be independently verified. Each outcome set vector, dominance check, constraint analysis, satisficing comparison, and regret computation shown in this document matches the engine output exactly.

---

## References

- MOADT (Multi-Objective Admissible Decision Theory) is defined in the companion paper.
- Freeman (2025), "The Scalarization Trap," provides the motivation for why scalar expected utility is structurally problematic for alignment.
- Worked Example 1 (Resource Allocation) applies the same framework to a three-objective, five-action problem.
- Worked Example 2 (Medical Treatment Selection) applies it to a four-objective, six-action clinical scenario.
