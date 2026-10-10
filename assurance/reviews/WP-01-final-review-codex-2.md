# WP-01 final review remediation re-review — Codex

**Verdict: APPROVED**

Exact approved pair:
- docs `83c66c25d560accb3d57ba20be631d55faab72ff`;
- code `bac6594e06dd321e547e917cebeeefc6562a19b9`.

Review branch: `review/wp01-final-2`, based on docs state
`9b38350299b638654351f1e7273d02c4e99a36e3`.
Handoff: `process/handoffs/WP-01-codex-final-review-2.md`.
Responds to the complete review `e340e4392b6c8646a69751e1230701e834a935ba`.
Claude's `assurance/reviews/WP-01-g3-evidence-claude.md` was a claim to verify, not closure evidence.

CR-009 and CR-010 are closed for this candidate. No new finding, semantic delta or regression was
found. The remaining conclusions of the complete review stand; prior closures are not reopened.
This approval supplies the independent review prerequisite for Claude's recorded G-009 acceptance
step. Codex did not accept onto main, modify coordination/certification registers, or start Rust.

## Per-finding dispositions

| Finding | Disposition | Independent evidence |
|---|---|---|
| WP01-CR-009 — current readiness records / decoder guidance | CLOSED for the exact pair | Read the rewritten feasibility matrix and WP plan. They cover G-035..G-043's record shape, native arrays/subclasses, cycles/shared aliases, duplicate base names, byte/control objects and exact returns, with checkpoint/closure references. They explicitly require structural stage 1 before numeric interpretation, using the duplicate-after-overflow witness. The JCS serializer defect is correctly separated from Mneme's integral bound. Historical review/probe records are unchanged. |
| WP01-CR-010 — G3 coverage evidence | CLOSED for the exact pair | Independently ran coverage 7.16.2 with branches and subprocess tracing over the whole minion_memory package: 618/618 statements and 282/282 branches, no missing/partial branches or excluded lines. Meaningful public-API controls now cover the reachable missing paths. The three source removals are unreachable on normalized public values; the regression probes below confirm equivalent observations. |

No new Owner decision is needed. Closure is technical and candidate-specific; this record does not
silently change the original classifications, registers or acceptance status.

## Delta challenge

The complete code delta was inspected: two production files, a new 79-line public-surface test
module, and the dev dependency/lock addition `coverage==7.16.2`. No canonical corpus, runner, typed
primitive, decoder, normalization, identity or timestamp implementation was changed.

The removed production branches are unreachable at the reviewed public seams:

1. `_format_number` receives only normalized numbers. `_number` converts all integral floats,
   including signed zero, to exact ints before serialization. Thus the float-zero branch cannot
   execute; zero still serializes as the int `0`.
2. A shortest decimal with `k <= n` in the old formatting branch denotes an integral value.
   All accepted integral values have already become ints; non-integral binary64 values continue
   through the remaining fractional/exponent paths. The finite/non-integral assertion documents
   this invariant and does not reject a new public value.
3. `describe` is an internal diagnostic helper, not a core public export. Its callers see exact
   admitted built-ins or decoder string tokens after native extraction. Tuple inputs become lists;
   unsupported native values fail stage 1 using constant diagnostics. The old arbitrary-kind
   fallback therefore cannot execute on a public validation path. The remaining list/dict case
   retains the prior bounded description, with an invariant assertion.

These arguments follow the existing G-023/G-025/G-042 normalization rules; they are not new
acceptance restrictions. Independent numerical, hostile-subclass and diagnostic controls reproduce
prior observations on the repaired code. No production import was patched by the reviewer.

The new tests exercise missing comma/colon errors, invalid text inputs, JsonText stored access,
representation and immutability, an uninitialized wrapper, invalid argument names, base-string
argument names, exact memoryview hashing, and invalid raw-hash input types through public APIs.
They preserve every earlier test. These were missing coverage, not behavioral defects, so the new
controls are not represented as semantic kills of the previous correct implementation. The prior
measured below-floor suite is the discriminating negative evidence for the coverage finding.

## Spec and records verification

Checked all changed docs paths against `18bc390c`; the historical governance, review and probe
records are unchanged. The state/handoff descendants of the new content candidate contain only
state and the new re-review handoff.

A mechanical text comparison confirms:
- all of `spec/core.md` is identical after removing the stale `, DRAFT` and `(DRAFT; observation`
  heading labels;
- the SER-008/009 text is identical after removing `, DRAFT` labels;
- serialization text before the Layer 01 section is unchanged;
- the Layer 01 introduction now names G-012..G-043 and the reviewed implementation-facing
  checkpoints, explicitly distinguishing them from pending acceptance onto main.

No normative grammar, acceptance rule, order, error code, bound, normalization or hash rule changed.
The plan records the remediation snapshot and points to the state file for coordination status.
It now accurately distinguishes historical CHANGES_REQUIRED reviews, contract approval, native
checkpoint/closure, and the final review findings. The maintained matrix describes the actual
strict decoder/extract-first Python implementation and the required Rust staged decoder. It does
not suggest that mapping an eager serde_json overflow error alone can satisfy stage precedence.

The author-run G3 record pins the repaired code SHA, declares the whole package as the covered
surface, accounts for every previously missed statement, and reports coverage, suite and quality
gates. Independent executions below reproduce its counts. Rust remains unimplemented, so no
cross-language certification is inferred from Python or the feasibility guidance.

## Own executions

All use healthy project-managed CPython 3.12.8. OWN-001 environment scripts were sourced before
commands; scratch, caches, coverage data, dependency environment, image and worktrees are inside
the project on E:. No system Python or production/candidate edits were used.

| Execution at the exact pair | Result |
|---|---|
| Full Windows suite under coverage | 354 passed, 5 placeholder xfails; 359 collected. |
| Whole-package coverage, subprocesses included | 618/618 statements; 282/282 branches; 100%; zero exclusions, missing lines or partial branches. Four process data files combined. |
| Case-sensitive POSIX exact code archive | 354 passed, 5 placeholder xfails in 7.63 s; suite wrapper exits successfully. Linux/WSL Ubuntu, project-local ext4/FUSE. Source matches the pinned detached checkout byte-for-byte; separate `A`/`a` files prove case sensitivity. |
| Characterization on Windows and POSIX | 25,470/25,470 OK; zero user hooks; 6,775 successful value returns recursively exact, zero non-exact returns. |
| Boundary oracles / completion controls on both hosts | All 75 boundary oracles met. Cross-host semantics and observations equal the prior approved code; cycle subprocess tracebacks compared by their actual exit/error rather than host path strings. M/D/CM completion controls also agree across hosts. |
| Re-derived ACTIVE corpus | 146/146 expectations match; eight ACTIVE scenario files. Corpus itself is unchanged. |
| Number-format regression challenge | 60,000 admitted binary64 samples match Node v22.15.1 JSON.stringify. |
| Independent time / stable-ID regressions | 5,000 generated timestamps match integer day/microsecond arithmetic; 5,000 generated ID tokens match the independent predicate. |
| Generated JSON/JCS regressions | 4,000 valid trees decode correctly and match rfc8785 0.1.4 bytes; 4,000 mutations agree with the structural acceptance/rejection oracle. Mixed-defect mutation checks do not claim precise first-error selection. |
| Supplied canonical/raw digest re-derivation | 13 canonical byte strings/digests and seven raw digests match. |
| Repository checks, deep source verification | repos/sources/spec/manifest/conformance/findings/registry/state: 8/8 pass. |
| Quality gates | ruff clean; 12 files already formatted; mypy strict clean on all 12 source/test files. |

Coverage totals by file (whole package, no scope narrowing):

| File | Statements | Branches | Covered |
|---|---:|---:|---|
| minion_memory/__init__.py | 1 | 0 | all |
| core/__init__.py | 5 | 0 | all |
| core/errors.py | 21 | 8 | all |
| core/identity.py | 83 | 26 | all |
| core/time.py | 38 | 14 | all |
| core/values.py | 470 | 234 | all |

The independent coverage configuration is:

```ini
[run]
source = E:/AI/Projects/OpenMinds/Minions/Minion-Memory/review-worktrees/code-wp01-final-2/minion-memory-python/src/minion_memory
branch = true
data_file = E:/AI/Projects/OpenMinds/Minions/Minion-Memory/.tmp/work/codex/wp01-final2.coverage
patch = subprocess
parallel = true
```

After sourcing `project-environment.ps1`, set PYTHONPATH to the exact candidate's
`minion-memory-python/src`. Use the reviewer-local Python to run `coverage run --rcfile=<above>
-m pytest <candidate>/minion-memory-python/tests --basetemp=<project-local scratch>`, then
`coverage combine`, `coverage report --fail-under=100`, and `coverage json` with that rcfile.
No coverage omission, exclusion or production instrumentation was added.

## Evidence and ownership

Own drivers/outputs under `.tmp/work/codex/`: `wp01-final2.coveragerc`,
`wp01-final2-coverage.json`, `wp01-final2-tests.xml`, `wp01-final2-posix.sh`,
`wp01-final2-posix/tests.xml` and `tests.log`, `wp01-final2-matrix.py`,
`wp01-final2-matrix/{win32,linux}/`, `wp01-final2-controls.py`,
`wp01-final2-probes.py/.json`, `wp01-final2-oracles.py/.json`,
`wp01-final2-audit.py`, `wp01-final2-matrix-audit.py`, `wp01-final2-audit-summary.json`.
The scripts reuse the prior independently authored recipes with candidate/output paths changed;
the oracle script imports only earlier reviewer oracle definitions, not Mneme implementation code.

The code checkout remains clean at `bac6594e`; the docs review branch adds only this record.
Claude-owned authoring worktrees, shared registers, main branches and remotes were untouched.
No Rust production work began. The only remaining action from this review is the required verified
loop-back notification; acceptance and the next Rust implementation handoff belong to coordination.
