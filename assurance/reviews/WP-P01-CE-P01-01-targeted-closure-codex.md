# WP-P01 CE-P01-01 targeted closure — Codex

## Verdict and reviewed objects

**CHANGES_REQUIRED** for the exact pair:

- Docs: `db672edc05d15f1f2981928c86e2bb9d4224966e`.
- Code: `bb05e3953a044ea8abd9d796675290ad9fe80941` (unchanged).
- Docs control head and review-branch parent: `0cebfcfd8f9ed294010679afaf930bf0f2f6c8ad`.
- Review branch: `review/wpP01-ce1-closure`.

Authority and scope are the targeted-closure handoff, G-018, and the agreed revision-2
`assurance/convergence/CE-P01-01-classification.md`: its row oracles, D1–D16 and §5.
Claude's remediation record and tests are review objects, not closure evidence. This review
does not grant acceptance or authorize another production implementation pass.

## Per-finding disposition

| Finding | Disposition | Independent evidence |
|---|---|---|
| WPP01-CR-001 | **Still open** | D16 case-variant directory is silently accepted; nested-marker domain differs between hosts; original E05 caller loses its named inventory error. See CL-001. |
| WPP01-CR-002 | **Still open** | Fatal errors in shallow and symbolic-ref verification queries become false passes of real disallowed repository states. See CL-002. |
| WPP01-CR-003 | **Still open** | Producer cleanup failure escapes the direct CLI entry point as an uncaught exception. See CL-003. |
| WPP01-CR-004 | **Still open** | A pre-existing staging symlink causes an outside-destination write and a successful build with a forbidden final symlink. See CL-004. |
| WPP01-CR-005 | **Closed** | D11/D12 type, token and routing oracles pass both supported-host controls and independent original-row replay. Valid string triggers, declared families, opaque fields and non-action nulls retain their agreed behavior. |
| WPP01-CR-006 | **Closed, runtime oracles** | Empty `--only` exits 2; `--docs` validation enforces the state boundary; bare-root roundtrip gives the named diagnostic. C05 is POLICY, not a historical defect kill. Missing contract synchronization is separately required below. |

No new WPP01 finding IDs are needed: the surviving witnesses refine the existing findings
within their agreed semantic neighborhoods. CL identifiers below label this review's evidence.

## Own executions and accounting

| Execution | Result | Evidence under `.tmp/work/codex/ce1-closure/` |
|---|---|---|
| Windows full tooling suite, Python 3.12.8 / Git 2.55.0.windows.1 | 255 passed, 5 skipped; exit 0 | `windows-suite.xml`, `windows-suite.log` |
| New controls against frozen six modules from `1422423e8fd7b163f498466d6596e3ef5741c53d` | 100 failed, 10 passed, 5 skipped | `windows-kill.xml`, `windows-kill.log` |
| Supported POSIX controls, Python 3.12.8 / Git 2.34.1, case-sensitive filesystem | 115 passed, zero skips; exit 0 | `posix312-controls-retry.xml`, `posix312-controls-retry.log` |
| Independent original characterization replay | All 688 unique original IDs executed on each supported host | `windows-matrix.jsonl`, `posix312-matrix.jsonl` and metadata |
| Actual candidate repositories, deep source check | Eight checks passed; exit 0 | `real-check-complete.log` |
| Actual candidate state roundtrip | ROUNDTRIP OK | `real-roundtrip.log` |
| Independent refined witnesses and positive controls | Results below, reproduced on Windows and supported POSIX | Five probe groups listed below |

Windows's five skips are the P09a–P13a host setup cases involving quote/tab/newline/NUL/CON
names. They receive no kill credit. The supported POSIX run executes them on an E-backed ext4
filesystem; distinct `A` and `a` files were also independently verified. Linux uses WSL2 kernel
6.18.40.1. The CPython runtime and installed dependencies are project-local on E:.

The frozen replay uses a separate scratch snapshot, with all six old module bytes verified
against their Git objects. Candidate production modules were never exchanged or restored.
Its 100 failures comprise 94 FIX-labelled tests, four POLICY tests and two incompatible-helper
failures (CH11's new `SOURCE_KEY`, and the replace-limit test's new `_replace`). The latter two
are not defect kills; POLICY remains separate. All ten passing controls are regression
controls: S330, three declared-ID kinds, string trigger, P01p, CH09, CH06, E10 and CH08.
No FIX-labelled test passes the frozen snapshot. This verifies the numerical replay claim,
but not the faithfulness of every control to its original row: E05 is the counterexample below.

The seven scratch replay scripts preserve the original inputs, adapting only the exact
candidate-byte assertion and the changed `_state_only_chain` call signature/resolved-tip
argument. Each fixture's baseline passes before mutation. Candidate module bytes are checked
against the exact Git objects. Host setup exceptions are labelled diagnostic, never credited
as product totality failures. The 688 replay plus the new control executions cover the agreed
row set; they do **not** establish that every oracle is satisfied.

KEEP-POS and OPAQUE gate signatures retain their baseline behavior. Thirteen KEEP-NEG cases
on each host move to an earlier intended shape refusal while remaining refused:
S172, S176, S183, S188, S199, S203, S210, S215, G06, G07, G08, G17 and O05.
Composite G08 retains its separate argument/equality interpretation. No unrelated semantics
are reopened. The acknowledged stale summary counts are not a new blocker.

## Required changes and witnesses

### CL-001 — D16 inventory domains and original E05 are incomplete

**Severity: medium. Maps to CR-001; D16/E03–E05 and nested-repository domain.**

1. An empty `spec/dir.md` directory produces the named unsupported-directory error. The same
   directory named `spec/dir.MD` produces `check_spec == []` and no inventory error on **both**
   hosts. `spec.py:inventory` checks the exact suffix in its directory branch, then silently
   traverses this case variant. D16 expressly refuses case-variant member suffixes.
2. A nested ordinary file named `.GIT` produces a nested-repository refusal on Windows and
   no error on POSIX. D16 defines an **exact-name and location** `.git` domain with identical
   results across hosts; `checks.py:check_repos` uses host-dependent `rglob(".git")` matching.
   This is an unreasonable Windows refusal against the agreed exact-name contract, not a
   request to weaken the genuine nested `.git` controls.
3. Re-executing original E05 means **renaming** `DOC.md` to `DOC.MD` and calling its original
   direct `check_spec` entry point. Both hosts return only the missing FROZEN-labelled-source
   citation error, without the named `DOC.MD` inventory error. `check_sources` does report the
   inventory violation. `_frozen_labelled_sections` consumes `_source_texts(ctx)[0]` and drops
   its errors. The new E05 control instead **adds** `EXTRA.MD` and calls `sources`. Its pass
   and frozen kill are a proxy for a different mutation/caller, not closure of original E05.

Required: enforce case-variant directory rules and the exact nested-marker name independently
of host matching; propagate source inventory errors to the original consuming entry point;
retain the original E05 recipe alongside useful additional source-check controls.

Evidence: `CW-D16-dir.md`, `CW-D16-dir.MD` in `witnesses/results.jsonl` and
`posix312-witnesses.jsonl`; `CN-D16-git-case`, `CN-E05` in `neighborhood/results.jsonl`
and `posix312-neighborhood.jsonl`; original E05 in both full replays. All are native filesystem
executions, not injected I/O.

### CL-002 — Failed proof queries become positive evidence

**Severity: high. Maps to CR-002; D5/D7/D8/D13 and G02/M05/J05/CH04, transport-error neighborhood.**

On each supported host, a valid CLOSED fixture with an actual shallow boundary is normally
refused with the named shallow-history error. Injecting exit 128, empty stdout and an error
stderr into **only** `rev-parse --is-shallow-repository` changes `all_errors()` to `{}`.
The independent real query still returns `true`. `_graph_overlays` ignores this query's exit
status and interprets an empty failed result as absence of a shallow overlay.

Likewise, a real `refs/heads/symbolic -> refs/heads/wp/test` candidate is normally refused.
Injecting exit 128 into **only** `symbolic-ref -q refs/heads/symbolic` changes `all_errors()`
to `{}`. The independent real query confirms the symbolic target. `_local_head` treats every
nonzero result as evidence of a non-symbolic head, including fatal errors.

These are native disallowed graph/ref states with **injected transport failures**; no claim
is made that Git spontaneously failed, or that the shallow witness fabricates ancestry.
The demonstrated false pass is acceptance of a state the agreed predicates explicitly refuse.

Required: unsuccessful proof queries must produce documented errors rather than authorize
their predicates. Distinguish a legitimate quiet non-symbolic result from fatal execution
errors, and validate successful shallow-query output. Preserve normal direct-head and
non-shallow positives and existing named overlay refusals.

Evidence: `CG-D7-shallow-query` in `graph-transport/results.jsonl` and
`posix312-graph-transport.jsonl`; `CG-D5-symbolic-query` in
`symbolic-transport/results.jsonl` and `posix312-symbolic-transport.jsonl`.

### CL-003 — Producer cleanup defeats totality

**Severity: medium. Maps to CR-003; D13 and D14's stated replacement limit.**

After valid staging, inject an OSError in the first replacement and then an OSError in cleanup
of the `.mneme-tmp` file. Direct `cli.main` raises `OSError("injected cleanup failure")` on
both hosts instead of returning error exit 1 with the replacement diagnostic.
The unprotected cleanup `unlink` masks the original failure.

Required: cleanup failures must remain within the documented error result and preserve useful
reporting of already replaced files and cleanup failures. This does not demand transactional
rollback. A separate first-replacement-only probe returns exit 1, reports `already replaced:
none` and rerun guidance, and removes the temporary files; that allowed limit is preserved.

Evidence: `CW-D14-cleanup` in both witness logs; `D14-first-replace` in both positive logs.
This is explicitly **injected I/O**, unlike the following native staging witness.

### CL-004 — Staging follows a symlink outside the producer destination

**Severity: high. Maps to CR-004; D14/Z06/CH08 and D16's regular-output domain.**

A valid single-entry fixture has an ordinary intended `DOC.md` destination and a pre-existing
`reference/source-text/.DOC.md.mneme-tmp` symlink to `escaped.md` outside the docs/source-text
destination. All paths, including the escaped witness, remain inside project scratch on E:.
Actual `sources build` follows the staging symlink, changes the outside-destination bytes,
then renames the symlink to `DOC.md`, returns exit 0 and reports one derived text plus index.
The final `DOC.md` resolves outside source-text and the candidate's own `check_sources`
refuses it as a forbidden symlink. Both supported hosts reproduce this without injected I/O.

Required: staging writes must obey the producer boundary and successful outputs must meet
the regular-file domain. Preflight of the declared final target alone does not establish this.
Retain CH07's unchanged-bytes invariant on later-entry preflight failures and CH08's ordinary
multi-entry success. This does not enlarge the agreed replacement rollback guarantee.

Evidence: `CW-D14-stage-symlink` in both witness logs. Independent CH11 execution accepts the
12 established bundle keys plus `DOC` and successfully builds all 13 scratch entries.

### CL-005 — Written contract did not move with all agreed rules

**Severity: medium. Shared checkpoint compliance; relates to open CR-001/004.**

The agreed classification's implementation commitment says `coordination-state.md` §§2–4
will state D1–D16 in the same implementation commit. Candidate §§2–4 omit D14's producer
preflight/staging/replacement limit and key/file bounds, D16's other-inventory domains, and
D15's empty-`--only` policy. The remediation record claims those sections state D1–D16.

Required: synchronize these agreed rules in the contract, or provide an explicit normative
reference to the exact agreed clauses. No new policy decision is requested. CR-006's runtime
oracles are closed; that does not excuse the separate written-contract commitment.

## Evidence custody, environment and limits

Raw logs, XML, JSONL, host metadata, preparation details and scratch harness fingerprints are
indexed in `.tmp/work/codex/ce1-closure/evidence-manifest.json`, SHA-256:
`9c11f6490193d9457587fafbd0179d8234ebcc0b7396964d793e77412990ad77`.
The manifest also records SHA-256 fingerprints of the six unchanged candidate modules.
These local scratch artifacts are evidence, not additional committed review files.

The five additional probe groups are `witnesses`, `neighborhood`, `graph-transport`,
`symbolic-transport` and `positives`, each with a Windows `results.jsonl` and a corresponding
`posix312-<group>.jsonl`. Scratch scripts are named `ce1-closure-<group>.py` under
`.tmp/work/codex/`. Positive probes independently verify CH05's raw blob reads with textconv
and smudge configured, CH11's established keys, and the ordinary replacement-failure limit.

**Excluded auxiliary-run incident:** I initially launched an auxiliary Python 3.10 POSIX
attempt with `MNEME_ROOT` set too late. Dot-sourcing the shell environment first caused
denied `/e` directory setup and left invalid temp variables. Pytest capture could then fall
back to `/tmp` outside the project; OWN-001 compliance cannot be certified for that attempt.
It is excluded entirely from closure evidence. A subsequent stop audit found no matching
live processes or open temp descriptors; the attempt had already ended. This is a reviewer
environment error, not a candidate defect, and no claim is made that every auxiliary temp
file stayed on E:.

The first supported Python 3.12 control launch on DrvFS also failed in pytest capture setup
and is excluded, with no candidate failure credit. The successful 115-test retry explicitly
sets TEMP/TMP/TMPDIR inside the case-sensitive E-backed ext4 image. Supported replay and
probe scripts set `MNEME_ROOT` before dot-sourcing and use project-local temporary paths.
Private mounts are unmounted by EXIT traps. The initial real deep-source check lacked
`python-docx`; project-local dependency installation followed by the successful eight-check
run supersedes that setup failure.

Only this review record is committed. Main docs remains on `wpP01/hardening`; code remains
at the exact unchanged main SHA. Production modules, source bundle and WP-01 worktrees
were not edited. The next coordination decision belongs to Claude/Owner under G-018.
