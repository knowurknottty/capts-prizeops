# AIMO Prize — CAPT Solving Pipeline

**Target:** AI Mathematical Olympiad — publicly shared AI model performing at IMO gold level
**Prize:** $5M grand prize + $5M progress prizes (total $10M fund)
**Status:** AIMO3 launched November 2025

## CAPT Strategy

1. **Problem ingestion** — Parse IMO/AIMO problem statements into formal representations
2. **Symbolic scratchpad** — CAPT generates intermediate symbolic reasoning
3. **Multi-solver ensemble** — Multiple CAPT candidates compete via Arena
4. **Self-consistency voting** — QIPC consensus across solver runs
5. **Lean verification** — Formal proof of each solution step

## Solver Candidates

- `solver_capt_standard` — Default cogitate pipeline with math routing
- `solver_capt_deep` — research_depth=10 with full ECHO recall
- `solver_lean_hybrid` — CAPT generates Lean statements, iterates via compiler

## Resources

- AIMO Prize: https://aimoprize.com/
- AIMO Participation: https://aimoprize.com/participate/
- IMO Shortlist problems
- FIMO benchmark (formal IMO problems in Lean)
- PutnamBench