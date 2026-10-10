# WP-P01 independent review — Codex

Reviewer: Codex, independent reviewer, Rust implementation owner and cross-language challenger. Date: 2026-10-10. Task: complete independent SCOPING_REVIEW of process-only WP-P01 under `process/handoffs/WP-P01-codex-review.md`. Claude's plan and gate observations are review objects, not closure evidence. No product implementation or Layer-01 decision is authorized by this review.

## Exact candidate and preflight

- Code C: `bb05e3953a044ea8abd9d796675290ad9fe80941`, actual code `main`, unchanged.
- Docs content D: `ba1217f76ef311f3ba0df749e43291b75fb2e0b4`, reachable from `wpP01/hardening`.
- Docs control head and new review-branch base: `06f9594c1d6f3019ce303e9fd25f09f2733c29d8`.
- Docs actual `main`: `237948fee550b691d0e83defb6c49186a27af3b8`.
- WP-P01 change base: `21fcb416d90d6544a94ad61c3ebe4e43362b1546`.
- Governance: `reference/governance/2026-10-10-owner-wp00-acceptance.md`, G-008–G-011.
- Bundle: unchanged `mneme-v2.3-dual-profile`; process pin `8744bd019066f9c18d000c1a0ad19b435775300a` (`minion-agent-docs`), consumer pin `3de4b75d0119b6c413dae651a3cba039873756c7` (`minion-agent`).

Preflight passed: objects exist; candidate reachability is correct; both trees were clean. Enumerated every commit in `D..wpP01/hardening`: only the handoff and WP-P01 state change. Reviewed the complete `237948fe..D` diff and the specific `21fcb416..D` diff. The handoff/environment is valid. WP-P01 remains SCOPING with empty requirements; WP-00 is accepted and CLOSED. G-009 delegates routine acceptance only for an independently approved exact pair with no blockers; it does not supply missing review or acceptance evidence.

## Scope judgments

### Positive-label guard / WP00-CR-014

**WP00-CR-014: PROVISIONALLY CLOSED @ C/D.** `has_positive_frozen_label` recognizes the actual positive status forms: exact/start-of-cell `FROZEN`, scoped boundary cells, and a line beginning `FROZEN —` (also its hyphen spelling). It rejects negation, prose/cell mentions and ASCII `->` change records. Escaped Markdown pipes do not split a cell. The three permanent repository negatives discriminate the repair on old tooling; both positive forms and the NORMATIVE-only unlabelled citation pass. The eleven unit cases pass on fixed tooling.

Rechecked the actual indexed Foundation sections and iterated all 49 FROZEN requirements against their cited positive sections. Every current requirement retains legitimate positive supporting anchors; none is justified solely by a legend or Appendix E change record. The previous independent main-statement/source review remains applicable because product/spec main statements did not change. The raw Foundation DOCX SHA-256 remains `f3352b902e7c6b5654c379254d464d55f519a7f933b823faf2576cf6f081b5d6`. A scoped FROZEN principle remains scoped; adjacent normative/unlabelled detail is not thereby promoted. `spec/README.md` §3 accurately states that the guard is necessary, not sufficient: a label's substantive scope and modal strength still require independent judgment.

### UTF-8 state round trip

Raw git blob bytes are decoded strictly as UTF-8 for roundtrip; both sides use the same YAML-core loader and semantic comparison. `_git` now explicitly decodes UTF-8 rather than the platform code page. Physical CRLF/LF normalization is sound for the reviewed portable YAML domain and checkout rule; it does not weaken escaped string-value equality. An independent committed `updated_reason` containing actual CRLF versus a working value containing LF produces both byte and semantic errors. Existing-file uncommitted-change, non-ASCII and CRLF-only controls pass.

The command nevertheless overlooks a deleted committed state file while another state file remains. This is WPP01-CR-001 below. The actual candidate passes roundtrip; that does not establish the guard's completeness.

### CLOSED exemption and acceptance

For populated candidate records, the intended behavior works: CLOSED with no `main` ancestry fails on both candidate sides; establishing both synthetic main refs makes it pass. Active SCOPING still rejects a non-state descendant even when its named docs candidate has already reached main. CLOSED post-acceptance records are legitimately exempt from the active descendant restriction.

However, acceptance checking iterates optional candidate entries. CLOSED with an empty candidate mapping, or with accepted code but null docs, passes all checks despite absent main acceptance evidence. This permissiveness predates this change, but it is a concrete dependency of the new exemption's stated safety premise and is explicitly in scope for this review. WPP01-CR-002 records it. The actual WP-00 CLOSED state supplies both accepted SHAs and is accurate; the witness does not invalidate the Owner's acceptance.

### Post-acceptance record landing

The docs chain from accepted main is linear, with single-parent commits:

```text
237948fe -> 3a92ef3e -> b089a59d -> fadf767b -> 92dc2871 -> 21fcb416 -> ba1217f7
```

These land the scoping approval state, original Codex review, Owner governance record, WP-00 closure/WP-P01 opening, and process hardening. The landed review record is byte-identical to the original `4293b797da7f3334bf4f630b46f19bb55f89efa8` record (SHA-256 `924907279371a2b91d25cfb42b7bc1d3c9187419ab74416a01f80cf9a117f862`). Future acceptance would fast-forward docs main over these records, as the plan says; it has not happened at review time.

G-008 accepts the independently approved pair; G-009 records standing routine delegation with its exclusions; G-010 preserves the registry split; G-011 closes WP-00 and carries CR-014 into WP-P01 and unresolved NF items to their owning layers. NF-003/006/020/021 closures correspond to their recorded taxonomy/priority/governance decisions. The registry records contract acceptance while Python/Rust remain NOT_IMPLEMENTED and cross-language NOT_CLOSED. No record grants implementation certification or resolves the open Layer-01 semantic choices. These records are accurate against their sources; I did not treat them as new decisions to make.

## Fresh gates and independent known-bad replay

Every shell first dot-sourced the absolute project environment. Venvs are `.tmp/cache/venvs/mneme-process-codex` and `.tmp/cache/venvs/minion-memory-python-codex`; scratch, backups and synthetic repositories are under `.tmp/work/codex`. Temp/cache/target paths remain inside the E: project. No Rust workspace, bundle edit, remote, push or implementation was made.

Required gates ran sequentially:

| Command | Fresh result |
|---|---|
| process/tools: `uv sync --python 3.12`; `uv run pytest` | passed; 121 passed in 348.15 s |
| Known-bad selected tests, `237948fe` checks.py | 19 failed, 4 passed, 98 deselected in 73.67 s; expected exit 1 |
| Same selection with fixed checks.py restored | 23 passed, 98 deselected in 123.13 s |
| `uv run ruff check src tests` | passed |
| `uv run ruff format --check src tests` | 11 files already formatted |
| `uv run mypy src` | no issues in 8 source files |
| `uv run mneme-process check --docs ../.. --code ../../../minion-memory --deep-sources` | 8/8 passed |
| `uv run mneme-process state roundtrip --docs ../..` | state ROUNDTRIP OK |
| minion-memory-python: `uv sync --python 3.12`; `uv run pytest` | passed; 2 passed, 6 xfailed in 1.42 s |

Scaffold xfails are placeholders, not behavioral certification. Manifest/spec remain 224 requirements/rows; all 49 FROZEN requirements pass the new necessary prefilter.

Independently saved fixed `checks.py` bytes, substituted the raw bytes of `git show 237948fe:process/tools/src/mneme_process/checks.py`, ran the following selection, and restored in a `finally` block with byte-equality assertion and clean real tooling tree verification:

```text
uv run pytest -o addopts="-p no:cacheprovider" -q -k "cr014 or positive_frozen_label_rule or roundtrip or closed_state_allows_post_acceptance or open_state_still_enforces_chain"
```

Inspection of the actual failure traces confirms Claude's classification:

| Group | Old / fixed | Judgment |
|---|---|---|
| Three CR-014 repository negatives | fail / pass | Discriminating: old spec check does not reject the non-label source; failure is at the intended assertion after clean baseline. |
| CLOSED post-acceptance positive | fail / pass | Discriminating: old state checker rejects the legitimate post-acceptance record as non-state content. |
| Eleven positive-label units | fail / pass | Feature absent: missing helper ImportError. Not semantic control kills. |
| Four roundtrip tests | fail / pass | Feature absent: missing function AttributeError. Not semantic control kills. |
| Two positive label forms, NORMATIVE-only, active-state chain negative | pass / pass | Compatibility controls, not repair discrimination. |

Thus 4 discriminating failures, 15 feature-absent failures, and 4 passes on both; no setup/API absence is credited as behavioral closure evidence. The roundtrip tests discriminate working-tree mutations on fixed tooling, but cannot establish old-tooling regression discrimination when the old feature does not exist.

Scratch recipes: `.tmp/work/codex/wpp01-controls.py`, `wpp01-known-bad-output.txt`, `wpp01-neighborhood.py`, and `wpp01-acceptance-probe.py`. The durable descriptions below reproduce the adversarial witnesses using the permanent `World` fixture without depending on retaining scratch output.

## Blocking findings

```yaml
- id: WPP01-CR-001
  title: State roundtrip silently omits a deleted committed state file
  classification: CONTRACT_ASSURANCE_DEFECT
  blocking: true
  owner_decision_required: false
  sources:
    - "ba1217f76ef311f3ba0df749e43291b75fb2e0b4:process/tools/src/mneme_process/checks.py:789-827"
    - "ba1217f76ef311f3ba0df749e43291b75fb2e0b4:process/tools/src/mneme_process/cli.py:98-103"
    - "ba1217f76ef311f3ba0df749e43291b75fb2e0b4:process/coordination-state.md:115-130"
  requirements: []
  observation: "The roundtrip command enumerates only currently existing working-tree *.yaml files, so a committed state deleted from the working tree is never compared when another state file remains. It reports success for inconsistent committed/intended state inventories."
  expected: "The step-4 gate must not report that state roundtrip succeeded when a requested committed state has no corresponding intended working-tree object. Any non-checkout difference must prevent dependent action."
  witness: "Build a clean permanent World and assert all_errors() == {}. Add process/state/WP-OTHER.yaml with dump(other, w.state(work_package='WP-OTHER')), commit_all, and assert all_errors() == {} and state_roundtrip(w.docs) == []. Delete only WP-OTHER.yaml without committing. state_roundtrip(w.docs) still returns []; cli.main(['state','roundtrip','--docs',str(w.docs)]) prints state ROUNDTRIP OK and returns 0, while git status --porcelain reports D process/state/WP-OTHER.yaml. The other committed state remains unchanged."
  recommendation: "Compare the committed and working-tree state inventories, then validate matching files; reject missing/deleted and extra/uncommitted state objects. Alternatively require explicit target states and reject missing targets, rather than silently dropping them. Add a multi-state deletion negative and a legitimate committed-deletion positive so inventory agreement is enforced without banning valid deletion."
- id: WPP01-CR-002
  title: CLOSED can omit candidate records and bypass the acceptance premise
  classification: CONTRACT_ASSURANCE_DEFECT
  blocking: true
  owner_decision_required: false
  sources:
    - "ba1217f76ef311f3ba0df749e43291b75fb2e0b4:process/tools/src/mneme_process/checks.py:561-592"
    - "ba1217f76ef311f3ba0df749e43291b75fb2e0b4:process/tools/src/mneme_process/checks.py:624-663"
    - "ba1217f76ef311f3ba0df749e43291b75fb2e0b4:process/coordination-state.md:51-55"
    - "ba1217f76ef311f3ba0df749e43291b75fb2e0b4:process/coordination-state.md:101-107"
    - "ba1217f76ef311f3ba0df749e43291b75fb2e0b4:process/agent-workflow.md:119-122"
  requirements: []
  observation: "validate_state permits absent/empty/null candidate records even for CLOSED, and check_state checks main ancestry only for populated entries. The CLOSED exemption therefore lacks its claimed acceptance protection when records are omitted."
  expected: "Closing an exact-pair scoping/process WP requires identifying the accepted artifacts and checking their acceptance evidence. Missing evidence must fail closed; an APPROVED token alone cannot substitute for the accepted pair."
  witness: "Build a clean permanent World and assert all_errors() == {}. Commit record.md as later non-state content. The ordinary active state correctly fails its state-only descendant rule. Write status CLOSED, requirements [], open_findings [], null next_owner/next_action, scoping_review {outcome: APPROVED, verdict: APPROVED, source: assurance/reviews/x.md}, and current_candidate {}. all_errors() returns {} although neither repository has main. A second variant creates only code main and supplies current_candidate {code: accepted-code-record, docs: null}; all_errors() again returns {} while docs has no main and the later docs content remains unaccepted."
  recommendation: "Require the applicable exact accepted candidate records before granting CLOSED and its descendant exemption; for the current two-repository exact-pair workflow, reject absent, empty or null candidate sides and then check both main ancestries. Add missing/empty/null/partial CLOSED negatives alongside the accepted-pair positive and active-chain negative. Preserve any legitimate pre-candidate states without applying that permissiveness to closure."
```

Both findings concern mechanical enforcement of existing process obligations, not unresolved Owner domain choices. CR-002 is an inherited permissiveness exposed in the changed CLOSED acceptance neighborhood; it is not claimed to be introduced by WP-P01. Neither witness changes the real coordination state, accepted main, source bundle, or product contract.

## Verdict and next coordination step

**CHANGES_REQUIRED** — WP00-CR-014 is provisionally closed at C/D, but WPP01-CR-001 and WPP01-CR-002 are open blockers. The positive-label change, UTF-8 decoding/line-ending treatment, normal populated-candidate CLOSED behavior, linear record landing, and replay classification pass their reviewed checks; the two missing-evidence paths need repair.

Claude should independently reproduce/classify these witnesses, repair the guard neighborhoods, and hand off a new exact candidate for independent review. WP-P01 remains SCOPING; this candidate has no approval for routine acceptance under G-009. WP-00's Owner acceptance/closure remains valid. No WP-01 work is authorized. This review branch adds only this record; its commit SHA is reported externally to avoid self-reference.
