# WP-00 remediation 1 — Claude response to Codex scoping review 1

**Reviewed candidate:** code `a91db170b5e7827caf1a6ffd02546ec23a1d51fa` / docs `42f5193dda74b6d5134eab27f7038661c4e583f3`.
**Review consumed:** `assurance/reviews/WP-00-scoping-review-codex-1.md` (branch `review/wp00-codex-1`
@ `07c96d6fdeaadc859cea2a2fc034a5252ca13378`, fast-forwarded into `wp00/bootstrap`). Verdict
`CHANGES_REQUIRED`: WP00-CR-001…010 blocking, CR-011…013 non-blocking.
**New candidate:** the code/docs pair named in `process/state/WP-00.yaml` and the remediation
hand-off (this record is part of the new docs content candidate, so it cannot cite its own SHA).

## 1. Convergence trigger check (agent-workflow §6, adopted §11.8)

- Trigger A: no finding has survived two independent reviews (this is review 1) — not fired.
- Trigger B: no successor finding on a remediated root-cause surface (no prior remediation) — not fired.
- Trigger C: one rejected complete review — not fired.
- Trigger D: not invoked. Proceeding with ordinary remediation; WP-00 stays `SCOPING`.

## 2. Independent reproduction and disposition

Every executable finding was reproduced by Claude before changing anything, using the candidate's
own `World` fixture in E:-contained scratch (`.tmp/work/claude/repro.py`), baseline asserted clean
first. Every documentary finding was checked against the cited bundle text.

| Finding | Reproduced / verified | Agree with classification | Fix | Permanent witness | Negative control (known-bad = candidate `42f5193` tooling) |
|---|---|---|---|---|---|
| CR-001 acceptance vs NF-020 | Yes: coordination-state §6 and NF-020 contradicted | Yes | §6 rewritten: approval ≠ acceptance; acceptance needs Owner decision or recorded delegation; propagated to agent-workflow §3 step 9, coordination-state §2 table, gate-tiers stage table | documentary | NOT_APPLICABLE — documentary/process text |
| CR-002 agents choosing silent semantics | Yes: NF-010…017/019 used `owner_decision_required: false` with "layer defines" | Yes | finding-taxonomy §1.1 paths A/B/C (C = Owner only); agent-workflow §9; NF-011/013/014/019 flagged Owner; NF-010/012/015/016/017 carry `escalation_condition`; validator rule; WP-01 proposal deliverable 1 | `test_cr002_uncertain_finding_without_escalation_is_caught` | FAILED on known-bad (rule absent), PASSED on fix |
| CR-003 closure unguarded | Yes: CLOSED, null review, no `main` → `{}` | Yes | validator: scoping/process-only closure needs exact `APPROVED` review + verdict + source; any closure needs candidates on `main`; product closure needs registry `CERTIFIED_CLOSED`; coordination-state §3 text | 7 controls (`test_cr003_*`, incl. 4 non-approval outcomes) + 1 positive control (valid closure passes) | all 7 FAILED on known-bad, PASSED on fix; positive control PASSED |
| CR-004 quarantine excludes Claude | Yes: quarantine + Claude → `[]` | Yes | guard applies to every agent; only Owner/null may own a quarantined state; coordination-state §3 | `test_cr004_quarantine_blocks_every_agent[Claude,Codex]` + positive control (Owner) | both FAILED on known-bad (Claude case is the defect; Codex message changed), PASSED on fix |
| CR-005 YAML tags/anchors accepted | Yes: `!!str`, `&unused` accepted at loader and gate level | Yes | token-level scan rejects tag/anchor/alias syntax before composition; surrogate code points rejected explicitly in the domain check | units: `!!str`, `&unused`, `!local`, `&x/*x`, `!!binary`; gate: `test_cr005_explicit_tag_or_anchor_in_scenario_is_caught[2]` | all FAILED on known-bad, PASSED on fix |
| CR-006 learner metadata in core checkpoint | Yes: PERS-009 required fitted parameters from R04 §33 for every profile | Yes | PERS-009 now profile-neutral (declared family + dependencies, cites R04 §41.1, R05 §12); new LMEM-015 carries learner specifics (R02 §11, R04 §28/§33, IAA §2/A15) | documentary | NOT_APPLICABLE — documentary |
| CR-007 episode order broadened | Yes: sources scope ordering to episode events | Yes | HIST-003 rewritten episode-scoped, profile learning, layer 08; HIST-005 wording "devices or episodes"; NF-016 qualified | documentary | NOT_APPLICABLE — documentary |
| CR-008 FROZEN scope / EVID-006 citations | Yes for both | Yes | KNOW-011 → NORMATIVE with its FROZEN sentence named; EVID-006 cites FND §8/§14. **Neighborhood re-audit** of all remaining FROZEN labels found six more with the same defect (FROZEN box covers only an adjacent sentence): OBS-004, EVID-002, CORE-004, LMEM-011, LMEM-012, ARCH-011 → NORMATIVE | documentary | NOT_APPLICABLE — documentary |
| CR-009 materiality qualifier | Yes: R05 §11 has no materiality exemption | Yes | ACTX-003 aligned to R05 §11; FND G.4 minimum noted | documentary | NOT_APPLICABLE — documentary |
| CR-010 evaluation discipline omitted | Yes: FND §15/§15.1 bullets untranscribed | Yes | new LMEM-014 with source modal strength ("prefer", "use … when"); MVP §10 deferral noted | documentary | NOT_APPLICABLE — documentary |
| CR-011 endpoint-only state check | Yes: content change + exact revert passes endpoint diff | Yes (non-blocking) | validator checks **every** commit in `D..ref`; coordination-state §2 rewritten (descendant chain; review records are content, not state) | `test_cr011_content_change_then_revert_after_candidate_is_caught` + positive multi-commit chain | FAILED on known-bad, PASSED on fix |
| CR-012 "Rust not created" | Yes | Yes (non-blocking) | wording in code README, `minion-memory-rust/README.md`, `plans/WP-00.md`. Note: the Rust README is a Claude-authored placeholder; only its wording changed, no Rust code exists | documentary | NOT_APPLICABLE |
| CR-013 H5 missing from WP-01 | Yes | Yes (non-blocking) | WP-01 proposal deliverable 2 adds H5 | documentary | NOT_APPLICABLE |

**Questions in the review:**
- *Lone surrogate accepted by the loader* — **confirmed.** Claude's first probe said "rejected", but
  that was an escaping artifact in Claude's own shell probe. Run from a file (as the test does), the
  candidate loader accepts `a: "\uD800"`. Now rejected explicitly (`_has_surrogate`), with 3 YAML and
  3 direct domain witnesses that FAILED on known-bad. NF-019 still owns the payload value-domain
  decision (path C); this rule constrains only the canonical/governance YAML profile, which both
  languages must be able to read.
- *List-valued status → TypeError* — confirmed; now reported as `unknown status`, never an internal
  error (`test_malformed_status_type_is_reported_not_crashed`, FAILED on known-bad).

Control recipe: copy fixed `checks.py`/`yamlcore.py` aside; replace them with
`git show 42f5193:process/tools/src/mneme_process/{checks,yamlcore}.py`; run
`uv run pytest -o addopts="-p no:cacheprovider" -q -k "cr00 or cr011 or malformed_status or rejects_lone or explicitly or rejects_nonportable" --runxfail`;
observed 25 failed (every control above) / 13 passed (positive controls and pre-existing unit cases);
restore the fixed files and confirm `git diff` shows them restored; full suite green. Baseline of
each control is asserted by the fixture before mutation. No `xfail` markers are involved.

## 3. Positions on NF-001…NF-021 (from the review)

Adopted: NF-002, NF-003, NF-004, NF-009 → `SEMANTICS_NEUTRAL_HARDENING` (no longer blocking);
NF-007, NF-012, NF-016 text qualified; NF-008 Owner flag set; escalation conditions per §2 above.
NF-021: the kickoff wording is now recorded verbatim (`reference/governance/...` G-007). All NFs
remain OPEN; none is self-closed.

## 4. Neighborhood re-check after the fixes

- State validator: every rule touched (status shape, closure, quarantine, chain) has positive and
  negative controls; existing state controls still pass.
- YAML boundary: anchors with aliases, tags (`!!binary`, `!!str`, local `!x`), duplicate keys,
  YAML 1.1 ambiguity, depth, surrogates — all covered; an astral scalar (`\U0001F600`) is still
  accepted (positive control).
- Spec: status labels re-audited across all FROZEN requirements (not only the two cited); citations
  re-resolved mechanically; manifest regenerated (224 rows) and bijection re-checked.
