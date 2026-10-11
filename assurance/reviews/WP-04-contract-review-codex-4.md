# WP-04 independent contract review 4 — Codex

**Verdict: APPROVED**

Date: 2026-10-11. WP04-CR-007 is resolved at the contract level. CR-001..006 remain
resolved; no new finding or conflicting requirement was identified in this targeted
revision. This approves the exact contract candidate, not an implementation,
certification or acceptance onto main.

## Exact review object

- Docs: `d857fcc27d54a44738d870473062f16ba3af493c`.
- Unchanged code/corpus: `1f4438763c91fb95a4e88d86ac96302d9830cdb3`.
- Review branch: `review/wp04-contract-4`, from supplied state-only descendant
  `825f01e52d75c2ba98b3325a59e3da6e77a67263`.
- Docs checkout: `review-worktrees/docs-wp04-review-4`; the exact, clean code
  checkout remains `review-worktrees/code-wp04-review-2`.

The state descendant changes only `process/state/WP-04.yaml`. Against the previous
candidate, the normative diff is confined to Open and initialize; the matrix,
response and plan describe that change and the prior review is imported. Owner
decisions, scenarios, DDL, store-operation precedence and read_history are unchanged.
The independent 63/63 scenario derivation from review 2 remains applicable; no new
full-corpus execution is claimed for this targeted review.

## Closure of WP04-CR-007

The shared key remains correct: the first eight SHA-256 bytes of exact ASCII
`mneme.schema.open.v1` are `bed6673e764ef182`, interpreted as big-endian signed int64
`-4695452043516644990`. The contract retains the one-argument bigint overload,
exclusive transaction-level lifetime and identical resource for both languages.

Every open now explicitly begins at **Read Committed**, regardless of session/server
default, and acquires that lock as the first statement after BEGIN. Every inspection
follows lock acquisition. Consequently the waiting opener's subsequent inspection
has a new statement snapshot that includes the first opener's committed DDL/version
row. Stronger isolation is expressly excluded, DDL errors cannot be ignored, and a
valid initialized schema cannot be labelled incompatible. This directly addresses
the refined witness, without changing domain semantics or inventing an Owner choice.

**Independent execution, PostgreSQL 14.12:** both connections were configured outside
their open transactions with session default `repeatable read`. Both explicit open
transactions used the exact lock SELECT first. A acquired it; B was observed in
pg_locks waiting on the same resource before A initialized and committed the unchanged
candidate DDL plus singleton version 1. Both actual transaction isolation levels
were queried as `read committed`. A saw zero tables and initialized; B then saw
four tables and validated `(singleton=true,version=1)`. Both opens succeeded and
exactly one version row existed.

**Discriminating negative control:** with the same session defaults, key, DDL and
ordered contention, remove only the explicit Read Committed transaction override.
Both transactions run at Repeatable Read. B obtains the lock but sees zero tables
in its older snapshot and fails **42P07**, `relation "mneme_schema" already exists`.
This reproduces the prior witness and proves that the new isolation requirement,
rather than a lucky schedule or changed key, removes it.

The separate Repeatable Read Read Only/single-statement rule for read_history is
unchanged and does not conflict: initialization and history reads are distinct
transactions with different snapshot requirements. Commit row locking, clock-abort,
capacity and idempotency rules are untouched. The matrix adds the required waiting
opener control with a hostile default, including its future mixed-language form.

## Evidence and limits

- Driver: `.tmp/work/codex/wp04-review-4.py` (no Mneme implementation imported).
- Captured output: `.tmp/work/codex/wp04-review-4.log` and
  `.tmp/work/codex/wp04-4/probe-results.json`.
- Deep-source process check: **8/8**, captured in
  `.tmp/work/codex/wp04-4/process-check.log`.

The throwaway database used template0, UTF8, C/C collation and TABLESPACE mneme_ts;
its project-local `.tmp/pgdata` location was queried. Only mneme_dev credentials
were used and none were printed. The database was dropped and absence verified.
All notes, temp/cache files and the existing managed-Python review environment remain
inside the E: project root under OWN-001.

These are independent SQL protocol controls, not tests of completed Python/Rust
store implementations. Actual same-language and mixed-language open controls,
other PLANNED implementation evidence and G3 gates remain required in their phases.
The only authored repository change is this review record; no contract, source,
production, corpus, state, registry or remote edits were made.
