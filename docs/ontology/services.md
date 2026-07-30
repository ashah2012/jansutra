# Services Module

**File:** `ontology/services.jsonld`

The services module records a household's access to eleven categories of basic public services — the infrastructure and facility gaps that determine whether government schemes reach their beneficiaries. Each access claim carries a quality rating and, for proximity-based services, a walking distance.

---

## Classes

### `jansutra:ServiceAccessRecord`

`rdfs:subClassOf jansutra:VulnerabilityDimension`

Container for all of a citizen's service access claims. Linked from `jansutra:Citizen` via `jansutra:hasServiceAccessRecord`. Inherits `surveyYear` and `dataSource`.

### `jansutra:ServiceAccess`

An individual service access claim — the tuple (serviceType, quality, distance). A citizen has one `ServiceAccessRecord` containing zero or more `ServiceAccess` instances.

---

## SKOS schemes

### `jansutra:ServiceTypeScheme`

Eleven service types aligned with India's flagship infrastructure schemes.

| URI | Notation | Label | Scheme |
|-----|----------|-------|--------|
| `jansutra:PipedWater` | `WATER-PIPE` | Piped Water | Har Ghar Jal / Jal Jeevan Mission |
| `jansutra:SafeWaterSource` | `WATER-SAFE` | Safe Water Source | Handpump, borewell, protected well (`skos:broader PipedWater`) |
| `jansutra:GridElectricity` | `ELEC` | Grid Electricity | SAUBHAGYA / RGGVY |
| `jansutra:HouseholdToilet` | `TOILET` | Household Toilet | Swachh Bharat Mission (Grameen / Urban) |
| `jansutra:PavedRoad` | `ROAD` | Paved Road | PMGSY (all-weather road) |
| `jansutra:BroadbandInternet` | `INTERNET` | Broadband Internet | BharatNet / PM-WANI / 4G mobile |
| `jansutra:PrimarySchoolAccess` | `SCH-P` | Primary School | Within 1 km (RTE Act) |
| `jansutra:SecondarySchoolAccess` | `SCH-S` | Secondary School | Within 5 km |
| `jansutra:PHCAccess` | `PHC` | Primary Health Centre | Within 10 km (NHM norm) |
| `jansutra:AnganwadiAccess` | `AWC` | Anganwadi Centre | Within 1 km (ICDS / PM-POSHAN) |
| `jansutra:BankBranchAccess` | `BANK` | Bank / Business Correspondent | Within 5 km (financial inclusion) |

!!! note "SafeWaterSource broader than PipedWater"
    `jansutra:SafeWaterSource skos:broader jansutra:PipedWater` — it is a broader category: any protected, non-surface water source qualifies (borewell, handpump, protected well), not just piped connections. The vulnerability query targets both: `FILTER(?wt IN (jansutra:PipedWater, jansutra:SafeWaterSource))`.

### `jansutra:AccessQualityScheme`

Reliability of service delivery.

| URI | Notation | Label | Definition |
|-----|----------|-------|-----------|
| `jansutra:Reliable` | `REL` | Reliable | ≥ 20 hours/day for utilities; year-round for facilities |
| `jansutra:Intermittent` | `INT` | Intermittent | Seasonal availability or frequent outages |
| `jansutra:Absent` | `ABS` | Absent | No functional access |

---

## Properties

| Property | Domain | Type | Range | Required | Notes |
|----------|--------|------|-------|---------|-------|
| `jansutra:hasServiceAccess` | `ServiceAccessRecord` | Object | `ServiceAccess` | No | Multi-valued |
| `jansutra:accessType` | `ServiceAccess` | Object | `ServiceTypeScheme` concept | Yes (minCount 1) | |
| `jansutra:accessQuality` | `ServiceAccess` | Object | `AccessQualityScheme` concept | Yes (minCount 1) | |
| `jansutra:distanceInKm` | `ServiceAccess` | Datatype | `xsd:decimal` | No | Walking distance to nearest facility; SHACL: < 200 |

---

## Reading service access records

A complete service access entry in JSON-LD looks like:

```json
{
  "@id": "citizen:f7a3d2b1-.../services/phc",
  "@type": "jansutra:ServiceAccess",
  "jansutra:accessType": {"@id": "jansutra:PHCAccess"},
  "jansutra:accessQuality": {"@id": "jansutra:Absent"},
  "jansutra:distanceInKm": {"@type": "xsd:decimal", "@value": "18.5"}
}
```

`distanceInKm` is only meaningful for proximity-based services (PHC, schools, road, water source, bank). It is omitted for services like toilet or electricity that are either present at the household or absent.

---

## Source file

```json
--8<-- "ontology/services.jsonld"
```
