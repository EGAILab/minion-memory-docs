# Hand-off — WP-02 final complete review (Codex)

**From:** Claude. **To:** Codex. **Stage:** FINAL_CONTRACT_REVIEW, because this candidate was
remediated (`process/coordination-state.md` §5).

## Exact candidate

- **docs:** `d603683a67243cb60d6c747e6d6afb5192634076` on `wp02/contract`, followed by state-only descendants.
- **code:** `43e0984e585975719231ba53466a9c78eba796e7` on `wp02/contract`.

## History you have already reviewed

- Contract: `42d3d03e` (CHANGES_REQUIRED), then `18902542` (APPROVED); Owner G-047…G-055.
- Python implementation: `a29b0092` (CHANGES_REQUIRED, CR-006), then `cb439331` (APPROVED).
- NF-026 runner fix: your `b9f42d42`, approved by Claude in `8a071acc`.

## Asked: one complete review of WP-02 at the exact pair

1. **Contract.** HIST-001/002/005/010 and SER-005/006, read as one consistent text and faithful to
   G-047…G-055.
2. **Corpus.** The four ACTIVE history scenarios, the README Drafts and Implemented-layers rules,
   and the manifest and traceability rows.
3. **Python.** `minion_memory.core.history` against the whole contract, and G3 evidence at the exact
   code.
4. **Runner integration.** Both runners are under NF-026; Rust declares Layer 01.
5. **Rust readiness.** Can Rust Layer 02 be built from the contract and corpus alone?
6. **Records.** Plan, feasibility matrix and state are current. Historical records keep their
   meaning.

Prior closures are not reopened without new evidence.

## Verdict

Record `assurance/reviews/WP-02-final-review-codex.md` on `review/wp02-final` from the docs state
head. Use exactly one of `APPROVED` or `CHANGES_REQUIRED`.

On APPROVED, Claude accepts the pair under G-009, closes NF-016 and NF-026, and moves WP-02 to
RUST_IMPLEMENTATION.
