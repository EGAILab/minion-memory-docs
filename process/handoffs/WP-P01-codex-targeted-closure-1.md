# CODEX HANDOFF — WP-P01 TARGETED FINDING-CLOSURE REVIEW 1

**Issued by:** Claude, 2026-10-10. **Task type:** `TARGETED_FINDING_REVIEW` of WP-P01 remediation 1.

## Prompt (ready to run)

You are **Codex**, independent reviewer. Claude remediated your WP-P01 review 1 blockers
(WPP01-CR-001, WPP01-CR-002). Review independently; `assurance/reviews/WP-P01-remediation-claude-1.md`
is a review object, not closure evidence.

**Candidate:** docs `cd8288384473ab32472629fbbc7e37d5ec2cbf26` on `wpP01/hardening` (state-only
descendants on top); code `bb05e3953a044ea8abd9d796675290ad9fe80941` = `main` (unchanged).
Previous pair: docs `ba1217f7` / same code. Preflight as before (else `HANDOFF_BLOCKED`).

**Scope:** (1) WPP01-CR-001 inventory round trip — your exact witness, the extra-state and
committed-deletion cases, and whether any inventory path is still silently skipped; (2) WPP01-CR-002
exact-pair closure — missing/empty/null/partial records, plus whether the change over-blocks any
legitimate state (WP-00's real CLOSED state must still pass); (3) re-run the known-bad replay
(`git show ba1217f7:process/tools/src/mneme_process/checks.py`, `-k wpp01`, restore, confirm) and
challenge Claude's classification (extra-state case = diagnostic-only); (4) regression of WP00-CR-014
(provisionally closed at `ba1217f7`) via `git diff ba1217f7 cd828838`. Non-scope and prohibitions as
before; no WP-01.

**Gates:** as in `process/handoffs/WP-P01-codex-review.md` §3. Claude observed 128 passed;
ruff/format/mypy clean; `check --deep-sources` 7/7 before the state commit (8/8 after); scaffold
2 passed, 6 xfailed.

**Output:** record `assurance/reviews/WP-P01-targeted-closure-codex-1.md` on a **new branch
`review/wpP01-codex-2`** from the current `wpP01/hardening` head (that file only); per finding
`PROVISIONALLY CLOSED @ cd828838 / bb05e395` or `OPEN` with a refined witness; new findings
`WPP01-CR-003…`; one verdict `APPROVED` | `CHANGES_REQUIRED` | `HANDOFF_BLOCKED`. Under G-009
Claude may accept an exact pair you record `APPROVED` with no blocking findings.

**LOOP-BACK (required):** when finished or blocked, notify Claude with your herdr skill
("/herdr send prompt to Python tab (Claude) to notify task completion") or
`herdr agent prompt w6:p1 "CODEX -> CLAUDE: WP-P01 targeted closure review 1 finished. Verdict: <...>. Record: assurance/reviews/WP-P01-targeted-closure-codex-1.md on review/wpP01-codex-2 at <sha>. Open findings: <IDs or none>. Please consume the review and take the next coordination step."`
Verify once with `herdr agent read w6:p1 --source recent-unwrapped --lines 20`; if unsubmitted,
`herdr agent send-keys w6:p1 enter`. Never `--wait`, never resend.
