# WP-03 contract review 2 — Codex

Date: 2026-10-11. Independent reviewer / Rust owner: Codex.

## Verdict

**CHANGES_REQUIRED** for docs `e25190267ce242c558309af462d86071421b7d2e` /
code `2bc2ee126a4c4086d848c099698522bfad5ce09e`.

**WP03-CR-001..004 are CLOSED for this candidate.** New blocking finding:
**WP03-CR-005**, path C, requiring an Owner decision about the external-artifact target domain.
All 49 DRAFT expectations match an independent derivation of the literal candidate. Matching
the draft does not settle the authority of its remaining target-domain restriction.

## Custody and review basis

Followed the handoff at state commit `5df6dd53b7bf93e73ce554050e0e29e018e3a2f2`.
New branch `review/wp03-contract-2` starts there; separate worktrees are
`review-worktrees/docs-wp03-review-2` and detached exact-code
`review-worktrees/code-wp03-review-2`. The docs spec, governance and feasibility contents are
identical to the pinned candidate despite the control descendants. Only this review record is
committed. No production, candidate, shared state, registry, source-bundle or other agent files
were edited. Environments, scratch and Cargo output remained project-local.

Read the complete remediation response, verbatim G-071..G-074, rewritten HIST-007/PROJ-001,
SER-008 and feasibility deltas, both complete scenarios, and the surrounding accepted artifact
and history contracts. Compared against review 1 and its exact pair. Consulted R04 §4 and
the accepted KNOW-009 asset normalization to challenge the new target domain. The deep-source
check verified the source inventory against the read-only upstream bundle.

## Per-finding closure

| Finding | Disposition and independently checked evidence |
|---|---|
| WP03-CR-001 | **CLOSED.** G-071 expressly chooses all self-links invalid, acyclic combined resolution family, independently acyclic derivation family, and no cross-family rule. G-072 chooses strict resolution endpoints, retained unavailable derivation targets, typed targets and relation multiplicity collapse. HIST-007 transcribes these; lineage steps 13, 15–23 distinguish the newly decided behavior, including a permitted cross-family cycle. The separate target-domain issue below is new. |
| WP03-CR-002 | **CLOSED.** G-073 chooses first-occurrence coalescing of complete canonical-envelope equality, duplicate-position metadata/boundary progress, and the first conflicting later position as an atomic entry failure. PROJ-001 moves this into the entry loop. Canonical steps 14–17 cover identical occurrences, conflict, distinct IDs and conflict before a later unknown-required entry. |
| WP03-CR-003 | **CLOSED.** HIST-007 now explicitly assigns closed member sets, IDs, vocabulary and target types/domains to early shape checks, and availability/self-links/cycles to late graph checks. Lineage steps 24–28 exercise the previous mixed-failure ambiguity and conflicting reuse before graph validation. The original non-string-kind witness is now unambiguously lineage.invalid before entry admission. |
| WP03-CR-004 | **CLOSED.** G-074 explicitly chooses direct-only interpretation association, with no inheritance through supersedes/corrects/derived_from. HIST-007 is faithful. Lineage step 14 executes the exact discriminant: e-2 supersedes e-1 without repeating e-1's reinterprets link, so e-2 is current but o-1 has an empty current-interpretation set. |

G-067..G-070 remain intact: canonical shared path, payload-owned decoder output, retained history,
no incidental head selection and atomic unknown-required failure. G-072's compatible base/checkpoint
availability is explicitly deferred to Layer 05, which has the corresponding input/state scope;
Layer 03 uses decoded records only. This is not an invented checkpoint implementation.

## WP03-CR-005 — Required artifact edition narrows G-072's external-target domain

- classification: **REQUIREMENT_UNCERTAIN**
- owner_decision_required: **true**; path **C**
- status: **OPEN**; raised_by: **Codex**; blocking: **[WP-03]**
- requirements: HIST-007, PROJ-001, CORE-003
- evidence: docs `e2519026`, `spec/core.md:590–595, 608–609, 622–624`;
  G-072 verbatim; CORE-003's G-021/G-035 scope; R04 §4 (AssetRecord);
  `spec/learning/knowledge.md` KNOW-009; lineage step 16 at code `2bc2ee12`.

G-072 permits a derivation target to be an external immutable artifact and requires a typed target.
It does not restrict that domain to **semantically versioned artifacts** with a required numeric
edition. The new closed shape `{stable_id, artifact_version}` imposes exactly that restriction.
G-021's immutable semantic revision identity applies to artifacts whose pair denotes such a
revision; it does not say that every immutable artifact has an edition. G-035 explicitly admits
an absent artifact_version for the comparison seam, and CORE-003 then returns not_applicable.
That comparison outcome does not establish that an unversioned artifact is mutable.

The upstream domain also expressly contains assets identified by **identity/version OR content
hash** (R04 §4; accepted KNOW-009). A hash-addressed immutable asset need not manufacture an
artifact edition. G-072 did not exclude that kind of external target from lineage.

Executed draft-model discriminants using an ordinary admitted e-1 and one derived_from relation:

```text
to_artifact: {stable_id: ku-7}                         -> lineage.invalid
to_artifact: {stable_id: ku-7, content_hash: <64 hex>} -> lineage.invalid
to_artifact: {stable_id: ku-7, artifact_version: 3}    -> retained, unresolved derivation
```

The first two are alternative encodings of possible target domains, not proposed approved shapes.
The hash witness is a syntactically specified unavailable reference; no claim of resolving an
actual asset is needed because G-072 expressly retains unavailable derivation targets.
The draft atomically rejects them at the early shape stage. A typed hash-reference branch could
instead preserve the target without pretending it is a record ID or fabricating an edition.
The outcomes differ in acceptance, reference identity and retained provenance, so the current
restriction is not merely lossless field spelling under path B.

Required resolution: Owner choice among (a) limit Layer 03 external targets explicitly to immutable
semantic revisions with stable_id + required CORE-002 edition; (b) support a typed immutable
content-hash reference alongside versioned revisions; or (c) another explicitly defined immutable
target domain. Record the admitted identity forms and distinguish absent/invalid editions and
wrong/multiple target variants. If the narrow form is chosen, the current implementation-friendly
shape can remain, with an explicit scope decision. Do not silently add a hash or optional-edition
branch either: those too would select observable semantics.

## Independent oracle derivation

Executed `.tmp/work/codex/wp03-oracles-2.py` with project-local CPython 3.12.8. It imports YAML
and standard-library helpers, never either production implementation. It is a fixture-domain
derivation, not a proposed Layer 03 implementation. It derives fixture admission, complete
envelope normalization/equality, occurrence coalescing, relation normalization/collapse,
separate iterative graph checks, unresolved retention and direct-only membership.

All fixture timestamps are known UTC civil spellings at 08:00 or 09:00 on 2026-10-11; the derived
canonical forms add `.000000Z`, without conversion or a host time parser. Compared full result
objects and every error code/argument/position, not just selected heads.

**49/49 match.** Evidence `.tmp/work/codex/wp03-oracles-2.json`, SHA-256
`8aaa86266ccc6456852fd27f37893ca0014f214048dc00763ae439af5fe3e426`.
Every unchanged named scenario case also matches its round-1 expectation after adding the two
new empty result fields. This independently confirms that the two deliberate semantic changes
are confined to identical occurrences and identical relations in the old cases.

| Canonical-path step | Derived outcome |
|---|---|
| 1 | Three retained/current records, through 3 |
| 2 | Empty projection, through 0 |
| 3 | o-1/e-1 retained; excluded 2, skipped 3; through 4 |
| 4 | Position gaps allowed, through 9 |
| 5 | unknown_required, position 3, no argument |
| 6 | id.invalid, stream, position 2 |
| 7 | unknown_required at 1 wins over later typed failure |
| 8 | Decreasing positions: stream_invalid |
| 9 | Equal positions: stream_invalid |
| 10 | Entry zero: stream_invalid |
| 11 | Extra stream member: stream_invalid |
| 12 | Extra entry member: stream_invalid |
| 13 | Uppercase store ID: stream_invalid |
| 14 | Identical o-1 coalesced at 1; duplicate metadata position 3; through 3 |
| 15 | Conflicting o-1 content: duplicate_record_id at 2 |
| 16 | Different IDs both retained despite otherwise equal content |
| 17 | Conflicting reuse at 2 precedes later unknown-required record |
| 18 | reader_invalid before stream_invalid |

| Lineage step | Derived outcome |
|---|---|
| 1 | Both direct interpretations e-1/e-2 current |
| 2 | e-1 superseded, e-2 sole current interpretation; all records retained |
| 3 | e-3 converges both heads, current o-1/e-3/c-1 |
| 4 | Permuted relation input yields exactly step 3's result |
| 5 | Correction removes o-1 from heads, retains its history |
| 6 | derived_from preserves all heads |
| 7 | Supersession self-link: lineage.invalid |
| 8 | Supersession cycle: lineage.invalid |
| 9 | Mixed correction/supersession cycle: lineage.invalid |
| 10 | Missing resolution target: lineage.invalid |
| 11 | Excluded resolution target: lineage.invalid |
| 12 | Unknown vocabulary: early lineage.invalid |
| 13 | Equal normalized relations collapse to one edge |
| 14 | Replacement without direct reinterprets link leaves observation group empty |
| 15 | Unavailable record derivation retained in relations and unresolved_derivations |
| 16 | Versioned external artifact retained as typed unresolved derivation |
| 17 | Artifact target on supersedes: early lineage.invalid |
| 18 | Both target variants: early lineage.invalid |
| 19 | derived_from self-link: lineage.invalid |
| 20 | derived_from cycle: lineage.invalid |
| 21 | reinterprets cycle: lineage.invalid |
| 22 | Cross-family cycle alone is allowed; independent graphs acyclic |
| 23 | Unavailable from endpoint: late lineage.invalid |
| 24 | Non-string kind: early lineage.invalid before entry error |
| 25 | Unknown kind: early lineage.invalid before entry error |
| 26 | Invalid endpoint spelling: early lineage.invalid before entry error |
| 27 | Unknown-required at 1 precedes unavailable-from graph error |
| 28 | Conflicting record reuse at 2 precedes self-link graph error |
| 29 | Extra relation member: early lineage.invalid |
| 30 | Missing relation members: early lineage.invalid before entry error |
| 31 | Unknown-required at 2 precedes dangling resolution error |

All stream errors name stream, reader errors reader, lineage errors relations, and unknown-required
errors no argument; entry errors carry the shown positions. Eight distinguishing alternative oracle
outputs were rejected by these comparisons: rejecting identical occurrences, accepting conflict,
rejecting equal relations, inheriting membership, rejecting unresolved derivations, allowing
derivation cycles, combining graph families and delaying the non-string-kind error. This is
oracle discrimination, not a production mutation-test claim.

## Rust feasibility and other observations

The decided graph/occurrence rules remain implementable with existing staged Input/Value
validation followed by explicit closed-shape checks. Normalize envelopes before comparing complete
SER-009 bytes; compare numeric aliases canonically, not host parser tags. Preserve first positions
for available-record ordering and later positions separately for duplicate metadata. Use two graph
families and iterative cycle detection; unavailable derivation targets must not be inserted as
available graph vertices or removed from the output. Equal normalized typed relations can be
deduplicated without input-order selection.

The presentation ordering of unresolved_derivations is path B: available records by position,
unavailable record targets by ASCII stable ID, then artifact revision pairs. This is a deterministic,
lossless rendering of already selected semantic edges, not a preferred-head policy. The chosen
typed **discriminator** is likewise representation mechanics; the admitted artifact identity domain
is the separate path-C issue above. Any added variant must receive an explicit total sort rule.

No new Rust representability problem was found. The feasibility row's structs/enums remain an
output of generic validation, never a replacement for it. The proposed optional error position
must remain distinct from source byte offsets. Original non-blocking questions about G-070's
routing-identity control and generic-stage attribution remain assurance suggestions, not newly
reopened findings. The plan's old 31-step subsection is superseded by its remediation section
and current 49-step corpus; refreshing it would remove stale prose.

## Checks

- Project-local process tool with the exact code and review docs checkout, `--deep-sources`:
  **8/8 PASS**.
- Windows Rust `cargo test --locked --offline`: **32 integration controls and 1 doctest PASS**.
  Layer 03 remains DRAFT; no Layer 03 production execution or POSIX run is claimed.
- Code delta is the two projection corpus files only. Original review record is imported unchanged.
  Candidate worktrees are clean; shared state and registry are untouched by this review.

Return the revised exact pair after the external-target domain is decided. This review approves
neither acceptance onto main nor an implementation guessed around that open choice.
