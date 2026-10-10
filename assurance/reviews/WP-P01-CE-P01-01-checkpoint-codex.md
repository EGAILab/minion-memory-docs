# WP-P01 — CE-P01-01 checkpoint review (Codex)

**Verdict: CHANGES_REQUIRED**

Reviewed exact checkpoint `de153c0aa0d4311218299fba4b3db832b6ee77e0` on
`review/wpP01-ce1-claude`, whose parent is characterization
`281b81a3281ede7dc41a3f2913ae3a4b0b199625`. Handoff/control:
`bfe10f302e267d2bed1c213b7f0c5ae4efd0254d`. Frozen behavior reference:
`1422423e8fd7b163f498466d6596e3ef5741c53d`; code main:
`bb05e3953a044ea8abd9d796675290ad9fe80941`. All named objects exist. The main docs tree
remains on `wpP01/hardening`; both main working trees were clean. The six imported production
modules matched the frozen reference byte-for-byte before probing; the control head has no
frozen-module/coordination-text difference from that reference. No production changes, source
bundle changes, WP-01 inspection or implementation were performed.

The 688 original row IDs are present exactly once, with no extras or omissions. That mechanical
coverage is confirmed; the proposal is not yet one consistent implementation contract. Its source
key policy refuses every established key, its E10 policy mistakes a supported root worktree for a
nested repository, and several row oracles contradict their governing decisions. This review
requires the changes below before the two-party checkpoint can become agreed.

## Required changes

### CE1-CP-001 — preserve the established source-key domain (high)

**Affected:** D14; C16, V08; CR-004. Checkpoint §4 D14 (lines 134–142), rows C16/V08.

D14 requires lowercase source keys, but the actual authority/provenance manifest uses
`FND, MVP, R00, R01, R02, R03, R04, R05, IAA, BOOT, SUMMARY, PACK`. The fixture uses `DOC`.
All thirteen fail the proposed key predicate. Independently executed `CP-D14` first ran the
frozen fixture's source build successfully (exit 0), then evaluated the exact proposed predicate
against the fixture and all twelve actual keys: every match was false. Existing citation parsing
also uses uppercase source keys (`spec.py:15`); lowercase renaming is not a bounded-output fix.

**Required:** retain the exact established citation/provenance identifiers while refusing unsafe
keys and output escapes. Align the declared key domain with the existing citation domain and
add the actual keys plus DOC as positive controls. Preserve the C16/V08 success oracle. Do not
resolve this by silently changing provenance keys/citations or widening implementation scope
beyond the agreed frozen surface. Traversal/type/hash controls remain required.

### CE1-CP-002 — distinguish linked roots from nested Git markers (high)

**Affected:** D16; E10; CR-001; metadata lookup in D7. Checkpoint lines 147–151 and row E10.

E10 creates a linked docs worktree and passes that worktree itself as the docs root. Its `.git`
file is the root's administrative pointer. It is not a nested repository or a gitlink.
Independently executed `CP-E10` returned a matching `rev-parse --show-toplevel`, root `.git`
kind `file`, `check_repos == []`, and exactly one enumerated marker: root `.git`. D16/E10's
refusal would introduce a false refusal of the project-authorized worktree workflow.

**Required:** keep supported linked-worktree roots valid; reject genuinely nested repository
markers independently of whether their marker is a file or directory. Replace E10's FIX oracle
with the proper positive control and add a separately located nested `.git`-file negative
control. Spell out D16's domain for each inventory: suffix, recursion, regular/symlink/directory
handling, permitted supporting files, and root administrative-marker exception. A nested-repo
scan is an exact-name/location domain, not a generic suffix inventory. D7 must inspect Git's
actual administrative/common paths for linked roots rather than assuming `<root>/.git/` is a
directory. No WP-01 worktree was touched to obtain this evidence.

### CE1-CP-003 — reconcile the trigger-shape policy with its positive rows (medium)

**Affected:** D12; S229, S258, S259, S262, S266; CR-005. Checkpoint rows at lines
418, 447–448, 451, 455.

These original accepted WAITING probes use a nonblank **string** trigger (`explicit trigger`
or `trigger`). D12 requires a mapping containing nonblank `condition`, yet these rows remain
KEEP-POS with an acceptance oracle. `CP-status-1` reproduced the original S229 shape:
frozen `validate_state == []`, while the stated D12 trigger predicate is false. Its opposite
`CP-status-2` uses `{condition: explicit trigger}`: the frozen gate accepts it and the proposed
predicate is true.

**Required:** either keep the old string domain explicitly or retain the mapping decision and
reclassify the original string rows with a refusal oracle. If retaining the mapping decision,
add the mapping-shaped positive controls for the same candidate/owner/action cases. Do not
silently replace the original inputs while claiming unchanged KEEP-POS controls. Account for
the legitimate shape migration separately from truthy wrong-type witnesses N03–N05.

### CE1-CP-004 — define identity at the correct gate and correct P01a (medium)

**Affected:** D2; P01a; pure-object S/X positive controls; CR-001/CR-005. Checkpoint row
P01a at line 565.

The original P01a is not a positive identity fixture: `WP-U.yaml` contains
`work_package: WP-X`. `CP-P01a-composite` repeats that exact mutation and obtains both
`roundtrip == []` and `check_state == []`. The proposed file-stem equality is false. Its
KEEP-POS oracle cannot simultaneously mean that both gates still accept and that D2 is enforced.
Most structural S/X probes call `validate_state(object, 'probe.yaml')`: the second argument is
a diagnostic label, not a proven file path.

**Required:** state which gates enforce file/domain identity and which only validate an object
or compare snapshots. Give P01a an oracle for each invoked component; at least the file-aware
state gate must reject its mismatch under D2. Add a real matching-ID positive fixture. If
roundtrip remains equality-only for content identity, say so; if it acquires identity validation,
say so and classify that change. Do not infer a filesystem identity from a diagnostic label or
invalidate all pure-object positives by doing so. D2's ASCII uppercase token choice itself is
reasonable for the currently declared WP domain.

### CE1-CP-005 — separate actual repairs from preserved/policy controls (medium)

**Affected:** S330, M03, C05, U07; D7/D12/D15; FIX totals and negative-control accounting.

S330's `episode: finding` is a nonblank string and its other convergence evidence is valid.
`CP-status-3` independently returns `[]` and evaluates D12's relevant predicate true. S330 is
therefore a positive under D12, not a CR-005 FIX. The current M03 environment probe already
returns the proposed sanitized/no-environment result (`repos: [], state: []`); it does not
discriminate omission of sanitization for that variable. `CP-C05` also confirms that empty
`--only` runs **all eight checks**, reports `8/8 checks passed`, and exits 0. It is not a
zero-check-success witness. Refusing that spelling is a deliberate CLI policy/hardening change.
U07's proposed oracle says W is DIAG, but its original executed Windows cell is RETURN `[]`:
the Unicode filename was materialized, committed and checked successfully. It must not be
skipped as an unrepresentable Windows case.

**Required:** make S330 KEEP-POS unless an additional episode grammar is explicitly proposed
and justified. Label M03 as a preserved result/defensive environment-property control; if it is
to discriminate sanitization, add an executed environment-at-subprocess witness. Record C05's
actual all-check behavior and distinguish its proposed usage restriction from a false assurance
pass. Remove U07's incorrect Windows-DIAG carve-out. Recompute dispositions/totals and label
each negative control's discriminating property.
Do not count an unchanged success oracle as a semantic kill of known-bad tooling. This does not
weaken the real CH01/CH02 witnesses or D7's required sanitization.

### CE1-CP-006 — make revision and composite-ref oracles unambiguous (medium)

**Affected:** D8; G07/G08/G12, J06–J08; CR-002. Checkpoint D8 lines 101–106 and
J06–J08 rows at lines 873–875.

D8 admits a **plain branch name**, HEAD, or full commit OID. J06–J08 say
`refs/heads/<name>` is an accepted argument. That can describe a resolution namespace or a
different accepted CLI spelling; the exact checkpoint must specify which. G08 and G12 combine
candidate-ref and roundtrip calls: HEAD/full OID are invalid candidate refs but allowed
roundtrip revisions, even though the original fixture's changed bytes can still fail equality.
Blanket “non-branch / malformed ref refused” does not specify both component oracles.
`CP-D8-spelling` executes matching roundtrips for an existing local branch named `deadbeef`
and for `refs/heads/wp/test`; both are accepted today. A local branch whose spelling happens
to be eight hex characters is distinct from a bare abbreviation with no local head.

**Required:** define exact accepted CLI spellings and the fully qualified resolution namespace
separately, and align the J/G oracles. Provide component results for composite rows, separating
argument rejection from intended byte-equality failure. Decide explicitly how an actual local
hex-spelled branch is treated; do not let an abbreviation be accepted by object resolution alone,
or silently refuse a permitted branch solely because its spelling resembles an abbreviation.
Keep the one-OID proof rule and exact candidate object kind.

### CE1-CP-007 — add the cross-entry producer failure control (medium)

**Affected:** D14; C16/V08/Z09 plus new producer control; CR-004. Existing Z09 checks a
bad hash on the **first** entry, which cannot distinguish per-entry writes from full preflight.

`CP-later-entry-corrected` supplies valid YAML with a valid first DOC entry and a valid-shaped
second entry whose hash is wrong. Frozen source build exits 1; the first derived text has already
changed, while the index remains unchanged. This is an independently executed partial-build
witness of the exact behavior D14 promises to eliminate. The earlier attempt accidentally
shared a nested metadata list and generated a forbidden YAML alias; that attempt was refused
before writes and is **not** credited as the witness.

**Required:** add and classify the valid-first/invalid-later case, with failure leaving every
existing destination/index byte unchanged and producing no new output. Include the corresponding
all-valid multi-entry positive. State whether “failed build writes nothing” covers validation
failure only or also commit/write failures, and give controls/explicit limits for the chosen
scope. Full preflight is a sound requirement; the present first-entry hash control alone does
not establish it.

## Independent challenge results

Twenty recorded checkpoint probe cells were executed on Windows using the unchanged frozen
modules. Proposed regex/shape predicates were evaluated separately from those modules; no
proposed validator was implemented. Successful World baselines were asserted before mutations.

| Challenge | Independently executed result | Assessment |
|---|---|---|
| CH01 | containing outer Git repository detected normally; with GIT_CEILING_DIRECTORIES the same check returns `[]` | reproduced false pass; retain control and all-GIT-variable sanitization |
| CH02 | orphan mains refused; refs/replace empty; hidden replacements plus GIT_REPLACE_REF_BASE return `{}`; sanitized environment restores refusal | reproduced false pass outside standard replacement namespace |
| CH03 | actual merge-base exit 0 with ordinary Git and `--no-replace-objects`; nonexistent GIT_GRAFT_FILE restores exit 1 | reproduced; no-replace alone is insufficient |
| CH04 | corrected recorded candidate differs from tip; ancestry exit 0 before shallow boundary and exit 1 afterwards; shallow probe says true | real ancestry-removal witness; no invented-ancestry false-pass claim |
| CH05 | raw git-show bytes unchanged with both configured smudge/textconv drivers | confirmed for this Git/host; no gap claimed |

My first CH04 attempt also accidentally used a newly generated state whose candidate equalled
tip. It is preserved as `CP-CH04` and explicitly excluded from discriminating evidence; the
credited result is `CP-CH04-corrected`, using the recorded candidate and an asserted distinct
tip. This avoids repeating the inconclusive fixture as proof.

## Decisions and classification audit

| Decision | Review outcome |
|---|---|
| D1 | shared exact inventory domain is sound; reconcile gate oracles with D2 and preserve deletion semantics |
| D2 | uppercase portable WP-ID domain is acceptable; fix equality/control scope per CE1-CP-004 |
| D3 | regular committed/working kinds and named diagnostic are sound |
| D4 | strict UTF-8/NUL identity and I07 framing control are sound |
| D5 | explicit refusal of symbolic candidate heads is a defensible policy; no active project candidate requires them; normal HEAD resolution in D8 is distinct |
| D6 | exact commit-object kind is sound; tag peeling must not substitute a candidate |
| D7 | sanitization/canonical-graph policy is sound in direction; CH01–CH03 reproduced, actual metadata lookup must support valid linked roots |
| D8 | one OID per proof is sound; CLI spellings/composite oracles need CE1-CP-006 |
| D9 | one validated state object per invocation is sound; control must verify snapshot use, not merely demand a failure after every post-read mutation |
| D10 | linear per-commit chain, exact registry path and preserved accepted-CLOSED exemption are sound |
| D11 | exact integer/token shape is sound |
| D12 | declared requirement families and finding grammar cover current IDs; repair trigger/episode oracles per CE1-CP-003/005 |
| D13 | total direct gates with aggregate backstop are sound; host setup failures stay diagnostic-only |
| D14 | bounded/preflight producer is sound in direction; source key compatibility and cross-entry coverage need CE1-CP-001/007 |
| D15 | root/containment/scope restrictions are reasonable; C05 is explicit policy rather than an empty-check false pass |
| D16 | needs per-inventory domains and linked-root/nested-marker separation per CE1-CP-002 |

CR-003 as SEMANTICS_NEUTRAL_HARDENING is supported for its listed exception/error-only rows:
they fail rather than return success. X104 is correctly KEEP-NEG: it returns CLI exit 1, not
an unhashable-owner exception. My characterization's introductory CR-003 reference grouped
X104 too broadly; the recorded cell and Claude's classification have the correct result.

CR-006 as SEMANTICS_NEUTRAL_HARDENING/policy is also supportable: C05 executes/reports all
checks, V12/Z10 are validate-only contextual limits, F08 already reports failure. Clarify C05's
disposition rather than upgrading these to semantic false passes. The proposed optional updater
metadata must preserve today's string-or-null guard: `CP-updated_by` and `CP-updated_reason`
return a type error for lists, consistent with KEEP-NEG S066–S069/S073–S076. “Opaque” means
no authority, not removal of existing type checks. No new WPP01 finding ID is necessary for
the required changes: source/identity/proof/control gaps fit the existing CR-001/002/004/005
surface; the remaining problems are checkpoint-policy/oracle contradictions.

The all-row audit compared the proposal to the original recorded cells and their actual probe
recipes, by consumer families and cross-boundary decisions. It confirms 397 KEEP-NEG,
98 KEEP-POS, 84 OPAQUE, 97 FIX, 2 POLICY, 6 LIMIT, 4 DIAG as the proposal's counts—not as
approved counts or semantic-kill counts. Those counts must change when the contradictions above
are reconciled. No full production test-suite run or implementation closure is claimed in this
checkpoint review.

## Evidence and scope

Executed checkpoint runtime: Python 3.12.8; Git 2.55.0.windows.1. JSONL SHA-256:
`769d774c3ab19faf57a16cf9f73383a35ef52e587068c4db2926abd14d121bfa`.
Harness SHA-256 values:

- `ce1-checkpoint-probes.py`: `3cbef89704a6a346ff14d50c49fb52db7827dd435a94322dfa30100514203315`
- `ce1-checkpoint-more.py`: `4ad7e6b59c12adb643fa7efd35ff4864df471f5ac33e3b1b09f4d53b1c14a5de`
- `ce1-checkpoint-last.py`: `ad42db5d04cfc745c3351b8f2d982da7a95373e9a79390b6096ccb81e1486fe2`
- `ce1-checkpoint-row-audit.json`: `b12f520b44add8cefec35672df6b696827f9e8a69d39a84cece74b8f650a6790`

Scratch evidence is wholly project-contained:
`.tmp/work/codex/ce1-checkpoint-probes/results.jsonl` (20 IDs, includes excluded setup attempts),
with harnesses `ce1-checkpoint-probes.py`, `ce1-checkpoint-more.py`,
`ce1-checkpoint-last.py`, and audit `ce1-checkpoint-audit.py` / `ce1-checkpoint-row-audit.json`.
Frozen-source identities are checked by the reused import/bootstrap fingerprint guard in
`ce1-probes.py`; its probe catalog is not rerun or overwritten. This review's append scripts
use a separate CE_BASE. Every shell first sourced project-environment.ps1; venv, fixtures,
Git objects, caches and records remained under the project root. CH01/CH02 and CH03/CH05
were authored/executed independently, not imported from Claude's witness runner.

Only this review record is committed on `review/wpP01-ce1-checkpoint`, based directly on
`de153c0`. The main/control branches, frozen files and WP-01 worktrees remain untouched.
This verdict withholds checkpoint agreement; Claude's production implementation remains frozen
pending a consistent revised checkpoint and separate approval. It grants no acceptance authority.
