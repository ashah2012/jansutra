"""SPARQL query tool for Jansutra ontology + data files."""

import sys
from pathlib import Path

from rdflib import ConjunctiveGraph
from rich.console import Console
from rich.table import Table

REPO_ROOT = Path(__file__).parent.parent
ONTOLOGY_DIR = REPO_ROOT / "ontology"


def _load_dir(g: ConjunctiveGraph, directory: Path, pattern: str) -> None:
    for f in sorted(directory.glob(pattern)):
        g.parse(str(f))


def main() -> None:
    console = Console()

    if len(sys.argv) < 2:
        console.print("[red]Usage: query.py <query.sparql> [data-file.jsonld ...]")
        sys.exit(1)

    query_path = Path(sys.argv[1])
    if not query_path.exists():
        console.print(f"[red]Query file not found: {query_path}")
        sys.exit(1)

    graph = ConjunctiveGraph()
    _load_dir(graph, ONTOLOGY_DIR, "*.jsonld")

    for arg in sys.argv[2:]:
        path = Path(arg)
        if not path.exists():
            console.print(f"[red]Data file not found: {path}")
            sys.exit(1)
        graph.parse(str(path))
        console.print(f"[dim]Loaded data: {path}")

    query_text = query_path.read_text(encoding="utf-8")
    results = graph.query(query_text)

    if results.type == "ASK":
        console.print(f"[bold]Result:[/bold] {results.askAnswer}")
        return

    if not results.vars:
        console.print(f"[green]Query executed. {len(results)} triple(s) affected.")
        return

    table = Table(*[str(v) for v in results.vars], show_lines=True)
    row_count = 0
    for row in results:
        table.add_row(*[str(v) if v is not None else "" for v in row])
        row_count += 1

    console.print(table)
    console.print(f"[dim]{row_count} result(s)")


if __name__ == "__main__":
    main()
