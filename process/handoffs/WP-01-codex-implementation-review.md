# Hand-off — WP-01 Python Layer 01 IMPLEMENTATION_REVIEW (Codex)

**From:** Claude (Python owner). **To:** Codex (independent reviewer; Rust owner).

## Exact candidate

- **docs:** `4c27bd5c5183658f589e0d856adc9b5c641dd1ad` on `wp01/contract`; the state-only
  descendants follow it.
- **code:** `f10c7b4f1c22b4daed4b6bc2f05028b5467a6ce9` on `wp01/contract`.

**Contract:** the agreed checkpoint at docs `62adec5f` / code `860e91c1`; the only contract-corpus
change since is the scenario status, DRAFT to ACTIVE. **Record:**
`assurance/reviews/WP-01-python-implementation-claude.md`.

## Asked

Review the Python implementation against the **contract**, not against the scenarios alone.
1. **Does every contract rule hold, including those no scenario pins?**
   - SER-008 stages, codes and canonical traversal, at both the native and JSON-text seams;
   - SER-009 bytes;
   - CORE-001/002/003/012;
   - the HIST-004 grammar and range.
2. **Find inputs where it is wrong.** Re-derive results independently, e.g. your own decoder, the
   reference library or the RFCs.
3. **Readings.** Judge the three implementation-level readings listed in the record; classify any
   observable one as path C (Owner).
4. **Runner.** Is the conformance runner thin (no semantics), and do the tests discriminate the
   named wrong implementations?
5. **POSIX.** Run the Python package suite on a case-sensitive POSIX host.

## Verdict

Record `assurance/reviews/WP-01-python-implementation-review-codex.md` on a new branch
`review/wp01-python-1` from the docs state head. Use exactly one of `APPROVED` or
`CHANGES_REQUIRED`, with findings classified per `process/finding-taxonomy.md`.

A clean first review allows IMPLEMENTATION_REVIEW to RUST_IMPLEMENTATION; acceptance onto main is part
of that transition, under G-009. Do not edit the candidate.
