# Hand-off — WP-P01 CE-P01-01 targeted closure (Codex)

**From:** Claude. **To:** Codex (independent reviewer). **Governs:** G-018 ("Codex then performs
targeted closure against the agreed matrix").

## Exact candidate

- Docs: `db672edc05d15f1f2981928c86e2bb9d4224966e`, on `wpP01/hardening`. The state-only
  descendants follow it.
- Code: `bb05e3953a044ea8abd9d796675290ad9fe80941` (`main`, unchanged).
- Agreed matrix: `assurance/convergence/CE-P01-01-classification.md`, revision 2 (now inside the
  candidate).
- Implementation record: `assurance/reviews/WP-P01-remediation-claude-3.md`.

## Scope

Closure of WPP01-CR-001…006, judged only against the agreed rows, decisions D1–D16 and §5
control accounting. Do not reopen unrelated WP-P01 semantics (G-018).

Please verify independently:
- **Rows.** Every FIX and POLICY row meets its agreed oracle on this candidate. Every KEEP and
  OPAQUE row keeps its oracle. DIAG and LIMIT rows are labelled. Use your own executions; the
  controls in `process/tools/tests/test_ce_p01_01.py` are evidence to challenge, not to trust.
- **Kill run.** The recorded claim is that no FIX control passes on the frozen modules
  (`1422423e`), with 2 failing tests not kill-credited (CH11, the replace-limit test).
- **POSIX run.** I have **not** executed the POSIX / case-sensitive host run of the new controls.
  Running it is in scope.
- **Implementation choices.** Check the implementation against the agreed text, especially:
  - D7: the graft-file path and overlay refusal via `--git-common-dir`;
  - D8: the three spellings;
  - D14: preflight and the stated replace limit;
  - D16: the per-inventory domains.
- **Contract text.** Check that `coordination-state.md` states D1–D16 faithfully.

## Verdict

Record `assurance/reviews/WP-P01-CE-P01-01-targeted-closure-codex.md` on a new branch
`review/wpP01-ce1-closure` from the docs state head. Give each finding a disposition (closed or
still open, with evidence) and an overall verdict of `APPROVED` or `CHANGES_REQUIRED` for the
exact pair.

Approval is not acceptance; acceptance onto `main` follows separately under G-009. Do not modify
production modules or the WP-01 worktrees.
