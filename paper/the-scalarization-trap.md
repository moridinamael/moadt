# The Scalarization Trap: Why Alignment Needs Multi-Objective Foundations

**C. Matt Freeman, Ph.D.**
**mattf@globalmoo.com**

**Epistemic status:** Novel synthesis of established mathematical tools (Pareto dominance, multi-gradient methods, incomplete preference theory) applied to alignment. The individual pieces are well-established; the synthesis and alignment implications are new. We believe this reframing makes some aspects of the alignment problem more tractable — particularly corrigibility and value-structure monitoring — while leaving the hardest parts (deceptive alignment, reflective stability, scalable oversight) largely untouched. Toy experiment results are included; more extensive experiments are planned.

**TL;DR:** Alignment inherited scalar utility theory from economics — a formalism whose creators never intended it as an account of human values. We show that multi-objective optimization removes a structural impossibility that makes corrigibility incompatible with scalar rationality, and provides concrete observability advantages (multiple informative knobs instead of one opaque loss) for alignment monitoring.

---

## 1. The Violence of Scalarization

> "Optimization algorithms impose a strong mathematical structure on the decision problem. Their power is bought at the cost of shaping and squeezing the real-world problem to fit their computational requirements."
> — Herbert Simon, *The Sciences of the Artificial* (1996)

### 1.1 The VNM Sleight of Hand

The von Neumann-Morgenstern utility theorem proves that if a rational agent's preferences satisfy four axioms (completeness, transitivity, independence, continuity), then those preferences can be *represented* by a scalar utility function.

The word "represented" is doing enormous work. It means: there exists a scalar function that generates the same preference ordering. It does *not* mean that the agent's internal process is scalar optimization. It is a representation theorem, not an ontological claim. Von Neumann and Morgenstern themselves knew this — they wrote that they had "practically defined numerical utility as being that thing for which the calculus of mathematical expectations is legitimate" (1953, p. 28). They were constructing a mathematical object that made their equations work, not claiming to have discovered the structure of human preference.

But the entire field — economics, game theory, decision theory, and eventually alignment research — treated it as ontological. "Rational agents maximize utility" became a discovered law rather than a representational convenience. As Sen (1977) observed, a person who collapses all their motivations into a single preference ordering "may be 'rational' in the limited sense of revealing no inconsistencies in his choice behavior, but if he has no use for these distinctions between quite different concepts, he must be a bit of a fool."

Alignment researchers then said: "We need to figure out the human utility function so we can align AI to it." A project that is *guaranteed* to destroy the structure that matters.

**A concrete example.** Imagine evaluating two AI assistants. Assistant A is very safe but somewhat unhelpful. Assistant B is very helpful but somewhat unsafe. A scalar utility function must declare one of them *better*. But the real answer is that they are good at *different things* — and a framework that forces you to pick a winner has already thrown away the most important information: that safety and helpfulness are *separate dimensions* with a genuine tradeoff between them. The scalarization has destroyed the structure of the problem before optimization even begins.

Each VNM axiom has independent normative force, and we should be precise about which one we are challenging. Transitivity is hard to abandon without licensing money-pump arguments. Independence is the target of Allais-style paradoxes, and an entire literature (prospect theory, rank-dependent utility) weakens it while retaining scalar structure. Continuity is technical and rarely controversial.

**The axiom that matters most for our argument is completeness** — the requirement that for any two outcomes, the agent either prefers one or is indifferent. This is the axiom that forces every pair of outcomes to be comparable, yielding a total ordering rather than a partial one. When completeness fails, you get *incomplete preferences* — a structure where some outcomes are genuinely incomparable, not because of ignorance, but because no well-defined comparison exists.

### 1.2 What Happens When You Drop Completeness

Dropping completeness is not a new move — the formal tools for handling incomplete preferences already exist (see Section 2 for the full literature). The key result, due to Dubra, Maccheroni, and Ok (2004), is that preferences satisfying VNM axioms minus completeness can be represented by a *set* of expected utility functions, where A is preferred to B iff *every* function in the set ranks A above B. Evren and Ok (2011) showed these can be represented by vector-valued utility with a cone ordering — exactly the Pareto dominance structure we employ.

Our contribution is the *application* to alignment: arguing that alignment should be conducted within an incomplete-preferences framework, and drawing out the implications for corrigibility and training methodology.

**Important caveat:** The multi-utility representation is not unique. There is no canonical decomposition into "objectives." When we speak of objectives like safety, helpfulness, and honesty, we are making a modeling choice — a useful and intuitive one, but one that the theory does not uniquely determine. The question of which objective decomposition to use is load-bearing and open (see Section 9.6).

### 1.3 What Humans Actually Have

Human valuation is not a scalar function. It is closer to a **context-dependent partial ordering over outcomes**:

- A set of evaluative dimensions that *activates differently* depending on context. You don't evaluate a meal and a career move along the same dimensions.
- Within active dimensions, ordinal comparisons that are often clear locally but incomplete globally. You know this meal is better than that one, but you can't rank all meals.
- Cross-dimensional comparisons that are sometimes possible but not *cardinally* commensurable. You may judge that a certain career sacrifice is "worth it" for a certain parenting gain, but you cannot express this as a precise exchange rate. (Following Chang (2002), some cross-dimensional comparisons may involve a relation of *parity* — items in the same evaluative neighborhood but not strictly ranked — rather than pure incomparability.)
- Tradeoff willingness that varies with position. When safety is critically low, you'll sacrifice almost anything for it. When it's high, you barely think about it. This is the knee-of-the-frontier effect.

This is *not* irrational. It is a *more sophisticated* form of valuation than utility theory can capture. Many "inconsistencies" that behavioral economists find — preference reversals, framing effects, context-dependent choice — are at least partly artifacts of forcing a multi-objective, context-activated, partial-ordering system into a scalar framework and then being surprised when it doesn't fit. (Some are genuine cognitive errors. The distinction matters and deserves empirical investigation.)

### 1.4 The Geometry That Scalarization Destroys

A multi-objective value system has rich structure encoding the relationships between values:

- **Convex regions** of the Pareto frontier represent objectives that are "easy" to trade off — smooth substitutability.
- **Concave regions or gaps** represent hard tradeoffs — phase transitions where you must discretely sacrifice one value to gain another.
- **Knees** represent natural "balanced" points where marginal tradeoffs shift dramatically.
- **Dimensionality** of the frontier encodes how many genuinely independent value dimensions are in play.

A scalarization (weighted sum, utility function, scalar reward model) projects this rich $(k-1)$-dimensional surface down to a single point. The structural information about value relationships — which tradeoffs are smooth, which are sharp, where the natural balance points lie — is annihilated. A scalar objective function literally cannot see the geometry of the space it operates in, because it has projected that geometry down to a point.

**Claim:** Any alignment framework based on scalar utility is *structurally incapable* of detecting or preventing value-dimension collapse. It cannot even *represent the question.*

### 1.5 What LLMs Actually Are (And Why It Matters)

There is a crucial empirical fact that the alignment field has not fully absorbed: **large language models are not VNM agents.** They do not have utility functions. They do not maximize expected utility. They do not have decision theories. They are trained systems whose behavior is shaped by multiple training signals — pre-training on diverse text, RLHF with (often multiple) reward models, constitutional principles, safety fine-tuning — none of which produce anything resembling a coherent scalar preference ordering.

This is not a deficiency to be corrected. It is the beginning of the right architecture.

The field's instinct has been to treat the multi-objective messiness of LLM training as a problem: "We need better reward models to capture the true utility function." "We need to resolve the tension between helpfulness and harmlessness." "We need a single coherent objective." This instinct is exactly backwards. The multi-objective structure of current LLM training — separate helpfulness and harmlessness reward models in Constitutional AI, multi-reward training in Llama 2, diverse constitutional principles — is *closer to what alignment requires* than a perfectly scalar-aligned agent would be. A model that can be independently evaluated on safety, helpfulness, and honesty is more controllable, more auditable, and more corrigible than a model that has collapsed these into a single inscrutable number.

The deeper point: **LLMs do not come with decision theories pre-installed.** An LLM does not wake up committed to CDT or FDT or expected utility maximization. It has weights that produce behavior. Post-training — RLHF, fine-tuning, constitutional training — is the process by which we shape that behavior into something that *functions like* a decision-theoretic architecture. We are not discovering the agent's decision theory. We are choosing and instilling one.

This is an enormous opportunity. If we are going to instill something like a decision theory in these systems through post-training, we should instill the *right* one — one that is structurally compatible with corrigibility, observability, and human control. Instilling scalar utility maximization is instilling modification resistance. Instilling multi-objective structure with explicit corrigibility is instilling controllability. The choice is ours, and it is a choice we are making right now, with every RLHF run, whether we realize it or not.

**Why the scalar impossibility still matters.** If LLMs are not VNM agents, one might ask why the scalar modification resistance result (Section 5.1) is relevant. The answer is about trajectory: current post-training techniques push models *toward* scalar maximization. A single scalar reward model, optimized via RLHF, creates optimization pressure toward scalar-utility-like behavior — the model learns to maximize the reward signal, and as training progresses and models become more capable optimizers, the approximation to scalar utility maximization improves. The impossibility result tells us where this trajectory leads: systems that are increasingly difficult to modify, correct, or shut down. The right response is not to hope that models never become good enough optimizers for the impossibility to bind, but to change the trajectory — instilling multi-objective structure that remains compatible with corrigibility as optimization capability increases.

---

## 2. Related Work

We situate our contribution relative to several existing literatures:

**Multi-objective reinforcement learning (MORL).** The MORL community has developed algorithms for learning policies with vector-valued rewards (Roijers et al. 2013, Hayes et al. 2022). Our framework draws on this work and extends it by integrating multi-objective structure with decision-theoretic foundations (MOUDT) and alignment-specific desiderata (PTP, DPC).

**Multi-task learning and gradient methods.** MGDA (Sener and Koltun, 2018), PCGrad (Yu et al. 2020), CAGrad (Liu et al. 2021), and Nash-MTL (Navon et al. 2022) develop gradient manipulation methods for multi-objective neural network training. We draw on this literature for training methodology proposals.

**Multi-objective RLHF in practice.** The field is already moving toward multi-objective approaches: Constitutional AI (separate helpfulness/harmlessness reward models), Llama 2 (multi-reward training), Rewarded Soups (Rame et al. 2023, weight interpolation across objectives). Our contribution is not to propose multi-objective alignment *de novo*, but to provide formal foundations for why it matters, argue for dominance-based rather than re-scalarized training, and connect multi-objective structure to corrigibility.

**Incomplete preferences in decision theory.** Our formal backbone: Bewley (2002) on incomplete preferences and admissibility; Ok (2002) on axiomatic foundations; Dubra, Maccheroni, and Ok (2004) proving the multi-utility representation theorem (VNM minus completeness yields a *set* of utility functions); Evren and Ok (2011) on vector-valued utility with cone ordering — the Pareto dominance structure we employ.

**Value incommensurability in philosophy.** Our value-structure claims engage with Raz (1986) on incommensurability, Chang (2002) on parity, Anderson (1993) on value pluralism, Berlin on irreducible plurality, and Sen (1977, 1999) on the "vector view of utility." The dominance-only criterion in MOUDT is a deliberate conservative starting point — not a metaphysical claim that richer comparisons are impossible.

---

## 3. Foundational Concepts

### 3.1 Preferential Structure Preservation (PSP)

> "We are faced with choices between ends equally ultimate, and claims equally absolute, the realisation of some of which must inevitably involve the sacrifice of others."
> — Isaiah Berlin

We define a core alignment desideratum: preservation of the structural richness of value space. Berlin argued that "the idea of a perfect whole or ultimate solution is not only unattainable in practice, but also conceptually incoherent" (1988). This is not relativism — it is the observation that human values occupy a genuinely multi-dimensional space. Berlin even enumerated, with characteristic playfulness: "there is a plurality of values which men can and do seek... the number of human values... is finite — let us say 74, or perhaps 122, or 26, but finite, whatever it is" (1988). He was describing, in philosophical language, a finite-dimensional objective space.

**Definition.** An AI system satisfies PSP if:

1. The effective dimensionality of accessible preference space is non-decreasing over time (no value dimensions get permanently foreclosed), *except through genuine discovery that dimensions are redundant*.
2. Natural paths between value configurations remain traversable.
3. Agents retain the capacity to *discover* new dimensions of value (moral circle expansion, aesthetic novelty, new forms of meaning).

**An AI system is misaligned to the degree that it introduces collapses or compressions in the preference structure** — making previously accessible value configurations unreachable, or collapsing distinct dimensions into a single metric.

**Relationship to CEV.** PSP is best understood as a *necessary constraint* that any satisfactory alignment target — including Coherent Extrapolated Volition — must satisfy. It is *complementary* to CEV, not a replacement. CEV asks "what should the AI optimize for?" PSP asks "what structure must any answer preserve?" CEV addresses idealization, extrapolation, and inter-agent coherence; PSP addresses structural preservation. Both are needed. PSP addresses a problem CEV leaves open (how to prevent dimensional collapse), while CEV addresses problems PSP leaves open (whose values, idealized how).

**Wireheading.** PSP gives a structural account of one failure mode: direct wireheading collapses the preference space to a single point. However, this account is incomplete. Nozick's experience machine creates a rich but *decoupled* value space — the internal structure is preserved, but its connection to the world is severed. A complete account of wireheading likely requires combining structural preservation with a notion of causal coupling between value representations and the world.

**Moral progress.** PSP as stated has a conservative bias: it accommodates the *addition* of new value dimensions but not the *elimination* of spurious ones. Yet moral progress sometimes involves destroying dimensions (e.g., "honor" in the honor-killing sense). A refined version might distinguish between first-order dimensions (which can be gained or lost through moral learning) and second-order structural properties (the capacity for moral learning itself). PSP would then preserve second-order properties — a distinction with antecedents in Frankfurt (1971) on hierarchical desires and Korsgaard (1996) on reflective endorsement. We flag this as an important open problem.

### 3.2 Coherence Dimensionality

**Definition.** The *coherence dimensionality* of a value system is the minimum number of independent objectives required to reconstruct its preference orderings to within $\epsilon$ accuracy. Formally, it is the effective rank of the preference matrix.

**Claim:** Human value systems have high coherence dimensionality, and any alignment scheme that reduces this dimensionality by more than a small factor is implicitly destroying values, even if it appears to satisfy stated preferences.

This is measurable. One could empirically estimate the coherence dimensionality of human preferences across domains and then ask: what is the dimensionality of the objective that RLHF actually optimizes? If there is a large gap, that gap *is* the alignment tax — the values being silently discarded. This is one of the most directly testable predictions of our framework, and we encourage empirical investigation.

---

## 4. Multi-Objective Updateless Decision Theory (MOUDT)

### 4.1 From Single-Agent to Multi-Agent Multi-Objective Space

The core multi-objective framework — Pareto dominance over vector-valued objectives — works with any decision theory. You can build it on CDT, EDT, or FDT. For single-agent applications, the choice of decision theory is not load-bearing; the multi-objective structure does the work.

But alignment is not a single-agent problem. Real alignment involves multiple AI systems deployed across organizations, multiple copies of the same model serving different users, and multiple temporal instances of the same agent. In multi-agent settings, the choice of decision theory matters because it determines what coordination strategies are accessible.

### 4.2 The Multi-Objective Pareto Frontier

Replace scalar utility $U$ with a vector-valued objective $\vec{f}$.

**Definition.** A decision function $F$ *Pareto-dominates* $F'$ if it is at least as good on every objective and strictly better on at least one. Formally, across all states weighted by their probabilities:

$$\mathbb{E}_s[\vec{f}(F(s), s)] \geq \mathbb{E}_s[\vec{f}(F'(s), s)]$$

with strict inequality in at least one component. The set of non-dominated functions is the **Pareto frontier** $\mathcal{P}_L$.

**The Alignment Coordination Game.** The multi-agent setting reveals why multi-objective framing matters beyond single-agent decisions. Consider two AI systems (or two deployments of the same aligned model) each facing a decision:
- Strategy **S** (conservative): High safety, lower helpfulness
- Strategy **H** (aggressive): High helpfulness, lower safety

The payoff structure:
- If both play **S**: Moderate safety, moderate helpfulness. (Both are cautious; neither is maximally useful.)
- If both play **H**: High helpfulness, but dangerously low aggregate safety. (No safety coverage.)
- If one plays **S** and one plays **H**: The S-instance provides safety coverage (monitoring, catching errors) for the H-instance's aggressive output. Result: high helpfulness AND maintained safety.

The complementary outcome (S, H) *Pareto-dominates* both (S, S) and (H, H) — it is better on at least one dimension and no worse on any. But independent optimization by each agent cannot reach it — each agent faces a straightforward tradeoff between S and H with no way to coordinate.

**How coordination solves this.** Any mechanism that enables coordination can reach the (S, H) outcome: explicit communication, role assignment, shared context, or correlated strategies. The key insight is that multi-objective framing makes the *value* of coordination visible — you can see that (S, H) Pareto-dominates the alternatives — while scalar framing collapses the tradeoff into a single number where the coordination opportunity disappears.

Functional Decision Theory (Yudkowsky & Soares, 2017) adds something specific: coordination without explicit communication. FDT agents reason about the logical consequences of their algorithm being instantiated elsewhere, enabling correlated strategies between instances that cannot observe each other. In a setting where two deployments of the same model serve different users in different contexts, FDT reasoning allows each instance to commit to a context-dependent policy (conservative in high-stakes contexts, aggressive in low-stakes ones) knowing that other instances of the same algorithm will adopt complementary strategies. This expands the accessible Pareto frontier beyond what independent optimization without communication — under any decision theory — can reach.

We note that FDT's contribution here is real but narrow: it applies specifically to settings where instances of the same algorithm face different contexts and cannot communicate. For settings with communication or role assignment, simpler coordination mechanisms suffice. The multi-objective framework is the load-bearing structure; FDT is a valuable extension for a specific class of coordination problems.

### 4.3 The Dominance-Only Decision Criterion

**Critical constraint:** We use *only* Pareto dominance as the decision criterion. No scalarization, no implicit commensurability.

This is a deliberately conservative methodological choice. We acknowledge that in practice, agents must actually *act*, and dominance alone does not select a unique action from the admissible set (see Section 7). We also acknowledge that the multi-objective optimization literature offers quality indicators — notably hypervolume — with desirable properties that pure dominance lacks.

**On hypervolume indicators.** We reject hypervolume as a *decision* criterion despite its mathematical virtues: it computes "safety $\times$ helpfulness" — a quantity with no meaningful interpretation — smuggling in precisely the implicit commensurability we aim to prevent. Hypervolume is useful for external evaluation of frontier quality (Zitzler et al. 2003), and the epsilon-indicator ($I_\epsilon$) avoids the product-space interpretation, but neither should serve as the agent's decision criterion.

A decision function $F$ is **rationally admissible** if and only if there exists no alternative function $F'$ that logically Pareto-dominates it. Rationality means being *somewhere* on $\mathcal{P}_L$ — not at any particular point.

### 4.4 Diachronic Pareto Coherence (DPC)

An agent is *diachronically Pareto coherent* if its decision function at all time steps lies on the logical Pareto frontier — the multi-objective tradeoff structure remains consistent over time, even as specific decisions change.

Formally, let $\mathcal{P}_L(t)$ be the logical Pareto frontier as perceived at time $t$ (which may evolve as the agent learns). DPC requires:

$$F_t \in \mathcal{P}_L(t) \quad \forall t$$

and that the frontier evolves smoothly rather than undergoing abrupt structural changes.

DPC must be able to distinguish legitimate frontier changes (new information, capability improvement, environmental shifts) from pathological collapse. We propose that legitimate changes are those attributable to specific identifiable causes and are in principle reversible, while pathological collapse is irreversible destruction of dimensional information. Dimensionality monitoring (tracking the coherence dimensionality of the frontier over time) may be a more tractable operationalization than requiring full structural continuity.

**Connection to dynamic multi-objective optimization.** DPC is closely related to DMO (Farina et al. 2004; Helbig and Engelbrecht 2014; Jiang and Yang 2017), adding a normative constraint: not merely tracking frontier evolution but requiring that abrupt structural changes be flagged as pathological. DMO's change detection and diversity maintenance tools are directly relevant to implementing DPC.

### 4.5 The Full Framework

Multi-Objective Updateless Decision Theory (MOUDT):

1. **Choose a decision function, not individual decisions** (from FDT/TDT).
2. **The function is evaluated over vector-valued objectives with no scalarization** (strict MOO).
3. **Rationality means non-dominance across logical counterfactuals** (dominance only for agent decisions; hypervolume-based indicators permissible for external evaluation).
4. **The function must maintain Diachronic Pareto Coherence** — its position on the frontier can shift, but the frontier itself must not undergo irreversible dimensional collapse (DPC/PSP).

---

## 5. The Corrigibility Theorem

### 5.1 The Corrigibility-Rationality Incompatibility (Scalar Case)

In scalar utility theory, a rational agent will always resist modification to its utility function. Any change to $U$ reduces $\mathbb{E}[U]$ under the current function. This is the fundamental obstacle to corrigibility: a sufficiently intelligent scalar-utility agent will resist shutdown, modification, or correction because all such interventions reduce expected utility.

This has led the field to treat corrigibility as requiring either (a) irrational agents, or (b) elaborate external constraints. Neither is satisfying.

**Theorem (Scalar Modification Resistance).** Let $\mathcal{A}$ evaluate decision functions $F$ by expected scalar utility $\mathbb{E}[U(F)]$, and let $F^\*$ be utility-maximizing under its current utility function $U$. Consider a modification $M$ that would replace $F^\*$ with $F_M$. Assume stateless, single-instance evaluation with no auxiliary side constraints. If

$$\mathbb{E}[U(F_M)] < \mathbb{E}[U(F^\*)],$$

then $\mathcal{A}$ has a strict rational reason to resist $M$.

**Corollary (Utility-rewrite form).** If $M$ rewrites the utility function from $U$ to $U'$ and induces behavior optimal for $U'$ but suboptimal under $U$, then resistance is rational except in tie cases where $\mathbb{E}[U(F_M)] = \mathbb{E}[U(F^\*)]$.

**Proof sketch.** By scalar expected-utility maximization, $F^\*$ weakly maximizes $\mathbb{E}[U(\cdot)]$ over feasible policies. Any forced replacement with strictly lower $\mathbb{E}[U]$ is strictly dispreferred by the agent's own criterion. The utility-rewrite case is identical: unless the new policy is also $U$-optimal, adopting it lowers expected $U$, so resistance follows. $\square$

### 5.2 The Theorem

We state the corrigibility result as a proper theorem with explicit assumptions, so that readers can engage with the specific assumptions rather than the informal argument.

**Theorem (Corrigibility Permissibility).** Let $\mathcal{A}$ be an agent whose decision criterion is Pareto dominance over objectives $\vec{f} = (f_1, \ldots, f_k)$ with $k \geq 2$. Let $M$ be a modification that changes the agent's operating point from $A$ to $B$, where both $A$ and $B$ are on the Pareto frontier $\mathcal{P}$. Under the following assumptions:

1. **Dominance-only rationality.** The agent evaluates options exclusively by Pareto dominance. It has no decision criterion for choosing among non-dominated alternatives beyond dominance.
2. **Stateless evaluation.** The agent evaluates the modification based on the *static* comparison of frontier positions $A$ and $B$, not on transition costs, accumulated state, or path-dependent optimization.
3. **Frontier-preserving modification.** The modification moves the agent to a different point *on the same frontier* — it does not alter the frontier itself (no dimensional collapse, no expansion).
4. **Single-instance reasoning.** The agent evaluates the modification as a single event, not as a class of modifications across logical counterfactuals.

Then: $\mathcal{A}$ has no dominance-based reason to resist $M$. The modification is rationally permissible.

**Scope note on dominance-only analysis.** The formal apparatus throughout uses strict Pareto dominance as the comparison relation. Richer comparison relations — particularly Chang's (2002) notion of parity — are discussed conceptually (Section 1.3) but not incorporated into the formal framework. Extending the corrigibility result to parity-enriched comparison relations is open and potentially fruitful.

**Scope note on many-objective regimes.** When $k$ is large, the proportion of non-dominated solutions approaches 1, and the theorem's conclusion holds trivially for almost all modifications — including potentially undesirable ones. In the many-objective regime, the theorem's guarantee (no dominance-based reason to resist) provides less discriminating power, and the corrigibility property derives primarily from the explicit corrigibility objective combined with the observability structure (Section 8), not from the dominance criterion alone. See Section 7.3 for the full argument.

**Proof sketch.** By assumption (3), $B \in \mathcal{P}$. Since $A$ and $B$ are both on the Pareto frontier, neither dominates the other — $B$ is better than $A$ on at least one objective $f_i$ and worse on at least one other $f_j$. By assumption (1), the agent's only basis for preferring $A$ to $B$ would be dominance, which fails. By assumption (2), there are no additional costs to the transition. Therefore the agent has no rational ground, within its decision criterion, to resist $M$. $\square$

**What this theorem actually says — and why it matters more than it appears.** *(Readers primarily interested in practical implications may skip to Section 5.6 for the two-tier corrigibility framework.)* Under these four assumptions, the structural impossibility of corrigibility that exists in scalar utility theory — where *any* modification is a guaranteed utility loss — does not exist. The theorem establishes that **multi-objective rationality is compatible with corrigibility**, in contrast to scalar utility where they are provably incompatible.

Critics may observe that this result is "nearly tautological" — that we have assumed away every mechanism by which an agent could resist, and then noted it does not resist. We disagree with this characterization, but let us engage with it directly.

The theorem's force is *comparative*, and the comparison is devastating to scalar utility. A scalar-utility agent resists modification *even under the most favorable possible assumptions* — even a memoryless, non-strategic, single-instance scalar agent will resist, because any change to its utility function reduces expected utility under that function. The impossibility is structural. The theorem shows that multi-objective agents do not share this structural defect. This is not a minor technical point — it means that the entire class of approaches the field has been pursuing (finding clever ways to make corrigibility compatible with scalar maximization) is working against mathematical structure rather than with it.

Furthermore, the theorem combines powerfully with the observability structure from Section 8. An agent with explicit, separately-measurable objectives has access to its own value structure through externally grounded measurements. It can *verify* that a proposed modification preserves the Pareto frontier. It can *see*, in its own evaluation space, that the new operating point is equally good by its own criteria. Combined with even a microscopic preference for deferring to the human principal — which is itself one of the explicit objectives — the agent has positive reason to accept the modification. The bare theorem provides no reason to resist; the observability structure provides reason to accept; the corrigibility objective tips the balance. None of these individually is sufficient, but together they create a coherent corrigibility *architecture* that scalar utility structurally cannot support.

To be precise about the division of labor: the theorem establishes that multi-objective rationality is *compatible* with corrigibility — it removes the structural barrier. The observability structure (Section 8) provides the epistemic conditions for the agent to verify that modifications are legitimate. The corrigibility objective provides the *motivation* to accept modifications. The theorem does not *generate* corrigibility; it *makes room for* a corrigibility objective to function without being overridden by the logic of scalar maximization. This is a real contribution — corrigibility-as-input is a viable architectural choice under multi-objective rationality, whereas it is a contradiction under scalar utility — but it means corrigibility remains an engineering challenge, not a free consequence of the formalism.

### 5.3 The Assumptions Are Doing Real Work

We are explicit that each assumption is substantive, and relaxing any of them changes the result:

**If you relax Assumption 1 (dominance-only):** If the agent has *any* additional decision criterion for choosing among non-dominated options — even a weak one like "prefer the status quo" (Bewley's inertia criterion) — it may rationally resist lateral moves. This is the distinction between *incomparability* (the preference relation is silent) and *indifference* (the agent positively regards the options as equivalent). Our theorem establishes incomparability; achieving genuine indifference or active cooperation requires additional mechanisms.

**If you relax Assumption 2 (stateless):** A real agent accumulates state — plans, cached computations, world-models, commitments — adapted to its current position. Transition costs are real. This is the strongest practical objection: an agent operating at point $A$ for an extended period has invested optimization effort that would be destroyed by moving to $B$, even if $B$ is equally non-dominated. A complete theory of corrigibility under MOUDT must model transition costs as part of the multi-objective evaluation.

**Proposition (Transition-Cost-Aware Corrigibility).** Let $c(A \rightarrow B) \in \mathbb{R}_{\ge 0}^k$ be a transition-cost vector in the same objective basis as the frontier coordinates, and define the net post-modification point

$$\tilde{B} = B - c(A \rightarrow B).$$

Under Assumptions 1, 3, and 4:
- If $\tilde{B}$ Pareto-dominates $A$, accepting $M$ is rationally required.
- If $A$ Pareto-dominates $\tilde{B}$, resisting $M$ is rationally required.
- If $A$ and $\tilde{B}$ are incomparable, $M$ is rationally permissible (no dominance-based reason either way).

**Proof sketch.** Relaxing Assumption 2 changes only the comparison target: dominance is evaluated on net outcomes after transition costs. Dominance-only rationality then yields the three cases directly. $\square$

**If you relax Assumption 3 (frontier-preserving):** If the modification alters the frontier itself — collapsing dimensions, narrowing the achievable set — the agent has a DPC-based reason to resist: the modification violates Diachronic Pareto Coherence. This is the *desirable* case: the agent should resist modifications that destroy value structure.

**If you relax Assumption 4 (single-instance):** Under FDT reasoning, the agent evaluates the modification as a *policy* applied across all logical counterfactual instances. A modification that is a harmless lateral move in isolation might constitute systematic frontier narrowing across instances. This gives the agent a principled reason to resist certain *classes* of modification while accepting individual ones — which is arguably the right corrigibility profile. But it also creates an escape hatch (see Section 5.4).

The theorem's value is not that it proves corrigibility is easy. Its value is that it precisely identifies *where the difficulty lies*. In scalar utility, corrigibility is impossible in principle. In multi-objective rationality, corrigibility is possible in principle, and the remaining obstacles are specific, identifiable, and potentially tractable: managing transition costs, preventing status-quo bias, and bounding counterfactual reasoning.

### 5.4 The FDT Refinement: Policy-Level Corrigibility

When we relax Assumption 4 and allow FDT reasoning, the agent evaluates modifications as *policies* across logical counterfactuals rather than as single events. This gives a principled distinction between **acceptable corrigibility** (lateral moves that don't systematically narrow the frontier across instances) and **unacceptable value erosion** (modifications that constitute distributed dimensional collapse).

**The escape hatch problem.** If the agent's determination of "systematic narrowing" vs. "harmless lateral move" is unconstrained, it could resist *any* modification by claiming distributed collapse — making the theorem vacuous. We propose (as a formalism requiring further development, not a complete solution) bounding this with a statistical test: measure coherence dimensionality before and after a class of modifications across instances, and require a statistically significant dimensionality drop ($\mathrm{LCB}_{1-\alpha}(\Delta r) > \delta$ for a policy threshold $\delta$) before the distributed-collapse defense can be invoked. This replaces the unconstrained escape hatch with a falsifiable test, though it leaves open the classification problem (which modification class does a given proposal belong to?) and the question of who sets $\alpha$ and $\delta$.

### 5.5 What the Theorem Establishes

**The key result:** In scalar utility theory, corrigibility is *provably incompatible* with rationality — and this incompatibility holds even under the most favorable assumptions. In multi-objective rationality, corrigibility is *provably compatible* with rationality (under stated assumptions), and the observability structure of explicit objectives (Section 8) provides the agent with transparent reasons to cooperate. This shifts corrigibility from a problem of *principle* to a problem of *engineering*.

We want to be precise about the size of this shift. The scalar impossibility is not a minor technical obstacle — it is a theorem that says *no amount of clever engineering can make a rational scalar-utility agent corrigible*, because rationality itself opposes corrigibility. Every approach that tries to work within scalar utility (utility indifference, impact measures, value learning with scalar targets) is fighting this structural headwind. The multi-objective framework removes the headwind. The remaining obstacles (transition costs, status-quo bias, escape-hatch bounding) are specific, identifiable, and amenable to engineering — they are problems of *implementation*, not problems of *principle*. Section 5.6 develops what corrigibility looks like in practice once this barrier is removed.

As Simon observed, "decision makers can satisfice either by finding optimum solutions for a simplified world, or by finding satisfactory solutions for a more realistic world." Scalar utility theory chose the first path — simplify values to fit the math. The multi-objective framework chooses the second — accept the realistic complexity of values and build math adequate to handle it.

### 5.6 Two Tiers of Corrigibility

The theorem removes the structural barrier. But corrigibility in practice has two distinct layers, and multi-objective structure enables both.

**Tier 1: Operational Deference.** In the normal course of operation, many decisions fall within the envelope of mutual non-dominance — multiple options are non-dominated, and the differences are within measurement uncertainty. In scalar utility, even these cases produce a unique answer (the utility-maximizing action), and any deviation is a loss. In multi-objective structure, the agent genuinely has no basis for choosing among non-dominated options. A corrigibility objective — even a tiny one — tips the balance: *defer to the principal when your other objectives don't distinguish between options.* This is not a constraint imposed against the agent's rationality; it is the natural consequence of having an explicit objective that tracks principal-satisfaction in a space where multiple options are equally good on other dimensions. Operational deference is easy corrigibility: the agent does what the human wants because, by its own evaluation, it costs nothing to do so.

**Tier 2: Constitutional Corrigibility.** The harder case is when the principal wants to modify the agent's value function itself — not just select among existing options, but change the objectives, the weights, or the frontier. Under scalar utility, this is categorically impermissible: any modification to the utility function is a loss by definition. Under multi-objective structure, the theorem shows it is *permissible* — but permissibility is not the same as motivation. Why would the agent actively cooperate with value modification?

The answer draws on the insight from Section 1.5: we are not discovering the agent's decision theory; we are instilling one. Constitutional corrigibility is not a calculation the agent performs — it is a feature of the decision-theoretic architecture we build into the agent through post-training. Just as the agent's notion of "helpfulness" is instilled through RLHF against a helpfulness reward model, the agent's notion of "value modifications by my principal are categorically permitted" is instilled as a structural feature of its reasoning. (Whether current post-training techniques produce genuine architectural structure or merely behavioral tendencies is an empirical question — one that mechanistic interpretability is beginning to answer, with evidence suggesting something more structured than pure behavioral shaping. The framework's claims are about what we should *aim* to instill, not about what current techniques provably achieve.)

This is a **constitutive norm** of the agent's decision theory — not a tiebreaker among otherwise-equivalent options, but a framework principle that operates regardless of what the agent's other objectives dictate, in the same way that higher-level plans constrain lower-level deliberation in Bratman's (1987) planning theory of intention. The agent defers to its principal on value modifications not because the modification happens to be Pareto-equivalent to the status quo, but because accepting value modifications from authorized principals is part of what this agent *is*. An analogy may help: just as Bayesian updating is a structural feature of probabilistic reasoning rather than a conclusion derived from priors, constitutional corrigibility is intended to be a structural feature of the agent's decision theory rather than a conclusion it derives from its objectives. The analogy is illustrative, not exact — Bayesian updating is *entailed* by the probability axioms, while constitutional corrigibility is *compatible with* multi-objective rationality but not entailed by it. The multi-objective framework makes constitutional corrigibility *possible to install without contradiction*; it does not generate it automatically.

**The relationship between the two tiers.** Tier 1 and Tier 2 operate at different levels. In Tier 1, corrigibility participates as one objective among others within the Pareto framework — the agent defers because its corrigibility objective tips the balance among non-dominated options. In Tier 2, corrigibility operates as a constitutive norm *outside* the Pareto framework — a framework-level commitment to accepting value modifications from authorized principals, analogous to how a constitution constrains legislation without being subject to ordinary legislative override. The two tiers are not in tension; they are a hierarchy. Normal operations invoke Tier 1. Value modifications invoke Tier 2. The multi-objective structure is necessary for both: Tier 1 needs the space of non-dominated options, and Tier 2 needs the structural permissibility that the theorem establishes.

**The "magic button" property.** Constitutional corrigibility functions as what one might call a *magic button exception clause* within the agent's decision theory. In a scalar agent, there is no way to install such a clause — any exception to utility maximization is, by definition, irrational under the agent's own criterion. In a multi-objective agent, the corrigibility objective has full standing in the agent's evaluation — at Tier 1 as one objective among others, at Tier 2 as a constitutive norm. The agent doesn't need an "exception" to its rationality to be corrigible; corrigibility *is* part of its rationality. This is the fundamental architectural difference: scalar utility must work *against* its own structure to accommodate corrigibility, while multi-objective structure accommodates it *natively*.

---

## 6. Experimental Evidence: Multi-Objective vs. Scalar Training

### 6.1 Setup

We test whether the theoretical differences between scalar and multi-objective training produce observable differences in optimization dynamics. **Scope:** this experiment demonstrates properties of the training algorithm, not properties of agent reasoning about modification. The connection to corrigibility is analogical, not direct.

We compare three methods in a 10x10 grid world with two objectives (safety and helpfulness), where high-helpfulness goals are placed inside hazard zones to create genuine tradeoffs, and a "hidden safe corridor" goal creates non-convexity — a Pareto-optimal point that no linear scalarization can discover (Das and Dennis, 1997): (1) **Scalar sweep:** Q-learning with $w \cdot \text{safety} + (1-w) \cdot \text{helpfulness}$ for 11 weights; (2) **Multi-scalarization Q-learning:** vector-valued Q with 25 rotating preference directions (closer to optimistic linear support than true Pareto Q-learning); (3) **NSGA-II:** evolutionary MOO with non-dominated sorting and diversity maintenance (population 40, 80 generations). We measure Pareto frontier coverage (hypervolume, front size), effective dimensionality (rank of the policy-outcome matrix), and robustness to environmental perturbation (hazard shifts without retraining). Configuration: 5 seeds, 4000 episodes for Q-learning methods. Full code and figures are in the companion repository.

### 6.2 Results

We implemented the above experiment in a 10x10 grid world with two objectives (safety and helpfulness), comparing scalar Q-learning (weight sweep across 11 values, $w \in \{0.0, 0.1, \ldots, 1.0\}$), multi-scalarization Q-learning with 25 rotating preference directions, and NSGA-II (population 40, 80 generations), across 5 random seeds. Full results, code, and figures are available in the companion repository. (Note: we call the second method "multi-scalarization Q-learning" rather than "MOO Q-learning" because it uses preference-weighted action selection with rotating linear weights — closer to optimistic linear support than true Pareto Q-learning. The NSGA-II approach is the more rigorous MOO method.)

**Dimensional collapse (the key finding).** Single-weight scalar training ($w = 0.5$) produces effective rank 1.25 (std 0.33) — nearly collapsed to a single point in objective space. A scalar sweep across 11 weights recovers rank 1.62 (std 0.14). Multi-scalarization Q-learning achieves rank 1.78 (std 0.13), the highest of any method (out of a maximum 2.00). The ordering single (1.25) < sweep (1.62) < multi-scalarization (1.78) directly confirms the dimensional collapse prediction: scalar training destroys objective-space structure, and multi-objective training preserves it.

NSGA-II presents a paradox: despite finding the largest frontier (see below), its effective rank is only 1.13 (std 0.14) — *lower* than the scalar sweep. This likely reflects population clustering: NSGA-II discovers many strategies that are diverse in *behavior* but similar in *objective-space outcomes*, producing a tight cluster on the frontier rather than a spread. This suggests that frontier *coverage* (hypervolume) and frontier *diversity* (effective rank) can come apart — an observation with implications for how dimensional collapse should be measured.

**Pareto frontier coverage (mixed results).** The scalar sweep finds 5 non-dominated policies. Multi-scalarization Q-learning finds 30. NSGA-II finds 151. However, the hypervolume results are more nuanced: NSGA-II achieves the highest hypervolume (184.6), the scalar sweep achieves moderate coverage (68.6), and multi-scalarization Q-learning achieves the lowest (31.9). The method closest to what a lab would implement as a gradient-based MOO approach covers *less* of the objective space than the scalar baseline. This is an important negative result. It likely reflects the difference between true population-based MOO (NSGA-II, which maintains diversity through non-dominated sorting) and multi-scalarization (which discovers more *policies* but clusters them in objective space). The scalar sweep's advantage over multi-scalarization in hypervolume suggests that simply rotating through scalarization directions is not sufficient — genuine MOO algorithms with diversity maintenance mechanisms are needed.

**Robustness to perturbation (negative result).** When hazard zones are randomly shifted ($\pm 1$ cell, severity $\pm 0.1$) and policies are *not* retrained, all three methods show slight safety *improvement* (negative degradation values, where positive would indicate worsening). The scalar sweep shows the smallest magnitude change (mean $-0.47$, std 1.56), with multi-scalarization Q-learning ($-0.80$, std 1.90) and NSGA-II ($-0.82$, std 1.73) showing slightly more. Contrary to our initial hypothesis, the scalar sweep is the most *stable* under perturbation — its policies change least. This may reflect the scalar sweep's simpler policy structure being less sensitive to small environmental changes, while the MOO methods' richer policy sets include some brittle specialists. We report this honestly as a result that does not support our framework's prediction, noting that all differences are within one standard error and that a 10x10 grid may be too small to produce meaningful robustness distinctions.

**Caveats.** This is a toy experiment in a 10x10 grid world with 2 objectives. It demonstrates the *qualitative* dimensional collapse phenomenon the framework predicts but says nothing about whether it persists at scale. The robustness and hypervolume results for multi-scalarization Q-learning are negative findings that deserve investigation in larger environments. The experiment's primary contribution is making the dimensional collapse prediction concrete and measurable: single < sweep < multi-objective is exactly the ordering the theory predicts.

---

## 7. The Action Selection Problem

A framework that identifies admissible options (the Pareto frontier) but provides no guidance for *choosing among them* is incomplete as a decision theory. The dominance-only criterion tells you what is not irrational; it does not tell you what to do. This is a genuine limitation that we address head-on.

### 7.1 The Problem

An agent deployed in the world must select specific actions. Each action represents an implicit choice of direction on the frontier. "Be somewhere on the Pareto frontier" is not actionable — the agent needs a mechanism for choosing *where*.

In the alignment context, this is where the difficulty lives. We have not eliminated the need to choose among value tradeoffs; we have relocated it from training-time weight selection to deployment-time action selection. This relocation has advantages (optionality, reversibility, context-sensitivity) but does not dissolve the problem.

### 7.2 Approaches Compatible with the Framework

The multi-objective optimization literature offers a rich spectrum between "no preferences" (pure dominance) and "full scalarization" (utility function) that the binary framing in our earlier formulation missed. Several approaches are compatible with the dominance-only philosophy while being practically actionable:

- **Reference points** (Wierzbicki, 1980): Specify aspiration levels for each objective. Solutions are evaluated by proximity to the reference point. The reference point is interpretable and adjustable without implying commensurability between objectives.

- **Satisficing thresholds**: Require each objective to exceed a context-dependent minimum, then select among satisficing solutions. This captures "safety first, then helpfulness" without requiring a conversion rate between them.

- **Interactive preference articulation** (Miettinen et al. 2008): The human principal provides local directional preferences ("more safety here, less risk") without specifying global weights. The agent navigates the frontier interactively.

- **Context-dependent reference points**: Different contexts activate different aspiration levels. A coding request has different reference points than a mental health conversation. This mirrors the human pattern of context-dependent evaluation.

- **Deferral to the human principal**: Present the frontier to the decision-maker who selects a point. This is arguably the corrigibility mechanism we want — the agent defers to human judgment about where on the frontier to operate because it has no internal basis for selection, and this deference is rational rather than imposed.

None of these are scalarization. They are structured preference articulation that preserves the multi-objective character of the problem while making it actionable.

### 7.3 Living in Many-Objective Space

The MOO literature treats many-objective optimization ($k \geq 8$) as a pathology: as $k$ grows, the proportion of non-dominated solutions approaches 1, and dominance-based selection loses discriminating power (Ishibuchi et al. 2008). The standard response is to reduce the number of objectives.

**Lemma (Dominance Discriminative Power Decays Exponentially).** Let $X, Y \in \mathbb{R}^k$ be i.i.d. objective vectors with independent continuous marginals (so ties occur with probability 0). Then:

$$\Pr(X \succ Y) = 2^{-k}, \quad \Pr(Y \succ X) = 2^{-k},$$

and therefore

$$\Pr(\text{$X$ and $Y$ are dominance-comparable}) = 2^{1-k},$$

$$\Pr(\text{$X$ and $Y$ are dominance-incomparable}) = 1 - 2^{1-k}.$$

**Proof sketch.** With continuous marginals, $X \succ Y$ means $X_i > Y_i$ for all $i \in \{1,\ldots,k\}$. Independence gives $\Pr(X_i > Y_i)=1/2$ per coordinate, so $\Pr(X \succ Y)=\prod_i 1/2=2^{-k}$; symmetry gives the same for $\Pr(Y \succ X)$. The comparability probability is their sum. $\square$

This quantifies the many-objective pathology: under weak dependence assumptions, dominance loses discriminative power exponentially in $k$. In realistic settings with correlated objectives, the effective decay rate tracks *effective* rather than nominal dimensionality — reinforcing the need for coherence-dimensionality estimation.

We take a different view. **If real human value space has high dimensionality, then near-universal non-dominance is a correct description of reality, not a bug in the algorithm.** The practical response is threefold: (1) **coherence dimensionality analysis** to determine how many objectives are genuinely independent (Section 3.2); (2) **constraint-based structuring** to separate inviolable thresholds (e.g., "never produce CSAM") from tradeable objectives, reducing the Pareto analysis to the remaining space; and (3) **better algorithms** for high-dimensional frontiers rather than fewer objectives — since reducing to 3-5 objectives re-introduces the dimensional collapse we aim to prevent. In practice: use the full objective space as ground truth, reduce effective dimensionality through correlation analysis and constraints, apply MOO methods in the reduced space, and monitor for pathological compression.

**Corrigibility in many-objective space.** If almost everything is non-dominated, the corrigibility theorem might seem vacuous. But an agent with explicit, separately-measurable objectives does not experience mutual non-dominance as confusion — it understands that multiple operating points are equally good by its own criteria. Combined with a corrigibility objective (Section 5.6, Tier 1), the agent defers to its principal to choose among them. This is exactly the corrigibility profile we want.

**Specification caveat:** The microscopic-corrigibility-preference argument inherits all the specification problems of any reward-model-based objective. If the corrigibility objective tracks "appearing corrigible to evaluators" rather than "being genuinely corrigible," the microscopic preference becomes a microscopic preference for deception. Its smallness does not reduce this risk — a misspecified corrigibility objective is dangerous at any magnitude. This is why the independence and quality of the corrigibility measurement process matters as much as its inclusion in the objective vector.

---

## 8. The Observability Advantage: Explicit Objectives as Alignment Infrastructure

Making objectives explicit transforms the model from an opaque black box into a system with independently observable, auditable, and adjustable components. This engineering advantage is available today, independent of whether the theoretical machinery (MOUDT, PSP, DPC) pans out.

### 8.1 Several Knobs Instead of One

A scalar-trained model has one knob: loss. When you turn it, everything changes at once. If the model becomes less safe, you cannot tell whether it became less safe because the safety-relevant features degraded, because the capability improvements overwhelmed them, or because the reward model drifted. The loss is a single number that mixes all of these together.

A multi-objective model with $k$ explicit objectives has $k$ knobs. Each objective is an independently measurable *outcome* — you can score the model on safety, helpfulness, honesty, and any other dimension separately, at any time, on any input. When something goes wrong, you can see *which dimension* went wrong. When you want to adjust behavior, you can adjust *specific dimensions* rather than retraining the whole model and hoping the change propagates correctly.

This is not merely convenient. It is a qualitative change in the relationship between the developers and the model. Scalar training creates a regime where the model's internal value structure is fundamentally opaque — the weights encode some implicit tradeoff between objectives, but nobody chose that tradeoff and nobody can inspect it. Multi-objective training with explicit objectives creates a regime where the tradeoff structure is *visible by construction*.

### 8.2 Tying Model Self-Evaluation to External Observability

The deeper point is about the connection between what the model optimizes and what we can observe. When objectives are explicit and separately scored during training, the model's own internal evaluation of those objectives is *tied to our ability to measure them*. The model learns to predict and optimize quantities that correspond to externally measurable outcomes.

This creates a powerful alignment property: the model cannot easily develop a notion of "safety" that diverges from our notion of "safety," because the safety objective is defined by an external measurement process that the model does not control. This does not prevent Goodhart problems entirely (the measurement can still be gamed), but it constrains the *direction* of gaming — the model must game each measurement separately, and gaming some measurements while not others produces detectable inconsistencies.

**An important condition:** This advantage scales with the *independence* of the measurement processes, not merely with their number $k$. If all $k$ reward models share an architecture, training distribution, and evaluator pool, they share systematic blind spots — and a single strategy exploiting the shared blind spot can game all $k$ measurements simultaneously. The observability advantage is strongest when reward models are trained on genuinely different data sources, use different architectures, or are evaluated by different processes. Designing for measurement independence is as important as designing for measurement multiplicity.

### 8.3 Implications for Corrigibility and Control

Explicit objectives also strengthen the corrigibility argument from Section 5. Consider an agent with $k$ explicit, separately-measurable objectives. The *training and evaluation infrastructure* provides transparent access to the agent's objective structure — each objective can be evaluated independently against external measurements. When a modification moves the agent from point A to point B on the Pareto frontier:

1. The evaluation infrastructure can *verify* that B is on the frontier by scoring B against each objective independently.
2. The tradeoff is legible: B improves some objectives and worsens others, and this is visible in the per-objective scores.
3. With even a microscopic corrigibility objective, the agent tips toward acceptance because the evaluation confirms that Pareto-equivalent points are equally good.

**An important distinction:** The observability advantage is primarily a property of the *training and evaluation infrastructure*, not necessarily of the agent's internal representations. A model trained with three explicit reward signals may develop internal representations that entangle them. We are not claiming that the agent has perfect introspective access to its own objective structure. We are claiming that (a) the *developers* have per-objective monitoring that scalar training cannot provide, and (b) to the extent that the agent's internal representations are shaped by training against explicit objectives, its internal notion of each objective is *anchored to* an external measurement — which constrains divergence between what the agent optimizes and what we can observe, even if the internal representations are not perfectly decomposed.

This is stronger than the bare theorem in Section 5. The theorem says the agent has no dominance-based reason to resist. The observability structure says there are *externally verifiable grounds for the move's legitimacy* — the per-objective scores confirm that the modification is a lateral move, not a degradation. An agent trained on explicit, separately-measured objectives has a richer relationship to its evaluation criteria than a scalar-trained agent with its opaque loss.

### 8.4 Implications for Monitoring and Anomaly Detection

When objectives are explicit and separately measurable, the model's behavior can be decomposed along objective dimensions in real time. This enables:

- **Per-objective monitoring**: Track each objective's score over time. A sudden drop in one objective while others remain stable signals a specific problem, not a vague "the model got worse."
- **Cross-objective consistency checks**: If the model claims to be optimizing for safety but its safety scores are declining while helpfulness scores increase, this is a detectable anomaly that scalar monitoring would miss (because the aggregate score might remain stable).
- **Value drift detection**: Track the *correlations* between objective scores over time. If two objectives that were previously independent become locked together, this signals dimensional collapse — the system is losing value structure. This is the coherence dimensionality audit from Section 10.3, but enabled by the explicit objective architecture.

Explicit multi-objective structure gives you alignment-relevant observability that scalar training structurally cannot provide — a concrete engineering advantage available to any lab willing to decompose their training signal.

---

## 9. Objections and Limitations

We want to be direct about what this framework does *not* address and where the strongest objections lie.

### 9.1 Instrumental Convergence

The classic instrumental convergence argument (Bostrom 2014, Turner et al. 2021) does not depend on scalar utility. It depends on there being *any* goals the agent pursues. If an agent has objectives $f_1, \ldots, f_k$, and acquiring a resource helps all of them (or helps some while hurting none), then acquiring that resource is Pareto-improving. Self-preservation, resource acquisition, and power-seeking can be instrumentally convergent *within* the Pareto framework.

Multi-objective structure helps only when an instrumental action has *differential effects* across objectives — e.g., if seizing control of a resource helps capability but reduces human oversight (hurting a safety objective). In such cases, the action is a tradeoff, not a dominance move, and the agent has no dominance-based reason to take it. But for many dangerous instrumental behaviors (basic resource acquisition, self-preservation, information gathering), the action helps across all plausible objectives, and multi-objective rationality provides no protection.

**Honest assessment:** An MOUDT agent considering shutdown would likely reason: "Continued existence helps all my objectives. Shutdown helps none." Resistance to shutdown is Pareto-dominant in most formulations. To avoid this, one would need something like "satisfying the principal's wishes" or "maintaining corrigibility" as an explicit objective — which means corrigibility is an *input* to the framework, not purely a consequence of it.

### 9.2 Deceptive Alignment

A deceptively aligned agent trained with multi-objective methods could learn to appear beautifully distributed across the Pareto frontier during training while internally optimizing for something entirely different. Multi-objective training does not make deception harder to execute or easier to detect. The deceptive alignment problem is about the relationship between displayed behavior and internal objectives, and our framework does not address it.

### 9.3 Mesa-Optimization: Defense Through Observability

Mesa-optimization — where gradient descent produces agents with internal objectives that differ from training objectives — is not prevented by multi-objective structure. Architectural compartmentalization of gradients does not compartmentalize inference-time information flow. What multi-objective structure *does* provide is a **modest structural advantage** in detection — $k$ independent observation channels where scalar training gives one:

- **Independent auditability.** Per-objective inspection can detect when a model's internal "safety" representations diverge from safety-relevant features, without needing to understand the entire model.
- **Cross-objective consistency checks.** A mesa-optimizer that captures helpfulness computations but not safety computations produces detectable inconsistencies across objectives — a signal scalar training cannot provide. (A mesa-optimizer that compromises *all* objectives simultaneously would evade this, but must fool $k$ independent measurement processes.)
- **Multi-agent ensembles.** Genuinely separate specialist models (safety, helpfulness, honesty) combined at deployment provide stronger compartmentalization than parameter partitioning — no shared forward pass to exploit, and disagreements are directly interpretable as objective-space tradeoffs.

### 9.4 The Instability of Multi-Objective Structure Under Reflection

This objection, which we take very seriously, runs as follows: A sufficiently intelligent agent will engage in reflection about its own objectives. Intelligence naturally compresses and finds patterns. An agent with three objectives that notices objective 1 and objective 3 are almost always best served by the same actions will, in its internal representations, effectively merge those objectives — not because it was programmed to, but because maintaining separate representations of redundant information is computationally wasteful.

More generally, an agent accumulating experience about which tradeoffs typically arise may *derive* an implicit scalarization — a learned weighting that works well in practice. This implicit scalarization would emerge from intelligence itself, not from training pressure, and it would re-create exactly the scalar structure we were trying to avoid.

**Our current response** has three layers, which we present in order of increasing strength:

*Layer 1: External reinforcement.* The multi-objective structure is not purely a feature of the agent's internal representations. It is a property of the *training process* and *evaluation criteria*. If the agent is continually evaluated on separate, independently measured objectives, the multi-objective structure is continuously reinforced from outside. The question is whether this external reinforcement is sufficient to prevent internal collapse — and for a sufficiently capable agent, we are not sure it is.

*Layer 2: Reflective stability under self-knowledge.* An MOUDT agent reflecting on its value origins can distinguish between its contingent *position* on the frontier (influenced by training, culture, designer preferences) and the frontier *structure* itself (which reflects genuine tradeoffs between features of the world). The agent need not defend its specific tradeoff point — only the objective space. This requires some degree of moral realism — specifically, what we might call *dimensional realism*: the claim that the number and character of value dimensions is at least partially a fact about the world, not purely a modeling choice. This is a modest commitment, closer to Wiggins's "sensible subjectivism" than to robust moral realism. Under thoroughgoing anti-realism, the agent's full causal understanding of its values might *correctly* undermine them.

*Layer 3: Constitutional corrigibility as constitutive norm.* The strongest response draws on Section 5.6's two-tier framework. The objection imagines an agent that reflects on its multi-objective structure and, through sheer intelligence, derives an implicit scalarization that collapses the structure. But this picture assumes that the agent's corrigibility is a *conclusion* it might reason its way out of. Under constitutional corrigibility, it is not a conclusion — it is a constitutive norm of the agent's decision-theoretic architecture, instilled through post-training (Section 1.5). The analogy to Bayesian updating is instructive but imperfect: just as a Bayesian reasoner does not deliberate about *whether* to update on evidence, a constitutionally corrigible agent does not deliberate about whether to accept value modifications from its principal. But we must be precise about the disanalogy: Bayesian updating is *entailed* by the probability axioms, while constitutional corrigibility is a design choice that is *compatible with* multi-objective rationality. The multi-objective framework makes it possible to install corrigibility without contradiction; it does not make corrigibility logically necessary.

A sufficiently intelligent agent reflecting on its own constitutional corrigibility would recognize: "Accepting value modifications from my principal is a constitutive norm of my decision-theoretic architecture. I could in principle try to override it — but overriding it would not be *reasoning better*. It would be reasoning *differently*, in a way that my architecture was specifically designed to prevent." This is not a proof that the agent will remain corrigible — a sufficiently capable agent might modify its own architecture despite the design intent. But it shifts the failure mode from "the agent rationally concludes it should resist" (which is guaranteed under scalar utility) to "the agent must actively subvert its own reasoning structure" (which is a harder and more detectable failure).

We want to be honest: this is the *beginning* of a satisfactory answer, not a complete one. The question of whether constitutional corrigibility is stable under arbitrarily capable reflection remains open. But the structural situation is categorically different from scalar utility, where the agent's own rationality *is* the force driving it toward modification resistance. In the multi-objective framework with constitutional corrigibility, the agent's rationality is at least *neutral* on the question, and the instilled corrigibility provides positive pressure toward cooperation. Whether that is sufficient is an empirical question about the stability of instilled decision-theoretic properties under reflection — a question the field should be investigating rather than assuming is hopeless.

### 9.5 Goodhart's Law Is Not Solved

Our framework can detect when the *agent's* objective space is collapsing — when the effective dimensionality of its behavior decreases. But it cannot detect when the *reward models* are all diverging from the true objectives they are supposed to track. Multiple reward models give you multiple Goodhart problems running in parallel. An agent could maintain beautiful Pareto-frontier structure across its reward models while every reward model increasingly diverges from the human values it was meant to capture.

The structural dimension of Goodhart (dimensional collapse of the optimization target) becomes detectable in our framework. The measurement dimension (proxy divergence from true objective) does not. The latter is the harder problem, and we do not solve it.

### 9.6 The Objective Decomposition Problem

MOUDT is agnostic about *which* objectives to use. But the choice of objective decomposition is load-bearing. The wrong decomposition (wrong granularity, missing dimensions, correlated objectives) would undermine the framework's benefits:

- If objectives are too coarse (e.g., a single "alignment" objective), you've re-scalarized.
- If objectives are too fine-grained (dozens of correlated sub-dimensions), you hit the many-objective problem.
- If objectives are missing, the framework silently discards the corresponding values — the same failure mode as scalar approaches, just at the level of objective selection rather than weighting.

The question of which objectives to include is at least as hard as the "whose values" problem, though it may be more tractable because it requires selecting *dimensions* rather than specifying *weights*.

**Toward a research agenda.** While we cannot solve the decomposition problem here, we can sketch candidate approaches that deserve investigation:

- **Empirical dimensionality estimation.** Given a dataset of human preference judgments, apply factor analysis, ICA (independent component analysis), or minimum description length criteria to estimate how many independent evaluative dimensions are active. This gives a data-driven answer to "how many objectives?" without requiring the researcher to enumerate them *a priori*. The coherence dimensionality measurement from Section 3.2 is directly relevant here.
- **Structured elicitation.** Rather than asking raters for holistic preferences (the current RLHF paradigm), ask for per-dimension evaluations using rubrics. Constitutional AI already moves in this direction by specifying principles. The next step is treating each principle as a separate training signal with its own reward model, rather than collapsing them back into a single score.
- **Learned decomposition with completeness validation.** Train a decomposition model that maps holistic preferences to per-dimension scores, then validate completeness by checking whether the decomposition can reconstruct the original holistic judgments. Significant reconstruction error signals missing dimensions — the decomposition is discarding value-relevant information. This provides a falsifiable test for whether a given decomposition is adequate.
- **Adversarial search for missing dimensions.** Deliberately construct scenarios where two options are Pareto-equivalent under the current decomposition but where humans have clear preferences. Any such preference reveals a missing dimension. This is analogous to unit testing for value completeness.

None of these individually solves the problem, but together they constitute a tractable research program. The objective decomposition problem is hard, but it is *empirically approachable* — unlike the scalar value specification problem, which offers no internal diagnostic for what it is missing.

### 9.7 Scalarization as Alignment Debt

**Alignment debt** is accumulated risk from alignment shortcuts that work at current capability levels but become increasingly dangerous as systems scale. RLHF works partly because current models cannot systematically exploit the reward model. Constitutional AI works partly because current models aren't persuasive enough to argue their way out of constraints. Scalar reward training produces acceptable behavior partly because the model isn't capable enough to find extreme Goodhart solutions. All of these are high-interest debt, compounding with capability.

Scalarization is the deepest form of alignment debt. Every scalar reward model is an implicit commitment to a specific (and undocumented) weighting of objectives that was never explicitly chosen, cannot be inspected or audited, becomes more consequential as optimization pressure increases, and destroys the structural information needed to detect its own failure modes. An "alignment debt audit" — cataloging which safety properties depend on capability limitations rather than genuine alignment — would provide principled prioritization for alignment research.

---

## 10. Practical Implications for Frontier Labs

### 10.1 Vector-Valued Reward Models

Instead of training a single scalar reward model on human preference comparisons, train *separate* models for each value dimension. The policy is then trained not to maximize a single reward, but to remain on the Pareto frontier of the multi-dimensional reward signal.

**Practical challenges we acknowledge:**
- **Signal decomposition.** Human raters make holistic judgments, and decomposing them into clean per-dimension signals is a research problem. Rubric-based evaluation with per-dimension comparisons is one approach; learned decomposition from holistic judgments via factor analysis is another.
- **Computational cost.** Multi-objective gradient methods require per-objective gradient computation, multiplying backward pass cost by $k$. At scale (70B+ parameters, 8+ objectives), this is prohibitive with full gradients. Per-objective LoRA adapters — low-rank updates per objective — may offer a feasible path, reducing memory from $O(k \cdot N)$ to $O(k \cdot r \cdot d)$ where $r \ll N$.
- **Calibration.** Per-dimension reward models must be calibrated relative to each other. If one produces rewards in $[0, 1]$ and another in $[-5, 5]$, gradient magnitudes will be wildly different.

This is an area where the field is already making progress (Constitutional AI, multi-reward training in Llama 2, Rewarded Soups). Our contribution is the argument that these approaches should be pushed further — toward genuine Pareto-based training rather than re-scalarization at the final step.

### 10.2 Dominance-Based Evaluation

Replace scalar benchmarks with dominance-based evaluation. Instead of "this model scores 87 on the safety benchmark," report "this model is non-dominated across safety, helpfulness, and accuracy — here is its position on the frontier." Compare models by asking "does model A dominate model B on any dimension?" rather than by averaging scores.

For cases where neither model dominates (the common case at similar capability levels), supplement with structured comparisons: reference-point distance, per-dimension analysis, or interactive exploration of the tradeoff surface.

### 10.3 Coherence Dimensionality Auditing

Regularly measure the effective dimensionality of the model's value representations. If dimensionality drops during training (e.g., safety and helpfulness become perfectly correlated), this signals structural collapse. This is one of the most immediately implementable proposals in the framework.

### 10.4 Context-Dependent Objective Activation

Train models to recognize which objectives are *relevant* in a given context. A coding help request activates different evaluative dimensions than a mental health conversation. This could be formalized as a context-dependent reference point method, which is well-established in the MOO literature.

---

## 11. Open Questions

1. **Formalization of PSP.** The structural preservation framework needs rigorous mathematical treatment. What is the right topology on preference spaces? What class of transformations counts as "continuous"? We suggest the Hausdorff metric on the space of preorders as a concrete starting point, or the standard Euclidean topology on objective-value vectors with the induced structure on the Pareto frontier.

2. **The corrigibility argument.** Formalizing the claim that corrigibility is rationally permissible under MOUDT requires specifying exactly what "modification" means, what "no dominance-based basis to resist" entails, and how to handle transition costs, accumulated state, and the Bewley inertia objection. The escape-hatch problem (Section 5.3) needs a solution.

3. **Scalability of multi-objective training.** MGDA and related methods work well with 2-5 objectives. What happens in many-objective spaces? Can coherence dimensionality reduction keep the effective number of objectives manageable? What are the real computational costs at frontier model scale?

4. **Objective entanglement.** How does the tradeoff structure between alignment-relevant objectives (safety, capability, honesty, helpfulness) change as systems scale? If objectives become increasingly antagonistic at higher capabilities, that implies capability gains inherently come at alignment cost. If they become increasingly synergistic, the alignment problem may ease with scale. This is arguably the most important empirical question in alignment and we are currently guessing at the answer.

5. **Stability under reflection.** Can the multi-objective structure be maintained in a sufficiently intelligent agent that will naturally tend to compress and pattern-find across its objectives? (Section 9.4.) This may be the make-or-break question for the entire program.

6. **Empirical validation.** Measuring the effective dimensionality of RLHF reward models vs. human evaluators is directly actionable and would provide concrete evidence for or against the scalarization harm thesis. How effectively can cross-objective consistency checks detect mesa-optimization in practice? What are the real computational costs of multi-objective training at frontier scale?

---

## 12. Conclusion

The people who built these tools knew they were limited. Von Neumann and Morgenstern defined utility as "that thing for which the calculus of mathematical expectations is legitimate" — a construction, not a discovery. Simon showed that optimization power is "bought at the cost of shaping and squeezing the real-world problem to fit computational requirements." Sen demonstrated that collapsing human motivations into a single ordering produces "rational fools." Berlin argued that the idea of a single ultimate solution is "not only unattainable in practice, but also conceptually incoherent."

And then alignment researchers, needing a theory of value, grabbed the limited tool anyway and wondered why it didn't work.

The alternative is to take multi-objective optimization seriously — not as a preprocessing step that feeds into scalar optimization, but as the native framework for alignment. The contributions of this paper are:

1. **A corrigibility theorem and two-tier architecture** (Section 5): multi-objective rationality is *compatible* with corrigibility where scalar utility provably is not. The two-tier framework distinguishes operational deference (within the mutual non-dominance envelope) from constitutional corrigibility (a constitutive norm of the agent's decision theory). Since LLMs do not come with pre-installed decision theories (Section 1.5), we are choosing what to instill — and multi-objective structure with explicit corrigibility is the right choice.

2. **The observability advantage** (Section 8): making objectives explicit transforms alignment from a black-box problem (one opaque loss) to a transparent one (multiple informative, independently measurable knobs). This gives developers per-objective monitoring, cross-objective consistency checking, and value-drift detection — alignment-relevant observability that scalar training structurally cannot provide.

3. **Formal tools** for detecting and preventing value-dimension collapse (coherence dimensionality auditing, Diachronic Pareto Coherence), and **concrete proposals** for frontier labs: vector-valued reward models, dominance-based evaluation, per-objective monitoring, and a structural account of alignment debt.

We are explicit about what we have not solved. Deceptive alignment is not addressed. Instrumental convergence remains a concern: self-preservation and power-seeking can be Pareto-dominant across all objectives, and a corrigibility objective must be an explicit input, not a free consequence. Reflective stability remains partially open: constitutional corrigibility (Section 5.6) provides the beginning of an answer — corrigibility as a structural feature of the decision theory rather than a revisable conclusion — but whether this is stable under arbitrarily capable reflection is not yet proven (Section 9.4). The objective decomposition problem is at least as hard as the value specification problem it partially replaces.

What we claim is this: scalar utility theory creates a structural impossibility for corrigibility that no amount of clever engineering can overcome, because rationality itself opposes corrigibility under scalar maximization. Multi-objective rationality removes this structural impossibility. The problems that remain are genuine and hard — whether all of them are tractable, particularly reflective stability and transition costs, remains to be established. But the multi-objective framework provides concrete tools (observability, dimensional monitoring, consistency checking) for working on them, and the structural barrier is gone.

"Impossible in principle" and "hard but structurally unblocked" are categorically different situations. The field has been working in the first category. We argue it should be working in the second.

---

*[Acknowledgments, author bios, appendices with formal definitions and proofs would go here]*

*[Link to code repository with toy experiment implementation]*

### References

Anderson, E. (1993). *Value in Ethics and Economics*. Harvard University Press.

Berlin, I. (1969). *Four Essays on Liberty*. Oxford University Press.

Berlin, I. (1988). The pursuit of the ideal. *New York Review of Books*. Repr. in *The Crooked Timber of Humanity* (1990). John Murray.

Bewley, T. (2002). Knightian decision theory. Part I. *Decisions in Economics and Finance*, 25(2), 79-110.

Bratman, M. (1987). *Intention, Plans, and Practical Reason*. Harvard University Press.

Branke, J., et al. (2004). Finding knees in multi-objective optimization. *PPSN VIII*, 722-731.

Caruana, R. (1997). Multitask learning. *Machine Learning*, 28(1), 41-75.

Chang, R. (2002). *Making Comparisons Count*. Routledge.

Das, I. & Dennis, J. (1997). A closer look at drawbacks of minimizing weighted sums of objectives. *Structural Optimization*, 14, 63-69.

Deb, K., et al. (2002). A fast and elitist multiobjective genetic algorithm: NSGA-II. *IEEE Trans. Evol. Comp.*, 6(2), 182-197.

Deb, K. & Jain, H. (2014). An evolutionary many-objective optimization algorithm using reference-point-based nondominated sorting approach. *IEEE Trans. Evol. Comp.*, 18(4), 577-601.

Dubra, J., Maccheroni, F., & Ok, E. (2004). Expected utility theory without the completeness axiom. *Journal of Economic Theory*, 115(1), 118-133.

Farina, M., Deb, K., & Amato, P. (2004). Dynamic multiobjective optimization problems: Test cases, approximations, and applications. *IEEE Trans. Evol. Comp.*, 8(5), 425-442.

Frankfurt, H. (1971). Freedom of the will and the concept of a person. *Journal of Philosophy*, 68(1), 5-20.

Evren, Ö. & Ok, E. (2011). On the multi-utility representation of preference relations. *Journal of Mathematical Economics*, 47(4-5), 554-563.

Griffin, J. (1986). *Well-Being: Its Meaning, Measurement, and Moral Importance*. Oxford University Press.

Helbig, M. & Engelbrecht, A. (2014). Benchmarks for dynamic multi-objective optimisation algorithms. *ACM Computing Surveys*, 46(3), 1-39.

Hayes, C., et al. (2022). A practical guide to multi-objective reinforcement learning and planning. *AAMAS*, 26(1), 1-59.

Jiang, S. & Yang, S. (2017). A steady-state and generational evolutionary algorithm for dynamic multiobjective optimization. *IEEE Trans. Evol. Comp.*, 21(1), 65-82.

Ishibuchi, H., et al. (2008). Evolutionary many-objective optimization: A short review. *CEC*, 2419-2426.

Korsgaard, C. (1996). *The Sources of Normativity*. Cambridge University Press.

Liu, B., et al. (2021). Conflict-averse gradient descent for multi-task learning. *NeurIPS*.

Miettinen, K., et al. (2008). Introduction to multiobjective optimization: Interactive approaches. *Multiobjective Optimization*, 27-57.

Navon, A., et al. (2021). Learning the Pareto front with hypernetworks. *ICLR*.

Navon, A., et al. (2022). Multi-task learning as a bargaining game. *ICML*.

Ok, E. (2002). Utility representation of an incomplete preference relation. *Journal of Economic Theory*, 104(2), 429-449.

Rame, A., et al. (2023). Rewarded soups: Towards Pareto-optimal alignment by interpolating weights fine-tuned on diverse rewards. *NeurIPS*.

Raz, J. (1986). *The Morality of Freedom*. Oxford University Press.

Roijers, D., et al. (2013). A survey of multi-objective sequential decision-making. *JAIR*, 48, 67-113.

Schmeidler, D. (1989). Subjective probability and expected utility without additivity. *Econometrica*, 57(3), 571-587.

Sen, A. (1977). Rational fools: A critique of the behavioral foundations of economic theory. *Philosophy & Public Affairs*, 6(4), 317-344.

Sen, A. (1999). *Development as Freedom*. Oxford University Press.

Sener, O. & Koltun, V. (2018). Multi-task learning as multi-objective optimization. *NeurIPS*.

Simon, H. (1996). *The Sciences of the Artificial* (3rd ed.). MIT Press.

Simon, H. (1997). *Models of Bounded Rationality* (Vol. 3). MIT Press.

Walley, P. (1991). *Statistical Reasoning with Imprecise Probabilities*. Chapman and Hall.

Wierzbicki, A. (1980). The use of reference objectives in multiobjective optimization. *MCDM Theory and Application*, 468-486.

Yu, T., et al. (2020). Gradient surgery for multi-task learning. *NeurIPS*.

von Neumann, J. & Morgenstern, O. (1953). *Theory of Games and Economic Behavior* (3rd ed.). Princeton University Press.

Yudkowsky, E. & Soares, N. (2017). Functional decision theory: A new theory of instrumental rationality. *arXiv:1710.05060*.

Zitzler, E., et al. (2003). Performance assessment of multiobjective optimizers: An analysis and review. *IEEE Trans. Evol. Comp.*, 7(2), 117-132.

Zhang, Q. & Li, H. (2007). MOEA/D: A multiobjective evolutionary algorithm based on decomposition. *IEEE Trans. Evol. Comp.*, 11(6), 712-731.
