# CODEX HANDOFF — WP-P01 CONVERGENCE CE-P01-01: CHARACTERIZATION PASS

**Issued by:** Claude (coordinator), 2026-10-10. **Task type:** convergence characterization
(adopted Minion-Agent agent-workflow §11.8.3), by Owner decision **G-018**
(`reference/governance/2026-10-10-owner-wpp01-convergence-and-wp01-parallel.md`).

## Prompt (ready to run)

You are **Codex**. WPP01-CR-001 and WPP01-CR-002 survived three independent reviews. The Owner
ruled (G-018) that this shows the **characterization of the validator trust boundary is
incomplete**, and assigned you, as the reviewer who discovered the defects, to produce the
**exhaustive characterization matrix**. Claude will then independently challenge completeness and
classify every row; only after a two-party checkpoint does Claude implement, once.

### 1. Exact reference

| Item | Value |
|---|---|
| Docs | `minion-memory-docs`, ref `wpP01/hardening`, **`1422423e8fd7b163f498466d6596e3ef5741c53d`**: the frozen validator surface (tooling byte-identical to `a9ed71d2`) + your review-2 record + G-018/G-019 |
| Code | `bb05e3953a044ea8abd9d796675290ad9fe80941` = `main` |
| Frozen surface | `process/tools/src/mneme_process/{checks,cli,yamlcore,sources,spec,transitions}.py`, `process/coordination-state.md` §2–§4 — **no production edits by anyone** until `AGREED FOR IMPLEMENTATION` |

Preflight (else `HANDOFF_BLOCKED`): SHAs exist; every commit in `1422423e..wpP01/hardening` is
state/hand-off only; trees clean.

### 2. What to characterize (G-018 dimensions)

Every relevant **input source** × **path-eligibility rule** × **state field** × **git ref namespace**
× **resolution path**, and **all malformed/ambiguous cases**. At minimum:

- **Input sources:** every git invocation in the validator (each call site), every state-file field
  that reaches a git argument or a comparison, every CLI argument, every filesystem enumeration
  (`glob`, `rglob`, `is_dir`) whose result is compared to git output.
- **Path eligibility:** the predicate each inventory applies (extension case, hidden files,
  directories, symlinks, nested paths, NUL/newline/quote/leading-space/non-ASCII/Unicode
  normalization, Windows case-insensitivity, reserved names), and whether both sides of every
  comparison apply the **same** predicate.
- **State fields:** `current_candidate.{code,docs}.{repo,ref,sha}`, presence/absence/null/empty,
  type confusion (list, int, bool), unknown sides, duplicate keys (already rejected by the YAML
  boundary: confirm), and per-status requirements (active, CLOSED, WAITING_FOR_TRIGGER,
  BLOCKED_FOR_OWNER).
- **Ref namespaces and resolution:** for each ref-consuming call, which namespace it resolves in
  (`refs/heads`, `refs/tags`, `refs/remotes`, `HEAD`, packed refs, symbolic refs, `@`, reflog
  `@{n}`, `^`/`~` suffixes, ambiguous short SHAs), and whether the object proven by one call is the
  object used by the next (check-then-use binding).
- **Host variants:** Windows (this host) and case-sensitive POSIX; `core.quotePath`,
  `core.ignorecase`, `core.precomposeunicode` settings.

### 3. Required artifact

`assurance/convergence/CE-P01-01-characterization.md` with these sections (adopted §11.8.1):

```text
OPEN FINDINGS            WPP01-CR-001, WPP01-CR-002 (+ any new IDs WPP01-CR-003…)
ROOT-CAUSE SURFACE       one paragraph
SOURCES AUDITED          file:line at 1422423e for every call site / field
OBSERVABLE RULES         the rules the validator must enforce (numbered R1…)
BEHAVIOR MATRIX          one row per (input × case): id, input, case, current behavior at
                         1422423e (EXECUTED, with the probe), required behavior (rule ref),
                         realistic wrong implementation, discriminating witness
NEGATIVE CONTROLS        the controls the implementation must ship, each tied to a row
IMPLEMENTATION CONSTRAINTS  e.g. "resolve refs/heads/<ref> to a commit id once, use only the id"
OUT-OF-SCOPE / DEFERRED  with reason + trigger
```

Every "current behavior" cell must come from an **executed** probe at `1422423e` (scratch under
`E:\AI\Projects\OpenMinds\Minions\Minion-Memory\.tmp\work\codex\`), not from reading code alone
(adopted §9.3). Do **not** propose code; propose rules, cases and witnesses. Do not reopen proven
WP-P01 items (WP00-CR-014, UTF-8 decoding, the CLOSED-exemption concept) unless the
characterization produces contradictory evidence; if it does, say so explicitly.

### 4. Delivery

Commit the artifact on a **new branch `review/wpP01-ce1`** from the current `wpP01/hardening` head
(that file only); report its SHA. No verdict is due — this is a characterization, not a review.
OWN-001 applies. No edits to the frozen surface or any Claude-owned file; no WP-01.

### 5. LOOP-BACK NOTIFICATION (required)

When finished or blocked, notify Claude in the Herdr "Python" tab with your herdr skill
("/herdr send prompt to Python tab (Claude) to notify task completion") or:

```sh
herdr agent prompt w6:p1 "CODEX -> CLAUDE: CE-P01-01 characterization finished. Artifact: assurance/convergence/CE-P01-01-characterization.md on review/wpP01-ce1 at <sha>. Rows: <n>. New findings: <IDs or none>. Please run the challenge pass."
```

Verify once with `herdr agent read w6:p1 --source recent-unwrapped --lines 20`; if unsubmitted,
`herdr agent send-keys w6:p1 enter`. If Claude's pane is blocked by a dialog, wait ~2 minutes and
retry once; never answer Claude's dialog; never `--wait`.
