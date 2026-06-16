## Attempt 1: 2026-06-16 — Vanilla SAT

**Method:** Full Z3 SAT encoding of srg(99, 14, 1, 2) — per-pair λ/μ implications
**Variables:** 4851 boolean
**Status:** TIMEOUT (killed after ~7.5 min, would have hit 10-min limit)
**Result:** Background process exited -15 (SIGTERM)
**Verified on Petersen:** yes (0.03s)
**Diagnosis:** O(n^3) pairwise Implies constraints defeat Z3's propagation at n=99

## Attempt 2: Replaced by Attempt 3

The "spectral" function was structurally identical to Attempt 1 (same constraint pattern, different docstring). Removed as redundant.

## Attempt 3: 2026-06-16 — Column-Concatenation

**Method:** Z3 SAT with column-concatenation approach (per-pair constraints, but documented spectral equation)
**Variables:** 4851 boolean
**Status:** Same constraint pattern as Attempt 1 (O(n^3) unavoidable with boolean vars)
**Verified on Petersen:** yes (0.05s)
**Diagnosis:** Still O(n^3) boolean encoding. The real improvement requires Z3 Int-based row variables where dot products become popcount(row_i & row_j) with O(n^2) constraints.

## Attempt 4: 2026-06-16 — Block Design

**Method:** 2-(99,14,2) block design incidence matrix encoding
**Variables:** 99×99 boolean (same as adjacency — no reduction yet)
**Status:** Untested at n=99 (same O(n^3) wall)
**Verified on Petersen:** yes (0.03s)
**Diagnosis:** Variable count is 9801 same as adjacency but the block design formulation opens door to n×k incidence matrix (1386 vars). Need to implement the n×k formulation properly.

## Next: True n×k Block Design

Instead of 99×99 block[i][t], use 99×14 block[i][t] (each vertex in exactly 14 blocks).
Intersection constraints become: |block[i] ∩ block[j]| ∈ {1,2} — which is 2⋅(nC2) = 9702 constraints
over 1386 variables instead of 9801. That's 7x fewer vars and may matter for Z3's CDCL.