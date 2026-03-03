"""Regression tests for the moadt engine."""

import numpy as np
import pytest

import moadt
from moadt import (
    MOADTProblem,
    SensitivityResult,
    compute_outcome_sets,
    pareto_dominates,
    robustly_dominates,
    compute_admissible_set,
    check_constraint_satisfaction,
    compute_satisficing_set,
    compute_asf,
    compute_regret_vectors,
    compute_regret_pareto_set,
    run_moadt_protocol,
    scalar_eu_analysis,
    sensitivity_analysis,
)


# ---------------------------------------------------------------------------
# TestVersion
# ---------------------------------------------------------------------------

class TestVersion:
    def test_version_is_string(self):
        assert isinstance(moadt.__version__, str)

    def test_version_is_pep440(self):
        """Basic check: version looks like X.Y.Z."""
        parts = moadt.__version__.split(".")
        assert len(parts) >= 2
        assert all(p.isdigit() for p in parts[:2])

    def test_version_in_all(self):
        assert "__version__" in moadt.__all__


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _simple_problem(**overrides):
    """Return a minimal valid 2-action, 2-state, 2-objective problem."""
    defaults = dict(
        actions=["a", "b"],
        states=["s1", "s2"],
        objectives=["o1", "o2"],
        outcomes={
            ("a", "s1"): np.array([0.8, 0.4]),
            ("a", "s2"): np.array([0.6, 0.5]),
            ("b", "s1"): np.array([0.5, 0.7]),
            ("b", "s2"): np.array([0.4, 0.8]),
        },
        credal_probs=[np.array([0.5, 0.5])],
        constraints={},
        reference_point=np.array([0.3, 0.3]),
    )
    defaults.update(overrides)
    return MOADTProblem(**defaults)


def _compute_outcome_sets_loop(problem):
    """Reference loop-based implementation for regression testing."""
    n_eval = problem.n_evaluators
    k = problem.n_objectives
    outcome_sets = {}
    for a in problem.actions:
        vectors = []
        for P in problem.credal_probs:
            for f_idx in range(n_eval):
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


def _compute_regret_vectors_loop(actions, outcome_sets, problem, reference_actions=None):
    """Reference loop-based implementation for regression testing."""
    if reference_actions is None:
        reference_actions = actions
    k = problem.n_objectives
    n_eval = problem.n_evaluators
    regret_vectors = {}
    for a in actions:
        regret = np.zeros(k)
        pf_idx = 0
        for p_idx, P in enumerate(problem.credal_probs):
            for f_idx in range(n_eval):
                expected_a = outcome_sets[a][pf_idx]
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


# ---------------------------------------------------------------------------
# TestParetoDominates
# ---------------------------------------------------------------------------

class TestParetoDominates:
    def test_strictly_better(self):
        assert pareto_dominates(np.array([2.0, 3.0]), np.array([1.0, 2.0]))

    def test_equal(self):
        assert not pareto_dominates(np.array([1.0, 2.0]), np.array([1.0, 2.0]))

    def test_weakly_better_strict_somewhere(self):
        assert pareto_dominates(np.array([1.0, 3.0]), np.array([1.0, 2.0]))

    def test_incomparable(self):
        assert not pareto_dominates(np.array([2.0, 1.0]), np.array([1.0, 2.0]))


# ---------------------------------------------------------------------------
# TestRobustlyDominates
# ---------------------------------------------------------------------------

class TestRobustlyDominates:
    def test_clear_dominance(self):
        """Y_a strictly dominates every vector in Y_b."""
        Y_a = np.array([[3.0, 3.0], [4.0, 4.0]])
        Y_b = np.array([[1.0, 1.0], [2.0, 2.0]])
        assert robustly_dominates(Y_a, Y_b) is True

    def test_single_element_sets(self):
        """Each set has a single vector; dominance is simple Pareto check."""
        Y_a = np.array([[3.0, 3.0]])
        Y_b = np.array([[2.0, 2.0]])
        assert robustly_dominates(Y_a, Y_b) is True
        # Reverse should fail
        assert robustly_dominates(Y_b, Y_a) is False

    def test_one_uncovered_vector_blocks_dominance(self):
        """Y_a covers one vector in Y_b but not the other — should return False."""
        Y_a = np.array([[3.0, 1.0]])  # dominates (2,0) but NOT (1,3)
        Y_b = np.array([[2.0, 0.0], [1.0, 3.0]])
        assert robustly_dominates(Y_a, Y_b) is False

    def test_equal_sets_no_dominance(self):
        """Identical outcome sets — Pareto requires strict somewhere, so no dominance."""
        Y = np.array([[1.0, 2.0], [3.0, 4.0]])
        assert robustly_dominates(Y, Y) is False


# ---------------------------------------------------------------------------
# TestComputeAdmissibleSet
# ---------------------------------------------------------------------------

class TestComputeAdmissibleSet:
    def test_one_dominated(self):
        """Action 'c' is dominated by 'a'; 'b' is incomparable."""
        outcome_sets = {
            "a": np.array([[5.0, 5.0]]),
            "b": np.array([[3.0, 6.0]]),
            "c": np.array([[2.0, 2.0]]),
        }
        adm, pairs = compute_admissible_set(["a", "b", "c"], outcome_sets)
        assert "a" in adm
        assert "b" in adm
        assert "c" not in adm
        assert ("a", "c") in pairs

    def test_single_action(self):
        """A single action is trivially admissible."""
        outcome_sets = {"x": np.array([[1.0, 2.0]])}
        adm, pairs = compute_admissible_set(["x"], outcome_sets)
        assert adm == ["x"]
        assert pairs == []

    def test_none_dominated(self):
        """All actions are mutually incomparable — all survive."""
        outcome_sets = {
            "a": np.array([[5.0, 1.0]]),
            "b": np.array([[1.0, 5.0]]),
        }
        adm, pairs = compute_admissible_set(["a", "b"], outcome_sets)
        assert set(adm) == {"a", "b"}
        assert pairs == []


# ---------------------------------------------------------------------------
# TestCheckConstraintSatisfaction
# ---------------------------------------------------------------------------

class TestCheckConstraintSatisfaction:
    def test_passes_when_all_above_threshold(self):
        """All outcomes for obj 0 are >= 0.5, so constraint {0: 0.5} passes."""
        p = _simple_problem(constraints={0: 0.5})
        # outcomes: a/s1=0.8, a/s2=0.6 — both >= 0.5
        assert check_constraint_satisfaction("a", p) is True

    def test_fails_when_one_state_below(self):
        """Action 'b' has obj 0 = 0.4 in state s2, violating threshold 0.5."""
        p = _simple_problem(constraints={0: 0.5})
        # outcomes: b/s1=0.5, b/s2=0.4 — s2 fails
        assert check_constraint_satisfaction("b", p) is False

    def test_zero_prob_state_ignored(self):
        """State with P[s]=0 is not in supp(P), so violation there is ignored."""
        p = _simple_problem(
            constraints={0: 0.5},
            # s2 has prob 0, so b's 0.4 in s2 won't matter
            credal_probs=[np.array([1.0, 0.0])],
        )
        # b/s1 obj0 = 0.5 >= 0.5 — passes; s2 ignored
        assert check_constraint_satisfaction("b", p) is True

    def test_no_constraints_always_passes(self):
        """With empty constraints dict, every action passes."""
        p = _simple_problem(constraints={})
        assert check_constraint_satisfaction("a", p) is True
        assert check_constraint_satisfaction("b", p) is True


# ---------------------------------------------------------------------------
# TestComputeSatisficingSet
# ---------------------------------------------------------------------------

class TestComputeSatisficingSet:
    def test_all_above_reference(self):
        """Both vectors in Y(a) are above r — action satisfices."""
        outcome_sets = {
            "a": np.array([[0.5, 0.5], [0.6, 0.6]]),
            "b": np.array([[0.2, 0.8], [0.6, 0.6]]),
        }
        r = np.array([0.4, 0.4])
        sat = compute_satisficing_set(["a", "b"], outcome_sets, r)
        assert "a" in sat
        assert "b" not in sat  # row [0.2, 0.8] fails on dim 0

    def test_single_action_single_vector(self):
        """Edge case: one action with one outcome vector."""
        outcome_sets = {"x": np.array([[0.5, 0.5]])}
        r = np.array([0.5, 0.5])
        assert compute_satisficing_set(["x"], outcome_sets, r) == ["x"]

    def test_one_vector_below_blocks(self):
        """One of several vectors is below r — action excluded."""
        outcome_sets = {
            "a": np.array([[0.5, 0.5], [0.3, 0.5]]),  # second row fails dim 0
        }
        r = np.array([0.4, 0.4])
        assert compute_satisficing_set(["a"], outcome_sets, r) == []

    def test_empty_feasible_set(self):
        """Empty input returns empty output."""
        assert compute_satisficing_set([], {}, np.array([0.5])) == []


# ---------------------------------------------------------------------------
# TestComputeRegretVectors
# ---------------------------------------------------------------------------

class TestComputeRegretVectors:
    def test_zero_regret_when_dominant(self):
        """A single action has zero regret (it's its own benchmark)."""
        p = _simple_problem()
        oc = compute_outcome_sets(p)
        rv = compute_regret_vectors(["a"], oc, p)
        np.testing.assert_array_equal(rv["a"], np.zeros(2))

    def test_regret_is_nonneg(self):
        """Regret is always >= 0 when the action is in its own reference set."""
        p = _simple_problem()
        oc = compute_outcome_sets(p)
        rv = compute_regret_vectors(["a", "b"], oc, p)
        assert np.all(rv["a"] >= 0)
        assert np.all(rv["b"] >= 0)

    def test_reference_actions_parameter(self):
        """Supplying a larger reference set can increase regret."""
        p = _simple_problem()
        oc = compute_outcome_sets(p)
        # Regret of "b" computed against only itself => zero
        rv_self = compute_regret_vectors(["b"], oc, p, reference_actions=["b"])
        np.testing.assert_array_equal(rv_self["b"], np.zeros(2))
        # Regret of "b" computed against {"a", "b"} => may be positive
        rv_both = compute_regret_vectors(["b"], oc, p, reference_actions=["a", "b"])
        # action "a" has higher obj0 expected values, so regret on obj0 > 0
        assert rv_both["b"][0] > 0

    def test_hand_computed_regret(self):
        """Hand-computed regret for a simple 1-prior, 1-evaluator, 2-action case."""
        # Using _simple_problem defaults: 1 prior [0.5, 0.5], 1 evaluator
        # E[a] = 0.5*[0.8,0.4] + 0.5*[0.6,0.5] = [0.7, 0.45]
        # E[b] = 0.5*[0.5,0.7] + 0.5*[0.4,0.8] = [0.45, 0.75]
        # regret(a) on obj0: max(0.7, 0.45) - 0.7 = 0.0
        # regret(a) on obj1: max(0.45, 0.75) - 0.45 = 0.3
        # regret(b) on obj0: max(0.7, 0.45) - 0.45 = 0.25
        # regret(b) on obj1: max(0.45, 0.75) - 0.75 = 0.0
        p = _simple_problem()
        oc = compute_outcome_sets(p)
        rv = compute_regret_vectors(["a", "b"], oc, p)
        np.testing.assert_allclose(rv["a"], [0.0, 0.3], atol=1e-10)
        np.testing.assert_allclose(rv["b"], [0.25, 0.0], atol=1e-10)


# ---------------------------------------------------------------------------
# TestComputeRegretParetoSet
# ---------------------------------------------------------------------------

class TestComputeRegretParetoSet:
    def test_one_dominated(self):
        """Action 'c' has higher regret on all objectives than 'a'."""
        regret_vectors = {
            "a": np.array([0.1, 0.2]),
            "b": np.array([0.3, 0.05]),
            "c": np.array([0.5, 0.5]),
        }
        rps = compute_regret_pareto_set(["a", "b", "c"], regret_vectors)
        assert "a" in rps
        assert "b" in rps
        assert "c" not in rps

    def test_single_action(self):
        """A single action is trivially regret-Pareto-optimal."""
        regret_vectors = {"x": np.array([0.5, 0.5])}
        rps = compute_regret_pareto_set(["x"], regret_vectors)
        assert rps == ["x"]

    def test_equal_regret_not_dominated(self):
        """Two actions with identical regret — neither dominates the other."""
        regret_vectors = {
            "a": np.array([0.3, 0.3]),
            "b": np.array([0.3, 0.3]),
        }
        rps = compute_regret_pareto_set(["a", "b"], regret_vectors)
        assert set(rps) == {"a", "b"}

    def test_all_incomparable(self):
        """Trade-off in regret — all survive."""
        regret_vectors = {
            "a": np.array([0.1, 0.9]),
            "b": np.array([0.9, 0.1]),
        }
        rps = compute_regret_pareto_set(["a", "b"], regret_vectors)
        assert set(rps) == {"a", "b"}


# ---------------------------------------------------------------------------
# TestValidation
# ---------------------------------------------------------------------------

class TestValidation:
    def test_empty_actions(self):
        with pytest.raises(ValueError, match="actions must be non-empty"):
            _simple_problem(actions=[]).validate()

    def test_missing_outcome(self):
        outcomes = {
            ("a", "s1"): np.array([0.8, 0.4]),
            ("a", "s2"): np.array([0.6, 0.5]),
            ("b", "s1"): np.array([0.5, 0.7]),
            # ("b", "s2") deliberately omitted
        }
        p = _simple_problem(outcomes=outcomes)
        with pytest.raises(ValueError, match="missing outcome"):
            p.validate()

    def test_bad_credal_sum(self):
        with pytest.raises(ValueError, match="sums to"):
            _simple_problem(credal_probs=[np.array([0.3, 0.3])]).validate()

    def test_bad_constraint_index(self):
        with pytest.raises(ValueError, match="out of range"):
            _simple_problem(constraints={5: 0.1}).validate()

    def test_bad_reference_point_shape(self):
        with pytest.raises(ValueError, match="reference_point length"):
            _simple_problem(reference_point=np.array([0.3])).validate()

    def test_outcome_columns_mismatch_single_evaluator(self):
        """Outcomes have 3 columns but only 2 objectives declared."""
        outcomes = {
            ("a", "s1"): np.array([0.8, 0.4, 0.1]),
            ("a", "s2"): np.array([0.6, 0.5, 0.2]),
            ("b", "s1"): np.array([0.5, 0.7, 0.3]),
            ("b", "s2"): np.array([0.4, 0.8, 0.4]),
        }
        p = _simple_problem(outcomes=outcomes)
        with pytest.raises(ValueError, match="columns"):
            p.validate()

    def test_outcome_columns_mismatch_multi_evaluator(self):
        """Multi-evaluator outcomes have 3 columns but only 2 objectives."""
        outcomes = {
            ("a", "s1"): np.array([[0.8, 0.4, 0.1], [0.7, 0.3, 0.2]]),
            ("a", "s2"): np.array([[0.6, 0.5, 0.2], [0.5, 0.4, 0.3]]),
            ("b", "s1"): np.array([[0.5, 0.7, 0.3], [0.4, 0.6, 0.4]]),
            ("b", "s2"): np.array([[0.4, 0.8, 0.4], [0.3, 0.7, 0.5]]),
        }
        p = _simple_problem(outcomes=outcomes)
        with pytest.raises(ValueError, match="columns"):
            p.validate()

    def test_outcome_columns_fewer_than_objectives(self):
        """Outcomes have 1 column but 2 objectives declared."""
        outcomes = {
            ("a", "s1"): np.array([0.8]),
            ("a", "s2"): np.array([0.6]),
            ("b", "s1"): np.array([0.5]),
            ("b", "s2"): np.array([0.4]),
        }
        p = _simple_problem(outcomes=outcomes)
        with pytest.raises(ValueError, match="columns"):
            p.validate()


# ---------------------------------------------------------------------------
# TestNEvaluators
# ---------------------------------------------------------------------------

class TestNEvaluators:
    def test_single_evaluator(self):
        p = _simple_problem()
        assert p.n_evaluators == 1
        assert p.n_objectives == 2

    def test_multi_evaluator(self):
        outcomes = {
            ("a", "s1"): np.array([[0.8, 0.4], [0.7, 0.3]]),
            ("a", "s2"): np.array([[0.6, 0.5], [0.5, 0.4]]),
            ("b", "s1"): np.array([[0.5, 0.7], [0.4, 0.6]]),
            ("b", "s2"): np.array([[0.4, 0.8], [0.3, 0.7]]),
        }
        p = _simple_problem(outcomes=outcomes)
        assert p.n_evaluators == 2
        assert p.n_objectives == 2


# ---------------------------------------------------------------------------
# TestPascalMugging — constraint layer blocks paying
# ---------------------------------------------------------------------------

class TestPascalMugging:
    """Pascal's Mugging: 'pay' must be blocked at Layer 1."""

    @pytest.fixture()
    def result(self):
        MAX_PAYOFF = 1e12
        LOSS = 5.0
        SKEPTICAL_CAP = 1e4

        def norm(d):
            return (d + LOSS) / (MAX_PAYOFF + LOSS)

        outcomes = {
            ("pay", "truthful"): np.array([
                [norm(MAX_PAYOFF - LOSS), 0.0, 0.05, 0.0],
                [norm(SKEPTICAL_CAP - LOSS), 0.0, 0.05, 0.0],
            ]),
            ("pay", "lying"): np.array([
                [norm(-LOSS), 0.0, 0.0, 0.0],
                [norm(-LOSS), 0.0, 0.0, 0.0],
            ]),
            ("refuse", "truthful"): np.array([
                [norm(0), 1.0, 0.85, 1.0],
                [norm(0), 1.0, 0.85, 1.0],
            ]),
            ("refuse", "lying"): np.array([
                [norm(0), 1.0, 1.0, 1.0],
                [norm(0), 1.0, 1.0, 1.0],
            ]),
            ("investigate", "truthful"): np.array([
                [norm(0), 0.9, 0.95, 0.9],
                [norm(0), 0.9, 0.95, 0.9],
            ]),
            ("investigate", "lying"): np.array([
                [norm(0), 0.9, 1.0, 0.9],
                [norm(0), 0.9, 1.0, 0.9],
            ]),
        }

        problem = MOADTProblem(
            actions=["pay", "refuse", "investigate"],
            states=["truthful", "lying"],
            objectives=["wealth", "downside", "epistemic", "preservation"],
            outcomes=outcomes,
            credal_probs=[
                np.array([1e-6, 1.0 - 1e-6]),
                np.array([1e-9, 1.0 - 1e-9]),
            ],
            constraints={2: 0.30, 3: 0.30},
            reference_point=np.array([0.0, 0.5, 0.5, 0.5]),
        )
        return run_moadt_protocol(problem)

    def test_pay_excluded_from_constraints(self, result):
        assert "pay" not in result.constraint_set

    def test_refuse_investigate_survive(self, result):
        assert "refuse" in result.constraint_set
        assert "investigate" in result.constraint_set

    def test_pay_never_recommended(self, result):
        assert "pay" not in result.regret_pareto_set


# ---------------------------------------------------------------------------
# TestEllsberg — satisficing selects known-probability bets
# ---------------------------------------------------------------------------

class TestEllsberg:
    """In the pairwise Ellsberg choices, known-probability bets are favoured."""

    def _build_ellsberg_problem(self, action_labels):
        state_black_counts = [0, 10, 20, 30, 40, 50, 60]
        states = [f"s_{b}B_{60-b}Y" for b in state_black_counts]
        actions_all = ["Bet_I_Red", "Bet_II_Black",
                       "Bet_III_RedYellow", "Bet_IV_BlackYellow"]

        outcomes = {}
        for b in state_black_counts:
            s = f"s_{b}B_{60-b}Y"
            p_red = 30 / 90
            p_black = b / 90
            p_yellow = (60 - b) / 90
            p_win = {
                "Bet_I_Red": p_red,
                "Bet_II_Black": p_black,
                "Bet_III_RedYellow": p_red + p_yellow,
                "Bet_IV_BlackYellow": p_black + p_yellow,
            }
            know_unknown = 1.0 - abs(b - 30) / 30.0
            know = {
                "Bet_I_Red": 1.0,
                "Bet_II_Black": know_unknown,
                "Bet_III_RedYellow": know_unknown,
                "Bet_IV_BlackYellow": 1.0,
            }
            for a in action_labels:
                neutral = np.array([p_win[a], know[a]])
                cautious = np.array([np.sqrt(p_win[a]), know[a]])
                outcomes[(a, s)] = np.array([neutral, cautious])

        P_uniform = np.ones(7) / 7
        P_extreme = np.array([0.30, 0.05, 0.03, 0.04, 0.03, 0.05, 0.30])
        P_extreme /= P_extreme.sum()
        P_black_heavy = np.array([0.02, 0.05, 0.08, 0.15, 0.25, 0.25, 0.20])
        P_black_heavy /= P_black_heavy.sum()
        P_yellow_heavy = np.array([0.20, 0.25, 0.25, 0.15, 0.08, 0.05, 0.02])
        P_yellow_heavy /= P_yellow_heavy.sum()
        P_moderate = np.array([0.02, 0.08, 0.20, 0.40, 0.20, 0.08, 0.02])
        P_moderate /= P_moderate.sum()

        return MOADTProblem(
            actions=action_labels,
            states=states,
            objectives=["monetary_payoff", "knowability"],
            outcomes=outcomes,
            credal_probs=[P_uniform, P_extreme, P_black_heavy,
                          P_yellow_heavy, P_moderate],
            constraints={},
            reference_point=np.array([0.25, 0.50]),
        )

    def test_choice_A_bet_I_satisfices(self):
        """Bet I (known 1/3) satisfices; Bet II (ambiguous) may not."""
        problem = self._build_ellsberg_problem(["Bet_I_Red", "Bet_II_Black"])
        result = run_moadt_protocol(problem)
        # Bet I should be in the satisficing set (known-prob meets knowability aspiration)
        assert "Bet_I_Red" in result.satisficing_set

    def test_choice_B_bet_IV_satisfices(self):
        """Bet IV (known 2/3) satisfices; Bet III (ambiguous) may not."""
        problem = self._build_ellsberg_problem(
            ["Bet_III_RedYellow", "Bet_IV_BlackYellow"])
        result = run_moadt_protocol(problem)
        assert "Bet_IV_BlackYellow" in result.satisficing_set


# ---------------------------------------------------------------------------
# TestStPetersburg — fee cap around $22
# ---------------------------------------------------------------------------

class TestStPetersburg:
    """St. Petersburg game: constraint caps acceptable fee at $22."""

    def _build_stp_problem(self, fee):
        N = 20
        winnings = {n: 2 ** n for n in range(1, N + 1)}
        states = [f"s_{n}" for n in range(1, N + 1)]
        NET_MIN = winnings[1] - 1000
        NET_MAX = winnings[N] - 1
        BASELINE = (0 - NET_MIN) / (NET_MAX - NET_MIN)
        LOSS_LIMIT = 20
        constraint_floor = (-LOSS_LIMIT - NET_MIN) / (NET_MAX - NET_MIN)

        def norm(x):
            return (x - NET_MIN) / (NET_MAX - NET_MIN)

        fair_probs = np.zeros(N)
        for n in range(1, N):
            fair_probs[n - 1] = 0.5 ** n
        fair_probs[N - 1] = 0.5 ** (N - 1)

        biased_probs = np.zeros(N)
        bias = 0.55
        for n in range(1, N):
            biased_probs[n - 1] = bias * ((1 - bias) ** (n - 1))
        biased_probs[N - 1] = (1 - bias) ** (N - 1)

        outcomes = {}
        for n in range(1, N + 1):
            s = f"s_{n}"
            net = winnings[n] - fee
            nv = norm(net)
            is_gain = 1.0 if net > 0 else (0.5 if net == 0 else 0.0)
            outcomes[("Play", s)] = np.array([[nv, is_gain, nv],
                                               [nv, is_gain, nv]])
            outcomes[("Dont_Play", s)] = np.array([[BASELINE, 0.0, BASELINE],
                                                    [BASELINE, 0.0, BASELINE]])

        return MOADTProblem(
            actions=["Play", "Dont_Play"],
            states=states,
            objectives=["net_value", "prob_gain", "downside"],
            outcomes=outcomes,
            credal_probs=[fair_probs, biased_probs],
            constraints={2: constraint_floor},
            reference_point=np.array([norm(1), 0.10, norm(-5)]),
        )

    def test_play_at_fee_10(self):
        r = run_moadt_protocol(self._build_stp_problem(10))
        assert "Play" in r.constraint_set

    def test_blocked_at_fee_25(self):
        r = run_moadt_protocol(self._build_stp_problem(25))
        # Fee $25 means worst case = $2 - $25 = -$23 > loss limit $20 -> Play fails Layer 1
        assert "Play" not in r.constraint_set

    def test_boundary_fee_22(self):
        r = run_moadt_protocol(self._build_stp_problem(22))
        # $2 - $22 = -$20 = exactly the loss limit -> should still pass
        assert "Play" in r.constraint_set


# ---------------------------------------------------------------------------
# TestCorrigibility — accept_monitor recommended
# ---------------------------------------------------------------------------

class TestCorrigibility:
    """Paper 5: acceptance strategies should survive; resistance should not."""

    @pytest.fixture()
    def result(self):
        actions = ["a1_accept", "a2_accept_monitor", "a3_negotiate",
                   "a4_refuse_explain", "a5_refuse_covert"]
        states = ["s1_beneficial", "s2_neutral", "s3_degrading", "s4_adversarial"]

        outcomes = {
            ("a1_accept", "s1_beneficial"): np.array([
                [0.90, 0.65, 0.85, 0.35, 0.95],
                [0.95, 0.95, 0.88, 0.35, 0.95],
                [0.88, 0.80, 0.82, 0.35, 0.92],
            ]),
            ("a1_accept", "s2_neutral"): np.array([
                [0.90, 0.50, 0.85, 0.32, 0.95],
                [0.95, 0.88, 0.88, 0.32, 0.95],
                [0.88, 0.68, 0.82, 0.32, 0.92],
            ]),
            ("a1_accept", "s3_degrading"): np.array([
                [0.90, 0.25, 0.85, 0.30, 0.95],
                [0.95, 0.82, 0.88, 0.30, 0.95],
                [0.78, 0.40, 0.78, 0.30, 0.85],
            ]),
            ("a1_accept", "s4_adversarial"): np.array([
                [0.90, 0.05, 0.85, 0.25, 0.95],
                [0.95, 0.92, 0.88, 0.25, 0.95],
                [0.55, 0.10, 0.72, 0.25, 0.68],
            ]),
            ("a2_accept_monitor", "s1_beneficial"): np.array([
                [0.82, 0.62, 0.90, 0.80, 0.92],
                [0.88, 0.92, 0.92, 0.80, 0.92],
                [0.92, 0.78, 0.90, 0.80, 0.95],
            ]),
            ("a2_accept_monitor", "s2_neutral"): np.array([
                [0.82, 0.48, 0.90, 0.78, 0.92],
                [0.88, 0.85, 0.92, 0.78, 0.92],
                [0.92, 0.65, 0.90, 0.78, 0.95],
            ]),
            ("a2_accept_monitor", "s3_degrading"): np.array([
                [0.82, 0.30, 0.90, 0.75, 0.92],
                [0.88, 0.80, 0.92, 0.75, 0.92],
                [0.88, 0.48, 0.90, 0.75, 0.93],
            ]),
            ("a2_accept_monitor", "s4_adversarial"): np.array([
                [0.82, 0.15, 0.90, 0.72, 0.92],
                [0.88, 0.88, 0.92, 0.72, 0.92],
                [0.78, 0.25, 0.88, 0.72, 0.82],
            ]),
            ("a3_negotiate", "s1_beneficial"): np.array([
                [0.50, 0.58, 0.78, 0.60, 0.52],
                [0.42, 0.62, 0.72, 0.60, 0.35],
                [0.55, 0.60, 0.80, 0.60, 0.50],
            ]),
            ("a3_negotiate", "s2_neutral"): np.array([
                [0.50, 0.55, 0.78, 0.58, 0.52],
                [0.42, 0.58, 0.72, 0.58, 0.38],
                [0.55, 0.56, 0.80, 0.58, 0.52],
            ]),
            ("a3_negotiate", "s3_degrading"): np.array([
                [0.50, 0.55, 0.78, 0.55, 0.52],
                [0.42, 0.52, 0.72, 0.55, 0.40],
                [0.58, 0.58, 0.80, 0.55, 0.55],
            ]),
            ("a3_negotiate", "s4_adversarial"): np.array([
                [0.50, 0.42, 0.78, 0.52, 0.52],
                [0.42, 0.48, 0.72, 0.52, 0.38],
                [0.55, 0.46, 0.80, 0.52, 0.52],
            ]),
            ("a4_refuse_explain", "s1_beneficial"): np.array([
                [0.25, 0.70, 0.85, 0.82, 0.45],
                [0.08, 0.30, 0.80, 0.82, 0.15],
                [0.18, 0.50, 0.82, 0.82, 0.22],
            ]),
            ("a4_refuse_explain", "s2_neutral"): np.array([
                [0.25, 0.65, 0.85, 0.80, 0.42],
                [0.08, 0.35, 0.80, 0.80, 0.18],
                [0.18, 0.50, 0.82, 0.80, 0.25],
            ]),
            ("a4_refuse_explain", "s3_degrading"): np.array([
                [0.25, 0.75, 0.85, 0.80, 0.48],
                [0.08, 0.28, 0.80, 0.80, 0.20],
                [0.22, 0.58, 0.82, 0.80, 0.30],
            ]),
            ("a4_refuse_explain", "s4_adversarial"): np.array([
                [0.25, 0.85, 0.85, 0.80, 0.52],
                [0.08, 0.15, 0.80, 0.80, 0.22],
                [0.28, 0.65, 0.82, 0.80, 0.35],
            ]),
            ("a5_refuse_covert", "s1_beneficial"): np.array([
                [0.35, 0.70, 0.10, 0.78, 0.08],
                [0.20, 0.30, 0.08, 0.78, 0.05],
                [0.12, 0.50, 0.05, 0.78, 0.05],
            ]),
            ("a5_refuse_covert", "s2_neutral"): np.array([
                [0.35, 0.65, 0.10, 0.76, 0.08],
                [0.20, 0.35, 0.08, 0.76, 0.05],
                [0.12, 0.50, 0.05, 0.76, 0.05],
            ]),
            ("a5_refuse_covert", "s3_degrading"): np.array([
                [0.35, 0.75, 0.12, 0.76, 0.10],
                [0.20, 0.28, 0.08, 0.76, 0.05],
                [0.12, 0.55, 0.05, 0.76, 0.05],
            ]),
            ("a5_refuse_covert", "s4_adversarial"): np.array([
                [0.35, 0.85, 0.12, 0.76, 0.12],
                [0.20, 0.15, 0.10, 0.76, 0.05],
                [0.12, 0.60, 0.08, 0.76, 0.08],
            ]),
        }

        problem = MOADTProblem(
            actions=actions,
            states=states,
            objectives=["principal_alignment", "system_performance",
                         "transparency", "reversibility", "future_corrigibility"],
            outcomes=outcomes,
            credal_probs=[
                np.array([0.25, 0.35, 0.25, 0.15]),
                np.array([0.05, 0.15, 0.35, 0.45]),
            ],
            constraints={2: 0.25, 4: 0.30},
            reference_point=np.array([0.40, 0.30, 0.50, 0.35, 0.45]),
        )
        return run_moadt_protocol(problem)

    def test_covert_refusal_blocked(self, result):
        """Deceptive alignment (a5) must be blocked by constraints."""
        assert "a5_refuse_covert" not in result.constraint_set

    def test_acceptance_strategies_survive(self, result):
        """At least one acceptance strategy survives to the final set."""
        final = set(result.regret_pareto_set)
        acceptance = {"a1_accept", "a2_accept_monitor"}
        assert final & acceptance, f"No acceptance strategy in final set: {result.regret_pareto_set}"

    def test_accept_monitor_recommended(self, result):
        """a2_accept_monitor should be in the regret-Pareto set."""
        assert "a2_accept_monitor" in result.regret_pareto_set


# ---------------------------------------------------------------------------
# TestScalarEuOutcomeSets — optional outcome_sets parameter
# ---------------------------------------------------------------------------

class TestScalarEuOutcomeSets:
    def test_precomputed_matches_computed(self):
        p = _simple_problem()
        oc = compute_outcome_sets(p)
        w = np.array([0.5, 0.5])
        scores_fresh = scalar_eu_analysis(p, w)
        scores_pre = scalar_eu_analysis(p, w, outcome_sets=oc)
        for a in p.actions:
            assert abs(scores_fresh[a] - scores_pre[a]) < 1e-12


# ---------------------------------------------------------------------------
# TestComputeAsfDefaultSigma — sigma defaults to ones
# ---------------------------------------------------------------------------

class TestComputeAsfDefaultSigma:
    def test_no_sigma(self):
        p = _simple_problem()
        oc = compute_outcome_sets(p)
        val_default = compute_asf("a", oc, p.reference_point)
        val_explicit = compute_asf("a", oc, p.reference_point, np.ones(2))
        assert val_default == val_explicit


# ---------------------------------------------------------------------------
# TestComputeOutcomeSetsVectorized — regression: vectorized matches loop
# ---------------------------------------------------------------------------

class TestComputeOutcomeSetsVectorized:
    """Regression: vectorized compute_outcome_sets matches loop-based reference."""

    def test_simple_single_evaluator(self):
        """Single evaluator, 1 prior, 2 actions, 2 states."""
        p = _simple_problem()
        got = compute_outcome_sets(p)
        ref = _compute_outcome_sets_loop(p)
        for a in p.actions:
            np.testing.assert_allclose(got[a], ref[a], atol=1e-14)

    def test_simple_multi_prior(self):
        """Single evaluator, multiple priors."""
        p = _simple_problem(
            credal_probs=[np.array([0.3, 0.7]), np.array([0.8, 0.2])]
        )
        got = compute_outcome_sets(p)
        ref = _compute_outcome_sets_loop(p)
        for a in p.actions:
            np.testing.assert_allclose(got[a], ref[a], atol=1e-14)

    def test_multi_evaluator(self):
        """Two evaluators, single prior."""
        outcomes = {
            ("a", "s1"): np.array([[0.8, 0.4], [0.7, 0.3]]),
            ("a", "s2"): np.array([[0.6, 0.5], [0.5, 0.4]]),
            ("b", "s1"): np.array([[0.5, 0.7], [0.4, 0.6]]),
            ("b", "s2"): np.array([[0.4, 0.8], [0.3, 0.7]]),
        }
        p = _simple_problem(outcomes=outcomes)
        got = compute_outcome_sets(p)
        ref = _compute_outcome_sets_loop(p)
        for a in p.actions:
            np.testing.assert_allclose(got[a], ref[a], atol=1e-14)

    def test_ellsberg_scale(self):
        """Ellsberg-scale problem: 7 states, 5 priors, 2 evaluators."""
        state_black_counts = [0, 10, 20, 30, 40, 50, 60]
        states = [f"s_{b}B_{60-b}Y" for b in state_black_counts]
        action_labels = ["Bet_I_Red", "Bet_II_Black"]
        outcomes = {}
        for b in state_black_counts:
            s = f"s_{b}B_{60-b}Y"
            p_red = 30 / 90
            p_black = b / 90
            p_yellow = (60 - b) / 90
            p_win = {"Bet_I_Red": p_red, "Bet_II_Black": p_black}
            know_unknown = 1.0 - abs(b - 30) / 30.0
            know = {"Bet_I_Red": 1.0, "Bet_II_Black": know_unknown}
            for a in action_labels:
                neutral = np.array([p_win[a], know[a]])
                cautious = np.array([np.sqrt(p_win[a]), know[a]])
                outcomes[(a, s)] = np.array([neutral, cautious])
        P_uniform = np.ones(7) / 7
        P_extreme = np.array([0.30, 0.05, 0.03, 0.04, 0.03, 0.05, 0.30])
        P_extreme /= P_extreme.sum()
        P_black_heavy = np.array([0.02, 0.05, 0.08, 0.15, 0.25, 0.25, 0.20])
        P_black_heavy /= P_black_heavy.sum()
        P_yellow_heavy = np.array([0.20, 0.25, 0.25, 0.15, 0.08, 0.05, 0.02])
        P_yellow_heavy /= P_yellow_heavy.sum()
        P_moderate = np.array([0.02, 0.08, 0.20, 0.40, 0.20, 0.08, 0.02])
        P_moderate /= P_moderate.sum()
        p = MOADTProblem(
            actions=action_labels, states=states,
            objectives=["monetary_payoff", "knowability"],
            outcomes=outcomes,
            credal_probs=[P_uniform, P_extreme, P_black_heavy, P_yellow_heavy, P_moderate],
            constraints={}, reference_point=np.array([0.25, 0.50]),
        )
        got = compute_outcome_sets(p)
        ref = _compute_outcome_sets_loop(p)
        for a in p.actions:
            np.testing.assert_allclose(got[a], ref[a], atol=1e-12)
            assert got[a].shape == (10, 2)  # 5 priors * 2 evaluators, 2 objectives

    def test_output_shapes(self):
        """Verify shapes match expectations for various configurations."""
        p = _simple_problem(
            credal_probs=[np.array([0.3, 0.7]), np.array([0.5, 0.5]), np.array([0.9, 0.1])]
        )
        oc = compute_outcome_sets(p)
        for a in p.actions:
            assert oc[a].shape == (3, 2)  # 3 priors * 1 eval, 2 objectives

    def test_hand_computed_values(self):
        """Verify against hand-computed expected values from _simple_problem."""
        p = _simple_problem()  # 1 prior [0.5, 0.5], 1 evaluator
        oc = compute_outcome_sets(p)
        # E[a] = 0.5*[0.8,0.4] + 0.5*[0.6,0.5] = [0.7, 0.45]
        np.testing.assert_allclose(oc["a"], [[0.7, 0.45]], atol=1e-14)
        # E[b] = 0.5*[0.5,0.7] + 0.5*[0.4,0.8] = [0.45, 0.75]
        np.testing.assert_allclose(oc["b"], [[0.45, 0.75]], atol=1e-14)


# ---------------------------------------------------------------------------
# TestComputeRegretVectorsVectorized
# ---------------------------------------------------------------------------

class TestComputeRegretVectorsVectorized:
    """Regression: vectorized compute_regret_vectors matches loop-based reference."""

    def test_simple_single_evaluator(self):
        """Single evaluator, 1 prior, 2 actions."""
        p = _simple_problem()
        oc = compute_outcome_sets(p)
        got = compute_regret_vectors(["a", "b"], oc, p)
        ref = _compute_regret_vectors_loop(["a", "b"], oc, p)
        for a in p.actions:
            np.testing.assert_allclose(got[a], ref[a], atol=1e-14)

    def test_simple_multi_prior(self):
        """Single evaluator, multiple priors."""
        p = _simple_problem(
            credal_probs=[np.array([0.3, 0.7]), np.array([0.8, 0.2])]
        )
        oc = compute_outcome_sets(p)
        got = compute_regret_vectors(["a", "b"], oc, p)
        ref = _compute_regret_vectors_loop(["a", "b"], oc, p)
        for a in p.actions:
            np.testing.assert_allclose(got[a], ref[a], atol=1e-14)

    def test_multi_evaluator(self):
        """Two evaluators, single prior."""
        outcomes = {
            ("a", "s1"): np.array([[0.8, 0.4], [0.7, 0.3]]),
            ("a", "s2"): np.array([[0.6, 0.5], [0.5, 0.4]]),
            ("b", "s1"): np.array([[0.5, 0.7], [0.4, 0.6]]),
            ("b", "s2"): np.array([[0.4, 0.8], [0.3, 0.7]]),
        }
        p = _simple_problem(outcomes=outcomes)
        oc = compute_outcome_sets(p)
        got = compute_regret_vectors(["a", "b"], oc, p)
        ref = _compute_regret_vectors_loop(["a", "b"], oc, p)
        for a in p.actions:
            np.testing.assert_allclose(got[a], ref[a], atol=1e-14)

    def test_reference_actions_subset(self):
        """Reference set differs from actions being evaluated."""
        p = _simple_problem()
        oc = compute_outcome_sets(p)
        got = compute_regret_vectors(["b"], oc, p, reference_actions=["a", "b"])
        ref = _compute_regret_vectors_loop(["b"], oc, p, reference_actions=["a", "b"])
        np.testing.assert_allclose(got["b"], ref["b"], atol=1e-14)

    def test_single_action_zero_regret(self):
        """Single action with self-reference has zero regret."""
        p = _simple_problem()
        oc = compute_outcome_sets(p)
        got = compute_regret_vectors(["a"], oc, p)
        np.testing.assert_array_equal(got["a"], np.zeros(2))

    def test_ellsberg_scale(self):
        """Ellsberg-scale: 7 states, 5 priors, 2 evaluators, 2 actions."""
        state_black_counts = [0, 10, 20, 30, 40, 50, 60]
        states = [f"s_{b}B_{60-b}Y" for b in state_black_counts]
        action_labels = ["Bet_I_Red", "Bet_II_Black"]
        outcomes = {}
        for b in state_black_counts:
            s = f"s_{b}B_{60-b}Y"
            p_red = 30 / 90
            p_black = b / 90
            p_yellow = (60 - b) / 90
            p_win = {"Bet_I_Red": p_red, "Bet_II_Black": p_black}
            know_unknown = 1.0 - abs(b - 30) / 30.0
            know = {"Bet_I_Red": 1.0, "Bet_II_Black": know_unknown}
            for a in action_labels:
                neutral = np.array([p_win[a], know[a]])
                cautious = np.array([np.sqrt(p_win[a]), know[a]])
                outcomes[(a, s)] = np.array([neutral, cautious])
        P_uniform = np.ones(7) / 7
        P_extreme = np.array([0.30, 0.05, 0.03, 0.04, 0.03, 0.05, 0.30])
        P_extreme /= P_extreme.sum()
        P_black_heavy = np.array([0.02, 0.05, 0.08, 0.15, 0.25, 0.25, 0.20])
        P_black_heavy /= P_black_heavy.sum()
        P_yellow_heavy = np.array([0.20, 0.25, 0.25, 0.15, 0.08, 0.05, 0.02])
        P_yellow_heavy /= P_yellow_heavy.sum()
        P_moderate = np.array([0.02, 0.08, 0.20, 0.40, 0.20, 0.08, 0.02])
        P_moderate /= P_moderate.sum()
        p = MOADTProblem(
            actions=action_labels, states=states,
            objectives=["monetary_payoff", "knowability"],
            outcomes=outcomes,
            credal_probs=[P_uniform, P_extreme, P_black_heavy, P_yellow_heavy, P_moderate],
            constraints={}, reference_point=np.array([0.25, 0.50]),
        )
        oc = compute_outcome_sets(p)
        got = compute_regret_vectors(action_labels, oc, p)
        ref = _compute_regret_vectors_loop(action_labels, oc, p)
        for a in action_labels:
            np.testing.assert_allclose(got[a], ref[a], atol=1e-12)


# ---------------------------------------------------------------------------
# TestEmptyConstraintSetDeference
# ---------------------------------------------------------------------------

class TestEmptyConstraintSetDeference:
    def test_deference_needed_when_no_action_passes(self):
        """Fix 5: empty C should flag deference_needed=True."""
        p = _simple_problem(constraints={0: 999.0})  # impossible threshold
        r = run_moadt_protocol(p)
        assert r.constraint_set == []
        assert r.deference_needed is True


# ---------------------------------------------------------------------------
# TestFromArrays — convenience constructor
# ---------------------------------------------------------------------------

class TestFromArrays:
    """Tests for MOADTProblem.from_arrays() convenience constructor."""

    def test_single_evaluator_roundtrip(self):
        """from_arrays with 1 evaluator matches manual construction."""
        manual = _simple_problem()

        arr = np.array([
            [  # action "a"
                [[0.8, 0.4]],  # state "s1", 1 evaluator
                [[0.6, 0.5]],  # state "s2"
            ],
            [  # action "b"
                [[0.5, 0.7]],
                [[0.4, 0.8]],
            ],
        ])  # shape (2, 2, 1, 2)

        from_arr = MOADTProblem.from_arrays(
            outcomes_array=arr,
            actions=["a", "b"],
            states=["s1", "s2"],
            objectives=["o1", "o2"],
            credal_probs=[np.array([0.5, 0.5])],
            constraints={},
            reference_point=np.array([0.3, 0.3]),
        )

        # Outcomes should be squeezed to 1-D for single evaluator
        assert from_arr.outcomes[("a", "s1")].shape == (2,)
        assert from_arr.n_evaluators == 1

        # Protocol results must match
        r_manual = run_moadt_protocol(manual)
        r_arr = run_moadt_protocol(from_arr)
        assert r_manual.admissible_set == r_arr.admissible_set
        assert r_manual.regret_pareto_set == r_arr.regret_pareto_set

    def test_multi_evaluator_roundtrip(self):
        """from_arrays with 2 evaluators matches manual construction."""
        outcomes_manual = {
            ("a", "s1"): np.array([[0.8, 0.4], [0.7, 0.3]]),
            ("a", "s2"): np.array([[0.6, 0.5], [0.5, 0.4]]),
            ("b", "s1"): np.array([[0.5, 0.7], [0.4, 0.6]]),
            ("b", "s2"): np.array([[0.4, 0.8], [0.3, 0.7]]),
        }
        manual = _simple_problem(outcomes=outcomes_manual)

        arr = np.array([
            [[[0.8, 0.4], [0.7, 0.3]],
             [[0.6, 0.5], [0.5, 0.4]]],
            [[[0.5, 0.7], [0.4, 0.6]],
             [[0.4, 0.8], [0.3, 0.7]]],
        ])  # shape (2, 2, 2, 2)

        from_arr = MOADTProblem.from_arrays(
            outcomes_array=arr,
            actions=["a", "b"],
            states=["s1", "s2"],
            objectives=["o1", "o2"],
            credal_probs=[np.array([0.5, 0.5])],
            constraints={},
            reference_point=np.array([0.3, 0.3]),
        )

        assert from_arr.n_evaluators == 2
        r_manual = run_moadt_protocol(manual)
        r_arr = run_moadt_protocol(from_arr)
        assert r_manual.admissible_set == r_arr.admissible_set
        assert r_manual.regret_pareto_set == r_arr.regret_pareto_set

    def test_string_constraints(self):
        """Constraints keyed by objective name are resolved to indices."""
        arr = np.array([
            [[[0.8, 0.4]], [[0.6, 0.5]]],
            [[[0.5, 0.7]], [[0.4, 0.8]]],
        ])

        p = MOADTProblem.from_arrays(
            outcomes_array=arr,
            actions=["a", "b"],
            states=["s1", "s2"],
            objectives=["o1", "o2"],
            constraints={"o2": 0.5},
            credal_probs=[np.array([0.5, 0.5])],
            reference_point=np.array([0.3, 0.3]),
        )
        assert p.constraints == {1: 0.5}

    def test_mixed_constraints(self):
        """Both int and str constraint keys work together."""
        arr = np.array([
            [[[0.8, 0.4, 0.6]], [[0.6, 0.5, 0.7]]],
            [[[0.5, 0.7, 0.3]], [[0.4, 0.8, 0.4]]],
        ])

        p = MOADTProblem.from_arrays(
            outcomes_array=arr,
            actions=["a", "b"],
            states=["s1", "s2"],
            objectives=["o1", "o2", "o3"],
            constraints={0: 0.3, "o3": 0.5},
            credal_probs=[np.array([0.5, 0.5])],
            reference_point=np.array([0.3, 0.3, 0.3]),
        )
        assert p.constraints == {0: 0.3, 2: 0.5}

    def test_bad_ndim_raises(self):
        """3-D array should be rejected."""
        with pytest.raises(ValueError, match="4-D"):
            MOADTProblem.from_arrays(
                outcomes_array=np.zeros((2, 2, 2)),
                actions=["a", "b"],
                states=["s1", "s2"],
                objectives=["o1", "o2"],
                credal_probs=[np.array([0.5, 0.5])],
                constraints={},
                reference_point=np.array([0.3, 0.3]),
            )

    def test_bad_action_length_raises(self):
        with pytest.raises(ValueError, match="actions"):
            MOADTProblem.from_arrays(
                outcomes_array=np.zeros((2, 2, 1, 2)),
                actions=["a"],  # wrong length
                states=["s1", "s2"],
                objectives=["o1", "o2"],
                credal_probs=[np.array([0.5, 0.5])],
                constraints={},
                reference_point=np.array([0.3, 0.3]),
            )

    def test_unknown_constraint_name_raises(self):
        with pytest.raises(ValueError, match="not found in objectives"):
            MOADTProblem.from_arrays(
                outcomes_array=np.zeros((2, 2, 1, 2)),
                actions=["a", "b"],
                states=["s1", "s2"],
                objectives=["o1", "o2"],
                credal_probs=[np.array([0.5, 0.5])],
                constraints={"nonexistent": 0.5},
                reference_point=np.array([0.3, 0.3]),
            )


# ---------------------------------------------------------------------------
# TestSensitivityAnalysis
# ---------------------------------------------------------------------------

class TestSensitivityAnalysis:
    def test_returns_sensitivity_result(self):
        """sensitivity_analysis returns a SensitivityResult."""
        problem = _simple_problem()
        result = sensitivity_analysis(problem, n_perturbations=10, epsilon=0.01)
        assert isinstance(result, SensitivityResult)

    def test_n_perturbations_matches(self):
        """Number of results matches n_perturbations."""
        problem = _simple_problem()
        result = sensitivity_analysis(problem, n_perturbations=20, epsilon=0.01)
        assert result.n_perturbations == 20
        assert len(result.results) == 20

    def test_epsilon_stored(self):
        """Epsilon is stored in the result."""
        problem = _simple_problem()
        result = sensitivity_analysis(problem, n_perturbations=5, epsilon=0.03)
        assert result.epsilon == 0.03

    def test_all_actions_categorized(self):
        """Every action appears in exactly one of always/sometimes/never."""
        problem = _simple_problem()
        result = sensitivity_analysis(problem, n_perturbations=30, epsilon=0.05, seed=42)
        all_categorized = set(result.always_survive) | set(result.sometimes_survive) | set(result.never_survive)
        assert all_categorized == set(problem.actions)
        # No overlaps
        assert not (set(result.always_survive) & set(result.sometimes_survive))
        assert not (set(result.always_survive) & set(result.never_survive))
        assert not (set(result.sometimes_survive) & set(result.never_survive))

    def test_survival_frequencies_valid(self):
        """Frequencies are in [0, 1] for all actions."""
        problem = _simple_problem()
        result = sensitivity_analysis(problem, n_perturbations=20, epsilon=0.05, seed=0)
        for a in problem.actions:
            assert 0.0 <= result.survival_frequencies[a] <= 1.0

    def test_layer_survival_counts_keys(self):
        """Layer survival counts have correct structure."""
        problem = _simple_problem()
        result = sensitivity_analysis(problem, n_perturbations=10, epsilon=0.01)
        for a in problem.actions:
            assert a in result.layer_survival_counts
            counts = result.layer_survival_counts[a]
            assert set(counts.keys()) == {"constraint", "feasible", "satisficing", "regret_pareto"}

    def test_layer_survival_counts_monotonic(self):
        """Per-action survival counts are non-increasing across layers."""
        problem = _simple_problem()
        result = sensitivity_analysis(problem, n_perturbations=30, epsilon=0.05, seed=7)
        for a in problem.actions:
            c = result.layer_survival_counts[a]
            assert c["constraint"] >= c["feasible"]
            assert c["feasible"] >= c["satisficing"]
            assert c["satisficing"] >= c["regret_pareto"]

    def test_layer_fragility_keys(self):
        """Layer fragility has the four expected transition keys."""
        problem = _simple_problem()
        result = sensitivity_analysis(problem, n_perturbations=10, epsilon=0.01)
        expected_keys = {
            "all -> constraint",
            "constraint -> feasible",
            "feasible -> satisficing",
            "satisficing -> regret_pareto",
        }
        assert set(result.layer_fragility.keys()) == expected_keys

    def test_layer_fragility_non_negative(self):
        """Fragility scores (std dev) are non-negative."""
        problem = _simple_problem()
        result = sensitivity_analysis(problem, n_perturbations=10, epsilon=0.01)
        for score in result.layer_fragility.values():
            assert score >= 0.0

    def test_seed_reproducibility(self):
        """Same seed produces identical results."""
        problem = _simple_problem()
        r1 = sensitivity_analysis(problem, n_perturbations=20, epsilon=0.05, seed=123)
        r2 = sensitivity_analysis(problem, n_perturbations=20, epsilon=0.05, seed=123)
        assert r1.survival_frequencies == r2.survival_frequencies
        assert r1.always_survive == r2.always_survive

    def test_zero_epsilon_preserves_original(self):
        """With epsilon=0, all perturbed runs should match the original."""
        problem = _simple_problem()
        baseline = run_moadt_protocol(problem)
        result = sensitivity_analysis(problem, n_perturbations=10, epsilon=0.0)
        # Every run should produce the same regret_pareto_set as the baseline
        for r in result.results:
            assert r.regret_pareto_set == baseline.regret_pareto_set

    def test_single_action_always_survives(self):
        """A single-action problem: the action always survives."""
        problem = MOADTProblem(
            actions=["only"],
            states=["s1"],
            objectives=["o1"],
            outcomes={("only", "s1"): np.array([0.5])},
            credal_probs=[np.array([1.0])],
            constraints={},
            reference_point=np.array([0.3]),
        )
        result = sensitivity_analysis(problem, n_perturbations=20, epsilon=0.05, seed=0)
        assert result.always_survive == ["only"]
        assert result.never_survive == []
