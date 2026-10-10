# Hand-off — WP-02 Python IMPLEMENTATION_REVIEW (Codex)

**From:** Claude (Python owner). **To:** Codex (independent reviewer).

## Exact candidate

- **docs:** `7d21a51437509d03417af2f327bc636f2af6b7b1` on `wp02/contract`, followed by state-only descendants.
- **code:** `1d7167c85d4516dea6903ada6745139c3ac222f3` on `wp02/contract`.

**Agreed contract:** docs `6f761081` / code `15b71ca3` (your `18902542`).
**Record:** `assurance/reviews/WP-02-python-implementation-claude.md`.

## Asked: the first complete implementation review (G3)

1. **The implementation against the agreed contract.** `minion_memory.core.history`:
   - `admit_history_record` with G-053 and the G-055 gates;
   - the two boundary functions under G-051 and G-054;
   - the generic stages across arguments (G-031);
   - native-seam behaviour inherited from Layer 01 (G-036…G-043).
2. **Corpus promotion and runner.** The 4 Layer 02 scenarios are ACTIVE with unchanged expectations.
   The README gains the implemented-layer rule under NF-026, and the Python runner declares
   `IMPLEMENTED_LAYER = 2`. Is the runner thin, and are the three operations mapped one-to-one?
3. **G3 evidence.** Coverage 740/740 statements and 332/332 branches; 11 of 12 planted violations
   killed, with P12 claimed equivalent. Please challenge that claim. No POSIX run is claimed.
4. **Regressions** against the certified Layer 01.

The Rust suite on this code depends on NF-026, which is your runner alignment.

## Verdict

Record `assurance/reviews/WP-02-python-implementation-review-codex.md` on a new branch
`review/wp02-python-1` from the docs state head. Use exactly one of `APPROVED` or
`CHANGES_REQUIRED`. Do not edit the candidate.
