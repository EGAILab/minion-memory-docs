# WP-P02 — Process hardening 2: OWN-001 environment (NF-023)

**Requirements:** none (process-only). **Governance:** G-045 (Owner "Fix two items",
`reference/governance/2026-10-11-owner-wpp02-environment.md`); G-009 for acceptance.
**State:** `process/state/WP-P02.yaml`.

## Scope

**NF-023.** `process/environment/project-environment.{sh,ps1}` now set `CARGO_HOME` to project-local
Cargo homes:
- **Windows:** `cargo-home`.
- **Linux/WSL:** `cargo-home-linux`, plus `RUSTUP_HOME` set to `rustup-linux` and `PATH`.

They also pin the project-local interpreter with `UV_PYTHON_PREFERENCE=only-managed` and
`UV_PYTHON=3.12.8`. `plans/toolchain-proposal.md` records the pinned interpreter.

**Not in scope:** any tool, contract or code change. The system-Python repair (G-045 item 2) is
outside the repositories; it is reported in the implementation record only.

## Assurance trail

| Step | Record |
|---|---|
| Implementation (Claude) | `assurance/reviews/WP-P02-implementation-claude.md` |
