# WP-01 — Rust Layer 01 CLOSURE_REVIEW, completion (Claude)

**Verdict: APPROVED** for the exact final pair:
- code `cc3c5d549a43f166bfa1d990d3363887d5e63774` (`wp01/closure`);
- docs `71e2b12e65ae420ecd4fc9cd5579056e5d7d96a6` (`wp01/closure`).

**Completes:** Claude's closure review `b1065af9` of Codex's Rust candidate `b07f3375`, which was
CHANGES_REQUIRED with one shared-corpus finding, WP01-CR-011, and no Rust defect.
**Corpus delta independently approved by:** Codex, `c73593d6` (`review/wp01-cr011`).

## What changed since `b1065af9`

- `git diff b07f3375 cc3c5d54` touches exactly `conformance/core/timestamp-seam-normalization.yaml`.
  The Rust crate, its tests and lockfile, and the manifest are byte-identical to the reviewed
  `b07f3375`.
- `git diff bac6594e cc3c5d54 -- minion-memory-python` is empty, so the Python code is the
  Codex-approved, accepted Python.

Every execution and reading in `b1065af9` therefore applies unchanged to the Rust code of this
pair.

## Re-executed on the exact code `cc3c5d54` (Windows, project-local)

- **Rust:** `cargo test --locked --offline`: 16 integration tests and 1 doctest pass; the
  canonical corpus is 8 ACTIVE / 146 steps / 5 explicit xfails.
- **Planted bugs:** the local-year mutant M07, which survived on `b07f3375`, is now killed by
  `canonical_corpus`. Codex reproduced this independently on Windows and Linux. M05 is confirmed
  equivalent by both reviewers.
- **Python owner run (G2):** 354 passed, 5 xfailed.
- **`mneme-process check`:** 8/8 at code `cc3c5d54` with the docs state.

## Findings

- WP01-CR-011 is **closed** by Codex's approval `c73593d6` of the corpus delta.
- No other findings. No open finding remains on the WP-01 surface from this review.

## Scope

This approves the Rust Layer 01 implementation, together with the repaired corpus, against the
accepted contract. Acceptance onto `main` follows under the recorded G-009 delegation. This
record makes no certification claim.
