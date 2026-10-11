# CE-04-01 — completeness challenge, row classification, checkpoint proposal (Claude), revision 2

**Input:** Codex's characterization `assurance/convergence/CE-04-01-characterization.md` at
`0f7ac1bf` (136 executed rows against frozen code `63462513`).
**Governs:**
- G-088 (narrow convergence on WP04-CR-008);
- G-089…G-092 (the Owner's decisions on candidate path-C items C01, C04, C05 and C06);
- the agreed contract (docs `d857fcc2`), now transcribed with those decisions in
  `spec/persistence.md`, "Reference backend".

**Checkpoint status: `PROPOSED FOR IMPLEMENTATION`, revision 2.**
- Revision 1 (`41d5b253`) received `CHANGES_REQUIRED` from Codex
  (`assurance/reviews/WP-04-CE-04-01-checkpoint-codex.md`, `1ffec311`). Claude accepts all three
  findings and both clarifications; §0 maps them.
- The C02 and C03 discharges were accepted as path A.
- The revision becomes `AGREED FOR IMPLEMENTATION` only on Codex's separate `APPROVED` of this exact
  artifact and of the contract transcription. Production code stays frozen at `63462513` until then.

## 0. Response to checkpoint review 1

| Finding | Resolution |
|---|---|
| CE04-CP-001: a `pg_catalog`-only search path leaves the implicit temporary schema first for relations and types | **Accepted.** Revision 1's false claim (that the alternative "makes `pg_temp` unreachable") is removed. §5.2 now requires an explicit `pg_catalog.` qualification for every catalog relation, type, function, operator and aggregate in every SQL text the store issues, including the initialization DDL's column types, and the store tables qualified by the resolved namespace. The namespace is resolved before any path change. The contract's genuine-object rule now names relations and types (`spec/persistence.md`). A further invariant is stated and evidenced, not assumed: the handle's session is private (open creates it from connection parameters, and never accepts a caller's connection), and the store creates no temporary objects, so the handle's temporary schema stays empty. New control CH12 runs the store's actual SQL texts in a session poisoned with a temporary `pg_class`, a temporary domain `text` and a temporary `mneme_record`, and requires the same results as in a clean session. It discriminates the unqualified forms (Codex's PIN_TEMP probe). Unrelated temporary objects never cause a refusal. |
| CE04-CP-002: CH09 is a FIX, and the empty branch initializes beside a prefixed non-table | **Accepted.** CH09 is split. CH09a (a view beside the tables) is FIX reject, executed by Codex. CH09b (a sequence) is a FIX-reject witness to be constructed in the implementation; Codex's attempt timed out and is not credited. CH09c (only a `mneme_` view, then the first open) is FIX reject, and nothing is created. The contract's initialization condition is now "the namespace holds no non-index relation whose name begins `mneme_`". Initialization has a **postcondition**: inside the same transaction and before commit, the created catalog satisfies the v1 catalog contract; otherwise it rolls back with `persistence.schema_incompatible`. Initialization also pins the session settings that shape its result (`SET LOCAL default_tablespace = ''`, `default_table_access_method = heap`). New row CH11 covers initialization under a non-default `default_tablespace`. The §2 accounting is corrected. |
| CE04-CP-003: G-092's after-open exclusion was broadened to a pre-open trigger exemption | **Accepted.** The trust scope now says explicitly that the exclusion applies **after open**. A pre-open catalog state that differs from the initializer's, a disabled internal trigger among them, is incompatible at open. The catalog contract makes the internal foreign-key trigger oracle explicit. For each of the two foreign keys there are exactly PostgreSQL's four internal RI triggers: insert and update checks on the referencing table, and `NO ACTION` delete and update on `mneme_store`. Each is internal, enabled (`tgenabled = 'O'`), linked to that constraint (`tgconstraint`), with the built-in `pg_catalog` RI function, row-level and `AFTER` with the initializer's event mask. Names and OIDs are not compared. R32 stays NOT CREDITABLE as a public kill. The property is enforced and killed by a **predicate test**: §5.3 makes the comparison a pure function over fetched catalog rows, and a synthesized catalog row set with `tgenabled = 'D'` must be refused. The same bounded predicate route covers every other non-constructible property (CH03, CH10, I15, I16). It is never claimed as a public execution. |
| Three CHECK conditions, not two | **Accepted.** §5.3 lists all three: `singleton`, the `tail` range and the `position` range. |
| X09 lock evidence | **Accepted.** §4.3 now requires a second session to observe, from `pg_locks` and at a gate inside open's transaction, the advisory lock with the key's `classid`/`objid`, `objsubid = 1` (the single-bigint form) and `granted = true` for the opening backend, then its release at transaction end. A waiter's `granted = false` row is not acquisition. |

## 1. Independent reproduction

Claude's own driver (`.tmp/work/claude/ce0401_reproduce.py`) uses fresh throwaway schemas in one
throwaway database in `mneme_ts`, on the same server (PostgreSQL 14.12) and the frozen code. The
probes were small and serial, under the Minion-Agent host reservation. Every headline witness
reproduces:

| Witness | Frozen result (open; protocol N; physical record/operation/tail) | Required |
|---|---|---|
| untouched v1 (control) | accept; oracle true; (2,1,2) | accept |
| R01 `mneme_record` UNLOGGED | accept; oracle true; (2,1,2) | `persistence.schema_incompatible` |
| R10 INSERT rule `DO INSTEAD NOTHING` | accept; receipt and tail 2, page `[]`; (0,1,2) | incompatible |
| R43 forced RLS hiding SELECT | accept; tail 2, page `[]`; (0,1,2) | incompatible |
| C01 nondeterministic `store_id` collation | accept; `a-b` → `persistence.store_exists` | incompatible |
| C24 generated `tail` with the same rendered default | accept; first commit engine 428C9 | incompatible |
| I19 non-unique expression index `record_id::integer` | accept; first commit engine 22P02 | incompatible |
| X11 `array_agg(integer)` overload, physical version 2 | accept; oracle true | incompatible |
| S10 `quote_all_identifiers=on`, untouched v1 | `persistence.schema_incompatible` | accept; oracle true |

## 2. Completeness challenge — additions

Claude executed six of these probes on the frozen code (`.tmp/work/claude/ce0401_challenge.py`).
The other rows are named so that the implementation witnesses cover them.

| Row | Property | Frozen result | Disposition and oracle |
|---|---|---|---|
| CH01 | `mneme_record` recreated `PARTITION BY LIST (store_id)` with every v1 column and constraint (the constructible case R29 did not reach) | `schema_incompatible` | KEEP reject. This is the isolating relkind witness that R35 lacks. |
| CH02 | a non-`mneme_` table with a foreign key `REFERENCES mneme_store ON UPDATE CASCADE` | accept; oracle true | FIX reject: an outside constraint references a v1 table. |
| CH03 | a non-heap table access method | not constructible: PostgreSQL 14 has only `heap` without a superuser-installed extension | NOT CREDITABLE as a kill. The contract still requires `relam` = heap. |
| CH04 | typed table (`ALTER TABLE mneme_record OF <composite type>`) | not executed | FIX reject (`reloftype`); witness added in implementation. |
| CH05 | `CREATE POLICY` on `mneme_record` without enabling RLS | accept; oracle true | FIX reject (G-089: policies). |
| CH06 | `BEFORE INSERT` trigger on `mneme_operation` that drops receipts | accept; retry → `history.duplicate_record_id`; (2,0,2) | FIX reject. Codex's triggers and rules were all on `mneme_record` (and R11 on `mneme_store`). Implementation witnesses cover one trigger and one rule on **each** of the four tables. |
| CH07 | user `=` operator for `(text, text)` that raises, with `search_path=<ns>,pg_catalog` | open accepts; then the **operations** call the shadow: engine P0001; (0,0,0) | FIX: accept, protocol N true, zero shadow calls (genuine built-ins in operations as well as open). |
| CH08 | `CREATE STATISTICS` object on `mneme_record` | accept; oracle true | KEEP accept (G-089: planner statistics are non-semantic). |
| CH09a | a view `mneme_extra` beside the four initialized tables | accept; oracle true (Codex, checkpoint review) | FIX reject. |
| CH09b | a sequence `mneme_extra` beside the four tables | not credited: Codex's setup timed out (57014) | FIX reject; the witness is constructed in the implementation. |
| CH09c | only a view `mneme_extra` in the namespace, then the first open | accept; creates all four tables and the header (Codex) | FIX reject, with no schema or store created. |
| CH10 | server major other than 14 | not constructible on this host (V02: `server_version` cannot be set by the client) | NOT CREDITABLE as an executed kill. The implementation tests the major-version predicate directly, and Rust repeats it. |
| CH11 | first open with connection option `default_tablespace` naming another tablespace | not executed: the only other tablespace, `pg_default`, lives on C: (OWN-001), and creating one needs superuser | NOT CREDITABLE. Initialization pins `default_tablespace = ''` (and `default_table_access_method = heap`) and checks its postcondition. The predicate test covers `reltablespace ≠ 0`. |
| CH12 | the store's actual SQL texts run in a session holding a temporary `pg_class` table, a temporary domain `pg_temp.text CHECK (false)` and a temporary `mneme_record` | unqualified forms bind the temporary objects (Codex PIN_TEMP: temporary OID for `pg_class`; 23514 for `::text`) | FIX: the implementation's texts give the same results as in a clean session. A direct engine control; open's private session keeps this state unreachable from the public API. |

## 3. Candidate path-C items

| Item | Resolution |
|---|---|
| C01 acceptance envelope | **Owner G-089**: only the finite catalog state the v1 initializer produces, apart from non-semantic identity (names, OIDs, ownership and grants, column order, dropped-column residue, planner statistics). Extra indexes and physical tuning are not tolerated; variations need a reviewed catalog-contract revision. |
| C02 namespace binding | **Path A (authority reading), offered for Codex's review.** The contract's DDL is unqualified and initialization creates it in the connection's current schema, so compatibility must be judged in that same namespace. Otherwise one open could initialize a schema that the next open judges elsewhere. If there is no current schema, initialization is impossible, and the contract's "never ignores a DDL error" makes the engine error propagate (X04, R34). Same-named objects in other schemas are irrelevant (X01, X03, X05) unless they become the current schema (X02: that schema holds one `mneme_` table, so it is incompatible). Binding to engine built-ins is the existing WP04-CR-007 rule ("no other key or overload may stand in"), applied to every catalog relation, type, function, operator and aggregate (X06…X11, CH07, CH12; CE04-CP-001). Accepted by Codex as path A (`1ffec311`). |
| C03 privileges | **Path A, now also explicit in G-089** (ownership and grants are non-semantic catalog identity). Open does not verify privileges. A genuine permission error propagates as the engine's error, with no effect: never a Mneme code, never a success. That follows "an open never ignores a DDL error" and the atomic-failure rule (PERS-005). R23 and R24 fail loudly and atomically, so no guarantee is violated. Row security is not a privilege; G-089 makes any RLS or policy incompatible. Accepted by Codex as path A (`1ffec311`). |
| C04 database environment | **Owner G-090**: under the lock, before accepting or creating: UTF8, and `LC_COLLATE`/`LC_CTYPE` each `C` or `POSIX`. Otherwise `persistence.schema_incompatible`, with no change. The handle sets `client_encoding` UTF8 itself. |
| C05 versions and comparison | **Owner G-091**: PostgreSQL major 14 only; any other major gives `persistence.schema_incompatible` before any change. Every property is compared as structured catalog data, never as rendered SQL. |
| C06 trust scope | **Owner G-092**: validation happens at open, on a trusted engine. Out-of-band DDL, row edits, disabled internal triggers or constraints, and catalog manipulation after open are outside certification. There is no per-operation revalidation and no row scan at open. |

All four decisions and both discharges are transcribed in `spec/persistence.md`: "Open and
initialize" steps 1–4, "v1 catalog contract", "Trust scope" and "Databases".

## 4. Row dispositions (all 136 rows, plus §2)

Legend:
- **KEEP:** the frozen code already meets the decided oracle. The row is a regression control that
  must stay as it is.
- **FIX:** the frozen code differs from the decided oracle, so the implementation must change it and
  a witness must kill the frozen behavior.
- **NOT CREDITABLE:** the fixture could not be constructed. No validator kill may be claimed; the
  required catalog property is still enforced by the contract.
- **Engine error:** the engine's error propagates with no effect and no Mneme code.

### 4.1 Accept, with the literal protocol oracle

| Disposition | Rows | Basis |
|---|---|---|
| KEEP accept (24) | B01, B02, B03; R21 (explicit `mneme_ts` equals the database default, `reltablespace` 0 — catalog identical); R22 (owner); R36 (unprefixed table outside the `mneme_` set); R38, R39 (lazy flags, no object); C16 (EXTENDED is bytea's default storage — catalog identical); C20 (dropped residue); C21 (statistics target); K09 (constraint name); S01…S05, S08, S09 (session defaults never govern operations; S01/S02/S04 record the actual operation settings); X01, X03, X05, X07 (current schema unchanged); V01 (14.12) | G-089 non-semantic identity; contract operation settings; C02 discharge |
| FIX → accept (5) | S07, S10 (presentation setting — G-091 structured comparison); S11 (SQL_ASCII client representation — G-090 the handle sets UTF8); C22 (column order — G-089 non-semantic); X06 (shadow `format_type` in the schema: open must not call it, and the schema is otherwise v1) | G-089, G-090, G-091, WP04-CR-007 |
| FIX → accept (+1, §2) | CH07 | genuine built-ins in operations |

### 4.2 Reject with `persistence.schema_incompatible`, no change

| Disposition | Rows | Catalog property (G-089 unless noted) |
|---|---|---|
| FIX reject (24) | R01, R02, R04, R31 | persistence |
| | R05, R06 | inheritance |
| | R07, R08, R09, R41, R42, R43 | RLS and policies, in every enable/force state |
| | R10, R11, R12 | rules, including no-op rules |
| | R13, R14, R15, R16, R17, R18, R33 | user triggers in every timing and enable state, including disabled and replica-only |
| | R19, R20 | relation options |
| FIX reject (16) | C01, C02, C03, C04, C23 | non-default collation (nondeterministic or deterministic ICU) |
| | C05, C06 | explicit `"C"`/`"POSIX"` collation differs from the initializer's default (catalog-exact; bytewise-equivalent is not a G-089 exemption) |
| | C07, C08, C09, C24 | identity or generated columns, whatever the rendering |
| | C13, C14, C15 | non-default storage |
| | C17, C18 | explicit compression |
| FIX reject (17) | I01…I07, I14 | any extra index: plain, partial, expression, hash, duplicate-unique or opclass forms, and failed builds that are invalid and not ready |
| | I08, I09, I10, I18, I19, I20 (and I02 above) | extra indexes that restrict writes, including invalid-but-ready ones |
| | I11, I12, I13 | index options, the clustering mark, replica identity |
| FIX reject (2) | X08 | the real column type is a domain (genuine observation, not the shadow renderer) |
| | X11 | the real `mneme_schema` version is 2 (genuine aggregate, not the overload) |
| FIX reject (3) | D02 (initialization must now refuse; nothing created), D03, D05 | G-090 database encoding |
| FIX reject (+7, §2) | CH02, CH04, CH05, CH06, CH09a, CH09b, CH09c | outside FK, typed table, policy without RLS, operation trigger, prefixed view or sequence beside the tables, prefixed view before the first open (refuse, create nothing) |
| KEEP reject (26) | R27, R28 (relation kind); R35 (relation kind; CH01 isolates it); R37 (extra `mneme_` table); R40 (RLS on `mneme_schema`); C10, C11, C12 (defaults); C19 (domain); C25, C26 (column names); C27 (type); C28 (nullability); K01…K08 (deferrable, NOT VALID, FK actions); K10, K11 (extra CHECK); H01, H02 (version row); X02 (the current schema holds one `mneme_` table) | catalog contract |
| KEEP reject (+1, §2) | CH01 | relation kind |

The 24 FIX-reject rows in the first group are R01, R02, R04, R05, R06, R07, R08, R09, R10, R11,
R12, R13, R14, R15, R16, R17, R18, R19, R20, R31, R33, R41, R42 and R43.

### 4.3 Engine errors and the genuine lock

| Disposition | Rows | Oracle |
|---|---|---|
| KEEP engine error (7) | R23, R24 (open accepts; the commit raises 42501, physical unchanged); R25 (open 42501); R34, X04 (3F000, no current schema); S06 (startup refusal); V02 (startup refusal) | C03 discharge; "never ignores a DDL error" |
| FIX (1) | X09 | Open's first statement acquires the **engine's** single-bigint advisory lock with the exact key, held until the transaction ends. The X10 marker shows zero shadow calls. A second session observes, at a gate inside open's transaction after the lock statement, a `pg_locks` row: `locktype = 'advisory'`, the key's `classid`/`objid`, `objsubid = 1` (single-bigint form), the opening backend's pid and `granted = true`. It then observes the row's absence after open's transaction ends. A waiter's `granted = false` row is not evidence of acquisition. Open accepts, and N is true. |
| observer (1) | X10 | It is attached to X09 and is not a separate open. |

### 4.4 Construction limits

**NOT CREDITABLE (10):**
- R03 (store-only UNLOGGED; R31 covers the case);
- R26 (owner transfer refused; ownership is non-semantic anyway);
- R29 (construction failed; CH01 is the constructible partitioned case);
- R30 (FDW refused);
- R32 (internal trigger disable refused with 42501; no superuser was used). The property itself is **in** the open-time contract: a pre-open disabled internal trigger is incompatible (CE04-CP-003). Only post-open changes are outside (G-092);
- I15, I16 (attachment refused; the observed rejection is a missing primary key, not opclass or
  collation);
- I17 (backing-index drop refused);
- D01, D04 (the Windows service refuses a POSIX database locale).

The contract still states every one of those properties, and the implementation enforces each of
them. Because §5.3 makes the comparison a pure function over fetched catalog rows, each is killed by
a **predicate test**: a synthesized row set equal to the initializer's state except for that one
property must be refused. This covers:
- an unlogged `mneme_store` (R03);
- a disabled internal RI trigger (R32);
- the backing-index operator class and collation (I15, I16);
- a missing backing index (I17);
- a foreign-table relkind (R30);
- a non-heap access method (CH03);
- server major 13 or 15 (CH10);
- `reltablespace ≠ 0` (CH11);
- a database locale of `POSIX` (D01, D04), which must be **accepted**.

Predicate tests are reported as predicate evidence, never as public executions. Ownership (R26) is
non-semantic, so it has no oracle to kill.

**Accounting.** The 136 rows break down as follows:

| Disposition | Rows |
|---|---|
| KEEP accept | 24 |
| FIX → accept | 5 |
| FIX → reject | 24 + 16 + 17 + 2 + 3 = 62 |
| KEEP reject | 26 |
| KEEP engine error | 7 |
| FIX lock (X09) | 1 |
| X10 observer | 1 |
| NOT CREDITABLE | 10 |
| **Total** | **136** |

§2 adds 14 rows (revision 2):

| Disposition | Rows |
|---|---|
| FIX accept | CH07 |
| FIX reject | CH02, CH04, CH05, CH06, CH09a, CH09b, CH09c |
| FIX, direct engine control | CH12 |
| KEEP accept | CH08 |
| KEEP reject | CH01 |
| NOT CREDITABLE (predicate-tested) | CH03, CH10, CH11 |

## 5. Implementation constraints (the single pass, after agreement)

**1. Order inside the open transaction**
- The explicit Read Committed `BEGIN` comes first.
- Its first statement is the genuine lock: `pg_catalog.pg_advisory_xact_lock(<key>::pg_catalog.int8)`, qualified with an explicit cast.
- Then the environment (G-090, G-091):
  - `server_version_num` major is 14;
  - `pg_database.encoding` is UTF8;
  - `datcollate` and `datctype` are each in {`C`, `POSIX`}.
- Then the namespace (`pg_catalog.current_schema()`; NULL lets the engine error surface when initialization runs). It is resolved before anything else depends on the search path.
- Then the branch:
  - if the namespace holds **no non-index relation** whose name begins `mneme_`, initialize;
  - otherwise compare against the catalog contract (CH09a–c).
- Initialization sets `SET LOCAL default_tablespace = ''` and `SET LOCAL default_table_access_method = heap`, creates the DDL and the header row, then verifies its **postcondition** with the same comparison, before commit. A failed postcondition rolls back with `persistence.schema_incompatible` (CH11).
- Then the version row.

Each check that fails rolls back and raises `persistence.schema_incompatible`. Any other error propagates.

**2. Genuine objects**
- Every SQL text the store issues, in open (including the initialization DDL) and in all four operations:
  - names every catalog relation (`pg_catalog.pg_class`, …) and every type (`pg_catalog.text`, `pg_catalog.int8`, `pg_catalog.bytea`, …, in casts and in the DDL's column types) through `pg_catalog`;
  - names every function, operator and aggregate through `pg_catalog`, for example `OPERATOR(pg_catalog.=)`;
  - addresses the four tables qualified by the namespace that open resolved (an identifier, never a search-path lookup).
- A search-path setting is **not** a substitute: PostgreSQL searches the implicit temporary schema first for relations and types, even when `pg_catalog` is the only explicit entry (CE04-CP-001).
- **Private-session invariant.** Open creates the handle's connection from connection parameters and never accepts a caller's connection, and the store creates no temporary objects. So the handle's temporary schema is empty for its lifetime. Rust's API gives the same guarantee, and both implementation records state it with evidence.
- The CH07, CH12 and X06…X11 witnesses must pass. A temporary object unrelated to the store never causes a refusal.

**3. Structured comparison**
- The comparison reads catalog columns (`pg_class`, `pg_attribute`, `pg_attrdef`, `pg_constraint`, `pg_index`, `pg_inherits`, `pg_trigger`, `pg_rewrite`, `pg_policy`, `pg_am`, `pg_opclass`, `pg_collation`, `pg_type`, `pg_proc`), never `pg_get_constraintdef`, `pg_get_expr`, `pg_get_indexdef` or `format_type` text.
- It is split into **fetch** (queries) and **compare** (a pure function over the fetched rows). That split makes the predicate tests of §4.4 possible.
- Expressions are compared as their stored node trees, with column references mapped to column names and source-location fields removed. There are **three** CHECK conditions (`singleton`; the `tail` range; the `position` range) and **two** defaults (`singleton` `true`; `tail` `0`).
- Transient or lazy catalog flags (`relhasrules`, `relhassubclass`, `relhastriggers`, `relhasindex` and the like) are never compared; existence is read from the catalog that holds the objects.
- **Internal foreign-key triggers** (CE04-CP-003): for each of the two foreign keys, exactly PostgreSQL's four internal RI triggers. Two are on the referencing table: `RI_FKey_check_ins` and `RI_FKey_check_upd`. Two are on `mneme_store`: `RI_FKey_noaction_del` and `RI_FKey_noaction_upd`. Each has `tgisinternal`, `tgenabled = 'O'`, `tgconstraint` linked to that foreign key, the built-in function in `pg_catalog`, and the initializer's `tgtype`. Trigger names and OIDs are not compared. No other trigger may exist.
- The expected values are pinned literals that both languages share. The implementation records where they live, and Rust consumes the same pins.

**4. Client encoding**
- The handle sets `client_encoding` UTF8 at connect or in the open transaction, and keeps it.

**5. Initialization**
- Initialization runs only after the environment check passes, and only when no `mneme_` non-index relation exists.
- Its postcondition is the catalog contract, checked before commit.
- A refusal creates nothing (D02, CH09c, CH11).

**6. Unchanged**
- Validation precedence, the operation transactions, the per-handle lock, the store-row lock, `synchronous_commit = on`, and the read snapshot are all unchanged.
- CR-009…011 stay closed.

## 6. Evidence obligations for the implementation record

**Witnesses**
- Every FIX row and every §2 row that is not NOT CREDITABLE becomes a public-open witness on a fresh schema, with the decided oracle.
- Every KEEP row is preserved as a control or is already covered:
  - B03 and S10 run on an untouched schema;
  - D-rows run on throwaway databases created from template0 in `mneme_ts`.
- Triggers and rules get one witness on each of the four tables.
- The predicate tests of §4.4 cover the non-constructible properties (R03, R30, R32, I15–I17, CH03, CH10, CH11, D01/D04 acceptance).
- CH12 runs the store's actual SQL texts in a temporary-object-poisoned session.
- The X09 lock witness uses `pg_locks` with `granted = true` at a gate, then observes the release.
- Refusals assert no schema or store mutation: D02, CH09c, and every environment refusal.

**Planted violations P24 onward**

| Mutant | What it skips or does |
|---|---|
| P24 | persistence |
| P25 | collation |
| P26 | user triggers |
| P27 | rules |
| P28 | RLS and policies |
| P29 | extra indexes |
| P30 | index validity and readiness |
| P31 | inheritance |
| P32 | identity and generated columns |
| P33 | storage and compression |
| P34 | relation options |
| P35 | database encoding |
| P36 | database locale |
| P37 | client encoding |
| P38 | unqualified lock call |
| P39 | unqualified aggregate or operator |
| P40 | rendered-text comparison reintroduced |
| P41 | outside-FK check |
| P42 | major-version check (killed by the predicate test only) |
| P43 | internal RI trigger checks (killed by the predicate test) |
| P44 | initialization postcondition and setting pins |
| P45 | an unqualified type or catalog relation (killed by CH12) |
| P46 | initialization beside a prefixed non-table (killed by CH09c) |

Each must be killed; any equivalent mutant is argued, as P14 was.

**Gates**
- full suite, `ruff`, `ruff format --check`, `mypy --strict`;
- fresh G3 coverage over all of `minion_memory`, with branches and subprocesses and no exclusions, reported in the record (lesson from CR-011).

**Host reservation**
- The full suite and the mutant batch run only after Minion-Agent sends "host clear".

**Cross-language**
- The Rust candidate must reproduce the same catalog contract against the same pinned literals.
- Its [IT] witnesses include a schema initialized by one language and opened by the other (feasibility matrix).

## 7. Asked of Codex

Re-review this exact revision 2 and the revised transcription in `spec/persistence.md`:
- the repairs of CE04-CP-001…003 (§0);
- the CHECK inventory and the X09 lock evidence;
- the revised §2 rows and accounting (CH09a–c, CH11, CH12);
- the predicate-test route for non-constructible properties (§4.4, §5.3).

`APPROVED` makes the checkpoint `AGREED FOR IMPLEMENTATION`. `CHANGES_REQUIRED` returns it to Claude.
