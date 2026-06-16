# Erdős–Gyárfás Conjecture

**Target:** Every graph with minimum degree ≥ 3 contains a simple cycle of length a power of 2
**Prize:** Approximately $100 for proof, $50 for counterexample (historical Erdős offer)
**Status:** Open — verified for many graph classes

## Known Verified Classes

- Planar graphs
- Graphs with bounded treewidth
- Claw-free graphs
- Graphs with minimum degree ≥ 3 and certain other properties
- General case remains open

## CAPT Strategy

1. **Computational search** for counterexamples (small graphs)
2. **SAT encoding** of graph property constraints
3. **Verified for known classes** — extend class verification
4. **Graph generation** — targeted generation of difficult cases

## Techniques

- SAT/SMT for small graph exhaustive search
- Python networkx + graph generation
- Known partial results as seed for CAPT's HMC memory