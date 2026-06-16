"""
literature_map.py — Known-results ingestion and arXiv search

For each prize problem, this module:
  1. Checks local knowledge base (yaml manifests, references/)
  2. Searches arXiv for recent papers
  3. Extracts known theorems, bounds, barriers
  4. Produces a structured literature map for the solver

This prevents CAPT from rediscovering known results.
"""

import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field, asdict
from typing import Optional
from pathlib import Path


@dataclass
class LiteratureEntry:
    """A known result from the literature."""
    problem_id: str
    title: str
    authors: str
    year: int
    result_type: str  # theorem / bound / barrier / computational / survey
    summary: str
    url: str = ""
    is_barrier: bool = False  # True if this result proves an approach impossible
    is_partial_proof: bool = False  # True if this proves a special case


@dataclass
class LiteratureMap:
    """Full literature map for a prize problem."""
    problem_id: str
    entries: list[LiteratureEntry] = field(default_factory=list)
    known_barriers: list[str] = field(default_factory=list)
    proven_subcases: list[str] = field(default_factory=list)
    computational_bounds: dict[str, str] = field(default_factory=dict)
    equivalent_formulations: list[str] = field(default_factory=list)


ARXIV_API = "http://export.arxiv.org/api/query"


def search_arxiv(query: str, max_results: int = 10) -> list[LiteratureEntry]:
    """
    Search arXiv for papers matching a query.

    Returns list of LiteratureEntry objects parsed from arXiv XML API.
    """
    params = urllib.parse.urlencode({
        "search_query": f"all:{query}",
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending",
    })
    url = f"{ARXIV_API}?{params}"

    entries = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "capts-prizeops/0.1"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read().decode("utf-8")

        ns = {"a": "http://www.w3.org/2005/Atom",
              "arxiv": "http://arxiv.org/schemas/atom"}
        root = ET.fromstring(data)

        for entry_elem in root.findall("a:entry", ns):
            title = entry_elem.find("a:title", ns)
            summary = entry_elem.find("a:summary", ns)
            published = entry_elem.find("a:published", ns)
            url = entry_elem.find("a:id", ns)
            authors = entry_elem.findall("a:author", ns)

            title_text = (title.text or "").strip() if title is not None else ""
            summary_text = (summary.text or "").strip()[:300] if summary is not None else ""
            pub_year = int((published.text or "")[:4]) if published is not None else 0
            author_text = ", ".join(
                (a.find("a:name", ns).text or "") for a in (authors or [])
                if a.find("a:name", ns) is not None
            )
            url_text = (url.text or "").strip() if url is not None else ""

            if title_text:
                entries.append(LiteratureEntry(
                    problem_id="",
                    title=title_text,
                    authors=author_text,
                    year=pub_year,
                    result_type="paper",
                    summary=summary_text[:300],
                    url=url_text,
                ))
    except Exception as e:
        print(f"[ARXIV] Error: {e}")

    return entries


def build_literature_map(prize_id: str) -> LiteratureMap:
    """
    Build a literature map for a prize problem.

    Combines data from:
      - prizes/<prize_id>.yaml (known constraints)
      - problems/<prize_id>/references/ (local references)
      - arXiv search (recent papers)
    """
    lmap = LiteratureMap(problem_id=prize_id)

    # Check local prizes/ YAML for known results
    prizes_dir = Path(__file__).parent.parent / "prizes"
    yaml_path = prizes_dir / f"{prize_id.split('_')[0]}.yaml"  # e.g. beal.yaml
    if yaml_path.exists():
        try:
            import yaml
            with open(yaml_path) as f:
                data = yaml.safe_load(f)
            if isinstance(data, dict):
                for key in ("proven_subcases", "known_barriers"):
                    items = data.get("constraints", {}).get(key, [])
                    for item in items:
                        lmap.entries.append(LiteratureEntry(
                            problem_id=prize_id,
                            title=item,
                            authors="(from prize manifest)",
                            year=0,
                            result_type="known_result",
                            summary=item,
                        ))
        except Exception:
            pass

    # Check problems/<prize_id>/references/
    ref_dir = Path(__file__).parent.parent / "problems" / prize_id / "references"
    if ref_dir.exists():
        for fpath in sorted(ref_dir.glob("*")):
            try:
                text = fpath.read_text()[:500]
                lmap.entries.append(LiteratureEntry(
                    problem_id=prize_id,
                    title=fpath.name,
                    authors="(local reference)",
                    year=0,
                    result_type="reference",
                    summary=text[:300],
                ))
            except Exception:
                pass

    # arXiv search
    try:
        arxiv_entries = search_arxiv(prize_id.replace("_", " "))
        lmap.entries.extend(arxiv_entries)
    except Exception as e:
        print(f"[LIT] arXiv search failed: {e}")

    return lmap


def summarize_map(lmap: LiteratureMap) -> str:
    """Generate a human-readable summary of the literature map."""
    lines = [f"Literature Map: {lmap.problem_id}", "=" * 50]
    lines.append(f"Total entries: {len(lmap.entries)}")
    barriers = [e for e in lmap.entries if e.is_barrier]
    if barriers:
        lines.append(f"\nKnown barriers ({len(barriers)}):")
        for b in barriers:
            lines.append(f"  - {b.title}")
    partials = [e for e in lmap.entries if e.is_partial_proof]
    if partials:
        lines.append(f"\nPartial proofs ({len(partials)}):")
        for p in partials:
            lines.append(f"  - {p.title}")
    if lmap.equivalent_formulations:
        lines.append(f"\nEquivalent formulations ({len(lmap.equivalent_formulations)}):")
        for f in lmap.equivalent_formulations:
            lines.append(f"  - {f}")
    lines.append("\nRecent arXiv papers:")
    for e in lmap.entries[-5:]:
        lines.append(f"  [{e.year}] {e.authors}: {e.title}")
    return "\n".join(lines)