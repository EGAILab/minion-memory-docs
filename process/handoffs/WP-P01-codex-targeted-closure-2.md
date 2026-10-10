# CODEX HANDOFF — WP-P01 TARGETED FINDING-CLOSURE REVIEW 2

**Issued by:** Claude, 2026-10-10. **Task type:** `TARGETED_FINDING_REVIEW` of WP-P01 remediation 2.

## Prompt (ready to run)

You are **Codex**, independent reviewer. Convergence trigger A has fired for WPP01-CR-001 and
WPP01-CR-002. Claude recorded the trigger and its route before remediating: characterize the
validator's whole trust surface (every input from git output or state records), then fix once.
Review independently; `assurance/reviews/WP-P01-remediation-claude-2.md` is a review object.

**Candidate:** docs `a9ed71d2f943c3fb5dc32f51fb7d5db99291abcb` on `wpP01/hardening` (state-only
descendants on top); code `bb05e3953a044ea8abd9d796675290ad9fe80941` = `main` (unchanged). Previous:
docs `cd828838`. Preflight as before (else `HANDOFF_BLOCKED`).

**Scope:**
1. Your refined witnesses for WPP01-CR-001 (quoted non-ASCII inventory under `core.quotePath=true`)
   and WPP01-CR-002 (side/repository binding).
2. **The characterization itself** (remediation record §2, 8 rows). Is any input missing? Is each
   disposition right, including the new ref-SHA chain-bypass Claude found and the DEFERRED macOS
   normalization row? Judge whether the route decision (§1) was adequate.
3. Over-blocking: WP-00's real CLOSED state and WP-P01's real active state must still pass; the
   corrected closure fixtures (positive uses `ref: main`; the acceptance negative uses an orphan
   `main`) must test what they claim.
4. Re-run the known-bad replay (`git show cd828838:process/tools/src/mneme_process/checks.py`,
   `-k wpp01_r2`, restore, confirm) and challenge Claude's classification: 10 discriminating,
   7 diagnostic-only.
5. Regression of WP00-CR-014 via `git diff cd828838 a9ed71d2`.

Non-scope and prohibitions as before; no WP-01. **Escalation note:** if either finding survives this
review, Claude stops and routes the decision to the Owner; record any surviving witness precisely
for that purpose.

**Gates:** as in `process/handoffs/WP-P01-codex-review.md` §3. Claude observed: tool suite
**145 passed** (on byte-identical tooling/tests); ruff/format/mypy clean; `check --deep-sources` 7/7
before the state commit (8/8 after); scaffold 2 passed, 6 xfailed. The suite takes ~10 minutes.

**Output:** record `assurance/reviews/WP-P01-targeted-closure-codex-2.md` on a **new branch
`review/wpP01-codex-3`** from the current `wpP01/hardening` head (that file only); per finding
`PROVISIONALLY CLOSED @ a9ed71d2 / bb05e395` or `OPEN` with a refined witness; new findings
`WPP01-CR-003…`; one verdict `APPROVED` | `CHANGES_REQUIRED` | `HANDOFF_BLOCKED`.

**LOOP-BACK (required):** when finished or blocked, notify Claude with your herdr skill
("/herdr send prompt to Python tab (Claude) to notify task completion") or
`herdr agent prompt w6:p1 "CODEX -> CLAUDE: WP-P01 targeted closure review 2 finished. Verdict: <...>. Record: assurance/reviews/WP-P01-targeted-closure-codex-2.md on review/wpP01-codex-3 at <sha>. Open findings: <IDs or none>. Please consume the review and take the next coordination step."`
Verify once with `herdr agent read w6:p1 --source recent-unwrapped --lines 20`. If unsubmitted, run
`herdr agent send-keys w6:p1 enter`. If Herdr reports Claude's pane as **blocked** (a question
dialog is open), wait ~2 minutes and retry the same notification once; do not answer Claude's
dialog. Never `--wait`, never resend otherwise.
