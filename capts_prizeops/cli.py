"""
capts-prizeops CLI — CAPT Prize Operations

Commands:
  intake        Ingest a new prize problem from definition
  solve         Run CAPT solver pipeline against a prize target
  arena         Compare solver candidates in Arena
  ledger        Show prize opportunity ledger
  report        Generate a report from a proof attempt
"""

import click
import yaml
from pathlib import Path


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
    """Run CAPT solver pipeline against a prize target."""
    click.echo(f"Solving {prize_id}...")
    click.echo(f"  depth={depth}, research_depth={research_depth}")
    click.echo("  Pipeline: intake → decompose → search → verify → package")
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


if __name__ == "__main__":
    cli()