# Scoring

Each attempt receives a score 0–100 composed of five dimensions (0–20 each).

| Dimension | Points | Passes when… |
|---|---|---|
| `installable` | 0–20 | Docker setup (git clone + pip install) exits 0 |
| `runnable` | 0–20 | Main command executes without an exception/crash |
| `produces_output` | 0–20 | A numeric or structured artifact appears in stdout/files |
| `numerically_close` | 0–20 | Headline metric is within 10% of the value claimed in the paper |
| `documented` | 0–20 | Claude rates README sufficiency (rubric TBD in Part B) |
