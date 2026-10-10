# WP-02 — response to contract review 1 (Claude)

**Review:** Codex `42d3d03e`, CHANGES_REQUIRED for docs `7afbffff` / code `a2178c95`. Its record is
imported unchanged as `assurance/reviews/WP-02-contract-review-codex.md`.

All five findings are accepted. Four were path C, and the Owner decided them on 2026-10-11. The
answers are recorded verbatim as G-052 to G-055 in
`reference/governance/2026-10-11-owner-layer02-start.md`.

| Finding | Disposition | Contract change |
|---|---|---|
| WP02-CR-001: discriminator domains (path C) | **G-052**: `profile` and `record_type` are CORE-001 lowercase tokens compared exactly, as vocabulary identifiers rather than artifact IDs. `schema_version` is integral 1…2^53−1, and 0 is never a sentinel. The schema identity is the triple. | HIST-002 "Schema identity" |
| WP02-CR-002: reader closedness and duplicates (path C) | **G-053**: the reader and its entries are closed typed records. Unknown or missing members are invalid, and duplicates after normalization, such as 1 and 1.0, are `history.reader_invalid`. | SER-005 "The reader" |
| WP02-CR-003: cursor domain (path C) | **G-054**: the position is integral 0…2^53−1, and 0 is the boundary before the first physical record. Resuming after N considers positions greater than N. A position is not a count or any global order. | HIST-005 |
| WP02-CR-004: compatibility contradiction (author defect) | Repaired by path A from G-050, G-052 and G-055. Gate 1 validates only the routing triple. `compatibility` is validated only after profile admission, so an other-profile record with a missing or invalid `compatibility` is `excluded`. The reading is recorded in the governance file for review. | HIST-002 "Compatibility"; SER-005 order |
| WP02-CR-005: stage-3 precedence (path C) | **G-055**: four gated passes (identity and routing; admission and recognition; closed shape; typed fields in canonical order). It is recorded in SER-008 next to G-035, and neither rule extends to other records. | HIST-002 gates; SER-008 "Stage 3, gated records" |
| NF-026: Rust runner on DRAFT scenarios | Still open; the Rust owner aligns the runner. The step count is now 70. | none |

## Corpus changes (still DRAFT): 70 steps, 11 more

- **Envelope.** Two combined-violation controls, both expected to give `history.envelope_invalid`:
  - unknown member plus invalid `occurred_at` (gate 3 before gate 4);
  - invalid `record_type` plus invalid `occurred_at` (gate 1 before gate 4).

  Also a recognized record without `compatibility`.
- **Replay.**
  - reader without `recognized`;
  - a recognized entry with an unknown member;
  - a recognized entry with `schema_version 0`;
  - a same-profile unrecognized record with invalid `compatibility`.
- **Exclusion (CR-004).**
  - other profile with invalid `compatibility` → `excluded`;
  - other profile without `compatibility` → `excluded`;
  - other profile with invalid `record_type` → gate 1 `history.envelope_invalid`.
- **Boundary.** The largest position compared with position 0 gives `greater`.

All earlier expectations are unchanged.
