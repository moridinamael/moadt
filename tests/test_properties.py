"""Property-based tests for MOADT structural invariants.

Uses hypothesis to generate random MOADTProblem instances and verify
that core invariants hold for ANY valid problem shape.
"""

import numpy as np
from hypothesis import given, settings, assume, HealthCheck
import hypothesis.strategies as st
import hypothesis.extra.numpy as hnp

from moadt import (
    MOADTProblem,
    run_moadt_protocol,
    pareto_dominates,
    robustly_dominates,
    sensitivity_analysis,
)


# ---------------------------------------------------------------------------
# Custom Hypothesis Strategies
# ---------------------------------------------------------------------------

@st.composite
def probability_vector(draw, n):
    """Draw a valid probability distribution over n states."""
    weights = draw(
        hnp.arrays(
            dtype=np.float64,
            shape=(n,),
            elements=st.floats(min_value=1e-8, max_value=1.0,
                               allow_nan=False, allow_infinity=False),
        )
    )
    return weights / weights.sum()


@st.composite
def finite_vectors(draw, n):
    """Draw a finite float vector of length n."""
    return draw(
        hnp.arrays(
            dtype=np.float64,
            shape=(n,),
            elements=st.floats(min_value=-1e6, max_value=1e6,
                               allow_nan=False, allow_infinity=False),
        )
    )


@st.composite
def outcome_matrices(draw):
    """Draw a 2-D outcome-set matrix for robustly_dominates tests."""
    n_rows = draw(st.integers(min_value=1, max_value=5))
    n_cols = draw(st.integers(min_value=1, max_value=4))
    return draw(
        hnp.arrays(
            dtype=np.float64,
            shape=(n_rows, n_cols),
            elements=st.floats(min_value=-1e6, max_value=1e6,
                               allow_nan=False, allow_infinity=False),
        )
    )


@st.composite
def moadt_problems(draw):
    """Draw a complete valid MOADTProblem with random dimensions."""
    n_actions = draw(st.integers(min_value=1, max_value=6))
    n_states = draw(st.integers(min_value=1, max_value=5))
    n_objectives = draw(st.integers(min_value=1, max_value=4))
    n_evaluators = draw(st.integers(min_value=1, max_value=3))
    n_credal = draw(st.integers(min_value=1, max_value=3))

    actions = [f"a{i}" for i in range(n_actions)]
    states = [f"s{i}" for i in range(n_states)]
    objectives = [f"o{i}" for i in range(n_objectives)]

    outcomes_array = draw(
        hnp.arrays(
            dtype=np.float64,
            shape=(n_actions, n_states, n_evaluators, n_objectives),
            elements=st.floats(min_value=0.0, max_value=1.0,
                               allow_nan=False, allow_infinity=False),
        )
    )

    credal_probs = [draw(probability_vector(n_states)) for _ in range(n_credal)]

    # Draw random constraints: pick a subset of objectives, assign thresholds
    constrained_indices = draw(
        st.lists(
            st.integers(0, n_objectives - 1),
            max_size=n_objectives,
            unique=True,
        )
    )
    constraints = {}
    for idx in constrained_indices:
        threshold = draw(
            st.floats(min_value=0.0, max_value=1.0,
                       allow_nan=False, allow_infinity=False)
        )
        constraints[idx] = threshold

    reference_point = draw(
        hnp.arrays(
            dtype=np.float64,
            shape=(n_objectives,),
            elements=st.floats(min_value=0.0, max_value=1.0,
                               allow_nan=False, allow_infinity=False),
        )
    )

    return MOADTProblem.from_arrays(
        outcomes_array=outcomes_array,
        actions=actions,
        states=states,
        objectives=objectives,
        credal_probs=credal_probs,
        constraints=constraints,
        reference_point=reference_point,
    )


@st.composite
def single_action_problems(draw):
    """Draw a valid MOADTProblem with exactly 1 action and no constraints."""
    n_states = draw(st.integers(min_value=1, max_value=5))
    n_objectives = draw(st.integers(min_value=1, max_value=4))
    n_evaluators = draw(st.integers(min_value=1, max_value=3))
    n_credal = draw(st.integers(min_value=1, max_value=3))

    outcomes_array = draw(
        hnp.arrays(
            dtype=np.float64,
            shape=(1, n_states, n_evaluators, n_objectives),
            elements=st.floats(min_value=0.0, max_value=1.0,
                               allow_nan=False, allow_infinity=False),
        )
    )

    credal_probs = [draw(probability_vector(n_states)) for _ in range(n_credal)]

    reference_point = draw(
        hnp.arrays(
            dtype=np.float64,
            shape=(n_objectives,),
            elements=st.floats(min_value=0.0, max_value=1.0,
                               allow_nan=False, allow_infinity=False),
        )
    )

    return MOADTProblem.from_arrays(
        outcomes_array=outcomes_array,
        actions=["a0"],
        states=[f"s{i}" for i in range(n_states)],
        objectives=[f"o{i}" for i in range(n_objectives)],
        credal_probs=credal_probs,
        constraints={},
        reference_point=reference_point,
    )


# ---------------------------------------------------------------------------
# Property 6: pareto_dominates is irreflexive and asymmetric
# ---------------------------------------------------------------------------

class TestParetoDominatesProperties:

    @given(n=st.integers(min_value=1, max_value=10), data=st.data())
    @settings(max_examples=500)
    def test_irreflexive(self, n, data):
        """pareto_dominates(x, x) is always False."""
        x = data.draw(finite_vectors(n))
        assert not pareto_dominates(x, x)

    @given(n=st.integers(min_value=1, max_value=10), data=st.data())
    @settings(max_examples=500,
              suppress_health_check=[HealthCheck.filter_too_much])
    def test_asymmetric(self, n, data):
        """If pareto_dominates(x, y) then not pareto_dominates(y, x)."""
        x = data.draw(finite_vectors(n))
        y = data.draw(finite_vectors(n))
        assume(pareto_dominates(x, y))
        assert not pareto_dominates(y, x)


# ---------------------------------------------------------------------------
# Property 7: robustly_dominates is irreflexive
# ---------------------------------------------------------------------------

class TestRobustlyDominatesProperties:

    @given(Y=outcome_matrices())
    @settings(max_examples=500)
    def test_irreflexive(self, Y):
        """robustly_dominates(Y, Y) is always False."""
        assert not robustly_dominates(Y, Y)


# ---------------------------------------------------------------------------
# Properties 1-5: Protocol invariants
# ---------------------------------------------------------------------------

class TestProtocolInvariants:

    @given(problem=moadt_problems())
    @settings(max_examples=200, deadline=None,
              suppress_health_check=[HealthCheck.too_slow])
    def test_admissible_subset_of_actions(self, problem):
        """Property 1: admissible_set is always a subset of actions."""
        result = run_moadt_protocol(problem)
        assert set(result.admissible_set) <= set(problem.actions)

    @given(problem=moadt_problems())
    @settings(max_examples=200, deadline=None,
              suppress_health_check=[HealthCheck.too_slow])
    def test_feasible_subset_of_constraint_set(self, problem):
        """Property 2: feasible_set is always a subset of constraint_set."""
        result = run_moadt_protocol(problem)
        assert set(result.feasible_set) <= set(result.constraint_set)

    @given(problem=moadt_problems())
    @settings(max_examples=200, deadline=None,
              suppress_health_check=[HealthCheck.too_slow])
    def test_satisficing_subset_of_feasible(self, problem):
        """Property 3: satisficing_set is always a subset of feasible_set."""
        result = run_moadt_protocol(problem)
        assert set(result.satisficing_set) <= set(result.feasible_set)

    @given(problem=moadt_problems())
    @settings(max_examples=200, deadline=None,
              suppress_health_check=[HealthCheck.too_slow])
    def test_regret_pareto_subset_of_working_set(self, problem):
        """Property 4: regret_pareto_set is always a subset of working_set."""
        result = run_moadt_protocol(problem)

        # Determine working set based on protocol path
        if not result.constraint_set:
            working = []
        elif result.sat_fallback_used:
            working = result.asf_selection or []
        else:
            working = result.satisficing_set

        assert set(result.regret_pareto_set) <= set(working)

    @given(problem=single_action_problems())
    @settings(max_examples=200, deadline=None,
              suppress_health_check=[HealthCheck.too_slow])
    def test_single_action_always_recommended(self, problem):
        """Property 5: if only one action exists (no constraints), it's always recommended."""
        result = run_moadt_protocol(problem)
        # Single action is always admissible (nothing can dominate it)
        assert problem.actions[0] in result.admissible_set
        # With no constraints, it passes through all layers
        assert result.constraint_set == ["a0"]
        assert result.regret_pareto_set == ["a0"]


# ---------------------------------------------------------------------------
# Sensitivity Analysis Properties
# ---------------------------------------------------------------------------

class TestSensitivityAnalysisProperties:

    @given(problem=moadt_problems())
    @settings(max_examples=50, deadline=None,
              suppress_health_check=[HealthCheck.too_slow])
    def test_all_actions_categorized(self, problem):
        """Every action appears in exactly one of always/sometimes/never."""
        result = sensitivity_analysis(problem, n_perturbations=10, epsilon=0.05, seed=42)
        all_cat = set(result.always_survive) | set(result.sometimes_survive) | set(result.never_survive)
        assert all_cat == set(problem.actions)

    @given(problem=moadt_problems())
    @settings(max_examples=50, deadline=None,
              suppress_health_check=[HealthCheck.too_slow])
    def test_survival_counts_bounded(self, problem):
        """Survival counts are between 0 and n_perturbations."""
        n = 10
        result = sensitivity_analysis(problem, n_perturbations=n, epsilon=0.05, seed=0)
        for a in problem.actions:
            for layer, count in result.layer_survival_counts[a].items():
                assert 0 <= count <= n
