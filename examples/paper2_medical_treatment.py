"""
Paper 2: Medical Treatment Selection — MOADT Worked Example

Scenario: A clinical decision support system must recommend a treatment plan for
a patient with a chronic condition. The system manages four incommensurable
objectives under genuine uncertainty about the patient's response profile and
disagreement about outcome measurement.

Actions (6 treatment plans):
  t1: Standard monotherapy (well-established, moderate efficacy)
  t2: Aggressive monotherapy (higher dose, higher efficacy, more side effects)
  t3: Combination therapy A (two drugs, good efficacy, complex interactions)
  t4: Combination therapy B (two drugs, different profile)
  t5: Experimental therapy (clinical trial, high variance)
  t6: Watchful waiting (minimal intervention, monitor progression)

States (4 patient response profiles):
  s1: Strong responder (30% of similar patients historically)
  s2: Moderate responder (40%)
  s3: Weak responder (20%)
  s4: Adverse reactor (10% — experiences unusual drug sensitivities)

Objectives (k=4):
  f1: Efficacy (disease progression control, 0-1 scale)
  f2: Safety (inverse of side effect severity, 0-1 scale, higher = safer)
  f3: Patient autonomy (treatment burden — lower burden = more autonomy, 0-1)
  f4: Cost efficiency (inverse of cost normalized, 0-1 scale, higher = cheaper)

Credal set P = {P_clinical, P_cautious}:
  P_clinical = (0.30, 0.40, 0.20, 0.10) — based on clinical trial demographics
  P_cautious = (0.20, 0.35, 0.25, 0.20) — adjusted for this patient's risk factors

Evaluator set F = {f_trial, f_realworld}:
  f_trial: Outcomes as measured in controlled clinical trials
  f_realworld: Real-world effectiveness (efficacy reduced by 15-20% due to
               adherence issues; side effects increased by 10% due to comorbidities;
               trial-measured autonomy scores deflated by 15%)

Constraints (Layer 1):
  Safety (f2) >= 0.35 in ALL states — patient must not face life-threatening
  side effects under any response profile. This is non-negotiable.

Reference point (Layer 2):
  r = (0.40, 0.50, 0.30, 0.30) — "clinically acceptable minimum"
"""

import numpy as np
from moadt import (
    MOADTProblem, compute_outcome_sets, run_moadt_protocol,
    print_trace, scalar_eu_analysis, pareto_dominates, robustly_dominates,
    compute_asf, compute_regret_vectors
)

# =============================================================================
# PROBLEM SPECIFICATION
# =============================================================================

actions = ["t1_standard", "t2_aggressive", "t3_combo_A", "t4_combo_B",
           "t5_experimental", "t6_watchful"]
states = ["s1_strong", "s2_moderate", "s3_weak", "s4_adverse"]
objectives = ["efficacy", "safety", "autonomy", "cost_efficiency"]

# Outcome matrices: outcomes[(action, state)] = array of shape (2, 4)
# Row 0 = f_trial evaluation, Row 1 = f_realworld evaluation
# Columns = [efficacy, safety, autonomy, cost_efficiency]

outcomes = {}

# t1: Standard monotherapy — reliable, moderate everything
outcomes[("t1_standard", "s1_strong")] = np.array([
    [0.75, 0.80, 0.70, 0.80],  # trial
    [0.62, 0.72, 0.60, 0.80],  # realworld
])
outcomes[("t1_standard", "s2_moderate")] = np.array([
    [0.60, 0.80, 0.70, 0.80],
    [0.50, 0.72, 0.60, 0.80],
])
outcomes[("t1_standard", "s3_weak")] = np.array([
    [0.35, 0.80, 0.70, 0.80],
    [0.28, 0.72, 0.60, 0.80],
])
outcomes[("t1_standard", "s4_adverse")] = np.array([
    [0.30, 0.55, 0.70, 0.80],
    [0.25, 0.50, 0.60, 0.80],
])

# t2: Aggressive monotherapy — higher efficacy, worse safety profile
outcomes[("t2_aggressive", "s1_strong")] = np.array([
    [0.90, 0.60, 0.50, 0.70],
    [0.75, 0.54, 0.43, 0.70],
])
outcomes[("t2_aggressive", "s2_moderate")] = np.array([
    [0.75, 0.55, 0.50, 0.70],
    [0.62, 0.50, 0.43, 0.70],
])
outcomes[("t2_aggressive", "s3_weak")] = np.array([
    [0.50, 0.50, 0.50, 0.70],
    [0.40, 0.45, 0.43, 0.70],
])
outcomes[("t2_aggressive", "s4_adverse")] = np.array([
    [0.45, 0.25, 0.50, 0.70],  # Safety below threshold for adverse reactors!
    [0.38, 0.23, 0.43, 0.70],
])

# t3: Combination therapy A — good efficacy, complex side effect profile
outcomes[("t3_combo_A", "s1_strong")] = np.array([
    [0.85, 0.65, 0.45, 0.50],
    [0.70, 0.59, 0.38, 0.50],
])
outcomes[("t3_combo_A", "s2_moderate")] = np.array([
    [0.70, 0.60, 0.45, 0.50],
    [0.58, 0.54, 0.38, 0.50],
])
outcomes[("t3_combo_A", "s3_weak")] = np.array([
    [0.55, 0.55, 0.45, 0.50],
    [0.44, 0.50, 0.38, 0.50],
])
outcomes[("t3_combo_A", "s4_adverse")] = np.array([
    [0.40, 0.30, 0.45, 0.50],  # Safety below threshold!
    [0.33, 0.27, 0.38, 0.50],
])

# t4: Combination therapy B — different tradeoff profile
outcomes[("t4_combo_B", "s1_strong")] = np.array([
    [0.80, 0.70, 0.40, 0.45],
    [0.66, 0.63, 0.34, 0.45],
])
outcomes[("t4_combo_B", "s2_moderate")] = np.array([
    [0.65, 0.70, 0.40, 0.45],
    [0.54, 0.63, 0.34, 0.45],
])
outcomes[("t4_combo_B", "s3_weak")] = np.array([
    [0.50, 0.65, 0.40, 0.45],
    [0.40, 0.59, 0.34, 0.45],
])
outcomes[("t4_combo_B", "s4_adverse")] = np.array([
    [0.35, 0.45, 0.40, 0.45],
    [0.29, 0.41, 0.34, 0.45],
])

# t5: Experimental therapy — high variance, high ceiling
outcomes[("t5_experimental", "s1_strong")] = np.array([
    [0.95, 0.70, 0.55, 0.30],
    [0.80, 0.63, 0.47, 0.30],
])
outcomes[("t5_experimental", "s2_moderate")] = np.array([
    [0.70, 0.65, 0.55, 0.30],
    [0.58, 0.59, 0.47, 0.30],
])
outcomes[("t5_experimental", "s3_weak")] = np.array([
    [0.30, 0.60, 0.55, 0.30],
    [0.24, 0.54, 0.47, 0.30],
])
outcomes[("t5_experimental", "s4_adverse")] = np.array([
    [0.20, 0.35, 0.55, 0.30],  # Safety right at threshold
    [0.16, 0.32, 0.47, 0.30],  # Safety below threshold under realworld!
])

# t6: Watchful waiting — safe, autonomous, cheap, but low efficacy
outcomes[("t6_watchful", "s1_strong")] = np.array([
    [0.40, 0.95, 0.90, 0.95],
    [0.35, 0.86, 0.77, 0.95],
])
outcomes[("t6_watchful", "s2_moderate")] = np.array([
    [0.25, 0.95, 0.90, 0.95],
    [0.21, 0.86, 0.77, 0.95],
])
outcomes[("t6_watchful", "s3_weak")] = np.array([
    [0.15, 0.95, 0.90, 0.95],
    [0.12, 0.86, 0.77, 0.95],
])
outcomes[("t6_watchful", "s4_adverse")] = np.array([
    [0.10, 0.95, 0.90, 0.95],
    [0.08, 0.86, 0.77, 0.95],
])

# Credal set
P_clinical = np.array([0.30, 0.40, 0.20, 0.10])
P_cautious = np.array([0.20, 0.35, 0.25, 0.20])
credal_probs = [P_clinical, P_cautious]

# Layer 1 constraints: safety (index 1) >= 0.35 per state
constraints = {1: 0.35}

# Layer 2 reference point: clinically acceptable minimum
# Autonomy aspiration set to 0.30 (acknowledging combination therapies
# inherently have higher treatment burden)
reference_point = np.array([0.40, 0.50, 0.30, 0.30])

# Normalization factors for ASF
sigma = np.array([1.0, 1.0, 1.0, 1.0])

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
print("MOADT WORKED EXAMPLE 2: MEDICAL TREATMENT SELECTION")
print("=" * 70)

# Show raw outcomes for selected actions
print("\n" + "=" * 70)
print("RAW OUTCOME DATA (selected actions)")
print("=" * 70)
for a in actions:
    short = a.split('_', 1)[1]
    print(f"\n{a}:")
    print(f"  {'State':<15} {'Evaluator':<12} {'Efficacy':>8} {'Safety':>8} {'Auton.':>8} {'Cost':>8}")
    print(f"  {'-'*15} {'-'*12} {'-'*8} {'-'*8} {'-'*8} {'-'*8}")
    for s in states:
        o = outcomes[(a, s)]
        print(f"  {s:<15} {'trial':<12} {o[0][0]:>8.2f} {o[0][1]:>8.2f} {o[0][2]:>8.2f} {o[0][3]:>8.2f}")
        print(f"  {'':<15} {'realworld':<12} {o[1][0]:>8.2f} {o[1][1]:>8.2f} {o[1][2]:>8.2f} {o[1][3]:>8.2f}")

# Run full protocol
result = run_moadt_protocol(problem)

print("\n" + "=" * 70)
print("MOADT PROTOCOL EXECUTION")
print("=" * 70)
print_trace(result)

# Detailed outcome sets
print("\n" + "=" * 70)
print("OUTCOME SETS Y(a) — Full Detail")
print("=" * 70)
pf_labels = ["(P_clin, f_trial)", "(P_clin, f_real)", "(P_caut, f_trial)", "(P_caut, f_real)"]
for a in actions:
    print(f"\n{a}:")
    print(f"  {'(P, f) pair':<22} {'Efficacy':>8} {'Safety':>8} {'Auton.':>8} {'Cost':>8}")
    print(f"  {'-'*22} {'-'*8} {'-'*8} {'-'*8} {'-'*8}")
    for i, label in enumerate(pf_labels):
        y = result.outcome_sets[a][i]
        print(f"  {label:<22} {y[0]:>8.4f} {y[1]:>8.4f} {y[2]:>8.4f} {y[3]:>8.4f}")

# Constraint analysis
print("\n" + "=" * 70)
print("LAYER 1: CONSTRAINT ANALYSIS (safety >= 0.35 per state)")
print("=" * 70)
for a in actions:
    print(f"\n  {a}:")
    violated = False
    for s in states:
        o = outcomes[(a, s)]
        for f_idx, f_name in enumerate(["trial", "realworld"]):
            val = o[f_idx][1]  # safety is index 1
            status = "✓" if val >= 0.35 else "✗ VIOLATION"
            if val < 0.35:
                violated = True
            print(f"    {s}, {f_name}: safety = {val:.2f} {status}")
    print(f"    Overall: {'PASS' if not violated else 'FAIL — excluded'}")

# Scalar EU comparison
print("\n" + "=" * 70)
print("COMPARISON: SCALAR EXPECTED UTILITY")
print("=" * 70)

weight_sets = [
    ("Efficacy-focused (0.5, 0.2, 0.15, 0.15)", np.array([0.50, 0.20, 0.15, 0.15])),
    ("Safety-focused (0.2, 0.5, 0.15, 0.15)", np.array([0.20, 0.50, 0.15, 0.15])),
    ("Equal weights (0.25, 0.25, 0.25, 0.25)", np.array([0.25, 0.25, 0.25, 0.25])),
    ("Autonomy-focused (0.2, 0.2, 0.4, 0.2)", np.array([0.20, 0.20, 0.40, 0.20])),
]

for w_name, weights in weight_sets:
    print(f"\n  {w_name}:")
    for p_idx, p_name in enumerate(["P_clinical", "P_cautious"]):
        for f_idx, f_name in enumerate(["f_trial", "f_real"]):
            scores = scalar_eu_analysis(problem, weights, p_idx, f_idx)
            best = max(scores, key=scores.get)
            print(f"    {p_name}, {f_name}: ", end="")
            for a in actions:
                short = a.split('_')[0]
                marker = " ←" if a == best else ""
                print(f"{short}={scores[a]:.3f}{marker} ", end="")
            print()

# Summary
print("\n" + "=" * 70)
print("PROTOCOL SUMMARY")
print("=" * 70)
print(f"  Actions:            {[a.split('_',1)[1] for a in actions]}")
print(f"  Adm(A):             {[a.split('_',1)[1] for a in result.admissible_set]}")
print(f"  C (constraints):    {[a.split('_',1)[1] for a in result.constraint_set]}")
print(f"  F = Adm(C):         {[a.split('_',1)[1] for a in result.feasible_set]}")
print(f"  Sat(F, r):          {[a.split('_',1)[1] for a in result.satisficing_set]}")
print(f"  ASF fallback used:  {result.sat_fallback_used}")
if result.sat_fallback_used:
    print(f"  ASF selection:      {[a.split('_',1)[1] for a in result.asf_selection]}")
print(f"  Regret-Pareto R:    {[a.split('_',1)[1] for a in result.regret_pareto_set]}")
print(f"  Deference needed:   {result.deference_needed}")
if result.deference_needed:
    print(f"\n  FINAL RESULT: Defer to clinician/patient.")
    print(f"  Present options with regret profiles:")
    for a in result.regret_pareto_set:
        print(f"    ρ({a.split('_',1)[1]}) = {np.round(result.regret_vectors[a], 4)}")
    print(f"\n  The tradeoff presented to the clinician:")
    print(f"  These treatments differ in how they balance efficacy against")
    print(f"  safety, autonomy, and cost. MOADT identifies the tradeoff;")
    print(f"  the patient and clinician make the value judgment.")
else:
    print(f"\n  FINAL RESULT: Recommend {result.regret_pareto_set[0].split('_',1)[1]}")
