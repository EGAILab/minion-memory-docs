# WP-03 Layer 03 contract review — Codex

Date: 2026-10-11. Independent reviewer and Rust owner: Codex.

## Verdict

**CHANGES_REQUIRED** for docs `eb2bd5d982dd1224789dbc832effc3527bbd6dfa` /
code `d3ae16680ed8694eaba3384daf582eda408d397f`.

Blocking findings: **WP03-CR-001..004**. Findings 001, 002 and 004 are path C and require Owner
decisions. Finding 003 is a contract-assurance defect. No implementation defect is alleged:
this candidate adds contract and DRAFT corpus, not a Layer 03 implementation.

## Custody and authority

Read the handoff at docs control head `197d151b`. Review branch `review/wp03-contract-1`
starts there in `review-worktrees/docs-wp03-review`. Code is a separate detached exact-candidate
checkout in `review-worktrees/code-wp03-review`. Only this record is committed. Candidate files,
shared state, registry, upstream bundle and other worktrees were not edited. All scratch evidence,
caches and build outputs are project-local; every shell first sourced the project environment.

Read G-066..G-070 verbatim, the WP-03 plan, Layer 03 spec blocks, the SER-008 stage rules,
Layer 02 admission/boundary rules, feasibility matrix, manifest delta and both complete scenarios.
Checked relevant source passages: R03 §§13–14; R04 §§31–36; IAA A16–A19; Foundation historical
integrity and dual-profile boundaries. References below are pinned to the exact docs candidate
unless explicitly stated otherwise. Source inventory and upstream hashes passed the independent
deep-source check. Author labels and matching draft expectations do not resolve authority.

G-067's single shared path, historical retention and Layer 04 boundary are preserved. G-068's
payload/decoder ownership and unchanged closed envelope are stated. G-069's set-valued heads,
absence of incidental selection and versioned consumer policy are preserved in the exercised
examples. G-070's atomic failure, position and routing-identity requirement are stated. The
remaining issues concern extra acceptance rules and unspecified semantic/validation boundaries.

## Findings

All four are OPEN, raised_by Codex, blocking [WP-03].

### WP03-CR-001 — Additional lineage rejection rules are observable path-C decisions

- classification: **REQUIREMENT_UNCERTAIN**
- owner_decision_required: **true**; path **C**
- requirements: HIST-007, PROJ-001
- evidence: `spec/core.md:600–613`; G-068; `plans/WP-03.md` author choices;
  lineage scenario steps 10, 11 and 13.

G-068 requires self-link/cycle rejection in resolution-affecting supersession relations. The draft
additionally (a) includes `reinterprets` in the cycle graph, (b) rejects self-links even for
non-resolution-affecting `derived_from`, (c) rejects all dangling endpoints, including excluded or
skipped records, and (d) rejects repeated identical triples. R03 §13, R04 §35 and IAA A16 require
auditable overlays; they do not choose these four additional rejection domains. Defining the
shared vocabulary does not automatically authorize choosing all its observable validity rules.

Executed draft-model discriminants, with ordinary admitted records `o-1`, `e-1`, `e-2`:

| Relations | Draft outcome | Distinguishing alternative |
|---|---|---|
| `e-1 reinterprets e-2`, `e-2 reinterprets e-1` | `lineage.invalid` | Check only supersession/replacement edges for cycles; keep both heads |
| `e-1 derived_from e-1` | `lineage.invalid` | Preserve a non-resolution provenance self-link |
| `e-1 derived_from absent` | `lineage.invalid` | Preserve an unresolved external/prefix reference explicitly |
| Twice `e-1 derived_from o-1` | `lineage.invalid` | Treat the relation set idempotently |

These alternatives change success versus atomic failure, not merely encoding. The third need
not silently repair a link: an explicit unresolved state also satisfies G-067's demand to surface
ambiguity. Neither alternative is approved here.

Required resolution: an Owner options packet deciding each rule (including `reinterprets` cycle
participation and the `derived_from` exception/domain), followed by transcription and controls.
The Owner may choose the draft exactly; acknowledgement by the author is not that decision.
Keep the already-decided supersession self-link/cycle errors and no-tie-break rule.

### WP03-CR-002 — Duplicate decoded IDs are not decided by deferring durable idempotency

- classification: **REQUIREMENT_UNCERTAIN**
- owner_decision_required: **true**; path **C**
- requirements: HIST-006, PROJ-001
- evidence: `spec/core.md:701–703`; G-067; R04 §§32, 36;
  canonical-path step 14 at code `d3ae1668`.

The draft fails two decoded records with the same `record_id`, including byte-identical retries,
as `history.duplicate_record_id` at the later position. G-067 defers durable idempotency to
Layer 04; it does not decide how a pure projector treats a supplied repeated identity. R04 §36
forbids semantic deduplication of observations, but does not equate identity-level replay handling
with semantic deduplication or mandate this specific error.

The executed step-14 derivation yields `history.duplicate_record_id`, argument `stream`, position
3, for identical `o-1` envelopes at positions 1 and 3. Alternatives include fail-all-duplicates,
coalesce identical identities while rejecting conflicting content, or retain occurrences with an
explicit occurrence/lineage identity policy. These differ in success, retained records and graph
addressing. They require an Owner decision; none can be selected by calling it corrupt history.

Required resolution: decide identical and conflicting duplicates separately, preserve the
no-semantic-dedup invariant, specify the error precedence/position, and add distinguishing controls.

### WP03-CR-003 — Relation shape versus graph validation has no complete stage boundary

- classification: **CONTRACT_ASSURANCE_DEFECT**
- owner_decision_required: **false**; repair the defined validation contract
- requirements: HIST-007, PROJ-001, SER-008
- evidence: `spec/core.md:590–613, 691–705`; SER-008 Layer 03 rows;
  lineage steps 12, 14–16.

PROJ-001 checks the "shape of relations" before admitting entries, then validates lineage after
admission and duplicate-ID checks. HIST-007 describes a closed triple and invalid kinds/endpoints,
but never exhaustively defines the early shape predicate: required member types, endpoint ID
grammar, and whether the vocabulary is an early enum check or a late graph check. The corpus
distinguishes a missing member from a dangling endpoint, but not these boundary cases.

Executed two plausible stage readings on the same input:

```text
stream: one otherwise valid required record of unrecognized type mystery at position 1
relations: [{from_record_id: o-1, relation: 17, to_record_id: o-1}]

closed-member-set-only early shape -> history.unknown_required, position 1
closed-member-set + string-field early shape -> lineage.invalid, argument relations
```

Both reject the relation on its own. They disagree in this mixed-failure case. Similarly,
`relation: replaces` and an invalid endpoint spelling require an explicit early/late assignment.
An independent implementer must not infer error precedence from its struct/enum deserializer.

Required resolution: list every early shape/type/domain check and every late graph check;
define argument/position attribution for them; add paired controls with an earlier failing entry
and with duplicate decoded IDs. If deciding the boundary entails a new observable policy outside
the existing stage authority, route that decision to the Owner rather than treating this finding
as permission to select it.

### WP03-CR-004 — Observation association across replacement is an unrecorded semantic choice

- classification: **REQUIREMENT_UNCERTAIN**
- owner_decision_required: **true**; path **C**
- requirements: HIST-007, PROJ-001, PROJ-002
- evidence: `spec/core.md:614–618`; G-068/G-069; R03 §13 and R04 §35;
  lineage scenario steps 2–4.

The draft's current-interpretations rule uses direct `reinterprets` edges only. Every replacement
example repeats the observation edge on the replacing record, so the corpus does not distinguish
direct-only association from association inherited along replacement links.

Executed discriminant:

```text
e-1 reinterprets o-1
e-2 supersedes e-1
```

The literal draft returns `e-2` as a current head but `interpretations` contains
`{observation: o-1, current: []}`. A replacement-chain reading returns `[e-2]` for that observation.
G-069 decides no tie-break and all unsuperseded interpretations, but does not decide whether the
replacement inherits the replaced interpretation's observation association. Neither do the cited
overlay passages. This is an observable result-membership choice, not the spelling of the result.

Required resolution: Owner decision on direct-only versus inherited association (or an explicit
requirement that replacement records repeat the observation relation), including `corrects`,
multi-head convergence and replacements spanning different observations. Add a control without
the repeated observation edge. Keep every historical record and avoid incidental tie-breaks.

## Independent derivation of all 31 expectations

Executed `.tmp/work/codex/wp03-oracles.py` using project-local CPython 3.12.8. It imports YAML,
not either production implementation. It derives admission/normalization for the fixture domain,
then resolves a graph using iterative topological elimination, ordered membership and explicit
target removal. All fixture timestamps denote the independently known UTC instant
`2026-10-11T08:00:00.000000Z`; none requires a time-library oracle. Whole result records, including
retained envelopes, through-boundary, skipped/excluded positions and relation order, were compared.

**31/31 match the literal draft.** This conditional result does not approve the choices in the
findings. The derivation script is deliberately fixture-scoped, not a general production decoder.
Evidence: `.tmp/work/codex/wp03-oracles.json`, SHA-256
`d3386720acc280a906d026c1adce751803806ef3b75d86d8b8961b3db443d6e4`.

| Canonical-path step | Re-derived result/reason |
|---|---|
| 1 | Three decoded retained envelopes; all three current; through 3 |
| 2 | Empty records/relations/current; through 0 |
| 3 | Retain o-1/e-1; excluded 2, skipped 3; through 4 |
| 4 | Gapped positions accepted; through 9 |
| 5 | Unknown required fails atomically at 3 |
| 6 | Invalid stable ID: id.invalid, stream, position 2 |
| 7 | Position-1 unknown required precedes position-2 typed error |
| 8 | Decreasing positions: history.stream_invalid |
| 9 | Equal positions: history.stream_invalid |
| 10 | Entry position zero: history.stream_invalid |
| 11 | Extra stream member: history.stream_invalid |
| 12 | Extra entry member: history.stream_invalid |
| 13 | Uppercase store ID: history.stream_invalid |
| 14 | Repeated decoded identity: history.duplicate_record_id, stream, position 3 |
| 15 | Reader shape failure precedes stream shape failure |

| Lineage step | Re-derived result/reason |
|---|---|
| 1 | Both e-1/e-2 interpretations current; all five retained/current |
| 2 | e-1 removed from heads; e-2 is o-1's sole current interpretation; all history retained |
| 3 | e-3 converges e-1/e-2; heads o-1/e-3/c-1 |
| 4 | Permuted relations give the same complete result as step 3 |
| 5 | Corrects removes o-1 from heads; retains o-1 in history |
| 6 | derived_from preserves all heads; no interpretation group |
| 7 | Supersession self-link: lineage.invalid |
| 8 | Supersession cycle: lineage.invalid |
| 9 | Mixed corrects/supersedes cycle: lineage.invalid |
| 10 | Unknown endpoint: lineage.invalid |
| 11 | Excluded endpoint: lineage.invalid |
| 12 | Unknown relation vocabulary: lineage.invalid |
| 13 | Duplicate triple: lineage.invalid |
| 14 | Extra relation member: lineage.invalid |
| 15 | Missing relation members precede unknown-required entry failure |
| 16 | Unknown-required entry at 2 precedes dangling graph failure |

All stream shape errors name `stream`; reader errors name `reader`; lineage errors name
`relations`; unknown-required errors name no argument. These attributes were compared too.

Four independent oracle mutations were killed: keeping only the last head (9 controls), dropping
superseded history (4), ignoring relations (6), and omitting error positions (5). These are
derivation negative controls, not claims about a future implementation's mutation score.

## Feasibility, representation choices and remaining questions

Rust has no representability obstacle: use the existing generic `Input`/`Value` stage seam before
typed extraction, retain store positions, map stable identities explicitly, resolve iteratively,
and sort presentation explicitly. Existing integer-domain validation bounds positive entry
positions by 2^53−1, so u64 is sufficient after validation. Validate reader/stream/relations jointly
before admission; constructing Rust typed structs/enums first must not determine the first error.
The current errors need an optional store-position field distinct from their existing byte-offset
diagnostic. The feasibility matrix's unconditional FEASIBLE is technically plausible but does not
establish implementability from text alone until findings 003 and the semantic decisions resolve.

The stream/result field spelling, closed encoding of those declared values, and deterministic
presentation of the preserved set can be path B: they retain identity, membership and store order
without selecting a preferred interpretation. The position attribute encodes G-070's required
store-position diagnostic. Neither explanation extends to duplicate/dangling rejection or graph
membership changes. `reinterprets` is called resolution-affecting in the draft but does not remove
its target from `current`; its present extra effect is cycle validity and grouping, not supersession.

Questions/assurance improvements, not additional blockers:

- State explicitly that the third argument is externally produced normalized decoder output,
  and that this core function does not invent a profile payload encoding or independent decoder.
  The reader remains the Layer 02 closed recognition descriptor, not a callable decoder registry.
- Add an observable control for G-070's routing identity. Existing unknown-required expectations
  check code and position, not that profile/type/schema are identified in detail. No exact free-text
  formatting is requested; the required identity must nevertheless be verifiable.
- Clarify generic-stage diagnostics: stages 1–2 run over the entire stream before entry admission.
  A malformed whole-stream JsonText cannot always yield a reliable entry position. Limit the
  entry-position promise to attributable failures, and distinguish it from source byte offsets.
- Narrow relation-order independence to successfully validated relation sets, or define diagnostic
  invariance deliberately. SER-008 still requires source/index order for certain generic failures.

## Executed checks and disposition

- `mneme_process.cli check --deep-sources`: **8/8 PASS** (repos, sources, spec, manifest,
  conformance, findings, registry, state), using this review checkout and exact code candidate.
- Windows Rust `cargo test --locked --offline`: **32 integration controls and 1 doctest PASS**.
  The Layer 03 DRAFT cases do not become silently successful implementations; the existing runner
  handles them under the reviewed DRAFT rule. No POSIX run or Layer 03 production execution is
  claimed in this contract-only review.
- Code delta from certified main is exactly the two corpus files and manifest. Docs carries
  Layer 02 closing/certification records alongside the new contract; no unrelated implementation
  delta was found. Prior certified Layers 01–02 are not reopened.

Resolve the Owner choices and the relation stage contract, update their distinguishing controls,
then return the exact revised pair for review. This verdict grants no acceptance onto main.
