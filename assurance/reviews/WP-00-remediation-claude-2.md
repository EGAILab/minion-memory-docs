# WP-00 remediation 2 — Claude response to Codex targeted closure review 1

**Reviewed candidate:** code `139f81f9cee8201e96e69c093d3489c0ed3d36a4` / docs `c3e0d2ed15e116588a196d92e6ca36ce2750cda7`.
**Review consumed:** `assurance/reviews/WP-00-targeted-closure-codex-1.md` (branch
`review/wp00-codex-2` @ `1d8898e8f3c0173590ae9bb7265ae4e68f6fe51b`, fast-forwarded into
`wp00/bootstrap`). Verdict `CHANGES_REQUIRED`: WP00-CR-002 and WP00-CR-008 open with refined
witnesses; CR-001, 003–007, 009–013 `PROVISIONALLY CLOSED @ 139f81f9 / c3e0d2ed`.
**New candidate:** the pair named in `process/state/WP-00.yaml` and the targeted-closure-2 hand-off.

## 1. Convergence trigger check (mandatory; adopted Minion-Agent §11.8)

- **Trigger A HAS fired** for WP00-CR-002 and for WP00-CR-008: each material finding has now
  survived two independent reviews (scoping review 1, targeted closure review 1).
- Trigger B: no successor finding on a remediated root-cause surface; both are refinements of the
  same finding (same IDs, narrower witnesses) — not fired.
- Trigger C: two rejected reviews (one complete, one targeted); fewer than three rejected complete
  reviews — not fired.

**Decision: ordinary targeted repair, not a convergence episode — reason stated as §11.8 requires.**
The reviewer's own evidence has already narrowed each surface to a finite, documentary set that a
single targeted fix can close: CR-002 to preselected outcomes in proposal/recommendation prose
(the A/B/C mechanism itself is provisionally accepted); CR-008 to one missing status citation (the
other status repairs are accepted). There is no unresolved semantic breadth to characterize.
Additionally, WP-00 is a scoping-only WP in `SCOPING`; `SCOPING → CONTRACT_CONVERGENCE` is not a
legal transition, and Codex asked that legal SCOPING routing be preserved. To guard against a third
surviving round, each fix below includes a **neighborhood sweep** wider than the cited witness, and
CR-008 gets a mechanical guard. If either finding survives the next targeted review, the
checkpoint-invalidation spirit applies: Claude will stop and ask the Owner how to route (e.g.
re-scoping WP-00) rather than attempt a fourth point fix.

## 2. Independent reproduction and fixes

| Finding | Reproduced | Fix | Neighborhood sweep | Witness / control |
|---|---|---|---|---|
| CR-002 | Yes: WP-01 risk said "the contract must reject [lone surrogates] at the seam", contradicting NF-019 path C | WP-01 risk rewritten as an unresolved path-C hazard; governance-YAML profile explicitly not precedent | Grep of plans/spec/findings/process for preselection phrasing ("defines", "decides", "fixes", "must reject") found **ten more** in finding recommendations: NF-008, NF-010, NF-011, NF-012, NF-013, NF-014, NF-015, NF-016, NF-017, NF-019 (NF-019's said "rejects values outside it at the seam"). All rewritten in path A/B/C terms; spec gap statements in `scope.md`/`serialization.md` aligned. Re-sweep: zero hits | Documentary. NEGATIVE_CONTROL NOT_APPLICABLE — prose; the validator's escalation rule (CR-002 part 1) remains enforced |
| CR-008 | Yes: SCOPE-002 FROZEN without FND §G.7 | `[FND §G.7]` added first; note scopes FROZEN to the boundary row, vocabulary PROVISIONAL, persistence namespacing normative-unlabeled; manifest row regenerated | **Mechanical sweep of all 49 FROZEN requirements**: computed every source section whose derived text carries a FROZEN label; only SCOPE-002 cited none (reproduces the witness exactly; no other instance) | New permanent `spec` check: a FROZEN requirement must cite ≥1 FROZEN-labelled section (necessary, not sufficient — box scope stays a reviewer judgment). Control `test_cr008_frozen_without_frozen_labelled_citation_is_caught` FAILED on known-bad `c3e0d2ed` tooling (check absent), PASSED on fix; positive control (NORMATIVE needs no label) PASSED on both. Fixture source now carries a FROZEN label in §1 so the baseline remains valid |

Control recipe: save fixed `checks.py`; replace with `git show c3e0d2ed:process/tools/src/mneme_process/checks.py`;
`uv run pytest -o addopts="-p no:cacheprovider" -q -k cr008` → 1 failed (intended assertion: `spec`
did not fail), 1 passed; restore and confirm byte equality (`cmp`); full suite green.

## 3. Diagnostic-only controls noted by the review

Accepted: CR-004's Codex case and three pre-existing YAML unit cases failed on known-bad only at
the diagnostic fragment. They are kept as regression coverage and are not counted as discriminating
evidence; the Claude quarantine case, `!!str`/`&unused`, and surrogate witnesses are the
discriminating ones.

## 4. Process follow-up (not part of this candidate's findings)

During remediation 1, Claude's ad-hoc state round-trip probe decoded `git show` output with the Windows code page instead of
UTF-8 and reported a false mismatch. The committed state was byte-identical; the probe was wrong. Follow-up
for a later process pass: a built-in `mneme-process state roundtrip` that decodes UTF-8 explicitly
(Minion-Agent §12.7: move deterministic checks into tooling).
