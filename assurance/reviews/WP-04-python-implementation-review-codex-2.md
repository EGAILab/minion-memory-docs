# WP-04 Python implementation — independent remediation review 2

**Verdict: CHANGES_REQUIRED.**

Date: 2026-10-11. Reviewer: Codex. WP04-CR-008 remains blocking; WP04-CR-009,
WP04-CR-010 and WP04-CR-011 are resolved at this exact pair. No new finding ID is
needed: the new schema witnesses refine the original CR-008 trust boundary.

## Reviewed pair and independence

- Code: `634625135851cccc188fe726acb86990911ebddb`.
- Docs content: `f16bb44a5e53f02ef6074a68466aab87ce5fdc54`.
- Review branch: `review/wp04-python-2`, from state-only descendant
  `e93df942ad204ccf8dca2b98ac578b95117d5514`.
- Authority: agreed contract `d857fcc27d54a44738d870473062f16ba3af493c` /
  `1f4438763c91fb95a4e88d86ac96302d9830cdb3`, approved by `67ba6632`, and
  Owner G-077..G-087. The normative specs are unchanged by this remediation.
- Previous review: `bb3dfa2c880dceb28a0aa81f0afe3bcd30426c94`, imported in
  the candidate. Claude's response is a review object, not closure evidence.

This is a targeted re-review of CR-008..011 and the directly changed neighborhoods:
the v1 catalog check, transaction lifecycle, JSON-only create fixture, two added
corpus steps and reachable malformed-read paths. I read the production and test
diffs, executed independent public-API witnesses, and ran the candidate gates.
Production modules, Claude's worktrees, state, registry, main and remotes were not
modified. Mutation replay uses an isolated source copy under my project-local notes.

## Per-finding dispositions

| Finding | Disposition | Evidence |
|---|---|---|
| WP04-CR-008 | OPEN, high, blocking WP-04 | Both original witnesses now reject correctly. Two different incompatible v1 properties still pass the new fingerprint and public open; see below. |
| WP04-CR-009 | RESOLVED | Same-handle gated-clock identical retry waits and receives the original receipt with one clock sample; mixed-operation controls pass; validation remains outside the lock. |
| WP04-CR-010 | RESOLVED | Actual JSON-only create runner followed by a real commit returns the independently derived literal receipt. The two added corpus steps follow the contract. |
| WP04-CR-011 | RESOLVED | Full independent Windows coverage: 1,166/1,166 statements and 470/470 branches, subprocesses included, no exclusions. Malformed-read and precedence controls pass with the required argument and no position. |

### WP04-CR-008 — the pinned shape still admits incompatible v1 semantics

Classification remains `IMPLEMENTATION_DEFECT`; severity high;
`owner_decision_required: false`. Authority: `spec/persistence.md`, Reference backend
DDL, Open and initialize, Databases, and the committed durability barrier.
Affected code: `persistence/postgres.py:71` (`_COLUMNS_SQL`), `:78`
(`_CONSTRAINTS_SQL`) and `:222` (open comparisons). Matrix H8's Python audit does
not establish the complete v1 compatibility boundary.

The new check is useful: renaming `mneme_schema.version` and dropping
`mneme_store.tail` now produce `persistence.schema_incompatible`, with no argument
or position, before a query depends on the damaged column. The ten damaged-shape
controls and fresh-v1 pin also pass. The explicit Read Committed transaction and
first-statement advisory lock remain intact; genuine DDL/availability errors are
not hidden by the remediation.

However, matching column names/types/nullability/defaults and rendered constraint
definitions is not sufficient to identify the normative reference schema. I
initialized fresh throwaway schemas with the public API, closed the handle,
applied each alteration below separately, and reopened through the public API.
This tests admission of an already incompatible schema, not alteration of a live
accepted handle by an administrator.

**Witness A: unlogged canonical records.**

```sql
ALTER TABLE mneme_record SET UNLOGGED;
```

On PostgreSQL 14.12, both fingerprint queries still equal their pinned constants.
`pg_class.relpersistence` for `mneme_record` is `u`. Public `open` succeeds;
`create_store('s')` and a valid one-record `commit_history` return a successful
receipt at position 1. The declared v1 DDL creates logged tables. An unlogged
record table does not deliver the required durable canonical history: PostgreSQL
documents that unlogged data is not crash-safe and is truncated after a crash or
unclean shutdown. [PostgreSQL 14 CREATE TABLE](https://www.postgresql.org/docs/14/sql-createtable.html)
I did not crash the shared service. The executed evidence establishes admission
and a returned receipt; the documented backend property establishes why that
admitted storage cannot satisfy the barrier.

**Witness B: non-bytewise store identity.** The same service has ICU support.

```sql
CREATE COLLATION loose
  (provider=icu, locale='und-u-ka-shifted', deterministic=false);
ALTER TABLE mneme_store ALTER COLUMN store_id TYPE text COLLATE loose;
```

Again, both pinned fingerprints match and public `open` succeeds.
`create_store('ab')` succeeds, but `create_store('a-b')` returns
`persistence.store_exists` (argument `store_id`, no position). Both strings are
distinct valid CORE-001 tokens. The altered column's equality conflates them,
violating the reference backend's required bytewise identities. PostgreSQL's
non-deterministic collations can equate different byte sequences; the collision
here was actually executed, not inferred from the locale name.
[PostgreSQL 14 collation support](https://www.postgresql.org/docs/14/collation.html#COLLATION-NONDETERMINISTIC)

Both changes retain the four table names, singleton version row, 18 pinned column
tuples and 10 pinned constraint tuples. `_COLUMNS_SQL` omits `attcollation`, and
neither query checks relation persistence. Each backend is still the prescribed
UTF-8/C/C throwaway database; the incompatible properties are on its tables.
The expected result for both is an unchanged backend and
`persistence.schema_incompatible` at open, before any store operation.

Required repair: characterize the catalog properties on which v1 durability and
identity depend, then reject incompatible properties at the agreed open boundary.
The two demonstrated properties must have discriminating public-open controls.
Keep the lock, isolation, no-modification rule and error distinction. Update the
matrix to distinguish the executed compatibility surface from its remaining
planned coverage. These are implementation violations of existing semantics;
allowing non-durable tables or different identity equality would require a new
authority decision, not a local narrowing of schema compatibility.

### WP04-CR-009 — whole-operation handle serialization

The handle lock now surrounds isolation/read-only setup, transaction entry,
operation execution and commit/rollback exit. A return inside the transaction
body still exits that context before returning the receipt. Store-row locking
continues to serialize separate handles.

In my public-API probe, a gated clock held the first commit while an identical
retry began on the same handle. The retry remained waiting. Releasing the clock
yielded equal successful receipts, one physical record and one clock invocation.
While the lock was held, an invalid `since` returned
`history.boundary_invalid` immediately with argument `since` and no position:
validation did not wait behind the transaction. The candidate's overlapping
mixed-operation test and the existing abort/concurrency/read controls also pass.

### WP04-CR-010 — runner seam and corpus oracles

I invoked the actual runner's JSON-only create observation, then a real commit.
The fixture is bound using the library decoder after successful creation.
The expected receipt was written literally in my probe, not obtained from a
second implementation. Its store is `store-3`, operation is `(app, c-1)`, range is
1..1, timestamp is `2026-10-11T08:00:00.000000Z`, and its sole `o-1` envelope has
that store-owned `recorded_at`.

The corpus diff adds exactly those two steps; all previous 63 steps are unchanged.
The five Layer 04 scenarios now contain 65 steps (14 + 19 + 12 + 4 + 16).
An independent newly created store starts at 0, so its first one-record commit
occupies position 1. The fixture supplies its own clock. Reusing `o-1` from another
store is permitted because record-ID uniqueness is per store; operation identity
is likewise scoped by store. Both expectations follow the agreed text, and the
runner remains a dispatcher/fixture adapter rather than a second validator.

### WP04-CR-011 — reachable assurance and precedence

The public controls reach the previously missing malformed-`since` exception
path, and sweep invalid boundary members, invalid ID, negative position, boolean
limit, unsafe number and typed ordering. My additional paired probe supplies a
malformed `since` with `JsonText('1e400')` as `limit`: the latter produces
`value.number_not_finite`, argument `limit`, no position, before typed checks.
The coverage run instruments the entire package, includes subprocesses and uses
an empty exclusion list. No production branch was hidden or excluded to close
this finding.

## Independent execution record

Project-local evidence: `.tmp/work/codex/wp04-python-review-2/`.
The executed drivers and their outputs are retained there; these notes are not
part of the candidate or committed review artifact.

- `probes.py`, `probe-results.json`: original CR-008 witnesses, unlogged and ICU
  witnesses, same-handle retry, lock-independent validation and actual runner
  create/commit with a literal receipt assertion.
- `gates.py`, `gates.json`, per-gate logs and `coverage.json`: Windows CPython
  3.12.8, locked candidate dependencies, PostgreSQL 14.12 as `mneme_dev`;
  **541 passed, 4 xfailed**; **1,166/1,166 statements, 470/470 branches**;
  Ruff, formatting and strict mypy clean.

- `mutants.py`, `mutant-results.json` and `mutant-P21/P22/P23.log`: isolated-copy
  replay of the three new planted violations. Unmodified affected-slice baseline:
  **11 passed**. **3/3 killed**: P21 leaks `UndefinedColumn` on renamed `version`;
  P22 wrongly accepts the missing record-ID unique constraint; P23's overlapping
  retry exits instead of waiting behind the gated first commit. These are the
  intended discriminating failures, not import failures or timeouts. Sources in
  the actual candidate were never mutated. Earlier P01..P20 evidence is retained
  by the prior review; the established P14 equivalence is not reopened.
- `process-check.log`: exact worktree pair, deep source validation, **8/8 PASS**.

The host coordinator requested a batch boundary during the mutation replay. I
let that already running batch finish, stopped the idle relay helpers, notified
`w1:p1`, and started no further test batch. No latency or performance claim is
made from the shared-host runs.

**Platform limit:** the case-sensitive POSIX suite was prepared but not started
at this pair because the host reservation remains in effect. A Linux client
connection preflight reported PostgreSQL 14.12 / `mneme_dev`; that is not suite
evidence. The previous review's POSIX run remains evidence only for its previous
pair. This targeted rejection and the three finding dispositions rest on the
executed Windows/public-API controls; they are not a new cross-platform approval
or candidate certification. The demonstrated schema false passes suffice to
reject this pair without an additional platform run.

**Cleanup:** all probes used throwaway UTF-8/C/C databases in `mneme_ts`, as the
non-superuser role `mneme_dev`. Automatic helper cleanup left reviewer-owned
databases behind; I removed only the known reviewer databases with ordinary
`DROP DATABASE` after checking there were no active sessions, without `FORCE`,
role grants or changes to the shared service. `cleanup-check-final.log` reports
no test activity and no remaining test databases. Both relay processes exited;
no FUSE mount or POSIX suite was started. Credentials are not committed, and the
temporary relay environment file was removed. All notes, caches, targets and
worktrees remain inside the E: project root.

## Mandatory convergence check

The adopted workflow (`process/agent-workflow.md` §6, reference workflow §11.8)
requires checking triggers before another ordinary remediation pass. CR-008 was
open in the first independent implementation review and remains materially open
in this second independent review. **Trigger A has fired.** Refining the witnesses
does not reset its identity. No successor IDs are minted here (trigger B is not
asserted); this targeted implementation review does not add a rejected complete
contract review to trigger C.

The default next route is characterization of the v1 catalog trust boundary,
challenge and the independent checkpoint before another implementation pass.
An ordinary repair exception needs an explicit recorded reason under the adopted
protocol. I have not updated coordination state or authorized such an exception.
Resolved findings do not approve this pair or acceptance onto main.
