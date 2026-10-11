# Persistence, durability, bounded history and ReplayCheckpoint — DRAFT normalization

Conventions: `spec/README.md`. Production storage schemas are out of scope for WP-00; these are the
semantic persistence rules every backend must honor. Backend choice (SQLite, JSONL, ...) is not
semantic authority ([R05 §12]).

### PERS-001 — Persistence tiers
<a id="pers-001"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [R04 §3] [MVP §9] [R00 §13]

Durable/authoritative data (Tier A), rebuildable materialized state (Tier B) and disposable
runtime cache (Tier C) are distinct. Failure or deletion of Tier B/C data must never erase canonical
history or make authoritative data unrecoverable; Tier B must be reconstructable from Tier A plus
the selected model/configuration; derived caches may be deleted/rebuilt without deleting durable
history.

*Note:* R04's tier membership lists are learning-specific; the agent equivalents are AMEM-005.

### PERS-002 — Durability hierarchy
<a id="pers-002"></a>
- **Profile:** core · **Source status:** FROZEN · **Sources:** [FND §17] [FND §8] [R03 §17] [R00 §13]

Persist observations richly; persist interpretations lightly. Raw history has the strongest
historical authority and highest protection; historical interpretations (evaluations, evidence)
are highly valuable; model state, predictions, schedule state and caches are rebuildable.

### PERS-003 — Durable semantics, replaceable storage layout
<a id="pers-003"></a>
- **Profile:** core · **Source status:** FROZEN · **Sources:** [FND §17] [R04 §4] [R04 §5] [R04 §6] [R04 §24]

Conceptual separation does not require one table per concept; storage normalization is a
replaceable implementation detail and domain schemas are durable contracts. However, a generic
`entity(type, payload)` or `event(type, payload)` store must not be the only structure: stable
identity, foreign-key integrity, lifecycle state, version, provenance, checksums and high-value
query fields remain explicitly represented.

### PERS-004 — Durable capture precedes enrichment
<a id="pers-004"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [MVP §M1] [MVP §18.3] [R03 §27.1] [IAA §A24] [R04 §39] [R04 §41.3] [R05 §6]

The canonical local record (learner episode/event/observation transaction; agent source reference
and provenance) commits durably before any optional AI analysis, extraction, compression,
embedding, semantic indexing, remote sync or expensive diagnostics. Successful completion of the
user-facing action never depends on those optional services, and optional processing can be
retried without duplicating the canonical record.

### PERS-005 — Transactions and crash safety
<a id="pers-005"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [R04 §18] [R04 §22] [R04 §14]

Canonical writes are crash-safe: either transactional with any immediate derived update, or
ordered so derived state can be rebuilt after interruption. If a history append succeeds but a
cache update fails, history wins and the cache is repaired/rebuilt. Multi-row semantic operations
(e.g. Knowledge import) are never visible half-applied.

### PERS-006 — Idempotent commit per operation identity
<a id="pers-006"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [R04 §32] [R04 §40] [IAA §A18] [R05 §14]

The persistence transaction enforces at most one committed historical mutation per durable
operation identity (CORE-012). Crash/retry after a successful commit returns/reuses the existing
result instead of creating duplicate history or evidence.

### PERS-007 — Bounded and incremental history access
<a id="pers-007"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [MVP §M5] [MVP §18.1] [R02 §10] [R04 §34] [IAA §A19] [R04 §40]

Repository interfaces must not assume full history fits in memory. They support pagination/ranges,
since-boundary reads, reads by container (e.g. episode) and by target, and compatible-checkpoint
plus incremental tail rebuild. Full replay remains the correctness fallback, not the normal runtime
path for long-lived datasets; bounded replay of a deterministic projection must equal full replay.

### PERS-008 — HistoryBoundary
<a id="pers-008"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [FND §G.2] [R04 §41.1] [MVP §M5]

HistoryBoundary is a shared-core concept: a declared position in canonical history up to which a
derived artifact (checkpoint, derived state) was computed.

*Note:* its representation depends on the unresolved ordering question (NF-016).

### PERS-009 — ReplayCheckpoint is an accelerator, never authority
<a id="pers-009"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [FND §foundation-level-clarifications] [R04 §28] [R04 §41.1] [R05 §12] [IAA §A10] [IAA §A15] [IAA §5]

A ReplayCheckpoint is a rebuild accelerator for one declared derived family. It records at least:
checkpoint ID; the history-through boundary it summarizes; the declared profile and the derived
model/projection/index family (with its definition version) it belongs to; the derived-state
snapshot; the semantic dependencies required to interpret that snapshot; creation
provenance/checksum. It is never authoritative history; it is compatible only with the
dependencies it declares; an incompatible or stale checkpoint is ignored (never migrated by
inventing meaning) and replay continues from an earlier boundary or full history; deleting it
cannot lose history; restore may ignore it. The MVP need not create checkpoints, but storage and
repository design must not preclude them.

*Note:* the dependencies are family-specific. The learner-model specialization (model
definition, fitted parameters, Knowledge/event/evidence boundaries) is LMEM-015; a deterministic
agent projection/index family has no fitted learner parameters and must not be required to invent
them (WP00-CR-006).

### PERS-010 — Checkpoint replay equivalence
<a id="pers-010"></a>
- **Profile:** core · **Source status:** GUARDRAIL · **Sources:** [IAA §5] [R04 §40]

A deterministic model replaying a compatible checkpoint plus the subsequent events must reproduce
a state equivalent to full replay.

### PERS-011 — Checkpoints never cross profiles
<a id="pers-011"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [R04 §41.1] [R05 §12]

A ReplayCheckpoint is tied to a declared profile/model/projection family and cannot be applied
across profiles merely because storage formats match. It may accelerate rebuild of a derived
projection/index family but never substitutes for source observations or records.

### PERS-012 — Domain repositories; append semantics for history
<a id="pers-012"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [R04 §11] [R04 §19]

Application code depends on domain-oriented persistence interfaces. History persistence exposes
append semantics, not generic update semantics. No generic "save everything" operation may blur
authored-artifact writes, append-only history and rebuildable derived state into one operation.

### PERS-013 — Local-first
<a id="pers-013"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [R01 §15] [R02 §13] [R04 §39] [R04 §20]

The local canonical store serves current use (review, scheduling, lookup, durable commits).
Remote sync, embeddings, cloud services and AI processing may refresh asynchronously and must not
block local reads or use; network failure leaves local operation functional.

### PERS-014 — Shared physical storage keeps profile identity explicit
<a id="pers-014"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [R04 §41.1] [R03 §28] [IAA §A27]

Stable IDs/version/provenance/lineage/integrity metadata may share physical persistence libraries
or schemas only when profile/type identity remains explicit in serialization and replay. Physical
co-location is allowed; semantic ownership is not collapsed.

### PERS-015 — Concurrency assumption
<a id="pers-015"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [R04 §18] [R03 §24]

The MVP assumes one local active writer unless a platform requires otherwise. Future sync must not
be simulated with unsafe last-write-wins over history; cross-device merge semantics are not in the
MVP.

### PERS-016 — Asset write integrity
<a id="pers-016"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [R04 §18]

Asset file writes use staging/rename or equivalent integrity checks so persisted references never
point to half-written files.

---

## Layer 04 canonical history store contract (WP-04)

Owner G-077…G-087 (`reference/governance/2026-10-11-owner-layer04-start.md`), with G-013, G-031,
G-033, G-051, G-054 and G-055. The contract is **backend-neutral** (G-079): it fixes repository
semantics only. The PostgreSQL reference backend and its shared schema are at the end of this
section.

### Store, backend and writer

- **Store.** A *store* is one logical canonical history store, identified by a CORE-001 `store_id`.
  - It may hold records of any profile; each record's `profile` stays explicit (PERS-014).
  - A new store is empty, with tail position 0.
  - Committed records receive **gapless store-local positions** 1, 2, 3, …, which are permanent and
    never reused or reassigned (G-080). The largest position is MAX = 2^53−1 (G-054, G-086).
  - Positions are a store-local cursor, never a global, causal or cross-device order (G-051).
- **Backend handle.** An implementation opens a *backend handle* (for the reference backend, a
  database) with an injectable **clock**. The clock is a callable `clock(store_id)` that yields a
  HIST-004 timestamp; the store stamps that instant's **canonical** HIST-004 form (G-082). A clock
  that yields a value HIST-004 rejects is a defect of the clock, not a store outcome. Opening is
  per-language API; the reference backend's open rule is at the end of this section.
- **Writer.** A *writer* declares its schema as a Layer 02 replay reader `{profile, recognized}`
  (G-053 rules).
- **Append-only API (PERS-012).** The repository exposes exactly four operations: `create_store`,
  `commit_history`, `read_history` and `store_tail`. There is no update, delete or generic save
  operation, and stores are never deleted through this API.

### Arguments, seams and errors (all four operations)

- Every argument is a public structured input. `store_id` is a value (a CORE-001 ID), not a handle;
  it is validated like every other argument.
- Each structured argument is accepted either as a native value or as JSON text (the Layer 01
  seams), and the evaluation order below is the same for both.
- **Generic stages first (G-031).** Stage 1 (decoding) and stage 2 (value domain) run across all
  arguments in declared order before any stage-3 check; the first failure reports.
- Every Layer 04 error names its argument where the list below gives one, and **never carries a
  position** (the Layer 03 entry position does not apply to store operations).

### `create_store(store_id)`

1. Generic stages over `store_id`.
2. `store_id`: CORE-001, else `id.invalid` (argument `store_id`).
3. If the backend already holds the store: `persistence.store_exists` (argument `store_id`).
4. Otherwise an empty store (tail 0) is durably created.

### `store_tail(store_id)`

1. Generic stages; 2. `store_id` as above; 3. unknown store: `persistence.store_unknown`
(argument `store_id`).
4. Returns the HistoryBoundary `{store_id, position}` of the last committed record (0 if empty).

### `commit_history(store_id, writer, operation, records)`

`operation` is a CORE-012 operation identity `{source_namespace, source_operation_id}` (G-032,
G-033). `records` is a non-empty array of **record drafts**: history envelopes *without*
`recorded_at`, which callers never supply (G-082).

**Draft admission (G-083, over G-055).** A draft passes the four Layer 02 gates exactly as an
envelope does, by the writer's reader, with one difference: the closed member set of a recognized
draft is the envelope's set **minus `recorded_at`**.
- **D1, identity and routing:** as gate 1 (`history.envelope_invalid`).
- **D2, admission and recognition:** `excluded`, `skip` and `history.unknown_required` are reader
  outcomes, not acceptable writes; each is **`persistence.record_unrecognized`**. A missing or
  invalid `compatibility` on an admitted draft is `history.envelope_invalid`, as in gate 2.
- **D3, closed shape:** an unknown member — **including a supplied `recorded_at`** — or a missing
  `record_id` is `history.envelope_invalid`.
- **D4, typed fields** in canonical member order (G-034): `occurred_at` gives `timestamp.invalid`,
  `record_id` gives `id.invalid`.
- The normalized draft is the draft with `occurred_at` in canonical HIST-004 form and all values as
  normalized SER-008 values.
- Profile-owned payload validation joins D4 once a profile defines it (Layers 07+ and 13+).

**Order of evaluation.** The first failure reports, and every failure has no effect at all
(PERS-005):
1. Generic stages across `store_id`, `writer`, `operation`, `records`, in that order.
2. `store_id`: CORE-001, else `id.invalid` (argument `store_id`).
3. `writer`: a valid reader, else `history.reader_invalid` (argument `writer`).
4. `operation`: valid, else `operation_identity.invalid` (argument `operation`).
5. `records`: a non-empty array, else `persistence.batch_invalid` (argument `records`).
6. Each draft in array order through D1–D4 (argument `records`).
7. Two drafts with the same `record_id`: `history.duplicate_record_id` (argument `records`).
8. Unknown store: `persistence.store_unknown` (argument `store_id`).

Steps 9–13 run under the store's **single serialization boundary** (G-084), atomically and
linearized with every other commit to the store:

9. **Idempotency.** If the store has committed `operation` before, compare the **mutation**: the
   SER-009 canonical bytes of the array of normalized drafts, in order (G-082). The writer is not
   part of the mutation; reordered drafts are a different mutation.
   - Equal: return the **original receipt** unchanged. Nothing is appended and the clock is not
     sampled, even if the store is now full (G-086).
   - Different: `persistence.operation_conflict` (argument `operation`), never last-write-wins
     (G-013). The clock is not sampled (G-085).
10. A draft whose `record_id` already exists in the store, under any profile or operation:
    `history.duplicate_record_id` (argument `records`) (G-083).
11. **Capacity.** With K drafts, if K > MAX − tail: `persistence.store_full` (no argument). No
    clock sample, no position, no receipt, no record (G-086).
12. **Clock.** Sample the clock once; its canonical instant is `recorded_at` for every record of
    the batch.
13. Assign positions `tail+1 … tail+K` in draft order (G-080); append the stamped envelopes; persist
    the receipt; advance the tail; make the transaction durable; return the receipt.

- **Durability barrier.** The receipt is returned only after the batch is durable: the
  **committed durability barrier** (HIST-009, PERS-004) that WP-04T consumes.
- **Aborts (G-085).** An attempt that aborts or crashes after step 12 may have sampled the clock;
  the sampled instant has no semantic status and nothing is persisted (no `recorded_at`, position,
  receipt or record). Steps 1–11 never sample. A later attempt may sample a different instant;
  only the successful commit's instant becomes canonical.
- **Concurrent identical retries** produce exactly one physical commit; every caller gets the same
  receipt (G-084).

**Receipt** (a closed record):

```text
{"store_id": ..., "operation": {source_namespace, source_operation_id},
 "first_position": <int>, "last_position": <int>, "recorded_at": <canonical timestamp>,
 "records": [<the committed envelopes, in position order>]}
```

### `read_history(store_id, since, limit)`

**Order of evaluation:**
1. Generic stages across `store_id`, `since`, `limit`, in that order.
2. `store_id`: CORE-001, else `id.invalid` (argument `store_id`).
3. `since`: a valid HIST-005 HistoryBoundary, else `history.boundary_invalid` (argument `since`).
4. `limit`: an integer from 1 to MAX, else `persistence.limit_invalid` (argument `limit`).
5. Unknown store: `persistence.store_unknown` (argument `store_id`).
6. Against **one read snapshot** (below): `since.store_id` other than `store_id` is
   `history.boundary_incomparable` (argument `since`) (G-051); `since.position` greater than the
   snapshot tail is `history.boundary_invalid` (argument `since`).

**Result:** `{"entries": [{"position", "record"}...], "through": <HistoryBoundary>,
"tail": <HistoryBoundary>}`:
- `entries`: the committed records with positions greater than `since.position`, ascending, at
  most `limit` of them.
- `through`: the boundary at the last returned position, or `since` if none was returned.
- `tail`: the snapshot's tail.

**Snapshot and paging (PERS-005, PERS-007):**
- The range check, `entries`, `through` and `tail` all come from **one consistent snapshot** of
  committed history. A snapshot contains each commit entirely or not at all; it never contains
  part of an in-progress or aborted commit. So `through ≤ tail` always holds.
- `limit` counts **records**. A page may end inside a committed batch; the next page, read from its
  `through`, continues with the rest. Slicing a committed batch across pages is not partial
  visibility.
- Reading pages from boundary 0 until `through` equals `tail` yields every record exactly once, in
  position order.

### No semantic deduplication (HIST-008)

The store never merges or drops records because their content is equal or similar. Records with
different `record_id`s are always distinct. The only automatic deduplication is the idempotent
retry of one operation identity (PERS-006).

### PERS-007 decomposition (G-087)

| Part of PERS-007 | Owner |
|---|---|
| bounded since-boundary paging over physical committed history | **WP-04** (this contract) |
| memory-bounded incremental rebuild: checkpoint plus tail, an incremental projector | **Layer 05** with ReplayCheckpoint (PERS-009…011) |
| reads by container (e.g. an episode) or by target | **the profile layers** that define those concepts; any index is a derived, rebuildable read model, not canonical-store semantics |

### Scenario and test seams

- **Scenario runs.** Layer 04 conformance scenarios are stateful: each scenario runs its steps in
  order against one fresh backend with no stores.
- **Clock fixtures.** A `create_store` step's `clock` is runner configuration, not an argument: the
  finite list of instants the runner's clock yields, in order, for commits to that store. Each
  new-commit attempt that reaches step 12 consumes one (G-085).
- **JSON seams.** A step may give a structured argument `<name>` as JSON text in `<name>_json`.
- **Backends.** The corpus is backend-neutral (G-079). Each implementation runs it against every
  backend it ships, and certification requires the PostgreSQL reference backend.
- **Outside the corpus.** Crash, abort, concurrency, capacity (G-086; 2^53 records cannot be
  written) and cross-language interoperability are proven by implementation tests listed in the
  WP-04 feasibility matrix.

### Reference backend: PostgreSQL shared schema (G-079, G-081)

Both languages implement the store on one PostgreSQL schema, so a store written by either is
readable and retryable by the other. Schema version 1, normative for the reference backend:

```sql
CREATE TABLE mneme_schema    (singleton boolean PRIMARY KEY DEFAULT true CHECK (singleton),
                              version integer NOT NULL);
CREATE TABLE mneme_store     (store_id text PRIMARY KEY,
                              tail bigint NOT NULL DEFAULT 0
                                   CHECK (tail BETWEEN 0 AND 9007199254740991));
CREATE TABLE mneme_record    (store_id text NOT NULL REFERENCES mneme_store,
                              position bigint NOT NULL
                                   CHECK (position BETWEEN 1 AND 9007199254740991),
                              record_id text NOT NULL,
                              profile text NOT NULL, record_type text NOT NULL,
                              schema_version bigint NOT NULL,
                              envelope bytea NOT NULL,             -- SER-009 canonical bytes
                              PRIMARY KEY (store_id, position),
                              UNIQUE (store_id, record_id));
CREATE TABLE mneme_operation (store_id text NOT NULL REFERENCES mneme_store,
                              source_namespace text NOT NULL,
                              source_operation_id bytea NOT NULL,  -- exact UTF-8 bytes (G-033)
                              mutation bytea NOT NULL,             -- SER-009 bytes, normalized drafts
                              first_position bigint NOT NULL, last_position bigint NOT NULL,
                              recorded_at text NOT NULL,           -- canonical HIST-004
                              PRIMARY KEY (store_id, source_namespace, source_operation_id));
```

- **Text columns** hold only CORE-001 tokens (`store_id`, `record_id`, `profile`, `record_type`,
  `source_namespace`) and canonical timestamps: ASCII, never NUL. Everything else that is an
  arbitrary SER-008 string is in `bytea`: `source_operation_id` as its exact UTF-8 bytes (so
  `"\u0000"` is representable and equality is bytewise, per G-033), and envelopes and mutations as
  canonical bytes.
- **Commit.** One transaction that first locks the store row (`SELECT … FOR UPDATE`); that lock is
  the serialization boundary. Steps 9–13 run under it, and the transaction commits with
  `synchronous_commit = on`.
- **Read.** One `REPEATABLE READ READ ONLY` transaction (or a single statement) supplies the
  snapshot for step 6, the entries and the tail.
- **Columns.** `profile`, `record_type` and `schema_version` repeat the envelope's routing triple
  for queries (PERS-003, PERS-014). The receipt is rebuilt from `mneme_operation` and the records
  in its range.
- **Open and initialize.** Every open, initializing or not, runs in one transaction whose **first
  statement** is `SELECT pg_advisory_xact_lock(-4695452043516644990)`: the single-`bigint` overload
  with the shared **schema-open key**. The key is the first 8 bytes of SHA-256 of the ASCII text
  `mneme.schema.open.v1` (`bed6673e764ef182`), read as a big-endian signed 64-bit integer. Both
  languages use exactly this key; no other key or overload may stand in for it (WP04-CR-007). The
  lock is held until the transaction ends. Under it:
  - if no `mneme_` table exists, the transaction creates schema version 1 (the DDL above plus the
    one `mneme_schema` row) and commits;
  - otherwise it requires exactly the four tables and one `mneme_schema` row with version 1;
    anything else fails the open with `persistence.schema_incompatible` and changes nothing.
- **Databases.** Created with `TEMPLATE template0 ENCODING 'UTF8' LC_COLLATE 'C' LC_CTYPE 'C'`, so
  text comparison is bytewise and independent of the host locale. Test databases live in the
  tablespace from G-081.
