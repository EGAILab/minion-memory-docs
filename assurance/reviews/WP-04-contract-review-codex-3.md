# WP-04 independent contract review 3 — Codex

**Verdict: CHANGES_REQUIRED**

Date: 2026-10-11. Targeted review of WP04-CR-007 and the initialization revision.

## Exact object

- Docs candidate: `0837d327902fb2eeb80a4f42c8feb7a993929f33`.
- Unchanged code/corpus: `1f4438763c91fb95a4e88d86ac96302d9830cdb3`.
- Review branch: `review/wp04-contract-3`, from supplied state-only descendant
  `cfc39ff76a428f20f11fa697ab8aa098e810bffa`.
- Separate docs checkout: `review-worktrees/docs-wp04-review-3`; exact, clean code
  checkout retained at `review-worktrees/code-wp04-review-2`.

The normative change is confined to the Open and initialize bullet. Matrix, plan and
response updates describe that repair; the prior review is imported. The state
descendant changes only WP-04 state. No scenario or Owner-decision change occurred.
The 63/63 scenario derivation from review 2 remains applicable to the unchanged code;
I did not claim another full scenario execution for this targeted review.

## CR-007 disposition — OPEN, refined executed witness

Classification remains `CONTRACT_ASSURANCE_DEFECT`, severity MEDIUM, blocking WP-04,
owner_decision_required: false. Requirements: PERS-005/014/015; G-079/G-081 shared
reference-backend initialization. No new finding ID or path-C choice is introduced.
CR-001..006 remain resolved at the contract level without contrary evidence.

**The lock identity repair is correct.** Independently hashing exact ASCII
`mneme.schema.open.v1` produces:

```text
SHA-256: bed6673e764ef1825660b777d935806e3a2160c94d3bbca6013cae34e1c47ae7
first 8 bytes: bed6673e764ef182
big-endian signed int64: -4695452043516644990
```

The prescribed one-argument bigint call identifies the same exclusive resource in
both languages. It applies to every open and is held through the transaction. The
mixed-language [IT] witness now addresses the original different-key risk.

**Remaining gap: snapshot isolation of open is unspecified.** The new first
statement can establish a Repeatable Read snapshot *before* waiting for the lock.
Taking the right lock does not refresh that transaction snapshot. The contract pins
Repeatable Read Read Only for history reads but does not pin isolation for opening,
or require a fresh-snapshot transaction retry for concurrent initialization. An open
using Repeatable Read is not forbidden by the new text.

**Executed witness at the exact key and candidate DDL, PostgreSQL 14.12:**

1. Begin opener A at Repeatable Read. Its first statement is exactly
   `SELECT pg_advisory_xact_lock(-4695452043516644990)`; it holds the shared lock.
2. Begin opener B at Repeatable Read. Its first statement is the same SELECT.
   Observe B's ungranted advisory lock in pg_locks before proceeding, ensuring that
   it really waits on the shared resource before A initializes.
3. A sees zero mneme_ tables, executes the unchanged candidate DDL, inserts singleton
   version 1 and commits. B then obtains the lock.
4. B's schema query still reports **zero** tables in its older snapshot. Its CREATE
   fails **SQLSTATE 42P07**, `relation "mneme_schema" already exists`.

The shared schema remains valid with exactly one `(true,1)` version row, but both
opens do not succeed. This is the same concurrent-first-open property CR-007 was
raised to protect, rather than a new application semantic request.

**Discriminating positive control:** repeat the same ordered two-connection experiment
on a fresh schema at **Read Committed**, with the same normative first statement and
key. A observes zero tables and initializes. B waits, then observes four tables and
the correct singleton/version row. Both open successfully. No key or DDL difference
separates the positive and negative runs; only transaction isolation differs.

**Required repair:** complete the reference open protocol with a snapshot/isolation
rule. Requiring Read Committed for the open transaction is sufficient: inspection
after acquiring the lock sees the initialization that committed while it waited.
Alternatively, specify a whole-transaction fresh-snapshot retry protocol for stronger
isolation. Do not simply ignore a DDL exception, inspect the same stale snapshot, or
classify a valid concurrently initialized schema as incompatible. Keep the separate
read_history snapshot requirement intact. Add the waiting-opener/isolation witness
to initialization assurance, including its mixed-language form.

This is a representation/protocol completion the contract author can make; the key,
domain, schema version and Owner semantics do not need a new decision. No other new
contradiction was found in the targeted diff.

## Evidence and scope

- Driver: `.tmp/work/codex/wp04-review-3.py` (no Mneme implementation imports).
- Captured output: `.tmp/work/codex/wp04-review-3.log` and
  `.tmp/work/codex/wp04-3/probe-results.json`.
- Deep-source process validation: **8/8**, captured in
  `.tmp/work/codex/wp04-3/process-check.log`.

Both experiments use the exact literal SQL call as their first statement after
BEGIN; isolation is selected in the transaction's BEGIN mode. The monitor explicitly
confirms lock contention before A's DDL, avoiding a timing-only race assumption.
All test data was in a throwaway database created with template0, UTF8, C/C collation,
TABLESPACE mneme_ts. Its project-local `.tmp/pgdata` location was queried. Only
mneme_dev credentials were used, never printed. The database was dropped and absence
confirmed after the probes.

Only this review record is authored in a repository. No production, contract, source,
scenario, state, registry or remote changes were made. All temp/cache files remain
inside the E: project root under OWN-001. Approval is withheld solely for the
remaining WP04-CR-007 initialization snapshot gap.
