# WP-04 — Python implementation record (Claude)

**Agreed contract:** docs `d857fcc2` / code `1f443876` (Codex APPROVED `67ba6632`).
**Implementation:** code `afb36081fc569246e6055f2bde99ca9481ca5e8a` on `wp04/contract`.
**Gate:** G3 (Python), author-run at the exact code. This record is evidence, not a review.

## Implementation (`minion_memory.persistence`)

- **`PostgresHistoryStore`** (`persistence/postgres.py`) implements the four operations in the
  contract's numbered orders. Validation (commit steps 1–8, read steps 1–4) completes before any
  database work.
- **Draft gates D1–D4.** `core.history._admit(..., draft=True)` runs the G-055 gates with
  `recorded_at` removed from the closed member set. Reader outcomes `excluded`, `skip` and
  `unknown_required` map to `persistence.record_unrecognized`. This is additive: the Layer 02
  behaviour is unchanged when `draft` is false.
- **Commit steps 9–13** run in one Read Committed transaction that first takes
  `SELECT … FOR UPDATE` on the store row, so every later statement sees the latest committed
  state:
  - idempotency compares the SER-009 bytes of the normalized draft array;
  - then the store-wide record-ID check, then capacity;
  - then one clock sample, normalized with HIST-004; a value HIST-004 rejects raises
    `ClockDefectError`, which is not a store outcome;
  - then the positions, the operation row and the tail.

  The receipt is returned after COMMIT, with `synchronous_commit = on` set on the session.
- **Reads** use one `REPEATABLE READ READ ONLY` transaction.
- **Open** runs an explicit Read Committed transaction whose first statement is
  `pg_advisory_xact_lock(-4695452043516644990)`; it then creates schema version 1 or validates it,
  else raises `persistence.schema_incompatible`.
- **Package.** `minion_memory.persistence` is a new package-root namespace. It keeps the database
  driver out of `core`. The scaffold gate is widened to allow it, for review.
- **Dependency.** `psycopg[binary]` 3.2.13 (libpq 16.9) is added to the project dependencies.

## Executions (project-local; CPython 3.12.8; PostgreSQL 14.12; role `mneme_dev`)

| Check | Result |
|---|---|
| `ruff check`, `ruff format --check`, `mypy --strict` (src and tests) | clean |
| `pytest`, full suite | **521 passed, 4 xfailed** (the remaining placeholders of later layers) |
| Layer 04 scenarios, ACTIVE, `IMPLEMENTED_LAYER = 4` | 5 files, 63 steps, all pass |
| `tests/core/test_layer04_store.py` | 20 tests: paging completeness; capacity with a synthetic tail; clock sampling counts; clock defect; abort after the sample; connection killed after the sample; NUL round-trips; receipt rebuild from another handle; `synchronous_commit`; open initialize-once and 4 incompatible-schema cases; concurrent first opens under a Repeatable Read default; a waiting opener while another initializes; 8 parallel writers; parallel identical retries; parallel conflicts; a reader loop during commits |
| `mneme-process check --deep-sources` | 8/8 |
| Planted violations (`py_mutants_wp04.py`) | **19/20 killed**; P04 (reads under Read Committed) killed in 3 of 3 runs |

**P14 survived and is equivalent.** It computes `through` as `min(since + limit, tail)` instead of
the last returned position. Within one snapshot, the committed positions are exactly 1…tail
(G-080; enforced by the step-13 allocation under the row lock, the `(store_id, position)` primary
key, and the tail `CHECK`). So the entries after `since` are exactly `since+1 … min(since+limit,
tail)`, and both formulas agree for every reachable state, including JSON-text input (the formula
reads only parsed integers). They could differ only in a store that already has a gap, which no
API path can produce. The equivalence is offered for challenge.

## Test-backend arrangement (reviewable)

- Each test session uses one throwaway database: template0, UTF-8, C collation, in `mneme_ts` on
  E:. It is dropped at exit.
- Scenarios and most store tests share one initialized schema, emptied with `DELETE` before each
  use. The open and initialize tests each get a fresh empty schema.
- Reason: creating files in the tablespace takes 1–28 s on this host, while the operations take
  milliseconds. The open rule inspects `current_schema()`, so an empty schema is an empty backend.

## Not yet executed

[IT], the cross-language witnesses: a store written by one language and read and retried by the
other, plus mixed-language concurrent and waiting first opens. They need the Rust candidate.
