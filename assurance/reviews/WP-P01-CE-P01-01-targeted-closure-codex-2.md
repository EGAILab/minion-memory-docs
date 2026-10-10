# WP-P01 CE-P01-01 targeted closure recheck — Codex

## Verdict and scope

**CHANGES_REQUIRED** for docs `c9be60e833d42c3981fb271e6882b0017b55c781` paired with
code `bb05e3953a044ea8abd9d796675290ad9fe80941`.

This is G-024's targeted recheck of CL-001–005, still-open CR-001–004 and direct regressions,
under the agreed revision-2 matrix and D1–D16. It is not a second full characterization or an
acceptance decision. The handoff and review branch start at docs control head
`56a02a640876d12dae34a93b8e9fb3ca3ab29ba7`.

Claude's remediation record and controls were challenged with my own executions. The original
CL-001 witnesses are fixed, but its replacement nested-marker enumeration silently skips a
directory-read failure. That direct regression prevents closure of CR-001. No item identified
here requires a new semantic decision or convergence reopening.

## Dispositions

| Item | Disposition | Evidence |
|---|---|---|
| CL-001 | Original witnesses resolved; direct regression remains | Case-variant directories receive named errors, `.GIT` is ignored on both hosts, and original E05's `check_spec` reports `DOC.MD`. The new marker scan loses a real `.git` marker on an injected read error; see R1. |
| CL-002 | Resolved | Failed shallow/symbolic queries refuse with named diagnostics. Valid quiet non-symbolic branches pass. Fatal and localized containment responses refuse; Git's ordinary not-a-repository answer remains accepted. |
| CL-003 | Resolved | Combined replacement/cleanup failure returns exit 1, names replacement and cleanup errors and already-replaced files, and gives rerun guidance. No uncaught cleanup exception. |
| CL-004 | Resolved | The original staging symlink's outside bytes remain unchanged; final output is regular, inside the destination, and passes source checking. Symlinked output directories refuse before writing. Ordinary multi-entry and established-key positives remain valid. |
| CL-005 | Resolved | Candidate `coordination-state.md` §3.1 now states the missing D14 producer bounds/preflight/staging/replace limit, D15 CLI scope and D16 inventory domains. Record 4 explicitly corrects record 3's erroneous synchronization claim. |
| WPP01-CR-001 | **Still open** | R1: incomplete nested-marker scan returns success. |
| WPP01-CR-002 | **Closed** | Original transport witnesses and direct Git/ref/overlay controls meet the agreed oracles. |
| WPP01-CR-003 | **Closed** | Original cleanup witness and direct producer-error controls meet the agreed oracles. |
| WPP01-CR-004 | **Closed** | Original native staging witness, output-chain control and producer positives meet the agreed oracles. |
| WPP01-CR-005 / 006 | **Remain closed** | No evidence from this limited recheck contradicts their prior closure; unrelated rows were not reopened. |

## R1 — Nested-marker enumeration silently skips an unreadable directory

**Severity: medium. Existing CR-001; CL-001 direct regression surface, D16 with D13.**

The fix replaces `rglob` with `_nested_markers`' exact-name `os.walk` scan. Its default error
handling silently ignores `scandir` errors. On **both Windows and case-sensitive POSIX**:

1. Build a valid two-repository fixture; all baseline checks pass.
2. Create a real `docs/nested/.git` file.
3. Direct `check_repos` normally reports `nested git repository inside docs repo: .../nested`.
4. Inject `PermissionError("injected unreadable nested directory")` into only the `os.scandir`
   call for `docs/nested`; every other filesystem and Git operation remains real.
5. Direct `check_repos` returns `[]` rather than a named enumeration failure.

This is a native marker with **injected filesystem I/O failure**, not a claim of naturally
occurring host permission denial. It demonstrates that incomplete traversal authorizes the
absence of a nested repository. The ordinary marker refusal proves that the fixture contains
the disallowed entry; the isolated failed read proves the false pass.

The agreed D16 domain requires an exact `.git` entry below the repository root to be refused;
D13 prohibits partial success/success-empty inventories. Candidate §3.1 also expressly says
“Every failure is a named error, never a silent skip.” Reporting inability to complete this
same scan is an implementation closure requirement, not a new naming, permission or policy
decision. The Windows `.GIT` correction must remain intact.

Required: return a named error for a failed directory enumeration instead of claiming a
complete scan. Retain the ordinary no-marker and exact-marker positives/negatives, and add
the above discriminating I/O witness. This review does not authorize a further fix pass.

Evidence: `DR-D16-walk-error` in `.tmp/work/codex/ce1-recheck/direct/results.jsonl` and
`posix-direct.jsonl`; scratch harness `ce1-recheck-direct.py`; production
`process/tools/src/mneme_process/checks.py`, `_nested_markers`.

## Executions and direct regression checks

| Own execution | Result | Evidence under `.tmp/work/codex/ce1-recheck/` |
|---|---|---|
| Windows targeted controls | 41 passed, zero skips/errors/failures; 188.815 seconds | `windows-tests-retry.xml`, `.log` |
| Case-sensitive POSIX targeted controls | 41 passed, zero skips/errors/failures; 335.019 seconds | `posix-tests.xml`, `.log` |
| Windows old-candidate kill replay | 10 failed, 1 passed, zero skips/setup errors | `windows-kill-retry.xml`, `.log` |
| Independent witness/positive/direct probes | 16 cases on each host; every entry point returned normally; R1 false pass reproduced twice | Six JSONL groups per host |
| Actual candidate repositories, affected checks with deep sources | 3/3 passed | `real-check.log` |

The targeted pytest selection includes all eleven new closure controls and the directly
affected existing controls: inventory enumeration, symbolic heads, hermetic Git selectors,
containing repositories, replace refs, grafts/shallow history, nested markers/linked roots,
producer path/key/entry validation, preflight and ordinary/failed replacement behavior.
The exact selection is retained in `ce1-recheck/selection.txt`. A full suite was deliberately
not repeated under G-024's targeted scope.

Independent old-candidate replay uses a scratch snapshot of all six production modules from
`db672edc05d15f1f2981928c86e2bb9d4224966e`, never an exchange of candidate files. It reproduces
**10 failed, 1 passed** on Windows: the pass is the plain-branch positive. The failing controls
are behavioral failures, not helper incompatibility or setup failures. The `.GIT` kill is
host-dependent and no POSIX kill is claimed for that Windows defect.

My prior original-witness scripts were reused with their inputs unchanged, adapting only
candidate/source location and scratch output paths. They assert all six candidate module
bytes against the exact Git objects. Both hosts execute the five groups `witnesses`,
`neighborhood`, `graph-transport`, `symbolic-transport` and `positives`, plus the new `direct`
group. Their input metadata's `wrong` field describes the challenged behavior, not an assertion
that it still occurs; the `current` results determine the dispositions above.

The containment neighborhood is within scope: the same absence-proof defect as CL-002,
in an existing `check_repos` predicate. Independent fatal and localized responses now produce
the named error; the ordinary English not-a-repository answer still passes. Fail-closed
localized output does not fabricate a repository or grant authority and introduces no new
semantic decision. CH01 retains its containing-repository refusal.

Independent producer positives execute a valid manifest with all twelve established keys
plus `DOC`, produce thirteen regular derived files, and preserve CH05 raw Git blob bytes with
textconv/smudge configured. A first-replace-only failure retains exit 1 and rerun guidance,
with successful cleanup; the agreed nontransactional replacement limit is not enlarged.
Actual repositories pass the three directly affected checks (`repos`, `sources`, `spec`)
with deep source verification.

## Environment, custody and repository boundaries

Windows uses Python 3.12.8 and Git 2.55.0.windows.1. Supported POSIX uses Python 3.12.8,
Git 2.34.1, WSL2 Linux 6.18.40.1 and an ext4 image physically stored under the project on E:.
Independent `A`/`a` files prove case sensitivity. `MNEME_ROOT` is set before dot-sourcing on
POSIX; TEMP/TMP/TMPDIR explicitly point inside the E-backed mounted image. Shells first
dot-source the project environment. Runtime, dependencies, bytecode, images and all test/probe
files stay under the project. Private FUSE mounts are unmounted with EXIT traps.

The first Windows pytest launches omitted the fixture's `MNEME_CODE_REPO` override and failed
in fixture setup. They are excluded; corrected runs explicitly point at the project code repo.
These setup errors receive no candidate or kill credit. The review worktree was initially
created at a relative Git-resolved location inside docs, then moved to the designated project
`review-worktrees` directory before executions; its empty old directory was removed. No
tracked production or coordination file was changed by these setup corrections.

All raw evidence is under `.tmp/work/codex/ce1-recheck/`; scratch harnesses are under
`.tmp/work/codex/ce1-recheck-*.py` and `ce1-recheck-posix*.sh`. Only this review record is
committed on `review/wpP01-ce1-closure-2`. Main docs stays on `wpP01/hardening`; the exact code
main is unchanged. Production modules, source bundle and WP-01 worktrees are untouched.
Claude/Owner must take the next coordination step under G-024.

Evidence files and harness SHA-256 fingerprints are indexed in
`.tmp/work/codex/ce1-recheck/evidence-manifest.json`, SHA-256
`afc503f4cd575bad0139b2bd3ee2dd035c67cf225c3e4583d34b2f885e579ea2`.
The candidate's six module fingerprints are in `candidate-hashes.json`. Both supported
POSIX processes finished successfully and their private mounts were unmounted.
