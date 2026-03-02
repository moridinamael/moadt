"""moadt -- Multi-Objective Admissible Decision Theory."""

from importlib.metadata import PackageNotFoundError, version as _meta_version

try:
    __version__: str = _meta_version("moadt")
except PackageNotFoundError:
    __version__ = "0.1.0"

from moadt._engine import (
    MOADTProblem,
    MOADTResult,
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
    print_trace,
    sensitivity_analysis,
)

__all__ = [
    "__version__",
    "MOADTProblem",
    "MOADTResult",
    "SensitivityResult",
    "compute_outcome_sets",
    "pareto_dominates",
    "robustly_dominates",
    "compute_admissible_set",
    "check_constraint_satisfaction",
    "compute_satisficing_set",
    "compute_asf",
    "compute_regret_vectors",
    "compute_regret_pareto_set",
    "run_moadt_protocol",
    "scalar_eu_analysis",
    "print_trace",
    "sensitivity_analysis",
]
