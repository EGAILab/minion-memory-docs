# WP-02 Layer 02 contract review — Codex

Date: 2026-10-11. Independent reviewer / Rust owner: Codex.

## Verdict and custody

**CHANGES_REQUIRED** for docs `7afbffffbe09357b7493188df34bcd2bfde4ac1f` /
code `a2178c955ffff1bd3bd604a628648463774f1b0e`.

Blocking new findings: **WP02-CR-001..005**. Existing **NF-026** is independently reproduced and
remains open. No candidate edits or implementation were made. The review branch
`review/wp02-contract-1` starts at the handed-off state head `803e5e85`; the code checkout is
detached at the exact SHA. Only this record is committed. Scratch probes and all caches/targets
are project-local. WP-02S is outside this review; no scope decisions or edits were made there.

The requested review is not satisfied by confirming the corpus against the draft: its 59
expectations do match the draft, but several draft acceptance choices lack authority and one
ordering rule contradicts another sentence. Those must be resolved before independent implementation.

## Findings

All references to draft spec below are at docs `7afbffff`; corpus references are at code `a2178c95`.
Each new finding is OPEN, raised_by Codex, blocking [WP-02]. The findings are classified under
`process/finding-taxonomy.md` section 1.1; G-009 does not delegate path-C choices.

### WP02-CR-001 — Envelope discriminator domains are new observable restrictions

- classification: **REQUIREMENT_UNCERTAIN**
- owner_decision_required: **true** (path C)
- requirements: HIST-002, SER-005, SER-006
- evidence: `spec/core.md:387–393`; G-048; G-020 and G-012 in the Layer-01 decision record;
  R04 sections 27 and 41.1 (bundle SHA-256 `b4c25d006e7db998feb5f955b55a9fcdc58ef589e72eae6cff742b9c0b92755f`).

The draft imports the complete CORE-001 stable-ID domain for `profile` and `record_type`, and
requires `schema_version` to be a positive integer edition. G-048 settles member names/closure
and versioned evolution, not these domains. G-020 is a stable-ID/filename decision; G-012 is
explicitly an **artifact** edition decision. The draft itself distinguishes schema versions from
artifact versions. R04 requires explicit namespaced identity and a schema version but does not
supply those lexical restrictions or a positive-integer-only schema-version domain. G-023
normalizes numbers; it does not choose a schema-version domain. G-032 is useful precedent: the
prior author's extension of CORE-001 to operation identity required an Owner decision.

Discriminants, independently executed against my literal draft model: `record_type: Attempt`
and `record_type: con` both give `history.envelope_invalid`; `schema_version: 0` also gives
that error. In the corpus these choices are already pinned by envelope steps 18–21 and replay
step 11 (`profile: Learning`). A profile-owned case-sensitive discriminator vocabulary or a
schema domain admitting edition zero yields different acceptance/recognition outcomes.

Required resolution: present the discriminator and schema-version domains as explicit Owner
options, or supply a deciding authority passage that actually applies to them. G-020's domain
is an available option, not implied merely by the word identity. Keep record_id's existing
CORE-001 rule; this finding does not reopen it.

### WP02-CR-002 — Closed reader input and duplicate rejection are unrecorded acceptance choices

- classification: **REQUIREMENT_UNCERTAIN**
- owner_decision_required: **true** (path C)
- requirements: SER-005
- evidence: `spec/serialization.md:55–59`; G-048; replay steps 9–10.

G-048 closes the **history envelope**, not a reader configuration. A closed `{profile, recognized}`
reader and closed recognized-pair elements are specified here without deciding authority. The
representation can be an array of pairs (path B), but rejecting duplicate declarations rather
than treating them as the same recognized set changes an observable outcome. Duplicate identity
being equal after normalization is already settled by Layer 01; **rejecting** it is not.

Witness: reader recognized entries `{record_type: attempt, schema_version: 1}` and the same
entry with `1.0`, with an otherwise valid recognized record. Draft/model/corpus return
`history.reader_invalid`, argument `reader`; treating recognized declarations as a set returns
`decode`. Likewise `{profile, recognized, mode: lenient}` is rejected under the draft, whereas
an open configuration representation could ignore an unrelated member without changing recognition.

Required resolution: Owner decision on closedness and duplicate rejection, separate from the
mechanics of normalizing/equating the pairs. Reader-before-record argument order is already
supported by the declared argument order and is not itself challenged.

### WP02-CR-003 — Cursor numeric domain and zero sentinel need a decision

- classification: **REQUIREMENT_UNCERTAIN**
- owner_decision_required: **true** (path C)
- requirements: HIST-005
- evidence: `spec/core.md:514–517`; G-047/G-051; R04 section 34 (same bundle SHA above);
  boundary steps 4, 12–14.

G-047/G-051 decide a store-local cursor and cross-store incomparability, not its numeric domain
or an externally visible before-first-record value. The draft chooses integers 0..2^53−1,
assigns 0 the before-first position, and rejects negative/fractional/string cursor values.
SER-008 constrains numeric values once chosen; it does not choose the cursor representation or
reserve position zero. Different conventions distinguish an actual append position from an
empty-store boundary differently and accept different values.

Executed discriminants: comparing positions 0 and 1 returns `less`; -1 and 1.5 are
`history.boundary_invalid`. Those are defined by the draft but not fixed by the quoted decisions.

Required resolution: Owner decision on the integer cursor domain and before-first sentinel, or
specific authority establishing them. Preserve the already-decided logical-store pairing,
structural equality and cross-store incomparability. No global/causal order is proposed.

### WP02-CR-004 — Compatibility is validated before a branch that says it is not consulted

- classification: **CONTRACT_ASSURANCE_DEFECT**
- owner_decision_required: **false** for repairing the contradiction to match G-050; escalate
  path C if a different foreign-record validity policy is proposed.
- requirements: HIST-002, SER-005, SER-006
- evidence: `spec/core.md:387–393,413–420`; `spec/serialization.md:62–67`; G-050.

HIST-002 defines compatibility as an identity member present and valid in every schema version.
SER-005 first validates all identity members, then excludes a foreign profile while claiming
`compatibility` is "not consulted." G-050 says required|ignorable applies only after profile
admission and the foreign record does not participate in the requested profile's compatibility.
The draft cannot both require compatibility's accepted value before exclusion and never consult it.

Witness: reader learning with recognized attempt/1; record
`{profile: agent, record_type: attempt, schema_version: 1, compatibility: bogus}`. The explicit
identity-first rule gives `history.envelope_invalid` (argument record), reproduced by my model;
profile admission before consulting compatibility gives `excluded`. Removing compatibility has
the same discrimination. Existing exclusion controls use valid compatibility and do not distinguish
these readings. The same distinction should be made explicit for record_type/schema_version
validation before foreign exclusion, since G-050 singles out validated profile identity.

Required resolution: make the foreign-record validity/admission rule and the extent of pre-admission
validation precise and consistent with G-050, then add invalid/missing-compatibility foreign controls.
Do not infer a new policy from the current corpus's omission of those witnesses.

### WP02-CR-005 — New stage-3 gates are not reconciled with G-034 canonical traversal

- classification: **REQUIREMENT_UNCERTAIN**
- owner_decision_required: **true** (path C for an observable stage-3 precedence exception)
- requirements: HIST-002, SER-005, SER-008
- evidence: `spec/core.md:413–420`; `spec/serialization.md:179–191`; G-034 and G-035.

The canonical order among the three recognized typed fields is correct: occurred_at, record_id,
recorded_at. The problem is the new earlier passes: identity validation and closed-shape validation
are all stage 3 and precede those fields. G-034's shared stage-3 depth-first canonical traversal
remains stated without a Layer-02 exception. G-035 authorizes shape-before-fields specifically
for CORE-003 revision records; it does not decide new history-envelope error precedence.
G-048 assigns an unknown-member error but does not settle which simultaneous violation wins.

Minimal recognized record: valid learning/attempt/1 identity, record_id ev-1, valid recorded_at,
`occurred_at: yesterday`, `zz_extra: 1`. The draft/model return `history.envelope_invalid`
(shape first). A single canonical stage-3
traversal encounters occurred_at first and returns `timestamp.invalid`. Another witness replaces
record_type with Attempt and removes zz_extra: the identity-first pass again wins ahead of
occurred_at. These differences survive all source/member order permutations; host-order neutrality
alone does not resolve them. Existing envelope step 13 uses `extra`, which sorts before record_id;
that control does not distinguish a whole-shape prepass from canonical traversal.

Required resolution: explicit Owner clarification of stage-3 gating/traversal for the new records,
or a deciding authority reading that reconciles G-034 with it; then transcribe the exception/rule
in SER-008 and add combined-violation controls. Keep the certified Layer-01 rules and G-035's
revision exception unchanged. Do not silently broaden G-035 to every future closed record.

## Corpus derivation and executions

Independent scratch oracle: `.tmp/work/codex/wp02-derive.py`; its 59 detailed derived observations
are in `.tmp/work/codex/wp02-derived.json`. It implements the draft text only for these review
inputs, using independent ID/number checks, JSON duplicate detection and datetime offset arithmetic;
it never imports `minion_memory` and does not use either production implementation as the oracle.
It is a contract-review probe, not proposed Layer-02 code or evidence of implemented conformance.
The additional witnesses above were executed against that same literal model and checked by reading
the pinned text. Layer 02 has no implementation in this candidate.

**59/59** expectations agree with the draft. That does not confer authority on the contested rules.
The decode expectations were compared in full, including timestamp offset subtraction, six-digit
UTC formatting, unchanged absence of occurred_at, score 1.0 -> 1, normalized schema_version 1.0 -> 1,
and preservation of payload/provenance. No new canonical byte/hash expectation is present to rehash.

| Execution at exact pair | Result |
|---|---|
| Independent expectation derivation | 59/59 match the literal draft |
| `mneme_process check --deep-sources` | 8/8 pass |
| Python canonical suite, project-local managed 3.12.8 | 9 passed, 9 xfailed: 8 ACTIVE scenarios plus discovery; 5 placeholders + 4 DRAFT xfails |
| Plain Cargo `test --locked --offline --test conformance canonical_corpus -- --nocapture` | Fails at tests/conformance.rs:118 on first non-placeholder DRAFT; reproduces NF-026 |

NF-026 is not duplicated as a new finding. I own its Rust runner repair. The handed-off instructions
say "Do not edit the candidate," so this review preserves the exact pair and does not slip a runner
implementation into a review-only branch. Alignment remains required before agreement; counts must
include four draft xfails (8/146/9 at this draft) and must not conceal later ACTIVE promotion.

## Fidelity, seams and Rust feasibility

G-047's separation is preserved: WP-02S does not block this envelope, and later scope consumers must
still wait for it. G-048's recognized closure versus unknown-schema compatibility distinction is
faithfully represented. G-049's mandatory recorded_at, optional/absent occurred_at, timestamp grammar,
no inference and no time inequality are correctly represented. G-051's store-local nature, cross-store
ordering error, structural equality and cursor advancement for excluded records are correctly stated.
G-050 has the unresolved admission/compatibility contradiction above. Numeric, reader and new precedence
choices are the unrecorded additions, not objections to the recorded Owner decisions.

Generic stages across all arguments before typed admission are a sound reuse of G-031; parsing and
SER-008 domain validation are distinct from interpreting a profile payload schema. The corpus's
foreign non-finite payload therefore correctly gives value.number_not_finite before exclusion under
the draft/common stage rules. Error argument names reader/record and a/b follow the declared arguments;
relation errors name none, as in Layer 01. Boundary validity precedes relational comparison, and
recognized typed fields use canonical member order.

Rust is mechanically feasible after these semantic decisions: normalize all arguments through the
existing staged JSON/native seam, inspect exact normalized Values, build recognition membership from
normalized pairs, and reuse Layer-01 IDs/timestamps. No new dependency or lossful representation is
needed. Boundaries can use an integer internally if that domain is approved. The current private
Value arena will need crate-local object/field inspection helpers; this is ordinary Rust implementation
work, not a reason to deserialize through serde_json and bypass stage precedence. Preserve iterative
handling of deeply nested payload/provenance and avoid canonical-byte reparse as a value-copy shortcut.
The feasibility matrix's mechanics are plausible; its domain rows and precedence claims remain
conditional on resolving the findings. Its NF-026 prerequisite is confirmed.

HIST-001/HIST-010 are sound as Layer-02 vocabulary and preservation constraints with later-layer
assurance. They do not prove rebuildability or profile-specific anti-feedback origin recognition here.
The admission API recognizes pairs, not payload schemas, so future profile validation owns those schemas;
no payload callback is supplied or implied by this core contract. A history event referring to a derived
checkpoint must remain distinguished from the derived checkpoint artifact itself in those later layers.

Prior Layer-01 closures are not reopened. This review introduces no MemoryScope decision, persistence
implementation, store allocation policy beyond the flagged draft choice, or automatic next-layer start.

## Per-step derivation ledger

The following observations compare the complete derived result to the corpus; the concise column
shows its distinguishing outcome/error. Step numbers are one-based within each file.

| Scenario | Step | Case | Derived outcome |
|---|---:|---|---|
| boundary-local-cursor | 1 | same store, lower position | less |
| boundary-local-cursor | 2 | same store, same position | equal |
| boundary-local-cursor | 3 | same store, higher position | greater |
| boundary-local-cursor | 4 | position 0 is before the first record | less |
| boundary-local-cursor | 5 | position 2.0 is 2 (one numeric kind) | equal |
| boundary-local-cursor | 6 | different stores are incomparable even at equal positions (G-051) | history.boundary_incomparable |
| boundary-local-cursor | 7 | no order is derived from store IDs | history.boundary_incomparable |
| boundary-local-cursor | 8 | equal pair | True |
| boundary-local-cursor | 9 | different stores: false, not an error (G-051) | False |
| boundary-local-cursor | 10 | different positions | False |
| boundary-local-cursor | 11 | unknown member | history.boundary_invalid (a) |
| boundary-local-cursor | 12 | negative position | history.boundary_invalid (b) |
| boundary-local-cursor | 13 | fractional position | history.boundary_invalid (a) |
| boundary-local-cursor | 14 | position as a string | history.boundary_invalid (b) |
| boundary-local-cursor | 15 | store_id outside the stable-ID domain | history.boundary_invalid (a) |
| boundary-local-cursor | 16 | missing position | history.boundary_invalid (a) |
| boundary-local-cursor | 17 | position beyond the safe integer bound: generic stage 2 | value.integer_out_of_range (a) |
| boundary-local-cursor | 18 | invalid boundary precedes incomparability | history.boundary_invalid (a) |
| boundary-local-cursor | 19 | argument a before argument b | history.boundary_invalid (a) |
| boundary-local-cursor | 20 | equality also validates its arguments | history.boundary_invalid (b) |
| envelope-admission-shape | 1 | minimal recognized envelope | decode |
| envelope-admission-shape | 2 | occurred_at after recorded_at is accepted; no order is required (G-049) | decode |
| envelope-admission-shape | 3 | payload and provenance reach the reader as normalized values (HIST-010) | decode |
| envelope-admission-shape | 4 | schema_version 1.0 is edition 1 (one numeric kind, G-023) | decode |
| envelope-admission-shape | 5 | unknown top-level member (closed envelope, G-048) | history.envelope_invalid (record) |
| envelope-admission-shape | 6 | missing recorded_at (G-049) | history.envelope_invalid (record) |
| envelope-admission-shape | 7 | missing record_id | history.envelope_invalid (record) |
| envelope-admission-shape | 8 | occurred_at null is not unknown; unknown is absence (G-049) | timestamp.invalid (record) |
| envelope-admission-shape | 9 | occurred_at empty string | timestamp.invalid (record) |
| envelope-admission-shape | 10 | record_id outside the stable-ID domain | id.invalid (record) |
| envelope-admission-shape | 11 | typed fields in canonical order: occurred_at before record_id (G-034) | timestamp.invalid (record) |
| envelope-admission-shape | 12 | typed fields in canonical order: record_id before recorded_at | id.invalid (record) |
| envelope-admission-shape | 13 | closed shape before typed fields | history.envelope_invalid (record) |
| envelope-admission-shape | 14 | generic stage 2 before typed fields (G-031) | value.number_not_finite (record) |
| envelope-admission-shape | 15 | generic stage 1: duplicate member | value.duplicate_key (record) |
| envelope-admission-shape | 16 | non-object envelope | history.envelope_invalid (record) |
| envelope-admission-shape | 17 | compatibility outside required\|ignorable | history.envelope_invalid (record) |
| envelope-admission-shape | 18 | schema_version 0 | history.envelope_invalid (record) |
| envelope-admission-shape | 19 | schema_version as a string | history.envelope_invalid (record) |
| envelope-admission-shape | 20 | schema_version fractional | history.envelope_invalid (record) |
| envelope-admission-shape | 21 | record_type outside the token domain | history.envelope_invalid (record) |
| profile-exclusion | 1 | other profile, unrecognized required type: excluded, compatibility not consulted | excluded |
| profile-exclusion | 2 | other profile with the same type name as a recognized type: excluded (namespacing) | excluded |
| profile-exclusion | 3 | other profile is not shape-validated: excluded | excluded |
| profile-exclusion | 4 | missing profile is an envelope error, not exclusion | history.envelope_invalid (record) |
| profile-exclusion | 5 | empty profile is an envelope error | history.envelope_invalid (record) |
| profile-exclusion | 6 | other profile with invalid identity: envelope error | history.envelope_invalid (record) |
| profile-exclusion | 7 | generic stages apply before exclusion (G-031) | value.number_not_finite (record) |
| replay-compatibility | 1 | unrecognized type, ignorable: skip | skip |
| replay-compatibility | 2 | unrecognized type, required: replay stops | history.unknown_required |
| replay-compatibility | 3 | recognized type, unrecognized schema version, required | history.unknown_required |
| replay-compatibility | 4 | recognized type, unrecognized schema version, ignorable | skip |
| replay-compatibility | 5 | unrecognized ignorable is not validated as a known closed schema (G-048) | skip |
| replay-compatibility | 6 | unrecognized required is not validated as a known closed schema (G-048) | history.unknown_required |
| replay-compatibility | 7 | unrecognized with invalid identity: envelope error, not skip | history.envelope_invalid (record) |
| replay-compatibility | 8 | recognized ignorable record is decoded, not skipped | decode |
| replay-compatibility | 9 | reader with an unknown member | history.reader_invalid (reader) |
| replay-compatibility | 10 | reader with a duplicate recognized pair | history.reader_invalid (reader) |
| replay-compatibility | 11 | reader errors precede record errors (declared order) | history.reader_invalid (reader) |
