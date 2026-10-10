# CODEX HANDOFF — WP-P01 REVIEW (independent, complete for this small WP)

**Issued by:** Claude (coordinator), 2026-10-10. **Task type:** `SCOPING_REVIEW` of process-only
WP-P01 (`requirements: []`, status `SCOPING`), created by Owner decision G-011.

---

## Prompt (ready to run)

You are **Codex**, independent reviewer for Minion-Memory. WP-00 is CLOSED and accepted
(`main`: code `bb05e395`, docs `237948fe`). Claude implemented WP-P01, which carries forward your
non-blocking WP00-CR-014 and three process items. Review it independently and completely (it is
small); Claude's plan `plans/WP-P01.md` is a review object.

### 1. Exact candidate

| Item | Value |
|---|---|
| Code | `minion-memory`, **`bb05e3953a044ea8abd9d796675290ad9fe80941`** = `main` (unchanged by WP-P01) |
| Docs content | `minion-memory-docs`, ref `wpP01/hardening`, **`ba1217f76ef311f3ba0df749e43291b75fb2e0b4`** |
| Review diff | `git diff 237948fe ba1217f7` (includes WP-00 post-acceptance records already governed by G-008..G-011 — review them only for accuracy, not as new decisions) and specifically `git diff 21fcb416 ba1217f7` (the WP-P01 change itself) |
| Governance | `reference/governance/2026-10-10-owner-wp00-acceptance.md` (G-008..G-011) |

Preflight (else `HANDOFF_BLOCKED`): SHAs exist; `ba1217f7` reachable from `wpP01/hardening`;
every commit in `ba1217f7..wpP01/hardening` touches only state/hand-off paths; trees clean.

### 2. Scope

1. **WP00-CR-014** — `has_positive_frozen_label` (`process/tools/src/mneme_process/checks.py`):
   is the positive-label grammar right for the real bundle (status boxes, status registers,
   `FROZEN —` lines, scoped `FROZEN boundary / …`), and does it correctly exclude `NOT FROZEN`,
   prose/cell mentions and Appendix E `->` change records? Do all 49 FROZEN requirements still
   cite a positively labelled section *legitimately* (not just mechanically)? Is `spec/README.md` §3
   accurate about the guard's guarantee (necessary, not sufficient)?
2. **State round trip** — `mneme-process state roundtrip`: raw bytes, explicit UTF-8, CRLF/LF
   normalized, semantic equality. Is ignoring CRLF/LF-only differences sound under the commit rule
   (coordination-state §4), or does it hide a real failure? Also the validator's `_git` now decodes
   UTF-8 explicitly.
3. **CLOSED-state rule** — `check_state` skips the state-only descendant rule for `CLOSED` states,
   relying on `main` ancestry (coordination-state §2 "After acceptance"). Can an active state
   exploit it? Is acceptance evidence still enforced?
4. **Record landing** — accepting this candidate fast-forwards docs `main` from `237948fe` to
   `ba1217f7`, landing WP-00's post-acceptance records. Confirm the chain is linear and the records
   are accurate (no record claims more than its source).
5. **Controls** — re-run the known-bad replay yourself (known-bad = `git show
   237948fe:process/tools/src/mneme_process/checks.py`; restore and confirm). Claude's
   classification: discriminating = 3 CR-014 negatives + CLOSED post-acceptance positive;
   feature-absent (not counted) = 11 label-rule units + 4 round-trip tests; pass-on-both = 2
   positive label forms, NORMATIVE-only, active-state chain negative. Challenge it.

Non-scope: spec semantics, product code, any Layer-01 decision. No implementation, no edits to
Claude-owned files, no touching `wpP01/hardening`/`wp00/bootstrap`/`main`, no bundle edits, no WP-01.

### 3. Gates (sequential, OWN-001)

Same commands as `process/handoffs/WP-00-codex-targeted-closure-1.md` §3, plus
`uv run mneme-process state roundtrip --docs ../..`. Claude observed: tool tests **121 passed**;
ruff/format/mypy clean; `check --deep-sources` 7/7 before the state commit (8/8 expected after);
Python scaffold 2 passed, 6 xfailed.

### 4. Output

1. Record `assurance/reviews/WP-P01-review-codex-1.md` on a **new branch `review/wpP01-codex-1`**
   from the current `wpP01/hardening` head of the docs repo (that file only); report its SHA.
2. Findings use IDs `WPP01-CR-001…` in the established format (classification, blocking, sources,
   witness, recommendation).
3. One verdict: `APPROVED` | `CHANGES_REQUIRED` | `HANDOFF_BLOCKED`. Under standing delegation
   G-009 Claude may accept an exact pair you record `APPROVED` with no blocking findings.

### 5. LOOP-BACK NOTIFICATION (required)

When finished or blocked, notify Claude in the Herdr "Python" tab with your herdr skill
("/herdr send prompt to Python tab (Claude) to notify task completion") or:

```sh
herdr agent prompt w6:p1 "CODEX -> CLAUDE: WP-P01 review finished. Verdict: <APPROVED|CHANGES_REQUIRED|HANDOFF_BLOCKED>. Record: assurance/reviews/WP-P01-review-codex-1.md on review/wpP01-codex-1 at <sha>. Open findings: <IDs or none>. Please consume the review and take the next coordination step."
```

Verify once with `herdr agent read w6:p1 --source recent-unwrapped --lines 20`; if unsubmitted,
`herdr agent send-keys w6:p1 enter`. Never `--wait`, never resend.
