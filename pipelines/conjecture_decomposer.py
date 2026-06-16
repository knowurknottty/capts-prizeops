"""
conjecture_decomposer.py — Decompose prize problems into CAPT-solvable subproblems

Each prize problem may be too large for CAPT to solve directly. This module
decomposes them into smaller, verifiable subproblems that CAPT can attack
individually.

Each subproblem:
  - Has a formal statement
  - Is independently verifiable (SAT, SMT, Lean, SymPy)
  - Has a known difficulty estimate
  - Can be fed to CAPT's cogitate or a specific solver pipeline

The decomposition strategy differs by problem type.
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum, auto


class SubproblemType(Enum):
    COMPUTATIONAL_SEARCH = auto()   # SAT/SMT/graph search
    FORMAL_PROOF = auto()           # Lean/Isabelle
    COUNTEREXAMPLE = auto()         # Counterexample search
    LITERATURE_MAP = auto()         # Survey known results
    EQUIVALENCE_CHECK = auto()      # Check if two formulations are equivalent
    SPECIAL_CASE = auto()           # Prove a special case


@dataclass
class Subproblem:
    """A decomposed subproblem that CAPT can solve."""
    subproblem_id: str
    parent_problem: str
    subproblem_type: SubproblemType
    statement: str
    verification_method: str  # "z3" / "lean" / "sympy" / "networkx"
    difficulty: float  # 0.0 (easy) to 1.0 (hard)
    dependencies: list[str] = field(default_factory=list)  # subproblem_ids this depends on
    solved: bool = False
    result: Optional[str] = None


@dataclass
class DecompositionPlan:
    """A plan for decomposing a prize problem."""
    prize_id: str
    subproblems: list[Subproblem] = field(default_factory=list)


def decompose_conway_99() -> DecompositionPlan:
    """Decompose Conway 99-graph into 4 subproblems."""
    return DecompositionPlan(
        prize_id="conway_99_graph",
        subproblems=[
            Subproblem(
                subproblem_id="conway_small_instance_srg_16",
                parent_problem="conway_99_graph",
                subproblem_type=SubproblemType.COMPUTATIONAL_SEARCH,
                statement="Find srg(16,5,0,2) as a warmup",
                verification_method="networkx",
                difficulty=0.2,
            ),
            Subproblem(
                subproblem_id="conway_spectral_constraints",
                parent_problem="conway_99_graph",
                subproblem_type=SubproblemType.EQUIVALENCE_CHECK,
                statement="Verify spectral eigenvalue multiplicities (r=5 mult=55, s=-2 mult=44)",
                verification_method="sympy",
                difficulty=0.3,
            ),
            Subproblem(
                subproblem_id="conway_block_design_equiv",
                parent_problem="conway_99_graph",
                subproblem_type=SubproblemType.EQUIVALENCE_CHECK,
                statement="Prove equivalence to symmetric 2-(99,14,2) block design",
                verification_method="z3",
                difficulty=0.4,
            ),
            Subproblem(
                subproblem_id="conway_nk_incidence_search",
                parent_problem="conway_99_graph",
                subproblem_type=SubproblemType.COMPUTATIONAL_SEARCH,
                statement="Search for SRG via n×k incidence encoding with Z3",
                verification_method="z3",
                difficulty=0.8,
            ),
        ]
    )


def decompose_beal() -> DecompositionPlan:
    """Decompose Beal conjecture into subproblems."""
    return DecompositionPlan(
        prize_id="beal_conjecture",
        subproblems=[
            Subproblem(
                subproblem_id="beal_modular_constraints",
                parent_problem="beal_conjecture",
                subproblem_type=SubproblemType.COMPUTATIONAL_SEARCH,
                statement="Enumerate modular constraints for small primes p dividing A,B,C",
                verification_method="sympy",
                difficulty=0.3,
            ),
            Subproblem(
                subproblem_id="beal_small_exponent_search",
                parent_problem="beal_conjecture",
                subproblem_type=SubproblemType.COUNTEREXAMPLE,
                statement="Search exponents (3 ≤ a,b,c ≤ 20) for counterexamples with sum ≤ 10^9",
                verification_method="z3",
                difficulty=0.5,
            ),
            Subproblem(
                subproblem_id="beal_frobenius_conditions",
                parent_problem="beal_conjecture",
                subproblem_type=SubproblemType.LITERATURE_MAP,
                statement="Map Darmon–Granville theorem and its constraints on coprime exponents",
                verification_method="manual",
                difficulty=0.4,
            ),
        ]
    )


def decompose_erdos_gyarfas() -> DecompositionPlan:
    """Decompose Erdős–Gyárfás into subproblems."""
    return DecompositionPlan(
        prize_id="erdos_gyarfas_conjecture",
        subproblems=[
            Subproblem(
                subproblem_id="eg_small_graph_search",
                parent_problem="erdos_gyarfas_conjecture",
                subproblem_type=SubproblemType.COMPUTATIONAL_SEARCH,
                statement="Exhaustive search for counterexamples with n ≤ 15, min degree ≥ 3",
                verification_method="networkx",
                difficulty=0.4,
            ),
            Subproblem(
                subproblem_id="eg_planar_class_check",
                parent_problem="erdos_gyarfas_conjecture",
                subproblem_type=SubproblemType.SPECIAL_CASE,
                statement="Verify the conjecture holds for all planar graphs (known result)",
                verification_method="manual",
                difficulty=0.3,
            ),
        ]
    )


# Registry of decomposition strategies
DECOMPOSERS = {
    "conway_99_graph": decompose_conway_99,
    "conway": decompose_conway_99,
    "beal_conjecture": decompose_beal,
    "beal": decompose_beal,
    "erdos_gyarfas_conjecture": decompose_erdos_gyarfas,
    "erdos_gyarfas": decompose_erdos_gyarfas,
}


def decompose(prize_id: str) -> DecompositionPlan:
    """Decompose a prize problem into CAPT-solvable subproblems."""
    fn = DECOMPOSERS.get(prize_id)
    if fn is None:
        return DecompositionPlan(
            prize_id=prize_id,
            subproblems=[
                Subproblem(
                    subproblem_id=f"{prize_id}_literature",
                    parent_problem=prize_id,
                    subproblem_type=SubproblemType.LITERATURE_MAP,
                    statement=f"Survey known results for {prize_id}",
                    verification_method="manual",
                    difficulty=0.5,
                )
            ],
        )
    return fn()