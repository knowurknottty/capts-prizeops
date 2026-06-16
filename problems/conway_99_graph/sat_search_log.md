# Conway 99-graph — Search Log

## Results Summary

| # | Method | Vars | n=10 | n=16 | n=99 |
|---|--------|:----:|:----:|:----:|:----:|
| 1 | SAT BoolVar λ/μ | 9,801 | 0.03s | - | **7.5m timeout** |
| 5 | IntVar incidence (n×k) | 1,386 | 0.1s | 1.0s | **16m timeout** |
| 6 | BitVec<99> + popcount tree | 99 BV | 1.2s | - | **30m timeout** (popcount too slow) |
| **7** | **Pseudo-Boolean PbEq** | **4,851** | **0.04s** | **0.09s** | **RUNNING (1h timeout)** |

## Attempt 7: Pseudo-Boolean (running)

**Status:** RUNNING — 20+ minutes into 1-hour timeout
**Solver type:** Z3 native PbEq (pseudo-boolean constraints)
**Variables:** 4,851 boolean (half adjacency matrix, i<j)
**Constraints:** 99 degree PbEq + 4,851 λ/μ Implies(PbEq) pairs + symmetry breaking
**Key insight:** Z3's PbEq uses specialized cardinality networks (totalizer, sorting networks) that handle 97-variable cardinality constraints efficiently. 4,851 such constraints × 97 variables = 470k network edges.

If this times out, the Conway 99-graph is beyond Z3's reach. Next approach would be a **dedicated C++ SRG solver** using:
1. Eigenvalue preconditioning (fix A² + 2A - 14I = 6J as matrix equation)
2. Column-generation search over partial adjacency matrices
3. Combinatorial block design generation (2-(99,14,2) design search)
4. GRAPE/GAP for computational group theory approach

## Erdős–Gyárfás Conjecture

| Method | Max n | Graphs | Counterexamples | Time |
|--------|:-----:|:------:|:---------------:|:----:|
| brute force | 7 | 238,811 | 0 | 22.7s |
| nauty geng | 10 | 5,290,143 | 0 | 499.3s |
| nauty geng | 11+ | (segfault) | - | - |

**Conclusion:** No counterexample exists for up to 10 vertices. 5.3M graphs verified.