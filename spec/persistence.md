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
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [FND §foundation-level-clarifications] [R02 §11] [R04 §28] [R04 §33] [IAA §A10] [IAA §A15] [IAA §5]

A ReplayCheckpoint records at least: checkpoint ID; history-through boundary; model definition/
version; fitted-parameter identity/version; state snapshot; the schema/artifact/interpretation
boundaries (semantic dependencies) needed to interpret the snapshot; creation provenance/checksum.
It is never authoritative history; it is compatible only with the assumptions it declares; an
incompatible or stale checkpoint is ignored (never migrated by inventing meaning) and replay
continues from an earlier boundary or full history; deleting it cannot lose history; restore may
ignore it. The MVP need not create checkpoints, but storage and repository design must not
preclude them.

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
