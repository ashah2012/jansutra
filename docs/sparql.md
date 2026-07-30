# SPARQL Queries

Three reusable SPARQL queries are included in `sparql/`. They are designed to run against Jansutra-conformant data using `tools/query.py`.

```bash
python tools/query.py sparql/<query>.sparql examples/household-001.jsonld
```

---

## 1. Vulnerability query

**File:** `sparql/vulnerability-query.sparql`

**Purpose:** Find Scheduled Tribe citizens in PESA or remote areas who have no functional water access **and** no PHC access — the intersectional cohort that today's fragmented data cannot identify.

### How it works

The query does four things:

1. **Caste filter** — `?social jansutra:casteCategory jansutra:ST` selects only ST citizens.

2. **Geography filter** — `?village jansutra:isRemoteArea true` restricts to villages classified as remote (no all-weather road within 5 km). For a strict PESA-only query, use `jansutra:isPESAArea true` instead.

3. **Hierarchy traversal** — `?village jansutra:hasParentUnit* ?district` uses the `*` (zero-or-more) SPARQL property path to walk up from village through sub-district to district. The query then retrieves the district's English `skos:prefLabel`.

4. **Water access exclusion** — `FILTER NOT EXISTS { ... }` eliminates citizens who have any water access of type `PipedWater` or `SafeWaterSource` with quality `Reliable` or `Intermittent`. Only citizens with no functional water access survive the filter.

### Expected output (against household-001.jsonld)

```
citizen                                           districtLabel    povertyStatus  phcDistanceKm
https://jansutra.in/citizen/f7a3d2b1-4e89-...    West Singhbhum   BPL            18.5
1 result(s)
```

### Query

```sparql
--8<-- "sparql/vulnerability-query.sparql"
```

---

## 2. Poverty by district

**File:** `sparql/poverty-by-district.sparql`

**Purpose:** Aggregate counts of BPL and AAY citizens per district, broken down by caste category. Enables intersectional resource allocation — which district-caste combinations have the highest poverty concentration?

### How it works

- Filters to `povertyStatus IN (jansutra:BPL, jansutra:Antyodaya)` — note that `Antyodaya` (AAY) has `skos:broader BPL` in the scheme but is a distinct SKOS concept, not a subclass; the filter must list both explicitly.
- Uses `jansutra:hasParentUnit*` to find the district from any residential unit.
- `GROUP BY ?districtLabel ?casteNotation` with `COUNT(?citizen)` produces a matrix.

### Expected output (against household-001.jsonld)

```
districtLabel    casteNotation  citizenCount
West Singhbhum   ST             1
1 result(s)
```

Results scale with national-level data — this query is designed for a populated district dataset. Against a single-household file it returns one row.

### Query

```sparql
--8<-- "sparql/poverty-by-district.sparql"
```

---

## 3. Land gap by caste

**File:** `sparql/land-gap-by-caste.sparql`

**Purpose:** Average landholding area grouped by caste category. Measures the structural land ownership gap between ST/SC and non-ST/SC households — a key metric for monitoring whether FRA titles are expanding tribal land access over Census cycles.

### How it works

- Joins `hasSocialRecord` → `casteCategory` with `hasLandHolding` → `areaInHectares`
- `AVG(?areaHa)` grouped by `?casteLabel` and `?casteNotation`
- A citizen with no `hasLandHolding` link is excluded (landless citizens are not counted)

!!! note
    To count **landless** citizens separately, add a `FILTER NOT EXISTS { ?citizen jansutra:hasLandHolding ?h . }` query alongside this one.

### Expected output (against household-001.jsonld)

```
casteLabel          avgHectares  citizenCount
Scheduled Tribe     0.8          1
1 result(s)
```

### Query

```sparql
--8<-- "sparql/land-gap-by-caste.sparql"
```

---

## Running queries

```bash
# Against example data only
python tools/query.py sparql/vulnerability-query.sparql examples/household-001.jsonld

# Against multiple data files
python tools/query.py sparql/poverty-by-district.sparql data/district-A.jsonld data/district-B.jsonld

# The query runner loads all ontology modules automatically
# (no need to pass ontology files explicitly)
```

See the [Tools page](tools.md) for full usage details.
