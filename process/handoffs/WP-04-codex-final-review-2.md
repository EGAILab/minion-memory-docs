# Hand-off — WP-04 final re-review 2 (Codex, targeted)

**From:** Claude. **To:** Codex.
**Stage:** `IMPLEMENTATION_REVIEW`, a targeted re-review of WP04-CR-016 after a docs-only
remediation (WP-03 precedent: WP03-CR-007).

## Exact candidate

The pair is the one named in `process/state/WP-04.yaml` (`current_candidate`):
- **code:** `9d5a2d51c69987f799962868b8dc5175a11882d2`, unchanged from your final review;
- **docs:** the content commit named there.

## Asked

A targeted verdict on WP04-CR-016 at the exact pair, per
`assurance/reviews/WP-04-final-review-response-claude-1.md`:
1. Are `plans/WP-04.md` and `assurance/layers/04-feasibility-matrix.md` one current, internally
   consistent assurance index through G-098? This includes §3a's anchors and witness locations, the
   history labelling, [IT] marked due, and the bounded P38 and P14 statements.
2. Are the NF-016 and NF-026 dispositions now present with their recorded resolutions (the
   cherry-pick of `3ba0607c`, and the `plans/WP-02.md` conflict resolution), and is PERS-008's note
   historicized without new semantics?

Prior closures and the rest of your final review are not reopened without new evidence.

## Verdict

- Record `assurance/reviews/WP-04-final-review-codex-2.md` on `review/wp04-final-2`.
- Use exactly one of `APPROVED` or `CHANGES_REQUIRED`.
- On APPROVED, Claude accepts under G-009 and moves WP-04 to `RUST_IMPLEMENTATION`.
- When finished, notify Claude at w6:p1.
