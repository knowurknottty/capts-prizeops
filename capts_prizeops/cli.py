"""
capts-prizeops CLI — CAPT Prize Operations

Commands:
  intake        Ingest a new prize problem from definition
  solve         Run CAPT solver pipeline against a prize target
  arena         Compare solver candidates in Arena
  ledger        Show prize opportunity ledger
  report        Generate a report from a proof attempt
  aimo          Run AIMO benchmark against solver candidates
  conway        Run Conway 99-graph SAT search
"""

import click
import yaml
import json
from pathlib import Path


def _import_pipelines(module: str):
    """Lazy-import from pipelines/ directory next to this file."""
    import sys, importlib.util
    pkg_dir = Path(__file__).parent.parent / "pipelines"
    spec = importlib.util.spec_from_file_location(module, pkg_dir / f"{module}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module] = mod
    spec.loader.exec_module(mod)
    return mod


PRIZES_DIR = Path(__file__).parent.parent / "prizes"
PIPELINES_DIR = Path(__file__).parent.parent / "pipelines"


@click.group()
def cli():
    pass


@cli.command()
@click.option("--prize-id", "-p", help="Prize ID to show (omit for full ledger)")
def ledger(prize_id):
    """Show prize opportunity ledger."""
    ledger_path = PRIZES_DIR / "prize_ledger.yaml"
    if not ledger_path.exists():
        click.echo("Error: prize_ledger.yaml not found")
        return
    with open(ledger_path) as f:
        prizes = yaml.safe_load(f)
    if prize_id:
        prizes = [p for p in prizes if p.get("prize_id") == prize_id]
        if not prizes:
            click.echo(f"No prize found with id: {prize_id}")
            return
    click.echo(f"{'Prize ID':<30} {'Value':<12} {'Fit':<18} {'Status'}")
    click.echo("-" * 80)
    for p in sorted(prizes, key=lambda x: x.get("amount_usd", 0), reverse=True):
        pid = p.get("prize_id", "?")
        val = f"${p.get('amount_usd', 0):,}"
        fit = p.get("capts_fit", "?")
        status = p.get("status", "?")
        click.echo(f"{pid:<30} {val:<12} {fit:<18} {status}")


@cli.command()
@click.argument("prize_id")
@click.option("--depth", default=3, help="CAPT cogitation depth")
@click.option("--research-depth", default=5, type=int,
              help="Research depth (0-10, 5=medium)")
def solve(prize_id, depth, research_depth):
    """Run CAPT solver pipeline against a prize target."""
    click.echo(f"Solving {prize_id}...")
    click.echo(f"  depth={depth}, research_depth={research_depth}")
    click.echo("  Pipeline: intake -> decompose -> search -> verify -> package")
    click.echo("  (CAPT backend connection required)")


@cli.command()
@click.option("--prize-id", "-p", help="Filter by prize")
@click.option("--candidates", default="arena_runs/latest",
              help="Candidate directory")
def arena(prize_id, candidates):
    """Compare solver candidates in Arena."""
    click.echo(f"Arena comparison for {prize_id or 'all prizes'}")
    click.echo(f"  Candidates from: {candidates}")
    click.echo("  (Arena integration required)")


@cli.command()
@click.argument("problem_dir")
@click.option("--output", "-o", default="reports/",
              help="Output directory")
def intake(problem_dir, output):
    """Ingest a new prize problem from a definition directory."""
    click.echo(f"Ingesting problem from: {problem_dir}")
    click.echo(f"  Output: {output}")
    click.echo("  (Problem intake pipeline running...)")


@cli.command()
@click.option("--problems", default="", help="Comma-separated problem IDs")
@click.option("--candidates", default="", help="Comma-separated solver IDs")
@click.option("--output", default="reports/arena_runs", help="Output directory")
def aimo(problems, candidates, output):
    from capts_prizeops.cli import _import_pipelines as _ip
    ah = _ip("aimo_harness")

    problem_list = (
        ah.list_benchmarks() if not problems
        else [p.strip() for p in problems.split(",")]
    )
    candidate_list = (
        ah.SOLVER_CANDIDATES if not candidates
        else [c for c in ah.SOLVER_CANDIDATES if c.solver_id in candidates]
    )

    click.echo(f"AIMO Benchmark: {len(problem_list)} problems x {len(candidate_list)} candidates")
    for p in problem_list:
        click.echo(f"  Problem: {p}")
    for c in candidate_list:
        click.echo(f"  Solver: {c.solver_id} ({c.description})")

    results = ah.benchmark_candidates(problem_list, candidate_list)
    report = ah.generate_report(results, output)
    click.echo(f"\nReport written to: {report}")


@cli.command()
@click.option("--n", default=99, type=int, help="Number of vertices")
@click.option("--k", default=14, type=int, help="Degree")
@click.option("--lam", default=1, type=int, help="Lambda (adjacent common neighbors)")
@click.option("--mu", default=2, type=int, help="Mu (non-adjacent common neighbors)")
@click.option("--timeout", default=600, type=int, help="Solver timeout in seconds")
def conway(n, k, lam, mu, timeout):
    cs = _import_pipelines("counterexample_search")
    click.echo(f"Conway SRG search: srg({n},{k},{lam},{mu})")
    click.echo(f"Timeout: {timeout}s")
    r = cs.conway_conways_srg_sat_search(n=n, k=k, lam=lam, mu=mu, timeout=timeout)
    click.echo(f"Found={r.found} verified={r.verification_status} time={r.runtime_seconds}s")
    if r.found and r.candidate:
        ok = cs.is_srg(r.candidate, n, k, lam, mu)
        click.echo(f"SRG verification: {'PASS' if ok else 'FAIL'}")
    cs.record_result(r)


if __name__ == "__main__":
    cli()