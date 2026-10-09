# CODEX HANDOFF — WP-00 TARGETED FINDING-CLOSURE REVIEW 2

**Issued by:** Claude (coordinator), 2026-10-09. **Task type:** `TARGETED_FINDING_REVIEW` of
remediation 2 (WP-00, scoping-only, `SCOPING`).

---

## Prompt (ready to run)

You are **Codex**, independent reviewer for Minion-Memory. Claude remediated the two findings
your targeted closure review 1 left open (WP00-CR-002, WP00-CR-008). Review independently; Claude's
record `assurance/reviews/WP-00-remediation-claude-2.md` is a review object, not closure evidence.

### 1. Exact candidate

| Item | Value |
|---|---|
| Code | `minion-memory`, ref `wp00/bootstrap`, **`bb05e3953a044ea8abd9d796675290ad9fe80941`** (previous `139f81f9…`) |
| Docs content | `minion-memory-docs`, ref `wp00/bootstrap`, **`237948fee550b691d0e83defb6c49186a27af3b8`** (previous `c3e0d2ed…`; includes your record `1d8898e` fast-forwarded in) |
| Bundle / process pin | unchanged |

Preflight (else `HANDOFF_BLOCKED`): SHAs exist and are reachable from `wp00/bootstrap`; every
commit in `237948fe..wp00/bootstrap` touches only state/hand-off paths; trees clean.

### 2. Scope

1. **WP00-CR-002** — your refined witness (WP-01 preselecting lone-surrogate rejection) plus the
   neighborhood Claude swept: ten finding recommendations (NF-008, NF-010…NF-017, NF-019) and the
   gap statements in `spec/scope.md` / `spec/serialization.md`. Is any observable choice still
   preselected anywhere in operative text?
2. **WP00-CR-008** — SCOPE-002 now cites `[FND §G.7]` with a scope note; manifest row regenerated.
   New `spec` check: a FROZEN requirement must cite ≥1 FROZEN-labelled section (necessary, not
   sufficient). Verify the check, its fixture change (fixture §1 now carries a FROZEN label), and
   re-run its control recipe (remediation record §2; known-bad = `c3e0d2ed` `checks.py`; restore
   and confirm).
3. **Convergence decision** — Claude recorded that trigger A fired for both findings and gave a
   reason for ordinary targeted repair (remediation record §1). Judge whether that reason is
   adequate under adopted §11.8.
4. Regression: the 11 findings you provisionally closed at `139f81f9 / c3e0d2ed` — confirm the diffs
   `c3e0d2ed..237948fe` and `139f81f9..bb05e395` did not reopen them.

Non-scope and prohibitions as before (no implementation, no Rust workspace, no edits to
Claude-owned files, no touching `wp00/bootstrap`/`main`, no bundle edits, no WP-01).

### 3. Gates (sequential, OWN-001)

Same commands as `process/handoffs/WP-00-codex-targeted-closure-1.md` §3. Claude observed:
tool tests **98 passed**; ruff/format/mypy clean; `mneme-process check --deep-sources` 7/7 before the
state commit (8/8 expected after); Python scaffold 2 passed, 6 xfailed.

### 4. Output

1. Record `assurance/reviews/WP-00-targeted-closure-codex-2.md` on a **new branch
   `review/wp00-codex-3`** from the current `wp00/bootstrap` head (that file only); report its SHA.
2. Per finding: `PROVISIONALLY CLOSED @ bb05e395 / 237948fe` with verified evidence, or `OPEN` with a
   refined discriminating witness. New findings: `WP00-CR-014…`.
3. One verdict: `APPROVED` (all WP00-CR findings provisionally closed, no new blocker, and this
   exact pair is the approved WP-00 scoping artifact) | `CHANGES_REQUIRED` | `HANDOFF_BLOCKED`.
   `APPROVED` approves the candidate only; acceptance onto `main` is the Owner's.

### 5. LOOP-BACK NOTIFICATION (required)

When finished or blocked, notify Claude in the Herdr "Python" tab with your herdr skill
("/herdr send prompt to Python tab (Claude) to notify task completion") or:

```sh
herdr agent prompt w6:p1 "CODEX -> CLAUDE: WP-00 targeted closure review 2 finished. Verdict: <APPROVED|CHANGES_REQUIRED|HANDOFF_BLOCKED>. Record: assurance/reviews/WP-00-targeted-closure-codex-2.md on review/wp00-codex-3 at <sha>. Open findings: <IDs or none>. Please consume the review and take the next coordination step."
```

Verify once with `herdr agent read w6:p1 --source recent-unwrapped --lines 20`; if unsubmitted,
`herdr agent send-keys w6:p1 enter`. Never `--wait`, never resend.
