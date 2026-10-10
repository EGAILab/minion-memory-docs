# WP-P01 CE-P01-01 R1 recheck — Codex

## Verdict and disposition

**APPROVED** for the exact pair:

- Docs: `be2f4e29b862bfe0b5d3e57604eb0d979ac57521`.
- Code: `bb05e3953a044ea8abd9d796675290ad9fe80941` (unchanged).
- Docs state head / review parent: `4e816b0f04d8ce337ea3a9a539f004e4d728b623`.
- Review branch: `review/wpP01-ce1-closure-3`.

**R1 resolved; WPP01-CR-001 closed.** CR-002–006 retain their closed dispositions from
`e557098b5e95aa270ea64fb96f8eade2990fbdb2`; unrelated semantics were not reopened.
No open finding or convergence reopening is identified in this recheck.

Scope and authority are Owner G-027, the R1-only handoff, and the agreed D16/D13 requirements.
This approves the candidate only. Acceptance onto main remains a separate coordination step.
Claude's remediation record and controls were review objects, not evidence assumed true.

## Independent closure evidence

The only production change from `c9be60e8` is in `checks.py`: `_nested_markers` supplies an
`os.walk` error callback and returns scan errors alongside markers; `check_repos` includes
those errors with the repository side. The exact-name comparison and exclusion of the root
administrative `.git` are retained.

I re-executed my original `DR-D16-walk-error` witness on Windows and case-sensitive POSIX:
the fixture contains a real `docs/nested/.git` file and is normally refused as a nested repo.
Injecting only its containing directory's `os.scandir` failure now returns a named `docs repo:
cannot scan ... for nested repositories` error instead of `[]`. No uncaught exception occurs.
This is a native marker with injected filesystem failure, not a claim of naturally occurring
host permission denial. The original injected exception lacks a filename, so its diagnostic
uses the repository-root fallback; it still refuses incomplete enumeration.

Three additional independent probes on each host inject OS-style errors carrying filenames:

- Failure reading the docs repository root: named docs scan error.
- Failures reading two docs subdirectories: both failed paths are reported.
- Failure reading a nested directory in the code repository: named code scan error.

All fixtures pass before injection. Every direct call returns normally and refuses after
injection. The errors retain side, path and cause. These witnesses exercise error propagation
through the actual `check_repos` entry point, not only the helper.

Direct regression controls preserve ordinary no-marker success, exact `.git` refusal,
`.GIT` acceptance on both hosts, linked-worktree root acceptance and containing-repository
refusal. The independently executed containment probes preserve fatal/localized-query
refusal and ordinary not-a-repository success. Actual candidate repositories pass `check repos`.
No additional semantic decision is required to close R1.

## Executions and accounting

| Own execution | Result | Evidence under `.tmp/work/codex/ce1-r1/` |
|---|---|---|
| Windows selected controls | 9 passed, zero failures/errors/skips; 65.011 seconds | `windows-tests.xml`, `windows-tests.log` |
| Case-sensitive POSIX selected controls | 9 passed, zero failures/errors/skips; 92.510 seconds | `posix-tests.xml`, `posix-tests.log` |
| Windows old-candidate replay on exact `c9be60e833d42c3981fb271e6882b0017b55c781` modules | R1 fails; other 12 closure controls pass; zero setup errors/skips | `windows-kill.xml`, `windows-kill.log` |
| Own original/direct probes | Four cases per host, including original R1 and containment | `direct/results.jsonl`, `posix-direct.jsonl` |
| Own additional scan probes | Three cases per host; root, multiple and code-side failures all named | `scan/results.jsonl`, `posix-scan.jsonl` |
| Actual repositories | 1/1 repo check passed | `real-repos.log` |

The selected candidate tests cover seven in-scope R1/repository controls. The substring
selection also includes two existing token/trigger controls, which pass; they do not reopen
CR-005. The exact selection is in `selection.txt`. Similarly, `-k R1` in the old scratch path
selected all thirteen closure controls: only R1 fails, and only that failure is kill-credited.
The R1 no-marker positive passes there. A full suite was not repeated under G-027's narrow
scope. Old-module replay is isolated scratch; production files were never swapped.

The independent probe scripts preserve the prior R1/containment inputs, changing only source
location, reference SHA and scratch destinations. They assert candidate module bytes against
the exact Git objects before executing. Additional scan probes explicitly assert baseline
success and named errors for every injected failed path. Their `wrong` metadata names the
challenged behavior; observed `current` cells establish closure.

## Environment, custody and boundaries

The previous Codex venv still points at the warned-about system Python. It was not used or
modified. I verified `warnings` imports under project-local managed CPython 3.12.8, created
`.tmp/cache/venvs/mneme-process-codex-r1` with that interpreter, and ran `uv sync --locked
--no-install-project` against the candidate tooling. Managed-only preference and the project
environment kept runtime/dependencies/caches under E:. No Python installation or bin export
was performed, and the damaged system runtime was not repaired by this review.

Windows uses managed Python 3.12.8 / Git 2.55.0.windows.1. POSIX uses managed Python 3.12.8 /
Git 2.34.1, WSL2 Linux 6.18.40.1 and a project E-backed ext4 image. Separate `A` and `a` files
prove case sensitivity. POSIX sets `MNEME_ROOT` before dot-sourcing and explicitly places
TEMP/TMP/TMPDIR in the mounted project image. Shells dot-source the project environment;
all review-controlled artifacts stay under the project. The POSIX process completed
successfully and its private mount was unmounted by its EXIT trap.

Evidence and harness SHA-256 fingerprints are indexed in
`.tmp/work/codex/ce1-r1/evidence-manifest.json`, SHA-256
`ac3a6c7c770ea229018612ba60abc8d3ce5e61df1100dff350e804a3ad80634c`.
Candidate module hashes are in `hashes.json`. Scratch scripts are
`.tmp/work/codex/ce1-r1-*.py` and `ce1-r1-posix*.sh`.

Only this review record is committed. Main docs stays on `wpP01/hardening` at the state head;
code remains at the exact main SHA. Production modules, source bundle and WP-01 worktrees
are untouched. Claude/Owner may take the next coordination step under G-027.
