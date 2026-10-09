# Toolchain proposal — PROPOSED (WP-00)

All caches/venvs/targets under OWN-001 paths (`process/environment/project-environment.*`).

## Python (Claude)

| Item | Proposal | Observed now |
|---|---|---|
| Interpreter | CPython 3.12 (floor), managed by uv | 3.12.8 (`E:\AI\Python\Python312`) |
| Project/env | uv; environments under `.tmp/cache/venvs/<project>` via `UV_PROJECT_ENVIRONMENT`; `uv.lock` committed | uv 0.10.9 |
| Lint/format | ruff (lint + format), line length 110 | ruff from the dev group |
| Types | mypy `--strict` | |
| Tests | pytest, hypothesis for property tests; `-p no:cacheprovider` | |
| Coverage | 100% of the certified Python surface (inherited Minion-Agent floor; reconfirm at WP-01) | |
| SQLite | stdlib `sqlite3`; record `sqlite3.sqlite_version` in every gate report | 3.45.3 |
| Schemas | `jsonschema` draft 2020-12 | |
| YAML | PyYAML only through the YAML-1.2-core boundary | |

## Rust (Codex — proposal for Codex to confirm or counter in its first Rust pass)

| Item | Proposal | Observed now |
|---|---|---|
| Toolchain | stable, pinned by `rust-toolchain.toml` to the version Codex verifies | rustc/cargo 1.97.1 on this host |
| Layout | Cargo workspace in `minion-memory-rust/` (crate split decided by Codex) | not created (Codex-owned) |
| Gates | `cargo fmt --check`, `cargo clippy --all-targets -D warnings`, `cargo test`, rustdoc where public | |
| Target dir | `CARGO_TARGET_DIR=.tmp/cache/cargo-target/<platform>` | |
| YAML/JSON | a YAML 1.2 loader configured to the same portable profile (reject duplicate keys, aliases, tags) and `serde_json` | |
| SQLite | `rusqlite` (bundled or system — record the exact SQLite version; drift vs Python is hazard H8) | |

## Shared

- Canonical corpus in YAML (portable profile) + JSON Schema 2020-12; both runners validate scenario
  envelopes against `conformance/schema/scenario.schema.json`.
- Line endings: `.gitattributes` `* text=auto eol=lf` in both repos (hazard H2).
- No network or AI service in any gate.
