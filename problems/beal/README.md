# Beal Conjecture — CAPT Solving Pipeline

**Target:** Counterexample or proof for A^x + B^y = C^z with x,y,z > 2 forcing A,B,C to share a prime factor
**Prize:** $1M (AMS-supervised)
**Status:** Open — verify prize terms before submission

## Known Results

- Darmon–Granville theorem (1995): for fixed coprime exponents, finitely many solutions
- Extensize computational searches up to various bounds (Boyer, 2010+)
- Modular constraints eliminate large regions
- If counterexample exists with sum ≤ 10^9, likely already found

## CAPT Strategy

1. **Modular search** with constraint pruning (mod small primes)
2. **Decompose into sub-claims** for partial proof
3. **Computational search** over exponent/sum ranges
4. **Formal subproofs** in Lean for partial results
5. **Known-results map** — what constraints are already proven

## Pipeline

`intake → decompose → search → verify_subclaims → assemble → lean_formalize → audit → package`