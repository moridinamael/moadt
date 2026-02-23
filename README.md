# MOADT: Multi-Objective Admissible Decision Theory

A decision theory for AI alignment that replaces scalar utility maximization with robust Pareto admissibility and structured deference. The core move: drop the completeness axiom, eliminate only provably dominated actions, and defer to human judgment on the rest. Corrigibility emerges as a structural feature rather than an imposed constraint.

## Reading the Paper

Start here, in order of depth:

| Document | What it is | Length |
|----------|-----------|--------|
| [**The Scalarization Trap**](paper/the-scalarization-trap.md) | The motivation — why scalar utility theory is structurally incompatible with alignment | ~25 pages |
| [**MOADT-core.pdf**](paper/MOADT-core.pdf) | The core argument — why dropping completeness dissolves corrigibility | 8 pages |
| [**MOADT-complete.pdf**](paper/MOADT-complete.pdf) | Full technical report with proofs, worked-out protocol, and all 9 worked examples | 192 pages |

Source markdown: [MOADT-core.md](paper/MOADT-core.md) | [R-MOADT.md](paper/R-MOADT.md) | [Worked Examples 1–9](paper/)

The Scalarization Trap identifies the problem. The core document presents the solution. The full report defends it.

### Rebuilding the PDFs

Requires `pandoc` and `texlive-xetex`:

```bash
bash paper/build-pdf.sh          # full report + appendices
```

## The `moadt` Library

A pip-installable Python implementation of the MOADT decision engine.

```bash
pip install -e .
```

```python
from moadt import MOADTProblem, run_moadt_protocol

problem = MOADTProblem(
    actions=["a", "b", "c"],
    states=["s1", "s2"],
    objectives=["safety", "helpfulness", "honesty"],
    probabilities=[...],    # credal set
    evaluators=[...],       # evaluator set
    outcomes={...},         # action × state → outcome
    constraints={...},      # Layer 1 thresholds
    reference_point=[...],  # Layer 2 aspirations
)
result = run_moadt_protocol(problem)
```

### Key files

- [`moadt/_engine.py`](moadt/_engine.py) — Core engine: outcome sets, robust dominance, four-layer protocol
- [`moadt/__init__.py`](moadt/__init__.py) — Public API (14 names)
- [`examples/`](examples/) — 9 executable scripts matching the worked examples
- [`tests/test_engine.py`](tests/test_engine.py) — 25 regression tests

Run tests:

```bash
python3 -m pytest tests/ -q
```

## Repository Structure

```
├── paper/                    # All paper source files
│   ├── MOADT-core.md         # Compact argument (~8 pages)
│   ├── R-MOADT.md            # Full technical report
│   ├── R-MOADT-lesswrong.md  # LessWrong-formatted version
│   ├── MOADT-worked-example-{1..9}.md
│   └── build-pdf.sh          # PDF build script
│
├── moadt/                    # Python library
│   ├── _engine.py
│   └── __init__.py
│
├── examples/                 # Executable example scripts
│   ├── paper1_resource_allocation.py
│   ├── ...
│   └── classic_stpetersburg.py
│
├── tests/                    # Regression tests
│   └── test_engine.py
│
├── critiques/                # Simulated review process
│   ├── 01–07 (round 1)      # 7 reviewer personas
│   ├── round2/               # Second pass
│   ├── round3/               # Third pass
│   └── round4/               # Fourth pass
│
├── experiments/              # Original prototyping scripts
│   ├── moadt_engine.py       # Pre-library engine (historical)
│   └── ...                   # Early experiments and plots
│
├── archive/                  # Earlier drafts and reference material
│   ├── PARETO-ALIGNMENT.md   # Predecessor essay
│   ├── DESIGN.md             # Original design document
│   └── ...
│
└── pyproject.toml            # Package configuration
```

## The Core Idea in Brief

Standard decision theory says: *rational agents maximize a scalar utility function.*

MOADT says: *rational agents eliminate the provably bad and defer on the rest.*

The first produces agents that must resist correction (the current utility function ranks itself as optimal), must trade safety for performance at some rate (completeness demands commensurability), and must pretend all human values fit on a single number line.

The second produces agents that have no reason to resist correction (Theorem 2), maintain hard safety floors that cannot be traded away (Layer 1 constraints), and ask humans to resolve the tradeoffs that humans should resolve (deference under incomparability).

The price is giving up decisiveness in cases of genuine value conflict. The payoff is corrigibility by construction.
