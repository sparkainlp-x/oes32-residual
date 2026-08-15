# Scope and Limitations

## Scope

This repository implements one exploratory computational construct: the maximum absolute difference between two supplied vectors of 32 finite real values, evaluated against a caller-supplied tolerance. Its purpose is to provide a compact, inspectable reference for checking that calculation and its stated decision rule.

The implementation is deliberately limited. It contains no data acquisition, no parameter estimation, no calibration, no probabilistic inference, no optimization, no simulation, and no external service dependency. It does not determine whether a chosen reference vector, observed vector, or tolerance is appropriate for any use case.

| Included | Not included |
|---|---|
| A deterministic 32-component numerical comparison | Measurement design or data collection |
| Explicit input validation and a pass/fail rule | Empirical validation or statistical inference |
| Contract tests for documented behavior | Domain-specific thresholds or recommended actions |
| Reproducible source code and documentation | Claims about physical, biological, psychological, or metaphysical phenomena |

## Limitations

A result from this implementation is conditional on the exact values supplied by the caller. The software checks only whether the largest absolute component difference is within the supplied tolerance. It does not indicate why vectors differ, whether a difference is meaningful, or whether the tolerance is justified.

Floating-point arithmetic is used for the numerical calculation. The stated contract concerns the algorithm and the comparison rule; users who require cross-platform bitwise identity or a particular numerical error analysis should independently validate the relevant runtime, hardware, and input ranges.

> **Interpretation boundary.** A pass or failure is solely the result of the documented comparison. It is not evidence of a physical effect, a biological property, consciousness, or any other claim beyond the computation.

## Review expectations

Independent review can reproduce the repository's stated behavior by inspecting [the residual definition](../residual_definition.md), [the failure criterion](../failure_criterion.md), [`src/residual_reference.py`](../src/residual_reference.py), and [`tests/test_contracts.py`](../tests/test_contracts.py). Reviewers should separately assess the suitability of any inputs, tolerance, and external application.
