# WP01-CR-011 — independent corpus-delta review (Codex)

**Verdict: APPROVED.** WP01-CR-011 is resolved by the reviewed corpus delta.
No new finding or Owner decision is required.

**Reviewer:** Codex. **Date:** 2026-10-11. **Corpus author:** Claude.
**Exact reviewed pair:**
- code `cc3c5d549a43f166bfa1d990d3363887d5e63774`;
- docs `71e2b12e65ae420ecd4fc9cd5579056e5d7d96a6`.

The review branch `review/wp01-cr011` starts at docs state head
`896734dae76526fd79445b5b47ba43c0527e2943`. I verified that its difference from the docs
candidate consists only of the WP-01 state and this review's hand-off. The code checkout is
detached at the exact candidate. No candidate file, state or registry was edited.

This approval covers Claude's shared-corpus repair. I authored the Rust implementation and do
not independently approve my own implementation here. Claude must finish the Rust closure review
on this exact pair; acceptance remains with the recorded workflow and authority.

## Authority and scope

Read `process/handoffs/WP-01-codex-cr011-review.md`, HIST-004, Owner G-029, the closure review
and remediation record. Checked the entire code delta against `b07f3375`: only
`conformance/core/timestamp-seam-normalization.yaml` changes, replacing one input and its labels.
Its expected error, scenario ID, requirement links, status and operation counts are unchanged.
Both language implementations, Rust tests, manifest and all other corpus files are identical.

G-029 explicitly forbids year 0000 and requires **both** the parsed local civil timestamp and
normalized UTC instant to be in years 0001–9999. This is a decided rule, not an open choice.
WP01-CR-011's `CONTRACT_ASSURANCE_DEFECT` classification and path A / no Owner decision are sound.

## New oracle and replacement coverage

`0000-12-31T23:30:00-01:00` has a syntactically well-formed date/time and offset. Subtracting the
negative one-hour offset adds one hour: 23:30 becomes next-day 00:30, so its UTC instant is
`0001-01-01T00:30:00.000000Z`. That UTC instant is inside the range; the **local** year 0000 is
outside it. Therefore `timestamp.invalid` follows directly from G-029. No Python result was used
as the oracle.

Replacing the old `0000-01-01T00:00:00Z` removes that exact spelling from the canonical corpus,
but loses no distinct range predicate coverage:
- the old input failed both local and UTC lower bounds, so either guard could mask the other;
- the new input isolates the local lower bound;
- the unchanged `0001-01-01T00:00:00+00:01` isolates UTC underflow with a valid local timestamp;
- UTC overflow and accepted earliest/latest instants retain their existing controls;
- the Rust public-API unit control still rejects the old year-zero-with-Z spelling, and my own
  probe independently re-executed it through native, JSON-text and JSON-byte inputs.

The replacement improves discrimination without changing semantics or requiring a ninth scenario
or a 147th step. It does not claim exhaustive coverage of every possible invalid timestamp spelling.

## Independent executions

**GATE: G2 (escalated from G1) — reason: shared ACTIVE corpus repair, exercised through both
platforms' Rust canonical runner.** Full Rust suites were rerun for the unchanged implementation;
no fresh Rust G3 lint/documentation claim is made in this targeted review. Claude's remediation
record supplies the Python-owner run, rather than a Python run or oracle by me.

| Execution | Observed result |
|---|---|
| Exact candidate, Windows / rustc 1.97.1 | 16 integration tests + 1 doctest pass; 8 ACTIVE / 146 steps / 5 explicit expected failures |
| Exact candidate, native Linux under WSL / rustc 1.97.1 | Same counts, all pass |
| Passing control baseline before mutation | Exact candidate passes the repaired corpus |
| Own M07 scratch mutant: remove only local-year condition; restore old corpus from `b07f3375` | Full suite survives: 16 integration tests + 1 doctest pass |
| Same M07, changing only scratch corpus to the repaired candidate | Intended kill: `canonical_corpus`, zero-based step 22 (23rd timestamp input), observes canonical `0001-01-01T00:30:00.000000Z` instead of expected `timestamp.invalid` |
| Own M05 scratch mutant: restore original code, remove only `second > 59`; repaired corpus | Full suite survives: 16 integration tests + 1 doctest pass |
| Independent boundary probe, exact candidate | 9 timestamp inputs × Native/Text/Bytes = 27 checks pass, covering the old/new witnesses and accepted/rejected neighboring local/UTC boundaries |
| Independent second-bound probe | Seconds 60–99 × microseconds 0/1/999999: 120 chrono-constructor checks reject and 120 candidate public-seam checks return `timestamp.invalid` |
| `mneme-process check --deep-sources`, exact code and review-state docs checkout | 8/8 pass |

Scratch controls were created independently in `.tmp/work/codex/cr011-mutant` and
`cr011-probe`; they did not use Claude's mutant or differential drivers.
`cr011-controls.py` records the two guard substitutions and byte-exact old/new corpus setup.
`cr011-run.ps1` and `cr011-linux.sh` record invocations. Batches ran sequentially; caches, Cargo
homes, target directories and all scratch outputs stayed project-local under OWN-001.

## Challenge to the closure review

M07 is non-equivalent, and the old-suite survivor/new-corpus kill is independently reproduced.
The repaired candidate's code remains correct without modification.

M05 is **observationally equivalent for the pinned implementation**, not an assurance gap:
`chrono` 0.4.45's `NaiveTime::from_hms_micro_opt` delegates to `from_hms_nano_opt`, which rejects
`sec >= 60` unconditionally (`src/naive/time/mod.rs`, lines 377–384 and 428–434). Fractional
precision remains capped at six digits, so this mutation cannot introduce chrono's alternative
leap-second encoding either. Valid seconds follow the unchanged code; invalid seconds still yield
the same single `timestamp.invalid` error. I inspected this dependency source, executed the
constructor/public-seam controls and reproduced M05's suite survival.

This classification does not authorize deleting the production grammar check or relaxing HIST-004;
the candidate retains the explicit guard. It only explains why that particular output-based mutant
cannot be killed by a conforming timestamp witness.

I found no contrary evidence in the closure conclusions relevant to this delta. I did not rerun
the 187,236-case differential campaign, the other 14 mutants or the whole prior implementation
review; those remain Claude's independent Rust-review evidence. This targeted corpus review does
not substitute for it or reopen earlier closures without new evidence.

## Disposition

**WP01-CR-011: resolved.** The new oracle is faithful to G-029, kills the intended wrong
implementation, preserves meaningful boundary coverage and passes unchanged Rust code on both
platforms. The shared artifact is suitable for Claude's final closure step on the exact pair above.
