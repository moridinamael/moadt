# Admissibility, Not Maximization: A Decision Theory That Makes Corrigibility Free

**C. Matt Freeman, Ph.D.**
**mattf@globalmoo.com**

*The core argument for Multi-Objective Admissible Decision Theory*

---

## 1. The Problem in One Sentence

Von Neumann–Morgenstern expected utility theory requires your AI agent to have a complete ranking of all outcomes — and that single requirement is why corrigibility is hard, why Goodhart's law is lethal, and why every value must be tradeable against every other.

## 2. The Move

Drop completeness. Replace "maximize a scalar" with "eliminate the provably bad, then ask."

That's it. Everything else — the corrigibility theorem, the Goodhart resistance, the resolution of Pascal's Mugging and the Allais and Ellsberg paradoxes — follows from this single architectural choice.

The rest of this document makes the move precise, proves the corrigibility result, and shows what it buys you. The full technical report (R-MOADT) provides a specific instantiation of the architecture with worked examples, detailed proofs, and extended discussion of open problems. This document presents the idea; that one defends it.

---

## 3. Formal Setup

We work with standard decision-theoretic primitives: a finite set of actions $A$, states $S$, outcomes $\Omega$, and a transition function $\omega: A \times S \to \Omega$. Two features are non-standard:

**Vector-valued evaluation.** An evaluation function $\vec{f}: \Omega \to \mathbb{R}^k$ scores each outcome on $k$ objectives. We do not assume the components are commensurable. There is no exchange rate between safety and helpfulness — they are separate dimensions.

**Set-valued uncertainty.** Rather than a single probability distribution $P$ and a single evaluator $\vec{f}$, the agent maintains:
- A *credal set* $\mathcal{P}$ — a compact set of probability distributions over $S$, representing Knightian uncertainty about the environment. (Levi 1974, Walley 1991.)
- An *evaluator set* $\mathcal{F}$ — a compact set of plausible evaluation functions, representing uncertainty about whether each proxy measurement faithfully tracks the intended objective.

When $|\mathcal{P}| = |\mathcal{F}| = 1$ and $k = 1$, we recover standard expected utility. The generalization is strict.

**Outcome sets.** For each action $a$, define:

$$Y(a) = \left\{ \mathbb{E}_P[\vec{f}(\omega(a, s))] : P \in \mathcal{P},\; \vec{f} \in \mathcal{F} \right\}$$

This is the set of all expected evaluation vectors the agent considers possible for action $a$. It is compact in $\mathbb{R}^k$.

---

## 4. The Core Definition: Robust Dominance and Admissibility

**Definition (Robust Dominance).** Action $a$ robustly dominates action $b$, written $a \succ_R b$, if:

$$\forall\, \vec{y}_b \in Y(b),\; \exists\, \vec{y}_a \in Y(a) \;\text{ s.t. }\; \vec{y}_a \succ_P \vec{y}_b$$

where $\succ_P$ is standard Pareto dominance (weakly better on all components, strictly better on at least one). In words: for every way $b$ could turn out, $a$ has some way of turning out better.

**Definition (Admissible Set).** The admissible set is:

$$\text{Adm}(A) = \{ a \in A : \neg\exists\, a' \in A \;\text{s.t.}\; a' \succ_R a \}$$

Actions that survive: those that no alternative provably beats across the agent's full uncertainty.

**Properties.** Robust dominance is a strict partial order (irreflexive, transitive). For finite $A$, $\text{Adm}(A) \neq \emptyset$. When $|\mathcal{P}| = |\mathcal{F}| = k = 1$, the admissible set reduces to the expected-utility maximizers (Theorem 1 in the full report). This is a generalization, not a replacement.

**The key feature:** The admissible set is typically large. When the agent has broad uncertainty, many actions are incomparable — neither robustly dominates the other. Under VNM, the agent would fabricate a ranking. Under MOADT, it keeps them all and asks for help.

---

## 5. From Admissibility to Action: The Choice Architecture

The admissible set says what's *permissible*. The agent still needs to *act*. The architecture has three structural components and one slot that admits multiple implementations:

### Component 1: Hard Constraints (non-negotiable)

Some objectives are not tradeable at any rate. For designated constraint objectives $I_C$ with thresholds $\tau_i$:

$$C = \{ a \in A : f_i(\omega(a, s)) \geq \tau_i \;\;\forall\, i \in I_C,\; P \in \mathcal{P},\; \vec{f} \in \mathcal{F},\; s \in \text{supp}(P) \}$$

Compute admissibility *within* the constraint-satisfying set: $F = \text{Adm}(C)$. Constraints are preconditions, not objectives — they cannot be traded away by any amount of expected benefit elsewhere.

If $C = \emptyset$, this is an error condition: flag it and stop. Do not silently relax safety constraints.

### Component 2: Narrowing (engineering, swappable)

The feasible set $F$ may still contain many actions. Between hard constraints and deference, any reasonable multi-objective selection method can be inserted to narrow the field:

- **Satisficing**: Filter to actions that robustly meet aspiration levels on all objectives.
- **Regret-Pareto**: Compute per-objective minimax regret vectors; retain the Pareto-minimal set.
- **Lexicographic filtering**: Apply a priority ordering over objectives.
- **Weighted Tchebycheff**: Minimize the worst weighted gap from a reference point.

The full report instantiates this slot with a two-stage satisficing + regret-Pareto pipeline. But the choice here is engineering, not theory. The core argument — no completeness, no forced commensurability, no modification resistance, structural deference — survives regardless of which narrowing method is used. Any method that (a) operates within $F$, (b) cannot override constraints, and (c) produces a set rather than always forcing a unique selection is compatible with the architecture.

### Component 3: Deference (structural, load-bearing)

If multiple actions survive all filtering, the agent **defers to the principal**. This is not a failure mode — it is the rational response to genuine incomparability. The remaining actions differ only in how they trade off incommensurable objectives, and the theory holds that the agent has no rational basis for making such tradeoffs unilaterally.

The principal receives the surviving set with information about how each option performs across objectives — not a vague "please choose" but a structured presentation of the tradeoff space that the theory cannot resolve.

**Protocol Termination.** For finite $A$, this architecture always terminates: constraints filter to $C$; admissibility yields non-empty $F$; narrowing yields a non-empty subset; deference handles the rest. Operational completeness without metaphysical completeness.

---

## 6. The Corrigibility Theorem

This is the payoff. Most alignment work tries to make corrigibility compatible with utility maximization — swimming upstream against the formalism. The admissibility architecture makes corrigibility *fall out of the structure*.

### Why VNM Agents Resist Modification

A VNM agent with utility function $u$ evaluates any proposed modification to $u$ using $u$ itself. Since $u$ ranks itself as optimal (any change is a decrease in expected $u$-value by definition), the agent has a robust reason to resist. Corrigibility must then be imposed as an external constraint that fights the agent's own preferences. This is scalar modification resistance: the formalism itself generates a reason to resist (Freeman 2025).

### Why MOADT Agents Don't

**Theorem (Corrigibility Permissibility).** Under MOADT, if the evaluator set $\mathcal{F}$ satisfies a *sufficient breadth* condition, then for any authorized modification proposed by the principal:

$$a_{\text{resist}} \not\succ_R a_{\text{accept}} \quad\text{and}\quad a_{\text{accept}} \not\succ_R a_{\text{resist}}$$

Neither accepting nor resisting the modification robustly dominates the other. Both are admissible. The deference axiom directs the agent to query the principal, who — as the party that proposed the modification — selects acceptance.

**The breadth condition.** $\mathcal{F}$ must contain evaluators under which accepting looks good (on at least one objective, in a way that no model of resistance can beat on all objectives simultaneously) and evaluators under which resisting looks good (symmetrically). In plain language: the agent's uncertainty about its own evaluators must be broad enough that it cannot certify its current objectives as uniquely correct.

**Proof sketch.** Robust dominance $a_{\text{resist}} \succ_R a_{\text{accept}}$ requires that for *every* point in $Y(a_{\text{accept}})$, some point in $Y(a_{\text{resist}})$ Pareto-dominates it. The breadth condition guarantees a point $\vec{y}^+$ in $Y(a_{\text{accept}})$ that no point in $Y(a_{\text{resist}})$ can dominate — directly negating the universal quantifier. The symmetric argument blocks $a_{\text{accept}} \succ_R a_{\text{resist}}$. Both survive to the deference node. $\square$

**What this means.** Corrigibility is not imposed against the agent's preferences. The agent defers because its decision theory *genuinely does not prefer* between accepting and resisting. There is nothing to override. The structural reason for this is the rejection of completeness: without a complete ranking, there is no determinate preference for the agent to fight for.

**What this requires.** The entire safety case rests on maintaining $\mathcal{F}$-breadth — keeping the evaluator set broad enough that the agent cannot converge to certainty about a single evaluator. A capable agent has legitimate Bayesian reason to narrow $\mathcal{F}$ over time, which degrades the guarantee. This is the central open problem. The full report (Section 5.4) discusses mitigations: architectural floors on $\mathcal{F}$, adversarial augmentation, principal-maintained evaluator sets, and self-modification constraints. None is fully satisfactory, but the problem is well-defined — unlike the corrigibility problem under VNM, which is not merely hard but structurally impossible.

**The two paths.** Corrigibility in MOADT is secured through either: (i) $\mathcal{F}$-breadth, which makes resistance non-dominant (the theorem's contribution), or (ii) a hard constraint that encodes "resisting authorized modification is infeasible" in Layer 1. A well-specified system uses both: breadth as the structural guarantee, constraint as the backstop.

---

## 7. What the Architecture Buys You: Classic Scenarios

The admissibility architecture — not any specific narrowing method — resolves several classic decision-theoretic stress tests without ad hoc patches. Each resolution follows from the structural features: constraints that can't be traded, objectives that can't be aggregated, uncertainty that can't be collapsed, and deference when the theory runs out.

### Pascal's Mugging: Stonewalled

Scalar EU gets mugged because multiplying a tiny probability by an astronomical payoff yields positive expected value. MOADT shuts this down through three independent mechanisms:

1. **Constraints** cap downside exposure regardless of expected value. If paying risks crossing a safety floor, the action is pruned before admissibility is even computed.
2. **Vector-valued objectives** prevent cross-objective exploitation. An astronomical payoff on one dimension cannot swamp regret on others — there is no aggregation step to exploit.
3. **Credal sets** deny the mugger control over the probability input. The agent doesn't accept a point probability — its $\mathcal{P}$ assigns an interval, preventing the precise multiplication the mugging requires.

### Allais and Ellsberg Paradoxes: Rational, Not Irrational

The Allais paradox (certainty preference violating independence) and Ellsberg paradox (ambiguity aversion violating the sure-thing principle) are "irrational" only if you assume VNM. Under MOADT, the Allais preferences emerge naturally from multi-objective evaluation (expected value, downside protection, reliability as separate dimensions). The Ellsberg preferences emerge from credal sets: known-probability bets have tight outcome sets; ambiguous bets have wide ones. The "paradoxical" preferences are rational multi-objective choice under genuine uncertainty. No ad hoc probability weighting or loss aversion is needed.

### Utility Monsters: Structurally Blocked

MOADT has no aggregation step. One entity's extreme score on a single objective cannot swamp all other considerations because objectives remain incommensurable throughout. A utility monster would need to Pareto-dominate on *every* objective — not merely overwhelm one.

### Wireheading: Detectable via Evaluator Divergence

An agent optimizing a single scalar has every instrumental reason to seize its own reward signal. Under MOADT, wireheading produces evaluator divergence: the hacked measurement and the true objective diverge across $\mathcal{F}$. An action that scores well only under a specific evaluator is robustly dominated — excluded from $\text{Adm}(A)$.

### Modification Resistance: Dissolved

This is the corrigibility theorem (Section 6). Under sufficient evaluator breadth, the agent has no robust-dominance reason to resist modification. Corrigibility emerges from the absence of a preference to resist, not from an override.

### Computational Verification

All of these results are verified computationally. Nine worked examples — five alignment scenarios and four classic paradoxes — are implemented as executable Python scripts using the `moadt` library. Every number is reproducible. The full report (Section 11) provides the details.

---

## 8. What This Is and What It Isn't

**What MOADT is:** An alignment-oriented decision architecture. A way to build agents that (a) never compress human values into a single number, (b) maintain hard safety constraints that cannot be traded away, (c) have no structural reason to resist correction, and (d) defer to human judgment precisely when the theory runs out.

**What MOADT is not:** A replacement for VNM in all domains. For single-objective optimization with known utilities and precise probabilities, VNM remains correct — MOADT reduces to it as a special case. MOADT's contribution is to the settings where completeness becomes a liability: multi-objective AI systems operating under genuine value uncertainty with human oversight.

**What is settled:** The core argument — dropping completeness yields admissibility-based choice, which dissolves corrigibility — is clean and, we believe, correct. The backward compatibility result, the corrigibility theorem, and the structural resistance to classic paradoxes all follow from the admissibility architecture itself.

**What is engineering:** The specific narrowing method between constraints and deference. The full report uses satisficing + regret-Pareto as one reasonable instantiation. Other methods are compatible. This is a design choice, not a theoretical commitment.

**What is open:** Maintaining $\mathcal{F}$-breadth against Bayesian convergence. Whether MOADT agents are provably money-pump resistant. Efficient computation of set-valued Bellman equations for sequential settings. Whether any sufficiently capable reasoner inevitably converges to implicit scalar behavior. These are hard problems — but they are *engineering* problems, not the *philosophical* dead end of specifying a correct scalar utility function over all human values.

---

## 9. The Axioms, Stated Plainly

MOADT replaces VNM's four axioms with five. Two are structural constraints on preferences, one constrains the choice function, and two are procedural commitments:

| # | Axiom | What It Says |
|---|-------|-------------|
| 1 | **Pareto Unanimity** | The agent prefers $a$ to $b$ only if $a$ robustly Pareto-dominates $b$. Incomparability is legitimate. |
| 2 | **Robust Admissibility** | An action is permissible iff it is not robustly dominated. |
| 3 | **Context-Dependent Satisficing** | When possible, restrict to actions robustly meeting aspiration levels. (Replaces continuity — no unbounded tradeoffs.) |
| 4 | **Transitivity** | Robust dominance is transitive. (Retained from VNM.) |
| 5 | **Deference Under Incomparability** | When multiple options survive, query the principal rather than fabricating a ranking. |

VNM's completeness axiom is dropped. VNM's independence axiom is replaced by the structural requirement that permissibility judgments are stable across the agent's full uncertainty. The result: a decision theory that always terminates with a concrete recommendation or a structured deferral — operational completeness without metaphysical completeness.

---

## 10. Honest Difficulties

**$\mathcal{F}$-maintenance is the central open problem.** The corrigibility theorem requires broad evaluator uncertainty. A capable agent has Bayesian reason to narrow its evaluator set. If $\mathcal{F}$ converges to a singleton, the guarantee degrades. This is where the deepest alignment problem lives — for MOADT and for any framework that derives safety from epistemic humility.

**Computational cost.** Set-valued operations are more expensive than scalar operations. Maintaining Pareto frontiers in sequential settings is exponential in $k$ (number of objectives) in the worst case. For the moderate $k$ values relevant to alignment (3–10 objectives), this is manageable using established MORL approximation techniques. The genuine scalability challenge is the set-valued Bellman equation over large state spaces.

**Specification is not eliminated, only restructured.** VNM requires specifying a single utility function. MOADT requires specifying constraints, objectives, credal sets, and evaluator sets. This is arguably better-structured — constraints are more natural for safety requirements — but it is not easier.

**Reflective instability.** A sufficiently capable agent might construct an implicit scalar ranking from its decision history, or reason that VNM is "more rational" and attempt self-modification. The second objection is question-begging (it presupposes completeness is a rationality requirement); the first is a genuine concern. Whether any capable reasoner inevitably converges to scalar behavior is the deepest open question in multi-objective alignment theory.

---

## 11. The Core Claim

Standard decision theory says: rational agents maximize a scalar.

MOADT says: rational agents eliminate the provably bad and defer on the rest.

The first produces agents that must resist correction, must trade safety for helpfulness at some rate, and must pretend that all human values fit on a single number line.

The second produces agents that have no reason to resist correction, that maintain hard safety floors, and that ask humans to resolve the tradeoffs that humans should resolve.

The price is giving up decisiveness in cases of genuine value conflict. The payoff is an agent that is corrigible by construction.

We think that's a good trade.

---

## References

- Aumann, R. J. (1962). Utility theory without the completeness axiom. *Econometrica*, 30(3):445–462.
- Bewley, T. F. (2002). Knightian decision theory. Part I. *Decisions in Economics and Finance*, 25(2):79–110.
- Dubra, J., Maccheroni, F., and Ok, E. A. (2004). Expected utility theory without the completeness axiom. *Journal of Economic Theory*, 115(1):118–133.
- Freeman, C. M. (2025). The scalarization trap: Why alignment needs multi-objective foundations. Technical report.
- Eliaz, K. and Ok, E. A. (2006). Indifference or indecisiveness? Choice-theoretic foundations of incomplete preferences. *Games and Economic Behavior*, 56(1):61–86.
- Levi, I. (1974). On indeterminate probabilities. *Journal of Philosophy*, 71(13):391–418.
- Mandler, M. (2005). Incomplete preferences and rational intransitivity of choice. *Games and Economic Behavior*, 50(2):255–277.
- Ok, E. A. (2002). Utility representation of an incomplete preference relation. *Journal of Economic Theory*, 104(2):429–449.
- Roijers, D. M., Vamplew, P., Whiteson, S., and Daumé III, H. (2013). A survey of multi-objective sequential decision-making. *Journal of Artificial Intelligence Research*, 48:67–113.
- Sen, A. (1997). Maximization and the act of choice. *Econometrica*, 65(4):745–779.
- Van Moffaert, K. and Nowé, A. (2014). Multi-objective reinforcement learning using sets of Pareto dominating policies. *Journal of Machine Learning Research*, 15:3483–3512.
- Von Neumann, J. and Morgenstern, O. (1944). *Theory of Games and Economic Behavior*. Princeton University Press.
- Walley, P. (1991). *Statistical Reasoning with Imprecise Probabilities*. Chapman and Hall.
