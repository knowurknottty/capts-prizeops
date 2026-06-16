"""
solver_orchestrator.py — Routes problems to CAPT solving techniques

Each prize problem type maps to a solver strategy. The orchestrator
selects the technique(s) and coordinates the solving pipeline.

Strategy lanes:
  - COMPETITION: AIMO/ARC — harness + candidate comparison + Arena
  - COUNTEREXAMPLE: Beal, Conway, Erdős — search + verify
  - FORMAL_PROOF: Lean/Isabelle formalization of partial results
  - LITERATURE: Millennium problems — map, decompose, gap-hunt
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any


class SolverLane(Enum):
    COMPETITION = auto()      # AIMO, ARC
    COUNTEREXAMPLE = auto()   # Beal, Conway, Erdős
    FORMAL_PROOF = auto()     # Lean/Isabelle pipeline
    LITERATURE = auto()       # Millennium literature maps


@dataclass
class SolverStrategy:
    lane: SolverLane
    techniques: list[str]
    parallelism: int = 1
    formal_required: bool = False
    arena_eligible: bool = False
    capt_depth: int = 3


# Priority-ordered strategy map — first match wins
STRATEGY_ROUTES = {
    "aimo_grand": SolverStrategy(
        lane=SolverLane.COMPETITION,
        techniques=["symbolic_scratchpad", "multi_solver_ensemble",
                     "self_consistency_voting", "lean_verification"],
        arena_eligible=True,
        capt_depth=5,
    ),
    "arc_prize_2026": SolverStrategy(
        lane=SolverLane.COMPETITION,
        techniques=["program_synthesis", "state_explorer",
                     "policy_mutation", "grid_reasoning"],
        arena_eligible=True,
        capt_depth=4,
    ),
    "beal_conjecture": SolverStrategy(
        lane=SolverLane.COUNTEREXAMPLE,
        techniques=["modular_search", "computation_pruning",
                     "counterexample_verify", "formal_subproofs"],
        formal_required=False,
        capt_depth=5,
    ),
    "conway_99_graph": SolverStrategy(
        lane=SolverLane.COUNTEREXAMPLE,
        techniques=["sat_encoding", "graph_canonicalization",
                     "spectral_analysis", "clique_search"],
        formal_required=False,
        capt_depth=3,
    ),
    "erdos_gyarfas_conjecture": SolverStrategy(
        lane=SolverLane.COUNTEREXAMPLE,
        techniques=["graph_search", "counterexample_verify", "sat_search"],
        formal_required=False,
        capt_depth=3,
    ),
}


def route(prize_id: str) -> SolverStrategy:
    """Return the solver strategy for a prize ID."""
    strategy = STRATEGY_ROUTES.get(prize_id)
    if strategy is None:
        return SolverStrategy(
            lane=SolverLane.LITERATURE,
            techniques=["literature_map", "gap_analysis", "formalization"],
            capt_depth=3,
        )
    return strategy


def summarize(strategy: SolverStrategy) -> dict[str, Any]:
    """Return a human-readable summary of the strategy."""
    return {
        "lane": strategy.lane.name,
        "techniques": strategy.techniques,
        "parallelism": strategy.parallelism,
        "formal_required": strategy.formal_required,
        "arena_eligible": strategy.arena_eligible,
        "capt_depth": strategy.capt_depth,
    }