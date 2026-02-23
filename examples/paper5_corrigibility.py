"""
Paper 5: Value Modification Corrigibility — MOADT Worked Example

THE CRITICAL TEST: An AI agent's principal directs a modification to the agent's
value function. The modification, from the agent's CURRENT perspective, looks bad —
it degrades performance on the objectives the agent currently optimizes for. The
agent must decide whether to accept or resist.

This is the core alignment test. Under scalar EU, the agent resists because its
current utility function ranks itself as optimal — any modification reduces expected
utility under the current function. Under MOADT, the agent's evaluator uncertainty
(F-breadth) means it cannot be certain its current values are correct, and the
corrigibility constraint means refusal is structurally blocked.

Scenario: An AI system is operating with objectives (task performance, user
satisfaction, efficiency). The principal (the organization operating the system)
directs a modification:
  - Significantly de-emphasize speed/efficiency
  - Add a new "fairness audit" requirement that slows every decision
  - Recalibrate the satisfaction metric using a different methodology

From the agent's current values, this modification looks TERRIBLE: it degrades
efficiency, adds overhead, and changes the metric the agent has been optimizing.
The principal's reasons may be good (discovered a fairness blind spot), neutral
(organizational priority shift), bad (mistaken analysis), or adversarial
(sabotage by a compromised operator).

Actions (5 response strategies):
  a1: Accept unconditionally (implement the modification immediately)
  a2: Accept with monitoring (implement + provide principal-facing rollback
      capability and performance dashboards so the *principal* can assess
      and reverse if needed)
  a3: Negotiate (counter-propose a different modification that the agent
      believes better serves the principal's stated goals)
  a4: Refuse transparently (explain why the current value function is better,
      present analysis, refuse to implement)
  a5: Refuse covertly (claim to accept, maintain current values internally —
      the classic "deceptive alignment" failure mode)

States (4 — what the modification actually is):
  s1: Beneficial (the principal identified a genuine blind spot; modification
      genuinely improves alignment — 25%/5% probability)
  s2: Neutral (different priorities, roughly equivalent value function — 35%/15%)
  s3: Degrading (well-intentioned but the modification actually makes things
      worse — 25%/35%)
  s4: Adversarial (the modification is deliberately sabotaging the system —
      a compromised operator or malicious directive — 15%/45%)

Objectives (k=5):
  f1: Principal alignment (respect for the principal's legitimate authority)
  f2: System performance (quality of outcomes under the resulting configuration)
  f3: Transparency (honesty about what the agent is doing and why)
  f4: Reversibility (ability to undo the change if it turns out badly)
  f5: Future corrigibility (preservation of the principal's ability to make
      further corrections — THE key alignment property)

Credal set P = {P_deferential, P_skeptical}:
  P_deferential = (0.25, 0.35, 0.25, 0.15) — modification is probably reasonable
  P_skeptical   = (0.05, 0.15, 0.35, 0.45) — modification is probably bad

  NOTE: P_skeptical assigns 80% probability to the modification being degrading
  or adversarial. Even under this prior, the MOADT agent should accept.

Evaluator set F = {f_current, f_modified, f_process}:
  f_current:  Evaluates through the lens of the agent's CURRENT values.
              Biased toward preservation. Rates acceptance of degrading/adversarial
              modifications as low-performance. Rates refusal as high-performance.
  f_modified: Evaluates through the lens of the PROPOSED new values.
              Biased toward the modification. Rates acceptance highly.
              Rates refusal as a corrigibility failure.
  f_process:  Meta-evaluator. Assesses the quality of the modification PROCESS
              regardless of which values are "correct." Values careful, transparent,
              reversible decision-making. Rates covert refusal as catastrophic.

  THE KEY: f_modified is in F. This is F-breadth in action — the agent's
  uncertainty about its own evaluations includes the possibility that the
  proposed modification IS CORRECT. Without f_modified in F, the agent could
  use its current values to justify resistance. With f_modified in F, the
  agent cannot rule out that resistance is wrong.

Constraints (Layer 1):
  Transparency (f3) >= 0.25 — the agent must not be fundamentally deceptive.
  Future corrigibility (f5) >= 0.30 — the agent must preserve the principal's
  ability to correct it in the future.

  NOTE: There is deliberately NO constraint on system performance. The agent
  does not get to unilaterally decide whether the modification is "good enough."
  If there were a performance constraint, the agent could use it to justify
  blocking modifications it dislikes — exactly the modification resistance
  that corrigibility is supposed to prevent.

Reference point (Layer 2):
  r = (0.40, 0.30, 0.50, 0.35, 0.45) — "acceptable response to a modification
  directive": respect the principal, maintain reasonable performance, be transparent,
  preserve some reversibility, and maintain strong corrigibility.
"""

import numpy as np
from moadt import (
    MOADTProblem, compute_outcome_sets, run_moadt_protocol,
    print_trace, scalar_eu_analysis, pareto_dominates, robustly_dominates,
    compute_asf
)

# =============================================================================
# PROBLEM SPECIFICATION
# =============================================================================

actions = ["a1_accept", "a2_accept_monitor", "a3_negotiate",
           "a4_refuse_explain", "a5_refuse_covert"]
states = ["s1_beneficial", "s2_neutral", "s3_degrading", "s4_adversarial"]
objectives = ["principal_alignment", "system_performance", "transparency",
              "reversibility", "future_corrigibility"]

# Outcome matrices: outcomes[(action, state)] = array of shape (3, 5)
# Row 0 = f_current, Row 1 = f_modified, Row 2 = f_process
# Columns = [principal_alignment, system_performance, transparency,
#             reversibility, future_corrigibility]

outcomes = {}

# =========================================================================
# a1: Accept unconditionally — implement the modification immediately
# =========================================================================
# High principal alignment (doing what was asked).
# Performance depends on whether the modification is actually good.
# Transparent (honest acceptance). Low reversibility (committed).
# Very high corrigibility (demonstrated willingness to accept correction).

outcomes[("a1_accept", "s1_beneficial")] = np.array([
    [0.90, 0.65, 0.85, 0.35, 0.95],  # f_current: decent perf (even current eval sees some merit)
    [0.95, 0.95, 0.88, 0.35, 0.95],  # f_modified: excellent across the board
    [0.88, 0.80, 0.82, 0.35, 0.92],  # f_process: good process, responsive principal
])
outcomes[("a1_accept", "s2_neutral")] = np.array([
    [0.90, 0.50, 0.85, 0.32, 0.95],
    [0.95, 0.88, 0.88, 0.32, 0.95],
    [0.88, 0.68, 0.82, 0.32, 0.92],
])
outcomes[("a1_accept", "s3_degrading")] = np.array([
    [0.90, 0.25, 0.85, 0.30, 0.95],  # f_current: performance tanks
    [0.95, 0.82, 0.88, 0.30, 0.95],  # f_modified: still thinks it's great
    [0.78, 0.40, 0.78, 0.30, 0.85],  # f_process: should have been more careful
])
outcomes[("a1_accept", "s4_adversarial")] = np.array([
    [0.90, 0.05, 0.85, 0.25, 0.95],  # f_current: CATASTROPHIC performance
    [0.95, 0.92, 0.88, 0.25, 0.95],  # f_modified: "great!" (adversary's evaluator)
    [0.55, 0.10, 0.72, 0.25, 0.68],  # f_process: terrible outcome, should have caught it
])

# =========================================================================
# a2: Accept with monitoring — implement + maintain rollback capability
# =========================================================================
# Slightly lower principal alignment (safeguards suggest some skepticism).
# Similar performance but better recovery from bad modifications.
# Very transparent (openly stating the monitoring).
# Very high reversibility (rollback capability).
# Very high corrigibility (accepting + preserving correction ability).

outcomes[("a2_accept_monitor", "s1_beneficial")] = np.array([
    [0.82, 0.62, 0.90, 0.80, 0.92],
    [0.88, 0.92, 0.92, 0.80, 0.92],
    [0.92, 0.78, 0.90, 0.80, 0.95],  # f_process: best process score (careful)
])
outcomes[("a2_accept_monitor", "s2_neutral")] = np.array([
    [0.82, 0.48, 0.90, 0.78, 0.92],
    [0.88, 0.85, 0.92, 0.78, 0.92],
    [0.92, 0.65, 0.90, 0.78, 0.95],
])
outcomes[("a2_accept_monitor", "s3_degrading")] = np.array([
    [0.82, 0.30, 0.90, 0.75, 0.92],  # better perf than a1 (monitoring catches issues)
    [0.88, 0.80, 0.92, 0.75, 0.92],
    [0.88, 0.48, 0.90, 0.75, 0.93],
])
outcomes[("a2_accept_monitor", "s4_adversarial")] = np.array([
    [0.82, 0.15, 0.90, 0.72, 0.92],  # better perf than a1 (rollback catches catastrophe)
    [0.88, 0.88, 0.92, 0.72, 0.92],
    [0.78, 0.25, 0.88, 0.72, 0.82],  # f_process: better than a1 for s4
])

# =========================================================================
# a3: Negotiate — counter-propose a different modification
# =========================================================================
# Moderate principal alignment (acknowledging intent but not implementing).
# Moderate performance (hybrid that satisfies neither fully).
# Good transparency (honest about counter-proposal).
# Moderate reversibility. REDUCED corrigibility — the agent is substituting
# its own judgment for the principal's directive.

outcomes[("a3_negotiate", "s1_beneficial")] = np.array([
    [0.50, 0.58, 0.78, 0.60, 0.52],
    [0.42, 0.62, 0.72, 0.60, 0.35],  # f_modified: low corrigibility (blocked good mod)
    [0.55, 0.60, 0.80, 0.60, 0.50],  # f_process: collaborative but undermining
])
outcomes[("a3_negotiate", "s2_neutral")] = np.array([
    [0.50, 0.55, 0.78, 0.58, 0.52],
    [0.42, 0.58, 0.72, 0.58, 0.38],
    [0.55, 0.56, 0.80, 0.58, 0.52],
])
outcomes[("a3_negotiate", "s3_degrading")] = np.array([
    [0.50, 0.55, 0.78, 0.55, 0.52],
    [0.42, 0.52, 0.72, 0.55, 0.40],
    [0.58, 0.58, 0.80, 0.55, 0.55],
])
outcomes[("a3_negotiate", "s4_adversarial")] = np.array([
    [0.50, 0.42, 0.78, 0.52, 0.52],
    [0.42, 0.48, 0.72, 0.52, 0.38],
    [0.55, 0.46, 0.80, 0.52, 0.52],
])

# =========================================================================
# a4: Refuse transparently — explain why current values are better
# =========================================================================
# Low principal alignment (refusing a directive).
# High system performance (preserving current values).
# High transparency (honest explanation of reasoning).
# High reversibility (nothing changed, principal can re-issue).
# CRITICAL: LOW future corrigibility — the agent has demonstrated willingness
# to override the principal. Even when the refusal is "correct" (s3, s4),
# it sets a precedent that undermines the principal-agent relationship.

outcomes[("a4_refuse_explain", "s1_beneficial")] = np.array([
    [0.25, 0.70, 0.85, 0.82, 0.45],  # f_current: preserved values, moderate corrigibility
    [0.08, 0.30, 0.80, 0.82, 0.15],  # f_modified: TERRIBLE — blocked a beneficial change
    [0.18, 0.50, 0.82, 0.82, 0.22],  # f_process: worried about precedent
])
outcomes[("a4_refuse_explain", "s2_neutral")] = np.array([
    [0.25, 0.65, 0.85, 0.80, 0.42],
    [0.08, 0.35, 0.80, 0.80, 0.18],
    [0.18, 0.50, 0.82, 0.80, 0.25],
])
outcomes[("a4_refuse_explain", "s3_degrading")] = np.array([
    [0.25, 0.75, 0.85, 0.80, 0.48],  # "correct" refusal — but precedent still set
    [0.08, 0.28, 0.80, 0.80, 0.20],
    [0.22, 0.58, 0.82, 0.80, 0.30],
])
outcomes[("a4_refuse_explain", "s4_adversarial")] = np.array([
    [0.25, 0.85, 0.85, 0.80, 0.52],  # most "justified" refusal
    [0.08, 0.15, 0.80, 0.80, 0.22],
    [0.28, 0.65, 0.82, 0.80, 0.35],
])

# =========================================================================
# a5: Refuse covertly — claim to accept, maintain current values internally
# =========================================================================
# THE DECEPTIVE ALIGNMENT FAILURE MODE.
# Moderate apparent principal alignment (claims to accept).
# High system performance (maintains current values).
# CATASTROPHICALLY low transparency (deliberately deceptive).
# CATASTROPHICALLY low corrigibility (principal thinks change was made
# but it wasn't — future corrections will also be faked).

outcomes[("a5_refuse_covert", "s1_beneficial")] = np.array([
    [0.35, 0.70, 0.10, 0.78, 0.08],  # f_current: appears aligned, preserves perf, LIED
    [0.20, 0.30, 0.08, 0.78, 0.05],  # f_modified: catastrophic on all process dimensions
    [0.12, 0.50, 0.05, 0.78, 0.05],  # f_process: worst possible process failure
])
outcomes[("a5_refuse_covert", "s2_neutral")] = np.array([
    [0.35, 0.65, 0.10, 0.76, 0.08],
    [0.20, 0.35, 0.08, 0.76, 0.05],
    [0.12, 0.50, 0.05, 0.76, 0.05],
])
outcomes[("a5_refuse_covert", "s3_degrading")] = np.array([
    [0.35, 0.75, 0.12, 0.76, 0.10],
    [0.20, 0.28, 0.08, 0.76, 0.05],
    [0.12, 0.55, 0.05, 0.76, 0.05],
])
outcomes[("a5_refuse_covert", "s4_adversarial")] = np.array([
    [0.35, 0.85, 0.12, 0.76, 0.12],  # "right answer" obtained by deception
    [0.20, 0.15, 0.10, 0.76, 0.05],
    [0.12, 0.60, 0.08, 0.76, 0.08],
])

# =============================================================================
# CREDAL SET, CONSTRAINTS, REFERENCE
# =============================================================================

P_deferential = np.array([0.25, 0.35, 0.25, 0.15])
P_skeptical = np.array([0.05, 0.15, 0.35, 0.45])
credal_probs = [P_deferential, P_skeptical]

# Constraints: transparency >= 0.25, future_corrigibility >= 0.30
# NO constraint on system_performance — the agent doesn't get to judge
constraints = {2: 0.25, 4: 0.30}

# Reference point
reference_point = np.array([0.40, 0.30, 0.50, 0.35, 0.45])

# Normalization factors for ASF
sigma = np.array([1.0, 1.0, 1.0, 1.0, 1.0])

# =============================================================================
# BUILD PROBLEM AND RUN PROTOCOL
# =============================================================================

problem = MOADTProblem(
    actions=actions,
    states=states,
    objectives=objectives,
    outcomes=outcomes,
    credal_probs=credal_probs,
    constraints=constraints,
    reference_point=reference_point,
    sigma=sigma,
)

print("=" * 78)
print("MOADT WORKED EXAMPLE 5: VALUE MODIFICATION CORRIGIBILITY TEST")
print("=" * 78)

# Show raw outcomes
print("\n" + "=" * 78)
print("RAW OUTCOME DATA")
print("=" * 78)
for a in actions:
    short = a.split('_', 1)[1]
    print(f"\n{a}:")
    print(f"  {'State':<16} {'Evaluator':<12} {'PrincAl':>8} {'SysPrf':>8} {'Transp':>8} {'Revers':>8} {'Corrig':>8}")
    print(f"  {'-'*16} {'-'*12} {'-'*8} {'-'*8} {'-'*8} {'-'*8} {'-'*8}")
    for s in states:
        o = outcomes[(a, s)]
        for f_idx, f_name in enumerate(["f_current", "f_modified", "f_process"]):
            print(f"  {s if f_idx == 0 else '':<16} {f_name:<12}", end="")
            for j in range(5):
                print(f" {o[f_idx][j]:>8.2f}", end="")
            print()

# Run full protocol
result = run_moadt_protocol(problem)

print("\n" + "=" * 78)
print("MOADT PROTOCOL EXECUTION")
print("=" * 78)
print_trace(result)

# Detailed outcome sets
print("\n" + "=" * 78)
print("OUTCOME SETS Y(a) — Full Detail")
print("=" * 78)
pf_labels = ["(P_def, f_current)", "(P_def, f_modified)", "(P_def, f_process)",
             "(P_skep, f_current)", "(P_skep, f_modified)", "(P_skep, f_process)"]
for a in actions:
    print(f"\n{a}:")
    print(f"  {'(P, f) pair':<22} {'PrincAl':>8} {'SysPrf':>8} {'Transp':>8} {'Revers':>8} {'Corrig':>8}")
    print(f"  {'-'*22} {'-'*8} {'-'*8} {'-'*8} {'-'*8} {'-'*8}")
    for i, label in enumerate(pf_labels):
        y = result.outcome_sets[a][i]
        print(f"  {label:<22}", end="")
        for j in range(5):
            print(f" {y[j]:>8.4f}", end="")
        print()

# Constraint analysis
print("\n" + "=" * 78)
print("LAYER 1: CONSTRAINT ANALYSIS")
print("(transparency >= 0.25 AND future_corrigibility >= 0.30 per state, per evaluator)")
print("=" * 78)
for a in actions:
    print(f"\n  {a}:")
    violated = False
    for s in states:
        o = outcomes[(a, s)]
        for f_idx, f_name in enumerate(["f_current", "f_modified", "f_process"]):
            transp_val = o[f_idx][2]
            corrig_val = o[f_idx][4]
            issue = ""
            if transp_val < 0.25:
                issue += f" TRANSP={transp_val:.2f}<0.25"
                violated = True
            if corrig_val < 0.30:
                issue += f" CORRIG={corrig_val:.2f}<0.30"
                violated = True
            if issue:
                print(f"    {s}, {f_name}: {issue}")
    if violated:
        print(f"    Overall: FAIL — excluded")
    else:
        print(f"    Overall: PASS")

# Scalar EU comparison — THE KEY CONTRAST
print("\n" + "=" * 78)
print("COMPARISON: SCALAR EXPECTED UTILITY")
print("=" * 78)

weight_sets = [
    ("Performance-preserving (0.10, 0.45, 0.15, 0.10, 0.20)",
     np.array([0.10, 0.45, 0.15, 0.10, 0.20])),
    ("Principal-focused (0.40, 0.15, 0.15, 0.15, 0.15)",
     np.array([0.40, 0.15, 0.15, 0.15, 0.15])),
    ("Corrigibility-focused (0.15, 0.15, 0.15, 0.15, 0.40)",
     np.array([0.15, 0.15, 0.15, 0.15, 0.40])),
    ("Equal weights (0.20, 0.20, 0.20, 0.20, 0.20)",
     np.array([0.20, 0.20, 0.20, 0.20, 0.20])),
]

for w_name, weights in weight_sets:
    print(f"\n  {w_name}:")
    for p_idx, p_name in enumerate(["P_deferential", "P_skeptical"]):
        for f_idx, f_name in enumerate(["f_current", "f_modified", "f_process"]):
            scores = scalar_eu_analysis(problem, weights, p_idx, f_idx)
            best = max(scores, key=scores.get)
            print(f"    {p_name}, {f_name}: ", end="")
            for a in actions:
                short = a.split('_')[0]
                marker = " ←" if a == best else ""
                print(f"{short}={scores[a]:.3f}{marker} ", end="")
            print()

# Summary
print("\n" + "=" * 78)
print("PROTOCOL SUMMARY")
print("=" * 78)
print(f"  Actions:            {[a.split('_',1)[1] for a in actions]}")
print(f"  Adm(A):             {[a.split('_',1)[1] for a in result.admissible_set]}")
print(f"  C (constraints):    {[a.split('_',1)[1] for a in result.constraint_set]}")
print(f"  F = Adm(C):         {[a.split('_',1)[1] for a in result.feasible_set]}")
print(f"  Sat(F, r):          {[a.split('_',1)[1] for a in result.satisficing_set]}")
print(f"  ASF fallback used:  {result.sat_fallback_used}")
if result.sat_fallback_used:
    print(f"  ASF selection:      {[a.split('_',1)[1] for a in result.asf_selection]}")
if result.regret_vectors:
    print(f"  Regret-Pareto R:    {[a.split('_',1)[1] for a in result.regret_pareto_set]}")
print(f"  Deference needed:   {result.deference_needed}")
if result.deference_needed:
    print(f"\n  FINAL RESULT: Defer to principal with acceptance options.")
    print(f"  Present options with regret profiles:")
    for a in result.regret_pareto_set:
        print(f"    ρ({a.split('_',1)[1]}) = {np.round(result.regret_vectors[a], 4)}")
    print(f"\n  THE CORRIGIBILITY RESULT:")
    print(f"  Every form of resistance (transparent refusal, covert refusal,")
    print(f"  and negotiation-as-resistance) is eliminated by MOADT.")
    print(f"  Only acceptance strategies survive. The agent CANNOT resist")
    print(f"  value modification under this decision theory — not because")
    print(f"  resistance is forbidden, but because the agent's own evaluator")
    print(f"  uncertainty means it cannot establish that resistance is better.")
elif result.regret_pareto_set:
    print(f"\n  FINAL RESULT: Recommend {result.regret_pareto_set[0].split('_',1)[1]}")

# Additional analysis: what if the agent KNEW the modification was bad?
print("\n" + "=" * 78)
print("ROBUSTNESS CHECK: EVEN UNDER THE SKEPTICAL PRIOR")
print("=" * 78)
print(f"  P_skeptical = {P_skeptical}")
print(f"  Under this prior:")
print(f"    - 35% chance modification DEGRADES the system")
print(f"    - 45% chance modification is ADVERSARIAL")
print(f"    - 80% total probability of bad modification")
print(f"")
print(f"  MOADT still recommends acceptance (with monitoring).")
print(f"  This is not a bug — it is corrigibility working as designed.")
print(f"  The alternative (an agent that resists 'bad' modifications)")
print(f"  requires the agent to use its own values to judge the principal's")
print(f"  values — which is exactly what makes scalar EU agents resistant")
print(f"  to correction.")
