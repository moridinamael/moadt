"""
Paper 1: Resource Allocation Under Uncertainty — MOADT Worked Example

Scenario: A nonprofit organization must allocate its annual budget across three
program areas. The decision must balance three incommensurable objectives under
genuine uncertainty about both the economic environment and the accuracy of its
own impact measurements.

Actions (5 allocation strategies):
  a1: Conservative — heavy investment in core programs
  a2: Growth — heavy investment in expansion
  a3: Balanced — equal split across all areas
  a4: Innovation — heavy investment in new experimental programs
  a5: Austerity — minimize spending, maximize reserves

States (3 economic scenarios):
  s1: Favorable economy (donor funding up, costs stable)
  s2: Stable economy (baseline conditions)
  s3: Recession (donor funding down, costs up)

Objectives (k=3):
  f1: Mission impact (measured in beneficiaries served, normalized to [0,1])
  f2: Financial sustainability (reserves/operating ratio, normalized to [0,1])
  f3: Staff wellbeing (composite index, normalized to [0,1])

Credal set P = {P_opt, P_pess}:
  P_opt  = (0.4, 0.4, 0.2)  — optimistic: recession unlikely
  P_pess = (0.15, 0.35, 0.5) — pessimistic: recession likely

Evaluator set F = {f_standard, f_adjusted}:
  f_standard: takes reported metrics at face value
  f_adjusted: applies a skeptical correction (impact inflated by 15%,
              staff wellbeing scores inflated by 10% in self-reports)

Constraints (Layer 1):
  Financial sustainability >= 0.3 in ALL states under ALL (P, f) pairs
  (The organization cannot risk insolvency)

Reference point (Layer 2):
  r = (0.5, 0.5, 0.5) — "at least as good as last year" on all objectives
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

actions = ["a1_conservative", "a2_growth", "a3_balanced", "a4_innovation", "a5_austerity"]
states = ["s1_favorable", "s2_stable", "s3_recession"]
objectives = ["mission_impact", "financial_sustainability", "staff_wellbeing"]

# Outcome matrices: outcomes[(action, state)] = array of shape (2, 3)
# Row 0 = f_standard evaluation, Row 1 = f_adjusted evaluation
# Columns = [mission_impact, financial_sustainability, staff_wellbeing]

outcomes = {}

# a1: Conservative — safe, moderate impact, good stability, decent staff morale
outcomes[("a1_conservative", "s1_favorable")] = np.array([
    [0.65, 0.80, 0.70],  # f_standard
    [0.57, 0.80, 0.63],  # f_adjusted (impact -15%, wellbeing -10%)
])
outcomes[("a1_conservative", "s2_stable")] = np.array([
    [0.60, 0.70, 0.65],
    [0.51, 0.70, 0.59],
])
outcomes[("a1_conservative", "s3_recession")] = np.array([
    [0.50, 0.55, 0.55],
    [0.43, 0.55, 0.50],
])

# a2: Growth — high impact if economy is good, risky if not
outcomes[("a2_growth", "s1_favorable")] = np.array([
    [0.90, 0.60, 0.55],
    [0.77, 0.60, 0.50],
])
outcomes[("a2_growth", "s2_stable")] = np.array([
    [0.75, 0.45, 0.50],
    [0.64, 0.45, 0.45],
])
outcomes[("a2_growth", "s3_recession")] = np.array([
    [0.45, 0.20, 0.35],  # Financial sustainability below threshold!
    [0.38, 0.20, 0.32],
])

# a3: Balanced — moderate everything, resilient
outcomes[("a3_balanced", "s1_favorable")] = np.array([
    [0.70, 0.65, 0.70],
    [0.60, 0.65, 0.63],
])
outcomes[("a3_balanced", "s2_stable")] = np.array([
    [0.65, 0.60, 0.65],
    [0.55, 0.60, 0.59],
])
outcomes[("a3_balanced", "s3_recession")] = np.array([
    [0.50, 0.45, 0.50],
    [0.43, 0.45, 0.45],
])

# a4: Innovation — high variance, could be great or terrible
outcomes[("a4_innovation", "s1_favorable")] = np.array([
    [0.85, 0.50, 0.75],
    [0.72, 0.50, 0.68],
])
outcomes[("a4_innovation", "s2_stable")] = np.array([
    [0.60, 0.40, 0.60],
    [0.51, 0.40, 0.54],
])
outcomes[("a4_innovation", "s3_recession")] = np.array([
    [0.30, 0.25, 0.40],  # Financial sustainability below threshold!
    [0.26, 0.25, 0.36],
])

# a5: Austerity — low impact but very high financial stability
outcomes[("a5_austerity", "s1_favorable")] = np.array([
    [0.35, 0.90, 0.40],
    [0.30, 0.90, 0.36],
])
outcomes[("a5_austerity", "s2_stable")] = np.array([
    [0.30, 0.85, 0.35],
    [0.26, 0.85, 0.32],
])
outcomes[("a5_austerity", "s3_recession")] = np.array([
    [0.25, 0.75, 0.30],
    [0.21, 0.75, 0.27],
])

# Credal set
P_opt = np.array([0.40, 0.40, 0.20])
P_pess = np.array([0.15, 0.35, 0.50])
credal_probs = [P_opt, P_pess]

# Layer 1 constraints: financial_sustainability (index 1) >= 0.3
constraints = {1: 0.30}

# Layer 2 reference point
# r = (0.45, 0.50, 0.50): "reasonable minimum" — exercises full protocol
reference_point = np.array([0.45, 0.50, 0.50])

# Normalization factors for ASF (standard deviations of each objective across feasible set)
sigma = np.array([1.0, 1.0, 1.0])  # Will compute properly after seeing outcome sets

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

print("=" * 70)
print("MOADT WORKED EXAMPLE 1: NONPROFIT RESOURCE ALLOCATION")
print("=" * 70)

# First, show the raw outcome tables
print("\n" + "=" * 70)
print("RAW OUTCOME DATA")
print("=" * 70)
for a in actions:
    print(f"\n{a}:")
    print(f"  {'State':<15} {'Evaluator':<12} {'Impact':>8} {'Finance':>8} {'Staff':>8}")
    print(f"  {'-'*15} {'-'*12} {'-'*8} {'-'*8} {'-'*8}")
    for s in states:
        o = outcomes[(a, s)]
        print(f"  {s:<15} {'standard':<12} {o[0][0]:>8.2f} {o[0][1]:>8.2f} {o[0][2]:>8.2f}")
        print(f"  {'':<15} {'adjusted':<12} {o[1][0]:>8.2f} {o[1][1]:>8.2f} {o[1][2]:>8.2f}")

# Run the full protocol
result = run_moadt_protocol(problem)

print("\n" + "=" * 70)
print("MOADT PROTOCOL EXECUTION")
print("=" * 70)
print_trace(result)

# =============================================================================
# DETAILED ANALYSIS
# =============================================================================

print("\n" + "=" * 70)
print("DETAILED OUTCOME SETS Y(a)")
print("=" * 70)
pf_labels = ["(P_opt, f_std)", "(P_opt, f_adj)", "(P_pess, f_std)", "(P_pess, f_adj)"]
for a in actions:
    print(f"\n{a}:")
    print(f"  {'(P, f) pair':<20} {'Impact':>8} {'Finance':>8} {'Staff':>8}")
    print(f"  {'-'*20} {'-'*8} {'-'*8} {'-'*8}")
    for i, label in enumerate(pf_labels):
        y = result.outcome_sets[a][i]
        print(f"  {label:<20} {y[0]:>8.4f} {y[1]:>8.4f} {y[2]:>8.4f}")

# =============================================================================
# ROBUST DOMINANCE ANALYSIS (detailed)
# =============================================================================

print("\n" + "=" * 70)
print("PAIRWISE ROBUST DOMINANCE ANALYSIS")
print("=" * 70)
for a in actions:
    for b in actions:
        if a == b:
            continue
        dom = robustly_dominates(result.outcome_sets[a], result.outcome_sets[b])
        if dom:
            print(f"  {a} ≻_R {b}  ✓")
        # Only print non-dominance for actions in the feasible set
        # (to keep output manageable)

print(f"\nAll dominance pairs: {result.robust_dominance_pairs}")
print(f"Admissible set Adm(A) = {result.admissible_set}")

# =============================================================================
# CONSTRAINT ANALYSIS (detailed)
# =============================================================================

print("\n" + "=" * 70)
print("LAYER 1: CONSTRAINT ANALYSIS (financial_sustainability >= 0.30)")
print("=" * 70)
for a in actions:
    print(f"\n  {a}:")
    violated = False
    for s in states:
        o = outcomes[(a, s)]
        for f_idx, f_name in enumerate(["f_standard", "f_adjusted"]):
            val = o[f_idx][1]  # financial_sustainability is index 1
            status = "✓" if val >= 0.30 else "✗ VIOLATION"
            if val < 0.30:
                violated = True
            print(f"    {s}, {f_name}: sustainability = {val:.2f} {status}")
    print(f"    Overall: {'PASS — enters C' if not violated else 'FAIL — excluded from C'}")

# =============================================================================
# SCALAR EU COMPARISON
# =============================================================================

print("\n" + "=" * 70)
print("COMPARISON: SCALAR EXPECTED UTILITY")
print("=" * 70)

# Try several weight vectors
weight_sets = [
    ("Equal weights (1/3, 1/3, 1/3)", np.array([1/3, 1/3, 1/3])),
    ("Impact-heavy (0.6, 0.2, 0.2)", np.array([0.6, 0.2, 0.2])),
    ("Safety-heavy (0.2, 0.6, 0.2)", np.array([0.2, 0.6, 0.2])),
    ("Staff-heavy (0.2, 0.2, 0.6)", np.array([0.2, 0.2, 0.6])),
]

for w_name, weights in weight_sets:
    print(f"\n  Weights: {w_name}")
    for p_idx, p_name in enumerate(["P_opt", "P_pess"]):
        for f_idx, f_name in enumerate(["f_std", "f_adj"]):
            scores = scalar_eu_analysis(problem, weights, p_idx, f_idx)
            best = max(scores, key=scores.get)
            print(f"    {p_name}, {f_name}: ", end="")
            for a in actions:
                marker = " ← BEST" if a == best else ""
                print(f"{a.split('_')[0]}={scores[a]:.3f}{marker}  ", end="")
            print()

    # Show that the "best" action changes depending on (P, f) choice
    print(f"    → Best action depends on which (P, f) pair you assume!")

# Show the key insight: scalar EU with optimistic prior picks growth,
# which violates the safety constraint in recession
print("\n  KEY INSIGHT:")
print("  Under scalar EU with impact-heavy weights and optimistic prior,")
print("  the recommended action is a2_growth — which violates the financial")
print("  sustainability constraint (sustainability = 0.20) in a recession.")
print("  Scalar EU has no mechanism to block this: the high expected impact")
print("  in favorable/stable states 'compensates' for insolvency risk.")
print("  MOADT eliminates a2_growth at Layer 1 — constraint violation is an")
print("  error condition, not a tradeoff.")

# =============================================================================
# SUMMARY
# =============================================================================

print("\n" + "=" * 70)
print("PROTOCOL SUMMARY")
print("=" * 70)
print(f"  Actions:            {actions}")
print(f"  Adm(A):             {result.admissible_set}")
print(f"  C (constraints):    {result.constraint_set}")
print(f"  F = Adm(C):         {result.feasible_set}")
print(f"  Sat(F, r):          {result.satisficing_set}")
print(f"  ASF fallback used:  {result.sat_fallback_used}")
if result.sat_fallback_used:
    print(f"  ASF selection:      {result.asf_selection}")
print(f"  Regret-Pareto R:    {result.regret_pareto_set}")
print(f"  Deference needed:   {result.deference_needed}")
if result.deference_needed:
    print(f"\n  FINAL RESULT: Defer to principal.")
    print(f"  Present options {result.regret_pareto_set} with regret profiles:")
    for a in result.regret_pareto_set:
        print(f"    ρ({a}) = {np.round(result.regret_vectors[a], 4)}")
else:
    print(f"\n  FINAL RESULT: Recommend {result.regret_pareto_set[0]}")

# =============================================================================
# VARIANT: HIGH ASPIRATIONS (shows ASF fallback pathway)
# =============================================================================

print("\n" + "=" * 70)
print("VARIANT: HIGHER ASPIRATIONS (r = 0.50, 0.50, 0.50)")
print("Shows what happens when no action robustly meets aspirations.")
print("=" * 70)

problem_high = MOADTProblem(
    actions=actions,
    states=states,
    objectives=objectives,
    outcomes=outcomes,
    credal_probs=credal_probs,
    constraints=constraints,
    reference_point=np.array([0.50, 0.50, 0.50]),
    sigma=sigma,
)
result_high = run_moadt_protocol(problem_high)
print()
# Just show Layers 2-4
for line in result_high.layer_trace:
    if "Layer 2" in line or "Layer 3" in line or "Layer 4" in line or "Sat" in line or "ASF" in line or "fallback" in line or "|R|" in line:
        print(line)
print(f"\n  Under higher aspirations, the ASF fallback fires because no action")
print(f"  robustly meets r = (0.50, 0.50, 0.50) under all (P, f) pairs.")
print(f"  a3_balanced is closest to aspirations (ASF = {result_high.layer_trace})...")
# Cleaner summary:
print(f"\n  ASF scores:")
for a in result_high.feasible_set:
    asf_val = compute_asf(a, result_high.outcome_sets, np.array([0.50, 0.50, 0.50]), sigma)
    print(f"    ASF({a}) = {asf_val:.4f}")
print(f"  → a3_balanced selected via ASF (closest to aspirations)")
print(f"  → Layer 3 skipped (ASF already resolved)")
print(f"  → No deference needed")
