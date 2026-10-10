# WP-02 Python implementation targeted re-review - Codex

Date: 2026-10-11. Independent reviewer / Rust owner: Codex.

## Verdict

**APPROVED** for docs `d603683a67243cb60d6c747e6d6afb5192634076` /
code `43e0984e585975719231ba53466a9c78eba796e7`.

**WP02-CR-006 is closed by this candidate.** No open finding or new regression was
found in the targeted delta. This approves the Python implementation candidate and
its assurance repair; acceptance onto main remains a separate authorized action.
Rust still implements Layer 01, not Layer 02.

## Custody and scope

Followed the handoff at state `fc9a79b6`. New branch `review/wp02-python-2` starts
there in `review-worktrees/docs-wp02-python-review-2`. Code is a separate detached
exact-SHA checkout in `review-worktrees/code-wp02-python-review-2`. Only this record
is committed. No production, state, registry, candidate or other worktree edits.
All environments, temporary files, mutation copies and the POSIX filesystem image
remain project-local. Each shell sourced the project environment.

The prior complete review `a29b0092` stands except for its repaired finding. Verified
`b9f42d42` is an ancestor of this code; the entire diff above that approved NF-026
candidate is 56 added lines in `tests/core/test_layer02_history.py`. Python source
and the shared corpus are byte-identical to `1d7167c8`. The approved Rust runner
integration adds no Python behavior, and Claude's independent approval `8a071acc`
and both NF-026 records are present in the docs candidate.

## WP02-CR-006 disposition and independent oracle

Classification remains CONTRACT_ASSURANCE_DEFECT; owner_decision_required false.
The response and implementation-record correction explicitly withdraw the false
P12 equivalence claim and accurately distinguish native extraction from JSON-text
source insertion order. The actual implementation is unchanged and retains its
necessary canonical gate-4 sort.

Independently inspected and executed the new generator. It contains exactly all
6 permutations of the three typed fields crossed with all 3 two-field-invalid
subsets and the one three-field-invalid subset: 24 combinations. Both JSON-text
and native seams give 48 cases; the exact reviewer witness adds one. Routing
members interleave the typed members without changing their relative source order.
There are no omitted or duplicate combinations.

Re-derived every expected code from G-034/G-055: choose the earliest invalid typed
member in canonical order `occurred_at`, `record_id`, `recorded_at`; only `record_id`
gives `id.invalid`, the timestamp members give `timestamp.invalid`. The error names
`record`. The tests invoke the public admission function, never a private gate.

Own executions with candidate and isolated P12 package imports:

| Execution | Result |
| --- | --- |
| Candidate, new sweep plus exact witness | 49 passed |
| P12, same controls | 9 failed, 40 passed |
| All 12 original planted violations, full suite per mutation | 12/12 killed by intended test assertions |

P12 changes only the gate-4 loop from `sorted(value, key=_utf16_key)` to `list(value)`.
The failures are JSON-text source-order cases, including the original witness's
`id.invalid` instead of `timestamp.invalid`. Native cases remain passing because
native extraction already inserts in canonical order. Cases where both possible
first fields are timestamps legitimately share the same observable code; they are
regressions rather than individually discriminating kills. No import or environment
failure is counted as a mutation kill.

## Gates and direct regressions

Windows, project-local locked managed CPython 3.12.8:

- Ruff lint/format clean; mypy strict clean on all 14 files.
- Full suite **435 passed, 5 xfailed**, including all 12 ACTIVE canonical scenarios.
- Coverage 7.16.2 with branches, subprocesses and no exclusions: **740/740 statements,
  332/332 branches**, all modules 100%. Four worker files combined without errors.
- Exact docs/code `mneme-process check --deep-sources`: **8/8**.

Native WSL POSIX, managed CPython 3.12.8: the exact code archive ran inside a
project-local ext4 image in a private user/mount namespace; distinct `A`/`a` files
proved case sensitivity. Temp files were inside that image, which was unmounted
on completion. Full suite: **435 passed, 5 xfailed**. No POSIX coverage claim is made.

No production or corpus delta needs a new semantic interpretation. The new assertions
exercise the previously missing observable sort, and full Layer 01/02 regressions
remain green. Prior closed findings are not reopened.

Reproduction artifacts under `.tmp/work/codex/`: `wp02-python2-controls.py`,
`wp02-python2-mutants.py`, `wp02-python2-posix{,-start}.sh`; outputs under
`wp02-python-review-2/`: `new-controls.json`, control/mutant logs, `mutants.json`,
`report.json`, `settings.ini` and `posix-suite.log`. These are independent review
observations, not production changes or acceptance records.
