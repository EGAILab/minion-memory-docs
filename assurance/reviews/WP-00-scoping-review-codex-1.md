# WP-00 independent scoping review — Codex 1

Reviewer: Codex, independent reviewer, Rust implementation owner and cross-language challenger. Date: 2026-10-09. Claude authored the candidate and remains coordinator/Python owner. This is a scoping review, not implementation, contract certification, or permission to accept onto main. I reconstructed the authorities independently; Python behavior was evidence about tooling, never semantic authority.

## Candidate and authority

- Code: `a91db170b5e7827caf1a6ffd02546ec23a1d51fa` (`wp00/bootstrap`).
- Docs content (D below): `42f5193dda74b6d5134eab27f7038661c4e583f3`.
- Docs control/base of this review: `201b7f7da8eb502d6157c44db2a01e5fcdc89820`, parent `3a6a94bf6eb5d8e8befc5c4fc473a437f8279b2c`, whose parent is D. The endpoint diff from D contains only state and the two handoffs. This is a two-commit descendant chain, not one immediate child.
- Bundle: `mneme-v2.3-dual-profile`, 12 loose files in `artifacts/20261009/Project_Mneme_Documentation_Bundle_2026-10_v2_3_Dual_Profile/`; ZIP SHA-256 `9d999c1934e33b70100e884ed5cb60d0cbdb71150af59a8b2334604b4220251e`.
- Process authority pin (P below): `EGAILab/minion-agent-docs` at `8744bd019066f9c18d000c1a0ad19b435775300a`.
- Consumer code pin (A below): `EGAILab/minion-agent` at `3de4b75d0119b6c413dae651a3cba039873756c7`.

Preflight: both frozen commit objects exist and are reachable from their bootstrap refs; both trees were clean; the docs endpoint diff satisfies the handoff allowlist. Neither repository has main or remotes. No handoff/environment failure occurred. WP-00 remains SCOPING, requirements empty, NF-001–021 open, with no recorded scoping approval.

Authority order used: Foundation > MVP > Requirements (R00 normative for R01–04, R05 agent) > Architecture Amendments > implementation pack/bootstrap guidance. Read G-001–G-006 and OWN-001 from the Owner kickoff record. The full unquoted kickoff was unavailable; claims about its additional wording were not independently validated. Candidate spec/process/plans/findings are review objects. P governs the process adaptation, not Mneme domain semantics.

Bundle source abbreviations in findings are content addressed by this table; section anchors plus these hashes identify the source, independently of derived source-text:

| Key | File SHA-256 |
|---|---|
| FND | `f3352b902e7c6b5654c379254d464d55f519a7f933b823faf2576cf6f081b5d6` |
| MVP | `5a28d40a0c3b859a5e81854d03a2480636c1833c9f5aa97cbac8bb393a650e2a` |
| R00 | `50a0fc28fca0a2e8fc4b42932a7388eb9e150b1e429ba110e95420c0a32d18d1` |
| R01 | `51c6a31f987d3ebe8fd4170d54508197d54e742150bb5966637a9faf47bbea51` |
| R02 | `6b6fbed00034b25e4440092684244425518572a05a736f4c7568ca42305407ec` |
| R03 | `651cacc5992d5da22f0d3ed10dde9f2bcb3b66e3fd4549bc1a4bf9050b83a797` |
| R04 | `b4c25d006e7db998feb5f955b55a9fcdc58ef589e72eae6cff742b9c0b92755f` |
| R05 | `a6c5dee570a5673a34fcd4a33057b2b3faeb1330847b2060235d903a99a4f240` |
| IAA | `436ea1a3a5ffa126d70a1c3cb8e1a8cc1e3d8baf1d50740df3a9098240daba33` |

## Reading, coverage and independent evidence

Read all nine authority DOCX files directly from their ZIP/XML paragraphs and table paragraphs, rather than trusting derived text, plus both bundle bootstrap prompts and implementation-pack guidance (AGENTS, README, implementation plan). The DOCX files contain no drawing elements; this was a textual audit, not a visual layout audit. Read both repository READMEs, Owner record, source manifest, spec conventions, all 222 requirements, both JSON schemas, all conformance placeholders, scaffold runner/tests, all process tooling source/tests, process/state/roles/gates/taxonomy/IDs/adoption/registry, WP-00 and WP-01 plans, layers, hazards, feasibility template and NF register. Read P's workflow/evidence/convergence, coordination closure and loader, and implementation/conformance rules at the pin. Inspected the pinned consumer implementations directly.

Sampling was exhaustive, above the required minimum:

| Family/file | Requirements read |
|---|---:|
| core / scope / persistence / serialization | 47 / 6 / 16 / 7 |
| agent capture / consolidation / context / integration / records / retrieval | 8 / 7 / 5 / 9 / 5 / 7 |
| backup / privacy | 8 / 6 |
| learning evidence / inference / interaction / knowledge / migration / package / scheduling | 16 / 13 / 18 / 16 / 6 / 11 / 11 |
| Total | 222 |

Independent inventory script compared actual bytes: all 12 loose-file hashes match the manifest, the ZIP has the same 12 files and matching bytes, all nine pack reference DOCX copies match, both BOOTSTRAP_PROMPT.md copies match the loose v1.1 prompt, and all 19 superseded files are present with recorded hashes. No inventory omission or duplicate-content discrepancy found.

Seam verification at A: Python `agent_loop/driver.py:1047–1050,1095` supplies `system_base`; `session/request_header.py:31–40` joins components in name-sorted order. Rust `crates/minion-agent/src/session/mod.rs:402,472` uses BTreeMap and joins its values. Composer-contributed content can be inside system_base; combined text is reconstructable, but a distinct attributable memory component is absent. An adapter might supply separate attribution metadata; the audit must not claim attribution is impossible in every adapter. Adding a component named memory places it before system_base under current assembly. NF-007/008 identify real seam/design work, not a mandate to implement it now.

The dual-profile split is sound overall; learner-specific persistence leakage and broadened history ordering are exceptions below. Core/profile/package dependency layering is reasonable. WP-01 is a sensible first semantic package (portable serialization/identity foundations), provided unresolved domain decisions are escalated and no later-profile behavior is silently fixed there. ARCH, PRIV and PKG are useful families and accepted as a taxonomy proposal; IDs should freeze only after normalization repairs, not by treating this review as approval.

Class 8 CONTRACT_CONSTRAINED_RISK is justified for an explicitly correct contract whose change would alter semantics. It must not shelter uncertainty or assurance defects. Claude-led coordination and independent reproduction are preserved in the written model, subject to acceptance and closure defects below. Pi/GitHub-specific mechanics have generally been replaced appropriately with bundle authority and file-based coordination.

Schemas, manifest traceability, canonical envelope and placeholder/runner rules are independently implementable in Rust. No format requires copying Python internals. YAML acceptance currently differs from its stated portable profile: fix the language-neutral grammar, not by blessing PyYAML's incidental node behavior. H1–H11 cover the major cross-language classes (numbers, Unicode, time, paths, ordering/hashes, YAML, failures, durability, identity, projection, runtime); surrogate handling remains an unresolved domain question, not a claim of complete equivalence.

## Fresh gates and environment

All shell invocations first dot-sourced the project environment. All created extraction/probe/fixture files are under `.tmp/work/codex`; environments are `.tmp/cache/venvs/mneme-process-codex` and `.tmp/cache/venvs/minion-memory-python-codex`. Temp, cache and Cargo target variables point within this E: project. No clone, build target, venv or temporary artifact was created on C:. No Rust workspace or implementation was created.

Observed tools: git 2.55.0.windows.1, uv 0.10.9, CPython 3.12.8 at `E:\AI\Python\Python312\python.exe`, rustc/cargo 1.97.1. Gates ran sequentially:

| Working directory / command | Fresh result |
|---|---|
| process/tools: `uv sync --python 3.12` | passed |
| `uv run pytest` | 69 passed, 89.65 s |
| `uv run ruff check src tests` | passed |
| `uv run ruff format --check src tests` | 11 files already formatted |
| `uv run mypy src` | no issues in 8 source files |
| `uv run mneme-process check --docs ../.. --code ../../../minion-memory --deep-sources` | 8/8 passed |
| minion-memory-python: `uv sync --python 3.12` | passed |
| `uv run pytest` | 2 passed, 6 xfailed, 0.35 s |

The six xfails are placeholders, not behavioral conformance evidence. Existing negative controls assert a clean baseline and generally exercise their intended error assertion; I found omitted cases, rather than counting import/setup failures as successful controls. Passing the current gates does not discharge the findings below.

## Findings

In sources below, D, P and A expand to the full commit hashes above; FND/MVP/Rxx expand to the file SHA-256 above. Each source remains content addressed. Owner flags concern repairing the identified defect; choosing previously unspecified semantics or granting delegation remains an Owner decision.

```yaml
- id: WP00-CR-001
  title: Acceptance authority contradicts the open no-delegation finding
  classification: CONTRACT_ASSURANCE_DEFECT
  blocking: true
  owner_decision_required: false
  sources: ["D:process/coordination-state.md:155-158", "D:assurance/findings/WP-00-findings.yaml:330-346 (NF-020)", "P:process/agent-workflow.md section 11.10"]
  requirements: []
  observation: "Coordination section 6 permits Claude acceptance after reviewer approval while NF-020 says no main acceptance without Owner delegation."
  expected: "Review approval and acceptance authority are separate; absent delegation, acceptance stays with the Owner."
  witness: "Read the two operative instructions together: the approval condition in section 6 does not include the delegation condition in NF-020."
  recommendation: "Make the acceptance instruction conditional on recorded authority. Do not infer delegation from review approval; only the Owner can grant it."
- id: WP00-CR-002
  title: Unspecified semantic choices are assigned to agents without conditional Owner escalation
  classification: CONTRACT_ASSURANCE_DEFECT
  blocking: true
  owner_decision_required: false
  sources: ["D:process/finding-taxonomy.md sections 1 and 4", "D:process/agent-workflow.md section 9", "D:assurance/findings/WP-00-findings.yaml NF-010 through NF-017 and NF-019", "D:plans/WP-01-proposal.md deliverables"]
  requirements: [CORE-001, CORE-002, CORE-003, CORE-011, CORE-012, HIST-004, SER-001]
  observation: "REQUIREMENT_UNCERTAIN records use false Owner flags and resolve via future layer definitions even when selecting among source-silent observable behaviors."
  expected: "Authority reading can resolve uncertainty; if it cannot, silent/conflicting semantic choices require Owner resolution. Implementation mechanics preserving a defined domain do not."
  witness: "NF-014's conflict rejection versus return-prior behavior changes API outcomes; NF-010's Unicode normalization choices change identity. A layer number does not supply authority for either choice."
  recommendation: "Add explicit conditional escalation and correct affected flags/closure criteria. Separate source clarification and representation mechanics from unresolved observable semantics. This review selects none of those semantics."
- id: WP00-CR-003
  title: State validator accepts closure without scoping approval or accepted main evidence
  classification: CONTRACT_ASSURANCE_DEFECT
  blocking: true
  owner_decision_required: false
  sources: ["D:process/coordination-state.md:77-92", "D:process/tools/src/mneme_process/checks.py:451-574", "P:process/coordinator-state.md section 10.3"]
  requirements: []
  observation: "The advertised state/closure validation accepts a CLOSED scoping-only WP with scoping_review null and no main branch."
  expected: "Closure must establish the approved scoping outcome and accepted target evidence required by the process, including for requirements-empty WPs."
  witness: "A clean World.build fixture yields all_errors == {}; set status CLOSED, open_findings [], next_action and next_owner null, retain scoping_review null and no main: all_errors still == {}."
  recommendation: "Enforce closure guards and add discriminating controls. If part of closure intentionally remains manual, state that boundary accurately and require recorded evidence rather than presenting this state as machine-validated closure."
- id: WP00-CR-004
  title: Quarantine protection excludes the coordinator
  classification: CONTRACT_ASSURANCE_DEFECT
  blocking: true
  owner_decision_required: false
  sources: ["D:process/agent-workflow.md section 6", "D:process/tools/src/mneme_process/checks.py:510-516", "P:process/agent-workflow.md section 11.12"]
  requirements: []
  observation: "The quarantine action guard rejects Codex as next actor but accepts Claude."
  expected: "Quarantined evidence cannot authorize an actionable next step by either paired agent; forensic records can remain non-actionable."
  witness: "In a clean synthetic state, quarantine.derived_from_quarantined_artifact true with next_owner Claude returns check_state errors []. The actor-specific branch only checks Codex."
  recommendation: "Apply the invariant to all actionable actors and test both directions without removing forensic evidence."
- id: WP00-CR-005
  title: Portable YAML loader accepts forbidden explicit tags and anchors
  classification: CONTRACT_ASSURANCE_DEFECT
  blocking: true
  owner_decision_required: false
  sources: ["a91db170b5e7827caf1a6ffd02546ec23a1d51fa:conformance/README.md portable YAML profile", "D:process/tools/src/mneme_process/yamlcore.py:89-115,157-175", "D:assurance/layers/00-cross-language-hazard-inventory.md H6"]
  requirements: []
  observation: "Composed-node checks admit explicit supported tags and unused anchors despite the no-tags/no-anchors profile."
  expected: "The same syntax subset must be rejected by independent Python and Rust readers."
  witness: "load_core accepts 'a: !!str plain' and 'a: &unused plain'. Replacing a fixture scenario title with 'title: !!str fixture' or 'title: &unused fixture' also returns check_conformance errors []. Baseline passes; duplicate keys are correctly rejected as a control."
  recommendation: "Inspect syntax events/tokens or equivalent parser information before composition erases explicit syntax. Specify an implementation-neutral grammar and add both gate-level negative controls."
- id: WP00-CR-006
  title: Shared checkpoints require learner-specific fitted-parameter metadata
  classification: CONTRACT_ASSURANCE_DEFECT
  blocking: true
  owner_decision_required: false
  sources: ["FND section G1", "R04 sections 33 and 41.1", "R05 section 12", "D:spec/persistence.md:82-99"]
  requirements: [PERS-009, PERS-011]
  observation: "Shared checkpoint requirements demand at least model definition/version and fitted-parameter identity/version."
  expected: "Shared checkpoint provenance is profile/model/projection aware; learner fitted-parameter metadata applies where the learner model actually has it. Agent models may be deterministic projections without learner fitting."
  witness: "R04 section 33 supplies learner-specific detail; R04 section 41.1 and R05 section 12 supply generic profile-aware checkpoints. A deterministic agent lexical projection has no fitted learner parameters, yet the normalized shared minimum requires them."
  recommendation: "Keep generic derivation dependencies in core and specialize learner metadata in the learning profile; do not force fictitious fitting fields into the agent profile."
- id: WP00-CR-007
  title: Episode event ordering is broadened to every history container
  classification: CONTRACT_ASSURANCE_DEFECT
  blocking: true
  owner_decision_required: false
  sources: ["FND section 6 and Appendix E", "MVP section 5.1", "R04 section 9", "D:spec/core.md:276-283"]
  requirements: [HIST-003, HIST-005]
  observation: "The normalized rule requires order inside a history container, giving episode events merely as an example."
  expected: "The cited sources define episode event ordering; an append-log cursor and semantic ordering of every profile container are different obligations."
  witness: "The sources' episode-scoped requirement becomes a universal container rule, imposing an unsupported total semantic sequence on independently captured agent data."
  recommendation: "Restore the cited scope, preserve core append ordering separately, and resolve any additional agent-container ordering at its authority boundary."
- id: WP00-CR-008
  title: FROZEN status and citations do not consistently follow explicit source labels
  classification: CONTRACT_ASSURANCE_DEFECT
  blocking: true
  owner_decision_required: false
  sources: ["D:spec/README.md section 3", "D:spec/learning/knowledge.md:93-102", "D:spec/learning/evidence.md:82-88", "FND sections 5, 14 and 19"]
  requirements: [KNOW-011, EVID-006]
  observation: "KNOW-011 marks an authored definition FROZEN from FND section 5; EVID-006 is FROZEN without a Foundation citation."
  expected: "The candidate's convention permits FROZEN only for explicitly frozen source material, with traceable support for the normalized rule."
  witness: "FND section 5 treats the name as provisional and explicitly freezes renderer/coverage aspects, not the entire authored definition. EVID-006 cites MVP/R03/R04 rather than the potentially supporting FND section 14."
  recommendation: "Audit source-status scope, split mixed-status rules where needed, add correct supporting citations, and update matching manifest metadata. This is a status/traceability repair, not a claim that all EVID-006 behavior is wrong."
- id: WP00-CR-009
  title: Model-visible reconstruction obligation is weakened by a materiality qualifier
  classification: CONTRACT_ASSURANCE_DEFECT
  blocking: true
  owner_decision_required: false
  sources: ["R05 section 11", "FND section G4", "D:spec/agent/context.md:22-28", "D:spec/agent/integration.md:54-62"]
  requirements: [ACTX-003, MINT-006]
  observation: "ACTX-003 requires reconstruction when visible and material, while MINT-006 and R05 require it for model-visible agent memory."
  expected: "Foundation's material-input minimum does not weaken the more specific agent-profile obligation."
  witness: "A model-visible projection judged immaterial falls outside ACTX-003 but remains inside R05 section 11 and MINT-006. Layer 15 cannot safely implement the context rule alone."
  recommendation: "Align the scope and dependency between context and integration rules; preserve the applicable R05 obligation without the added exemption."
- id: WP00-CR-010
  title: Learner evaluation discipline is omitted from normalization
  classification: CONTRACT_ASSURANCE_DEFECT
  blocking: true
  owner_decision_required: false
  sources: ["FND section 15.1", "MVP section 10", "D:spec/learning/inference.md LMEM-007 and LMEM-013"]
  requirements: [LMEM-007, LMEM-013]
  observation: "The baseline-model requirement is retained, but the adjacent evaluation discipline is not transcribed elsewhere in the 222 requirements."
  expected: "Normalization preserves source instructions and their modal strength, even when a research/evaluation platform is deferred from MVP implementation."
  witness: "FND section 15.1 addresses temporal training/future-test splits, leakage avoidance, learner holdout, knowledge/domain holdout, and retrospective versus prospective evaluation; LMEM-013 retains only the interpretable baseline, and the remaining spec does not capture those distinctions."
  recommendation: "Normalize the evaluation instructions with their original strength and applicability. Do not turn preferred techniques into unconditional requirements or mandate a deferred platform now."
- id: WP00-CR-011
  title: Single-child wording does not describe the authorized control chain
  classification: SEMANTICS_NEUTRAL_HARDENING
  blocking: false
  owner_decision_required: false
  sources: ["D:process/coordination-state.md:33-43", "D:process/tools/src/mneme_process/checks.py:536-574", "201b7f7da8eb502d6157c44db2a01e5fcdc89820 commit parents"]
  requirements: []
  observation: "Documentation says state-only child; the authorized head is two commits above D and validation examines an endpoint diff."
  expected: "Precisely distinguish immediate-child and allowed descendant-chain rules, and endpoint versus per-commit guarantees."
  witness: "The control parent is 3a6a94bf, whose parent is D. A scratch content-change commit followed by an exact revert also passes the endpoint check; this establishes its limit, not a current frozen-content discrepancy."
  recommendation: "Document the intended descendant-chain policy and git-object round trip accurately, including whether every intervening commit or only the endpoint is constrained. Current authorized endpoint contents are valid."
- id: WP00-CR-012
  title: Rust placeholder directory is described as not created
  classification: SEMANTICS_NEUTRAL_HARDENING
  blocking: false
  owner_decision_required: false
  sources: ["a91db170b5e7827caf1a6ffd02546ec23a1d51fa:README.md", "a91db170b5e7827caf1a6ffd02546ec23a1d51fa:minion-memory-rust/README.md", "D:plans/WP-00.md"]
  requirements: []
  observation: "A Rust directory and README exist while narrative wording says Rust is not created."
  expected: "Distinguish an ownership placeholder from an implemented Cargo workspace."
  witness: "The directory contains its README and no Cargo workspace. There is no premature Rust implementation."
  recommendation: "Say the Rust workspace is not created and the ownership README is present."
- id: WP00-CR-013
  title: WP-01 explicit hazard checklist omits key-order and hash hazards
  classification: CONTRACT_ASSURANCE_DEFECT
  blocking: false
  owner_decision_required: false
  sources: ["D:plans/WP-01-proposal.md deliverables", "D:process/hazard-families.md H5", "D:assurance/layers/00-cross-language-hazard-inventory.md H5 and H7"]
  requirements: [CORE-011]
  observation: "The explicit WP-01 list includes H1/H2/H3/H4/H6/H7/H11 but omits H5 despite canonical ordering and identity/hash work."
  expected: "The package's explicit hazard plan includes its ordering/hash domain."
  witness: "H5 owns map/key ordering and hashing/object-byte hazards; H7's failure semantics do not replace it. General mandatory hazard review still covers it transitively."
  recommendation: "Add H5 before the WP-01 checkpoint. The general rule prevents this omission alone from blocking WP-00."
```

## Positions on Claude's NF-001–021

| Finding | Position and rationale |
|---|---|
| NF-001 | Agree: package-layout alternatives affect scope; Owner flag and Layer 12 resolution are appropriate. |
| NF-002 | Reclassify duplicate section numbering as SEMANTICS_NEUTRAL_HARDENING once anchors are disambiguated; numbering alone is not an active semantic contract defect. |
| NF-003 | Taxonomy proposal is reasonable organizational scoping. Do not treat suggested family names themselves as a demonstrated semantic defect or freeze defective normalization. |
| NF-004 | Reclassify stale self-references as SEMANTICS_NEUTRAL_HARDENING where operative text is unambiguous; demonstrate an actual conflicting rule before stronger classification. |
| NF-005 | Agree on the sequencing decision; profile independence is sensible, but changing profile/layer order needs Owner governance. Later backup obligations still apply. |
| NF-006 | Agree: Owner excerpts outrank implementation guidance; no present blocker established by guidance alone. |
| NF-007 | Agree with the seam gap and Layer 16/Owner scope path; qualify attribution claims because system_base retains combined content and adapter metadata is possible. |
| NF-008 | Agree on name-sorted placement and canonical injection-path risk; an unresolved observable path/placement choice needs conditional Owner escalation, not an unconditional false flag. |
| NF-009 | Reclassify generic drift/evidence maintenance as SEMANTICS_NEUTRAL_HARDENING absent a demonstrated stale or unfaithful contract. |
| NF-010 | Agree on identity/Unicode gap and Layer 01; sources must resolve the domain or Owner must decide. |
| NF-011 | Agree that version edition versus SemVer is unresolved; engineering representation must not silently select version semantics. |
| NF-012 | Qualify: derived durable artifacts with canonical lineage can coexist with rebuildability. Distinguish that from a genuine source-of-truth conflict; resolve at core/agent boundaries. |
| NF-013 | Agree on hash-domain gap; conditional Owner escalation applies where the authority leaves observable identity undecided. |
| NF-014 | Agree on idempotency conflict gap; reject-conflict versus return-prior changes outcomes and cannot be silently decided under a false Owner flag. |
| NF-015 | Agree on timestamp representation gap; preserving a defined time domain is mechanics, choosing precision, unknown-time semantics or a lossy restriction requires authority. |
| NF-016 | Qualify: append cursors coexist with episode semantic order. Do not infer a source contradiction or universal semantic ordering merely from those two concepts; Layer 02/04 scope remains relevant. |
| NF-017 | Agree on cost/tokenizer boundary; a cost contract does not imply a universally prescribed tokenizer. Resolve source-silent observable choices conditionally through Owner. |
| NF-018 | Agree on scope/visibility semantics and Owner flag, resolving at Layer 02. |
| NF-019 | Agree on portable value-domain gap; apply it to process/conformance readers too. Domain choice requires authority, not matching Python permissiveness. |
| NF-020 | Agree: no acceptance delegation is established. Correct the conflicting operative instruction (CR-001); only Owner can grant authority. |
| NF-021 | Separating certification status into the registry is technically sensible as a proposal, pending Owner confirmation. The additional unquoted kickoff claim cannot be verified from available authority; do not promote it to an approved direction. |

These positions distinguish current assurance repairs from future package blockers. Not every NF uncertainty must be decided during WP-00, but the escalation mechanism must be correct now.

## Reproduction and open questions

Supplemental probes used imports from the candidate tooling and its existing `tests/conftest.py` World fixture, in temporary repositories under `.tmp/work/codex`. No real state or conformance file was mutated. Scratch scripts are `probe_inventory.py`, `probe_bootstrap.py`, and `probe_state_world.py`; the durable witnesses above and recipe below do not depend on retaining them.

To reproduce CR-003–005: import `World` from the candidate's `tests/conftest.py`, construct `World(path)` in an E:-contained temporary directory, call `build()`, and assert `world.all_errors() == {}` before each independent mutation. For closure, call `write_state(status='CLOSED', open_findings=[], next_owner=None, next_action=None, scoping_review=None)` while there is no main; `all_errors()` returns `{}`. For quarantine, call `write_state(status='SCOPING', next_owner='Claude', next_action='test', quarantine={'derived_from_quarantined_artifact': True})`; `checks.check_state(world.ctx)` returns `[]`. For YAML, replace the fixture scenario's `title: fixture` with either `title: !!str fixture` or `title: &unused fixture`; the conformance checker returns `[]`. Independently, `load_core('a: !!str plain\n')` and `load_core('a: &unused plain\n')` return mappings, whereas a duplicate-key mapping raises rejection. Each synthetic baseline was checked first. Those are successful false-pass witnesses, not assumptions about the other language.

Questions, not additional blockers: the loader accepts an escaped lone surrogate (`a: "\\uD800"`), which should be considered when NF-019 defines the common value domain. A list-valued state status produces a TypeError in direct validation; clarify whether the aggregate command intentionally reports malformed types as internal errors or should provide structured diagnostics. Neither observation establishes an additional source-defined semantic choice in this review.

## Verdict and next coordination step

**CHANGES_REQUIRED** — WP00-CR-001 through WP00-CR-010 are blocking; WP00-CR-011 through WP00-CR-013 are non-blocking.

Claude should independently reproduce and classify the shared-contract findings, record this review in the coordination state, and repair the candidate while WP-00 stays SCOPING. Freeze a new code/docs pair as needed and request independent re-review. Do not start WP-01, certify these drafts, accept onto main, or treat this result as acceptance delegation. This review branch adds only this record; bootstrap refs, source bundle and implementation remain untouched. The review commit SHA is supplied with the handoff notification rather than self-referenced inside its own commit.
