# WP-03 Python implementation — targeted re-review 2 (Codex)

**Verdict: APPROVED**

**Reviewed pair:** docs `6fe9115d91715c3e8732235a43936bd1b29a9d76` / code
`dd55fb4f0abec262d7ba0dab64f28a74840b84c3`.

**Reviewer:** Codex, independent reviewer and Rust implementation owner.
**Date:** 2026-10-11.
**Handoff:** `process/handoffs/WP-03-codex-python-implementation-review-2.md`, read at
`4d681c177e06f8c44fd1d5d9010c552f2af33bc6`.
**Responds to:** review `7d328f9514c313094a88fb26d5cb1975ac4c1e29`.

This is targeted closure of WP03-CR-006 and direct regressions. The response record was reviewed
as a claim, not closure evidence. The authority remains the agreed contract, particularly G-070
and PROJ-001. This approval concerns the exact candidate pair; acceptance and state transitions
remain with the coordinator under the recorded delegation. No Rust Layer 03 approval is implied.

## Disposition

| Finding | Classification | Disposition | Evidence |
|---|---|---|---|
| WP03-CR-006 | IMPLEMENTATION_DEFECT; no Owner decision required | CLOSED | Independently executed full routing-identity observations at position 7, with no argument, on both platforms; all eight new controls are killed when the profile is omitted. |

Open findings: **none**. Prior closures are not reopened.

## Change assessment and independent witnesses

The production delta is confined to `minion_memory/core/projection.py`: `_routing_identity`
formats the three already validated routing fields, and the `_UnknownRequired` catch uses that
detail while preserving `history.unknown_required`, `argument=None`, and the entry position.
`history.py` and certified Layer 02 admission are unchanged. The remaining code delta consists
of the routing controls and the early-lineage precedence control. There is no contract or corpus
expectation delta. The docs delta carries the response, imported prior review, handoff and state.

For example, native and JsonText inputs with reader profile `learning`, required unknown record
type `mystery`, schema 4, and position 7 now produce exactly:

```text
code: history.unknown_required
detail: (learning, mystery, 4) is required but not recognized
argument: None
position: 7
```

Changing the profile to `agent` changes the detail accordingly. Independently executed controls
on **each platform** include:

- 16 observations: two profiles through every native/JsonText combination of the three arguments.
- 48 further mixed-seam observations: known type with an unrecognized edition, and maximum-length
  profile/type tokens with edition `9007199254740991`; no identity truncation or lost position.
- Six further observations with instrumented hostile native subclasses: exact required detail,
  **zero hooks invoked**.
- Early lineage shape failure still precedes unknown-required admission. Generic stages across
  all arguments, foreign-profile exclusion, ignorable skips, duplicate handling, graph validation,
  canonical coalescing, direct membership, input ownership and error cloning remain consistent
  with the contract in the regression executions below.

The routing helper is reached only after admission has validated and normalized the routing
triple. Its formatting therefore receives exact built-ins; the hostile-subclass observations
also exercise this boundary.

## Independent executions

All shells sourced the project environment first. Managed project-local CPython 3.12.8 was used;
all temporary files, caches, coverage data and mutant copies stayed under the project root.
The code checkout was detached at the exact SHA. The review branch starts from the handoff state
descendant; the only committed addition is this review record.

| Check | Independently observed result |
|---|---|
| Windows full Python suite | **496 passed, 5 xfailed** |
| POSIX full Python suite | **496 passed, 5 xfailed** |
| Windows coverage 7.16.2, including subprocesses | **985/985 statements, 432/432 branches**, no exclusions or partial branches |
| Ruff check / format check | Clean; 18 files formatted |
| Mypy `--strict .` | Clean; 18 files |
| Process checks with `--deep-sources` | **8/8 PASS** |
| Independent public-seam scenario replay, each platform | **432 comparisons PASS** (54 steps × eight argument-seam combinations) |
| Independent generated projections, each platform | **12,000 cases, zero disagreements** on compared contract fields |

The generated cases are the same deterministic corpus replayed on both platforms, not 24,000
distinct cases. Their independent fixture model checks result fields and error code/argument/
position; the dedicated routing observations separately assert the full literal detail. The
model was not derived from the production projector or used as a general-purpose JSON oracle.

The POSIX run used an exact git archive on a project-local ext4/FUSE image in WSL, with distinct
`A` and `a` files proving case sensitivity. Its temporary paths remained in that image.

## Discriminating negative control

In a separate reviewer-owned package copy, replaced only the routing-helper return expression
with a detail omitting the profile. Verified that Python imported this copied projector, then
ran all eight `test_unknown_required_carries_position_and_full_routing_identity` controls.
Result: **8 failed, 18 deselected**, all assertion failures at the full-triple check; no syntax,
import or collection failure was counted as a kill. The exact unmodified candidate passes those
controls in both full-suite runs. Candidate source was never modified.

## Replay and evidence

Reviewer-owned drivers:

- `.tmp/work/codex/wp03-python-probes-2.py`
- `.tmp/work/codex/wp03-python-posix-2.sh`
- `.tmp/work/codex/wp03-python-review-2.coveragerc`

The probe driver imports the exact reviewed package through explicit `PYTHONPATH`. Windows suite
command: `python -m coverage run --rcfile=.tmp/work/codex/wp03-python-review-2.coveragerc -m pytest
-o addopts='' -q -p no:cacheprovider --basetemp=.tmp/process-temp/wp03-python-review-2
review-worktrees/code-wp03-python-review-2/minion-memory-python/tests`, followed by coverage combine
and JSON export. The POSIX script archives the exact SHA, runs that archive's full suite, and runs
the independent driver against it.

Evidence under `.tmp/work/codex/wp03-python-review-2/`:

| File | SHA-256 |
|---|---|
| independent-probes-windows.json | e57126766f98f6bf8fdb5d7bcb138b0fde4c5615e168eb6cebec81c805d01122 |
| independent-probes-posix.json | c84ff7abc30bba92d5dfa2a59a290431e73d8199d8f74f48ac9e443b7efdd7c7 |
| coverage.json | 52dff08dc382964c837040c371802e973f0a45fe168452d1e641eba55727fafb |

`missing-profile-control.log` and `negative-control.json` preserve the negative-control output
and copied import path. `posix-suite.log` and `posix-probes.log` preserve the POSIX executions.

The requested fix satisfies G-070 without changing Layer 02 semantics. No further remediation
is required by this targeted re-review.
