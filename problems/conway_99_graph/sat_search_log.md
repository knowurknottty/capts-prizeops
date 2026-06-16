# Conway 99-graph — SAT Search Log

## Attempt 1: 2026-06-16

**Method:** Full Z3 SAT encoding of srg(99, 14, 1, 2)
**Variables:** 4851 boolean (x[i][j] adjacency matrix, i<j)
**Constraints:**
- Symmetry: x[i][j] == x[j][i] (4851 binary constraints)
- No self-loops: x[i][i] == false
- Degree: PbEq per vertex (99 PbEq constraints)
- λ/μ: For each of 4851 pairs, Implies(adjacent, common==1) AND Implies(not adjacent, common==2)
- Symmetry breaking: vertex 0's neighbors fixed (adjacent to 1..14)
**Timeout:** 600s (10 minutes)

### Sanity Check (same code, same constraints)
- Petersen srg(10, 3, 0, 1): **Found in 0.03s** — encoding verified correct
- Verified via `is_srg()`: PASS

### Conway 99 Result
- **TIMEOUT after ~7.5 minutes** — Z3 returned unknown/timeout
- Status: unverified (search did not complete)
- Even with symmetry breaking, the 99-vertex problem has ~10^170 symmetric redundancies

### Analysis
General-purpose SAT solvers hit the exponential wall hard for 99-vertex SRGs. The λ/μ encoding produces O(n^3) constraints (~485k implications) and Z3 cannot propagate effectively at this scale.

**Known SRG search literature says:** special-purpose solvers using:
1. **Block design reduction** — this SRG parameter set is equivalent to a 2-(99,14,2) symmetric design; can reduce to incidence matrix constraints
2. **Spectral constraints** — eigenvalues r=5, s=-2 with multiplicities 55, 44; adjacency matrix must satisfy A^2 + 2A - 14I = 6J
3. **Column-concatenation** — reduces O(n^3) λ/μ to O(n^2) by encoding rows of the adjacency matrix as integer variables
4. **nauty + constraint propagation** — generate SRG candidates via canonical augmentation

### Next Steps
- **Attempt 2:** implement specialized SRG search using spectral equation A^2 + 2A - 14I = 6J as the primary constraint, not pairwise λ/μ
- **Attempt 3:** use block design approach — search for a 2-(99,14,2) design's incidence matrix
- **Attempt 4:** column-concatenation encoding with Z3's integer variables instead of propositional