# Data Collection

!!! info "Jansutra is a data model, not a collection platform"
    These pages describe **recommended pathways** for generating conformant Jansutra JSON-LD from India's existing data collection programs. The ontology defines the vocabulary; the ETL pipelines that populate it are the deployer's responsibility.

---

## Collection points by module

### Geography module — populate first

The geography module is the foundation. Every other module references `AdministrativeUnit` via `residesIn` or `holdingLocatedIn`. Populate it before any other module.

**Source:** MoPR Local Government Directory (LGD)
**URL:** Available as bulk CSV download from the MoPR portal

**Key mapping:**

| LGD field | Jansutra property |
|-----------|------------------|
| LGD code (integer) | `jansutra:lgdCode` |
| Unit name (English) | `skos:prefLabel` (lang `"en"`) |
| Unit name (Hindi) | `skos:prefLabel` (lang `"hi"`) |
| Unit type (State/District/Sub-district/Village) | `jansutra:adminLevel` → `jansutra:StateUT` / `jansutra:District` / `jansutra:SubDistrict` / `jansutra:VillageWard` |
| Parent LGD code | `jansutra:hasParentUnit` → URI of parent unit |

**URI pattern:**
```
geo:village/jharkhand/west-singhbhum/chakradharpur/bandgaon
```
Constructed from the state slug + parent chain; the LGD code is stored as a literal (`lgdCode`), not embedded in the URI.

**PESA and remote flags:** Must be layered from MoTA's list of Fifth Schedule villages (for `isPESAArea`) and PMGSY's unconnected habitation list (for `isRemoteArea`). Both are publicly available datasets joinable by LGD code.

---

### Social module

**Primary source:** Socio-Economic and Caste Census (SECC)
- Most recent completed: SECC 2011 (Ministry of Rural Development)
- Next: Census-2026 Caste Enumeration (planned)

**Key mapping:**

| SECC / Census field | Jansutra property |
|--------------------|------------------|
| Social category (SC/ST/OBC/GEN) | `jansutra:casteCategory` → SKOS concept |
| Gender | `jansutra:genderIdentity` → SKOS concept |
| Religion code | `jansutra:religion` → SKOS concept |
| Mother tongue (Census schedule) | `jansutra:motherTongue` (BCP47 tag) |

**Privacy requirement:** SECC unit-level microdata is restricted. Any real deployment requires a data sharing agreement with MoRD and DPDP Act consent framework implementation before individual-level records can be processed.

---

### Economic module

**Primary sources:**

| Source | Fields | Frequency |
|--------|--------|-----------|
| SECC | povertyStatus, occupationType, householdSize, hasMGNREGACard | Decennial |
| NSO HCES (Household Consumption Expenditure Survey) | monthlyPerCapitaExpenditure | ~5 years (last: 2022–23) |
| PM-GKY / MGNREGA MIS | hasMGNREGACard (real-time) | Continuous |

**Key mapping:**

| Source field | Jansutra property |
|-------------|------------------|
| BPL/APL/AAY classification | `jansutra:povertyStatus` |
| Primary livelihood (SECC category) | `jansutra:occupationType` |
| Household member count | `jansutra:householdSize` |
| Job card issued (Y/N) | `jansutra:hasMGNREGACard` |
| MPCE (HCES unit record) | `jansutra:monthlyPerCapitaExpenditure` |

**Note on HCES:** The NSO HCES provides household-level consumption data including unit records. The 2022–23 HCES data is the most recent available. MPCE from HCES can be mapped to a Jansutra record using LGD village code as the geographic join key.

---

### Land module

**Primary sources:**

| Source | Fields | Maintained by |
|--------|--------|--------------|
| DILRMP / State RoR | khasraNumber, areaInHectares, tenureType | State revenue departments |
| MoTA FRA dashboard | landType=ForestLand, hasTitleDeed, OwnedTitled vs OwnedUntitled | Ministry of Tribal Affairs |
| PMFBY / e-Fard | irrigated/dryland classification | State agriculture departments |

**Key mapping:**

| Source field | Jansutra property |
|-------------|------------------|
| Survey/Khasra/Dag number | `jansutra:khasraNumber` |
| Area (acres → hectares) | `jansutra:areaInHectares` (1 acre = 0.4047 ha) |
| Land use type | `jansutra:landType` → SKOS concept |
| Ownership status | `jansutra:tenureType` → SKOS concept |
| Title deed registered | `jansutra:hasTitleDeed` |
| Village (LGD code) | `jansutra:holdingLocatedIn` → AdministrativeUnit URI |

**FRA title identification:**

- MoTA's FRA individual title register uses patta number as primary key. The `khasraNumber` from the state revenue record is the join field to Jansutra's land module.
- `OwnedUntitled` tenure with `landType=ForestLand` identifies un-recognised customary claims — potential FRA filing candidates.

---

### Health module

**Primary sources:**

| Source | Fields | Frequency |
|--------|--------|-----------|
| NFHS (National Family Health Survey) | childrenUnder5, isPregnantOrLactating, disability indicators | ~5 years (NFHS-6: 2023–24) |
| NHA PM-JAY database | isPMAYBeneficiary, hasHealthInsurance | Continuous |
| RPWD district registry | hasDisability, disabilityType, disabilityBenchmark | On certificate issuance |

!!! warning "NFHS is district-aggregate"
    NFHS unit-level microdata is available for research use but covers a sample, not all households. For population-level individual disability data, the source is the RPWD district certificate registry and the Unique Disability ID (UDID) portal (`swavlambancard.gov.in`). UDID records include disability type and benchmark percentage — direct mapping to Jansutra's health module.

**Key mapping:**

| Source field | Jansutra property |
|-------------|------------------|
| Disability certificate (Y/N) | `jansutra:hasDisability` |
| RPWD disability category | `jansutra:disabilityType` → SKOS concept |
| Benchmark percentage | `jansutra:disabilityBenchmark` |
| PM-JAY beneficiary (Y/N) | `jansutra:isPMAYBeneficiary`, `jansutra:hasHealthInsurance` |
| Pregnant/lactating at survey date | `jansutra:isPregnantOrLactating` |
| Children aged 0–4 in household | `jansutra:childrenUnder5` |

---

### Services module

**Primary sources:**

| Source | Service types | Format |
|--------|-------------|--------|
| DISHA Dashboard (MoRD) | All infrastructure | Portal export / API |
| Jal Jeevan Mission portal | PipedWater, SafeWaterSource | Dashboard API |
| SAUBHAGYA portal (MoP) | GridElectricity | Dashboard |
| SBM-G ODF verification (MoJS) | HouseholdToilet | Portal |
| PMGSY MIS (MoRD) | PavedRoad, distance | GIS / MIS export |
| BharatNet / TRAI | BroadbandInternet | Coverage maps |
| District HMIS (MoHFW) | PHCAccess, distanceInKm | State NHM data |
| UDISE+ (MoE) | PrimarySchoolAccess, SecondarySchoolAccess | Annual census |

**Key mapping:**

| Source field | Jansutra property |
|-------------|------------------|
| Water connection type | `jansutra:accessType` → `PipedWater` or `SafeWaterSource` |
| Connection functional (Y/N/seasonal) | `jansutra:accessQuality` → `Reliable` / `Intermittent` / `Absent` |
| Distance to water source (km) | `jansutra:distanceInKm` |
| Electricity connection (Y/N) | `accessType=GridElectricity`, quality based on hours/day |
| ODF village status | `accessType=HouseholdToilet`, quality=`Reliable` if ODF+ |
| Distance to all-weather road | `accessType=PavedRoad`, `distanceInKm` |
| PHC within 10 km | `accessType=PHCAccess`, quality=`Reliable`/`Absent`, `distanceInKm` |

---

## ETL patterns

### CSV to JSON-LD

For each module, the ETL script:
1. Reads a CSV with one row per citizen (or per parcel, for land)
2. Maps each column to a Jansutra property using the tables above
3. Generates a citizen UUID for each row (or reuses if a UUID registry exists)
4. Produces a JSON-LD `@graph` array conforming to the module's schema
5. Runs `jansutra-validate` to confirm conformance before ingestion

Example column mapping for a social record CSV:

```python
import uuid, json

def row_to_social_record(row, citizen_uri):
    caste_map = {"SC": "jansutra:SC", "ST": "jansutra:ST", "OBC": "jansutra:OBCCentral", ...}
    gender_map = {"M": "jansutra:Male", "F": "jansutra:Female", "T": "jansutra:ThirdGender"}
    return {
        "@id": f"{citizen_uri}/social",
        "@type": "jansutra:SocialRecord",
        "jansutra:surveyYear": {"@type": "xsd:gYear", "@value": str(row["survey_year"])},
        "jansutra:dataSource": row["data_source"],
        "jansutra:casteCategory": {"@id": caste_map[row["caste_category"]]},
        "jansutra:genderIdentity": {"@id": gender_map[row["gender"]]},
    }
```

### REST API integration

For real-time service access data, ministries expose portal APIs:

```python
import requests

# Jal Jeevan Mission village-level data (illustrative)
resp = requests.get("https://ejalshakti.gov.in/api/village/", params={"lgd": "265432"})
data = resp.json()

service_access = {
    "@id": f"{citizen_uri}/services/water",
    "@type": "jansutra:ServiceAccess",
    "jansutra:accessType": {"@id": "jansutra:PipedWater" if data["piped"] else "jansutra:SafeWaterSource"},
    "jansutra:accessQuality": {"@id": "jansutra:Reliable" if data["functional"] else "jansutra:Absent"},
}
```

---

## Operational requirements for real deployment

Any real deployment collecting actual citizen data requires:

1. **Data sharing agreement** — with the originating ministry (MoRD, MoHFW, MoTA, etc.) before accessing unit-level microdata.

2. **DPDP Act 2023 compliance** — caste, religion, disability, and health data are Sensitive Personal Data under Schedule I. Consent must be obtained, purpose must be specified, and data must be minimised to what is necessary for the stated purpose.

3. **UUID assignment policy** — who generates citizen UUIDs, how they are maintained across survey cycles, and how the UUID ↔ Aadhaar mapping (held externally, not in Jansutra) is secured and audited.

4. **State-level coordination** — land and service access data vary by state registry format. Each state will require a separate ETL configuration.
