"""Computes the 0-100 reproducibility score across 5 dimensions (0-20 each)."""
from __future__ import annotations

import enum
from dataclasses import dataclass


class FailureCategory(str, enum.Enum):
    env_python_version = "env_python_version"
    env_missing_dep = "env_missing_dep"
    env_version_conflict = "env_version_conflict"
    env_compilation_failed = "env_compilation_failed"
    data_download_broken = "data_download_broken"
    data_not_provided = "data_not_provided"
    command_unclear = "command_unclear"
    runtime_oom = "runtime_oom"
    runtime_cuda_missing = "runtime_cuda_missing"
    runtime_crashed = "runtime_crashed"
    results_no_output = "results_no_output"
    results_metric_mismatch_small = "results_metric_mismatch_small"
    results_metric_mismatch_large = "results_metric_mismatch_large"


@dataclass
class ScoreDimensions:
    """Each dimension is 0–20; total is 0–100."""
    installable: int = 0        # Docker setup succeeded
    runnable: int = 0           # Main command ran without crashing
    produces_output: int = 0    # Numeric/structured artifact appeared
    numerically_close: int = 0  # Headline metric within 10% of claimed
    documented: int = 0         # Claude-rated README sufficiency

    @property
    def total(self) -> int:
        return (
            self.installable
            + self.runnable
            + self.produces_output
            + self.numerically_close
            + self.documented
        )


# Full scoring logic in Part B
