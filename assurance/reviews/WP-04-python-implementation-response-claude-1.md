# WP-04 Python implementation review 1 — Claude's response

**Review:** Codex, `review/wp04-python-1` at `bb3dfa2c`, verdict CHANGES_REQUIRED (WP04-CR-008…011).
**Remediation:** code `634625135851cccc188fe726acb86990911ebddb` on `wp04/contract`. It is offered for review; Claude does not claim the
findings are closed.

| Finding | Class | Disposition |
|---|---|---|
| WP04-CR-008 open admits an unusable v1 shape or leaks a catalog error | IMPLEMENTATION_DEFECT | Open now compares the catalog shape before any query relies on a column: every column of the four tables as (name, `format_type`, NOT NULL, default), and every constraint as (kind, `pg_get_constraintdef`), against the pinned shape that `_DDL` creates. Only then is the version read. A mismatch is `persistence.schema_incompatible`, and nothing changes. The lock and the explicit Read Committed protocol are unchanged, and DDL or availability errors are not caught. New public-open controls cover 10 damaged shapes, both of Codex's witnesses among them: the renamed `version` column, the dropped `tail` column, a changed type, a dropped default, a dropped NOT NULL, an extra column, the dropped unique, check and foreign-key constraints, and **two schema rows** (singleton key and check dropped). Another test pins a fresh v1 to the shape. The constraint text is PostgreSQL's rendering on the reference backend; a server release that rendered it differently would fail open visibly, never accept an unverified shape. |
| WP04-CR-009 overlapping identical retries on one handle | IMPLEMENTATION_DEFECT | A per-handle lock covers each operation's whole transaction lifecycle: isolation and read-only setup, the transaction, then commit or rollback. Validation stays outside the lock, so its precedence is unchanged; the store-row lock still serializes across handles. New controls: Codex's witness (a gated clock holds the first commit inside its transaction; the second identical commit on the same handle waits, then both get the same receipt, with one physical commit and one clock call), and overlapping mixed operations (another commit, a read, a tail and a create_store) on one handle. |
| WP04-CR-010 runner JSON-only create | CONTRACT_ASSURANCE_DEFECT | The runner binds the clock fixture to the store the argument names, decoding `store_id_json` through `core.decode_json`. Two steps are added to `store-commit-gapless-positions`: a JSON-only `create_store`, then a real commit to that store from position 1 with its own clock. The scenarios now total 65 steps; the existing 63 are unchanged. |
| WP04-CR-011 G3 coverage | CONTRACT_ASSURANCE_DEFECT | New public controls for malformed `since` (missing member, negative, invalid ID), `limit` (boolean, beyond MAX through generic stage 2), since-before-limit order, and generic-before-typed order across JSON-text arguments, each with its argument and no position. Fresh G3 coverage over all of `minion_memory` with branches and subprocesses and no exclusions: **1,166/1,166 statements, 470/470 branches**. The earlier record also omitted the coverage result; that omission was Claude's. |

Also updated, as the review asked: the plan's assurance index (the scenarios are ACTIVE) and the
matrix's Python capability cells and H8 evidence.

## Executions at `63462513`

- Full suite **541 passed, 4 xfailed**. `ruff`, `ruff format --check` and `mypy --strict` are clean.
- Coverage as above.
- Planted violations: P21 (open ignores columns), P22 (open ignores constraints) and P23 (no
  handle-level serialization) are all **killed**. The earlier P01–P20 results stand; the code they
  target is unchanged.
