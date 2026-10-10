# Hand-off — WP-01 Python Layer 01 targeted closure, with contract delta (Codex)

**From:** Claude. **To:** Codex.
- **Prior review:** `assurance/reviews/WP-01-python-implementation-review-codex.md` (`716d7218`,
  CHANGES_REQUIRED).
- **Response:** `assurance/reviews/WP-01-python-remediation-claude-1.md`.
- **Owner decisions for its path-C items:** G-035 and G-036, recorded verbatim in
  `reference/governance/2026-10-10-owner-layer01-decisions.md`.

## Exact candidate

- **docs:** `81192e3adf29ef474ce1ecdd0096bb306543a5ae` on `wp01/contract`; the state-only
  descendants follow it.
- **code:** `eb47635c6ea997f030d04b8099366044a2f702aa` on `wp01/contract`.

Please review separate checkouts.

## Scope

1. **Contract delta, review as contract.** Does it transcribe G-035 and G-036 exactly?
   - CORE-003 revision record;
   - the SER-008 stage-3 row with `artifact.revision_invalid`;
   - SER-008 "Native array binding";
   - SER-008 "Stages across arguments": my explicit statement of the G-031 reading you applied in
     PY-001 (path A in your review).
2. **Findings.** Is each of WP01-PY-001…004 and PY-007 resolved? Verify with your own
   counterexamples, including neighbourhoods of the witnesses you used.
3. **New corpus content.**
   - the G-035 shape cases;
   - the cross-argument precedence case;
   - the unpaired-escape case;
   - the new `core.serialization.raw-content-hash` scenario.
   Re-derive their expectations independently.
4. **Regressions.** Check direct regressions of the fix pass, including the generator's YAML
   quoting change (the corpus diff should be insertions only), and run the suite on POSIX.

Already-closed rows and unrelated semantics are not reopened.

## Verdict

Record `assurance/reviews/WP-01-python-implementation-review-codex-2.md` on a new branch
`review/wp01-python-2` from the docs state head. Use exactly one of `APPROVED` or
`CHANGES_REQUIRED`.

On `APPROVED`, IMPLEMENTATION_REVIEW → RUST_IMPLEMENTATION, with acceptance onto main (G-009).
Do not edit the candidate.
