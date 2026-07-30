"""SHACL validation tool for Jansutra data files."""

import sys
from pathlib import Path

import pyshacl
from rdflib import Graph
from rich.console import Console

REPO_ROOT = Path(__file__).parent.parent
ONTOLOGY_DIR = REPO_ROOT / "ontology"
SHAPES_DIR = REPO_ROOT / "shapes"


def _load_dir(g: Graph, directory: Path, pattern: str) -> None:
    for f in sorted(directory.glob(pattern)):
        g.parse(str(f))


def main() -> None:
    console = Console()

    if len(sys.argv) < 2:
        console.print("[red]Usage: validate.py <data-file.jsonld> [data-file2 ...]")
        sys.exit(1)

    data_graph = Graph()
    for arg in sys.argv[1:]:
        path = Path(arg)
        if not path.exists():
            console.print(f"[red]File not found: {path}")
            sys.exit(1)
        data_graph.parse(str(path))
        console.print(f"[dim]Loaded data: {path}")

    ontology_graph = Graph()
    _load_dir(ontology_graph, ONTOLOGY_DIR, "*.jsonld")
    console.print(f"[dim]Loaded {len(list(ONTOLOGY_DIR.glob('*.jsonld')))} ontology module(s)")

    shapes_graph = Graph()
    _load_dir(shapes_graph, SHAPES_DIR, "*.shacl.ttl")
    console.print(f"[dim]Loaded {len(list(SHAPES_DIR.glob('*.shacl.ttl')))} SHACL shape file(s)")

    # Merge ontology into data so SKOS concept membership triples (skos:inScheme)
    # are available as facts during sh:node / sh:hasValue shape checks.
    merged_graph = data_graph + ontology_graph

    conforms, results_graph, results_text = pyshacl.validate(
        merged_graph,
        shacl_graph=shapes_graph,
        inference="rdfs",
        abort_on_first=False,
    )

    if conforms:
        console.print("[green bold]✓ Data conforms to all SHACL shapes.")
    else:
        console.print("[red bold]✗ Validation failed — constraint violations found:\n")
        console.print(results_text)
        sys.exit(1)


if __name__ == "__main__":
    main()
