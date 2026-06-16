"""
intake.py — Problem Intake Pipeline

Ingests a prize problem from a structured definition directory,
normalizes it into CAPT's internal representation, and stages it
for solver orchestration.

Flow:
  definition_dir/
    problem.yaml      # Problem statement, constraints, background
    known_results/    # Known theorems, bounds, computational results
    references/       # Literature references, papers
    formal/           # Lean/Isabelle formalization (if any)
"""

import yaml
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class ProblemConstraints:
    """Known constraints on the problem — what is already proven or excluded."""
    proven_subcases: list[str] = field(default_factory=list)
    known_barriers: list[str] = field(default_factory=list)
    computational_bounds: dict[str, str] = field(default_factory=dict)
    equivalent_formulations: list[str] = field(default_factory=list)


@dataclass
class PrizeProblem:
    """Normalized internal representation of a prize problem."""
    prize_id: str
    title: str
    statement: str
    target_type: str  # "proof", "counterexample", "computation", "benchmark"
    constraints: ProblemConstraints = field(default_factory=ProblemConstraints)
    attempts: list[dict] = field(default_factory=list)
    formal_dir: Optional[Path] = None


def ingest(problem_dir: str) -> PrizeProblem:
    """
    Ingest a problem from a structured definition directory.

    Expects:
      problem_dir/problem.yaml — with fields: prize_id, title, statement,
        target_type, constraints (proven_subcases, known_barriers,
        computational_bounds, equivalent_formulations)
    """
    prob_path = Path(problem_dir)
    yaml_path = prob_path / "problem.yaml"

    if not yaml_path.exists():
        raise FileNotFoundError(f"No problem.yaml in {problem_dir}")

    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    constraints_data = data.get("constraints", {})
    constraints = ProblemConstraints(
        proven_subcases=constraints_data.get("proven_subcases", []),
        known_barriers=constraints_data.get("known_barriers", []),
        computational_bounds=constraints_data.get("computational_bounds", {}),
        equivalent_formulations=constraints_data.get("equivalent_formulations", []),
    )

    formal_dir = prob_path / "formal"
    if not formal_dir.exists():
        formal_dir = None

    return PrizeProblem(
        prize_id=data["prize_id"],
        title=data["title"],
        statement=data["statement"],
        target_type=data["target_type"],
        constraints=constraints,
        formal_dir=formal_dir,
    )


def validate(problem: PrizeProblem) -> list[str]:
    """Validate that a problem has all required fields."""
    issues = []
    if not problem.prize_id:
        issues.append("Missing prize_id")
    if not problem.title:
        issues.append("Missing title")
    if not problem.statement:
        issues.append("Missing statement")
    if problem.target_type not in ["proof", "counterexample", "computation", "benchmark"]:
        issues.append(f"Unknown target_type: {problem.target_type}")
    return issues


def stage(problem: PrizeProblem, output_dir: str = "problems/") -> Path:
    """Stage an ingested problem for solver orchestration."""
    out = Path(output_dir) / problem.prize_id
    out.mkdir(parents=True, exist_ok=True)

    manifest = asdict(problem)
    manifest["constraints"] = asdict(problem.constraints)

    with open(out / "manifest.yaml", "w") as f:
        yaml.dump(manifest, f, default_flow_style=False)

    return out