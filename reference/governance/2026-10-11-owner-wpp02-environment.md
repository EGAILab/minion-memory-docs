# Owner decision — WP-P02 environment hardening (2026-10-11)

Recorded verbatim by Claude.

## G-045 — Fix the two carried items

**Context.** Claude's WP-01 closing report listed two open items:
1. **NF-023:** add `CARGO_HOME` to the environment script and pin the project's own Python.
2. **System Python:** `E:\AI\Python\Python312` is damaged and needs repairing outside the project.

> **Owner:** "Fix two items"

**Scope.**
- **Item 1** becomes WP-P02, a process-only WP, `requirements: []`. It changes
  `process/environment/project-environment.{sh,ps1}` and the interpreter row of
  `plans/toolchain-proposal.md`. Like every process change it is independently reviewed by Codex
  before acceptance under G-009.
- **Item 2** is outside both repositories. It is done on the Owner's machine and reported in the
  WP-P02 record, with no project artifact other than that report.
