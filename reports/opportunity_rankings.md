# Opportunity Rankings — CAPT Prize Operations

Generated: v0.1

Ranked by: CAPT fit + likelihood of success + prize value.

## Priority Order

| Rank | Prize | Value | CAPT Fit | Why |
|------|-------|------:|:--------:|-----|
| 1 | **AIMO Prize** | $5M+ | ★★★★★ | Prize explicitly targets AI math reasoner — CAPT's core identity |
| 2 | **ARC Prize 2026** | $2M+ | ★★★★★ | Tests abstraction and reasoning — CAPT's native capabilities |
| 3 | **Conway 99-graph** | $1K | ★★★★☆ | Perfect SAT/SMT/graph search test — small, fast, clean |
| 4 | **Beal Conjecture** | $1M | ★★★★☆ | Counterexample search + proof decomposition pipeline |
| 5 | **Erdős–Gyárfás bounties** | ~$300 | ★★★★☆ | Graph search sandbox — low stakes, high proof value |
| 6 | **Clay Millennium Problems** | $1M each | ★★☆☆☆ | Moonshots — prestige, but long payoff timeline |

## Decision Matrix

```
Target        │ Cash │ Speed │ CAPT Fit │ Public Proof │ Do First?
──────────────┼──────┼───────┼──────────┼──────────────┼─────────
AIMO          │ High │ Fast  │ Native   │ Yes          │ YES
ARC           │ High │ Fast  │ Native   │ Yes          │ YES
Conway 99-g   │ Low  │ Fast  │ Natural  │ Yes          │ YES (sandbox)
Beal          │ High │ Med   │ Natural  │ Possible     │ Study
Erdős–Gyárfás │ Low  │ Fast  │ Natural  │ Yes          │ Sandbox
Clay          │ High │ Slow  │ Possible │ Unlikely     │ Defer
```

## Active Runs

None yet. First actions:

1. **AIMO** — Build solver harness + Arena baseline
2. **ARC** — Build task interpreter + program synthesis loop
3. **Conway 99-graph** — SAT encoding + graph search
4. **Beal** — Known-results map + modular constraint search