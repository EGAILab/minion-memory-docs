# Hand-off — WP-01 CE-01-01 checkpoint review (Codex)

**From:** Claude. **To:** Codex. **Governs:** G-037, G-038, G-039…G-042 (recorded verbatim in
`reference/governance/2026-10-10-owner-layer01-decisions.md`).

## What to review

`assurance/convergence/CE-01-01-classification.md` at docs `d46dfa1ca378d1e2c97ea0137053f8b86f5afc9b`
on `wp01/contract`. It carries your characterization `2cf2b21b` unchanged, and contains:
1. an independent reproduction of seven witnesses;
2. the completeness challenge CH01–CH05 (`__class__` spoofing objects are admitted or leak host
   errors on the frozen code);
3. the Owner decisions for C01–C05 and their SER-008 transcription ("Native binding completion" and
   the stage table);
4. implementation constraints;
5. control accounting;
6. a disposition and oracle for all 25,554 rows.

## Asked

Challenge, do not confirm:
- **Decision transcription.** Do the decision transcriptions state exactly what G-039…G-042 say?
- **Challenge rows.** Is the CH oracle a sound authority reading of G-037 (subclasses only)?
  Re-execute CH01–CH05.
- **Rows.** Is any row's disposition or oracle wrong, or did a decision change a boundary oracle
  in a way the decision does not support?
- **Constraints.** Are the implementation constraints sufficient to kill every FIX row without a
  rejection-only shortcut?

## Verdict

Record `assurance/reviews/WP-01-CE-01-01-checkpoint-codex.md` on a new branch
`review/wp01-ce1-checkpoint` from the docs state head. Use exactly one of:
- `APPROVED`: AGREED FOR IMPLEMENTATION exactly as written;
- `CHANGES_REQUIRED`.

Production stays frozen for you; approval is not acceptance.
