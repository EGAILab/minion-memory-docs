# WP-02S contract review 2 - Codex

Date: 2026-10-11. Independent reviewer / Rust owner: Codex.

## Verdict

**CHANGES_REQUIRED** for docs `acb572513c016ef7bd6bfccda9437568d8012b3d` /
code `0c569afba20477e0687a1de837b70e4b8996fa1e`.

The normative repairs resolve **WP02S-CR-001 and WP02S-CR-002**. One new blocker in
that same neighborhood remains: **WP02S-CR-003**, the feasibility matrix contradicts
G-064's accepted facet-name domain. No new Owner choice is needed.

## Custody and scope

Followed `process/handoffs/WP-02S-codex-contract-review-2.md` at state head `72f99fa5`.
New docs branch `review/wp02s-contract-2` starts there in
`review-worktrees/docs-wp02s-review-2`; separate code checkout is detached at the exact
candidate in `review-worktrees/code-wp02s-review-2`. Only this record is committed.
No candidate, state, registry, production code or other worktree was changed.
All scratch, caches and environments are project-local; each shell sourced the
project environment. Review is targeted to the two findings and direct regressions.

## Per-finding dispositions

### WP02S-CR-001 - resolved by G-064 and its normative transcription

The verbatim Owner decision and `spec/scope.md` now agree: exactly two lowercase ASCII
segments, one literal dot, each segment 1-128 bytes, initial `[a-z0-9]` and remaining
`[a-z0-9_-]`. Device names are not excluded. Facet values remain CORE-001 tokens.
This acceptance choice is explicitly G-064, no longer called path B. Only the
lossless two-state scope representation retains that label.

Consequences independently derived:

- `agent.con` is well formed and preserved by validation, then hidden as unknown.
- `agent.session.x` is invalid, not a future unknown facet.
- 129-byte segments, Unicode and uppercase names are invalid.
- 128-byte namespace plus dot plus 128-byte facet (257 bytes total) is well formed.
- `con.prn` is a well-formed unknown name; a facet **value** of `con` is still invalid.

The outstanding feasibility transcription is classified separately below; the
semantic authority uncertainty itself is closed by the Owner's explicit choice.

### WP02S-CR-002 - resolved

`validate_scope(scope)` is now an explicit single-argument public primitive returning
the normalized scope, with exact unchanged facet names/values and preservation of
well-formed unknown facets. Generic validation precedes scope validation. Its errors
name no argument, consistently with the single-argument Layer 01 convention.
`scope_visible` declares record then query; `scopes_equal` declares a then b; both
name the failing argument. The two scope codes are in SER-008's stage-3 table.

All eleven existing validator-error expectations now omit the argument field.
The two added invalid-name controls likewise expect only `scope.invalid`. This is a
clear operation and error contract that does not require guessing from the corpus.

## Independent expectation derivation and regressions

The own spec model executed **73/73** scope corpus observations: 24 value/shape,
18 matching and 31 six-dimension isolation. The latter still includes four individual
controls per dimension, six composed mismatches and one composed match. Matching,
global/unresolved distinctions, exact equality and unknown-facet behavior are unchanged.

The four new corpus expectations re-derived from G-064/G-061:

| Control | Derived expectation |
| --- | --- |
| Validate `agent.con: c-1` | Return the exact normalized resolved scope, preserving the facet |
| Validate a 129-byte facet segment | `scope.invalid`, no argument |
| Validate `agent.séance` | `scope.invalid`, no argument |
| Match a record carrying `agent.con` | `false`, without dropping the constraint |

Nineteen additional direct model controls passed: exact segment boundaries, allowed
ASCII punctuation/initial characters, reserved-name separation from facet values,
unknown query rejection even for an unresolved record, and a/b error naming/order.
These are executed contract models, not evidence that a MemoryScope implementation
already exists. No production scope code was added or modified.

`mneme-process check --deep-sources`: **8/8** for the exact checkout pair. The Python
canonical runner: **9 passed, 8 xfailed** (5 placeholders plus the 3 scope drafts).
Code diff from `95d1df60` changes only the three scope corpus files: four new steps,
the eleven single-argument expectation changes, and governance-description updates.
Spec diff adds G-064, the validator and error/order text, and the scope stage-table row.
Unrelated rows and prior semantic closures were not reopened.

Scratch reproduction: `.tmp/work/codex/wp02s2-derive.py`; outputs
`wp02s2-derived.json` and `wp02s2-grammar-controls.json`.

## WP02S-CR-003 - feasibility guidance still specifies the rejected old grammar

- **classification:** CONTRACT_ASSURANCE_DEFECT
- **owner_decision_required:** false
- **blocking:** WP-02S contract agreement
- **requirements:** SCOPE-001, SCOPE-002; G-064
- **status:** OPEN
- **Evidence:** docs `acb57251`, `assurance/layers/02s-feasibility-matrix.md`,
  section 1 facet-name row and section 2 H11 row, versus `spec/scope.md` Facet names
  and `reference/governance/2026-10-11-owner-wp02s-memoryscope.md` G-064.

The implementation-facing matrix still says facet names are **two dot-free CORE-001
tokens joined by one dot**. H11 likewise says facet names and values are CORE-001
tokens. CORE-001 rejects device basenames; G-064 deliberately does not do so for
facet-name segments. The matrix has not been updated by this remediation.

Minimal discriminant, executed through both literal grammar models:

```text
validate_scope({scope_state: resolved, facets: {"agent.con": "c-1"}})
G-064/spec/corpus: valid, return the scope unchanged
Matrix's two CORE-001-segment rule: con is reserved -> scope.invalid
```

A Rust implementer following this guidance would reasonably reuse the stable-ID
validator on each segment and violate the newly added normative scenario. The pure
map operations remain feasible; the claimed grammar is what is wrong. This is a direct
regression of the CR-001 repair, not an unrelated reopened scope question.

**Required repair:** update the facet-name domain and H11 explanation to G-064's
separate segment grammar, retaining CORE-001 only for facet values. Include the
reserved-name distinction and segment bounds in the implementation guidance. Update
the matrix's governance range to include G-064. `plans/WP-02S.md` also still reports
69 DRAFT steps rather than 73; correct that stale progress count with the record sweep.
No semantic decision or candidate code change is required for the demonstrated issue.

Approval would only agree this exact contract candidate, not certify an implementation
or grant acceptance onto main. That approval is withheld until the contradictory
implementation guidance is repaired.
