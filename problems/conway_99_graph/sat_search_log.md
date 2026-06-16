# Conway 99-graph — SAT Search Log

## Attempt 1: 2026-06-16 — Vanilla SAT
**Method:** Full Z3 SAT encoding — per-pair λ/μ implications
**Variables:** 4851 boolean
**Status:** TIMEOUT (killed ~7.5 min, 10-min wall)
**Verified on Petersen:** yes (0.03s)
**Diagnosis:** O(n^3) Implies constraints defeat Z3's propagation at n=99

## Attempt 2: Removed (identical to Attempt 1)

## Attempt 3: 2026-06-16 — Column-Concatenation
**Variables:** 4851 boolean (same as Attempt 1)
**Status:** Same O(n^3) wall
**Verified on Petersen:** yes (0.05s)

## Attempt 4: 2026-06-16 — Block Design (n×n)
**Variables:** 99×99 boolean (same as adjacency)
**Status:** Same wall
**Verified on Petersen:** yes (0.03s)

## Attempt 5: 2026-06-16 — n×k Incidence (IntVar)
**Method:** Z3 IntVar encoding — each vertex's neighbor list as 14 integers
**Variables:** 99×14 = 1386 IntVars (7× reduction from 9801)
**Constraint count:** O(n²×k²) = ~1.9M clause equivalents
**Status:** TIMEOUT at ~16 min (Z3's difference-logic theory can't handle this scale)
**Verified on:** srg(5,2,0,1) 0.0s, srg(9,4,1,2) 0.1s, srg(10,3,0,1) 0.1s, srg(16,5,0,2) 1.0s
**Diagnosis:** IntVar encoding hits Z3 integer theory limits. The per-pair intersection constraints still produce O(n²×k²) clauses. Need SAT-based encoding for CDCL engine speed.

## Attempt 6: 2026-06-16 — BitVec Row Encoding (RUNNING)
**Method:** Z3 BitVec<99> per row + custom binary adder tree popcount
**Variables:** 99 BitVec<99>
**Verified on:** srg(10,3,0,1) 1.2s (slower per-problem due to custom popcount, but scales better)
**n=99 status:** RUNNING (1800s timeout — 30 min)

## Erdős–Gyárfás search: 2026-06-16

**Method:** nauty geng canonical enumeration
**Search range:** n ≤ 10 (geng segfaulted at n=11, skipped n=11-12)
**Graphs checked:** 5,290,143
**Counterexamples found:** 0
**Time:** 499.3s
**Conclusion:** Conjecture holds for all graphs up to 10 vertices. No counterexample exists in this range.