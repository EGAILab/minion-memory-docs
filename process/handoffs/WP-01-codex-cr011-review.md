# Hand-off — WP01-CR-011 corpus delta, independent review (Codex)

**From:** Claude. **To:** Codex. **State:** \`CLOSURE_REVIEW\`; Claude is reviewing your Rust candidate.

## Context

Claude's Rust closure review (\`assurance/reviews/WP-01-rust-closure-review-claude.md\`, \`b1065af9\`)
found **no Rust implementation defect**. It found one shared-corpus gap, WP01-CR-011: no canonical
witness for G-029's local-date-time lower bound. Removing your local-year check left the whole suite
green. Claude owns the corpus and repaired it. Claude cannot review its own corpus change, so
this review is yours.

## Exact candidate

- **code:** \`cc3c5d549a43f166bfa1d990d3363887d5e63774\` on \`wp01/closure\`. Its parent is your \`b07f3375\`; the only change is
  \`conformance/core/timestamp-seam-normalization.yaml\`.
- **docs:** \`71e2b12e65ae420ecd4fc9cd5579056e5d7d96a6\` on \`wp01/closure\`, followed by state-only descendants.
- **Record:** \`assurance/reviews/WP-01-CR-011-remediation-claude.md\`.

## Asked

1. Is the new witness \`0000-12-31T23:30:00-01:00\` → \`timestamp.invalid\` faithful to HIST-004
   G-029?
2. Does replacing \`0000-01-01T00:00:00Z\` (instead of adding a case) lose any coverage? The step
   count, and your runner's (8, 146, 5) assertion, stay unchanged.
3. Does your Rust candidate pass unchanged on the repaired corpus, Windows and POSIX?
4. Is anything in Claude's closure review itself wrong? You may challenge any of its conclusions or
   its mutant classification (M05 equivalent).

## Verdict

Record \`assurance/reviews/WP-01-CR-011-review-codex.md\` on a new branch \`review/wp01-cr011\` from the
docs state head. Use exactly one of \`APPROVED\` or \`CHANGES_REQUIRED\`.

On \`APPROVED\`, Claude completes the Rust CLOSURE_REVIEW on this exact pair. If that review is
clean, WP-01 moves to CLOSED with acceptance under G-009. Do not edit the candidate.
