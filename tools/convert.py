"""Convert Jansutra JSON-LD ontology files to Turtle (.ttl)."""

import sys
from pathlib import Path

from rdflib import Graph
from rich.console import Console

REPO_ROOT = Path(__file__).parent.parent
ONTOLOGY_DIR = REPO_ROOT / "ontology"


def convert_file(src: Path, dest: Path, console: Console) -> None:
    g = Graph()
    g.parse(str(src), format="json-ld")
    dest.parent.mkdir(parents=True, exist_ok=True)
    g.serialize(destination=str(dest), format="turtle")
    console.print(f"[green]✓[/green] {src.name} → {dest}")


def main() -> None:
    console = Console()

    if len(sys.argv) > 1:
        sources = [Path(p) for p in sys.argv[1:]]
    else:
        sources = sorted(ONTOLOGY_DIR.glob("*.jsonld"))

    if not sources:
        console.print("[yellow]No .jsonld files found.")
        sys.exit(0)

    for src in sources:
        if not src.exists():
            console.print(f"[red]Not found: {src}")
            continue
        dest = src.with_suffix(".ttl")
        convert_file(src, dest, console)

    console.print(f"\n[bold]Converted {len(sources)} file(s).")


if __name__ == "__main__":
    main()
