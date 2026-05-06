# Failure Taxonomy

Every failed attempt is assigned exactly one of the following 13 labels.

| Category | Description |
|---|---|
| `env_python_version` | Python version mismatch |
| `env_missing_dep` | requirements.txt incomplete |
| `env_version_conflict` | pip resolver failure |
| `env_compilation_failed` | C extension build failure |
| `data_download_broken` | Dataset URL 404 or auth-walled |
| `data_not_provided` | Dataset not included and no download path |
| `command_unclear` | Claude could not identify the main command |
| `runtime_oom` | Out of memory inside container |
| `runtime_cuda_missing` | Code requires GPU we don't have |
| `runtime_crashed` | Exception not covered by another category |
| `results_no_output` | Script ran but produced no result file or metric line |
| `results_metric_mismatch_small` | Observed metric within 10% of claimed |
| `results_metric_mismatch_large` | Observed metric more than 10% off claimed |
