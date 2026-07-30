# Ontology Reference

Jansutra's ontology is split into seven domain modules, each a separate JSON-LD file. They share a common context file and are linked through the `jansutra:Citizen` class in `core.jsonld`.

## Module summary

| Module | File | Key class | SKOS schemes | Properties |
|--------|------|-----------|--------------|-----------|
| [Core](core.md) | `core.jsonld` | `Citizen`, `VulnerabilityDimension` | — | 8 |
| [Social](social.md) | `social.jsonld` | `SocialRecord` | CasteCategoryScheme · GenderIdentityScheme · ReligionScheme | 4 |
| [Economic](economic.md) | `economic.jsonld` | `EconomicRecord` | PovertyStatusScheme · OccupationTypeScheme | 6 |
| [Geography](geography.md) | `geography.jsonld` | `AdministrativeUnit` | AdminLevelScheme | 5 |
| [Land](land.md) | `land.jsonld` | `LandHolding` | LandTypeScheme · TenureTypeScheme | 6 |
| [Health](health.md) | `health.jsonld` | `HealthRecord` | DisabilityTypeScheme | 6 |
| [Services](services.md) | `services.jsonld` | `ServiceAccessRecord`, `ServiceAccess` | ServiceTypeScheme · AccessQualityScheme | 5 |

---

## The `VulnerabilityDimension` superclass

Every domain record class — `SocialRecord`, `EconomicRecord`, `LandHolding`, `HealthRecord`, `ServiceAccessRecord` — is declared `rdfs:subClassOf jansutra:VulnerabilityDimension`.

`VulnerabilityDimension` requires two provenance properties on every instance:

| Property | Datatype | Purpose |
|----------|----------|---------|
| `jansutra:surveyYear` | `xsd:gYear` | Year data was collected (e.g., `"2026"^^xsd:gYear`) |
| `jansutra:dataSource` | `xsd:string` | Survey or registry name (e.g., `"SECC-2026"`, `"NFHS-6"`) |

This ensures every record carries an explicit vintage — critical for a model whose primary flaw-to-fix is 15-year-old data.

---

## The `Citizen` class

`jansutra:Citizen` is a `rdfs:subClassOf schema:Person`. Its URI follows the pattern `citizen:<uuid>` — an opaque UUID with no embedded identity information.

| Property | Range | Card. | Notes |
|----------|-------|-------|-------|
| `jansutra:residesIn` | `AdministrativeUnit` | ≥1 | Primary residence village/ward |
| `jansutra:hasSocialRecord` | `SocialRecord` | 0–1 | Functional (one per citizen) |
| `jansutra:hasEconomicRecord` | `EconomicRecord` | 0–1 | Functional |
| `jansutra:hasLandHolding` | `LandHolding` | 0–* | Multi-valued; one per parcel |
| `jansutra:hasHealthRecord` | `HealthRecord` | 0–1 | Functional |
| `jansutra:hasServiceAccessRecord` | `ServiceAccessRecord` | 0–1 | Functional |

---

## The shared context file

All modules reference `ontology/context/jansutra.context.jsonld` as their `@context`. This file centralises all prefix-to-IRI mappings so namespace declarations are not duplicated across modules.

```json
{ "@context": "../ontology/context/jansutra.context.jsonld" }
```

Instance data files (e.g., `examples/household-001.jsonld`) also reference this context directly:

```json
{ "@context": "../ontology/context/jansutra.context.jsonld" }
```
