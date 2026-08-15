# OES-32 Residual Reference

This repository is a small, deterministic **computational residual reference** for independently examining the numerical difference between two 32-component real-valued vectors. It includes an open definition, a minimal reference implementation, executable contract tests, and an explicit failure criterion.

It is **not** an empirical study, a scientific theory, a physical model, a biological model, a diagnostic, or a claim about consciousness. The `OES-32` name is an identifier for this implementation only.

## Contract

The calculation is defined in [residual_definition.md](residual_definition.md). The pass/fail decision is defined separately in [failure_criterion.md](failure_criterion.md). Together, those files are the public contract for the code and tests.

| Item | Contract |
|---|---|
| Input | Two finite real-valued vectors of length 32 and a finite, non-negative tolerance. |
| Component residual | `abs(observed[i] - reference[i])` for each index `i`. |
| Aggregate residual | The maximum of the 32 component residuals. |
| Failure rule | Failure occurs if and only if aggregate residual `> tolerance`. |
| Invalid input | Rejected with `ValueError`; no residual status is produced. |

## Run the reference code

The reference implementation uses only the Python standard library. Create an environment, install the test dependency, and evaluate a simple input from the repository root.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
PYTHONPATH=src python3 -c "from residual_reference import evaluate_residual; result = evaluate_residual([0.0] * 32, [0.0] * 32, 0.0); print(result)"
```

The command prints a `ResidualResult` with an aggregate residual of `0.0`, `passed=True`, and `failed=False`.

## Run the contract tests

Run the complete contract suite from the repository root:

```bash
python3 -m pytest -q
```

The tests verify the component formula, maximum aggregation, strict failure inequality, boundary behavior at equality, deterministic repeatability, and invalid-input rejection.

## Repository layout

```text
.
├── README.md
├── LICENSE
├── residual_definition.md
├── failure_criterion.md
├── src/
│   └── residual_reference.py
├── tests/
│   └── test_contracts.py
└── docs/
    └── scope_and_limitations.md
```

## Scope

This repository supplies a transparent software artifact for a narrowly defined numerical comparison. It does not validate how a caller selects vectors or tolerances, establish the relevance of the calculation in any external setting, or justify decisions based on a pass/fail result. See [docs/scope_and_limitations.md](docs/scope_and_limitations.md) for the complete boundary statement.

## License

The repository is distributed under the [MIT License](LICENSE).
