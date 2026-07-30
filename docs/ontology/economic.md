# Economic Module

**File:** `ontology/economic.jsonld`

The economic module captures household income, poverty classification, livelihood type, and consumption expenditure — the primary determinants of welfare scheme eligibility.

---

## Class: `jansutra:EconomicRecord`

`rdfs:subClassOf jansutra:VulnerabilityDimension`

Inherits `surveyYear` and `dataSource`. Linked from `jansutra:Citizen` via the functional property `jansutra:hasEconomicRecord`.

---

## SKOS schemes

### `jansutra:PovertyStatusScheme`

Based on the National Food Security Act 2013 (NFSA) and PMAY-G eligibility classifications.

| URI | Notation | Label | Notes |
|-----|----------|-------|-------|
| `jansutra:BPL` | `BPL` | Below Poverty Line | Top concept; NFSA Priority Household |
| `jansutra:APL` | `APL` | Above Poverty Line | Top concept |
| `jansutra:Antyodaya` | `AAY` | Antyodaya Anna Yojana | `skos:broader jansutra:BPL`; destitute / poorest of poor |

!!! note
    `jansutra:Antyodaya` has `skos:broader jansutra:BPL` — it is a specialisation of BPL, not a separate category. SPARQL queries targeting all BPL households should use `FILTER(?ps IN (jansutra:BPL, jansutra:Antyodaya))` or traverse the broader/narrower chain.

### `jansutra:OccupationTypeScheme`

Livelihood categories based on SECC 2011 primary occupation classification (main earner of household).

| URI | Notation | Label | Notes |
|-----|----------|-------|-------|
| `jansutra:AgriculturalLabourer` | `AGR-LAB` | Agricultural Labourer | Wage labour on others' land |
| `jansutra:MarginalFarmer` | `FARM-SM` | Marginal Farmer | Owner-cultivator, ≤2 ha |
| `jansutra:MediumLargeFarmer` | `FARM-LG` | Medium/Large Farmer | Owner-cultivator, >2 ha |
| `jansutra:ManualLabourer` | `MAN-LAB` | Manual Labourer (non-agri) | Construction, loading, etc. |
| `jansutra:SalariedEmployee` | `SALARIED` | Salaried Employee | Regular wage/salary |
| `jansutra:SelfEmployed` | `SELF-EMP` | Self-Employed | Petty trade, micro-enterprise |
| `jansutra:Unemployed` | `UNEMP` | Unemployed | Working-age, not student |

---

## Properties

| Property | Type | Range | Required | Notes |
|----------|------|-------|---------|-------|
| `jansutra:annualHouseholdIncome` | Datatype | `xsd:decimal` (INR) | No | Self-reported; SHACL: ≥ 0 |
| `jansutra:monthlyPerCapitaExpenditure` | Datatype | `xsd:decimal` (INR) | No | MPCE — welfare economics proxy |
| `jansutra:povertyStatus` | Object | `PovertyStatusScheme` concept | No | SHACL: scheme membership enforced |
| `jansutra:occupationType` | Object | `OccupationTypeScheme` concept | No | Main earner only |
| `jansutra:householdSize` | Datatype | `xsd:positiveInteger` | No | SHACL: ≤ 30 |
| `jansutra:hasMGNREGACard` | Datatype | `xsd:boolean` | No | Proxy for rural wage dependency |

---

## Source file

```json
--8<-- "ontology/economic.jsonld"
```
