# WP-04 CE-04-01 checkpoint review — Codex

**Verdict: CHANGES_REQUIRED**

Reviewed docs state `41d5b253f9cb945b26a69e9c02317c6747fd6d1f`: classification revision 1, the reference-backend contract transcription, and verbatim G-089..G-092. Behavior reference: frozen code `634625135851cccc188fe726acb86990911ebddb`. This verdict concerns the proposed convergence checkpoint, not candidate acceptance. Production remains frozen. WP04-CR-009..011 remain resolved and outside this episode.

Three blocking contract-assurance findings follow. Neither C02 nor C03 requires a new Owner decision on the evidence reviewed. No new semantic choice is made in this record.

## Independent executions

Used the separate frozen code checkout, the project-managed CPython 3.12.8 venv with psycopg 3.2.13, PostgreSQL 14.12 and the non-superuser `mneme_dev`. Every shell sourced the project environment. Two private databases were created with template0, UTF8/C/C and `TABLESPACE mneme_ts`, and dropped in finally blocks. All notes/cache/probe files stayed inside the E: project. No production changes, administrator credentials, service changes, test suite, mutant batch or Docker batch were used. These were small throwaway-schema probes under the continuing host reservation.

Fresh schema for each public-open cell; public protocol N is the characterization's literal create/commit/identical retry/read/tail protocol. Expected successful range 1..2, identical retry, positions [1,2], tail 2. These results come from my own executions, not Claude's reproduction record:

| Cell | Executed setup | Frozen observation | Checkpoint judgement |
| --- | --- | --- | --- |
| CH01 | Recreate record table partitioned by LIST(store_id), with all normative columns/constraints and a default partition | open: `persistence.schema_incompatible` | KEEP reject confirmed. Constructible full-constraint partitioned case; the actual predicate causing refusal is not inferred from the result. |
| CH02 | Outside table with FK to mneme_store, ON UPDATE CASCADE | open accepts; N true | FIX reject consistent with finite initializer catalog contract. |
| CH04 | Composite type with record's seven columns; ALTER TABLE mneme_record OF that type | `reloftype` nonzero; open accepts; N true | FIX reject confirmed independently; no longer only a proposed fixture. |
| CH05 | Policy USING(false), RLS not enabled | open accepts; N true | FIX reject confirmed. Presence of policies is forbidden independently of current activation. |
| CH06 | BEFORE INSERT row trigger on mneme_operation returning NULL | open accepts; first receipt 1..2; retry raises `history.duplicate_record_id` | FIX reject confirmed; receipt loss is observable. |
| CH07 | Raising user text/text `=` operator with schema before explicit pg_catalog | open accepts; create succeeds; first commit calls shadow, P0001 | FIX accept with N true and zero shadow calls confirmed as necessary. |
| CH08 | CREATE STATISTICS on profile, record_type | open accepts; N true | KEEP accept confirmed by G-089 statistics exemption. |
| CH09/view | Extra mneme_extra view beside initialized four tables | open accepts; N true | **FIX reject**, not KEEP reject. |
| CH09/sequence attempt | CREATE SEQUENCE mneme_extra beside initialized tables | setup timed out, SQLSTATE 57014; no public open credited | Construction limit of this execution; no sequence result inferred. No retry batch was launched. |
| CH09/initialization | Only mneme_extra view exists before first public open | open accepts, durably creates all four tables and header, N true; view remains | Refusal must apply to initialization too; steps 3/4 currently conflict. |
| PIN_TEMP | Direct engine probe of proposed alternative, SET search_path=pg_catalog with session-local pg_class table and text domain | unqualified pg_class binds temporary OID 35626, not engine OID 1259; unqualified text cast invokes restrictive temporary domain, 23514; qualified cast succeeds | Proposed strategy does not make pg_temp unreachable. This is **not** a claimed frozen public-open result. |

The time-out is reported as a setup limit, not a validator rejection or a killed control. Both databases were dropped, including its residual schema. CH03 and CH10 remain construction-limited; no other server major, non-heap extension or privileged trigger-disable fixture was executed.

## Blocking findings

### CE04-CP-001 — proposed pg_catalog-only strategy leaves implicit temporary lookup

- Classification: **CONTRACT_ASSURANCE_DEFECT**.
- Severity: **medium**; blocking: CE-04-01 checkpoint / WP-04.
- `owner_decision_required: false`; repair follows the already-required genuine-object rule.
- Evidence: classification at reviewed docs SHA, §5.2, line 181, permits setting search_path to pg_catalog alone and qualifying the store tables, stating that this also makes pg_temp unreachable. The contract, spec/persistence.md lines 427..429, requires genuine built-in types as well as functions/operators/aggregates.

Minimal direct-engine counterexample, in one private connection:

```sql
SET temp_tablespaces=mneme_ts;
CREATE TEMP TABLE pg_class (shadow integer);
CREATE DOMAIN pg_temp.text AS pg_catalog.text CHECK(false);
SET search_path=pg_catalog;
SELECT pg_catalog.to_regclass('pg_class')::oid,
       'pg_catalog.pg_class'::regclass::oid;
-- actual: 35626, 1259 (first OID is run-local)
SELECT 'x'::text;            -- actual CheckViolation 23514
SELECT 'x'::pg_catalog.text; -- actual 'x'
```

PostgreSQL searches an existing implicit temporary schema first for relation and type names even when pg_catalog is the only explicit path entry. This is documented and independently executed. [PostgreSQL 14 client settings, search_path](https://www.postgresql.org/docs/14/runtime-config-client.html)

Qualifying the four store tables alone does not authenticate catalog relations or type references. The first strategy also enumerates functions/operators/aggregates without explicitly addressing catalog relation/type lookup. The encompassing contract is correct; the stated implementation alternatives and their evidence are incomplete. A fresh Python connection currently lacking temporary objects does not make the general PostgreSQL assertion true or supply a cross-language invariant.

Required repair: remove the false assertion and require actual engine catalog relations/types under the chosen strategy. Add a discriminating pre-inspection temporary relation/type control or state and prove the invariant excluding that state for both language backends. Preserve namespace resolution before any path rewrite. Existing shadow function/operator controls alone cannot close this gap. This is a repair of genuine lookup, not permission to reject an otherwise valid schema because unrelated temporary objects exist.

### CE04-CP-002 — CH09 is a FIX and the empty-table branch bypasses the finite catalog rule

- Classification: **CONTRACT_ASSURANCE_DEFECT**.
- Severity: **high**; blocking: CE-04-01 checkpoint / WP-04.
- `owner_decision_required: false`; G-089 decides the rejection.
- Evidence: classification §2 CH09 line 49 says unexecuted/FIX-or-KEEP, but §4.2 line 108 and §4 accounting line 159 place it in KEEP reject. Independently executed view case accepts. Spec/persistence.md lines 394..397 initializes when no mneme_ **table** exists; lines 404..406 require exactly four prefixed non-index relations, explicitly forbidding prefixed views/sequences.

Two minimal cases, both independently executed:

1. After public initialization, `CREATE VIEW mneme_extra AS SELECT 1 AS x`; frozen public open accepts and N succeeds. The oracle is incompatible. Hence CH09/view must be **FIX reject**.
2. In a fresh private schema, create only that view and then call public open. Frozen open accepts, creates all four tables/header, and leaves the view. N succeeds. The candidate transcription's numbered step 3 also permits this because no mneme_ table existed, while the stated finite v1 relation contract forbids the result.

Required repair: make the empty/initialize condition and its postcondition consistent with the complete prefix relation/catalog rule. An incompatible preexisting prefixed object must not trigger successful durable initialization. Add both the beside-existing-tables and before-first-open controls; the latter must assert no schema/store mutation on refusal. Correct CH09's disposition and extra-row accounting. The original 136-row counts need not change; the ten challenge rows' KEEP/FIX counts do.

This is not an Owner choice about accepting auxiliary views: G-089 and the transcription already decide that mneme_-prefixed non-index relations are incompatible. Unprefixed unrelated objects remain a different case (R36).

### CE04-CP-003 — G-092's after-open exclusion is broadened to an open-time trigger exemption

- Classification: **CONTRACT_ASSURANCE_DEFECT**.
- Severity: **medium**; blocking: CE-04-01 checkpoint / WP-04.
- `owner_decision_required: false`; G-089/G-092 determine the boundary.
- Evidence: classification §4.4 line 128 marks R32 construction-limited and adds “G-092 puts it outside.” Contract Trust scope lines 432..438 lists disabled internal constraints/triggers without making the exclusion's timing explicit. Relation contract lines 405..412 permits PostgreSQL internal foreign-key triggers but does not explicitly state their initialized activation/linkage oracle. §6's trigger controls only cover user triggers.

The Owner's verbatim G-092 at governance line 232 requires open to verify the **complete certified v1 catalog contract before returning a usable handle**, and excludes administrator interference **after open**. G-089 requires all catalog properties capable of changing accepted writes/transaction behavior, including triggers. A disabled internal FK trigger is not the initializer's finite state. A genuine engine can record that state following privileged ALTER before open; it is not necessarily manual catalog corruption. PostgreSQL exposes activation through pg_trigger.tgenabled.

R32 correctly remains NOT CREDITABLE as a kill: my characterization's actual ALTER attempt was refused with 42501, and I did not use superuser credentials. That construction limit does not authorize omitting an observable initialized trigger property from validation. Likewise, no data scan or repeated validation after open is required.

Required repair: retain the construction limit, distinguish pre-open incompatible catalog state from post-open out-of-band changes, and make the finite internal-FK-trigger oracle explicit (including initialized enabled state and genuine constraint linkage/function identity, modulo irrelevant names/OIDs). State how the implementation verifies those properties and how any nonconstructible kill is bounded or tested as a predicate. Do not claim a public privileged-fixture kill that was never executed. No new threat model or per-operation catalog scan is requested.

## Other checkpoint judgements

### C02 and C03

**C02 discharge accepted as path A**, subject to CE04-CP-001/002 repairs. The unqualified normative DDL selects the first usable current schema; inspection and operations must stay bound to that same namespace. This is standard PostgreSQL schema behavior, not a newly selected store identity rule. A missing current schema surfaces a genuine engine initialization error. Genuine built-ins cannot be substituted merely because search_path changes. [PostgreSQL 14 schemas](https://www.postgresql.org/docs/14/ddl-schemas.html)

**C03 discharge accepted as path A.** G-089 explicitly exempts ownership/grants from catalog identity; open need not preflight every later privilege. A permission failure must propagate and roll back, not become schema_incompatible or success. This reading preserves the existing transaction/DDL failure rules and does not relax v1 shape, RLS, or write semantics. Role names/owner OIDs alone cannot establish privileges; the classification does not require such a check. No extra Owner choice is identified.

### Owner transcription and all original 136 rows

- G-089's strict initializer-state acceptance with the enumerated identity exemptions is transcribed, including explicit C/POSIX **column** collation rejection when it differs from the default catalog collation, extra-index rejection and physical-tuning rejection. Database locale C/POSIX acceptance under G-090 is a separate property. No semantic-equivalence permission was silently introduced.
- G-090's environment check before creation/acceptance and handle-established UTF8 client encoding, plus G-091's major-14-only rule, are transcribed faithfully. D02 now needs a first-open refusal/no-mutation control, not only its former second-open failure. G-091 permits 14.x; 14.12 remains the actual executed certification version, not a claim of executions on other minor releases.
- The structured-expression oracle correctly avoids rendered SQL, but §5.3 says **two** CHECK conditions. The DDL has **three**: singleton, tail range, position range. Correct that inventory before implementation and preserve all three condition controls. The surrounding normative exact-constraint rule already requires all three; this is an additional correction, not a new semantic finding.
- Original disposition groups were checked as disjoint sets covering the characterization's 136 IDs. Counts 24 KEEP accept, 5 FIX accept, 62 FIX reject, 26 KEEP reject, 7 engine errors, 1 FIX lock, 1 attached observer and 10 NOT CREDITABLE sum to 136. No missing/duplicate original ID was identified. The challenge additions' CH09 accounting is wrong as CE04-CP-002 explains.
- R21 is KEEP accept: the executed ALTER to database-default mneme_ts leaves reltablespace 0. C16 is KEEP accept: explicit EXTENDED equals the initializer's bytea storage. These are catalog-identical states, not new physical-tuning exemptions.
- C05/C06 are FIX reject: their explicit C/POSIX column collation OIDs differ from the initializer's database-default collation. Their observed bytewise behavior does not exempt the different catalog state under G-089.
- Constraint name K09, column order C22, dropped residue C20, statistics C21/CH08 and lazy flags R38/R39 are treated as identity/statistical history, not new semantic state. Transient/lazy catalog flags must not become impossible literal equality pins; G-089 calls for the properties changing guarantees and exempts planner statistics/identity. Cross-database OIDs are not portable expected values.
- I08..10 remain FIX reject based on the **effectful residual extra indexes**, despite failed constraint attachment. I15/I16 are NOT CREDITABLE as opclass/collation kills because their actual refusals observe a missing PK. R03/R26/R29/R30/R32/I15/I16/I17/D01/D04 construction limits are otherwise correctly retained. CH03/CH10 similarly require bounded direct predicates/engine assumptions, not imaginary public executions.
- The remaining original FIX/KEEP oracles follow G-089..G-091 and the genuine-object rule. No original closure is reopened by disagreeing with its acknowledged status. X10 remains an observation attached to X09, not another open.

### Lock and evidence obligations

X09's decided oracle is right: actual single-bigint engine transaction lock, exact key, held across inspection until commit/rollback, plus zero shadow calls. A second-session pg_locks witness must identify the expected classid/objid, single-bigint overload and **granted=true** for the opening backend while it is held at a later observation gate. A waiter with granted=false does not prove acquisition. Observe release at transaction end; do not infer the lock from merely not calling the shadow function. This clarifies the evidence, not a different locking contract.

Public fresh-schema witnesses for every FIX plus KEEP controls, actual wrong-environment/no-mutation cases, both language initialization/open interoperability, major-version predicate, G3 and planted violations are appropriate. “Every FIX” must incorporate the repaired CH09 and initialization control. The lookup strategy must cover relation/type shadowing as well as CH07/functions/aggregates, and the internal-trigger boundary must be explicit before claiming one-pass completeness. An unconstructible backing-index state is not automatically a killed P30: any equivalence/engine invariant claim needs its own explanation as §6 already allows.

Full suites, mutation batches, POSIX/Docker and G3 were not rerun in this checkpoint; the host reservation remains in force. Their execution obligations apply after host clear and implementation, not as fictional checkpoint evidence.

## Evidence retained

Project-local files in `.tmp/work/codex/ce04-01/`:

- `checkpoint_probe.py`, `checkpoint-observations.jsonl`, `checkpoint-probe.log` (independent challenge reproductions and direct temporary-lookup probe).
- `checkpoint_initialize_probe.py`, `checkpoint-initialize-observation.json`, `checkpoint-initialize.log` (empty-table-branch witness).
- Original `rows.jsonl` and characterization recipes (unchanged reference evidence).

No secrets are in this review. All throwaway databases were dropped with ordinary DROP of their own names, no FORCE/foreign-session termination. Only this review record is committed on `review/wp04-ce1-checkpoint` from the pinned docs state. Claude should repair the three findings and the CHECK inventory/lock-observer clarification, then present a revised checkpoint. This record does not authorize production edits.
