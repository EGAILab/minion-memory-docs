# WP-P01 — Remediation 4: CE-P01-01 targeted-closure fixes CL-001…CL-005 (Claude)

**Governs:** G-018 and Owner **G-024**: one remediation pass limited to CL-001…005 and their direct
regression surface, with no new semantic rules; each finding reproduced at the candidate first.
**Input:** Codex targeted closure `c7dadc07` (CHANGES_REQUIRED) on candidate `db672edc`.
CR-005 and CR-006 stay closed. This is not a review and not a closure claim.

## Reproduce first (G-024)

`process/tools/tests/test_ce_p01_01_closure.py` was written and executed against the unchanged
candidate `db672edc` **before** any production edit.
- On that candidate: **10 failed, 1 passed**. The pass is the plain-branch positive control.
- Each failure is the witnessed behaviour:
  - a silent traversal of `dir.MD` / `dir.YAML`;
  - a Windows-only refusal of `.GIT`;
  - E05's inventory error missing from `check_spec`;
  - failed shallow / symbolic / containment queries reading as passes;
  - an uncaught cleanup `OSError`;
  - outside bytes changed through a staging symlink;
  - a symlinked output directory written through.

## Fixes (agreed rules only)

| Item | Rule | Fix |
|---|---|---|
| CL-001 | D16 | `spec.inventory` refuses member-suffix directories in any letter case. The nested-repository scan is an exact-name `os.walk` (`_nested_markers`), so `.GIT` is not a marker on any host. `check_spec` names the source-text inventory errors it consumes (original E05 recipe kept as a control, beside the earlier `EXTRA.MD` control). |
| CL-002 | D5/D7/D13 | `--is-shallow-repository` must succeed with `true`/`false`; anything else refuses. `symbolic-ref -q`: 0 = symbolic, 1 = plain, other = refused. **Neighborhood:** the workspace-containment query had the same defect (a failed query read as "not inside a repository"); only Git's own `not a git repository` answer now proves absence, and a localized message fails closed. |
| CL-003 | D13/D14 | Cleanup goes through `_discard`, so failures are added to the documented error (exit 1), never raised. |
| CL-004 | D14/D16 | The `reference/source-text` chain must be real directories (a symlink is refused before any write). Staging removes a stale entry itself, never its target, and creates exclusively (`O_EXCL`, plus `O_NOFOLLOW` where available). |
| CL-005 | commitment | `coordination-state.md` §3.1 states D14 (key, file and sha bounds; preflight; staging; replacement limit), D15 (`--only`, `--docs` containment, root check) and D16 (per-inventory domains, exact nested marker). Remediation record 3's statement that §§2–4 already stated all of D1–D16 was **incorrect**; this record corrects it. |

No item needed a semantic decision, so convergence was not reopened (G-024).

## Evidence

Evidence on the fixed code:
- closure controls: 11 passed;
- containment control: fails on `db672edc`, passes on the fix;
- lint and mypy clean;
- the full suite and the real deep-source check are recorded in the hand-off.

The POSIX run is still Codex's: no POSIX execution is claimed here.

Executed on Windows (Python 3.12.8, Git 2.55.0.windows.1):
- full tooling suite on the fixed code: **266 passed, 5 skipped**, no failures or errors (the
  skips are the P09a–P13a DIAG names);
- real repositories, `check --deep-sources`: 8/8 PASS.
