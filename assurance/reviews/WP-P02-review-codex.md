# WP-P02 environment hardening — independent review (Codex)

Date: 2026-10-11. Reviewer: Codex (independent of Claude's changes).

## Verdict

**APPROVED** for docs `34c1b752d8d6d54a1181219eada48d07f792730f` / unchanged code
`cc3c5d549a43f166bfa1d990d3363887d5e63774`. No new findings. NF-023's requested repair is
verified; Claude may perform acceptance and closure under G-009. This review itself does not
accept onto main or start another layer.

## Scope and custody

Followed `process/handoffs/WP-P02-codex-review.md` at state head `ef68555b` and Owner G-045.
The review worktree is `review-worktrees/docs-wpp02-review`, branch `review/wpP02-env`, based
on that state head; the clean code checkout is `review-worktrees/code-wp01-cr011` at the exact
code SHA. The state-head delta adds only the WP-P02 registry entry, state and handoff.
Only this review record is changed in the repositories. Probes live in `.tmp/work/codex/`;
all probe caches, interpreter caches and build targets remain under the project root.
No production, state, registry, other worktree or system-Python repair edits were made.

## Results against the four requests

1. **NF-023:** PowerShell and Git Bash export `.tmp/cache/cargo-home`; WSL Ubuntu exports
   `.tmp/cache/cargo-home-linux` and `.tmp/cache/rustup-linux`, and resolves plain `cargo`
   through the project Cargo home. Platform-specific targets remain project-local.
   The scripts set `UV_PYTHON_PREFERENCE=only-managed`, `UV_PYTHON=3.12.8`, and preserve the
   existing project-local `UV_PYTHON_INSTALL_DIR`. Windows `uv python find --offline` in both
   PowerShell and Git Bash resolves the project's managed CPython 3.12.8.
2. **Compatibility:** The environment diff adds only the declared Cargo/Rustup/PATH and uv
   assignments; all prior assignments are unchanged. Re-sourcing PowerShell causes zero
   environment changes; the WSL PATH is identical after a second source. Existing Codex scripts'
   manual Cargo-home assignments name the same homes, and their custom targets remain local.
   An actual Windows direct-toolchain Cargo run with explicit RUSTC/RUSTDOC and the existing
   Codex target override passes. No manual home override was needed for the three plain-Cargo runs.
3. **Interpreter/plan:** The updated interpreter row and WP-P02 scope accurately describe the
   observed managed interpreter and environment changes. The existing `mneme-process-codex-r1`
   venv executes normally, with a project-managed 3.12.8 base prefix. An offline locked
   `uv sync --dry-run` against that existing venv keeps the environment: its proposed package
   differences are the editable checkout relocation and removal of reviewer-added dev extras
   (`coverage`, `rfc8785`), not interpreter replacement. No actual sync was performed.
4. **Carried WP-01 records:** No objection to landing them with this candidate. G-044 specifies
   the accepted code/docs pair and independent approving parties; registry certification and
   CLOSED state agree with it. The newly carried Codex CR-011 record is byte-identical to
   `c73593d6`, and Claude's closure-completion record is byte-identical to `689efef9` (git diffs
   empty). The plan now records the Rust implementation, corpus repair, approvals and closure.
   The NF register closes the Layer-01-resolved findings with governance references while
   leaving NF-023 OPEN pending this review; findings assigned to later layers are not newly
   closed by this change. No Layer-02 work is authorized by these records.

## Independently executed evidence

| Execution | Result |
|---|---|
| PowerShell: source candidate; `cargo test --locked --offline` | 16 integration tests + 1 doctest pass |
| Git Bash: source candidate; `cargo test --locked --offline` | 16 integration tests + 1 doctest pass |
| WSL Ubuntu: source candidate with `/mnt/e/...` MNEME_ROOT; `cargo test --locked --offline` | 16 integration tests + 1 doctest pass, Cargo 1.97.1 |
| Windows direct toolchain, explicit compiler/doc tool and Codex target override | 16 integration tests + 1 doctest pass |
| PowerShell/Git Bash `uv python find --offline` | Project-local managed 3.12.8 |
| Existing Codex venv import/version/base-prefix probe | Healthy, managed 3.12.8 base |
| `uv sync --locked --offline --dry-run` against existing process venv | Environment retained; no actual changes |
| Candidate `mneme_process check`, exact code, project workspace, `--deep-sources` | 8/8 checks pass |
| Repeated source: PowerShell environment / WSL PATH | Unchanged |

Reproduction scripts: `.tmp/work/codex/wpp02-windows.ps1`, `wpp02-bash.sh`,
`wpp02-linux.sh`, and `wpp02-python.py`. The first WSL invocation hit CRLF in my own scratch
script (`--offline\r`); after converting that script to LF the run passed. The candidate was
not changed. WSL executes Linux binaries over the shared E: checkout; this is not evidence of
filesystem case sensitivity. Linux Python discovery was not exercised; Linux environment
assignments were inspected and Cargo execution was exercised.

For G-045's system-Python item, independently executed `E:\AI\Python\Python312\python.exe`
with imports of `warnings`, `ssl`, `sqlite3`, `venv` and `ensurepip`: healthy CPython 3.12.8,
base prefix `E:\AI\Python\Python312`. This corroborates the repair outcome without rerunning
an installer. Claude's signature, installer-log and 1,956-test claims remain author evidence;
I do not represent them as my own executions. The project pin keeps project discovery on the
managed interpreter regardless of the repaired system interpreter.
