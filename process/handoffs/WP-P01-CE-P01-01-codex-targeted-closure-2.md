# Hand-off — WP-P01 CE-P01-01 targeted closure recheck (Codex)

**From:** Claude. **To:** Codex. **Governs:** G-018 and Owner **G-024**. The verbatim G-024 record
is in `reference/governance/2026-10-10-owner-wpp01-convergence-and-wp01-parallel.md`, inside the
candidate.

**Exact pair:**
- docs: `c9be60e833d42c3981fb271e6882b0017b55c781` (on `wpP01/hardening`; state-only descendants follow);
- code: `bb05e3953a044ea8abd9d796675290ad9fe80941` (unchanged).

**Record under review:** `assurance/reviews/WP-P01-remediation-claude-4.md`, with controls in
`process/tools/tests/test_ce_p01_01_closure.py`.

## Scope (per G-024: a targeted recheck, not a second full G-018 review)

1. **CL-001…CL-005.** Check whether each is resolved by your own executions, on Windows and on a
   case-sensitive POSIX host.
2. **Still-open findings.** Check whether WPP01-CR-001…004 can now be closed against the agreed
   matrix.
3. **Direct regressions from this fix pass.** One neighbourhood item was added beyond the five:
   the workspace-containment query in `check_repos` now refuses on a failed query. It has its
   own control; please judge whether it is in the agreed scope.

CR-005 and CR-006 stay closed unless new evidence specifically contradicts their closure.

If any item could only be fixed by deciding previously unspecified semantics, report it as a
convergence reopening, not as an implementation defect (G-024).

## Verdict

Record `assurance/reviews/WP-P01-CE-P01-01-targeted-closure-codex-2.md` on a new branch
`review/wpP01-ce1-closure-2` from the docs state head. Give per-finding dispositions and an
overall verdict of `APPROVED` or `CHANGES_REQUIRED` for the exact pair.

Approval is not acceptance. Do not modify production modules or the WP-01 worktrees.
