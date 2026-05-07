# Part A Verification Guide

This is for AVANI teammates testing the scaffolding on a fresh machine. Goal: confirm the project clones, all services boot, migrations apply, frontend renders, and tests pass — *before* anyone starts on Part B.

If any step fails, **stop and paste the exact error in the team chat**. Do not try to fix it solo — we want a clean baseline first.

Estimated time: **30 minutes** if you have prerequisites installed, ~60 minutes if not.

---

## 0. Prerequisites — install these first

You need all four. Check each with the version commands; if any fails, install before moving on.

| Tool | Min version | Check command | Where to get it |
|---|---|---|---|
| Git | 2.40+ | `git --version` | https://git-scm.com/downloads |
| Python | 3.11 (exactly) | `python --version` or `python3 --version` | https://www.python.org/downloads/ |
| Node.js | 20+ | `node --version` | https://nodejs.org (LTS) |
| Docker Desktop | latest | `docker --version` and `docker compose version` | https://www.docker.com/products/docker-desktop |

**Important platform notes:**

- **Windows users**: install Docker Desktop with the WSL 2 backend. After install, open Docker Desktop once and let it finish setting up before continuing.
- **Mac users**: Docker Desktop is a ~1 GB download — start it early.
- **Make sure Docker Desktop is actually running** before any step that uses Docker. The whale icon should be in your system tray / menu bar.

---

## 1. Clone the repo

```bash
git clone https://github.com/Variiish06/reproducibility-radar.git
cd reproducibility-radar
```

Verify the structure looks right:

```bash
# Mac/Linux
ls -la

# Windows PowerShell
Get-ChildItem -Force
```

You should see at minimum: `orchestrator/`, `frontend/`, `sandbox-images/`, `openclaw-skills/`, `scripts/`, `docs/`, `.gitignore`, `.env.example`, `README.md`, `CLAUDE.md`, `LICENSE`.

If anything's missing → flag in chat.

---

## 2. Set up the .env file

```bash
# Mac/Linux
cp .env.example .env

# Windows PowerShell
Copy-Item .env.example .env
```

Open `.env` in any editor. For verification, you only need:

```
DATABASE_URL=postgresql://radar:changeme@localhost:5432/radar
```

You do **not** need real `ANTHROPIC_API_KEY` or `GITHUB_TOKEN` values for Part A verification — those are only used in Part B. Leave the placeholders.

**Never commit your `.env`** — `.gitignore` already excludes it, but be aware.

---

## 3. Verify the Python orchestrator

```bash
cd orchestrator
python -m venv .venv
```

Activate the virtual environment:

```bash
# Mac/Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1

# Windows Command Prompt
.venv\Scripts\activate.bat
```

(If PowerShell blocks the script, run once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then retry.)

Your prompt should now show `(.venv)` at the start.

Install dependencies:

```bash
pip install -e ".[dev]"
```

This will take 1–3 minutes. If it fails, paste the full error.

**Run the toolchain checks — all three should pass with zero issues:**

```bash
ruff check .
mypy radar/
pytest -v
```

**Expected results:**
- `ruff check .` → `All checks passed!` 
- `mypy radar/` → `Success: no issues found` 
- `pytest -v` → 3 tests pass (the smoke tests in `tests/test_scoring.py`)

If any of these fail → paste the full output in chat.

---

## 4. Verify the database migration

Make sure Docker Desktop is running, then from the `orchestrator/` folder:

```bash
docker compose up -d postgres
```

Wait ~10 seconds for Postgres to finish starting. Verify it's healthy:

```bash
docker compose ps
```

You should see `postgres` with status `Up` and `(healthy)`. If it says `(starting)`, wait another 10 seconds and check again.

**Apply the migration:**

```bash
# Mac/Linux
export DATABASE_URL="postgresql://radar:changeme@localhost:5432/radar"
alembic upgrade head

# Windows PowerShell
$env:DATABASE_URL="postgresql://radar:changeme@localhost:5432/radar"
alembic upgrade head
```

**Expected output:** something like `Running upgrade  -> 0001, initial_schema`.

**Verify the tables actually exist:**

```bash
docker compose exec postgres psql -U radar -d radar -c "\dt"
```

You should see exactly these tables: `alembic_version`, `attempts`, `labs`, `papers`, `subscribers`. If any are missing → flag.

**Test that the migration is reversible** (this catches sloppy migrations):

```bash
alembic downgrade base
alembic upgrade head
```

Both should succeed without errors.

---

## 5. Verify the frontend builds

Open a **second terminal** (keep Postgres running in the first). Navigate to the repo root, then:

```bash
cd frontend
npm install
```

This takes 1–2 minutes.

```bash
npm run build
```

Expected: build completes with no errors. You'll see Next.js output ending with route listings.

```bash
npm run dev
```

Open http://localhost:3000 in your browser. You should see the placeholder page ("Reproducibility Radar — coming soon" or similar).

Press `Ctrl+C` in the terminal to stop the dev server when satisfied.

If the build errors out → paste the error.

---

## 6. Verify the full stack via docker compose

Stop everything from previous steps:

```bash
# In the orchestrator/ folder, in your first terminal
docker compose down
```

Then bring up everything together:

```bash
docker compose up --build
```

This builds all three service images (postgres, orchestrator, frontend) and starts them. First run takes 3–5 minutes.

**Expected:**
- All three services log to the terminal
- No service crash-loops (no service repeatedly restarting)
- The orchestrator container may exit cleanly or stay idle — both fine for now (no nightly logic yet)
- http://localhost:3000 still serves the frontend

If a service crash-loops → paste its logs.

When done, `Ctrl+C` to stop, then:

```bash
docker compose down
```

---

## 7. Final sanity checks

Back at the repo root:

```bash
git status
```

Should print `nothing to commit, working tree clean`. If any new files appeared (build artifacts, caches), they should already be gitignored — if any aren't, flag it.

---

## When you're done

If all of steps 1–7 passed, post in the team chat:

> ✅ Part A verified on [your OS]. Lint clean, mypy clean, 3 tests pass, alembic up/down works, all 5 tables present, frontend serves, docker compose up brings all services healthy.

Then we're cleared to move on to Part B together.

If any step failed, post:

> ❌ Part A failed at step [N], here's the output:
> ```
> [paste full error]
> ```

Don't try to fix it locally — we want everyone on the same baseline.

---

## Troubleshooting common issues

**"docker: command not found"** → Docker Desktop isn't installed or isn't running. Start the app, wait for the whale icon to stop animating, retry.

**"port 5432 already in use"** → You have a Postgres instance already running on your machine. Either stop it (`brew services stop postgresql` on Mac, or stop the Postgres service in Windows Services), or edit `orchestrator/docker-compose.yml` to map Postgres to a different port (e.g. `5433:5432`) and update `DATABASE_URL` accordingly.

**"port 3000 already in use"** → Some other dev server is using it. Stop that, or run the frontend on a different port: `PORT=3001 npm run dev`.

**`pip install` fails on a specific package** → Often a Python version mismatch. Confirm `python --version` shows 3.11, not 3.12 or 3.10. If you have multiple Pythons, use `python3.11 -m venv .venv` explicitly.

**`mypy` reports issues but `ruff` and `pytest` are clean** → Type errors in scaffolding code. Paste the mypy output — this is a real bug worth fixing before Part B.

**Windows `Activate.ps1` blocked** → `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then retry.

**Anything else** → Paste full error in chat. Better to ask than guess.
