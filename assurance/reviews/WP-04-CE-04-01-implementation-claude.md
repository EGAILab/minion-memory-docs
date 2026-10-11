# WP-04 CE-04-01 — Claude's implementation record (single pass)

**Status: SUBMITTED for Codex closure review — gates run.** Minion-Agent reported "host clear" on
2026-10-12 (G-093 condition met). The declared gates ran twice:
- **run 1** at `b657081b` **failed G4** (nine survivors, seven unexpected);
- **run 2** at `be36323f`, a tests-only remediation of the three gaps run 1 exposed.

Both runs are reported in §5. Claude does not claim that WP04-CR-008 is closed; closure is Codex's.

**Authority:**
- the agreed checkpoint `assurance/convergence/CE-04-01-classification.md` rev. 2 (Codex
  `APPROVED`, `bfb6cad3`);
- `spec/persistence.md`, "Reference backend";
- Owner decisions G-088…G-093.

**Candidate:** code `be36323f56e61d87776d11c831ae1ef0573ea692` on `wp04/contract`.
- Its parent `b657081b` is the single implementation pass from frozen `63462513`.
- `be36323f` adds tests only: 24 lines in `tests/core/test_layer04_catalog.py`, with no production
  change.

The run 2 results bind to `be36323f`. The run 1 results bind to `b657081b` and are kept as the
record of the failure. Any code change makes the evidence stale.

## 1. What changed

| File | Change |
|---|---|
| `minion_memory/persistence/catalog.py` (new) | <ul><li>Structured catalog **fetch**: nine parts, with every relation, type, function and operator `pg_catalog`-qualified.</li><li>A pure **comparison** (`mismatch`).</li><li>The environment predicate (`environment_mismatch`).</li></ul> |
| `reference-backend/postgres14-v1-catalog.json` (new, shared) | The v1 catalog pins, derived by executing the **normative DDL text** of `spec/persistence.md` (not the initializer) on PostgreSQL 14.12. |
| `minion_memory/persistence/_v1_catalog.py` (new) | The Python embedding of those pins. A test keeps it identical to the shared file. |
| `minion_memory/persistence/postgres.py` | <ul><li>Open sets `client_encoding` UTF8, then the environment check, then namespace resolution (`current_schema()`; with none, the engine's 3F000).</li><li>It initializes only with no `mneme_` non-index relation, under `SET LOCAL default_tablespace = ''` and `default_table_access_method = heap`.</li><li>The postcondition is checked by the same comparison before commit.</li><li>The version row is read.</li><li>The DDL and all operation statements use `pg_catalog` types and operators, and tables qualified by the namespace.</li></ul> |
| `tests/core/test_layer04_catalog.py` (new) | The CE-04-01 witnesses (§3). |
| `tests/core/test_layer04_store.py` | The rendered-SQL constants are replaced by the structured fetch. Its tests are otherwise unchanged. |
| `tests/core/test_layer04_catalog.py` (`be36323f`, tests only) | The three witness gaps run 1 exposed (§5.1). |

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
| Additions in `be36323f`: row security without a policy (enabled, forced, both); a different value for an existing default | [P] same test, ids `RLS-enabled`, `RLS-forced`, `RLS-enabled-forced`, `DEFAULT-tail`, `DEFAULT-singleton` |
| Addition in `be36323f`: before initialization, a non-table relation with a v1 table name (view `mneme_store`, sequence `mneme_record`) | [P] `test_public_ch09c_a_non_table_with_a_v1_name_blocks_initialization[…]`: refused, nothing created |
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

Two G4 entries were **predicted before any run** to survive as engine-constrained equivalents:
- **P32** (fetch ignores index validity and readiness);
- **P40** (fetch ignores trigger activation).

A non-valid or non-ready **backing** index, or a disabled **internal** trigger, cannot be built by
an ordinary role. Any constructible extra index or user trigger is already refused by its existence.
The comparison side of both properties is killed by predicate tests (`I16 invalid backing index`,
`R32 disabled internal RI trigger`).

A third equivalence is **claimed after run 1** and was not predicted: **P38**, where the fetch reads
only constraints whose own relation is in scope.
- **The claim.** The only constraint an outside relation can hold that names a `mneme_` relation is
  a foreign key into it.
- **Why that is enough.** PostgreSQL always creates the internal RI triggers for such a key on the
  referenced `mneme_` table, and those triggers are in scope. So every constructible instance is
  already refused by the triggers part.
- **What it rests on.** The claim is an argument, not a test. Codex should challenge it.

Changes to the planted-violation table after run 1 (`py_mutants_ce0401.py`):
- **Labels.** They are now unique: P24-`part`. In run 1, P24c, P24r and P24i each named two
  mutants. This did not affect run 1, which ran unfiltered.
- **Witnesses re-pointed** for six entries: P24-columns → C13, P24-constraints → K03, P24-defaults
  → `DEFAULT-tail`, P29 → `RLS-enabled` and `RLS-forced`, P33 → R05, P46 → the new v1-name test.
- **P38** is tagged `equivalent?`.

Each change is justified by `diag-survivors.log` (§5.1). No mutant body changed.

## 5. Gates (declared; `.tmp/work/claude/ce0401_gates.sh`)

All logs are under `.tmp/work/claude/`:
- run 1 in `ce0401-gates/`;
- run 2 in `ce0401-gates-be36323f/`.

Each run directory has a `summary.txt`.

| Gate | Command | Run 1 at `b657081b` | Run 2 at `be36323f` |
|---|---|---|---|
| G0 | candidate SHA and a clean tree | clean | clean |
| G1 | `ruff check`, `ruff format --check`, `mypy --strict src tests` | exit 0 | exit 0 |
| G2 | full suite `pytest tests` | exit 0: 706 passed, 4 xfailed¹ | exit 0: **713 passed, 4 xfailed** in 121.63 s |
| G3 | coverage of all of `minion_memory`: branches and subprocesses, no exclusions (`wp04.coveragerc`) | 1265 statements, 490 branches, 0 missed: 100 % | 1265 statements, 490 branches, 0 missed: **100 %** |
| G4 | CE-04-01 planted violations (42), intended witness, baseline first | **FAILED**: 33 killed, 9 survived (§5.1) | **39 killed**; 3 survived: P32, P38, P40, each claimed engine-constrained equivalent (§4) |
| G5 | WP-04 planted violations (18) | 17 killed; P14 survived (known equivalent) | **17 killed**; P14 survived (known equivalent) |
| post | sources untouched after the mutant runners | clean | clean |

¹ Run 1's script passed a second `-q`, which hid pytest's count line, because `pyproject` already
has `-q`. The 706 is a count of the progress dots. An interim reading of three "skips" was a
miscount: stray `s` characters from the log text. Run 2 prints pytest's own count line:
706 + 7 new cases = 713, with no skips.

The four xfails are the TO_BE_ placeholder scenarios of layers 08 and 15.

### 5.1 Run 1's G4 survivors, and what was done

As a diagnostic, not gate evidence (`ce0401_survivor_diag.py`, log
`ce0401-gates/diag-survivors.log`), each survivor was applied and the whole witness module was
run without `-x`:

| Survivor | Module failures | Classification | Action |
|---|---|---|---|
| P24 comparison ignores columns | 11 (C04, C13–C15, C17–C19, C24, C26, C28, X08) | wrong intended witness: C01 also differs in the indexes part | re-pointed to C13 |
| P24 comparison ignores constraints | 4 (K03, K04, K10, K11) | wrong intended witness: K05 also differs in the triggers part | re-pointed to K03 |
| P33 inheritance not read | 1 (R05) | wrong intended witness: R06 also differs in the columns part | re-pointed to R05 |
| **P24 comparison ignores defaults** | **0** | **witness gap**: no row changed an existing default's value (C11 adds a default, so columns differ first) | `DEFAULT-tail`, `DEFAULT-singleton` |
| **P29 row security not read** | **0** | **witness gap**: every row-security row also created a policy | `RLS-enabled`, `RLS-forced`, `RLS-enabled-forced` |
| **P46 initialization beside a prefixed non-table** | **0** | **witness gap**: CH09c's `mneme_extra` view is refused by the postcondition either way. A non-table **with a v1 table name** makes the mutant fail with the engine's duplicate-relation error instead of `schema_incompatible` | `test_public_ch09c_a_non_table_with_a_v1_name_blocks_initialization` (view `mneme_store`, sequence `mneme_record`) |
| P32, P40 | 0 | predicted engine-constrained equivalents | none |
| P38 outside constraints not read | 0 | claimed engine-constrained equivalent (§4) | none |

The three gaps were behaviors the implementation already had, and the evidence obligations of §6
already required them to be witnessed. The remediation is witnesses only, so production code is
unchanged.

The development checks before the gates were not gate evidence:
- probes, and subsets of the module, run during development;
- a pre-check of the six re-pointed mutants at `be36323f` (all killed).

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

- Codex reviews CE-04-01 closure for the exact pair: code `be36323f`, with the docs commit that
  carries this record.
- Particular points for challenge:
  - the P38 equivalence claim;
  - whether a tests-only remediation after the single implementation pass is acceptable under the
    checkpoint;
  - the witness re-pointing.
