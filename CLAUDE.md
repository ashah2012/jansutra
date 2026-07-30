# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**Jansutra** ("citizen thread") is a federated, privacy-by-design semantic data model for India's citizen socioeconomic data — motivated by [this blog post](https://abhishek-shah.dev/blog/2026/07/25/india-needs-central-database/). It is an OWL ontology with SHACL validation shapes and Python tooling, serialized in JSON-LD (primary) and Turtle (derived).

## Commands

```bash
# Install
pip install -e .

# Validate a data file against all SHACL shapes
python tools/validate.py examples/household-001.jsonld

# Run a SPARQL query (loads all ontology modules + optional data files)
python tools/query.py sparql/vulnerability-query.sparql examples/household-001.jsonld

# Convert all JSON-LD ontology files to Turtle
python tools/convert.py

# Convert a single file
python tools/convert.py ontology/core.jsonld
```

## Architecture

Each socioeconomic domain is a **separate JSON-LD file** under `ontology/` — no single file holds the full citizen profile. This mirrors the blog's "federated datastores" principle.

```
ontology/
  context/jansutra.context.jsonld   ← shared prefix declarations (load this everywhere)
  core.jsonld                       ← jansutra:Citizen class + links to all domain records
  social.jsonld                     ← caste (SC/ST/OBC/NT/DNT), gender, religion SKOS schemes
  economic.jsonld                   ← income, poverty status, occupation SKOS schemes
  geography.jsonld                  ← administrative hierarchy (State→District→Sub-district→Village)
  land.jsonld                       ← land holdings, tenure type, FRA titles
  health.jsonld                     ← disability (RPWD 2016), health insurance, children under 5
  services.jsonld                   ← access to water, electricity, PHC, school, road, internet

shapes/                             ← SHACL constraint files (Turtle), one per ontology module
examples/household-001.jsonld       ← annotated ST BPL female citizen in Jharkhand (PESA area)
sparql/                             ← reusable SPARQL queries for vulnerability analysis
tools/validate.py                   ← pyshacl runner
tools/query.py                      ← rdflib SPARQL runner with Rich table output
tools/convert.py                    ← JSON-LD → Turtle serializer
```

## Namespace conventions

| Prefix | Base IRI | Purpose |
|--------|----------|---------|
| `jansutra:` | `https://jansutra.in/vocab/` | All custom classes, properties, and SKOS concepts |
| `citizen:` | `https://jansutra.in/citizen/` | Citizen instance URIs (`citizen:<uuid>`) |
| `geo:` | `https://jansutra.in/geo/` | Administrative unit instance URIs |
| `scheme:` | `https://jansutra.in/scheme/` | Scheme-level URIs (reserved) |

Reused vocabularies: `schema:` (Person/Place), `skos:` (taxonomies), `dpv:` (DPDP Act compliance annotations), `prov:` (data provenance), `gsp:` (GeoSPARQL geometry), `owl:`/`rdfs:`/`xsd:`.

## Key design rules

- **No Aadhaar numbers** — citizens are identified by opaque UUID URIs only.
- **All SKOS taxonomies are defined inline** in their domain module (e.g., `jansutra:CasteCategoryScheme` lives in `social.jsonld`).
- **LGD codes** are mandatory on every `jansutra:AdministrativeUnit` — they are India's canonical administrative identifiers (MoPR Local Government Directory).
- **`dpv:SensitivePersonalData`** annotation is required on all caste, religion, disability, and gender properties (DPDP Act 2023 compliance).
- **Provenance**: every `VulnerabilityDimension` subclass instance should carry `jansutra:surveyYear` and `jansutra:dataSource`.
- SHACL shapes enforce scheme membership via `sh:node` + `sh:hasValue jansutra:<SchemeName>` — don't bypass this by adding concepts without `skos:inScheme`.

## Adding a new dimension

1. Create `ontology/<domain>.jsonld` — define the class (subClassOf `jansutra:VulnerabilityDimension`), its SKOS schemes, and OWL properties.
2. Add the linking property (`jansutra:has<Domain>Record`) in `ontology/core.jsonld`.
3. Create `shapes/<domain>.shacl.ttl`.
4. Add an example instance to `examples/household-001.jsonld`.
5. Run `python tools/validate.py examples/household-001.jsonld` to confirm conformance.
