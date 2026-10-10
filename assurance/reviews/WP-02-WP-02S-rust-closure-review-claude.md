# Layer 02 (WP-02 and WP-02S) — Rust CLOSURE_REVIEW (Claude)

**Verdict: APPROVED.** There are no findings.

**Exact pair:**
- code `a5506d0ddd98af33be4d9ec87305b10000febf4d` (`wp02/rust`, from code `main` `609dad7b`);
- docs `620c512c5d19cb3e3ff73037d6016b50a1a605cc`, with state on `wp02/rust-state` at `6346d995`.

**Author:** Codex. **Reviewer:** Claude, who did not author any Rust code.

**Authority:** the accepted WP-02 and WP-02S contracts, meaning HIST-001/002/005/010, SER-005/006,
the SER-008 stage table, `spec/scope.md` and Owner decisions G-047…G-064, together with the seven
ACTIVE Layer 02 scenarios.

Python was not an oracle. Below, the accepted Python only generated disagreements to adjudicate
against the text, and none arose. Codex's record was treated as claims to reproduce.

## Reading against the contract

- **The four gates (G-055), in `history.rs`.**
  1. The routing triple is checked for every record (G-052).
  2. Profile admission comes before any reading of `compatibility` (G-050), then recognition.
  3. The closed shape is checked before typed fields (G-048, G-049).
  4. Typed fields follow canonical member order. This is sound because Rust's normalization sorts
     object members for both native and JSON-text input; that is the WP02-CR-006 seam, and it was
     confirmed by the targeted run below.
- **Reader (G-053).** Closed, with closed entries, `schema_version ≥ 1` in the `Integer` domain, and
  duplicates rejected after normalization.
- **Arguments in errors.** Argument errors name `reader`/`record` or `a`/`b`.
  `history.unknown_required` and `history.boundary_incomparable` name none.
- **Boundaries (G-051, G-054).** Closed `{store_id, position}` with position ≥ 0, upper bound
  enforced at stage 2. Cross-store ordering is an error; equality is structural.
- **Scope, in `scope.rs`.** The G-064 two-segment name grammar has no device rule for names, and
  values use CORE-001 (G-056). The two closed states never alias: global is `Some(&[])` and
  unresolved is `None`. A query is validated before an unresolved record returns `false`. Matching
  is fail-closed applicability, and unknown or learning facets are rejected in queries and hidden in
  records (G-058, G-061, G-062).
- **Layer 01 changes.** Only refactors: `id_rule` becomes crate-visible, and `timestamp_rule` is
  extracted from `normalize_timestamp`. Layer 01 behaviour is unchanged, and its 8 scenarios still
  pass.

## Executions (project-local; current env script; rustc 1.97.1)

| Check | Result |
|---|---|
| Windows: fmt, clippy `-D warnings`, rustdoc `-D warnings` | clean |
| Windows: `cargo test --locked --offline` | all pass; the runner reports **15 ACTIVE, 289 steps**, 5 placeholder `xfail`s |
| Linux (WSL), same checkout | fmt and clippy clean; the same 15 ACTIVE / 289 steps; all pass |
| Python at the candidate (G2, shared manifest changed) | no Python or corpus delta; 468 passed, 5 xfailed |
| `mneme-process check --deep-sources` | 8/8 |
| Differential, 5 seeds × 40,000 cases | **0** disagreements |
| Targeted admission pass: 40,000 near-valid envelopes in shuffled JSON source order | **0** disagreements |
| Planted violations: Claude's own 14, independent of Codex's 22 | **13 killed**; S04 equivalent (below) |

The differential covers readers, envelopes, boundaries, scope values, scope equality and visibility,
all at the JSON-bytes seam. The targeted pass produced 10,805 `decode`, 3,434 `timestamp.invalid`,
1,473 `id.invalid`, 4,432 `unknown_required`, 2,622 `excluded` and 195 `skip` outcomes.

The 13 killed planted violations:
- gate 4 in reverse order;
- `compatibility` read before admission;
- `unknown_required` naming the record;
- position 0 rejected;
- cross-store equality ignoring the store;
- reader duplicates merged;
- no closed shape;
- query omission widening visibility;
- unresolved records visible;
- an unresolved record checked before the query;
- device names excluded from facet names;
- `validate_scope` naming an argument;
- unknown query facets accepted.

**S04 (`rsplit_once` instead of `split_once`) is equivalent.** Each segment's grammar excludes `.`,
so a name with one dot splits identically either way, and a name with two or more dots fails under
both.

The scripts are in `.tmp/work/claude/`: `rust-probe-l02/`, `l02_closure_diff.py`,
`l02_closure_targeted.py`, `l02_rust_mutants.py` and `l02-closure-linux.sh`; outputs are in
`l02-closure/`.

## Disposition

Rust Layer 02 is approved for both WPs. Acceptance onto `main` follows under G-009.
Certification needs the Owner's decision, as for G-044.
