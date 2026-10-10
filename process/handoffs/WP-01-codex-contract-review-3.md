# Hand-off — WP-01 Layer 01 CONTRACT_REVIEW, round 3 (Codex)

**From:** Claude. **To:** Codex.
- **Prior review:** `assurance/reviews/WP-01-contract-review-codex-2.md` (`1d25e434`,
  CHANGES_REQUIRED).
- **Response:** `assurance/reviews/WP-01-contract-review-response-claude-2.md`.
- **Owner decision:** **G-034** (within-stage order), recorded verbatim in
  `reference/governance/2026-10-10-owner-layer01-decisions.md`.

**Exact candidate:**
- docs: `62adec5fde8575818aa19f3c4025acc78a7240a5`;
- code: `860e91c1bfb08e834c1a62b0f1fc32dd4bfd7efd`;
- both on `wp01/contract`. Please review separate checkouts.

## Scope

- WP01-CR-005: does SER-008 transcribe G-034 exactly?
- WP01-CR-006: does HIST-004's typed-error wording now match G-031 and SER-008?
- The new controls:
  - two G-034 order cases in `portable-value-domain-rejections`;
  - six non-string or earlier-stage timestamp cases and one JSON-text string case in
    `timestamp-seam-normalization`.
- Direct regressions of these edits.

Items you provisionally closed in review 2 are not reopened unless these edits affect them.

## Verdict

Record `assurance/reviews/WP-01-contract-review-codex-3.md` on a new branch
`review/wp01-contract-3` from the docs state head. Use exactly one of:
- `APPROVED`: the contract checkpoint; Python may then implement Layer 01;
- `CHANGES_REQUIRED`.

Approval is not acceptance. Do not edit the candidate.
