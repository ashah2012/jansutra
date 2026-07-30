# Land Module

**File:** `ontology/land.jsonld`

The land module records individual land parcels — their area, type (irrigated, forest, homestead), and tenure status. A citizen may have zero or more `LandHolding` instances. This module is the primary vehicle for tracking Forest Rights Act (FRA 2006) title recognition.

---

## Class: `jansutra:LandHolding`

`rdfs:subClassOf jansutra:VulnerabilityDimension`

Inherits `surveyYear` and `dataSource`. Unlike other domain records, `LandHolding` is **not functional** — a citizen may hold multiple parcels (e.g., a homestead plot and a forest land parcel under FRA). Linked via `jansutra:hasLandHolding`.

---

## SKOS schemes

### `jansutra:LandTypeScheme`

Agricultural and land-use classification, aligned with State Revenue Department categories and FRA 2006 definitional scope.

| URI | Notation | Label | Notes |
|-----|----------|-------|-------|
| `jansutra:IrrigatedLand` | `IRRIG` | Irrigated Land | Net irrigated (canal, borewell, tank) |
| `jansutra:DrylandRainfed` | `DRY` | Dryland / Rainfed | Unirrigated cultivation |
| `jansutra:HomsteadLand` | `HOME` | Homestead Land | House site / kitchen garden |
| `jansutra:ForestLand` | `FOREST` | Forest Land (FRA) | Recognised or claimable under Forest Rights Act 2006 |
| `jansutra:WastelandFallow` | `FALLOW` | Wasteland / Fallow | Degraded or seasonally uncultivated |

### `jansutra:TenureTypeScheme`

Ownership and usage rights classification. Covers the full spectrum from formally titled to informally occupied — critical for identifying where land policy interventions (FRA recognition, tenancy reform) are needed.

| URI | Notation | Label | Notes |
|-----|----------|-------|-------|
| `jansutra:OwnedTitled` | `OWN-T` | Owned — Titled | Registered title deed in state revenue records |
| `jansutra:OwnedUntitled` | `OWN-U` | Owned — Untitled | Customary or tribal tenure, no formal registration; primary FRA claim category |
| `jansutra:Leased` | `LEASE` | Leased | Formal tenancy contract |
| `jansutra:Sharecropped` | `SHARE` | Sharecropped (*batai*) | Informal share-cropping arrangement |
| `jansutra:Encroached` | `ENC` | Encroached | Informal occupation, contested |
| `jansutra:CommunalCommons` | `COMM` | Communal Commons | Gram sabha land, shared pasture/forest |

!!! important "FRA identification pattern"
    To identify un-recognised customary tribal land claims (candidates for FRA filing):
    ```sparql
    ?holding jansutra:landType jansutra:ForestLand ;
             jansutra:tenureType jansutra:OwnedUntitled .
    ```
    To identify recognised FRA titles:
    ```sparql
    ?holding jansutra:landType jansutra:ForestLand ;
             jansutra:tenureType jansutra:OwnedTitled ;
             jansutra:hasTitleDeed true .
    ```

---

## Properties

| Property | Type | Range | Required | Notes |
|----------|------|-------|---------|-------|
| `jansutra:areaInHectares` | Datatype | `xsd:decimal` | Yes (minCount 1) | SHACL: ≥ 0, < 500 (flags implausible values) |
| `jansutra:landType` | Object | `LandTypeScheme` concept | Yes (minCount 1) | |
| `jansutra:tenureType` | Object | `TenureTypeScheme` concept | Yes (minCount 1) | |
| `jansutra:hasTitleDeed` | Datatype | `xsd:boolean` | No | Registered title exists |
| `jansutra:khasraNumber` | Datatype | `xsd:string` | No | Revenue survey plot number (state land registry cross-reference) |
| `jansutra:holdingLocatedIn` | Object | `AdministrativeUnit` | No | Village where parcel is located; may differ from citizen's residence |

---

## The khasra number

`jansutra:khasraNumber` stores the plot identifier from the state Revenue Department's Record of Rights (RoR). In Jharkhand, this is the khasra number in the Khatiyan register. In other states it may be called survey number, khata number, or dag number.

This field is the primary cross-reference key for joining Jansutra land records with:
- DILRMP (Digital India Land Records Modernisation Programme) — `https://dilrmp.gov.in`
- State revenue portals (Jharbhoomi, Bhoomi, Bhulekh, etc.)
- MoTA's FRA individual title dashboard

---

## Source file

```json
--8<-- "ontology/land.jsonld"
```
