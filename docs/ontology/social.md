# Social Module

**File:** `ontology/social.jsonld`

The social module captures constitutional and Census-defined social identity dimensions: caste category, gender identity, religion, and mother tongue. All properties in this module are annotated `dpv:SensitivePersonalData` per the DPDP Act 2023 Schedule I.

---

## Class: `jansutra:SocialRecord`

`rdfs:subClassOf jansutra:VulnerabilityDimension`

Inherits `surveyYear` and `dataSource` from `VulnerabilityDimension`. Linked from `jansutra:Citizen` via the functional property `jansutra:hasSocialRecord`.

---

## SKOS schemes

### `jansutra:CasteCategoryScheme`

Constitutional and administrative caste categories. Covers Articles 341 (SC), 342 (ST), OBC notification (Mandal Commission + state lists), EWS (103rd Amendment 2019), and the NT/DNT categories recognised by the Renke Commission (2008).

!!! note
    This scheme records **constitutional category only** — not jati (sub-caste) enumeration. Sub-caste data is excluded by design: it is the most sensitive field in any Indian welfare dataset and is not required for program eligibility targeting.

| URI | Notation | Label | Legal basis |
|-----|----------|-------|-------------|
| `jansutra:SC` | `SC` | Scheduled Caste | Article 341, Constitution of India |
| `jansutra:ST` | `ST` | Scheduled Tribe | Article 342 |
| `jansutra:OBCCentral` | `OBC-C` | OBC (Central List) | Mandal Commission / National OBC list |
| `jansutra:OBCState` | `OBC-S` | OBC (State List) | State government OBC notifications |
| `jansutra:EWS` | `EWS` | Economically Weaker Section | 103rd Constitutional Amendment, 2019 |
| `jansutra:General` | `GEN` | General / Unreserved | — |
| `jansutra:NT` | `NT` | Nomadic Tribe | Renke Commission 2008 |
| `jansutra:DNT` | `DNT` | De-Notified Tribe | Renke Commission 2008 (broader: NT) |

### `jansutra:GenderIdentityScheme`

Aligned with Census 2011 gender codes and the Supreme Court's NALSA v. Union of India (2014) recognition of third gender.

| URI | Notation | Label |
|-----|----------|-------|
| `jansutra:Male` | `M` | Male |
| `jansutra:Female` | `F` | Female |
| `jansutra:ThirdGender` | `T` | Third Gender |
| `jansutra:PreferNotToDisclose` | `X` | Prefer not to disclose |

### `jansutra:ReligionScheme`

Census 2011 religion codes, used for scheme eligibility (e.g., minority welfare programs).

| URI | Notation | Census 2011 code |
|-----|----------|-----------------|
| `jansutra:Hindu` | `1` | 1 |
| `jansutra:Muslim` | `2` | 2 |
| `jansutra:Christian` | `3` | 3 |
| `jansutra:Sikh` | `4` | 4 |
| `jansutra:Buddhist` | `5` | 5 |
| `jansutra:Jain` | `6` | 6 |
| `jansutra:OtherReligion` | `7` | 7 |
| `jansutra:NoReligion` | `9` | 9 |

---

## Properties

| Property | Type | Range | Required | Notes |
|----------|------|-------|---------|-------|
| `jansutra:casteCategory` | Object | `CasteCategoryScheme` concept | Yes (minCount 1) | `dpv:SensitivePersonalData` |
| `jansutra:genderIdentity` | Object | `GenderIdentityScheme` concept | Yes (minCount 1) | `dpv:SensitivePersonalData` |
| `jansutra:religion` | Object | `ReligionScheme` concept | No | `dpv:SensitivePersonalData` |
| `jansutra:motherTongue` | Datatype | `xsd:language` (BCP47) | No | e.g., `"ho"` for Ho language |

---

## Source file

```json
--8<-- "ontology/social.jsonld"
```
