# WP-02S MemoryScope contract review — Codex

Date: 2026-10-11. Independent reviewer / Rust owner: Codex.

## Verdict

**CHANGES_REQUIRED** for docs `bc362b9ff4139826c9ed5984ddc474d34afbc1ff` /
code `95d1df6022aac1e203e4b677652fb2a885d20185`.

New blocking findings: **WP02S-CR-001, WP02S-CR-002**. NF-026 remains the separately assigned
Rust runner task and is not duplicated here. The matching semantics and the six-dimension
conformance set are otherwise faithful to G-056..G-063. All 69 observations match the literal
candidate plus the corpus's validation operation; matching a draft does not settle its authority.

## Custody and review basis

Followed the handoff at state head `21ec7de2`. The new branch `review/wp02s-contract-1` starts
there, in `review-worktrees/docs-wp02s-review`; code is a separate detached exact-SHA checkout
in `review-worktrees/code-wp02s-review`. Only this record is committed. Scratch files, caches
and targets are project-local. No candidate, state, registry or other worktree edits.

Read the Owner decisions, the characterization's passage register and analysis, the decision
packet, scope spec, feasibility matrix and all three scenarios. Checked the path-A additions
against the pinned source-text passages and the source provenance inventory. Source hashes and
anchors were independently verified by the deep-source mechanical check. The research/packet
are evidence objects, not substitutes for the selected Owner answers.

## Findings

Both findings are OPEN, raised_by Codex, blocking [WP-02S]. Spec and governance references below
are at docs `bc362b9f`; scenarios are at code `95d1df60`.

### WP02S-CR-001 — The facet-name grammar changes acceptance; it is not purely path B

- classification: **REQUIREMENT_UNCERTAIN**
- owner_decision_required: **true** (path C)
- requirements: SCOPE-001, SCOPE-002, SCOPE-003
- evidence: `spec/scope.md:100–103`, G-056/G-057/G-061, characterization Q7, and
  `core.scope.value-shape` step 11.

G-056 chooses canonical namespaced names in `<profile>.<facet>` form; G-057 says their dotted
spelling is lexical and carries no hierarchy. Neither decision chooses **dot-free CORE-001
segments**, segment length limits or reserved-device-name rejection for facet names. G-056
chooses portable-token **values**, not the full stable-ID grammar for each part of a facet name.
The draft calls these additional acceptance restrictions path B. A representation of a semantic
name must preserve its admitted domain; rejecting names changes the domain.

Executed discriminants against an independent literal draft model:

```text
validate_scope({scope_state: resolved, facets: {"agent.session.x": "s-1"}})
    -> scope.invalid, argument scope
validate_scope({scope_state: resolved, facets: {"agent.con": "s-1"}})
    -> scope.invalid, argument scope
```

The first is already a corpus expectation. A 129-character facet segment is likewise rejected.
An alternative lexical domain can represent these as unknown future facet names, preserve them
and return false on ordinary visibility under G-061, rather than reject the stored scope. Neither
alternative infers hierarchy. The author-selected grammar therefore distinguishes invalid scope
from preserved unknown scope and changes validation/equality outcomes.

Required resolution: Owner decision fixing the facet-name domain (including delimiter count,
segment grammar/length and reserved-name behavior), or specific deciding authority for each
restriction. Keep the six canonical Agent names and CORE-001 value domain unchanged. Do not
choose a broader grammar silently either: that would also be a semantic choice.

### WP02S-CR-002 — Corpus validation seam and error argument are missing from the spec

- classification: **CONTRACT_ASSURANCE_DEFECT**
- owner_decision_required: **false**
- requirements: SCOPE-001, SCOPE-002
- evidence: `spec/scope.md:138–173`; `core.scope.value-shape` steps 1–16.

The spec defines `scope_visible(record, query)` and `scopes_equal(a, b)` but never defines
`validate_scope(scope)`. The corpus calls it 16 times, returns normalized scope values on success,
and names `scope` on errors. The error paragraph lists only record/a/b arguments. An independent
implementer must infer an extra public operation, its return contract and a new declared argument
name from the corpus rather than the normative API text. The representation may be lossless,
but the operation mapping needs to be explicit for a thin runner.

Minimal witness: `validate_scope({scope_state: resolved})` is corpus step 7, expected
`scope.invalid` with argument `scope`. My draft-plus-corpus model reproduces it, but the spec's
operation/error list cannot by itself derive that operation and argument. In contrast,
`scopes_equal` with that value as b explicitly names b and is specified.

Required resolution: define the validator's public input, normalized result, generic/typed stage
behavior and `scope` argument naming in the spec (or change the corpus to a genuinely specified
public seam). Clarify argument order for equality explicitly as a then b. The existing value
rules determine validation semantics; this repair does not require a new Owner choice. Include
or cross-reference the scope error vocabulary in the common stage table for implementers.

## Representation choices and fidelity

- **Two-state record:** sound path B. It represents the Owner's resolved map plus a separate
  unresolved value bijectively; facets remain exact and unresolved cannot collapse to global.
  Closedness prevents alternative encodings from becoming a third semantic state.
- **Query bare map:** sound path B for G-058's resolved allowed-scope map. Unknown queries are
  rejected under G-061; no unresolved query is silently interpreted as global.
- **Error names:** scope.query_invalid is explicit in G-061. scope.invalid names the rejection
  class for values outside the agreed domain; its spelling does not select a new visibility
  policy. The missing validator/argument transcription is CR-002.
- **Registry held in core, Agent-only:** sound representation of G-061/G-062. The six canonical
  names are selected by the Owner; Learning adoption is deferred. The core does not invent
  learning aliases or a learning vocabulary. Records with well-formed unknown facets are preserved
  and fail closed, while unknown queries reject. Future vocabulary changes remain versioned.
- **One-dot grammar:** acceptance restriction, not proven path B; CR-001.

G-056's single values, exact equality, absent/present distinction, global empty scope, immutable
canonical content and revision/lineage rules are retained. G-057's flat facets and explicit future
widening policy are retained. G-058's subset matching and query omission behavior are accurately
stated; G-059's public indistinguishability from absence, separate audit, bounded telemetry and
consolidation deferral are accurately stated. The Layer-02 pure matcher does not by itself prove
search/count/ID-lookup privacy; those consumers remain later-layer obligations.

G-060's unresolved/hidden/new-revision model is retained, while actual capture is deferred to Layer
13, as the packet's landing table specifies. When that layer consumes the decision, it must use
the Owner's strengthened rule: **any** missing/ambiguous/incomplete context requires unresolved;
a resolved capture may omit a facet only with affirmative knowledge of intentional unconstrainedness.
The older packet recommendation (unresolved only when no facets are known) is not authority. The
current pure scope validator cannot and must not guess capture context from a facet map. This is
recorded as a deferred consumer obligation, not an additional blocker on this core API.

G-062 keeps current Learning records unscoped, not implicitly global or unresolved; G-063's six
Agent dimensions all have match/mismatch/record-omission/query-omission controls and composed
mismatch controls. No new capture, Learning adoption, hierarchy or cross-agent sharing decision
is inferred.

## Path-A source omissions

The added references are sound: allowed scope and scope-bearing observations/projections/request
reconstruction (R05 5.1/5.5/5.6/6/11); scope-aware ranking (MVP 18.3); distinct namespaces/scopes
(R01 21); isolation acceptance (R05 16); private-record omission (R05 15); profile separation
(R05 13); deferred automatic sharing/global synthesis (R05 17). Package authoritative scope and
runtime scoped services are correctly treated as homonyms, not MemoryScope semantics. R00 21's
permissive Learning adoption is consistent with G-062. The six-dimension versus four-test subset
is resolved by G-063, not by discarding normative session/task constraints.

Pinned source provenance: R05 SHA-256
`a6c5dee570a5673a34fcd4a33057b2b3faeb1330847b2060235d903a99a4f240`, R01
`51c6a31f987d3ebe8fd4170d54508197d54e742150bb5966637a9faf47bbea51`, R00
`50a0fc28fca0a2e8fc4b42932a7388eb9e150b1e429ba110e95420c0a32d18d1` in the
candidate source inventory. The characterization's 93 passages establish the audit trail; I do
not claim to have mechanically reproduced all of its quoted fragments as literal contiguous text.

## Independent derivation and gates

Scratch oracle `.tmp/work/codex/wp02s-derive.py` uses independent token/name predicates and exact
map/subset operations, not either production library. Detailed per-step observations are in
`wp02s-derived.json`. The validator operation in this scratch model is inferred from the corpus
and deliberately identified as such; CR-002 explains that missing spec seam.

| Scenario | Independently derived observations |
|---|---:|
| scope-value-shape | 21/21 |
| scope-applicability-matching | 17/17 |
| scope-agent-isolation-six-dimensions | 31/31 |
| Total | 69/69 |

The six-dimension set contains 24 individual controls (four per dimension), six composed single
mismatches and one composed all-match. Unknown and unresolved records stay hidden; empty/global
and omitted facets behave as G-058 requires; equality preserves all unknown facets and distinguishes
unresolved from global. No canonical byte/hash oracle is added by this candidate.

`mneme_process check --deep-sources`: **8/8 pass**. Python canonical suite on project-managed
CPython 3.12.8: **9 passed, 8 xfailed** (eight ACTIVE scenarios plus discovery; five placeholders
and three scope drafts). Draft xfails are not implementation conformance evidence. NF-026's
Rust DRAFT assertion remains unchanged and is handled next under the explicit separate assignment.

## Rust readiness

Mechanically feasible after CR-001/002: normalize across all arguments before typed checks; inspect
exact normalized Value objects; represent resolved/unresolved internally as an enum; compare names
and tokens exactly; validate the query even when the record will be hidden; then apply the fixed
registry and conjunctive subset test. Matching order cannot influence a boolean result. Structural
validation errors share scope.invalid, so no new record-gating precedence exception is necessary.
Use the existing staged seam and iterative arena helpers rather than implementing scope semantics
in the runner. Preserve unknown record constraints during normalization and equality. The feasibility
matrix is plausible but its facet-name domain is contingent on the Owner resolution and its public
validator seam must be completed.

This review does not accept onto main, certify the layer, or update coordination state.
