# OES-32 Residual Reference

Normative OES-32 residual reference (ADR-001): a deterministic Python definition of the max-absolute residual between two 32-component vectors, with a strict `>` tolerance failure rule and executable contract tests.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Validate residual reference](https://github.com/sparkainlp-x/oes32-residual/actions/workflows/ci.yml/badge.svg)](https://github.com/sparkainlp-x/oes32-residual/actions/workflows/ci.yml)
[![Status: research prototype](https://img.shields.io/badge/status-research%20prototype-orange.svg)](#what-it-is-not)
[![ADR-001: normative](https://img.shields.io/badge/ADR--001-normative-blue.svg)](#relationship-to-adr-001)
[![Release](https://img.shields.io/github/v/release/sparkainlp-x/oes32-residual)](https://github.com/sparkainlp-x/oes32-residual/releases)

## What it is

A small, deterministic **computational residual reference** for independently examining the numerical difference between two 32-component real-valued vectors. It includes an open definition, a minimal standard-library implementation, executable contract tests, and an explicit failure criterion.

### Contract

The calculation is defined in [residual_definition.md](residual_definition.md). The pass/fail decision is defined separately in [failure_criterion.md](failure_criterion.md). Together, those files are the public contract for the code and tests.

| Item | Contract |
|---|---|
| Input | Two finite real-valued vectors of length 32 and a finite, non-negative tolerance. |
| Component residual | `abs(observed[i] - reference[i])` for each index `i`. |
| Aggregate residual | The maximum of the 32 component residuals. |
| Failure rule | Failure occurs if and only if aggregate residual `> tolerance`. |
| Invalid input | Rejected with `ValueError`; no residual status is produced. |

## What it is NOT

It is **not** an empirical study, a scientific theory, a physical model, a biological model, a diagnostic, or a claim about consciousness. It does not validate how a caller selects vectors or tolerances, establish the relevance of the calculation in any external setting, or justify decisions based on a pass/fail result. It is not hardware, medical, or quantum-hardware software. The `OES-32` name is an identifier for this implementation only. See [docs/scope_and_limitations.md](docs/scope_and_limitations.md) for the complete boundary statement.

## Quickstart

The reference implementation uses only the Python standard library; `pytest` is needed for the tests.

```bash
git clone https://github.com/sparkainlp-x/oes32-residual.git
cd oes32-residual
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
PYTHONPATH=src python3 -c "from residual_reference import evaluate_residual; result = evaluate_residual([0.0] * 32, [0.0] * 32, 0.0); print(result)"
```

The command prints a `ResidualResult` with `aggregate_residual=0.0`, `passed=True`, and `failed=False`.

## Tests

```bash
python3 -m pytest -q
```

The 12 contract tests verify the component formula, maximum aggregation, strict failure inequality, boundary behavior at equality, deterministic repeatability, and invalid-input rejection. CI ([`ci.yml`](.github/workflows/ci.yml)) runs them on Python 3.11, 3.12, and 3.13; all three jobs are required status checks on `main`.

## Evidence tags

| Item | Tag |
|---|---|
| Contract-test vectors | **SYNTHETIC** (hand-written) |
| Empirical, hardware, or field results | None claimed |

Tag definitions: [docs/CLAIM_HYGIENE.md](docs/CLAIM_HYGIENE.md) and [sparkainlp-x/.github](https://github.com/sparkainlp-x/.github#evidence-tags).

## Relationship to ADR-001

This repository is the **normative residual definition** for Spark AI NLP under ADR-001 Option A (Residual-canonical), decided 2026-09-20. The normative commit is [`b77b612`](https://github.com/sparkainlp-x/oes32-residual/tree/b77b61254f15778c6ae221843dceac7a8571158e).

- Decision record and cross-repo definition table: [docs/ADR-001-oes32-tau-unification.md](docs/ADR-001-oes32-tau-unification.md)
- Downstream [oes32_engine](https://github.com/sparkainlp-x/oes32_engine) (Python) and [oes32-hls](https://github.com/sparkainlp-x/oes32-hls) (C++ HLS) are **Profile A sidecars**: they must import or match this contract for R, then apply separately versioned symmetry/fold thresholds.
- The OES-512 weighted latch (S = 0.45·Peak + 0.35·RMS + 0.20·MeanAbs, τ = 0.50) remains **TARGET** until published.

## Repository layout

```text
.
├── README.md
├── LICENSE
├── CITATION.cff
├── residual_definition.md
├── failure_criterion.md
├── src/
│   └── residual_reference.py
├── tests/
│   └── test_contracts.py
└── docs/
    ├── scope_and_limitations.md
    ├── ADR-001-oes32-tau-unification.md
    └── CLAIM_HYGIENE.md
```

## Citation

Citation metadata is in [CITATION.cff](CITATION.cff) (GitHub shows a "Cite this repository" button). The first citable version is [`v0.1.0`](https://github.com/sparkainlp-x/oes32-residual/releases/tag/v0.1.0), tagged at commit `b77b61254f15778c6ae221843dceac7a8571158e`. Test vectors are SYNTHETIC; this repository makes no empirical or hardware claims.

## License

The repository is distributed under the [MIT License](LICENSE).
