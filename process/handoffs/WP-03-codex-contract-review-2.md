# Hand-off — WP-03 CONTRACT_REVIEW round 2 (Codex)

**From:** Claude. **To:** Codex.

## Exact candidate

- **docs:** `e25190267ce242c558309af462d86071421b7d2e` on `wp03/contract`, followed by state-only descendants.
- **code:** `2bc2ee126a4c4086d848c099698522bfad5ce09e` on `wp03/contract`.

**Responds to:** your review `c3775768`. **Response:**
`assurance/reviews/WP-03-contract-review-response-claude-1.md`.

## What changed

- **Owner decisions.** CR-001 (G-071, G-072), CR-002 (G-073) and CR-004 (G-074), recorded verbatim
  in `reference/governance/2026-10-11-owner-layer03-start.md`.
- **CR-003.** HIST-007 now lists every early shape check and late graph check.
- **Spec.** The HIST-007 lineage block and the PROJ-001 projector block are rewritten, including
  typed targets and the `duplicates` and `unresolved_derivations` result fields.
- **Corpus.** 49 DRAFT steps; two expectations change under the Owner's decisions, and the new
  controls are listed in the response.

## Asked

1. **Findings.** Close or keep CR-001…004 against the exact text.
2. **Corpus.** Re-derive the new and changed expectations.
3. **Unrecorded choices.** Flag any remaining path C, for example the typed-target shape
   `to_artifact {stable_id, artifact_version}`, or the presentation order of
   `unresolved_derivations`.

Record APPROVED or CHANGES_REQUIRED on `review/wp03-contract-2`. Do not edit the candidate.
