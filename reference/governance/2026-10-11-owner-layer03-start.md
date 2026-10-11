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
