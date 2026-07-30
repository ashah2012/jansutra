# Geography Module

**File:** `ontology/geography.jsonld`

The geography module models India's four-level administrative hierarchy. Every administrative unit carries a mandatory LGD code — the interoperability key that makes Jansutra data joinable with all central government ministry datasets.

---

## Class: `jansutra:AdministrativeUnit`

Represents a node in India's administrative hierarchy: State/UT → District → Sub-district (Block/Taluka) → Village/Ward.

Instance URIs follow the `geo:` namespace pattern:
- State: `geo:state/jharkhand`
- District: `geo:district/jharkhand/west-singhbhum`
- Sub-district: `geo:subdistrict/jharkhand/west-singhbhum/chakradharpur`
- Village: `geo:village/jharkhand/west-singhbhum/chakradharpur/bandgaon`

---

## SKOS scheme

### `jansutra:AdminLevelScheme`

Four hierarchical levels, encoded as a `skos:broader` chain (L2 broader than L1, etc.).

| URI | Notation | Level | Description |
|-----|----------|-------|-------------|
| `jansutra:StateUT` | `L1` | 1 | State or Union Territory (36 units) |
| `jansutra:District` | `L2` | 2 | District (`skos:broader StateUT`) |
| `jansutra:SubDistrict` | `L3` | 3 | Block / Taluka / Mandal (`skos:broader District`) |
| `jansutra:VillageWard` | `L4` | 4 | Revenue village or urban ward (`skos:broader SubDistrict`) |

---

## Properties

| Property | Type | Range | Required | Notes |
|----------|------|-------|---------|-------|
| `jansutra:adminLevel` | Object | `AdminLevelScheme` concept | Yes (minCount 1) | Must be one of L1–L4 |
| `jansutra:lgdCode` | Datatype | `xsd:string` | Yes (minCount 1, minLength 1) | MoPR LGD canonical code |
| `jansutra:hasParentUnit` | Object | `AdministrativeUnit` | No | `owl:equivalentProperty skos:broader`; enables `hasParentUnit*` transitive SPARQL path |
| `jansutra:isRemoteArea` | Datatype | `xsd:boolean` | No | `true` if no all-weather road within 5 km (PMGSY criterion) |
| `jansutra:isPESAArea` | Datatype | `xsd:boolean` | No | `true` if under Fifth Schedule (PESA Act 1996); tribal self-governance applies |
| `jansutra:hasGeometry` | Object | `gsp:Geometry` | No | WKT polygon (district level and above) |

---

## Why LGD codes

The Ministry of Panchayati Raj's Local Government Directory (LGD) is India's canonical administrative gazetteer. It assigns stable numeric codes to every state, district, sub-district, and village. Unlike census village codes — which change between decennial surveys due to splits, merges, and reclassifications — LGD codes are designed for ongoing administrative use.

Pinning Jansutra administrative unit IRIs to LGD codes means:
- Jansutra data from a 2024 survey can be joined with 2026 survey data without key-remapping
- Ministry datasets that use LGD codes (MGNREGA, PMGSY, JJM, SBM-G) can be linked without fuzzy name matching
- The `lgdCode` field is the primary cross-reference key for ETL pipelines

---

## PESA and remoteness flags

`jansutra:isPESAArea` — marks villages under the Panchayats (Extension to Scheduled Areas) Act 1996, which applies in Fifth Schedule tribal areas across nine states. PESA confers gram sabha authority over natural resources and welfare delivery. It is a prerequisite for many MoTA-administered programs.

`jansutra:isRemoteArea` — marks villages without an all-weather (paved) road within 5 km, the threshold used by PMGSY to classify unconnected habitations. In the example data, Bandgaon village carries both flags.

---

## Hierarchy traversal in SPARQL

The `jansutra:hasParentUnit*` property path uses SPARQL's zero-or-more transitive closure to traverse the hierarchy in either direction:

```sparql
# Find the district for a given village
?village jansutra:hasParentUnit* ?district .
?district jansutra:adminLevel jansutra:District .
```

This works because each unit has exactly one `hasParentUnit` pointing upward, and the `*` path follows the chain: Village → Sub-district → District → State.

---

## Source file

```json
--8<-- "ontology/geography.jsonld"
```
