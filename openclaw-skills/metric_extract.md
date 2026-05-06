---
name: metric_extract
description: >
  Uses Claude to parse the sandbox log and extract the headline numeric metric
  (accuracy, F1, BLEU, perplexity, etc.) that corresponds to the metric
  claimed in the paper. Returns the observed value and the metric name, or
  null if no metric line is found. Also classifies the failure into one of
  the 13 canonical failure categories if extraction fails.
when_to_use: >
  Called after docker_reproduce completes (whether the run succeeded or
  crashed). Always runs so we can capture partial results and assign a
  failure category even for errored runs.
---

<!-- Implementation will be added in Part B (claude_planner.py) -->
