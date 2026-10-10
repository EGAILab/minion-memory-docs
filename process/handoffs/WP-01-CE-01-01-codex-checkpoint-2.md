# Hand-off — WP-01 CE-01-01 checkpoint revision 2 (Codex targeted re-review)

**From:** Claude. **To:** Codex.

**Under review:** `assurance/convergence/CE-01-01-classification.md` at docs
`3d4e83398a4cd0cc3f96b61d0967b9b1cdf63853` (`wp01/contract`). Revision 1 was `d46dfa1c`; your
review is `65775db3`.

## Scope

1. **Each finding.** Is each of CE01-CP-001…003 resolved? §0 maps them.
2. **Re-executed rows.** The 537 newly FIX rows come from re-executing your embedded driver with
   only an added G-042 exact-return observer (`.tmp/work/claude/ce0101_driver.py`; the patch is in
   `ce0101_patch_driver.py`). It reproduces your 21,925/3,545 statuses and IDs exactly. Please
   re-derive them.
3. **Boundary rows.** Check the 75 literal boundary oracles and dispositions (25 FIX / 50 KEEP), and
   the four controls M01, M02, D01 and D02.
4. **Two G-041 readings flagged for your judgement:**
   - `decode_json` reads bytearray (and its subclasses) as bytes;
   - a non-`dict` argument mapping is a caller `TypeError`.

   Classify either as path C if it is an observable choice the Owner has not made.
5. **SER-008.** The stage-1 ordering correction.
6. **Regressions.** Check for regressions in anything else revision 2 changed.

## Verdict

Record `assurance/reviews/WP-01-CE-01-01-checkpoint-codex-2.md` on a new branch
`review/wp01-ce1-checkpoint-2` from the docs state head. Use exactly one of:
- `APPROVED`: AGREED FOR IMPLEMENTATION exactly as written;
- `CHANGES_REQUIRED`.

Production stays frozen; approval is not acceptance.
