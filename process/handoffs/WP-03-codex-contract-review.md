# Hand-off — WP-03 CONTRACT_REVIEW (Codex)

**From:** Claude (contract author). **To:** Codex (independent reviewer, Rust owner).
**Governance:** G-066 (start); G-067…G-070 (scope, lineage, current heads, atomic failure), verbatim in
`reference/governance/2026-10-11-owner-layer03-start.md`.

## Exact candidate

- **docs:** `eb2bd5d982dd1224789dbc832effc3527bbd6dfa` on `wp03/contract`, followed by state-only descendants. Its base includes the
  Layer 02 post-acceptance records.
- **code:** `d3ae16680ed8694eaba3384daf582eda408d397f` on `wp03/contract`. Its parent is code `main` `a5506d0d`; the delta is corpus and
  manifest only.

## Scope

WP-03 is Layer 03: PROJ-001, PROJ-002, HIST-006 and HIST-007, plus HIST-001's determinism.

The candidate contains:
- **Spec.** Layer 03 blocks in `spec/core.md`: HIST-006 (corrections append), HIST-007 (lineage),
  PROJ-001 (`project_history`) and PROJ-002. New SER-008 stage-table rows.
- **Corpus.** Two DRAFT scenarios, `conformance/core/projection-*.yaml`, 31 steps. The semantic
  expectations are hand-written literals.
- **Feasibility.** `assurance/layers/03-feasibility-matrix.md`.

**Author choices flagged in the plan for your challenge:**
- the stream shape and the `history.stream_invalid` code;
- the result shape and its presentation order;
- `reinterprets` counting as resolution-affecting;
- dangling links being invalid;
- duplicate decoded `record_id`s being an error;
- duplicate relation triples being invalid;
- the new error `position` attribute.

Any of these that is really an observable choice should be named as path C, for the Owner.

## Asked

1. **Fidelity** to G-067…G-070. Flag any unrecorded path C.
2. **Corpus.** Re-derive the 31 expectations from the text.
3. **Rust readiness.**

## Verdict

Record `assurance/reviews/WP-03-contract-review-codex.md` on `review/wp03-contract-1`. Use exactly one
of `APPROVED` or `CHANGES_REQUIRED`. Do not edit the candidate.
