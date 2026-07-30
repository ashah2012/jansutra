# Design Rationale

The choices that shape Jansutra's architecture are not arbitrary — each is a response to a specific constraint imposed by India's political economy, legal environment, or technical landscape. This page explains the reasoning behind the five most consequential decisions.

---

## Why no Aadhaar

A Jansutra profile linking caste category + poverty status + disability type + FRA land tenure + no-water access is a high-resolution welfare vulnerability fingerprint. If that profile were tied to an Aadhaar number — a stable, biometrically-anchored national identifier — the dataset would become a surveillance instrument.

An adversary (government or private) with access to the Aadhaar ↔ Jansutra mapping could:
- Identify all ST/disabled/BPL individuals in a geography without their knowledge
- Correlate welfare profiles with political activity, land disputes, or protest records
- De-anonymise the dataset by joining it with other Aadhaar-linked registers

Jansutra uses opaque UUID URIs (`citizen:f7a3d2b1-...`) instead. A UUID has no embedded information — it cannot be reversed to an identity without an external mapping table. That mapping table is explicitly held **outside Jansutra**, controlled by the deployer, and subject to separate access governance.

This also places Jansutra outside the Aadhaar Act 2016's scope (which regulates uses of the Aadhaar number and Aadhaar-enabled payment systems). Welfare analysis using Jansutra does not require Aadhaar compliance.

---

## Why federated modules

India's welfare data is already siloed by ministry. The federated module design mirrors that reality rather than fighting it.

**A ministry can share one module without exposing others.** The Ministry of Tribal Affairs can make available a land module (FRA title data) to MoRD for PMAY-G targeting without exposing health records or economic income data. The JSON-LD serialisation makes modules independently parseable.

**Modules can be deployed in different datastores.** A state government's land registry can expose a Jansutra-conformant SPARQL endpoint for just the land module. A district health department can expose just the health module. Federated SPARQL querying across these endpoints is possible without centralising the data.

**The common vocabulary does the heavy lifting.** Ministry registers do not need to merge — they just need to expose data using the same property URIs and SKOS concept identifiers. The ontology is the interoperability contract, not a shared database.

A monolithic schema would force an all-or-nothing data sharing decision. The federated design makes incremental, domain-specific sharing possible.

---

## Why LGD codes and not census village codes

Census village codes change between decennial surveys. When a village splits into two, is renamed, or is reclassified as an urban area, the old census code becomes invalid and a new one is assigned. A database pinned to Census 2011 village codes cannot be directly joined with a database using Census 2031 village codes without a remapping exercise.

The Ministry of Panchayati Raj's Local Government Directory (LGD) assigns stable numeric codes to every administrative unit — codes that persist across census cycles. When a village splits, the LGD records both the successor units with new codes and retains the old code as a historical reference. The parent-child relationship is maintained.

By pinning all Jansutra administrative unit IRIs to LGD codes:
- Survey data from 2024 joins with survey data from 2026 on the same URI
- Ministry datasets that already use LGD codes (MGNREGA MIS, PMGSY GIS, JJM dashboard) can be linked without fuzzy name matching
- The 6% spelling inconsistency problem across ministry datasets disappears when the integer LGD code is the join key

The `skos:prefLabel` multilingual labels are for human readability. The `lgdCode` property is the canonical join key.

---

## Why DPDP Act annotations

The Digital Personal Data Protection Act 2023 creates legal obligations for any entity that processes personal data belonging to Indian citizens. Sensitive personal data — which includes caste, religion, disability, and health information — triggers heightened obligations: explicit consent, data minimisation, purpose limitation, and enhanced security.

Embedding `dpv:hasPersonalDataCategory dpv:SensitivePersonalData` at the property level in the ontology makes these obligations **discoverable in the schema**. Any developer who reads the ontology — not just the legal document — sees that `jansutra:casteCategory` triggers special handling. Code generators, access control systems, and compliance audits can query the ontology directly to find sensitive properties:

```sparql
SELECT ?property WHERE {
  ?property dpv:hasPersonalDataCategory dpv:SensitivePersonalData .
}
```

This is the "privacy by default" principle applied at the semantic layer: the schema itself tells the system what to protect, rather than relying on developers to remember which fields are sensitive.

---

## Why OWL + JSON-LD + SHACL rather than a simpler format

**Why not a relational schema?**

A relational schema requires a fixed join key to link tables. Without a national citizen ID, joining across ministry databases requires probabilistic record linkage — fuzzy-matching names, dates of birth, and village addresses across registers that use different transliteration conventions (Bandgaon / Bandagaon / बांडगाँव), different village name standards, and different script conventions. Studies of such linkages in India find 15–25% false-match rates — both false positives (wrong person linked) and false negatives (same person not linked).

URI-based semantic linking avoids this entirely. Two records about the same citizen share the same UUID URI. The join is exact.

**Why OWL for class and property definitions?**

OWL's open-world assumption and `rdfs:subClassOf` hierarchy support the inference that a `SocialRecord` is also a `VulnerabilityDimension` — enabling shapes and queries that target the superclass to work on all subclass instances. OWL functional property declarations on the five domain record links enforce the one-record-per-citizen constraint.

**Why JSON-LD as the primary serialisation?**

JSON-LD is the most accessible RDF serialisation for government data engineers who work in Python and REST API contexts. It reads as familiar JSON; the `@context` file handles the vocabulary mapping invisibly. A ministry data engineer can work with `household-001.jsonld` without knowing anything about RDF or Turtle syntax.

**Why SHACL rather than OWL constraints alone?**

OWL operates under the open-world assumption — it cannot conclude that a property is absent just because it is not asserted. SHACL operates under a closed-world assumption on the shape target: if `sh:minCount 1` is not satisfied, the constraint fails. This makes SHACL suitable for data quality validation in a way OWL is not.

SHACL also produces precise, human-readable constraint violation messages (which property failed, which value was invalid, which constraint was violated). OWL reasoner outputs require post-processing to extract actionable error information.

The combination — OWL for semantics and inference, SHACL for validation — is the current best practice for production knowledge graphs.
