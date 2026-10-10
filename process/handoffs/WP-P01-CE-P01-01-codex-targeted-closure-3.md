# Hand-off — WP-P01 CE-P01-01 recheck of R1 (Codex)

**From:** Claude. **To:** Codex. **Governs:** G-018, G-024 and Owner **G-027** ("Fix only R1 ...
Codex then rechecks only R1/CR-001 and its direct regressions"). The verbatim record is in the
candidate's governance file.

**Exact pair:**
- docs: `be2f4e29b862bfe0b5d3e57604eb0d979ac57521` (on `wpP01/hardening`; state-only descendants follow);
- code: `bb05e3953a044ea8abd9d796675290ad9fe80941` (unchanged).

**Record:** `assurance/reviews/WP-P01-remediation-claude-5.md`. **Controls:** the `R1` tests in
`process/tools/tests/test_ce_p01_01_closure.py`; the R1 control failed on `c9be60e8` first.

## Scope

R1 and WPP01-CR-001, plus direct regressions of the `_nested_markers` / `check_repos` change
only. All other findings stay as you dispositioned them in `e557098b`.

## Verdict

Record `assurance/reviews/WP-P01-CE-P01-01-targeted-closure-codex-3.md` on a new branch
`review/wpP01-ce1-closure-3` from the docs state head. Give an overall `APPROVED` or
`CHANGES_REQUIRED` for the exact pair, with WPP01-CR-001's disposition.

Approval is not acceptance. Do not modify production modules or the WP-01 worktrees.
