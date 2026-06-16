# Conway's 99-graph Problem

**Target:** Does a strongly regular graph (99, 14, 1, 2) exist?
**Prize:** $1,000 (historical offer by John Conway)
**Status:** Open since 1970s

## Problem Description

Find a graph with:
- 99 vertices
- Each vertex adjacent to 14 others (regular of degree 14)
- Any two adjacent vertices share exactly 1 common neighbor (λ=1)
- Any two non-adjacent vertices share exactly 2 common neighbors (μ=2)

## Known Constraints

- Parameters (99, 14, 1, 2) satisfy necessary conditions for a strongly regular graph
- Spectral analysis: eigenvalues r=5, s=-2 with multiplicities 55 and 44
- Extensive SAT/SMT searches reducing the search space
- Equivalent to a symmetric 2-(99, 14, 2) block design with certain properties

## CAPT Strategy

1. **SAT encoding** — Encode existence as SAT/SMT problem
2. **Graph canonicalization** — Symmetry breaking for search
3. **Spectral analysis** — Check eigenvalue-derived constraints
4. **Clique counting** — Combinatorial constraint satisfaction
5. **Exhaustive search** — Bounded search with pruning

## Techniques

- Z3 SAT solver with symmetry breaking
- nauty/traces for graph isomorphism
- Eigenvalue constraints via spectral graph theory
- Combinatorial block design approach