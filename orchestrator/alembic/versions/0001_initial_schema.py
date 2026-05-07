"""Initial schema: papers, attempts, labs, subscribers

Revision ID: 0001
Revises:
Create Date: 2026-05-05 00:00:00.000000
"""
from __future__ import annotations

from collections.abc import Sequence

from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ── labs ──────────────────────────────────────────────────────────────────
    op.execute("""
        CREATE TABLE labs (
            id              SERIAL PRIMARY KEY,
            institution     TEXT NOT NULL,
            normalized_name TEXT NOT NULL UNIQUE,
            created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
    """)

    # ── papers ────────────────────────────────────────────────────────────────
    op.execute("""
        CREATE TABLE papers (
            id           SERIAL PRIMARY KEY,
            arxiv_id     TEXT NOT NULL UNIQUE,
            title        TEXT NOT NULL,
            authors      TEXT[] NOT NULL,
            abstract     TEXT NOT NULL,
            github_url   TEXT,
            submitted_at TIMESTAMPTZ NOT NULL,
            institution  TEXT,
            lab_id       INTEGER REFERENCES labs(id),
            created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
    """)
    op.execute("CREATE INDEX idx_papers_submitted_at ON papers (submitted_at)")
    op.execute("CREATE INDEX idx_papers_lab_id ON papers (lab_id)")

    # ── attempts ──────────────────────────────────────────────────────────────
    # Time-series table: one row per nightly run per paper.
    op.execute("""
        CREATE TABLE attempts (
            id               BIGSERIAL PRIMARY KEY,
            paper_id         INTEGER NOT NULL REFERENCES papers(id),
            attempted_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            status           TEXT NOT NULL,          -- success | failed | error
            score            SMALLINT,               -- 0-100
            failure_category TEXT,                   -- one of the 13 enum values, or NULL
            log_blob_path    TEXT,                   -- path to raw log on disk
            claimed_metric   DOUBLE PRECISION,
            observed_metric  DOUBLE PRECISION,
            dimensions       JSONB NOT NULL DEFAULT '{}'::jsonb,
            -- dimensions keys: installable, runnable, produces_output,
            --                  numerically_close, documented  (each 0-20)
            sandbox_image    TEXT,
            wall_seconds     INTEGER,                -- actual runtime
            created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
    """)
    # Primary access patterns: recent attempts, per-paper history
    op.execute("CREATE INDEX idx_attempts_attempted_at ON attempts (attempted_at DESC)")
    op.execute("CREATE INDEX idx_attempts_paper_id ON attempts (paper_id)")
    op.execute("CREATE INDEX idx_attempts_paper_attempted ON attempts (paper_id, attempted_at DESC)")
    op.execute("CREATE INDEX idx_attempts_status ON attempts (status)")
    op.execute("CREATE INDEX idx_attempts_score ON attempts (score DESC NULLS LAST)")
    # GIN index for JSONB dimension queries
    op.execute("CREATE INDEX idx_attempts_dimensions_gin ON attempts USING gin (dimensions)")

    # ── subscribers ───────────────────────────────────────────────────────────
    op.execute("""
        CREATE TABLE subscribers (
            id            SERIAL PRIMARY KEY,
            email         TEXT NOT NULL UNIQUE,
            subscribed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            active        BOOLEAN NOT NULL DEFAULT TRUE
        )
    """)
    op.execute("CREATE INDEX idx_subscribers_active ON subscribers (active) WHERE active = TRUE")


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS subscribers")
    op.execute("DROP TABLE IF EXISTS attempts")
    op.execute("DROP TABLE IF EXISTS papers")
    op.execute("DROP TABLE IF EXISTS labs")
