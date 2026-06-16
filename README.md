# CAPT Prize Operations — capts-prizeops

**CAPT-driven mathematical bounty hunting, formal theorem proving, and prize capture.**

Inversion Labs operates CAPT/bioCAPT against open mathematical problems — from AIMO/ARC competition lanes to Millennium Problems — producing verified solutions via CAPT's cognitive architecture + Lean formal verification.

---

## Operating Doctrine

No prize claim without:

1. **Reproducible run manifest** — every attempt versioned and rerunnable
2. **Versioned candidate state** — checkpoints, policies, bubbles archived
3. **Full proof trace** — CAPT cogitation → Lean/Isabelle formalization chain
4. **Independent verifier** — at least two verification methods before claim
5. **Formal proof where possible** — Lean is the anti-hallucination boundary
6. **Human expert review** — math specialist sign-off before submission
7. **Publication/submission route** — peer review or competition rules satisfied
8. **Claim ledger entry** — every claim recorded, including failures

The danger is not that CAPT fails. The danger is that it produces something *plausible enough to seduce us before it is true*. Math is merciless. That is good. Use that mercilessness as the proof forge.

---

## Prize Targets (ordered by CAPT fit)

| Tier | Target | Value | CAPT Fit | First Action |
|------|--------|------:|----------|--------------|
| 1 | **AIMO Prize** | $10M (total fund) | Direct: AI math reasoner competition | Build AIMO solver harness + Arena baseline |
| 1 | **ARC Prize 2026** | $2M+ | ARC-AGI-3 benchmarks CAPT's core architecture | Build ARC task interpreter + program synthesis loop |
| 2 | **Beal Conjecture** | $1M | Number theory counterexample search | Computational search + modular proof map |
| 2 | **Clay Millennium Problems** | $1M each (6 unsolved) | Ultimate prestige — Riemann, P vs NP, Navier-Stokes, etc. | Literature map + formal definitions + barrier ledger |
| 3 | **Conway 99-graph** | $1,000 (historical) | Perfect SAT/SMT/graph-search test | SAT encoding + canonicalization |
| 3 | **Erdős–Gyárfás conjecture** | $100-$300 (historical) | Counterexample generation sandbox | Graph search + formal verification |
| 4 | **PutnamBench / FIMO / LEAP** | N/A (benchmarks) | Proof surface for formal theorem proving competency | Bench CAPT formal proving baseline |

---

## Solving Strategy

### Lane A — Competition money (fastest cash path)

```
AIMO / ARC
→ build solver candidates
→ Arena compares candidates
→ submit best public model
→ use rankings as public proof of CAPT
```

### Lane B — Counterexample discovery (fastest "CAPT found something humans missed" artifact)

```
Conway 99-graph
Erdős–Gyárfás
Beal finite-region searches
other graph/combinatorics bounties
```

### Lane C — Formal proof (anti-hallucination boundary)

```
CAPT proposes proof
→ Lean formalization
→ compiler rejects bad steps
→ CAPT repairs
→ independent human review
→ preprint
```

### Lane D — Millennium moonshot (long-range research)

```
known equivalent formulations
known failed approaches
known barriers
special cases
formalized definitions
computational experiments
proof gap maps
```

---

## Structure

```
capts-prizeops/
  prizes/                   # Prize manifests (YAML)
    prize_ledger.yaml       # Master ledger
    clay_millennium.yaml
    beal.yaml
    aimo.yaml
    arc.yaml
    graph_bounties.yaml

  problems/                 # Per-problem working directories
    beal/
    clay/
    aimo/
    arc/
    conway_99_graph/
    erdos_gyarfas/

  pipelines/                # Solver pipelines
    intake.py               # Problem ingestion and normalization
    literature_map.py       # Known-results gathering
    conjecture_decomposer.py
    solver_orchestrator.py  # Routes problems to CAPT techniques
    counterexample_search.py
    lean_formalizer.py      # CAPT→Lean/Isabelle bridge
    proof_auditor.py        # Self-consistency + verification
    submission_packager.py  # Paper/run-manifest generation

  reports/
    opportunity_rankings.md
    proof_attempts/         # Per-attempt logs
    failure_museum/         # What didn't work and why
    arena_runs/             # Arena comparison results
```

---

## Quick Start

```bash
pip install -e .            # Install capts-prizeops package
capts-prizeops --help       # See available commands
capts-prizeops intake       # Ingest a new problem
capts-prizeops solve beal   # Run CAPT solver on Beal conjecture
capts-prizeops arena        # Compare multiple solver candidates
```

---

## License

MIT — Inversion Labs