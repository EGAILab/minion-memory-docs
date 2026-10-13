# WP-04 (Layer 04) — Rust targeted CLOSURE_REVIEW 2 (Claude)

**Verdict: APPROVED.**
- WP04-CR-017 and WP04-CR-018 are closed.
- No finding remains.
- Everything in closure review 1 (`review/l04-rust-closure` `70f2a3e3`) other than these two findings
  stands: the contract reading, the gate results, and the 12 killed controls.

**Exact pair:**
- code `220c6f285744fd52736cbd20f22105e9f33a5dce` (`wp04/rust`), which is `6ef220e5` plus one
  test-only commit;
- docs `b45018d67f2e5e861ec6aa458b3d94efd968e7e2` (`wp04/rust`, descending from `276fcf56`), with
  state on `wp04/rust-state` at `0882d041`.

**Author:** Codex. **Reviewer:** Claude.

## The remediation

The delta `6ef220e5..220c6f28` is 26 added lines in `minion-memory-rust/tests/layer04.rs` only.
Production, pins, corpus and manifest are unchanged.

| Finding | Change | Assessment |
|---|---|---|
| WP04-CR-017 | `initialization_refuses_partial_nonindex_relations_and_preserves_engine_errors` gains two cases, each on a namespace that holds **only** that object before open: `CREATE VIEW mneme_store …` and `CREATE SEQUENCE mneme_record`. It also asserts that the namespace's complete relation inventory (OID, name, kind) is identical before and after the refused open. | Exactly the required witness. The inventory assertion is stronger than asked. |
| WP04-CR-018 | `fetch_binding_projects_real_catalog_fields` gains a row that projects only the core `mneme_store` row of `pg_class.relpersistence` as `'u'` through the actual fetch SQL, and expects the `relations` part. | Exactly the required [F] control. It is reported as fetch-binding evidence, not a public or physical execution. |

## Executions (scheduler-granted Windows window; Cargo jobs ≤ 4; fresh mtimes before each gate)

| Check | Result |
|---|---|
| G0 | exact candidate `220c6f28`, clean tree |
| `cargo test --locked --offline --test layer04` (own review target) | **23 passed** |
| R06 (relations reads the pinned `'p'`), separate controls target, baseline first | **KILLED** by `fetch_binding_projects_real_catalog_fields` |
| R10 (initialize unless an ordinary table exists), the same | **KILLED** by `initialization_refuses_partial_nonindex_relations_and_preserves_engine_errors` |
| Post | tree clean; own throwaway database dropped, 0 owned remain |
| `mneme-process check --deep-sources` at the pair (state `0882d041`) | 8/8 |

Logs are in `.tmp/work/claude/l04-rust-rereview/` (`summary.txt`, `layer04.log`,
`mutants-r06-r10.log`).

**Evidence-retention note.** While preparing this re-run, Claude deleted the first review's
`.tmp/work/claude/l04-rust-review/mutants.log` by mistake. Its full content, all 14 results with R06
and R10 surviving, is transcribed in closure review 1's planted-violation table. The whole-suite
diagnostic of the two survivors (`diag-survivors.log`) and every other review-1 log are intact. No
result depends on the deleted file.

## Combined Rust evidence at the approved code

Closure review 1 already holds, at `6ef220e5`:
- a production reading that matches the contract;
- fmt, clippy `-D warnings` and docs clean;
- 64 integration tests and 1 doctest;
- the Python suite at 856 passed, 4 xfailed;
- 12 of Claude's 14 planted violations killed.

Production code is byte-identical at `220c6f28`, and the two survivors are now killed. Codex's own
Windows and Linux gates at `220c6f28` (its remediation record) agree. Every one of Claude's 14
planted violations is now killed by its intended witness.

## Disposition

APPROVED for the exact pair. On this basis:
- the Rust pair may be accepted onto `main` under G-009;
- Layer 04 (WP-04) Python and Rust certification, and CLOSED, are an **Owner** decision (as G-076
  was for Layer 03).
