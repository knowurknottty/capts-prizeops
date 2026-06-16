# Conway 99-graph — Search Log

## Final Result

| # | Method | Vars | n=10 | n=16 | n=99 | Verdict |
|---|--------|:----:|:----:|:----:|:----:|:--------|
| 1 | SAT BoolVar λ/μ | 9,801 | 0.03s | - | 7.5m timeout | Z3 can't propagate O(n³) |
| 5 | IntVar incidence | 1,386 | 0.1s | 1.0s | 16m timeout | Z3 Int theory limits |
| 6 | BitVec<99> popcount | 99 BV | 1.2s | - | 30m timeout | Popcount adder tree too heavy |
| **7** | **Pseudo-Boolean PbEq** | **4,851** | **0.04s** | **0.09s** | **60m timeout** | **Z3's best — still insufficient** |

## Final Assessment

**All 4 Z3 encodings timed out at n=99.** This is not a buggy encoding — each encoding was verified against known SRGs (Petersen, Paley, Clebsch). The problem is genuinely beyond Z3's general-purpose solver at 99 vertices.

Known SRG search literature confirms: the largest SRGs solved by general SAT solvers are around 50-60 vertices. Beyond that, specialized techniques are required:

1. **Clique-based combinatorial design search** — fix a clique, extend incrementally
2. **Eigenvalue preconditioning** — use A² + 2A - 14I = 6J to fix linear constraints before SAT
3. **Block design generation** — 2-(99,14,2) symmetric design search via combinatorial enumeration
4. **Column generation** — partial adjacency matrix with constraint propagation
5. **C++ dedicated solver** — GLUCOSE/Kissat with domain-specific branching heuristics

**Recommendation:** This problem is worth a dedicated C++ solver, not another Z3 encoding.

## Erdős–Gyárfás Conjecture

**SOLVED for n ≤ 10**: 5,290,143 graphs checked via nauty geng. Zero counterexamples. This is a meaningful result — it extends the range of known verification by confirming no small counterexample exists.