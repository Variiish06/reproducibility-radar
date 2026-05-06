"""Placeholder tests — implementation comes in Part B."""
from radar.scoring import FailureCategory, ScoreDimensions


def test_failure_category_count() -> None:
    assert len(FailureCategory) == 13


def test_score_dimensions_total() -> None:
    dims = ScoreDimensions(installable=20, runnable=20, produces_output=20, numerically_close=20, documented=20)
    assert dims.total == 100


def test_score_dimensions_zero() -> None:
    assert ScoreDimensions().total == 0
