# Cross-Language Feasibility Matrix — WP-04: canonical history store

**Required by:** `process/agent-workflow.md` §3 step 5. **Template:**
`process/templates/cross-language-feasibility-matrix.md`.
**Authority bundle:** `mneme-v2.3-dual-profile`. **Author:** Claude (shared-contract owner).
**Independent reviewer:** Codex.

**Contract:** `spec/persistence.md`, "Layer 04 canonical history store contract (WP-04)", with
stage-table rows in `spec/serialization.md` and notes under HIST-008 and HIST-009.
**Governance:** G-077…G-087 (`reference/governance/2026-10-11-owner-layer04-start.md`), plus
G-013, G-051 and G-054.

**Status:** CONTRACT-STAGE DRAFT, revision 1 (Codex review `0cc23387`: WP04-CR-001…006, Q1…Q3).
- Every row names the witness that will carry its evidence.
- A state of `PLANNED` becomes `AUDITED` only when the Python candidate supplies that evidence,
  before the Rust handoff, as in Layer 03.
- `NOT_APPLICABLE` and `DEFERRED_WITH_REASON` rows are final now.

**Toolchains:**
- Python: CPython 3.12.8 (uv-managed) and the psycopg 3 driver.
- Rust: 1.97.1 with a synchronous PostgreSQL client crate, chosen by Codex.
- Reference backend: PostgreSQL 14.12, a local service, databases created per the spec rule.

**Evidence keys:**
- **[SC]** the five WP-04 scenarios: `store-commit-gapless-positions`, `store-commit-strict-writer`,
  `history-same-operation-retry-commits-once`, `store-no-semantic-dedup` and `store-bounded-read`;
- **[PT]** the planned Python store tests, `tests/core/test_layer04_store.py`;
- **[IT]** the planned cross-language interoperability test: a store written by one language is read
  and retried by the other, both directions;
- **[CT]** the planned crash and concurrency tests;
- **[L1]**, **[L2]** and **[L3]** the certified lower layers (G-044, G-065, G-076).

## 1. Value-domain matrix

| Observable value / field | Contract domain | Python repr | Rust repr (required) | Persisted form (reference backend) | Lossless? | Witness |
|---|---|---|---|---|---|---|
| `store_id` | CORE-001 | `str` | `String` | `text`, C collation | YES (ASCII) | [SC] unknown store; [IT] |
| position / tail | gapless 1…2^53−1, 0 = empty (G-080) | `int` | `i64` (u53 range) | `bigint` | YES | [SC] gapless steps; [PT] range near 2^53 is unreachable by count, so bound-checked by unit test |
| `recorded_at` | one canonical HIST-004 instant (`.ffffffZ`) per batch, from the clock's instant (G-082) | `str` canonical | `String` canonical | inside canonical envelope bytes plus `text` in `mneme_operation` | YES | [SC] receipts, incl. an offset-spelled clock instant stored canonically (CR-002); [IT] |
| `source_operation_id` | 1–256 exact UTF-8 bytes, any Unicode scalars incl. U+0000 (G-033) | `str` | `String` | `bytea`, exact UTF-8 bytes; bytewise equality (CR-001) | YES | [SC] NUL and a-NUL-b identities: commit, normalized retry, conflict; [IT] cross-language NUL retry |
| `source_namespace` | CORE-001 token | `str` | `String` | `text` (ASCII, never NUL) | YES | [SC] namespace step |
| draft | closed envelope without `recorded_at` | normalized `dict` | normalized `Value` | not stored itself; folded into the mutation | YES | [SC] strict-writer steps |
| envelope | Layer 02 envelope + stamped `recorded_at` | `dict` | `Value` | `bytea` SER-009 canonical bytes | YES | [IT] byte equality across languages |
| mutation | SER-009 bytes of the normalized draft array | `bytes` | `Vec<u8>` | `bytea` | YES | [SC] retry, reorder, namespace steps; [IT] cross-language retry |
| receipt | closed record (spec) | `dict` | `Value` / struct | rebuilt from `mneme_operation` + records | YES | [SC]; [IT] |
| page | `{entries, through, tail}` | `dict` | `Value` / struct | query result | YES | [SC] bounded-read |
| `limit` | integer 1…2^53−1 | `int` (bool rejected) | `i64` after L01 normalization | not persisted | YES | [SC] limit 0, 1.5 |

## 2. Lower-layer capability matrix

| Required semantic operation | Owning layer | Existing reviewed seam | Exact? | Python | Rust | Additive extension? | Reopen? |
|---|---|---|---|---|---|---|---|
| generic stages across arguments (G-031) | 01 | `validate_arguments` / `staged` | yes | yes | yes | no | no |
| draft admission via the gates (G-055) | 02 | `_admit` / `envelope_rule` | needs a draft mode | to add | to add | **yes**: gates D1–D4, the envelope gates with `recorded_at` removed from the closed member set; a supplied `recorded_at` is a D3 unknown member | no |
| reader (writer) validation (G-053) | 02 | `_reader_rule` / `reader_rule` | yes | yes | yes | no | no |
| operation identity (G-032/G-033) | 01 | `operation_identity` | yes | yes | yes | no | no |
| boundary validation and comparison (G-051) | 02 | HistoryBoundary rules | yes | yes | yes | no | no |
| canonical bytes (SER-009) | 01 | `canonical_bytes` | yes | yes | yes | no | no |
| paging completeness (PERS-007, WP-04 part) | 04 | `read_history` | — | to add | to add | no | no |
| memory-bounded incremental rebuild (PERS-007) | 05 | none yet (an incremental projector is not exact over Layer 03's whole-stream projector) | — | — | — | DEFERRED to Layer 05 (G-087) | no |
| container / target reads (PERS-007) | profile layers | none | — | — | — | DEFERRED to the profile layers; indexes are derived read models (G-087) | no |

## 3. Hazard checklist

| Hazard (family/member) | State | Evidence / reason |
|---|---|---|
| H1 integer width | PLANNED | positions as `bigint`, read back as `int` / `i64`; limit bound 2^53−1 ([SC] limit; [PT] bound unit test) |
| H1 JSON number lexical forms | PLANNED | `limit: 1.5` invalid, `2.0` normalizes by L01 ([SC]; [PT]) |
| H1 float policy | AUDITED | payload floats pass the L01 domain before canonical bytes ([L1]) |
| H1 arithmetic | PLANNED | the only arithmetic is `tail+1…tail+K`, under the lock, after the capacity check K ≤ MAX − tail (G-086); `CHECK` constraints bound tail and position. [PT] synthetic tail MAX−1: K=1 commits, K=2 is `persistence.store_full` with no clock sample; at tail MAX an identical retry still returns its receipt and a different mutation conflicts (CR-006) |
| H1 SQLite affinity | NOT_APPLICABLE | the reference backend is PostgreSQL with typed columns (G-079); an embedded backend re-opens this row |
| H2 scalar domain | AUDITED | records enter only as SER-009 canonical UTF-8 bytes, compared as bytes, never as `text` ([L1]) |
| H2 encoding | PLANNED | databases are UTF-8 with C collation (spec rule); envelopes are `bytea`, so no server re-encoding ([IT]) |
| H2 NUL | PLANNED | PostgreSQL `text` cannot hold NUL (SQLSTATE 22021, Codex probe). `text` holds only CORE-001 tokens and canonical timestamps; `source_operation_id`, envelopes and mutations are `bytea` (CR-001) ([SC] NUL identity; [PT] a payload string containing U+0000 round-trips) |
| H2 length units | AUDITED | IDs and tokens are ASCII ([L1]) |
| H2 line endings | NOT_APPLICABLE | no text files are written |
| H3 normalization | NOT_APPLICABLE | no Unicode normalization (CORE-001 exact compare) |
| H3 case mapping/folding | PLANNED | `store_id` and `record_id` uniqueness is exact under C collation (`o-1` vs `O-1` is an invalid ID anyway; [PT] uniqueness of IDs differing only after position 1) |
| H3 collation/sort | PLANNED | ordering is by `bigint` position only, never by text ([SC] pages) |
| H3 Unicode version | NOT_APPLICABLE | no Unicode tables |
| H3 lexical tokenization | NOT_APPLICABLE | no lexical retrieval |
| H4 representation | PLANNED | the store stamps the clock instant's canonical HIST-004 form; scenarios use `.ffffffZ` expectations and one offset-spelled clock instant (CR-002) ([SC] gapless) |
| H4 unknown vs present | AUDITED | `occurred_at` optional as in G-049 ([L2]) |
| H4 clocks | PLANNED | at most one sample per new-commit attempt, at step 12 under the lock; steps 1–11 (validation, retries, conflicts, store duplicates, capacity) never sample (G-085, G-086) ([SC] exact instants consumed; [CT] counting clock) |
| H4 ordering | PLANNED | `recorded_at` never orders records; position does (G-082, G-051) ([PT] a clock running backwards still yields ascending positions) |
| H4 leap seconds/DST | AUDITED | HIST-004 rejects `:60` ([L1]) |
| H5 map iteration | AUDITED | mutation and envelopes are canonical bytes ([L1]) |
| H5 canonical key order | AUDITED | SER-009 ([L1]) |
| H5 sort stability and keys | PLANNED | pages are `ORDER BY position` on a primary key ([SC]) |
| H5 sets | NOT_APPLICABLE | no set-valued output in Layer 04 |
| H5 pagination | PLANNED | record-counted since-boundary pages may slice a committed batch; pages from 0 to the tail yield every record once ([SC] bounded-read; [PT] property test). Incremental bounded rebuild is DEFERRED to Layer 05 with ReplayCheckpoint, and container/target reads to the profile layers (G-087) |
| H6 YAML version / anchors / duplicate keys / big numbers / null vs missing / enforcement | AUDITED | corpus gate `mneme-process check` 8/8 ([L1]) |
| H7 algorithm and output | NOT_APPLICABLE | Layer 04 computes no hashes |
| H7 canonical form | PLANNED | retry identity compares normalized canonical draft bytes ([SC] retry and reorder steps; [IT] a retry from the other language) |
| H7 identity vs integrity | PLANNED | equal content under different IDs is two records (HIST-008) ([SC] no-semantic-dedup) |
| H8 SQLite version | NOT_APPLICABLE | PostgreSQL reference backend (G-079) |
| H8 isolation | PLANNED | commit locks the store row (`FOR UPDATE`) before steps 9–13; reads use one `REPEATABLE READ READ ONLY` snapshot for range check, entries and tail (CR-004; Codex probe: Read Committed gave through 19 > tail 18) ([CT] reader loop during commits checks the whole page: `through ≤ tail`, contiguous positions, whole commits) |
| H8 crash points | PLANNED | one transaction per commit; [CT] kills the connection (`pg_terminate_backend`) before COMMIT and confirms no effect, then retries |
| H8 idempotency | PLANNED | `mneme_operation` primary key; [SC] retry; [CT] concurrent identical retries yield one physical commit and the same receipt |
| H8 JSONL | NOT_APPLICABLE | no JSONL backend |
| H8 durability | PLANNED | `synchronous_commit = on` asserted per connection ([PT] reads the setting) |
| H8 schema version | PLANNED | singleton `mneme_schema` row; open creates schema v1 under an advisory lock or requires exactly the four tables and version 1, else `persistence.schema_incompatible` with no change (Q3) ([PT] absent, mismatched, malformed and two-row cases; [CT] concurrent first opens) |
| H9 (all members) | NOT_APPLICABLE | no filesystem paths in WP-04; asset files are WP-04T (PERS-016) |
| H10 concurrent retry | PLANNED | [CT] N parallel identical commits → one physical commit, N equal receipts |
| H10 async enrichment | NOT_APPLICABLE | enrichment ordering is WP-04T (PERS-004); WP-04 provides only the receipt barrier |
| H10 cancellation | PLANNED | an attempt aborted after step 12 may have sampled the clock but persists nothing; a later retry may get a different instant (G-085) ([CT] rollback and `pg_terminate_backend` after the sample: tail, records and operations unchanged; the retry commits with the next instant) |
| H11 ID lexical domain | AUDITED | CORE-001 for `store_id`, `record_id` ([L1]) |
| H11 version domain | AUDITED | `schema_version` per G-053 ([L2]) |
| H11 scope encoding | NOT_APPLICABLE | no MemoryScope in WP-04 |
| H11 reference integrity | PLANNED | `record_id` unique across the store and across profiles (G-083) ([SC] strict writer) |

## 4. Concurrency / order matrix

| Ordering guarantee | Realistic wrong implementation | Witness that kills it |
|---|---|---|
| commits are linearized; ranges are gapless and consecutive (G-084) | read tail, then insert without locking | [CT] 8 writers × 50 commits: the union of ranges is exactly 1…N, no gaps or overlaps |
| at most one physical commit per operation (G-084) | check-then-insert outside the lock | [CT] parallel identical retries |
| conflicting mutations never last-write-wins | upsert on the operation key | [SC] conflict; [CT] parallel conflicting commits: exactly one wins, the others conflict |
| failed commits consume nothing (G-080, G-082) | allocate positions from a sequence | [SC] rejected-batch step; [CT] killed transaction |
| validation precedes every effect | append, then validate | [SC] mixed valid and invalid batch |
| the evaluation order of each operation (CR-003) | check store existence first | [SC] precedence pairs: in-batch duplicate before unknown store; `store_id` before writer; D2 before D3 before D4; limit before boundary comparison; JSON stage-1 errors before stage-3 errors |
| idempotency, then store duplicates, then capacity, then clock (G-085, G-086) | sample the clock before the retry check | [SC] retries consume no instant; [PT] full-store retry |
| reads come from one snapshot containing whole commits only | separate Read Committed queries for tail and entries | [CT] reader loop during commits (CR-004) |
| retry check precedes the store record-ID check | check record IDs first, so a retry fails as a duplicate | [SC] identical retry returns the receipt |

## 5. Neighborhood expansion record

To be filled during implementation review.

## 6. Verdict

```text
FEASIBILITY
    DRAFT     contract stage; PLANNED rows become AUDITED from the Python candidate's evidence
              before the Rust handoff. Rust needs: a draft admission mode over the certified
              Layer 02 gates (additive), the PostgreSQL schema, and the [CT]/[IT] tests.
```
