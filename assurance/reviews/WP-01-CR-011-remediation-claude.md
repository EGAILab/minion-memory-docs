# WP01-CR-011 — remediation record (Claude)

**Finding:** WP01-CR-011, raised in Claude's Rust CLOSURE_REVIEW (`b1065af9`). It is a shared-corpus
gap, and its owner is Claude. **Repaired code:** `cc3c5d549a43f166bfa1d990d3363887d5e63774` on `wp01/closure`, whose parent is the
Rust candidate `b07f3375`. The delta is one corpus file, and the Rust and Python code are unchanged.

## Change

`conformance/core/timestamp-seam-normalization.yaml`: the case "year zero (G-029)",
`0000-01-01T00:00:00Z`, is replaced by "local year 0000 whose UTC instant is in year 0001
(G-029)", `0000-12-31T23:30:00-01:00`. Both expect `timestamp.invalid`.

- **Why the old case was not enough.** It is also rejected by the UTC bound, so it did not
  discriminate the local-range rule.
- **Why the new case works.** Its UTC instant, `0001-01-01T00:30:00Z`, is inside the range, so
  only HIST-004's local-date-time bound (G-029) rejects it.
- **What else covers year 0000 with Z.** The UTC bound keeps its own witnesses in
  "UTC result before year 0001", and the Rust unit tests still contain `0000-01-01T00:00:00Z`.
- **Counts.** The step count is unchanged: 8 ACTIVE, 146 steps, 5 xfails.

## Evidence (Windows, project-local)

- Rust `b07f3375` code, unchanged, on the repaired corpus: 16 integration tests and 1 doctest pass.
- The planted mutant M07 (local-year check removed from `time.rs`) is now **killed** by
  `canonical_corpus`. M05 remains an equivalent mutant: chrono rejects second 60.
- Python: 354 passed, 5 xfailed. Python's `datetime` cannot represent year 0, so its local bound
  cannot be bypassed in this way.
- The scratch generator `gen_l01_scenarios.py` was updated to match.

This is author evidence for Codex's independent review of the corpus delta. It is not a closure claim.
