# Hand-off — WP-02 CONTRACT_REVIEW round 2 (Codex)

**From:** Claude. **To:** Codex.

## Exact candidate

- **docs:** `6f761081dcabc3975e526b262b8d0c5e493ab9a5` on `wp02/contract`, followed by state-only descendants.
- **code:** `15b71ca392384b447f4b2c0ca023a69538f977d8` on `wp02/contract`.

**Responds to:** your review `42d3d03e`. **Response:**
`assurance/reviews/WP-02-contract-review-response-claude-1.md`.

## What changed

- **Owner decisions.** The Owner decided CR-001, -002, -003 and -005 as G-052 to G-055, recorded
  verbatim in `reference/governance/2026-10-11-owner-layer02-start.md`.
- **CR-004.** Repaired by an author reading of G-050, G-052 and G-055, recorded in the same file:
  gate 1 validates only the routing triple, and `compatibility` is validated only after profile
  admission.
- **Spec.** HIST-002 (schema identity, gates), HIST-005 (G-054) and SER-005 (G-053 reader, order) are
  rewritten. SER-008 records the gated stage-3 rule next to G-035.
- **Corpus.** 70 DRAFT steps; the 11 new controls are listed in the response.

## Asked

1. **Findings.** Close or keep each of CR-001…005 against the exact text and Owner decisions. Is
   the CR-004 reading sound under G-050?
2. **Corpus.** Re-derive the new controls. Confirm that no earlier expectation changed.
3. **NF-026.** Report its status; the Rust runner alignment is yours.

## Verdict

Record `assurance/reviews/WP-02-contract-review-codex-2.md` on a new branch `review/wp02-contract-2`
from the docs state head. Use exactly one of `APPROVED` or `CHANGES_REQUIRED`. Do not edit the
candidate.
