# Shared Memory Core — DRAFT normalization

Conventions: `spec/README.md`. Profile for every requirement in this file: **core**, unless stated.

---

## ARCH — cross-cutting architecture

### ARCH-001 — Two primary proving profiles
<a id="arch-001"></a>
- **Profile:** core · **Source status:** FROZEN · **Sources:** [FND §executive-summary] [FND §1] [FND §G.7] [MVP §1] [MVP §2]

Mneme is a general durable memory substrate with two primary proving profiles: the Human Learning
Profile (first consumer: the Flashcard App) and the Agent Memory Profile (first consumer:
Minion-Agent). The profiles do not share one cognitive ontology; a small shared core holds
identity, provenance, durable history, scope, projections, retrieval, replay and persistence, and
each profile keeps its own semantics. The MVP does not require one universal memory object model.

### ARCH-002 — Shared-core admission rule
<a id="arch-002"></a>
- **Profile:** core · **Source status:** FROZEN · **Sources:** [FND §G.1] [FND §G.7] [IAA §A26] [MVP §18.4] [R00 §21]

A concept belongs in the shared core only when the Learning Profile and the Agent Memory Profile
can both consume it without weakening or distorting either profile. Reuse alone is not sufficient
justification. A shared term must not smuggle one profile's semantics into the other. Any shared
persistence/retrieval primitive must preserve the richer provenance needed by both profiles rather
than degrading one to fit the other.

### ARCH-003 — Profile namespaces; no universal Memory entity
<a id="arch-003"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [FND §G.1] [IAA §A27] [R00 §21] [MVP §18.4]

Learner-specific concepts remain in the Learning Profile and agent capture/consolidation/context
concepts remain in the Agent Memory Profile. Namespacing is preferred over artificially universal
entities. KnowledgeUnit, KnowledgeComponent, RecallForm, LearningEpisode, EvaluationOutcome,
MemoryEvidence, LearnerMemoryModel and SchedulingPolicy are learner-specific unless separately
promoted by the Foundation; implementation namespaces SHOULD make this explicit (`learning.*` or
equivalent), and existing public names MAY remain compatibility aliases during migration. Agent
Memory MUST NOT be forced into LearningEpisode, RecallForm, MemoryEvidence or SchedulingPolicy, and
the Flashcard App is not required to understand agent-memory entities.

### ARCH-004 — `MemoryModel` means the learner memory model
<a id="arch-004"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [FND §G.6] [MVP §18.2] [R02 §17]

`MemoryModel` in the learning documents is learner-specific. New code and normalized
specifications prefer `LearnerMemoryModel` or `learning.MemoryModel`; existing references may
remain as compatibility aliases. Its evidence and scheduling semantics are not imposed on the
Agent Memory Profile, which has retrieval/ranking/consolidation policies instead of a learner-state
model or spaced-review scheduler.

### ARCH-005 — Cross-profile analogies are not type aliases
<a id="arch-005"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [R05 §13] [R03 §28] [IAA §13]

Correspondences between Learning and Agent Memory concepts (e.g. LearningEvent ~
AgentMemoryObservation, exposure provenance ~ context fencing) are architectural analogies only.
They are not type aliases and do not authorize one profile to interpret the other's data. Agent
session events are not reclassified as learning events. Agent source observations are not
automatically interpreted as evidence about a human learner or fed into LearnerMemoryModel state.

### ARCH-006 — Knowledge, interaction, observation, inference and decision are separate layers
<a id="arch-006"></a>
- **Profile:** learning · **Source status:** FROZEN · **Sources:** [FND §3] [FND §19] [R00 §3] [R03 §3]

Knowledge ontology, learner-memory inference and observed performance are separate layers:
Knowledge is not learner state; observed performance is not learner state; current model state is
not historical source of truth. No layer may silently promote its output into the semantics of the
layer above or below it.

*Note:* placed in ARCH because every Learning family depends on it; its profile is learning.

### ARCH-007 — Capability seams, not a plugin runtime
<a id="arch-007"></a>
- **Profile:** core · **Source status:** GUARDRAIL · **Sources:** [IAA §A6] [IAA §6] [IAA §7] [IAA §9] [R04 §26] [FND §deliberately-not-frozen]

Replaceable capabilities expose explicit Definition → Provider → Consumer boundaries, implemented
with ordinary explicit dependency injection. Mneme does not adopt an everything-is-a-plugin
runtime, a general service-locator architecture, dynamic plugin loading, service registries or
hot-swappable provider discovery (rejected for the MVP). A universal plugin/provider runtime is
deliberately not frozen into the Foundation.

### ARCH-008 — Optional services are never on the authoritative critical path
<a id="arch-008"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [FND §1.1] [MVP §2] [MVP §18.4] [IAA §A14] [R04 §30] [R04 §39] [R00 §2]

Core memory operation requires no AI, cloud service or backend. Vector databases, embedding
providers, LLM extractors, remote sync, AI evaluators/diagnostics and dynamic plugin systems are
not mandatory to the core and must not block or endanger the local critical path; they may run
asynchronously and fail open. Canonical local history writes fail closed and visibly if durability
cannot be guaranteed.

### ARCH-009 — Persisted does not imply active
<a id="arch-009"></a>
- **Profile:** core · **Source status:** GUARDRAIL · **Sources:** [IAA §A5] [R04 §26] [R04 §30]

A persisted artifact is not automatically an input to inference, scheduling or retrieval policy.
Every durable derived artifact has explicit consumers and participation semantics.

### ARCH-010 — Durable domain events are separate from runtime events
<a id="arch-010"></a>
- **Profile:** core · **Source status:** GUARDRAIL · **Sources:** [IAA §A2] [R04 §26] [FND §App-F]

Durable domain events (e.g. LearningEvents, agent source observations) represent durable facts.
UI lifecycle events, timers, loading states, cache invalidation, renderer events and internal
coordination signals belong to a separate runtime event domain and are not automatically durable.

### ARCH-011 — Simplify behavior, not semantics
<a id="arch-011"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [MVP §1.1] [MVP §15] [FND §1] [R03 §26]

A feature may be deferred, but an implementation must not encode assumptions that contradict or
block the Foundation. If an MVP shortcut conflicts with a FROZEN Foundation principle, the
implementation changes. If implementation pressure exposes a genuine Foundation flaw, it is
recorded as a research/architecture issue and the Foundation is revised explicitly rather than
silently coded around. A general foundation does not imply a general MVP.

### ARCH-012 — Status labels and freeze policy
<a id="arch-012"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [FND §document-status-legend] [FND §E.1]

FROZEN decisions change only when new evidence materially falsifies or improves them; PROVISIONAL
decisions are designed for revision; RESEARCH CANDIDATE items are not implementation contracts;
MVP-ONLY items are deliberate Flashcard simplifications that must not be mistaken for the general
model. Taxonomies, naming vocabularies, canonicalization rules and model-specific state shapes stay
provisional unless evidence shows they are necessary and stable; status changes are explicit, never
silent.

### ARCH-013 — External standards are adapters
<a id="arch-013"></a>
- **Profile:** core · **Source status:** FROZEN · **Sources:** [FND §13] [MVP §10] [R00 §2.1]

External standards (QTI, xAPI, Caliper and similar) are adapters, not Mneme ontology. The internal
model must not depend on them; standards-based exports may be intentional projections.

---

## CORE — identity, version, provenance, lineage, operation identity

### CORE-001 — Opaque immutable identity
<a id="core-001"></a>
- **Profile:** core · **Source status:** FROZEN · **Sources:** [FND §16] [R00 §10] [R04 §7] [MVP §18.1]

Core IDs are opaque, stable, immutable and producer-generated (by the Knowledge producer, migration
adapter or other producing component). IDs must not encode mutable semantics.

*Note:* no source fixes an ID lexical form, alphabet, length or comparison rule (NF-010).

### CORE-002 — ID, key and version answer different questions
<a id="core-002"></a>
- **Profile:** core · **Source status:** FROZEN · **Sources:** [FND §16] [FND §8] [R00 §10] [R04 §7] [R04 §24]

The ID answers "which entity"; an optional key answers "how humans refer to it"; the version
answers "which edition". Keys, slugs, titles, paths and collection membership are mutable and are
not identity.

*Note:* "semantic version" ([MVP §18.1]) versus the integer editions shown in examples is not
defined by the sources (NF-011).

### CORE-003 — Same ID and same version imply identical content
<a id="core-003"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [FND §8] [R00 §10] [R01 §4] [R04 §7] [R04 §24]

Same ID + same version must imply semantically identical content. Differing (normalized) content
at the same ID and version is a conflict; it fails visibly and is never silently overwritten or
merged.

*Note:* every source states this for Knowledge entities. Whether it binds every versioned core
artifact (e.g. MemoryRecord) is not stated (NF-012). The content-hash normalization is unspecified
(NF-013).

### CORE-004 — Edits version; replacement, split and merge create identities with lineage
<a id="core-004"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [FND §4.6] [FND §14] [MVP §3] [R00 §10] [R01 §11]

Ordinary corrections/edits retain the ID and increment the version while semantic identity is
unchanged. Semantic replacement, split and merge create new IDs with lineage rather than
pretending to be a content edit. Old historical records remain unchanged.

### CORE-005 — Schema versions are distinct from artifact and model versions
<a id="core-005"></a>
- **Profile:** core · **Source status:** FROZEN · **Sources:** [FND §16] [R00 §13] [R01 §18] [R04 §16]

Schema versions (knowledge, event, evidence, package, backup format, database) and artifact/model
versions (KnowledgeUnit, KnowledgeComponent, RecallForm, Evaluator, EvidenceMapping, MemoryModel,
SchedulingPolicy, ...) are distinct concerns and evolve independently. A database schema version is
an implementation version.

### CORE-006 — Provenance capability
<a id="core-006"></a>
- **Profile:** core · **Source status:** FROZEN · **Sources:** [FND §8] [MVP §3] [MVP §18.1] [R00 §10] [R01 §12]

Every durable authored knowledge artifact must be able to carry provenance (producer/source,
generation method such as human/AI/import, creation/update time, source package, lineage and
correction metadata) sufficient for later audit or correction. Knowledge and derived artifacts can
record source/producer/generation/version information. Provenance is not learner evidence.

### CORE-007 — Producer provenance on interpretations
<a id="core-007"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [FND §8] [R03 §12] [FND §7.3]

Provenance identifies the producer, evaluator, evidence mapper or model and their versions where
relevant, so derived conclusions can be traced back toward the historical observations they rest
on. Provenance may be minimal in the MVP but the boundary must be preserved.

### CORE-008 — Lineage
<a id="core-008"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [MVP §18.1] [FND §G.1] [FND §G.2] [R01 §11]

Lineage (correction, supersession, split, merge, derivation) is a shared-core concept. Lineage
records relationships between identities; it never rewrites the records it relates.

### CORE-009 — Retired is not deleted
<a id="core-009"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [R00 §10] [R04 §7] [R04 §8] [R04 §24] [MVP §8]

Retirement is distinct from deletion. Retired entities remain addressable and interpretable for
historical records that reference them. Hard delete is an exceptional maintenance operation, not
normal evolution.

### CORE-010 — Large content is referenced, not duplicated
<a id="core-010"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [FND §8] [MVP §9] [R00 §4.6] [R03 §11]

Large assets are referenced by stable ID/version/checksum rather than duplicated into each event
or record when such a reference is sufficient for interpretation.

### CORE-011 — Integrity hashes where required
<a id="core-011"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [MVP §18.1] [R04 §7] [R01 §8] [R01 §9]

The shared core provides hashes/checksums where required: normalized content hashes for
same-version conflict detection and integrity hashes for assets and package entries.

*Note:* algorithm and canonical byte form are unspecified (NF-013).

### CORE-012 — Durable operation identity
<a id="core-012"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [MVP §18.1] [MVP §M2] [R00 §20.2] [R04 §32] [IAA §A18] [R05 §6] [R05 §14]

A canonical commit (a completed learner interaction, an agent source capture, or another canonical
history mutation) carries a durable operation identity (`operation_id`, submission identity or
durable source identity). Retrying the same operation identity must not create a second historical
record; a retry after a successful commit returns/reuses the existing result.

*Note:* the uniqueness domain of an operation identity, and the outcome when the same identity
arrives with different content, are not specified (NF-014).

### CORE-013 — Similarity is never identity
<a id="core-013"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [FND §G.4] [R01 §13] [R04 §36] [IAA §A23] [IAA §13] [R05 §5.5] [R05 §18]

Lexical or semantic similarity can produce candidates or warnings only. It never establishes,
merges or defines stable identity, and never bypasses scope.

---

## HIST — canonical history

### HIST-001 — Canonical history is authoritative; everything else is derived
<a id="hist-001"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [FND §App-F] [FND §foundation-level-clarifications] [IAA §A1] [MVP §18.1] [R00 §20.1] [R04 §26] [R04 §30]

Canonical durable history is the source of truth. Current state, diagnostics, summaries,
schedules, model state, checkpoints, indexes and projections are derived and rebuildable. A lossy
projection, summary, model state, checkpoint, diagnostic or semantic index never replaces canonical
history.

### HIST-002 — Typed, profile-owned canonical history
<a id="hist-002"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [FND §G.2] [MVP §18.1] [R04 §41.1]

The core provides typed canonical history primitives (`CanonicalHistory<T profile record>`); each
profile owns its history record types and payloads, which remain namespaced.

### HIST-003 — Deterministic episode event order
<a id="hist-003"></a>
- **Profile:** learning · **Source status:** FROZEN · **Sources:** [FND §6] [MVP §5.1] [IAA §A12] [R04 §9] [R04 §26] [R03 §5]

Events inside a LearningEpisode have a deterministic semantic sequence, assigned independently of
wall-clock timestamps. Semantic event order is explicit: wall-clock completion order or
asynchronous evaluator completion order must not silently define event meaning.

*Note:* the sources state this for episode events; its profile is therefore learning (kept in HIST
because the history envelope that carries it is core). They define no semantic order for other
history containers such as agent source observations, and none is implied here. A durable
per-store append order used for bounded reads is a separate, non-semantic concept (NF-016,
WP00-CR-007).

### HIST-004 — `occurred_at` and `recorded_at` are distinct
<a id="hist-004"></a>
- **Profile:** core · **Source status:** FROZEN · **Sources:** [FND §6] [MVP §5.1] [R04 §9] [R03 §5] [R05 §5.1]

The time something happened (`occurred_at`; for agent memory, source time) and the time it was
durably recorded or synchronized (`recorded_at`) are distinct, supporting offline-first capture and
later synchronization.

*Note:* representation, timezone and precision are unspecified (NF-015).

### HIST-005 — No global total order is assumed
<a id="hist-005"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [FND §App-E] [MVP §5.1] [R00 §6] [R04 §9]

No total global order across devices or episodes is assumed or required.

*Note:* bounded "since boundary" reads ([R04 §34]) need some durable ordering; how that coexists
with this rule is unspecified (NF-016).

### HIST-006 — History is append-only
<a id="hist-006"></a>
- **Profile:** core · **Source status:** FROZEN · **Sources:** [FND §8] [FND §14] [R03 §14] [R04 §9] [R04 §11] [R03 §26]

Normal behavior appends to canonical history and never mutates prior records in place. A
correction is a new record that references the original rather than an in-place edit.

### HIST-007 — Reinterpretation appends overlays
<a id="hist-007"></a>
- **Profile:** core · **Source status:** FROZEN · **Sources:** [FND §14] [FND §19] [IAA §A16] [MVP §6] [R03 §13] [R03 §27.4] [R04 §35]

Evolution adds interpretations; it never rewrites observation history. A later interpretation is
appended with derived_from / supersedes / reinterprets provenance identifying its producer and
version. Historical interpretations remain auditable. A "current preferred" interpretation is a
projection, not an in-place rewrite.

### HIST-008 — No semantic deduplication of canonical observations
<a id="hist-008"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [FND §foundation-level-clarifications] [MVP §M2] [R00 §20.5] [R00 §21] [R03 §27.3] [R04 §36] [IAA §A20] [IAA §A31] [R05 §16]

Canonical historical observations — learner events/observations and agent source observations —
are never semantically deduplicated or collapsed because their content is similar. Repeated learner
behavior is evidence. The only automatic historical deduplication allowed is idempotent retry of
the same durable operation identity (CORE-012). Derived artifacts (Knowledge duplicate candidates,
MemoryRecord consolidation) follow their own artifact-specific policies and never change this rule.

### HIST-009 — Durability barrier before lossy compaction
<a id="hist-009"></a>
- **Profile:** core · **Source status:** GUARDRAIL · **Sources:** [IAA §A13]

Any compaction, pruning or archival operation must first ensure that irrecoverable observations
and required historical context are durably persisted.

### HIST-010 — System-provided information keeps its origin
<a id="hist-010"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [FND §foundation-level-clarifications] [IAA §A7] [IAA §A30] [MVP §M4] [R03 §28] [FND §App-F]

Information the system itself provided (prompts, hints, answer reveals, sibling exposure, worked
examples, previously injected/recalled context) retains provenance so that a later outcome is not
misclassified as independent retrieval or as new independent evidence. The system records what it
exposed; it does not claim to know an internal cognitive source. Each profile owns its own
mechanism (OBS-006, ACTX-004).

---

## PROJ — projections

### PROJ-001 — One canonical projection path per history family
<a id="proj-001"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [FND §foundation-level-clarifications] [MVP §M3] [MVP §18.1] [IAA §A17] [R04 §31~2] [R02 §10] [R04 §40]

All downstream consumers obtain historical semantics through one shared normalization/projection
path per history family (for learning: the HistoryProjector reused by memory-model rebuild,
scheduler, diagnostics, backup/research export and audit tooling) rather than independently
decoding raw payloads. No subsystem may invent a second incompatible interpretation of history
envelopes. Unknown required semantics fail safely on that path.

### PROJ-002 — Purpose-specific projections
<a id="proj-002"></a>
- **Profile:** core · **Source status:** GUARDRAIL · **Sources:** [IAA §A11] [R04 §26] [FND §deliberately-not-frozen]

Different purposes (scheduling, diagnostics, progress UI, reporting, research, agent context)
derive different projections from the same history. There is no universal summary/profile blob;
a single global learner summary is deliberately not frozen.

### PROJ-003 — ProjectionBudget
<a id="proj-003"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [MVP §18.1] [R04 §38] [IAA §A22] [R05 §9]

A derived projection may declare a budget (time, bytes/characters/tokens, result count, plus
measured cost) and a degradation policy, budgeted by actual resource cost where feasible rather
than merely a fixed count. Degradation drops whole low-value layers/items rather than corrupting
semantic records by arbitrary truncation.

*Note:* cost units such as tokens are consumer/model-specific (NF-017).

### PROJ-004 — Budgets apply to projections, never to canonical storage
<a id="proj-004"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [R04 §38] [IAA §A22] [R05 §9]

Budgeting belongs to read/selection projections. Canonical records are never truncated to satisfy a
view budget; degradation applies only to the projection.

### PROJ-005 — Material projected context carries provenance
<a id="proj-005"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [MVP §18.1] [R05 §11] [IAA §A3]

Projected context that materially affects a consumer's behavior carries provenance sufficient to
explain or reconstruct it later.

---

## RET — retrieval primitives

### RET-001 — Identity first, discovery last
<a id="ret-001"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [FND §G.4] [MVP §18.1] [R00 §20.4] [R01 §14] [IAA §A9] [IAA §A23] [R05 §8]

Retrieval authority order: stable identity / explicit reference first; structured queries and
domain relations next; lexical and semantic retrieval only for candidate discovery. Discovery never
defines identity or truth.

### RET-002 — Indexes are rebuildable read models
<a id="ret-002"></a>
- **Profile:** core · **Source status:** GUARDRAIL · **Sources:** [R01 §14] [R04 §37] [R04 §41.1] [IAA §A23] [R05 §12]

FTS, lexical, vector and semantic indexes and embeddings are derived, rebuildable read models for
discovery. They may be absent, stale or rebuilt without changing identity, Knowledge, learner truth
or agent memory truth, and are never authoritative.

### RET-003 — Structured retrieval works without semantic indexing
<a id="ret-003"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [R05 §16] [R01 §15] [R01 §19] [R04 §40]

Exact and structured lookup continue to work with semantic indexing disabled or unavailable.

### RET-004 — Index loss never touches canonical data
<a id="ret-004"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [R04 §40] [R04 §41.1] [R04 §42] [R05 §14]

Deleting or rebuilding an index cannot delete or alter canonical history, Knowledge, source
observations or MemoryRecords, and cannot change MemoryRecord identity or lineage.

### RET-005 — Progressive disclosure
<a id="ret-005"></a>
- **Profile:** core · **Source status:** GUARDRAIL · **Sources:** [IAA §A21] [R01 §14] [R04 §37] [R03 §27.5] [R05 §8]

Reads SHOULD support Index → Context → Detail so consumers fetch full payloads only when needed;
canonical artifacts stay rich while read projections fetch the resolution the purpose requires.

### RET-006 — Shared index infrastructure keeps namespaces distinct
<a id="ret-006"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [R01 §21] [R02 §17] [R03 §27.5]

Shared retrieval infrastructure may index both Knowledge and Agent Memory, but namespaces, scopes
and stable identities remain distinct, and semantic search never substitutes for structured learner
state, stable Knowledge identity or learner truth.
