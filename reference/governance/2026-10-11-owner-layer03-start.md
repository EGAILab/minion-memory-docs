# Owner decisions — Layer 03 start and scope (2026-10-11)

Recorded verbatim by Claude.

## G-066 — Start Layer 03

**Context.** Layers 01 and 02 were certified (G-044, G-065). Claude reported that the workflow does
not start the next layer automatically.

> **Owner:** "Start layer 03"

**Scope.** Layer 03 per `plans/layer-plan.md`: the projection/normalization path and append-only
reinterpretation (PROJ-001, PROJ-002, HIST-006, HIST-007). Rust is certified at Layer 02, so Python
Layer 03 is allowed.

## G-067 — WP-03 scope: canonical HistoryProjector and shared lineage resolver

> **Q:** WP-03 scope: what should Layer 03's core contract provide? (Sources: one shared
> HistoryProjector reused by every consumer, R04 §31/IAA A17; reinterpretation appends overlays
> and 'current preferred' is a projection, R03 §13, R04 §35; append-only API enforcement is a
> persistence concern, R04 §11.)
>
> **A:** "Choose 1 — Layer 03 provides the canonical HistoryProjector and the shared lineage
> resolver.
> project_history(reader, records) is the single deterministic, fail-safe semantic path from Layer
> 02-admitted records to a purpose-neutral history projection. Layer 03 defines lineage
> representation, validation and resolution of current/preferred interpretations while retaining
> every historical record.
> Downstream consumers must consume this projection rather than independently parsing history or
> selecting current records. Ambiguous or invalid lineage must be surfaced explicitly, never
> resolved through timestamps, container order or an implementation-local tie-break.
> Layer 03 defines append-only reinterpretation semantics, but Layer 04 owns durable append
> enforcement, transactions, idempotency and prevention of historical mutation."

## G-068 — Lineage: profile-owned encoding, Core-owned semantics and resolution

> **Q:** Where do lineage links (corrects, supersedes, reinterprets, derived_from) live? The Layer
> 02 envelope is closed (G-048) and payload/provenance shapes are profile-owned.
>
> **A:** "Choose 1 — profile-owned durable encoding with Core-owned lineage semantics and
> resolution.
> The closed Layer 02 envelope is unchanged. A recognized profile/schema stores lineage links within
> its own versioned payload and exposes them through its profile decoder as a normalized Core
> relation list {from_record_id, relation, to_record_id}. The from_record_id is normally derived
> from the containing envelope’s record_id.
> Layer 03 defines the shared relation vocabulary, graph validation, ambiguity behavior, and
> current/preferred resolution. Every consumer uses the shared HistoryProjector; consumers must not
> independently parse profile payload lineage.
> Lineage that affects projection does not live in provenance. Self-links and cycles in
> resolution-affecting supersession relations are errors, and ambiguous current heads are surfaced
> explicitly rather than resolved through timestamp or implementation-local ordering."

## G-069 — Current is set-valued; no universal tie-break

> **Q:** When several interpretations of the same observation are all unsuperseded, what is
> 'current'? (R03 §13: the current model 'may choose the latest trusted evidence set without erasing
> previous interpretations'.)
>
> **A:** "Choose 1 — Layer 03 returns every unsuperseded interpretation and applies no universal
> tie-break.
> “Current” is set-valued: the current heads are all valid interpretations not superseded by another
> admitted record. Multiple current heads are a valid divergent lineage state, not automatically an
> error. Core must not select by recorded_at, store position, record ID, or another incidental
> ordering.
> A purpose-specific consumer may apply a documented, versioned selection policy to produce a
> preferred interpretation, while retaining every candidate and recording the selection provenance.
> A later record may explicitly supersede multiple heads to converge the lineage."

## G-070 — An unknown required record fails the projection atomically

> **Q:** If the canonical projector meets an unrecognized required record mid-stream, what does the
> projection return?
>
> **A:** "Choose 1 — an unrecognized required record atomically fails the requested projection with
> history.unknown_required. The error identifies the blocking store position and routing identity,
> but no partial semantic projection is returned or published. Existing projections remain valid
> only at their previously completed history boundary. Foreign-profile records remain excluded and
> unknown ignorable records remain skippable under Layer 02 rules."

## G-071 — Self-links and cycles (resolves WP03-CR-001, part a)

> **Q:** WP03-CR-001a: which self-links and cycles are invalid lineage? (G-068 already makes
> self-links and cycles in supersession relations errors. The vocabulary is supersedes, corrects,
> reinterprets, derived_from.)
>
> **A:** "Choose 1 — all lineage self-links are invalid. The combined resolution graph formed by
> supersedes, corrects, and reinterprets MUST be acyclic, including cycles that mix those relation
> types. The derived_from graph MUST independently be acyclic. A violation produces lineage.invalid
> and atomically fails projection.This decision does not yet impose one combined acyclicity rule
> across resolution and derivation relations; any cross-family consistency rule requires an explicit
> additional contract decision."

## G-072 — Endpoints, typed targets and repeated relations (resolves WP03-CR-001, part b)

> **Q:** WP03-CR-001b: links whose endpoint is not a record in this projection, and repeated
> identical links. (derived_from may legitimately point at non-history artifacts, e.g. a Knowledge
> unit.)
>
> **A:** "Choose 1 — resolution-affecting relations are strict, while derived_from may retain
> unresolved external targets.supersedes, corrects, and reinterprets must reference history records
> available to the effective projection, including compatible base/checkpoint state. A missing
> endpoint produces lineage.invalid and atomically fails projection.derived_from may reference a
> history record or an external immutable artifact. An unavailable target is preserved and reported
> as an unresolved derivation reference; it is never silently dropped and does not by itself fail
> projection.Relation targets must be typed so external artifacts are not disguised as record IDs.
> Exact duplicate normalized relations collapse to one Core edge because relation multiplicity has no
> semantic meaning."

## G-073 — Repeated record IDs (resolves WP03-CR-002)

> **Q:** WP03-CR-002: the stream contains two records with the same record_id. (Durable idempotent
> retry is Layer 04; R04 §36 forbids semantic deduplication of observations.)
>
> **A:** "Choose 1 — identical canonical occurrences coalesce; conflicting reuse fails.Within an
> effective projection, one record_id denotes one logical record. Repeated occurrences with the same
> complete canonical envelope are coalesced at the first occurrence, while all later physical
> positions are retained as derived duplicate-occurrence metadata and still advance the store
> boundary. They have no additional semantic effect.Reusing a record_id with different canonical
> envelope content produces history.duplicate_record_id at the first conflicting later position and
> atomically fails projection. Records with different IDs are never deduplicated merely because their
> content is equal or similar."

## G-074 — Interpretation membership is direct only (resolves WP03-CR-004)

> **Q:** WP03-CR-004: e-1 reinterprets o-1, and e-2 supersedes e-1 without its own reinterprets link.
> Is e-2 a current interpretation of o-1?
>
> **A:** "Choose 1 — interpretation membership is established only by a record’s own direct
> reinterprets links.supersedes, corrects, and derived_from do not propagate or inherit
> interpretation targets. A replacement that is intended to remain an interpretation of an
> observation must repeat the relevant reinterprets link through its profile-owned encoding.
> Consequently, when e-1 reinterprets o-1 and e-2 supersedes e-1 without its own reinterprets o-1
> relation, e-1 remains a historical interpretation, e-2 is a current record but not an
> interpretation of o-1, and o-1 has no current interpretation. Core exposes that result and never
> infers the missing association."

## G-075 — External derivation target identities (resolves WP03-CR-005)

> **Q:** WP03-CR-005: a derived_from link may point at an external immutable artifact (G-072).
> Which artifact identities may that typed target carry? (Sources identify assets by stable ID +
> version OR by content hash: R04 §4, KNOW-009.)
>
> **A:** "Choose 1 — an external derived_from target is either a versioned artifact identity
> {stable_id, artifact_version} or a content-addressed identity {content_hash}. The alternatives are
> mutually exclusive and closed.A missing edition, both forms together, neither form, or unknown
> members produce lineage.invalid. Bare stable IDs are forbidden because they do not pin immutable
> content. The content hash must use the exact CORE-011 canonical SHA-256 form.Layer 03 preserves
> these references as unresolved external derivations unless an explicit artifact resolver is
> available. They do not affect current-head resolution and are never silently dropped or
> rewritten."
