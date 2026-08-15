"""Contract tests for the documented OES-32 residual reference."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from residual_reference import DIMENSION, calculate_residual, evaluate_residual


def vector_with(value: float, index: int = 0) -> list[float]:
    """Return a zero vector with one specified component set to ``value``."""
    vector = [0.0] * DIMENSION
    vector[index] = value
    return vector


def test_zero_difference_has_zero_component_and_aggregate_residuals() -> None:
    result = evaluate_residual([0.0] * DIMENSION, [0.0] * DIMENSION, tolerance=0.0)

    assert result.component_residuals == (0.0,) * DIMENSION
    assert result.aggregate_residual == 0.0
    assert result.passed is True
    assert result.failed is False


def test_aggregate_residual_is_the_maximum_absolute_component_difference() -> None:
    observed = vector_with(-0.75, index=7)
    observed[13] = 0.50

    component_residuals, aggregate_residual = calculate_residual(
        [0.0] * DIMENSION, observed
    )

    assert component_residuals[7] == 0.75
    assert component_residuals[13] == 0.50
    assert aggregate_residual == max(component_residuals) == 0.75


def test_residual_equal_to_tolerance_passes() -> None:
    result = evaluate_residual(
        [0.0] * DIMENSION, vector_with(0.25), tolerance=0.25
    )

    assert result.aggregate_residual == 0.25
    assert result.passed is True
    assert result.failed is False


def test_residual_strictly_greater_than_tolerance_fails() -> None:
    result = evaluate_residual(
        [0.0] * DIMENSION, vector_with(0.250001), tolerance=0.25
    )

    assert result.aggregate_residual == 0.250001
    assert result.passed is False
    assert result.failed is True


def test_identical_valid_inputs_produce_identical_results() -> None:
    reference = [float(index) / 10.0 for index in range(DIMENSION)]
    observed = [value + 0.125 for value in reference]

    first = evaluate_residual(reference, observed, tolerance=0.125)
    second = evaluate_residual(reference, observed, tolerance=0.125)

    assert first == second


@pytest.mark.parametrize(
    ("reference", "observed", "tolerance"),
    [
        ([0.0] * (DIMENSION - 1), [0.0] * DIMENSION, 0.0),
        ([0.0] * DIMENSION, [0.0] * (DIMENSION + 1), 0.0),
        (vector_with(math.nan), [0.0] * DIMENSION, 0.0),
        ([0.0] * DIMENSION, vector_with(math.inf), 0.0),
        ([0.0] * DIMENSION, [0.0] * DIMENSION, -0.01),
        ([0.0] * DIMENSION, [0.0] * DIMENSION, math.nan),
        ([0.0] * DIMENSION, [0.0] * DIMENSION, True),
    ],
)
def test_invalid_inputs_are_rejected(
    reference: list[float], observed: list[float], tolerance: float
) -> None:
    with pytest.raises(ValueError):
        evaluate_residual(reference, observed, tolerance)
