# SHACL Validation

Jansutra uses SHACL (Shapes Constraint Language) to enforce data quality. SHACL shapes are defined in `shapes/*.shacl.ttl` — one file per ontology module — and cover three categories of constraint.

---

## What SHACL enforces here

**Structural constraints** — cardinality and datatype:
- `jansutra:residesIn` must appear at least once on every `Citizen`
- `jansutra:disabilityBenchmark` must be a `xsd:decimal` between 0 and 100
- `jansutra:householdSize` must be a positive integer ≤ 30

**Taxonomic constraints** — SKOS scheme membership:
- `jansutra:casteCategory` must be a concept `skos:inScheme jansutra:CasteCategoryScheme`
- `jansutra:accessType` must be a concept in `jansutra:ServiceTypeScheme`
- (All SKOS-typed properties are similarly constrained)

**Semantic co-constraints** — cross-property logic (SPARQL-based):
- If `jansutra:hasDisability true` is present on a `HealthRecord`, then `jansutra:disabilityType` must also be present

---

## Shape summary

| Shape | Target class | Key constraints |
|-------|-------------|----------------|
| `CitizenShape` | `Citizen` | `residesIn` minCount 1; `schema:birthDate` maxCount 1 xsd:date; all domain records maxCount 1 |
| `VulnerabilityDimensionShape` | `VulnerabilityDimension` | `surveyYear` maxCount 1 xsd:gYear; `dataSource` maxCount 1 xsd:string |
| `SocialRecordShape` | `SocialRecord` | `casteCategory` min/max 1 in CasteCategoryScheme; `genderIdentity` min/max 1 in GenderIdentityScheme; `religion` maxCount 1 in ReligionScheme |
| `EconomicRecordShape` | `EconomicRecord` | `annualHouseholdIncome` ≥ 0; `householdSize` ≤ 30; `povertyStatus` in PovertyStatusScheme |
| `AdministrativeUnitShape` | `AdministrativeUnit` | `adminLevel` min/max 1 in AdminLevelScheme; `lgdCode` minCount 1 minLength 1; `skos:prefLabel` minCount 1 |
| `LandHoldingShape` | `LandHolding` | `areaInHectares` minCount 1, ≥ 0, < 500; `landType` and `tenureType` min/max 1 in their schemes |
| `HealthRecordShape` | `HealthRecord` | `disabilityBenchmark` 0–100; `childrenUnder5` ≤ 10; SPARQL co-constraint on disability |
| `ServiceAccessRecordShape` | `ServiceAccessRecord` | `hasServiceAccess` must point to `ServiceAccess` instances |
| `ServiceAccessShape` | `ServiceAccess` | `accessType` minCount 1 in ServiceTypeScheme; `accessQuality` minCount 1 in AccessQualityScheme; `distanceInKm` < 200 |

---

## How to run

```bash
pip install rdflib pyshacl rich

python tools/validate.py examples/household-001.jsonld
```

Expected output:

```
Loaded data: examples/household-001.jsonld
Loaded 7 ontology module(s)
Loaded 7 SHACL shape file(s)
✓ Data conforms to all SHACL shapes.
```

To validate multiple files at once:

```bash
python tools/validate.py examples/household-001.jsonld examples/household-002.jsonld
```

---

## The merged-graph trick

SHACL scheme membership checks (`sh:node` + `sh:hasValue`) require the SKOS concept triples to be present in the data graph — not just the ontology graph.

Specifically, to validate that `jansutra:ST skos:inScheme jansutra:CasteCategoryScheme`, pyshacl needs the triple `jansutra:ST skos:inScheme jansutra:CasteCategoryScheme` to be a **fact** accessible during shape evaluation. When this triple lives only in the ontology graph and pyshacl receives it separately via the `ont_graph` parameter, the check silently fails — `ont_graph` is used for OWL inference hints, not for making ontology triples into shape-evaluation facts.

The fix in `tools/validate.py`:

```python
# Merge ontology into data so skos:inScheme triples are available
# as facts during sh:node / sh:hasValue shape checks.
merged_graph = data_graph + ontology_graph

conforms, results_graph, results_text = pyshacl.validate(
    merged_graph,
    shacl_graph=shapes_graph,
    inference="rdfs",
    abort_on_first=False,
)
```

This is the canonical pattern for pyshacl validation in Jansutra. Any ETL script or test that calls pyshacl directly must use the same merge.

---

## SHACL shape files

=== "core.shacl.ttl"

    ```turtle
    --8<-- "shapes/core.shacl.ttl"
    ```

=== "social.shacl.ttl"

    ```turtle
    --8<-- "shapes/social.shacl.ttl"
    ```

=== "economic.shacl.ttl"

    ```turtle
    --8<-- "shapes/economic.shacl.ttl"
    ```

=== "geography.shacl.ttl"

    ```turtle
    --8<-- "shapes/geography.shacl.ttl"
    ```

=== "land.shacl.ttl"

    ```turtle
    --8<-- "shapes/land.shacl.ttl"
    ```

=== "health.shacl.ttl"

    ```turtle
    --8<-- "shapes/health.shacl.ttl"
    ```

=== "services.shacl.ttl"

    ```turtle
    --8<-- "shapes/services.shacl.ttl"
    ```
