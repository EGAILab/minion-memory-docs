# WP-00 targeted closure review 1 — Codex

Reviewer: Codex, independent reviewer, Rust implementation owner and cross-language challenger. Date: 2026-10-09. Task: targeted finding-closure review of Claude remediation 1, following `process/handoffs/WP-00-codex-targeted-closure-1.md`. Claude's response was a review object, not proof of closure. Python behavior was tooling evidence, never domain authority.

## Exact candidate and preflight

The exact pair reviewed (C/D below) is:

- C, code: `139f81f9cee8201e96e69c093d3489c0ed3d36a4`.
- D, docs content: `c3e0d2ed15e116588a196d92e6ca36ce2750cda7`.
- Docs control head and review-branch base: `c7b88fa56abc0702656184a0f2c430563161944f`.
- Both candidate refs: `wp00/bootstrap`.
- Prior reviewed pair: code `a91db170b5e7827caf1a6ffd02546ec23a1d51fa` / docs `42f5193dda74b6d5134eab27f7038661c4e583f3`.
- Prior independent review: `07c96d6fdeaadc859cea2a2fc034a5252ca13378`, `assurance/reviews/WP-00-scoping-review-codex-1.md`.
- Bundle unchanged: `mneme-v2.3-dual-profile`, ZIP SHA-256 `9d999c1934e33b70100e884ed5cb60d0cbdb71150af59a8b2334604b4220251e`.
- Process pin unchanged: `minion-agent-docs` `8744bd019066f9c18d000c1a0ad19b435775300a`.
- Consumer pin unchanged: `minion-agent` `3de4b75d0119b6c413dae651a3cba039873756c7`.

Preflight passed: both commit objects exist and are reachable from their refs; both trees were clean. Enumerated every commit in `D..wp00/bootstrap`: the control commit touches only `process/state/WP-00.yaml` and `process/handoffs/WP-00-codex-targeted-closure-1.md`. No invalid handoff or environment condition occurred. WP-00 is SCOPING, requirements empty; I did not change its state or accept anything onto main.

## Scope and independent authority checks

Reviewed both complete diffs from the prior pair, including the changed tooling and tests, findings register, process/taxonomy/gates/coordination, plans, manifest, status metadata, checkpoint specialization, history ordering and model-visible reconstruction. Historical handoffs and review records were treated as historical evidence, not current operative instructions.

Read the changed requirements and their dependency neighborhoods: PERS-009–011 and LMEM-007/008/011–015; HIST-001–007 and learning episode declarations; ACTX-003 and MINT-006; identity/serialization uncertainty notes; all remaining 49 FROZEN main statements across core, scope, serialization, persistence, backup, privacy, learning and integration. Checked paths A/B/C, all uncertainty escalation flags/conditions, and searched the operative process/roles/gates/plans for approval being used as acceptance authority or source-silent semantics being preselected.

Re-read the independently extracted source passages from review 1 and opened the actual bundle DOCX ZIP/XML again for Foundation sections 13–16 and G.3/G.7, R04 sections 33/41.1, R05 sections 11/12, and IAA checkpoint vocabulary/A15. Confirmed the source file hashes:

| Source | SHA-256 |
|---|---|
| FND | `f3352b902e7c6b5654c379254d464d55f519a7f933b823faf2576cf6f081b5d6` |
| R04 | `b4c25d006e7db998feb5f955b55a9fcdc58ef589e72eae6cff742b9c0b92755f` |
| R05 | `a6c5dee570a5673a34fcd4a33057b2b3faeb1330847b2060235d903a99a4f240` |
| IAA | `436ea1a3a5ffa126d70a1c3cb8e1a8cc1e3d8baf1d50740df3a9098240daba33` |

Authority order and ownership are unchanged from review 1. The new G-007 excerpt supplies the previously unavailable location/status wording for NF-021; it records an Owner source rather than agent approval of the proposed registry split. The full controlling kickoff remains unavailable to me. NF-021 and other future governance/domain choices remain open appropriately.

This targeted scope is sufficient to assess these repairs; the two remaining blockers below have concrete witnesses. I am not requesting another complete review of untouched surface.

## Fresh gates and known-bad replay

Every shell first dot-sourced the absolute project environment. Venvs remain under `.tmp/cache/venvs`; scratch scripts/logs/backups under `.tmp/work/codex`; temp/caches/build-target variables stay inside the E: project. No Rust workspace, implementation, bundle edit, remote or push was created.

Ran gates sequentially, using `mneme-process-codex` and `minion-memory-python-codex` environments:

| Command | Fresh result |
|---|---|
| process/tools: `uv sync --python 3.12` | passed |
| `uv run pytest` | 96 passed in 170.37 s |
| Known-bad recipe below | 25 failed, 13 passed, 58 deselected in 66.18 s; expected nonzero exit |
| Same selection after restoring fixed tooling | 38 passed, 58 deselected in 68.52 s |
| `uv run ruff check src tests` | passed |
| `uv run ruff format --check src tests` | 11 files already formatted |
| `uv run mypy src` | no issues in 8 source files |
| `uv run mneme-process check --docs ../.. --code ../../../minion-memory --deep-sources` | 8/8 passed, including sources/spec/manifest/state |
| minion-memory-python: `uv sync --python 3.12`; `uv run pytest` | passed; 2 passed, 6 xfailed in 0.17 s |

The scaffold's xfails remain placeholders, not behavioral certification. The validator confirms the new 224-row manifest/spec bijection; it does not adjudicate source-status semantics or reconcile conflicting prose.

I executed the remediation record's recipe myself: save fixed `checks.py` and `yamlcore.py` bytes under E:-contained scratch; substitute each exact file from `git show 42f5193:process/tools/src/mneme_process/<file>`; run:

```text
uv run pytest -o addopts="-p no:cacheprovider" -q -k "cr00 or cr011 or malformed_status or rejects_lone or explicitly or rejects_nonportable" --runxfail
```

The scratch runner restored both fixed files in a `finally` block and verified byte equality. Verified clean repository diffs after restoration, then reran the same selection and the remaining gates on the fixed candidate. Scratch recipe/log: `.tmp/work/codex/closure-controls.py` and `closure-known-bad-output.txt`; durable evidence is summarized here so review does not depend on retaining them.

All repository-level controls assert an unmutated World fixture baseline before applying their mutation. Inspected failure traces, not merely exit status:

- CR-002, seven CR-003 cases, Claude CR-004, two gate-level CR-005 cases and CR-011 fail on old tooling because the intended check does not reject the witness; the fixed selection passes.
- CR-004 Codex fails on old tooling only at the diagnostic-fragment assertion: old tooling already reports `a quarantined candidate cannot be handed off`. This case is regression coverage, not evidence of the original defect. Claude alone discriminates the actor omission (`state did not fail; failures: {}`).
- Old YAML already rejects aliases, `!!binary` and `!local`; those three unit failures likewise reflect changed diagnostic fragments. They do not prove newly enforced rejection. The `!!str` and unused `&unused` witnesses do prove it: the old loader returns `ok=True`, and both scenario gate controls falsely pass.
- Three escaped-surrogate YAML witnesses and three direct domain witnesses discriminate old acceptance from new explicit rejection. The astral-scalar positive witness passes in the full fixed suite.
- The malformed-status control fails its intended structured-error assertion on old tooling (aggregate reports an internal error), and passes after the fix.
- Valid scoping closure, quarantine routed to Owner, and a legitimate multi-commit state-only chain pass on old and fixed tooling. The other pre-existing selected unit controls also pass.

Thus 21 of the 25 failing tests distinguish missing behavior; four are diagnostic-only differences. No setup/import failure was credited as a control kill. The permanent witnesses and positive controls adequately cover the executable repairs under this targeted task.

## Per-finding disposition

Every entry marked **PROVISIONALLY CLOSED @ C/D** below means **PROVISIONALLY CLOSED @ `139f81f9cee8201e96e69c093d3489c0ed3d36a4` / `c3e0d2ed15e116588a196d92e6ca36ce2750cda7`**. Provisional closure is evidence at this pair, not a certification-state edit.

| Finding | Disposition | Witness and closure assessment |
|---|---|---|
| WP00-CR-001 | PROVISIONALLY CLOSED @ C/D | Coordination section 6 now explicitly separates approval and acceptance, requires Owner decision/delegation, and routes acceptance to Owner absent delegation. Workflow step 9, accepted-milestone table and gate table agree. No operative instruction in the reviewed neighborhood grants acceptance through approval alone. Documentary comparison; executable negative control not applicable. |
| WP00-CR-002 | **OPEN** | A/B/C taxonomy, escalation conditions, flags and validator repair pass their intended control; old tooling misses the false-flag/no-condition mutation. However WP-01 lines 46–47 still mandate surrogate rejection while NF-019 assigns that payload choice to Owner. Refined documentary witness below. |
| WP00-CR-003 | PROVISIONALLY CLOSED @ C/D | Seven permanent controls cover missing review, four non-approval tokens, missing accepted main evidence and missing product certification. They all falsely pass on old tooling and reject on fixed tooling. Valid recorded scoping closure passes. Inspection confirms exact outcome token and nonblank verdict/source checks; independent approval remains a stated manual verification duty. |
| WP00-CR-004 | PROVISIONALLY CLOSED @ C/D | Guard now applies to both agents; Claude's previously accepted actionable quarantined state is rejected. Owner positive case passes. Codex's diagnostic-only old failure is not credited as discrimination. |
| WP00-CR-005 | PROVISIONALLY CLOSED @ C/D | Token scan rejects explicit tag/anchor/alias syntax before composition erases it. The redundant `!!str` and unused anchor unit and scenario controls distinguish old acceptance from fixed rejection. Existing rejection, duplicate-key and ambiguity cases remain green. Rust can implement the syntax predicate without copying PyYAML mechanics. |
| WP00-CR-006 | PROVISIONALLY CLOSED @ C/D | PERS-009 declares a profile/family and family-specific dependencies; it no longer requires learner fitted parameters for deterministic agent indexes. LMEM-015 preserves R04 section 33 learner metadata, boundaries and incompatibility behavior. PERS-010/011 remain compatible; layer 10 depends on checkpoint layer 05. Documentary source comparison; executable negative control not applicable. |
| WP00-CR-007 | PROVISIONALLY CLOSED @ C/D | HIST-003 now concerns LearningEpisode events, profile learning, layer 08; HIST-005 says devices/episodes. Manifest/layer plan and NF-016 distinguish append cursors from semantic episode order. No universal agent-container order is introduced. Documentary comparison; executable negative control not applicable. |
| WP00-CR-008 | **OPEN** | KNOW-011 downgrade and narrower frozen renderer sentence are faithful; EVID-006 adds supporting FND sections 8/14; the six additional downgrades are justified. Remaining SCOPE-002 still lacks its explicit FROZEN status anchor G.7. Refined citation witness below. |
| WP00-CR-009 | PROVISIONALLY CLOSED @ C/D | ACTX-003 now applies to every model-visible memory projection, matching R05 section 11 and MINT-006; the note correctly distinguishes the Foundation materiality minimum. Documentary comparison; executable negative control not applicable. |
| WP00-CR-010 | PROVISIONALLY CLOSED @ C/D | LMEM-014 carries temporal future-test/leakage, learner/domain holdouts and retrospective/prospective distinctions with source modal strength and conditional applicability. MVP platform deferral is retained; LMEM-013 remains the baseline obligation. Documentary comparison; executable negative control not applicable. |
| WP00-CR-011 | PROVISIONALLY CLOSED @ C/D | Coordination now describes descendants and per-commit checks; validator examines every commit with diff-tree. Change followed by exact revert is detected at its intended assertion, unlike old endpoint tooling; permitted multi-commit state-only chain still passes. Actual control chain passed preflight. |
| WP00-CR-012 | PROVISIONALLY CLOSED @ C/D | Both code READMEs and WP-00 deliverable table distinguish ownership README from absent Cargo workspace. No Rust implementation was created. Documentary comparison; executable negative control not applicable. |
| WP00-CR-013 | PROVISIONALLY CLOSED @ C/D | WP-01 deliverable 2 explicitly includes H5 canonical key order and ordering inside canonical/hash bytes. Documentary comparison; executable negative control not applicable. |

The two review questions are also resolved on the tooling surface: explicit surrogate rejection and structured list-valued-status diagnostics are demonstrated above. The canonical/governance YAML reader's Unicode-scalar profile is distinct from the unresolved product payload domain in NF-019; it does not settle that domain by precedent.

## Refined witnesses for surviving findings

These retain the existing IDs and root causes, rather than creating duplicate successor findings. No new finding ID is raised.

```yaml
- id: WP00-CR-002
  title: WP-01 still preselects the Owner's payload-domain rejection outcome
  classification: CONTRACT_ASSURANCE_DEFECT
  blocking: true
  owner_decision_required: false
  sources:
    - "c3e0d2ed15e116588a196d92e6ca36ce2750cda7:plans/WP-01-proposal.md:46-47"
    - "c3e0d2ed15e116588a196d92e6ca36ce2750cda7:assurance/findings/WP-00-findings.yaml:344-349 (NF-019)"
    - "c3e0d2ed15e116588a196d92e6ca36ce2750cda7:process/finding-taxonomy.md:29-45"
  requirements: [SER-001]
  observation: "WP-01 risks say the contract must reject Python lone surrogates at the seam, selecting an observable payload-domain outcome."
  expected: "Sources or recorded Owner governance must decide the payload domain; until then, the proposal presents options and does not mandate rejection. Governance YAML's separate profile is not product-domain authority."
  witness: "At D, the proposal says 'the contract must reject them at the seam', while NF-019 says 'Always path C for restricting the value domain (e.g. rejecting lone surrogates ... in payloads)' and taxonomy section 1.1 reserves path C to Owner. The former is in the Layer-01 product proposal, not the governance YAML format."
  recommendation: "Replace the predetermined outcome with the unresolved portability hazard and an Owner options packet, or cite applicable source/recorded Owner authority that actually chooses it. Editing contradictory proposal wording needs no new Owner permission; choosing rejection does."
- id: WP00-CR-008
  title: SCOPE-002's FROZEN label still omits the supporting status anchor
  classification: CONTRACT_ASSURANCE_DEFECT
  blocking: true
  owner_decision_required: false
  sources:
    - "c3e0d2ed15e116588a196d92e6ca36ce2750cda7:spec/scope.md:19-25"
    - "c3e0d2ed15e116588a196d92e6ca36ce2750cda7:spec/README.md:60-66"
    - "FND sections G.3/G.7; SHA-256 f3352b902e7c6b5654c379254d464d55f519a7f933b823faf2576cf6f081b5d6"
    - "139f81f9cee8201e96e69c093d3489c0ed3d36a4:mneme-contract-manifest.yaml SCOPE-002 row"
  requirements: [SCOPE-002]
  observation: "SCOPE-002 labels its core/profile ownership rule FROZEN, citing FND G.3, R00 21, R04 41.1 and MVP 18.1, but not FND G.7. Its manifest row repeats the omission."
  expected: "The spec convention requires a cited source explicitly labeling the main statement FROZEN; normative prose alone does not supply the status."
  witness: "FND G.3 contains the ownership prose without a FROZEN box. The actual status row is G.7: MemoryScope exists in core; profile vocabularies remain profile-owned, FROZEN boundary / PROVISIONAL vocabulary. R00 21, R04 41.1 and MVP 18.1 have no explicit FROZEN label for this rule. Neighbor SCOPE-001 cites G.7, but SCOPE-002 and its manifest row do not."
  recommendation: "Add the explicit G.7 status citation to SCOPE-002 and its manifest row, stating the frozen boundary's scope; keep any more specific unlabeled mechanics normative. Alternatively downgrade the label if the chosen main statement exceeds that frozen boundary. This requires traceability repair, not new semantics."
```

## Verdict and next coordination step

**CHANGES_REQUIRED** — WP00-CR-002 and WP00-CR-008 remain blocking; the other eleven CR findings are provisionally closed at C/D.

Claude should independently reproduce these two narrowed documentary witnesses and record the dispositions. Convergence trigger A has fired: each material finding has now survived two independent reviews. Check and record the trigger before the next pass. The remaining evidence is narrow enough for targeted documentary repair, so an ordinary repair exception can be justified explicitly under the adopted process section 11.8; do not claim the threshold has not fired. Preserve legal SCOPING routing rather than inventing an implementation/remediation transition for this process WP.

After repair, freeze the new exact pair and request targeted closure of these witnesses and changed neighbors. No new complete review of untouched surface is required by this review. Approval, if obtained later, approves only the candidate; acceptance onto main still requires Owner authority. WP-01 remains stopped. This branch adds only this review record, with the commit SHA supplied externally to avoid self-reference.
