# WP-P02 — implementation record (Claude)

**Finding:** NF-023 (`SEMANTICS_NEUTRAL_HARDENING`). **Governance:** G-045. **Gate:** process-only
hand-off: `mneme-process check` (all checks), plus the scripts exercised on every supported shell.
This is author evidence, not a review.

## Change

- **`project-environment.sh`.**
  - Windows (Git Bash): `CARGO_HOME=.tmp/cache/cargo-home`.
  - Linux/WSL: `CARGO_HOME=.tmp/cache/cargo-home-linux` and `RUSTUP_HOME=.tmp/cache/rustup-linux`.
    The project-local rustup toolchain that Codex installed with `--no-modify-path` is prepended to
    `PATH`, idempotently.
  - Both platforms: `UV_PYTHON_PREFERENCE=only-managed` and `UV_PYTHON=3.12.8`.
- **`project-environment.ps1`.** `CARGO_HOME=.tmp\cache\cargo-home`, `UV_PYTHON_PREFERENCE`,
  `UV_PYTHON`.
- **Windows toolchains.** These keep using the rustup toolchains already installed on C:. Those are
  executed, never written, which agent-workflow §7 permits.
- **Unchanged.** The only other edit is the `plans/toolchain-proposal.md` interpreter row. No other
  variable, tool or path changed.
- **No new cache locations.** These Cargo homes, the rustup home and the uv-managed 3.12.8 are the
  ones the WP-01 Rust and Python work already used, with the variables set by hand. The scripts now
  set them.

## Executions (exact docs candidate; code `main` `cc3c5d54`)

| Shell | Variables | `uv python find` / project venv | Rust suite via plain `cargo` |
|---|---|---|---|
| Git Bash (Windows) | set as above; `RUSTUP_HOME` unset | `.tmp\cache\uv-python\cpython-3.12…\python.exe`; venv `base_prefix` is the uv-managed 3.12.8 | rustup proxy uses 1.97.1 (`rust-toolchain.toml`); `--locked --offline`: 4/4 test groups ok |
| PowerShell 5.1 | set as above | same uv-managed interpreter | 4/4 ok |
| WSL Ubuntu (`MNEME_ROOT=/mnt/e/...`) | `platform=linux`; Linux homes as above | n/a (no Linux Python use in scope) | `cargo` resolves to `.tmp/cache/cargo-home-linux/bin/cargo`, version 1.97.1; 4/4 ok |

With the script sourced, nothing new is written under `C:\Users\<user>\.cargo`. That folder's
existing `registry` predates this work and is left untouched.

## System Python (G-045 item 2; outside both repositories)

The Windows registry and the installer bundle still listed `Python 3.12.8 (64-bit)`, installed per
user at `E:\AI\Python\Python312`. Only `Lib\site-packages\pip` (a fragment) and `Lib\test`
remained.

1. **Repair.** Ran the bundle's own cached installer
   `%LOCALAPPDATA%\Package Cache\{a6d11f3a-…}\python-3.12.8-amd64.exe`, which has a valid
   Authenticode signature from the Python Software Foundation (SHA-256 `1948229d…8b91`), with
   `/repair /quiet`. The log is in `.tmp/work/claude/python312-repair.log`. Exit code 0; no download.
2. **Verification.**
   - `python.exe` is 3.12.8 (`tags/v3.12.8:2dc476b`);
   - `py -3.12` resolves to it;
   - `venv`, `ssl`, `sqlite3` and `ensurepip` import;
   - stdlib `test_json test_hashlib test_datetime test_ssl test_sqlite3 test_venv`: 1,956 tests,
     SUCCESS.
3. **pip.** The surviving pip fragment had no `__init__`/`__main__` and no dist-info, so it broke
   `-m pip`. It was moved, not deleted, to `.tmp/work/claude/python312-pip-fragment-backup`. Then
   `ensurepip --default-pip` installed the bundled pip 24.3.1 offline, and `pip check` is clean.

The project still does not depend on the system Python. The scripts now pin the uv-managed 3.12.8.
