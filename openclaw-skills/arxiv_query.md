---
name: arxiv_query
description: >
  Fetches recent ArXiv papers from cs.LG, cs.CL, and cs.AI submitted in the
  last 24 hours. Returns structured paper metadata including title, authors,
  abstract, ArXiv ID, PDF URL, and submission timestamp.
when_to_use: >
  Invoke at the start of each nightly run to populate the candidate pool
  before filtering and scoring. Also usable interactively to inspect what
  papers dropped today.
---

<!-- Implementation will be added in Part B (arxiv_crawler.py) -->
