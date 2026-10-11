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

**Layer 01 contract (Owner G-020):** a stable ID is an ASCII token of 1–128 bytes.
- **Characters.** It begins with `a`–`z` or `0`–`9` and continues only with `a`–`z`, `0`–`9`, `.`,
  `_` and `-`. It must not end with `.`.
- **Reserved names.** Its basename must not be a Windows reserved device name (`con`, `prn`, `aux`,
  `nul`, `com1`–`com9`, `lpt1`–`lpt9`). This holds whether the name stands alone or carries an
  extension-like suffix, so `con` and `con.x` are both invalid.
- **Comparison.** IDs are compared byte for byte. No Unicode normalization or case folding is ever
  part of stable-ID identity. Human-readable Unicode belongs in titles, labels and source keys, not
  in stable IDs.
- **Path projection.** A package path such as `memories/<id>.md` is a deterministic projection of
  the stable ID, not a second identity namespace.

*Note:* resolves NF-010 by Owner decision G-020
(`reference/governance/2026-10-10-owner-layer01-decisions.md`).

### CORE-002 — ID, key and version answer different questions
<a id="core-002"></a>
- **Profile:** core · **Source status:** FROZEN · **Sources:** [FND §16] [FND §8] [R00 §10] [R04 §7] [R04 §24]

The ID answers "which entity"; an optional key answers "how humans refer to it"; the version
answers "which edition". Keys, slugs, titles, paths and collection membership are mutable and are
not identity.

**Layer 01 contract (Owner G-012):** an artifact version is a positive integer edition
(1 ≤ v ≤ 2^53−1, the SER-008 integer domain), compared numerically. Zero, negatives, non-integers
and values outside the domain are invalid versions.

*Note:* resolves NF-011 by Owner decision G-012
(`reference/governance/2026-10-10-owner-layer01-decisions.md`); the integer bound follows G-016.

### CORE-003 — Same ID and same version imply identical content
<a id="core-003"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [FND §8] [R00 §10] [R01 §4] [R04 §7] [R04 §24]

Same ID + same version must imply semantically identical content. Differing (normalized) content
at the same ID and version is a conflict; it fails visibly and is never silently overwritten or
merged.

**Layer 01 contract (Owner G-021):** the rule is core-wide, scoped to **immutable
semantically versioned artifacts**.
- **Uniqueness.** For every artifact whose `(stable_id, artifact_version)` denotes an immutable
  semantic revision, that pair resolves to exactly one canonical content value.
- **Conflict.** The same pair with different canonical content (SER-009 bytes of the artifact
  type's semantic-content projection) is a visible conflict. Implementations must not silently
  overwrite, merge, normalize it away or choose one side.
- **Exclusions.** The rule does not apply merely because something carries a `schema_version`,
  `model_version`, `database_schema_version` or checkpoint-format version.
- **Per-type projection.** Each artifact type defines its canonical semantic-content projection.
  Mutable counters, access history, reinforcement/retrieval observations and derived state
  normally live outside the immutable versioned artifact, rather than mutating it under the same
  version.

**Layer 01 comparison (observation of G-021).** Two artifact revisions are compared
on `(stable_id, artifact_version, semantic-content projection)`:
- **Not applicable.** If either revision has no `artifact_version`, the rule does not apply. A
  `schema_version`, model version or format version alone never invokes it.
- **Distinct.** Different `stable_id` or different `artifact_version` (CORE-002 numeric comparison).
- **Identical.** Same `stable_id` and `artifact_version`, and the projections have equal SER-009
  canonical bytes. Equivalent numeric spellings are therefore identical (G-023).
- **Conflict.** Same `stable_id` and `artifact_version` with different canonical bytes. It is
  reported as the visible error `artifact.revision_conflict` and is never resolved by overwrite,
  merge, normalization or choosing a side.

The projection is supplied by the artifact type. Persistence and commit behaviour are later
layers; Layer 01 fixes only this comparison.

**Revision record (Owner G-035):** each compared input is a closed record
`{stable_id, projection, artifact_version?}`.
- **Shape.** `stable_id` and `projection` are required and `artifact_version` is optional. A
  non-object input, a missing required member or any other member is `artifact.revision_invalid`
  (stage 3).
- **Fields after shape.** Only once the shape is valid are the present typed fields validated, in
  the canonical member order (G-034):
  - an invalid `artifact_version` is `version.invalid`;
  - an invalid `stable_id` is `id.invalid`;
  - `projection` carries no typed rule.
- **Generic errors.** Values failing the generic domain remain stage-2 errors.
- **Not applicable.** `not_applicable` is reached only after the complete record has validated: an
  absent `artifact_version` never bypasses the missing-member or extra-member checks.

*Note:* every source states this for Knowledge entities. NF-012 is resolved by G-021. The
content-hash normalization is SER-009 (NF-013, G-014). The outcome names and the error code are
representation (path B) of the G-021 outcomes.

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

**Layer 01 contract (Owner G-014):** the content hash of a structured value is defined by
SER-009 (SHA-256, lowercase hex, over RFC 8785 canonical bytes); "normalized content" means that
canonical form. Text and binary content are hashed as given (no Unicode or line-ending
normalization).

*Note:* resolves NF-013 by Owner decision G-014.

### CORE-012 — Durable operation identity
<a id="core-012"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [MVP §18.1] [MVP §M2] [R00 §20.2] [R04 §32] [IAA §A18] [R05 §6] [R05 §14]

A canonical commit (a completed learner interaction, an agent source capture, or another canonical
history mutation) carries a durable operation identity (`operation_id`, submission identity or
durable source identity). Retrying the same operation identity must not create a second historical
record; a retry after a successful commit returns/reuses the existing result.

**Layer 01 contract (Owner G-013):** an operation identity is unique within one
Minion-Memory store, across both profiles. A retry with the same operation identity and identical
content — equal SER-009 canonical bytes — returns the prior result and writes nothing. The same
operation identity with different content is a visible conflict error and writes nothing. (The
persistence behavior is implemented in Layer 04; Layer 01 fixes the identity's domain and the
identical/different test.)

**Operation identity domain (Owner G-032, G-033):** an operation identity is the pair
`{source_namespace, source_operation_id}`.
- **`source_namespace`.** A stable-ID token in the CORE-001 domain (G-020). It names the producer's
  uniqueness domain. A producer whose IDs are unique only within one deployment or instance uses a
  namespace naming that domain, not a broader one.
- **`source_operation_id`.** A non-empty opaque string of 1–256 bytes, measured on its exact UTF-8
  encoding (G-033). It is a SER-008 string, compared byte for byte: no normalization, case
  folding, trimming, parsing or filename restriction. Empty or longer values are rejected, never
  truncated or replaced by a digest.
- **Identity.** Uniqueness and idempotency apply to the pair, never to either field alone; equal
  `source_operation_id` values under different namespaces are different identities. The canonical
  model keeps the two fields separate and never joins them into one delimited string.
- **Retry and conflict.** The same pair for the same logical mutation is an idempotent retry. The
  same pair with materially different canonical mutation content is a visible conflict, never
  last-write-wins (G-013).
- **Errors.** A malformed pair (wrong shape, invalid namespace token, empty or over-long
  `source_operation_id`) is `operation_identity.invalid`, a stage-3 error (SER-008, G-031). A
  string that fails the generic value domain (e.g. a lone surrogate) reports that stage-2 error
  instead.

*Note:* resolves NF-014 by Owner decision G-013; the identity domain is G-032/G-033. The earlier
draft's statement that the operation identity "follows CORE-001's ID domain" was an author
addition without a decision (Codex review Q1) and is withdrawn.

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

**Layer 02 contract (WP-02).**
- **Canonical history records.** A canonical history record is a history envelope (HIST-002) that a
  reader of its profile admits with outcome `decode` (SER-005).
- **Derived artifacts.** Current state, summaries, checkpoints, indexes, projections and diagnostics
  are never history envelopes. They are never admitted as canonical history, and they never replace
  it.
- **Conformance.** Layer 02 fixes this vocabulary only. Rebuildability and non-replacement are
  verified where derived artifacts first exist: Layer 03 projections, Layer 04 persistence and
  Layer 05 checkpoints.


### HIST-002 — Typed, profile-owned canonical history
<a id="hist-002"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [FND §G.2] [MVP §18.1] [R04 §41.1]

The core provides typed canonical history primitives (`CanonicalHistory<T profile record>`); each
profile owns its history record types and payloads, which remain namespaced.

**History envelope (Owner G-048, G-049, G-052, G-055; `reference/governance/2026-10-11-owner-layer02-start.md`).** Every canonical history
record is serialized as one envelope, a JSON object:

```text
{record_id, profile, record_type, schema_version, compatibility, recorded_at,
 occurred_at?, payload?, provenance?}
```

- **Schema identity (G-052).** The triple `(profile, record_type, schema_version)` routes every
  record and is validated for every record.
  - `profile` and `record_type` are tokens in the CORE-001 lowercase portable-token grammar,
    compared exactly. They are vocabulary identifiers, not artifact IDs. Each profile owns its
    vocabulary, and a `record_type` is meaningful only within its `profile` (namespacing,
    R04 §41.1).
  - `schema_version` is a required integral value from 1 to 2^53−1 (one numeric kind, G-023;
    `1.0` is 1). It is a schema edition, not an artifact version. Version 0 is not an edition and
    is never a sentinel for unknown, legacy or draft.
  - A triple that is lexically valid but unrecognized proceeds to profile admission and SER-005
    compatibility. A malformed token or an out-of-range version is `history.envelope_invalid`.
- **Compatibility.** `compatibility` is exactly `"required"` or `"ignorable"` (SER-005). It is not
  part of the routing identity: it is validated only for records admitted to the reader's profile
  (G-050).
- **Recognized versus unrecognized.** A reader *recognizes* the `(record_type, schema_version)`
  pairs it declares for its profile.
  - For a recognized pair the member set is **closed**: exactly the members above. Any other
    top-level member, or a missing `record_id` or `recorded_at`, is `history.envelope_invalid`
    (G-048).
  - Envelope-level semantics evolve only through a new `schema_version` and/or `record_type`, never
    by adding a member to a known schema.
  - An unrecognized pair is never validated against a known closed shape.
- **Fields of a recognized envelope.**
  - `record_id`: a CORE-001 stable ID.
  - `recorded_at`: required. It is the HIST-004 instant at which the local durable writer recorded
    the record.
  - `occurred_at`: optional. It is the HIST-004 source-event instant. **Absence means unknown**,
    never `null`, epoch or any other sentinel, and a present `null` is `timestamp.invalid`. No
    reader infers `occurred_at` from `recorded_at`, and no ordering between the two is required
    (G-049).
  - `payload` and `provenance`: any SER-008 values. Their shapes are governed by the profile's own
    schemas for that `record_type`, not by the core, and admission returns them unchanged
    (HIST-010).
- **Gated stage-3 validation (G-055).** After stage 1 (decoding) and stage 2 (the generic value
  domain), an envelope passes four ordered gates, and the first failing gate reports:
  1. **Identity and routing.** A non-object envelope, or a missing or invalid `profile`,
     `record_type` or `schema_version`, is `history.envelope_invalid`.
  2. **Profile admission and schema recognition (SER-005).**
     - An other-profile record terminates as `excluded`.
     - For an admitted record, a missing or invalid `compatibility` is `history.envelope_invalid`.
     - An unrecognized pair terminates as `skip` (ignorable) or `history.unknown_required`
       (required).
  3. **Closed shape**, for a recognized same-profile pair: an unknown member, or a missing
     `record_id` or `recorded_at`, is `history.envelope_invalid`. This gate precedes all timestamp,
     payload and provenance validation.
  4. **Typed fields**, in canonical member order (G-034): `occurred_at` and `recorded_at` give
     `timestamp.invalid`, and `record_id` gives `id.invalid`.

  This is the Layer 02 stage-3 rule for history envelopes. It is recorded in SER-008 alongside
  G-035's rule for revision records, and does not extend to other records.
- **Normalized result.** The envelope with both timestamps in HIST-004 canonical form, and all
  values as the exact normalized SER-008 values.

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

**Layer 01 contract (Owner G-022):** the sole canonical persisted and wire spelling of a
timestamp is RFC 3339 UTC with exactly six fractional digits: `YYYY-MM-DDTHH:MM:SS.ffffffZ`.
- **Non-canonical forms.** `Z` is mandatory. Equivalent local-offset spellings, fractions with
  fewer or more than six digits, and leap-second `:60` forms are non-canonical.
- **Unknown time.** It is represented by absence of the field, never `null`, the epoch or another
  sentinel.
- **Semantics.** `occurred_at` and `recorded_at` keep distinct meanings. Timestamps must not
  substitute for explicit semantic ordering such as an episode `sequence_no`.
- **Local context.** Local wall-clock or time-zone context, if later required, is represented
  separately from the canonical instant.
- **Storage.** Physical storage may use integer microseconds internally if and only if the
  canonical round trip is lossless.

**Seam input (Owner G-026, G-028, G-029, G-030):** accepted input is distinct from the
canonical representation. Every conforming implementation **must** accept exactly the spellings
of the grammar below and **must** reject every other input as `timestamp.invalid` (G-030); a
host-language datetime parser's behaviour is never relied on.

```text
timestamp   = date sep time [fraction] offset        ; nothing before, between or after
date        = year "-" month "-" day
year        = 4DIGIT                                  ; 0001-9999 (0000 rejected, G-029)
month       = 2DIGIT                                  ; 01-12
day         = 2DIGIT                                  ; 01-28/29/30/31, proleptic Gregorian (G-029)
sep         = "T" / "t"                               ; G-028
time        = hour ":" minute ":" second
hour        = 2DIGIT                                  ; 00-23
minute      = 2DIGIT                                  ; 00-59
second      = 2DIGIT                                  ; 00-59 (":60" rejected, G-026)
fraction    = "." 1*6DIGIT                            ; one to six digits ("." alone rejected)
offset      = "Z" / "z" / ( "+" / "-" ) 2DIGIT ":" 2DIGIT   ; offset hour 00-23, minute 00-59
DIGIT       = %x30-39                                 ; ASCII digits only
```

- **Normalization.** The instant is the local civil time minus the offset; `-00:00` is the same
  instant as `Z`. It is emitted and stored exactly as `YYYY-MM-DDTHH:MM:SS.ffffffZ`, with uppercase
  `T` and `Z` and the fraction right-padded with zeros to six digits.
- **Range (G-029).** Both the parsed local civil date-time and the normalized UTC instant must lie
  within `0001-01-01T00:00:00` … `9999-12-31T23:59:59.999999`. An offset that moves the instant
  across either boundary is rejected (`timestamp.invalid`); it is never clamped or wrapped, and
  the offset form is never preserved instead. Leap years follow the Gregorian rule (divisible by
  4, except centuries not divisible by 400).
- **Semantics.** Equality, hashing, persistence, conflict detection and cross-language
  conformance operate only on the normalized canonical value. The original offset, letter case or
  spelling is not part of timestamp semantics; local-time context, if needed, is separate
  metadata.
- **Error stage.** `timestamp.invalid` is a stage-3 (typed field) error (SER-008, G-031).
  - **Wrong type.** A valid generic value of the wrong type (`null`, `true`, a number, an array or
    an object) passes stages 1 and 2 and fails here as `timestamp.invalid`.
  - **Earlier failure.** Only an actual stage-1 or stage-2 failure reports that earlier error
    instead (e.g. a string containing a lone surrogate is `value.lone_surrogate`).

*Note:* resolves NF-015 (G-022) and NF-025 (G-026), and the input-grammar questions in WP01-CR-001
(G-028…G-030). The offset, second and fraction grammar follows RFC 3339 §5.6 (an authority
reading); letter case, year range, overflow and required acceptance are Owner decisions.

### HIST-005 — No global total order is assumed
<a id="hist-005"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [FND §App-E] [MVP §5.1] [R00 §6] [R04 §9]

No total global order across devices or episodes is assumed or required.

*Note:* bounded "since boundary" reads ([R04 §34]) need some durable ordering; how that coexists
with this rule is unspecified (NF-016).

**HistoryBoundary (Owner G-047, G-051, G-054, resolving NF-016; `reference/governance/2026-10-11-owner-layer02-start.md`).**

A HistoryBoundary is the closed record `{store_id, position}`.
- **`store_id`.** A CORE-001 stable ID naming one logical store.
- **`position`.** An integral value from 0 to 2^53−1 (G-054):
  - position 0 is the boundary before the store's first physical record;
  - positive positions denote store-local append progress;
  - resuming or replaying after boundary N considers the physical records whose positions are
    greater than N.
- **What a position is.** It is a **store-local ordering cursor only**. It is **not** a record
  count, a timestamp, a cross-store sequence, or a global, causal or cross-device event order, and
  it must never be used as one.
- **Mixed-profile stores.** Records that a profile reader excludes (G-050) still occupy store
  positions and advance the shared cursor.

Operations:
- **Ordering.** `compare_history_boundaries(a, b)` returns `less`, `equal` or `greater` by position
  only when both boundaries name the same `store_id`. Otherwise it fails with
  `history.boundary_incomparable`. Implementations never compare positions alone and never derive
  an order from store IDs.
- **Equality.** `history_boundaries_equal(a, b)` is structural equality over the complete pair, so
  it returns `false`, not an error, for different stores.
- **Store-dependent operations.** Range, distance, minimum/maximum and since-boundary operations
  likewise require a common store. They belong to Layer 04 (PERS-007/008).

Errors (SER-008 G-031):
- **Generic stages first.** The generic stages run across both arguments first.
- **Invalid boundary.** Then a boundary with a non-object value, a missing or other member, an
  invalid `store_id`, or a negative, fractional, string or out-of-range `position` is
  `history.boundary_invalid` (stage 3), checked in declared order `a`, then `b`.
- **Incomparable.** Incomparability is reported only once both boundaries are valid.
- **Arguments in errors.** Argument errors name `a` or `b`. `history.boundary_incomparable` is a
  relation and names no argument.

### HIST-006 — History is append-only
<a id="hist-006"></a>
- **Profile:** core · **Source status:** FROZEN · **Sources:** [FND §8] [FND §14] [R03 §14] [R04 §9] [R04 §11] [R03 §26]

Normal behavior appends to canonical history and never mutates prior records in place. A
correction is a new record that references the original rather than an in-place edit.

**Layer 03 contract (WP-03; Owner G-067; `reference/governance/2026-10-11-owner-layer03-start.md`).**
- **Corrections append.** A correction is a new history record that the profile decoder links to
  the original with a `corrects` relation (HIST-007). It never edits the original, and both remain
  in every projection.
- **Projection never mutates.** `project_history` (PROJ-001) never mutates, drops or reorders its
  inputs.
- **Layer 04 enforces.** Durable append enforcement, transactions, idempotency and prevention of
  historical mutation belong to Layer 04 (PERS-*).


### HIST-007 — Reinterpretation appends overlays
<a id="hist-007"></a>
- **Profile:** core · **Source status:** FROZEN · **Sources:** [FND §14] [FND §19] [IAA §A16] [MVP §6] [R03 §13] [R03 §27.4] [R04 §35]

Evolution adds interpretations; it never rewrites observation history. A later interpretation is
appended with derived_from / supersedes / reinterprets provenance identifying its producer and
version. Historical interpretations remain auditable. A "current preferred" interpretation is a
projection, not an in-place rewrite.

**Lineage (Owner G-068, G-069, G-071…G-074; `reference/governance/2026-10-11-owner-layer03-start.md`).**

Lineage between history records is a relation list. Each relation is a closed record with exactly
one typed target (G-072):

```text
{"from_record_id": "<id>", "relation": "<kind>", "to_record_id": "<id>"}
{"from_record_id": "<id>", "relation": "derived_from",
 "to_artifact": {"stable_id": "<id>", "artifact_version": <edition>}}
```

- **Producer.** The relation list comes from the profile decoder: the links live in the profile's
  versioned payload, never in provenance, and the closed envelope is unchanged (G-048).
  `from_record_id` is normally the containing envelope's `record_id`. Consumers never parse payload
  lineage themselves.
- **Vocabulary** (core-owned, closed in Layer 03):
  - `supersedes`: `from` replaces `to` as a current head.
  - `corrects`: `from` is a correction of `to` (HIST-006) and replaces it as a current head.
  - `reinterprets`: `from` is an interpretation of the observation `to`.
  - `derived_from`: a provenance link; it does not affect resolution.
  - `supersedes`, `corrects` and `reinterprets` form the *resolution* family.
- **Typed targets.** Only `derived_from` may use `to_artifact`. Its target is an external immutable
  artifact: a CORE-001 `stable_id` with a CORE-002 `artifact_version`. An external artifact is never
  written as a record ID.
- **Repeated relations.** Two relations that are equal after normalization are one relation:
  multiplicity has no meaning (G-072).
- **Early (shape) checks, before any entry is admitted.** Each gives `lineage.invalid`, argument
  `relations`:
  - `relations` is not an array;
  - an element is not a closed object;
  - `from_record_id` is not a CORE-001 ID;
  - `relation` is not exactly one of the four kind strings;
  - the target is not exactly one of `to_record_id` (a CORE-001 ID) or `to_artifact` (closed, as
    above);
  - `to_artifact` is used with a kind other than `derived_from`.
- **Late (graph) checks, after every entry is admitted.** Each gives `lineage.invalid`, argument
  `relations`, and atomically fails the projection:
  - `from_record_id` is not a record available to the projection;
  - a resolution-family target is not a record available to the projection (G-072);
  - a self-link of any kind (G-071);
  - a cycle in the resolution family taken together, including mixed kinds (G-071);
  - a cycle among `derived_from` relations between available records (G-071).
  There is no combined rule across the two families.
- **Available records.** Available means decoded in this projection. In Layer 05 it also includes a
  compatible base or checkpoint state (G-072). Skipped and excluded records are not available.
- **Unresolved derivations.** A `derived_from` target that is unavailable (an artifact, or a record
  outside the projection) is kept and reported as an *unresolved derivation*. It is never dropped,
  and it does not fail the projection (G-072).
- **Current heads (G-069).** The current heads are the decoded records targeted by no `supersedes`
  or `corrects` relation. "Current" is set-valued: several heads are a valid divergent state, and a
  later record may supersede several heads to converge them.
- **Interpretations (G-074).** An observation `o` has interpretations only through records with
  their own direct `reinterprets o` relation. `supersedes`, `corrects` and `derived_from` never
  propagate that membership. So the current interpretations of `o` are the records that directly
  reinterpret `o` and are current heads. The set may be empty, and the core never infers a missing
  association.
- **No ordering ever decides currency.** No `recorded_at`, store position, record ID or container
  order is ever used to pick among heads. A purpose-specific consumer may apply a documented,
  versioned selection policy, recording its selection provenance and keeping every candidate
  (PROJ-002).

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

**Layer 02 contract (WP-02).**
- **No core origin vocabulary.** The core defines none: each profile owns its mechanism (OBS-006,
  ACTX-004). "Shared in spirit" (R03 §28) is not a shared term (FND §G.1).
- **Core guarantee.** The envelope's `payload` and `provenance` reach an admitting reader exactly,
  as normalized SER-008 values. Envelope admission never drops, rewrites or summarizes the data in
  which a profile records information origin.


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

**Canonical HistoryProjector (Owner G-067, G-070, G-073; `reference/governance/2026-10-11-owner-layer03-start.md`).**

`project_history(reader, stream, relations)` is the single semantic path from stored records to a
purpose-neutral projection.

**Arguments:**
- **`reader`** is the Layer 02 replay reader (SER-005, G-053).
- **`stream`** is the closed record `{store_id, entries}`.
  - `store_id` is a CORE-001 stable ID.
  - `entries` is an array of closed `{position, record}` entries, with positions integral and
    strictly increasing from 1. Position 0 is the boundary before the first record (G-054), never an
    entry.
  - Any other stream value is `history.stream_invalid`. (Author choice, flagged: the stream shape
    and the error code.)
- **`relations`** is the decoder's lineage list (HIST-007).

**Order of evaluation.** Each step fails atomically and no partial result is ever returned (G-070):
1. **Generic stages.** Stages 1–2 run across `reader`, `stream` and `relations` (G-031).
2. **Argument shapes.** Then `history.reader_invalid`, `history.stream_invalid`, and the early
   lineage shape checks (HIST-007), in that order.
3. **Entries.** Each entry is admitted in position order through the Layer 02 gates (G-055). The
   first failing entry wins:
   - `decode` adds the normalized envelope;
   - `skip` and `excluded` add nothing, but the position still counts (G-050, G-051);
   - `history.unknown_required`, or any envelope, typed or generic error, fails the projection. The
     error carries the entry's store `position`; for `unknown_required` its detail gives the routing
     identity `(profile, record_type, schema_version)`.
   - **Repeated `record_id` (G-073).** One `record_id` denotes one logical record. A later decoded
     occurrence whose complete canonical envelope (SER-009 bytes) equals the first one's is
     coalesced: it is recorded as a *duplicate occurrence*, advances the boundary and has no other
     effect. A later occurrence with different canonical content is `history.duplicate_record_id`
     at that position. Records with different IDs are never deduplicated, however similar.
4. **Lineage.** The late lineage checks run, then resolution (HIST-007).

**Result** (a closed record, purpose-neutral):

```text
{"through":    {"store_id": ..., "position": <last entry position, 0 if none>},
 "records":    [<decoded envelopes, one per record_id, in first-position order>],
 "skipped":    [<positions>],  "excluded": [<positions>],
 "duplicates": [{"position": <later position>, "record_id": <id>}, ...],
 "relations":  [<the distinct validated relations>],
 "unresolved_derivations": [<the derived_from relations whose target is unavailable>],
 "current":    [<record_ids of current heads, in position order>],
 "interpretations": [{"observation": <record_id>, "current": [<record_ids>]}, ...]}
```

- **Presentation order.**
  - `relations` and `unresolved_derivations` are ordered by the `from` record's position, then the
    relation kind, then the target: available records by position, then record targets by ID, then
    artifacts by `(stable_id, artifact_version)`.
  - `interpretations` is ordered by the observation's position, and lists every observation that
    any `reinterprets` relation targets.
  - All ordering is presentation only, and never selects (G-069).
- **Errors.** Argument errors name `reader`, `stream` or `relations`. Entry errors also carry the
  entry's `position`. `history.unknown_required` keeps Layer 02's convention: it names no argument,
  but it carries the `position`.
- **Determinism (HIST-001).** Equal inputs give equal results, whatever the order of `relations`
  and of object members. The projection is rebuildable from the stream and the decoder output alone.

### PROJ-002 — Purpose-specific projections
<a id="proj-002"></a>
- **Profile:** core · **Source status:** GUARDRAIL · **Sources:** [IAA §A11] [R04 §26] [FND §deliberately-not-frozen]

Different purposes (scheduling, diagnostics, progress UI, reporting, research, agent context)
derive different projections from the same history. There is no universal summary/profile blob;
a single global learner summary is deliberately not frozen.

**Layer 03 contract (WP-03; Owner G-069).**
- **Purpose-neutral.** The `project_history` result is the purpose-neutral base.
- **Purpose-specific projections** (scheduling, diagnostics, progress, research, agent context)
  derive from it with a documented, versioned policy. They record that policy's identity as
  selection provenance and never discard candidates from the base.
- **No universal summary.** No single universal summary is defined.


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
