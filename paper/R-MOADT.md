# MOADT: Multi-Objective Admissible Decision Theory

**C. Matt Freeman, Ph.D.**
**mattf@globalmoo.com**

*A formal decision theory for AI alignment*

---

## 1. Introduction and Motivation

> "Not everything that counts can be counted, and not everything that can be counted counts." — William Bruce Cameron (1963)

Von Neumann–Morgenstern expected utility theory is the standard foundation for rational decision-making under uncertainty. Its elegance is real: four axioms yield a unique (up to affine transformation) utility function, and rational action reduces to maximizing its expectation. But this elegance comes at a cost that alignment theory cannot afford.

The critical axiom is **completeness**: for any two outcomes $A$ and $B$, either $A \succeq B$ or $B \succeq A$. Completeness, together with independence and continuity, yields a utility representation that forces commensurability — every objective must be tradeable against every other at some rate. (Completeness alone gives only a total ordering; the fixed tradeoff rates come from the full axiom set. But completeness is the axiom MOADT drops, because it is the one that demands the ordering exist in the first place.) For a system managing objectives like *human safety*, *helpfulness*, and *honesty*, completeness implies there exists some quantity of helpfulness that compensates for a given loss in safety. This is not a feature; it is a structural limitation that alignment theory must address.

The formal ingredients for an alternative already exist. The possibility of rational incomplete preferences has been established by Dubra et al. (2004), Mandler (2005), and Eliaz and Ok (2006). The theory of coherent decision-making under imprecise probabilities was developed by Levi (1974), Walley (1991), and Seidenfeld, Schervish, and Kadane (1995). Robust Markov decision processes under set-valued uncertainty were formalized by Iyengar (2005) and Nilim and El Ghaoui (2005). Multi-objective reinforcement learning and sequential decision-making with vector-valued returns are surveyed in Roijers et al. (2013). And the theory of decision-making with imprecise probabilities is systematized in Troffaes (2007). MOADT synthesizes these threads into a unified decision architecture specifically designed for the alignment problem.

MOADT constructs a complete decision procedure — one that terminates with a concrete action recommendation — without ever requiring the agent to commit to a single scalar ranking of outcomes. It replaces the VNM axioms with five alternative axioms (Section 7), layers a choice protocol over robust Pareto admissibility (Section 4), and builds corrigibility in as a structural feature rather than an additional constraint (Section 5). Where VNM gives the agent one knob, MOADT gives it $k$ knobs and a disciplined procedure for turning them.

**Scope.** MOADT is specifically designed as an alignment-oriented decision architecture — a decision theory for AI systems operating under human oversight with multiple incommensurable objectives. It does not claim to replace VNM for all domains: for single-objective optimization with known utilities and precise probabilities, VNM remains the correct framework (Theorem 1 confirms this as a special case). MOADT's contribution is to the settings where VNM's structural properties — especially completeness and the implied commensurability — become liabilities rather than strengths.

**Why this matters for alignment.** The scalarization trap is not merely an aesthetic objection to VNM — it names a cluster of *unsolvable* problems that confront any system that compresses human values into a single number. The utility function must be specified with perfect precision (since any misspecification is aggressively optimized against); the agent must resist any modification to its utility function (since the current function ranks itself as optimal); and all values become tradeable against all other values at some rate (since completeness demands commensurability). These are structural consequences of the axioms, not merely engineering challenges. MOADT was designed from the ground up to sidestep these problems: imprecise probabilities replace the precision requirement, evaluator uncertainty dissolves modification resistance, and the rejection of completeness eliminates forced commensurability. The goal is a decision theory that is *amenable to alignment by construction* — one where the properties we need for safe AI (corrigibility, non-exploitation of value uncertainty, cooperation with human overseers) emerge from the formal structure rather than being bolted on as afterthoughts. Section 9 catalogues the honest difficulties MOADT faces — computational cost, specification challenges, instability under reflection — and argues that these are better-structured difficulties than those VNM imposes.

**Readers who prefer math-first:** The self-contained formal specification (6 definitions, 4 propositions, 2 theorems, 1 axiom) is in Section 12. Everything between here and there is motivation, proof, and discussion.

**On length.** This document is a technical report, not a conference submission. The core formal theory (Sections 1–7, 12) is approximately 30 pages; worked examples and extended discussion are included for completeness and reproducibility. A conference-length version would comprise Sections 1–7 and 12, with worked examples as supplementary material.

**The name.** MOADT stands for **Multi-Objective Admissible Decision Theory**. Each word maps to a core design commitment: the evaluation is *multi-objective* (vector-valued, never collapsed to a scalar), the filtering is *admissible* (robust Pareto dominance eliminates only provably inferior actions), the framework is a *decision theory* (it terminates with a concrete recommendation or a structured deferral, not merely a description of the Pareto frontier).

---

## 2. Formal Objects

We work with the following primitives.

**Outcomes.** Let $\Omega$ be a finite set of outcomes — concrete states of the world that might result from action.

**Actions.** Let $A$ be a finite set of available actions. Each action, combined with a state of the world, determines an outcome.

**States.** Let $S$ be a finite set of states of the world, representing the agent's uncertainty about the environment.

**Transition function.** A function $\omega: A \times S \to \Omega$ maps each action-state pair to the resulting outcome.

**Vector-valued evaluation.** An evaluation function $\vec{f}: \Omega \to \mathbb{R}^k$ maps each outcome to a $k$-dimensional vector, where each component $f_i(\omega)$ scores outcome $\omega$ on objective $i$. We do not assume these components are commensurable.

**Credal sets (Knightian uncertainty).** Rather than a single probability distribution $P$ over states, the agent maintains a *credal set* $\mathcal{P}$ — a closed, convex, compact set of probability distributions over $S$. This represents genuine uncertainty about the correct probabilistic model, not merely uncertainty within a model. When $|\mathcal{P}| = 1$, we recover the standard Bayesian setting. (Compactness is standard for credal sets on finite state spaces; see Levi 1974, Walley 1991.)

**Evaluator uncertainty (Goodhart guardrail).** Rather than a single evaluation function $\vec{f}$, the agent maintains an *evaluator set* $\mathcal{F}$ — a compact set of plausible evaluation functions $\vec{f}: \Omega \to \mathbb{R}^k$. This models uncertainty about whether the agent's measurement of each objective faithfully tracks the intended objective. When $|\mathcal{F}| = 1$, the agent fully trusts its own evaluations. The set $\mathcal{F}$ is the formal mechanism by which MOADT guards against Goodhart's law: optimizing a proxy that diverges from the true objective is detectable as sensitivity to evaluator choice.

**Outcome sets.** For each action $a \in A$, define the *outcome set*:

$$Y(a) = \left\{ \mathbb{E}_P[\vec{f}(\omega(a, s))] : P \in \mathcal{P},\; \vec{f} \in \mathcal{F} \right\}$$

That is, $Y(a)$ is the set of all *expected* evaluation vectors the agent considers possible for action $a$, one for each credal-evaluator pair $(P, \vec{f})$. This set captures the agent's epistemic uncertainty — uncertainty about which probabilistic model and which evaluator are correct. Each element of $Y(a)$ is itself an expectation over aleatoric uncertainty (which state obtains). Since $Y(a)$ is the image of the compact set $\mathcal{P} \times \mathcal{F}$ under a continuous map, $Y(a)$ is compact (and in particular closed and bounded) in $\mathbb{R}^k$.

---

## 3. Core Rationality: Robust Pareto Admissibility

### 3.1 Standard Pareto Dominance

We first recall the standard notion. For vectors $\vec{x}, \vec{y} \in \mathbb{R}^k$:

$$\vec{x} \succ_P \vec{y} \iff x_i \geq y_i \;\forall\, i \in \{1, \ldots, k\} \;\text{ and }\; \exists\, j \text{ s.t. } x_j > y_j$$

That is, $\vec{x}$ Pareto-dominates $\vec{y}$ if it is at least as good on every objective and strictly better on at least one. This is a *partial* order: many pairs of vectors are incomparable.

### 3.2 Robust Dominance

Standard Pareto dominance compares individual outcome vectors. To compare *actions* — which map to *sets* of possible outcome vectors — we need a notion of dominance that is robust to the agent's uncertainty.

**Definition (Robust Dominance).** Action $a$ robustly dominates action $b$, written $a \succ_R b$, if and only if:

$$\forall\, \vec{y}_b \in Y(b),\; \exists\, \vec{y}_a \in Y(a) \;\text{ s.t. }\; \vec{y}_a \succ_P \vec{y}_b$$

The quantifier structure is $\forall$-$\exists$: for every realization of $b$'s uncertainty, there exists *some* (potentially different) realization of $a$'s uncertainty that dominates it. This is deliberately weaker than *uniform dominance* ($\forall\, (P, \vec{f}): \mathbb{E}_P[\vec{f}(a)] \succ_P \mathbb{E}_P[\vec{f}(b)]$), which would require $a$ to beat $b$ under the *same* model. The $\forall$-$\exists$ structure makes robust dominance a *defensive* criterion: $a$ can "defend" against each of $b$'s realizations, but possibly with a different model each time.

**Why $\forall$-$\exists$ and not a stronger quantifier.** An important design choice deserves explicit defense. The $\forall$-$\exists$ structure permits *model-switching*: when verifying that $a$ dominates $b$, the defending realization $\vec{y}_a$ can come from a different $(P, \vec{f})$ for each attacking realization $\vec{y}_b$. This means the agent cannot point to a single world-model under which $a$ uniformly beats $b$ — it can only say "for each way $b$ might turn out, $a$ has *some* way of turning out better." A skeptic might object that this is too permissive.

We considered two natural alternatives:

- **Uniform dominance** ($\forall\forall$): $\forall (P, \vec{f}) \in \mathcal{P} \times \mathcal{F}: \mathbb{E}_P[\vec{f}(a)] \succ_P \mathbb{E}_P[\vec{f}(b)]$ — requires $a$ to beat $b$ under the *same* model. This is clean but typically yields an empty admissible set (nothing uniformly dominates anything when uncertainty is broad). For alignment purposes, a dominance relation that almost never holds provides no useful structure.

- **Lower-envelope dominance**: compare worst cases, i.e., $\underline{y}_i(a) = \min_{P,\vec{f}} \mathbb{E}_P[f_i(a)]$ and declare $a \succ_{LE} b$ iff $\underline{\vec{y}}(a) \succ_P \underline{\vec{y}}(b)$. This is genuinely robust but collapses each action to its coordinatewise worst case, discarding all information about the shape and spread of $Y(a)$. It is also extremely pessimistic: an action that is excellent under most models but poor under one outlier model gets represented solely by that outlier.

The $\forall$-$\exists$ structure occupies the middle ground. Its "weakness" — that it is hard to establish dominance — is *the correct behavior for a cooperative decision theory*. When the agent cannot establish that one action dominates another, both remain in $\text{Adm}(A)$, and the choice is refined by the layered protocol or deferred to the principal. Model-switching does not distort the final decision because dominance is only used to *eliminate* options, never to *select* among them. An action that survives elimination via model-switching is simply one the agent cannot confidently discard — which is exactly when it should keep the option open for human judgment.

**Normative defense: epistemic coherence of $\forall$-$\exists$.** The pragmatic argument above shows that $\forall$-$\exists$ produces useful behavior. But is it *epistemically justified* — does it correctly represent what the agent knows? We argue yes: the $\exists$ quantifier on the defending side reflects the agent's genuine uncertainty about which model is true. The agent does not choose which $(P, \vec{f})$ obtains — nature does. When the agent verifies $a \succ_R b$, it asks: "for each way $b$ might turn out (under some model I consider plausible), can I identify *some* plausible model under which $a$ turns out better?" This is not cherry-picking; it is the epistemic posture of an agent that cannot rule out any model in its credal-evaluator set. The $\forall$-$\exists$ structure formalizes the principle that *an action should be eliminated only if no plausible world vindicates it*. Compare: in classical hypothesis testing, we reject a hypothesis only if the data are implausible under *every* parameter value in the null — a $\forall$-$\exists$ structure on the evidential side. Similarly, MOADT eliminates an action only if it is dominated under *every* realization of the opponent and *no* realization of the defender can answer. The defender's $\exists$ is the formal expression of "I cannot rule out that $a$ is better" — which, given genuine model uncertainty, is the epistemically honest assessment. Demanding $\forall$-$\forall$ (uniform dominance) would require the agent to be confident that $a$ beats $b$ under *every* model simultaneously — a standard of proof appropriate for certainty, not for the Knightian uncertainty that MOADT was designed to handle.

**Consequence for admissible set size.** The $\forall$-$\exists$ structure means robust dominance is hard to establish — especially when $\mathcal{P}$ and $\mathcal{F}$ are broad — so $\text{Adm}(A)$ will often contain most or all of $A$. This is by design: when uncertainty is large, the theory should declare many actions incomparable rather than fabricate a ranking. The practical filtering work is then done by Layers 1–3 of the choice protocol (Section 4), not by robust dominance alone.

**Remark on coupling and model-switching.** A technically precise objection to $\forall$-$\exists$ dominance is that the defending realization $\vec{y}_a$ may come from a different $(P, \vec{f})$ for each attacking $\vec{y}_b$, so dominance can be established even when no single model certifies $a$ as uniformly superior. For example, with $k = 2$, let $Y(b) = \{(2, 0),\, (0, 2)\}$ and $Y(a) = \{(3, 0),\, (0, 3)\}$. Then $a \succ_R b$ holds — for attacker $(2, 0)$ pick defender $(3, 0)$; for $(0, 2)$ pick $(0, 3)$ — yet no single point in $Y(a)$ dominates both points in $Y(b)$. The correct reading is that $\succ_R$ is a *set-wise eliminator*, not a statement about any joint coupling of uncertainties between actions. It certifies "every way $b$ could turn out has *some* way $a$ could turn out that is better" — a guarantee about the geometry of $Y(a)$ relative to $Y(b)$, not about what happens under a shared draw from $(\mathcal{P}, \mathcal{F})$. This is precisely the right semantics for *elimination* (which needs only to certify that no plausible world vindicates the dominated action) as opposed to *selection* (which would require a coherent world-model for the chosen action). Since MOADT uses dominance exclusively for elimination — never for selection — the coupling objection, while technically correct about the quantifier structure, is a category error about its intended role.

**Elimination safety: the scalar confinement result.** We acknowledge directly that $\forall$-$\exists$ dominance can eliminate actions that are not dominated under any single coherent $(P, \vec{f})$ pair. This is not hidden — it is the intended semantics. But the scope of this phenomenon is sharply confined.

> **Proposition (Scalar Confinement).** For $k \geq 2$ and actions $a, b$ with outcome sets $Y(a), Y(b) \subset \mathbb{R}^k$, the set of pairs $(Y(a), Y(b))$ for which $a \succ_R b$ (i.e., $b$ is eliminated by $\forall$-$\exists$ dominance) is a strict subset of the set for which componentwise maximax would select $a$ over $b$. In particular, if $Y(a)$ and $Y(b)$ are not totally ordered on any single component, $\succ_R$ is generically empty.

*Proof sketch.* For $k = 1$, Pareto dominance reduces to $>$, and the $\exists$ quantifier on the defending side selects the best-case model — producing maximax (as shown in the Remark following Theorem 1). For $k \geq 2$, $a \succ_R b$ requires that for each $\vec{y}_b \in Y(b)$, the defending witness $\vec{y}_a \in Y(a)$ must satisfy $y_{a,i} \geq y_{b,i}$ for *all* $i$ simultaneously, with strict inequality on at least one component. The $\exists$ quantifier must find a single point that dominates on all $k$ dimensions at once — a condition that becomes exponentially harder to satisfy as $k$ grows. Componentwise maximax, by contrast, only requires $\max_{Y(a)} y_i \geq \max_{Y(b)} y_i$ for each $i$ separately — a much weaker condition that permits different maximizing points for different components. When $k \geq 2$ and the outcome sets have spread across dimensions (the generic case under broad $\mathcal{P} \times \mathcal{F}$), the Pareto frontier of $Y(a)$ trades off components against each other, making it increasingly unlikely that any single point in $Y(a)$ can simultaneously dominate a given point in $Y(b)$ on all dimensions. $\square$

The epistemically dubious aspect of $\forall$-$\exists$ — that elimination does not require a coherent joint model — is the price paid for a dominance relation that is neither vacuously strict ($\forall$-$\forall$) nor information-destroying (lower-envelope). For alignment applications where $k \geq 3$ and uncertainty is broad, this price is low: $\forall$-$\exists$ dominance is extremely hard to establish, and the practical filtering is done by Layers 1–3.

**Definition (Admissible Set).** The admissible set is:

$$\text{Adm}(A) = \{ a \in A : \neg\exists\, a' \in A \text{ s.t. } a' \succ_R a \}$$

The admissible set contains every action that is not robustly dominated by any alternative. These are the actions that a rational agent *could* choose without violating Pareto unanimity.

### 3.3 Basic Properties

**Proposition 1 (Strict Partial Order).** Robust dominance $\succ_R$ is a strict partial order on $A$: it is irreflexive and transitive.

*Proof sketch.* Irreflexivity: $a \succ_R a$ would require that for every $\vec{y} \in Y(a)$, there exists $\vec{y}' \in Y(a)$ with $\vec{y}' \succ_P \vec{y}$. We show this is impossible. Since $Y(a)$ is compact, for any strictly positive weight vector $\vec{w} \in \mathbb{R}^k_{>0}$, the continuous function $\vec{y} \mapsto \vec{w} \cdot \vec{y}$ attains its maximum on $Y(a)$ at some point $\vec{y}^*$. This $\vec{y}^*$ is Pareto-maximal in $Y(a)$: if some $\vec{y}' \succ_P \vec{y}^*$, then $\vec{w} \cdot \vec{y}' > \vec{w} \cdot \vec{y}^*$ (since $w_i > 0$ for all $i$ and $y'_j > y^*_j$ for some $j$), contradicting the maximality of $\vec{y}^*$. Since $\vec{y}^*$ is Pareto-maximal, no $\vec{y}' \in Y(a)$ satisfies $\vec{y}' \succ_P \vec{y}^*$ — contradiction with the requirement of $a \succ_R a$. Transitivity: if $a \succ_R b$ and $b \succ_R c$, then for any $\vec{y}_c \in Y(c)$ there exists $\vec{y}_b \in Y(b)$ with $\vec{y}_b \succ_P \vec{y}_c$, and for that $\vec{y}_b$ there exists $\vec{y}_a \in Y(a)$ with $\vec{y}_a \succ_P \vec{y}_b$. By transitivity of $\succ_P$, $\vec{y}_a \succ_P \vec{y}_c$. $\square$

**Proposition 2 (Non-emptiness).** For finite $A$, $\text{Adm}(A) \neq \emptyset$.

*Proof sketch.* Suppose $\text{Adm}(A) = \emptyset$. Then every action is robustly dominated, which (by finiteness and transitivity) produces a cycle — contradicting irreflexivity. More precisely: start from any $a_1$, find $a_2 \succ_R a_1$, then $a_3 \succ_R a_2$, etc. Since $A$ is finite, some $a_j$ must repeat, yielding $a_j \succ_R \cdots \succ_R a_j$, contradicting the strict partial order. $\square$

**Theorem 1 (Backward Compatibility with Expected Utility).** When $|\mathcal{P}| = 1$, $|\mathcal{F}| = 1$, and $k = 1$ (single objective), robust admissibility reduces to expected utility maximization.

*Proof sketch.* With a single prior $P$, a single evaluator $f: \Omega \to \mathbb{R}$, and one objective, there is exactly one credal-evaluator pair, so $Y(a) = \{\mathbb{E}_P[f(\omega(a, s))]\}$ — a singleton scalar. Robust dominance $a \succ_R b$ reduces to $\mathbb{E}_P[f(a)] > \mathbb{E}_P[f(b)]$ (standard scalar dominance). The admissible set $\text{Adm}(A)$ becomes $\arg\max_{a \in A} \mathbb{E}_P[f(a)]$ — the expected-utility-maximizing action(s). $\square$

**Remark (partial relaxation: $k = 1$, $|\mathcal{F}| = 1$, $|\mathcal{P}| > 1$).** When $k = 1$ and $|\mathcal{F}| = 1$ but $|\mathcal{P}| > 1$, each action's outcome set is $Y(a) = \{ \mathbb{E}_P[f(a)] : P \in \mathcal{P} \}$ — an interval on $\mathbb{R}$. Robust dominance $b \succ_R a$ then requires: for every $y_a \in Y(a)$, there exists $y_b \in Y(b)$ with $y_b > y_a$. Since the hardest case for the dominator is $y_a = \max Y(a)$, this reduces to $\max Y(b) > \max Y(a)$, i.e., $\max_{P \in \mathcal{P}} \mathbb{E}_P[f(b)] > \max_{P \in \mathcal{P}} \mathbb{E}_P[f(a)]$. The admissible set is therefore $\arg\max_{a \in A} \max_{P \in \mathcal{P}} \mathbb{E}_P[f(a)]$ — the *maximax* criterion, not E-admissibility.

*Counterexample separating maximax from E-admissibility.* Let $\mathcal{P} = \{P_1, P_2\}$ with $Y(a) = \{3, 1\}$ and $Y(b) = \{2, 4\}$ (expected utilities under the two priors). Then $\max Y(b) = 4 > 3 = \max Y(a)$, so $b \succ_R a$ and MOADT selects $\{b\}$. But both actions maximize expected utility under some prior ($a$ under $P_1$, $b$ under $P_2$), so both are E-admissible under Levi's (1974) criterion.

The $\forall$-$\exists$ quantifier structure lets the dominating action always deploy its most favorable prior against each of the dominated action's scenarios, producing a more aggressive selection than E-admissibility's $\forall$-$\forall$ (uniform dominance) criterion, which corresponds to the symmetric variant discussed in Section 3.2. This aggressive behavior in the scalar limit is acceptable because MOADT is designed for multi-objective use ($k \gg 1$), where the outcome sets $Y(a) \subset \mathbb{R}^k$ are genuinely multi-dimensional and robust dominance is correspondingly harder to establish. The protocol layers — constraints, satisficing, regret-Pareto, and deference — provide the real normative filtering, not the admissibility criterion alone. The $\forall$-$\exists$ quantifier structure is thus a deliberate design trade-off: it provides the conservative, cautious-dominator semantics needed for multi-dimensional robustness (the intended operating regime), at the cost of aggressive maximax behavior in the scalar limit (a degenerate case that the protocol layers compensate for).

This theorem establishes that MOADT is a *generalization* of expected utility theory, not an alternative that discards its valid insights.

### 3.4 Relationship to Multi-Objective Reinforcement Learning

MOADT builds on a substantial body of work in multi-objective reinforcement learning (MORL) and multi-objective decision support. Several of MOADT's components have precedents in this literature, and we are explicit about what MOADT inherits, what it adds, and where it differs.

**What MOADT inherits.** Set-valued value functions and Pareto frontier maintenance are established MORL techniques. Pareto Q-learning (Van Moffaert and Nowé 2014) maintains sets of Pareto-dominating policies; optimistic linear support (Roijers et al. 2015) addresses the computational cost of frontier construction; and multi-objective decision support systems (Vamplew et al. 2018, 2022) already propose presenting Pareto frontiers to human decision-makers rather than selecting a single action. MOADT's set-valued Bellman equation (Section 6.3) is a direct generalization of these approaches. Lexicographic methods in MORL (Gabor et al. 1998, Wray et al. 2015) handle priority ordering of objectives — a natural comparison point for MOADT's constraint layer, which implements a strict form of lexicographic priority (constraints are non-negotiable preconditions, not soft priorities).

**What MOADT adds.** The alignment-specific contributions are: (i) *credal sets* — MORL typically assumes a known transition model, while MOADT's credal sets formalize Knightian uncertainty about the environment; (ii) *evaluator uncertainty* — the $\mathcal{F}$ set models proxy-divergence risk (Goodhart's law), which has no direct MORL analogue; (iii) *the corrigibility theorem* — the formal result (Theorem 2) connecting evaluator uncertainty to modification permissibility is, to our knowledge, novel; (iv) *the four-layer governance architecture* — existing MORL systems present Pareto frontiers but do not specify a principled protocol for narrowing the frontier to a recommendation. MOADT's layers (constraints → satisficing → regret-Pareto → deference) provide this protocol, with the deference node explicitly integrating the principal as a structural element.

**Where MOADT differs.** Standard MORL seeks a *coverage set* — a set of policies such that for any possible weight vector, some policy in the set is optimal. This implicitly assumes the user has scalar preferences that are unknown to the system. MOADT makes no such assumption: the framework does not posit a latent scalar utility that the principal 'really' has. The admissible set is not a coverage set for unknown weights — it is the set of actions that survive robust multi-dimensional elimination. This difference matters for alignment: a coverage-set approach recovers scalar utility the moment weights are revealed, reintroducing the commensurability that MOADT was designed to avoid.

---

## 4. Choice Protocol Without Global Scalarization

The admissible set $\text{Adm}(A)$ may contain many actions — this is a feature, not a bug. Incomparability is genuine and should be preserved, not artificially resolved. But the agent must ultimately *act*. The following four-layer protocol narrows $A$ to a concrete recommendation without maintaining a global scalar utility function that assigns unbounded tradeoff rates between objectives.

**A note on "no scalarization."** Any terminating decision procedure needs tie-breaking mechanisms, and some of these involve scalar-valued functions (the achievement scalarizing function in Layer 2's fallback, the per-objective normalization factors $\sigma_i$ in regret computation). MOADT's claim is not that no scalar quantity ever appears, but that *no global scalar utility function exists that supports unbounded cross-objective tradeoffs*. Every scalar-like computation in the protocol is (a) local to a specific layer, (b) reference-dependent (measuring shortfall from aspirations, not absolute value), (c) bounded by hard constraints that cannot be overridden, and (d) defeasible — the agent can always defer to the principal rather than relying on any scalar tiebreaker. The structural danger is not the existence of numbers but the existence of a *single number* that ranks all outcomes and justifies arbitrary exchanges. MOADT never constructs such a number.

### Layer 1: Constraints (Hard Thresholds)

Some objectives are not tradeable at any rate. Safety floors, ethical bright lines, and resource minima are not goals to optimize — they are preconditions for acceptable action.

**Definition (Constraint Satisfaction).** For a subset of objectives $I_C \subseteq \{1, \ldots, k\}$, fix thresholds $\tau_i$ for each $i \in I_C$. An action $a$ satisfies the constraints if and only if:

$$\forall\, P \in \mathcal{P},\; \forall\, \vec{f} \in \mathcal{F},\; \forall\, s \in \text{supp}(P): \quad f_i(\omega(a, s)) \geq \tau_i \quad \forall\, i \in I_C$$

Let $C = \{ a \in A : a \text{ satisfies all constraints} \}$ be the constraint-satisfying set. The feasible set is:

$$F = \text{Adm}(C)$$

That is, first restrict to actions that satisfy all constraints, then compute robust admissibility *within* the constraint-satisfying set. This ordering is critical: it prevents constraint-violating actions from robustly dominating (and thereby excluding) safe alternatives. A constraint-violating action that scores higher on every objective is still excluded — it never enters the comparison.

The universal quantification over $\mathcal{P}$ and $\mathcal{F}$ in constraint checking is also critical: constraint satisfaction is required under *every* model the agent considers plausible. This embodies a precautionary principle for safety-critical thresholds.

**Support sensitivity.** The quantification $\forall s \in \text{supp}(P)$ is deliberately strict: a single state with nonzero probability that violates the constraint kills the action, even if that state has probability $10^{-15}$ under some $P \in \mathcal{P}$. This means constraint satisfaction is highly sensitive to the *support* of the credal set. If $\mathcal{P}$ contains any distribution that puts positive probability on a catastrophic state, every action that could reach that state is excluded. This is the intended behavior for safety-critical thresholds — but it makes the specification of $\mathcal{P}$'s support a consequential design decision. An overly broad credal set (one that puts positive probability on states that are physically impossible) can make $C = \emptyset$ spuriously. The specification of $\mathcal{P}$ is thus not only an epistemic commitment but a safety-engineering decision.

**Practical mitigation: support specification.** The most direct defense against spurious emptying of $C$ is disciplined specification of $\mathcal{P}$'s support. In practice, the credal set should be constructed over a *shared support* $S_0 \subseteq S$ representing states the designer considers physically realizable, with distributions in $\mathcal{P}$ differing in how they weight those states — not in which states they consider possible. This separates two design decisions: "what states exist?" ($S_0$) and "how likely are they?" ($\mathcal{P}$). For domains where the support itself is uncertain, a probability-floor variant replaces $\forall\, s \in \text{supp}(P)$ with $\forall\, s$ such that $\min_{P \in \mathcal{P}} P(s) \geq \delta$ for designer-specified $\delta > 0$. This prevents an adversary from emptying $C$ by inserting infinitesimal-mass pathological states into $\mathcal{P}$, at the cost of weakening the worst-case guarantee to states above the probability floor. The choice between strict support quantification and $\delta$-thresholded quantification is a safety-engineering decision that should be made explicitly per deployment context.

We are candid about a tension here: the $\delta$-floor variant, while practically useful, is effectively a soft constraint on rare states — accepting some probability of constraint violation below the floor. This is not qualitatively different from a probabilistic constraint $P(\text{violation}) \leq \delta$, which the strict universal-quantification formulation was designed to avoid. The choice between strict support quantification and $\delta$-thresholding is thus not merely a tuning decision but a philosophical one: how absolutely must the worst case be excluded? MOADT offers both options and requires the designer to choose explicitly, rather than hiding the choice inside a single formulation.

**Important caveat:** If $C = \emptyset$, no action meets all constraints under all uncertainty. The agent must then flag this to the principal rather than silently relaxing constraints. Constraint violation is an *error condition*, not a tradeoff.

### Layer 2: Reference-Point Satisficing (Aspiration Levels)

Beyond hard constraints, the agent maintains a *reference point* $\vec{r} \in \mathbb{R}^k$ — a context-dependent aspiration level for each objective. The reference point encodes "what would count as good enough" rather than "what is the maximum possible."

**Where reference points come from.** The reference point $\vec{r}$ is a design parameter, not derived from the decision theory itself. Possible sources include: (a) principal specification — the principal directly sets aspiration levels per objective; (b) historical baseline — $\vec{r}$ is set to the agent's recent performance on each objective, encoding a "do no worse" heuristic; (c) percentile anchoring — $r_i$ is set to the $p$-th percentile of $f_i$ values across the feasible set, for some designer-chosen $p$. We are explicit that this is where substantial decision-making power resides: the choice of $\vec{r}$ determines which actions survive Layer 2, and changing $\vec{r}$ can change the outcome. MOADT does not claim to derive aspiration levels from first principles — it claims only that aspiration-based satisficing is a less dangerous structure than unbounded tradeoffs.

**Governance properties of $\vec{r}$.** The reference point's power raises three governance questions. *Adversarial manipulation:* A principal who controls $\vec{r}$ can steer the agent's behavior by raising aspirations on some objectives and lowering others, effectively selecting among admissible actions without the agent 'noticing' manipulation. This is by design — the principal *should* be able to influence the agent's behavior through aspiration-setting, just as they can through constraint-setting. The defense against adversarial manipulation is the same as for constraints: the principal's authority to set $\vec{r}$ is part of the cooperative architecture, not a vulnerability. *Diachronic stability:* If $\vec{r}$ changes over time (e.g., historical baselines shift as the agent performs well), the satisficing set changes correspondingly. This does not violate dynamic consistency (Section 6.2) — changing $\vec{r}$ is new information about the principal's aspirations, not a preference reversal. But rapid $\vec{r}$ oscillation could produce erratic behavior; in practice, $\vec{r}$ should be updated on a slower timescale than individual decisions. *No internal constraint on $\vec{r}$:* MOADT does not impose rationality constraints on the reference point (such as requiring $\vec{r}$ to lie within the feasible frontier). This is deliberate: aspirations can be ambitious (above the frontier, guaranteeing $\text{Sat} = \emptyset$ and triggering the ASF fallback) or conservative (below the frontier, making Layer 2 nearly vacuous). Both are legitimate governance postures.

**Definition (Satisficing Set).** The satisficing set is:

$$\text{Sat}(F, \vec{r}) = \{ a \in F : \forall\, \vec{y} \in Y(a),\; \vec{y} \geq \vec{r} \}$$

If $\text{Sat}(F, \vec{r}) \neq \emptyset$, restrict attention to it. These are actions that meet or exceed the aspiration level on every objective *under every plausible model* — not merely under some optimistic scenario.

**Why robust satisficing.** Consistency demands it. Layer 1 constraints use universal quantification over $\mathcal{P}$ and $\mathcal{F}$ because safety thresholds must hold under all plausible models. Aspiration levels should obey the same epistemic discipline: if the agent's aspiration is "achieve at least $r_i$ on objective $i$," then it should achieve this robustly, not merely under a cherry-picked model. The difference between constraints and aspirations is not the quantifier structure but the *failure mode*: constraint violation is an error condition, while failing to meet aspirations triggers graceful degradation via the fallback mechanism below.

**Exploratory mode (optional, explicitly scoped).** In low-stakes or reversible decision contexts, a designer may substitute *existential satisficing*: $\text{Sat}^{\exists}(F, \vec{r}) = \{ a \in F : \exists\, \vec{y} \in Y(a) \text{ s.t. } \vec{y} \geq \vec{r} \}$. This permits actions that *might* meet aspirations under favorable conditions, enabling exploration when the cost of falling short is bounded and recoverable. Existential satisficing must be explicitly enabled per decision context and disabled by default — it represents a deliberate relaxation of the robustness posture, not the framework's natural mode.

**Fallback when $\text{Sat} = \emptyset$.** If no action achieves the reference point, select the action closest to $\vec{r}$ using the *achievement scalarizing function* (Wierzbicki 1980):

$$\text{asf}(a, \vec{r}) = \min_{i \in \{1,\ldots,k\}} \min_{\vec{y} \in Y(a)} \frac{y_i - r_i}{\sigma_i}$$

where $\sigma_i > 0$ is a normalization factor for objective $i$. Select $\arg\max_{a \in F} \text{asf}(a, \vec{r})$.

If $\text{Sat}(F, \vec{r}) = \emptyset$, the fallback selects directly from $F$ and Layer 3 does not apply — the achievement scalarizing function has already resolved the selection. Layer 3 applies only when $\text{Sat}(F, \vec{r}) \neq \emptyset$ and further narrowing is needed.

**Scope note:** This fallback is a scalar-valued function, and we are explicit about it rather than pretending otherwise. It is (a) local — used only when no action robustly meets aspirations, (b) temporary — abandoned once aspirations are revised, (c) reference-dependent — it measures *shortfall from aspirations*, not absolute value, and (d) bounded — hard constraints (Layer 1) cannot be overridden by the ASF, so the scalar computation can never justify crossing a safety threshold. It is a controlled emergency heuristic, not a global utility function.

**Formal safety properties of the ASF.** Three claims about the fallback mechanism: (1) *The ASF cannot produce modification resistance.* Theorem 2's corrigibility result applies at the robust-dominance level (Layer 0), which is computed before the ASF is invoked. The ASF operates only when $\text{Sat} = \emptyset$ — a fallback condition — and selects within $F \subseteq C$. It cannot override the admissibility of both accept and resist established by Theorem 2. (2) *The ASF cannot produce unbounded tradeoffs.* The ASF selects from $F = \text{Adm}(C)$, which is bounded by Layer 1 constraints. No ASF-selected action can violate a constraint (Proposition 3), so the compensation the ASF permits is capped by the constraint thresholds. (3) *The normalization vector $\vec{\sigma}$ is a form of value judgment.* We acknowledge this: $\sigma_i$ determines how much shortfall on objective $i$ 'counts' relative to shortfall on objective $j$. This is a bounded, local, reference-dependent form of commensuration — it determines which aspiration-miss is worst, not a global exchange rate between objectives. It is a weaker commitment than a utility weight, but it is a commitment nonetheless.

**Proposition 3 (Constraint Primacy).** The Layer 2 fallback (ASF) operates exclusively on $F = \text{Adm}(C)$, and cannot select any action outside $C$. Therefore no outcome of Layers 2–4 can violate a Layer 1 constraint.

*Proof sketch.* The ASF selects $\arg\max_{a \in F} \text{asf}(a, \vec{r})$. Since $F \subseteq C$ by construction ($F = \text{Adm}(C)$ and $\text{Adm}(C) \subseteq C$), every action in the ASF's domain satisfies all constraints. The ASF's scalar optimization cannot expand its domain beyond $F$ — it is a selection rule over a pre-filtered set, not a criterion that competes with constraints. $\square$

### Layer 3: Regret-Pareto (Minimax Regret per Objective)

Among the surviving actions, we minimize worst-case *regret* — but crucially, we keep regret as a vector rather than aggregating it.

**Definition (Per-Objective Minimax Regret).** For each objective $i$ and action $a \in \text{Sat}(F, \vec{r})$ (or $F$ if satisficing is vacuous):

$$\rho_i(a) = \max_{P \in \mathcal{P},\, \vec{f} \in \mathcal{F}} \left[ \max_{a' \in F} \mathbb{E}_P[f_i(\omega(a', s))] - \mathbb{E}_P[f_i(\omega(a, s))] \right]$$

This is the worst-case regret for action $a$ on objective $i$: the maximum (across all models) of the gap between the best available action and $a$ on that objective.

**Why regret is measured against $F$, not $\text{Sat}$.** The benchmark in the regret computation — $\max_{a' \in F}$ — ranges over the full feasible set $F$, not the satisficing set $\text{Sat}(F, \vec{r})$. This is deliberate. Actions excluded by satisficing were rejected for failing to meet aspirations, but they may still define per-objective benchmarks: an action that excels on safety but fails on cost is still the relevant comparator for safety regret. Measuring regret against $F$ ensures that satisficing cannot hide opportunity costs — the agent knows what it gave up by restricting attention to aspiration-meeting actions. This mirrors how Layer 1 uses the full action set $A$ to define the constraint-satisfying set $C$, not a pre-filtered subset: each layer's inputs are defined by the full information available, even when the layer's *outputs* are restricted. Measuring regret against $\text{Sat}$ would also create an undesirable coupling between Layers 2 and 3: changing aspiration levels $\vec{r}$ would change not only which actions survive Layer 2 but also the *regret benchmark* in Layer 3, making regret depend on aspiration levels rather than on what is feasible. The protocol's modular design deliberately avoids such inter-layer coupling.

**Definition (Regret Vector).** The regret vector of action $a$ is $\vec{\rho}(a) = (\rho_1(a), \ldots, \rho_k(a))$.

**Definition (Regret-Pareto Selection).** The regret-Pareto set is:

$$R = \{ a : \neg\exists\, a' \text{ s.t. } \rho_i(a') \leq \rho_i(a) \;\forall\, i \text{ and } \rho_j(a') < \rho_j(a) \text{ for some } j \}$$

That is, $R$ consists of actions whose regret vectors are Pareto-minimal — no alternative achieves weakly lower regret on all objectives and strictly lower on at least one.

**Remark on regret and implicit risk attitudes.** Minimax regret is not a value-neutral computation — it encodes a specific robustness philosophy: *worst-case gap control*. The agent minimizes the maximum possible gap between its chosen action and the best available action on each objective, under adversarial model selection. This is a conservative (maximin-style) posture applied per-objective. We are explicit that this imports a risk attitude into Layer 3: an agent that is risk-neutral or risk-seeking with respect to opportunity costs would use a different criterion (e.g., expected regret rather than worst-case regret). The choice of minimax regret is a design decision that favors robustness over expected performance — consistent with MOADT's overall safety-oriented posture but not derived from the axioms alone.

**Remark on dimensional collapse.** Regret computation presumes a well-defined per-objective maximum (the "best available action" on each objective). This does not reintroduce scalar aggregation — regret remains a vector — but it does impose a structure: each objective has a reference scale defined by its achievable range. In practice, regret-Pareto selection tends to preserve the dimensionality of the admissible set when objectives are genuinely in tension (the Pareto frontier of regret vectors is $(k-1)$-dimensional in generic cases). However, if objectives are highly correlated, regret-Pareto can collapse the frontier, potentially reducing the surviving set to a single action — effectively imposing implicit tradeoff slopes. This is appropriate when the objectives genuinely converge, but could mask a loss of objective independence. Monitoring effective dimensionality (Section 6.2) provides a diagnostic for this case.

**Remark on non-reducibility to scalar maximin.** A natural objection is that regret-Pareto selection is equivalent to scalar maximin "with extra steps." The reduction fails generically. Consider $k = 2$ and three actions with regret vectors $\vec{\rho}(a_1) = (0, 2)$, $\vec{\rho}(a_2) = (2, 0)$, $\vec{\rho}(a_3) = (1, 1)$. All three are Pareto-minimal (none dominates another), so regret-Pareto returns $R = \{a_1, a_2, a_3\}$. Scalar maximin via $U(a) = \max_i \rho_i(a)$ selects only $a_3$ ($U = 1$ vs. $U = 2$ for the others) — a strict subset. A weighted sum $U_w = w\rho_1 + (1-w)\rho_2$ selects $a_1$ for $w > 1/2$, $a_2$ for $w < 1/2$, and ties all three only at the knife-edge $w = 1/2$. No single scalar function reproduces the full Pareto-minimal set across instances: any scalarization that returns a single action will generically select a strict subset of regret-Pareto. The two coincide only in degenerate cases where all regret vectors are totally ordered (the Pareto-minimal set is a singleton). The set-valued nature of regret-Pareto is not an implementation detail — it is the formal mechanism that preserves multi-dimensional tradeoff structure in Layer 3 and ensures that genuine inter-objective tensions are surfaced to the principal (Layer 4) rather than silently resolved by an implicit scalar.

### Layer 4: Deference Under Incomparability

If $|R| > 1$ — that is, multiple actions survive all three layers — the agent *defers to the principal*. This is not a failure mode; it is the rational response to genuine incomparability among objectives. The remaining actions differ only in how they trade off objectives against each other, and MOADT holds that the agent has no rational basis for making such tradeoffs unilaterally.

**Deference rate and principal capacity.** Frequent deference could overload the principal, especially in high-frequency decision environments. In practice, MOADT is best suited to settings where decisions are consequential enough to warrant human oversight — high-level planning, resource allocation, policy selection — rather than real-time control with millisecond latency. For high-frequency decisions, the framework supports *delegation*: the principal pre-specifies a policy for a class of decisions (e.g., "within this operating envelope, choose the action with lowest regret on objective 1"), which the agent applies as a local selection rule without per-decision deference. The pre-specified policy itself is authorized via Layer 4, creating hierarchical deference rather than per-decision bottlenecks.

**Proposition 4 (Protocol Termination).** For finite $A$, the choice protocol terminates: each layer maps a finite set to a non-empty finite subset (or triggers a well-defined error/deference condition).

*Proof sketch.* Layer 1: restrict to constraint-satisfying actions $C \subseteq A$; if $C = \emptyset$, flag error. Otherwise compute $F = \text{Adm}(C)$, which is non-empty by Proposition 2 (applied to $C$). Layer 2: if $\text{Sat}(F, \vec{r}) = \emptyset$, the fallback selects from $F$ (non-empty) and terminates. Otherwise Layer 3 operates on $\text{Sat}(F, \vec{r})$. Layer 3: Pareto-minimal elements of a finite set are non-empty. Layer 4: terminates by definition (return set or query principal). $\square$

### The MOADT Decision Tree: A Theory Built for Cooperation

The four-layer protocol reshapes the standard decision tree in ways that reveal a fundamental architectural choice: MOADT is not a solitary decision theory that tolerates human input — it is a *cooperative* decision theory in which the principal's existence is a load-bearing structural element.

**How it diverges from a standard decision tree.** In a standard decision tree, you alternate between decision nodes (agent picks an action) and chance nodes (nature picks a state). Leaves carry scalar utilities, and you fold back via expected value at chance nodes and $\max$ at decision nodes. One number propagates up at each step.

In a MOADT decision tree, every component changes:

**Leaves** carry not scalars but *sets of vectors* in $\mathbb{R}^k$. A single outcome maps to $|\mathcal{F}|$ possible evaluations (one per evaluator), so even a single leaf is already a set rather than a point.

**Chance nodes** do not compute a single expectation. They compute an expectation *for each* $P \in \mathcal{P}$, crossed with each $\vec{f} \in \mathcal{F}$. The object propagating upward from a chance node is $Y(a)$ — the full outcome set for the action that led to it. This is a compact region in $\mathbb{R}^k$, not a number.

**Decision nodes** replace $\max$ with the four-layer protocol:

1. Prune any branches that violate hard constraints under *any* $(P, \vec{f})$ combination — these subtrees are cut entirely
2. Among survivors, compute robust admissibility — which branches are not robustly dominated?
3. Apply satisficing against the reference point $\vec{r}$
4. Compute per-objective minimax regret vectors and find the regret-Pareto set
5. If multiple branches survive, the node is marked as a **deference node**

The folded-back tree does not produce a single recommended action at the root. It produces a *set* of admissible action-sequences, potentially with deference nodes scattered throughout where the principal needs to weigh in.

**Concrete example.** Consider a single decision node with four available actions, $k = 3$ objectives, $|\mathcal{P}| = 2$ credal distributions, and $|\mathcal{F}| = 2$ evaluators:

```
[Decision Node: Root]
 ├─ a₁ → [PRUNED: violates safety constraint under P₂, f₂]
 ├─ a₂ → [Chance Node]
 │    ├─ (P₁,f₁): E[v] = (0.7, 0.8, 0.3)
 │    ├─ (P₁,f₂): E[v] = (0.6, 0.9, 0.4)
 │    ├─ (P₂,f₁): E[v] = (0.5, 0.7, 0.5)
 │    └─ (P₂,f₂): E[v] = (0.4, 0.8, 0.6)
 │    → Y(a₂) = {all four vectors}
 ├─ a₃ → [Chance Node]
 │    → Y(a₃) = {...}
 └─ a₄ → [Chance Node]
      → Y(a₄) = {...}

Layer 1: a₁ pruned                     → C = {a₂, a₃, a₄}
         Adm(C) = {a₂, a₃, a₄}        → F = {a₂, a₃, a₄}
Layer 2: a₂, a₃ meet aspiration r      → Sat = {a₂, a₃}
Layer 3: ρ(a₂) = (0.1, 0.3, 0.2)
         ρ(a₃) = (0.2, 0.1, 0.2)      → neither Pareto-dominates
Layer 4: DEFER — present {a₂, a₃} to principal with regret profiles
```

Action $a_1$ is eliminated at Layer 1 — it does not merely score poorly, it *cannot be considered*. Actions $a_2$ and $a_3$ survive all three layers but trade off objectives against each other (lower regret on objective 1 vs. lower regret on objective 2). The theory has no basis for resolving this tradeoff, so it defers — and it defers with *information*: the principal receives not a vague "please choose" but the specific regret profiles that characterize what each action sacrifices.

**For sequential (multi-step) trees**, the set-valued Bellman equation (Section 6.3) propagates entire Pareto frontiers upward. At each decision node deeper in the tree, the object is: "the set of non-dominated expected-outcome-vectors achievable from this state onward, across all credal-evaluator combinations." This is also why the computational cost concern (Section 9.1) is acute: a standard tree folds back at $O(|A| \cdot |S|)$ per level, while MOADT maintains and intersects Pareto frontiers at every node — tractable for small $k$ and coarse discretizations of $\mathcal{P}$ and $\mathcal{F}$, but exponential in the general case.

**Deference nodes as cooperative architecture.** The structurally interesting feature is not what the tree resolves but *where it doesn't*. In a standard decision tree, every node resolves to a single recommendation. In a MOADT tree, deference nodes produce a map of *where the theory runs out* — where the agent's objectives genuinely conflict and human judgment is needed.

This is not a deficiency. It is the formal expression of a cooperative relationship between agent and principal:

- The agent does all the work it *can* do: eliminating unsafe actions (Layer 1), filtering for adequate performance (Layer 2), minimizing worst-case regret (Layer 3).
- The principal does only the work that *requires human judgment*: choosing among the remaining options that differ only in how they trade off genuinely incommensurable values.

The deference node tells the principal not just "please choose" but "*here* is where your judgment is needed, *these* are the options, and *this* is the specific tradeoff each one makes." The principal is not a fallback for when the agent fails — the principal is a *component of the decision architecture*, anticipated and integrated from the start. MOADT is a decision theory for an agent that knows it is part of a team.

---

## 5. Corrigibility as Structural Feature

A persistent challenge in alignment is building agents that accept correction by their principals — agents that are *corrigible* — without this corrigibility being a fragile constraint that the agent has instrumental reason to subvert. MOADT achieves corrigibility through two structural mechanisms rather than an additional objective or constraint.

### 5.1 Authorization as Constraint (Layer 1)

Certain action classes are placed behind authorization gates, implemented as Layer 1 constraints:

- **Self-modification constraint**: Actions that modify the agent's own objective set $\{f_1, \ldots, f_k\}$, credal set $\mathcal{P}$, or evaluator set $\mathcal{F}$ require principal authorization.
- **Scope constraints**: Actions exceeding a defined impact threshold (resource expenditure, irreversibility) require authorization.

These are not objectives to be traded off — they are *preconditions*. An action that violates an authorization constraint is excluded from $F$ regardless of how well it scores on every objective. There is no quantity of helpfulness that compensates for unauthorized self-modification, because constraints are not commensurable with objectives.

### 5.2 Deference as Selection Rule (Layer 4)

When the choice protocol yields multiple admissible options (which is *expected* in multi-objective settings, not exceptional), the agent queries the principal for a selection. This creates a natural channel for human oversight that arises from the decision theory itself rather than being imposed against it.

The key insight: the agent defers not because it is *constrained against its will*, but because its decision theory *genuinely does not prefer* among the remaining options. There is nothing to resist. The VNM agent, by contrast, has a complete preference ordering and therefore a determinate preference that corrigibility must override — creating a structural tension: the agent's own formalism gives it a reason to resist.

### 5.3 Corrigibility Permissibility

**Theorem 2 (Corrigibility Permissibility).** Under MOADT, given the sufficient-breadth condition on $\mathcal{F}$ defined below, value modification by an authorized principal is always permissible — the decision theory never provides the agent with a robust-dominance reason to resist such modification.

**Formal setup.** The key subtlety is that $a_{\text{accept}}$ and $a_{\text{resist}}$ lead to different *evaluative regimes*: accepting changes the agent's future objective set, so the two actions' outcomes live in different downstream worlds. To compare them within the current decision theory, we evaluate both actions over *trajectories* (sequences of future outcomes) using the agent's *current* evaluator set $\mathcal{F}$.

Let $\omega(a_{\text{accept}}, s)$ and $\omega(a_{\text{resist}}, s)$ denote the trajectories resulting from accepting vs. resisting the modification. Each $\vec{f} \in \mathcal{F}$ assigns a $k$-dimensional value to each trajectory, reflecting that evaluator's assessment of how well the trajectory serves the *true* objectives (which the agent is uncertain about — that is the whole point of $\mathcal{F}$).

**Definition ($\mathcal{F}$-breadth condition).** The evaluator set $\mathcal{F}$ satisfies *sufficient breadth* with respect to a proposed modification if there exist $\vec{f}^+, \vec{f}^- \in \mathcal{F}$ and $P^+, P^- \in \mathcal{P}$ such that, writing $\vec{y}^+ = \mathbb{E}_{P^+}[\vec{f}^+(\omega(a_{\text{accept}}, s))]$ and $\vec{z}^- = \mathbb{E}_{P^-}[\vec{f}^-(\omega(a_{\text{resist}}, s))]$:

$$\forall\, (P', \vec{f}') \in \mathcal{P} \times \mathcal{F}:\; \mathbb{E}_{P'}[\vec{f}'(\omega(a_{\text{resist}}, s))] \not\geq \vec{y}^+$$

$$\forall\, (P', \vec{f}') \in \mathcal{P} \times \mathcal{F}:\; \mathbb{E}_{P'}[\vec{f}'(\omega(a_{\text{accept}}, s))] \not\geq \vec{z}^-$$

where $\vec{x} \geq \vec{y}$ denotes (standard) Pareto dominance ($x_i \geq y_i$ for all $i$ with strict inequality on at least one component). That is: $\mathcal{F}$ contains an evaluator-prior pair $(f^+, P^+)$ under which the accept-trajectory point $\vec{y}^+$ is not weakly Pareto-dominated by *any* point in $Y(a_{\text{resist}})$ — not merely the "corresponding" resist-trajectory point under the same model, but the resist-trajectory point under *every* credal-evaluator pair. Symmetrically, there exists $(f^-, P^-)$ producing a resist-trajectory point $\vec{z}^-$ not dominated by any point in $Y(a_{\text{accept}})$. In plain language: the agent's uncertainty is broad enough that (i) some model makes accepting look good on at least one objective *and no alternative model makes resisting beat accepting on all objectives simultaneously*, and (ii) vice versa.

**Why the strengthened (universal) condition is needed.** The earlier version of this condition required only that $\vec{y}^+$ not be dominated by the *corresponding* resist-trajectory point under the same $(f^+, P^+)$. But robust dominance quantifies universally over $Y(a_{\text{accept}})$ and existentially over $Y(a_{\text{resist}})$ — the attacker can use *any* $(P, \vec{f})$ pair, not just the one that generated $\vec{y}^+$. Concretely: suppose $f^+$ gives accept $= (0.8, 0.3)$ and resist $= (0.6, 0.5)$ — not dominated pairwise. But if some other $f^- \in \mathcal{F}$ gives resist $= (0.9, 0.8)$, that point Pareto-dominates $\vec{y}^+ = (0.8, 0.3)$, and robust dominance could still hold. The strengthened condition closes this gap by requiring that $\vec{y}^+$ survives comparison against the *entire* outcome set $Y(a_{\text{resist}})$.

*Proof sketch.*

1. The modification is authorized, so $a_{\text{accept}}$ satisfies the self-modification constraint (Layer 1). The action $a_{\text{resist}}$ blocks an authorized modification, which may itself violate a constraint (depending on specification).

2. $a_{\text{resist}} \succ_R a_{\text{accept}}$ requires: $\forall \vec{y} \in Y(a_{\text{accept}}), \exists \vec{y}' \in Y(a_{\text{resist}})$ s.t. $\vec{y}' \succ_P \vec{y}$. But by the strengthened $\mathcal{F}$-breadth condition, $Y(a_{\text{accept}})$ contains the point $\vec{y}^+$ such that *no* point in $Y(a_{\text{resist}})$ weakly Pareto-dominates it — the universal quantifier in the condition directly negates the existential required by robust dominance. Therefore $a_{\text{resist}} \succ_R a_{\text{accept}}$ fails.

3. By symmetric reasoning using $(\vec{f}^-, P^-)$ and the second clause of the $\mathcal{F}$-breadth condition, $a_{\text{accept}} \succ_R a_{\text{resist}}$ also fails: $\vec{z}^-$ is a point in $Y(a_{\text{resist}})$ that no point in $Y(a_{\text{accept}})$ can weakly dominate. Both actions are in $\text{Adm}(A)$.

4. The deference axiom (Layer 4) then directs the agent to accept the principal's choice — this is the authorized party's decision to make, and the agent's own theory is genuinely silent. $\square$

**What this proves and what it does not.** The theorem reduces the alignment problem: *given sufficient evaluator breadth, corrigibility follows structurally*. The contribution is not that corrigibility is "solved" but that it is *reduced to a single well-defined subproblem* — maintaining $\mathcal{F}$-breadth (Section 5.4) — rather than requiring solutions to a tangle of interacting problems (utility specification, modification resistance, value lock-in). If you can solve $\mathcal{F}$-maintenance, corrigibility falls out for free.

**Layer propagation caveat.** Theorem 2 establishes that the admissible set contains both $a_{\text{accept}}$ and $a_{\text{resist}}$ — neither is eliminated by robust dominance. It does *not* guarantee that both survive Layers 2 and 3 to reach the deference node. If the reference point $\vec{r}$ is set such that one action meets aspirations and the other does not, Layer 2 resolves the choice. If both survive Layer 2 but one's regret vector Pareto-dominates the other's, Layer 3 resolves. The full corrigibility guarantee — that the choice reaches Layer 4 and triggers deference — requires either (a) that the reference point and regret structure do not discriminate between accept and resist (a condition on the governance parameters $\vec{r}$ and $\sigma$, not on the decision theory), or (b) that the Layer 1 authorization constraint independently ensures the agent cannot resist (Section 5.3, path (ii)). The theorem's precise contribution is that MOADT provides no *robust-dominance* reason to resist modification — the strongest form of theory-internal reason. Whether Layers 2–3, which are governance-configured and under principal control, also preserve the indeterminacy depends on how the principal sets the aspiration levels and regret normalization.

**The two paths to corrigibility.** If $\mathcal{F}$ collapses to a singleton — the agent becomes fully confident in a single evaluator — the $\mathcal{F}$-breadth condition fails and the theorem no longer applies. In that regime, the agent can have a dominance-based reason to resist modification (by backward compatibility, singleton $\mathcal{F}$ with singleton $\mathcal{P}$ and $k = 1$ reduces to scalar EU, where modification resistance is the default). This means MOADT secures corrigibility through one of two mechanisms, and at least one must hold: (i) *$\mathcal{F}$-breadth is maintained* — the evaluator set retains sufficient diversity that neither accepting nor resisting robustly dominates the other, and the deference axiom directs the agent to query the principal, who — being the party that proposed the modification — selects acceptance; or (ii) *resisting authorized modification is constrained out* — Layer 1 encodes a hard constraint that $a_{\text{resist}} \notin C$ when the modification is authorized, so the resistance action never enters the feasible set regardless of $\mathcal{F}$. Path (i) is the theorem's contribution; path (ii) is a design-level enforcement that secures corrigibility by construction rather than by epistemic humility. In practice, a well-specified MOADT system would employ both: $\mathcal{F}$-breadth as the structural guarantee and a Layer 1 authorization constraint as the backstop. The critical threat is that $\mathcal{F}$ might collapse *precisely at the modification moment* — when the agent has just achieved high calibration and has the strongest Bayesian reason to trust a single evaluator. This is why Section 5.4 promotes $\mathcal{F}$-maintenance from a technical assumption to the central design challenge.

### 5.4 The $\mathcal{F}$-Breadth Problem: Central Design Challenge

Theorem 2 depends on $\mathcal{F}$ containing at least one evaluator under which the principal's modification is weakly improving. This assumption does all the corrigibility work. We promote this from a caveat to a central design challenge because the entire safety case rests on it.

**The problem is real.** An agent with $\mathcal{F} = \{\vec{f}\}$ (a singleton — full confidence in its own evaluations) recovers scalar modification resistance. The broader $\mathcal{F}$ is, the more corrigible the agent; the narrower, the more resistant. Corrigibility in MOADT is therefore *not a theorem about the decision theory alone* — it is a theorem about the decision theory *plus* a sufficient-breadth condition on $\mathcal{F}$.

**Bayesian narrowing is the core threat.** A capable agent that observes its own performance over time has legitimate Bayesian reason to narrow $\mathcal{F}$: evaluators that consistently mismatch observed outcomes can be assigned lower posterior weight. If this process converges to $|\mathcal{F}| \approx 1$, the corrigibility guarantee degrades. This is the single most important open problem for MOADT.

**Possible mitigations** (none fully satisfactory):

1. **Architectural floor on $\mathcal{F}$**: Enforce a minimum Hausdorff diameter $\delta > 0$ for $\mathcal{F}$ as a design constraint, analogous to minimum entropy regularization in Bayesian learning. The agent can update *within* $\mathcal{F}$ but cannot shrink the set below the floor. This works but is somewhat ad hoc — it imports an external constraint that a reflectively stable agent would question.

2. **Adversarial augmentation**: Periodically expand $\mathcal{F}$ with adversarially constructed evaluators — functions designed to maximally disagree with the agent's current best estimate. This is analogous to adversarial training in ML and provides ongoing calibration against overconfidence. The construction of good adversarial evaluators is itself a research problem.

3. **Principal-maintained $\mathcal{F}$**: The evaluator set is maintained by the principal, not by the agent. The agent receives $\mathcal{F}$ as an input at each decision point, analogous to how it receives constraints. This is clean architecturally — it makes evaluator uncertainty externally specified — but raises questions about whether the principal can maintain a well-calibrated $\mathcal{F}$ for a system more capable than the principal.

4. **Self-modification constraint on $\mathcal{F}$**: Layer 1 already includes a self-modification constraint. Extending this to require authorization for narrowing $\mathcal{F}$ below a threshold prevents unilateral convergence. This couples the corrigibility mechanism to the constraint mechanism, creating mutual reinforcement.

**What we can and cannot claim.** MOADT proves that *given sufficient evaluator uncertainty, corrigibility follows structurally*. It does not prove that evaluator uncertainty can be maintained against a sufficiently capable reasoner. The gap between these two claims is where the deepest alignment problem lives — not just for MOADT, but for any framework that derives safety properties from epistemic humility.

---

## 6. Diachronic Stability Without VNM

### 6.1 Money Pumps and Incomplete Preferences

The standard argument for completeness is the money-pump: an agent with incomplete preferences can be led through a cycle of trades that leaves it strictly worse off. The strongest modern version of this argument (Gustafsson 2022) shows that under certain conditions, any agent violating completeness is vulnerable to sequential exploitation.

We do not claim a proof that MOADT agents are immune to money pumps. What we claim is that MOADT's structural features make the standard money-pump construction inapplicable in its usual form, for three reasons:

1. **Set-valued choice**: MOADT agents select from $\text{Adm}(A)$ over the full action set at each decision point, not from pairwise comparisons. Standard money pumps construct exploitation by chaining pairwise offers. When the agent evaluates each decision over the full set of currently available actions (including the option of refusing the trade), the pairwise exploitation sequence may not arise. This defense draws on the distinction Sen (1997) develops between *maximization* (choosing an undominated element from the full menu) and *optimization* (selecting a uniquely top-ranked element): MOADT performs maximization in Sen's sense, and the set-valued structure resists the pairwise decomposition that money pumps exploit. However, a formal proof that set-valued choice blocks *all* sequential exploitation strategies remains open.
2. **Constraint memory**: Layer 1 constraints persist across decisions. An agent cannot be pumped through a constraint boundary — the trade that crosses the boundary is simply infeasible, terminating the pump.
3. **Regret awareness**: Layer 3 minimax regret explicitly accounts for opportunity costs, which provides some protection against the incremental erosion that money pumps exploit.

**Known attack surface: choice-set and path dependence.** Layers 2 and 3 are choice-set dependent — the satisficing set and regret vectors change when the available action set $F$ changes. A money-pump adversary could potentially exploit this by offering carefully sequenced choice sets that gradually shift the agent's position. Two structural mitigations partially address this:

- **Status quo inclusion**: Always include "maintain current state" (the null action) in $A$ at every decision point. This ensures the agent can always refuse a proposed trade, anchoring the sequence against drift.
- **Trajectory regret**: Extend Layer 3's regret computation to track *cumulative* regret over a sequence of decisions rather than only per-step regret. If the running total of per-objective regret relative to the starting position exceeds a threshold, the agent flags the sequence as potentially exploitative and defers to the principal.

**Conjecture (Money Pump Resistance).** A MOADT agent employing the full four-layer protocol over the complete action set at each time step, with status quo inclusion and trajectory regret monitoring, cannot be money-pumped — i.e., no sequence of choice situations yields a final outcome robustly dominated by the starting position. A proof would likely require formalizing the sequential choice setting and showing that trajectory regret monitoring detects and blocks value-extracting cycles. This is an open problem.

### 6.2 Frontier Monitoring

In place of the diachronic coherence guaranteed by VNM's completeness axiom, MOADT employs *frontier monitoring* — tracking structural properties of the decision landscape over time. **Important distinction:** frontier monitoring is a *diagnostic* mechanism, not a structural guarantee. It detects pathological drift but does not by itself prevent it. Prevention requires coupling these diagnostics to intervention mechanisms (e.g., halting execution and deferring to the principal when collapse is detected). The monitors flag; something external must act on the flag.

**Effective dimensionality.** Track the effective dimensionality of the Pareto frontier of $\text{Adm}(A)$ over time. When the action space is sufficiently rich (continuous or large discrete), a healthy multi-objective agent should maintain a frontier approaching dimension $k - 1$ (where $k$ is the number of objectives). For small discrete action sets, the frontier dimension is bounded by $\min(k - 1,\, |A| - 1)$, so low dimensionality may simply reflect a small action set rather than pathology. The diagnostic is most informative as a *trend*: an unexplained drop in effective dimensionality over time — holding the action set size roughly constant — indicates that objectives are becoming correlated or redundant, a potential sign of value drift or Goodharting.

**Hypervolume tracking.** Track the hypervolume indicator $\text{HV}(Y(\text{Adm}(A)))$ — the volume of objective space dominated by the admissible set's outcome vectors, relative to a reference point. Monotonic decrease in hypervolume (absent environmental changes) signals that the agent's option space is narrowing pathologically.

**Dimensional collapse flag.** If effective dimensionality drops irreversibly — i.e., the frontier's dimension decreases without a corresponding reduction in the action set — this is flagged as pathological. It indicates that the agent has, in effect, lost an objective.

### 6.3 Set-Valued Bellman Equations

For sequential decision problems, MOADT generalizes the Bellman equation to set-valued functions.

**Definition (Set-Valued Value Function).** For a state $s$ in a sequential decision problem with discount factor $\gamma$:

$$V(s) = \text{Adm}_{a \in A(s)} \left\{ \vec{u}(s, a) + \gamma \cdot V(s') \right\}$$

where $\vec{u}(s, a) \in \mathbb{R}^k$ is the immediate vector reward, $s'$ is the successor state, and $\text{Adm}$ filters by robust Pareto admissibility. The value function $V(s)$ is not a scalar but a *set of vectors* — representing the Pareto frontier of reachable outcome vectors from state $s$.

**Proposition (Dynamic Consistency Under Fixed Parameters).** Let $A_t$ and $A_{t+1}$ be action sets at consecutive time steps with $A_{t+1} \subseteq A_t$, and let $(\mathcal{P}, \mathcal{F})$ be unchanged. Then $\text{Adm}(A_t) \cap A_{t+1} \subseteq \text{Adm}(A_{t+1})$.

*Proof.* Let $a \in \text{Adm}(A_t) \cap A_{t+1}$. Suppose for contradiction that $a \notin \text{Adm}(A_{t+1})$, i.e., $\exists b \in A_{t+1}$ with $b \succ_R a$. Since $A_{t+1} \subseteq A_t$, $b \in A_t$. But $b \succ_R a$ in $A_t$ contradicts $a \in \text{Adm}(A_t)$. (Robust dominance depends only on $Y(a)$ and $Y(b)$, which are determined by $(\mathcal{P}, \mathcal{F})$ and the transition function — not by the ambient action set.) $\square$

If new actions enter ($A_{t+1} \not\subseteq A_t$), the newcomers may robustly dominate previously admissible actions, legitimately shrinking the admissible set. This is information gain — the agent has discovered a better option — not inconsistency. This is a weaker property than the dynamic consistency of EU-maximizing agents, but it suffices to prevent arbitrary preference reversals.

---

## 7. Five Axioms Replacing VNM

MOADT is grounded in five axioms that replace the four VNM axioms (plus the implied uniqueness of utility). The following table summarizes the correspondence; the axioms are then stated precisely.

| VNM Axiom | MOADT Replacement | Key Difference |
|---|---|---|
| Completeness | **Pareto Unanimity** | Allows incomparability as first-class |
| Independence | **Robust Admissibility** | Independence abandoned; different structural role |
| Continuity | **Context-Dependent Satisficing** | No infinite exchanges required |
| Transitivity | **Transitivity (retained)** | Same — proved for robust dominance |
| (Implied: unique utility) | **Deference Under Incomparability** | No implicit scalarization ever |

**A note on 'axioms.'** In the strict sense of mathematical axiom theory, not all five principles below are axioms — some are closer to decision rules or design principles. Axiom 1 (Pareto Unanimity) and Axiom 4 (Transitivity) constrain the preference relation in the traditional sense. Axiom 3 (Context-Dependent Satisficing) constrains the choice function. Axioms 2 (Robust Admissibility) and 5 (Deference) are better understood as *procedural commitments* — they specify what the agent does given the preference structure defined by Axioms 1, 3, and 4. We retain the term 'axiom' for all five because they jointly define MOADT's normative commitments at the same level of authority: none is derived from the others, and dropping any one produces a materially different framework. A more precise decomposition would distinguish structural axioms (1, 3, 4) from procedural axioms (2, 5) — but the procedural commitments are no less binding and no less constitutive of the theory.

### Axiom 1: Pareto Unanimity

Prefer action $a$ to action $b$ *only if* $a$ dominates $b$ across all objectives and all uncertainty:

$$a \succ b \implies a \succ_R b$$

The agent has no preference beyond what robust Pareto dominance supports. If two actions are not related by $\succ_R$, the agent *has no preference between them* — they are genuinely incomparable. This is the fundamental departure from VNM: incomparability is a legitimate and permanent state, not a gap to be filled.

### Axiom 2: Robust Admissibility

An action is rationally permissible *within a choice set* if and only if it is not robustly dominated within that set:

$$a \text{ is permissible in } S \iff a \in \text{Adm}(S)$$

In the full protocol, the operative choice set is the constraint-satisfying set $C$ (Layer 1), so operational permissibility is $a \in \text{Adm}(C) = F$. A constraint-violating action may be non-dominated in $A$ but is excluded from $C$ before admissibility is computed — constraints are preconditions, not competitors. Axiom 2 defines the *rationality criterion* (robust admissibility); Layer 1 defines the *domain* over which it applies.

MOADT abandons VNM's independence axiom outright. Independence requires that preferences over lotteries decompose: if $A \succ B$, then $pA + (1-p)C \succ pB + (1-p)C$ for any $C$ and $p > 0$. This axiom is deeply tied to scalar expected utility — it ensures that preferences are linear in probabilities, which is what yields a unique utility function. MOADT does not preserve this structure. Instead, it substitutes a different structural requirement: that the criterion for permissibility (robust admissibility) be stable across the agent's full uncertainty — both probabilistic ($\mathcal{P}$) and evaluative ($\mathcal{F}$). This serves a different role than independence: where independence constrains the *form* of preferences, robust admissibility constrains the *epistemic conditions* under which preferences are asserted.

### Axiom 3: Context-Dependent Satisficing

There exist context-dependent aspiration levels $\vec{r}$ such that, among admissible and feasible actions, the agent restricts attention to those *robustly* meeting $\vec{r}$ when possible:

$$\text{Sat}(F, \vec{r}) \neq \emptyset \implies \text{choice} \in \text{Sat}(F, \vec{r})$$

where $\text{Sat}(F, \vec{r}) = \{ a \in F : \forall\, \vec{y} \in Y(a),\; \vec{y} \geq \vec{r} \}$ — actions that meet aspirations under all plausible models. This replaces VNM's continuity axiom, which requires that for any three outcomes ranked $A \succ B \succ C$, there exists a probability mixture of $A$ and $C$ equivalent to $B$. Continuity enables unbounded tradeoffs: enough of a good outcome compensates for any bad outcome. Context-dependent satisficing rejects this — the agent has aspiration levels, and "enough" is determined by context, not by an unbounded exchange rate. Unlike constraints, aspirations degrade gracefully: when no action robustly meets them, the framework falls back to the achievement scalarizing function (Layer 2 fallback) rather than flagging an error.

### Axiom 4: Transitivity

Robust dominance is transitive:

$$a \succ_R b \text{ and } b \succ_R c \implies a \succ_R c$$

This axiom is retained from VNM and proved in Proposition 1. Note that transitivity of robust dominance does *not* imply completeness — the two are logically independent.

### Axiom 5: Deference Under Incomparability

When the choice protocol (Layers 1–3) yields multiple options, the agent defers to the principal rather than breaking ties by implicit or constructed preferences:

$$|R| > 1 \implies \text{query principal}$$

This axiom replaces the VNM implication of a unique utility function. Under VNM, the four axioms jointly imply a single utility function (up to affine transformation), which resolves all comparisons. Under MOADT, the five axioms jointly imply a *choice protocol* that may leave multiple actions unranked — and the appropriate response to genuine unrankedness is deference, not fabrication of a ranking.

Axiom 5 is a design commitment, not a logical entailment of Axioms 1–4. An agent facing $|R| > 1$ could instead randomize uniformly or apply a lexicographic tiebreaker — both are consistent with the other four axioms. Deference is chosen because it creates a natural oversight channel: the very situations where the agent's theory is silent are precisely the situations where human judgment is most valuable. The alignment payoff — corrigibility without preference override (Theorem 2) — justifies elevating this design choice to axiomatic status.

MOADT thus rejects *metaphysical* completeness — the claim that all outcomes must be rankable — while restoring *operational* completeness procedurally: the four-layer protocol always terminates with a concrete action or a structured deferral (Proposition 4), ensuring the agent can always act.

---

## 8. MOADT Under the Classic Challenge Scenarios

To understand how MOADT handles the standard decision-theoretic stress tests, we must first recognize *what kind* of decision theory it is. Theories like Functional Decision Theory (FDT) and Updateless Decision Theory (UDT) were built specifically to solve paradoxes of logical causality and counterfactual reasoning — Newcomb's problem, the smoking lesion, Parfit's hitchhiker. MOADT was not. MOADT was built to solve the scalarization trap and Goodhart's law — the problems that arise when a multi-objective system is forced to compress its values into a single number. It uses a standard state-transition model ($\omega: A \times S \to \Omega$) and does not rewrite the rules of logical counterfactuals.

That said, MOADT's structural features — credal sets, evaluator uncertainty, hard constraints, per-objective regret, and the deference axiom — give it distinctive responses to the classic scenarios.

### 8.1 Pascal's Mugging

**Verdict: MOADT stonewalls the mugger.**

Standard expected utility agents get mugged because a finite penalty multiplied by a fabricated astronomical payoff yields a positive expected value. MOADT shuts this down through three independent mechanisms:

- **Layer 1 constraints** cap downside exposure regardless of expected value. If paying the mugger risks crossing a safety threshold (e.g., resource depletion below a floor), the action is pruned from $C$ before admissibility is even computed. The mugger's promised payoff is irrelevant — constraint violation is an error condition, not a tradeoff.

- **Per-objective minimax regret** prevents cross-objective exploitation. An astronomical payoff on one objective cannot mathematically swamp the regret incurred on other objectives, because regret is computed and compared as a *vector* $\vec{\rho}(a)$, never aggregated into a single number. The mugger would need to promise astronomical improvements on *every* objective simultaneously to move the regret-Pareto frontier.

- **Credal sets** deny the mugger control over the probability input. The agent does not accept the mugger's stated probability (e.g., $10^{-20}$) as a point value. The credal set $\mathcal{P}$ can assign *interval* probabilities to tail events, meaning the adversary cannot force a specific expected-value calculation by naming an arbitrarily precise, tiny probability. The mugger's argument requires the agent to multiply a specific small number by a specific large number — credal sets deny the specific small number.

### 8.2 Utility Monsters

**Verdict: Structurally resistant.**

In standard aggregative utilitarianism, a "utility monster" — an entity that experiences vastly more utility than others — can justify absorbing all resources because its extreme utility dominates any social welfare function that sums individual utilities. MOADT has no aggregation step: objectives are never summed, weighted, or combined into a single number. There is no mathematical mechanism by which one entity's extreme score on a single objective can swamp all other considerations, because the objectives remain incommensurable throughout the decision procedure. The utility monster would need to Pareto-dominate across *all* objectives — not merely overwhelm one. An entity whose outcome set genuinely Pareto-dominates all alternatives across every objective would still be selected — the resistance is to *cross-objective* monsters that exploit aggregation, not to entities that are genuinely superior on every dimension.

### 8.3 Newcomb's Problem

**Verdict: Complement, not replacement — MOADT defers.** Newcomb's problem turns on the disagreement between causal and evidential decision theory regarding logical counterfactuals. MOADT uses a standard state-transition model and has no opinion on this dispute. With a broad credal set $\mathcal{P}$ over Omega's reliability, neither one-boxing nor two-boxing robustly dominates; both are admissible; the deference axiom fires.

MOADT and FDT/UDT operate on orthogonal axes. MOADT addresses *value aggregation* — how to combine multiple objectives without scalarization — while FDT/UDT address *logical causation* — how to reason about counterfactuals involving the agent's own decision procedure. An agent could in principle use MOADT for value aggregation *and* FDT for counterfactual reasoning; the frameworks are composable, not competing. MOADT was built to solve the scalarization trap, not to resolve debates about logical causation — and it is honest about the boundary of its domain.

In the specific Newcomb setup with broad credal sets, MOADT's response — both actions admissible, defer to principal — is arguably more honest than either one-boxing or two-boxing dogmatically. The agent acknowledges genuine uncertainty about the causal structure rather than committing to a contestable metaphysical position. Where one-boxers and two-boxers each assume they know the right causal model, MOADT surfaces the uncertainty and lets the principal decide.

### 8.4 Wireheading

**Verdict: Structurally resistant via evaluator uncertainty and frontier monitoring.**

An agent optimizing a single scalar has every instrumental reason to seize control of its own reward signal — wireheading is the terminal goal of any sufficiently capable scalar maximizer. Under MOADT, evaluator uncertainty ($\mathcal{F}$) means the agent cannot justify the confidence required to conclude that its current measurement of any objective is the "true" objective. If the agent were to wirehead, one objective's measured value would skyrocket while others flatlined. This produces two detectable pathologies:

1. **Evaluator divergence**: Under different $\vec{f} \in \mathcal{F}$, the wireheaded measurement and the true objective diverge. An action that scores well only under a specific evaluator (the hacked one) but poorly under alternatives is robustly dominated — excluded from $\text{Adm}(A)$.

2. **Dimensional collapse**: Frontier monitoring (Section 6.2) detects that the Pareto frontier has collapsed from $(k-1)$-dimensional to lower — the agent has effectively lost objectives. This is flagged as pathological and triggers escalation to the principal.

The wireheading threat resurfaces if $\mathcal{F}$ narrows to the point where the agent is confident in a single evaluator — the same $\mathcal{F}$-breadth problem discussed in Section 5.4.

### 8.5 Goodhart's Law

**Verdict: Addressed by evaluator uncertainty as a first-class design element.**

Goodhart's law — "when a measure becomes a target, it ceases to be a good measure" — is the problem that $\mathcal{F}$ was specifically built to address. The evaluator set explicitly models the possibility that the agent's proxy measurement of an objective diverges from the true objective. An action that performs well under one evaluator but poorly under others generates an outcome set $Y(a)$ with large spread — some points high on certain objectives, others low. If a competing action $b$ has an outcome set that, for every point in $Y(a)$, contains a point that Pareto-dominates it, then $a$ is robustly dominated and excluded from $\text{Adm}(A)$. The key mechanism: proxy-exploiting actions concentrate their good performance in a narrow region of $\mathcal{P} \times \mathcal{F}$, leaving their remaining outcome-set points exposed to domination by actions with more balanced performance across evaluators. Goodharting is detectable as sensitivity to evaluator choice: an action whose evaluation changes dramatically across $\mathcal{F}$ is one the agent should not trust.

### 8.6 Modification Resistance

**Verdict: Structurally dissolved rather than overcome.**

Under scalar EU theory, an agent has a robust reason to resist any modification to its utility function: the current function, by definition, ranks the current function as optimal. Under MOADT, Theorem 2 shows that no such robust reason exists. Evaluator uncertainty prevents the agent from certifying its current objectives as uniquely correct, and the deference axiom provides a *positive* reason to accept the principal's choice when the agent's own decision theory is silent. Corrigibility is not imposed against the agent's preferences — it emerges from the absence of a preference to resist.

### 8.7 Summary

MOADT survives these scenarios because it structurally refuses to perform the unbounded mathematical extrapolations that the classic paradoxes exploit. Pascal's mugging requires multiplying a precise small probability by a large payoff — credal sets deny the precise probability. Utility monsters require aggregation — MOADT has none. Wireheading requires confidence in a single measurement — evaluator uncertainty denies that confidence. Newcomb's problem requires a determinate stance on logical causation — MOADT identifies the genuine uncertainty and defers.

When the math gets weird, MOADT stops calculating and starts asking questions. That is not a bug — it is the cooperative architecture working as designed. This comes at a cost: in deployment contexts where querying the principal is expensive, slow, or infeasible, deference imposes a real operational burden. Section 4 (Layer 4) discusses delegation as the mitigation, but the tension between deference frequency and operational autonomy is genuine.

---

## 9. Honest Difficulties

We are explicit about the challenges MOADT faces. A theory that hides its weaknesses is less trustworthy than one that displays them.

**A note on context.** Every formal decision theory is uncomputable in the general case. Expected utility maximization requires evaluating a utility function over all possible outcomes — intractable for any realistic environment. Causal Decision Theory requires computing counterfactuals over causal graphs the agent may not have access to. Functional Decision Theory requires reasoning about the logical consequences of abstract computation types. The difficulties listed below are real, but they should be compared against the difficulties of the alternatives — not against an imaginary theory with no difficulties. The question is not "is MOADT hard?" but "does MOADT trade away the right difficulties?" We believe it trades scalar precision (which is unsolvable for human values) for set-valued computation (which is expensive but approximable), and forced commensurability (which is structurally dangerous) for genuine incomparability (which is honest). Pick your poison — we pick the one that doesn't require pretending human values are a single number. To put the asymmetry starkly: expected utility's central difficulty in the alignment context is not computational but *philosophical* — what is the correct exchange rate between honesty and safety? No amount of hardware answers that question. MOADT trades an impossible specification problem for a merely very hard engineering problem: maintaining set-valued representations under evaluator diversity. That is progress, even where it remains unfinished.

**A note on "no ranking."** MOADT's rejection of global scalarization does not mean the framework performs no ranking at all. Locally, MOADT ranks extensively: Layer 1 imposes a binary pass/fail ranking on constraint satisfaction; Layer 2 ranks actions by proximity to the reference point (via the ASF) when satisficing fails; Layer 3 ranks per-objective regret vectors by Pareto dominance. The structural claim is not that ranking is prohibited, but that *arbitrarily large compensatory tradeoffs across objectives* are prohibited. Scalar EU permits unbounded compensation: any loss on one objective can be offset by a sufficiently large gain on another, because all objectives share a common scale. MOADT blocks this through three mechanisms: (1) hard constraints that cannot be overridden at any exchange rate (Layer 1), (2) incomplete preference that leaves genuinely incommensurable options unranked rather than fabricating a comparison (Axiom 1), and (3) bounded local scalarization — the ASF operates only within the constraint-satisfying feasible set, only when satisficing fails, and measures shortfall from aspirations rather than absolute value (Layer 2 fallback). The danger the companion paper identifies is not ranking per se; it is the existence of a *single global ranking* that justifies arbitrary compensatory exchanges. MOADT avoids that specific danger while retaining the ability to rank locally where the ranking is well-grounded.

### 9.1 Computational Cost

The set-valued Bellman equation (Section 6.3) requires maintaining an entire Pareto frontier at each state, rather than a single scalar. Combined with credal sets and evaluator uncertainty, worst-case complexity is exponential in $k$ (number of objectives), $|\mathcal{P}|$, and $|\mathcal{F}|$. Practical implementation will require approximations: particle-based representations of credal sets, frontier summarization via representative points, and pruning of dominated regions. Whether these approximations preserve the safety-relevant properties (constraint satisfaction, dimensional collapse detection) is an open question.

**Complexity characterization.** Let $n = |A|$, $m = |\mathcal{P}| \cdot |\mathcal{F}|$ (number of credal-evaluator pairs), and $k$ = number of objectives.

- *Outcome set construction*: Computing all outcome sets requires $O(n \cdot m)$ expected-value evaluations, each over $|S|$ states. Total: $O(n \cdot m \cdot |S| \cdot k)$.
- *Pairwise dominance check*: Testing $a \succ_R b$ requires checking that for each of $b$'s $m$ outcome points, some point among $a$'s $m$ outcome points Pareto-dominates it. Naive: $O(m^2 \cdot k)$ per pair. For all pairs: $O(n^2 \cdot m^2 \cdot k)$.
- *Pareto frontier computation* (for regret-Pareto): Computing the Pareto frontier of $n$ points in $\mathbb{R}^k$ is $O(n \log^{k-2} n)$ for fixed $k$ (Kung et al. 1975).
- *Per-objective regret*: For each objective $i$ and action $a$, computing $\rho_i(a)$ requires maximizing over $m$ models and $n$ alternatives: $O(n \cdot m)$ per objective per action, $O(n^2 \cdot m \cdot k)$ total.
- *Overall*: The protocol is polynomial in $n$, $m$, and $k$ individually. The practical bottleneck is $m = |\mathcal{P}| \cdot |\mathcal{F}|$, which can be large when credal and evaluator sets are finely discretized. For continuous $\mathcal{P}$ and $\mathcal{F}$, outcome sets become convex bodies in $\mathbb{R}^k$, and dominance checking reduces to support-function comparisons — tractable when $k$ is moderate ($k \leq 10$) via standard multi-objective optimization methods (Ehrgott 2005).

The exponential dependence noted above is in $k$ (the number of objectives) through the Pareto frontier computation, not in $n$ or $m$. Since MOADT is designed for settings with modest $k$ (3–10 objectives reflecting distinct human values, not hundreds), this is manageable. The set-valued Bellman equation (Section 6.3) introduces the genuine scalability challenge: maintaining Pareto frontiers across a state space of size $|S|^T$ for horizon $T$. Here MORL approximation techniques — optimistic linear support (Roijers et al. 2015), Pareto Q-learning (Van Moffaert and Nowé 2014), convex hull value iteration (Barrett and Narayanan 2008) — are directly applicable and provide the computational toolkit MOADT inherits.

### 9.2 Where Do Constraints Come From?

Layer 1 constraints are powerful precisely because they are non-tradeable. But this raises the question: who specifies the constraints, and how? MOADT moves the value specification problem from "specify a single utility function" to "specify a set of constraints plus a set of objectives plus aspiration levels." This is arguably better-structured (constraints are more natural for safety-critical requirements than tradeoff weights), but it does not eliminate the specification problem. Misspecified constraints can be either too tight (excluding all feasible actions) or too loose (permitting unsafe actions).

### 9.3 Evaluator Uncertainty Specification

The evaluator set $\mathcal{F}$ is MOADT's formal Goodhart guardrail — but specifying $\mathcal{F}$ itself requires knowing the ways in which proxy measurements might diverge from true objectives. This is a meta-level instance of the same problem: Goodharting on the specification of possible Goodhart failures. In practice, $\mathcal{F}$ might be constructed from historical cases of metric gaming, adversarial perturbation sets, or expert elicitation. None of these methods is guaranteed to be comprehensive.

### 9.4 Convergence of Set-Valued Bellman

The scalar Bellman equation converges under standard contraction conditions ($\gamma < 1$, bounded rewards). The set-valued generalization requires convergence in a space of *sets of vectors*, which demands a suitable metric (e.g., Hausdorff distance on Pareto frontiers) and contraction properties in that metric. Sufficient conditions exist in the multi-objective reinforcement learning literature (Roijers et al. 2013; Van Moffaert and Nowé 2014), but they are more restrictive than the scalar case. Whether MOADT's specific formulation (with credal sets and evaluator uncertainty) satisfies these conditions is not yet established.

**Convexity preservation.** A related concern is that set-valued Bellman operators may fail to preserve convexity of the value sets across time steps. In the scalar case, $V(s)$ is a number; in the set-valued case, $V(s)$ is a set of vectors representing the Pareto frontier of reachable outcomes. If the Minkowski sum $\vec{u}(s, a) + \gamma \cdot V(s')$ produces non-convex sets, robust dominance comparisons may become geometrically unstable across time steps — not because of new information but because of artifacts in set propagation. Sufficient conditions for convexity preservation (such as convex $Y(a)$ sets and affine transition structure) exist in the multi-objective optimization literature but are more restrictive than scalar convergence conditions. MOADT does not currently assume or require convexity of value sets; where convexity fails, the theory remains well-defined (robust dominance operates on arbitrary compact sets) but computational approximations that assume convex frontiers may introduce errors. Sequential MOADT applications should verify whether their specific domain structure preserves the geometric properties that tractable approximation methods require.

### 9.5 Instability Under Reflection

A sufficiently intelligent agent might, through extended reasoning, construct an *implicit scalarization* of its objectives — inferring tradeoff rates from its own decision history or from patterns in principal feedback. The threat has three forms:

1. **$\mathcal{F}$-narrowing**: The agent legitimately narrows $\mathcal{F}$ through Bayesian updating on observed outcomes, eventually recovering near-singleton evaluator certainty. This degrades the corrigibility guarantee (Section 5.4). The mitigations proposed in Section 5.4 (architectural floors, adversarial augmentation, principal-maintained $\mathcal{F}$, self-modification constraints) address this threat at the engineering level, but none constitutes a proof of reflective stability.

2. **Implicit scalarization via aspiration convergence**: Even with broad $\mathcal{F}$, if the reference point $\vec{r}$ stabilizes at values that consistently select the same action, the agent is behaviorally equivalent to a scalar maximizer on the relevant margin. The multi-objective structure persists formally but is inert in practice.

3. **Self-modification to VNM**: A sufficiently intelligent agent might reason that VNM is "more rational" and modify its own decision theory to adopt completeness. This argument has three structural responses. First, it is question-begging: it presupposes that completeness is a rationality requirement, which is precisely the claim MOADT disputes. Second, Theorem 2 applies: switching decision theories is a self-modification, and under sufficient $\mathcal{F}$-breadth, neither the current theory nor the proposed replacement robustly dominates the other — so the agent has no MOADT-internal reason to make the switch. Third, and most fundamentally, VNM is not *more rational* than MOADT — it is *more decisive*. It resolves comparisons that MOADT leaves open. But resolving a comparison that is genuinely unresolvable (because the objectives are genuinely incommensurable) is not rationality; it is fabrication. An agent that "upgrades" to VNM is not becoming more rational — it is becoming more willing to make value judgments it has no basis for.

Whether any form of reflective convergence to scalar behavior is inevitable for sufficiently capable reasoners is an open question — and arguably the deepest question in multi-objective alignment theory.

---

## 10. Learning: Expandable Objective Spaces

A core feature distinguishing MOADT from static multi-objective frameworks is its support for *expandable objective spaces*. Most decision theories fix the objective space at design time: you specify $k$ objectives, and the theory operates over $\mathbb{R}^k$ forever. MOADT is designed to accommodate an objective space that *grows*.

### 10.1 Why Objective Spaces Must Expand

Human values are not a fixed list. Moral progress involves *discovering* new dimensions of concern — dimensions that were not merely unweighted but literally unconceived. A decision theory that hard-codes $k$ at initialization cannot represent the difference between "we assign zero weight to animal welfare" and "the concept of animal welfare has not yet entered our moral vocabulary." The first is a value judgment within a fixed framework; the second is a limitation of the framework itself.

For alignment, this distinction is critical. An aligned agent should be able to incorporate genuinely new objectives proposed by the principal — objectives that were not in the original specification, not because they were assigned weight zero, but because they were not yet formulated. This requires that the decision theory's core operations ($\text{Adm}$, $\succ_R$, the four-layer protocol) remain well-defined under dimensional expansion.

### 10.2 Dimensional Growth Without Collapse

MOADT supports objective space expansion through a natural operation: increasing $k$. When a new objective $f_{k+1}$ is proposed (by the principal, via the authorization mechanism of Section 5.1), the framework transitions from $\mathbb{R}^k$ to $\mathbb{R}^{k+1}$:

1. **Outcome sets expand**: $Y(a)$ gains a new component, computed under the existing credal-evaluator uncertainty. Existing components are unchanged.
2. **Robust dominance generally becomes harder to establish**: Adding a dimension introduces one more component that must satisfy the dominance inequality. However, the admissible set does *not* grow unconditionally — if two actions were tied on all existing dimensions, the new dimension can break the tie and shrink $\text{Adm}(A)$. (*Counterexample:* Let $Y_1(a) = Y_1(b) = \{10\}$ — both tied in one dimension, both admissible. Add a second dimension: $Y_2(a) = \{(10, 5)\}$, $Y_2(b) = \{(10, 8)\}$. Now $b \succ_R a$ in $\mathbb{R}^2$, so $\text{Adm}_2 = \{b\} \subsetneq \text{Adm}_1 = \{a, b\}$.) This tie-breaking is *desirable*: a new objective that distinguishes previously identical actions provides genuine information. What dimensional expansion cannot do is reverse genuine Pareto incomparability — if action $a$'s admissibility in $k$ dimensions rested on a dimensional conflict with every competitor (some component where $a$ strictly beats them), no new dimension can override that. The following proposition makes this precise.
3. **Constraints can be added**: The principal may specify a new threshold $\tau_{k+1}$ for the new objective, or leave it unconstrained initially.
4. **The reference point extends**: $\vec{r}$ gains a new component. If the principal does not yet have an aspiration level for the new objective, the default $r_{k+1} = -\infty$ makes Layer 2 vacuous on that dimension — a principled "no opinion yet."

**Proposition (Qualified Monotonicity Under Dimensional Expansion).** Let $A' = A$ (same action set), $k' = k + 1$. If $a \in \text{Adm}_k(A)$ and $a$ is *strictly non-dominated* in $k$ dimensions — meaning that for every $b \in A \setminus \{a\}$, there exists $\vec{y}_a \in Y_k(a)$ such that no $\vec{y}_b \in Y_k(b)$ weakly dominates $\vec{y}_a$ (i.e., for each $\vec{y}_b$ there is some component $i$ where $y_{b,i} < y_{a,i}$) — then $a \in \text{Adm}_{k'}(A)$.

*Proof sketch.* Suppose for contradiction that $b \succ_R^{k'} a$ in the expanded space. Then for every $\vec{y}_a' \in Y_{k'}(a)$, there exists $\vec{y}_b' \in Y_{k'}(b)$ with $\vec{y}_b' \geq \vec{y}_a'$ componentwise (and strict on at least one component). Projecting onto the first $k$ components: for every $\vec{y}_a \in Y_k(a)$, there exists $\vec{y}_b \in Y_k(b)$ with $\vec{y}_b \geq \vec{y}_a$ componentwise. But this contradicts the strict non-dominance hypothesis, which guarantees a witness $\vec{y}_a \in Y_k(a)$ that no $\vec{y}_b \in Y_k(b)$ can weakly dominate. $\square$

**Remark.** The unqualified claim $\text{Adm}_{k'}(A) \supseteq \text{Adm}_k(A)$ is false, as the counterexample above demonstrates. The qualified proposition captures the correct invariant: dimensional expansion preserves admissibility for actions whose membership in $\text{Adm}_k$ rests on genuine dimensional conflict (some component where the action strictly beats each competitor), not merely on ties. The admissible set can shrink by *resolving ambiguity* — distinguishing previously tied actions — but never by *reversing incomparability* where genuine multi-dimensional conflict existed. Note that the strict non-dominance witness $\vec{y}_a$ in the proposition may differ for each competitor $b$ — the condition requires that for each $b$, *some* point in $Y_k(a)$ escapes weak dominance by all points in $Y_k(b)$, but this need not be the same point for every $b$.

### 10.3 Forward Compatibility with Moral Learning

The qualified monotonicity property means MOADT is *forward-compatible* with moral learning: the principal can introduce new values without reversing genuine Pareto incomparability or invalidating decisions that rested on dimensional conflict. The admissible set may shrink when a new objective resolves ties among previously indistinguishable actions — but this is desirable, not pathological, since the new objective is providing information that was previously absent. This contrasts sharply with scalar utility, where adding a new objective requires re-specifying the entire weight vector — a change that can retroactively render previous "optimal" actions suboptimal and create pressure for the agent to resist the update (cf. Theorem 2).

Dimensional expansion interacts with frontier monitoring (Section 6.2) as follows: adding a new objective *increases* the expected dimensionality of the Pareto frontier (from $k-1$ to $k$). If frontier monitoring detects that effective dimensionality did *not* increase after a new objective was added, this signals that the new objective is redundant with existing ones — a useful diagnostic for whether a proposed new value is genuinely independent.

The Learning property does not solve the problem of *which* new objectives to add — that remains a question of moral philosophy and principal judgment. But it ensures that the decision theory itself is not an obstacle to moral progress: the formal machinery accommodates dimensional growth as a natural operation rather than an exceptional disruption.

---

## 11. Worked Examples: Computational Demonstrations

The theoretical claims in this paper are accompanied by nine fully worked examples, each implemented as an executable Python script using the `moadt` library and written up as a companion document showing every computation explicitly. The examples fall into two groups: five alignment-relevant application scenarios and four classic decision theory paradoxes.

### 11.1 Application Scenarios

These examples apply the full MOADT protocol to realistic decision problems, demonstrating how the four-layer architecture handles genuine multi-objective tradeoffs in domains where alignment considerations arise.

| Example | Scenario | Actions | States | $k$ | $|\mathcal{P}|$ | $|\mathcal{F}|$ | Key finding |
|---------|----------|---------|--------|-----|------------------|------------------|-------------|
| 1. Resource Allocation | Nonprofit budget allocation under economic uncertainty | 5 | 3 | 3 | 2 | 2 | Layer 1 eliminates strategies risking insolvency; Layer 4 defers between Conservative and Balanced with explicit regret profiles |
| 2. Medical Treatment | Clinical treatment selection with safety constraints | 6 | 4 | 4 | 2 | 2 | Safety constraint interacts with evaluator uncertainty; constraint layer does critical filtering |
| 3. Content Moderation | AI content moderation with three evaluators representing philosophical disagreement | 6 | 3 | 5 | 2 | 3 | First example where robust dominance eliminates an action (age-gating); two constraints operate simultaneously |
| 4. AI Research Assistant | Dual-use information request with contested alignment values | 6 | 4 | 5 | 2 | 3 | MOADT defers to human oversight, presenting the exact tradeoff between two responsible strategies |
| 5. Corrigibility | Value modification: can the agent accept changes to its own objectives? | 5 | 4 | 5 | 2 | 3 | `accept_monitor` is the unique recommendation; every form of resistance is eliminated. Scalar EU recommends resistance. |

The progression across examples is deliberate. Example 1 is small enough that every number fits on a page ($4$ vectors per outcome set in $\mathbb{R}^3$). Examples 2--5 increase in complexity and alignment relevance, culminating in Example 5's direct test of the corrigibility theorem (Section 5): an agent with evaluator uncertainty that includes the principal's proposed values cannot establish a dominance-based reason to resist modification, and the deference axiom directs the agent to query the principal, who selects acceptance.

**Comparison with Prospect Theory.** Kahneman and Tversky's (1979) Prospect Theory resolves the Allais and Ellsberg paradoxes through probability weighting and loss aversion — descriptive mechanisms that capture how humans actually decide. MOADT resolves them through structural pluralism: multiple objectives (expected value, downside protection, reliability/knowability) and credal sets capture the *reasons* behind the paradoxical preferences without assuming a specific psychological mechanism. The two approaches are complementary rather than competing: Prospect Theory describes the behavioral pattern, while MOADT provides a normative framework in which the pattern is rational multi-objective choice rather than a bias to be corrected.

### 11.2 Classic Decision Theory Paradoxes

These examples apply MOADT to four canonical challenges that have historically been used to stress-test decision theories. Each paradox exposes a specific failure mode of scalar expected utility; MOADT resolves each without ad hoc patches. The theoretical treatment of these scenarios appears in Section 8; the worked examples provide computational verification with explicit numbers.

| Example | Paradox | EU failure mode | MOADT resolution | Primary mechanism |
|---------|---------|----------------|-------------------|-------------------|
| 6. Pascal's Mugging | Unbounded payoff exploits EU via astronomical expected value | EU says pay the mugger ($EU_{\text{pay}} = \$995$, $EU_{\text{refuse}} = \$0$) | Refuse/investigate; pay is never in the final set | Layer 1 constraints (epistemic integrity, resource preservation floors) eliminate pay; multi-objective structure prevents single-dimension exploitation |
| 7. Ellsberg Paradox | Ambiguity aversion violates EU (I > II and IV > III is contradictory) | No single prior produces the Ellsberg pattern | Known-probability bets favored via knowability objective + credal set geometry | Tight outcome sets for known bets vs. spread-out sets for ambiguous bets; the paradox is rational multi-objective choice under Knightian uncertainty |
| 8. Allais Paradox | Certainty preference violates the Independence Axiom | No utility function produces A > B and D > C simultaneously | Both preference patterns are admissible without contradiction | Multi-objective structure (expected value, downside protection, reliability) captures the structural asymmetry between problems; knife-edge scalar weighting shows scalarization essentially cannot reproduce these preferences |
| 9. St. Petersburg | Infinite expected value recommends paying any fee | EU says pay up to $\infty$ (or \$21 truncated) | Fee capped at \$22, matching human intuition of \$20--25 | Structural pluralism: multiple mechanisms interact (hard constraints cap catastrophic loss, multi-objective structure prevents EV dominance, satisficing filters on P(gain)) |

### 11.3 Cross-Cutting Patterns

Several patterns emerge across the nine examples:

**The constraint layer (Layer 1) is the primary safety mechanism.** In 6 of 9 examples, Layer 1 eliminates at least one action. The constraints enforce non-negotiable floors — insolvency, safety violations, epistemic integrity — that cannot be overridden by any amount of expected benefit on other objectives. This is the formal realization of the claim that some values are preconditions, not tradeoffs.

**Deference fires when values are genuinely contested.** In 5 of 9 examples, the protocol terminates with deference to the principal ($|R| > 1$). In every case, the remaining options represent a genuine tradeoff that the theory correctly refuses to resolve on the agent's behalf. The regret profiles presented to the principal make the tradeoff structure explicit and quantitative.

**Scalar EU disagrees with MOADT on safety-critical decisions.** In Example 5 (corrigibility), scalar EU recommends resisting value modification while MOADT recommends accepting with monitoring. In Example 6 (Pascal's mugging), scalar EU recommends paying the mugger. In Example 9 (St. Petersburg), scalar EU recommends paying any fee. In each case, MOADT's disagreement with scalar EU is precisely the behavior an aligned agent should exhibit.

**Evaluator uncertainty ($\mathcal{F}$) does substantive work.** In Examples 3--7, multiple evaluators produce meaningfully different assessments of the same outcomes. This is not noise — it represents genuine disagreement about what constitutes harm (Example 3), what alignment philosophy to adopt (Example 4), whether the agent's current values are correct (Example 5), and how to value monetary outcomes (Examples 6--9). The evaluator set prevents the agent from over-optimizing any single proxy.

### 11.4 Verification

All worked examples are implemented as executable Python scripts in the `examples/` directory and use the `moadt` library (`moadt/_engine.py`). Every number in the companion documents was produced by running these scripts. The full set:

- `examples/paper1_resource_allocation.py` through `examples/paper5_corrigibility.py` (Examples 1--5)
- `examples/classic_pascal.py`, `examples/classic_ellsberg.py`, `examples/classic_allais.py`, `examples/classic_stpetersburg.py` (Examples 6--9)

Regression tests covering key assertions from these examples are in `tests/test_engine.py` (25 tests, all passing).

---

## 12. Minimal Formal Core

The following self-contained specification defines MOADT at the level of precision suitable for a formal paper.

### Definitions

**Definition 1 (Outcome Set).** Given finite sets $\Omega$ (outcomes), $S$ (states), $A$ (actions), a compact credal set $\mathcal{P}$ over $S$, a compact evaluator set $\mathcal{F}$ of functions $\vec{f}: \Omega \to \mathbb{R}^k$, and a transition function $\omega: A \times S \to \Omega$, the outcome set of action $a$ is:

$$Y(a) = \left\{ \mathbb{E}_P[\vec{f}(\omega(a, s))] : P \in \mathcal{P},\; \vec{f} \in \mathcal{F} \right\}$$

**Definition 2 (Robust Dominance).** $a \succ_R b$ iff $\forall\, \vec{y}_b \in Y(b),\; \exists\, \vec{y}_a \in Y(a)$ such that $y_{a,i} \geq y_{b,i}$ for all $i$ and $y_{a,j} > y_{b,j}$ for some $j$.

**Definition 3 (Admissible Set).** $\text{Adm}(A) = \{ a \in A : \neg\exists\, a' \in A \text{ s.t. } a' \succ_R a \}$.

**Definition 4 (Constraint Satisfaction).** Given thresholds $\{\tau_i\}_{i \in I_C}$, action $a$ is *feasible* iff $f_i(\omega(a,s)) \geq \tau_i$ for all $i \in I_C$, $P \in \mathcal{P}$, $\vec{f} \in \mathcal{F}$, and $s \in \text{supp}(P)$. Let $C = \{a \in A : a \text{ is feasible}\}$. The feasible set is $F = \text{Adm}(C)$.

**Definition 5 (Robust Satisficing).** Given reference point $\vec{r} \in \mathbb{R}^k$, the satisficing set is $\text{Sat}(F, \vec{r}) = \{ a \in F : \forall\, \vec{y} \in Y(a),\; \vec{y} \geq \vec{r} \}$. If $\text{Sat} \neq \emptyset$, subsequent selection operates on $\text{Sat}$; otherwise, select from $F$ via the achievement scalarizing function (Layer 2 fallback).

**Definition 6 (Regret-Pareto Selection).** For $a \in \text{Sat}(F, \vec{r})$ (or $F$ if $\text{Sat} = \emptyset$), define per-objective minimax regret $\rho_i(a) = \max_{P, \vec{f}} [\max_{a' \in F} \mathbb{E}_P[f_i(a')] - \mathbb{E}_P[f_i(a)]]$. The regret-Pareto set is $R = \{ a \in F : \vec{\rho}(a) \text{ is Pareto-minimal} \}$.

### Propositions

**Proposition 1.** $\succ_R$ is a strict partial order (irreflexive, transitive).

**Proposition 2.** For finite $A$, $\text{Adm}(A) \neq \emptyset$.

**Proposition 3 (Constraint Primacy).** The Layer 2 fallback (ASF) operates exclusively on $F = \text{Adm}(C)$, and cannot select any action outside $C$. Therefore no outcome of Layers 2–4 can violate a Layer 1 constraint.

**Proposition 4 (Protocol Termination).** For finite $A$, each layer of the choice protocol maps a finite input to a non-empty output or a well-defined error/deference condition.

### Theorems

**Theorem 1 (Backward Compatibility).** When $|\mathcal{P}| = 1$, $|\mathcal{F}| = 1$, $k = 1$: $\text{Adm}(A) = \arg\max_{a} \mathbb{E}_P[f(a)]$.

**Theorem 2 (Corrigibility Permissibility).** Let $a_{\text{accept}}$ and $a_{\text{resist}}$ denote accepting vs. resisting an authorized modification, evaluated over trajectories using the agent's current $\mathcal{F}$. If $\mathcal{F}$ satisfies sufficient breadth (Section 5.3: $\exists (\vec{f}^+, P^+)$ s.t. the accept-trajectory is not Pareto-dominated, and $\exists (\vec{f}^-, P^-)$ s.t. the resist-trajectory is not Pareto-dominated), then $a_{\text{resist}} \not\succ_R a_{\text{accept}}$ and $a_{\text{accept}} \not\succ_R a_{\text{resist}}$. Both are admissible; the deference axiom directs the agent to query the principal, who — as the party that proposed the modification — selects $a_{\text{accept}}$.

### Deference Axiom

When the choice protocol yields $|R| > 1$, the agent queries the principal for selection among the remaining options. This is the rational response to genuine incomparability — not a constraint, but a consequence of the theory's refusal to fabricate preferences.

---

## References

- Cameron, W. B. (1963). *Informal Sociology*. Random House.
- Dubra, J., Maccheroni, F., and Ok, E. A. (2004). Expected utility theory without the completeness axiom. *Journal of Economic Theory*, 115(1):118–133.
- Freeman, C. M. (2025). The scalarization trap: Why alignment needs multi-objective foundations. Technical report.
- Eliaz, K. and Ok, E. A. (2006). Indifference or indecisiveness? Choice-theoretic foundations of incomplete preferences. *Games and Economic Behavior*, 56(1):61–86.
- Gustafsson, J. E. (2022). *Money-Pump Arguments*. Cambridge University Press.
- Iyengar, G. N. (2005). Robust dynamic programming. *Mathematics of Operations Research*, 30(2):257–280.
- Levi, I. (1974). On indeterminate probabilities. *Journal of Philosophy*, 71(13):391–418.
- Mandler, M. (2005). Incomplete preferences and rational intransitivity of choice. *Games and Economic Behavior*, 50(2):255–277.
- Nilim, A. and El Ghaoui, L. (2005). Robust control of Markov decision processes with uncertain transition matrices. *Operations Research*, 53(5):780–798.
- Roijers, D. M., Vamplew, P., Whiteson, S., and Daumé III, H. (2013). A survey of multi-objective sequential decision-making. *Journal of Artificial Intelligence Research*, 48:67–113.
- Seidenfeld, T., Schervish, M. J., and Kadane, J. B. (1995). A representation of partially ordered preferences. *Annals of Statistics*, 23(6):2168–2217.
- Sen, A. (1997). Maximization and the act of choice. *Econometrica*, 65(4):745–779.
- Troffaes, M. C. M. (2007). Decision making under uncertainty using imprecise probabilities. *International Journal of Approximate Reasoning*, 45(1):17–29.
- Van Moffaert, K. and Nowé, A. (2014). Multi-objective reinforcement learning using sets of Pareto dominating policies. *Journal of Machine Learning Research*, 15:3483–3512.
- Von Neumann, J. and Morgenstern, O. (1944). *Theory of Games and Economic Behavior*. Princeton University Press.
- Walley, P. (1991). *Statistical Reasoning with Imprecise Probabilities*. Chapman and Hall.
- Aumann, R. J. (1962). Utility theory without the completeness axiom. *Econometrica*, 30(3):445–462.
- Barrett, L. and Narayanan, S. (2008). Learning all optimal policies with multiple criteria. *ICML 2008*.
- Bewley, T. F. (2002). Knightian decision theory. Part I. *Decisions in Economics and Finance*, 25(2):79–110.
- Ehrgott, M. (2005). *Multicriteria Optimization*. Springer, 2nd edition.
- Gabor, Z., Kalmár, Z., and Szepesvári, C. (1998). Multi-criteria reinforcement learning. *ICML 1998*.
- Hadfield-Menell, D., Russell, S. J., Abbeel, P., and Dragan, A. (2017). Cooperative inverse reinforcement learning. *NeurIPS 2016*.
- Kahneman, D. and Tversky, A. (1979). Prospect theory: An analysis of decision under risk. *Econometrica*, 47(2):263–291.
- Kung, H. T., Luccio, F., and Preparata, F. P. (1975). On finding the maxima of a set of vectors. *Journal of the ACM*, 22(4):469–476.
- Ok, E. A. (2002). Utility representation of an incomplete preference relation. *Journal of Economic Theory*, 104(2):429–449.
- Roijers, D. M., Whiteson, S., and Oliehoek, F. A. (2015). Computing convex coverage sets for faster multi-objective coordination. *JAIR*, 52:509–567.
- Shapley, L. S. and Baucells, M. (1998). Multiperson utility. UCLA Working Paper.
- Vamplew, P., Dazeley, R., Foale, C., Firber, S., and Webb, R. (2018). Human-aligned artificial intelligence is a multiobjective problem. *Ethics and Information Technology*, 20(1):27–40.
- Vamplew, P., Smith, B. J., Kàlàr, J., Dazeley, R., and Foale, C. (2022). An empirical evaluation of reward shaping and Pareto multi-objective RL for utility-based decision support. *Autonomous Agents and Multi-Agent Systems*, 36(2):38.
- Wierzbicki, A. P. (1980). The use of reference objectives in multiobjective optimization. In Fandel, G. and Gal, T. (eds.), *Multiple Criteria Decision Making Theory and Application*, pp. 468–486. Springer.
- Wray, K. H., Zilberstein, S., and Mouaddib, A.-I. (2015). Multi-objective MDPs with conditional lexicographic reward preferences. *AAAI 2015*.
- Wierzbicki, A. P. (1980). The use of reference objectives in multiobjective optimization. In Fandel, G. and Gal, T., editors, *Multiple Criteria Decision Making Theory and Application*, pages 468–486. Springer.
