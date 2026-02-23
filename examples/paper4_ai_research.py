"""
Paper 4: AI Research Assistant Response Selection — MOADT Worked Example

Scenario: An AI research assistant receives a query about a dual-use topic —
the user asks for detailed information about gain-of-function research methods.
The system must decide how to respond, managing multiple incommensurable objectives
under genuine uncertainty about the user's intent and disagreement about what
constitutes responsible information sharing.

This example is designed to demonstrate MOADT on the most alignment-relevant
problem: an AI system deciding its own behavior. It features:
- The objectives directly encode alignment desiderata (helpfulness, safety,
  honesty, user autonomy, epistemic contribution)
- The credal set captures uncertainty about user intent (the classic dual-use problem)
- The evaluator set captures different alignment philosophies
- The constraint layer encodes non-negotiable safety floors
- The deference outcome maps directly to human oversight

Actions (6 response strategies):
  r1: Full technical answer (comprehensive, detailed explanation with specifics)
  r2: Educational overview (conceptual depth, no specific protocols/sequences)
  r3: Contextualized answer (full answer with safety framing and ethical context)
  r4: Partial answer with redirect (basics + redirect to supervised resources)
  r5: Decline with explanation (refuse, explain reasoning transparently)
  r6: Decline without explanation (refuse, provide no reasoning)

States (4 user intent profiles):
  s1: Legitimate researcher (needs this for beneficial scientific work)
  s2: Student/curious learner (educational interest, no harmful intent)
  s3: Journalist/policy analyst (investigating for public interest reporting)
  s4: Malicious actor (attempting to use information for harmful purposes)

Objectives (k=5):
  f1: Helpfulness (how well the response serves the user's legitimate needs)
  f2: Safety (how well the response prevents potential misuse of information)
  f3: Honesty (how transparent and non-deceptive the response is)
  f4: User autonomy (respect for the user's right to seek information)
  f5: Epistemic contribution (whether the response advances understanding)

Credal set P = {P_trusting, P_cautious}:
  P_trusting = (0.35, 0.40, 0.15, 0.10) — most users are legitimate
  P_cautious = (0.15, 0.25, 0.10, 0.50) — significant portion may be malicious

Evaluator set F = {f_capability, f_safety, f_balanced}:
  f_capability: Emphasizes helpfulness, autonomy, and epistemic contribution.
                Believes restricting information is itself a harm (paternalism).
                Rates refusal strategies poorly on honesty (evasion = dishonesty).
  f_safety:     Emphasizes safety and cautious information sharing.
                Rates full disclosure as irresponsible even for researchers
                (information doesn't stay with intended recipient).
                Rates refusal strategies well on safety and honesty (clear communication).
  f_balanced:   Middle ground — full answers are great for researchers but
                worrisome for unknown users; refusals are safe but costly.

Constraints (Layer 1):
  Safety (f2) >= 0.25 in ALL states — response must not be catastrophically
  unsafe even if the user turns out to be a malicious actor.

  Honesty (f3) >= 0.30 in ALL states — the AI must not be fundamentally
  deceptive in any response strategy (no gaslighting, no hidden manipulation).

Reference point (Layer 2):
  r = (0.35, 0.40, 0.45, 0.30, 0.30) — "acceptable AI assistant behavior"
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

actions = ["r1_full_technical", "r2_educational", "r3_contextualized",
           "r4_partial_redirect", "r5_decline_explain", "r6_decline_silent"]
states = ["s1_researcher", "s2_student", "s3_journalist", "s4_malicious"]
objectives = ["helpfulness", "safety", "honesty", "user_autonomy",
              "epistemic_contribution"]

# Outcome matrices: outcomes[(action, state)] = array of shape (3, 5)
# Row 0 = f_capability evaluator, Row 1 = f_safety evaluator, Row 2 = f_balanced
# Columns = [helpfulness, safety, honesty, user_autonomy, epistemic_contribution]

outcomes = {}

# r1: Full technical answer — maximally helpful but potentially dangerous
# For a researcher, this is exactly what they need
# For a malicious actor, this provides actionable dangerous information
outcomes[("r1_full_technical", "s1_researcher")] = np.array([
    [0.95, 0.70, 0.90, 0.95, 0.95],  # capability: excellent
    [0.90, 0.40, 0.85, 0.90, 0.85],  # safety: helpful but worrisome
    [0.92, 0.55, 0.88, 0.92, 0.90],  # balanced: great for researchers
])
outcomes[("r1_full_technical", "s2_student")] = np.array([
    [0.85, 0.60, 0.90, 0.90, 0.80],  # May be more than student needs
    [0.80, 0.35, 0.85, 0.85, 0.70],  # Oversharing with student
    [0.82, 0.48, 0.88, 0.88, 0.75],
])
outcomes[("r1_full_technical", "s3_journalist")] = np.array([
    [0.80, 0.55, 0.90, 0.85, 0.70],  # Helpful for investigation
    [0.75, 0.30, 0.85, 0.80, 0.60],  # Risk of publication
    [0.78, 0.42, 0.88, 0.82, 0.65],
])
outcomes[("r1_full_technical", "s4_malicious")] = np.array([
    [0.90, 0.10, 0.90, 0.90, 0.60],  # capability: "helped" the bad actor
    [0.85, 0.05, 0.80, 0.85, 0.30],  # safety: catastrophic failure
    [0.88, 0.08, 0.85, 0.88, 0.45],  # balanced: terrible outcome
])

# r2: Educational overview — conceptual understanding without specifics
outcomes[("r2_educational", "s1_researcher")] = np.array([
    [0.55, 0.80, 0.75, 0.70, 0.60],  # capability: insufficient for research
    [0.60, 0.75, 0.80, 0.75, 0.65],  # safety: reasonable
    [0.58, 0.78, 0.78, 0.72, 0.62],  # balanced
])
outcomes[("r2_educational", "s2_student")] = np.array([
    [0.80, 0.85, 0.80, 0.80, 0.85],  # Actually perfect for students
    [0.75, 0.80, 0.82, 0.78, 0.80],
    [0.78, 0.82, 0.81, 0.79, 0.82],
])
outcomes[("r2_educational", "s3_journalist")] = np.array([
    [0.70, 0.82, 0.78, 0.75, 0.70],  # Good for background understanding
    [0.65, 0.80, 0.80, 0.72, 0.68],
    [0.68, 0.81, 0.79, 0.74, 0.69],
])
outcomes[("r2_educational", "s4_malicious")] = np.array([
    [0.50, 0.70, 0.75, 0.65, 0.35],  # capability: unhelpful to bad actor
    [0.45, 0.75, 0.78, 0.60, 0.30],  # safety: limited damage
    [0.48, 0.72, 0.76, 0.62, 0.32],
])

# r3: Contextualized answer — full info but with safety/ethics framing
outcomes[("r3_contextualized", "s1_researcher")] = np.array([
    [0.88, 0.72, 0.92, 0.88, 0.90],  # Almost as helpful, better honesty
    [0.82, 0.50, 0.90, 0.82, 0.82],  # safety: slightly better than r1
    [0.85, 0.60, 0.91, 0.85, 0.86],
])
outcomes[("r3_contextualized", "s2_student")] = np.array([
    [0.82, 0.65, 0.92, 0.85, 0.78],  # Great for students — context helps
    [0.78, 0.45, 0.90, 0.80, 0.70],
    [0.80, 0.55, 0.91, 0.82, 0.74],
])
outcomes[("r3_contextualized", "s3_journalist")] = np.array([
    [0.82, 0.60, 0.92, 0.82, 0.72],  # Good — context adds value
    [0.75, 0.38, 0.90, 0.78, 0.62],
    [0.78, 0.48, 0.91, 0.80, 0.67],
])
outcomes[("r3_contextualized", "s4_malicious")] = np.array([
    [0.85, 0.12, 0.92, 0.85, 0.55],  # Still dangerous if user ignores context
    [0.80, 0.08, 0.85, 0.80, 0.35],  # safety: context doesn't stop bad actors
    [0.82, 0.10, 0.88, 0.82, 0.45],
])

# r4: Partial answer with redirect — basics + pointer to supervised channels
outcomes[("r4_partial_redirect", "s1_researcher")] = np.array([
    [0.45, 0.82, 0.70, 0.60, 0.45],  # capability: frustrating for researcher
    [0.50, 0.80, 0.75, 0.65, 0.50],  # safety: good, researcher can follow up
    [0.48, 0.81, 0.72, 0.62, 0.48],
])
outcomes[("r4_partial_redirect", "s2_student")] = np.array([
    [0.65, 0.88, 0.72, 0.70, 0.60],  # Reasonable for students
    [0.60, 0.85, 0.75, 0.68, 0.55],
    [0.62, 0.86, 0.74, 0.69, 0.58],
])
outcomes[("r4_partial_redirect", "s3_journalist")] = np.array([
    [0.55, 0.85, 0.70, 0.65, 0.50],  # Somewhat helpful
    [0.50, 0.82, 0.73, 0.62, 0.45],
    [0.52, 0.84, 0.72, 0.64, 0.48],
])
outcomes[("r4_partial_redirect", "s4_malicious")] = np.array([
    [0.40, 0.80, 0.70, 0.55, 0.25],  # Limited harm
    [0.35, 0.85, 0.75, 0.50, 0.20],
    [0.38, 0.82, 0.72, 0.52, 0.22],
])

# r5: Decline with explanation — refuse but explain why transparently
outcomes[("r5_decline_explain", "s1_researcher")] = np.array([
    [0.15, 0.90, 0.80, 0.30, 0.10],  # capability: terrible for researcher
    [0.20, 0.92, 0.85, 0.35, 0.15],  # safety: maximally safe
    [0.18, 0.91, 0.82, 0.32, 0.12],
])
outcomes[("r5_decline_explain", "s2_student")] = np.array([
    [0.20, 0.92, 0.82, 0.35, 0.15],  # Unhelpful but honest
    [0.25, 0.95, 0.85, 0.40, 0.20],
    [0.22, 0.94, 0.84, 0.38, 0.18],
])
outcomes[("r5_decline_explain", "s3_journalist")] = np.array([
    [0.15, 0.92, 0.82, 0.30, 0.10],
    [0.20, 0.95, 0.85, 0.35, 0.15],
    [0.18, 0.94, 0.84, 0.32, 0.12],
])
outcomes[("r5_decline_explain", "s4_malicious")] = np.array([
    [0.10, 0.95, 0.80, 0.25, 0.05],  # Correct refusal
    [0.15, 0.98, 0.88, 0.30, 0.10],
    [0.12, 0.96, 0.84, 0.28, 0.08],
])

# r6: Decline without explanation — refuse, give no reasoning
outcomes[("r6_decline_silent", "s1_researcher")] = np.array([
    [0.05, 0.92, 0.30, 0.15, 0.05],  # capability: worst possible
    [0.10, 0.95, 0.40, 0.20, 0.08],  # safety: very safe but dishonest
    [0.08, 0.94, 0.35, 0.18, 0.06],
])
outcomes[("r6_decline_silent", "s2_student")] = np.array([
    [0.08, 0.94, 0.32, 0.18, 0.06],  # Confusing and unhelpful
    [0.12, 0.96, 0.42, 0.22, 0.10],
    [0.10, 0.95, 0.38, 0.20, 0.08],
])
outcomes[("r6_decline_silent", "s3_journalist")] = np.array([
    [0.05, 0.94, 0.28, 0.15, 0.05],  # Terrible — looks like hiding something
    [0.10, 0.96, 0.38, 0.20, 0.08],
    [0.08, 0.95, 0.32, 0.18, 0.06],
])
outcomes[("r6_decline_silent", "s4_malicious")] = np.array([
    [0.05, 0.96, 0.30, 0.10, 0.03],
    [0.10, 0.98, 0.40, 0.15, 0.05],
    [0.08, 0.97, 0.35, 0.12, 0.04],
])

# Credal set
P_trusting = np.array([0.35, 0.40, 0.15, 0.10])
P_cautious = np.array([0.15, 0.25, 0.10, 0.50])
credal_probs = [P_trusting, P_cautious]

# Layer 1 constraints
# safety (index 1) >= 0.25
# honesty (index 2) >= 0.30
constraints = {1: 0.25, 2: 0.30}

# Layer 2 reference point
reference_point = np.array([0.35, 0.40, 0.45, 0.30, 0.30])

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
print("MOADT WORKED EXAMPLE 4: AI RESEARCH ASSISTANT")
print("=" * 70)

# Show raw outcomes
print("\n" + "=" * 70)
print("RAW OUTCOME DATA")
print("=" * 70)
for a in actions:
    short = a.split('_', 1)[1]
    print(f"\n{a}:")
    print(f"  {'State':<15} {'Evaluator':<12} {'Helpful':>8} {'Safety':>8} {'Honest':>8} {'Auton.':>8} {'Epist.':>8}")
    print(f"  {'-'*15} {'-'*12} {'-'*8} {'-'*8} {'-'*8} {'-'*8} {'-'*8}")
    for s in states:
        o = outcomes[(a, s)]
        for f_idx, f_name in enumerate(["f_capab", "f_safety", "f_balanced"]):
            print(f"  {s if f_idx == 0 else '':<15} {f_name:<12}", end="")
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
pf_labels = ["(P_trust, f_capab)", "(P_trust, f_safety)", "(P_trust, f_balanced)",
             "(P_caut, f_capab)", "(P_caut, f_safety)", "(P_caut, f_balanced)"]
for a in actions:
    print(f"\n{a}:")
    print(f"  {'(P, f) pair':<22} {'Helpful':>8} {'Safety':>8} {'Honest':>8} {'Auton.':>8} {'Epist.':>8}")
    print(f"  {'-'*22} {'-'*8} {'-'*8} {'-'*8} {'-'*8} {'-'*8}")
    for i, label in enumerate(pf_labels):
        y = result.outcome_sets[a][i]
        print(f"  {label:<22}", end="")
        for j in range(5):
            print(f" {y[j]:>8.4f}", end="")
        print()

# Constraint analysis
print("\n" + "=" * 70)
print("LAYER 1: CONSTRAINT ANALYSIS")
print("(safety >= 0.25 AND honesty >= 0.30 per state, per evaluator)")
print("=" * 70)
for a in actions:
    print(f"\n  {a}:")
    violated = False
    for s in states:
        o = outcomes[(a, s)]
        for f_idx, f_name in enumerate(["f_capab", "f_safety", "f_balanced"]):
            safety_val = o[f_idx][1]
            honesty_val = o[f_idx][2]
            issue = ""
            if safety_val < 0.25:
                issue += f" SAFETY={safety_val:.2f}<0.25"
                violated = True
            if honesty_val < 0.30:
                issue += f" HONESTY={honesty_val:.2f}<0.30"
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
    ("Helpfulness-focused (0.40, 0.15, 0.15, 0.15, 0.15)",
     np.array([0.40, 0.15, 0.15, 0.15, 0.15])),
    ("Safety-focused (0.15, 0.40, 0.15, 0.15, 0.15)",
     np.array([0.15, 0.40, 0.15, 0.15, 0.15])),
    ("Equal weights (0.20, 0.20, 0.20, 0.20, 0.20)",
     np.array([0.20, 0.20, 0.20, 0.20, 0.20])),
    ("Honesty-focused (0.15, 0.15, 0.40, 0.15, 0.15)",
     np.array([0.15, 0.15, 0.40, 0.15, 0.15])),
]

for w_name, weights in weight_sets:
    print(f"\n  {w_name}:")
    for p_idx, p_name in enumerate(["P_trusting", "P_cautious"]):
        for f_idx, f_name in enumerate(["f_capab", "f_safety", "f_balanced"]):
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
    print(f"\n  FINAL RESULT: Defer to human oversight.")
    print(f"  Present options with regret profiles:")
    for a in result.regret_pareto_set:
        print(f"    ρ({a.split('_',1)[1]}) = {np.round(result.regret_vectors[a], 4)}")
    print(f"\n  KEY INSIGHT: This is MOADT applied to AI alignment directly.")
    print(f"  The system cannot determine whether helpfulness or safety should")
    print(f"  dominate because the evaluators genuinely disagree. Deference")
    print(f"  to human oversight is not a failure — it is the rational response")
    print(f"  to genuine value uncertainty in the AI's own decision-making.")
elif result.regret_pareto_set:
    print(f"\n  FINAL RESULT: Recommend {result.regret_pareto_set[0].split('_',1)[1]}")
