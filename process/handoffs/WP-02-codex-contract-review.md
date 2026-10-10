# Hand-off — WP-02 CONTRACT_REVIEW (Codex)

**From:** Claude (contract author). **To:** Codex (independent reviewer, Rust owner).
**Governance:** G-046 start, G-047 split, G-048…G-051 envelope/timestamps/exclusion/boundary
(`reference/governance/2026-10-11-owner-layer02-start.md`, recorded verbatim).

## Exact candidate

- **docs:** `2c8647fd9ad4b0553552bce05ea629c32803f1da` on `wp02/contract`, followed by state-only descendants.
- **code:** `a2178c955ffff1bd3bd604a628648463774f1b0e` on `wp02/contract`. Its parent is code `main` `cc3c5d54`; the delta is corpus and
  manifest only.

## Scope

WP-02 is the Layer 02 history and compatibility envelope: HIST-001, HIST-002, HIST-005, HIST-010,
SER-005 and SER-006. MemoryScope is WP-02S, which is separate and does not block WP-02.

The candidate contains:
- **Spec.** Layer 02 blocks in `spec/core.md` (HIST-001, HIST-002, HIST-005, HIST-010) and
  `spec/serialization.md` (SER-005, SER-006), and new SER-008 stage-table rows.
- **Corpus.** Four DRAFT scenarios in code `conformance/core/history-*.yaml`, 59 steps with
  expectations written from the text, and their manifest links.
- **Feasibility.** `assurance/layers/02-feasibility-matrix.md`.
- **NF-016** is resolved under G-047 and G-051 as a store-local cursor.
- **NF-026** is new. The corpus README now says DRAFT is an expected failure in both runners. Your
  Rust runner currently fails the suite on DRAFT scenarios and pins (8, 146, 5); Python reports
  them as xfail. Aligning the Rust runner is yours as Rust owner. The Rust suite fails on this code
  candidate until then.

## Asked

1. **Fidelity.** Is every Owner decision (G-047…G-051) faithfully transcribed? Are the authority
   readings (path A) sound, and is anything an unrecorded observable choice (path C)? Check
   especially:
   - the identity members validated for every version;
   - typed-field order;
   - reader shape and duplicate rule;
   - which errors name arguments;
   - `position` 0;
   - generic stages applying before exclusion.
2. **Corpus.** Re-derive the 59 expectations independently from the text.
3. **Rust readiness.** Is the text implementable from the contract alone?
4. **HIST-001 and HIST-010.** Are these sound as Layer 02 vocabulary and constraint only, with
   conformance in the later layers listed?

## Verdict

Record `assurance/reviews/WP-02-contract-review-codex.md` on a new branch `review/wp02-contract-1`
from the docs state head. Use exactly one of `APPROVED` or `CHANGES_REQUIRED`, with findings per
`process/finding-taxonomy.md`. Do not edit the candidate.
