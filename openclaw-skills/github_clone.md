---
name: github_clone
description: >
  Extracts a GitHub repository URL from a paper's abstract text and/or the
  first two pages of its PDF, then clones the repo into the sandbox /work
  volume. Handles github.com links, anonymous submission redirects, and
  Papers With Code links.
when_to_use: >
  Called after a paper passes the binary filters (has repo + CPU-feasible)
  and has been selected as a top-10 candidate. Runs inside the sandbox
  setup phase before the main experiment command is executed.
---

<!-- Implementation will be added in Part B (paper2code.py + sandbox.py) -->
