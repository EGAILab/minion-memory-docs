# WP-04 CE-04-01 targeted closure review 2 — Codex

**Verdict: APPROVED**

Exact pair: code `038416286631a34846f99bd53b7c4d6ed41d30cf`, docs
`a1d9252c4911ddffb49ee2faa530bbb75b5d4f5d`. Review branch:
`review/wp04-ce1-closure-2`, from that docs state head. Authority: the agreed
CE-04-01 checkpoint revisions 2–5, `spec/persistence.md` reference-backend
catalog contract and Trust scope, and G-088..G-098. This approves the submitted
candidate for this targeted closure; it grants neither main acceptance nor
Layer 04 certification.

I used separate exact checkouts and the ordinary `mneme_dev` role. No production
module, shared pin, contract, state or registry was edited. CR-009..011 remain
resolved and outside the episode. No new Owner semantic choice is proposed.

## Finding dispositions

| Finding | Disposition at this exact pair | Independent evidence |
|---|---|---|
| WP04-CR-008 | CLOSED against the agreed, extended v1 catalog contract | Full classified witness suite, whole-row inventory, predicate/fetch negative controls, normative-DDL baseline and public boundary probes below. |
| WP04-CR-012 | CLOSED | Repeated the pre-open DROP/ADD tail DEFAULT 1 / restore DEFAULT 0 witness with an old store: fetch differs in `columns`; public reopen raises `persistence.schema_incompatible`. Flag-only, cache-only and type-copy fetch controls pass and kill P55/P68/P65. E004 retains its distinct, agreed materialized-row oracle. |
| WP04-CR-013 | CLOSED | Repeated the ordinary-role outside constraint trigger `FROM mneme_store`: fetch differs in `boundary`; public reopen raises `persistence.schema_incompatible`. Row-type and array-type references also differ in boundary and are refused. The inbound/outbound, statistics-class and member-certification controls kill their intended violations. |
| WP04-CR-014 | CLOSED | P40 is killed by the actual-fetch projection of disabled activation, not by a physical/public privileged ALTER. P32 validity/readiness is likewise fetch evidence. Earlier survivor records remain intact. |

## Own executions

All recipes, logs and observations are under `.tmp/work/codex/ce04-closure2/`.
Managed Python is CPython 3.12.8; psycopg is 3.2.13; the database server is
PostgreSQL 14.12. Environment scripts were sourced for each shell; scratch,
interpreter dependencies, pytest temporary directories and images stayed in
the project. Gate batches ran sequentially. Both requested Minion-Agent host
windows were honored; no gate result is credited from concurrent batches.

| Execution | Result / evidence |
|---|---|
| Windows static checks | `ruff check .`, `ruff format --check .`, `mypy --strict src tests`: pass. |
| Windows full suite, exact candidate | **856 passed, 4 xfailed**, 248.82 s; `windows-suite.log`. |
| Fresh Windows coverage | **1304/1304 statements, 490/490 branches**, zero misses, 100%; subprocess data combined, no exclusions. `coveragerc`, `coverage.json`, `coverage-report.txt`. |
| Independent G4 replay | **58 killed / 59**; only P38 survives. `mutations.py`, `mutation-results.json`, per-control baseline and mutant logs. |
| Independent selected G5 replay | **17 killed / 18**; only P14 survives. Same results file, rows 60–77. |
| Direct catalog neighborhoods | `audit.py`, `audit-results.json`, `audit.log`: 11 public/boundary cases and 5 patched-row observations. Own UTF8/C/C database created in `mneme_ts`, then dropped. |
| POSIX full suite | **856 passed, 4 xfailed**, 334.06 s; `posix-suite.log`, `posix-orchestrator.log`, `posix.sh`, `run-posix.py`. Linux Python on a case-sensitive ext4 image under E: (A/a distinct), against the same Windows PostgreSQL server through own temporary relays; not a Linux PostgreSQL-server claim. |
| Shared process checks | `mneme-process check --deep-sources`, exact pair: **8/8**; `process-check.log`. |

The replay copied source into an isolated scratch tree, applied one exact
mutation at a time, and restored original bytes after every run and in cleanup.
Each distinct ordered witness selection first passed against the baseline;
identical selections reuse that baseline result. No collection, syntax or
fixture setup failure was credited as a kill. Failure assertions/exceptions
were inspected, not merely return codes. The initial audit recipe had a quoting
error before execution; it made no database changes and supplies no evidence.
The corrected recipe supplies the observations above.

## Whole-row comparison and boundary

The normative-DDL baseline agrees with the shared and embedded pins and passes
public protocol N: positions 1..2, equal retry receipt, read [1, 2], tail 2.
The whole-row member comparison includes live `pg_class`, `pg_index`,
`pg_attribute` and `pg_type` fields, removes only the named exclusions, and
normalizes the agreed associations, type copies and count invariants. The live
inventory test passes: compared and excluded keys are disjoint and exhaustive,
and normalized keys are compared. The members and index_columns skip controls
are killed; TOAST ordering/options, index descriptors, row-type fields and
array backlinks have actual-fetch controls rather than predicate-only claims.

Discovery does not alone grant acceptance: member cardinality/shape and
association comparison certify the discovered internal members before an open
can succeed. The separately executed row-type and array references demonstrate
the inbound boundary; statistics and comments remain accepted and pass N.
Security labels, outgoing user dependencies and the widened-statistics-exemption
negative controls retain their classified oracles. I found no new disagreement
with the agreed rows. This is not a claim to reject dynamic references lacking
recorded catalog dependencies, audit stored history, or cover arbitrary engine
corruption outside the agreed trust scope.

## Re-pointed witnesses, equivalence and implement-once

The run-3 failure remains a failure. `03841628` changes two test files only:
80 added lines and 2 removed, with production unchanged from `426f14f3`.
The three single-part predicates isolate comparison skips. The table-persistence
fetch projection isolates that read from its physical TOAST consequence. The
P01 open-before-commit barrier creates the missing overlap; removal of the
store-row lock now produces conflicting writers and fails the witness. These
strengthen evidence for the agreed oracle rather than change production
semantics or select new requirements. They are legitimate tests-only repairs
under implement-once, with the failed run preserved.

The five patched-row controls pass through the actual fetch SQL. My complete
part comparisons are:

| Projection | Differing parts |
|---|---|
| Internal RI trigger copied with `tgisinternal = false` | triggers |
| Outside rule redirected to a core table | rules |
| Outside policy redirected to a core table | policies |
| Outside index redirected to a core table | **indexes, index_columns, boundary** |
| Outside inheritance edge redirected to a core table | inheritance |

For P31, loss of the indexes read changes the first mismatch from `indexes` to
`index_columns`, and the intended fetch assertion fails. This is a valid bounded
dataflow kill; it is not a public false-pass witness or a single-part projection.
Changing island membership makes existing dependency edges cross even though
the projection adds no dependency row. None of these controls is credited as a
physical altered-catalog execution.

P38's exact confrelid-clause omission remains redundant in the narrower,
previously reviewed inbound-FK scope. I independently executed ordinary,
NOT VALID, deferred and partitioned FKs: baseline differences are triggers,
constraints and boundary; after removing that clause in transient query text,
triggers and boundary still differ. The text was restored. The formerly missed
FROM-trigger route is now refused independently by boundary. This does not
generalize P38 to all possible outside references. P14 remains equivalent
because gapless positions make `min(since + limit, tail)` the through-boundary
for a nonempty page, with the agreed empty-page behavior.

## Non-blocking documentary finding

### WP04-CR-015 — current witness overview overstates isolation and retains old counts

- Classification: **CONTRACT_ASSURANCE_DEFECT**; severity: **low**.
- `owner_decision_required: false`; `blocking: [none]`; status: **OPEN**.
- Sources: exact docs above, implementation record 2 §2 and §5.1; exact code
  above, `tests/core/test_layer04_catalog.py`, patched-row comment and controls.
- Executed evidence: `audit-results.json`, all five patched-row observations;
  collection guard/full suite and mutation logs.

The current overview says 55 extension predicates and 17 field controls; the
candidate has **58** and **18**. Its five-row caption says every source is an
unrelated object and only one part changes. The trigger source is an existing
core RI trigger; the index projection changes three parts, as measured above.
Correct the overview/caption and explain P31 as an intended-part fetch kill.

This does not block the four targeted closures: current gate totals are correct,
the evidence kind is explicitly [F], and the exact intended mutant is genuinely
caught by loss of its read. This review supplies the corrected observations and
bounds the claim. Repair the author record and test comment before Layer 04's
final assurance/certification; no production repair or convergence reopening is
required for this documentary issue.

No blocking finding remains for this targeted candidate.
