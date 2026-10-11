# CE-04-01 — completeness challenge, row classification, checkpoint proposal (Claude), revision 1

**Input:** Codex's characterization `assurance/convergence/CE-04-01-characterization.md` at
`0f7ac1bf` (136 executed rows against frozen code `63462513`).
**Governs:**
- G-088 (narrow convergence on WP04-CR-008);
- G-089…G-092 (the Owner's decisions on candidate path-C items C01, C04, C05 and C06);
- the agreed contract (docs `d857fcc2`), now transcribed with those decisions in
  `spec/persistence.md`, "Reference backend".

**Checkpoint status: `PROPOSED FOR IMPLEMENTATION`, revision 1.** It becomes `AGREED FOR
IMPLEMENTATION` only on Codex's separate `APPROVED` of this exact artifact and of the contract
transcription. Production code stays frozen at `63462513` until then.

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
| CH09 | a view or sequence named `mneme_…` beside the four tables | not executed | FIX/KEEP reject (implementation witness: a `mneme_` view). |
| CH10 | server major other than 14 | not constructible on this host (V02: `server_version` cannot be set by the client) | NOT CREDITABLE as an executed kill. The implementation tests the major-version predicate directly, and Rust repeats it. |

## 3. Candidate path-C items

| Item | Resolution |
|---|---|
| C01 acceptance envelope | **Owner G-089**: only the finite catalog state the v1 initializer produces, apart from non-semantic identity (names, OIDs, ownership and grants, column order, dropped-column residue, planner statistics). Extra indexes and physical tuning are not tolerated; variations need a reviewed catalog-contract revision. |
| C02 namespace binding | **Path A (authority reading), offered for Codex's review.** The contract's DDL is unqualified and initialization creates it in the connection's current schema, so compatibility must be judged in that same namespace. Otherwise one open could initialize a schema that the next open judges elsewhere. If there is no current schema, initialization is impossible, and the contract's "never ignores a DDL error" makes the engine error propagate (X04, R34). Same-named objects in other schemas are irrelevant (X01, X03, X05) unless they become the current schema (X02: that schema holds one `mneme_` table, so it is incompatible). Binding to engine built-ins is the existing WP04-CR-007 rule ("no other key or overload may stand in"), applied to every function, operator and aggregate (X06…X11, CH07). |
| C03 privileges | **Path A, now also explicit in G-089** (ownership and grants are non-semantic catalog identity). Open does not verify privileges. A genuine permission error propagates as the engine's error, with no effect: never a Mneme code, never a success. That follows "an open never ignores a DDL error" and the atomic-failure rule (PERS-005). R23 and R24 fail loudly and atomically, so no guarantee is violated. Row security is not a privilege; G-089 makes any RLS or policy incompatible. |
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
| FIX reject (+4, §2) | CH02, CH04, CH05, CH06 | outside FK, typed table, policy without RLS, operation trigger |
| KEEP reject (26) | R27, R28 (relation kind); R35 (relation kind; CH01 isolates it); R37 (extra `mneme_` table); R40 (RLS on `mneme_schema`); C10, C11, C12 (defaults); C19 (domain); C25, C26 (column names); C27 (type); C28 (nullability); K01…K08 (deferrable, NOT VALID, FK actions); K10, K11 (extra CHECK); H01, H02 (version row); X02 (the current schema holds one `mneme_` table) | catalog contract |
| KEEP reject (+2, §2) | CH01, CH09 | relation kind; prefixed non-table |

The 24 FIX-reject rows in the first group are R01, R02, R04, R05, R06, R07, R08, R09, R10, R11,
R12, R13, R14, R15, R16, R17, R18, R19, R20, R31, R33, R41, R42 and R43.

### 4.3 Engine errors and the genuine lock

| Disposition | Rows | Oracle |
|---|---|---|
| KEEP engine error (7) | R23, R24 (open accepts; the commit raises 42501, physical unchanged); R25 (open 42501); R34, X04 (3F000, no current schema); S06 (startup refusal); V02 (startup refusal) | C03 discharge; "never ignores a DDL error" |
| FIX (1) | X09 | Open's first statement acquires the **engine's** single-bigint advisory lock. The X10 marker must show that the shadow was never called and that the lock is genuinely held: the witness observes `pg_locks` from a second session while open waits. Open then accepts, and N is true. |
| observer (1) | X10 | It is attached to X09 and is not a separate open. |

### 4.4 Construction limits

**NOT CREDITABLE (10):**
- R03 (store-only UNLOGGED; R31 covers the case);
- R26 (owner transfer refused; ownership is non-semantic anyway);
- R29 (construction failed; CH01 is the constructible partitioned case);
- R30 (FDW refused);
- R32 (internal trigger disable refused; G-092 puts it outside);
- I15, I16 (attachment refused; the observed rejection is a missing primary key, not opclass or
  collation);
- I17 (backing-index drop refused);
- D01, D04 (the Windows service refuses a POSIX database locale).

The contract still states every one of those properties. The implementation enforces each property
it can observe: persistence, ownership-insensitivity, relkind, opclass and collation of the backing
indexes, and database locale. No kill may be claimed for them.

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

§2 adds 10 rows:

| Disposition | Rows |
|---|---|
| FIX accept | CH07 |
| FIX reject | CH02, CH04, CH05, CH06 |
| KEEP accept | CH08 |
| KEEP reject | CH01, CH09 |
| NOT CREDITABLE | CH03, CH10 |

## 5. Implementation constraints (the single pass, after agreement)

**1. Order inside the open transaction**
- The explicit Read Committed `BEGIN` comes first.
- Its first statement is the genuine lock: `pg_catalog.pg_advisory_xact_lock(<key>::pg_catalog.int8)`, qualified with an explicit cast.
- Then the environment (G-090, G-091):
  - `server_version_num` major is 14;
  - `pg_database.encoding` is UTF8;
  - `datcollate` and `datctype` are each in {`C`, `POSIX`}.
- Then the namespace (`pg_catalog.current_schema()`; NULL lets the engine error surface when initialization runs).
- Then initialize, or compare against the catalog contract.
- Then the version row.

Each check that fails rolls back and raises `persistence.schema_incompatible`. Any other error propagates.

**2. Genuine objects**
- Every SQL text the store issues, in open and in all four operations:
  - names its functions, operators and aggregates through `pg_catalog`, for example `OPERATOR(pg_catalog.=)`;
  - addresses its tables qualified by the namespace that open resolved (an identifier, never a search-path lookup).
- Alternatively, the handle may pin its session `search_path` to `pg_catalog` alone and qualify the tables. This also makes `pg_temp` unreachable.
- Either way, the CH07 and X06…X11 witnesses must pass.

**3. Structured comparison**
- The comparison reads catalog columns (`pg_class`, `pg_attribute`, `pg_attrdef`, `pg_constraint`, `pg_index`, `pg_inherits`, `pg_trigger`, `pg_rewrite`, `pg_policy`, `pg_am`, `pg_opclass`, `pg_collation`, `pg_type`), never `pg_get_constraintdef`, `pg_get_expr`, `pg_get_indexdef` or `format_type` text.
- Expressions (the two CHECK conditions, the two defaults) are compared as their stored node trees. Column references are mapped to column names, and source-location fields are removed.
- The expected values are pinned literals that both languages share. The implementation records where they live, and Rust consumes the same pins.

**4. Client encoding**
- The handle sets `client_encoding` UTF8 at connect or in the open transaction, and keeps it.

**5. Initialization**
- Initialization runs only after the environment check passes.
- A refusal creates nothing (D02).

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
- The version predicate gets a direct test (CH10).

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

Review this exact artifact and the contract transcription in `spec/persistence.md`. Specifically:
- the C02 and C03 discharges as path A;
- the §2 additions;
- every disposition, including:
  - the two catalog-identical accepts (R21, C16);
  - the catalog-exact rejection of explicit `"C"`/`"POSIX"` collation (C05, C06);
  - the CH07 operations finding.

`APPROVED` makes the checkpoint `AGREED FOR IMPLEMENTATION`. `CHANGES_REQUIRED` returns it to Claude.
