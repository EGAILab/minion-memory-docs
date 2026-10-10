# NF-026 — review of the Rust runner fix (Claude)

**Verdict: APPROVED** for code `b9f42d4227093cb3b9144e2d8ca2b068c8cb5876` (`wp02/rust-runner`,
on top of `wp02/contract` `1d7167c8`). The companion record is docs `940e102d`.

**Author:** Codex, Rust owner. **Reviewer:** Claude, who did not author this change.
**Authority:** `conformance/README.md` at `1d7167c8`: the Drafts rule and the Implemented-layers
rule.

## Delta

Only `minion-memory-rust/tests/conformance.rs` and `minion-memory-rust/README.md` change. No library
code, corpus or Python is touched.

## Reading against the corpus rules

- **DRAFT.** Every DRAFT scenario is an `xfail` whose reason names the layer and the Drafts rule. It
  is never executed as evidence and never fails the suite. The status is checked before any
  operation dispatch, so a DRAFT with unsupported operations stays an `xfail`.
- **Implemented layers.** `IMPLEMENTED_LAYER = 1`. An ACTIVE scenario above it is an `xfail` naming
  its layer, Rust and the rule. At or below it, every step runs against the real library, and
  unknown operations and wrong results fail.
- **Placeholders and validity.** An ACTIVE scenario carrying a `TO_BE_` value is an error, and
  unknown statuses are errors.
- **Counts.** The pinned `(8, 146, 5)` inventory is replaced by derived counts with
  `active > 0`. That matches the Python runner, which pins no inventory either, and is required for
  ACTIVE promotion to be visible. Silent scenario loss is still guarded by schema validation of
  every discovered file and by `mneme-process check conformance`, which links scenarios to manifest
  rows.

## Executions (Windows, rustc 1.97.1, a detached checkout of `b9f42d42`)

| Check | Result |
|---|---|
| `cargo fmt --check`; `clippy --all-targets -D warnings` | clean |
| `cargo test --locked --offline` | all pass, including the new controls `draft_rule_and_active_promotion` and `implemented_layer_and_promotion` |
| Corpus | 8 ACTIVE / 146 steps executed. The 4 Layer 02 ACTIVE scenarios and the 5 placeholders are reported `xfail` with their reasons; 9 `xfail`s in total. |
| Planted: `IMPLEMENTED_LAYER = 2` | `canonical_corpus` **fails** on `unsupported ACTIVE operation compare_history_boundaries`, so the declaration gates real execution |
| Planted: the three WP-02S DRAFT `scope-*` scenarios added to the corpus | each is reported `xfail` under the Drafts rule; the suite passes (12 `xfail`s) |

The scratch corpus change was reverted, leaving the checkout clean.

## Disposition

NF-026's runner side is resolved by this candidate, together with the README rules at `1d7167c8`.
The finding closes when WP-02's code containing both reaches `main`. This approval is not
acceptance.
