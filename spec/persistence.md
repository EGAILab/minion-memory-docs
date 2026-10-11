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

Owner G-077…G-084 (`reference/governance/2026-10-11-owner-layer04-start.md`), with G-013, G-047, G-051 and G-054. The contract is
**backend-neutral** (G-079): it fixes repository semantics only. The PostgreSQL reference backend
and its shared schema are at the end of this section.

### Store and writer

- **Store.** A *store* is one logical canonical history store, identified by a CORE-001 `store_id`.
  - It may hold records of any profile; each record's `profile` stays explicit (PERS-014).
  - A new store is empty, with tail position 0.
  - Committed records receive **gapless store-local positions** 1, 2, 3, …, which are permanent and
    never reused or reassigned (G-080).
  - Positions are a store-local cursor, never a global, causal or cross-device order (G-051).
- **Writer.** A *writer* declares its schema as a Layer 02 replay reader `{profile, recognized}`
  (G-053 rules).
- **Append-only API (PERS-012).** The repository exposes only `commit_history`, `read_history` and
  `store_tail`. There is no update, delete or generic save operation.

### `commit_history(store, writer, operation, records)`

**Arguments:**
- **`operation`** is a CORE-012 operation identity (G-032/G-033).
- **`records`** is a non-empty array of **record drafts**. A draft is a closed history envelope
  *without* `recorded_at`:
  `{record_id, profile, record_type, schema_version, compatibility, occurred_at?, payload?, provenance?}`.
  Callers never supply `recorded_at` (G-082).

**Validation** happens before any effect, and every failure rejects the whole batch with no
effect (PERS-005):
1. **Generic stages** run across `writer`, `operation` and `records` (G-031).
2. **Writer.** `writer` must be a valid reader, else `history.reader_invalid`.
3. **Operation.** `operation` must be valid, else `operation_identity.invalid`.
4. **Batch.** `records` must be a non-empty array, else `persistence.batch_invalid`.
5. **Each draft, in batch order** (G-083), is admitted through the Layer 02 gates (G-055) by the
   writer's reader, as the envelope it would become. A draft that already carries `recorded_at` is
   `history.envelope_invalid`.
   - Envelope, typed and generic errors keep their codes.
   - An outcome other than `decode` is `persistence.record_unrecognized`: `excluded` (a foreign
     profile), `skip`, or `history.unknown_required`. Write outcomes are strict; reader outcomes
     are not acceptable writes.
   - Profile-owned payload validation applies once a profile defines it (Layers 07+ and 13+).
6. **Repeated IDs.** Two drafts in one batch with the same `record_id` are
   `history.duplicate_record_id`.

Errors name their argument: `writer`, `operation` or `records`.

**Commit** happens under the store's single serialization boundary (G-084). The steps are atomic
and linearized with every other commit to the store:
- **Already committed operation.** If the store has already committed `operation`, its
  **mutation** is compared: the SER-009 canonical bytes of the submitted draft array, in order,
  excluding everything store-generated (G-082).
  - Equal: the **original receipt** is returned unchanged, and nothing is appended.
  - Different: `persistence.operation_conflict`, a visible conflict that is never last-write-wins
    (G-013).
- **New operation.** Otherwise:
  - any draft whose `record_id` already exists in the store, under any profile or operation, is
    `history.duplicate_record_id` (G-083);
  - the store samples its **clock once**, giving one canonical HIST-004 `recorded_at` for the
    whole batch;
  - it assigns the consecutive positions `tail+1 … tail+n` in draft order (G-080);
  - it appends the stamped envelopes and persists the receipt.
- **Receipt.** The commit returns the **receipt** only after the batch is durable. That is the
  **committed durability barrier** (HIST-009, PERS-004) that WP-04T consumes.
- **Failed or aborted commits** persist nothing: no position, no timestamp, no receipt (G-082).
- **Concurrent identical retries** produce exactly one physical commit, and every caller gets the
  same receipt (G-084).

**Receipt** (a closed record):

```text
{"store_id": ..., "operation": {source_namespace, source_operation_id},
 "first_position": <int>, "last_position": <int>, "recorded_at": <canonical timestamp>,
 "records": [<the committed envelopes, in position order>]}
```

### `read_history(store, since, limit)`

- **Arguments.**
  - `since` is a HistoryBoundary. Its `store_id` must be this store's, else
    `history.boundary_incomparable` (G-051).
  - Its `position` must not exceed the tail, else `history.boundary_invalid`.
  - `limit` is an integer from 1 to 2^53−1, else `persistence.limit_invalid`.
- **Result.** `{"entries": [{"position", "record"}...], "through": <HistoryBoundary>,
  "tail": <HistoryBoundary>}`.
  - `entries` holds the committed records with positions greater than `since`, ascending, at most
    `limit` of them.
  - `through` is the boundary at the last returned position, or `since` if none was returned.
  - `tail` is the store's tail at read time.
- **No partial batches.** A read never observes part of a batch.
- **Bounded replay (PERS-007).** Reading in pages from boundary 0 and projecting
  (`project_history`) equals projecting one full read.

### `store_tail(store)`

Returns the HistoryBoundary `{store_id, position}` of the last committed record, or position 0 for
an empty store.

### No semantic deduplication (HIST-008)

The store never merges or drops records because their content is equal or similar. Records with
different `record_id`s are always distinct. The only automatic deduplication is the idempotent
retry of one operation identity (PERS-006).

### Clock and test seams

The store's clock is injectable (G-082). A conformance scenario declares a store with a fixed
sequence of clock instants; each *new* commit consumes exactly one. Retries and failed commits
consume none.

### Reference backend: PostgreSQL shared schema (G-079, G-081)

Both languages implement the store on one PostgreSQL schema, so a store written by either is
readable by the other. Schema version 1, normative for the reference backend:

```sql
CREATE TABLE mneme_schema   (version integer NOT NULL);
CREATE TABLE mneme_store    (store_id text PRIMARY KEY, tail bigint NOT NULL DEFAULT 0);
CREATE TABLE mneme_record   (store_id text NOT NULL REFERENCES mneme_store,
                             position bigint NOT NULL, record_id text NOT NULL,
                             profile text NOT NULL, record_type text NOT NULL,
                             schema_version bigint NOT NULL,
                             source_namespace text NOT NULL, source_operation_id text NOT NULL,
                             envelope bytea NOT NULL,            -- SER-009 canonical bytes
                             PRIMARY KEY (store_id, position),
                             UNIQUE (store_id, record_id));
CREATE TABLE mneme_operation (store_id text NOT NULL REFERENCES mneme_store,
                             source_namespace text NOT NULL, source_operation_id text NOT NULL,
                             mutation bytea NOT NULL,            -- SER-009 bytes of the draft array
                             first_position bigint NOT NULL, last_position bigint NOT NULL,
                             recorded_at text NOT NULL,
                             PRIMARY KEY (store_id, source_namespace, source_operation_id));
```

- **Commit.** One transaction that locks the store row first (`SELECT … FOR UPDATE`). That is the
  serialization boundary, and the transaction runs with `synchronous_commit = on`.
- **Columns.** `profile`, `record_type` and `schema_version` repeat the envelope's routing triple
  for queries (PERS-003, PERS-014).
- **Databases.** Created with `TEMPLATE template0 ENCODING 'UTF8' LC_COLLATE 'C' LC_CTYPE 'C'`, so text
  comparison is bytewise and independent of the host locale. Test databases live in the tablespace from
  G-081.
