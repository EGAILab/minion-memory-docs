# WP-04 independent contract review 2 — Codex

**Verdict: CHANGES_REQUIRED**

Date: 2026-10-11. CR-001..006 are resolved at the contract level. One new blocking
assurance finding, WP04-CR-007, concerns the added PostgreSQL initialization protocol.
No new Owner decision is requested by this review.

## Exact object and method

- Docs candidate: `5cceb3176f7a502fb95ea5c216ca64d99c919ab5`.
- Code/corpus candidate: `1f4438763c91fb95a4e88d86ac96302d9830cdb3`.
- Review branch: `review/wp04-contract-2`, from state commit
  `b56094a41218a56fc3f2cd1f12da49535635791d`.
- Separate worktrees: `review-worktrees/docs-wp04-review-2` and
  `review-worktrees/code-wp04-review-2`. State commit differs from the docs candidate
  only in `process/state/WP-04.yaml`; it does not change normative content.

I reviewed the rewritten store section, SER-008 rows, matrix, plan, response record,
verbatim G-085..G-087 and relevant accepted G-031/G-033/G-054/G-055/G-080..G-084.
The response record is a claim to challenge, not closure evidence. The imported first
review remains the starting finding record. Its source pins and authority chain apply.

I independently derived every one of the 63 scenario results from the text, including
the new paired errors, JSON arguments, clock offset, occurred_at normalization,
numeric spelling, wider writer and NUL identities. No Mneme implementation was used
as an oracle. PostgreSQL probes use the candidate DDL unchanged. The scratch model
only covers these fixture inputs; it is not an implementation or proof of arbitrary
input behavior.

## Per-finding dispositions

| Finding | Contract-review disposition | Independent basis |
|---|---|---|
| WP04-CR-001 | RESOLVED | The sole persisted operation-ID column is exact UTF-8 `bytea`. The record table no longer duplicates it as text. Both NUL and a-NUL-b store and compare exactly in the executed database probe; matrix now includes the opaque operation identity domain. |
| WP04-CR-002 | RESOLVED | Every expected recorded_at is canonical `.ffffffZ`. The clock now supplies an admitted HIST-004 input instant and the store canonicalizes it; this makes the offset-spelled clock fixture valid. All resulting timestamps, including occurred_at, match independently calculated UTC microsecond spellings. |
| WP04-CR-003 | RESOLVED | All four APIs declare structured arguments and ordered generic/typed/state checks. D1–D4 are explicit. The four original paired inputs now have determined codes/arguments; 63 fixture observations, including JSON duplicate keys, match the declared order. Store errors carry no position. |
| WP04-CR-004 | RESOLVED | One committed snapshot supplies range validation, entries, through and tail. Record-counted pages may slice a committed batch. The revised Repeatable Read Read Only probe preserves tail 0 and an empty page despite a concurrent committed position 1; the original separate-Read-Committed-query algorithm is excluded. |
| WP04-CR-005 | RESOLVED by G-085 | The Owner permits an aborted attempt to have sampled. The text distinguishes durable timestamp status from callback invocation, with no clock call on validation, retries or pre-commit conflicts. Matrix cancellation no longer promises reversible sampling. |
| WP04-CR-006 | RESOLVED by G-086 | Idempotency precedes store duplicate checks and capacity; capacity precedes the clock/writes. MAX−tail arithmetic and `persistence.store_full` with no argument are defined, and physical tail/position CHECK constraints preserve the canonical bound. Actual full-store branch and retry tests remain correctly PLANNED for implementation. |

These are contract dispositions, not proof that a future implementation meets the
rules, and do not mutate the coordinator's state or finding register.

### Checks of the revised readings

**Steps 9–13.** Equal operation mutations return their original receipts before any
duplicate-ID/capacity/clock action. Different mutations return operation_conflict
without sampling. For a new operation, existing-ID rejection is the existing strict
G-083 rule; an otherwise-admissible new range then checks K > MAX−tail. Only a range
that passes those checks reaches the single sample and atomic write. This respects
G-085/G-086 without converting a full-store retry into a duplicate or capacity error.
Post-sample aborts have no committed timestamp, receipt, records or position effect.

**Draft derivation.** G-055 gate 1 concerns the routing triple, not typed record_id.
Removing recorded_at from the recognized closed set therefore makes it a D3 error:
BAD record_id plus recorded_at reports envelope_invalid before D4. A foreign profile
terminates at D2, so the same supplied member yields record_unrecognized. An admitted
unrecognized schema still validates compatibility before its terminal reader outcome
is mapped to strict-writer rejection. All generic stages precede these gates. This is
a faithful gate adaptation to G-082/G-083, not a reopened Layer 02 reading.

**Snapshot.** Repeatable Read Read Only gives one snapshot across range/tail/entry
queries; one SQL statement is also a valid alternative. A page ending at position 2
of a committed three-record batch is legal and remains bounded. A partially visible
in-progress batch and a through greater than its snapshot tail are prohibited.

## New finding: WP04-CR-007 — No shared advisory-lock identity for first open

- Classification: `CONTRACT_ASSURANCE_DEFECT`; representation/protocol mechanics,
  not a path-C semantic choice.
- Severity: MEDIUM; blocking: WP-04; status: OPEN; owner_decision_required: false.
- Requirements: PERS-005/014/015; reference-backend shared schema under G-079/G-081.
- Pinned evidence: docs `5cceb317`, `spec/persistence.md`, “Open and initialize”:
  opening creates v1 in one transaction “under a transaction-level advisory lock”
  if no mneme_ table exists. The matrix H8 schema row promises a concurrent-first-open
  control. Neither text specifies the common lock identifier, SQL overload/key
  namespace, or an agreed deterministic derivation. Unlike the existing-store row
  lock, an advisory lock has no implicit identity supplied by the table definition.

**Executed discriminating witness (PostgreSQL 14.12).** Start with no mneme_ tables.
Two openers each begin a transaction and call `pg_advisory_xact_lock` on their own
fixed integer (404001 and 404002). Each checks the schema while holding its lock;
a barrier ensures both see zero tables. Each executes exactly the candidate DDL
and inserts schema version 1. One succeeds; the other fails **SQLSTATE 23505**,
`duplicate key value violates unique constraint "pg_type_typname_nsp_index"`.
Both used the prescribed kind of advisory lock. They did not acquire the same
resource, so the stated mechanism alone did not serialize first opens.

**Positive discriminating control.** Reset only the throwaway schema. Both openers
instead call the same lock, key 404003, before inspection. Both succeed: the first
observes zero tables and initializes; the second observes four and opens v1. There
is exactly one schema/version initialization. These numeric keys are probe values,
not a proposal to adopt them in production.

**Required repair.** Define the shared initialization lock identity and its scope
in the reference-backend contract, including the exact SQL key representation or a
fully specified deterministic mapping. Require both languages to acquire that same
exclusive transaction-level lock before schema inspection and hold it through the
initialization/validation transaction. Add a mixed-language concurrent-first-open
witness to [CT]/[IT]; same-language concurrency alone cannot catch two different
hard-coded keys. Do not make Rust infer Python's private key from implementation.

This does not call the proposed shared schema intrinsically infeasible; the positive
control demonstrates the repair. It is a new omission on the newly specified open
surface, not survival of CR-001..006 or a reason to reopen their Owner decisions.
PostgreSQL documents advisory locks as application-defined resources in its
[advisory-lock section](https://www.postgresql.org/docs/14/explicit-locking.html#ADVISORY-LOCKS).

## Executed evidence and regression scope

Driver: `.tmp/work/codex/wp04-review-2.py`. Outputs:

- `.tmp/work/codex/wp04-2/oracle-rows.json`: **63/63** canonical observations match
  (12 + 19 + 12 + 4 + 16), including every new scenario expectation. Canonical-byte
  comparisons preserve numeric normalization without changing timestamp spelling.
- `.tmp/work/codex/wp04-2/pg-results.json`: PostgreSQL 14.12; exact bytea operation
  keys `00` and `610062` both round-trip, and lookup of `00` returns only its receipt
  row; singleton duplicate and false rows reject with 23505/23514; a tail above MAX
  rejects with 23514; the snapshot and concurrent-open witnesses above.
- `.tmp/work/codex/wp04-review-2.log`: captured execution output.
- `.tmp/work/codex/wp04-2/process-check.log`: deep-source process validation **8/8**.

The database was created with template0, UTF8, C/C collation and TABLESPACE mneme_ts,
using only mneme_dev credentials read from the project-local pg.env. It was dropped
after all probes; database absence was queried and confirmed. No credentials were
printed, no superuser was used, and all temporary files/environments/caches remain
under the E: project root. The only authored repository change is this record.

The new schema singleton and bounded columns are workable SQL representations.
The removed duplicate operation-ID record columns do not prevent receipt rebuilding:
the operation's original range identifies its immutable records. Commit serialization
continues to use the same unambiguous store row; CR-007 concerns only initialization.
No production implementation, contract, corpus, state, registry or source edits were
made; no remotes or pushes were used.

Q1's normalized retry witness now genuinely changes occurred_at and numeric spelling,
and the wider writer is a different recognized set. Q2 is resolved explicitly by
G-087 in the spec, plan and matrix; memory-bounded rebuild is no longer attributed
to Layer 03's whole-stream projector. Q3's singleton/open rule is a substantive
improvement, with the shared-lock protocol omission isolated as CR-007. Planned
schema-mismatch/crash/concurrency/capacity and interoperability implementation tests
still must be executed before certification; they are not claimed complete here.

Rust remains feasible from the revised contract, subject to pinning CR-007's common
initialization resource. No additional scenario mismatch or contract contradiction
was found in this re-review. Approval is withheld solely for WP04-CR-007.
