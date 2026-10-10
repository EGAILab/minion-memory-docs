# `mneme-process`

Workflow mechanics and bootstrap validation. It decides mechanical well-formedness and legality
only — never semantics, never verdicts, never approval.

| Command | Purpose |
|---|---|
| `sources build --docs <docs>` | Re-derive `reference/source-text/*.md` and `reference/source-index.yaml` from the hashed bundle (needs the `sources` extra / dev group for `python-docx`) |
| `check --docs <docs> --code <code> [--only …] [--deep-sources]` | All checks: `repos`, `sources`, `spec`, `manifest`, `conformance`, `findings`, `registry`, `state` |
| `state validate <file>` | One state file's structural invariants |
| `state transition-check FROM TO` | Legality per `process/coordination-state.md` §5 |
| `state roundtrip --docs <docs> [--revision S]` | Commit-rule step 4: every working state file equals its committed copy in `S` (raw bytes, explicit UTF-8; line endings normalized) |

Tests (`tests/`) build a synthetic two-repository world, assert it passes every check (baseline),
then apply one realistic mutation per rule and assert the intended check reports it.

Run under OWN-001: `. ../environment/project-environment.sh` and
`UV_PROJECT_ENVIRONMENT=$MNEME_VENV_ROOT/mneme-process`.
