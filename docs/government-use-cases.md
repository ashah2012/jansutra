# Government Use Cases

!!! important "Jansutra identifies cohorts — it does not execute transfers"
    Jansutra's role is to answer the question: *which citizens are eligible for this scheme and currently unreached?* The actual transfer — whether cash, ration, or service — remains in the ministry's own DBT or delivery infrastructure. Jansutra stores no Aadhaar number and cannot execute a payment.

    **The workflow:** Jansutra SPARQL query → UUID cohort → Ministry maps UUIDs to Aadhaar-linked beneficiary register (in a controlled external lookup) → DBT/service delivery proceeds normally. Jansutra never becomes an Aadhaar database.

---

## Ministry of Rural Development (MoRD)

### MGNREGA

**Gap:** MGNREGA job cards are issued village-wise, but card holders with the greatest wage-dependency (BPL, no paved road, remote area) are not systematically identified for enhanced entitlements or priority work allocation.

**Jansutra query:**
```sparql
SELECT ?citizen ?village WHERE {
  ?citizen jansutra:hasEconomicRecord ?eco ;
           jansutra:residesIn ?village .
  ?eco jansutra:hasMGNREGACard true ;
       jansutra:povertyStatus jansutra:BPL .
  ?village jansutra:isRemoteArea true .
  FILTER NOT EXISTS {
    ?citizen jansutra:hasServiceAccessRecord ?svc .
    ?svc jansutra:hasServiceAccess ?road .
    ?road jansutra:accessType jansutra:PavedRoad ;
          jansutra:accessQuality ?q .
    FILTER(?q != jansutra:Absent)
  }
}
```

**Value:** Cross-links MGNREGA card holders with remote-area and road-absent flags — primary cohort for PMGSY road work priority and 100-day entitlement fulfilment.

---

### PMAY-G (Pradhan Mantri Awaas Yojana — Gramin)

**Gap:** Beneficiary lists derived from SECC 2011 miss households that crossed into the eligible category after 2011 (migration, household formation, disaster displacement).

**Jansutra query:**
```sparql
SELECT ?citizen ?village WHERE {
  ?citizen jansutra:hasEconomicRecord ?eco ;
           jansutra:residesIn ?village .
  ?eco jansutra:povertyStatus ?ps .
  FILTER(?ps IN (jansutra:BPL, jansutra:Antyodaya))
  ?village jansutra:isPESAArea true .
}
```

**Value:** Identifies BPL citizens in PESA villages — the priority segment for PMAY-G tribal beneficiary lists — from current survey data rather than 15-year-old SECC records.

---

### PMGSY (Pradhan Mantri Gram Sadak Yojana)

**Gap:** Road construction priority is administratively determined (habitation population thresholds) without weighting by the socioeconomic profile of unconnected households.

**Jansutra value:** `PavedRoad` with `Absent` quality + `distanceInKm` enables ranking unconnected habitations by the number of BPL/ST/SC citizens affected. `geo:` URIs with LGD codes map directly to PMGSY's habitation GIS layer.

---

## Ministry of Tribal Affairs (MoTA)

### PESA Act 1996 delivery

**Gap:** PESA gram sabha authority covers ~100,000 villages across nine states, but welfare delivery within PESA areas is not systematically differentiated from non-PESA areas in most ministry MIS systems.

**Jansutra value:** `jansutra:isPESAArea true` on the village `AdministrativeUnit` enables every ministry to extract its PESA sub-population from any intersectional query. No separate PESA registry is needed.

---

### Forest Rights Act (FRA 2006) — title tracking

**Recognised titles:**
```sparql
SELECT ?citizen ?khasra ?areaHa WHERE {
  ?citizen jansutra:hasLandHolding ?land .
  ?land jansutra:landType jansutra:ForestLand ;
        jansutra:tenureType jansutra:OwnedTitled ;
        jansutra:hasTitleDeed true ;
        jansutra:khasraNumber ?khasra ;
        jansutra:areaInHectares ?areaHa .
}
```

**Un-recognised customary claims** (candidates for FRA filing):
```sparql
SELECT ?citizen ?village WHERE {
  ?citizen jansutra:hasLandHolding ?land ;
           jansutra:residesIn ?village ;
           jansutra:hasSocialRecord ?soc .
  ?soc jansutra:casteCategory jansutra:ST .
  ?land jansutra:landType jansutra:ForestLand ;
        jansutra:tenureType jansutra:OwnedUntitled .
}
```

**FRA credit-linkage gap:**
```sparql
SELECT ?citizen WHERE {
  ?citizen jansutra:hasLandHolding ?land ;
           jansutra:hasEconomicRecord ?eco .
  ?land jansutra:landType jansutra:ForestLand ;
        jansutra:tenureType jansutra:OwnedTitled ;
        jansutra:hasTitleDeed true .
  ?eco jansutra:povertyStatus ?ps .
  FILTER(?ps IN (jansutra:BPL, jansutra:Antyodaya))
}
```

**Value:** This last query identifies citizens with recognised FRA titles who are still below the poverty line — a signal that the title has not been converted into agricultural credit (NABARD/KCC) or livelihood support. This is the most actionable post-FRA follow-up dataset MoTA does not currently generate.

---

## Ministry of Health and Family Welfare (MoHFW) / National Health Authority (NHA)

### PM-JAY / Ayushman Bharat — enrollment gaps

**Gap:** BPL citizens not yet enrolled in PM-JAY.

```sparql
SELECT ?citizen WHERE {
  ?citizen jansutra:hasEconomicRecord ?eco ;
           jansutra:hasHealthRecord ?health .
  ?eco jansutra:povertyStatus ?ps .
  FILTER(?ps IN (jansutra:BPL, jansutra:Antyodaya))
  ?health jansutra:isPMAYBeneficiary false .
}
```

**Value:** Enrollment gap cohort for NHA outreach camps.

---

### PHC gap mapping

**Gap:** NHM norms require a PHC within 10 km of every habitation. Current gaps are known at district level but not mapped to the BPL/ST population affected.

```sparql
SELECT ?village ?districtLabel (COUNT(?citizen) AS ?affectedCount) WHERE {
  ?citizen jansutra:residesIn ?village ;
           jansutra:hasServiceAccessRecord ?svc .
  ?svc jansutra:hasServiceAccess ?phc .
  ?phc jansutra:accessType jansutra:PHCAccess ;
       jansutra:accessQuality jansutra:Absent .
  ?village jansutra:hasParentUnit* ?district .
  ?district jansutra:adminLevel jansutra:District ;
            skos:prefLabel ?districtLabel .
  FILTER(LANG(?districtLabel) = "en")
}
GROUP BY ?village ?districtLabel
ORDER BY DESC(?affectedCount)
```

**Value:** Priority ranking for PHC sub-centre establishment under NHM.

---

## Ministry of Women and Child Development (MWCD) / PM-POSHAN

### ICDS and Anganwadi Centre targeting

**Gap:** AWC enrollment lists are maintained at the AWC level; there is no systematic query capability for identifying unserved young children or pregnant women by geographic area.

```sparql
SELECT ?citizen ?village WHERE {
  ?citizen jansutra:hasHealthRecord ?health ;
           jansutra:residesIn ?village .
  { ?health jansutra:childrenUnder5 ?n . FILTER(?n > 0) }
  UNION
  { ?health jansutra:isPregnantOrLactating true . }
  FILTER NOT EXISTS {
    ?citizen jansutra:hasServiceAccessRecord ?svc .
    ?svc jansutra:hasServiceAccess ?awc .
    ?awc jansutra:accessType jansutra:AnganwadiAccess ;
         jansutra:accessQuality ?q .
    FILTER(?q != jansutra:Absent)
  }
}
```

**Value:** Identifies households with young children or pregnant/lactating women who lack AWC access — priority for new Anganwadi centre establishment under PM-POSHAN.

### PMMVY (Pradhan Mantri Matru Vandana Yojana)

First-birth maternity benefit eligibility:

```sparql
SELECT ?citizen WHERE {
  ?citizen jansutra:hasHealthRecord ?health ;
           jansutra:hasEconomicRecord ?eco .
  ?health jansutra:isPregnantOrLactating true .
  ?eco jansutra:povertyStatus ?ps .
  FILTER(?ps IN (jansutra:BPL, jansutra:Antyodaya))
}
```

---

## Jal Shakti Ministry / Jal Jeevan Mission

**Gap:** JJM targets habitations, not individual households. The lowest-income, most-remote households within a habitation may still lack functional connections even after a habitation is declared "tap-connected."

```sparql
SELECT ?village (COUNT(?citizen) AS ?unservedCount) WHERE {
  ?citizen jansutra:residesIn ?village ;
           jansutra:hasServiceAccessRecord ?svc .
  ?village jansutra:isRemoteArea true .
  FILTER NOT EXISTS {
    ?svc jansutra:hasServiceAccess ?w .
    ?w jansutra:accessType ?wt ; jansutra:accessQuality ?wq .
    FILTER(?wt IN (jansutra:PipedWater, jansutra:SafeWaterSource))
    FILTER(?wq IN (jansutra:Reliable, jansutra:Intermittent))
  }
}
GROUP BY ?village
ORDER BY DESC(?unservedCount)
```

**Value:** Village-level count of households without functional water access, orderable by LGD code for pipeline extension planning.

---

## Ministry of Power / SAUBHAGYA

```sparql
SELECT ?citizen WHERE {
  ?citizen jansutra:hasServiceAccessRecord ?svc ;
           jansutra:hasEconomicRecord ?eco .
  ?svc jansutra:hasServiceAccess ?elec .
  ?elec jansutra:accessType jansutra:GridElectricity ;
        jansutra:accessQuality jansutra:Absent .
  ?eco jansutra:povertyStatus ?ps .
  FILTER(?ps IN (jansutra:BPL, jansutra:Antyodaya))
}
```

**Value:** BPL households with no electricity connection — primary cohort for SAUBHAGYA scheme outreach and free connection provision.

---

## MeitY / BharatNet

```sparql
SELECT ?village WHERE {
  ?village jansutra:isPESAArea true .
  FILTER NOT EXISTS {
    ?citizen jansutra:residesIn ?village ;
             jansutra:hasServiceAccessRecord ?svc .
    ?svc jansutra:hasServiceAccess ?net .
    ?net jansutra:accessType jansutra:BroadbandInternet ;
         jansutra:accessQuality ?q .
    FILTER(?q != jansutra:Absent)
  }
}
```

**Value:** PESA villages without broadband — priority for BharatNet optical fibre rollout and digital gram sabha facilitation (e-Gram Swaraj).

---

## Cross-ministry intersectional prioritisation

The highest-value use case is a composite vulnerability score across dimensions — not available from any single ministry's data today:

```sparql
SELECT ?citizen ?village
       (COUNT(*) AS ?deprivationScore)
WHERE {
  ?citizen jansutra:residesIn ?village ;
           jansutra:hasSocialRecord ?soc ;
           jansutra:hasEconomicRecord ?eco ;
           jansutra:hasServiceAccessRecord ?svc .

  # Score 1 point per deprivation dimension
  { ?soc jansutra:casteCategory ?cc . FILTER(?cc IN (jansutra:SC, jansutra:ST)) }
  UNION
  { ?eco jansutra:povertyStatus ?ps . FILTER(?ps IN (jansutra:BPL, jansutra:Antyodaya)) }
  UNION
  {
    ?svc jansutra:hasServiceAccess ?w .
    ?w jansutra:accessType ?wt ; jansutra:accessQuality jansutra:Absent .
    FILTER(?wt IN (jansutra:PipedWater, jansutra:SafeWaterSource))
  }
  UNION
  {
    ?svc jansutra:hasServiceAccess ?p .
    ?p jansutra:accessType jansutra:PHCAccess ; jansutra:accessQuality jansutra:Absent .
  }
  UNION
  { ?village jansutra:isRemoteArea true . }
}
GROUP BY ?citizen ?village
ORDER BY DESC(?deprivationScore)
```

This query ranks every citizen by the number of deprivation dimensions they carry — putting the most multiply-deprived households at the top of every scheme's priority list.
