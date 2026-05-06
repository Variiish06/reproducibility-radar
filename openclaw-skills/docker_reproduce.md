---
name: docker_reproduce
description: >
  Runs the full reproduction loop inside an isolated Docker sandbox: pulls the
  base image, bind-mounts the /work volume, installs dependencies from
  requirements.txt, asks Claude to identify the main experiment command from
  the README, executes it under resource caps (4 CPU / 8 GB RAM / 30 min),
  and streams stdout+stderr to a log file.
when_to_use: >
  The core skill invoked for each of the top-10 selected papers during the
  nightly run. Also callable manually via scripts/reproduce_one.py for
  debugging a specific ArXiv ID.
---

<!-- Implementation will be added in Part B (sandbox.py + reproducer.py) -->
