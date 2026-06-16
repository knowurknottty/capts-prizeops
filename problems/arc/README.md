# ARC Prize 2026 — CAPT Solving Pipeline

**Target:** ARC-AGI-3 benchmark — abstraction and reasoning from few examples
**Prize:** $2M+ prize pool
**Status:** Active — 2026 competition

## How ARC Tests CAPT

ARC tasks require:
- **Abstraction** from 2-5 example input-output grids
- **Pattern extraction** — identify the transformation rule
- **Generalization** — apply the rule to a new test case
- **Exploration** — search over possible transformations

These map directly to CAPT's:
- HMC (pattern extraction from examples)
- NEDA (spike-based pattern matching)
- CIG (causal structure inference in transformations)
- ALLO (exploration/exploitation balance)

## CAPT Strategy

1. **Grid interpreter** — Parse ARC grid format into CAPT inputs
2. **Program synthesis** — Search over DSL of grid transformations
3. **State-memory explorer** — HMC stores discovered patterns
4. **Policy mutation** — Multiple candidate policies via Arena
5. **Failure museum** — Classify failing task categories

## Resources

- ARC Prize: https://arcprize.org/
- ARC-AGI-3 dataset
- Public leaderboard