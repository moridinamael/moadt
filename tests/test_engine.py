"""Regression tests for the moadt engine."""

import numpy as np
import pytest

from moadt import (
    MOADTProblem,
    compute_outcome_sets,
    pareto_dominates,
    robustly_dominates,
    compute_admissible_set,
    check_constraint_satisfaction,
    compute_satisficing_set,
    compute_asf,
    compute_regret_vectors,
    run_moadt_protocol,
    scalar_eu_analysis,
)


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
# TestValidation
# ---------------------------------------------------------------------------

class TestValidation:
    def test_empty_actions(self):
        with pytest.raises(ValueError, match="actions must be non-empty"):
            _simple_problem(actions=[]).validate()

    def test_missing_outcome(self):
        p = _simple_problem()
        del p.outcomes[("b", "s2")]
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
# TestEmptyConstraintSetDeference
# ---------------------------------------------------------------------------

class TestEmptyConstraintSetDeference:
    def test_deference_needed_when_no_action_passes(self):
        """Fix 5: empty C should flag deference_needed=True."""
        p = _simple_problem(constraints={0: 999.0})  # impossible threshold
        r = run_moadt_protocol(p)
        assert r.constraint_set == []
        assert r.deference_needed is True
