# Health Module

**File:** `ontology/health.jsonld`

!!! warning "Not a clinical health record"
    The health module captures **welfare eligibility dimensions only** — disability status, health insurance coverage, and child/maternal indicators used for ICDS and NHM targeting. It does not store diagnoses, prescriptions, treatment history, or clinical measurements.

---

## Class: `jansutra:HealthRecord`

`rdfs:subClassOf jansutra:VulnerabilityDimension`

Inherits `surveyYear` and `dataSource`. Linked from `jansutra:Citizen` via the functional property `jansutra:hasHealthRecord`.

---

## SKOS scheme

### `jansutra:DisabilityTypeScheme`

21 specified disability categories under the Rights of Persons with Disabilities (RPWD) Act 2016, consolidated into 8 practical categories for welfare targeting.

| URI | Notation | Label | RPWD 2016 basis |
|-----|----------|-------|----------------|
| `jansutra:NoDisability` | `NONE` | No Disability | — |
| `jansutra:VisualImpairment` | `VIS` | Visual Impairment | Blindness, low vision |
| `jansutra:HearingImpairment` | `HEAR` | Hearing Impairment | Deaf, hard of hearing |
| `jansutra:LocomotorImpairment` | `LOCO` | Locomotor Impairment | Cerebral palsy, leprosy-cured, dwarfism, acid attack victims, muscular dystrophy |
| `jansutra:IntellectualDisability` | `INTEL` | Intellectual Disability | Autism, specific learning disabilities, intellectual disability |
| `jansutra:MentalIllness` | `MENTAL` | Mental Illness | Mental illness |
| `jansutra:MultipleDisabilities` | `MULTI` | Multiple Disabilities | Two or more of the above |
| `jansutra:OtherDisability` | `OTHER` | Other Disability | Any of the remaining RPWD categories |

---

## Properties

| Property | Type | Range | Required | Notes |
|----------|------|-------|---------|-------|
| `jansutra:hasDisability` | Datatype | `xsd:boolean` | No | If `true`, `disabilityType` must be present (SPARQL constraint) |
| `jansutra:disabilityType` | Object | `DisabilityTypeScheme` concept | Conditional | Required when `hasDisability = true` |
| `jansutra:disabilityBenchmark` | Datatype | `xsd:decimal` | No | 0–100%; ≥40% qualifies for most RPWD benefits |
| `jansutra:hasHealthInsurance` | Datatype | `xsd:boolean` | No | PM-JAY / Ayushman Bharat or private insurance |
| `jansutra:isPMAYBeneficiary` | Datatype | `xsd:boolean` | No | Pradhan Mantri Awaas Yojana beneficiary |
| `jansutra:isPregnantOrLactating` | Datatype | `xsd:boolean` | No | At time of survey; triggers PMMVY and ICDS eligibility |
| `jansutra:childrenUnder5` | Datatype | `xsd:nonNegativeInteger` | No | Primary ICDS targeting criterion; SHACL: ≤ 10 |

---

## The disability co-constraint

The health SHACL shape includes a SPARQL-based co-constraint:

> If `jansutra:hasDisability true` is present, then `jansutra:disabilityType` must also be present.

This is implemented in `shapes/health.shacl.ttl` as a `sh:sparql` constraint, since SHACL's standard property shapes cannot express cross-property conditional logic. The constraint fires only on `HealthRecord` instances where `hasDisability = true`.

---

## The 40% disability benchmark

`jansutra:disabilityBenchmark` records the assessed degree of disability as a percentage. The 40% threshold is the RPWD Act 2016's minimum for most benefits (disability certificate, reservation, welfare allowances). Values below 40% may indicate partial disability not qualifying for benefits — but the field is still useful for program planning (e.g., assistive device distribution).

---

## Source file

```json
--8<-- "ontology/health.jsonld"
```
