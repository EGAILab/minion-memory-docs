# Owner decisions — Layer 02 start and split (2026-10-11)

Recorded verbatim by Claude.

## G-046 — Start Layer 02

**Context.** WP-01 and WP-P02 were closed and accepted. Claude reported that the workflow does not
start the next layer automatically.

> **Owner:** "Start next layer"

**Scope.** Authorizes starting Layer 02 per `plans/layer-plan.md`. Python is at most one layer
ahead of Rust: Rust is certified at Layer 01, so Python Layer 02 is allowed.

## G-047 — Split Layer 02; envelope first; NF-016 constraint

> **Q:** Layer 02 holds two fairly independent surfaces: MemoryScope (SCOPE-001..006; needs several
> of your product decisions on visibility/inheritance, NF-018) and the history/compatibility
> envelope (HIST-001/002/005/010, SER-005/006; mostly resolvable from the sources, NF-016). How
> should I run it?
>
> **A:** "Choose 1 — Split, envelope first.
> Create WP-02 for the history/compatibility envelope and let it proceed immediately through
> contract draft and independent review. Create sibling WP-02S for MemoryScope. Start WP-02S
> characterization and prepare one consolidated Owner-decision packet in parallel, but do not let
> unresolved MemoryScope semantics block WP-02.
> Keep the dependency explicit: later work that consumes scope semantics must wait for WP-02S,
> while history/compatibility work may close independently.
> For NF-016, a per-store durable append position is a valid candidate resolution only as a local
> persistence/read cursor; it must not be interpreted as a global causal or cross-device event
> order."

**Effect.**
- **WP-02** is the history/compatibility envelope: HIST-001, HIST-002, HIST-005, HIST-010, SER-005
  and SER-006. HIST-004's Layer 01 timestamp grammar is consumed, not reopened. It proceeds through
  contract draft, independent review and the rest of the workflow, and may close independently of
  WP-02S.
- **WP-02S** is MemoryScope: SCOPE-001…006, with NF-018 characterization and one consolidated
  Owner-decision packet. Anything that consumes scope semantics declares `blocked_by: WP-02S`.
- **NF-016 constraint.** A per-store durable append position may resolve NF-016 only as a local
  persistence/read cursor. The contract must state that it is not a global, causal or cross-device
  event order, and it must never be used as one.

## G-048 — Closed history envelope per recognized schema version (WP-02)

> **Q:** WP-02 history envelope shape: the sources require explicit profile/type/schema identity,
> required|ignorable compatibility and distinct occurred/recorded times (R04 §27, IAA §3, SER-006),
> but not whether the envelope is closed. Should an envelope with an unknown extra top-level
> member be rejected?
>
> **A:** "Choose 1 — Closed envelope.For every recognized history-envelope schema version, the
> top-level member set is closed. The permitted members are exactly {record_id, profile,
> record_type, schema_version, compatibility, recorded_at, occurred_at?, payload?, provenance?};
> an unknown top-level member is history.envelope_invalid. Envelope-level semantics evolve through
> an explicit schema-version and/or record-type change, never by silently adding fields to a known
> schema.Keep this distinct from unknown-version compatibility: if the envelope identifies an
> unrecognized schema/type, apply the required | ignorable compatibility rules rather than
> pretending to validate it as the current closed schema. Nested payload and provenance shapes
> remain governed by their own applicable schemas."

## G-049 — Envelope timestamps (WP-02)

> **Q:** Timestamps on the envelope (HIST-004 grammar from Layer 01): which are mandatory?
>
> **A:** "Choose 1 — recorded_at required; occurred_at optional.Every canonical history envelope
> MUST carry recorded_at, representing when the local durable writer committed/recorded the history
> record. occurred_at represents source-event time and MAY be absent when unknown. Unknown is field
> absence, never null, epoch, or another sentinel.Do not infer occurred_at = recorded_at when
> absent, and do not require occurred_at <= recorded_at; clock skew and imported/external sources
> make that relation non-authoritative. Timestamps remain metadata, not a substitute for
> store-local append ordering."

## G-050 — Foreign-profile records are excluded from a profile replay (WP-02)

> **Q:** Shared storage may hold both profiles (R04 §41.1). When a profile's reader replays a
> stream and meets a record of the other profile, what happens?
>
> **A:** "Choose 1 — excluded, not an error.A profile replay processes only records whose
> validated envelope profile equals the requested profile. Any valid non-matching profile record
> has replay outcome excluded; it is not payload-decoded and does not participate in the requested
> profile’s compatibility, history, projection, or derived state. required | ignorable applies only
> after profile admission and must not be used to classify foreign-profile records.Excluded records
> still advance the underlying shared-store read boundary. Invalid or absent profile identity is an
> envelope error, not exclusion."

## G-051 — HistoryBoundary is a store-local cursor; cross-store is incomparable (WP-02, NF-016)

> **Q:** NF-016 under your G-047 constraint: a HistoryBoundary is a local per-store cursor
> {store_id, position}. What should comparing boundaries from two different stores do?
>
> **A:** "Choose 1 — cross-store boundaries are incomparable.HistoryBoundary.position is
> meaningful only within the logical store identified by store_id. Ordering two boundaries with
> different store IDs MUST fail with history.boundary_incomparable; implementations MUST NOT
> compare positions alone or manufacture an order from store IDs. Structural equality remains
> defined over the complete pair and therefore returns false, rather than an error, for different
> stores.Range, distance, minimum/maximum and since-boundary operations likewise require a common
> store. In a mixed-profile store, records excluded by a profile reader still occupy store positions
> and advance the shared cursor."

## G-052 — Envelope schema identity domains (WP-02, resolves WP02-CR-001)

> **Q:** WP02-CR-001: what values may the envelope's profile, record_type and schema_version take?
> (record_id stays a CORE-001 stable ID.)
>
> **A:** "Choose 1 — portable tokens plus schema edition ≥1.profile and record_type use the
> CORE-001 lowercase portable-token domain and are compared exactly. They are distinct vocabulary
> identifiers, not artifact IDs, despite sharing the same lexical grammar. schema_version is a
> required integral canonical numeric value in 1..2^53−1.The schema identity is the triple
> (profile, record_type, schema_version). Lexically valid but unrecognized values proceed through
> profile-admission and required | ignorable compatibility handling; malformed tokens or
> out-of-range versions are envelope validation errors. Version zero is not a valid schema edition
> and must not be used as an unknown, legacy, or draft sentinel."

## G-053 — Closed replay reader with duplicate rejection (WP-02, resolves WP02-CR-002)

> **Q:** WP02-CR-002: the replay reader configuration {profile, recognized: [{record_type,
> schema_version}]} — how strict?
>
> **A:** "Choose 1 — closed configuration with duplicate rejection.ReplayReader and each
> recognized-schema entry are closed typed records. Unknown or missing members are invalid. After
> typed normalization, every (record_type, schema_version) pair must be unique; duplicates—including
> numeric aliases such as 1 and 1.0—produce history.reader_invalid. Implementations may use a set
> internally only after the public configuration has passed duplicate-free validation."

## G-054 — HistoryBoundary position domain (WP-02, resolves WP02-CR-003)

> **Q:** WP02-CR-003: the HistoryBoundary position (store-local cursor, G-051) — which numeric
> domain?
>
> **A:** "Choose 1 — HistoryBoundary.position is an integral canonical numeric value from 0 through
> 2^53−1. Position 0 denotes the boundary before the first physical record of the identified store;
> positive positions denote store-local append progress. Resume/replay after boundary N considers
> physical records with positions greater than N.Negative, fractional, string, and out-of-range
> values produce history.boundary_invalid. Position is a local ordering cursor, not a record count,
> global order, timestamp, or cross-store sequence."

## G-055 — Gated stage-3 validation of history envelopes (WP-02, resolves WP02-CR-005)

> **Q:** WP02-CR-005: when one history envelope has several stage-3 problems at once, which error
> wins?
>
> **A:** "Choose 1 — gated Stage-3 validation.After Stage-1 decoding and Stage-2 generic-value
> validation, validate history envelopes through four ordered gates: identity/routing members;
> profile admission and schema recognition; closed shape for a recognized same-profile schema; then
> remaining typed fields in canonical traversal order.Foreign-profile records terminate as
> excluded, and unknown ignorable schemas terminate as compatibility skips before the reader applies
> its recognized envelope shape. For a recognized schema, missing or unknown envelope members
> produce history.envelope_invalid before timestamp, payload, or provenance validation. Thus an
> extra member plus an invalid occurred_at reports history.envelope_invalid."

**WP02-CR-004 (author repair, path A from G-050 + G-052 + G-055).**
- Gate 1 validates the schema-identity triple `(profile, record_type, schema_version)` for every
  record.
- `compatibility` is not part of that routing identity. It is validated only for records admitted
  to the reader's profile (gate 2), because G-050 forbids using it for, or letting it participate in
  classifying, other-profile records.
- So an other-profile record whose triple is valid is `excluded`, even if its `compatibility` is
  missing or invalid.
