# Prize Search Log

## Conway 99-graph

| # | Method | Vars | n=10 | n=99 | Notes |
|---|--------|:----:|:----:|:----:|-------|
| 1 | Vanilla SAT BoolVar | 9,801 | 0.03s | 7.5m timeout | O(n³) pairwise λ/μ |
| 3 | Column-concatenation | 9,801 | 0.05s | - | Same as 1 |
| 5 | n×k IntVar incidence | 1,386 | 0.1s | 16m timeout | Z3 Int theory limit |
| **6** | **BitVec<99> + popcount tree** | **99 BV** | **1.2s** | **RUNNING (30m)** | **Bit-blast to SAT** |

## Erdős–Gyárfás

| Method | Max n | Graphs | Counterexamples | Time |
|--------|:-----:|:------:|:---------------:|:----:|
| brute force | 7 | 238,811 | 0 | 22.7s |
| nauty geng | 10 | 5,290,143 | 0 | 499.3s |
| nauty geng | 11 | (geng segfault) | - | - |

## AIMO Benchmarks (stub results — need CAPT backend)

| Candidate | putnam_2024_a1 | putnam_2024_a2 | imo_2024_p1 |
|-----------|:--------------:|:--------------:|:-----------:|
| capt_standard | stub | stub | stub |
| capt_deep_research | stub | stub | stub |
| capt_ensemble_x3 | stub | stub | stub |
| capt_lean_hybrid | stub | stub | stub |

## Beal Conjecture

Not yet attempted. Decomposition: 3 subproblems (modular constraints, small exponent search, Darmon–Granville literature). No solver launched.

## Millennium Problems

Not yet attempted. Strategy: literature mapping + equivalent formulations. No solver launched.