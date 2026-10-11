# WP-04 CE-04-01 — Claude's implementation record (single pass)

**Status: DRAFT — gate results PENDING.** The declared gate set runs only after Minion-Agent
reports "host clear" (Owner G-093). Until then this record lists the gates and the witnesses but
claims none of their results. Claude does not claim that WP04-CR-008 is closed; closure is Codex's.

**Authority:**
- the agreed checkpoint `assurance/convergence/CE-04-01-classification.md` rev. 2 (Codex
  `APPROVED`, `bfb6cad3`);
- `spec/persistence.md`, "Reference backend";
- Owner decisions G-088…G-093.

**Candidate:** code `b657081b96d67f7c2202c7fa541e1dceb09c8222` on `wp04/contract`, from frozen
`63462513`. Every gate result below binds to this exact SHA. Any code change makes the evidence
stale.

## 1. What changed

| File | Change |
|---|---|
| `minion_memory/persistence/catalog.py` (new) | <ul><li>Structured catalog **fetch**: nine parts, with every relation, type, function and operator `pg_catalog`-qualified.</li><li>A pure **comparison** (`mismatch`).</li><li>The environment predicate (`environment_mismatch`).</li></ul> |
| `reference-backend/postgres14-v1-catalog.json` (new, shared) | The v1 catalog pins, derived by executing the **normative DDL text** of `spec/persistence.md` (not the initializer) on PostgreSQL 14.12. |
| `minion_memory/persistence/_v1_catalog.py` (new) | The Python embedding of those pins. A test keeps it identical to the shared file. |
| `minion_memory/persistence/postgres.py` | <ul><li>Open sets `client_encoding` UTF8, then the environment check, then namespace resolution (`current_schema()`; with none, the engine's 3F000).</li><li>It initializes only with no `mneme_` non-index relation, under `SET LOCAL default_tablespace = ''` and `default_table_access_method = heap`.</li><li>The postcondition is checked by the same comparison before commit.</li><li>The version row is read.</li><li>The DDL and all operation statements use `pg_catalog` types and operators, and tables qualified by the namespace.</li></ul> |
| `tests/core/test_layer04_catalog.py` (new) | The CE-04-01 witnesses (§3). |
| `tests/core/test_layer04_store.py` | The rendered-SQL constants are replaced by the structured fetch. Its tests are otherwise unchanged. |

Unchanged:
- validation precedence;
- the operation transactions;
- the per-handle lock and the store-row lock;
- `synchronous_commit = on`;
- the read snapshot.

## 2. Pins, as Rust must read them

Each part is a sorted set of OID-free rows. `.` means "no collation" or "none".

| Part | Row fields, in order |
|---|---|
| relations | name, relkind, relpersistence, access-method name, reloptions, reltablespace (0 = default), reloftype (0), relispartition, relrowsecurity, relforcerowsecurity, relreplident, TOAST reloptions |
| inheritance | one marker row per `pg_inherits` row touching a `mneme_` relation (pinned empty) |
| policies / rules | relation name, object name (pinned empty) |
| triggers | relation, tgisinternal, tgenabled, function schema, function name, tgtype, linked constraint contype, constraint table, referenced table, tgconstrrelid table, tgdeferrable, tginitdeferred, tgnargs, cardinality of tgattr, tgqual is null, constraint table in scope |
| columns | relation, column name, type schema, type name, typtype, atttypmod, attnotnull, collation `schema.name`, attidentity, attgenerated, attstorage, attcompression, atthasdef, attndims, attislocal, attinhcount |
| defaults | relation, column, normalized `adbin` |
| constraints | relation, relation in scope, contype, condeferrable, condeferred, convalidated, connoinherit, conislocal, coninhcount, key column names, referenced relation, referenced in scope, referenced column names, confupdtype, confdeltype, confmatchtype, normalized `conbin` |
| indexes | relation, indisunique, indisprimary, indisexclusion, indimmediate, indisclustered, indisvalid, indisready, indislive, indisreplident, indnatts, indnkeyatts, key column names, operator classes `schema.name`, collations `schema.name`, indoption, indexprs is null, indpred is null, access method, index reloptions, index tablespace, contypes of constraints backed by it on the same relation |

Expression normalization removes every ` :location N` and replaces `:varattno N` and
`:varattnosyn N` with the column name. Constant bytes in a node tree are server byte order; the pins
come from x86-64.

## 3. Witness map

Each row is tagged with its evidence kind:
- **[P]** public;
- **[T]** transaction control;
- **[E]** direct engine control;
- **[Pr]** predicate.

Tests are in `tests/core/test_layer04_catalog.py` unless noted.

| Rows | Witness |
|---|---|
| R01 R02 R04 R31 R05 R06 R07 R08 R09 R40–R43 R10–R18 R33 R19 R20 R27 R28 R35 R37 C01–C15 C17–C19 C23–C28 K01–K08 K10 K11 I01–I13 I19 I20 H01 H02 CH01 CH02 CH04 CH05 CH06 CH09a CH09b | [P] `test_public_open_refuses_an_incompatible_catalog_and_changes_nothing[<row>]` |
| Additions, one rule and one trigger on each table, plus TOAST options | [P] same test, ids `RULE-operation`, `RULE-schema`, `TRIGGER-store`, `TRIGGER-schema`, `TOAST-options` |
| I14, I18, X08, X11, X02, CH09c | [P] `test_public_i14_…`, `test_public_i18_…` (the gated invalid-but-ready build), `test_public_x08_…`, `test_public_x11_…`, `test_public_x02_…`, `test_public_ch09c_…` |
| B01 R21 R22 R36 R38 R39 C16 C20 C21 C22 K09 CH08 S01–S05 S07–S09 S11 X06 X07 CH07, plus CH07b (a raising user `=` on oid, int2 and name) | [P] `test_public_open_accepts_a_v1_catalog_and_protocol_n_holds[<row>]` |
| B02, C16 with large payloads; B03/S10; X01, X03, X05 | [P] `test_public_large_payloads_round_trip`, `test_public_b03_s10_…`, `test_public_x01_x03_x05_…` |
| R23, R24; R25; X04, R34; S06, V02 | [P] engine errors propagate: `test_public_a_permission_error_propagates_atomically`, `test_public_r25_…`, `test_public_x04_r34_…`, `test_public_s06_v02_…` |
| D02, D03, D05 | [P] `test_public_d02_d03_d05_…`: refused before initialization, nothing created |
| V01 | [P] `test_the_normative_ddl_produces_the_pinned_catalog`, `test_the_initializer_produces_the_pinned_catalog_…` (three CHECKs, two defaults, eight enabled internal RI triggers) |
| X09, X10 | [T] `test_x09_x10_…`: a second session sees, at a gate, the advisory lock with `classid`/`objid` of the key, `objsubid = 1` and `granted = true` for the opener, then its release; the shadow marker has zero calls |
| CH11 pins (P44); the postcondition | [T] `test_initialization_pins_its_settings_against_session_defaults`; `test_initialization_checks_its_postcondition_before_commit` |
| CH12; the private session | [E] `test_ch12_…`: a baseline proves the poison binds unqualified names, then open's, the initializer's and the operations' texts give clean results. `test_the_handle_session_is_private_…` |
| R03 R30 R32 I15 I16 I17 CH03 CH10 CH11; D01 D04 accepted | [Pr] `test_predicate_a_non_constructible_difference_is_refused[…]`, `test_predicate_the_environment[…]`. Never reported as public executions. |
| R26 (ownership is non-semantic), R29 (covered by CH01) | none needed |
| shared pins | `test_the_embedded_pins_equal_the_shared_pin_file` |

## 4. Planted violations

| Set | Script | Contents |
|---|---|---|
| G4 | `.tmp/work/claude/py_mutants_ce0401.py` | 42 entries, each with its intended witness and a baseline run first. Re-anchored P01, P06 and P15; the per-part comparison mutants P24\*; P25–P54. |
| G5 | `.tmp/work/claude/py_mutants_wp04.py` | The unchanged WP-04 set: P02–P05, P07–P14, P16–P20 and P23. P14 is the known equivalent. |

Two G4 entries are expected to survive as **engine-constrained equivalents**:
- **P32** (fetch ignores index validity and readiness);
- **P40** (fetch ignores trigger activation).

A non-valid or non-ready **backing** index, or a disabled **internal** trigger, cannot be built by
an ordinary role. Any constructible extra index or user trigger is already refused by its existence.
The comparison side of both properties is killed by predicate tests (`I16 invalid backing index`,
`R32 disabled internal RI trigger`). If either is killed, or another entry survives, the record
reports it as observed.

## 5. Gates (declared; `.tmp/work/claude/ce0401_gates.sh`)

| Gate | Command | Result |
|---|---|---|
| G0 | candidate SHA and a clean tree | PENDING |
| G1 | `ruff check`, `ruff format --check`, `mypy --strict src tests` | PENDING (clean at commit time in development; not counted as gate evidence) |
| G2 | full suite `pytest tests` | PENDING |
| G3 | coverage of all of `minion_memory`, with branches and subprocesses and no exclusions (`wp04.coveragerc`) | PENDING |
| G4 | CE-04-01 planted violations | PENDING |
| G5 | WP-04 planted violations | PENDING |

The pre-gate development checks under the reservation were small, serial and throwaway:
- 15 of Claude's probes;
- about 45 tests of the new module (predicates, pins, CH12, X09, the transaction controls, CH07b,
  D02/D03, and ten public rows).

They are not gate evidence.

## 6. Rust hand-off notes (for the later Rust candidate; not a hand-off yet)

- **From the contract and the shared pins only**, never from Python's code:
  - the environment, namespace, initialization (pins and postcondition) and version steps of
    `spec/persistence.md`;
  - the catalog contract;
  - the genuine-object rule.
- **Embed `reference-backend/postgres14-v1-catalog.json`** and test the embedding against it. Its
  fetch must produce the row layout of §2.
- **The API opens its own connection** from parameters and creates no temporary objects (the
  private-session invariant). State this with evidence.
- **Port the witness classes:**
  - the public rows;
  - CH07/CH07b;
  - CH12, in a poisoned session over Rust's own SQL texts;
  - X09 with `granted = true`;
  - the transaction controls;
  - the predicates.
- **[IT] cross-language:**
  - a schema initialized by Python is opened by Rust and passes protocol N, and the reverse;
  - a retry committed by one language returns the same receipt in the other.

## 7. Next

- After "host clear", run `ce0401_gates.sh` fresh at `b657081b`.
- Fill in §5 with the literal outputs.
- Hand to Codex for CE-04-01 closure.
