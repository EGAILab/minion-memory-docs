# WP-P01 targeted closure review 1 — Codex

Reviewer: Codex, independent reviewer, Rust implementation owner and cross-language challenger. Date: 2026-10-10. Task: TARGETED_FINDING_REVIEW under `process/handoffs/WP-P01-codex-targeted-closure-1.md`. Claude's remediation record is a review object, not evidence of closure.

## Exact candidate and preflight

- Docs D: `cd8288384473ab32472629fbbc7e37d5ec2cbf26`, reachable from `wpP01/hardening`.
- Code C: `bb05e3953a044ea8abd9d796675290ad9fe80941`, actual code `main`, unchanged.
- Docs control head/review-branch base: `814b789de88aed27613a019f04512f1311c9ecd5`.
- Previous reviewed docs: `ba1217f76ef311f3ba0df749e43291b75fb2e0b4`, same code.
- Previous review: `assurance/reviews/WP-P01-review-codex-1.md` at `719efb9b3c1ad4fb55ad6bfa4b689be50171b214`.
- Actual docs main remains `237948fee550b691d0e83defb6c49186a27af3b8`; governance G-008–G-011 remains unchanged.

Preflight passed: both objects exist; candidate reachability is correct; both main working trees were clean. Enumerated every commit in `D..wpP01/hardening`: the sole control commit changes only the current handoff and WP-P01 state. The handoff/environment is valid. Read the complete previous-candidate-to-D diff, the response record, state, changed validation/tests and applicable coordination/exact-pair rules.

The main docs working tree stayed on `wpP01/hardening`. This record is created on new branch `review/wpP01-codex-2` in separate E:-contained worktree `review-worktrees/docs-wpp01-codex2`, based on the control head. Claude's `review-worktrees/docs-wp01` and its uncommitted Owner-decision record were not inspected or changed. No WP-01 work was done.

## Per-finding disposition and neighborhoods

### WPP01-CR-001 — OPEN, refined inventory witness

The original ASCII deletion witness is caught: after committing two states and deleting one without committing, roundtrip reports the missing committed state. Extra working states are rejected; committing a legitimate deletion with another state remaining passes. The permanent tests substantiate these cases.

However, the new inventory uses human-readable `git ls-tree --name-only` output, then splits lines and filters names ending in `.yaml`. With the normal `core.quotePath=true`, a committed `WP-Ü.yaml` is emitted as `"WP-\303\234.yaml"`. The closing quote makes it fail the suffix filter. A matching working file is falsely called uncommitted; deleting it makes the inventory comparison silently overlook the committed state and return success. This is a concrete surviving path in the explicitly requested inventory neighborhood, not a restatement of the original ASCII witness.

The independent World baseline passes all checks before mutation. The scratch recipe also refreshes the remaining ASCII state's candidate after the Unicode-state commit, so the inherited descendant-path parser is not a competing cause of rejection after deletion. At that point deletion produces `state_roundtrip == []` and `all_errors == {}`; the CLI prints `state ROUNDTRIP OK` and exits 0, while Git reports the uncommitted deletion. No authority bundle or real state was modified.

### WPP01-CR-002 — OPEN, refined repository-identity witness

The original missing/empty/null/partial records now fail. Both side records must contain SHA-shaped values; existing reference/object checks still reject missing objects and unaccepted populated candidates. The real WP-00 CLOSED state retains both correct records and passes. Legitimate active/pre-candidate state permissiveness was not removed by the CLOSED-specific completeness check.

But completeness does not bind a side to its repository. `check_state` resolves each repository using the record's `repo` value and accepts either repo name for either side. Copying the accepted code record into both `code` and `docs` satisfies the new completeness condition and checks code/main twice; no docs acceptance is checked. In an independent clean World with later unaccepted docs content and no docs main, a CLOSED state with both sides pointing to accepted code returns `all_errors == {}`. The immediately preceding null-docs variant correctly fails. This exposes incomplete enforcement of the same exact accepted pair obligation.

### WP00-CR-014 — regression judgment

**PROVISIONALLY CLOSED @ D/C**, preserving the judgment at `ba1217f7` / C. No positive-label predicate, source-section slicing, spec statement, manifest citation or guard documentation changed in this remediation. The full suite re-exercises the positive-label units, three repository negatives, both positive forms and NORMATIVE-only case. The prior independent source review of all 49 FROZEN main statements remains applicable; no fresh source-status semantic judgment is inferred from a mechanical test pass.

UTF-8 blob decoding, CRLF/LF-only normalization and semantic equality are unchanged and re-exercised. The CLOSED exemption still works for correctly populated accepted pairs and still rejects an active non-state descendant. Post-acceptance record/governance accuracy from the complete review is unchanged. Neither surviving witness invalidates the real Owner-accepted WP-00 pair; both concern validation of other purported evidence.

## Refined finding records

```yaml
- id: WPP01-CR-001
  title: Quoted Git filenames are omitted from the committed state inventory
  classification: CONTRACT_ASSURANCE_DEFECT
  blocking: true
  owner_decision_required: false
  sources:
    - "cd8288384473ab32472629fbbc7e37d5ec2cbf26:process/tools/src/mneme_process/checks.py:803-830"
    - "cd8288384473ab32472629fbbc7e37d5ec2cbf26:process/tools/src/mneme_process/checks.py:116-131"
    - "cd8288384473ab32472629fbbc7e37d5ec2cbf26:process/coordination-state.md:117-135"
  requirements: []
  observation: "The committed inventory consumes Git's quoted display names as literal names, then drops quoted .yaml entries because they end with a quote. A committed non-ASCII state can be silently skipped after deletion, and a matching working state is falsely reported as extra."
  expected: "Committed and working inventories must compare actual path identities losslessly, independent of Git display quoting. Missing committed state objects must fail; matching committed/working objects must pass."
  witness: "Build a permanent World and assert all_errors() == {}. Verify the repaired ASCII deletion and committed-deletion cases. Commit a second state WP-Ü.yaml, set synthetic-repo core.quotePath=true (the usual default), and inspect ls-tree --name-only HEAD:process/state: it emits WP-T.yaml and a quoted WP-\\303\\234.yaml. roundtrip falsely calls the matching WP-Ü.yaml uncommitted. Refresh and commit the remaining WP-T state's candidate, then delete only WP-Ü.yaml without committing. roundtrip returns [] and all_errors() returns {}, while git status reports the deletion."
  recommendation: "Read machine-oriented Git path output losslessly, preferably NUL-delimited raw path bytes with explicit UTF-8 decoding rather than quoted line display output. Add non-ASCII matching-inventory and uncommitted-deletion controls under core.quotePath=true, and sweep inventory name handling for other display transformations. Preserve the committed-deletion positive."
- id: WPP01-CR-002
  title: Complete CLOSED records can identify the code repository for both sides
  classification: CONTRACT_ASSURANCE_DEFECT
  blocking: true
  owner_decision_required: false
  sources:
    - "cd8288384473ab32472629fbbc7e37d5ec2cbf26:process/tools/src/mneme_process/checks.py:561-579"
    - "cd8288384473ab32472629fbbc7e37d5ec2cbf26:process/tools/src/mneme_process/checks.py:637-672"
    - "cd8288384473ab32472629fbbc7e37d5ec2cbf26:process/coordination-state.md:67-71"
    - "cd8288384473ab32472629fbbc7e37d5ec2cbf26:process/coordination-state.md:101-109"
    - "cd8288384473ab32472629fbbc7e37d5ec2cbf26:process/agent-workflow.md:119-122"
  requirements: []
  observation: "The new CLOSED completeness guard checks both side keys and SHA shapes, but side.repo is not bound to that side. check_state selects a repository using the untrusted record value, allowing code and docs records to both prove only code acceptance."
  expected: "The exact accepted pair identifies code in minion-memory and docs in minion-memory-docs, and each side's object/reachability/main checks run against its own repository. A populated record for the wrong repository cannot substitute for missing docs acceptance evidence."
  witness: "Build a clean permanent World and assert all_errors() == {}. Commit later unaccepted docs content, create only code main, and obtain the accepted code record with ref main. Write a valid CLOSED process-only state with exact APPROVED review evidence, no findings and null owner/action. A docs-null record is now caught. Replace docs-null with a copy of the accepted code record, leaving both side keys populated with 40-hex SHA records. all_errors() returns {} although docs has no main."
  recommendation: "Bind candidate sides to their canonical repositories before resolving objects, refs or acceptance ancestry; reject copied/swapped/wrong-side repository records. Add both-code, both-docs and swapped-side negatives plus the correct accepted-pair positive, and sweep active-state repository binding so descendant checks cannot be redirected either."
```

Both remain mechanical `CONTRACT_ASSURANCE_DEFECT` findings with no unresolved Owner semantic choice. CR-002's repository-selection permissiveness is inherited; this review does not claim it was newly introduced. It directly defeats the remediation's claimed accepted-pair protection.

## Fresh gates and known-bad replay

Every shell first dot-sourced the absolute project environment. Temp/cache/venv/target paths stayed inside the E: project; venvs are `.tmp/cache/venvs/mneme-process-codex` and `.tmp/cache/venvs/minion-memory-python-codex`. Scratch, backups and synthetic repositories are under `.tmp/work/codex`. Required gates ran sequentially against the actual candidate working trees. No implementation, Rust workspace, bundle edit, remote or push was made.

| Command | Fresh result |
|---|---|
| process/tools: `uv sync --python 3.12`; `uv run pytest` | passed; 128 passed in 232.30 s |
| `-k wpp01` against old `ba1217f7` checks.py | 6 failed, 1 passed, 121 deselected in 25.37 s; expected exit 1 |
| Same selection after fixed checks.py restoration | 7 passed, 121 deselected in 29.36 s |
| `uv run ruff check src tests` | passed |
| `uv run ruff format --check src tests` | 11 files already formatted |
| `uv run mypy src` | no issues in 8 source files |
| `uv run mneme-process check --docs ../.. --code ../../../minion-memory --deep-sources` | 8/8 passed, including real WP-00 CLOSED state |
| `uv run mneme-process state roundtrip --docs ../..` | state ROUNDTRIP OK |
| minion-memory-python: `uv sync --python 3.12`; `uv run pytest` | passed; 2 passed, 6 xfailed in 0.17 s |

The scaffold xfails remain placeholders, not implementation certification. A passing real-state roundtrip is not evidence that arbitrary committed path inventories are compared correctly.

Replayed the exact recipe independently: save fixed `checks.py` bytes, substitute raw `git show ba1217f7:process/tools/src/mneme_process/checks.py` bytes, run:

```text
uv run pytest -o addopts="-p no:cacheprovider" -q -k wpp01
```

Restored in a `finally` block, asserted byte equality, and reran the selection and remaining gates. Inspection of actual old-tooling traces confirms Claude's classification: the deletion test fails with `errors == []`; the four incomplete-pair cases fail at `state did not fail; failures: {}` after the valid fixture baseline. These are five discriminating kills. The extra-state case already returns `WP-NEW.yaml: not present in HEAD` on old tooling and fails solely because the expected message fragment changed; it is diagnostic regression coverage, not a sixth behavioral kill. The committed-deletion positive passes on both. There are no missing-API or import failures in this replay.

Reproducibility scratch: `.tmp/work/codex/wpp01-closure1-controls.py`, `wpp01-closure1-known-bad.txt`, `wpp01-closure1-fixed.py`, and `wpp01-closure1-neighborhood.py`. The durable finding recipes above specify the new probes independently of retaining scratch. The initial exploratory Unicode probe also exposed the inherited quoted-path descendant diagnostic; the refined recipe refreshes the remaining state's docs candidate to isolate the inventory false pass and obtains aggregate `{}`.

## Convergence and verdict

Claude's response correctly checked triggers before this remediation: at that time neither finding had survived two reviews and only one complete WP-P01 review had been rejected. At this review's outcome both material findings remain open for a second independent review: **trigger A HAS fired** for both. This is not a second rejected complete contract review, and no two differently numbered successor findings are being asserted for trigger B.

Before another ordinary remediation pass, Claude must perform the adopted §11.8 trigger check and choose the permitted route. Convergence is the default when triggered; an ordinary targeted repair requires a contemporaneous substantive reason. The narrowed witnesses concern machine path identity and repository-side binding, so such a reason may be supportable, but it is Claude's next recorded coordination decision, not supplied retroactively by this review. SCOPING does not acquire an unauthorized direct convergence transition.

**CHANGES_REQUIRED** — WPP01-CR-001 and WPP01-CR-002 remain open with refined discriminating witnesses. WP00-CR-014 remains provisionally closed at D/C. This exact candidate has no independent approval for acceptance under G-009; WP-P01 remains SCOPING. Claude should independently reproduce the refined witnesses, check the convergence triggers, and hand off the next exact candidate after repairing/sweeping these neighborhoods. WP-00 acceptance remains valid; no WP-01 work or product certification is authorized by this review.

This branch adds only this review record. The commit SHA is supplied externally to avoid self-reference; no coordination-state edit or acceptance transition was made.
