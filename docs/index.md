# Jansutra — जनसूत्र

**Citizen Thread** — a federated, privacy-by-design semantic data model for India's citizen socioeconomic data.

India's welfare state has a data problem. The last comprehensive socioeconomic survey (SECC 2011) is fifteen years old. Ministries run separate beneficiary registers that cannot be joined. A Scheduled Tribe woman in a PESA village with no piped water, no PHC within 20 km, and an FRA forest title she cannot leverage for credit — every deprivation flag set — is invisible to the systems meant to help her.

Jansutra models multi-dimensional vulnerability as a **linked, federated OWL ontology** so that intersectional SPARQL queries across caste, income, land, health, and service access become a few lines of code.

---

## The core use case in one query

```sparql
SELECT ?citizen ?districtLabel ?povertyStatus ?phcDistanceKm
WHERE {
  ?citizen a jansutra:Citizen ;
           jansutra:residesIn ?village ;
           jansutra:hasSocialRecord ?social .
  ?social jansutra:casteCategory jansutra:ST .
  ?village jansutra:isRemoteArea true .
  ?village jansutra:hasParentUnit* ?district .
  ?district jansutra:adminLevel jansutra:District ;
            skos:prefLabel ?districtLabel .
  FILTER(LANG(?districtLabel) = "en")

  FILTER NOT EXISTS {
    ?citizen jansutra:hasServiceAccessRecord ?services .
    ?services jansutra:hasServiceAccess ?waterAccess .
    ?waterAccess jansutra:accessType ?wt ; jansutra:accessQuality ?wq .
    FILTER(?wt IN (jansutra:PipedWater, jansutra:SafeWaterSource))
    FILTER(?wq IN (jansutra:Reliable, jansutra:Intermittent))
  }
}
```

This query identifies **ST citizens in remote/PESA areas without functional water access** — the cohort the current fragmented data system cannot find.

---

## Quickstart

```bash
pip install rdflib pyshacl rich

# Validate a data file against all SHACL shapes
python tools/validate.py examples/household-001.jsonld

# Run the intersectional vulnerability query
python tools/query.py sparql/vulnerability-query.sparql examples/household-001.jsonld

# Convert all ontology JSON-LD files to Turtle
python tools/convert.py
```

---

## Seven ontology modules

| Module | Domain | Key SKOS schemes |
|--------|--------|-----------------|
| [Core](ontology/core.md) | `Citizen` identity, record links | — |
| [Social](ontology/social.md) | Caste, gender, religion, language | CasteCategory · GenderIdentity · Religion |
| [Economic](ontology/economic.md) | Income, poverty, occupation | PovertyStatus · OccupationType |
| [Geography](ontology/geography.md) | Administrative hierarchy, LGD codes | AdminLevel |
| [Land](ontology/land.md) | Land holdings, FRA titles, tenure | LandType · TenureType |
| [Health](ontology/health.md) | Disability (RPWD 2016), insurance, children | DisabilityType |
| [Services](ontology/services.md) | Water, electricity, road, PHC, school | ServiceType · AccessQuality |

---

## Design principles

**No Aadhaar** · Citizens are identified by opaque UUID URIs only. No name, no Aadhaar number, no biometric reference is stored in the model.

**Federated modules** · Each socioeconomic domain is a separate JSON-LD file. No single file contains the full citizen profile. Modules are linked but independently deployable.

**Privacy by design** · Caste, religion, gender, and disability properties carry `dpv:SensitivePersonalData` annotations per the Digital Personal Data Protection Act 2023.

**LGD-anchored geography** · Every `AdministrativeUnit` carries a mandatory MoPR Local Government Directory code — India's canonical administrative interoperability key.

**SHACL-enforced** · Structural and taxonomic constraints are machine-checkable. A data file that fails `validate.py` is not valid Jansutra data.
