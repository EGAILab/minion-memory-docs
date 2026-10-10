# WP-P01 targeted closure review 2 — Codex

Reviewer: Codex, independent reviewer, Rust implementation owner and cross-language challenger. Date: 2026-10-10. Task: TARGETED_FINDING_REVIEW under `process/handoffs/WP-P01-codex-targeted-closure-2.md`. Claude's characterization and response are review objects, not evidence of closure.

## Exact candidate and preflight

- Docs D: `a9ed71d2f943c3fb5dc32f51fb7d5db99291abcb`, reachable from `wpP01/hardening`.
- Code C: `bb05e3953a044ea8abd9d796675290ad9fe80941`, actual code main, unchanged.
- Docs control head/review-branch base: `aaaa46f1d65ee49e9038c19a66ebb56b0d18fbd3`.
- Previous docs: `cd8288384473ab32472629fbbc7e37d5ec2cbf26`, same code.
- Previous review: `assurance/reviews/WP-P01-targeted-closure-codex-1.md` at `869fa5734bf47c39c751cead34c6a1065e4f9237`.
- Actual docs main: `237948fee550b691d0e83defb6c49186a27af3b8`; docs `wp00/bootstrap`: `21fcb416d90d6544a94ad61c3ebe4e43362b1546`.
- Governance G-008–G-011, bundle and process/consumer pins are unchanged.

Preflight passed: both objects exist; candidate reachability is correct; both main working trees were clean. The sole commit in `D..wpP01/hardening` changes only the handoff and WP-P01 state. Read the complete `cd828838..D` diff, characterization, corrected fixtures, operative state and applicable coordination/exact-pair rules. The handoff/environment is valid.

The main docs working tree remained on `wpP01/hardening`. New branch `review/wpP01-codex-3` is based on the control head in separate E:-contained worktree `review-worktrees/docs-wpp01-codex3`; this branch adds only this record. Claude's WP-01 worktree and its contents were not inspected or changed. No implementation or WP-01 work was done.

## Per-finding disposition

### WPP01-CR-001 — OPEN, refined Windows inventory-eligibility witness

The refined non-ASCII witness is repaired. `ls-tree -z` and `diff-tree -z` use `_git_paths`, which splits raw NUL-delimited output and strictly decodes actual path bytes as UTF-8. It preserves quotes, non-ASCII characters and leading spaces as path data rather than display transformations. Failure/undecodable output is rejected, not treated as an empty successful inventory. Both current call sites supply `-z`.

Independently reran the preceding review's exact scratch recipe against D: matching `WP-Ü.yaml` no longer produces the false uncommitted-state error, and deleting it now reports it as committed but missing. The CLI fails the deleted-state roundtrip. Also independently tested matching inventory, uncommitted deletion and committed deletion for both `WP-Ü.yaml` and ` WP-space.yaml` with `core.quotePath=true`. Matching and committed-deletion cases pass; missing working objects fail. The permanent non-ASCII descendant-path positive and prior ASCII inventory controls cover that path-display neighborhood.

The inventory comparison nevertheless still uses different eligibility rules. On this Windows host, `Path.glob('*.yaml')` includes `WP-UP.YAML`, while committed names are filtered by case-sensitive `name.endswith('.yaml')`. In a fresh baseline-valid World, commit that second state: raw Git inventory contains it, the working glob contains it, and all ordinary checks pass, but roundtrip falsely calls it uncommitted. Refresh the remaining state's candidate and commit, then delete only `WP-UP.YAML` without committing: roundtrip returns `[]`, aggregate checks return `{}`, and Git reports `D process/state/WP-UP.YAML`. No macOS behavior or hypothetical filesystem is needed for this witness. The scratch script imports the frozen candidate from the review worktree, independently of the temporary old-tool replay.

### WPP01-CR-002 — OPEN, refined acceptance-namespace witness

The prior repository-side witness is repaired: code/docs repositories are fixed by side, wrong-side records are rejected, and wrong-side repositories are never used for object/ref checks. Missing/empty/null/partial CLOSED records remain rejected. The earlier both-code CLOSED probe now fails as intended. However, the exact accepted pair is still not protected against a different reference-identity substitution.

`show-ref --verify refs/heads/<ref>` checks branch existence, but later reachability/descendant checks pass the bare `<ref>` to Git. CLOSED acceptance also passes bare `main`. A same-named tag is resolved instead of the checked branch. In fresh Worlds with correctly bound, complete CLOSED records and existing orphan main branches, adding `refs/tags/main` at the named candidates changes aggregate errors from explicit non-acceptance errors to `{}`. Both candidates still fail `merge-base --is-ancestor <candidate> refs/heads/main` with exit 1.

The active counterpart also bypasses the new ref-SHA repair: preserve the original docs candidate, commit non-state `record.md` on `refs/heads/wp/test`, and add tag `wp/test` at the candidate. The plain branch exists and the recorded ref passes the grammar, but the unqualified descendant range becomes empty. Aggregate errors change from the intended non-state-descendant error to `{}`. Calling the descendant check with `refs/heads/wp/test` reports the hidden content again.

These probes start from `World.build()` with aggregate `{}`. Each first proves the correct rejection before adding only the colliding tags. They do not manipulate real candidate refs or main. This remains the same exact accepted-pair evidence obligation: field/repository completeness is repaired, but the branch identity used to prove acceptance is not bound. It is not claimed that this inherited ambiguity was introduced by remediation 2. The new characterization and branch-existence check explicitly place its safety premise in scope.

### WP00-CR-014 — regression judgment

**PROVISIONALLY CLOSED @ D/C**, preserving the previous judgment. No positive-label predicate, source-section slicing, spec statement, manifest citation, or guard documentation changed. The full suite re-exercises the positive-label units and repository controls. The prior independent source review of all 49 FROZEN main statements remains applicable; a mechanical label pass is not substituted for that review.

## Characterization and route judgment

The trigger-A acknowledgment and characterize-before-fixing decision are substantively adequate as a route choice. The record recognizes the real pattern, does not use SCOPING's lack of a direct convergence transition to deny the trigger, and commits to Owner escalation on another surviving finding. Its trigger counts were accurate at the decision point. The adopted §11.8 exception permits a reasoned ordinary route; it does not guarantee characterization completeness.

| Row | Independent disposition |
|---|---|
| 1 — inventory paths | Repair adequate for the quoted-path witness and tested non-ASCII/leading-space neighborhood; raw NUL framing and strict decode are appropriate. Inventory eligibility is still inconsistent on the current Windows host: case-insensitive glob versus case-sensitive committed-name filtering. |
| 2 — changed paths | Same path repair is correctly applied to per-commit descendant checking; the positive control tests the previous false rejection. |
| 3 — candidate repository | Canonical side binding is implemented, including avoidance of wrong-side Git resolution; earlier witness is caught. |
| 4 — candidate ref | SHA/range/option-like/nonexistent refs are rejected, and the discovered SHA-empty-range witness is repaired. The characterization omits namespace ambiguity: existence is checked as a branch but subsequent resolution uses an unqualified name. The refined WPP01-CR-002 witness survives. |
| 5 — roundtrip revision | Syntax/commit-existence checks reject the tested bad revisions. Plain-name resolution also uses unqualified Git revision syntax; it is not an assurance that the named local branch was selected. This needs inclusion in the reference-identity sweep rather than a claim that grammar alone binds a branch. |
| 6 — other Git commands | Hex/no-output/raw-byte framing avoids display-quoting failures, but does not establish reference identity. `merge-base` and `rev-list` consume the ambiguous refs above. Also `rev-parse --show-toplevel` emits a path, not hex/no-output; its current fixed workspace check is not a general raw-path guarantee. |
| 7 — Unicode normalization | Deferral of macOS normalization is adequate for this Windows-host review with no macOS gate in scope, explicit first-macOS-run trigger, and no macOS correctness claim. No normalization was imposed that could conflate distinct preserved names. However, filename preservation does not establish equal matching rules: current Windows case-sensitive/case-insensitive inventory selection was omitted and is not covered by the macOS deferral. |
| 8 — `_git` text decode | Explicit UTF-8 remains appropriate for the reviewed text/hex/no-output uses; path comparisons now use the strict raw helper. Text decoding does not fix ambiguous name resolution. |

The eight rows also need to account explicitly for the candidate SHA and side/container shape validations, the eligibility predicate applied to each path inventory, and the final resolution namespace of each caller-supplied ref. Shape validation was inspected and remains fail-closed for the reviewed incomplete/wrong-side inputs. The missing dimensions are inventory eligibility on the actual host and **which Git namespace/object a validated name resolves to**, not new bundle semantic choices.

The corrected `_closed` fixture supplies `ref: main` for positive closure; `_unrelated_main` makes actual orphan main branches without candidate ancestry. Therefore the existing acceptance negative tests ancestry rather than mere branch absence, and the positive tests a legitimate complete pair. These are correct controls. They need the additional same-named-tag negative; current branch existence alone does not make them exhaustive. Real WP-00 CLOSED and WP-P01 SCOPING states pass the deep gate at D/C; no actual tag collision or invalid real acceptance is asserted.

## Refined blocking findings

```yaml
- id: WPP01-CR-001
  title: Windows working and committed state inventories use different extension matching
  classification: CONTRACT_ASSURANCE_DEFECT
  blocking: true
  owner_decision_required: false
  sources:
    - "a9ed71d2f943c3fb5dc32f51fb7d5db99291abcb:process/tools/src/mneme_process/checks.py:853-881"
    - "a9ed71d2f943c3fb5dc32f51fb7d5db99291abcb:process/tools/src/mneme_process/checks.py:676-684"
    - "a9ed71d2f943c3fb5dc32f51fb7d5db99291abcb:process/coordination-state.md:132-140"
    - "a9ed71d2f943c3fb5dc32f51fb7d5db99291abcb:assurance/reviews/WP-P01-remediation-claude-2.md:24-37"
  requirements: []
  observation: "On Windows the working glob includes uppercase .YAML state files, but the committed inventory excludes them using case-sensitive endswith('.yaml'). A valid matching inventory is rejected, and an uncommitted deletion of that state is silently skipped."
  expected: "Both inventories must apply the same eligible-state definition. Every state file admitted by the working finder/validator must have a committed counterpart compared, including detection when its committed copy is deleted from the working tree."
  witness: "Build a clean World and assert all_errors() == {}. dump process/state/WP-UP.YAML using w.state(work_package='WP-UP'), then commit_all. On this Windows host glob('*.yaml') and raw ls-tree both return WP-T.yaml and WP-UP.YAML, and all_errors() remains {}, yet roundtrip reports WP-UP.YAML as uncommitted. Refresh and commit WP-T's candidate, then delete WP-UP.YAML without committing. roundtrip returns [], all_errors() returns {}, and git status reports D process/state/WP-UP.YAML."
  recommendation: "For the Owner escalation packet, include this current-host inventory witness. Apply one explicit eligibility rule to both committed and working paths, or enforce a canonical extension consistently instead of treating an admitted state as an uncommitted extra/ignoring its deletion. Add matching and missing uppercase-extension controls on Windows, retain case-sensitive-host coverage, and sweep glob/filter/case assumptions without case-folding distinct path identities."
- id: WPP01-CR-002
  title: Acceptance and descendant checks resolve bare names outside the checked branch namespace
  classification: CONTRACT_ASSURANCE_DEFECT
  blocking: true
  owner_decision_required: false
  sources:
    - "a9ed71d2f943c3fb5dc32f51fb7d5db99291abcb:process/tools/src/mneme_process/checks.py:687-720"
    - "a9ed71d2f943c3fb5dc32f51fb7d5db99291abcb:process/tools/src/mneme_process/checks.py:729-751"
    - "a9ed71d2f943c3fb5dc32f51fb7d5db99291abcb:process/tools/src/mneme_process/checks.py:860-887"
    - "a9ed71d2f943c3fb5dc32f51fb7d5db99291abcb:process/coordination-state.md:51-55"
    - "a9ed71d2f943c3fb5dc32f51fb7d5db99291abcb:process/coordination-state.md:101-115"
    - "a9ed71d2f943c3fb5dc32f51fb7d5db99291abcb:assurance/reviews/WP-P01-remediation-claude-2.md:24-37"
  requirements: []
  observation: "Branch existence is checked at refs/heads/<ref>, but later merge-base/rev-list use bare ref names, including bare main for CLOSED acceptance. Same-named tags can supply different objects and defeat the exact accepted-pair proof and active descendant check."
  expected: "All checks must resolve the same canonical branch identity that was validated. Acceptance means ancestry of refs/heads/main; a tag named main is not acceptance onto that branch. A same-named tag must not change the state-only range of a validated local branch."
  witness: "CLOSED: build a clean World; record both correctly bound candidates, APPROVED process review, no findings and null owner/action; set both refs main. Create unrelated orphan refs/heads/main in each repo. Aggregate reports non-acceptance. Add a lightweight tag main at each candidate; aggregate becomes {} while candidate ancestry of refs/heads/main remains exit 1 in both repos. Active: start another clean World; keep its original docs candidate, commit record.md on wp/test, observe the non-state-descendant rejection, then tag wp/test at the candidate. Aggregate becomes {}; qualified refs/heads/wp/test still exposes the descendant."
  recommendation: "For the Owner's escalation packet, record these two branch/tag collisions and the exact Git resolutions. Bind all branch operations to fully qualified refs/heads names or resolved commit IDs obtained from those qualified refs, including main acceptance and descendant ranges. Include roundtrip plain-name resolution in the same sweep. Preserve deliberate HEAD/full-SHA revision support and add collision negatives alongside the valid-branch/accepted-pair positives."
```

The flags remain false because the mechanical inventory/acceptance obligations are already determined; the required Owner escalation is a separate convergence/process route decision, not a new semantic uncertainty in these findings. No new finding numbers are needed: these refine the existing inventory and accepted-pair obligations with concrete eligibility/branch-identity witnesses.

## Fresh gates and known-bad replay

Every shell first dot-sourced the absolute project environment. Temp/cache/venv/target paths stayed inside the E: project. Venvs are `.tmp/cache/venvs/mneme-process-codex` and `.tmp/cache/venvs/minion-memory-python-codex`; scratch/backups/synthetic Worlds are under `.tmp/work/codex`; the new review worktree is under `review-worktrees`. Required gates ran sequentially against the actual candidate working trees. No implementation, Rust workspace, bundle edit, remote or push was made.

| Command | Fresh result |
|---|---|
| process/tools: `uv sync --python 3.12`; `uv run pytest` | passed; 145 passed in 284.25 s |
| `-k wpp01_r2` against old `cd828838` checks.py | 17 failed, 128 deselected in 55.41 s; expected exit 1 |
| Same selection after fixed checks.py restoration | 17 passed, 128 deselected in 61.25 s |
| `uv run ruff check src tests` | passed |
| `uv run ruff format --check src tests` | 11 files already formatted |
| `uv run mypy src` | no issues in 8 source files |
| `uv run mneme-process check --docs ../.. --code ../../../minion-memory --deep-sources` | 8/8 passed, including actual WP-00 CLOSED and WP-P01 SCOPING |
| `uv run mneme-process state roundtrip --docs ../..` | state ROUNDTRIP OK |
| minion-memory-python: `uv sync --python 3.12`; `uv run pytest` | passed; 2 passed, 6 xfailed in 0.17 s |

Scaffold xfails remain placeholders, not implementation certification. Passing real-state gates do not establish that the two adversarial inputs are rejected.

Independently executed the exact replay: save fixed `checks.py` bytes; substitute raw `git show cd828838:process/tools/src/mneme_process/checks.py` bytes; run:

```text
uv run pytest -o addopts="-p no:cacheprovider" -q -k wpp01_r2
```

Restored in a `finally` block, asserted exact byte equality, verified no real tooling diff, and reran the selection plus remaining gates. Inspected all 17 failure traces. Claude's count is correct: **10 discriminating failures, 7 diagnostic-only failures**. The wording that old tooling "accepted bad input" is too broad for the two positive controls: these discriminate incorrect rejection of legitimate non-ASCII inventory/state-only paths. This does not change the count.

| Group | Old-tooling evidence | Classification |
|---|---|---|
| Non-ASCII matching inventory, deletion, state-only path | false extra-file error; `[]` on deletion; quoted state path wrongly called non-state | 3 discriminating |
| Both-code, both-docs, swapped sides | aggregate `{}` at the intended state assertion | 3 discriminating |
| SHA ref, HEAD~0 ref, SHA-empty-range witness | aggregate `{}` at the intended state assertion | 3 discriminating |
| CLOSED ref other than main | aggregate `{}` at the intended state assertion | 1 discriminating |
| Option-like/range/nonexistent candidate refs | already rejected as unreachable/cannot-list; new diagnostic fragment absent | 3 diagnostic-only |
| Four bad roundtrip revisions | already rejected as cannot-list committed inventory; new diagnostic fragment absent | 4 diagnostic-only |

No import/API-absence failure is counted as a kill. Permanent fixture baselines pass before mutations. The actual orphan-main acceptance fixture and valid-main closure positive are correctly separated as discussed above.

Scratch reproducibility: `.tmp/work/codex/wpp01-closure2-controls.py`, `wpp01-closure2-known-bad.txt`, `wpp01-closure2-fixed.py`, `wpp01-closure2-neighborhood.py`, `wpp01-closure2-case-probe.py`, plus the prior `wpp01-closure1-neighborhood.py` rerun against D. The durable recipes above specify the branch/tag and Windows case witnesses without relying on scratch retention.

## Verdict and next coordination step

**CHANGES_REQUIRED** — WPP01-CR-001 and WPP01-CR-002 survive with the precise current-host inventory and branch/tag witnesses above. WP00-CR-014 remains provisionally closed at D/C. Characterization improved the trust boundary and the recorded route choice was adequate, but its inventory-eligibility and reference-identity safety premises are incomplete.

Per remediation §1 and the handoff escalation note, Claude must now stop ordinary remediation and route the surviving finding/route decision to the Owner. This review does not authorize another repair pass, acceptance under G-009, or a transition onto main. The actual accepted WP-00 pair remains valid; WP-P01 remains SCOPING. No WP-01 decision or work was performed. This branch adds only this record; its commit SHA is reported externally to avoid self-reference.
