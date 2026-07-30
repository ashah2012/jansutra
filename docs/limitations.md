# Limitations

## What Jansutra models

Jansutra models **seven welfare-eligibility dimensions** at a **point in time**:

1. Social identity (caste, gender, religion, language)
2. Economic status (income, poverty classification, occupation)
3. Geographic location (administrative hierarchy, PESA/remote flags)
4. Land holding (area, type, tenure, FRA recognition)
5. Health status (disability, insurance, maternal/child indicators)
6. Service access (11 infrastructure and facility types)
7. Provenance (survey year and source for every record)

Every record carries a `surveyYear` — it captures a snapshot, not a live state.

---

## What Jansutra is not

**Not a citizen registry.** No name, address, phone number, Aadhaar number, or biometric reference is stored. A Jansutra citizen URI is an opaque UUID. It cannot be used to identify or contact an individual without an external mapping table the deployer maintains separately.

**Not a clinical health record.** The health module captures welfare-eligibility markers only: disability classification, insurance status, children under 5, pregnant/lactating. It does not store diagnoses, prescriptions, lab results, treatment history, or clinical measurements. For clinical data, see the NHA's Ayushman Bharat Digital Mission (ABDM) FHIR-based health records standard.

**Not a real-time system.** Data is point-in-time, not live. A citizen's poverty status may change between surveys. A road may be constructed after the survey date. The `surveyYear` property exists precisely to make this staleness explicit.

**Not a sub-caste registry.** `CasteCategoryScheme` captures constitutional categories (SC, ST, OBC-C, OBC-S, EWS, GEN, NT, DNT) — not jati (sub-caste) enumeration. Sub-caste data is excluded by design: it is the most politically and socially sensitive field in Indian welfare data and is not required for program eligibility targeting at the constitutional category level.

**Not a land transaction system.** `LandHolding` records land facts at survey time. Mutations (transfers, partitions, sales), encumbrances, and disputes require integration with the state revenue department's live RoR system (DILRMP), which is outside Jansutra's scope.

**Not a payments platform.** Jansutra cannot execute DBT transfers, issue ration cards, or trigger scheme enrollment. It identifies eligible cohorts; delivery happens through ministry systems.

---

## Data quality dependencies

The ontology is only as good as the surveys that feed it.

| Source | Problem | Impact |
|--------|---------|--------|
| SECC 2011 | 15 years old | Poverty status, occupation, MGNREGA data are stale for an estimated 20–25% of households |
| NFHS-5/6 | District-level aggregate, not individual | `childrenUnder5` and `isPregnantOrLactating` from NFHS cannot be attached to individual citizens; only a state HMIS or survey provides individual-level data |
| LGD codes | ~6% spelling inconsistency across ministry datasets | Always join on the integer LGD code, never on name strings |
| State land registries | Digitisation varies by state; Jharkhand (DILRMP), Karnataka (Bhoomi), and AP are well-digitised; UP and Bihar have significant paper-record backlogs | `khasraNumber` cross-references will fail where records are not digitised |
| DISHA / JJM dashboards | Habitation-level, not household-level | `distanceInKm` values from DISHA are approximate; household-level service access requires primary survey |

---

## Scale

`rdflib` in-memory loading is appropriate for:
- Development and testing
- District or block-level analysis datasets (tens of thousands of citizens, millions of triples)
- SPARQL queries on single files or small multi-file loads

For national-scale citizen data (hundreds of millions of individuals → billions of triples), a dedicated triple store is required:
- **Apache Jena Fuseki** (open source, Java)
- **Virtuoso Open Source** (open source, C)
- **Amazon Neptune** (managed, AWS)
- **Stardog** (commercial)

The ontology and SHACL shapes are compatible with any standards-compliant triple store. The Python tools (`validate.py`, `query.py`) would need to be rewritten as SPARQL client calls against the triple store's HTTP endpoint.

---

## Privacy boundary

`dpv:SensitivePersonalData` annotations on caste, religion, disability, and health properties are **metadata declarations**, not enforcement mechanisms. They make compliance requirements discoverable in the schema. They do not:
- Enforce access control (who can read which properties)
- Implement consent management (tracking which citizens consented to which data uses)
- Ensure data residency (where data is stored)
- Encrypt sensitive fields

All of these must be implemented by the **deploying system**. Jansutra specifies what is sensitive; the infrastructure around it is responsible for protecting it.

---

## Current state

`examples/household-001.jsonld` is an illustrative data file — one carefully constructed citizen profile demonstrating all seven modules. SPARQL queries against this file return single-row results.

The design target is a nationally-populated dataset where the vulnerability query returns millions of households and the poverty-by-district query produces a 640 × 8 matrix (640 districts × 8 caste categories). That dataset does not exist yet. Jansutra defines the vocabulary it would use.
