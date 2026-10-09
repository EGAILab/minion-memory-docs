# CODEX HANDOFF — WP-00 TARGETED FINDING-CLOSURE REVIEW 1

**Issued by:** Claude (coordinator), 2026-10-09. **Task type:** `TARGETED_FINDING_REVIEW` of
remediation 1 for WP-00 (scoping-only WP, `requirements: []`, status `SCOPING`).

---

## Prompt (ready to run)

You are **Codex**, independent reviewer for Minion-Memory. Claude remediated your WP-00 scoping
review 1 (`CHANGES_REQUIRED`, WP00-CR-001…010 blocking, CR-011…013 non-blocking). Review the
remediation independently. Claude's remediation record is a review object, not evidence that a
finding is closed.

### 1. Exact candidate

| Item | Value |
|---|---|
| Code repo | `E:\AI\Projects\OpenMinds\Minions\Minion-Memory\minion-memory`, ref `wp00/bootstrap`, **SHA `139f81f9cee8201e96e69c093d3489c0ed3d36a4`** (previous `a91db170…`) |
| Docs repo | `E:\AI\Projects\OpenMinds\Minions\Minion-Memory\minion-memory-docs`, ref `wp00/bootstrap`, **content SHA `c3e0d2ed15e116588a196d92e6ca36ce2750cda7`** (previous `42f5193d…`; it contains your review record `07c96d6` fast-forwarded in, plus `assurance/reviews/WP-00-remediation-claude-1.md`). The state + this hand-off are state-only descendants on top of it |
| Bundle / process pin | unchanged: `mneme-v2.3-dual-profile`; `minion-agent-docs` `8744bd0…`, `minion-agent` `3de4b75…` |

Preflight (else `HANDOFF_BLOCKED`): both SHAs exist and are reachable from `wp00/bootstrap`; every
commit in `c3e0d2ed..wp00/bootstrap` touches only `process/state/**` / `process/handoffs/**`
(per commit — the rule you asked for in CR-011); both trees clean.

### 2. Scope (targeted, per process/agent-workflow §6 / Minion-Agent §11.4)

1. **Each of WP00-CR-001…013:** is it closed at this candidate? Use `git diff 42f5193d c3e0d2ed`
   and `git diff a91db170 139f81f9`. For executable findings (CR-002 validator rule, CR-003, CR-004,
   CR-005, CR-011, and the two review questions), verify the permanent witnesses and **re-run the
   negative-control recipe** in the remediation record §2 yourself (known-bad = `42f5193` tooling;
   restore afterwards and confirm the tree is clean). A control counts only if killed by its
   intended assertion — note CR-004's Codex case fails on known-bad partly because the message
   changed; judge whether the Claude case alone is the discriminating witness.
2. **Semantic dependencies touched by the fixes:** `process/finding-taxonomy.md` §1.1 (new
   escalation paths A/B/C), `process/coordination-state.md` §2/§3/§6, the findings register
   (reclassifications, `escalation_condition`s), `spec/persistence.md` PERS-009, new
   `spec/learning/inference.md` LMEM-014/LMEM-015, `spec/core.md` HIST-003/HIST-005,
   `spec/agent/context.md` ACTX-003, and the **status re-audit** beyond your citation (OBS-004,
   EVID-002, CORE-004, LMEM-011, LMEM-012, ARCH-011 downgraded; KNOW-011, EVID-006).
3. **Neighborhood:** any remaining FROZEN label still broader than its source box; any other
   requirement still assigning a path-C choice to agents; any other place where approval is
   treated as acceptance authority.

Non-scope: re-reviewing untouched surface, unless you record a concrete blast-radius reason a
fix changed it. Same prohibitions as review 1: no implementation, no Rust workspace, no edits to
Claude-owned files, no touching `wp00/bootstrap`/`main`, no bundle edits, no WP-01.

### 3. Gates (sequential, OWN-001)

```sh
. /e/AI/Projects/OpenMinds/Minions/Minion-Memory/minion-memory-docs/process/environment/project-environment.sh
cd /e/AI/Projects/OpenMinds/Minions/Minion-Memory/minion-memory-docs/process/tools
export UV_PROJECT_ENVIRONMENT="$MNEME_VENV_ROOT/mneme-process-codex"
uv sync --python 3.12 && uv run pytest     # Claude observed: 96 passed
uv run ruff check src tests && uv run ruff format --check src tests && uv run mypy src
uv run mneme-process check --docs ../.. --code ../../../minion-memory --deep-sources   # observed 8/8 after the state commit
cd ../../../minion-memory/minion-memory-python
export UV_PROJECT_ENVIRONMENT="$MNEME_VENV_ROOT/minion-memory-python-codex"
uv sync --python 3.12 && uv run pytest     # observed: 2 passed, 6 xfailed
```

Report your own fresh counts. Temp/caches/venvs/targets stay inside
`E:\AI\Projects\OpenMinds\Minions\Minion-Memory` (never C:).

### 4. Output

1. Review record `assurance/reviews/WP-00-targeted-closure-codex-1.md` committed on a **new
   branch `review/wp00-codex-2`** from the current `wp00/bootstrap` head of the docs repo (that
   file only). Report its SHA.
2. Per finding: `PROVISIONALLY CLOSED @ <code/docs SHA pair>` with the witness and negative-control
   evidence you verified, or `OPEN` with a new/refined discriminating witness (do not merely restate).
   New findings use `WP00-CR-014…` in the review-1 format.
3. Exactly one verdict:
   - `APPROVED` — every CR finding provisionally closed, no new blocker, **and** you judge the
     changed surface adequately covered so that this exact pair is the approved WP-00 scoping
     artifact (you saw the whole candidate in review 1). If you need one more complete review
     first, say so with the blast-radius reason and use `CHANGES_REQUIRED` only if something is
     actually open.
   - `CHANGES_REQUIRED` — any CR finding still open or any new blocking finding.
   - `HANDOFF_BLOCKED` — hand-off/environment invalid.
   `APPROVED` approves the candidate only; it grants no authority to accept onto `main` (Owner,
   coordination-state §6).

### 5. LOOP-BACK NOTIFICATION (required)

When finished (or `HANDOFF_BLOCKED`), notify Claude in the Herdr "Python" tab. Use your herdr skill
if available ("/herdr send prompt to Python tab (Claude) to notify task completion"), otherwise:

```sh
herdr agent prompt w6:p1 "CODEX -> CLAUDE: WP-00 targeted closure review 1 finished. Verdict: <APPROVED|CHANGES_REQUIRED|HANDOFF_BLOCKED>. Record: assurance/reviews/WP-00-targeted-closure-codex-1.md on review/wp00-codex-2 at <sha>. Open findings: <IDs or none>. Please consume the review and take the next coordination step."
```

Verify once with `herdr agent read w6:p1 --source recent-unwrapped --lines 20`; if the text sits
unsubmitted in the input box, run `herdr agent send-keys w6:p1 enter`. Never `--wait`, never resend.

---

## Candidate gate evidence (Claude, author-run; not a review)

At code `139f81f9…` / docs `c3e0d2ed…`, trees clean, sequential, OWN-001 (Windows 11, Python 3.12.8,
uv 0.10.9): tool tests **96 passed**; ruff/format/mypy strict clean (11 files formatted, 8 sources);
`mneme-process check --deep-sources` repos/sources/spec/manifest/conformance/findings/registry
**7/7** (state check runs after the state commit); Python scaffold **2 passed, 6 xfailed**; trees
clean after gates. Negative-control replay against `42f5193` tooling: 25 failed / 13 passed, as
recorded in the remediation record.
