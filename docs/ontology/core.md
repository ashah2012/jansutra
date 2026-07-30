# Core Module

**File:** `ontology/core.jsonld`

The core module defines the `Citizen` class, the abstract `VulnerabilityDimension` superclass for all domain records, and the object properties that link them. It does not model any specific socioeconomic dimension — it is the structural backbone the other six modules attach to.

---

## Classes

### `jansutra:VulnerabilityDimension`

Abstract superclass for all point-in-time socioeconomic domain records.

- All domain records (`SocialRecord`, `EconomicRecord`, `LandHolding`, `HealthRecord`, `ServiceAccessRecord`) are `rdfs:subClassOf` this class.
- Annotated `dpv:hasPersonalDataCategory dpv:SensitivePersonalData` at the class level, since all subclass instances carry sensitive data.
- Carries two mandatory provenance properties (see below).

### `jansutra:Citizen`

A resident of India identified by an opaque UUID URI.

- `rdfs:subClassOf schema:Person`
- **No Aadhaar number stored.** URI pattern: `citizen:<uuid4>` (e.g., `citizen:f7a3d2b1-4e89-4c56-a123-9b0c12de3f45`)
- Links to all domain records via functional object properties (one record per domain per citizen).

---

## Object properties

| Property | Domain | Range | Functional | Notes |
|----------|--------|-------|-----------|-------|
| `jansutra:residesIn` | `Citizen` | `AdministrativeUnit` | No | Primary residence; minCount 1 |
| `jansutra:hasEconomicRecord` | `Citizen` | `EconomicRecord` | Yes | At most one per citizen |
| `jansutra:hasSocialRecord` | `Citizen` | `SocialRecord` | Yes | |
| `jansutra:hasLandHolding` | `Citizen` | `LandHolding` | No | Multiple parcels allowed |
| `jansutra:hasHealthRecord` | `Citizen` | `HealthRecord` | Yes | |
| `jansutra:hasServiceAccessRecord` | `Citizen` | `ServiceAccessRecord` | Yes | |

---

## Datatype properties

| Property | Domain | Range | Notes |
|----------|--------|-------|-------|
| `jansutra:surveyYear` | `VulnerabilityDimension` | `xsd:gYear` | Year data collected; required on every domain record |
| `jansutra:dataSource` | `VulnerabilityDimension` | `xsd:string` | Survey/registry name (e.g., `"SECC-2026"`) |

---

## Source file

```json
--8<-- "ontology/core.jsonld"
```
