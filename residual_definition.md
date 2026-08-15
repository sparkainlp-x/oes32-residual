# Residual Definition

## Purpose

This document specifies a small, deterministic **computational residual**. The residual is a numerical comparison between two finite real-valued vectors. It is intended to make the computation inspectable and reproducible; it does not assign any interpretation beyond that computation.

## Inputs

Let \(x, y \in \mathbb{R}^{32}\) be the reference and observed vectors, respectively. The vectors must each contain exactly 32 finite real numbers. Let \(\tau \in \mathbb{R}\) be a finite, non-negative tolerance.

| Symbol | Name | Type and constraint |
|---|---|---|
| \(x\) | Reference vector | A sequence of exactly 32 finite real values. |
| \(y\) | Observed vector | A sequence of exactly 32 finite real values. |
| \(\tau\) | Tolerance | A finite real value satisfying \(\tau \geq 0\). |
| \(r_i\) | Component residual | \(\lvert y_i - x_i \rvert\) for component \(i\). |
| \(R\) | Aggregate residual | The maximum component residual. |

## Calculation

For each component \(i \in \{1, \ldots, 32\}\), calculate the absolute component residual:

\[
r_i = \lvert y_i - x_i \rvert.
\]

The aggregate residual is the Chebyshev (maximum absolute) difference:

\[
R(x, y) = \max_{1 \leq i \leq 32} r_i = \max_{1 \leq i \leq 32} \lvert y_i - x_i \rvert.
\]

The reference implementation returns each \(r_i\), the aggregate \(R\), the supplied tolerance \(\tau\), and a Boolean status derived solely from the documented failure criterion. It performs no random sampling, model fitting, state mutation, normalization, or external I/O.

> **Determinism.** For identical valid inputs, the implementation applies the same finite arithmetic operations in the same order and returns the same values and status within a given Python runtime and numeric platform.

## Input validity

The computation is undefined for an input with a non-finite value, a vector length other than 32, a non-real value, or a negative tolerance. The reference implementation rejects these inputs with `ValueError` rather than producing a residual.

## Interpretation boundary

`OES-32` is only an identifier for this 32-component computational reference. This definition does not establish a physical quantity, a biological measurement, a statement about consciousness, or an empirical model.
