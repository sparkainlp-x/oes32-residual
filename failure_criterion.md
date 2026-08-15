# Failure Criterion

## Normative rule

For valid vectors \(x, y \in \mathbb{R}^{32}\) and a valid tolerance \(\tau \geq 0\), calculate the aggregate residual \(R(x,y)\) as defined in [the residual definition](residual_definition.md):

\[
R(x,y) = \max_{1 \leq i \leq 32} \lvert y_i - x_i \rvert.
\]

The residual **fails if and only if**:

\[
R(x,y) > \tau.
\]

Equality is not failure. Therefore, \(R(x,y) = \tau\) passes the criterion.

## Decision table

| Condition | Required result | Rationale |
|---|---|---|
| Both vectors are valid, \(\tau\) is valid, and \(R \leq \tau\) | `passed = True`, `failed = False` | No component exceeds the permitted absolute difference. |
| Both vectors are valid, \(\tau\) is valid, and \(R > \tau\) | `passed = False`, `failed = True` | At least one component exceeds the permitted absolute difference. |
| Either vector is not a finite real-valued sequence of length 32 | Raise `ValueError`; do not report pass or failure | The residual is not defined for invalid vectors. |
| Tolerance is non-finite, non-real, or negative | Raise `ValueError`; do not report pass or failure | The threshold is not valid under this contract. |

## Measurable examples

| Reference vector \(x\) | Observed vector \(y\) | Tolerance \(\tau\) | Aggregate residual \(R\) | Required status |
|---|---|---:|---:|---|
| 32 zeros | 32 zeros | 0.0 | 0.0 | Pass |
| 32 zeros | One component is 0.25; all others are 0 | 0.25 | 0.25 | Pass |
| 32 zeros | One component is 0.250001; all others are 0 | 0.25 | 0.250001 | Fail |

## Testability and review

The contract tests in [`tests/test_contracts.py`](tests/test_contracts.py) exercise the formula, the strict inequality at the tolerance boundary, a known failure case, and invalid-input rejection. A proposed change to this rule is a change to the public contract and should update this file, [the residual definition](residual_definition.md), the implementation, and the tests together.

> **Scope of the result.** A passing status means only that the two supplied vectors satisfy this numerical threshold. A failing status means only that they do not. Neither status supports an inference outside this computational comparison.
