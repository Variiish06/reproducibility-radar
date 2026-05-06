# Reproducibility Radar

**Team AVANI — Samsung PRISM "OpenClaw: Clash of the Claws" Hackathon**

Reproducibility Radar is a nightly agent that automatically verifies whether machine-learning papers published on ArXiv can actually be reproduced. Each night it pulls new papers from cs.LG, cs.CL, and cs.AI, filters to those that have a linked GitHub repo and are feasible to run on CPU hardware, selects the top 10 candidates using a five-signal heuristic (repo activity, attention proxy, lab diversity), then spins up isolated Docker sandboxes to clone, install, run, and verify each one. Observed metrics are compared against the numbers claimed in the paper, failures are classified into one of 13 categories, and each attempt receives a 0–100 reproducibility score across five dimensions: installable, runnable, produces output, numerically close, and documented. Claude (Anthropic API) powers run planning, log analysis, metric extraction, and failure classification throughout.

Results are published to a public leaderboard website with per-paper detail pages and per-lab rollup charts. Once a week a DOCX digest is generated and emailed to subscribers. The system runs on a single Linux VPS (16 GB RAM, 8 vCPU, 200 GB disk) with no Kubernetes required — just Docker Compose.

## Running the project

### Prerequisites
- Docker ≥ 24 and Docker Compose v2
- Node.js 20+ (for the frontend)
- A `.env` file populated from `.env.example`

### Quickstart

```bash
# 1. Clone and configure
cp .env.example .env
# Fill in ANTHROPIC_API_KEY, GITHUB_TOKEN, DATABASE_URL, SMTP_* values

# 2. Start Postgres + orchestrator + frontend
docker compose up -d

# 3. Run DB migrations (first time)
docker compose exec orchestrator alembic upgrade head

# 4. Trigger a manual single-paper run (for testing)
docker compose exec orchestrator python scripts/reproduce_one.py --arxiv-id 2401.00001

# 5. Open the leaderboard
# http://localhost:3000
```

The orchestrator's nightly job is scheduled via an internal cron. Logs stream to stdout and are captured by Docker's log driver.
