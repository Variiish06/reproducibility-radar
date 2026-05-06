# Architecture

> Full write-up in Part B.

## High-level flow

```
ArXiv API → crawler → paper2code → selector (top 10)
   → [concurrent, cap=3] sandbox → reproducer → claude_planner
   → scoring → db → leaderboard frontend
```
