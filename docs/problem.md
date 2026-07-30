# The Problem

## India's welfare data is fragmented and stale

The last comprehensive socioeconomic household census — SECC 2011 — is fifteen years old. Poverty lines, BPL lists, and caste registers derived from it are still the primary basis for welfare eligibility across most of India's flagship schemes.

In those fifteen years:
- Approximately 45 million households have changed income status
- The Forest Rights Act has granted 2.3 million individual titles, but most are not in any machine-readable registry
- JJM (Jal Jeevan Mission) claims to have provided tap connections to 120 million rural households since 2019 — but no survey has updated the village-level service-access record

The data lag means schemes reach the wrong people. The 2021-22 HCES found that 22% of AAY ration-card holders in rural India had crossed the income threshold; the cards had not been updated. Simultaneously, an estimated 18% of genuinely BPL households had no ration card at all.

---

## Ministry silos cannot be joined

India administers welfare through twelve separate central ministries, each running its own beneficiary register:

| Ministry | Register | Primary key |
|----------|----------|-------------|
| MoRD | MGNREGA job cards | Job card number |
| NHA | PM-JAY beneficiary list | Aadhaar + state ID |
| MoTA | FRA title holders | Patta number |
| MoFPS | Ration cards | Ration card number |
| NRLM | SHG members | SHG ID |
| MWCD | ICDS beneficiaries | Anganwadi code |

None of these registers share a primary key. Joining them requires probabilistic record linkage — fuzzy-matching names, dates of birth, and addresses across registers that use different spelling conventions, different language scripts, and different village name standards. Studies of such linkages in India typically find 15–25% false-match rates.

Aadhaar was intended to solve the linking problem. It partially does for payment channels, but it does not expose the underlying welfare-eligibility dimensions — caste, land tenure, service access gaps, disability status — that would let a planner ask: *which households need which interventions?*

---

## What precision targeting requires

The blog post that motivated this project identifies the core analytical question:

> *Find the Scheduled Tribe woman in a PESA village who has no piped water, no PHC within 20 km, and an FRA title she cannot leverage for credit.*

To answer this requires joining across:

1. **Caste register** — to identify ST status
2. **Geography** — to identify PESA village classification
3. **Service access survey** — to check piped water and PHC proximity
4. **Land registry** — to identify FRA title holders
5. **Income data** — to assess credit-gap severity (BPL income despite titled land)

Today, those five datasets live in five different systems with five different keys. No ministry can answer this query without a multi-year data reconciliation exercise.

---

## The Bandgaon example

Citizen `f7a3d2b1-...` lives in Bandgaon village, Chakradharpur Block, West Singhbhum district, Jharkhand.

She is:
- **Scheduled Tribe**, mother tongue Ho
- **BPL** — annual household income ₹48,000 for a family of five (₹1,100/month per capita)
- Holds a **Forest Rights Act title** to 0.8 hectares of forest land, khasra 285/2, with a registered deed
- **Agricultural labourer**, MGNREGA job card holder
- **No safe water source within 4.5 km**
- **Nearest PHC is 18.5 km away** — nearly double the 10 km NHM threshold
- **No paved road for 12 km**
- **Grid electricity intermittent**
- **One child under 5**

Under current systems:
- MoRD's MGNREGA system knows she has a job card
- NHA's PM-JAY system knows she has health insurance
- The Jharkhand land registry has her FRA title
- No system knows she has no water, no PHC access, and an FRA title that could generate credit but hasn't

She is invisible to the intersectional analysis that would flag her village for Jal Jeevan Mission attention, PMGSY road construction priority, and PHC sub-centre establishment.

---

## What Jansutra does differently

Jansutra is an **OWL ontology** that expresses all six of these dimensions in a single linked data model. The modules are federated — no single database — but share a common vocabulary, shared administrative unit identifiers (LGD codes), and a shared citizen URI scheme (UUID, no Aadhaar).

When the modules are populated with survey data, the query above becomes four SPARQL clauses. The answer takes milliseconds.

The goal is not to build a centralized database — India's political economy makes that impossible and dangerous. The goal is to define a **semantic interoperability standard** that lets existing ministry registers speak to each other through a common vocabulary, without replacing them.
