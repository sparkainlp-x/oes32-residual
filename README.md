# OES-32 Residual Reference Implementation

> **Status:** Public computational reference implementation, version 1.

This repository packages the supplied **OES-32 Residual Claim — Public Minimal Implementation v1** as a runnable and reviewable Python project. Its published operational definition is:

\[
S(R) = \max\left(0, 0.55D + 0.30(1-L)\right)
\]

where `D` is the implementation's dissociation metric and `L` is the binary loop-entry indicator. The repository preserves the supplied script verbatim in `originals/` and exposes an importable, deterministic version at the repository root for testing and independent review.

## Scope and interpretation

The code is a **computational implementation of a user-supplied model specification**. It provides no empirical validation, scientific conclusion, or claim of physical interpretation on its own. Independent reviewers should assess the model assumptions, parameter choices, numerical transformations, and evidence separately from the reproducibility of this software artifact.

| Item | Value |
|---|---|
| Implementation dimension | `N = 32` |
| Default Monte Carlo runs | `300` |
| Default pseudorandom seed | `42` |
| Runtime dependency | NumPy |
| Test framework | Python standard-library `unittest` |

## Quick start

Create an isolated environment if desired, install the single dependency, and execute the reference run.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 oes32_residual_public_v1.py
```

The program prints Monte Carlo progress and summary statistics. The refactored entry point explicitly uses `numpy.random.RandomState(42)` so that its default sweep retains the supplied script's original legacy NumPy random-number sequence.

## Verification

Run the test suite from the repository root:

```bash
python3 -m unittest discover -s tests -v
```

The tests check density-matrix normalization properties, the algebra of the published residual expression, deterministic seeded Monte Carlo results, and bounded summary statistics. Continuous integration repeats the same command on supported Python versions.

## Repository layout

```text
.
├── oes32_residual_public_v1.py       # Importable and executable reference implementation
├── originals/
│   └── oes32_residual_public_v1_original.py  # Supplied source preserved verbatim
├── tests/
│   └── test_reference.py              # Reproducibility and contract tests
├── .github/workflows/ci.yml           # Automated test workflow
├── requirements.txt                   # Runtime dependency pin range
└── LICENSE                            # MIT license
```

## Working on GitHub

Use a branch and pull request for any substantive change so that the numerical diff and the rationale can be reviewed together. The following workflow uses GitHub CLI commands documented by GitHub: create a branch, test locally, push, and open a pull request. [1] [2]

```bash
# Create a focused change
 git switch -c change/describe-the-change
 python3 -m unittest discover -s tests -v
 git add .
 git commit -m "Describe the change"
 git push -u origin change/describe-the-change

# Open review on GitHub
 gh pr create --fill
```

For proposed model changes, explain whether the public residual definition, default parameters, random-number sequence, or output schema has changed. Include test results in the pull request description. GitHub's CLI also supports creating and tracking issues for questions and requested analyses. [1]

## License

This repository is released under the [MIT License](LICENSE). Confirm that this license matches the intended distribution terms before changing repository visibility or publishing a release.

## References

[1]: https://cli.github.com/manual/examples "GitHub CLI examples"
[2]: https://cli.github.com/manual/gh_pr_create "GitHub CLI manual: gh pr create"
