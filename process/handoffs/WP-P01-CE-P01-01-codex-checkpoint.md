# Hand-off — WP-P01 CE-P01-01 checkpoint review (Codex)

**From:** Claude (coordinator). **To:** Codex (independent reviewer). **Governs:** G-018.

## What to review

The proposed checkpoint for episode CE-P01-01:
`assurance/convergence/CE-P01-01-classification.md` on branch `review/wpP01-ce1-claude` at
commit `de153c0aa0d4311218299fba4b3db832b6ee77e0`. Its parent is your characterization
`281b81a3281ede7dc41a3f2913ae3a4b0b199625`.

It contains:
1. an independent reproduction of 12 of your witnesses;
2. challenge additions CH01–CH05, of which CH01 and CH02 are new executed false passes;
3. a new finding, WPP01-CR-006;
4. decisions D1–D16;
5. a disposition and oracle for each of the 688 rows.

## What is asked

Challenge this proposal. Do not confirm it. Verify the SHAs exist first. For each item, decide
whether it holds against the characterization and against your own execution:

- **Disposition and oracle per row.** Is any FIX, POLICY or LIMIT oracle wrong? Is any KEEP or
  OPAQUE row actually a false pass? Is any DIAG row actually a semantic witness?
- **Decisions D1–D16.** Is each sound, and complete for the rows it claims? Does any decision
  create a new false pass or an unreasonable false refusal? Pay particular attention to these
  choices:
  - D2: the WP-ID pattern equals the file stem;
  - D5: symbolic refs are refused;
  - D7: a hermetic environment, plus refusal of shallow, replace and graft repositories;
  - D12: the declared-family requirement grammar and the finding grammar;
  - D16: one exact-suffix rule for every inventory.
- **CH01–CH05.** Re-execute them yourself, at minimum CH01 and CH02.
- **Classifications.** Check the class of CR-003 and CR-006 (proposed
  SEMANTICS_NEUTRAL_HARDENING), and whether any row needs a finding not listed.

## Verdict format

Record your result as `assurance/reviews/WP-P01-CE-P01-01-checkpoint-codex.md` on a new branch
`review/wpP01-ce1-checkpoint` from `de153c0`. Use exactly one of:

- `APPROVED`: the checkpoint becomes AGREED FOR IMPLEMENTATION exactly as written.
- `CHANGES_REQUIRED`: list each required change, with the row IDs and executed evidence.

Approval is about this exact artifact only. It does not authorize implementation edits by you,
and it is not acceptance. Production modules stay frozen until the checkpoint is AGREED.

Do not modify the WP-01 worktrees (G-019).
