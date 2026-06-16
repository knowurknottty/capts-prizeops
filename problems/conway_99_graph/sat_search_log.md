# Conway 99-graph — SAT Search Log

## Attempt 1: 2026-06-16

**Method:** Full Z3 SAT encoding of srg(99, 14, 1, 2)
**Variables:** 4851 boolean (x[i][j] adjacency)
**Constraints:** Symmetry + no-loop + degree (99 PbEq) + λ/μ condition (4851 Implies)
**Symmetry breaking:** First vertex's 14 neighbors fixed
**Timeout:** 600s (10 minutes)
**Status:** RUNNING (as of 40s in)
**Result:** PENDING

## Sanity Check (same code, same constraints)

Ran Petersen graph srg(10, 3, 0, 1) as validation:
- Found: TRUE (0.03s)
- Verified: PASS
- Encoding confirmed correct

**Note:** Even with symmetry breaking, the 99-vertex problem has ~10^170 symmetric
redundancies. SAT solvers can handle srg up to ~40 vertices tractably. For 99,
more advanced techniques are needed:
- Block design reduction (this SRG is equivalent to a 2-(99,14,2) design)
- Spectral constraints (eigenvalues r=5, s=-2 with multiplicities 55, 44)
- Column/row sum precomputation via combinatorial constraints
- Specialized SRG solver (not general-purpose Z3)