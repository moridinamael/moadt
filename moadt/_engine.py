"""
MOADT Engine: Multi-Objective Admissible Decision Theory
Computational implementation of the four-layer choice protocol.

This module provides concrete implementations of:
- Outcome set computation Y(a)
- Pareto dominance checking
- Robust dominance checking (forall-exists quantifier structure)
- Admissible set computation
- Layer 1: Constraint satisfaction
- Layer 2: Robust satisficing with ASF fallback
- Layer 3: Regret-Pareto selection
- Layer 4: Deference identification

Used by the worked-example papers to produce verifiable numerical results.
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass


@dataclass(frozen=True)
class MOADTProblem:
    """A fully specified MOADT decision problem.

    Attributes:
        actions: Action labels.
        states: State labels.
        objectives: Objective labels.
        outcomes: Mapping from (action, state) to outcome array.
            Shape is ``(n_evaluators, n_objectives)`` for multi-evaluator
            problems or ``(n_objectives,)`` for single-evaluator problems.
        credal_probs: List of probability vectors over states.
        constraints: Mapping from objective index to hard threshold (Layer 1).
        reference_point: Aspiration levels for satisficing (Layer 2).
        sigma: Optional normalisation factors for the ASF fallback.
            When *None*, all-ones is used.
    """

    actions: list[str]                          # Action labels
    states: list[str]                           # State labels
    objectives: list[str]                       # Objective labels
    outcomes: dict[tuple[str, str], np.ndarray] # (action, state) -> outcome vector per evaluator
    # outcomes[(a, s)] shape: (|F|, k) -- one row per evaluator
    credal_probs: list[np.ndarray]              # List of probability vectors over states
    constraints: dict[int, float]               # objective_index -> threshold (Layer 1)
    reference_point: np.ndarray                 # Aspiration levels (Layer 2)
    sigma: np.ndarray | None = None             # Normalization factors for ASF

    @classmethod
    def from_arrays(
        cls,
        outcomes_array: np.ndarray,
        actions: list[str],
        states: list[str],
        objectives: list[str],
        credal_probs: list[np.ndarray],
        constraints: dict[int, float] | dict[str, float],
        reference_point: np.ndarray,
        sigma: np.ndarray | None = None,
    ) -> MOADTProblem:
        """Construct a problem from a 4-D outcome array.

        This convenience constructor eliminates the need to manually build the
        ``(action, state)``-keyed outcomes dict.

        Args:
            outcomes_array: Array of shape
                ``(n_actions, n_states, n_evaluators, n_objectives)``.
            actions: Action labels (length must match axis 0).
            states: State labels (length must match axis 1).
            objectives: Objective labels (length must match axis 3).
            credal_probs: List of probability vectors over states.
            constraints: Hard thresholds for Layer 1.  Keys may be
                objective *names* (str) or integer indices.
            reference_point: Aspiration levels for satisficing (Layer 2).
            sigma: Optional normalisation factors for the ASF fallback.

        Returns:
            A fully constructed :class:`MOADTProblem`.

        Raises:
            ValueError: If array dimensions don't match label lengths or
                constraint names are not found among objectives.
        """
        arr = np.asarray(outcomes_array, dtype=float)
        if arr.ndim != 4:
            raise ValueError(
                f"outcomes_array must be 4-D "
                f"(n_actions, n_states, n_evaluators, n_objectives), "
                f"got {arr.ndim}-D"
            )

        n_a, n_s, n_f, n_k = arr.shape
        if len(actions) != n_a:
            raise ValueError(
                f"len(actions)={len(actions)} != outcomes_array axis 0 ({n_a})"
            )
        if len(states) != n_s:
            raise ValueError(
                f"len(states)={len(states)} != outcomes_array axis 1 ({n_s})"
            )
        if len(objectives) != n_k:
            raise ValueError(
                f"len(objectives)={len(objectives)} != outcomes_array axis 3 ({n_k})"
            )

        # Build outcomes dict; squeeze evaluator axis when n_evaluators == 1
        outcomes: dict[tuple[str, str], np.ndarray] = {}
        for i, a in enumerate(actions):
            for j, s in enumerate(states):
                val = arr[i, j]            # (n_evaluators, n_objectives)
                if n_f == 1:
                    val = val[0]           # squeeze to (n_objectives,)
                outcomes[(a, s)] = val

        # Resolve string constraint keys to integer indices
        idx_constraints: dict[int, float] = {}
        obj_index = {name: idx for idx, name in enumerate(objectives)}
        for key, threshold in constraints.items():
            if isinstance(key, str):
                if key not in obj_index:
                    raise ValueError(
                        f"constraint key {key!r} not found in objectives "
                        f"{objectives}"
                    )
                idx_constraints[obj_index[key]] = threshold
            else:
                idx_constraints[key] = threshold

        return cls(
            actions=list(actions),
            states=list(states),
            objectives=list(objectives),
            outcomes=outcomes,
            credal_probs=credal_probs,
            constraints=idx_constraints,
            reference_point=np.asarray(reference_point),
            sigma=sigma,
        )

    @property
    def n_evaluators(self) -> int:
        """Number of evaluators, inferred from the first outcome array."""
        first = self.outcomes[(self.actions[0], self.states[0])]
        return first.shape[0] if first.ndim > 1 else 1

    @property
    def n_objectives(self) -> int:
        """Number of objectives."""
        return len(self.objectives)

    def validate(self) -> None:
        """Check internal consistency.  Raises *ValueError* on failure."""
        if not self.actions:
            raise ValueError("actions must be non-empty")
        if not self.states:
            raise ValueError("states must be non-empty")
        if not self.objectives:
            raise ValueError("objectives must be non-empty")

        k = self.n_objectives

        # All (action, state) pairs present
        for a in self.actions:
            for s in self.states:
                if (a, s) not in self.outcomes:
                    raise ValueError(f"missing outcome for ({a!r}, {s!r})")

        # Shape consistency
        first_key = (self.actions[0], self.states[0])
        expected_shape = self.outcomes[first_key].shape
        for (a, s), arr in self.outcomes.items():
            if arr.shape != expected_shape:
                raise ValueError(
                    f"outcome shape mismatch for ({a!r}, {s!r}): "
                    f"expected {expected_shape}, got {arr.shape}"
                )

        # Credal probs
        if not self.credal_probs:
            raise ValueError("credal_probs must be non-empty")
        for i, P in enumerate(self.credal_probs):
            if len(P) != len(self.states):
                raise ValueError(
                    f"credal_probs[{i}] length {len(P)} != "
                    f"number of states {len(self.states)}"
                )
            if np.any(P < -1e-12):
                raise ValueError(f"credal_probs[{i}] contains negative values")
            if abs(P.sum() - 1.0) > 1e-6:
                raise ValueError(
                    f"credal_probs[{i}] sums to {P.sum()}, expected 1.0"
                )

        # Constraint indices
        for idx in self.constraints:
            if idx < 0 or idx >= k:
                raise ValueError(
                    f"constraint index {idx} out of range [0, {k})"
                )

        # Reference point shape
        if len(self.reference_point) != k:
            raise ValueError(
                f"reference_point length {len(self.reference_point)} != "
                f"number of objectives {k}"
            )


@dataclass(frozen=True)
class MOADTResult:
    """Results from running the MOADT protocol.

    Attributes:
        outcome_sets: Mapping from action to its Y(a) matrix (rows are
            expected-value vectors, one per (prior, evaluator) pair).
        admissible_set: Actions surviving robust dominance (Adm(A)).
        constraint_set: Actions satisfying Layer 1 constraints (C).
        feasible_set: Admissible subset of C (F = Adm(C)).
        satisficing_set: Actions robustly meeting aspirations (Sat(F, r)).
        sat_fallback_used: Whether the ASF fallback was triggered.
        asf_selection: ASF-optimal actions when fallback is used.
        regret_vectors: Per-action minimax regret vectors.  Empty dict
            when Layer 3 is skipped (e.g. ASF fallback resolved selection).
        regret_pareto_set: Regret-Pareto-optimal actions (R).
        deference_needed: True when the protocol cannot identify a unique
            recommendation (|R| > 1, or the constraint set is empty).
        robust_dominance_pairs: All (a, b) pairs where a robustly dominates b.
        layer_trace: Human-readable log of each protocol layer.
    """

    outcome_sets: dict[str, np.ndarray]         # action -> Y(a) matrix (rows = vectors)
    admissible_set: list[str]                   # Adm(A)
    constraint_set: list[str]                   # C
    feasible_set: list[str]                     # F = Adm(C)
    satisficing_set: list[str]                  # Sat(F, r)
    sat_fallback_used: bool                     # Whether ASF fallback was needed
    asf_selection: list[str] | None             # ASF selection if fallback used
    regret_vectors: dict[str, np.ndarray]       # action -> regret vector
    regret_pareto_set: list[str]                # R
    deference_needed: bool                      # Whether |R| > 1
    robust_dominance_pairs: list[tuple[str, str]]  # (a, b) where a >_R b
    layer_trace: list[str]                      # Human-readable trace of protocol


def compute_outcome_sets(problem: MOADTProblem) -> dict[str, np.ndarray]:
    """Compute the outcome set Y(a) for every action.

    Y(a) = { E_P[f(omega(a, s))] : P in P, f in F }

    Returns:
        Mapping from action label to an array of shape
        ``(|P| * n_evaluators, n_objectives)``.
    """
    n_eval = problem.n_evaluators
    k = problem.n_objectives

    outcome_sets = {}
    for a in problem.actions:
        vectors = []
        for P in problem.credal_probs:
            for f_idx in range(n_eval):
                # Compute E_P[f(omega(a, s))] for this (P, f) pair
                expected = np.zeros(k)
                for s_idx, s in enumerate(problem.states):
                    outcome = problem.outcomes[(a, s)]
                    if outcome.ndim > 1:
                        eval_vector = outcome[f_idx]
                    else:
                        eval_vector = outcome
                    expected += P[s_idx] * eval_vector
                vectors.append(expected)
        outcome_sets[a] = np.array(vectors)
    return outcome_sets


def pareto_dominates(x: np.ndarray, y: np.ndarray) -> bool:
    """Return True if *x* Pareto-dominates *y* (x >= y everywhere, strict somewhere)."""
    return bool(np.all(x >= y) and np.any(x > y))


def robustly_dominates(Y_a: np.ndarray, Y_b: np.ndarray) -> bool:
    """Return True if action *a* robustly dominates action *b*.

    a >_R b iff for every y_b in Y(b) there exists y_a in Y(a) such that
    y_a Pareto-dominates y_b.

    Uses numpy broadcasting to compute the full (n, m) dominance matrix
    in a single vectorized operation instead of nested Python loops.
    """
    # Y_a: (n, k), Y_b: (m, k) -> broadcast to (n, m, k)
    diff = Y_a[:, np.newaxis, :] - Y_b[np.newaxis, :, :]
    # dom[i, j] = True iff y_a[i] Pareto-dominates y_b[j]
    dom = np.all(diff >= 0, axis=2) & np.any(diff > 0, axis=2)
    # For every y_b (column), at least one y_a (row) must dominate it
    return bool(np.all(np.any(dom, axis=0)))


def compute_admissible_set(
    actions: list[str],
    outcome_sets: dict[str, np.ndarray]
) -> tuple[list[str], list[tuple[str, str]]]:
    """Compute Adm(actions) = {a : no a' robustly dominates a}.

    Returns:
        ``(admissible_set, dominance_pairs)`` where each dominance pair
        is ``(dominator, dominated)``.
    """
    dominated = set()
    dominance_pairs = []

    for a in actions:
        for b in actions:
            if a == b:
                continue
            if robustly_dominates(outcome_sets[a], outcome_sets[b]):
                dominated.add(b)
                dominance_pairs.append((a, b))

    admissible = [a for a in actions if a not in dominated]
    return admissible, dominance_pairs


def check_constraint_satisfaction(
    action: str,
    problem: MOADTProblem
) -> bool:
    """Check whether *action* satisfies all Layer 1 constraints.

    A constraint is satisfied when, for every prior P, every evaluator f,
    and every state s in supp(P), the relevant objective meets its threshold.
    """
    n_eval = problem.n_evaluators

    for obj_idx, threshold in problem.constraints.items():
        for P in problem.credal_probs:
            for s_idx, s in enumerate(problem.states):
                if P[s_idx] > 0:  # s in supp(P)
                    outcome = problem.outcomes[(action, s)]
                    for f_idx in range(n_eval):
                        if outcome.ndim > 1:
                            val = outcome[f_idx][obj_idx]
                        else:
                            val = outcome[obj_idx]
                        if val < threshold:
                            return False
    return True


def compute_satisficing_set(
    feasible: list[str],
    outcome_sets: dict[str, np.ndarray],
    reference_point: np.ndarray
) -> list[str]:
    """Compute Sat(F, r) = {a in F : every y in Y(a) >= r}.

    An action robustly satisfices when it meets aspirations under *all*
    models (priors x evaluators).
    """
    sat = []
    for a in feasible:
        if np.all(outcome_sets[a] >= reference_point):
            sat.append(a)
    return sat


def compute_asf(
    action: str,
    outcome_sets: dict[str, np.ndarray],
    reference_point: np.ndarray,
    sigma: np.ndarray | None = None
) -> float:
    """Achievement scalarising function (Layer 2 fallback).

    ``asf(a, r) = min_i min_{y in Y(a)} (y_i - r_i) / sigma_i``

    When *sigma* is ``None``, all-ones is used.
    """
    if sigma is None:
        sigma = np.ones(len(reference_point))
    Y_a = outcome_sets[action]
    min_val = float('inf')
    for y in Y_a:
        for i in range(len(reference_point)):
            val = (y[i] - reference_point[i]) / sigma[i]
            min_val = min(min_val, val)
    return min_val


def compute_regret_vectors(
    actions: list[str],
    outcome_sets: dict[str, np.ndarray],
    problem: MOADTProblem,
    reference_actions: list[str] | None = None,
) -> dict[str, np.ndarray]:
    """Compute per-objective minimax regret vectors.

    ``rho_i(a) = max_{P,f} [ max_{a' in ref} E_P[f_i(a')] - E_P[f_i(a)] ]``

    Args:
        actions: Actions whose regret vectors are computed.
        outcome_sets: Pre-computed outcome sets.
        problem: The decision problem.
        reference_actions: Actions that define the "best available"
            benchmark (the inner max).  Per the paper's Definition 6,
            this should be the feasible set *F*.  When *None*, falls
            back to *actions* for backward compatibility.

    Returns:
        Mapping from action label to its regret vector of shape
        ``(n_objectives,)``.
    """
    if reference_actions is None:
        reference_actions = actions

    k = problem.n_objectives
    n_eval = problem.n_evaluators

    regret_vectors = {}

    for a in actions:
        regret = np.zeros(k)

        # For each (P, f) pair, compute the regret of a on each objective
        pf_idx = 0
        for p_idx, P in enumerate(problem.credal_probs):
            for f_idx in range(n_eval):
                # E_P[f_i(a)] for this (P, f)
                expected_a = outcome_sets[a][pf_idx]

                # max_{a' in reference set} E_P[f_i(a')] for this (P, f)
                for obj_i in range(k):
                    best_val = max(
                        outcome_sets[a_prime][pf_idx][obj_i]
                        for a_prime in reference_actions
                    )
                    gap = best_val - expected_a[obj_i]
                    regret[obj_i] = max(regret[obj_i], gap)

                pf_idx += 1

        regret_vectors[a] = regret

    return regret_vectors


def compute_regret_pareto_set(
    actions: list[str],
    regret_vectors: dict[str, np.ndarray]
) -> list[str]:
    """Compute the regret-Pareto set (actions with Pareto-minimal regret).

    An action is regret-dominated if another action has weakly lower regret
    on every objective and strictly lower on at least one.
    """
    dominated = set()
    for a in actions:
        for b in actions:
            if a == b:
                continue
            # Does b have strictly better (lower) regret than a?
            if (np.all(regret_vectors[b] <= regret_vectors[a]) and
                np.any(regret_vectors[b] < regret_vectors[a])):
                dominated.add(a)
                break

    return [a for a in actions if a not in dominated]


def run_moadt_protocol(problem: MOADTProblem) -> MOADTResult:
    """Run the full four-layer MOADT choice protocol.

    Validates the problem, computes outcome sets, and then applies
    each layer in sequence.  Returns a :class:`MOADTResult` with
    the full trace.
    """
    problem.validate()

    trace = []

    # Compute outcome sets
    outcome_sets = compute_outcome_sets(problem)
    trace.append("=== Outcome Sets Y(a) ===")
    for a in problem.actions:
        trace.append(f"  Y({a}):")
        for i, y in enumerate(outcome_sets[a]):
            trace.append(f"    y_{i+1} = {np.round(y, 4)}")

    # Compute full admissible set (for reference)
    full_adm, all_dom_pairs = compute_admissible_set(problem.actions, outcome_sets)
    trace.append(f"\n=== Robust Dominance ===")
    if all_dom_pairs:
        for a, b in all_dom_pairs:
            trace.append(f"  {a} \u227b_R {b}")
    else:
        trace.append("  No robust dominance relations found.")
    trace.append(f"  Adm(A) = {full_adm}")

    # Layer 1: Constraints
    trace.append(f"\n=== Layer 1: Constraints ===")
    constraint_set = []
    for a in problem.actions:
        satisfies = check_constraint_satisfaction(a, problem)
        trace.append(f"  {a}: {'PASS' if satisfies else 'FAIL'}")
        if satisfies:
            constraint_set.append(a)

    if not constraint_set:
        trace.append("  WARNING: C = \u2205 \u2014 no action satisfies all constraints!")
        trace.append("  ERROR CONDITION: Flag to principal.")
        return MOADTResult(
            outcome_sets=outcome_sets,
            admissible_set=full_adm,
            constraint_set=[],
            feasible_set=[],
            satisficing_set=[],
            sat_fallback_used=False,
            asf_selection=None,
            regret_vectors={},
            regret_pareto_set=[],
            deference_needed=True,
            robust_dominance_pairs=all_dom_pairs,
            layer_trace=trace
        )

    # Compute F = Adm(C)
    feasible, dom_pairs_c = compute_admissible_set(constraint_set, outcome_sets)
    trace.append(f"  C = {constraint_set}")
    trace.append(f"  F = Adm(C) = {feasible}")

    # Layer 2: Satisficing
    trace.append(f"\n=== Layer 2: Reference-Point Satisficing ===")
    trace.append(f"  Reference point r = {problem.reference_point}")
    satisficing = compute_satisficing_set(feasible, outcome_sets, problem.reference_point)
    trace.append(f"  Sat(F, r) = {satisficing}")

    sat_fallback_used = False
    asf_selection = None

    if not satisficing:
        sat_fallback_used = True
        trace.append("  Sat = \u2205 \u2014 falling back to ASF")
        sigma = problem.sigma if problem.sigma is not None else np.ones(len(problem.objectives))
        asf_scores = {}
        for a in feasible:
            score = compute_asf(a, outcome_sets, problem.reference_point, sigma)
            asf_scores[a] = score
            trace.append(f"    ASF({a}) = {score:.4f}")
        best_score = max(asf_scores.values())
        asf_selection = [a for a, s in asf_scores.items() if abs(s - best_score) < 1e-10]
        trace.append(f"  ASF selection: {asf_selection}")
        working_set = asf_selection
    else:
        working_set = satisficing

    # Layer 3: Regret-Pareto
    trace.append(f"\n=== Layer 3: Regret-Pareto ===")

    if sat_fallback_used:
        trace.append("  (Layer 3 skipped \u2014 ASF fallback already resolved selection)")
        regret_vectors = {}
        regret_pareto = asf_selection
    else:
        regret_vectors = compute_regret_vectors(
            working_set, outcome_sets, problem, reference_actions=feasible
        )
        for a in working_set:
            trace.append(f"  \u03c1({a}) = {np.round(regret_vectors[a], 4)}")

        regret_pareto = compute_regret_pareto_set(working_set, regret_vectors)
        trace.append(f"  Regret-Pareto set R = {regret_pareto}")

    # Layer 4: Deference
    trace.append(f"\n=== Layer 4: Deference ===")
    deference_needed = len(regret_pareto) > 1
    if deference_needed:
        trace.append(f"  |R| = {len(regret_pareto)} > 1 \u2014 DEFER to principal")
        trace.append(f"  Present options {regret_pareto} with regret profiles")
    else:
        trace.append(f"  |R| = 1 \u2014 unique recommendation: {regret_pareto[0]}")

    return MOADTResult(
        outcome_sets=outcome_sets,
        admissible_set=full_adm,
        constraint_set=constraint_set,
        feasible_set=feasible,
        satisficing_set=satisficing,
        sat_fallback_used=sat_fallback_used,
        asf_selection=asf_selection,
        regret_vectors=regret_vectors,
        regret_pareto_set=regret_pareto,
        deference_needed=deference_needed,
        robust_dominance_pairs=all_dom_pairs,
        layer_trace=trace
    )


def scalar_eu_analysis(
    problem: MOADTProblem,
    weights: np.ndarray,
    prior_idx: int = 0,
    evaluator_idx: int = 0,
    outcome_sets: dict[str, np.ndarray] | None = None,
) -> dict[str, float]:
    """Compute scalar expected utility for comparison.

    ``U(a) = w . E_P[f(omega(a, s))]`` under a fixed weight vector,
    prior, and evaluator.

    Args:
        problem: The decision problem.
        weights: Objective weight vector.
        prior_idx: Index into ``problem.credal_probs``.
        evaluator_idx: Index of the evaluator row.
        outcome_sets: Pre-computed outcome sets.  When *None* (the default)
            they are recomputed from *problem*.
    """
    if outcome_sets is None:
        outcome_sets = compute_outcome_sets(problem)
    n_eval = problem.n_evaluators

    eu_scores = {}
    for a in problem.actions:
        # Index into the outcome set: prior_idx * n_evaluators + evaluator_idx
        idx = prior_idx * n_eval + evaluator_idx
        expected = outcome_sets[a][idx]
        eu_scores[a] = float(np.dot(weights, expected))

    return eu_scores


def print_trace(result: MOADTResult) -> None:
    """Print the human-readable protocol trace to stdout."""
    for line in result.layer_trace:
        print(line)
