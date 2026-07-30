# Jansutra — जनसूत्र

**"Citizen thread"** — a federated, privacy-by-design semantic data model for India's citizen socioeconomic data.

Motivated by [this blog post](https://abhishek-shah.dev/blog/2026/07/25/india-needs-central-database/): India's welfare system runs on fragmented, 15-year-old SECC data. Ministry silos cannot be joined. Precision welfare targeting — finding the ST woman in a PESA village who has no piped water, no PHC within 20 km, and a 0.8-hectare FRA title she can't leverage — is impossible today.

Jansutra models multi-dimensional vulnerability as a **linked, federated OWL ontology** so that intersectional queries across caste, income, land, health, and service access become straightforward SPARQL.

---

## Design principles

- **No Aadhaar** — citizens are opaque UUID URIs. Identity is never stored.
- **Federated modules** — each socioeconomic domain is a separate JSON-LD file. No single file contains the full citizen profile.
- **Privacy by design** — caste, religion, gender, and disability properties carry `dpv:SensitivePersonalData` annotations (DPDP Act 2023).
- **LGD-anchored geography** — every administrative unit carries a mandatory MoPR Local Government Directory code.
- **SHACL-enforced** — all structural and taxonomic constraints are machine-checkable.

---

## Repository layout

```
ontology/
  context/jansutra.context.jsonld   ← shared prefix declarations
  core.jsonld                       ← Citizen class + links to domain records
  social.jsonld                     ← caste, gender, religion (SKOS schemes)
  economic.jsonld                   ← income, poverty status, occupation
  geography.jsonld                  ← State → District → Sub-district → Village
  land.jsonld                       ← land holdings, tenure, FRA titles
  health.jsonld                     ← disability (RPWD 2016), insurance, ICDS
  services.jsonld                   ← water, electricity, road, school, PHC, internet

shapes/                             ← SHACL constraint files (one per module)
examples/
  household-001.jsonld              ← ST/BPL female citizen, West Singhbhum, Jharkhand
sparql/
  vulnerability-query.sparql        ← ST citizens in PESA areas without water + PHC
  poverty-by-district.sparql        ← BPL/AAY counts per district, broken down by caste
  land-gap-by-caste.sparql          ← average landholding area by caste category
tools/
  validate.py                       ← SHACL validation runner
  query.py                          ← SPARQL query runner (Rich table output)
  convert.py                        ← JSON-LD → Turtle serializer
```

---

## Quickstart

```bash
pip install rdflib pyshacl rich

# Validate a data file against all SHACL shapes
python tools/validate.py examples/household-001.jsonld

# Run the core vulnerability query
python tools/query.py sparql/vulnerability-query.sparql examples/household-001.jsonld

# Convert all ontology JSON-LD files to Turtle
python tools/convert.py
```

---

## The core use case

```sparql
-- Find ST citizens in PESA/remote areas with no safe water AND no PHC access
SELECT ?citizen ?districtLabel ?povertyStatus ?phcDistanceKm
WHERE {
  ?citizen a jansutra:Citizen ;
           jansutra:residesIn ?village ;
           jansutra:hasSocialRecord ?social .
  ?social jansutra:casteCategory jansutra:ST .
  ?village jansutra:isRemoteArea true .
  ...
  FILTER NOT EXISTS { ... water access with Reliable/Intermittent quality ... }
}
```

Against the example data, this surfaces the Bandgaon (West Singhbhum) household — ST, BPL, PHC 18.5 km away, no functional water source.

---

## Ontology modules

| Module | Key classes & schemes |
|--------|----------------------|
| `core` | `jansutra:Citizen`, `jansutra:VulnerabilityDimension` |
| `social` | `CasteCategoryScheme` (SC/ST/OBC-C/OBC-S/EWS/NT/DNT/GEN), `GenderIdentityScheme`, `ReligionScheme` |
| `economic` | `PovertyStatusScheme` (BPL/APL/AAY), `OccupationTypeScheme` |
| `geography` | `AdminLevelScheme` (L1–L4), LGD codes, PESA/remote flags |
| `land` | `LandTypeScheme` (FRA forest land, irrigated, dryland…), `TenureTypeScheme` |
| `health` | `DisabilityTypeScheme` (RPWD Act 2016), PM-JAY, children under 5 |
| `services` | `ServiceTypeScheme` (piped water, electricity, PHC, school…), `AccessQualityScheme` |

---

## Namespaces

| Prefix | Base IRI | Purpose |
|--------|----------|---------|
| `jansutra:` | `https://jansutra.in/vocab/` | All custom classes, properties, SKOS concepts |
| `citizen:` | `https://jansutra.in/citizen/` | Citizen instance URIs |
| `geo:` | `https://jansutra.in/geo/` | Administrative unit instance URIs |
| `schema:` | `https://schema.org/` | Person, Place |
| `skos:` | `http://www.w3.org/2004/02/skos/core#` | Taxonomies |
| `dpv:` | `https://w3id.org/dpv#` | DPDP Act 2023 privacy annotations |
| `prov:` | `http://www.w3.org/ns/prov#` | Data provenance |
| `gsp:` | `http://www.opengis.net/ont/geosparql#` | Geographic geometry |

---

## Adding a new dimension

1. Create `ontology/<domain>.jsonld` — define the class (`rdfs:subClassOf jansutra:VulnerabilityDimension`), SKOS schemes, and OWL properties.
2. Add the linking property (`jansutra:has<Domain>Record`) in `ontology/core.jsonld`.
3. Create `shapes/<domain>.shacl.ttl`.
4. Add an instance to `examples/household-001.jsonld`.
5. Run `python tools/validate.py examples/household-001.jsonld` to confirm conformance.
