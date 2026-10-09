# WP-00 targeted closure review 2 — Codex

Reviewer: Codex, independent reviewer, Rust implementation owner and cross-language challenger. Date: 2026-10-09. Task: targeted finding-closure review of remediation 2 under `process/handoffs/WP-00-codex-targeted-closure-2.md`. Claude's response record was a review object, not closure evidence. Python behavior was tooling evidence, not semantic authority.

## Exact candidate and preflight

The reviewed pair (C/D below) is:

- Code C: `bb05e3953a044ea8abd9d796675290ad9fe80941`.
- Docs content D: `237948fee550b691d0e83defb6c49186a27af3b8`.
- Both candidate refs: `wp00/bootstrap`.
- Docs control head and review-branch base: `3a92ef3ea460378aa611421ebb0645e6121bfd89`.
- Previous pair: code `139f81f9cee8201e96e69c093d3489c0ed3d36a4` / docs `c3e0d2ed15e116588a196d92e6ca36ce2750cda7`.
- Previous independent review: `1d8898e8f3c0173590ae9bb7265ae4e68f6fe51b`, `assurance/reviews/WP-00-targeted-closure-codex-1.md`.
- Bundle unchanged: `mneme-v2.3-dual-profile`, ZIP SHA-256 `9d999c1934e33b70100e884ed5cb60d0cbdb71150af59a8b2334604b4220251e`.
- Process pin unchanged: `minion-agent-docs` `8744bd019066f9c18d000c1a0ad19b435775300a`.
- Consumer pin unchanged: `minion-agent` `3de4b75d0119b6c413dae651a3cba039873756c7`.

Preflight passed: both objects exist and are reachable from the named refs; both trees were clean. Enumerated every commit in `D..wp00/bootstrap` and its per-parent diff-tree paths: the control commit changes only the current handoff and WP-00 state. WP-00 remains SCOPING with empty requirements. No handoff/environment failure occurred.

## Reading, scope and independent judgment

Read the complete docs and code diffs from the previous pair, the remediation and control state, every changed recommendation and gap statement, the new citation guard/fixture/controls, and the affected scope/serialization/uncertainty neighborhoods. Re-swept operative plans, spec, findings and process for preselected domain, version, hash, retry, scope and injection outcomes and approval being treated as acceptance authority. Historical handoffs and review records were not treated as operative instructions.

CR-002: the WP-01 surrogate risk now states the unresolved rejection/escape/representation options and requires Owner choice; governance YAML is explicitly not precedent for the payload domain. NF-008, NF-010–017 and NF-019 recommendations now agree with their flags/conditions and paths A/B/C. Scope and serialization gap statements route unanswered observable choices correctly. A per-store append position in NF-016 is representation mechanics asserting no semantic order, not a new total semantic order. Consumer-supplied cost functions in NF-017 do not prescribe a universal cost unit/tokenizer. I found no remaining preselection contrary to this mechanism in the reviewed operative neighborhood. Source-defined behavior remains an obligation, not an agent-created option.

CR-008: independently reopened the actual Foundation DOCX ZIP/XML, verified SHA-256 `f3352b902e7c6b5654c379254d464d55f519a7f933b823faf2576cf6f081b5d6`, and read G.3/G.7. The added G.7 citation supports the core/profile ownership boundary; the note preserves provisional vocabulary and identifies persistence namespacing as normative-unlabeled. The manifest row mirrors the citation. The prior manual review of all 49 FROZEN main statements remains applicable: only SCOPE-002 changed, and that change is faithful. No candidate requirement is justified solely by the new mechanical guard.

Regression judgment: the eleven previously closed repairs are preserved. Apart from the SCOPE-002 manifest citation, the code diff is empty. The docs changes affect recommendation/gap prose, citation validation and its fixture/tests, plus review/control artifacts. They do not alter checkpoint specialization, episode ordering, model-visible reconstruction, evaluation discipline, acceptance/closure/quarantine/chain rules, YAML syntax/domain rejection, Rust placeholder wording, or H5 inclusion. The full tool suite exercises the earlier executable controls again with the amended fixture baseline.

## Convergence trigger decision

Compared remediation section 1 with pinned process section 11.8, including its explicit exception at line 1027. The record correctly states that trigger A HAS fired for both findings, distinguishes finding-specific/root-surface/work-package triggers, and counts only one rejected complete review for trigger C. It gives a substantive, contemporaneously recorded reason for ordinary targeted repair: the remaining witnesses are a finite documentary surface, not unresolved semantic breadth. The neighborhood sweep and citation guard support that reason. SCOPING's lack of a legal direct convergence transition reinforces the chosen routing but is not used to deny the trigger.

The exception is adequate for this pass. The two findings are now provisionally closed, so there is no third surviving blocker that would require invoking the record's promised Owner-routing stop. The non-blocking guard limitation below does not turn a source-status check into domain authority or require further semantic convergence.

## Fresh gates and controls

Every shell first dot-sourced the absolute project environment. Venvs are `.tmp/cache/venvs/mneme-process-codex` and `.tmp/cache/venvs/minion-memory-python-codex`; scratch, backups and synthetic repositories are under `.tmp/work/codex`; temp/cache/target variables stay inside the E: project. No implementation, Cargo workspace, bundle edit, remote or push was made.

Ran sequentially:

| Command | Fresh result |
|---|---|
| process/tools: `uv sync --python 3.12` | passed |
| `uv run pytest` | 98 passed in 150.87 s |
| Citation control selection against old `c3e0d2ed` checks.py | 1 failed, 1 passed, 96 deselected in 5.99 s (expected nonzero exit) |
| Same selection after restoring fixed checks.py | 2 passed, 96 deselected in 8.83 s |
| `uv run ruff check src tests` | passed |
| `uv run ruff format --check src tests` | 11 files already formatted |
| `uv run mypy src` | no issues in 8 source files |
| `uv run mneme-process check --docs ../.. --code ../../../minion-memory --deep-sources` | 8/8 passed |
| minion-memory-python: `uv sync --python 3.12`; `uv run pytest` | passed; 2 passed, 6 xfailed in 0.45 s |

The scaffold xfails remain placeholders, not behavioral certification. Manifest/spec remain 224 rows/requirements. The earlier CR-002 escalation, closure, quarantine, YAML, chain, surrogate and malformed-status regression controls pass in the full 98-test suite; their old-tooling discrimination was established in review 1 of targeted closure and is not claimed as a newly replayed old-tooling run here.

Executed the exact new control recipe independently: save fixed `checks.py` bytes; substitute `git show c3e0d2ed:process/tools/src/mneme_process/checks.py`; run:

```text
uv run pytest -o addopts="-p no:cacheprovider" -q -k cr008
```

Restored in a `finally` block, asserted byte equality, confirmed no real tooling diff, and reran the selection plus remaining gates. The permanent World fixture proves an unmutated baseline before either control; fixture DOC section 1 now has a positive FROZEN label. On old tooling the negative control fails at its intended assertion (`spec did not fail`), not setup/import failure. Its spec-only citation mutation also produces an unrelated manifest mismatch, so this control demonstrates the new **spec check**, not an old whole-pipeline false pass. The fixed spec check reports the intended missing-labelled-citation error.

The permanent positive control passes on both versions. Because its NORMATIVE requirement also cites labelled section 1, I additionally tested a NORMATIVE requirement citing **only** unlabelled section 2, updating the synthetic manifest and committing a valid content/state pair; all checks pass. This confirms that the guard does not require FROZEN support for NORMATIVE metadata.

Additional scope probe: in two clean synthetic Worlds, replace section 1's positive label with `NOT FROZEN` or `This section discusses a FROZEN decision elsewhere.`, regenerate source hash/derived text/index, and commit a valid content/state pair. The fixed spec check returns `[]` and aggregate returns `{}` in both. This characterizes the guard's lexical limit, recorded below. Each baseline passed before mutation. No real authority bundle was modified.

Scratch reproducibility files: `.tmp/work/codex/closure2-controls.py`, `closure2-known-bad-output.txt`, and `closure2-label-probe.py`. The recipes/results above are durable evidence independent of keeping that scratch.

## Per-finding disposition

Every entry below means **PROVISIONALLY CLOSED @ `bb05e3953a044ea8abd9d796675290ad9fe80941` / `237948fee550b691d0e83defb6c49186a27af3b8`**. These are review judgments at C/D, not certification-state edits.

| Finding | Disposition | Verified evidence |
|---|---|---|
| WP00-CR-001 | PROVISIONALLY CLOSED @ C/D | Acceptance-authority separation unchanged; operative process still requires Owner decision/delegation. |
| WP00-CR-002 | PROVISIONALLY CLOSED @ C/D | Refined surrogate witness repaired; ten recommendations and two gap statements align with A/B/C. Escalation validator and regression control remain green. |
| WP00-CR-003 | PROVISIONALLY CLOSED @ C/D | Closure rules/implementation unchanged; seven negative controls and valid scoping-closure positive control pass. |
| WP00-CR-004 | PROVISIONALLY CLOSED @ C/D | Both-agent quarantine guard unchanged; Claude/Codex and Owner positive regression controls pass. Earlier Codex diagnostic-only kill is not reclassified as behavioral evidence. |
| WP00-CR-005 | PROVISIONALLY CLOSED @ C/D | YAML loader unchanged; redundant explicit-tag/unused-anchor unit and scenario controls and portable-domain regressions pass. |
| WP00-CR-006 | PROVISIONALLY CLOSED @ C/D | Profile-neutral PERS-009 and learner-specific LMEM-015 unchanged; no learner fitting fields reintroduced into agent core. |
| WP00-CR-007 | PROVISIONALLY CLOSED @ C/D | Episode-only HIST-003/profile/layer mapping unchanged; NF-016 continues to distinguish non-semantic append position. |
| WP00-CR-008 | PROVISIONALLY CLOSED @ C/D | G.7 citation and boundary note verified against actual Foundation; manifest agrees. Necessary lexical guard catches absent-support case in its intended spec assertion. Manual status judgment remains required; guard hardening below is non-blocking. |
| WP00-CR-009 | PROVISIONALLY CLOSED @ C/D | Unqualified model-visible reconstruction obligation unchanged; no materiality exemption reintroduced. |
| WP00-CR-010 | PROVISIONALLY CLOSED @ C/D | LMEM-014 evaluation discipline and modal-strength/MVP-deferral note unchanged. |
| WP00-CR-011 | PROVISIONALLY CLOSED @ C/D | Per-commit descendant checker unchanged; change/revert negative and legitimate multi-commit positive controls pass; actual control-chain preflight passes. |
| WP00-CR-012 | PROVISIONALLY CLOSED @ C/D | Ownership README versus absent Cargo workspace wording unchanged; no Rust implementation added. |
| WP00-CR-013 | PROVISIONALLY CLOSED @ C/D | H5 remains explicitly included in the WP-01 feasibility checklist. |

Documentary findings have exact text/source comparisons rather than executable negative controls. Previously validated documentary neighborhoods were checked for delta regression, not re-reviewed as unrelated surface.

## New non-blocking finding

```yaml
- id: WP00-CR-014
  title: FROZEN citation prefilter matches mentions as well as positive status labels
  classification: SEMANTICS_NEUTRAL_HARDENING
  blocking: false
  owner_decision_required: false
  sources:
    - "237948fee550b691d0e83defb6c49186a27af3b8:process/tools/src/mneme_process/checks.py:347-385"
    - "237948fee550b691d0e83defb6c49186a27af3b8:process/tools/tests/test_negative_controls.py:346-364"
    - "237948fee550b691d0e83defb6c49186a27af3b8:spec/README.md:60-66"
  requirements: []
  observation: "The helper describes FROZEN-labelled sections but implements a word-presence regex anywhere in the section; negation and ordinary mentions qualify."
  expected: "Document the check as a lexical prefilter, or distinguish a positive source-status label from negation and prose mentions. Independent reviewers must still check the label's scope against the main statement."
  witness: "In clean synthetic Worlds, replace the only positive DOC section 1 label with NOT FROZEN or an ordinary sentence mentioning a FROZEN decision elsewhere, regenerate hashes/text/index and commit a valid candidate/state pair. check_spec returns [] and all_errors returns {} in both; the FROZEN requirement still cites that section."
  recommendation: "Clarify the guard's actual guarantee or recognize positive status forms and add negated/mention-only controls. Also make the permanent NORMATIVE positive control cite only an unlabelled section; the independent probe confirms that behavior already works."
```

This is non-blocking because the guard is explicitly supplementary and insufficient for source-status judgment, the current 49 FROZEN main statements have independent source review, and the surviving actual citation defect is repaired. I do not treat a lexical pass as evidence that a requirement is frozen. Strengthening the prefilter or its documentation preserves the reviewed contract; there is no unresolved domain choice here.

## Verdict and next coordination step

**APPROVED** — all WP00-CR-001–013 are provisionally closed at C/D; no new blocker remains. This exact pair is the approved WP-00 scoping artifact. WP00-CR-014 remains open as non-blocking hardening; future-layer NF/domain/governance decisions remain open at their recorded boundaries.

Claude should record this exact-pair approval and provisional closures, retain the non-blocking finding, and route acceptance to the Owner with the exact C/D SHAs. This approval never grants authority to advance main, certify implementation, or start WP-01. Acceptance and any subsequent work need their existing governance/process conditions. I made no coordination-state edits and no acceptance transition. This review branch adds only this record; its commit SHA is supplied externally to avoid self-reference.
