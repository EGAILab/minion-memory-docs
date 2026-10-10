# WP-P01 — Remediation 5: recheck regression R1 (Claude)

**Governs:** G-018, G-024 and Owner **G-027**: fix only R1, reproduced first, then Codex rechecks
R1/CR-001 and its direct regressions. **Input:** Codex recheck `e557098b` (CHANGES_REQUIRED, R1
only).
- Codex closed: WPP01-CR-002, CR-003 and CR-004; CR-005 and CR-006 remain closed.
- Codex resolved: CL-002 through CL-005; the CL-001 original witnesses are resolved.

## R1

**Defect.** The nested-marker scan (`checks._nested_markers`, introduced by remediation 4) used
`os.walk` with its default error handling, which silently skips a directory it cannot read. An
incomplete scan therefore reported "no nested repository" (D16 with D13).

**Reproduced first.** `test_R1_unreadable_directory_in_nested_marker_scan_is_a_named_error`
injects a `PermissionError` into `os.scandir` for one directory holding a real `.git` marker.
- It was executed against the unchanged candidate `c9be60e8` and **failed** there: after the
  baseline refusal, `check_repos` returned no error.
- The no-marker positive `test_R1_complete_scan_without_marker_still_passes` passed there.

**Fix.** `os.walk(..., onerror=...)` records every unreadable directory, and `check_repos`
reports each one as `<side> repo: cannot scan <dir> for nested repositories (...)`. The
exact-name rule (`.GIT` is not a marker) and the root administrative marker are unchanged.

## Evidence (Windows, Python 3.12.8, Git 2.55.0.windows.1)

- Closure controls on the fix: 13 passed.
- Lint and mypy clean.
- Full suite: **268 passed, 5 skipped** (the P09a–P13a DIAG names); real `check --deep-sources`: 8/8 PASS.
- No POSIX execution is claimed.
