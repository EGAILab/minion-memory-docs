# Hand-off — WP-01 Layer 01 CONTRACT_REVIEW, round 2 (Codex)

**From:** Claude. **To:** Codex. **Prior review:** `assurance/reviews/WP-01-contract-review-codex.md`
(`2b388e62`, CHANGES_REQUIRED). **Response:**
`assurance/reviews/WP-01-contract-review-response-claude-1.md`. **Owner decisions for its path-C
items:** G-028…G-033, recorded verbatim in
`reference/governance/2026-10-10-owner-layer01-decisions.md`.

## Exact candidate

- **docs:** `7d51960ba1343ec7f7dadb7f7ec954610573e5bb` on `wp01/contract`; the state-only
  descendants follow it.
- **code:** `4224a45e4606a55d0bfaa08097956a4952ddd512` on `wp01/contract`.

Please review separate checkouts of the exact SHAs.

## Scope

1. **Findings.** Is each of WP01-CR-001…004 resolved, and is Q1 answered? The response maps each
   item to its resolution.
2. **Fidelity.** Do the repairs state exactly what G-028…G-033 decide, with no added choice?
   **Flagged for you:** the SER-008 stage-2/3 traversal order, which is my concrete reading of
   G-031's "shared deterministic document traversal order". If you judge that reading to be an
   observable choice the Owner has not made, classify it as path C.
3. **Oracles.** Re-derive the new oracles independently:
   - the precedence cases;
   - the rounding, underflow and subnormal canonical bytes;
   - the 36 timestamp cases;
   - the operation-identity byte bounds;
   - the CORE-003 identical/conflict outcomes.
4. **Rust feasibility of the repaired text.** The new timestamp-domain probe is in
   `assurance/layers/01-probes/timestamp-domain.md`.
5. **Regressions.** Check for any regression in the previously verified items. Unrelated,
   already-verified fidelity rows need not be re-argued.

## Verdict

Record `assurance/reviews/WP-01-contract-review-codex-2.md` on a new branch
`review/wp01-contract-2` from the docs state head. Use exactly one of `APPROVED` (the contract
checkpoint) or `CHANGES_REQUIRED`, with findings classified and path C marked
`owner_decision_required`. Approval is not acceptance. Do not edit the candidate.
