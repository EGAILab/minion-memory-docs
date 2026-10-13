# Cross-Language Feasibility Matrix — WP-04: canonical history store

**Required by:** `process/agent-workflow.md` §3 step 5. **Template:**
`process/templates/cross-language-feasibility-matrix.md`.
**Authority bundle:** `mneme-v2.3-dual-profile`. **Author:** Claude (shared-contract owner).
**Independent reviewer:** Codex.

**Contract:** `spec/persistence.md`, "Layer 04 canonical history store contract (WP-04)", including
"Reference backend: PostgreSQL shared schema". Stage-table rows are in `spec/serialization.md`, with
notes under HIST-008 and HIST-009.
**Governance:** G-077…G-098 (`reference/governance/2026-10-11-owner-layer04-start.md`), plus G-013,
G-031, G-033, G-051, G-054 and G-055.
- **G-077…G-087:** store semantics.
- **G-088:** convergence CE-04-01.
- **G-089…G-092:** the exact v1 catalog, the database environment, PostgreSQL 14 with structured
  comparison, and the trust scope.
- **G-093:** gates wait for host clear.
- **G-094…G-097:** the dependency island, row-type references, the engine-bookkeeping exemption, and
  comments and labels.
- **G-098:** no further exemption for engine-generated fields.

## Current candidate and evidence

**Status:** `FINAL_CONTRACT_REVIEW`.

**Current pair:**
- **code:** `9d5a2d51c69987f799962868b8dc5175a11882d2` on `wp04/contract`;
- **docs:** the content commit named in `process/state/WP-04.yaml`.

**Current gate evidence:** `assurance/reviews/WP-04-CE-04-01-implementation-claude-2.md` §5.3
(run 5):

| Gate | Result |
|---|---|
| G2 | 856 passed, 4 xfailed |
| G3 | 100 % of 1304 statements and 490 branches |
| G4 | 58 of 59 CE-04-01 planted violations killed; P38 is a bounded equivalent |
| G5 | 17 of 18 WP-04 planted violations killed; P14 is equivalent |

The checkpoint is the agreed CE-04-01 classification, revisions 2–5:
- `assurance/convergence/CE-04-01-classification.md` §0–§10;
- Codex `APPROVED` `bfb6cad3` and `955d91f6`;
- targeted closure `46514f00`.

**History** (superseded, kept for traceability; not current premises):
- **The contract** was agreed at docs `d857fcc2` (Codex `67ba6632`).
- **The first Python evidence** was at code `afb36081`, remediated at `63462513` after Codex review
  `bb3dfa2c`. At that stage there were:
  - 20 store tests;
  - planted violations P01–P20 (later P01–P23, 22 of 23 killed);
  - an H8 schema-version check of "10 damaged v1 shapes compared by catalog columns and
    constraints".

  Codex review `391fca64` showed that check was not a trust boundary (WP04-CR-008, trigger A). It
  was replaced by the CE-04-01 catalog contract of §3a.
- **CE-04-01 gate runs:**
  - run 1 at `b657081b` (G4 failed);
  - run 2 at `be36323f`;
  - run 3 at `426f14f3` (G4 failed);
  - run 4 at `03841628`.

**Toolchains:**
- Python: CPython 3.12.8 (uv-managed) and psycopg 3.2.13.
- Rust: 1.97.1 with a synchronous PostgreSQL client crate, chosen by Codex.
- Reference backend: PostgreSQL 14.12 (G-091), a local service. Databases are UTF-8 with C/POSIX
  collation and ctype (G-090), created per the spec rule.

**Evidence keys (current):**
- **[SC]** the five WP-04 scenarios, 65 steps: `store-commit-gapless-positions` (14),
  `store-commit-strict-writer` (19), `history-same-operation-retry-commits-once` (12),
  `store-no-semantic-dedup` (4) and `store-bounded-read` (16).
- **[PT]** / **[CT]** `tests/core/test_layer04_store.py`: 40 tests, covering the operations and the
  crash, concurrency, clock, capacity and open-protocol behavior.
- **[CW]** `tests/core/test_layer04_catalog.py`: 315 catalog witnesses, each tagged with its
  evidence kind:
  - **[P]** public open, 199 in all:
    - 140 refused, every one with no change;
    - 38 accepted, each with protocol N;
    - E004, which has its own oracle;
    - 20 more: D02/D03/D05 (2), CH09c (3), I14, I18, the large payloads (2), B03/S10, X01/X03/X05,
      X02, X04/R34, X08, X11, the permission rows (2), R25, S06/V02 (2).
  - **[T]** transaction control: initialization pins and postcondition; X09/X10.
  - **[E]** direct engine control: CH12, the poisoned session; the private session.
  - **[Pr]** predicate over synthesized catalogs: 12 + 58, the environment (9), and the pinned
    catalog and residue controls.
  - **[F]** fetch binding (CR-014): 18 field, 2 row and 5 patched-row controls.
  - **[INV]** the catalog-column inventory.
  - **[PIN]** the normative-DDL and initializer pin tests, and the shared-pin embedding.
- **[MU]** the planted violations:
  - `.tmp/work/claude/py_mutants_ce0401.py`, 59 entries (G4);
  - `.tmp/work/claude/py_mutants_wp04.py`, 18 entries (G5: P02–P05, P07–P14, P16–P20, P23).
- **[IT]** the cross-language interoperability tests, **due at the Rust candidate, not executed**:
  - a store written by one language is read and retried by the other, in both directions;
  - mixed-language concurrent and waiting first opens;
  - a schema initialized by one language is opened by the other;
  - a retry committed by one language returns the same receipt in the other.
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
| v1 catalog pins | the catalog state the normative DDL produces (G-089, G-098, CE04-CP-005) | `Catalog` of OID-free row tuples (`_v1_catalog.py`) | the same rows, embedded from the shared file | `reference-backend/postgres14-v1-catalog.json`, derived by executing the spec's normative DDL on PostgreSQL 14.12 | YES; member rows are PostgreSQL's own `jsonb::text` (canonical key order), which is data serialization, not rendered SQL (G-091) | [PIN] normative DDL = pins = initializer; embedding = shared file. Rust embeds the same file and must render members with the same `::pg_catalog.text` |

## 2. Lower-layer capability matrix

| Required semantic operation | Owning layer | Existing reviewed seam | Exact? | Python | Rust | Additive extension? | Reopen? |
|---|---|---|---|---|---|---|---|
| generic stages across arguments (G-031) | 01 | `validate_arguments` / `staged` | yes | yes | yes | no | no |
| draft admission via the gates (G-055) | 02 | `_admit` / `envelope_rule` | needs a draft mode | yes (`draft=True`) | to add | **yes**: gates D1–D4, the envelope gates with `recorded_at` removed from the closed member set; a supplied `recorded_at` is a D3 unknown member | no |
| reader (writer) validation (G-053) | 02 | `_reader_rule` / `reader_rule` | yes | yes | yes | no | no |
| operation identity (G-032/G-033) | 01 | `operation_identity` | yes | yes | yes | no | no |
| boundary validation and comparison (G-051; HistoryBoundary as a store-local cursor, NF-016 CLOSED) | 02 | HistoryBoundary rules | yes | yes | yes | no | no |
| canonical bytes (SER-009) | 01 | `canonical_bytes` | yes | yes | yes | no | no |
| paging completeness (PERS-007, WP-04 part) | 04 | `read_history` | — | yes | to add | no | no |
| v1 catalog validation at open (CE-04-01) | 04 | `persistence.catalog` (`fetch`, `mismatch`, `environment_mismatch`) | — | yes | to add, from the contract and shared pins only | no | no |
| memory-bounded incremental rebuild (PERS-007) | 05 | none yet (an incremental projector is not exact over Layer 03's whole-stream projector) | — | — | — | DEFERRED to Layer 05 (G-087) | no |
| container / target reads (PERS-007) | profile layers | none | — | — | — | DEFERRED to the profile layers; indexes are derived read models (G-087) | no |

## 3. Hazard checklist

| Hazard (family/member) | State | Evidence / reason |
|---|---|---|
| H1 integer width | AUDITED | positions as `bigint`, read back as `int` / `i64`; limit bound 2^53−1 ([SC] limit; [PT] bound unit test) |
| H1 JSON number lexical forms | AUDITED | `limit: 1.5` invalid, `2.0` normalizes by L01 ([SC]; [PT]) |
| H1 float policy | AUDITED | payload floats pass the L01 domain before canonical bytes ([L1]) |
| H1 arithmetic | AUDITED | the only arithmetic is `tail+1…tail+K`, under the lock, after the capacity check K ≤ MAX − tail (G-086); `CHECK` constraints bound tail and position. [PT] synthetic tail MAX−1: K=1 commits, K=2 is `persistence.store_full` with no clock sample; at tail MAX an identical retry still returns its receipt and a different mutation conflicts (CR-006) |
| H1 SQLite affinity | NOT_APPLICABLE | the reference backend is PostgreSQL with typed columns (G-079); an embedded backend re-opens this row |
| H2 scalar domain | AUDITED | records enter only as SER-009 canonical UTF-8 bytes, compared as bytes, never as `text` ([L1]) |
| H2 encoding | AUDITED | open refuses a non-UTF8 database and sets `client_encoding` UTF8 itself (G-090) ([CW][P] D02/D03/D05, S11; [Pr] the environment); envelopes are `bytea`, so no server re-encoding ([IT]) |
| H2 NUL | AUDITED | PostgreSQL `text` cannot hold NUL (SQLSTATE 22021, Codex probe). `text` holds only CORE-001 tokens and canonical timestamps; `source_operation_id`, envelopes and mutations are `bytea` (CR-001) ([SC] NUL identity; [PT] a payload string containing U+0000 round-trips) |
| H2 length units | AUDITED | IDs and tokens are ASCII ([L1]) |
| H2 line endings | NOT_APPLICABLE | no text files are written |
| H3 normalization | NOT_APPLICABLE | no Unicode normalization (CORE-001 exact compare) |
| H3 case mapping/folding | AUDITED | `store_id` and `record_id` uniqueness is exact under C collation; open refuses a database whose collation or ctype is not C/POSIX (G-090) ([PT]; [CW][Pr] the environment) |
| H3 collation/sort | AUDITED | ordering is by `bigint` position only, never by text ([SC] pages); column and index collations are compared as catalog properties ([CW][P] C01–C06, I15) |
| H3 Unicode version | NOT_APPLICABLE | no Unicode tables |
| H3 lexical tokenization | NOT_APPLICABLE | no lexical retrieval |
| H4 representation | AUDITED | the store stamps the clock instant's canonical HIST-004 form; scenarios use `.ffffffZ` expectations and one offset-spelled clock instant (CR-002) ([SC] gapless) |
| H4 unknown vs present | AUDITED | `occurred_at` optional as in G-049 ([L2]) |
| H4 clocks | AUDITED | at most one sample per new-commit attempt, at step 12 under the lock; steps 1–11 (validation, retries, conflicts, store duplicates, capacity) never sample (G-085, G-086) ([SC] exact instants consumed; [CT] counting clock) |
| H4 ordering | AUDITED | `recorded_at` never orders records; position does (G-082, G-051) ([PT] a clock running backwards still yields ascending positions) |
| H4 leap seconds/DST | AUDITED | HIST-004 rejects `:60` ([L1]) |
| H5 map iteration | AUDITED | mutation and envelopes are canonical bytes ([L1]); catalog rows are compared as sorted OID-free tuples |
| H5 canonical key order | AUDITED | SER-009 ([L1]); member rows use PostgreSQL's canonical `jsonb` key order ([PIN]) |
| H5 sort stability and keys | AUDITED | pages are `ORDER BY position` on a primary key ([SC]) |
| H5 sets | NOT_APPLICABLE | no set-valued output in Layer 04 |
| H5 pagination | AUDITED | record-counted since-boundary pages may slice a committed batch; pages from 0 to the tail yield every record once ([SC] bounded-read; [PT] property test). P14 (`through` = min(since + limit, tail)) is equivalent only over certified gapless v1 state. Incremental bounded rebuild is DEFERRED to Layer 05 with ReplayCheckpoint, and container/target reads to the profile layers (G-087) |
| H6 YAML version / anchors / duplicate keys / big numbers / null vs missing / enforcement | AUDITED | corpus gate `mneme-process check` 8/8 ([L1]) |
| H7 algorithm and output | NOT_APPLICABLE | Layer 04 computes no hashes |
| H7 canonical form | AUDITED | retry identity compares normalized canonical draft bytes ([SC] retry and reorder steps; [IT] a retry from the other language) |
| H7 identity vs integrity | AUDITED | equal content under different IDs is two records (HIST-008) ([SC] no-semantic-dedup) |
| H8 SQLite version | NOT_APPLICABLE | PostgreSQL reference backend (G-079) |
| H8 server version | AUDITED | PostgreSQL major 14 only; any other major is `persistence.schema_incompatible` before any change (G-091) ([CW][Pr] the environment) |
| H8 isolation | AUDITED | commit locks the store row (`FOR UPDATE`) before steps 9–13; reads use one `REPEATABLE READ READ ONLY` snapshot for range check, entries and tail (CR-004) ([CT] reader loop during commits; [MU] P01 with the barrier witness, P04) |
| H8 crash points | AUDITED | one transaction per commit; [CT] kills the connection (`pg_terminate_backend`) before COMMIT and confirms no effect, then retries |
| H8 idempotency | AUDITED | `mneme_operation` primary key; [SC] retry; [CT] concurrent identical retries yield one physical commit and the same receipt |
| H8 JSONL | NOT_APPLICABLE | no JSONL backend |
| H8 durability | AUDITED | `synchronous_commit = on` asserted per connection ([PT] reads the setting) |
| H8 schema version and catalog | AUDITED | the open protocol and the complete v1 catalog contract: **see §3a** (this supersedes the earlier "10 damaged shapes" row) |
| H9 (all members) | NOT_APPLICABLE | no filesystem paths in WP-04; asset files are WP-04T (PERS-016) |
| H10 concurrent retry | AUDITED | [CT] N parallel identical commits → one physical commit, N equal receipts |
| H10 async enrichment | NOT_APPLICABLE | enrichment ordering is WP-04T (PERS-004); WP-04 provides only the receipt barrier |
| H10 cancellation | AUDITED | an attempt aborted after step 12 may have sampled the clock but persists nothing; a later retry may get a different instant (G-085) ([CT] rollback and `pg_terminate_backend` after the sample) |
| H11 ID lexical domain | AUDITED | CORE-001 for `store_id`, `record_id` ([L1]) |
| H11 version domain | AUDITED | `schema_version` per G-053 ([L2]) |
| H11 scope encoding | NOT_APPLICABLE | no MemoryScope in WP-04 |
| H11 reference integrity | AUDITED | `record_id` unique across the store and across profiles (G-083) ([SC] strict writer) |

## 3a. The v1 catalog trust boundary at open (CE-04-01, settled)

Spec anchors are `spec/persistence.md`, "Reference backend". Checkpoint anchors are
`assurance/convergence/CE-04-01-classification.md`. Every row is AUDITED from Python evidence at
`9d5a2d51`. [IT] is due at the Rust candidate.

| Surface | Spec / checkpoint | Python witnesses (kind) | Rust obligation |
|---|---|---|---|
| Open order: lock (shared key, explicit Read Committed), then environment, namespace, initialization, comparison, version row | "Open and initialize" 1–4; §5.1–5.2 | [T] X09/X10 (`granted = true`); [PT] concurrent and waiting first opens; [MU] P06, P48 | same order; [IT] mixed-language concurrent and waiting first opens |
| Environment: major 14, UTF8, C/POSIX, the handle's own UTF8 `client_encoding` | G-090, G-091; "Databases"; §5 | [Pr] `test_predicate_the_environment` (9); [P] D02/D03/D05, S11; [MU] P41–P43, P47 | the same predicate and controls |
| Genuine objects: every relation, type, function and operator `pg_catalog`-qualified; the temporary schema searched first (CE04-CP-001) | "Genuine observations"; §0, §5.2 | [E] CH12 poisoned session over open, initializer and operation texts; [E] private session; [P] CH07/CH07b, X06–X08, X11; [MU] P49–P54 | qualify Rust's own SQL texts; port CH12 over them |
| Initialization only with no `mneme_` non-index relation; settings pinned; postcondition before commit | "Open and initialize" 3; CE04-CP-002, CH11 | [P] CH09a–c (v1-name views and sequences); [T] pins and postcondition; [MU] P44–P46 | same |
| Structured comparison (G-091): relations, inheritance, policies, rules, triggers (8 internal RI, enabled, linked), columns, defaults, constraints, indexes | "v1 catalog contract", "Structured comparison"; §4, §5.3 | [P] `…refuses…` rows R/C/K/I/H and accept rows; [Pr] the 12 rev-2 predicates (R03, R30, R32, CH03, CH11, I15–I17); [F] `tgenabled`, `indisvalid`, `indisready`, table persistence, patched trigger/rule/policy/index/inheritance rows; [MU] P24 (all parts), P25–P37, P39 | port the row layouts (record 1 §2) and each witness class |
| Cached missing values on live columns are refused (CR-012). A rewrite that materializes the value into a row is not audited (E004, G-092). | "Columns", "Trust scope"; §8.2, §9.3 | [P] E002, E003, E005, E006, E110 refused; [P] E004 with its own oracle; [F] flag only, cached value only; [MU] P55, P68 | the same distinction; never treat E004 as protocol N |
| G-098 engine-generated fields: type copies checked against `pg_type`; `relnatts` and `relchecks` as invariants; offset cache and index descriptors pinned | the exclusions paragraph; §9.1–9.2 | [Pr] 28 G-098 cases; [F] type copy, `attcacheoff`, index descriptor; [Pr] residue positive control (E013); [MU] P65, P66 | consistency with the type, never literal bytes |
| `index_columns`: whole index-attribute rows | §9.2.2 | [Pr] 20 index-attribute cases; [F] index descriptor; [MU] P24-index_columns | same keying (table, backing constraint kinds, key names, attribute number) |
| Internal members: TOAST relations and indexes, their attributes, row and array types, each compared over every catalog column except a named exclusion list (CE04-CP-005) | "Internal members are certified"; §10.1–10.3 | [INV] every live column of `pg_class`, `pg_index`, `pg_attribute` and `pg_type` is compared or excluded, never both; [Pr] the member row layouts and the extra TOAST index; [F] TOAST options, ordering, operator class, uniqueness and persistence, row-type field, array backlink, extra TOAST index; [MU] P24-members, P67 | embed `MEMBER_EXCLUSIONS` and the normalizations (record 2 §1, §6); port the inventory test |
| Closed dependency island (CR-013, G-094, G-095): no recorded inbound edge except planner statistics (by dependent class); no outbound edge except the namespace and built-ins; no security label (G-097) | "Closed dependency island", "Security labels"; §8.1, §8.5.4 | [P] E021–E040, E057–E061, E088, E093, E094, E103–E108 (dependencies), E028/E050–E052/E097/E111/E112 (`FROM` triggers), E062/E109 (extension membership), CH14 refused; E020 (statistics), E033/E042 (no recorded dependency), E056 accepted; [Pr]/[F] security label; [MU] P56–P63 | the same structural island; [P] rows ported |
| Exemptions: names, OIDs, ownership and grants, column order, dropped residue, planner statistics, comments (G-097), and the closed engine-bookkeeping set (G-096) | the exclusions paragraph; §8.2–8.3 | [P] E011–E018, E046, R21/R22, C20–C22, CH08 accepted | same |
| Trust scope: open-time validation; references with no recorded catalog dependency, post-open out-of-band edits and stored-row audits are outside certification (G-092, G-094) | "Trust scope"; §8.4 CH17 | E004; E033/E042; CH17 (privileged, not refused) | the same scope; never a row scan |

## 4. Concurrency / order matrix

| Ordering guarantee | Realistic wrong implementation | Witness that kills it |
|---|---|---|
| commits are linearized; ranges are gapless and consecutive (G-084) | read tail, then insert without locking | [CT] 8 writers, all opened before a barrier, then 15 commits each: the union of ranges is exactly 1…240 with no gaps or overlaps ([MU] P01) |
| at most one physical commit per operation (G-084) | check-then-insert outside the lock | [CT] parallel identical retries, on separate handles and overlapping on one handle (CR-009) |
| conflicting mutations never last-write-wins | upsert on the operation key | [SC] conflict; [CT] parallel conflicting commits: exactly one wins, the others conflict |
| failed commits consume nothing (G-080, G-082) | allocate positions from a sequence | [SC] rejected-batch step; [CT] killed transaction |
| validation precedes every effect | append, then validate | [SC] mixed valid and invalid batch |
| the evaluation order of each operation (CR-003) | check store existence first | [SC] precedence pairs |
| idempotency, then store duplicates, then capacity, then clock (G-085, G-086) | sample the clock before the retry check | [SC] retries consume no instant; [PT] full-store retry |
| reads come from one snapshot containing whole commits only | separate Read Committed queries for tail and entries | [CT] reader loop during commits (CR-004) |
| retry check precedes the store record-ID check | check record IDs first, so a retry fails as a duplicate | [SC] identical retry returns the receipt |
| open: the lock before any inspection; inspection in an explicit Read Committed transaction | inspect, then lock; inherit the session's isolation | [CT] concurrent and waiting first opens, including under a Repeatable Read default ([MU] P05, P06) |
| open: environment before namespace before initialization; postcondition before commit; comparison parts in a fixed order | initialize, then check the environment; commit, then compare | [P] D02/D03/D05 (nothing created); [T] postcondition; the first mismatching part is reported ([Pr], [F]) |

## 5. Neighborhood expansion record

| Family | Members probed | Probe source | New rows / findings |
|---|---|---|---|
| H8 isolation and open | lock, isolation and inspection order × first, waiting and concurrent opens | [PT]; [MU] P05, P06 | the waiting-opener test was rewritten so the lock holder initializes while the waiter is blocked (contract review 3's witness) |
| H4 clocks | sampling order against steps 9–11 and aborts | [PT]; [MU] P02, P03, P16 | none |
| H7 canonical form | raw against normalized mutation, reordering | [SC]; [MU] P07, P20 | none |
| H5 pagination | `through` computation | [MU] P14 | equivalent under gaplessness over certified v1 state |
| H8 catalog trust boundary (CE-04-01) | the 136-row characterization (`0f7ac1bf`); Claude's challenge rows CH01–CH12 | Codex characterization; classification rev. 2 | WP04-CR-008 → G-089…G-092; CE04-CP-001…003 |
| H8 catalog: omitted live metadata and inbound linkage | the 112-row extension and the 85-field inventory (`d8262cf5`); the route ledger | Codex closure review 1 (`779a8f21`) and its extension | WP04-CR-012 (cached values), CR-013 (`FROM` triggers), CR-014 (P40 not equivalent; [F] method) → G-094…G-097; CE04-CP-004…007 → G-098 and the whole-row member rule |
| H8 catalog: overlapping parts | the old single-part witnesses after the new parts were added | gate run 3 (`426f14f3`, G4 failed) | single-part [Pr] and patched-row [F] witnesses; P31's bounded fetch kill (CR-015) |
| Bounded equivalents | P38 (the `confrelid` clause): inbound FKs always add in-scope RI triggers; P14 | closure reviews 1–2 | P38 holds only for that exact clause, in Codex's narrower scope; `FROM` triggers are refused independently by `boundary`; P14 holds only over certified gapless v1 state |

## 6. Verdict

```text
FEASIBILITY
    READY     every row AUDITED from Python evidence at 9d5a2d51, NOT_APPLICABLE or
              DEFERRED_WITH_REASON (G-087). [IT] cross-language witnesses are due at the Rust
              candidate and are NOT executed.
              Rust needs:
              - a draft admission mode over the certified Layer 02 gates (additive);
              - the PostgreSQL schema version 1 and the open protocol (shared key, explicit Read
                Committed, environment, namespace, initialization with pins and postcondition);
              - the v1 catalog validation from the contract and the shared pins only: structured
                parts, G-098 fields, index columns, whole-row members with the named exclusions,
                and the dependency island and labels;
              - genuine-object SQL;
              - the witness classes [P] [T] [E] [Pr] [F] [INV] [PIN];
              - the [CT] and [IT] tests.
```
