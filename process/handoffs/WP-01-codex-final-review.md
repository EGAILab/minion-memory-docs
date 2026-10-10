# Hand-off — WP-01 final complete review (Codex)

**From:** Claude (coordinator, Python owner). **To:** Codex (independent reviewer, Rust owner).
**Workflow:** this is the one final complete review before IMPLEMENTATION_REVIEW / FINAL_CONTRACT_REVIEW
-> RUST_IMPLEMENTATION, with acceptance onto main under G-009 as part of that transition.

## Exact candidate

- **docs:** `18bc390c2e8102113b3c152ff21d79fdc3201a15` on `wp01/contract`; the state-only
  descendants follow it.
- **code:** `4fe3ed34c29a6868a3f5050ecee95885b73bead0` on `wp01/contract`.

## History you have already reviewed

Contract reviews `2b388e62`, `1d25e434` and `154b4164` (APPROVED); implementation reviews `716d7218`
and `2f50acc0`; convergence CE-01-01 (characterization `2cf2b21b`, checkpoint `1d99bc2c`, closure
`dc9f9aaa`). The Owner decisions are G-012…G-043.

## Asked: a complete review of WP-01 at the exact pair

1. **Contract.** CORE-001/002/003/011/012, HIST-004, SER-008, SER-009 and their notes, as a whole
   and as one consistent text:
   - every Owner decision is faithfully transcribed;
   - no internal contradiction remains after the many deltas;
   - an independent Rust implementer can work from the text alone.
2. **Canonical corpus.** All ACTIVE Layer 01 scenarios and the manifest/traceability rows.
3. **Python implementation (`minion_memory.core`)** against the whole contract, not only the
   episode surfaces. This covers the runner's thinness and the test suite's discrimination.
4. **Rust readiness.** As Rust owner: does anything block starting the Rust Layer 01 from this
   contract and corpus alone?
5. **Records.** The feasibility matrix and records reflect the final state.

Prior closures are not reopened without new evidence; findings follow
`process/finding-taxonomy.md`.

## Verdict

Record `assurance/reviews/WP-01-final-review-codex.md` on a new branch `review/wp01-final` from
the docs state head. Use exactly one of `APPROVED` or `CHANGES_REQUIRED`. On `APPROVED`, Claude
accepts the pair onto main under G-009 and moves WP-01 to RUST_IMPLEMENTATION. Do not edit the
candidate.
