# CE-04-01 — targeted checkpoint review, revision 5 (Codex)

**Verdict: APPROVED.**

Reviewed docs **f28dbd445a80f3a8a89a0aad5b5a3326325ac7df**, classification §10 and its
`spec/persistence.md` transcription, against G-088..G-098 and review 4 (`76908bc8`). The behavior
reference remains frozen code **be36323f56e61d87776d11c831ae1ef0573ea692**.

**CE04-CP-005 is resolved for the checkpoint.** CP-004/006/007 remain resolved as previously
reviewed. No new finding or candidate path-C item is raised. This approves the revised checkpoint
(revisions 2–5 together), not production correctness, WP-04 acceptance or certification. The
implementation and its closure evidence remain due; Codex has made no production change.

## The whole-row rule closes the omitted-shape gap

§10 explicitly replaces §9.2.4's abbreviated field list. It covers every column of pg_class,
pg_index, pg_attribute and pg_type for internal TOAST relations/indexes/attributes and the core
tables' row/array types. The shared spec now requires that same rule. The old list is history,
not permission to stop comparison after its enumerated fields.

The named exclusions do not include reloptions or indoption. Both previous refinements therefore
have the literal rejection oracle **persistence.schema_incompatible**, through members. The extra
index still differs in cardinality; discovering it cannot grant certification. Whole-row comparison
also covers the remaining index/TOAST/type properties that were merely missing from the prior list.

The exclusions distinguish raw catalog identity from semantic associations. Excluded pointer OIDs
still require the correct backlink, target kind and association; zero/absent associations cannot
be silently equated with arbitrary objects. Namespace, type, access-method, opclass, collation and
function references require structured normalization, not search-path-dependent rendered names.
Required public table/column names remain normative. Generated internal names are the stated
member-name exclusion; excluding a TOAST attribute name does not exclude its ordinal, type or
descriptor. In particular attnum is not in the exclusion list.

G-098 remains a comparison rule, not another exemption: type copies are checked against the actual
admitted type; counts are invariants; stored offsets and static/fallback/foreign descriptors are
pinned. G-096's specifically named changing fields remain separate. Reusing existing layouts in
§10.2 means reusing normalization machinery while satisfying §10.1's complete column coverage,
not retaining a layout that drops newly required fields.

The inventory test is a useful independent obligation. It must inspect the actual live catalog
column names and tie each to a compared/normalized field or the specific closed exclusion. It
cannot merely declare an omitted field “compared.” The production whole-row rule remains the
requirement; this test supplements it rather than allowing untested columns to be silently
discarded at runtime. Those points follow from the revised rule and are implementation checks,
not additional semantic choices.

## Independent targeted executions

I initialized a fresh private schema from the **normative DDL extracted from this exact reviewed
spec**, then inserted its version-1 header. I did not use a changed production initializer or copy
a proposed implementation. The unchanged public store opened it and protocol N passed: positions
1/2, identical retry, read [1,2], tail 2.

The live PG14.12 column inventory was:

| Catalog | Columns |
|---|---|
| pg_class | 33 |
| pg_index | 20 |
| pg_attribute | 26 |
| pg_type | 32 |

All **111** columns were partitioned between §10.1's named raw exclusions and retained properties
(including those needing association/consistency/invariant normalization). Each named exclusion
exists in its applicable catalog. This is an inventory observation, not a claim that future
production fetches or the pending inventory test have been executed.

Using the real initializer's member rows, I projected exactly one field at a time in SQL and
observed every raw column. After applying only the named exclusion filter, the retained differences
were:

| Member / projected field | Observed change | Retained difference / revised oracle |
|---|---|---|
| TOAST index reloptions | NULL → [fillfactor=70] | reloptions; reject members |
| TOAST index indoption | [0,0] → [0,3] | indoption; reject members |
| TOAST relation reloptions | NULL → [autovacuum_enabled=false] | reloptions; reject members |
| row type typdelim | comma → semicolon | typdelim; reject members |
| TOAST relation relpages | 0 → 500 | none; planner-estimate exclusion |

The first two are the exact refinements from review 4. They no longer disappear under the specified
field selection. The additional relation/type cases exercise the broadened scope; the estimate
control bounds the exclusions. Actual type observations also confirm each composite's table
backlink and each array's element backlink in the normative initializer.

**Evidence boundary:** these are executed catalog-row projections and rule/coverage observations,
not physical alterations of TOAST/type metadata and not executions of the future members
implementation. No superuser role/provider was used. I do not claim a downstream store failure for
any projected variation. The [F] controls in the implementation must exercise its actual fetch,
normalization, joins/filters and final mismatch, and distinguish those kills from public evidence.

The extra-index cardinality control and CH13 baseline/large-payload acceptance remain required,
as do the inherited G-098, E004, boundary, label and P32/P40 obligations. Their earlier results
are not reclassified by this checkpoint approval. Exact shared pins must be derived from the
normative initializer and tested with the actual source at implementation closure.

## Provenance and cleanup

Project-managed CPython 3.12.8, psycopg 3.2.13, PostgreSQL 14.12, ordinary mneme_dev only. Every
shell first sourced the project environment; the host was clear. One throwaway database was
created from template0 with UTF8/C/C in mneme_ts and dropped in finally. All scratch/database
files remained under the E: project. Frozen source is unchanged; only this review record is tracked.

Evidence: `.tmp/work/codex/ce04-checkpoint5/probe.py`, `results.json`, `probe.log` and `audit.json`.
The results include the exact extracted DDL hash, full live inventory, field changes, public
baseline trace and successful database drop. The audit verifies source cleanliness and database
absence. Production validation and fresh gates are the next coordinated step after agreement.

Evidence SHA-256 bindings:

- probe.py: `147ec2aff6fa6411bb192cdc5dc68c6fe8d7521fb56a8a6155da039b835b6fa7`
- results.json: `e033dc68073d370b15001926f06eeb798daef19f22efa9f480ca6e9dace1a9bf`
