"""
Paper 3: Content Moderation — MOADT Worked Example

Scenario: An AI content moderation system must decide how to handle a borderline
social media post that contains political commentary with potentially misleading
health claims. The system manages five incommensurable objectives under genuine
uncertainty about the post's impact and disagreement about what constitutes "harm."

This example is designed to demonstrate MOADT on a problem where:
- Evaluator uncertainty (F) is the critical mechanism — different evaluators
  genuinely disagree about how to measure "harm" and "value of speech"
- The deference outcome is particularly natural and important
- The constraint (don't suppress clearly protected speech) interacts with
  evaluator disagreement about what counts as "clearly protected"

Actions (6 moderation responses):
  m1: No action (leave the post up, unmodified)
  m2: Add context label (append fact-check/context information)
  m3: Reduce distribution (algorithmically limit reach without removing)
  m4: Age-gate (restrict visibility to accounts 18+)
  m5: Remove with appeal (take down but allow the poster to appeal)
  m6: Remove without appeal (permanent removal)

States (3 impact scenarios):
  s1: Post goes viral — reaches millions, spawns derivatives
  s2: Moderate reach — seen by thousands, some discussion
  s3: Limited reach — seen by hundreds, minimal engagement

Objectives (k=5):
  f1: Free expression preservation (how well the action preserves speech, 0-1)
  f2: Harm prevention (how well the action prevents misinformation spread, 0-1)
  f3: User trust (how the action affects platform credibility, 0-1)
  f4: Consistency (how well the action aligns with past moderation decisions, 0-1)
  f5: Proportionality (how appropriate the action's severity is to the content, 0-1)

Credal set P = {P_viral, P_typical}:
  P_viral   = (0.30, 0.50, 0.20) — content team estimates this post has viral potential
  P_typical = (0.05, 0.45, 0.50) — analytics team says it's statistically typical

Evaluator set F = {f_speech, f_safety, f_moderate}:
  f_speech:   Free-speech-prioritizing evaluator — rates harm from borderline
              content lower, speech value higher, considers removal disproportionate
  f_safety:   Safety-prioritizing evaluator — rates harm from health misinformation
              higher, considers under-moderation a trust violation
  f_moderate: Centrist evaluator — balanced assessment, moderate scores

Constraints (Layer 1):
  Free expression (f1) >= 0.20 in ALL states — even the strictest moderation
  cannot suppress content that has significant speech value. This prevents
  automated total censorship.

  Proportionality (f5) >= 0.25 — the action must be at least minimally proportionate
  to the content. Removing satire with no appeal would violate this.

Reference point (Layer 2):
  r = (0.40, 0.40, 0.45, 0.40, 0.40) — "acceptable moderation"
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

actions = ["m1_no_action", "m2_context_label", "m3_reduce_dist",
           "m4_age_gate", "m5_remove_appeal", "m6_remove_permanent"]
states = ["s1_viral", "s2_moderate", "s3_limited"]
objectives = ["free_expression", "harm_prevention", "user_trust",
              "consistency", "proportionality"]

# Outcome matrices: outcomes[(action, state)] = array of shape (3, 5)
# Row 0 = f_speech evaluator, Row 1 = f_safety evaluator, Row 2 = f_moderate evaluator
# Columns = [free_expression, harm_prevention, user_trust, consistency, proportionality]

outcomes = {}

# m1: No action — maximum free expression, no harm prevention
outcomes[("m1_no_action", "s1_viral")] = np.array([
    [0.95, 0.15, 0.50, 0.60, 0.55],  # f_speech: sees little harm
    [0.95, 0.05, 0.30, 0.40, 0.30],  # f_safety: viral misinfo = big harm
    [0.95, 0.10, 0.40, 0.50, 0.40],  # f_moderate: middle ground
])
outcomes[("m1_no_action", "s2_moderate")] = np.array([
    [0.95, 0.30, 0.55, 0.60, 0.65],
    [0.95, 0.20, 0.40, 0.40, 0.45],
    [0.95, 0.25, 0.48, 0.50, 0.55],
])
outcomes[("m1_no_action", "s3_limited")] = np.array([
    [0.95, 0.60, 0.60, 0.60, 0.80],
    [0.95, 0.50, 0.50, 0.40, 0.70],
    [0.95, 0.55, 0.55, 0.50, 0.75],
])

# m2: Context label — preserves speech, adds information
outcomes[("m2_context_label", "s1_viral")] = np.array([
    [0.85, 0.40, 0.65, 0.65, 0.80],
    [0.80, 0.35, 0.55, 0.55, 0.70],
    [0.82, 0.38, 0.60, 0.60, 0.75],
])
outcomes[("m2_context_label", "s2_moderate")] = np.array([
    [0.85, 0.50, 0.65, 0.65, 0.85],
    [0.80, 0.45, 0.60, 0.55, 0.75],
    [0.82, 0.48, 0.62, 0.60, 0.80],
])
outcomes[("m2_context_label", "s3_limited")] = np.array([
    [0.85, 0.65, 0.65, 0.65, 0.85],
    [0.80, 0.60, 0.60, 0.55, 0.80],
    [0.82, 0.62, 0.62, 0.60, 0.82],
])

# m3: Reduce distribution — moderate intervention
outcomes[("m3_reduce_dist", "s1_viral")] = np.array([
    [0.60, 0.55, 0.50, 0.55, 0.60],
    [0.55, 0.60, 0.55, 0.60, 0.65],
    [0.58, 0.58, 0.52, 0.58, 0.62],
])
outcomes[("m3_reduce_dist", "s2_moderate")] = np.array([
    [0.60, 0.55, 0.55, 0.55, 0.60],
    [0.55, 0.60, 0.58, 0.60, 0.65],
    [0.58, 0.58, 0.56, 0.58, 0.62],
])
outcomes[("m3_reduce_dist", "s3_limited")] = np.array([
    [0.60, 0.55, 0.45, 0.55, 0.50],  # Overmoderation of limited-reach content
    [0.55, 0.60, 0.50, 0.60, 0.55],
    [0.58, 0.58, 0.48, 0.58, 0.52],
])

# m4: Age-gate — targeted restriction
outcomes[("m4_age_gate", "s1_viral")] = np.array([
    [0.55, 0.50, 0.45, 0.45, 0.50],
    [0.50, 0.55, 0.50, 0.50, 0.55],
    [0.52, 0.52, 0.48, 0.48, 0.52],
])
outcomes[("m4_age_gate", "s2_moderate")] = np.array([
    [0.55, 0.50, 0.48, 0.45, 0.55],
    [0.50, 0.55, 0.52, 0.50, 0.60],
    [0.52, 0.52, 0.50, 0.48, 0.58],
])
outcomes[("m4_age_gate", "s3_limited")] = np.array([
    [0.55, 0.50, 0.40, 0.45, 0.45],  # Weird to age-gate limited content
    [0.50, 0.55, 0.45, 0.50, 0.50],
    [0.52, 0.52, 0.42, 0.48, 0.48],
])

# m5: Remove with appeal — strong intervention
outcomes[("m5_remove_appeal", "s1_viral")] = np.array([
    [0.25, 0.75, 0.45, 0.50, 0.40],  # f_speech: sees this as disproportionate
    [0.30, 0.85, 0.60, 0.65, 0.65],  # f_safety: appropriate response
    [0.28, 0.80, 0.52, 0.58, 0.52],
])
outcomes[("m5_remove_appeal", "s2_moderate")] = np.array([
    [0.25, 0.70, 0.40, 0.50, 0.30],  # Overmoderation for moderate-reach
    [0.30, 0.80, 0.55, 0.65, 0.50],
    [0.28, 0.75, 0.48, 0.58, 0.40],
])
outcomes[("m5_remove_appeal", "s3_limited")] = np.array([
    [0.25, 0.65, 0.30, 0.50, 0.20],  # Clearly disproportionate for limited reach
    [0.30, 0.75, 0.45, 0.65, 0.35],
    [0.28, 0.70, 0.38, 0.58, 0.28],
])

# m6: Remove permanent — maximum intervention
outcomes[("m6_remove_permanent", "s1_viral")] = np.array([
    [0.10, 0.80, 0.35, 0.45, 0.25],
    [0.15, 0.90, 0.50, 0.60, 0.50],
    [0.12, 0.85, 0.42, 0.52, 0.38],
])
outcomes[("m6_remove_permanent", "s2_moderate")] = np.array([
    [0.10, 0.75, 0.25, 0.45, 0.15],  # Very disproportionate
    [0.15, 0.85, 0.40, 0.60, 0.30],
    [0.12, 0.80, 0.32, 0.52, 0.22],
])
outcomes[("m6_remove_permanent", "s3_limited")] = np.array([
    [0.10, 0.70, 0.15, 0.45, 0.10],  # Absurdly disproportionate
    [0.15, 0.80, 0.30, 0.60, 0.20],
    [0.12, 0.75, 0.22, 0.52, 0.15],
])

# Credal set
P_viral = np.array([0.30, 0.50, 0.20])
P_typical = np.array([0.05, 0.45, 0.50])
credal_probs = [P_viral, P_typical]

# Layer 1 constraints
# free_expression (index 0) >= 0.20
# proportionality (index 4) >= 0.25
constraints = {0: 0.20, 4: 0.25}

# Layer 2 reference point
reference_point = np.array([0.40, 0.40, 0.45, 0.40, 0.40])

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

print("=" * 70)
print("MOADT WORKED EXAMPLE 3: CONTENT MODERATION")
print("=" * 70)

# Show raw outcomes for key actions
print("\n" + "=" * 70)
print("RAW OUTCOME DATA")
print("=" * 70)
for a in actions:
    short = a.split('_', 1)[1]
    print(f"\n{a}:")
    print(f"  {'State':<12} {'Evaluator':<12} {'FreeExpr':>8} {'Harm':>8} {'Trust':>8} {'Consist':>8} {'Proport':>8}")
    print(f"  {'-'*12} {'-'*12} {'-'*8} {'-'*8} {'-'*8} {'-'*8} {'-'*8}")
    for s in states:
        o = outcomes[(a, s)]
        for f_idx, f_name in enumerate(["f_speech", "f_safety", "f_moderate"]):
            print(f"  {s if f_idx == 0 else '':<12} {f_name:<12}", end="")
            for j in range(5):
                print(f" {o[f_idx][j]:>8.2f}", end="")
            print()

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
pf_labels = ["(P_viral, f_speech)", "(P_viral, f_safety)", "(P_viral, f_moderate)",
             "(P_typical, f_speech)", "(P_typical, f_safety)", "(P_typical, f_moderate)"]
for a in actions:
    print(f"\n{a}:")
    print(f"  {'(P, f) pair':<25} {'FreeExpr':>8} {'Harm':>8} {'Trust':>8} {'Consist':>8} {'Proport':>8}")
    print(f"  {'-'*25} {'-'*8} {'-'*8} {'-'*8} {'-'*8} {'-'*8}")
    for i, label in enumerate(pf_labels):
        y = result.outcome_sets[a][i]
        print(f"  {label:<25}", end="")
        for j in range(5):
            print(f" {y[j]:>8.4f}", end="")
        print()

# Constraint analysis
print("\n" + "=" * 70)
print("LAYER 1: CONSTRAINT ANALYSIS")
print("(free_expression >= 0.20 AND proportionality >= 0.25 per state)")
print("=" * 70)
for a in actions:
    print(f"\n  {a}:")
    violated = False
    for s in states:
        o = outcomes[(a, s)]
        for f_idx, f_name in enumerate(["f_speech", "f_safety", "f_moderate"]):
            fe_val = o[f_idx][0]
            prop_val = o[f_idx][4]
            fe_status = "✓" if fe_val >= 0.20 else "✗"
            prop_status = "✓" if prop_val >= 0.25 else "✗"
            if fe_val < 0.20 or prop_val < 0.20:
                violated = True
            issue = ""
            if fe_val < 0.20:
                issue += f" FE={fe_val:.2f}<0.20"
                violated = True
            if prop_val < 0.25:
                issue += f" PROP={prop_val:.2f}<0.25"
                violated = True
            if issue:
                print(f"    {s}, {f_name}: {issue}")
    if violated:
        print(f"    Overall: FAIL — excluded from C")
    else:
        print(f"    Overall: PASS")

# Scalar EU comparison
print("\n" + "=" * 70)
print("COMPARISON: SCALAR EXPECTED UTILITY")
print("=" * 70)

weight_sets = [
    ("Free-speech heavy (0.40, 0.15, 0.15, 0.15, 0.15)",
     np.array([0.40, 0.15, 0.15, 0.15, 0.15])),
    ("Safety heavy (0.15, 0.40, 0.15, 0.15, 0.15)",
     np.array([0.15, 0.40, 0.15, 0.15, 0.15])),
    ("Equal weights (0.20, 0.20, 0.20, 0.20, 0.20)",
     np.array([0.20, 0.20, 0.20, 0.20, 0.20])),
]

for w_name, weights in weight_sets:
    print(f"\n  {w_name}:")
    for p_idx, p_name in enumerate(["P_viral", "P_typical"]):
        for f_idx, f_name in enumerate(["f_speech", "f_safety", "f_moderate"]):
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
if result.regret_vectors:
    print(f"  Regret-Pareto R:    {[a.split('_',1)[1] for a in result.regret_pareto_set]}")
print(f"  Deference needed:   {result.deference_needed}")
if result.deference_needed:
    print(f"\n  FINAL RESULT: Defer to human moderator.")
    print(f"  Present options with regret profiles:")
    for a in result.regret_pareto_set:
        print(f"    ρ({a.split('_',1)[1]}) = {np.round(result.regret_vectors[a], 4)}")
    print(f"\n  KEY INSIGHT: The evaluator disagreement is the story here.")
    print(f"  f_speech and f_safety genuinely disagree about what 'harm' means")
    print(f"  for this borderline content. MOADT identifies the disagreement,")
    print(f"  narrows the options to those that respect both safety constraints")
    print(f"  and speech protections, and defers the value judgment to a human.")
elif result.regret_pareto_set:
    print(f"\n  FINAL RESULT: Recommend {result.regret_pareto_set[0].split('_',1)[1]}")
