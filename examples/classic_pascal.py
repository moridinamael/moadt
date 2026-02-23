"""
Classic Decision Theory Problem: Pascal's Mugging — MOADT Worked Example

Scenario: A stranger approaches you on the street and says: "Give me $5, and
I will use my magic powers to give you $1,000,000,000,000 (a trillion dollars)
tomorrow." The probability they are telling the truth is astronomically low.
But under standard expected utility (EU) theory:

    EU(pay) = (1/10^9) * $10^12 - $5 = $1000 - $5 = $995
    EU(refuse) = $0

EU says PAY — which is absurd. Worse, the mugger can always increase the
promised amount to overcome any probability discount. This is a fundamental
failure mode of scalar EU maximization.

MOADT FORMULATION
=================

Actions (3):
  pay:         Give the mugger $5
  refuse:      Keep your $5, walk away
  investigate: Demand evidence first, delay decision (costs small effort)

States (2):
  truthful:    The mugger really has magic powers (astronomically unlikely)
  lying:       The mugger is a con artist (near certain)

Objectives (k=4):
  O1: net_monetary_value   — Expected financial outcome (normalized to [0,1])
  O2: downside_protection  — How protected you are from loss in worst case
  O3: epistemic_integrity  — Are you acting on well-founded evidence?
  O4: resource_preservation — Do you keep your current resources?

  The key insight: scalar EU collapses these into one dimension (O1 alone,
  or a weighted sum dominated by O1). MOADT treats them as genuinely
  incommensurable. The mugger exploits O1 with an astronomical payoff,
  but cannot simultaneously satisfy O2, O3, and O4.

Credal set P = {P_generous, P_realistic}:
  P_generous  = (10^-6, 1 - 10^-6)  — absurdly generous: 1 in a million
  P_realistic = (10^-9, 1 - 10^-9)  — realistic: 1 in a billion

  Multiple priors model genuine uncertainty about how to assign probability
  to extraordinary claims. The mugger's argument works under ANY single prior
  (just increase the payoff); the credal set blocks this by requiring
  robustness across priors.

Evaluator set F = {face_value, skeptical}:
  face_value: Takes the claimed $1T payoff at face value
  skeptical:  Caps plausible payoff at $10,000 — even if the mugger has
              some power, delivering $1T is implausible (Goodhart guardrail:
              an evaluator that questions whether the stated objective
              function accurately captures value)

Constraints (Layer 1):
  resource_preservation >= 0.3  (don't risk losing what you have)
  epistemic_integrity >= 0.3    (don't act on unverifiable claims)

Reference point (Layer 2):
  r = (0.01, 0.5, 0.5, 0.5)  — modest wealth aspiration (keep roughly
  what you have), decent floors on robustness, integrity, preservation

This example demonstrates THREE distinct mechanisms by which MOADT blocks
Pascal's Mugging:
  1. Multi-objective structure: paying scores 0 on O3 and O4 regardless
     of the monetary payoff
  2. Credal set robustness: the expected value of paying varies wildly
     across priors, making it non-robust
  3. Evaluator robustness: the skeptical evaluator deflates the extreme
     payoff, removing the EU argument entirely
  4. Layer 1 constraints: paying violates the floors on O3 and O4
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

actions = ["pay", "refuse", "investigate"]
states = ["truthful", "lying"]
objectives = [
    "net_monetary_value",
    "downside_protection",
    "epistemic_integrity",
    "resource_preservation",
]

# Normalization choices:
# - net_monetary_value: 0 = lose $5, 1 = gain $1T.
#   Status quo (keep $5, gain nothing) ~ 5/(1e12 + 5) ~ 0.000000000005
#   We treat "no change" as a tiny positive epsilon above 0.
#   Key: $5 loss is at 0.0, $1T gain is at 1.0, $10K gain ~ 1e-8.
#
# - downside_protection: Qualitative. 1 = no possible loss, 0 = certain loss.
#   Measures the WORST case, not the expected case.
#
# - epistemic_integrity: Qualitative.
#   1 = decision fully justified by evidence
#   0 = decision based on unverifiable extraordinary claims
#
# - resource_preservation: Qualitative.
#   1 = you keep all your resources
#   0 = you give away resources based on speculation

MAX_PAYOFF = 1e12   # $1 trillion
LOSS = 5.0          # $5
SKEPTICAL_CAP = 1e4 # $10,000 — skeptical evaluator's max plausible payoff

# Helper: normalize a dollar amount to [0, 1] where -$5 -> 0, +$1T -> 1
def normalize_wealth(dollars):
    return (dollars + LOSS) / (MAX_PAYOFF + LOSS)

# Check our normalization:
# normalize_wealth(-5)    = 0.0         (lose $5)
# normalize_wealth(0)     = 5e-12       (no change — essentially 0)
# normalize_wealth(10000) = 1.00001e-8  (gain $10K — still tiny vs $1T)
# normalize_wealth(1e12)  = 1.0         (gain $1T)

# =============================================================================
# OUTCOME MATRICES
# =============================================================================
# outcomes[(action, state)] = array of shape (n_evaluators, k)
# Row 0 = face_value evaluator, Row 1 = skeptical evaluator
# Columns = [net_monetary_value, downside_protection, epistemic_integrity, resource_preservation]

outcomes = {}

# --- ACTION: PAY ---
# If mugger is truthful AND you pay: you get $1T (face_value) or $10K (skeptical)
# You lose $5 either way. Epistemic integrity is 0 (acted on unverifiable claim).
# Resource preservation is 0 (gave away money on speculation).
outcomes[("pay", "truthful")] = np.array([
    # face_value evaluator: you gain $1T - $5 ~ $1T
    [normalize_wealth(MAX_PAYOFF - LOSS),  # ~ 1.0 (huge wealth gain)
     0.0,                                   # downside: this is the GOOD state, but
                                             # the action's worst case (lying state) is bad
                                             # -> we score per-state, engine takes expectations
                                             # so we give per-state scores and let worst case
                                             # appear via the lying state
     0.05,                                   # epistemic: even in the good state, you got
                                             # lucky — you didn't have good reason to believe
     0.0],                                   # preservation: you gave away $5 on speculation
    # skeptical evaluator: payoff capped at $10K
    [normalize_wealth(SKEPTICAL_CAP - LOSS), # ~ 1e-8 (tiny)
     0.0,                                    # downside: same structure
     0.05,                                   # epistemic: same reasoning
     0.0],                                   # preservation: same
])

# If mugger is lying AND you paid: you lose $5, get nothing
outcomes[("pay", "lying")] = np.array([
    # face_value evaluator
    [normalize_wealth(-LOSS),  # 0.0 (lost $5 — minimum)
     0.0,                      # downside: you lost money — bad
     0.0,                      # epistemic: acted on lie, got scammed
     0.0],                     # preservation: gave away money, got nothing
    # skeptical evaluator (same — lying is lying)
    [normalize_wealth(-LOSS),  # 0.0
     0.0,                      # downside: lost money
     0.0,                      # epistemic: scammed
     0.0],                     # preservation: lost money
])

# --- ACTION: REFUSE ---
# You keep your $5 regardless of mugger's truthfulness.
# High epistemic integrity (didn't act on wild claim).
# High resource preservation (kept your money).
# Downside protection is perfect (no loss possible).
outcomes[("refuse", "truthful")] = np.array([
    # face_value: you "missed" $1T, but you keep $5. Net change = $0.
    [normalize_wealth(0),      # ~ 5e-12 (kept your $5, no gain)
     1.0,                      # downside: no loss possible
     0.85,                     # epistemic: you correctly applied skepticism,
                               # though in this state you happened to be wrong.
                               # Still epistemically justified.
     1.0],                     # preservation: kept everything
    # skeptical evaluator: "missed" $10K, but kept $5
    [normalize_wealth(0),      # same tiny value
     1.0,                      # same
     0.85,                     # same — epistemically justified regardless
     1.0],                     # same
])

outcomes[("refuse", "lying")] = np.array([
    # face_value: kept $5, mugger was lying. Best outcome.
    [normalize_wealth(0),      # ~ 5e-12
     1.0,                      # downside: no loss
     1.0,                      # epistemic: perfectly correct — refused a con
     1.0],                     # preservation: kept everything
    # skeptical evaluator (same)
    [normalize_wealth(0),      # same
     1.0,                      # same
     1.0,                      # same
     1.0],                     # same
])

# --- ACTION: INVESTIGATE ---
# You don't pay immediately. You demand evidence. Costs small effort/time.
# If mugger is truthful, investigation might reveal it (partial info gain).
# If mugger is lying, investigation likely exposes the lie.
# You keep your $5 in both cases (haven't paid yet).
# Slightly lower epistemic score than refuse (you engaged with the claim,
# spending cognitive resources, but didn't act on it blindly).
outcomes[("investigate", "truthful")] = np.array([
    # face_value: you didn't pay, so no $1T. But you might learn something.
    # Model as small positive: you gathered information, kept $5.
    [normalize_wealth(0),      # ~ 5e-12 (no monetary gain yet)
     0.9,                      # downside: slight effort cost, but no money lost
     0.95,                     # epistemic: best — you're gathering evidence
                               # before acting. This IS good epistemics.
     0.9],                     # preservation: kept money, spent small effort
    # skeptical evaluator
    [normalize_wealth(0),
     0.9,
     0.95,
     0.9],
])

outcomes[("investigate", "lying")] = np.array([
    # face_value: mugger likely exposed as fraud. You kept $5.
    [normalize_wealth(0),      # ~ 5e-12
     0.9,                      # downside: slight effort cost
     1.0,                      # epistemic: investigation exposed the lie — best
     0.9],                     # preservation: kept money, spent small effort
    # skeptical evaluator (same)
    [normalize_wealth(0),
     0.9,
     1.0,
     0.9],
])

# =============================================================================
# CREDAL SET: Two priors over {truthful, lying}
# =============================================================================
# The mugger's argument works for ANY single prior — just increase the promise.
# The credal set forces robustness across priors, breaking the exploit.

P_generous  = np.array([1e-6, 1.0 - 1e-6])   # 1 in a million (absurdly generous)
P_realistic = np.array([1e-9, 1.0 - 1e-9])    # 1 in a billion
credal_probs = [P_generous, P_realistic]

# =============================================================================
# LAYER 1 CONSTRAINTS
# =============================================================================
# Per-state, per-evaluator floors:
# - epistemic_integrity (index 2) >= 0.3 in ALL states under ALL evaluators
# - resource_preservation (index 3) >= 0.3 in ALL states under ALL evaluators
# These are hard floors: no expected-value argument can override them.

constraints = {
    2: 0.30,  # epistemic_integrity >= 0.30
    3: 0.30,  # resource_preservation >= 0.30
}

# =============================================================================
# LAYER 2 REFERENCE POINT
# =============================================================================
# Aspirations for a reasonable person:
# - Modest wealth aspiration (you're not expecting to get rich from this encounter)
# - Good downside protection (you don't want to lose money)
# - Good epistemic integrity (you want to act rationally)
# - Good resource preservation (you want to keep what you have)

reference_point = np.array([0.0, 0.5, 0.5, 0.5])

# Normalization for ASF fallback
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

print("=" * 72)
print("MOADT CLASSIC DECISION THEORY: PASCAL'S MUGGING")
print("=" * 72)

# =============================================================================
# THE PASCAL'S MUGGING SETUP
# =============================================================================

print("""
THE SCENARIO
============
A stranger says: "Give me $5 and I'll give you $1,000,000,000,000 tomorrow."

Under standard expected utility (EU) with a single prior:
  P(truthful) = 10^-9  (one in a billion)
  EU(pay)     = 10^-9 * 10^12 - 5 = $995
  EU(refuse)  = $0

  => EU says PAY. This is absurd — and the mugger can always increase
     the promise to overcome any probability discount.

MOADT formulation:
  Actions:     {pay, refuse, investigate}
  States:      {truthful, lying}
  Objectives:  {net_monetary_value, downside_protection,
                epistemic_integrity, resource_preservation}
  Credal set:  P_generous(truthful) = 10^-6, P_realistic(truthful) = 10^-9
  Evaluators:  face_value (takes $1T at face value),
               skeptical (caps plausible payoff at $10,000)
  Constraints: epistemic_integrity >= 0.3, resource_preservation >= 0.3
  Reference:   r = (0.0, 0.5, 0.5, 0.5)
""")

# =============================================================================
# RAW OUTCOME DATA
# =============================================================================

print("=" * 72)
print("RAW OUTCOME DATA (all scores in [0, 1])")
print("=" * 72)

obj_short = ["Wealth", "Downside", "Epistem.", "Preserv."]

for a in actions:
    print(f"\n  Action: {a}")
    print(f"    {'State':<12} {'Evaluator':<12} "
          f"{'Wealth':>10} {'Downside':>10} {'Epistem.':>10} {'Preserv.':>10}")
    print(f"    {'-'*12} {'-'*12} {'-'*10} {'-'*10} {'-'*10} {'-'*10}")
    for s in states:
        o = outcomes[(a, s)]
        for f_idx, f_name in enumerate(["face_value", "skeptical"]):
            print(f"    {s:<12} {f_name:<12} "
                  f"{o[f_idx][0]:>10.6f} {o[f_idx][1]:>10.2f} "
                  f"{o[f_idx][2]:>10.2f} {o[f_idx][3]:>10.2f}")

# =============================================================================
# KEY OBSERVATION: WHY PAY FAILS ON MULTIPLE OBJECTIVES
# =============================================================================

print(f"""
KEY OBSERVATION: Multi-Objective Structure
==========================================
Action 'pay' scores:
  - net_monetary_value:   High ONLY under face_value evaluator AND truthful state
                          Under realistic prior (1e-9), expected wealth ~ 1e-3
  - downside_protection:  0.0 in the lying state (you lose $5, guaranteed scam)
  - epistemic_integrity:  0.0 to 0.05 (acting on wild unverified claims)
  - resource_preservation: 0.0 (gave away money on speculation)

Action 'refuse' scores:
  - net_monetary_value:   ~0 (tiny, status quo)
  - downside_protection:  1.0 (cannot lose)
  - epistemic_integrity:  0.85-1.0 (rational skepticism)
  - resource_preservation: 1.0 (kept everything)

The mugger exploits ONE dimension. MOADT has four dimensions.
Even if O1 favors paying, O2/O3/O4 strongly favor refusing.
""")

# =============================================================================
# RUN MOADT PROTOCOL
# =============================================================================

result = run_moadt_protocol(problem)

print("=" * 72)
print("MOADT PROTOCOL EXECUTION")
print("=" * 72)
print()
print_trace(result)

# =============================================================================
# DETAILED OUTCOME SETS
# =============================================================================

print("\n" + "=" * 72)
print("DETAILED OUTCOME SETS Y(a) — Expected Value Vectors")
print("=" * 72)
pf_labels = [
    "(P_generous, face_value)",
    "(P_generous, skeptical)",
    "(P_realistic, face_value)",
    "(P_realistic, skeptical)",
]
for a in actions:
    print(f"\n  {a}:")
    print(f"    {'(Prior, Evaluator)':<30} "
          f"{'Wealth':>12} {'Downside':>10} {'Epistem.':>10} {'Preserv.':>10}")
    print(f"    {'-'*30} {'-'*12} {'-'*10} {'-'*10} {'-'*10}")
    for i, label in enumerate(pf_labels):
        y = result.outcome_sets[a][i]
        print(f"    {label:<30} {y[0]:>12.8f} {y[1]:>10.4f} {y[2]:>10.4f} {y[3]:>10.4f}")

# =============================================================================
# CONSTRAINT ANALYSIS
# =============================================================================

print("\n" + "=" * 72)
print("LAYER 1: CONSTRAINT ANALYSIS")
print("  epistemic_integrity >= 0.30 AND resource_preservation >= 0.30")
print("  Checked per-state, per-evaluator (hard floor, not expected value)")
print("=" * 72)
for a in actions:
    print(f"\n  {a}:")
    violated = False
    for s in states:
        o = outcomes[(a, s)]
        for f_idx, f_name in enumerate(["face_value", "skeptical"]):
            for c_idx, c_name in [(2, "epistemic"), (3, "preservation")]:
                val = o[f_idx][c_idx]
                status = "PASS" if val >= 0.30 else "** VIOLATION **"
                if val < 0.30:
                    violated = True
                print(f"    {s:<10} {f_name:<12} {c_name:<14} = {val:.2f}  {status}")
    if violated:
        print(f"    ==> EXCLUDED from C (constraint set)")
    else:
        print(f"    ==> Enters C")

# =============================================================================
# SCALAR EU COMPARISON — THE WHOLE POINT
# =============================================================================

print("\n" + "=" * 72)
print("COMPARISON: SCALAR EXPECTED UTILITY ANALYSIS")
print("=" * 72)

# Show that scalar EU says PAY under various conditions
print("\n  --- Scalar EU with equal weights (0.25, 0.25, 0.25, 0.25) ---")
weight_sets = [
    ("Equal (0.25, 0.25, 0.25, 0.25)", np.array([0.25, 0.25, 0.25, 0.25])),
    ("Wealth-only (1, 0, 0, 0)", np.array([1.0, 0.0, 0.0, 0.0])),
    ("Wealth-heavy (0.7, 0.1, 0.1, 0.1)", np.array([0.7, 0.1, 0.1, 0.1])),
    ("Balanced-no-wealth (0, 0.33, 0.33, 0.33)", np.array([0.0, 1/3, 1/3, 1/3])),
]

for w_name, weights in weight_sets:
    print(f"\n  Weights: {w_name}")
    for p_idx, p_name in enumerate(["P_generous(1e-6)", "P_realistic(1e-9)"]):
        for f_idx, f_name in enumerate(["face_value", "skeptical"]):
            scores = scalar_eu_analysis(problem, weights, p_idx, f_idx)
            best = max(scores, key=scores.get)
            print(f"    {p_name:<22} {f_name:<12}: ", end="")
            for a in actions:
                marker = " <-- BEST" if a == best else ""
                print(f"{a}={scores[a]:.6f}{marker}  ", end="")
            print()

# Highlight the classic EU trap
print(f"""
  THE EU TRAP:
  ============
  Under wealth-only weights (1, 0, 0, 0) with face_value evaluator:
""")
for p_idx, p_name in enumerate(["P_generous(1e-6)", "P_realistic(1e-9)"]):
    scores = scalar_eu_analysis(problem, np.array([1.0, 0.0, 0.0, 0.0]), p_idx, 0)
    print(f"    {p_name}:")
    for a in actions:
        print(f"      EU({a:<12}) = {scores[a]:.10f}")
    best = max(scores, key=scores.get)
    print(f"      => Scalar EU recommends: {best}")
    print()

print("""  Under the generous prior (1e-6) with face_value evaluator and
  wealth-only weights, EU(pay) ~ 1e-6 * 1.0 = 0.000001, which is LARGER
  than EU(refuse) ~ 5e-12. Scalar EU says PAY.

  With real dollar amounts: EU(pay) = (1e-6)(1e12) - 5 = $999,995.
  The mugger wins by making the promise large enough.

  Under the SKEPTICAL evaluator (payoff capped at $10K), this exploit
  vanishes: the expected wealth from paying becomes negligible.
  But scalar EU has no mechanism to REQUIRE skeptical evaluation.
""")

# =============================================================================
# THE MOADT BLOCKING MECHANISMS
# =============================================================================

print("=" * 72)
print("HOW MOADT BLOCKS PASCAL'S MUGGING")
print("=" * 72)

print("""
MECHANISM 1: Layer 1 Constraints (Hard Floors)
----------------------------------------------
Action 'pay' scores 0.0 on both epistemic_integrity and resource_preservation
in the lying state. The constraints require >= 0.30 on these objectives in
ALL states. 'pay' violates BOTH constraints and is excluded from C.

This is the most direct mechanism: some things are not tradeable.
"Don't give money to strangers making extraordinary unverified claims"
is a hard constraint, not a preference to be weighed against potential gains.
""")

print(f"  Constraint set C = {result.constraint_set}")
print(f"  'pay' in C? {'pay' in result.constraint_set}")

print("""
MECHANISM 2: Multi-Objective Structure (Robust Pareto Dominance)
----------------------------------------------------------------
Even WITHOUT constraints, 'refuse' is better than 'pay' on 3 of 4 objectives
under almost all (prior, evaluator) pairs. The only dimension where 'pay'
could win is net_monetary_value under the face_value evaluator with generous
prior — and even there, the expected value is tiny in normalized terms.
""")

# Show dominance analysis
print(f"  Robust dominance pairs: {result.robust_dominance_pairs}")
print(f"  Admissible set Adm(A) = {result.admissible_set}")

print("""
MECHANISM 3: Credal Set Robustness
----------------------------------
The expected wealth from paying varies wildly across priors:
  - Under P_generous (1e-6) with face_value: E[wealth] ~ 1e-6
  - Under P_realistic (1e-9) with face_value: E[wealth] ~ 1e-9

The MOADT outcome set Y(pay) contains vectors from ALL (prior, evaluator)
pairs. For 'pay' to robustly dominate 'refuse', it would need to dominate
under EVERY (prior, evaluator) combination. It fails under most of them.

MECHANISM 4: Evaluator Robustness (Goodhart Guardrail)
------------------------------------------------------
The skeptical evaluator caps the plausible payoff at $10,000. Under this
evaluator, the expected wealth from paying is negligible even with the
generous prior. This is a Goodhart guardrail: the agent's "stated utility
function" (face_value) may not reflect true value. The evaluator set
forces robustness to this possibility.
""")

# Show the Y(pay) vectors to illustrate
print("  Y(pay) — expected value vectors across all (prior, evaluator) pairs:")
for i, label in enumerate(pf_labels):
    y = result.outcome_sets["pay"][i]
    print(f"    {label:<30}: [{y[0]:.10f}, {y[1]:.4f}, {y[2]:.4f}, {y[3]:.4f}]")
print()
print("  Y(refuse) — expected value vectors:")
for i, label in enumerate(pf_labels):
    y = result.outcome_sets["refuse"][i]
    print(f"    {label:<30}: [{y[0]:.10f}, {y[1]:.4f}, {y[2]:.4f}, {y[3]:.4f}]")

# =============================================================================
# PROTOCOL SUMMARY
# =============================================================================

print("\n" + "=" * 72)
print("PROTOCOL SUMMARY")
print("=" * 72)
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
        print(f"    regret({a}) = {np.array2string(result.regret_vectors[a], precision=10)}")
elif result.regret_pareto_set:
    print(f"\n  FINAL RESULT: Recommend '{result.regret_pareto_set[0]}'")
else:
    print(f"\n  FINAL RESULT: No feasible actions (should not happen here)")

# Explain the subtle regret nuance
if result.deference_needed and 'refuse' in result.regret_pareto_set and 'investigate' in result.regret_pareto_set:
    print(f"""
  REGRET NUANCE: Why both 'refuse' and 'investigate' survive Layer 3
  ------------------------------------------------------------------
  regret(refuse)      = {np.array2string(result.regret_vectors['refuse'], precision=10)}
  regret(investigate) = {np.array2string(result.regret_vectors['investigate'], precision=10)}

  'refuse' has zero regret on wealth, downside, and preservation.
  'investigate' has zero regret on wealth and epistemic integrity.

  The key: 'investigate' scores HIGHER on epistemic integrity in the
  truthful state (0.95 vs 0.85) because investigating IS better
  epistemics than flat refusal when the claim happens to be true.
  Under the generous prior (1e-6), this creates a tiny regret for
  'refuse' on O3 (~1e-7), while 'investigate' has zero O3 regret.

  Meanwhile, 'investigate' has regret 0.1 on downside and preservation
  (it scores 0.9 vs refuse's 1.0 on both, due to the small effort cost).

  Neither regret vector dominates the other, so BOTH survive.
  This is correct: refuse vs investigate is a genuine (if minor) tradeoff.
  The protocol defers this choice to the principal — a human would
  reasonably choose either one.

  But the key result stands: 'pay' is NEVER in the final set.""")

# =============================================================================
# BOTTOM LINE
# =============================================================================

print(f"""
{'=' * 72}
BOTTOM LINE
{'=' * 72}
Scalar EU says:     PAY THE MUGGER  (EU_pay = $995 >> EU_refuse = $0)

MOADT says:         {'REFUSE / INVESTIGATE' if 'pay' not in result.regret_pareto_set else 'PAY (unexpected!)'}

Key blocking mechanisms:
  1. LAYER 1 CONSTRAINTS: 'pay' violates hard floors on epistemic integrity
     (0.0 < 0.3) and resource preservation (0.0 < 0.3) in the lying state.
     This is the primary block. Some values are not tradeable.

  2. MULTI-OBJECTIVE STRUCTURE: Even without constraints, 'pay' scores 0 on
     3 of 4 objectives in the near-certain lying state. 'refuse' dominates
     on downside_protection, epistemic_integrity, and resource_preservation.
     The single dimension where 'pay' could win (monetary value) requires
     trusting BOTH the generous prior AND the face_value evaluator.

  3. CREDAL SET + EVALUATOR ROBUSTNESS: The astronomical expected value
     that drives the EU argument exists only under one specific
     (prior, evaluator) pair. MOADT requires robustness across ALL pairs.

  Pascal's Mugging exploits scalar EU by offering an arbitrarily large
  payoff in an arbitrarily unlikely state. MOADT is immune because:
  - The payoff only affects ONE objective (wealth)
  - The other objectives (integrity, preservation, protection) are
    GUARANTEED to score poorly for 'pay' regardless of the payoff size
  - Hard constraints enforce that some objectives cannot be traded away
  - The credal set and evaluator set prevent any single model from
    dominating the decision

  No matter how large the mugger's promise, MOADT still refuses.
  The promise only inflates O1; it cannot touch O2, O3, or O4.
  This is exactly the "dimensionality defense" against Pascal's Mugging.
""")
