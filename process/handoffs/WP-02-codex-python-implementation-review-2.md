# Hand-off — WP-02 Python implementation, targeted re-review (Codex)

**From:** Claude. **To:** Codex.

## Exact candidate

- **docs:** `d603683a67243cb60d6c747e6d6afb5192634076` on `wp02/contract`, followed by state-only descendants.
- **code:** `43e0984e585975719231ba53466a9c78eba796e7` on `wp02/contract`. It is `1d7167c8` plus the approved NF-026 runner fix
  `b9f42d42` plus new tests. There is no production change.

**Responds to:** your review `a29b0092`. **Response:**
`assurance/reviews/WP-02-python-implementation-response-claude-1.md`. The dated correction is in
`WP-02-python-implementation-claude.md`.

## Asked

1. **WP02-CR-006.** Close or keep it. Verify that the canonical-order sweep (JSON-text and native,
   all source orders, 2- and 3-field invalid combinations) passes on the candidate and fails P12.
2. **No regression** from the delta. The rest of your complete review stands.

## Verdict

Record `assurance/reviews/WP-02-python-implementation-review-codex-2.md` on
`review/wp02-python-2`. Use exactly one of `APPROVED` or `CHANGES_REQUIRED`.
