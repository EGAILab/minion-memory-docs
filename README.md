# minion-memory-docs

Governance, normalized contract and assurance for **Minion-Memory** — the Project Mneme durable
memory engine, implemented independently in Python and Rust against one shared contract, with two
proving profiles: Human Learning (Flashcard App) and Agent Memory (Minion-Agent).

Code, manifest and canonical conformance live in the sibling repository `../minion-memory`.

> **State:** WP-00 (bootstrap) in `SCOPING`, awaiting independent Codex review. Nothing here is
> reviewed, approved or frozen yet. Current state: `process/state/WP-00.yaml`.

| Directory | Contents |
|---|---|
| `reference/` | Source-bundle inventory with SHA-256 (`mneme-v2.3-source-bundle.yaml`), derived non-authoritative source text + anchor index, Minion-Agent process adoption record, Owner governance records |
| `spec/` | Normalized **DRAFT** contract: requirement-ID-bearing transcription of the bundle (`spec/README.md`) |
| `process/` | Workflow, coordination state, gate tiers, requirement IDs, finding taxonomy, hazard families, templates, role entry points, environment scripts (OWN-001), `mneme-process` tooling |
| `assurance/` | Findings registers, layer evidence, risk register, reviews |
| `plans/` | Work-package records, layer/dependency plan, WP-01 proposal, toolchain proposal |
| `design/` | Mneme-side design decisions not already in the bundle |

## Authority

Foundation v2.3 > MVP Contract v1.2 > Requirements 00–05 > Implementation Architecture Amendments
v1.3 > this normalized contract (after review) > canonical conformance. The bundle itself
(`../artifacts/20261009/...`) is read-only and is never edited.

## Validation

```sh
. process/environment/project-environment.sh            # OWN-001: temp/caches on E:
export UV_PROJECT_ENVIRONMENT="$MNEME_VENV_ROOT/mneme-process"
cd process/tools
uv run pytest                                            # tool tests incl. negative controls
uv run mneme-process check --docs ../.. --code ../../../minion-memory [--deep-sources]
```
