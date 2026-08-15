# Validation Record

**Validation date:** 2026-08-15  
**Implementation:** OES-32 Residual Public v1  
**Environment:** Python 3.11 and NumPy available in the build environment

## Scope

This record documents **software-level checks only**. Passing tests confirms that the packaged code executes deterministically under the stated seed and that selected mathematical and structural contracts hold. It does not validate the model's scientific interpretation, parameter selection, or external claims.

| Check | Command | Result |
|---|---|---|
| Syntax compilation | `python3 -m py_compile oes32_residual_public_v1.py tests/test_reference.py` | Passed |
| Contract test suite | `python3 -m unittest discover -s tests -v` | Passed: 4/4 tests |
| Default deterministic sweep | `python3 oes32_residual_public_v1.py` | Completed: 300/300 runs |

## Test coverage

The four contract tests verify that density-matrix normalization produces a Hermitian, unit-trace, positive-semidefinite result; that the published residual expression evaluates as expected for both loop states; that seeded Monte Carlo results repeat exactly; and that summary proportions remain within their defined bounds.

## Reference execution summary

The default 300-run sweep completed successfully with the output formatting provided by the source implementation. At four decimal places, the reported mean, standard deviation, median, and 5th–95th-percentile interval for `S(R)` display as `0.0000`; the run also reports an `11.0%` positive-`S(R)` fraction and `100.0%` loop-entry rate. The apparent discrepancy is a display-precision consideration: values can be positive but smaller than the four-decimal reporting precision.

> Reproduce the validation after any numerical change. Treat differences in the residual formula, random-number sequence, result schema, or default parameter ranges as review-requiring changes.
