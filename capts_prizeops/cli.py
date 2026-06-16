"""
capts-prizeops CLI — CAPT Prize Operations

Commands:
  intake        Ingest a new prize problem from definition
  solve         Run CAPT solver pipeline against a prize target
  decompose     Decompose a prize problem into CAPT-solvable subproblems
  literature    Search literature for known results on a problem
  erdos         Run Erdős–Gyárfás counterexample search
  conway        Run Conway 99-graph SAT search (various encodings)
  aimo          Run AIMO benchmark against solver candidates
  arena         Compare solver candidates in Arena
  ledger        Show prize opportunity ledger
"""

import click
import yaml
from pathlib import Path


def _import_pipelines(module: str):
    import sys, importlib.util
    pkg_dir = Path(__file__).parent.parent / "pipelines"
    spec = importlib.util.spec_from_file_location(module, pkg_dir / f"{module}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module] = mod
    spec.loader.exec_module(mod)
    return mod


PRIZES_DIR = Path(__file__).parent.parent / "prizes"


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
    """Run SOLVE pipeline: decompose -> literature -> search -> verify -> package."""
    cd = _import_pipelines("conjecture_decomposer")
    plan = cd.decompose(prize_id)
    click.echo(f"Solving {prize_id}")
    click.echo(f"  Decomposed into {len(plan.subproblems)} subproblems:")
    for sp in plan.subproblems:
        status = "DONE" if sp.solved else "PENDING"
        click.echo(f"    [{status}] {sp.subproblem_id} ({sp.verification_method}, diff={sp.difficulty})")


@cli.command()
@click.argument("prize_id")
def decompose(prize_id):
    """Decompose a prize problem into CAPT-solvable subproblems."""
    cd = _import_pipelines("conjecture_decomposer")
    plan = cd.decompose(prize_id)
    click.echo(f"Decomposition plan for {prize_id}:")
    click.echo(f"  {len(plan.subproblems)} subproblems")
    for sp in plan.subproblems:
        deps = f"  depends on: {sp.dependencies}" if sp.dependencies else ""
        click.echo(f"  [{sp.subproblem_type.name}] {sp.subproblem_id} ({sp.verification_method}){deps}")
        click.echo(f"    {sp.statement[:120]}")


@cli.command()
@click.argument("prize_id")
@click.option("--arxiv/--no-arxiv", default=True, help="Include arXiv search")
def literature(prize_id, arxiv):
    """Search literature for known results on a problem."""
    lm = _import_pipelines("literature_map")
    lmap = lm.build_literature_map(prize_id)
    click.echo(f"Literature map for {prize_id}")
    click.echo(f"  Total entries: {len(lmap.entries)}")
    for entry in lmap.entries:
        click.echo(f"  [{entry.year}] {entry.title}")


@cli.command()
@click.option("--problems", default="", help="Comma-separated problem IDs")
@click.option("--candidates", default="", help="Comma-separated solver IDs")
@click.option("--output", default="reports/arena_runs", help="Output directory")
def aimo(problems, candidates, output):
    """Run AIMO benchmark against solver candidates."""
    ah = _import_pipelines("aimo_harness")
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
@click.option("--method", default="incidence",
              type=click.Choice(["sat", "concat", "incidence"]),
              help="Z3 encoding method (incidence = n×k, 1386 vars)")
def conway(n, k, lam, mu, timeout, method):
    """Run Conway 99-graph search with the specified encoding method."""
    cs = _import_pipelines("counterexample_search")
    solvers = {
        "sat": cs.conway_conways_srg_sat_search,
        "concat": cs.conway_concatenated_search,
        "incidence": cs.conway_incidence_search,
    }
    solver_fn = solvers[method]
    click.echo(f"Conway SRG search: srg({n},{k},{lam},{mu}) via {method}")
    click.echo(f"  Timeout: {timeout}s")
    r = solver_fn(n=n, k=k, lam=lam, mu=mu, timeout=timeout)
    click.echo(f"  Found={r.found} verified={r.verification_status} in {r.runtime_seconds}s")
    if r.found and r.candidate:
        ok = cs.is_srg(r.candidate, n, k, lam, mu)
        click.echo(f"  SRG verification: {'PASS' if ok else 'FAIL'}")
    cs.record_result(r)


@cli.command()
@click.option("--max-n", default=12, type=int, help="Max vertices to search")
@click.option("--min-degree", default=3, type=int, help="Minimum vertex degree")
@click.option("--timeout", default=600, type=int, help="Search timeout in seconds")
def erdos(max_n, min_degree, timeout):
    """Run Erdős–Gyárfás counterexample search (nauty-backed)."""
    cs = _import_pipelines("counterexample_search")
    click.echo(f"Erdős–Gyárfás search: n ≤ {max_n}, min degree ≥ {min_degree}")
    click.echo(f"  Timeout: {timeout}s")
    results = cs.erdos_gyarfas_search(max_n=max_n, min_degree=min_degree, timeout=timeout)
    counterexamples = [r for r in results if r.found]
    if counterexamples:
        click.echo(f"\nFound {len(counterexamples)} counterexample(s)!")
        for r in counterexamples:
            click.echo(f"  n={r.search_parameters.get('n', '?')} "
                       f"graph={r.search_parameters.get('graph6', '?')}")
    else:
        click.echo(f"\nNo counterexamples found — conjecture holds in this range")
    for r in results:
        cs.record_result(r)


if __name__ == "__main__":
    cli()