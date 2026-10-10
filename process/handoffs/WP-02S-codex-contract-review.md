# Hand-off — WP-02S CONTRACT_REVIEW (Codex)

**From:** Claude (contract author). **To:** Codex (independent reviewer, Rust owner).
**Governance:** G-047 (split); G-056…G-063 (MemoryScope decisions on the consolidated packet,
verbatim in `reference/governance/2026-10-11-owner-wp02s-memoryscope.md`).

## Exact candidate

- **docs:** `bc362b9ff4139826c9ed5984ddc474d34afbc1ff` on `wp02s/scoping`, followed by state-only descendants.
- **code:** `95d1df6022aac1e203e4b677652fb2a885d20185` on `wp02s/contract`. Its parent is code `main` `cc3c5d54`; the delta is corpus and
  manifest only.

## Scope

WP-02S is Layer 02 MemoryScope: SCOPE-001…006 and NF-018. It is independent of WP-02.

The candidate contains:
- **Spec.** `spec/scope.md`: the "Layer 02 MemoryScope contract" section (value, vocabulary,
  matching, errors, conformance), the transcribed source omissions and the homonym note.
- **Research and decisions.** `assurance/layers/02s-memoryscope-characterization.md` (93 passages)
  and `02s-owner-decision-packet.md`.
- **Corpus.** Three DRAFT scenarios in code `conformance/core/scope-*.yaml`, 69 steps, with their
  manifest links.
- **Feasibility.** `assurance/layers/02s-feasibility-matrix.md`.

**Author representation choices (path B), flagged in the spec for your challenge:**
- the two-state scope record `{scope_state, facets}`;
- the one-dot facet-name grammar;
- the error codes `scope.invalid` and `scope.query_invalid` (`scope.query_invalid` is named by
  G-061);
- the shape of the `query` argument;
- a core-held registry holding only the Agent vocabulary.

## Asked

1. **Fidelity.** Is every Owner decision G-056…G-063 transcribed faithfully? Is any remaining
   choice an unrecorded path C?
2. **Path A.** Are the source-omission transcriptions sound?
3. **Corpus.** Re-derive the 69 expectations from the text.
4. **Rust readiness.**
5. **NF-026.** It applies here too (DRAFT in the Rust runner).

## Verdict

Record `assurance/reviews/WP-02S-contract-review-codex.md` on a new branch
`review/wp02s-contract-1` from the docs state head. Use exactly one of `APPROVED` or
`CHANGES_REQUIRED`. Do not edit the candidate.
