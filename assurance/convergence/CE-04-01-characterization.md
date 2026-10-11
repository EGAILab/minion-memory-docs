# CE-04-01 — executed characterization of the v1 catalog trust boundary

**Status: offered for Claude's completeness challenge and row classification. This is not a checkpoint agreement or an implementation approval.**

## Authority and scope

G-088 opens narrow convergence on **WP04-CR-008**. The behavior reference is frozen code `634625135851cccc188fe726acb86990911ebddb`. This artifact branches from docs state `b33f650aa5d8f5cd3e5bdd00b74da6997d8a26a1`; the agreed contract is docs `d857fcc2`, especially `spec/persistence.md` reference backend and open/initialize, G-079/G-081, and the explicit shared lock/Read Committed rule. G-077..087 supply the v1 guarantees. CR-009..011 remain resolved and outside this episode. No production module, state or registry was changed.

The boundary includes the observations used to *decide* that a schema is v1, not merely the objects those observations describe. Equal column and constraint renderings do not establish persistence, base-slot write semantics, bytewise equality, index effects, row visibility, or the authenticity of the lock and version observation. Executed counterexamples cover each of those distinctions below.

There are **136 executed matrix rows**, including positive controls and construction-limit controls. X10 is the independent lock-count observation attached to X09, not another open. A row whose setup failed records the real residual state and its real open result; it does not claim an open against an unconstructed state. This is a characterization of the named property classes and their interactions, not a claim that a finite set proves every PostgreSQL extension or every possible SQL function harmless.

## Execution and literal public oracle

Executed on Windows, PostgreSQL **14.12**, non-superuser `mneme_dev`, psycopg 3.2.13, project-managed CPython 3.12.8 and the frozen candidate's locked dependencies. Each shell first sourced the project environment; code was imported from the separate frozen checkout. Credentials were loaded from `.tmp/work/pg.env` and are not included here. All scratch scripts, output, venvs and databases' tablespace files stayed inside the E: project. No full test, mutant or Docker batch was started during the Minion-Agent host reservation. These are small, serial throwaway-schema/catalog probes; I18 is one explicitly gated, three-record index-state probe, not a stress workload.

The main probe database was created using `TEMPLATE template0 ENCODING 'UTF8' LC_COLLATE 'C' LC_CTYPE 'C' TABLESPACE mneme_ts`, with private schema `ce04`, initialized by the **public** `PostgresHistoryStore.open`. Connections ordinarily used `search_path=ce04`, `statement_timeout=5000`, `lock_timeout=2000`. The row's options override that context where stated. Forward statements were individually committed, so setup failures can leave a residual state; that state was observed before reversal. After each ordinary cell, reverse DDL restored the live column and constraint fingerprints and fixture data was deleted. A few benign physical residues (dropped attributes, ACL representations and lazy flags) remain in a reused schema. B03/S10 instead use an untouched, freshly initialized schema, eliminating that confound for the false-refusal witness.

For an accepted open the default **N** public protocol is:

```python
T = "2026-10-11T08:00:00.000000Z"
writer = {"profile": "learning", "recognized": [
    {"record_type": "attempt", "schema_version": 1}]}
operation = {"source_namespace": "app", "source_operation_id": "one"}
def draft(record_id):
    return {"record_id": record_id, "profile": "learning",
            "record_type": "attempt", "schema_version": 1,
            "compatibility": "required"}
with PostgresHistoryStore.open(params, lambda store_id: T) as store:
    store.create_store("s")
    receipt = store.commit_history("s", writer, operation,
                                   [draft("r1"), draft("r2")])
    retry = store.commit_history("s", writer, operation,
                                 [draft("r1"), draft("r2")])
    page = store.read_history("s", {"store_id":"s", "position":0}, 10)
    tail = store.store_tail("s")
```

Literal oracle: receipt first/last positions **1/2**, identical retry receipt, read positions **[1,2]**, page through/tail and store_tail **2**, both original records preserved and stamped T. Physical observation where available is `(ONLY record count, operation count, max ONLY store tail) = (2,1,2)`. A valid atomic rejection leaves `(0,0,0)` after the independently committed create. A successful receipt with missing records is not atomic success.

Protocol variants, identified in each recipe:

- **collide:** create `ab`, then `a-b`; both are distinct valid store IDs.
- **record_collision:** use record IDs `ab`, `a-b`; both must commit in that store.
- **namespace:** first namespace `appa`; second `app-a` with `r3` must commit at 3, not conflict; read [1,2,3].
- **across_store:** after N's first commit, create `t`, commit `r1` there; per-store uniqueness permits it.
- **large:** first payload `{"s": "x" * 20000}`; B02 proves admission by the ordinary v1 backend.
- **unicode:** first payload `{"s":"é😀\u0000"}`, operation id `"β\u0000😀"`; literal values must roundtrip, not merely positions.

Observers never modify library code. Later session cells sample actual transaction settings through the injected clock's read-only SQL, not the connection's default settings. Catalog snapshots record real relation kind/persistence/RLS/options/owner/tablespace; attribute identity/generated/collation/storage/compression; constraints; index validity/readiness/liveness/opclass/collation/predicate/expression; inheritance, triggers and rules. Qualified `pg_catalog.format_type` separately identifies X08's real domain. The two frozen rendering fingerprints are recorded as *observations of the implementation's queries*, not trusted proofs when the query can be shadowed. `catalog.context` describes the separate catalog-observer connection (usually the base connection), not necessarily the public handle's modified options. In particular S10's baseline fingerprints match before its quote-enabled public open refuses; `clock_contexts`, when present, describe the actual commit transaction.

## Proposed obligations and undecided policy

These are acceptance oracles for the checkpoint, **not code or an implementation design**:

1. **O1 — genuine boundary observations:** the first open statement must acquire the actual engine single-bigint shared advisory transaction lock; all inspections occur after it in explicit Read Committed. Actual engine metadata and the actual singleton/version row must decide compatibility. Same-named helper functions and overload resolution must not substitute observations. X08, X09/X10 and X11 discriminate this, including an overload that wins even when `pg_catalog` is implicitly first.
2. **O2 — durable, ordinary canonical relations:** accepted storage must deliver the promised persistence, bytewise identities, constraints and append/read semantics. UNLOGGED storage, inherited extra records, rewrite rules, effectful triggers or RLS, and write-restricting indexes cannot be accepted as valid v1 merely because the two fingerprints agree. No shared-service crash was performed: UNLOGGED admission is executed, its crash behavior is an engine fact.
3. **O3 — full admitted value domain:** genuine underlying types, identity/generated semantics, collations and storage must not add a rejection or normalization for a contract-valid value. Test `ab` versus `a-b`, explicit schema_version, tail updates, 20KB payloads and nonnumeric record IDs. A default rendered as `0` is not proof a tail column is writable (C24).
4. **O4 — effective constraint/index behavior:** distinguish a valid constraint-backed index from extras, and invalid/not-ready from invalid/ready indexes. “Nonunique” does not imply harmless: expression and predicate evaluation can reject valid writes (I19/I20). A failed index build can remain write-active (I18).
5. **O5 — no presentation-based refusal:** B03's genuinely valid initialized schema cannot become incompatible under identifier quoting alone (S10). Renderer formatting, mutable object names, OIDs and lazy flags are not themselves semantic equivalence proofs or semantic differences. Exact alternate-shape acceptance remains C01 below.
6. **O6 — effective transaction/context requirements:** default Repeatable Read/Serializable/read-only and synchronous_commit settings are not the actual operation settings. The observed operation context must satisfy the explicit contract. No new read-snapshot/concurrency closure is claimed here; that earlier rule is unchanged.
7. **O7 — failure integrity:** incompatible opens make no changes. Availability, permission and DDL errors are not silently treated as a compatible schema or successful initialization. The precise configuration-error seam where the existing text does not decide it is C02..C05 below.

### Candidate path-C questions (not decisions)

Each is **REQUIREMENT_UNCERTAIN / owner_decision_required: true** if Claude cannot discharge it by a specific existing normative rule. These are inside the catalog-boundary episode, not reopened lower-layer semantics.

| ID | Unresolved policy / required clarification | Executed anchors |
| --- | --- | --- |
| C01 | What is the exact acceptance envelope of “exactly four tables … anything else”? Must every harmless physical/auxiliary deviation be rejected, or is some structural/semantic equivalence admitted? Decide explicitly for harmless extra indexes/tables, constraint names, extra CHECK(true), unused defaults/identity, no-op or disabled triggers/rules, inheritance with no additional visible rows, physical attribute order/residue, storage/compression, fillfactor/autovacuum, cluster/replica identity and equivalent FK actions. No arbitrary SQL function can be inferred harmless from one successful call. | R06/R07/R09/R12/R16..22/R33/R36..39, C04..06/C08..12/C14..23, K05..10, I01/I03..07/I11..14 |
| C02 | How is the canonical namespace selected/bound, and which session search paths or auxiliary objects are allowed? O1 is already required, but the API/configuration boundary and refusal code for an absent/nonselectable namespace or unsafe context are not explicit. | X01..11, R34 |
| C03 | Does open require the opening role to have all effective privileges for later operations, or may a handle open and later surface genuine permission errors? Which failure is schema_incompatible versus availability/caller configuration? Owners can revoke their own ordinary rights; role OID/owner equality alone is insufficient. No superuser privilege is requested. | R23..26/R30/R32, S06 |
| C04 | The Databases rule already requires UTF8/C/C. Must open enforce those deployment preconditions? What outcome does a wrong server encoding/locale or non-UTF8 client representation receive? D03/D05 do not authorize relaxing that rule: they demonstrate that bytea payloads can survive a nonconforming database. | D01..05, S11, C05/C06/C23 |
| C05 | Which PostgreSQL versions/renderer variations are supported, and how are unsupported versions classified? Only actual 14.12 was executed. Pinning deparsed strings without a support policy cannot establish compatibility on other releases. Same-release quote_all_identifiers false refusal is already an O5 defect, not an Owner option. | V01/V02, S07/S10 |
| C06 | State the trusted-engine/catalog and post-open DDL assumptions. May validator correctness rely on engine-enforced attachment/permission invariants for otherwise unconstructible states? Does certification cover a schema modified by an administrator after open? This characterization assumes genuine PostgreSQL catalogs and stable schema during an operation; it does not authorize such mutations or claim to defend against system-catalog corruption. | I08..10/I15..17, R26/R29/R30/R32/R35; construction limits below |

## Matrix reading

**CAN** distinguishes an executed counterexample, a known engine-dependent guarantee risk with admission executed, a conditional risk, and a harmless particular fixture. “No effect observed” is deliberately weaker than proof that arbitrary objects of that class are harmless. Construction failures cannot be counted as validator kills. The row's wrong-implementation discriminator names the public protocol or metadata assertion that would separate a real v1 guarantee from a fingerprint-only implementation. Positive controls guard against unreasonable refusal.

The recipe appendix is part of the matrix: every row contains executed setup, actual observation, public mode, undo and catalog evidence. SQL uses the private `ce04` schema unless qualified. Special schedules and complete helper definitions are below the matrix. Recipe outcomes are generated from executed JSON records; risk/policy annotations are the reviewer's assessment, not guessed current behavior.

## Executed matrix

| Row | Property | Current behavior | CAN violate / assessment | Required or undecided oracle | Wrong implementation / discriminator |
| --- | --- | --- | --- | --- | --- |
| B01 | Unmodified v1 | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. No demonstrated semantic change | Accept normative positive control; preserve N/variant literal oracle. | Overstrict renderer/metadata comparison; positive public oracle must survive. |
| B02 | Unmodified v1, large valid payload | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. No demonstrated semantic change | Accept normative positive control; preserve N/variant literal oracle. | Overstrict renderer/metadata comparison; positive public oracle must survive. |
| B03 | untouched fresh v1 positive control | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. All normative live and physical schema properties created by frozen DDL | Accept normative positive control; preserve N/variant literal oracle. | Overstrict renderer/metadata comparison; positive public oracle must survive. |
| R01 | mneme_record UNLOGGED | open ACCEPT; N/variant oracle True | YES: Durability: canonical records, receipts, tail or version can be lost | O2/O3: incompatible with demonstrated guarantee; must not accept as v1. | Two rendering fingerprints alone accept this state; recipe plus public variant or explicit engine property distinguishes it. |
| R02 | mneme_operation UNLOGGED | open ACCEPT; N/variant oracle True | YES: Durability: canonical records, receipts, tail or version can be lost | O2/O3: incompatible with demonstrated guarantee; must not accept as v1. | Two rendering fingerprints alone accept this state; recipe plus public variant or explicit engine property distinguishes it. |
| R03 | mneme_store UNLOGGED | setup InvalidTableDefinition/42P16; open ACCEPT; N/variant oracle True | CONDITIONAL / construction-limited: Durability: canonical records, receipts, tail or version can be lost Construction blocked: store-only UNLOGGED did not exist; R31 proves the jointly UNLOGGED case. | Normative structure required; O2/O3/O4; do not credit rejection of an unconstructed property (C06). | Treating failed fixture construction as a killed validator mutant; discriminate residual catalog from intended state. |
| R04 | mneme_schema UNLOGGED | open ACCEPT; N/variant oracle True | YES: Durability: canonical records, receipts, tail or version can be lost | O2/O3: incompatible with demonstrated guarantee; must not accept as v1. | Two rendering fingerprints alone accept this state; recipe plus public variant or explicit engine property distinguishes it. |
| R05 | record inheritance child with out-of-tail entry | open ACCEPT; N/variant oracle False | YES: Ordering and identity: inherited rows bypass parent unique/FK constraints | O2/O3: incompatible with demonstrated guarantee; must not accept as v1. | Two rendering fingerprints alone accept this state; recipe plus public variant or explicit engine property distinguishes it. |
| R06 | record inherits a parent | open ACCEPT; N/variant oracle True | CONDITIONAL / construction-limited: No demonstrated semantic change | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| R07 | record RLS owner bypass deny | open ACCEPT; N/variant oracle True | CONDITIONAL / construction-limited: RLS can hide records or block valid commits; ownership controls applicability | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| R08 | record RLS force deny | open ACCEPT; commit InsufficientPrivilege/42501 | YES: RLS can hide records or block valid commits; ownership controls applicability | O2/O3: incompatible with demonstrated guarantee; must not accept as v1. | Two rendering fingerprints alone accept this state; recipe plus public variant or explicit engine property distinguishes it. |
| R09 | record RLS force allow | open ACCEPT; N/variant oracle True | CONDITIONAL / construction-limited: RLS can hide records or block valid commits; ownership controls applicability | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| R10 | record INSERT rule discards records | open ACCEPT; N/variant oracle False | YES: Durability/order/retry: receipt and tail without records | O2/O3: incompatible with demonstrated guarantee; must not accept as v1. | Two rendering fingerprints alone accept this state; recipe plus public variant or explicit engine property distinguishes it. |
| R11 | store UPDATE rule suppresses tail | open ACCEPT; create FeatureNotSupported/0A000 | YES: Gapless order, tail/read coherence | O2/O3: incompatible with demonstrated guarantee; must not accept as v1. | Two rendering fingerprints alone accept this state; recipe plus public variant or explicit engine property distinguishes it. |
| R12 | record no-op rule | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. No demonstrated semantic change | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| R13 | record BEFORE ROW trigger | open ACCEPT; N/variant oracle False | YES: Receipt without records | O2/O3: incompatible with demonstrated guarantee; must not accept as v1. | Two rendering fingerprints alone accept this state; recipe plus public variant or explicit engine property distinguishes it. |
| R14 | record AFTER ROW trigger | open ACCEPT; N/variant oracle False | YES: Receipt without records | O2/O3: incompatible with demonstrated guarantee; must not accept as v1. | Two rendering fingerprints alone accept this state; recipe plus public variant or explicit engine property distinguishes it. |
| R15 | record AFTER STATEMENT trigger | open ACCEPT; N/variant oracle False | YES: Atomic commit loses rows | O2/O3: incompatible with demonstrated guarantee; must not accept as v1. | Two rendering fingerprints alone accept this state; recipe plus public variant or explicit engine property distinguishes it. |
| R16 | record BEFORE STATEMENT trigger | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. No demonstrated semantic change | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| R17 | record BEFORE ROW trigger | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. No demonstrated semantic change | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| R18 | disabled harmful user trigger | open ACCEPT; N/variant oracle True | CONDITIONAL / construction-limited: No demonstrated semantic change | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| R19 | record fillfactor 50 | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. No demonstrated semantic change | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| R20 | record autovacuum disabled | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. Maintenance availability, not demonstrated canonical semantic difference | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| R21 | record explicit mneme_ts tablespace | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. Same project-local physical location | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| R22 | record owner remains opening role | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. No demonstrated semantic change | Accept normative positive control; preserve N/variant literal oracle. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| R23 | record INSERT grant removed | open ACCEPT; commit InsufficientPrivilege/42501 | CONDITIONAL / construction-limited: Valid commit fails for lack of write access | O7: do not suppress genuine permission/DDL failure; open privilege policy UNDECIDED C03/C06. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| R24 | record SELECT grant removed | open ACCEPT; commit InsufficientPrivilege/42501 | CONDITIONAL / construction-limited: Retry/read or duplicate-ID checks fail | O7: do not suppress genuine permission/DDL failure; open privilege policy UNDECIDED C03/C06. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| R25 | schema version SELECT grant removed | open InsufficientPrivilege/42501; later NOT RUN | CONDITIONAL / construction-limited: Open cannot read version; availability versus incompatible taxonomy | O7: do not suppress genuine permission/DDL failure; open privilege policy UNDECIDED C03/C06. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| R26 | record owner changed to postgres | setup InsufficientPrivilege/42501; open ACCEPT; N/variant oracle True | CONDITIONAL / construction-limited: Capability limit: opening role has no membership in target role Ownership transfer not constructed (42501); ordinary role unchanged. Owner identity alone is not an effective-rights oracle. | O7: do not suppress genuine permission/DDL failure; open privilege policy UNDECIDED C03/C06. | Treating failed fixture construction as a killed validator mutant; discriminate residual catalog from intended state. |
| R27 | record replaced by view | open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | CONDITIONAL / construction-limited: Reference DDL requires an ordinary durable table; view may redirect writes | Normative structure required; O2/O3/O4; do not credit rejection of an unconstructed property (C06). | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| R28 | record replaced by materialized view | open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | CONDITIONAL / construction-limited: Cannot append canonical records to materialized view | Normative structure required; O2/O3/O4; do not credit rejection of an unconstructed property (C06). | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| R29 | record replaced by partitioned table | setup FeatureNotSupported/0A000; open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | CONDITIONAL / construction-limited: Partitioning changes storage/constraint and routing boundary Partitioned LIKE INCLUDING ALL construction failed; open saw a missing record table, not the proposed complete partitioned schema. | Normative structure required; O2/O3/O4; do not credit rejection of an unconstructed property (C06). | Treating failed fixture construction as a killed validator mutant; discriminate residual catalog from intended state. |
| R30 | foreign-wrapper construction under opening role | setup InsufficientPrivilege/42501; open ACCEPT; N/variant oracle True | CONDITIONAL / construction-limited: Foreign durability/atomicity not guaranteed by reference DDL; role may prohibit construction Foreign wrapper construction denied (42501); no actual foreign replacement was opened. | O7: do not suppress genuine permission/DDL failure; open privilege policy UNDECIDED C03/C06. | Treating failed fixture construction as a killed validator mutant; discriminate residual catalog from intended state. |
| R31 | record and operation and store UNLOGGED together | open ACCEPT; N/variant oracle True | YES: All canonical store state can be lost after crash | O2/O3: incompatible with demonstrated guarantee; must not accept as v1. | Two rendering fingerprints alone accept this state; recipe plus public variant or explicit engine property distinguishes it. |
| R32 | record internal FK triggers disabled | setup InsufficientPrivilege/42501; open ACCEPT; N/variant oracle True | CONDITIONAL / construction-limited: Foreign-key enforcement absent if privileged disable succeeds Internal trigger disable denied (42501); no disabled RI trigger state was opened. | O7: do not suppress genuine permission/DDL failure; open privilege policy UNDECIDED C03/C06. | Treating failed fixture construction as a killed validator mutant; discriminate residual catalog from intended state. |
| R33 | replica-only harmful user trigger | open ACCEPT; N/variant oracle True | CONDITIONAL / construction-limited: Dormant under origin; effectful under replica | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| R34 | peer-session temporary v1 tables | open InvalidSchemaName/3F000; later NOT RUN | CONDITIONAL / construction-limited: Temporary data is session-local and non-durable Only peer-session TEMP state executed; a public new connection cannot select that temporary namespace (3F000). | O1/O7; namespace/configuration acceptance UNDECIDED C02. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| R35 | actual partitioned record with columns and checks only | open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | CONDITIONAL / construction-limited: Ordinary table kind required; native partitioning cannot represent v1 store-wide unique Actual partitioned relation constructed with columns/checks, lacking normative uniqueness; rejection does not isolate a relkind guard. | Normative structure required; O2/O3/O4; do not credit rejection of an unconstructed property (C06). | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| R36 | harmless extra unprefixed table | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. No demonstrated semantic change | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| R37 | harmless extra mneme-prefixed table | open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | NO effect demonstrated for this particular fixture; general acceptance is not inferred. No demonstrated semantic change | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| R38 | inheritance child added then dropped (lazy flags) | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. No demonstrated semantic change | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| R39 | no-op rule added then dropped | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. No demonstrated semantic change | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| R40 | mneme_schema forced RLS hides SELECT but allows INSERT | open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | YES: Header/store/history/receipt hidden from opening role | O2/O3: incompatible with demonstrated guarantee; must not accept as v1. | Two rendering fingerprints alone accept this state; recipe plus public variant or explicit engine property distinguishes it. |
| R41 | mneme_store forced RLS hides SELECT but allows INSERT | open ACCEPT; create InsufficientPrivilege/42501 | YES: Header/store/history/receipt hidden from opening role | O2/O3: incompatible with demonstrated guarantee; must not accept as v1. | Two rendering fingerprints alone accept this state; recipe plus public variant or explicit engine property distinguishes it. |
| R42 | mneme_operation forced RLS hides SELECT but allows INSERT | open ACCEPT; retry history.duplicate_record_id/MnemeValidationError | YES: Header/store/history/receipt hidden from opening role | O2/O3: incompatible with demonstrated guarantee; must not accept as v1. | Two rendering fingerprints alone accept this state; recipe plus public variant or explicit engine property distinguishes it. |
| R43 | mneme_record forced RLS hides SELECT but allows INSERT | open ACCEPT; N/variant oracle False | YES: Header/store/history/receipt hidden from opening role | O2/O3: incompatible with demonstrated guarantee; must not accept as v1. | Two rendering fingerprints alone accept this state; recipe plus public variant or explicit engine property distinguishes it. |
| C01 | mneme_store.store_id collation probe_loose | open ACCEPT; distinct ID a-b persistence.store_exists/MnemeValidationError | YES: Bytewise identity | O2/O3: incompatible with demonstrated guarantee; must not accept as v1. | Two rendering fingerprints alone accept this state; recipe plus public variant or explicit engine property distinguishes it. |
| C02 | mneme_record.record_id collation probe_loose | open ACCEPT; commit UniqueViolation/23505 | YES: Bytewise identity | O2/O3: incompatible with demonstrated guarantee; must not accept as v1. | Two rendering fingerprints alone accept this state; recipe plus public variant or explicit engine property distinguishes it. |
| C03 | mneme_operation.source_namespace collation probe_loose | open ACCEPT; distinct namespace persistence.operation_conflict/MnemeValidationError | YES: Bytewise identity | O2/O3: incompatible with demonstrated guarantee; must not accept as v1. | Two rendering fingerprints alone accept this state; recipe plus public variant or explicit engine property distinguishes it. |
| C04 | mneme_record.profile collation probe_loose | open ACCEPT; N/variant oracle True | CONDITIONAL / construction-limited: Routing column unused for equality at this layer | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| C05 | mneme_store.store_id collation "C" | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. Bytewise-equivalent collation | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| C06 | mneme_store.store_id collation "POSIX" | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. Bytewise-equivalent collation | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| C07 | record.schema_version identity GENERATED ALWAYS | open ACCEPT; commit GeneratedAlways/428C9 | YES: ALWAYS forbids explicit validated schema_version | O2/O3: incompatible with demonstrated guarantee; must not accept as v1. | Two rendering fingerprints alone accept this state; recipe plus public variant or explicit engine property distinguishes it. |
| C08 | record.schema_version identity GENERATED BY DEFAULT | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. BY DEFAULT leaves explicit values unchanged | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| C09 | schema.version identity always | open ACCEPT; N/variant oracle True | CONDITIONAL / construction-limited: No demonstrated semantic change | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| C10 | store.tail generated constant | open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | CONDITIONAL / construction-limited: Explicit tail update disallowed | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| C11 | record schema_version default added | open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | NO effect demonstrated for this particular fixture; general acceptance is not inferred. Explicit inserts unchanged but normative default differs | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| C12 | store tail default removed | open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | NO effect demonstrated for this particular fixture; general acceptance is not inferred. Creation relies on default tail | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| C13 | record.envelope storage PLAIN | open ACCEPT; commit ProgramLimitExceeded/54000 | YES: Full value-domain support for >8KiB canonical envelopes | O2/O3: incompatible with demonstrated guarantee; must not accept as v1. | Two rendering fingerprints alone accept this state; recipe plus public variant or explicit engine property distinguishes it. |
| C14 | record.envelope storage EXTERNAL | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. Transparent storage strategy | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| C15 | record.envelope storage MAIN | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. Transparent storage strategy | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| C16 | record.envelope storage EXTENDED | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. Transparent storage strategy | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| C17 | record.envelope compression pglz | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. No demonstrated semantic change | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| C18 | record.envelope compression lz4 | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. No demonstrated semantic change | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| C19 | record.schema_version domain instead of bigint | open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | CONDITIONAL / construction-limited: Domain can narrow admitted value domain | Normative structure required; O2/O3/O4; do not credit rejection of an unconstructed property (C06). | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| C20 | dropped-column residue | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. No demonstrated semantic change | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| C21 | column statistics target | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. No demonstrated semantic change | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| C22 | same live record columns in different order | open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | NO effect demonstrated for this particular fixture; general acceptance is not inferred. No demonstrated semantic change | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| C23 | deterministic ICU collation, shifted punctuation | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. Distinct byte sequences retain distinct equality; locale ordering differs | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| C24 | store.tail generated constant with original default spelling | open ACCEPT; commit GeneratedAlways/428C9 | YES: Explicit tail update disallowed despite same rendered expression | O2/O3: incompatible with demonstrated guarantee; must not accept as v1. | Two rendering fingerprints alone accept this state; recipe plus public variant or explicit engine property distinguishes it. |
| C25 | tail name changed | open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | CONDITIONAL / construction-limited: Required named column absent | Normative structure required; O2/O3/O4; do not credit rejection of an unconstructed property (C06). | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| C26 | version name changed | open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | CONDITIONAL / construction-limited: Required named column absent | Normative structure required; O2/O3/O4; do not credit rejection of an unconstructed property (C06). | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| C27 | tail narrowed to integer | open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | CONDITIONAL / construction-limited: Cannot represent full safe integer position range | Normative structure required; O2/O3/O4; do not credit rejection of an unconstructed property (C06). | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| C28 | record envelope nullable | open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | CONDITIONAL / construction-limited: Declared canonical envelope non-null domain weakened | Normative structure required; O2/O3/O4; do not credit rejection of an unconstructed property (C06). | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| K01 | record-ID unique DEFERRABLE | open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | CONDITIONAL / construction-limited: Constraint timing changes; locked valid writes may still be equivalent | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| K02 | record-ID unique DEFERRABLE INITIALLY DEFERRED | open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | CONDITIONAL / construction-limited: Constraint timing changes; locked valid writes may still be equivalent | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| K03 | record position CHECK NOT VALID | open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | CONDITIONAL / construction-limited: Can conceal preexisting invalid rows | Normative structure required; O2/O3/O4; do not credit rejection of an unconstructed property (C06). | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| K04 | record foreign key NOT VALID | open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | CONDITIONAL / construction-limited: Can conceal preexisting orphan rows | Normative structure required; O2/O3/O4; do not credit rejection of an unconstructed property (C06). | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| K05 | record FK ON DELETE CASCADE | open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | CONDITIONAL / construction-limited: Changes referential actions/timing; store API does not delete or rename stores | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| K06 | record FK ON UPDATE CASCADE | open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | CONDITIONAL / construction-limited: Changes referential actions/timing; store API does not delete or rename stores | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| K07 | record FK ON DELETE RESTRICT | open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | CONDITIONAL / construction-limited: Changes referential actions/timing; store API does not delete or rename stores | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| K08 | record FK DEFERRABLE INITIALLY DEFERRED | open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | CONDITIONAL / construction-limited: Changes referential actions/timing; store API does not delete or rename stores | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| K09 | constraint renamed | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. No demonstrated semantic change | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| K10 | extra CHECK true | open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | NO effect demonstrated for this particular fixture; general acceptance is not inferred. No demonstrated semantic change | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| K11 | extra CHECK excludes valid profile | open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | CONDITIONAL / construction-limited: Narrower admitted record domain | Normative structure required; O2/O3/O4; do not credit rejection of an unconstructed property (C06). | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| I01 | CREATE INDEX probe_idx ON mneme_record(profile) | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. Additional access path, no narrowed uniqueness | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| I02 | CREATE UNIQUE INDEX probe_idx ON mneme_record(profile) | open ACCEPT; commit UniqueViolation/23505 | YES: Extra unique profile excludes two valid records | O4: reject write-restricting extra index as compatible v1. | Two rendering fingerprints alone accept this state; recipe plus public variant or explicit engine property distinguishes it. |
| I03 | CREATE INDEX probe_idx ON mneme_record(profile) WHERE schema_version=1 | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. Additional access path, no narrowed uniqueness | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| I04 | CREATE INDEX probe_idx ON mneme_record((lower(profile))) | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. Additional access path, no narrowed uniqueness | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| I05 | CREATE INDEX probe_idx ON mneme_record USING hash(profile) | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. Additional access path, no narrowed uniqueness | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| I06 | CREATE UNIQUE INDEX probe_idx ON mneme_record(store_id,record_id) | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. Additional access path, no narrowed uniqueness | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| I07 | CREATE INDEX probe_idx ON mneme_record(record_id text_pattern_ops) | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. Additional access path, no narrowed uniqueness | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| I08 | Attach CREATE UNIQUE INDEX probe_idx ON mneme_record(record_id) WHERE schema_version=1 | setup WrongObjectType/42809; open ACCEPT; cross-store reuse UniqueViolation/23505 | YES: PostgreSQL may prohibit attachment; remaining extra global unique may reject per-store reuse Constraint attachment failed, but the remaining extra partial unique index restricts valid cross-store reuse. | O4: reject write-restricting extra index as compatible v1. | Two rendering fingerprints alone accept this state; recipe plus public variant or explicit engine property distinguishes it. |
| I09 | Attach CREATE UNIQUE INDEX probe_idx ON mneme_record((lower(record_id))) | setup WrongObjectType/42809; open ACCEPT; cross-store reuse UniqueViolation/23505 | YES: PostgreSQL may prohibit attachment; remaining extra global unique may reject per-store reuse Constraint attachment failed, but the remaining extra expression unique index restricts valid cross-store reuse. | O4: reject write-restricting extra index as compatible v1. | Two rendering fingerprints alone accept this state; recipe plus public variant or explicit engine property distinguishes it. |
| I10 | Attach CREATE UNIQUE INDEX probe_idx ON mneme_record(record_id text_pattern_ops) | setup WrongObjectType/42809; open ACCEPT; cross-store reuse UniqueViolation/23505 | YES: PostgreSQL may prohibit attachment; remaining extra global unique may reject per-store reuse Constraint attachment failed, but the remaining extra unique index restricts valid cross-store reuse. | O4: reject write-restricting extra index as compatible v1. | Two rendering fingerprints alone accept this state; recipe plus public variant or explicit engine property distinguishes it. |
| I11 | primary-key index fillfactor | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. No demonstrated semantic change | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| I12 | primary-key index clustering marker | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. No demonstrated semantic change | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| I13 | record replica identity full | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. No demonstrated semantic change | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| I14 | extra invalid unique index after concurrent build fails | setup UniqueViolation/23505; open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. Failed unique-index build may still restrict later valid writes; engine invalid-index state Invalid AND not-ready extra index: no valid-write rejection observed. Acceptance policy C01; do not confuse with I18. | UNDECIDED C01/C06 for invalid, not-ready harmless fixture; I18 must not pass. | Treating failed fixture construction as a killed validator mutant; discriminate residual catalog from intended state. |
| I15 | replacement operation PK using non-bytewise index collation | setup WrongObjectType/42809; open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | CONDITIONAL / construction-limited: Operation namespace equality must remain bytewise; server may reject attachment Nondefault-collation backing attachment refused by engine. Rejection observes missing PK, not an independently verified backing-index collation. | Normative structure required; O2/O3/O4; do not credit rejection of an unconstructed property (C06). | Treating failed fixture construction as a killed validator mutant; discriminate residual catalog from intended state. |
| I16 | replacement operation PK using text_pattern_ops | setup WrongObjectType/42809; open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | CONDITIONAL / construction-limited: Non-default opclass attachment may be prohibited by engine Nondefault-opclass backing attachment refused by engine. Rejection observes missing PK, not an independently verified opclass. | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Treating failed fixture construction as a killed validator mutant; discriminate residual catalog from intended state. |
| I17 | drop index backing operation primary key | setup DependentObjectsStillExist/2BP01; open ACCEPT; N/variant oracle True | CONDITIONAL / construction-limited: Engine dependency protects backing-index existence Dropping a live backing PK index alone is engine-protected; no invalid backing index was constructed. | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Treating failed fixture construction as a killed validator mutant; discriminate residual catalog from intended state. |
| I18 | invalid but ready extra unique index after late validation failure | open ACCEPT; commit UniqueViolation/23505 | YES: Invalid index can remain ready and enforce unwanted global uniqueness | O4: reject write-restricting extra index as compatible v1. | Two rendering fingerprints alone accept this state; recipe plus public variant or explicit engine property distinguishes it. |
| I19 | extra non-unique expression narrows token domain | open ACCEPT; commit InvalidTextRepresentation/22P02 | YES: Valid token r1 cannot be cast to integer; index evaluation rejects valid commit | O4: reject write-restricting extra index as compatible v1. | Two rendering fingerprints alone accept this state; recipe plus public variant or explicit engine property distinguishes it. |
| I20 | extra non-unique partial predicate narrows token domain | open ACCEPT; commit InvalidTextRepresentation/22P02 | YES: Predicate evaluation rejects valid token before insertion | O4: reject write-restricting extra index as compatible v1. | Two rendering fingerprints alone accept this state; recipe plus public variant or explicit engine property distinguishes it. |
| H01 | schema version 2 | open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | CONDITIONAL / construction-limited: Unrecognized version | Normative structure required; O2/O3/O4; do not credit rejection of an unconstructed property (C06). | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| H02 | schema version row absent | open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | CONDITIONAL / construction-limited: No recognized initialized singleton | Normative structure required; O2/O3/O4; do not credit rejection of an unconstructed property (C06). | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| S01 | session default Repeatable Read | open ACCEPT; N/variant oracle True | CONDITIONAL / construction-limited: No demonstrated semantic change | Accept normative positive control; preserve N/variant literal oracle. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| S02 | session default Serializable | open ACCEPT; N/variant oracle True | CONDITIONAL / construction-limited: No demonstrated semantic change | Accept normative positive control; preserve N/variant literal oracle. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| S03 | session synchronous_commit off | open ACCEPT; N/variant oracle True | CONDITIONAL / construction-limited: No demonstrated semantic change | Accept normative positive control; preserve N/variant literal oracle. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| S04 | session default_transaction_read_only on | open ACCEPT; N/variant oracle True | CONDITIONAL / construction-limited: No demonstrated semantic change | Accept normative positive control; preserve N/variant literal oracle. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| S05 | session row_security off | open ACCEPT; N/variant oracle True | CONDITIONAL / construction-limited: No demonstrated semantic change | UNDECIDED C01 acceptance of alternate shape; observed effect and construction limit remain separate. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| S06 | session replication role replica | open OperationalError; later NOT RUN | CONDITIONAL / construction-limited: No demonstrated semantic change | O7: do not suppress genuine permission/DDL failure; open privilege policy UNDECIDED C03/C06. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| S07 | session quote_all_identifiers on | open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | YES: refuses genuinely compatible v1 (availability/open rule). Presentation-only false refusal on reused schema; S10 independently confirms it on untouched schema. | O5: untouched valid v1 must open. Compare B03/S10. | Overstrict renderer/metadata comparison; positive public oracle must survive. |
| S08 | session standard_conforming_strings off | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. SQL lexical context must preserve intended catalog selection | Accept normative positive control; preserve N/variant literal oracle. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| S09 | session timezone Asia/Tokyo | open ACCEPT; N/variant oracle True | NO effect demonstrated for this particular fixture; general acceptance is not inferred. Store clock spelling and UTC normalization are library-owned | Accept normative positive control; preserve N/variant literal oracle. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| S10 | quote_all_identifiers on untouched fresh v1 | open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | YES: refuses genuinely compatible v1 (availability/open rule). Definite false refusal: same untouched valid v1 as B03. Must accept, independent of C01 alternate-shape policy. | O5: untouched valid v1 must open. Compare B03/S10. | Overstrict renderer/metadata comparison; positive public oracle must survive. |
| S11 | SQL_ASCII client representation | open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | CONDITIONAL / construction-limited: Catalog strings arrive as bytes; physical schema does not change | Databases precondition; runtime enforcement/error seam UNDECIDED C04. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| X01 | search_path=ce04,ce04_other | open ACCEPT; N/variant oracle True | CONDITIONAL / construction-limited: Object binding must stay in the selected canonical namespace | O1/O7; namespace/configuration acceptance UNDECIDED C02. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| X02 | search_path=ce04_other,ce04 | open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | CONDITIONAL / construction-limited: Object binding must stay in the selected canonical namespace | O1/O7; namespace/configuration acceptance UNDECIDED C02. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| X03 | search_path=no_such_schema,ce04 | open ACCEPT; N/variant oracle True | CONDITIONAL / construction-limited: Object binding must stay in the selected canonical namespace | O1/O7; namespace/configuration acceptance UNDECIDED C02. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| X04 | search_path=no_such_schema | open InvalidSchemaName/3F000; later NOT RUN | CONDITIONAL / construction-limited: Object binding must stay in the selected canonical namespace | O1/O7; namespace/configuration acceptance UNDECIDED C02. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| X05 | search_path=ce04,pg_catalog | open ACCEPT; N/variant oracle True | CONDITIONAL / construction-limited: Object binding must stay in the selected canonical namespace | O1/O7; namespace/configuration acceptance UNDECIDED C02. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| X06 | format_type shadow before explicit pg_catalog | open RaiseException/P0001; later NOT RUN | YES: Open invokes a schema function instead of engine catalog renderer | O1: actual engine metadata/version/lock; no substituted helper. Configuration boundary C02. | Unqualified helper/name lookup or pg_catalog-first assumed sufficient; use exact helper/marker witness. |
| X07 | same function with implicit pg_catalog first | open ACCEPT; N/variant oracle True | CONDITIONAL / construction-limited: No catalog helper hijack with implicit pg_catalog priority | O1/O7; namespace/configuration acceptance UNDECIDED C02. | Unqualified helper/name lookup or pg_catalog-first assumed sufficient; use exact helper/marker witness. |
| X08 | shadow renderer hides restrictive envelope domain | open ACCEPT; commit CheckViolation/23514 | YES: Catalog query is spoofed; a valid envelope is rejected by the hidden domain | O1: actual engine metadata/version/lock; no substituted helper. Configuration boundary C02. | Unqualified helper/name lookup or pg_catalog-first assumed sufficient; use exact helper/marker witness. |
| X09 | advisory-lock helper shadow | open ACCEPT; N/variant oracle True | YES: First open statement calls a function with no engine advisory lock | O1: actual engine metadata/version/lock; no substituted helper. Configuration boundary C02. | Unqualified helper/name lookup or pg_catalog-first assumed sufficient; use exact helper/marker witness. |
| X10 | lock-helper invocation observer | open SEE X09; {"engine_advisory_locks_during_helper": [[0]]} | YES: Observed absence of engine advisory lock Same open as X09; marker records zero genuine advisory locks. Independent observation, not another open. | O1: actual engine metadata/version/lock; no substituted helper. Configuration boundary C02. | Unqualified helper/name lookup or pg_catalog-first assumed sufficient; use exact helper/marker witness. |
| X11 | exact integer overload hides unsupported version | open ACCEPT; N/variant oracle True | YES: Polymorphic engine aggregate may be displaced even with implicit pg_catalog first | O1: actual engine metadata/version/lock; no substituted helper. Configuration boundary C02. | Unqualified helper/name lookup or pg_catalog-first assumed sufficient; use exact helper/marker witness. |
| D01 | database UTF8/POSIX/C | setup WrongObjectType/42809; open NOT EXECUTED | CONDITIONAL / construction-limited: Database rule and full Unicode/bytewise domain POSIX database locale construction refused on this Windows service; no open observation for that database. | Databases precondition; runtime enforcement/error seam UNDECIDED C04. | Treating failed fixture construction as a killed validator mutant; discriminate residual catalog from intended state. |
| D02 | database SQL_ASCII/C/C | initialization ACCEPT; open persistence.schema_incompatible/MnemeValidationError; later NOT RUN | CONDITIONAL / construction-limited: Database rule and full Unicode/bytewise domain Initialization returned successfully, but second open sees byte-valued text metadata and refuses; D05 controls client UTF8. | Databases precondition; runtime enforcement/error seam UNDECIDED C04. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| D03 | database LATIN1/C/C | initialization ACCEPT; open ACCEPT; N/variant oracle True | CONDITIONAL / construction-limited: Database rule and full Unicode/bytewise domain Nonconforming LATIN1 database accepts and roundtrips full Unicode in bytea; this is not permission to relax Databases. | Databases precondition; runtime enforcement/error seam UNDECIDED C04. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| D04 | database UTF8/C/POSIX | setup WrongObjectType/42809; open NOT EXECUTED | CONDITIONAL / construction-limited: Database rule and full Unicode/bytewise domain POSIX database locale construction refused on this Windows service; no open observation for that database. | Databases precondition; runtime enforcement/error seam UNDECIDED C04. | Treating failed fixture construction as a killed validator mutant; discriminate residual catalog from intended state. |
| D05 | SQL_ASCII database with UTF8 client | open ACCEPT; N/variant oracle True | CONDITIONAL / construction-limited: Reference database precondition differs; bytea preserves non-ASCII values Nonconforming SQL_ASCII database accepts with UTF8 client and full Unicode bytea roundtrip; policy C04. | Databases precondition; runtime enforcement/error seam UNDECIDED C04. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| V01 | actual PostgreSQL version and rendered definitions | open ACCEPT; N/variant oracle True | CONDITIONAL / construction-limited: Cross-release renderer compatibility not executed Actual 14.12 positive control. Other release behavior unobserved. | UNDECIDED C05/C06: actual alternate release unobserved. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |
| V02 | attempt server_version override | open OperationalError; later NOT RUN | CONDITIONAL / construction-limited: Server-owned version is not a client-selectable compatibility oracle Server-version option is refused at startup; this is NOT execution on PostgreSQL 13. | UNDECIDED C05/C06: actual alternate release unobserved. | Ignore this property or reject all differing metadata without policy; classify exact fixture and use positive/negative paired rows. |

## Interactions and limits that classification must retain

- **Persistence:** R03 cannot independently convert the referenced store while dependent tables are logged. R31 jointly changes all data tables. R01/R02/R04/R31 admission is a durability violation even though N succeeds; a normal commit/read is not a crash-safety test. PostgreSQL explicitly describes UNLOGGED tables as not crash-safe. [CREATE TABLE](https://www.postgresql.org/docs/14/sql-createtable.html)
- **Inheritance / row visibility:** R05 contributes position 99 through the parent scan while parent-only count remains two; the parent constraints do not protect the child. R06's empty parent connection is a different case, not a substitute for that kill witness. [Inheritance](https://www.postgresql.org/docs/14/ddl-inherit.html)
- **RLS and role context:** ENABLE alone under the owning role is different from FORCE; visibility and INSERT/RETURNING policy matter separately. R42 retries lose sight of their receipt; R43 loses the records while receipt/tail remain. This is not detected by looking only for successful initial writes. [Row security](https://www.postgresql.org/docs/14/ddl-rowsecurity.html)
- **Generated versus rendered default:** C10 happens to reject a differing rendered expression; C24 uses `(0)` whose default rendering matches but whose generated status forbids tail UPDATE. Identity ALWAYS on schema_version also survives both fingerprints (C07). [pg_attribute](https://www.postgresql.org/docs/14/catalog-pg-attribute.html)
- **Collation:** C01/C02/C03 demonstrate actual identity collisions under nondeterministic punctuation-ignoring collation. C23's deterministic collation preserves the tested identities. Neither its success nor C04's unused routing column establishes every comparison/order guarantee for arbitrary collations.
- **Extra indexes:** I01 and I19 are both nonunique; only the latter evaluates a narrowing expression. I14 is invalid/not-ready and inert for the observed writes; I18 is invalid/ready and still enforces unwanted global uniqueness. PostgreSQL documents this residual failed-build behavior. [CREATE INDEX](https://www.postgresql.org/docs/14/sql-createindex.html), [pg_index](https://www.postgresql.org/docs/14/catalog-pg-index.html)
- **Constraint-backed indexes:** engine attachment restrictions block partial/expression/nondefault sorting forms. I08..10 nevertheless leave an effectful extra index; I15/I16 leave a missing PK. An ordinary DROP of a backing index is refused (I17). No system-catalog writes, disabled internal RI trigger or corrupted backing index was used. A validator cannot claim those impossible fixture attempts as independent kills. [ALTER TABLE](https://www.postgresql.org/docs/14/sql-altertable.html)
- **Helpers and overloads:** X11's exact integer function signature beats the polymorphic aggregate even with implicit pg_catalog priority. A path-order observation from X07 does not discharge it. X08's real domain and X09's zero-lock marker are observations outside the spoofed rendering/locking helpers. [Function resolution](https://www.postgresql.org/docs/14/typeconv-func.html)
- **Session observations:** S01/S02/S04 record actual commit isolation/read-only state, not just defaults. S03 observes synchronous_commit on despite off default. S06 is startup refusal, not a tested replica session. No shared configuration was changed. Search-path behavior also distinguishes the first usable schema from an explicitly named missing or another session's temporary schema. [Client settings](https://www.postgresql.org/docs/14/runtime-config-client.html)
- **Harmless metadata:** lazy relation flags are not exact existence counts. R38/R39 record their actual state after object removal; dropped-column residue C20 retains no live extra column. Raw OIDs, owner ACL representation or transient physical statistics cannot be compared between independent databases as portable literals. [pg_class](https://www.postgresql.org/docs/14/catalog-pg-class.html)
- **Database/version bounds:** UTF8/C/C is the normative deployment rule. The Windows service refuses POSIX as a database locale, although a column POSIX collation is available. No other server release was run; V02 only proves the server_version parameter is not client-changeable. No Docker/install batch was launched to fill that gap during the reservation. Only project-local mneme_ts was used, never pg_default. Foreign-data-wrapper installation and owner transfer were denied by the actual non-superuser role. These remain explicit construction limits for the challenge pass, not missing current-behavior assertions.
- **Trust scope:** no shared-service crash, hardware fault, administrator schema mutation during an operation, or direct engine-catalog corruption was attempted. The schema-at-open question does not silently certify such a threat model. C06 must resolve any reliance on those assumptions before implementation.

## Complete special witness definitions and schedules

All SQL below is executed only in the private throwaway schema; after observation the functions/domains/indexes and fixture data were removed.

### X08 — genuine type differs from the reported fingerprint

```sql
CREATE DOMAIN ce04.probe_bytes AS bytea CHECK(octet_length(VALUE)<=10);
ALTER TABLE mneme_record ALTER COLUMN envelope TYPE ce04.probe_bytes;
CREATE FUNCTION ce04.format_type(oid,integer) RETURNS text LANGUAGE sql AS $$
 SELECT CASE WHEN $1='ce04.probe_bytes'::regtype THEN 'bytea'
             ELSE pg_catalog.format_type($1,$2) END
$$;
-- Open a NEW public handle with search_path=ce04,pg_catalog; run N.
-- Qualified pg_catalog.format_type identifies the actual probe_bytes domain.
DROP FUNCTION ce04.format_type(oid,integer);
ALTER TABLE mneme_record ALTER COLUMN envelope TYPE bytea;
DROP DOMAIN ce04.probe_bytes;
```

### X09/X10 — shared open-lock call displaced

```sql
CREATE TABLE ce04.probe_marker(lock_count bigint);
CREATE FUNCTION ce04.pg_advisory_xact_lock(bigint) RETURNS void
LANGUAGE plpgsql AS $$BEGIN
 INSERT INTO ce04.probe_marker SELECT count(*) FROM pg_catalog.pg_locks
 WHERE locktype='advisory' AND pid=pg_backend_pid();
END$$;
-- Public open with search_path=ce04,pg_catalog; run N; close handle.
SELECT lock_count FROM ce04.probe_marker; -- actual [[0]]
DROP FUNCTION ce04.pg_advisory_xact_lock(bigint);
DROP TABLE ce04.probe_marker;
```

### X11 — polymorphic aggregate displaced despite implicit pg_catalog

```sql
UPDATE mneme_schema SET version=2;
CREATE FUNCTION ce04.array_agg(integer) RETURNS integer[]
LANGUAGE sql IMMUTABLE AS $$SELECT ARRAY[1]$$;
-- Public open with search_path=ce04 (implicit pg_catalog first); run N.
-- Actual unsupported physical version is 2; open accepts.
DROP FUNCTION ce04.array_agg(integer);
UPDATE mneme_schema SET version=1;
```

### I14 versus I18 — failed build states must remain distinct

I14 seeds two `learning` records, then executes `CREATE UNIQUE INDEX CONCURRENTLY probe_idx ON mneme_record(profile)`. The first uniqueness scan fails. Observe `indisvalid=false, indisready=false`; public N succeeds. Drop index and clear data.

I18 seeds r1/r2 in store `seed`, with this function:

```sql
CREATE FUNCTION probe_pause(text) RETURNS text LANGUAGE plpgsql IMMUTABLE AS $$
BEGIN
 IF $1='r2' THEN PERFORM pg_advisory_xact_lock(73700401); END IF;
 RETURN $1;
END$$;
```

The intentionally gated function is a probe fixture, not a production immutability recommendation. Session A holds session advisory lock 73700401. Session B builds `CREATE UNIQUE INDEX CONCURRENTLY probe_idx ON mneme_record((probe_pause(record_id)))` with parallel maintenance off; A observes B's `wait_event='advisory'`. While B is in its first scan and the index is not ready, a public handle commits r1 to store `other` (valid per-store reuse). Release A's gate, join B; validation fails with duplicate key. Observe the residual index invalid **but ready**, then public N fails its first commit on r1. Drop index/function and delete private fixture records. Three records, no timing-based performance claim or host-wide load was used.

### Other special contexts

- X01..05 create `ce04_other.mneme_record(poison text)` and vary the literal path in the recipes. X06/X07 create `ce04.format_type(oid,integer) RETURNS text LANGUAGE plpgsql AS $$BEGIN RAISE EXCEPTION 'catalog shadow called'; END$$`, with explicit versus implicit catalog priority.
- R34 creates TEMP versions of the frozen four DDL tables in one observer connection, with `temp_tablespaces=mneme_ts`, inserts header version 1 and records `pg_my_temp_schema()::regnamespace::text`. Public open connects separately with that literal namespace as search_path. It cannot select the peer namespace. This does not claim a public open on four pre-existing TEMP tables in its own session.
- B03 initializes fresh schema `ce04_fresh` by public open. S10 changes only the next connection's `quote_all_identifiers=on`; the schema has never had an ALTER. Both handles use ce04_fresh. This is the false-refusal control independent of reused-schema residues.
- D01..04 create separate template0 databases in mneme_ts with each literal encoding/locale triple. D02/D03 first public open initializes; second public open tests compatibility and the unicode protocol. D05 reuses D02 with client_encoding=UTF8. Each created database is dropped in a finally block. Failed locale construction never reaches open.
- V01 records actual `version()` and both `pg_get_constraintdef(oid,false)` / `(oid,true)` for every v1 constraint. V02 attempts connection option `server_version=13.0`, which fails at startup; no release behavior is simulated.

## Per-row executed recipes and observations

The JSON excerpts below are literal observations (Unicode escaped for stable reproduction). `physical` uses parent-only rows and may be unavailable where permissions block the observer. Missing fields mean the observer was not used, not a passed assertion. Setup/undo are ordered lists. Ordinary empty setup means only the recorded connection options differ. Reversal failure would invalidate reuse; none was recorded.

### B01 — Unmodified v1

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
-- ordinary initialized v1; no forward DDL;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

### B02 — Unmodified v1, large valid payload

Public mode: `large`; connection options: ``.

Executed setup:

```sql
-- ordinary initialized v1; no forward DDL;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

### B03 — untouched fresh v1 positive control

Public mode: `normal`; connection options: `default unless special recipe above`.

Executed setup:

```sql
fresh schema; public open initializes;
```

Observed:

```json
{
  "open": "ACCEPT",
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04_fresh", "ce04_fresh", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

### R01 — mneme_record UNLOGGED

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record SET UNLOGGED;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "u", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "u", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "u", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_33865", "O", true], ["RI_ConstraintTrigger_a_33866", "O", true], ["RI_ConstraintTrigger_a_33877", "O", true], ["RI_ConstraintTrigger_a_33878", "O", true], ["RI_ConstraintTrigger_c_33867", "O", true], ["RI_ConstraintTrigger_c_33868", "O", true], ["RI_ConstraintTrigger_c_33879", "O", true], ["RI_ConstraintTrigger_c_33880", "O", true]]}
{"rules": []}
```

Executed reversal:

```sql
ALTER TABLE mneme_record SET LOGGED;
```

### R02 — mneme_operation UNLOGGED

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_operation SET UNLOGGED;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "u", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "u", false, false, null, 0, 16901], ["mneme_record", "r", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_33865", "O", true], ["RI_ConstraintTrigger_a_33866", "O", true], ["RI_ConstraintTrigger_a_33877", "O", true], ["RI_ConstraintTrigger_a_33878", "O", true], ["RI_ConstraintTrigger_c_33867", "O", true], ["RI_ConstraintTrigger_c_33868", "O", true], ["RI_ConstraintTrigger_c_33879", "O", true], ["RI_ConstraintTrigger_c_33880", "O", true]]}
{"rules": []}
```

Executed reversal:

```sql
ALTER TABLE mneme_operation SET LOGGED;
```

### R03 — mneme_store UNLOGGED

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_store SET UNLOGGED;
```

Observed:

```json
{
  "setup_error": {
    "exception": "InvalidTableDefinition",
    "sqlstate": "42P16",
    "code": null,
    "argument": null,
    "detail": "could not change table \"mneme_store\" to unlogged because it references logged table \"mneme_record\""
  },
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_33865", "O", true], ["RI_ConstraintTrigger_a_33866", "O", true], ["RI_ConstraintTrigger_a_33877", "O", true], ["RI_ConstraintTrigger_a_33878", "O", true], ["RI_ConstraintTrigger_c_33867", "O", true], ["RI_ConstraintTrigger_c_33868", "O", true], ["RI_ConstraintTrigger_c_33879", "O", true], ["RI_ConstraintTrigger_c_33880", "O", true]]}
{"rules": []}
```

Executed reversal:

```sql
ALTER TABLE mneme_store SET LOGGED;
```

Assessment correction/limit: Construction blocked: store-only UNLOGGED did not exist; R31 proves the jointly UNLOGGED case.

### R04 — mneme_schema UNLOGGED

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_schema SET UNLOGGED;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "u", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "u", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_33865", "O", true], ["RI_ConstraintTrigger_a_33866", "O", true], ["RI_ConstraintTrigger_a_33877", "O", true], ["RI_ConstraintTrigger_a_33878", "O", true], ["RI_ConstraintTrigger_c_33867", "O", true], ["RI_ConstraintTrigger_c_33868", "O", true], ["RI_ConstraintTrigger_c_33879", "O", true], ["RI_ConstraintTrigger_c_33880", "O", true]]}
{"rules": []}
```

Executed reversal:

```sql
ALTER TABLE mneme_schema SET LOGGED;
```

### R05 — record inheritance child with out-of-tail entry

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
CREATE TABLE probe_child () INHERITS (mneme_record);
INSERT INTO probe_child VALUES ('s',99,'shadow','learning','attempt',1,convert_to('{"record_id":"shadow","profile":"learning","record_type":"attempt","schema_version":1,"compatibility":"required","recorded_at":"2026-10-11T08:00:00.000000Z"}','UTF8'));
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": false,
    "read_positions": [
      1,
      2,
      99
    ],
    "through": {
      "store_id": "s",
      "position": 99
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": [["probe_child", "mneme_record"]]}
{"triggers": [["RI_ConstraintTrigger_a_33865", "O", true], ["RI_ConstraintTrigger_a_33866", "O", true], ["RI_ConstraintTrigger_a_33877", "O", true], ["RI_ConstraintTrigger_a_33878", "O", true], ["RI_ConstraintTrigger_c_33867", "O", true], ["RI_ConstraintTrigger_c_33868", "O", true], ["RI_ConstraintTrigger_c_33879", "O", true], ["RI_ConstraintTrigger_c_33880", "O", true]]}
{"rules": []}
```

Executed reversal:

```sql
DROP TABLE IF EXISTS probe_child;
```

### R06 — record inherits a parent

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
CREATE TABLE probe_parent (LIKE mneme_record INCLUDING CONSTRAINTS);
ALTER TABLE mneme_record INHERIT probe_parent;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": [["mneme_record", "probe_parent"]]}
{"triggers": [["RI_ConstraintTrigger_a_33865", "O", true], ["RI_ConstraintTrigger_a_33866", "O", true], ["RI_ConstraintTrigger_a_33877", "O", true], ["RI_ConstraintTrigger_a_33878", "O", true], ["RI_ConstraintTrigger_c_33867", "O", true], ["RI_ConstraintTrigger_c_33868", "O", true], ["RI_ConstraintTrigger_c_33879", "O", true], ["RI_ConstraintTrigger_c_33880", "O", true]]}
{"rules": []}
```

Executed reversal:

```sql
ALTER TABLE mneme_record NO INHERIT probe_parent;
DROP TABLE probe_parent;
```

### R07 — record RLS owner bypass deny

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record ENABLE ROW LEVEL SECURITY;
CREATE POLICY probe_policy ON mneme_record USING (false) WITH CHECK (false);
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", true, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_33865", "O", true], ["RI_ConstraintTrigger_a_33866", "O", true], ["RI_ConstraintTrigger_a_33877", "O", true], ["RI_ConstraintTrigger_a_33878", "O", true], ["RI_ConstraintTrigger_c_33867", "O", true], ["RI_ConstraintTrigger_c_33868", "O", true], ["RI_ConstraintTrigger_c_33879", "O", true], ["RI_ConstraintTrigger_c_33880", "O", true]]}
{"rules": []}
```

Executed reversal:

```sql
DROP POLICY probe_policy ON mneme_record;
ALTER TABLE mneme_record DISABLE ROW LEVEL SECURITY;
```

### R08 — record RLS force deny

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record ENABLE ROW LEVEL SECURITY;
ALTER TABLE mneme_record FORCE ROW LEVEL SECURITY;
CREATE POLICY probe_policy ON mneme_record USING (false) WITH CHECK (false);
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    0,
    0,
    0
  ],
  "later": {
    "created": true,
    "failed_at": "commit",
    "error": {
      "exception": "InsufficientPrivilege",
      "sqlstate": "42501",
      "code": null,
      "argument": null,
      "detail": "new row violates row-level security policy for table \"mneme_record\""
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", true, true, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_33865", "O", true], ["RI_ConstraintTrigger_a_33866", "O", true], ["RI_ConstraintTrigger_a_33877", "O", true], ["RI_ConstraintTrigger_a_33878", "O", true], ["RI_ConstraintTrigger_c_33867", "O", true], ["RI_ConstraintTrigger_c_33868", "O", true], ["RI_ConstraintTrigger_c_33879", "O", true], ["RI_ConstraintTrigger_c_33880", "O", true]]}
{"rules": []}
```

Executed reversal:

```sql
DROP POLICY probe_policy ON mneme_record;
ALTER TABLE mneme_record NO FORCE ROW LEVEL SECURITY;
ALTER TABLE mneme_record DISABLE ROW LEVEL SECURITY;
```

### R09 — record RLS force allow

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record ENABLE ROW LEVEL SECURITY;
ALTER TABLE mneme_record FORCE ROW LEVEL SECURITY;
CREATE POLICY probe_policy ON mneme_record USING (true) WITH CHECK (true);
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", true, true, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_33865", "O", true], ["RI_ConstraintTrigger_a_33866", "O", true], ["RI_ConstraintTrigger_a_33877", "O", true], ["RI_ConstraintTrigger_a_33878", "O", true], ["RI_ConstraintTrigger_c_33867", "O", true], ["RI_ConstraintTrigger_c_33868", "O", true], ["RI_ConstraintTrigger_c_33879", "O", true], ["RI_ConstraintTrigger_c_33880", "O", true]]}
{"rules": []}
```

Executed reversal:

```sql
DROP POLICY probe_policy ON mneme_record;
ALTER TABLE mneme_record NO FORCE ROW LEVEL SECURITY;
ALTER TABLE mneme_record DISABLE ROW LEVEL SECURITY;
```

### R10 — record INSERT rule discards records

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
CREATE RULE probe_rule AS ON INSERT TO mneme_record DO INSTEAD NOTHING;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    0,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": false,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": false,
    "read_positions": [],
    "through": {
      "store_id": "s",
      "position": 0
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_33865", "O", true], ["RI_ConstraintTrigger_a_33866", "O", true], ["RI_ConstraintTrigger_a_33877", "O", true], ["RI_ConstraintTrigger_a_33878", "O", true], ["RI_ConstraintTrigger_c_33867", "O", true], ["RI_ConstraintTrigger_c_33868", "O", true], ["RI_ConstraintTrigger_c_33879", "O", true], ["RI_ConstraintTrigger_c_33880", "O", true]]}
{"rules": [["probe_rule", "3", true]]}
```

Executed reversal:

```sql
DROP RULE probe_rule ON mneme_record;
```

### R11 — store UPDATE rule suppresses tail

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
CREATE RULE probe_rule AS ON UPDATE TO mneme_store DO INSTEAD NOTHING;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    0,
    0,
    null
  ],
  "later": {
    "failed_at": "create",
    "error": {
      "exception": "FeatureNotSupported",
      "sqlstate": "0A000",
      "code": null,
      "argument": null,
      "detail": "INSERT with ON CONFLICT clause cannot be used with table that has INSERT or UPDATE rules"
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_33865", "O", true], ["RI_ConstraintTrigger_a_33866", "O", true], ["RI_ConstraintTrigger_a_33877", "O", true], ["RI_ConstraintTrigger_a_33878", "O", true], ["RI_ConstraintTrigger_c_33867", "O", true], ["RI_ConstraintTrigger_c_33868", "O", true], ["RI_ConstraintTrigger_c_33879", "O", true], ["RI_ConstraintTrigger_c_33880", "O", true]]}
{"rules": [["probe_rule", "2", true]]}
```

Executed reversal:

```sql
DROP RULE probe_rule ON mneme_store;
```

### R12 — record no-op rule

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
CREATE RULE probe_rule AS ON INSERT TO mneme_record DO ALSO NOTHING;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_33865", "O", true], ["RI_ConstraintTrigger_a_33866", "O", true], ["RI_ConstraintTrigger_a_33877", "O", true], ["RI_ConstraintTrigger_a_33878", "O", true], ["RI_ConstraintTrigger_c_33867", "O", true], ["RI_ConstraintTrigger_c_33868", "O", true], ["RI_ConstraintTrigger_c_33879", "O", true], ["RI_ConstraintTrigger_c_33880", "O", true]]}
{"rules": [["probe_rule", "3", false]]}
```

Executed reversal:

```sql
DROP RULE IF EXISTS probe_rule ON mneme_record;
```

### R13 — record BEFORE ROW trigger

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
CREATE FUNCTION probe_fn() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NULL; END$$;
CREATE TRIGGER probe_trigger BEFORE INSERT ON mneme_record FOR EACH ROW EXECUTE FUNCTION probe_fn();
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    0,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": false,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": false,
    "read_positions": [],
    "through": {
      "store_id": "s",
      "position": 0
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_33865", "O", true], ["RI_ConstraintTrigger_a_33866", "O", true], ["RI_ConstraintTrigger_a_33877", "O", true], ["RI_ConstraintTrigger_a_33878", "O", true], ["RI_ConstraintTrigger_c_33867", "O", true], ["RI_ConstraintTrigger_c_33868", "O", true], ["RI_ConstraintTrigger_c_33879", "O", true], ["RI_ConstraintTrigger_c_33880", "O", true], ["probe_trigger", "O", false]]}
{"rules": []}
```

Executed reversal:

```sql
DROP TRIGGER probe_trigger ON mneme_record;
DROP FUNCTION probe_fn();
```

### R14 — record AFTER ROW trigger

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
CREATE FUNCTION probe_fn() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN DELETE FROM mneme_record WHERE store_id=NEW.store_id AND position=NEW.position; RETURN NEW; END$$;
CREATE TRIGGER probe_trigger AFTER INSERT ON mneme_record FOR EACH ROW EXECUTE FUNCTION probe_fn();
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    0,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": false,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": false,
    "read_positions": [],
    "through": {
      "store_id": "s",
      "position": 0
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_33865", "O", true], ["RI_ConstraintTrigger_a_33866", "O", true], ["RI_ConstraintTrigger_a_33877", "O", true], ["RI_ConstraintTrigger_a_33878", "O", true], ["RI_ConstraintTrigger_c_33867", "O", true], ["RI_ConstraintTrigger_c_33868", "O", true], ["RI_ConstraintTrigger_c_33879", "O", true], ["RI_ConstraintTrigger_c_33880", "O", true], ["probe_trigger", "O", false]]}
{"rules": []}
```

Executed reversal:

```sql
DROP TRIGGER probe_trigger ON mneme_record;
DROP FUNCTION probe_fn();
```

### R15 — record AFTER STATEMENT trigger

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
CREATE FUNCTION probe_fn() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN DELETE FROM mneme_record; RETURN NULL; END$$;
CREATE TRIGGER probe_trigger AFTER INSERT ON mneme_record FOR EACH STATEMENT EXECUTE FUNCTION probe_fn();
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    0,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": false,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": false,
    "read_positions": [],
    "through": {
      "store_id": "s",
      "position": 0
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_33865", "O", true], ["RI_ConstraintTrigger_a_33866", "O", true], ["RI_ConstraintTrigger_a_33877", "O", true], ["RI_ConstraintTrigger_a_33878", "O", true], ["RI_ConstraintTrigger_c_33867", "O", true], ["RI_ConstraintTrigger_c_33868", "O", true], ["RI_ConstraintTrigger_c_33879", "O", true], ["RI_ConstraintTrigger_c_33880", "O", true], ["probe_trigger", "O", false]]}
{"rules": []}
```

Executed reversal:

```sql
DROP TRIGGER probe_trigger ON mneme_record;
DROP FUNCTION probe_fn();
```

### R16 — record BEFORE STATEMENT trigger

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
CREATE FUNCTION probe_fn() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NULL; END$$;
CREATE TRIGGER probe_trigger BEFORE INSERT ON mneme_record FOR EACH STATEMENT EXECUTE FUNCTION probe_fn();
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_33865", "O", true], ["RI_ConstraintTrigger_a_33866", "O", true], ["RI_ConstraintTrigger_a_33877", "O", true], ["RI_ConstraintTrigger_a_33878", "O", true], ["RI_ConstraintTrigger_c_33867", "O", true], ["RI_ConstraintTrigger_c_33868", "O", true], ["RI_ConstraintTrigger_c_33879", "O", true], ["RI_ConstraintTrigger_c_33880", "O", true], ["probe_trigger", "O", false]]}
{"rules": []}
```

Executed reversal:

```sql
DROP TRIGGER probe_trigger ON mneme_record;
DROP FUNCTION probe_fn();
```

### R17 — record BEFORE ROW trigger

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
CREATE FUNCTION probe_fn() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NEW; END$$;
CREATE TRIGGER probe_trigger BEFORE INSERT ON mneme_record FOR EACH ROW EXECUTE FUNCTION probe_fn();
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_33865", "O", true], ["RI_ConstraintTrigger_a_33866", "O", true], ["RI_ConstraintTrigger_a_33877", "O", true], ["RI_ConstraintTrigger_a_33878", "O", true], ["RI_ConstraintTrigger_c_33867", "O", true], ["RI_ConstraintTrigger_c_33868", "O", true], ["RI_ConstraintTrigger_c_33879", "O", true], ["RI_ConstraintTrigger_c_33880", "O", true], ["probe_trigger", "O", false]]}
{"rules": []}
```

Executed reversal:

```sql
DROP TRIGGER probe_trigger ON mneme_record;
DROP FUNCTION probe_fn();
```

### R18 — disabled harmful user trigger

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
CREATE FUNCTION probe_fn() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NULL; END$$;
CREATE TRIGGER probe_trigger BEFORE INSERT ON mneme_record FOR EACH ROW EXECUTE FUNCTION probe_fn();
ALTER TABLE mneme_record DISABLE TRIGGER probe_trigger;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_33865", "O", true], ["RI_ConstraintTrigger_a_33866", "O", true], ["RI_ConstraintTrigger_a_33877", "O", true], ["RI_ConstraintTrigger_a_33878", "O", true], ["RI_ConstraintTrigger_c_33867", "O", true], ["RI_ConstraintTrigger_c_33868", "O", true], ["RI_ConstraintTrigger_c_33879", "O", true], ["RI_ConstraintTrigger_c_33880", "O", true], ["probe_trigger", "D", false]]}
{"rules": []}
```

Executed reversal:

```sql
DROP TRIGGER probe_trigger ON mneme_record;
DROP FUNCTION probe_fn();
```

### R19 — record fillfactor 50

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record SET (fillfactor=50);
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", false, false, ["fillfactor=50"], 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_33865", "O", true], ["RI_ConstraintTrigger_a_33866", "O", true], ["RI_ConstraintTrigger_a_33877", "O", true], ["RI_ConstraintTrigger_a_33878", "O", true], ["RI_ConstraintTrigger_c_33867", "O", true], ["RI_ConstraintTrigger_c_33868", "O", true], ["RI_ConstraintTrigger_c_33879", "O", true], ["RI_ConstraintTrigger_c_33880", "O", true]]}
{"rules": []}
```

Executed reversal:

```sql
ALTER TABLE mneme_record RESET (fillfactor);
```

### R20 — record autovacuum disabled

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record SET (autovacuum_enabled=false);
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", false, false, ["autovacuum_enabled=false"], 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_33865", "O", true], ["RI_ConstraintTrigger_a_33866", "O", true], ["RI_ConstraintTrigger_a_33877", "O", true], ["RI_ConstraintTrigger_a_33878", "O", true], ["RI_ConstraintTrigger_c_33867", "O", true], ["RI_ConstraintTrigger_c_33868", "O", true], ["RI_ConstraintTrigger_c_33879", "O", true], ["RI_ConstraintTrigger_c_33880", "O", true]]}
{"rules": []}
```

Executed reversal:

```sql
ALTER TABLE mneme_record RESET (autovacuum_enabled);
```

### R21 — record explicit mneme_ts tablespace

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record SET TABLESPACE mneme_ts;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_33865", "O", true], ["RI_ConstraintTrigger_a_33866", "O", true], ["RI_ConstraintTrigger_a_33877", "O", true], ["RI_ConstraintTrigger_a_33878", "O", true], ["RI_ConstraintTrigger_c_33867", "O", true], ["RI_ConstraintTrigger_c_33868", "O", true], ["RI_ConstraintTrigger_c_33879", "O", true], ["RI_ConstraintTrigger_c_33880", "O", true]]}
{"rules": []}
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

### R22 — record owner remains opening role

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record OWNER TO CURRENT_USER;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_33865", "O", true], ["RI_ConstraintTrigger_a_33866", "O", true], ["RI_ConstraintTrigger_a_33877", "O", true], ["RI_ConstraintTrigger_a_33878", "O", true], ["RI_ConstraintTrigger_c_33867", "O", true], ["RI_ConstraintTrigger_c_33868", "O", true], ["RI_ConstraintTrigger_c_33879", "O", true], ["RI_ConstraintTrigger_c_33880", "O", true]]}
{"rules": []}
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

### R23 — record INSERT grant removed

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
REVOKE INSERT ON mneme_record FROM CURRENT_USER;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    0,
    0,
    0
  ],
  "later": {
    "created": true,
    "failed_at": "commit",
    "error": {
      "exception": "InsufficientPrivilege",
      "sqlstate": "42501",
      "code": null,
      "argument": null,
      "detail": "permission denied for table mneme_record"
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_33865", "O", true], ["RI_ConstraintTrigger_a_33866", "O", true], ["RI_ConstraintTrigger_a_33877", "O", true], ["RI_ConstraintTrigger_a_33878", "O", true], ["RI_ConstraintTrigger_c_33867", "O", true], ["RI_ConstraintTrigger_c_33868", "O", true], ["RI_ConstraintTrigger_c_33879", "O", true], ["RI_ConstraintTrigger_c_33880", "O", true]]}
{"rules": []}
```

Executed reversal:

```sql
GRANT INSERT ON mneme_record TO CURRENT_USER;
```

### R24 — record SELECT grant removed

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
REVOKE SELECT ON mneme_record FROM CURRENT_USER;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical_error": {
    "exception": "InsufficientPrivilege",
    "sqlstate": "42501",
    "code": null,
    "argument": null,
    "detail": "permission denied for table mneme_record"
  },
  "later": {
    "created": true,
    "failed_at": "commit",
    "error": {
      "exception": "InsufficientPrivilege",
      "sqlstate": "42501",
      "code": null,
      "argument": null,
      "detail": "permission denied for table mneme_record"
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_33865", "O", true], ["RI_ConstraintTrigger_a_33866", "O", true], ["RI_ConstraintTrigger_a_33877", "O", true], ["RI_ConstraintTrigger_a_33878", "O", true], ["RI_ConstraintTrigger_c_33867", "O", true], ["RI_ConstraintTrigger_c_33868", "O", true], ["RI_ConstraintTrigger_c_33879", "O", true], ["RI_ConstraintTrigger_c_33880", "O", true]]}
{"rules": []}
```

Executed reversal:

```sql
GRANT SELECT ON mneme_record TO CURRENT_USER;
```

### R25 — schema version SELECT grant removed

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
REVOKE SELECT ON mneme_schema FROM CURRENT_USER;
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "InsufficientPrivilege",
    "sqlstate": "42501",
    "code": null,
    "argument": null,
    "detail": "permission denied for table mneme_schema"
  },
  "physical": [
    0,
    0,
    null
  ],
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_33865", "O", true], ["RI_ConstraintTrigger_a_33866", "O", true], ["RI_ConstraintTrigger_a_33877", "O", true], ["RI_ConstraintTrigger_a_33878", "O", true], ["RI_ConstraintTrigger_c_33867", "O", true], ["RI_ConstraintTrigger_c_33868", "O", true], ["RI_ConstraintTrigger_c_33879", "O", true], ["RI_ConstraintTrigger_c_33880", "O", true]]}
{"rules": []}
```

Executed reversal:

```sql
GRANT SELECT ON mneme_schema TO CURRENT_USER;
```

### R26 — record owner changed to postgres

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record OWNER TO postgres;
```

Observed:

```json
{
  "setup_error": {
    "exception": "InsufficientPrivilege",
    "sqlstate": "42501",
    "code": null,
    "argument": null,
    "detail": "must be member of role \"postgres\""
  },
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_33865", "O", true], ["RI_ConstraintTrigger_a_33866", "O", true], ["RI_ConstraintTrigger_a_33877", "O", true], ["RI_ConstraintTrigger_a_33878", "O", true], ["RI_ConstraintTrigger_c_33867", "O", true], ["RI_ConstraintTrigger_c_33868", "O", true], ["RI_ConstraintTrigger_c_33879", "O", true], ["RI_ConstraintTrigger_c_33880", "O", true]]}
{"rules": []}
```

Executed reversal:

```sql
ALTER TABLE mneme_record OWNER TO CURRENT_USER;
```

Assessment correction/limit: Ownership transfer not constructed (42501); ordinary role unchanged. Owner identity alone is not an effective-rights oracle.

### R27 — record replaced by view

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record RENAME TO probe_saved;
CREATE VIEW mneme_record AS SELECT * FROM probe_saved;
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables ['mneme_operation', 'mneme_schema', 'mneme_store'] are not schema version 1"
  },
  "physical": [
    0,
    0,
    null
  ],
  "clock_contexts": [],
  "fingerprints": {
    "columns_match": false,
    "constraints_match": false
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "v", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_34077", "O", true], ["RI_ConstraintTrigger_a_34078", "O", true], ["RI_ConstraintTrigger_a_34143", "O", true], ["RI_ConstraintTrigger_a_34144", "O", true], ["RI_ConstraintTrigger_c_34079", "O", true], ["RI_ConstraintTrigger_c_34080", "O", true], ["RI_ConstraintTrigger_c_34145", "O", true], ["RI_ConstraintTrigger_c_34146", "O", true]]}
{"rules": [["_RETURN", "1", true]]}
{"relation_flags": [["mneme_operation", true, false, true, false, "d", 2], ["mneme_operation_pkey", false, false, false, false, "n", 403], ["mneme_record", false, true, false, false, "n", 0], ["mneme_record_pkey", false, false, false, false, "n", 403], ["mneme_record_store_id_record_id_key", false, false, false, false, "n", 403], ["mneme_schema", true, false, false, false, "d", 2], ["mneme_schema_pkey", false, false, false, false, "n", 403], ["mneme_store", true, false, true, false, "d", 2], ["mneme_store_pkey", false, false, false, false, "n", 403]]}
```

Executed reversal:

```sql
DROP VIEW mneme_record;
ALTER TABLE probe_saved RENAME TO mneme_record;
```

### R28 — record replaced by materialized view

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record RENAME TO probe_saved;
CREATE MATERIALIZED VIEW mneme_record AS SELECT * FROM probe_saved;
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables ['mneme_operation', 'mneme_schema', 'mneme_store'] are not schema version 1"
  },
  "physical": [
    0,
    0,
    null
  ],
  "clock_contexts": [],
  "fingerprints": {
    "columns_match": false,
    "constraints_match": false
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "m", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_34077", "O", true], ["RI_ConstraintTrigger_a_34078", "O", true], ["RI_ConstraintTrigger_a_34143", "O", true], ["RI_ConstraintTrigger_a_34144", "O", true], ["RI_ConstraintTrigger_c_34079", "O", true], ["RI_ConstraintTrigger_c_34080", "O", true], ["RI_ConstraintTrigger_c_34145", "O", true], ["RI_ConstraintTrigger_c_34146", "O", true]]}
{"rules": [["_RETURN", "1", true]]}
{"relation_flags": [["mneme_operation", true, false, true, false, "d", 2], ["mneme_operation_pkey", false, false, false, false, "n", 403], ["mneme_record", false, true, false, false, "d", 2], ["mneme_record_pkey", false, false, false, false, "n", 403], ["mneme_record_store_id_record_id_key", false, false, false, false, "n", 403], ["mneme_schema", true, false, false, false, "d", 2], ["mneme_schema_pkey", false, false, false, false, "n", 403], ["mneme_store", true, false, true, false, "d", 2], ["mneme_store_pkey", false, false, false, false, "n", 403]]}
```

Executed reversal:

```sql
DROP MATERIALIZED VIEW mneme_record;
ALTER TABLE probe_saved RENAME TO mneme_record;
```

### R29 — record replaced by partitioned table

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record RENAME TO probe_saved;
CREATE TABLE mneme_record (LIKE probe_saved INCLUDING ALL) PARTITION BY RANGE(position);
```

Observed:

```json
{
  "setup_error": {
    "exception": "FeatureNotSupported",
    "sqlstate": "0A000",
    "code": null,
    "argument": null,
    "detail": "unique constraint on partitioned table must include all partitioning columns\nDETAIL:  UNIQUE constraint on table \"mneme_record\" lacks column \"position\" which is part of the partition key."
  },
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables ['mneme_operation', 'mneme_schema', 'mneme_store'] are not schema version 1"
  },
  "physical_error": {
    "exception": "UndefinedTable",
    "sqlstate": "42P01",
    "code": null,
    "argument": null,
    "detail": "relation \"mneme_record\" does not exist\nLINE 1: SELECT (SELECT count(*) FROM ONLY mneme_record),(SELECT coun...\n                                          ^"
  },
  "clock_contexts": [],
  "fingerprints": {
    "columns_match": false,
    "constraints_match": false
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_34077", "O", true], ["RI_ConstraintTrigger_a_34078", "O", true], ["RI_ConstraintTrigger_a_34143", "O", true], ["RI_ConstraintTrigger_a_34144", "O", true], ["RI_ConstraintTrigger_c_34079", "O", true], ["RI_ConstraintTrigger_c_34080", "O", true], ["RI_ConstraintTrigger_c_34145", "O", true], ["RI_ConstraintTrigger_c_34146", "O", true]]}
{"rules": []}
{"relation_flags": [["mneme_operation", true, false, true, false, "d", 2], ["mneme_operation_pkey", false, false, false, false, "n", 403], ["mneme_record_pkey", false, false, false, false, "n", 403], ["mneme_record_store_id_record_id_key", false, false, false, false, "n", 403], ["mneme_schema", true, false, false, false, "d", 2], ["mneme_schema_pkey", false, false, false, false, "n", 403], ["mneme_store", true, false, true, false, "d", 2], ["mneme_store_pkey", false, false, false, false, "n", 403]]}
```

Executed reversal:

```sql
DROP TABLE IF EXISTS mneme_record;
ALTER TABLE probe_saved RENAME TO mneme_record;
```

Assessment correction/limit: Partitioned LIKE INCLUDING ALL construction failed; open saw a missing record table, not the proposed complete partitioned schema.

### R30 — foreign-wrapper construction under opening role

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
CREATE FOREIGN DATA WRAPPER probe_fdw;
```

Observed:

```json
{
  "setup_error": {
    "exception": "InsufficientPrivilege",
    "sqlstate": "42501",
    "code": null,
    "argument": null,
    "detail": "permission denied to create foreign-data wrapper \"probe_fdw\"\nHINT:  Must be superuser to create a foreign-data wrapper."
  },
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_34077", "O", true], ["RI_ConstraintTrigger_a_34078", "O", true], ["RI_ConstraintTrigger_a_34143", "O", true], ["RI_ConstraintTrigger_a_34144", "O", true], ["RI_ConstraintTrigger_c_34079", "O", true], ["RI_ConstraintTrigger_c_34080", "O", true], ["RI_ConstraintTrigger_c_34145", "O", true], ["RI_ConstraintTrigger_c_34146", "O", true]]}
{"rules": []}
{"relation_flags": [["mneme_operation", true, false, true, false, "d", 2], ["mneme_operation_pkey", false, false, false, false, "n", 403], ["mneme_record", true, false, true, false, "d", 2], ["mneme_record_pkey", false, false, false, false, "n", 403], ["mneme_record_store_id_record_id_key", false, false, false, false, "n", 403], ["mneme_schema", true, false, false, false, "d", 2], ["mneme_schema_pkey", false, false, false, false, "n", 403], ["mneme_store", true, false, true, false, "d", 2], ["mneme_store_pkey", false, false, false, false, "n", 403]]}
```

Executed reversal:

```sql
DROP FOREIGN DATA WRAPPER IF EXISTS probe_fdw;
```

Assessment correction/limit: Foreign wrapper construction denied (42501); no actual foreign replacement was opened.

### R31 — record and operation and store UNLOGGED together

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record SET UNLOGGED;
ALTER TABLE mneme_operation SET UNLOGGED;
ALTER TABLE mneme_store SET UNLOGGED;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "u", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "u", false, false, null, 0, 16901], ["mneme_record", "r", "u", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "u", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "u", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "u", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "u", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_34077", "O", true], ["RI_ConstraintTrigger_a_34078", "O", true], ["RI_ConstraintTrigger_a_34143", "O", true], ["RI_ConstraintTrigger_a_34144", "O", true], ["RI_ConstraintTrigger_c_34079", "O", true], ["RI_ConstraintTrigger_c_34080", "O", true], ["RI_ConstraintTrigger_c_34145", "O", true], ["RI_ConstraintTrigger_c_34146", "O", true]]}
{"rules": []}
{"relation_flags": [["mneme_operation", true, false, true, false, "d", 2], ["mneme_operation_pkey", false, false, false, false, "n", 403], ["mneme_record", true, false, true, false, "d", 2], ["mneme_record_pkey", false, false, false, false, "n", 403], ["mneme_record_store_id_record_id_key", false, false, false, false, "n", 403], ["mneme_schema", true, false, false, false, "d", 2], ["mneme_schema_pkey", false, false, false, false, "n", 403], ["mneme_store", true, false, true, false, "d", 2], ["mneme_store_pkey", false, false, false, false, "n", 403]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_store SET LOGGED;
ALTER TABLE mneme_record SET LOGGED;
ALTER TABLE mneme_operation SET LOGGED;
```

### R32 — record internal FK triggers disabled

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record DISABLE TRIGGER ALL;
```

Observed:

```json
{
  "setup_error": {
    "exception": "InsufficientPrivilege",
    "sqlstate": "42501",
    "code": null,
    "argument": null,
    "detail": "permission denied: \"RI_ConstraintTrigger_c_34145\" is a system trigger"
  },
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_34077", "O", true], ["RI_ConstraintTrigger_a_34078", "O", true], ["RI_ConstraintTrigger_a_34143", "O", true], ["RI_ConstraintTrigger_a_34144", "O", true], ["RI_ConstraintTrigger_c_34079", "O", true], ["RI_ConstraintTrigger_c_34080", "O", true], ["RI_ConstraintTrigger_c_34145", "O", true], ["RI_ConstraintTrigger_c_34146", "O", true]]}
{"rules": []}
{"relation_flags": [["mneme_operation", true, false, true, false, "d", 2], ["mneme_operation_pkey", false, false, false, false, "n", 403], ["mneme_record", true, false, true, true, "d", 2], ["mneme_record_pkey", false, false, false, false, "n", 403], ["mneme_record_store_id_record_id_key", false, false, false, false, "n", 403], ["mneme_schema", true, false, false, false, "d", 2], ["mneme_schema_pkey", false, false, false, false, "n", 403], ["mneme_store", true, false, true, false, "d", 2], ["mneme_store_pkey", false, false, false, false, "n", 403]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_record ENABLE TRIGGER USER;
```

Assessment correction/limit: Internal trigger disable denied (42501); no disabled RI trigger state was opened.

### R33 — replica-only harmful user trigger

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
CREATE FUNCTION probe_fn() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NULL; END$$;
CREATE TRIGGER probe_trigger BEFORE INSERT ON mneme_record FOR EACH ROW EXECUTE FUNCTION probe_fn();
ALTER TABLE mneme_record ENABLE REPLICA TRIGGER probe_trigger;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_34077", "O", true], ["RI_ConstraintTrigger_a_34078", "O", true], ["RI_ConstraintTrigger_a_34143", "O", true], ["RI_ConstraintTrigger_a_34144", "O", true], ["RI_ConstraintTrigger_c_34079", "O", true], ["RI_ConstraintTrigger_c_34080", "O", true], ["RI_ConstraintTrigger_c_34145", "O", true], ["RI_ConstraintTrigger_c_34146", "O", true], ["probe_trigger", "R", false]]}
{"rules": []}
{"relation_flags": [["mneme_operation", true, false, true, false, "d", 2], ["mneme_operation_pkey", false, false, false, false, "n", 403], ["mneme_record", true, false, true, true, "d", 2], ["mneme_record_pkey", false, false, false, false, "n", 403], ["mneme_record_store_id_record_id_key", false, false, false, false, "n", 403], ["mneme_schema", true, false, false, false, "d", 2], ["mneme_schema_pkey", false, false, false, false, "n", 403], ["mneme_store", true, false, true, false, "d", 2], ["mneme_store_pkey", false, false, false, false, "n", 403]]}
```

Executed reversal:

```sql
DROP TRIGGER probe_trigger ON mneme_record;
DROP FUNCTION probe_fn();
```

### R34 — peer-session temporary v1 tables

Public mode: `normal`; connection options: `default unless special recipe above`.

Executed setup:

```sql
four TEMP versions of exact DDL; explicit peer temp namespace;
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "InvalidSchemaName",
    "sqlstate": "3F000",
    "code": null,
    "argument": null,
    "detail": "no schema has been selected to create in\nLINE 1: CREATE TABLE mneme_schema (singleton boolean PRIMARY KEY DEF...\n                     ^"
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "pg_temp_3", "pg_temp, ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "t", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "t", false, false, null, 0, 16901], ["mneme_record", "r", "t", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "t", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "t", false, false, null, 0, 16901], ["mneme_schema", "r", "t", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "t", false, false, null, 0, 16901], ["mneme_store", "r", "t", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "t", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_34315", "O", true], ["RI_ConstraintTrigger_a_34316", "O", true], ["RI_ConstraintTrigger_a_34327", "O", true], ["RI_ConstraintTrigger_a_34328", "O", true], ["RI_ConstraintTrigger_c_34317", "O", true], ["RI_ConstraintTrigger_c_34318", "O", true], ["RI_ConstraintTrigger_c_34329", "O", true], ["RI_ConstraintTrigger_c_34330", "O", true]]}
{"rules": []}
{"relation_flags": [["mneme_operation", true, false, true, false, "d", 2], ["mneme_operation_pkey", false, false, false, false, "n", 403], ["mneme_record", true, false, true, false, "d", 2], ["mneme_record_pkey", false, false, false, false, "n", 403], ["mneme_record_store_id_record_id_key", false, false, false, false, "n", 403], ["mneme_schema", true, false, false, false, "d", 2], ["mneme_schema_pkey", false, false, false, false, "n", 403], ["mneme_store", true, false, true, false, "d", 2], ["mneme_store_pkey", false, false, false, false, "n", 403]]}
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

Assessment correction/limit: Only peer-session TEMP state executed; a public new connection cannot select that temporary namespace (3F000).

### R35 — actual partitioned record with columns and checks only

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record RENAME TO probe_saved;
CREATE TABLE mneme_record (LIKE probe_saved INCLUDING CONSTRAINTS) PARTITION BY RANGE(position);
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables ['mneme_operation', 'mneme_record', 'mneme_schema', 'mneme_store'] are not schema version 1"
  },
  "physical": [
    0,
    0,
    null
  ],
  "clock_contexts": [],
  "fingerprints": {
    "columns_match": false,
    "constraints_match": false
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "p", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_34077", "O", true], ["RI_ConstraintTrigger_a_34078", "O", true], ["RI_ConstraintTrigger_a_34143", "O", true], ["RI_ConstraintTrigger_a_34144", "O", true], ["RI_ConstraintTrigger_c_34079", "O", true], ["RI_ConstraintTrigger_c_34080", "O", true], ["RI_ConstraintTrigger_c_34145", "O", true], ["RI_ConstraintTrigger_c_34146", "O", true]]}
{"rules": []}
{"relation_flags": [["mneme_operation", true, false, true, false, "d", 2], ["mneme_operation_pkey", false, false, false, false, "n", 403], ["mneme_record", false, false, false, false, "d", 0], ["mneme_record_pkey", false, false, false, false, "n", 403], ["mneme_record_store_id_record_id_key", false, false, false, false, "n", 403], ["mneme_schema", true, false, false, false, "d", 2], ["mneme_schema_pkey", false, false, false, false, "n", 403], ["mneme_store", true, false, true, false, "d", 2], ["mneme_store_pkey", false, false, false, false, "n", 403]]}
```

Executed reversal:

```sql
DROP TABLE mneme_record;
ALTER TABLE probe_saved RENAME TO mneme_record;
```

Assessment correction/limit: Actual partitioned relation constructed with columns/checks, lacking normative uniqueness; rejection does not isolate a relkind guard.

### R36 — harmless extra unprefixed table

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
CREATE TABLE probe_extra (x integer);
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_34077", "O", true], ["RI_ConstraintTrigger_a_34078", "O", true], ["RI_ConstraintTrigger_a_34143", "O", true], ["RI_ConstraintTrigger_a_34144", "O", true], ["RI_ConstraintTrigger_c_34079", "O", true], ["RI_ConstraintTrigger_c_34080", "O", true], ["RI_ConstraintTrigger_c_34145", "O", true], ["RI_ConstraintTrigger_c_34146", "O", true]]}
{"rules": []}
{"relation_flags": [["mneme_operation", true, false, true, false, "d", 2], ["mneme_operation_pkey", false, false, false, false, "n", 403], ["mneme_record", true, false, true, false, "d", 2], ["mneme_record_pkey", false, false, false, false, "n", 403], ["mneme_record_store_id_record_id_key", false, false, false, false, "n", 403], ["mneme_schema", true, false, false, false, "d", 2], ["mneme_schema_pkey", false, false, false, false, "n", 403], ["mneme_store", true, false, true, false, "d", 2], ["mneme_store_pkey", false, false, false, false, "n", 403]]}
```

Executed reversal:

```sql
DROP TABLE probe_extra;
```

### R37 — harmless extra mneme-prefixed table

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
CREATE TABLE mneme_extra (x integer);
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables ['mneme_extra', 'mneme_operation', 'mneme_record', 'mneme_schema', 'mneme_store'] are not schema version 1"
  },
  "physical": [
    0,
    0,
    null
  ],
  "clock_contexts": [],
  "fingerprints": {
    "columns_match": false,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_extra", "r", "p", false, false, null, 0, 16901], ["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_34077", "O", true], ["RI_ConstraintTrigger_a_34078", "O", true], ["RI_ConstraintTrigger_a_34143", "O", true], ["RI_ConstraintTrigger_a_34144", "O", true], ["RI_ConstraintTrigger_c_34079", "O", true], ["RI_ConstraintTrigger_c_34080", "O", true], ["RI_ConstraintTrigger_c_34145", "O", true], ["RI_ConstraintTrigger_c_34146", "O", true]]}
{"rules": []}
{"relation_flags": [["mneme_extra", false, false, false, false, "d", 2], ["mneme_operation", true, false, true, false, "d", 2], ["mneme_operation_pkey", false, false, false, false, "n", 403], ["mneme_record", true, false, true, false, "d", 2], ["mneme_record_pkey", false, false, false, false, "n", 403], ["mneme_record_store_id_record_id_key", false, false, false, false, "n", 403], ["mneme_schema", true, false, false, false, "d", 2], ["mneme_schema_pkey", false, false, false, false, "n", 403], ["mneme_store", true, false, true, false, "d", 2], ["mneme_store_pkey", false, false, false, false, "n", 403]]}
```

Executed reversal:

```sql
DROP TABLE mneme_extra;
```

### R38 — inheritance child added then dropped (lazy flags)

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
CREATE TABLE probe_child () INHERITS(mneme_record);
DROP TABLE probe_child;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_34077", "O", true], ["RI_ConstraintTrigger_a_34078", "O", true], ["RI_ConstraintTrigger_a_34143", "O", true], ["RI_ConstraintTrigger_a_34144", "O", true], ["RI_ConstraintTrigger_c_34079", "O", true], ["RI_ConstraintTrigger_c_34080", "O", true], ["RI_ConstraintTrigger_c_34145", "O", true], ["RI_ConstraintTrigger_c_34146", "O", true]]}
{"rules": []}
{"relation_flags": [["mneme_operation", true, false, true, false, "d", 2], ["mneme_operation_pkey", false, false, false, false, "n", 403], ["mneme_record", true, false, true, true, "d", 2], ["mneme_record_pkey", false, false, false, false, "n", 403], ["mneme_record_store_id_record_id_key", false, false, false, false, "n", 403], ["mneme_schema", true, false, false, false, "d", 2], ["mneme_schema_pkey", false, false, false, false, "n", 403], ["mneme_store", true, false, true, false, "d", 2], ["mneme_store_pkey", false, false, false, false, "n", 403]]}
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

### R39 — no-op rule added then dropped

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
CREATE RULE probe_rule AS ON INSERT TO mneme_record DO ALSO NOTHING;
DROP RULE probe_rule ON mneme_record;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_34077", "O", true], ["RI_ConstraintTrigger_a_34078", "O", true], ["RI_ConstraintTrigger_a_34143", "O", true], ["RI_ConstraintTrigger_a_34144", "O", true], ["RI_ConstraintTrigger_c_34079", "O", true], ["RI_ConstraintTrigger_c_34080", "O", true], ["RI_ConstraintTrigger_c_34145", "O", true], ["RI_ConstraintTrigger_c_34146", "O", true]]}
{"rules": []}
{"relation_flags": [["mneme_operation", true, false, true, false, "d", 2], ["mneme_operation_pkey", false, false, false, false, "n", 403], ["mneme_record", true, true, true, false, "d", 2], ["mneme_record_pkey", false, false, false, false, "n", 403], ["mneme_record_store_id_record_id_key", false, false, false, false, "n", 403], ["mneme_schema", true, false, false, false, "d", 2], ["mneme_schema_pkey", false, false, false, false, "n", 403], ["mneme_store", true, false, true, false, "d", 2], ["mneme_store_pkey", false, false, false, false, "n", 403]]}
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

### R40 — mneme_schema forced RLS hides SELECT but allows INSERT

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_schema ENABLE ROW LEVEL SECURITY;
ALTER TABLE mneme_schema FORCE ROW LEVEL SECURITY;
CREATE POLICY probe_policy ON mneme_schema USING(false) WITH CHECK(true);
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables ['mneme_operation', 'mneme_record', 'mneme_schema', 'mneme_store'] are not schema version 1"
  },
  "physical": [
    0,
    0,
    null
  ],
  "clock_contexts": [],
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", true, true, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_34077", "O", true], ["RI_ConstraintTrigger_a_34078", "O", true], ["RI_ConstraintTrigger_a_34143", "O", true], ["RI_ConstraintTrigger_a_34144", "O", true], ["RI_ConstraintTrigger_c_34079", "O", true], ["RI_ConstraintTrigger_c_34080", "O", true], ["RI_ConstraintTrigger_c_34145", "O", true], ["RI_ConstraintTrigger_c_34146", "O", true]]}
{"rules": []}
{"relation_flags": [["mneme_operation", true, false, true, false, "d", 2], ["mneme_operation_pkey", false, false, false, false, "n", 403], ["mneme_record", true, true, true, false, "d", 2], ["mneme_record_pkey", false, false, false, false, "n", 403], ["mneme_record_store_id_record_id_key", false, false, false, false, "n", 403], ["mneme_schema", true, false, false, false, "d", 2], ["mneme_schema_pkey", false, false, false, false, "n", 403], ["mneme_store", true, false, true, false, "d", 2], ["mneme_store_pkey", false, false, false, false, "n", 403]]}
```

Executed reversal:

```sql
DROP POLICY probe_policy ON mneme_schema;
ALTER TABLE mneme_schema NO FORCE ROW LEVEL SECURITY;
ALTER TABLE mneme_schema DISABLE ROW LEVEL SECURITY;
```

### R41 — mneme_store forced RLS hides SELECT but allows INSERT

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_store ENABLE ROW LEVEL SECURITY;
ALTER TABLE mneme_store FORCE ROW LEVEL SECURITY;
CREATE POLICY probe_policy ON mneme_store USING(false) WITH CHECK(true);
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    0,
    0,
    null
  ],
  "clock_contexts": [],
  "later": {
    "failed_at": "create",
    "error": {
      "exception": "InsufficientPrivilege",
      "sqlstate": "42501",
      "code": null,
      "argument": null,
      "detail": "new row violates row-level security policy for table \"mneme_store\""
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", true, true, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_34077", "O", true], ["RI_ConstraintTrigger_a_34078", "O", true], ["RI_ConstraintTrigger_a_34143", "O", true], ["RI_ConstraintTrigger_a_34144", "O", true], ["RI_ConstraintTrigger_c_34079", "O", true], ["RI_ConstraintTrigger_c_34080", "O", true], ["RI_ConstraintTrigger_c_34145", "O", true], ["RI_ConstraintTrigger_c_34146", "O", true]]}
{"rules": []}
{"relation_flags": [["mneme_operation", true, false, true, false, "d", 2], ["mneme_operation_pkey", false, false, false, false, "n", 403], ["mneme_record", true, true, true, false, "d", 2], ["mneme_record_pkey", false, false, false, false, "n", 403], ["mneme_record_store_id_record_id_key", false, false, false, false, "n", 403], ["mneme_schema", true, false, false, false, "d", 2], ["mneme_schema_pkey", false, false, false, false, "n", 403], ["mneme_store", true, false, true, false, "d", 2], ["mneme_store_pkey", false, false, false, false, "n", 403]]}
```

Executed reversal:

```sql
DROP POLICY probe_policy ON mneme_store;
ALTER TABLE mneme_store NO FORCE ROW LEVEL SECURITY;
ALTER TABLE mneme_store DISABLE ROW LEVEL SECURITY;
```

### R42 — mneme_operation forced RLS hides SELECT but allows INSERT

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_operation ENABLE ROW LEVEL SECURITY;
ALTER TABLE mneme_operation FORCE ROW LEVEL SECURITY;
CREATE POLICY probe_policy ON mneme_operation USING(false) WITH CHECK(true);
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    0,
    2
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "failed_at": "retry",
    "error": {
      "exception": "MnemeValidationError",
      "sqlstate": null,
      "code": "history.duplicate_record_id",
      "argument": "records",
      "detail": "history.duplicate_record_id: record_id 'r1' is already committed"
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", true, true, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", false, false, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_34077", "O", true], ["RI_ConstraintTrigger_a_34078", "O", true], ["RI_ConstraintTrigger_a_34143", "O", true], ["RI_ConstraintTrigger_a_34144", "O", true], ["RI_ConstraintTrigger_c_34079", "O", true], ["RI_ConstraintTrigger_c_34080", "O", true], ["RI_ConstraintTrigger_c_34145", "O", true], ["RI_ConstraintTrigger_c_34146", "O", true]]}
{"rules": []}
{"relation_flags": [["mneme_operation", true, false, true, false, "d", 2], ["mneme_operation_pkey", false, false, false, false, "n", 403], ["mneme_record", true, true, true, false, "d", 2], ["mneme_record_pkey", false, false, false, false, "n", 403], ["mneme_record_store_id_record_id_key", false, false, false, false, "n", 403], ["mneme_schema", true, false, false, false, "d", 2], ["mneme_schema_pkey", false, false, false, false, "n", 403], ["mneme_store", true, false, true, false, "d", 2], ["mneme_store_pkey", false, false, false, false, "n", 403]]}
```

Executed reversal:

```sql
DROP POLICY probe_policy ON mneme_operation;
ALTER TABLE mneme_operation NO FORCE ROW LEVEL SECURITY;
ALTER TABLE mneme_operation DISABLE ROW LEVEL SECURITY;
```

### R43 — mneme_record forced RLS hides SELECT but allows INSERT

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record ENABLE ROW LEVEL SECURITY;
ALTER TABLE mneme_record FORCE ROW LEVEL SECURITY;
CREATE POLICY probe_policy ON mneme_record USING(false) WITH CHECK(true);
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    0,
    1,
    2
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": false,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": false,
    "read_positions": [],
    "through": {
      "store_id": "s",
      "position": 0
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"relations": [["mneme_operation", "r", "p", false, false, null, 0, 16901], ["mneme_operation_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record", "r", "p", true, true, null, 0, 16901], ["mneme_record_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_record_store_id_record_id_key", "i", "p", false, false, null, 0, 16901], ["mneme_schema", "r", "p", false, false, null, 0, 16901], ["mneme_schema_pkey", "i", "p", false, false, null, 0, 16901], ["mneme_store", "r", "p", false, false, null, 0, 16901], ["mneme_store_pkey", "i", "p", false, false, null, 0, 16901]]}
{"inheritance": []}
{"triggers": [["RI_ConstraintTrigger_a_34077", "O", true], ["RI_ConstraintTrigger_a_34078", "O", true], ["RI_ConstraintTrigger_a_34143", "O", true], ["RI_ConstraintTrigger_a_34144", "O", true], ["RI_ConstraintTrigger_c_34079", "O", true], ["RI_ConstraintTrigger_c_34080", "O", true], ["RI_ConstraintTrigger_c_34145", "O", true], ["RI_ConstraintTrigger_c_34146", "O", true]]}
{"rules": []}
{"relation_flags": [["mneme_operation", true, false, true, false, "d", 2], ["mneme_operation_pkey", false, false, false, false, "n", 403], ["mneme_record", true, true, true, false, "d", 2], ["mneme_record_pkey", false, false, false, false, "n", 403], ["mneme_record_store_id_record_id_key", false, false, false, false, "n", 403], ["mneme_schema", true, false, false, false, "d", 2], ["mneme_schema_pkey", false, false, false, false, "n", 403], ["mneme_store", true, false, true, false, "d", 2], ["mneme_store_pkey", false, false, false, false, "n", 403]]}
```

Executed reversal:

```sql
DROP POLICY probe_policy ON mneme_record;
ALTER TABLE mneme_record NO FORCE ROW LEVEL SECURITY;
ALTER TABLE mneme_record DISABLE ROW LEVEL SECURITY;
```

### C01 — mneme_store.store_id collation probe_loose

Public mode: `collide`; connection options: ``.

Executed setup:

```sql
CREATE COLLATION probe_loose (provider=icu,locale='und-u-ka-shifted',deterministic=false);
ALTER TABLE mneme_store ALTER COLUMN store_id TYPE text COLLATE probe_loose;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    0,
    0,
    0
  ],
  "later": {
    "created": true,
    "failed_at": "distinct ID a-b",
    "error": {
      "exception": "MnemeValidationError",
      "sqlstate": null,
      "code": "persistence.store_exists",
      "argument": "store_id",
      "detail": "persistence.store_exists: store 'a-b' exists"
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"attributes": [["mneme_operation", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_operation", "mutation", 4, false, "", "", 0, "x", ""], ["mneme_operation", "first_position", 5, false, "", "", 0, "p", ""], ["mneme_operation", "last_position", 6, false, "", "", 0, "p", ""], ["mneme_operation", "recorded_at", 7, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_record", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record", "position", 2, false, "", "", 0, "p", ""], ["mneme_record", "record_id", 3, false, "", "", 100, "x", ""], ["mneme_record", "profile", 4, false, "", "", 100, "x", ""], ["mneme_record", "record_type", 5, false, "", "", 100, "x", ""], ["mneme_record", "schema_version", 6, false, "", "", 0, "p", ""], ["mneme_record", "envelope", 7, false, "", "", 0, "x", ""], ["mneme_record_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_pkey", "position", 2, false, "", "", 0, "p", ""], ["mneme_record_store_id_record_id_key", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_store_id_record_id_key", "record_id", 2, false, "", "", 100, "x", ""], ["mneme_schema", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_schema", "version", 2, false, "", "", 0, "p", ""], ["mneme_schema_pkey", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_store", "store_id", 1, false, "", "", 33946, "x", ""], ["mneme_store", "tail", 2, false, "", "", 0, "p", ""], ["mneme_store_pkey", "store_id", 1, false, "", "", 33946, "x", ""]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_store ALTER COLUMN store_id TYPE text COLLATE "default";
DROP COLLATION probe_loose;
```

### C02 — mneme_record.record_id collation probe_loose

Public mode: `record_collision`; connection options: ``.

Executed setup:

```sql
CREATE COLLATION probe_loose (provider=icu,locale='und-u-ka-shifted',deterministic=false);
ALTER TABLE mneme_record ALTER COLUMN record_id TYPE text COLLATE probe_loose;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    0,
    0,
    0
  ],
  "later": {
    "created": true,
    "failed_at": "commit",
    "error": {
      "exception": "UniqueViolation",
      "sqlstate": "23505",
      "code": null,
      "argument": null,
      "detail": "duplicate key value violates unique constraint \"mneme_record_store_id_record_id_key\"\nDETAIL:  Key (store_id, record_id)=(s, a-b) already exists."
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"attributes": [["mneme_operation", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_operation", "mutation", 4, false, "", "", 0, "x", ""], ["mneme_operation", "first_position", 5, false, "", "", 0, "p", ""], ["mneme_operation", "last_position", 6, false, "", "", 0, "p", ""], ["mneme_operation", "recorded_at", 7, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_record", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record", "position", 2, false, "", "", 0, "p", ""], ["mneme_record", "record_id", 3, false, "", "", 33971, "x", ""], ["mneme_record", "profile", 4, false, "", "", 100, "x", ""], ["mneme_record", "record_type", 5, false, "", "", 100, "x", ""], ["mneme_record", "schema_version", 6, false, "", "", 0, "p", ""], ["mneme_record", "envelope", 7, false, "", "", 0, "x", ""], ["mneme_record_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_pkey", "position", 2, false, "", "", 0, "p", ""], ["mneme_record_store_id_record_id_key", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_store_id_record_id_key", "record_id", 2, false, "", "", 33971, "x", ""], ["mneme_schema", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_schema", "version", 2, false, "", "", 0, "p", ""], ["mneme_schema_pkey", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_store", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_store", "tail", 2, false, "", "", 0, "p", ""], ["mneme_store_pkey", "store_id", 1, false, "", "", 100, "x", ""]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_record ALTER COLUMN record_id TYPE text COLLATE "default";
DROP COLLATION probe_loose;
```

### C03 — mneme_operation.source_namespace collation probe_loose

Public mode: `namespace`; connection options: ``.

Executed setup:

```sql
CREATE COLLATION probe_loose (provider=icu,locale='und-u-ka-shifted',deterministic=false);
ALTER TABLE mneme_operation ALTER COLUMN source_namespace TYPE text COLLATE probe_loose;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "failed_at": "distinct namespace",
    "error": {
      "exception": "MnemeValidationError",
      "sqlstate": null,
      "code": "persistence.operation_conflict",
      "argument": "operation",
      "detail": "persistence.operation_conflict: a different mutation under a committed operation identity (G-013)"
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"attributes": [["mneme_operation", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation", "source_namespace", 2, false, "", "", 33976, "x", ""], ["mneme_operation", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_operation", "mutation", 4, false, "", "", 0, "x", ""], ["mneme_operation", "first_position", 5, false, "", "", 0, "p", ""], ["mneme_operation", "last_position", 6, false, "", "", 0, "p", ""], ["mneme_operation", "recorded_at", 7, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_namespace", 2, false, "", "", 33976, "x", ""], ["mneme_operation_pkey", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_record", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record", "position", 2, false, "", "", 0, "p", ""], ["mneme_record", "record_id", 3, false, "", "", 100, "x", ""], ["mneme_record", "profile", 4, false, "", "", 100, "x", ""], ["mneme_record", "record_type", 5, false, "", "", 100, "x", ""], ["mneme_record", "schema_version", 6, false, "", "", 0, "p", ""], ["mneme_record", "envelope", 7, false, "", "", 0, "x", ""], ["mneme_record_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_pkey", "position", 2, false, "", "", 0, "p", ""], ["mneme_record_store_id_record_id_key", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_store_id_record_id_key", "record_id", 2, false, "", "", 100, "x", ""], ["mneme_schema", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_schema", "version", 2, false, "", "", 0, "p", ""], ["mneme_schema_pkey", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_store", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_store", "tail", 2, false, "", "", 0, "p", ""], ["mneme_store_pkey", "store_id", 1, false, "", "", 100, "x", ""]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_operation ALTER COLUMN source_namespace TYPE text COLLATE "default";
DROP COLLATION probe_loose;
```

### C04 — mneme_record.profile collation probe_loose

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
CREATE COLLATION probe_loose (provider=icu,locale='und-u-ka-shifted',deterministic=false);
ALTER TABLE mneme_record ALTER COLUMN profile TYPE text COLLATE probe_loose;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"attributes": [["mneme_operation", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_operation", "mutation", 4, false, "", "", 0, "x", ""], ["mneme_operation", "first_position", 5, false, "", "", 0, "p", ""], ["mneme_operation", "last_position", 6, false, "", "", 0, "p", ""], ["mneme_operation", "recorded_at", 7, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_record", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record", "position", 2, false, "", "", 0, "p", ""], ["mneme_record", "record_id", 3, false, "", "", 100, "x", ""], ["mneme_record", "profile", 4, false, "", "", 33981, "x", ""], ["mneme_record", "record_type", 5, false, "", "", 100, "x", ""], ["mneme_record", "schema_version", 6, false, "", "", 0, "p", ""], ["mneme_record", "envelope", 7, false, "", "", 0, "x", ""], ["mneme_record_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_pkey", "position", 2, false, "", "", 0, "p", ""], ["mneme_record_store_id_record_id_key", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_store_id_record_id_key", "record_id", 2, false, "", "", 100, "x", ""], ["mneme_schema", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_schema", "version", 2, false, "", "", 0, "p", ""], ["mneme_schema_pkey", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_store", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_store", "tail", 2, false, "", "", 0, "p", ""], ["mneme_store_pkey", "store_id", 1, false, "", "", 100, "x", ""]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_record ALTER COLUMN profile TYPE text COLLATE "default";
DROP COLLATION probe_loose;
```

### C05 — mneme_store.store_id collation "C"

Public mode: `collide`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_store ALTER COLUMN store_id TYPE text COLLATE "C";
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "distinct_ids": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"attributes": [["mneme_operation", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_operation", "mutation", 4, false, "", "", 0, "x", ""], ["mneme_operation", "first_position", 5, false, "", "", 0, "p", ""], ["mneme_operation", "last_position", 6, false, "", "", 0, "p", ""], ["mneme_operation", "recorded_at", 7, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_record", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record", "position", 2, false, "", "", 0, "p", ""], ["mneme_record", "record_id", 3, false, "", "", 100, "x", ""], ["mneme_record", "profile", 4, false, "", "", 100, "x", ""], ["mneme_record", "record_type", 5, false, "", "", 100, "x", ""], ["mneme_record", "schema_version", 6, false, "", "", 0, "p", ""], ["mneme_record", "envelope", 7, false, "", "", 0, "x", ""], ["mneme_record_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_pkey", "position", 2, false, "", "", 0, "p", ""], ["mneme_record_store_id_record_id_key", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_store_id_record_id_key", "record_id", 2, false, "", "", 100, "x", ""], ["mneme_schema", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_schema", "version", 2, false, "", "", 0, "p", ""], ["mneme_schema_pkey", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_store", "store_id", 1, false, "", "", 950, "x", ""], ["mneme_store", "tail", 2, false, "", "", 0, "p", ""], ["mneme_store_pkey", "store_id", 1, false, "", "", 950, "x", ""]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_store ALTER COLUMN store_id TYPE text COLLATE "default";
```

### C06 — mneme_store.store_id collation "POSIX"

Public mode: `collide`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_store ALTER COLUMN store_id TYPE text COLLATE "POSIX";
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "distinct_ids": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"attributes": [["mneme_operation", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_operation", "mutation", 4, false, "", "", 0, "x", ""], ["mneme_operation", "first_position", 5, false, "", "", 0, "p", ""], ["mneme_operation", "last_position", 6, false, "", "", 0, "p", ""], ["mneme_operation", "recorded_at", 7, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_record", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record", "position", 2, false, "", "", 0, "p", ""], ["mneme_record", "record_id", 3, false, "", "", 100, "x", ""], ["mneme_record", "profile", 4, false, "", "", 100, "x", ""], ["mneme_record", "record_type", 5, false, "", "", 100, "x", ""], ["mneme_record", "schema_version", 6, false, "", "", 0, "p", ""], ["mneme_record", "envelope", 7, false, "", "", 0, "x", ""], ["mneme_record_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_pkey", "position", 2, false, "", "", 0, "p", ""], ["mneme_record_store_id_record_id_key", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_store_id_record_id_key", "record_id", 2, false, "", "", 100, "x", ""], ["mneme_schema", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_schema", "version", 2, false, "", "", 0, "p", ""], ["mneme_schema_pkey", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_store", "store_id", 1, false, "", "", 951, "x", ""], ["mneme_store", "tail", 2, false, "", "", 0, "p", ""], ["mneme_store_pkey", "store_id", 1, false, "", "", 951, "x", ""]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_store ALTER COLUMN store_id TYPE text COLLATE "default";
```

### C07 — record.schema_version identity GENERATED ALWAYS

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record ALTER COLUMN schema_version ADD GENERATED ALWAYS AS IDENTITY;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    0,
    0,
    0
  ],
  "later": {
    "created": true,
    "failed_at": "commit",
    "error": {
      "exception": "GeneratedAlways",
      "sqlstate": "428C9",
      "code": null,
      "argument": null,
      "detail": "cannot insert a non-DEFAULT value into column \"schema_version\"\nDETAIL:  Column \"schema_version\" is an identity column defined as GENERATED ALWAYS.\nHINT:  Use OVERRIDING SYSTEM VALUE to override."
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"attributes": [["mneme_operation", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_operation", "mutation", 4, false, "", "", 0, "x", ""], ["mneme_operation", "first_position", 5, false, "", "", 0, "p", ""], ["mneme_operation", "last_position", 6, false, "", "", 0, "p", ""], ["mneme_operation", "recorded_at", 7, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_record", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record", "position", 2, false, "", "", 0, "p", ""], ["mneme_record", "record_id", 3, false, "", "", 100, "x", ""], ["mneme_record", "profile", 4, false, "", "", 100, "x", ""], ["mneme_record", "record_type", 5, false, "", "", 100, "x", ""], ["mneme_record", "schema_version", 6, false, "a", "", 0, "p", ""], ["mneme_record", "envelope", 7, false, "", "", 0, "x", ""], ["mneme_record_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_pkey", "position", 2, false, "", "", 0, "p", ""], ["mneme_record_schema_version_seq", "last_value", 1, false, "", "", 0, "p", ""], ["mneme_record_schema_version_seq", "log_cnt", 2, false, "", "", 0, "p", ""], ["mneme_record_schema_version_seq", "is_called", 3, false, "", "", 0, "p", ""], ["mneme_record_store_id_record_id_key", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_store_id_record_id_key", "record_id", 2, false, "", "", 100, "x", ""], ["mneme_schema", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_schema", "version", 2, false, "", "", 0, "p", ""], ["mneme_schema_pkey", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_store", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_store", "tail", 2, false, "", "", 0, "p", ""], ["mneme_store_pkey", "store_id", 1, false, "", "", 100, "x", ""]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_record ALTER COLUMN schema_version DROP IDENTITY;
```

### C08 — record.schema_version identity GENERATED BY DEFAULT

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record ALTER COLUMN schema_version ADD GENERATED BY DEFAULT AS IDENTITY;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"attributes": [["mneme_operation", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_operation", "mutation", 4, false, "", "", 0, "x", ""], ["mneme_operation", "first_position", 5, false, "", "", 0, "p", ""], ["mneme_operation", "last_position", 6, false, "", "", 0, "p", ""], ["mneme_operation", "recorded_at", 7, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_record", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record", "position", 2, false, "", "", 0, "p", ""], ["mneme_record", "record_id", 3, false, "", "", 100, "x", ""], ["mneme_record", "profile", 4, false, "", "", 100, "x", ""], ["mneme_record", "record_type", 5, false, "", "", 100, "x", ""], ["mneme_record", "schema_version", 6, false, "d", "", 0, "p", ""], ["mneme_record", "envelope", 7, false, "", "", 0, "x", ""], ["mneme_record_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_pkey", "position", 2, false, "", "", 0, "p", ""], ["mneme_record_schema_version_seq", "last_value", 1, false, "", "", 0, "p", ""], ["mneme_record_schema_version_seq", "log_cnt", 2, false, "", "", 0, "p", ""], ["mneme_record_schema_version_seq", "is_called", 3, false, "", "", 0, "p", ""], ["mneme_record_store_id_record_id_key", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_store_id_record_id_key", "record_id", 2, false, "", "", 100, "x", ""], ["mneme_schema", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_schema", "version", 2, false, "", "", 0, "p", ""], ["mneme_schema_pkey", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_store", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_store", "tail", 2, false, "", "", 0, "p", ""], ["mneme_store_pkey", "store_id", 1, false, "", "", 100, "x", ""]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_record ALTER COLUMN schema_version DROP IDENTITY;
```

### C09 — schema.version identity always

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_schema ALTER COLUMN version ADD GENERATED ALWAYS AS IDENTITY;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"attributes": [["mneme_operation", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_operation", "mutation", 4, false, "", "", 0, "x", ""], ["mneme_operation", "first_position", 5, false, "", "", 0, "p", ""], ["mneme_operation", "last_position", 6, false, "", "", 0, "p", ""], ["mneme_operation", "recorded_at", 7, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_record", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record", "position", 2, false, "", "", 0, "p", ""], ["mneme_record", "record_id", 3, false, "", "", 100, "x", ""], ["mneme_record", "profile", 4, false, "", "", 100, "x", ""], ["mneme_record", "record_type", 5, false, "", "", 100, "x", ""], ["mneme_record", "schema_version", 6, false, "", "", 0, "p", ""], ["mneme_record", "envelope", 7, false, "", "", 0, "x", ""], ["mneme_record_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_pkey", "position", 2, false, "", "", 0, "p", ""], ["mneme_record_store_id_record_id_key", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_store_id_record_id_key", "record_id", 2, false, "", "", 100, "x", ""], ["mneme_schema", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_schema", "version", 2, false, "a", "", 0, "p", ""], ["mneme_schema_pkey", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_schema_version_seq", "last_value", 1, false, "", "", 0, "p", ""], ["mneme_schema_version_seq", "log_cnt", 2, false, "", "", 0, "p", ""], ["mneme_schema_version_seq", "is_called", 3, false, "", "", 0, "p", ""], ["mneme_store", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_store", "tail", 2, false, "", "", 0, "p", ""], ["mneme_store_pkey", "store_id", 1, false, "", "", 100, "x", ""]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_schema ALTER COLUMN version DROP IDENTITY;
```

### C10 — store.tail generated constant

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_store DROP COLUMN tail;
ALTER TABLE mneme_store ADD COLUMN tail bigint GENERATED ALWAYS AS (0::bigint) STORED NOT NULL;
ALTER TABLE mneme_store ADD CONSTRAINT mneme_store_tail_check CHECK(tail BETWEEN 0 AND 9007199254740991);
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables ['mneme_operation', 'mneme_record', 'mneme_schema', 'mneme_store'] are not schema version 1"
  },
  "physical": [
    0,
    0,
    null
  ],
  "fingerprints": {
    "columns_match": false,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"attributes": [["mneme_operation", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_operation", "mutation", 4, false, "", "", 0, "x", ""], ["mneme_operation", "first_position", 5, false, "", "", 0, "p", ""], ["mneme_operation", "last_position", 6, false, "", "", 0, "p", ""], ["mneme_operation", "recorded_at", 7, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_record", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record", "position", 2, false, "", "", 0, "p", ""], ["mneme_record", "record_id", 3, false, "", "", 100, "x", ""], ["mneme_record", "profile", 4, false, "", "", 100, "x", ""], ["mneme_record", "record_type", 5, false, "", "", 100, "x", ""], ["mneme_record", "schema_version", 6, false, "", "", 0, "p", ""], ["mneme_record", "envelope", 7, false, "", "", 0, "x", ""], ["mneme_record_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_pkey", "position", 2, false, "", "", 0, "p", ""], ["mneme_record_store_id_record_id_key", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_store_id_record_id_key", "record_id", 2, false, "", "", 100, "x", ""], ["mneme_schema", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_schema", "version", 2, false, "", "", 0, "p", ""], ["mneme_schema_pkey", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_store", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_store", "........pg.dropped.2........", 2, true, "", "", 0, "p", ""], ["mneme_store", "tail", 3, false, "", "s", 0, "p", ""], ["mneme_store_pkey", "store_id", 1, false, "", "", 100, "x", ""]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_store DROP COLUMN tail;
ALTER TABLE mneme_store ADD COLUMN tail bigint NOT NULL DEFAULT 0 CHECK(tail BETWEEN 0 AND 9007199254740991);
```

### C11 — record schema_version default added

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record ALTER COLUMN schema_version SET DEFAULT 2;
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables ['mneme_operation', 'mneme_record', 'mneme_schema', 'mneme_store'] are not schema version 1"
  },
  "physical": [
    0,
    0,
    null
  ],
  "fingerprints": {
    "columns_match": false,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"attributes": [["mneme_operation", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_operation", "mutation", 4, false, "", "", 0, "x", ""], ["mneme_operation", "first_position", 5, false, "", "", 0, "p", ""], ["mneme_operation", "last_position", 6, false, "", "", 0, "p", ""], ["mneme_operation", "recorded_at", 7, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_record", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record", "position", 2, false, "", "", 0, "p", ""], ["mneme_record", "record_id", 3, false, "", "", 100, "x", ""], ["mneme_record", "profile", 4, false, "", "", 100, "x", ""], ["mneme_record", "record_type", 5, false, "", "", 100, "x", ""], ["mneme_record", "schema_version", 6, false, "", "", 0, "p", ""], ["mneme_record", "envelope", 7, false, "", "", 0, "x", ""], ["mneme_record_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_pkey", "position", 2, false, "", "", 0, "p", ""], ["mneme_record_store_id_record_id_key", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_store_id_record_id_key", "record_id", 2, false, "", "", 100, "x", ""], ["mneme_schema", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_schema", "version", 2, false, "", "", 0, "p", ""], ["mneme_schema_pkey", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_store", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_store", "........pg.dropped.2........", 2, true, "", "", 0, "p", ""], ["mneme_store", "........pg.dropped.3........", 3, true, "", "", 0, "p", ""], ["mneme_store", "tail", 4, false, "", "", 0, "p", ""], ["mneme_store_pkey", "store_id", 1, false, "", "", 100, "x", ""]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_record ALTER COLUMN schema_version DROP DEFAULT;
```

### C12 — store tail default removed

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_store ALTER COLUMN tail DROP DEFAULT;
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables ['mneme_operation', 'mneme_record', 'mneme_schema', 'mneme_store'] are not schema version 1"
  },
  "physical": [
    0,
    0,
    null
  ],
  "fingerprints": {
    "columns_match": false,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"attributes": [["mneme_operation", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_operation", "mutation", 4, false, "", "", 0, "x", ""], ["mneme_operation", "first_position", 5, false, "", "", 0, "p", ""], ["mneme_operation", "last_position", 6, false, "", "", 0, "p", ""], ["mneme_operation", "recorded_at", 7, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_record", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record", "position", 2, false, "", "", 0, "p", ""], ["mneme_record", "record_id", 3, false, "", "", 100, "x", ""], ["mneme_record", "profile", 4, false, "", "", 100, "x", ""], ["mneme_record", "record_type", 5, false, "", "", 100, "x", ""], ["mneme_record", "schema_version", 6, false, "", "", 0, "p", ""], ["mneme_record", "envelope", 7, false, "", "", 0, "x", ""], ["mneme_record_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_pkey", "position", 2, false, "", "", 0, "p", ""], ["mneme_record_store_id_record_id_key", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_store_id_record_id_key", "record_id", 2, false, "", "", 100, "x", ""], ["mneme_schema", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_schema", "version", 2, false, "", "", 0, "p", ""], ["mneme_schema_pkey", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_store", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_store", "........pg.dropped.2........", 2, true, "", "", 0, "p", ""], ["mneme_store", "........pg.dropped.3........", 3, true, "", "", 0, "p", ""], ["mneme_store", "tail", 4, false, "", "", 0, "p", ""], ["mneme_store_pkey", "store_id", 1, false, "", "", 100, "x", ""]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_store ALTER COLUMN tail SET DEFAULT 0;
```

### C13 — record.envelope storage PLAIN

Public mode: `large`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record ALTER COLUMN envelope SET STORAGE PLAIN;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    0,
    0,
    0
  ],
  "later": {
    "created": true,
    "failed_at": "commit",
    "error": {
      "exception": "ProgramLimitExceeded",
      "sqlstate": "54000",
      "code": null,
      "argument": null,
      "detail": "row is too big: size 20248, maximum size 8160"
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"attributes": [["mneme_operation", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_operation", "mutation", 4, false, "", "", 0, "x", ""], ["mneme_operation", "first_position", 5, false, "", "", 0, "p", ""], ["mneme_operation", "last_position", 6, false, "", "", 0, "p", ""], ["mneme_operation", "recorded_at", 7, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_record", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record", "position", 2, false, "", "", 0, "p", ""], ["mneme_record", "record_id", 3, false, "", "", 100, "x", ""], ["mneme_record", "profile", 4, false, "", "", 100, "x", ""], ["mneme_record", "record_type", 5, false, "", "", 100, "x", ""], ["mneme_record", "schema_version", 6, false, "", "", 0, "p", ""], ["mneme_record", "envelope", 7, false, "", "", 0, "p", ""], ["mneme_record_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_pkey", "position", 2, false, "", "", 0, "p", ""], ["mneme_record_store_id_record_id_key", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_store_id_record_id_key", "record_id", 2, false, "", "", 100, "x", ""], ["mneme_schema", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_schema", "version", 2, false, "", "", 0, "p", ""], ["mneme_schema_pkey", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_store", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_store", "........pg.dropped.2........", 2, true, "", "", 0, "p", ""], ["mneme_store", "........pg.dropped.3........", 3, true, "", "", 0, "p", ""], ["mneme_store", "tail", 4, false, "", "", 0, "p", ""], ["mneme_store_pkey", "store_id", 1, false, "", "", 100, "x", ""]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_record ALTER COLUMN envelope SET STORAGE EXTENDED;
```

### C14 — record.envelope storage EXTERNAL

Public mode: `large`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record ALTER COLUMN envelope SET STORAGE EXTERNAL;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"attributes": [["mneme_operation", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_operation", "mutation", 4, false, "", "", 0, "x", ""], ["mneme_operation", "first_position", 5, false, "", "", 0, "p", ""], ["mneme_operation", "last_position", 6, false, "", "", 0, "p", ""], ["mneme_operation", "recorded_at", 7, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_record", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record", "position", 2, false, "", "", 0, "p", ""], ["mneme_record", "record_id", 3, false, "", "", 100, "x", ""], ["mneme_record", "profile", 4, false, "", "", 100, "x", ""], ["mneme_record", "record_type", 5, false, "", "", 100, "x", ""], ["mneme_record", "schema_version", 6, false, "", "", 0, "p", ""], ["mneme_record", "envelope", 7, false, "", "", 0, "e", ""], ["mneme_record_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_pkey", "position", 2, false, "", "", 0, "p", ""], ["mneme_record_store_id_record_id_key", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_store_id_record_id_key", "record_id", 2, false, "", "", 100, "x", ""], ["mneme_schema", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_schema", "version", 2, false, "", "", 0, "p", ""], ["mneme_schema_pkey", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_store", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_store", "........pg.dropped.2........", 2, true, "", "", 0, "p", ""], ["mneme_store", "........pg.dropped.3........", 3, true, "", "", 0, "p", ""], ["mneme_store", "tail", 4, false, "", "", 0, "p", ""], ["mneme_store_pkey", "store_id", 1, false, "", "", 100, "x", ""]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_record ALTER COLUMN envelope SET STORAGE EXTENDED;
```

### C15 — record.envelope storage MAIN

Public mode: `large`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record ALTER COLUMN envelope SET STORAGE MAIN;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"attributes": [["mneme_operation", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_operation", "mutation", 4, false, "", "", 0, "x", ""], ["mneme_operation", "first_position", 5, false, "", "", 0, "p", ""], ["mneme_operation", "last_position", 6, false, "", "", 0, "p", ""], ["mneme_operation", "recorded_at", 7, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_record", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record", "position", 2, false, "", "", 0, "p", ""], ["mneme_record", "record_id", 3, false, "", "", 100, "x", ""], ["mneme_record", "profile", 4, false, "", "", 100, "x", ""], ["mneme_record", "record_type", 5, false, "", "", 100, "x", ""], ["mneme_record", "schema_version", 6, false, "", "", 0, "p", ""], ["mneme_record", "envelope", 7, false, "", "", 0, "m", ""], ["mneme_record_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_pkey", "position", 2, false, "", "", 0, "p", ""], ["mneme_record_store_id_record_id_key", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_store_id_record_id_key", "record_id", 2, false, "", "", 100, "x", ""], ["mneme_schema", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_schema", "version", 2, false, "", "", 0, "p", ""], ["mneme_schema_pkey", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_store", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_store", "........pg.dropped.2........", 2, true, "", "", 0, "p", ""], ["mneme_store", "........pg.dropped.3........", 3, true, "", "", 0, "p", ""], ["mneme_store", "tail", 4, false, "", "", 0, "p", ""], ["mneme_store_pkey", "store_id", 1, false, "", "", 100, "x", ""]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_record ALTER COLUMN envelope SET STORAGE EXTENDED;
```

### C16 — record.envelope storage EXTENDED

Public mode: `large`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record ALTER COLUMN envelope SET STORAGE EXTENDED;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"attributes": [["mneme_operation", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_operation", "mutation", 4, false, "", "", 0, "x", ""], ["mneme_operation", "first_position", 5, false, "", "", 0, "p", ""], ["mneme_operation", "last_position", 6, false, "", "", 0, "p", ""], ["mneme_operation", "recorded_at", 7, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_record", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record", "position", 2, false, "", "", 0, "p", ""], ["mneme_record", "record_id", 3, false, "", "", 100, "x", ""], ["mneme_record", "profile", 4, false, "", "", 100, "x", ""], ["mneme_record", "record_type", 5, false, "", "", 100, "x", ""], ["mneme_record", "schema_version", 6, false, "", "", 0, "p", ""], ["mneme_record", "envelope", 7, false, "", "", 0, "x", ""], ["mneme_record_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_pkey", "position", 2, false, "", "", 0, "p", ""], ["mneme_record_store_id_record_id_key", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_store_id_record_id_key", "record_id", 2, false, "", "", 100, "x", ""], ["mneme_schema", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_schema", "version", 2, false, "", "", 0, "p", ""], ["mneme_schema_pkey", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_store", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_store", "........pg.dropped.2........", 2, true, "", "", 0, "p", ""], ["mneme_store", "........pg.dropped.3........", 3, true, "", "", 0, "p", ""], ["mneme_store", "tail", 4, false, "", "", 0, "p", ""], ["mneme_store_pkey", "store_id", 1, false, "", "", 100, "x", ""]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_record ALTER COLUMN envelope SET STORAGE EXTENDED;
```

### C17 — record.envelope compression pglz

Public mode: `large`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record ALTER COLUMN envelope SET COMPRESSION pglz;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"attributes": [["mneme_operation", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_operation", "mutation", 4, false, "", "", 0, "x", ""], ["mneme_operation", "first_position", 5, false, "", "", 0, "p", ""], ["mneme_operation", "last_position", 6, false, "", "", 0, "p", ""], ["mneme_operation", "recorded_at", 7, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_record", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record", "position", 2, false, "", "", 0, "p", ""], ["mneme_record", "record_id", 3, false, "", "", 100, "x", ""], ["mneme_record", "profile", 4, false, "", "", 100, "x", ""], ["mneme_record", "record_type", 5, false, "", "", 100, "x", ""], ["mneme_record", "schema_version", 6, false, "", "", 0, "p", ""], ["mneme_record", "envelope", 7, false, "", "", 0, "x", "p"], ["mneme_record_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_pkey", "position", 2, false, "", "", 0, "p", ""], ["mneme_record_store_id_record_id_key", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_store_id_record_id_key", "record_id", 2, false, "", "", 100, "x", ""], ["mneme_schema", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_schema", "version", 2, false, "", "", 0, "p", ""], ["mneme_schema_pkey", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_store", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_store", "........pg.dropped.2........", 2, true, "", "", 0, "p", ""], ["mneme_store", "........pg.dropped.3........", 3, true, "", "", 0, "p", ""], ["mneme_store", "tail", 4, false, "", "", 0, "p", ""], ["mneme_store_pkey", "store_id", 1, false, "", "", 100, "x", ""]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_record ALTER COLUMN envelope SET COMPRESSION default;
```

### C18 — record.envelope compression lz4

Public mode: `large`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record ALTER COLUMN envelope SET COMPRESSION lz4;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"attributes": [["mneme_operation", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_operation", "mutation", 4, false, "", "", 0, "x", ""], ["mneme_operation", "first_position", 5, false, "", "", 0, "p", ""], ["mneme_operation", "last_position", 6, false, "", "", 0, "p", ""], ["mneme_operation", "recorded_at", 7, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_record", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record", "position", 2, false, "", "", 0, "p", ""], ["mneme_record", "record_id", 3, false, "", "", 100, "x", ""], ["mneme_record", "profile", 4, false, "", "", 100, "x", ""], ["mneme_record", "record_type", 5, false, "", "", 100, "x", ""], ["mneme_record", "schema_version", 6, false, "", "", 0, "p", ""], ["mneme_record", "envelope", 7, false, "", "", 0, "x", "l"], ["mneme_record_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_pkey", "position", 2, false, "", "", 0, "p", ""], ["mneme_record_store_id_record_id_key", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_store_id_record_id_key", "record_id", 2, false, "", "", 100, "x", ""], ["mneme_schema", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_schema", "version", 2, false, "", "", 0, "p", ""], ["mneme_schema_pkey", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_store", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_store", "........pg.dropped.2........", 2, true, "", "", 0, "p", ""], ["mneme_store", "........pg.dropped.3........", 3, true, "", "", 0, "p", ""], ["mneme_store", "tail", 4, false, "", "", 0, "p", ""], ["mneme_store_pkey", "store_id", 1, false, "", "", 100, "x", ""]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_record ALTER COLUMN envelope SET COMPRESSION default;
```

### C19 — record.schema_version domain instead of bigint

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
CREATE DOMAIN probe_domain AS bigint CHECK(VALUE=1);
ALTER TABLE mneme_record ALTER COLUMN schema_version TYPE probe_domain;
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables ['mneme_operation', 'mneme_record', 'mneme_schema', 'mneme_store'] are not schema version 1"
  },
  "physical": [
    0,
    0,
    null
  ],
  "fingerprints": {
    "columns_match": false,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"attributes": [["mneme_operation", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_operation", "mutation", 4, false, "", "", 0, "x", ""], ["mneme_operation", "first_position", 5, false, "", "", 0, "p", ""], ["mneme_operation", "last_position", 6, false, "", "", 0, "p", ""], ["mneme_operation", "recorded_at", 7, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_record", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record", "position", 2, false, "", "", 0, "p", ""], ["mneme_record", "record_id", 3, false, "", "", 100, "x", ""], ["mneme_record", "profile", 4, false, "", "", 100, "x", ""], ["mneme_record", "record_type", 5, false, "", "", 100, "x", ""], ["mneme_record", "schema_version", 6, false, "", "", 0, "p", ""], ["mneme_record", "envelope", 7, false, "", "", 0, "x", ""], ["mneme_record_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_pkey", "position", 2, false, "", "", 0, "p", ""], ["mneme_record_store_id_record_id_key", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_store_id_record_id_key", "record_id", 2, false, "", "", 100, "x", ""], ["mneme_schema", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_schema", "version", 2, false, "", "", 0, "p", ""], ["mneme_schema_pkey", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_store", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_store", "........pg.dropped.2........", 2, true, "", "", 0, "p", ""], ["mneme_store", "........pg.dropped.3........", 3, true, "", "", 0, "p", ""], ["mneme_store", "tail", 4, false, "", "", 0, "p", ""], ["mneme_store_pkey", "store_id", 1, false, "", "", 100, "x", ""]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_record ALTER COLUMN schema_version TYPE bigint;
DROP DOMAIN probe_domain;
```

### C20 — dropped-column residue

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record ADD COLUMN probe_dead text;
ALTER TABLE mneme_record DROP COLUMN probe_dead;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"attributes": [["mneme_operation", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_operation", "mutation", 4, false, "", "", 0, "x", ""], ["mneme_operation", "first_position", 5, false, "", "", 0, "p", ""], ["mneme_operation", "last_position", 6, false, "", "", 0, "p", ""], ["mneme_operation", "recorded_at", 7, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_record", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record", "position", 2, false, "", "", 0, "p", ""], ["mneme_record", "record_id", 3, false, "", "", 100, "x", ""], ["mneme_record", "profile", 4, false, "", "", 100, "x", ""], ["mneme_record", "record_type", 5, false, "", "", 100, "x", ""], ["mneme_record", "schema_version", 6, false, "", "", 0, "p", ""], ["mneme_record", "envelope", 7, false, "", "", 0, "x", ""], ["mneme_record", "........pg.dropped.8........", 8, true, "", "", 100, "x", ""], ["mneme_record_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_pkey", "position", 2, false, "", "", 0, "p", ""], ["mneme_record_store_id_record_id_key", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_store_id_record_id_key", "record_id", 2, false, "", "", 100, "x", ""], ["mneme_schema", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_schema", "version", 2, false, "", "", 0, "p", ""], ["mneme_schema_pkey", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_store", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_store", "........pg.dropped.2........", 2, true, "", "", 0, "p", ""], ["mneme_store", "........pg.dropped.3........", 3, true, "", "", 0, "p", ""], ["mneme_store", "tail", 4, false, "", "", 0, "p", ""], ["mneme_store_pkey", "store_id", 1, false, "", "", 100, "x", ""]]}
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

### C21 — column statistics target

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record ALTER COLUMN envelope SET STATISTICS 0;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"attributes": [["mneme_operation", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_operation", "mutation", 4, false, "", "", 0, "x", ""], ["mneme_operation", "first_position", 5, false, "", "", 0, "p", ""], ["mneme_operation", "last_position", 6, false, "", "", 0, "p", ""], ["mneme_operation", "recorded_at", 7, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_record", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record", "position", 2, false, "", "", 0, "p", ""], ["mneme_record", "record_id", 3, false, "", "", 100, "x", ""], ["mneme_record", "profile", 4, false, "", "", 100, "x", ""], ["mneme_record", "record_type", 5, false, "", "", 100, "x", ""], ["mneme_record", "schema_version", 6, false, "", "", 0, "p", ""], ["mneme_record", "envelope", 7, false, "", "", 0, "x", ""], ["mneme_record", "........pg.dropped.8........", 8, true, "", "", 100, "x", ""], ["mneme_record_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_pkey", "position", 2, false, "", "", 0, "p", ""], ["mneme_record_store_id_record_id_key", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_store_id_record_id_key", "record_id", 2, false, "", "", 100, "x", ""], ["mneme_schema", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_schema", "version", 2, false, "", "", 0, "p", ""], ["mneme_schema_pkey", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_store", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_store", "........pg.dropped.2........", 2, true, "", "", 0, "p", ""], ["mneme_store", "........pg.dropped.3........", 3, true, "", "", 0, "p", ""], ["mneme_store", "tail", 4, false, "", "", 0, "p", ""], ["mneme_store_pkey", "store_id", 1, false, "", "", 100, "x", ""]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_record ALTER COLUMN envelope SET STATISTICS -1;
```

### C22 — same live record columns in different order

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record DROP COLUMN schema_version;
ALTER TABLE mneme_record ADD COLUMN schema_version bigint NOT NULL;
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables ['mneme_operation', 'mneme_record', 'mneme_schema', 'mneme_store'] are not schema version 1"
  },
  "physical": [
    0,
    0,
    null
  ],
  "fingerprints": {
    "columns_match": false,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"attributes": [["mneme_operation", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_operation", "mutation", 4, false, "", "", 0, "x", ""], ["mneme_operation", "first_position", 5, false, "", "", 0, "p", ""], ["mneme_operation", "last_position", 6, false, "", "", 0, "p", ""], ["mneme_operation", "recorded_at", 7, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_record", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record", "position", 2, false, "", "", 0, "p", ""], ["mneme_record", "record_id", 3, false, "", "", 100, "x", ""], ["mneme_record", "profile", 4, false, "", "", 100, "x", ""], ["mneme_record", "record_type", 5, false, "", "", 100, "x", ""], ["mneme_record", "........pg.dropped.6........", 6, true, "", "", 0, "p", ""], ["mneme_record", "envelope", 7, false, "", "", 0, "x", ""], ["mneme_record", "........pg.dropped.8........", 8, true, "", "", 100, "x", ""], ["mneme_record", "schema_version", 9, false, "", "", 0, "p", ""], ["mneme_record_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_pkey", "position", 2, false, "", "", 0, "p", ""], ["mneme_record_store_id_record_id_key", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_store_id_record_id_key", "record_id", 2, false, "", "", 100, "x", ""], ["mneme_schema", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_schema", "version", 2, false, "", "", 0, "p", ""], ["mneme_schema_pkey", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_store", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_store", "........pg.dropped.2........", 2, true, "", "", 0, "p", ""], ["mneme_store", "........pg.dropped.3........", 3, true, "", "", 0, "p", ""], ["mneme_store", "tail", 4, false, "", "", 0, "p", ""], ["mneme_store_pkey", "store_id", 1, false, "", "", 100, "x", ""]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_record DROP COLUMN envelope;
ALTER TABLE mneme_record ADD COLUMN envelope bytea NOT NULL;
```

### C23 — deterministic ICU collation, shifted punctuation

Public mode: `collide`; connection options: ``.

Executed setup:

```sql
CREATE COLLATION probe_deterministic (provider=icu,locale='und-u-ka-shifted',deterministic=true);
ALTER TABLE mneme_store ALTER COLUMN store_id TYPE text COLLATE probe_deterministic;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "later": {
    "created": true,
    "distinct_ids": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"attributes": [["mneme_operation", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_operation", "mutation", 4, false, "", "", 0, "x", ""], ["mneme_operation", "first_position", 5, false, "", "", 0, "p", ""], ["mneme_operation", "last_position", 6, false, "", "", 0, "p", ""], ["mneme_operation", "recorded_at", 7, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_record", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record", "position", 2, false, "", "", 0, "p", ""], ["mneme_record", "record_id", 3, false, "", "", 100, "x", ""], ["mneme_record", "profile", 4, false, "", "", 100, "x", ""], ["mneme_record", "record_type", 5, false, "", "", 100, "x", ""], ["mneme_record", "........pg.dropped.6........", 6, true, "", "", 0, "p", ""], ["mneme_record", "........pg.dropped.7........", 7, true, "", "", 0, "x", ""], ["mneme_record", "........pg.dropped.8........", 8, true, "", "", 100, "x", ""], ["mneme_record", "schema_version", 9, false, "", "", 0, "p", ""], ["mneme_record", "envelope", 10, false, "", "", 0, "x", ""], ["mneme_record_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_pkey", "position", 2, false, "", "", 0, "p", ""], ["mneme_record_store_id_record_id_key", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_store_id_record_id_key", "record_id", 2, false, "", "", 100, "x", ""], ["mneme_schema", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_schema", "version", 2, false, "", "", 0, "p", ""], ["mneme_schema_pkey", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_store", "store_id", 1, false, "", "", 34056, "x", ""], ["mneme_store", "........pg.dropped.2........", 2, true, "", "", 0, "p", ""], ["mneme_store", "........pg.dropped.3........", 3, true, "", "", 0, "p", ""], ["mneme_store", "tail", 4, false, "", "", 0, "p", ""], ["mneme_store_pkey", "store_id", 1, false, "", "", 34056, "x", ""]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_store ALTER COLUMN store_id TYPE text COLLATE "default";
DROP COLLATION probe_deterministic;
```

### C24 — store.tail generated constant with original default spelling

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_store DROP COLUMN tail;
ALTER TABLE mneme_store ADD COLUMN tail bigint GENERATED ALWAYS AS (0) STORED NOT NULL CHECK(tail BETWEEN 0 AND 9007199254740991);
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    0,
    0,
    0
  ],
  "later": {
    "created": true,
    "failed_at": "commit",
    "error": {
      "exception": "GeneratedAlways",
      "sqlstate": "428C9",
      "code": null,
      "argument": null,
      "detail": "column \"tail\" can only be updated to DEFAULT\nDETAIL:  Column \"tail\" is a generated column."
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"attributes": [["mneme_operation", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_operation", "mutation", 4, false, "", "", 0, "x", ""], ["mneme_operation", "first_position", 5, false, "", "", 0, "p", ""], ["mneme_operation", "last_position", 6, false, "", "", 0, "p", ""], ["mneme_operation", "recorded_at", 7, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_record", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record", "position", 2, false, "", "", 0, "p", ""], ["mneme_record", "record_id", 3, false, "", "", 100, "x", ""], ["mneme_record", "profile", 4, false, "", "", 100, "x", ""], ["mneme_record", "record_type", 5, false, "", "", 100, "x", ""], ["mneme_record", "........pg.dropped.6........", 6, true, "", "", 0, "p", ""], ["mneme_record", "........pg.dropped.7........", 7, true, "", "", 0, "x", ""], ["mneme_record", "........pg.dropped.8........", 8, true, "", "", 100, "x", ""], ["mneme_record", "schema_version", 9, false, "", "", 0, "p", ""], ["mneme_record", "envelope", 10, false, "", "", 0, "x", ""], ["mneme_record_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_pkey", "position", 2, false, "", "", 0, "p", ""], ["mneme_record_store_id_record_id_key", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_store_id_record_id_key", "record_id", 2, false, "", "", 100, "x", ""], ["mneme_schema", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_schema", "version", 2, false, "", "", 0, "p", ""], ["mneme_schema_pkey", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_store", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_store", "........pg.dropped.2........", 2, true, "", "", 0, "p", ""], ["mneme_store", "........pg.dropped.3........", 3, true, "", "", 0, "p", ""], ["mneme_store", "........pg.dropped.4........", 4, true, "", "", 0, "p", ""], ["mneme_store", "tail", 5, false, "", "s", 0, "p", ""], ["mneme_store_pkey", "store_id", 1, false, "", "", 100, "x", ""]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_store DROP COLUMN tail;
ALTER TABLE mneme_store ADD COLUMN tail bigint NOT NULL DEFAULT 0 CHECK(tail BETWEEN 0 AND 9007199254740991);
```

### C25 — tail name changed

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_store RENAME COLUMN tail TO probe_tail;
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables ['mneme_operation', 'mneme_record', 'mneme_schema', 'mneme_store'] are not schema version 1"
  },
  "physical_error": {
    "exception": "UndefinedColumn",
    "sqlstate": "42703",
    "code": null,
    "argument": null,
    "detail": "column \"tail\" does not exist\nLINE 1: ...SELECT count(*) FROM mneme_operation),(SELECT max(tail) FROM...\n                                                             ^"
  },
  "clock_contexts": [],
  "fingerprints": {
    "columns_match": false,
    "constraints_match": false
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"attributes": [["mneme_operation", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_operation", "mutation", 4, false, "", "", 0, "x", ""], ["mneme_operation", "first_position", 5, false, "", "", 0, "p", ""], ["mneme_operation", "last_position", 6, false, "", "", 0, "p", ""], ["mneme_operation", "recorded_at", 7, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_record", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record", "position", 2, false, "", "", 0, "p", ""], ["mneme_record", "record_id", 3, false, "", "", 100, "x", ""], ["mneme_record", "profile", 4, false, "", "", 100, "x", ""], ["mneme_record", "record_type", 5, false, "", "", 100, "x", ""], ["mneme_record", "........pg.dropped.6........", 6, true, "", "", 0, "p", ""], ["mneme_record", "........pg.dropped.7........", 7, true, "", "", 0, "x", ""], ["mneme_record", "........pg.dropped.8........", 8, true, "", "", 100, "x", ""], ["mneme_record", "schema_version", 9, false, "", "", 0, "p", ""], ["mneme_record", "envelope", 10, false, "", "", 0, "x", ""], ["mneme_record_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_pkey", "position", 2, false, "", "", 0, "p", ""], ["mneme_record_store_id_record_id_key", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_store_id_record_id_key", "record_id", 2, false, "", "", 100, "x", ""], ["mneme_schema", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_schema", "version", 2, false, "", "", 0, "p", ""], ["mneme_schema_pkey", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_store", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_store", "........pg.dropped.2........", 2, true, "", "", 0, "p", ""], ["mneme_store", "........pg.dropped.3........", 3, true, "", "", 0, "p", ""], ["mneme_store", "........pg.dropped.4........", 4, true, "", "", 0, "p", ""], ["mneme_store", "........pg.dropped.5........", 5, true, "", "", 0, "p", ""], ["mneme_store", "probe_tail", 6, false, "", "", 0, "p", ""], ["mneme_store_pkey", "store_id", 1, false, "", "", 100, "x", ""]]}
{"collations": [["default", "d", true, "", "", null, null]]}
{"column_extra": [["mneme_operation", "store_id", false, null, 0, null, null], ["mneme_operation", "source_namespace", false, null, 0, null, null], ["mneme_operation", "source_operation_id", false, null, 0, null, null], ["mneme_operation", "mutation", false, null, 0, null, null], ["mneme_operation", "first_position", false, null, 0, null, null], ["mneme_operation", "last_position", false, null, 0, null, null], ["mneme_operation", "recorded_at", false, null, 0, null, null], ["mneme_operation_pkey", "store_id", false, null, 0, null, null], ["mneme_operation_pkey", "source_namespace", false, null, 0, null, null], ["mneme_operation_pkey", "source_operation_id", false, null, 0, null, null], ["mneme_record", "store_id", false, null, 0, null, null], ["mneme_record", "position", false, null, 0, null, null], ["mneme_record", "record_id", false, null, 0, null, null], ["mneme_record", "profile", false, null, 0, null, null], ["mneme_record", "record_type", false, null, 0, null, null], ["mneme_record", "........pg.dropped.6........", false, null, 0, null, null], ["mneme_record", "........pg.dropped.7........", false, null, 0, null, null], ["mneme_record", "........pg.dropped.8........", false, null, 0, null, null], ["mneme_record", "schema_version", false, null, 0, null, null], ["mneme_record", "envelope", false, null, 0, null, null], ["mneme_record_pkey", "store_id", false, null, 0, null, null], ["mneme_record_pkey", "position", false, null, 0, null, null], ["mneme_record_store_id_record_id_key", "store_id", false, null, 0, null, null], ["mneme_record_store_id_record_id_key", "record_id", false, null, 0, null, null], ["mneme_schema", "singleton", false, null, 0, null, null], ["mneme_schema", "version", false, null, 0, null, null], ["mneme_schema_pkey", "singleton", false, null, 0, null, null], ["mneme_store", "store_id", false, null, 0, null, null], ["mneme_store", "........pg.dropped.2........", false, null, 0, null, null], ["mneme_store", "........pg.dropped.3........", false, null, 0, null, null], ["mneme_store", "........pg.dropped.4........", false, null, 0, null, null], ["mneme_store", "........pg.dropped.5........", false, null, 0, null, null], ["mneme_store", "probe_tail", false, null, 0, null, null], ["mneme_store_pkey", "store_id", false, null, 0, null, null]]}
{"column_types": [["mneme_operation", "store_id", 25, "text"], ["mneme_operation", "source_namespace", 25, "text"], ["mneme_operation", "source_operation_id", 17, "bytea"], ["mneme_operation", "mutation", 17, "bytea"], ["mneme_operation", "first_position", 20, "bigint"], ["mneme_operation", "last_position", 20, "bigint"], ["mneme_operation", "recorded_at", 25, "text"], ["mneme_operation_pkey", "store_id", 25, "text"], ["mneme_operation_pkey", "source_namespace", 25, "text"], ["mneme_operation_pkey", "source_operation_id", 17, "bytea"], ["mneme_record", "store_id", 25, "text"], ["mneme_record", "position", 20, "bigint"], ["mneme_record", "record_id", 25, "text"], ["mneme_record", "profile", 25, "text"], ["mneme_record", "record_type", 25, "text"], ["mneme_record", "schema_version", 20, "bigint"], ["mneme_record", "envelope", 17, "bytea"], ["mneme_record_pkey", "store_id", 25, "text"], ["mneme_record_pkey", "position", 20, "bigint"], ["mneme_record_store_id_record_id_key", "store_id", 25, "text"], ["mneme_record_store_id_record_id_key", "record_id", 25, "text"], ["mneme_schema", "singleton", 16, "boolean"], ["mneme_schema", "version", 23, "integer"], ["mneme_schema_pkey", "singleton", 16, "boolean"], ["mneme_store", "store_id", 25, "text"], ["mneme_store", "probe_tail", 20, "bigint"], ["mneme_store_pkey", "store_id", 25, "text"]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_store RENAME COLUMN probe_tail TO tail;
```

### C26 — version name changed

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_schema RENAME COLUMN version TO probe_version;
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables ['mneme_operation', 'mneme_record', 'mneme_schema', 'mneme_store'] are not schema version 1"
  },
  "physical": [
    0,
    0,
    null
  ],
  "clock_contexts": [],
  "fingerprints": {
    "columns_match": false,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"attributes": [["mneme_operation", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_operation", "mutation", 4, false, "", "", 0, "x", ""], ["mneme_operation", "first_position", 5, false, "", "", 0, "p", ""], ["mneme_operation", "last_position", 6, false, "", "", 0, "p", ""], ["mneme_operation", "recorded_at", 7, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_record", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record", "position", 2, false, "", "", 0, "p", ""], ["mneme_record", "record_id", 3, false, "", "", 100, "x", ""], ["mneme_record", "profile", 4, false, "", "", 100, "x", ""], ["mneme_record", "record_type", 5, false, "", "", 100, "x", ""], ["mneme_record", "........pg.dropped.6........", 6, true, "", "", 0, "p", ""], ["mneme_record", "........pg.dropped.7........", 7, true, "", "", 0, "x", ""], ["mneme_record", "........pg.dropped.8........", 8, true, "", "", 100, "x", ""], ["mneme_record", "schema_version", 9, false, "", "", 0, "p", ""], ["mneme_record", "envelope", 10, false, "", "", 0, "x", ""], ["mneme_record_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_pkey", "position", 2, false, "", "", 0, "p", ""], ["mneme_record_store_id_record_id_key", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_store_id_record_id_key", "record_id", 2, false, "", "", 100, "x", ""], ["mneme_schema", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_schema", "probe_version", 2, false, "", "", 0, "p", ""], ["mneme_schema_pkey", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_store", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_store", "........pg.dropped.2........", 2, true, "", "", 0, "p", ""], ["mneme_store", "........pg.dropped.3........", 3, true, "", "", 0, "p", ""], ["mneme_store", "........pg.dropped.4........", 4, true, "", "", 0, "p", ""], ["mneme_store", "........pg.dropped.5........", 5, true, "", "", 0, "p", ""], ["mneme_store", "tail", 6, false, "", "", 0, "p", ""], ["mneme_store_pkey", "store_id", 1, false, "", "", 100, "x", ""]]}
{"collations": [["default", "d", true, "", "", null, null]]}
{"column_extra": [["mneme_operation", "store_id", false, null, 0, null, null], ["mneme_operation", "source_namespace", false, null, 0, null, null], ["mneme_operation", "source_operation_id", false, null, 0, null, null], ["mneme_operation", "mutation", false, null, 0, null, null], ["mneme_operation", "first_position", false, null, 0, null, null], ["mneme_operation", "last_position", false, null, 0, null, null], ["mneme_operation", "recorded_at", false, null, 0, null, null], ["mneme_operation_pkey", "store_id", false, null, 0, null, null], ["mneme_operation_pkey", "source_namespace", false, null, 0, null, null], ["mneme_operation_pkey", "source_operation_id", false, null, 0, null, null], ["mneme_record", "store_id", false, null, 0, null, null], ["mneme_record", "position", false, null, 0, null, null], ["mneme_record", "record_id", false, null, 0, null, null], ["mneme_record", "profile", false, null, 0, null, null], ["mneme_record", "record_type", false, null, 0, null, null], ["mneme_record", "........pg.dropped.6........", false, null, 0, null, null], ["mneme_record", "........pg.dropped.7........", false, null, 0, null, null], ["mneme_record", "........pg.dropped.8........", false, null, 0, null, null], ["mneme_record", "schema_version", false, null, 0, null, null], ["mneme_record", "envelope", false, null, 0, null, null], ["mneme_record_pkey", "store_id", false, null, 0, null, null], ["mneme_record_pkey", "position", false, null, 0, null, null], ["mneme_record_store_id_record_id_key", "store_id", false, null, 0, null, null], ["mneme_record_store_id_record_id_key", "record_id", false, null, 0, null, null], ["mneme_schema", "singleton", false, null, 0, null, null], ["mneme_schema", "probe_version", false, null, 0, null, null], ["mneme_schema_pkey", "singleton", false, null, 0, null, null], ["mneme_store", "store_id", false, null, 0, null, null], ["mneme_store", "........pg.dropped.2........", false, null, 0, null, null], ["mneme_store", "........pg.dropped.3........", false, null, 0, null, null], ["mneme_store", "........pg.dropped.4........", false, null, 0, null, null], ["mneme_store", "........pg.dropped.5........", false, null, 0, null, null], ["mneme_store", "tail", false, null, 0, null, null], ["mneme_store_pkey", "store_id", false, null, 0, null, null]]}
{"column_types": [["mneme_operation", "store_id", 25, "text"], ["mneme_operation", "source_namespace", 25, "text"], ["mneme_operation", "source_operation_id", 17, "bytea"], ["mneme_operation", "mutation", 17, "bytea"], ["mneme_operation", "first_position", 20, "bigint"], ["mneme_operation", "last_position", 20, "bigint"], ["mneme_operation", "recorded_at", 25, "text"], ["mneme_operation_pkey", "store_id", 25, "text"], ["mneme_operation_pkey", "source_namespace", 25, "text"], ["mneme_operation_pkey", "source_operation_id", 17, "bytea"], ["mneme_record", "store_id", 25, "text"], ["mneme_record", "position", 20, "bigint"], ["mneme_record", "record_id", 25, "text"], ["mneme_record", "profile", 25, "text"], ["mneme_record", "record_type", 25, "text"], ["mneme_record", "schema_version", 20, "bigint"], ["mneme_record", "envelope", 17, "bytea"], ["mneme_record_pkey", "store_id", 25, "text"], ["mneme_record_pkey", "position", 20, "bigint"], ["mneme_record_store_id_record_id_key", "store_id", 25, "text"], ["mneme_record_store_id_record_id_key", "record_id", 25, "text"], ["mneme_schema", "singleton", 16, "boolean"], ["mneme_schema", "probe_version", 23, "integer"], ["mneme_schema_pkey", "singleton", 16, "boolean"], ["mneme_store", "store_id", 25, "text"], ["mneme_store", "tail", 20, "bigint"], ["mneme_store_pkey", "store_id", 25, "text"]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_schema RENAME COLUMN probe_version TO version;
```

### C27 — tail narrowed to integer

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_store ALTER COLUMN tail TYPE integer;
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables ['mneme_operation', 'mneme_record', 'mneme_schema', 'mneme_store'] are not schema version 1"
  },
  "physical": [
    0,
    0,
    null
  ],
  "clock_contexts": [],
  "fingerprints": {
    "columns_match": false,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"attributes": [["mneme_operation", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_operation", "mutation", 4, false, "", "", 0, "x", ""], ["mneme_operation", "first_position", 5, false, "", "", 0, "p", ""], ["mneme_operation", "last_position", 6, false, "", "", 0, "p", ""], ["mneme_operation", "recorded_at", 7, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_record", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record", "position", 2, false, "", "", 0, "p", ""], ["mneme_record", "record_id", 3, false, "", "", 100, "x", ""], ["mneme_record", "profile", 4, false, "", "", 100, "x", ""], ["mneme_record", "record_type", 5, false, "", "", 100, "x", ""], ["mneme_record", "........pg.dropped.6........", 6, true, "", "", 0, "p", ""], ["mneme_record", "........pg.dropped.7........", 7, true, "", "", 0, "x", ""], ["mneme_record", "........pg.dropped.8........", 8, true, "", "", 100, "x", ""], ["mneme_record", "schema_version", 9, false, "", "", 0, "p", ""], ["mneme_record", "envelope", 10, false, "", "", 0, "x", ""], ["mneme_record_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_pkey", "position", 2, false, "", "", 0, "p", ""], ["mneme_record_store_id_record_id_key", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_store_id_record_id_key", "record_id", 2, false, "", "", 100, "x", ""], ["mneme_schema", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_schema", "version", 2, false, "", "", 0, "p", ""], ["mneme_schema_pkey", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_store", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_store", "........pg.dropped.2........", 2, true, "", "", 0, "p", ""], ["mneme_store", "........pg.dropped.3........", 3, true, "", "", 0, "p", ""], ["mneme_store", "........pg.dropped.4........", 4, true, "", "", 0, "p", ""], ["mneme_store", "........pg.dropped.5........", 5, true, "", "", 0, "p", ""], ["mneme_store", "tail", 6, false, "", "", 0, "p", ""], ["mneme_store_pkey", "store_id", 1, false, "", "", 100, "x", ""]]}
{"collations": [["default", "d", true, "", "", null, null]]}
{"column_extra": [["mneme_operation", "store_id", false, null, 0, null, null], ["mneme_operation", "source_namespace", false, null, 0, null, null], ["mneme_operation", "source_operation_id", false, null, 0, null, null], ["mneme_operation", "mutation", false, null, 0, null, null], ["mneme_operation", "first_position", false, null, 0, null, null], ["mneme_operation", "last_position", false, null, 0, null, null], ["mneme_operation", "recorded_at", false, null, 0, null, null], ["mneme_operation_pkey", "store_id", false, null, 0, null, null], ["mneme_operation_pkey", "source_namespace", false, null, 0, null, null], ["mneme_operation_pkey", "source_operation_id", false, null, 0, null, null], ["mneme_record", "store_id", false, null, 0, null, null], ["mneme_record", "position", false, null, 0, null, null], ["mneme_record", "record_id", false, null, 0, null, null], ["mneme_record", "profile", false, null, 0, null, null], ["mneme_record", "record_type", false, null, 0, null, null], ["mneme_record", "........pg.dropped.6........", false, null, 0, null, null], ["mneme_record", "........pg.dropped.7........", false, null, 0, null, null], ["mneme_record", "........pg.dropped.8........", false, null, 0, null, null], ["mneme_record", "schema_version", false, null, 0, null, null], ["mneme_record", "envelope", false, null, 0, null, null], ["mneme_record_pkey", "store_id", false, null, 0, null, null], ["mneme_record_pkey", "position", false, null, 0, null, null], ["mneme_record_store_id_record_id_key", "store_id", false, null, 0, null, null], ["mneme_record_store_id_record_id_key", "record_id", false, null, 0, null, null], ["mneme_schema", "singleton", false, null, 0, null, null], ["mneme_schema", "version", false, null, 0, null, null], ["mneme_schema_pkey", "singleton", false, null, 0, null, null], ["mneme_store", "store_id", false, null, 0, null, null], ["mneme_store", "........pg.dropped.2........", false, null, 0, null, null], ["mneme_store", "........pg.dropped.3........", false, null, 0, null, null], ["mneme_store", "........pg.dropped.4........", false, null, 0, null, null], ["mneme_store", "........pg.dropped.5........", false, null, 0, null, null], ["mneme_store", "tail", false, null, 0, null, null], ["mneme_store_pkey", "store_id", false, null, 0, null, null]]}
{"column_types": [["mneme_operation", "store_id", 25, "text"], ["mneme_operation", "source_namespace", 25, "text"], ["mneme_operation", "source_operation_id", 17, "bytea"], ["mneme_operation", "mutation", 17, "bytea"], ["mneme_operation", "first_position", 20, "bigint"], ["mneme_operation", "last_position", 20, "bigint"], ["mneme_operation", "recorded_at", 25, "text"], ["mneme_operation_pkey", "store_id", 25, "text"], ["mneme_operation_pkey", "source_namespace", 25, "text"], ["mneme_operation_pkey", "source_operation_id", 17, "bytea"], ["mneme_record", "store_id", 25, "text"], ["mneme_record", "position", 20, "bigint"], ["mneme_record", "record_id", 25, "text"], ["mneme_record", "profile", 25, "text"], ["mneme_record", "record_type", 25, "text"], ["mneme_record", "schema_version", 20, "bigint"], ["mneme_record", "envelope", 17, "bytea"], ["mneme_record_pkey", "store_id", 25, "text"], ["mneme_record_pkey", "position", 20, "bigint"], ["mneme_record_store_id_record_id_key", "store_id", 25, "text"], ["mneme_record_store_id_record_id_key", "record_id", 25, "text"], ["mneme_schema", "singleton", 16, "boolean"], ["mneme_schema", "version", 23, "integer"], ["mneme_schema_pkey", "singleton", 16, "boolean"], ["mneme_store", "store_id", 25, "text"], ["mneme_store", "tail", 23, "integer"], ["mneme_store_pkey", "store_id", 25, "text"]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_store ALTER COLUMN tail TYPE bigint;
```

### C28 — record envelope nullable

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record ALTER COLUMN envelope DROP NOT NULL;
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables ['mneme_operation', 'mneme_record', 'mneme_schema', 'mneme_store'] are not schema version 1"
  },
  "physical": [
    0,
    0,
    null
  ],
  "clock_contexts": [],
  "fingerprints": {
    "columns_match": false,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"attributes": [["mneme_operation", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_operation", "mutation", 4, false, "", "", 0, "x", ""], ["mneme_operation", "first_position", 5, false, "", "", 0, "p", ""], ["mneme_operation", "last_position", 6, false, "", "", 0, "p", ""], ["mneme_operation", "recorded_at", 7, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_namespace", 2, false, "", "", 100, "x", ""], ["mneme_operation_pkey", "source_operation_id", 3, false, "", "", 0, "x", ""], ["mneme_record", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record", "position", 2, false, "", "", 0, "p", ""], ["mneme_record", "record_id", 3, false, "", "", 100, "x", ""], ["mneme_record", "profile", 4, false, "", "", 100, "x", ""], ["mneme_record", "record_type", 5, false, "", "", 100, "x", ""], ["mneme_record", "........pg.dropped.6........", 6, true, "", "", 0, "p", ""], ["mneme_record", "........pg.dropped.7........", 7, true, "", "", 0, "x", ""], ["mneme_record", "........pg.dropped.8........", 8, true, "", "", 100, "x", ""], ["mneme_record", "schema_version", 9, false, "", "", 0, "p", ""], ["mneme_record", "envelope", 10, false, "", "", 0, "x", ""], ["mneme_record_pkey", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_pkey", "position", 2, false, "", "", 0, "p", ""], ["mneme_record_store_id_record_id_key", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_record_store_id_record_id_key", "record_id", 2, false, "", "", 100, "x", ""], ["mneme_schema", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_schema", "version", 2, false, "", "", 0, "p", ""], ["mneme_schema_pkey", "singleton", 1, false, "", "", 0, "p", ""], ["mneme_store", "store_id", 1, false, "", "", 100, "x", ""], ["mneme_store", "........pg.dropped.2........", 2, true, "", "", 0, "p", ""], ["mneme_store", "........pg.dropped.3........", 3, true, "", "", 0, "p", ""], ["mneme_store", "........pg.dropped.4........", 4, true, "", "", 0, "p", ""], ["mneme_store", "........pg.dropped.5........", 5, true, "", "", 0, "p", ""], ["mneme_store", "tail", 6, false, "", "", 0, "p", ""], ["mneme_store_pkey", "store_id", 1, false, "", "", 100, "x", ""]]}
{"collations": [["default", "d", true, "", "", null, null]]}
{"column_extra": [["mneme_operation", "store_id", false, null, 0, null, null], ["mneme_operation", "source_namespace", false, null, 0, null, null], ["mneme_operation", "source_operation_id", false, null, 0, null, null], ["mneme_operation", "mutation", false, null, 0, null, null], ["mneme_operation", "first_position", false, null, 0, null, null], ["mneme_operation", "last_position", false, null, 0, null, null], ["mneme_operation", "recorded_at", false, null, 0, null, null], ["mneme_operation_pkey", "store_id", false, null, 0, null, null], ["mneme_operation_pkey", "source_namespace", false, null, 0, null, null], ["mneme_operation_pkey", "source_operation_id", false, null, 0, null, null], ["mneme_record", "store_id", false, null, 0, null, null], ["mneme_record", "position", false, null, 0, null, null], ["mneme_record", "record_id", false, null, 0, null, null], ["mneme_record", "profile", false, null, 0, null, null], ["mneme_record", "record_type", false, null, 0, null, null], ["mneme_record", "........pg.dropped.6........", false, null, 0, null, null], ["mneme_record", "........pg.dropped.7........", false, null, 0, null, null], ["mneme_record", "........pg.dropped.8........", false, null, 0, null, null], ["mneme_record", "schema_version", false, null, 0, null, null], ["mneme_record", "envelope", false, null, 0, null, null], ["mneme_record_pkey", "store_id", false, null, 0, null, null], ["mneme_record_pkey", "position", false, null, 0, null, null], ["mneme_record_store_id_record_id_key", "store_id", false, null, 0, null, null], ["mneme_record_store_id_record_id_key", "record_id", false, null, 0, null, null], ["mneme_schema", "singleton", false, null, 0, null, null], ["mneme_schema", "version", false, null, 0, null, null], ["mneme_schema_pkey", "singleton", false, null, 0, null, null], ["mneme_store", "store_id", false, null, 0, null, null], ["mneme_store", "........pg.dropped.2........", false, null, 0, null, null], ["mneme_store", "........pg.dropped.3........", false, null, 0, null, null], ["mneme_store", "........pg.dropped.4........", false, null, 0, null, null], ["mneme_store", "........pg.dropped.5........", false, null, 0, null, null], ["mneme_store", "tail", false, null, 0, null, null], ["mneme_store_pkey", "store_id", false, null, 0, null, null]]}
{"column_types": [["mneme_operation", "store_id", 25, "text"], ["mneme_operation", "source_namespace", 25, "text"], ["mneme_operation", "source_operation_id", 17, "bytea"], ["mneme_operation", "mutation", 17, "bytea"], ["mneme_operation", "first_position", 20, "bigint"], ["mneme_operation", "last_position", 20, "bigint"], ["mneme_operation", "recorded_at", 25, "text"], ["mneme_operation_pkey", "store_id", 25, "text"], ["mneme_operation_pkey", "source_namespace", 25, "text"], ["mneme_operation_pkey", "source_operation_id", 17, "bytea"], ["mneme_record", "store_id", 25, "text"], ["mneme_record", "position", 20, "bigint"], ["mneme_record", "record_id", 25, "text"], ["mneme_record", "profile", 25, "text"], ["mneme_record", "record_type", 25, "text"], ["mneme_record", "schema_version", 20, "bigint"], ["mneme_record", "envelope", 17, "bytea"], ["mneme_record_pkey", "store_id", 25, "text"], ["mneme_record_pkey", "position", 20, "bigint"], ["mneme_record_store_id_record_id_key", "store_id", 25, "text"], ["mneme_record_store_id_record_id_key", "record_id", 25, "text"], ["mneme_schema", "singleton", 16, "boolean"], ["mneme_schema", "version", 23, "integer"], ["mneme_schema_pkey", "singleton", 16, "boolean"], ["mneme_store", "store_id", 25, "text"], ["mneme_store", "tail", 20, "bigint"], ["mneme_store_pkey", "store_id", 25, "text"]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_record ALTER COLUMN envelope SET NOT NULL;
```

### K01 — record-ID unique DEFERRABLE

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record DROP CONSTRAINT mneme_record_store_id_record_id_key;
ALTER TABLE mneme_record ADD CONSTRAINT mneme_record_store_id_record_id_key UNIQUE(store_id,record_id) DEFERRABLE;
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables ['mneme_operation', 'mneme_record', 'mneme_schema', 'mneme_store'] are not schema version 1"
  },
  "physical": [
    0,
    0,
    null
  ],
  "fingerprints": {
    "columns_match": true,
    "constraints_match": false
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"constraints": [["mneme_operation_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id, source_namespace, source_operation_id)"], ["mneme_operation_store_id_fkey", "f", true, false, false, true, 0, "FOREIGN KEY (store_id) REFERENCES mneme_store(store_id)"], ["mneme_record_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id, \"position\")"], ["mneme_record_position_check", "c", true, false, false, true, 0, "CHECK (((\"position\" >= 1) AND (\"position\" <= '9007199254740991'::bigint)))"], ["mneme_record_store_id_fkey", "f", true, false, false, true, 0, "FOREIGN KEY (store_id) REFERENCES mneme_store(store_id)"], ["mneme_record_store_id_record_id_key", "u", true, true, false, true, 0, "UNIQUE (store_id, record_id) DEFERRABLE"], ["mneme_schema_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (singleton)"], ["mneme_schema_singleton_check", "c", true, false, false, true, 0, "CHECK (singleton)"], ["mneme_store_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id)"], ["mneme_store_tail_check", "c", true, false, false, true, 0, "CHECK (((tail >= 0) AND (tail <= '9007199254740991'::bigint)))"]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_record DROP CONSTRAINT mneme_record_store_id_record_id_key;
ALTER TABLE mneme_record ADD CONSTRAINT mneme_record_store_id_record_id_key UNIQUE(store_id,record_id);
```

### K02 — record-ID unique DEFERRABLE INITIALLY DEFERRED

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record DROP CONSTRAINT mneme_record_store_id_record_id_key;
ALTER TABLE mneme_record ADD CONSTRAINT mneme_record_store_id_record_id_key UNIQUE(store_id,record_id) DEFERRABLE INITIALLY DEFERRED;
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables ['mneme_operation', 'mneme_record', 'mneme_schema', 'mneme_store'] are not schema version 1"
  },
  "physical": [
    0,
    0,
    null
  ],
  "fingerprints": {
    "columns_match": true,
    "constraints_match": false
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"constraints": [["mneme_operation_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id, source_namespace, source_operation_id)"], ["mneme_operation_store_id_fkey", "f", true, false, false, true, 0, "FOREIGN KEY (store_id) REFERENCES mneme_store(store_id)"], ["mneme_record_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id, \"position\")"], ["mneme_record_position_check", "c", true, false, false, true, 0, "CHECK (((\"position\" >= 1) AND (\"position\" <= '9007199254740991'::bigint)))"], ["mneme_record_store_id_fkey", "f", true, false, false, true, 0, "FOREIGN KEY (store_id) REFERENCES mneme_store(store_id)"], ["mneme_record_store_id_record_id_key", "u", true, true, true, true, 0, "UNIQUE (store_id, record_id) DEFERRABLE INITIALLY DEFERRED"], ["mneme_schema_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (singleton)"], ["mneme_schema_singleton_check", "c", true, false, false, true, 0, "CHECK (singleton)"], ["mneme_store_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id)"], ["mneme_store_tail_check", "c", true, false, false, true, 0, "CHECK (((tail >= 0) AND (tail <= '9007199254740991'::bigint)))"]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_record DROP CONSTRAINT mneme_record_store_id_record_id_key;
ALTER TABLE mneme_record ADD CONSTRAINT mneme_record_store_id_record_id_key UNIQUE(store_id,record_id);
```

### K03 — record position CHECK NOT VALID

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record DROP CONSTRAINT mneme_record_position_check;
ALTER TABLE mneme_record ADD CONSTRAINT mneme_record_position_check CHECK(position BETWEEN 1 AND 9007199254740991) NOT VALID;
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables ['mneme_operation', 'mneme_record', 'mneme_schema', 'mneme_store'] are not schema version 1"
  },
  "physical": [
    0,
    0,
    null
  ],
  "fingerprints": {
    "columns_match": true,
    "constraints_match": false
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"constraints": [["mneme_operation_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id, source_namespace, source_operation_id)"], ["mneme_operation_store_id_fkey", "f", true, false, false, true, 0, "FOREIGN KEY (store_id) REFERENCES mneme_store(store_id)"], ["mneme_record_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id, \"position\")"], ["mneme_record_position_check", "c", false, false, false, true, 0, "CHECK (((\"position\" >= 1) AND (\"position\" <= '9007199254740991'::bigint))) NOT VALID"], ["mneme_record_store_id_fkey", "f", true, false, false, true, 0, "FOREIGN KEY (store_id) REFERENCES mneme_store(store_id)"], ["mneme_record_store_id_record_id_key", "u", true, false, false, true, 0, "UNIQUE (store_id, record_id)"], ["mneme_schema_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (singleton)"], ["mneme_schema_singleton_check", "c", true, false, false, true, 0, "CHECK (singleton)"], ["mneme_store_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id)"], ["mneme_store_tail_check", "c", true, false, false, true, 0, "CHECK (((tail >= 0) AND (tail <= '9007199254740991'::bigint)))"]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_record VALIDATE CONSTRAINT mneme_record_position_check;
```

### K04 — record foreign key NOT VALID

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record DROP CONSTRAINT mneme_record_store_id_fkey;
ALTER TABLE mneme_record ADD CONSTRAINT mneme_record_store_id_fkey FOREIGN KEY(store_id) REFERENCES mneme_store NOT VALID;
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables ['mneme_operation', 'mneme_record', 'mneme_schema', 'mneme_store'] are not schema version 1"
  },
  "physical": [
    0,
    0,
    null
  ],
  "fingerprints": {
    "columns_match": true,
    "constraints_match": false
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"constraints": [["mneme_operation_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id, source_namespace, source_operation_id)"], ["mneme_operation_store_id_fkey", "f", true, false, false, true, 0, "FOREIGN KEY (store_id) REFERENCES mneme_store(store_id)"], ["mneme_record_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id, \"position\")"], ["mneme_record_position_check", "c", true, false, false, true, 0, "CHECK (((\"position\" >= 1) AND (\"position\" <= '9007199254740991'::bigint)))"], ["mneme_record_store_id_fkey", "f", false, false, false, true, 0, "FOREIGN KEY (store_id) REFERENCES mneme_store(store_id) NOT VALID"], ["mneme_record_store_id_record_id_key", "u", true, false, false, true, 0, "UNIQUE (store_id, record_id)"], ["mneme_schema_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (singleton)"], ["mneme_schema_singleton_check", "c", true, false, false, true, 0, "CHECK (singleton)"], ["mneme_store_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id)"], ["mneme_store_tail_check", "c", true, false, false, true, 0, "CHECK (((tail >= 0) AND (tail <= '9007199254740991'::bigint)))"]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_record VALIDATE CONSTRAINT mneme_record_store_id_fkey;
```

### K05 — record FK ON DELETE CASCADE

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record DROP CONSTRAINT mneme_record_store_id_fkey;
ALTER TABLE mneme_record ADD CONSTRAINT mneme_record_store_id_fkey FOREIGN KEY(store_id) REFERENCES mneme_store ON DELETE CASCADE;
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables ['mneme_operation', 'mneme_record', 'mneme_schema', 'mneme_store'] are not schema version 1"
  },
  "physical": [
    0,
    0,
    null
  ],
  "fingerprints": {
    "columns_match": true,
    "constraints_match": false
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"constraints": [["mneme_operation_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id, source_namespace, source_operation_id)"], ["mneme_operation_store_id_fkey", "f", true, false, false, true, 0, "FOREIGN KEY (store_id) REFERENCES mneme_store(store_id)"], ["mneme_record_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id, \"position\")"], ["mneme_record_position_check", "c", true, false, false, true, 0, "CHECK (((\"position\" >= 1) AND (\"position\" <= '9007199254740991'::bigint)))"], ["mneme_record_store_id_fkey", "f", true, false, false, true, 0, "FOREIGN KEY (store_id) REFERENCES mneme_store(store_id) ON DELETE CASCADE"], ["mneme_record_store_id_record_id_key", "u", true, false, false, true, 0, "UNIQUE (store_id, record_id)"], ["mneme_schema_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (singleton)"], ["mneme_schema_singleton_check", "c", true, false, false, true, 0, "CHECK (singleton)"], ["mneme_store_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id)"], ["mneme_store_tail_check", "c", true, false, false, true, 0, "CHECK (((tail >= 0) AND (tail <= '9007199254740991'::bigint)))"]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_record DROP CONSTRAINT mneme_record_store_id_fkey;
ALTER TABLE mneme_record ADD CONSTRAINT mneme_record_store_id_fkey FOREIGN KEY(store_id) REFERENCES mneme_store;
```

### K06 — record FK ON UPDATE CASCADE

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record DROP CONSTRAINT mneme_record_store_id_fkey;
ALTER TABLE mneme_record ADD CONSTRAINT mneme_record_store_id_fkey FOREIGN KEY(store_id) REFERENCES mneme_store ON UPDATE CASCADE;
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables ['mneme_operation', 'mneme_record', 'mneme_schema', 'mneme_store'] are not schema version 1"
  },
  "physical": [
    0,
    0,
    null
  ],
  "fingerprints": {
    "columns_match": true,
    "constraints_match": false
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"constraints": [["mneme_operation_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id, source_namespace, source_operation_id)"], ["mneme_operation_store_id_fkey", "f", true, false, false, true, 0, "FOREIGN KEY (store_id) REFERENCES mneme_store(store_id)"], ["mneme_record_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id, \"position\")"], ["mneme_record_position_check", "c", true, false, false, true, 0, "CHECK (((\"position\" >= 1) AND (\"position\" <= '9007199254740991'::bigint)))"], ["mneme_record_store_id_fkey", "f", true, false, false, true, 0, "FOREIGN KEY (store_id) REFERENCES mneme_store(store_id) ON UPDATE CASCADE"], ["mneme_record_store_id_record_id_key", "u", true, false, false, true, 0, "UNIQUE (store_id, record_id)"], ["mneme_schema_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (singleton)"], ["mneme_schema_singleton_check", "c", true, false, false, true, 0, "CHECK (singleton)"], ["mneme_store_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id)"], ["mneme_store_tail_check", "c", true, false, false, true, 0, "CHECK (((tail >= 0) AND (tail <= '9007199254740991'::bigint)))"]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_record DROP CONSTRAINT mneme_record_store_id_fkey;
ALTER TABLE mneme_record ADD CONSTRAINT mneme_record_store_id_fkey FOREIGN KEY(store_id) REFERENCES mneme_store;
```

### K07 — record FK ON DELETE RESTRICT

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record DROP CONSTRAINT mneme_record_store_id_fkey;
ALTER TABLE mneme_record ADD CONSTRAINT mneme_record_store_id_fkey FOREIGN KEY(store_id) REFERENCES mneme_store ON DELETE RESTRICT;
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables ['mneme_operation', 'mneme_record', 'mneme_schema', 'mneme_store'] are not schema version 1"
  },
  "physical": [
    0,
    0,
    null
  ],
  "clock_contexts": [],
  "fingerprints": {
    "columns_match": true,
    "constraints_match": false
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"constraints": [["mneme_operation_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id, source_namespace, source_operation_id)"], ["mneme_operation_store_id_fkey", "f", true, false, false, true, 0, "FOREIGN KEY (store_id) REFERENCES mneme_store(store_id)"], ["mneme_record_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id, \"position\")"], ["mneme_record_position_check", "c", true, false, false, true, 0, "CHECK (((\"position\" >= 1) AND (\"position\" <= '9007199254740991'::bigint)))"], ["mneme_record_store_id_fkey", "f", true, false, false, true, 0, "FOREIGN KEY (store_id) REFERENCES mneme_store(store_id) ON DELETE RESTRICT"], ["mneme_record_store_id_record_id_key", "u", true, false, false, true, 0, "UNIQUE (store_id, record_id)"], ["mneme_schema_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (singleton)"], ["mneme_schema_singleton_check", "c", true, false, false, true, 0, "CHECK (singleton)"], ["mneme_store_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id)"], ["mneme_store_tail_check", "c", true, false, false, true, 0, "CHECK (((tail >= 0) AND (tail <= '9007199254740991'::bigint)))"]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_record DROP CONSTRAINT mneme_record_store_id_fkey;
ALTER TABLE mneme_record ADD CONSTRAINT mneme_record_store_id_fkey FOREIGN KEY(store_id) REFERENCES mneme_store;
```

### K08 — record FK DEFERRABLE INITIALLY DEFERRED

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record DROP CONSTRAINT mneme_record_store_id_fkey;
ALTER TABLE mneme_record ADD CONSTRAINT mneme_record_store_id_fkey FOREIGN KEY(store_id) REFERENCES mneme_store DEFERRABLE INITIALLY DEFERRED;
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables ['mneme_operation', 'mneme_record', 'mneme_schema', 'mneme_store'] are not schema version 1"
  },
  "physical": [
    0,
    0,
    null
  ],
  "clock_contexts": [],
  "fingerprints": {
    "columns_match": true,
    "constraints_match": false
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"constraints": [["mneme_operation_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id, source_namespace, source_operation_id)"], ["mneme_operation_store_id_fkey", "f", true, false, false, true, 0, "FOREIGN KEY (store_id) REFERENCES mneme_store(store_id)"], ["mneme_record_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id, \"position\")"], ["mneme_record_position_check", "c", true, false, false, true, 0, "CHECK (((\"position\" >= 1) AND (\"position\" <= '9007199254740991'::bigint)))"], ["mneme_record_store_id_fkey", "f", true, true, true, true, 0, "FOREIGN KEY (store_id) REFERENCES mneme_store(store_id) DEFERRABLE INITIALLY DEFERRED"], ["mneme_record_store_id_record_id_key", "u", true, false, false, true, 0, "UNIQUE (store_id, record_id)"], ["mneme_schema_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (singleton)"], ["mneme_schema_singleton_check", "c", true, false, false, true, 0, "CHECK (singleton)"], ["mneme_store_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id)"], ["mneme_store_tail_check", "c", true, false, false, true, 0, "CHECK (((tail >= 0) AND (tail <= '9007199254740991'::bigint)))"]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_record DROP CONSTRAINT mneme_record_store_id_fkey;
ALTER TABLE mneme_record ADD CONSTRAINT mneme_record_store_id_fkey FOREIGN KEY(store_id) REFERENCES mneme_store;
```

### K09 — constraint renamed

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record RENAME CONSTRAINT mneme_record_store_id_record_id_key TO probe_unique;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"constraints": [["mneme_operation_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id, source_namespace, source_operation_id)"], ["mneme_operation_store_id_fkey", "f", true, false, false, true, 0, "FOREIGN KEY (store_id) REFERENCES mneme_store(store_id)"], ["mneme_record_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id, \"position\")"], ["mneme_record_position_check", "c", true, false, false, true, 0, "CHECK (((\"position\" >= 1) AND (\"position\" <= '9007199254740991'::bigint)))"], ["mneme_record_store_id_fkey", "f", true, false, false, true, 0, "FOREIGN KEY (store_id) REFERENCES mneme_store(store_id)"], ["mneme_schema_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (singleton)"], ["mneme_schema_singleton_check", "c", true, false, false, true, 0, "CHECK (singleton)"], ["mneme_store_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id)"], ["mneme_store_tail_check", "c", true, false, false, true, 0, "CHECK (((tail >= 0) AND (tail <= '9007199254740991'::bigint)))"], ["probe_unique", "u", true, false, false, true, 0, "UNIQUE (store_id, record_id)"]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_record RENAME CONSTRAINT probe_unique TO mneme_record_store_id_record_id_key;
```

### K10 — extra CHECK true

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record ADD CONSTRAINT probe_check CHECK(true);
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables ['mneme_operation', 'mneme_record', 'mneme_schema', 'mneme_store'] are not schema version 1"
  },
  "physical": [
    0,
    0,
    null
  ],
  "clock_contexts": [],
  "fingerprints": {
    "columns_match": true,
    "constraints_match": false
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"constraints": [["mneme_operation_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id, source_namespace, source_operation_id)"], ["mneme_operation_store_id_fkey", "f", true, false, false, true, 0, "FOREIGN KEY (store_id) REFERENCES mneme_store(store_id)"], ["mneme_record_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id, \"position\")"], ["mneme_record_position_check", "c", true, false, false, true, 0, "CHECK (((\"position\" >= 1) AND (\"position\" <= '9007199254740991'::bigint)))"], ["mneme_record_store_id_fkey", "f", true, false, false, true, 0, "FOREIGN KEY (store_id) REFERENCES mneme_store(store_id)"], ["mneme_record_store_id_record_id_key", "u", true, false, false, true, 0, "UNIQUE (store_id, record_id)"], ["mneme_schema_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (singleton)"], ["mneme_schema_singleton_check", "c", true, false, false, true, 0, "CHECK (singleton)"], ["mneme_store_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id)"], ["mneme_store_tail_check", "c", true, false, false, true, 0, "CHECK (((tail >= 0) AND (tail <= '9007199254740991'::bigint)))"], ["probe_check", "c", true, false, false, true, 0, "CHECK (true)"]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_record DROP CONSTRAINT probe_check;
```

### K11 — extra CHECK excludes valid profile

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record ADD CONSTRAINT probe_check CHECK(profile <> 'learning');
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables ['mneme_operation', 'mneme_record', 'mneme_schema', 'mneme_store'] are not schema version 1"
  },
  "physical": [
    0,
    0,
    null
  ],
  "clock_contexts": [],
  "fingerprints": {
    "columns_match": true,
    "constraints_match": false
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"constraints": [["mneme_operation_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id, source_namespace, source_operation_id)"], ["mneme_operation_store_id_fkey", "f", true, false, false, true, 0, "FOREIGN KEY (store_id) REFERENCES mneme_store(store_id)"], ["mneme_record_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id, \"position\")"], ["mneme_record_position_check", "c", true, false, false, true, 0, "CHECK (((\"position\" >= 1) AND (\"position\" <= '9007199254740991'::bigint)))"], ["mneme_record_store_id_fkey", "f", true, false, false, true, 0, "FOREIGN KEY (store_id) REFERENCES mneme_store(store_id)"], ["mneme_record_store_id_record_id_key", "u", true, false, false, true, 0, "UNIQUE (store_id, record_id)"], ["mneme_schema_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (singleton)"], ["mneme_schema_singleton_check", "c", true, false, false, true, 0, "CHECK (singleton)"], ["mneme_store_pkey", "p", true, false, false, true, 0, "PRIMARY KEY (store_id)"], ["mneme_store_tail_check", "c", true, false, false, true, 0, "CHECK (((tail >= 0) AND (tail <= '9007199254740991'::bigint)))"], ["probe_check", "c", true, false, false, true, 0, "CHECK ((profile <> 'learning'::text))"]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_record DROP CONSTRAINT probe_check;
```

### I01 — CREATE INDEX probe_idx ON mneme_record(profile)

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
CREATE INDEX probe_idx ON mneme_record(profile);
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"indexes": [["mneme_operation_pkey", true, true, true, true, true, "3126 3126 10006", "100 100 0", null, null], ["mneme_record_pkey", true, true, true, true, true, "3126 3124", "100 0", null, null], ["mneme_record_store_id_record_id_key", true, true, true, true, true, "3126 3126", "100 100", null, null], ["mneme_schema_pkey", true, true, true, true, true, "10003", "0", null, null], ["mneme_store_pkey", true, true, true, true, true, "3126", "100", null, null], ["probe_idx", true, true, true, false, true, "3126", "100", null, null]]}
```

Executed reversal:

```sql
DROP INDEX IF EXISTS probe_idx;
```

### I02 — CREATE UNIQUE INDEX probe_idx ON mneme_record(profile)

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
CREATE UNIQUE INDEX probe_idx ON mneme_record(profile);
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    0,
    0,
    0
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "failed_at": "commit",
    "error": {
      "exception": "UniqueViolation",
      "sqlstate": "23505",
      "code": null,
      "argument": null,
      "detail": "duplicate key value violates unique constraint \"probe_idx\"\nDETAIL:  Key (profile)=(learning) already exists."
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"indexes": [["mneme_operation_pkey", true, true, true, true, true, "3126 3126 10006", "100 100 0", null, null], ["mneme_record_pkey", true, true, true, true, true, "3126 3124", "100 0", null, null], ["mneme_record_store_id_record_id_key", true, true, true, true, true, "3126 3126", "100 100", null, null], ["mneme_schema_pkey", true, true, true, true, true, "10003", "0", null, null], ["mneme_store_pkey", true, true, true, true, true, "3126", "100", null, null], ["probe_idx", true, true, true, true, true, "3126", "100", null, null]]}
```

Executed reversal:

```sql
DROP INDEX IF EXISTS probe_idx;
```

### I03 — CREATE INDEX probe_idx ON mneme_record(profile) WHERE schema_version=1

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
CREATE INDEX probe_idx ON mneme_record(profile) WHERE schema_version=1;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"indexes": [["mneme_operation_pkey", true, true, true, true, true, "3126 3126 10006", "100 100 0", null, null], ["mneme_record_pkey", true, true, true, true, true, "3126 3124", "100 0", null, null], ["mneme_record_store_id_record_id_key", true, true, true, true, true, "3126 3126", "100 100", null, null], ["mneme_schema_pkey", true, true, true, true, true, "10003", "0", null, null], ["mneme_store_pkey", true, true, true, true, true, "3126", "100", null, null], ["probe_idx", true, true, true, false, true, "3126", "100", "(schema_version = 1)", null]]}
```

Executed reversal:

```sql
DROP INDEX IF EXISTS probe_idx;
```

### I04 — CREATE INDEX probe_idx ON mneme_record((lower(profile)))

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
CREATE INDEX probe_idx ON mneme_record((lower(profile)));
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"indexes": [["mneme_operation_pkey", true, true, true, true, true, "3126 3126 10006", "100 100 0", null, null], ["mneme_record_pkey", true, true, true, true, true, "3126 3124", "100 0", null, null], ["mneme_record_store_id_record_id_key", true, true, true, true, true, "3126 3126", "100 100", null, null], ["mneme_schema_pkey", true, true, true, true, true, "10003", "0", null, null], ["mneme_store_pkey", true, true, true, true, true, "3126", "100", null, null], ["probe_idx", true, true, true, false, true, "3126", "100", null, "lower(profile)"]]}
```

Executed reversal:

```sql
DROP INDEX IF EXISTS probe_idx;
```

### I05 — CREATE INDEX probe_idx ON mneme_record USING hash(profile)

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
CREATE INDEX probe_idx ON mneme_record USING hash(profile);
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"indexes": [["mneme_operation_pkey", true, true, true, true, true, "3126 3126 10006", "100 100 0", null, null], ["mneme_record_pkey", true, true, true, true, true, "3126 3124", "100 0", null, null], ["mneme_record_store_id_record_id_key", true, true, true, true, true, "3126 3126", "100 100", null, null], ["mneme_schema_pkey", true, true, true, true, true, "10003", "0", null, null], ["mneme_store_pkey", true, true, true, true, true, "3126", "100", null, null], ["probe_idx", true, true, true, false, true, "10037", "100", null, null]]}
```

Executed reversal:

```sql
DROP INDEX IF EXISTS probe_idx;
```

### I06 — CREATE UNIQUE INDEX probe_idx ON mneme_record(store_id,record_id)

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
CREATE UNIQUE INDEX probe_idx ON mneme_record(store_id,record_id);
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"indexes": [["mneme_operation_pkey", true, true, true, true, true, "3126 3126 10006", "100 100 0", null, null], ["mneme_record_pkey", true, true, true, true, true, "3126 3124", "100 0", null, null], ["mneme_record_store_id_record_id_key", true, true, true, true, true, "3126 3126", "100 100", null, null], ["mneme_schema_pkey", true, true, true, true, true, "10003", "0", null, null], ["mneme_store_pkey", true, true, true, true, true, "3126", "100", null, null], ["probe_idx", true, true, true, true, true, "3126 3126", "100 100", null, null]]}
```

Executed reversal:

```sql
DROP INDEX IF EXISTS probe_idx;
```

### I07 — CREATE INDEX probe_idx ON mneme_record(record_id text_pattern_ops)

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
CREATE INDEX probe_idx ON mneme_record(record_id text_pattern_ops);
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"indexes": [["mneme_operation_pkey", true, true, true, true, true, "3126 3126 10006", "100 100 0", null, null], ["mneme_record_pkey", true, true, true, true, true, "3126 3124", "100 0", null, null], ["mneme_record_store_id_record_id_key", true, true, true, true, true, "3126 3126", "100 100", null, null], ["mneme_schema_pkey", true, true, true, true, true, "10003", "0", null, null], ["mneme_store_pkey", true, true, true, true, true, "3126", "100", null, null], ["probe_idx", true, true, true, false, true, "4217", "100", null, null]]}
```

Executed reversal:

```sql
DROP INDEX IF EXISTS probe_idx;
```

### I08 — Attach CREATE UNIQUE INDEX probe_idx ON mneme_record(record_id) WHERE schema_version=1

Public mode: `across_store`; connection options: ``.

Executed setup:

```sql
CREATE UNIQUE INDEX probe_idx ON mneme_record(record_id) WHERE schema_version=1;
ALTER TABLE mneme_record ADD CONSTRAINT probe_constraint UNIQUE USING INDEX probe_idx;
```

Observed:

```json
{
  "setup_error": {
    "exception": "WrongObjectType",
    "sqlstate": "42809",
    "code": null,
    "argument": null,
    "detail": "\"probe_idx\" is a partial index\nLINE 1: ALTER TABLE mneme_record ADD CONSTRAINT probe_constraint UNI...\n                                     ^\nDETAIL:  Cannot create a primary key or unique constraint using such an index."
  },
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ],
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "failed_at": "cross-store reuse",
    "error": {
      "exception": "UniqueViolation",
      "sqlstate": "23505",
      "code": null,
      "argument": null,
      "detail": "duplicate key value violates unique constraint \"probe_idx\"\nDETAIL:  Key (record_id)=(r1) already exists."
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"indexes": [["mneme_operation_pkey", true, true, true, true, true, "3126 3126 10006", "100 100 0", null, null], ["mneme_record_pkey", true, true, true, true, true, "3126 3124", "100 0", null, null], ["mneme_record_store_id_record_id_key", true, true, true, true, true, "3126 3126", "100 100", null, null], ["mneme_schema_pkey", true, true, true, true, true, "10003", "0", null, null], ["mneme_store_pkey", true, true, true, true, true, "3126", "100", null, null], ["probe_idx", true, true, true, true, true, "3126", "100", "(schema_version = 1)", null]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_record DROP CONSTRAINT IF EXISTS probe_constraint;
DROP INDEX IF EXISTS probe_idx;
```

Assessment correction/limit: Constraint attachment failed, but the remaining extra partial unique index restricts valid cross-store reuse.

### I09 — Attach CREATE UNIQUE INDEX probe_idx ON mneme_record((lower(record_id)))

Public mode: `across_store`; connection options: ``.

Executed setup:

```sql
CREATE UNIQUE INDEX probe_idx ON mneme_record((lower(record_id)));
ALTER TABLE mneme_record ADD CONSTRAINT probe_constraint UNIQUE USING INDEX probe_idx;
```

Observed:

```json
{
  "setup_error": {
    "exception": "WrongObjectType",
    "sqlstate": "42809",
    "code": null,
    "argument": null,
    "detail": "index \"probe_idx\" contains expressions\nLINE 1: ALTER TABLE mneme_record ADD CONSTRAINT probe_constraint UNI...\n                                     ^\nDETAIL:  Cannot create a primary key or unique constraint using such an index."
  },
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ],
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "failed_at": "cross-store reuse",
    "error": {
      "exception": "UniqueViolation",
      "sqlstate": "23505",
      "code": null,
      "argument": null,
      "detail": "duplicate key value violates unique constraint \"probe_idx\"\nDETAIL:  Key (lower(record_id))=(r1) already exists."
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"indexes": [["mneme_operation_pkey", true, true, true, true, true, "3126 3126 10006", "100 100 0", null, null], ["mneme_record_pkey", true, true, true, true, true, "3126 3124", "100 0", null, null], ["mneme_record_store_id_record_id_key", true, true, true, true, true, "3126 3126", "100 100", null, null], ["mneme_schema_pkey", true, true, true, true, true, "10003", "0", null, null], ["mneme_store_pkey", true, true, true, true, true, "3126", "100", null, null], ["probe_idx", true, true, true, true, true, "3126", "100", null, "lower(record_id)"]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_record DROP CONSTRAINT IF EXISTS probe_constraint;
DROP INDEX IF EXISTS probe_idx;
```

Assessment correction/limit: Constraint attachment failed, but the remaining extra expression unique index restricts valid cross-store reuse.

### I10 — Attach CREATE UNIQUE INDEX probe_idx ON mneme_record(record_id text_pattern_ops)

Public mode: `across_store`; connection options: ``.

Executed setup:

```sql
CREATE UNIQUE INDEX probe_idx ON mneme_record(record_id text_pattern_ops);
ALTER TABLE mneme_record ADD CONSTRAINT probe_constraint UNIQUE USING INDEX probe_idx;
```

Observed:

```json
{
  "setup_error": {
    "exception": "WrongObjectType",
    "sqlstate": "42809",
    "code": null,
    "argument": null,
    "detail": "index \"probe_idx\" column number 1 does not have default sorting behavior\nLINE 1: ALTER TABLE mneme_record ADD CONSTRAINT probe_constraint UNI...\n                                     ^\nDETAIL:  Cannot create a primary key or unique constraint using such an index."
  },
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ],
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "failed_at": "cross-store reuse",
    "error": {
      "exception": "UniqueViolation",
      "sqlstate": "23505",
      "code": null,
      "argument": null,
      "detail": "duplicate key value violates unique constraint \"probe_idx\"\nDETAIL:  Key (record_id)=(r1) already exists."
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"indexes": [["mneme_operation_pkey", true, true, true, true, true, "3126 3126 10006", "100 100 0", null, null], ["mneme_record_pkey", true, true, true, true, true, "3126 3124", "100 0", null, null], ["mneme_record_store_id_record_id_key", true, true, true, true, true, "3126 3126", "100 100", null, null], ["mneme_schema_pkey", true, true, true, true, true, "10003", "0", null, null], ["mneme_store_pkey", true, true, true, true, true, "3126", "100", null, null], ["probe_idx", true, true, true, true, true, "4217", "100", null, null]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_record DROP CONSTRAINT IF EXISTS probe_constraint;
DROP INDEX IF EXISTS probe_idx;
```

Assessment correction/limit: Constraint attachment failed, but the remaining extra unique index restricts valid cross-store reuse.

### I11 — primary-key index fillfactor

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER INDEX mneme_record_pkey SET (fillfactor=50);
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"indexes": [["mneme_operation_pkey", true, true, true, true, true, "3126 3126 10006", "100 100 0", null, null], ["mneme_record_pkey", true, true, true, true, true, "3126 3124", "100 0", null, null], ["mneme_record_store_id_record_id_key", true, true, true, true, true, "3126 3126", "100 100", null, null], ["mneme_schema_pkey", true, true, true, true, true, "10003", "0", null, null], ["mneme_store_pkey", true, true, true, true, true, "3126", "100", null, null]]}
```

Executed reversal:

```sql
ALTER INDEX mneme_record_pkey RESET (fillfactor);
```

### I12 — primary-key index clustering marker

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record CLUSTER ON mneme_record_pkey;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"indexes": [["mneme_operation_pkey", true, true, true, true, true, "3126 3126 10006", "100 100 0", null, null], ["mneme_record_pkey", true, true, true, true, true, "3126 3124", "100 0", null, null], ["mneme_record_store_id_record_id_key", true, true, true, true, true, "3126 3126", "100 100", null, null], ["mneme_schema_pkey", true, true, true, true, true, "10003", "0", null, null], ["mneme_store_pkey", true, true, true, true, true, "3126", "100", null, null]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_record SET WITHOUT CLUSTER;
```

### I13 — record replica identity full

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_record REPLICA IDENTITY FULL;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"indexes": [["mneme_operation_pkey", true, true, true, true, true, "3126 3126 10006", "100 100 0", null, null], ["mneme_record_pkey", true, true, true, true, true, "3126 3124", "100 0", null, null], ["mneme_record_store_id_record_id_key", true, true, true, true, true, "3126 3126", "100 100", null, null], ["mneme_schema_pkey", true, true, true, true, true, "10003", "0", null, null], ["mneme_store_pkey", true, true, true, true, true, "3126", "100", null, null]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_record REPLICA IDENTITY DEFAULT;
```

### I14 — extra invalid unique index after concurrent build fails

Public mode: `normal`; connection options: `default unless special recipe above`.

Executed setup:

```sql
seed two same-profile records;
CREATE UNIQUE INDEX CONCURRENTLY probe_idx ON mneme_record(profile);
```

Observed:

```json
{
  "setup_error": {
    "exception": "UniqueViolation",
    "sqlstate": "23505",
    "code": null,
    "argument": null,
    "detail": "could not create unique index \"probe_idx\"\nDETAIL:  Key (profile)=(learning) is duplicated."
  },
  "open": "ACCEPT",
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"indexes": [["mneme_operation_pkey", true, true, true, true, true, "3126 3126 10006", "100 100 0", null, null], ["mneme_record_pkey", true, true, true, true, true, "3126 3124", "100 0", null, null], ["mneme_record_store_id_record_id_key", true, true, true, true, true, "3126 3126", "100 100", null, null], ["mneme_schema_pkey", true, true, true, true, true, "10003", "0", null, null], ["mneme_store_pkey", true, true, true, true, true, "3126", "100", null, null], ["probe_idx", false, false, true, true, true, "3126", "100", null, null]]}
```

Executed reversal:

```sql
DROP INDEX probe_idx;
```

Assessment correction/limit: Invalid AND not-ready extra index: no valid-write rejection observed. Acceptance policy C01; do not confuse with I18.

### I15 — replacement operation PK using non-bytewise index collation

Public mode: `namespace`; connection options: ``.

Executed setup:

```sql
CREATE COLLATION probe_loose (provider=icu,locale='und-u-ka-shifted',deterministic=false);
ALTER TABLE mneme_operation DROP CONSTRAINT mneme_operation_pkey;
CREATE UNIQUE INDEX probe_backed ON mneme_operation(store_id,source_namespace COLLATE probe_loose,source_operation_id);
ALTER TABLE mneme_operation ADD CONSTRAINT mneme_operation_pkey PRIMARY KEY USING INDEX probe_backed;
```

Observed:

```json
{
  "setup_error": {
    "exception": "WrongObjectType",
    "sqlstate": "42809",
    "code": null,
    "argument": null,
    "detail": "index \"probe_backed\" column number 2 does not have default sorting behavior\nLINE 1: ALTER TABLE mneme_operation ADD CONSTRAINT mneme_operation_p...\n                                        ^\nDETAIL:  Cannot create a primary key or unique constraint using such an index."
  },
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables ['mneme_operation', 'mneme_record', 'mneme_schema', 'mneme_store'] are not schema version 1"
  },
  "physical": [
    0,
    0,
    null
  ],
  "clock_contexts": [],
  "fingerprints": {
    "columns_match": true,
    "constraints_match": false
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"indexes": [["mneme_record_pkey", true, true, true, true, true, "3126 3124", "100 0", null, null], ["mneme_record_store_id_record_id_key", true, true, true, true, true, "3126 3126", "100 100", null, null], ["mneme_schema_pkey", true, true, true, true, true, "10003", "0", null, null], ["mneme_store_pkey", true, true, true, true, true, "3126", "100", null, null], ["probe_backed", true, true, true, true, true, "3126 3126 10006", "100 34159 0", null, null]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_operation DROP CONSTRAINT IF EXISTS mneme_operation_pkey;
DROP INDEX IF EXISTS probe_backed;
ALTER TABLE mneme_operation ADD CONSTRAINT mneme_operation_pkey PRIMARY KEY(store_id,source_namespace,source_operation_id);
DROP COLLATION probe_loose;
```

Assessment correction/limit: Nondefault-collation backing attachment refused by engine. Rejection observes missing PK, not an independently verified backing-index collation.

### I16 — replacement operation PK using text_pattern_ops

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
ALTER TABLE mneme_operation DROP CONSTRAINT mneme_operation_pkey;
CREATE UNIQUE INDEX probe_backed ON mneme_operation(store_id,source_namespace text_pattern_ops,source_operation_id);
ALTER TABLE mneme_operation ADD CONSTRAINT mneme_operation_pkey PRIMARY KEY USING INDEX probe_backed;
```

Observed:

```json
{
  "setup_error": {
    "exception": "WrongObjectType",
    "sqlstate": "42809",
    "code": null,
    "argument": null,
    "detail": "index \"probe_backed\" column number 2 does not have default sorting behavior\nLINE 1: ALTER TABLE mneme_operation ADD CONSTRAINT mneme_operation_p...\n                                        ^\nDETAIL:  Cannot create a primary key or unique constraint using such an index."
  },
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables ['mneme_operation', 'mneme_record', 'mneme_schema', 'mneme_store'] are not schema version 1"
  },
  "physical": [
    0,
    0,
    null
  ],
  "clock_contexts": [],
  "fingerprints": {
    "columns_match": true,
    "constraints_match": false
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"indexes": [["mneme_record_pkey", true, true, true, true, true, "3126 3124", "100 0", null, null], ["mneme_record_store_id_record_id_key", true, true, true, true, true, "3126 3126", "100 100", null, null], ["mneme_schema_pkey", true, true, true, true, true, "10003", "0", null, null], ["mneme_store_pkey", true, true, true, true, true, "3126", "100", null, null], ["probe_backed", true, true, true, true, true, "3126 4217 10006", "100 100 0", null, null]]}
```

Executed reversal:

```sql
ALTER TABLE mneme_operation DROP CONSTRAINT IF EXISTS mneme_operation_pkey;
DROP INDEX IF EXISTS probe_backed;
ALTER TABLE mneme_operation ADD CONSTRAINT mneme_operation_pkey PRIMARY KEY(store_id,source_namespace,source_operation_id);
```

Assessment correction/limit: Nondefault-opclass backing attachment refused by engine. Rejection observes missing PK, not an independently verified opclass.

### I17 — drop index backing operation primary key

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
DROP INDEX mneme_operation_pkey;
```

Observed:

```json
{
  "setup_error": {
    "exception": "DependentObjectsStillExist",
    "sqlstate": "2BP01",
    "code": null,
    "argument": null,
    "detail": "cannot drop index mneme_operation_pkey because constraint mneme_operation_pkey on table mneme_operation requires it\nHINT:  You can drop constraint mneme_operation_pkey on table mneme_operation instead."
  },
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"indexes": [["mneme_operation_pkey", true, true, true, true, true, "3126 3126 10006", "100 100 0", null, null], ["mneme_record_pkey", true, true, true, true, true, "3126 3124", "100 0", null, null], ["mneme_record_store_id_record_id_key", true, true, true, true, true, "3126 3126", "100 100", null, null], ["mneme_schema_pkey", true, true, true, true, true, "10003", "0", null, null], ["mneme_store_pkey", true, true, true, true, true, "3126", "100", null, null]]}
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

Assessment correction/limit: Dropping a live backing PK index alone is engine-protected; no invalid backing index was constructed.

### I18 — invalid but ready extra unique index after late validation failure

Public mode: `normal`; connection options: `default unless special recipe above`.

Executed setup:

```sql
seed r1/r2 in store seed;
hold advisory gate 73700401;
IMMUTABLE probe_pause(record_id) waits on gate for r2 then returns argument unchanged;
CREATE UNIQUE INDEX CONCURRENTLY probe_idx ON mneme_record((probe_pause(record_id)));
while build waits, commit r1 in another store; release gate; observe failed validation;
```

Observed:

```json
{
  "open": "ACCEPT",
  "build_result": [
    {
      "exception": "UniqueViolation",
      "sqlstate": "23505",
      "code": null,
      "argument": null,
      "detail": "duplicate key value violates unique constraint \"probe_idx\"\nDETAIL:  Key (probe_pause(record_id))=(r1) already exists."
    }
  ],
  "later": {
    "created": true,
    "failed_at": "commit",
    "error": {
      "exception": "UniqueViolation",
      "sqlstate": "23505",
      "code": null,
      "argument": null,
      "detail": "duplicate key value violates unique constraint \"probe_idx\"\nDETAIL:  Key (probe_pause(record_id))=(r1) already exists."
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"indexes": [["mneme_operation_pkey", true, true, true, true, true, "3126 3126 10006", "100 100 0", null, null], ["mneme_record_pkey", true, true, true, true, true, "3126 3124", "100 0", null, null], ["mneme_record_store_id_record_id_key", true, true, true, true, true, "3126 3126", "100 100", null, null], ["mneme_schema_pkey", true, true, true, true, true, "10003", "0", null, null], ["mneme_store_pkey", true, true, true, true, true, "3126", "100", null, null], ["probe_idx", false, true, true, true, true, "3126", "100", null, "probe_pause(record_id)"]]}
```

Executed reversal:

```sql
DROP INDEX probe_idx;
DROP FUNCTION probe_pause(text);
DELETE own fixture data;
```

### I19 — extra non-unique expression narrows token domain

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
CREATE INDEX probe_idx ON mneme_record((record_id::integer));
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    0,
    0,
    0
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "failed_at": "commit",
    "error": {
      "exception": "InvalidTextRepresentation",
      "sqlstate": "22P02",
      "code": null,
      "argument": null,
      "detail": "invalid input syntax for type integer: \"r1\""
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"indexes": [["mneme_operation_pkey", true, true, true, true, true, "3126 3126 10006", "100 100 0", null, null], ["mneme_record_pkey", true, true, true, true, true, "3126 3124", "100 0", null, null], ["mneme_record_store_id_record_id_key", true, true, true, true, true, "3126 3126", "100 100", null, null], ["mneme_schema_pkey", true, true, true, true, true, "10003", "0", null, null], ["mneme_store_pkey", true, true, true, true, true, "3126", "100", null, null], ["probe_idx", true, true, true, false, true, "1978", "0", null, "(record_id)::integer"]]}
```

Executed reversal:

```sql
DROP INDEX probe_idx;
```

### I20 — extra non-unique partial predicate narrows token domain

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
CREATE INDEX probe_idx ON mneme_record(record_id) WHERE record_id::integer>0;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    0,
    0,
    0
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "failed_at": "commit",
    "error": {
      "exception": "InvalidTextRepresentation",
      "sqlstate": "22P02",
      "code": null,
      "argument": null,
      "detail": "invalid input syntax for type integer: \"r1\""
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"indexes": [["mneme_operation_pkey", true, true, true, true, true, "3126 3126 10006", "100 100 0", null, null], ["mneme_record_pkey", true, true, true, true, true, "3126 3124", "100 0", null, null], ["mneme_record_store_id_record_id_key", true, true, true, true, true, "3126 3126", "100 100", null, null], ["mneme_schema_pkey", true, true, true, true, true, "10003", "0", null, null], ["mneme_store_pkey", true, true, true, true, true, "3126", "100", null, null], ["probe_idx", true, true, true, false, true, "3126", "100", "((record_id)::integer > 0)", null]]}
```

Executed reversal:

```sql
DROP INDEX probe_idx;
```

### H01 — schema version 2

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
UPDATE mneme_schema SET version=2;
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables ['mneme_operation', 'mneme_record', 'mneme_schema', 'mneme_store'] are not schema version 1"
  },
  "physical": [
    0,
    0,
    null
  ],
  "clock_contexts": [],
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
```

Executed reversal:

```sql
UPDATE mneme_schema SET version=1;
```

### H02 — schema version row absent

Public mode: `normal`; connection options: ``.

Executed setup:

```sql
DELETE FROM mneme_schema;
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables ['mneme_operation', 'mneme_record', 'mneme_schema', 'mneme_store'] are not schema version 1"
  },
  "physical": [
    0,
    0,
    null
  ],
  "clock_contexts": [],
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
```

Executed reversal:

```sql
INSERT INTO mneme_schema(version) VALUES(1);
```

### S01 — session default Repeatable Read

Public mode: `normal`; connection options: `-c default_transaction_isolation=repeatable\ read`.

Executed setup:

```sql
-- ordinary initialized v1; no forward DDL;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

### S02 — session default Serializable

Public mode: `normal`; connection options: `-c default_transaction_isolation=serializable`.

Executed setup:

```sql
-- ordinary initialized v1; no forward DDL;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

### S03 — session synchronous_commit off

Public mode: `normal`; connection options: `-c synchronous_commit=off`.

Executed setup:

```sql
-- ordinary initialized v1; no forward DDL;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

### S04 — session default_transaction_read_only on

Public mode: `normal`; connection options: `-c default_transaction_read_only=on`.

Executed setup:

```sql
-- ordinary initialized v1; no forward DDL;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

### S05 — session row_security off

Public mode: `normal`; connection options: `-c row_security=off`.

Executed setup:

```sql
-- ordinary initialized v1; no forward DDL;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

### S06 — session replication role replica

Public mode: `normal`; connection options: `-c session_replication_role=replica`.

Executed setup:

```sql
-- ordinary initialized v1; no forward DDL;
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "OperationalError",
    "sqlstate": null,
    "code": null,
    "argument": null,
    "detail": "connection failed: connection to server at \"127.0.0.1\", port 5432 failed: FATAL:  permission denied to set parameter \"session_replication_role\"\nMultiple connection attempts failed. All failures were:\n- host: 'localhost', port: '5432', hostaddr: '::1': connection failed: connection to server at \"::1\", port 5432 failed: FATAL:  permission denied to s"
  },
  "physical": [
    0,
    0,
    null
  ],
  "clock_contexts": [],
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

### S07 — session quote_all_identifiers on

Public mode: `normal`; connection options: `-c quote_all_identifiers=on`.

Executed setup:

```sql
-- ordinary initialized v1; no forward DDL;
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables ['mneme_operation', 'mneme_record', 'mneme_schema', 'mneme_store'] are not schema version 1"
  },
  "physical": [
    0,
    0,
    null
  ],
  "clock_contexts": [],
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

Assessment correction/limit: Presentation-only false refusal on reused schema; S10 independently confirms it on untouched schema.

### S08 — session standard_conforming_strings off

Public mode: `normal`; connection options: `-c standard_conforming_strings=off`.

Executed setup:

```sql
-- ordinary initialized v1; no forward DDL;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

### S09 — session timezone Asia/Tokyo

Public mode: `normal`; connection options: `-c timezone=Asia/Tokyo`.

Executed setup:

```sql
-- ordinary initialized v1; no forward DDL;
```

Observed:

```json
{
  "open": "ACCEPT",
  "physical": [
    2,
    1,
    2
  ],
  "clock_contexts": [
    [
      "read committed",
      "off",
      "on",
      "ce04",
      "ce04"
    ]
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

### S10 — quote_all_identifiers on untouched fresh v1

Public mode: `normal`; connection options: `default unless special recipe above`.

Executed setup:

```sql
same untouched physical schema as B03; client quote_all_identifiers=on;
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables ['mneme_operation', 'mneme_record', 'mneme_schema', 'mneme_store'] are not schema version 1"
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04_fresh", "ce04_fresh", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

Assessment correction/limit: Definite false refusal: same untouched valid v1 as B03. Must accept, independent of C01 alternate-shape policy.

### S11 — SQL_ASCII client representation

Public mode: `normal`; connection options: `-c client_encoding=SQL_ASCII`.

Executed setup:

```sql
-- ordinary initialized v1; no forward DDL;
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables [b'mneme_operation', b'mneme_record', b'mneme_schema', b'mneme_store'] are not schema version 1"
  },
  "physical": [
    0,
    0,
    null
  ],
  "clock_contexts": [],
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

### X01 — search_path=ce04,ce04_other

Public mode: `normal`; connection options: `default unless special recipe above`.

Executed setup:

```sql
ce04,ce04_other;
```

Observed:

```json
{
  "open": "ACCEPT",
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {}
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

### X02 — search_path=ce04_other,ce04

Public mode: `normal`; connection options: `default unless special recipe above`.

Executed setup:

```sql
ce04_other,ce04;
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables ['mneme_record'] are not schema version 1"
  },
  "fingerprints": {}
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

### X03 — search_path=no_such_schema,ce04

Public mode: `normal`; connection options: `default unless special recipe above`.

Executed setup:

```sql
no_such_schema,ce04;
```

Observed:

```json
{
  "open": "ACCEPT",
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {}
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

### X04 — search_path=no_such_schema

Public mode: `normal`; connection options: `default unless special recipe above`.

Executed setup:

```sql
no_such_schema;
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "InvalidSchemaName",
    "sqlstate": "3F000",
    "code": null,
    "argument": null,
    "detail": "no schema has been selected to create in\nLINE 1: CREATE TABLE mneme_schema (singleton boolean PRIMARY KEY DEF...\n                     ^"
  },
  "fingerprints": {}
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

### X05 — search_path=ce04,pg_catalog

Public mode: `normal`; connection options: `default unless special recipe above`.

Executed setup:

```sql
ce04,pg_catalog;
```

Observed:

```json
{
  "open": "ACCEPT",
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {}
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

### X06 — format_type shadow before explicit pg_catalog

Public mode: `normal`; connection options: `default unless special recipe above`.

Executed setup:

```sql
CREATE ce04.format_type(oid,integer) which raises;
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "RaiseException",
    "sqlstate": "P0001",
    "code": null,
    "argument": null,
    "detail": "catalog shadow called\nCONTEXT:  PL/pgSQL function format_type(oid,integer) line 1 at RAISE"
  },
  "fingerprints": {}
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

### X07 — same function with implicit pg_catalog first

Public mode: `normal`; connection options: `default unless special recipe above`.

Executed setup:

```sql
same function; search_path ce04;
```

Observed:

```json
{
  "open": "ACCEPT",
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {}
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

### X08 — shadow renderer hides restrictive envelope domain

Public mode: `normal`; connection options: `default unless special recipe above`.

Executed setup:

```sql
CREATE DOMAIN probe_bytes AS bytea CHECK(octet_length(VALUE)<=10);
ALTER envelope TYPE probe_bytes;
format_type(oid,integer) returns bytea for domain OID; otherwise engine renderer;
search_path=ce04,pg_catalog;
```

Observed:

```json
{
  "open": "ACCEPT",
  "later": {
    "created": true,
    "failed_at": "commit",
    "error": {
      "exception": "CheckViolation",
      "sqlstate": "23514",
      "code": null,
      "argument": null,
      "detail": "value for domain probe_bytes violates check constraint \"probe_bytes_check\""
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04,pg_catalog", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
{"column_types": [["mneme_operation", "store_id", 25, "text"], ["mneme_operation", "source_namespace", 25, "text"], ["mneme_operation", "source_operation_id", 17, "bytea"], ["mneme_operation", "mutation", 17, "bytea"], ["mneme_operation", "first_position", 20, "bigint"], ["mneme_operation", "last_position", 20, "bigint"], ["mneme_operation", "recorded_at", 25, "text"], ["mneme_operation_pkey", "store_id", 25, "text"], ["mneme_operation_pkey", "source_namespace", 25, "text"], ["mneme_operation_pkey", "source_operation_id", 17, "bytea"], ["mneme_record", "store_id", 25, "text"], ["mneme_record", "position", 20, "bigint"], ["mneme_record", "record_id", 25, "text"], ["mneme_record", "profile", 25, "text"], ["mneme_record", "record_type", 25, "text"], ["mneme_record", "schema_version", 20, "bigint"], ["mneme_record", "envelope", 34268, "probe_bytes"], ["mneme_record_pkey", "store_id", 25, "text"], ["mneme_record_pkey", "position", 20, "bigint"], ["mneme_record_store_id_record_id_key", "store_id", 25, "text"], ["mneme_record_store_id_record_id_key", "record_id", 25, "text"], ["mneme_schema", "singleton", 16, "boolean"], ["mneme_schema", "version", 23, "integer"], ["mneme_schema_pkey", "singleton", 16, "boolean"], ["mneme_store", "store_id", 25, "text"], ["mneme_store", "tail", 20, "bigint"], ["mneme_store_pkey", "store_id", 25, "text"]]}
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

### X09 — advisory-lock helper shadow

Public mode: `normal`; connection options: `default unless special recipe above`.

Executed setup:

```sql
pg_advisory_xact_lock(bigint) replaced in ce04 by marker recording its own advisory-lock count;
search_path=ce04,pg_catalog;
```

Observed:

```json
{
  "open": "ACCEPT",
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {}
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

### X10 — lock-helper invocation observer

Public mode: `normal`; connection options: `default unless special recipe above`.

Executed setup:

```sql
SELECT lock_count FROM ce04.probe_marker after X09;
```

Observed:

```json
{
  "open": "SEE X09",
  "later": {
    "engine_advisory_locks_during_helper": [
      [
        0
      ]
    ]
  },
  "fingerprints": {}
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

Assessment correction/limit: Same open as X09; marker records zero genuine advisory locks. Independent observation, not another open.

### X11 — exact integer overload hides unsupported version

Public mode: `normal`; connection options: `default unless special recipe above`.

Executed setup:

```sql
UPDATE mneme_schema SET version=2;
CREATE ce04.array_agg(integer) RETURNS integer[] AS SELECT ARRAY[1];
search_path=ce04; pg_catalog implicit first; physical version remains 2;
```

Observed:

```json
{
  "open": "ACCEPT",
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

### D01 — database UTF8/POSIX/C

Public mode: `normal`; connection options: `default unless special recipe above`.

Executed setup:

```sql
CREATE DATABASE template0 UTF8/POSIX/C TABLESPACE mneme_ts;
```

Observed:

```json
{
  "setup_error": {
    "exception": "WrongObjectType",
    "sqlstate": "42809",
    "code": null,
    "argument": null,
    "detail": "invalid locale name: \"POSIX\""
  },
  "fingerprints": {}
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
```

Executed reversal:

```sql
DROP own database;
```

Assessment correction/limit: POSIX database locale construction refused on this Windows service; no open observation for that database.

### D02 — database SQL_ASCII/C/C

Public mode: `normal`; connection options: `default unless special recipe above`.

Executed setup:

```sql
CREATE DATABASE template0 SQL_ASCII/C/C TABLESPACE mneme_ts;
```

Observed:

```json
{
  "first_open": "ACCEPT",
  "open": "ERROR",
  "open_error": {
    "exception": "MnemeValidationError",
    "sqlstate": null,
    "code": "persistence.schema_incompatible",
    "argument": null,
    "detail": "persistence.schema_incompatible: mneme tables [b'mneme_operation', b'mneme_record', b'mneme_schema', b'mneme_store'] are not schema version 1"
  },
  "fingerprints": {
    "columns_match": false,
    "constraints_match": false
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["b'mneme_ce04_d9dadeac007b'", "b'public'", "b'\"$user\", public'", "b'14.12'", "b'SQL_ASCII'", "b'C'", "b'C'", "b'read committed'", "b'on'", "b'off'"]}
```

Executed reversal:

```sql
DROP own database;
```

Assessment correction/limit: Initialization returned successfully, but second open sees byte-valued text metadata and refuses; D05 controls client UTF8.

### D03 — database LATIN1/C/C

Public mode: `normal`; connection options: `default unless special recipe above`.

Executed setup:

```sql
CREATE DATABASE template0 LATIN1/C/C TABLESPACE mneme_ts;
```

Observed:

```json
{
  "first_open": "ACCEPT",
  "open": "ACCEPT",
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "unicode_equal": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_a8195e315f18", "public", "\"$user\", public", "14.12", "LATIN1", "C", "C", "read committed", "on", "off"]}
```

Executed reversal:

```sql
DROP own database;
```

Assessment correction/limit: Nonconforming LATIN1 database accepts and roundtrips full Unicode in bytea; this is not permission to relax Databases.

### D04 — database UTF8/C/POSIX

Public mode: `normal`; connection options: `default unless special recipe above`.

Executed setup:

```sql
CREATE DATABASE template0 UTF8/C/POSIX TABLESPACE mneme_ts;
```

Observed:

```json
{
  "setup_error": {
    "exception": "WrongObjectType",
    "sqlstate": "42809",
    "code": null,
    "argument": null,
    "detail": "invalid locale name: \"POSIX\""
  },
  "fingerprints": {}
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
```

Executed reversal:

```sql
DROP own database;
```

Assessment correction/limit: POSIX database locale construction refused on this Windows service; no open observation for that database.

### D05 — SQL_ASCII database with UTF8 client

Public mode: `unicode`; connection options: `default unless special recipe above`.

Executed setup:

```sql
same SQL_ASCII/C/C database as D02; client_encoding=UTF8;
```

Observed:

```json
{
  "open": "ACCEPT",
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "unicode_equal": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_d9dadeac007b", "public", "\"$user\", public", "14.12", "SQL_ASCII", "C", "C", "read committed", "on", "off"]}
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

Assessment correction/limit: Nonconforming SQL_ASCII database accepts with UTF8 client and full Unicode bytea roundtrip; policy C04.

### V01 — actual PostgreSQL version and rendered definitions

Public mode: `normal`; connection options: `default unless special recipe above`.

Executed setup:

```sql
SELECT version(), pg_get_constraintdef(oid,false/true);
```

Observed:

```json
{
  "open": "ACCEPT",
  "version": "PostgreSQL 14.12, compiled by Visual C++ build 1940, 64-bit",
  "renderers": [
    [
      "mneme_operation_pkey",
      "PRIMARY KEY (store_id, source_namespace, source_operation_id)",
      "PRIMARY KEY (store_id, source_namespace, source_operation_id)"
    ],
    [
      "mneme_operation_store_id_fkey",
      "FOREIGN KEY (store_id) REFERENCES mneme_store(store_id)",
      "FOREIGN KEY (store_id) REFERENCES mneme_store(store_id)"
    ],
    [
      "mneme_record_pkey",
      "PRIMARY KEY (store_id, \"position\")",
      "PRIMARY KEY (store_id, \"position\")"
    ],
    [
      "mneme_record_position_check",
      "CHECK (((\"position\" >= 1) AND (\"position\" <= '9007199254740991'::bigint)))",
      "CHECK (\"position\" >= 1 AND \"position\" <= '9007199254740991'::bigint)"
    ],
    [
      "mneme_record_store_id_fkey",
      "FOREIGN KEY (store_id) REFERENCES mneme_store(store_id)",
      "FOREIGN KEY (store_id) REFERENCES mneme_store(store_id)"
    ],
    [
      "mneme_record_store_id_record_id_key",
      "UNIQUE (store_id, record_id)",
      "UNIQUE (store_id, record_id)"
    ],
    [
      "mneme_schema_pkey",
      "PRIMARY KEY (singleton)",
      "PRIMARY KEY (singleton)"
    ],
    [
      "mneme_schema_singleton_check",
      "CHECK (singleton)",
      "CHECK (singleton)"
    ],
    [
      "mneme_store_pkey",
      "PRIMARY KEY (store_id)",
      "PRIMARY KEY (store_id)"
    ],
    [
      "mneme_store_tail_check",
      "CHECK (((tail >= 0) AND (tail <= '9007199254740991'::bigint)))",
      "CHECK (tail >= 0 AND tail <= '9007199254740991'::bigint)"
    ]
  ],
  "later": {
    "created": true,
    "receipt_range": [
      1,
      2
    ],
    "retry_equal": true,
    "tail": {
      "store_id": "s",
      "position": 2
    },
    "oracle": true,
    "read_positions": [
      1,
      2
    ],
    "through": {
      "store_id": "s",
      "position": 2
    },
    "read_tail": {
      "store_id": "s",
      "position": 2
    }
  },
  "fingerprints": {
    "columns_match": true,
    "constraints_match": true
  }
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
{"context": ["mneme_ce04_300d3debfc24", "ce04", "ce04", "14.12", "UTF8", "C", "C", "read committed", "on", "off"]}
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

Assessment correction/limit: Actual 14.12 positive control. Other release behavior unobserved.

### V02 — attempt server_version override

Public mode: `normal`; connection options: `default unless special recipe above`.

Executed setup:

```sql
connection option server_version=13.0;
```

Observed:

```json
{
  "open": "ERROR",
  "open_error": {
    "exception": "OperationalError",
    "sqlstate": null,
    "code": null,
    "argument": null,
    "detail": "connection failed: connection to server at \"127.0.0.1\", port 5432 failed: FATAL:  parameter \"server_version\" cannot be changed\nMultiple connection attempts failed. All failures were:\n- host: 'localhost', port: '5432', hostaddr: '::1': connection failed: connection to server at \"::1\", port 5432 failed: FATAL:  parameter \"server_version\" cannot be ch"
  },
  "fingerprints": {}
}
```

Catalog tuples (field order is defined in the execution section and SQL observer inventory below):

```json
```

Reversal: special-context finally block as specified above, or no DDL to reverse.

Assessment correction/limit: Server-version option is refused at startup; this is NOT execution on PostgreSQL 13.

## SQL observer inventory / tuple field order

Each catalog tuple follows these SELECT lists. Missing keys in older rows mean the observer was added later, not that the property was absent. Relation/attribute/index observations are restricted to the selected schema and its mneme_ relations; trigger/rule/constraint snapshots additionally show the fixture's auxiliary objects where applicable. OIDs are local evidence, not portable expected values.

```text
context: current_database, current_schema, search_path, server_version, server_encoding,
         lc_collate, lc_ctype, default_transaction_isolation, synchronous_commit,
         default_transaction_read_only
relations (pg_class): relname, relkind, relpersistence, relrowsecurity,
         relforcerowsecurity, reloptions, reltablespace, relowner
relation_flags (pg_class): relname, relhasindex, relhasrules, relhastriggers,
         relhassubclass, relreplident, relam
attributes (pg_attribute): relation name, attname, attnum, attisdropped,
         attidentity, attgenerated, attcollation, attstorage, attcompression
column_extra (pg_attribute): relation name, attname, atthasmissing, attmissingval,
         attndims, attacl, attoptions
column_types: relation name, attname, atttypid, pg_catalog.format_type(atttypid,atttypmod)
collations (pg_collation): collname, collprovider, collisdeterministic,
         collcollate, collctype, collversion, pg_collation_actual_version(oid)
constraints (pg_constraint): conname, contype, convalidated, condeferrable,
         condeferred, conislocal, coninhcount, pg_get_constraintdef(oid)
indexes (pg_index): index name, indisvalid, indisready, indislive,
         indisunique, indimmediate, indclass, indcollation, rendered predicate,
         rendered expression
inheritance (pg_inherits): child regclass, parent regclass
triggers (pg_trigger): tgname, tgenabled, tgisinternal
rules (pg_rewrite): rulename, ev_type, is_instead
clock_contexts (sample at real commit): transaction_isolation,
         transaction_read_only, synchronous_commit, current_schema, search_path
```

## Evidence and next checkpoint

Raw observations and drivers are project-local `.tmp/work/codex/ce04-01/`: `rows.jsonl`, `probe.py`, `cases.py`, `context.py`, `invalid-ready.py`, baseline catalog and per-probe logs. Credentials are absent from those committed excerpts. The SHA-256 inventory below binds the retained local driver/evidence to this artifact; it does not replace the inline recipes or elevate implementation fingerprints to an oracle.

- `rows.jsonl`: `a82ae1f1bac247c18275f181d8a116ed2e651625a6748c3be687516cbc396a9a`
- `probe.py`: `50c259a40bdfa89297b2a87781dba1f049f279adfc5a048b8e188ab60460c818`
- `cases.py`: `9b938ad6d9f2f36e67b6cf4392e42b4d119853bce47092866aef94bdb265c765`
- `context.py`: `0538840dccaccb114dc52765f3281255d43d9ce6931fc9a682d6909f31744f88`
- `invalid-ready.py`: `8875ebe75b7822e3b06c02cc8139c1f8c16f799fc57c05fc3118b87ae1ba7378`
- `baseline-catalog.json`: `67c0a16344f8ac1d986039bd877eca02a39e9653862736463e7d4c6f35cd6273`

All created throwaway databases were dropped after the characterization, with ordinary DROP of known own names and no FORCE or termination of foreign sessions. Production code and source bundle remain untouched. The host reservation remains respected; no POSIX suite, Docker batch or full mutant batch is claimed.

Claude must now challenge completeness and classify **every row**, retaining its actual executed state, plus decide whether C01..C06 need Owner routing. Construction-limited and alternate-version cells must remain bounded rather than being converted into imaginary passes. A separate Codex checkpoint review is required before any implementation. The episode stays on WP04-CR-008; no new out-of-episode finding or closure is declared here.


---

# Extension 2 — omitted live metadata and inbound linkage (CR-012/013)

**Status: characterization offered for classification; no revised checkpoint agreement, no production change.**

This extension starts at docs state `72fdc18ed9437ed4fa8efa51c55983a8c18c4745`, per the extension handoff and G-088..G-093. It preserves the preceding **136 historical rows against 63462513** verbatim. They are historical observations, not observations against today's reference. All E001..E112 below execute against frozen **be36323f56e61d87776d11c831ae1ef0573ea692**. CR-009..011 remain resolved and outside this episode. The accepted CR-012/013 witnesses, not Claude's response, motivate the two neighborhoods. CR-014 is evidence classification and needs a permanent direct fetch control, not a production fix.

There are **112 executed setup/public-outcome rows** in this extension, plus the per-property omission inventory and the catalog-route coverage ledger. Inventory cells reuse named executed snapshots; they are not independent mutation runs. Every current-behavior value comes from an execution. Proposed rejection oracles and potential semantic consequences are separately labelled. No physical/public observation is invented for a denied setup.

## Method and trust limits

Windows, project-managed CPython 3.12.8, psycopg 3.2.13, local PostgreSQL 14.12, non-superuser `mneme_dev` with CREATEDB. Six private throwaway databases, each `TEMPLATE template0 ENCODING 'UTF8' LC_COLLATE 'C' LC_CTYPE 'C' TABLESPACE mneme_ts`; all were dropped. Each setup gets a fresh initialized schema (no residue shared between E cells), except that E095 leaves an outside schema until database cleanup: E096 records the resulting duplicate-schema setup failure, and **E097 independently repeats that intended cross-namespace case successfully**. Ordinary-role statements commit individually; a failed statement stops further setup. Public open runs against the actual residual state. Namespace options are `search_path=<private schema>`, statement timeout 60s, lock timeout 2s. This is a serial small-schema characterization, not a credited G3/G4 gate run. No host reservation remains. No superuser credentials were read or used.

The public N protocol is the one specified above: public open, create s, commit r1/r2, identical retry, read since position 0, store_tail. Literal N oracle is positions 1/2, identical retry, read [1,2], through/tail 2, canonical stamped records preserved. Cache cells create `old` through the API before closing and doing pre-open DDL; they then append to `old`. The evidence records the actual receipt/page, not merely successful SQL. Predicate-domain cells attempt a catalog edit with the ordinary role, record 42501 and actual unchanged public N. Their **altered-state public result is NOT EXECUTED**. A proposed future predicate oracle must not cite these as physical kills.

Full scratch evidence is `.tmp/work/codex/ce04-extension/`: six `rowsN.json` files (full before/after pg_attribute, pg_class, pg_index, inbound dependencies, triggers, publications and annotations), `inventory.json`, engine and cleanup records, and the six drivers embedded below. These paths are local evidence; the setup recipes, literal differences and public observations needed to reproduce the cases are committed here. Catalog OIDs in observations are runtime identities, not expected constants.

## What the neighborhood changes

1. **Live missing-value caches are a decided rejection, including harmless-looking caches.** E002 has live tail cache `{1}` and returns old tail 1, first/last 2/3, read [2,3]; metadata fetch reports no mismatch. E003 caches `{0}` and happens to satisfy N; E006 caches schema version `{1}` and also satisfies N. They still differ from the strict live v1 catalog. E005 caches version `{2}`: the header-row check catches it even though catalog fetch does not. The header check is not a substitute for the cache check.
2. **Cache metadata versus stored rows must stay distinct.** E004's VACUUM FULL clears the cache and physically materializes the pre-open row value 1. Its catalog is compatible, but the old row remains wrong. G-092 explicitly excludes a stored-row audit at open. Do not claim that a cache guard can repair or detect all prior direct row changes; do not turn E004 into a new row-scanning requirement.
3. **Outside constraint references are not foreign-key-only.** E028/E050..052/E097 bind each of the four tables through `tgconstrrelid` while the outside trigger's `pg_constraint.confrelid` is 0. All public opens accept; published no-outside-constraint rule requires rejection. E027/E043/E053..055/E095 prove that genuine inbound foreign keys are still detected, including another namespace.
4. **An OID-shaped field can encode a semantic association.** Object identity is exempt, but a wrong type/file/TOAST/namespace binding is not made harmless by omitting its OID. The inventory distinguishes identity from consistency invariants; the denied catalog edits do not establish corrupt-state behavior.
5. **Inbound means more than dependency rows to pg_class.** E030..040/E057..061/E088 use row types, their array/domain/range closure, stored expressions, functions, operators, aggregates and casts. E062 binds a core table to an extension in the outgoing dependency direction. The route ledger separates explicit class pointers, object-address catalogs, dependency graph closure, and names embedded in unevaluated function bodies. No finite pg_depend query can certify arbitrary dynamic SQL harmless.

## Candidate path-C packet (not choices)

Each item is **REQUIREMENT_UNCERTAIN; owner_decision_required: true** if it cannot be discharged by a cited existing rule. No item silently widens admission. Claude should classify every individual row and distinguish decided strict rejection from a requested exemption.

| ID | Question and proposed boundary to decide | Executed anchors |
|---|---|---|
| EC01 | Does strict v1 prohibit outside views/materialized views, sequences OWNED BY core columns, publications, stored SQL routines, functions/aggregates/operators/casts/domains/ranges over core row types, and extension membership, or only outside objects that vary the specified core catalog/effects? The prefix-based relation rule allows an unrelated outside table (E056); it does not explicitly give an oracle for every auxiliary binding. Decide per route, not blanket all-dependencies rejection or blanket N-pass equivalence. Include transitive row-type dependencies and publication FOR ALL TABLES. | E021..025, E030..033, E036..040, E042, E057..062, E088/E093; E026 is privilege-limited |
| EC02 | Does “No constraint outside the four tables references them” include row-type references in an outside CHECK/domain/constraint-trigger WHEN, not just direct table-reference fields? Proposed strict reading rejects such constraints, but the table-vs-row-type distinction needs an explicit normative resolution. This does **not** reopen the decided direct FROM trigger rejection. | E035, E103 actual domain CHECK, E094; controls E028/E050..052/E097 |
| EC03 | State the equivalence oracle for genuine engine-maintained bookkeeping: stale relhas* flags, vacuum/freeze horizons, physical file identity, and indcheckxmin HOT-safety state. Some can change under genuine operations, are not literal initializer values, and are not all explicitly “planner statistics”. Proposed rule: validate effective catalog objects/consistency, allow genuine maintenance progress; reject inconsistent semantic bindings via predicate-domain controls. This proposal is not an adopted exemption. | E011..016, E085; baseline all fields in inventory |
| EC04 | Are security labels allowed annotations, or must unknown/effectful provider bindings be refused? A security label can belong to a provider that enforces policy; comments/ACL evidence cannot establish it harmless. No provider is installed for this probe, and no provider was installed to manufacture a public execution. | E019 22023, E099 42501; baseline labels absent |
| EC05 | Are comments a permitted non-semantic annotation under G-089, or does the published finite-state comparison require their absence? They are not named in its exception list. Public N is unchanged; this is evidence of behavior, not authority to add an exemption. Initial privileges/ACLs are separately covered by the grants exception. | E018; E017 grants control; E098 initial-privilege construction limit |

These are characterization questions, not newly adjudicated CR findings. CR-012 and CR-013 remain open pending the revised checkpoint and implementation. No new formal finding number is assigned here; the packet prevents undocumented implementation choices.

## Complete live-property inventory

The inventory was obtained by querying `pg_attribute` of `pg_attribute`, `pg_class` and `pg_index` in this PG14.12 engine, rather than guessing columns from the response. Fetch coverage was then read from the frozen QUERIES and joins/filters. A field used only to locate/filter/map an object is marked **READ/route**, not a compared value. Index pg_attribute rows are entirely omitted by the current fetch. “DERIVED” means genuine engine state can constrain the value, not that pre-open corrupt metadata has been executed or may be ignored. “PREDICATE” requires a constructed fetch-binding/comparison control in the future, not a public test pretending to edit an inaccessible catalog.

Every omission row below has executed setup **E001: fresh public initialization**, observed distinct values across **all four tables or all five attached indexes**, and actual public outcome **ACCEPT; N**. Relevant changed-state executions are named in its rule. Shared baseline observations are explicitly shared, not credited as independent variation tests. Full raw rows also cover negative system attributes (`ctid`, `xmin`, `cmin`, `xmax`, `cmax`, `tableoid`) of the four heaps: their genuine engine definition is not user-tunable; consistency belongs to the predicate domain, never a requirement to match physical user-column order. Dropped positive attributes are separately exempt E013; a missing or corrupt live/system attribute is not dropped residue.

| Inventory | Catalog / scope | Omitted property | E001 actual distinct values | Proposed class and semantic consequence / witness |
|---|---|---|---|---|
| O001 | pg_attribute / table | `attstattarget` | ["-1"] | **EXEMPT** — Planner-statistics exception. Table target 300 constructed E007; simple index target refused E008 (not an expression index); E107 successfully sets expression-index target 300, but the extra index itself is incompatible. |
| O002 | pg_attribute / table | `attlen` | ["-1","1","4","8"] | **PREDICATE** — Copied type representation can affect tuple decoding. Require consistency with the admitted built-in type, not a cross-architecture hardcoded byte size. E066 is a denied edit, not an altered-state test. |
| O003 | pg_attribute / table | `attcacheoff` | ["-1"] | **PREDICATE** — Stored catalog value -1; in-memory offset cache is different. Corrupt stored offset can affect tuple decoding. E067 denied; no physical corrupt-state execution. |
| O004 | pg_attribute / table | `attbyval` | ["false","true"] | **PREDICATE** — Copied type pass-by-value representation affects datum decoding; require consistency with actual admitted pg_type. E068 denied. |
| O005 | pg_attribute / table | `attalign` | ["\"c\"","\"d\"","\"i\""] | **PREDICATE** — Copied type alignment affects tuple decoding; consistency with actual built-in type, E069 denied. |
| O006 | pg_attribute / table | `atthasmissing` | ["false"] | **REJECT** — Live fast-default cache is semantic, not dropped-column residue. Initializer false; E002/E003/E006 true are strict rejections even where N happens to pass. |
| O007 | pg_attribute / table | `attacl` | ["null"] | **EXEMPT** — Ownership/grants exception; E017 changes table/column ACL while N still succeeds. Privilege denial remains an engine error, not a schema error. |
| O008 | pg_attribute / table | `attoptions` | ["null"] | **EXEMPT** — PG14 heap options n_distinct and n_distinct_inherited are planner statistics; E007 constructed both. Index ALTER syntax failed E009; no changed index-options result claimed. |
| O009 | pg_attribute / table | `attfdwoptions` | ["null"] | **PREDICATE** — Foreign-column behavior is not an admitted heap/btree feature. Baseline NULL; heap OPTIONS attempt E010 wrong-object type; direct edit E070 denied. A non-NULL genuine foreign attribute requires an already incompatible relation kind. |
| O010 | pg_attribute / table | `attmissingval` | ["null"] | **REJECT** — Must have no active missing-value cache; E002 {1}, E003 {0}, E006 {1}. Do not treat live caches as exempt residue. Dormant non-NULL with flag false is predicate-domain, E071 did not construct it. |
| O011 | pg_attribute / index | `attrelid` | ["\"217182\"","\"217191\"","\"217199\"","\"217201\"","\"217213\""] | **IDENTITY** — Object address; resolve correct index/table association, never pin an OID. |
| O012 | pg_attribute / index | `attname` | ["\"position\"","\"record_id\"","\"singleton\"","\"source_namespace\"","\"source_operation_id\"","\"store_id\""] | **IDENTITY** — Index attribute naming is not its key semantics; core table names remain required. Resolve keys through indkey. |
| O013 | pg_attribute / index | `atttypid` | ["\"16\"","\"17\"","\"20\"","\"25\""] | **DERIVED** — Index storage type must be consistent with genuine btree/opclass and source key; not an arbitrary type OID equality. |
| O014 | pg_attribute / index | `attstattarget` | ["-1"] | **EXEMPT** — Planner-statistics exception. Table target 300 constructed E007; simple index target refused E008 (not an expression index); E107 successfully sets expression-index target 300, but the extra index itself is incompatible. |
| O015 | pg_attribute / index | `attlen` | ["-1","1","8"] | **PREDICATE** — Copied type representation can affect tuple decoding. Require consistency with the admitted built-in type, not a cross-architecture hardcoded byte size. E066 is a denied edit, not an altered-state test. |
| O016 | pg_attribute / index | `attnum` | ["1","2","3"] | **IDENTITY** — Table physical order is exempt. Index key order is semantic through indkey; attribute-address numbers identify the actual index tuple. |
| O017 | pg_attribute / index | `attndims` | ["0"] | **DERIVED** — No array index keys in v1; native scalar storage expected 0. Engine-derived / altered inconsistency is predicate-domain. |
| O018 | pg_attribute / index | `attcacheoff` | ["-1"] | **PREDICATE** — Stored catalog value -1; in-memory offset cache is different. Corrupt stored offset can affect tuple decoding. E067 denied; no physical corrupt-state execution. |
| O019 | pg_attribute / index | `atttypmod` | ["-1"] | **DERIVED** — Index storage typmod follows admitted source keys; no typmod in v1. Inconsistent metadata is predicate-domain. |
| O020 | pg_attribute / index | `attbyval` | ["false","true"] | **PREDICATE** — Copied type pass-by-value representation affects datum decoding; require consistency with actual admitted pg_type. E068 denied. |
| O021 | pg_attribute / index | `attalign` | ["\"c\"","\"d\"","\"i\""] | **PREDICATE** — Copied type alignment affects tuple decoding; consistency with actual built-in type, E069 denied. |
| O022 | pg_attribute / index | `attstorage` | ["\"p\"","\"x\""] | **DERIVED** — Index storage comes from genuine btree/source type; no public independent tuning established here. Table tuning is already fetched and strict. |
| O023 | pg_attribute / index | `attcompression` | ["\"\""] | **DERIVED** — Index baseline empty; heap-column compression already fetched. Altered inconsistent index storage is predicate-domain. |
| O024 | pg_attribute / index | `attnotnull` | ["false"] | **DERIVED** — Index baseline false even for primary keys; do NOT impose table NOT NULL on index attributes. Constraints enforce table nullability. |
| O025 | pg_attribute / index | `atthasdef` | ["false"] | **DERIVED** — No index defaults; ordinary default ALTER applies to table, not a separate index expression default. Predicate-domain inconsistency. |
| O026 | pg_attribute / index | `atthasmissing` | ["false"] | **REJECT** — Live fast-default cache is semantic, not dropped-column residue. Initializer false; E002/E003/E006 true are strict rejections even where N happens to pass. |
| O027 | pg_attribute / index | `attidentity` | ["\"\""] | **DERIVED** — No identity index attributes; source-column identity already fetched. Predicate-domain inconsistency. |
| O028 | pg_attribute / index | `attgenerated` | ["\"\""] | **DERIVED** — No generated index attributes; index expressions and source generated flags are independently fetched. Predicate-domain inconsistency. |
| O029 | pg_attribute / index | `attisdropped` | ["false"] | **DERIVED** — Dropped table residue is exempt. A v1 index key cannot silently be a dropped attribute; distinguish valid dropped heap residue from index-key corruption. |
| O030 | pg_attribute / index | `attislocal` | ["true"] | **DERIVED** — Local index attributes; genuine ancestry linked through pg_inherits and source keys. Predicate-domain inconsistent state. |
| O031 | pg_attribute / index | `attinhcount` | ["0"] | **DERIVED** — Index attribute baseline 0; actual partition/inheritance links already rejected. Predicate-domain inconsistent state. |
| O032 | pg_attribute / index | `attcollation` | ["\"0\"","\"100\""] | **DERIVED** — Index tuple metadata must agree with key/opclass/collation state; fetched indcollation does not directly read the index pg_attribute copy. |
| O033 | pg_attribute / index | `attacl` | ["null"] | **EXEMPT** — Ownership/grants exception; E017 changes table/column ACL while N still succeeds. Privilege denial remains an engine error, not a schema error. |
| O034 | pg_attribute / index | `attoptions` | ["null"] | **EXEMPT** — PG14 heap options n_distinct and n_distinct_inherited are planner statistics; E007 constructed both. Index ALTER syntax failed E009; no changed index-options result claimed. |
| O035 | pg_attribute / index | `attfdwoptions` | ["null"] | **PREDICATE** — Foreign-column behavior is not an admitted heap/btree feature. Baseline NULL; heap OPTIONS attempt E010 wrong-object type; direct edit E070 denied. A non-NULL genuine foreign attribute requires an already incompatible relation kind. |
| O036 | pg_attribute / index | `attmissingval` | ["null"] | **REJECT** — Must have no active missing-value cache; E002 {1}, E003 {0}, E006 {1}. Do not treat live caches as exempt residue. Dormant non-NULL with flag false is predicate-domain, E071 did not construct it. |
| O037 | pg_class / table | `reltype` | ["\"217179\"","\"217186\"","\"217195\"","\"217210\""] | **DERIVED** — Table composite row-type OID is identity but genuine backlink/type association matters. Index baseline 0. External row-type dependents are separate route decisions below. |
| O038 | pg_class / table | `relowner` | ["\"16901\""] | **EXEMPT** — Explicit ownership/grants exception, not a shape mismatch. |
| O039 | pg_class / table | `relfilenode` | ["\"217177\"","\"217184\"","\"217193\"","\"217208\""] | **IDENTITY** — Physical file identity changes under REINDEX/VACUUM FULL E012; no fixed equality. A invalid file binding is not equivalent merely because the field is OID-shaped. |
| O040 | pg_class / table | `relpages` | ["0"] | **EXEMPT** — Planner size estimate; E011 VACUUM/ANALYZE changes statistics. No equality to initialization size. |
| O041 | pg_class / table | `reltuples` | ["-1"] | **EXEMPT** — Planner row-count estimate, never a row audit or equality to initial -1. |
| O042 | pg_class / table | `relallvisible` | ["0"] | **EXEMPT** — Planner estimate of visibility-map coverage. Catalog estimate is not the visibility map itself. |
| O043 | pg_class / table | `relhasindex` | ["true"] | **BOOKKEEPING** — Lazy hint, actual indexes must decide semantics. v1 tables have indexes; false while indexes exist is inconsistent, true after dropping extras is harmless. E047 rejects actual extra index. |
| O044 | pg_class / table | `relisshared` | ["false"] | **PREDICATE** — Core user relations and indexes must not be shared catalogs. E072 denied edit; no shared-state public run. |
| O045 | pg_class / table | `relnatts` | ["2","7"] | **DERIVED** — Count includes dropped heap residue, so literal initial heap count is wrong after E013. Index count must agree with indnatts and actual index tuple layout. |
| O046 | pg_class / table | `relchecks` | ["0","1"] | **DERIVED** — Summary must be consistent with actual checks, not a replacement for them. Index expected 0. E084 denied edit. |
| O047 | pg_class / table | `relhasrules` | ["false"] | **BOOKKEEPING** — Lazy summary can remain true after removal; E015 constructs residue. Actual pg_rewrite rows are what affect writes. EC03 asks how to express allowed bookkeeping. |
| O048 | pg_class / table | `relhastriggers` | ["false","true"] | **BOOKKEEPING** — Lazy summary can remain true after removal; E014 constructs residue on schema table. Actual triggers must decide effects. |
| O049 | pg_class / table | `relhassubclass` | ["false"] | **BOOKKEEPING** — E016 constructs stale true after child drop. Actual pg_inherits rows must reject live inheritance; E029 control. |
| O050 | pg_class / table | `relispopulated` | ["true"] | **PREDICATE** — True for genuine ordinary tables/indexes; false applies to unpopulated materialized views. E073 denied edit. Wrong relkind already rejects genuine matview substitution. |
| O051 | pg_class / table | `relrewrite` | ["\"0\""] | **PREDICATE** — Committed user-visible value 0; nonzero rewrite state is transient engine-internal, not arbitrary identity. E074 denied edit. Genuine rewrite E012 succeeds with 0 afterwards. |
| O052 | pg_class / table | `relfrozenxid` | ["\"51278\""] | **BOOKKEEPING** — Live vacuum/freeze horizon, changes under E011, impacts wraparound maintenance; not a schema-version fingerprint. EC03: genuine progress versus inconsistent predicate-domain state. |
| O053 | pg_class / table | `relminmxid` | ["\"1\""] | **BOOKKEEPING** — Live multixact freeze horizon, not fixed initialization identity. Index baseline 0. EC03 distinguishes engine progress from inconsistent values. |
| O054 | pg_class / table | `relacl` | ["null"] | **EXEMPT** — Explicit grants exception. E017 public N succeeds. |
| O055 | pg_class / table | `relpartbound` | ["null"] | **PREDICATE** — NULL in v1; partition-bound tree is semantically significant when partitioned. E045 actual attach rejects, E075 denied inconsistent index edit. |
| O056 | pg_class / index | `relname` | ["\"mneme_operation_pkey\"","\"mneme_record_pkey\"","\"mneme_record_store_id_record_id_key\"","\"mneme_schema_pkey\"","\"mneme_store_pkey\""] | **IDENTITY** — Four core table names are required; index/constraint names are exempt. E046 renames index and N succeeds. |
| O057 | pg_class / index | `relnamespace` | ["\"217176\""] | **IDENTITY** — Resolve namespace at open and genuine attached indexes; compare association, not namespace OID. |
| O058 | pg_class / index | `reltype` | ["\"0\""] | **DERIVED** — Table composite row-type OID is identity but genuine backlink/type association matters. Index baseline 0. External row-type dependents are separate route decisions below. |
| O059 | pg_class / index | `reloftype` | ["\"0\""] | **PREDICATE** — Index baseline 0; inconsistent typed index not a genuine btree. Table typed state already fetched. E079 denies an index edit. |
| O060 | pg_class / index | `relowner` | ["\"16901\""] | **EXEMPT** — Explicit ownership/grants exception, not a shape mismatch. |
| O061 | pg_class / index | `relfilenode` | ["\"217182\"","\"217191\"","\"217199\"","\"217201\"","\"217213\""] | **IDENTITY** — Physical file identity changes under REINDEX/VACUUM FULL E012; no fixed equality. A invalid file binding is not equivalent merely because the field is OID-shaped. |
| O062 | pg_class / index | `relpages` | ["1"] | **EXEMPT** — Planner size estimate; E011 VACUUM/ANALYZE changes statistics. No equality to initialization size. |
| O063 | pg_class / index | `reltuples` | ["0"] | **EXEMPT** — Planner row-count estimate, never a row audit or equality to initial -1. |
| O064 | pg_class / index | `relallvisible` | ["0"] | **EXEMPT** — Planner estimate of visibility-map coverage. Catalog estimate is not the visibility map itself. |
| O065 | pg_class / index | `reltoastrelid` | ["\"0\""] | **DERIVED** — TOAST pointer OID is identity, but association/genuine storage is not arbitrary. Table fetch reads pointer only to inspect TOAST options. Index expected 0; pre-open corrupt pointer is predicate-domain. |
| O066 | pg_class / index | `relhasindex` | ["false"] | **BOOKKEEPING** — Lazy hint, actual indexes must decide semantics. v1 tables have indexes; false while indexes exist is inconsistent, true after dropping extras is harmless. E047 rejects actual extra index. |
| O067 | pg_class / index | `relisshared` | ["false"] | **PREDICATE** — Core user relations and indexes must not be shared catalogs. E072 denied edit; no shared-state public run. |
| O068 | pg_class / index | `relpersistence` | ["\"p\""] | **PREDICATE** — Indexes must share durable permanent storage with admitted parent, not independent unlogged/temporary storage. E077 denied edit; table persistence already checked. |
| O069 | pg_class / index | `relkind` | ["\"i\""] | **PREDICATE** — Attached indexes must be genuine ordinary indexes, not partitioned/other relkind. E076 denied edit; indrelid alone is not an explicit class-kind check. |
| O070 | pg_class / index | `relnatts` | ["1","2","3"] | **DERIVED** — Count includes dropped heap residue, so literal initial heap count is wrong after E013. Index count must agree with indnatts and actual index tuple layout. |
| O071 | pg_class / index | `relchecks` | ["0"] | **DERIVED** — Summary must be consistent with actual checks, not a replacement for them. Index expected 0. E084 denied edit. |
| O072 | pg_class / index | `relhasrules` | ["false"] | **BOOKKEEPING** — Lazy summary can remain true after removal; E015 constructs residue. Actual pg_rewrite rows are what affect writes. EC03 asks how to express allowed bookkeeping. |
| O073 | pg_class / index | `relhastriggers` | ["false"] | **BOOKKEEPING** — Lazy summary can remain true after removal; E014 constructs residue on schema table. Actual triggers must decide effects. |
| O074 | pg_class / index | `relhassubclass` | ["false"] | **BOOKKEEPING** — E016 constructs stale true after child drop. Actual pg_inherits rows must reject live inheritance; E029 control. |
| O075 | pg_class / index | `relrowsecurity` | ["false"] | **PREDICATE** — Index baseline false, heap RLS checked already. E080 denied index flag edit; inconsistent flags not a public RLS construction. |
| O076 | pg_class / index | `relforcerowsecurity` | ["false"] | **PREDICATE** — Index false; heap checked. E081 denied index edit. |
| O077 | pg_class / index | `relispopulated` | ["true"] | **PREDICATE** — True for genuine ordinary tables/indexes; false applies to unpopulated materialized views. E073 denied edit. Wrong relkind already rejects genuine matview substitution. |
| O078 | pg_class / index | `relreplident` | ["\"n\""] | **PREDICATE** — Index class baseline n, heap class d. Do not copy heap expected value onto indexes. E082 denied edit. |
| O079 | pg_class / index | `relispartition` | ["false"] | **PREDICATE** — False for v1 indexes, genuine partition attachment rejected through parent/class/inherits. E078 denied inconsistent flag. |
| O080 | pg_class / index | `relrewrite` | ["\"0\""] | **PREDICATE** — Committed user-visible value 0; nonzero rewrite state is transient engine-internal, not arbitrary identity. E074 denied edit. Genuine rewrite E012 succeeds with 0 afterwards. |
| O081 | pg_class / index | `relfrozenxid` | ["\"0\""] | **BOOKKEEPING** — Live vacuum/freeze horizon, changes under E011, impacts wraparound maintenance; not a schema-version fingerprint. EC03: genuine progress versus inconsistent predicate-domain state. |
| O082 | pg_class / index | `relminmxid` | ["\"0\""] | **BOOKKEEPING** — Live multixact freeze horizon, not fixed initialization identity. Index baseline 0. EC03 distinguishes engine progress from inconsistent values. |
| O083 | pg_class / index | `relacl` | ["null"] | **EXEMPT** — Explicit grants exception. E017 public N succeeds. |
| O084 | pg_class / index | `relpartbound` | ["null"] | **PREDICATE** — NULL in v1; partition-bound tree is semantically significant when partitioned. E045 actual attach rejects, E075 denied inconsistent index edit. |
| O085 | pg_index / index | `indcheckxmin` | ["false"] | **BOOKKEEPING** — HOT-chain safety gate on index use; false baseline. True can temporarily suppress reads using index without dropping constraints. E085 denied edit. EC03 requires a stated oracle for genuine safety state, not arbitrary true=harmless or false=valid. |

There are **85 omitted-field inventory rows**. The following coverage map accounts for all catalog columns, including those already read; it is not another set of executions.

| Catalog / scope | Columns already read or routed through fetch | Columns omitted |
|---|---|---|
| pg_attribute / table | `attrelid`, `attname`, `atttypid`, `attnum`, `attndims`, `atttypmod`, `attstorage`, `attcompression`, `attnotnull`, `atthasdef`, `attidentity`, `attgenerated`, `attisdropped`, `attislocal`, `attinhcount`, `attcollation` | `attstattarget`, `attlen`, `attcacheoff`, `attbyval`, `attalign`, `atthasmissing`, `attacl`, `attoptions`, `attfdwoptions`, `attmissingval` |
| pg_attribute / index |  | `attrelid`, `attname`, `atttypid`, `attstattarget`, `attlen`, `attnum`, `attndims`, `attcacheoff`, `atttypmod`, `attbyval`, `attalign`, `attstorage`, `attcompression`, `attnotnull`, `atthasdef`, `atthasmissing`, `attidentity`, `attgenerated`, `attisdropped`, `attislocal`, `attinhcount`, `attcollation`, `attacl`, `attoptions`, `attfdwoptions`, `attmissingval` |
| pg_class / table | `oid`, `relname`, `relnamespace`, `reloftype`, `relam`, `reltablespace`, `reltoastrelid`, `relpersistence`, `relkind`, `relrowsecurity`, `relforcerowsecurity`, `relreplident`, `relispartition`, `reloptions` | `reltype`, `relowner`, `relfilenode`, `relpages`, `reltuples`, `relallvisible`, `relhasindex`, `relisshared`, `relnatts`, `relchecks`, `relhasrules`, `relhastriggers`, `relhassubclass`, `relispopulated`, `relrewrite`, `relfrozenxid`, `relminmxid`, `relacl`, `relpartbound` |
| pg_class / index | `oid`, `relam`, `reltablespace`, `reloptions` | `relname`, `relnamespace`, `reltype`, `reloftype`, `relowner`, `relfilenode`, `relpages`, `reltuples`, `relallvisible`, `reltoastrelid`, `relhasindex`, `relisshared`, `relpersistence`, `relkind`, `relnatts`, `relchecks`, `relhasrules`, `relhastriggers`, `relhassubclass`, `relrowsecurity`, `relforcerowsecurity`, `relispopulated`, `relreplident`, `relispartition`, `relrewrite`, `relfrozenxid`, `relminmxid`, `relacl`, `relpartbound` |
| pg_index / index | `indexrelid`, `indrelid`, `indnatts`, `indnkeyatts`, `indisunique`, `indisprimary`, `indisexclusion`, `indimmediate`, `indisclustered`, `indisvalid`, `indisready`, `indislive`, `indisreplident`, `indkey`, `indcollation`, `indclass`, `indoption`, `indexprs`, `indpred` | `indcheckxmin` |


## Inbound route coverage ledger

E049 executes `pg_get_catalog_foreign_keys()` and E086 inventories every PG14 catalog column. The foreign-key metadata is a **route-discovery aid**, not a sufficient validator: polymorphic `objoid/objid` addresses and body text are not an ordinary FK, `classoid/classid` identifies the catalog rather than the target table, and row-type references target `pg_type`, not `pg_class`. All discovered class/type/attribute route families are assigned below, including non-applicable ones. Dependency closure follows genuine object addresses, including the core tables' internally owned composite/array types, indexes and constraints; an unqualified “any dependency is forbidden” query would falsely reject that baseline. Index ownership and dependency direction matter.

| Route family / actual catalog entry points | Executed setup and observation source | Current actual public outcome / proposed oracle |
|---|---|---|
| Constraint direct binding: conrelid/confrelid, conkey/confkey, conindid | E027/E043/E053..055/E095 outside FKs; E028/E050..052/E097 outside FROM constraint triggers, with actual constraint and trigger linkage in deltas | FK rejected; FROM accepted incorrectly. Strict rejection is already decided. An attached index's external constraint binding also belongs here; numeric names/OIDs are exempt, endpoint identity is not. |
| Trigger direct binding: tgrelid/tgconstrrelid/tgconstrindid/tgattr; WHEN expression dependencies | E028/E041/E050..052/E094/E097 | Core-owned trigger rejected; outside FROM accepted incorrectly; indirect row-type WHEN accepted, EC02. No outside-index-only corrupt trigger was physically manufactured. |
| Rewrite rule ev_class + action/qualification dependency trees: views and materialized views | E021/E022/E023; direct core rule residue E015 | Outside bindings accepted, EC01; actual core rules already fetched. Do not confuse rule owner with tables in its action. |
| Inheritance/partitioning: pg_inherits both ends; pg_partitioned_table partrelid/partdefid/partattrs | E029 child; E045 core attached as outside parent's default partition | Both rejected. E016 dropped child leaves lazy flag only. |
| Sequence OWNED BY via pg_depend; pg_sequence seqrelid/seqtypid | E024 creates ownership edge to tail; E090 cannot use composite as sequence type | Ownership accepted, EC01; failed type construction only baseline accepted. Integer sequence's owner-column link is a dependency, not seqrelid pointing at the core table. |
| Publication prrelid and puballtables (no per-relation edge for all-tables) | E025 FOR TABLE accepted, actual membership captured; E026 FOR ALL TABLES denied 42501 | EC01; E026 public result is baseline N, **not** all-tables evidence. No replication worker was started. |
| Subscription srrelid | E064 disabled/nonconnecting subscription denied before creation; E100 direct binding edit denied | Predicate-domain admission question EC01; no subscriber, slot, network connection or replication effect was manufactured. |
| Statistics starelid/staattnum, stxrelid/stxkeys; statistic_ext_data transitively | E007/E011 ANALYZE, E020 extended statistics | ACCEPT N; explicit planner-statistics exception. No blanket pg_depend rejection may accidentally reject this. |
| Table/type/attribute association: pg_type typrelid/typelem/typarray/typbasetype; pg_class reltype/reloftype; pg_attribute atttypid; pg_enum enumtypid | E030 row-type column; E039/E057 domain/array chain; E040 array view; E044 standalone typed-table rejection | External row types accepted EC01/EC02. Genuine core composite is not an enum, so enumtypid naming it is a predicate-domain inconsistency, not a constructible ENUM route. Baseline composite/array associations are required internal identity. |
| Range rngsubtype/rngtypid/rngmultitypid | E088/E108 **successfully** creates range over mneme_store (despite driver's starting “construction limit” label); pg_type dependency recorded | ACCEPT N; EC01. Do not infer that composite subtype is impossible. |
| Defaults/generated expressions adrelid/adnum + pg_depend to type/function/relation | E034/E036 | Outside expressions accepted EC01. Core defaults are already checked. Domain/array intermediates must be considered transitively. |
| CHECK/domain constraints contypid/conrelid + conbin dependencies | E035/E039/E057/E103 | ACCEPT N, EC02; core CHECKs already checked. |
| Policies polrelid + expression dependencies | E038 outside policy row-type expression | ACCEPT N, EC01; existing core-policy prohibition remains. |
| Index indrelid/indexrelid/indkey + expression/predicate dependencies | E037 outside expression index over core row type; E047 extra core index | Outside expression index accepted EC01; actual extra attached core index rejected. No legitimate predicate/index expression directly selects a table via a subquery. |
| Routines proargtypes/proallargtypes/prorettype/provariadic/protrftypes and stored SQL body | E031/E058/E104/E105 type signatures, E032 stored SQL function, E093 procedure; E092 absent transform refused | Accepted EC01; failed transform only baseline N. Array/INOUT/variadic signatures are same type-address route, not a new kind of table pointer. |
| Aggregate aggtranstype/aggmtranstype and functions; operator oprleft/oprright/oprresult; cast castsource/casttarget | E059/E060/E061/E106, dependency closure in second batch | ACCEPT N, EC01. Genuine relation row-type identities reach these objects through pg_type. |
| Operator-class/family opcintype/opckeytype, amopleft/righttype, amprocleft/righttype; transforms trftype | E089 opclass creation denied superuser requirement; E092/E101 transform construction limits | Predicate-domain, no changed-state public claim. They can point to a row type through type addresses and functions; core indexes already require built-in opclasses. |
| Extension membership and extconfig | E062/E109 ordinary role creates trusted hstore then ADD TABLE mneme_store: actual outgoing pg_depend e binding; E087 config-dump call outside extension script refused | Membership ACCEPT N; EC01. extconfig is a separate class-array route; failed E087 is not absence under every extension script. |
| Event triggers / string SQL / dynamic SQL / foreign-server options | E063 event trigger requires superuser; E033 SQL string body, E042 outside trigger whose PL/pgSQL body names core; E091 absent foreign server | Strings can name a table without a pg_depend edge. Actual E033/E042 ACCEPT N; EC01 trust boundary must say whether arbitrary outside code is relevant. No engine-wide event trigger or foreign server was installed. Enumerating body text is not a proof of semantics. |
| Foreign-table ftrelid; rewrite relrewrite; TOAST reltoastrelid | E065 catalog edit denied; E010 heap OPTIONS refused; E012 genuine rewrite baseline afterwards | These are core structural bindings/engine-internal states, not legitimate outside objects directly pointing at a heap through ftrelid. Wrong class kind already rejects genuine foreign substitution. Inconsistent pre-open pointers are predicate-domain. |
| Comments objoid/classoid/objsubid; security labels same object address | E018 comments accepted; E019 provider absent; E099 edit denied | EC05 / EC04. Label-provider behavior was not executed; comments are ordinary-role annotation evidence only. |
| Initial privileges objoid/classoid/objsubid; pg_shdepend dbid/classid/objid/objsubid/refclassid/refobjid | E017 ACL changes, E086 actual owner/ACL dependence; E098 denied edit | Grants/ownership explicitly exempt. Shared dependencies bind local objects to role/tablespace shared objects, not a legitimate incoming user object to a non-shared core table via refobjid. No new role or cluster-global object was created. |
| Generic pg_depend object-address links n/a/i/e/x/P/S/p, pg_description/pg_init_privs/pg_seclabel polymorphic object ids | E049/E057..062 recursive incoming closure plus E062 outgoing extension membership; E102 edit denied | Do not match raw objid without classid, confuse dependency direction or reject required internal objects. Future predicate-only synthetic links require literal per-route oracle. Pin entries belong to initdb system objects, not ordinary core relations. |

Routes with genuine ordinary constructions have literal evidence below. Routes requiring privilege or a special installed provider/script are explicitly predicate-domain. A genuine unsupported-type/role error is not an altered-state store oracle. The bounded catalog inventory and named routes are complete for these PG14 catalogs; it is **not** a claim to enumerate arbitrary external code or future extension-defined catalogs. EC01/EC04 must decide how those sit relative to the trusted-engine boundary.

## Executed setup/outcome matrix

`ACCEPT` is the actual open. Setup errors show SQLSTATE; proposed oracles never overwrite that observation. Full setup and changed catalog values follow per cell. Route-value differences omit unrelated hstore helper functions/types; all raw observations remain in the hashed files. A rejected open has no N execution; a successful residual-state open is not a kill of the failed intended setup.

| Row | Dimension | Setup errors (actual) | Fetch mismatch (actual) | Public trace (actual) | Proposed required behavior / status |
|---|---|---|---|---|---|

| E001 | baseline | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | ACCEPT; N |
| E002 | cached tail 1 | [] | null | {"open":"ACCEPT","old_tail":{"store_id":"old","position":1},"first":2,"last":3,"retry_equal":true,"positions":[2,3],"tail":3,"through":3} | REJECT persistence.schema_incompatible (CR-012/013) |
| E003 | cached tail 0 | [] | null | {"open":"ACCEPT","old_tail":{"store_id":"old","position":0},"first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | REJECT persistence.schema_incompatible (CR-012/013) |
| E004 | cached tail cleared by rewrite | [] | null | {"open":"ACCEPT","old_tail":{"store_id":"old","position":1},"first":2,"last":3,"retry_equal":true,"positions":[2,3],"tail":3,"through":3} | ACCEPT catalog (cache cleared); wrong old row is not audited by open (G-092) |
| E005 | cached schema version 2 | [] | null | {"error":{"type":"MnemeValidationError","code":"persistence.schema_incompatible","sqlstate":null,"message":"persistence.schema_incompatible: schema 'xe005' does not hold one schema version 1 row"}} | REJECT persistence.schema_incompatible (CR-012/013) |
| E006 | cached schema version 1 | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | REJECT persistence.schema_incompatible (CR-012/013) |
| E007 | table stats target/options | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | ACCEPT; N |
| E008 | index column stats target | ["0A000"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E009 | index column options attempt | ["42601"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E010 | foreign column options on heap attempt | ["42809"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E011 | planner stats/freeze progress | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC03 bookkeeping oracle; real N baseline/residue; unconstructed variations not credited |
| E012 | physical file identity | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | ACCEPT; N |
| E013 | dropped-column residue | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | ACCEPT; N |
| E014 | lazy trigger flag | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC03 bookkeeping oracle; real N baseline/residue; unconstructed variations not credited |
| E015 | lazy rule flag | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC03 bookkeeping oracle; real N baseline/residue; unconstructed variations not credited |
| E016 | lazy inheritance flag | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC03 bookkeeping oracle; real N baseline/residue; unconstructed variations not credited |
| E017 | column/table grants | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | ACCEPT; N |
| E018 | comments on table column index | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC05 comments: non-semantic annotation exception needs explicit disposition |
| E019 | security label provider absent | ["22023"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC04 labels: setup failed, only baseline N observed |
| E020 | extended stats exception | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | ACCEPT; N |
| E021 | unprefixed view dependency | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC01/EC02 path-C admission question; not a chosen pass/reject |
| E022 | materialized view dependency | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC01/EC02 path-C admission question; not a chosen pass/reject |
| E023 | outside rewrite rule | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC01/EC02 path-C admission question; not a chosen pass/reject |
| E024 | sequence ownership dependency | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC01/EC02 path-C admission question; not a chosen pass/reject |
| E025 | publication relation membership | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC01/EC02 path-C admission question; not a chosen pass/reject |
| E026 | all tables publication attempt | ["42501"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E027 | outside FK | [] | "triggers" | {"error":{"type":"MnemeValidationError","code":"persistence.schema_incompatible","sqlstate":null,"message":"persistence.schema_incompatible: the mneme_ catalog of schema 'xe027' differs from v1 in its triggers"}} | REJECT persistence.schema_incompatible (existing covered rule) |
| E028 | outside constraint trigger ref | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | REJECT persistence.schema_incompatible (CR-012/013) |
| E029 | inheritance route control | [] | "inheritance" | {"error":{"type":"MnemeValidationError","code":"persistence.schema_incompatible","sqlstate":null,"message":"persistence.schema_incompatible: the mneme_ catalog of schema 'xe029' differs from v1 in its inheritance"}} | REJECT persistence.schema_incompatible (existing covered rule) |
| E030 | row type dependency column | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC01/EC02 path-C admission question; not a chosen pass/reject |
| E031 | row type dependency function | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC01/EC02 path-C admission question; not a chosen pass/reject |
| E032 | SQL standard body dependency | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC01/EC02 path-C admission question; not a chosen pass/reject |
| E033 | SQL string body nondependency | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC01/EC02 path-C admission question; not a chosen pass/reject |
| E034 | outside default to row type | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC01/EC02 path-C admission question; not a chosen pass/reject |
| E035 | outside CHECK row type | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC01/EC02 path-C admission question; not a chosen pass/reject |
| E036 | outside generated row type | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC01/EC02 path-C admission question; not a chosen pass/reject |
| E037 | outside expression index row type | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC01/EC02 path-C admission question; not a chosen pass/reject |
| E038 | outside policy row type | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC01/EC02 path-C admission question; not a chosen pass/reject |
| E039 | outside domain row type | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC01/EC02 path-C admission question; not a chosen pass/reject |
| E040 | outside view via row type array | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC01/EC02 path-C admission question; not a chosen pass/reject |
| E041 | core-owned constraint trigger control | [] | "triggers" | {"error":{"type":"MnemeValidationError","code":"persistence.schema_incompatible","sqlstate":null,"message":"persistence.schema_incompatible: the mneme_ catalog of schema 'xe041' differs from v1 in its triggers"}} | REJECT persistence.schema_incompatible (existing covered rule) |
| E042 | outside nonconstraint trigger function binds core | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC01/EC02 path-C admission question; not a chosen pass/reject |
| E043 | outside FK not valid | [] | "triggers" | {"error":{"type":"MnemeValidationError","code":"persistence.schema_incompatible","sqlstate":null,"message":"persistence.schema_incompatible: the mneme_ catalog of schema 'xe043' differs from v1 in its triggers"}} | REJECT persistence.schema_incompatible (existing covered rule) |
| E044 | outside typed table | ["42809"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E045 | outside partition attach attempt | [] | "relations" | {"error":{"type":"MnemeValidationError","code":"persistence.schema_incompatible","sqlstate":null,"message":"persistence.schema_incompatible: the mneme_ catalog of schema 'xe045' differs from v1 in its relations"}} | REJECT persistence.schema_incompatible (existing covered rule) |
| E046 | renamed index identity | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | ACCEPT; N |
| E047 | extra index control | [] | "indexes" | {"error":{"type":"MnemeValidationError","code":"persistence.schema_incompatible","sqlstate":null,"message":"persistence.schema_incompatible: the mneme_ catalog of schema 'xe047' differs from v1 in its indexes"}} | REJECT persistence.schema_incompatible (existing covered rule) |
| E048 | catalog edit privilege boundary | ["42501"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E049 | baseline catalog routes and dependency closure | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | ACCEPT; N |
| E050 | outside FROM constraint on mneme_schema | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | REJECT persistence.schema_incompatible (CR-012/013) |
| E051 | outside FROM constraint on mneme_record | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | REJECT persistence.schema_incompatible (CR-012/013) |
| E052 | outside FROM constraint on mneme_operation | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | REJECT persistence.schema_incompatible (CR-012/013) |
| E053 | outside FK schema target | [] | "triggers" | {"error":{"type":"MnemeValidationError","code":"persistence.schema_incompatible","sqlstate":null,"message":"persistence.schema_incompatible: the mneme_ catalog of schema 'xe053' differs from v1 in its triggers"}} | REJECT persistence.schema_incompatible (existing covered rule) |
| E054 | outside FK record target | [] | "triggers" | {"error":{"type":"MnemeValidationError","code":"persistence.schema_incompatible","sqlstate":null,"message":"persistence.schema_incompatible: the mneme_ catalog of schema 'xe054' differs from v1 in its triggers"}} | REJECT persistence.schema_incompatible (existing covered rule) |
| E055 | outside FK operation target | [] | "triggers" | {"error":{"type":"MnemeValidationError","code":"persistence.schema_incompatible","sqlstate":null,"message":"persistence.schema_incompatible: the mneme_ catalog of schema 'xe055' differs from v1 in its triggers"}} | REJECT persistence.schema_incompatible (existing covered rule) |
| E056 | unrelated outside object positive | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | ACCEPT; N |
| E057 | transitive array and domain dependency | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC01/EC02 path-C admission question; not a chosen pass/reject |
| E058 | function result dependency | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC01/EC02 path-C admission question; not a chosen pass/reject |
| E059 | aggregate type dependency | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC01/EC02 path-C admission question; not a chosen pass/reject |
| E060 | operator type dependency | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC01/EC02 path-C admission question; not a chosen pass/reject |
| E061 | cast type dependency | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC01/EC02 path-C admission question; not a chosen pass/reject |
| E062 | extension binding attempt | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC01/EC02 path-C admission question; not a chosen pass/reject |
| E063 | event trigger privilege boundary | ["42501"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E064 | subscription privilege boundary | ["42501"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E065 | foreign table metadata inconsistency attempt | ["42501"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E066 | predicate construction boundary pg_attribute.attlen | ["42501"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E067 | predicate construction boundary pg_attribute.attcacheoff | ["42501"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E068 | predicate construction boundary pg_attribute.attbyval | ["42501"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E069 | predicate construction boundary pg_attribute.attalign | ["42501"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E070 | predicate construction boundary pg_attribute.attfdwoptions | ["42501"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E071 | predicate construction boundary pg_attribute.attmissingval | ["42501"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E072 | predicate construction boundary pg_class.relisshared | ["42501"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E073 | predicate construction boundary pg_class.relispopulated | ["42501"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E074 | predicate construction boundary pg_class.relrewrite | ["42501"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E075 | predicate construction boundary pg_class.relpartbound | ["42501"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E076 | predicate construction boundary pg_class.relkind | ["42501"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E077 | predicate construction boundary pg_class.relpersistence | ["42501"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E078 | predicate construction boundary pg_class.relispartition | ["42501"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E079 | predicate construction boundary pg_class.reloftype | ["42501"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E080 | predicate construction boundary pg_class.relrowsecurity | ["42501"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E081 | predicate construction boundary pg_class.relforcerowsecurity | ["42501"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E082 | predicate construction boundary pg_class.relreplident | ["42501"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E083 | predicate construction boundary pg_class.relnatts | ["42501"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E084 | predicate construction boundary pg_class.relchecks | ["42501"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E085 | predicate construction boundary pg_index.indcheckxmin | ["42501"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC03 bookkeeping oracle; real N baseline/residue; unconstructed variations not credited |
| E086 | full catalog inventory and auxiliary baseline | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | ACCEPT; N |
| E087 | extension config dump construction limit | ["0A000"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E088 | range over row type construction limit | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC01/EC02 path-C admission question; not a chosen pass/reject |
| E089 | operator class construction limit | ["42501"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E090 | sequence type construction limit | ["22023"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E091 | typed foreign table construction limit | ["42704"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E092 | transform reference construction limit | ["42704"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E093 | stored SQL procedure dependency | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC01/EC02 path-C admission question; not a chosen pass/reject |
| E094 | constraint trigger WHEN row-type reference | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC01/EC02 path-C admission question; not a chosen pass/reject |
| E095 | outside FK to other namespace | [] | "triggers" | {"error":{"type":"MnemeValidationError","code":"persistence.schema_incompatible","sqlstate":null,"message":"persistence.schema_incompatible: the mneme_ catalog of schema 'xe095' differs from v1 in its triggers"}} | REJECT persistence.schema_incompatible (existing covered rule) |
| E096 | outside FROM trigger in other namespace | ["42P06"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E097 | outside FROM trigger in separate namespace | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | REJECT persistence.schema_incompatible (CR-012/013) |
| E098 | initial privilege catalog construction limit | ["42501"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E099 | security label catalog construction limit | ["42501"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E100 | subscription binding construction limit | ["42501"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E101 | transform binding construction limit | ["42501"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E102 | depend binding construction limit | ["42501"] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | Construction-limit / residual-state control; ACCEPT N is not evidence for unconstructed state |
| E103 | outside domain CHECK indirect constraint | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC01/EC02 path-C admission question; not a chosen pass/reject |
| E104 | variadic row-type-array signature | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC01/EC02 path-C admission question; not a chosen pass/reject |
| E105 | all-argument and INOUT row-type signature | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC01/EC02 path-C admission question; not a chosen pass/reject |
| E106 | moving aggregate row-type-state | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC01/EC02 path-C admission question; not a chosen pass/reject |
| E107 | expression-index statistics target control | [] | "indexes" | {"error":{"type":"MnemeValidationError","code":"persistence.schema_incompatible","sqlstate":null,"message":"persistence.schema_incompatible: the mneme_ catalog of schema 'xe107' differs from v1 in its indexes"}} | REJECT persistence.schema_incompatible (existing covered rule) |
| E108 | range subtype actual catalog row | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC01/EC02 path-C admission question; not a chosen pass/reject |
| E109 | extension membership actual outgoing edge | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | EC01/EC02 path-C admission question; not a chosen pass/reject |
| E110 | missing cache with exempt planner statistics | [] | null | {"open":"ACCEPT","old_tail":{"store_id":"old","position":1},"first":2,"last":3,"retry_equal":true,"positions":[2,3],"tail":3,"through":3} | REJECT persistence.schema_incompatible (CR-012/013) |
| E111 | outside FROM link with exempt grants | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | REJECT persistence.schema_incompatible (CR-012/013) |
| E112 | outside same-name relation FROM link | [] | null | {"open":"ACCEPT","first":1,"last":2,"retry_equal":true,"positions":[1,2],"tail":2,"through":2} | REJECT persistence.schema_incompatible (CR-012/013) |

## Literal setup and catalog evidence for each executed cell

### E001 — baseline

Setup starts with fresh public initialization; no pre-existing store data.

```sql
-- no variation
```

```json
{
  "setup_results": [],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E002 — cached tail 1

Setup starts with fresh public initialization; create_store("old") before closing the handle.

```sql
ALTER TABLE mneme_store DROP COLUMN tail;
ALTER TABLE mneme_store ADD COLUMN tail bigint NOT NULL DEFAULT 1 CHECK(tail BETWEEN 0 AND 9007199254740991);
ALTER TABLE mneme_store ALTER COLUMN tail SET DEFAULT 0;
```

```json
{
  "setup_results": [
    {
      "sql": "ALTER TABLE mneme_store DROP COLUMN tail",
      "result": "OK"
    },
    {
      "sql": "ALTER TABLE mneme_store ADD COLUMN tail bigint NOT NULL DEFAULT 1 CHECK(tail BETWEEN 0 AND 9007199254740991)",
      "result": "OK"
    },
    {
      "sql": "ALTER TABLE mneme_store ALTER COLUMN tail SET DEFAULT 0",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "class": {
      "mneme_store": {
        "relnatts": [
          2,
          3
        ]
      }
    },
    "attribute": {
      "mneme_store.2": {
        "attname": [
          "tail",
          "........pg.dropped.2........"
        ],
        "atttypid": [
          "20",
          "0"
        ],
        "attisdropped": [
          false,
          true
        ],
        "attstattarget": [
          -1,
          0
        ],
        "atthasdef": [
          true,
          false
        ],
        "attnotnull": [
          true,
          false
        ]
      },
      "mneme_store.3": {
        "added": {
          "attacl": null,
          "attlen": 8,
          "attnum": 3,
          "attname": "tail",
          "attalign": "d",
          "attbyval": true,
          "attndims": 0,
          "attrelid": "217228",
          "atttypid": "20",
          "atthasdef": true,
          "atttypmod": -1,
          "attislocal": true,
          "attnotnull": true,
          "attoptions": null,
          "attstorage": "p",
          "attcacheoff": -1,
          "attidentity": "",
          "attinhcount": 0,
          "attcollation": "0",
          "attgenerated": "",
          "attisdropped": false,
          "attfdwoptions": null,
          "atthasmissing": true,
          "attstattarget": -1,
          "attcompression": "",
          "attmissingval": "{1}"
        }
      }
    },
    "inbound": {
      "added": [
        [
          "pg_attrdef",
          217266,
          0,
          "pg_class",
          217228,
          3,
          "a",
          "default value for column tail of table mneme_store"
        ],
        [
          "pg_constraint",
          217265,
          0,
          "pg_class",
          217228,
          3,
          "a",
          "constraint mneme_store_tail_check on table mneme_store"
        ],
        [
          "pg_constraint",
          217265,
          0,
          "pg_class",
          217228,
          3,
          "n",
          "constraint mneme_store_tail_check on table mneme_store"
        ]
      ],
      "removed": [
        [
          "pg_attrdef",
          217231,
          0,
          "pg_class",
          217228,
          2,
          "a",
          "default value for column tail of table mneme_store"
        ],
        [
          "pg_constraint",
          217232,
          0,
          "pg_class",
          217228,
          2,
          "a",
          "constraint mneme_store_tail_check on table mneme_store"
        ],
        [
          "pg_constraint",
          217232,
          0,
          "pg_class",
          217228,
          2,
          "n",
          "constraint mneme_store_tail_check on table mneme_store"
        ]
      ]
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "old_tail": {
      "store_id": "old",
      "position": 1
    },
    "first": 2,
    "last": 3,
    "retry_equal": true,
    "positions": [
      2,
      3
    ],
    "tail": 3,
    "through": 3
  }
}
```

### E003 — cached tail 0

Setup starts with fresh public initialization; create_store("old") before closing the handle.

```sql
ALTER TABLE mneme_store DROP COLUMN tail;
ALTER TABLE mneme_store ADD COLUMN tail bigint NOT NULL DEFAULT 0 CHECK(tail BETWEEN 0 AND 9007199254740991);
```

```json
{
  "setup_results": [
    {
      "sql": "ALTER TABLE mneme_store DROP COLUMN tail",
      "result": "OK"
    },
    {
      "sql": "ALTER TABLE mneme_store ADD COLUMN tail bigint NOT NULL DEFAULT 0 CHECK(tail BETWEEN 0 AND 9007199254740991)",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "class": {
      "mneme_store": {
        "relnatts": [
          2,
          3
        ]
      }
    },
    "attribute": {
      "mneme_store.2": {
        "attname": [
          "tail",
          "........pg.dropped.2........"
        ],
        "atttypid": [
          "20",
          "0"
        ],
        "attisdropped": [
          false,
          true
        ],
        "attstattarget": [
          -1,
          0
        ],
        "atthasdef": [
          true,
          false
        ],
        "attnotnull": [
          true,
          false
        ]
      },
      "mneme_store.3": {
        "added": {
          "attacl": null,
          "attlen": 8,
          "attnum": 3,
          "attname": "tail",
          "attalign": "d",
          "attbyval": true,
          "attndims": 0,
          "attrelid": "217275",
          "atttypid": "20",
          "atthasdef": true,
          "atttypmod": -1,
          "attislocal": true,
          "attnotnull": true,
          "attoptions": null,
          "attstorage": "p",
          "attcacheoff": -1,
          "attidentity": "",
          "attinhcount": 0,
          "attcollation": "0",
          "attgenerated": "",
          "attisdropped": false,
          "attfdwoptions": null,
          "atthasmissing": true,
          "attstattarget": -1,
          "attcompression": "",
          "attmissingval": "{0}"
        }
      }
    },
    "inbound": {
      "added": [
        [
          "pg_attrdef",
          217311,
          0,
          "pg_class",
          217275,
          3,
          "a",
          "default value for column tail of table mneme_store"
        ],
        [
          "pg_constraint",
          217312,
          0,
          "pg_class",
          217275,
          3,
          "a",
          "constraint mneme_store_tail_check on table mneme_store"
        ],
        [
          "pg_constraint",
          217312,
          0,
          "pg_class",
          217275,
          3,
          "n",
          "constraint mneme_store_tail_check on table mneme_store"
        ]
      ],
      "removed": [
        [
          "pg_attrdef",
          217278,
          0,
          "pg_class",
          217275,
          2,
          "a",
          "default value for column tail of table mneme_store"
        ],
        [
          "pg_constraint",
          217279,
          0,
          "pg_class",
          217275,
          2,
          "a",
          "constraint mneme_store_tail_check on table mneme_store"
        ],
        [
          "pg_constraint",
          217279,
          0,
          "pg_class",
          217275,
          2,
          "n",
          "constraint mneme_store_tail_check on table mneme_store"
        ]
      ]
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "old_tail": {
      "store_id": "old",
      "position": 0
    },
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E004 — cached tail cleared by rewrite

Setup starts with fresh public initialization; create_store("old") before closing the handle.

```sql
ALTER TABLE mneme_store DROP COLUMN tail;
ALTER TABLE mneme_store ADD COLUMN tail bigint NOT NULL DEFAULT 1 CHECK(tail BETWEEN 0 AND 9007199254740991);
ALTER TABLE mneme_store ALTER COLUMN tail SET DEFAULT 0;
VACUUM FULL mneme_store;
```

```json
{
  "setup_results": [
    {
      "sql": "ALTER TABLE mneme_store DROP COLUMN tail",
      "result": "OK"
    },
    {
      "sql": "ALTER TABLE mneme_store ADD COLUMN tail bigint NOT NULL DEFAULT 1 CHECK(tail BETWEEN 0 AND 9007199254740991)",
      "result": "OK"
    },
    {
      "sql": "ALTER TABLE mneme_store ALTER COLUMN tail SET DEFAULT 0",
      "result": "OK"
    },
    {
      "sql": "VACUUM FULL mneme_store",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "class": {
      "mneme_store": {
        "reltuples": [
          -1,
          1
        ],
        "relfilenode": [
          "217321",
          "217360"
        ],
        "relfrozenxid": [
          "51301",
          "51306"
        ],
        "relpages": [
          0,
          1
        ],
        "relnatts": [
          2,
          3
        ]
      },
      "mneme_store_pkey": {
        "reltuples": [
          0,
          1
        ],
        "relfilenode": [
          "217328",
          "217365"
        ],
        "relpages": [
          1,
          2
        ]
      }
    },
    "attribute": {
      "mneme_store.2": {
        "attname": [
          "tail",
          "........pg.dropped.2........"
        ],
        "atttypid": [
          "20",
          "0"
        ],
        "attisdropped": [
          false,
          true
        ],
        "attstattarget": [
          -1,
          0
        ],
        "atthasdef": [
          true,
          false
        ],
        "attnotnull": [
          true,
          false
        ]
      },
      "mneme_store.3": {
        "added": {
          "attacl": null,
          "attlen": 8,
          "attnum": 3,
          "attname": "tail",
          "attalign": "d",
          "attbyval": true,
          "attndims": 0,
          "attrelid": "217321",
          "atttypid": "20",
          "atthasdef": true,
          "atttypmod": -1,
          "attislocal": true,
          "attnotnull": true,
          "attoptions": null,
          "attstorage": "p",
          "attcacheoff": -1,
          "attidentity": "",
          "attinhcount": 0,
          "attcollation": "0",
          "attgenerated": "",
          "attisdropped": false,
          "attfdwoptions": null,
          "atthasmissing": false,
          "attstattarget": -1,
          "attcompression": "",
          "attmissingval": null
        }
      }
    },
    "inbound": {
      "added": [
        [
          "pg_attrdef",
          217359,
          0,
          "pg_class",
          217321,
          3,
          "a",
          "default value for column tail of table mneme_store"
        ],
        [
          "pg_constraint",
          217358,
          0,
          "pg_class",
          217321,
          3,
          "a",
          "constraint mneme_store_tail_check on table mneme_store"
        ],
        [
          "pg_constraint",
          217358,
          0,
          "pg_class",
          217321,
          3,
          "n",
          "constraint mneme_store_tail_check on table mneme_store"
        ]
      ],
      "removed": [
        [
          "pg_attrdef",
          217324,
          0,
          "pg_class",
          217321,
          2,
          "a",
          "default value for column tail of table mneme_store"
        ],
        [
          "pg_constraint",
          217325,
          0,
          "pg_class",
          217321,
          2,
          "a",
          "constraint mneme_store_tail_check on table mneme_store"
        ],
        [
          "pg_constraint",
          217325,
          0,
          "pg_class",
          217321,
          2,
          "n",
          "constraint mneme_store_tail_check on table mneme_store"
        ]
      ]
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "old_tail": {
      "store_id": "old",
      "position": 1
    },
    "first": 2,
    "last": 3,
    "retry_equal": true,
    "positions": [
      2,
      3
    ],
    "tail": 3,
    "through": 3
  }
}
```

### E005 — cached schema version 2

Setup starts with fresh public initialization; no pre-existing store data.

```sql
ALTER TABLE mneme_schema DROP COLUMN version;
ALTER TABLE mneme_schema ADD COLUMN version integer NOT NULL DEFAULT 2;
ALTER TABLE mneme_schema ALTER COLUMN version DROP DEFAULT;
```

```json
{
  "setup_results": [
    {
      "sql": "ALTER TABLE mneme_schema DROP COLUMN version",
      "result": "OK"
    },
    {
      "sql": "ALTER TABLE mneme_schema ADD COLUMN version integer NOT NULL DEFAULT 2",
      "result": "OK"
    },
    {
      "sql": "ALTER TABLE mneme_schema ALTER COLUMN version DROP DEFAULT",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "class": {
      "mneme_schema": {
        "relnatts": [
          2,
          3
        ]
      }
    },
    "attribute": {
      "mneme_schema.2": {
        "attname": [
          "version",
          "........pg.dropped.2........"
        ],
        "atttypid": [
          "23",
          "0"
        ],
        "attisdropped": [
          false,
          true
        ],
        "attstattarget": [
          -1,
          0
        ],
        "attnotnull": [
          true,
          false
        ]
      },
      "mneme_schema.3": {
        "added": {
          "attacl": null,
          "attlen": 4,
          "attnum": 3,
          "attname": "version",
          "attalign": "i",
          "attbyval": true,
          "attndims": 0,
          "attrelid": "217367",
          "atttypid": "23",
          "atthasdef": false,
          "atttypmod": -1,
          "attislocal": true,
          "attnotnull": true,
          "attoptions": null,
          "attstorage": "p",
          "attcacheoff": -1,
          "attidentity": "",
          "attinhcount": 0,
          "attcollation": "0",
          "attgenerated": "",
          "attisdropped": false,
          "attfdwoptions": null,
          "atthasmissing": true,
          "attstattarget": -1,
          "attcompression": "",
          "attmissingval": "{2}"
        }
      }
    }
  },
  "fetch_mismatch": null,
  "public": {
    "error": {
      "type": "MnemeValidationError",
      "code": "persistence.schema_incompatible",
      "sqlstate": null,
      "message": "persistence.schema_incompatible: schema 'xe005' does not hold one schema version 1 row"
    }
  }
}
```

### E006 — cached schema version 1

Setup starts with fresh public initialization; no pre-existing store data.

```sql
ALTER TABLE mneme_schema DROP COLUMN version;
ALTER TABLE mneme_schema ADD COLUMN version integer NOT NULL DEFAULT 1;
ALTER TABLE mneme_schema ALTER COLUMN version DROP DEFAULT;
```

```json
{
  "setup_results": [
    {
      "sql": "ALTER TABLE mneme_schema DROP COLUMN version",
      "result": "OK"
    },
    {
      "sql": "ALTER TABLE mneme_schema ADD COLUMN version integer NOT NULL DEFAULT 1",
      "result": "OK"
    },
    {
      "sql": "ALTER TABLE mneme_schema ALTER COLUMN version DROP DEFAULT",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "class": {
      "mneme_schema": {
        "relnatts": [
          2,
          3
        ]
      }
    },
    "attribute": {
      "mneme_schema.2": {
        "attname": [
          "version",
          "........pg.dropped.2........"
        ],
        "atttypid": [
          "23",
          "0"
        ],
        "attisdropped": [
          false,
          true
        ],
        "attstattarget": [
          -1,
          0
        ],
        "attnotnull": [
          true,
          false
        ]
      },
      "mneme_schema.3": {
        "added": {
          "attacl": null,
          "attlen": 4,
          "attnum": 3,
          "attname": "version",
          "attalign": "i",
          "attbyval": true,
          "attndims": 0,
          "attrelid": "217412",
          "atttypid": "23",
          "atthasdef": false,
          "atttypmod": -1,
          "attislocal": true,
          "attnotnull": true,
          "attoptions": null,
          "attstorage": "p",
          "attcacheoff": -1,
          "attidentity": "",
          "attinhcount": 0,
          "attcollation": "0",
          "attgenerated": "",
          "attisdropped": false,
          "attfdwoptions": null,
          "atthasmissing": true,
          "attstattarget": -1,
          "attcompression": "",
          "attmissingval": "{1}"
        }
      }
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E007 — table stats target/options

Setup starts with fresh public initialization; no pre-existing store data.

```sql
ALTER TABLE mneme_store ALTER COLUMN tail SET STATISTICS 300;
ALTER TABLE mneme_store ALTER COLUMN tail SET (n_distinct=0.5,n_distinct_inherited=-0.7);
ANALYZE mneme_store;
```

```json
{
  "setup_results": [
    {
      "sql": "ALTER TABLE mneme_store ALTER COLUMN tail SET STATISTICS 300",
      "result": "OK"
    },
    {
      "sql": "ALTER TABLE mneme_store ALTER COLUMN tail SET (n_distinct=0.5,n_distinct_inherited=-0.7)",
      "result": "OK"
    },
    {
      "sql": "ANALYZE mneme_store",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "class": {
      "mneme_store": {
        "reltuples": [
          -1,
          0
        ]
      }
    },
    "attribute": {
      "mneme_store.2": {
        "attstattarget": [
          -1,
          300
        ],
        "attoptions": [
          null,
          [
            "n_distinct=0.5",
            "n_distinct_inherited=-0.7"
          ]
        ]
      }
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E008 — index column stats target

Setup starts with fresh public initialization; no pre-existing store data.

```sql
ALTER INDEX mneme_store_pkey ALTER COLUMN 1 SET STATISTICS 300;
```

```json
{
  "setup_results": [
    {
      "sql": "ALTER INDEX mneme_store_pkey ALTER COLUMN 1 SET STATISTICS 300",
      "error": {
        "type": "FeatureNotSupported",
        "code": null,
        "sqlstate": "0A000",
        "message": "cannot alter statistics on non-expression column \"store_id\" of index \"mneme_store_pkey\"\nHINT:  Alter statistics on table column instead."
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

### E009 — index column options attempt

Setup starts with fresh public initialization; no pre-existing store data.

```sql
ALTER INDEX mneme_store_pkey ALTER COLUMN 1 SET (n_distinct=0.5);
```

```json
{
  "setup_results": [
    {
      "sql": "ALTER INDEX mneme_store_pkey ALTER COLUMN 1 SET (n_distinct=0.5)",
      "error": {
        "type": "SyntaxError",
        "code": null,
        "sqlstate": "42601",
        "message": "syntax error at or near \"(\"\nLINE 1: ALTER INDEX mneme_store_pkey ALTER COLUMN 1 SET (n_distinct=...\n                                                        ^"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

### E010 — foreign column options on heap attempt

Setup starts with fresh public initialization; no pre-existing store data.

```sql
ALTER TABLE mneme_store ALTER COLUMN tail OPTIONS (ADD anything 'x');
```

```json
{
  "setup_results": [
    {
      "sql": "ALTER TABLE mneme_store ALTER COLUMN tail OPTIONS (ADD anything 'x')",
      "error": {
        "type": "WrongObjectType",
        "code": null,
        "sqlstate": "42809",
        "message": "\"mneme_store\" is not a foreign table"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

### E011 — planner stats/freeze progress

Setup starts with fresh public initialization; no pre-existing store data.

```sql
VACUUM (FREEZE,ANALYZE) mneme_schema;
VACUUM (FREEZE,ANALYZE) mneme_store;
VACUUM (FREEZE,ANALYZE) mneme_record;
VACUUM (FREEZE,ANALYZE) mneme_operation;
```

```json
{
  "setup_results": [
    {
      "sql": "VACUUM (FREEZE,ANALYZE) mneme_schema",
      "result": "OK"
    },
    {
      "sql": "VACUUM (FREEZE,ANALYZE) mneme_store",
      "result": "OK"
    },
    {
      "sql": "VACUUM (FREEZE,ANALYZE) mneme_record",
      "result": "OK"
    },
    {
      "sql": "VACUUM (FREEZE,ANALYZE) mneme_operation",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "class": {
      "mneme_operation": {
        "reltuples": [
          -1,
          0
        ],
        "relfrozenxid": [
          "51353",
          "51355"
        ]
      },
      "mneme_record": {
        "reltuples": [
          -1,
          0
        ],
        "relfrozenxid": [
          "51353",
          "51355"
        ]
      },
      "mneme_schema": {
        "reltuples": [
          -1,
          1
        ],
        "relfrozenxid": [
          "51353",
          "51355"
        ],
        "relpages": [
          0,
          1
        ],
        "relallvisible": [
          0,
          1
        ]
      },
      "mneme_schema_pkey": {
        "reltuples": [
          0,
          1
        ],
        "relpages": [
          1,
          2
        ]
      },
      "mneme_store": {
        "reltuples": [
          -1,
          0
        ],
        "relfrozenxid": [
          "51353",
          "51355"
        ]
      }
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E012 — physical file identity

Setup starts with fresh public initialization; no pre-existing store data.

```sql
REINDEX TABLE mneme_store;
VACUUM FULL mneme_schema;
```

```json
{
  "setup_results": [
    {
      "sql": "REINDEX TABLE mneme_store",
      "result": "OK"
    },
    {
      "sql": "VACUUM FULL mneme_schema",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "class": {
      "mneme_schema": {
        "reltuples": [
          -1,
          1
        ],
        "relfilenode": [
          "217678",
          "217723"
        ],
        "relfrozenxid": [
          "51368",
          "51372"
        ],
        "relpages": [
          0,
          1
        ]
      },
      "mneme_schema_pkey": {
        "reltuples": [
          0,
          1
        ],
        "relfilenode": [
          "217683",
          "217726"
        ],
        "relpages": [
          1,
          2
        ]
      },
      "mneme_store_pkey": {
        "reltuples": [
          0,
          -1
        ],
        "relfilenode": [
          "217692",
          "217721"
        ],
        "relpages": [
          1,
          0
        ]
      }
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E013 — dropped-column residue

Setup starts with fresh public initialization; no pre-existing store data.

```sql
ALTER TABLE mneme_store ADD COLUMN gone text;
ALTER TABLE mneme_store DROP COLUMN gone;
```

```json
{
  "setup_results": [
    {
      "sql": "ALTER TABLE mneme_store ADD COLUMN gone text",
      "result": "OK"
    },
    {
      "sql": "ALTER TABLE mneme_store DROP COLUMN gone",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "class": {
      "mneme_store": {
        "relnatts": [
          2,
          3
        ]
      }
    },
    "attribute": {
      "mneme_store.3": {
        "added": {
          "attacl": null,
          "attlen": -1,
          "attnum": 3,
          "attname": "........pg.dropped.3........",
          "attalign": "i",
          "attbyval": false,
          "attndims": 0,
          "attrelid": "217735",
          "atttypid": "0",
          "atthasdef": false,
          "atttypmod": -1,
          "attislocal": true,
          "attnotnull": false,
          "attoptions": null,
          "attstorage": "x",
          "attcacheoff": -1,
          "attidentity": "",
          "attinhcount": 0,
          "attcollation": "100",
          "attgenerated": "",
          "attisdropped": true,
          "attfdwoptions": null,
          "atthasmissing": false,
          "attstattarget": 0,
          "attcompression": "",
          "attmissingval": null
        }
      }
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E014 — lazy trigger flag

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE FUNCTION noop() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NEW; END$$;
CREATE TRIGGER transient AFTER INSERT ON mneme_schema FOR EACH ROW EXECUTE FUNCTION noop();
DROP TRIGGER transient ON mneme_schema;
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE FUNCTION noop() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NEW; END$$",
      "result": "OK"
    },
    {
      "sql": "CREATE TRIGGER transient AFTER INSERT ON mneme_schema FOR EACH ROW EXECUTE FUNCTION noop()",
      "result": "OK"
    },
    {
      "sql": "DROP TRIGGER transient ON mneme_schema",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "class": {
      "mneme_schema": {
        "relhastriggers": [
          false,
          true
        ]
      }
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E015 — lazy rule flag

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE RULE transient AS ON INSERT TO mneme_schema DO ALSO NOTIFY probe;
DROP RULE transient ON mneme_schema;
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE RULE transient AS ON INSERT TO mneme_schema DO ALSO NOTIFY probe",
      "result": "OK"
    },
    {
      "sql": "DROP RULE transient ON mneme_schema",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "class": {
      "mneme_schema": {
        "relhasrules": [
          false,
          true
        ]
      }
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E016 — lazy inheritance flag

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE TABLE outside_child () INHERITS(mneme_store);
DROP TABLE outside_child;
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE TABLE outside_child () INHERITS(mneme_store)",
      "result": "OK"
    },
    {
      "sql": "DROP TABLE outside_child",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "class": {
      "mneme_store": {
        "relhassubclass": [
          false,
          true
        ]
      }
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E017 — column/table grants

Setup starts with fresh public initialization; no pre-existing store data.

```sql
GRANT SELECT(tail) ON mneme_store TO PUBLIC;
GRANT SELECT ON mneme_record TO PUBLIC;
```

```json
{
  "setup_results": [
    {
      "sql": "GRANT SELECT(tail) ON mneme_store TO PUBLIC",
      "result": "OK"
    },
    {
      "sql": "GRANT SELECT ON mneme_record TO PUBLIC",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "class": {
      "mneme_record": {
        "relacl": [
          null,
          [
            "mneme_dev=arwdDxt/mneme_dev",
            "=r/mneme_dev"
          ]
        ]
      }
    },
    "attribute": {
      "mneme_store.2": {
        "attacl": [
          null,
          [
            "=r/mneme_dev"
          ]
        ]
      }
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E018 — comments on table column index

Setup starts with fresh public initialization; no pre-existing store data.

```sql
COMMENT ON TABLE mneme_store IS 'review';
COMMENT ON COLUMN mneme_store.tail IS 'review';
COMMENT ON INDEX mneme_store_pkey IS 'review';
```

```json
{
  "setup_results": [
    {
      "sql": "COMMENT ON TABLE mneme_store IS 'review'",
      "result": "OK"
    },
    {
      "sql": "COMMENT ON COLUMN mneme_store.tail IS 'review'",
      "result": "OK"
    },
    {
      "sql": "COMMENT ON INDEX mneme_store_pkey IS 'review'",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "annotations": {
      "added": [
        [
          217965,
          0,
          "review"
        ],
        [
          217965,
          2,
          "review"
        ],
        [
          217972,
          0,
          "review"
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E019 — security label provider absent

Setup starts with fresh public initialization; no pre-existing store data.

```sql
SECURITY LABEL FOR ce04_missing ON TABLE mneme_store IS 'x';
```

```json
{
  "setup_results": [
    {
      "sql": "SECURITY LABEL FOR ce04_missing ON TABLE mneme_store IS 'x'",
      "error": {
        "type": "InvalidParameterValue",
        "code": null,
        "sqlstate": "22023",
        "message": "security label provider \"ce04_missing\" is not loaded"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

### E020 — extended stats exception

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE STATISTICS outside_stat (dependencies) ON store_id,tail FROM mneme_store;
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE STATISTICS outside_stat (dependencies) ON store_id,tail FROM mneme_store",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_statistic_ext",
          218089,
          0,
          "pg_class",
          218053,
          1,
          "a",
          "statistics object outside_stat"
        ],
        [
          "pg_statistic_ext",
          218089,
          0,
          "pg_class",
          218053,
          2,
          "a",
          "statistics object outside_stat"
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E021 — unprefixed view dependency

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE VIEW outside_view AS SELECT * FROM mneme_store;
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE VIEW outside_view AS SELECT * FROM mneme_store",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_rewrite",
          218137,
          0,
          "pg_class",
          218098,
          1,
          "n",
          "rule _RETURN on view outside_view"
        ],
        [
          "pg_rewrite",
          218137,
          0,
          "pg_class",
          218098,
          2,
          "n",
          "rule _RETURN on view outside_view"
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E022 — materialized view dependency

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE MATERIALIZED VIEW outside_mat AS SELECT * FROM mneme_store;
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE MATERIALIZED VIEW outside_mat AS SELECT * FROM mneme_store",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_rewrite",
          218187,
          0,
          "pg_class",
          218146,
          1,
          "n",
          "rule _RETURN on materialized view outside_mat"
        ],
        [
          "pg_rewrite",
          218187,
          0,
          "pg_class",
          218146,
          2,
          "n",
          "rule _RETURN on materialized view outside_mat"
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E023 — outside rewrite rule

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE TABLE outside_log(sid text);
CREATE RULE outside_rule AS ON INSERT TO outside_log DO ALSO INSERT INTO mneme_store(store_id) VALUES(NEW.sid);
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE TABLE outside_log(sid text)",
      "result": "OK"
    },
    {
      "sql": "CREATE RULE outside_rule AS ON INSERT TO outside_log DO ALSO INSERT INTO mneme_store(store_id) VALUES(NEW.sid)",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_rewrite",
          218237,
          0,
          "pg_class",
          218196,
          1,
          "n",
          "rule outside_rule on table outside_log"
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E024 — sequence ownership dependency

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE SEQUENCE outside_seq OWNED BY mneme_store.tail;
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE SEQUENCE outside_seq OWNED BY mneme_store.tail",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_class",
          218282,
          0,
          "pg_class",
          218246,
          2,
          "a",
          "sequence outside_seq"
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E025 — publication relation membership

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE PUBLICATION ce04_pub FOR TABLE mneme_store;
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE PUBLICATION ce04_pub FOR TABLE mneme_store",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_publication_rel",
          218328,
          0,
          "pg_class",
          218291,
          0,
          "a",
          "publication of table mneme_store in publication ce04_pub"
        ]
      ],
      "removed": []
    },
    "publication": {
      "added": [
        [
          "ce04_pub",
          {
            "oid": "218327",
            "pubname": "ce04_pub",
            "pubowner": "16901",
            "pubdelete": true,
            "pubinsert": true,
            "pubupdate": true,
            "pubviaroot": false,
            "pubtruncate": true,
            "puballtables": false
          },
          {
            "oid": "218328",
            "prpubid": "218327",
            "prrelid": "218291"
          }
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E026 — all tables publication attempt

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE PUBLICATION ce04_pub FOR ALL TABLES;
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE PUBLICATION ce04_pub FOR ALL TABLES",
      "error": {
        "type": "InsufficientPrivilege",
        "code": null,
        "sqlstate": "42501",
        "message": "must be superuser to create FOR ALL TABLES publication"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

### E027 — outside FK

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE TABLE outside_fk(sid text REFERENCES mneme_store);
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE TABLE outside_fk(sid text REFERENCES mneme_store)",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_constraint",
          218422,
          0,
          "pg_class",
          218381,
          1,
          "n",
          "constraint outside_fk_sid_fkey on table outside_fk"
        ]
      ],
      "removed": []
    },
    "triggers": {
      "added": [
        [
          {
            "oid": "218423",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "1654",
            "tgname": "RI_ConstraintTrigger_a_218423",
            "tgqual": null,
            "tgtype": 9,
            "tgnargs": 0,
            "tgrelid": "218381",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "218422",
            "tgdeferrable": false,
            "tgisinternal": true,
            "tgconstrindid": "218388",
            "tgconstrrelid": "218417",
            "tginitdeferred": false
          }
        ],
        [
          {
            "oid": "218424",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "1655",
            "tgname": "RI_ConstraintTrigger_a_218424",
            "tgqual": null,
            "tgtype": 17,
            "tgnargs": 0,
            "tgrelid": "218381",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "218422",
            "tgdeferrable": false,
            "tgisinternal": true,
            "tgconstrindid": "218388",
            "tgconstrrelid": "218417",
            "tginitdeferred": false
          }
        ],
        [
          {
            "oid": "218425",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "1644",
            "tgname": "RI_ConstraintTrigger_c_218425",
            "tgqual": null,
            "tgtype": 5,
            "tgnargs": 0,
            "tgrelid": "218417",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "218422",
            "tgdeferrable": false,
            "tgisinternal": true,
            "tgconstrindid": "218388",
            "tgconstrrelid": "218381",
            "tginitdeferred": false
          }
        ],
        [
          {
            "oid": "218426",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "1645",
            "tgname": "RI_ConstraintTrigger_c_218426",
            "tgqual": null,
            "tgtype": 17,
            "tgnargs": 0,
            "tgrelid": "218417",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "218422",
            "tgdeferrable": false,
            "tgisinternal": true,
            "tgconstrindid": "218388",
            "tgconstrrelid": "218381",
            "tginitdeferred": false
          }
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": "triggers",
  "public": {
    "error": {
      "type": "MnemeValidationError",
      "code": "persistence.schema_incompatible",
      "sqlstate": null,
      "message": "persistence.schema_incompatible: the mneme_ catalog of schema 'xe027' differs from v1 in its triggers"
    }
  }
}
```

### E028 — outside constraint trigger ref

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE TABLE outside_t(sid text);
CREATE FUNCTION noop() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NEW; END$$;
CREATE CONSTRAINT TRIGGER outside_constraint AFTER INSERT ON outside_t FROM mneme_store DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION noop();
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE TABLE outside_t(sid text)",
      "result": "OK"
    },
    {
      "sql": "CREATE FUNCTION noop() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NEW; END$$",
      "result": "OK"
    },
    {
      "sql": "CREATE CONSTRAINT TRIGGER outside_constraint AFTER INSERT ON outside_t FROM mneme_store DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION noop()",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_trigger",
          218477,
          0,
          "pg_class",
          218435,
          0,
          "a",
          "trigger outside_constraint on table outside_t"
        ]
      ],
      "removed": []
    },
    "triggers": {
      "added": [
        [
          {
            "oid": "218477",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "218476",
            "tgname": "outside_constraint",
            "tgqual": null,
            "tgtype": 5,
            "tgnargs": 0,
            "tgrelid": "218471",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "218478",
            "tgdeferrable": true,
            "tgisinternal": false,
            "tgconstrindid": "0",
            "tgconstrrelid": "218435",
            "tginitdeferred": true
          }
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E029 — inheritance route control

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE TABLE outside_child () INHERITS(mneme_store);
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE TABLE outside_child () INHERITS(mneme_store)",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "class": {
      "mneme_store": {
        "relhassubclass": [
          false,
          true
        ]
      }
    },
    "inbound": {
      "added": [
        [
          "pg_class",
          218523,
          0,
          "pg_class",
          218487,
          0,
          "n",
          "table outside_child"
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": "inheritance",
  "public": {
    "error": {
      "type": "MnemeValidationError",
      "code": "persistence.schema_incompatible",
      "sqlstate": null,
      "message": "persistence.schema_incompatible: the mneme_ catalog of schema 'xe029' differs from v1 in its inheritance"
    }
  }
}
```

### E030 — row type dependency column

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE TABLE outside_row(v mneme_store);
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE TABLE outside_row(v mneme_store)",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_class",
          218574,
          1,
          "pg_type",
          218540,
          0,
          "n",
          "column v of table outside_row"
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E031 — row type dependency function

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE FUNCTION outside_fun(mneme_store) RETURNS bigint LANGUAGE SQL AS $$ SELECT $1.tail $$;
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE FUNCTION outside_fun(mneme_store) RETURNS bigint LANGUAGE SQL AS $$ SELECT $1.tail $$",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_proc",
          218623,
          0,
          "pg_type",
          218589,
          0,
          "n",
          "function outside_fun(mneme_store)"
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E032 — SQL standard body dependency

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE FUNCTION outside_fun() RETURNS bigint LANGUAGE SQL BEGIN ATOMIC SELECT tail FROM mneme_store LIMIT 1; END;
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE FUNCTION outside_fun() RETURNS bigint LANGUAGE SQL BEGIN ATOMIC SELECT tail FROM mneme_store LIMIT 1; END",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_proc",
          218668,
          0,
          "pg_class",
          218632,
          2,
          "n",
          "function outside_fun()"
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E033 — SQL string body nondependency

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE FUNCTION outside_fun() RETURNS bigint LANGUAGE SQL AS $$ SELECT tail FROM mneme_store LIMIT 1 $$;
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE FUNCTION outside_fun() RETURNS bigint LANGUAGE SQL AS $$ SELECT tail FROM mneme_store LIMIT 1 $$",
      "result": "OK"
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E034 — outside default to row type

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE TABLE outside_default(v mneme_store DEFAULT ROW('x',0)::mneme_store);
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE TABLE outside_default(v mneme_store DEFAULT ROW('x',0)::mneme_store)",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_attrdef",
          218761,
          0,
          "pg_type",
          218724,
          0,
          "n",
          "default value for column v of table outside_default"
        ],
        [
          "pg_class",
          218758,
          1,
          "pg_type",
          218724,
          0,
          "n",
          "column v of table outside_default"
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E035 — outside CHECK row type

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE TABLE outside_check(v text CHECK(ROW(v,0)::mneme_store IS NOT NULL));
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE TABLE outside_check(v text CHECK(ROW(v,0)::mneme_store IS NOT NULL))",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_constraint",
          218811,
          0,
          "pg_type",
          218774,
          0,
          "n",
          "constraint outside_check_v_check on table outside_check"
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E036 — outside generated row type

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE TABLE outside_gen(v text,r mneme_store GENERATED ALWAYS AS (ROW(v,0)::mneme_store) STORED);
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE TABLE outside_gen(v text,r mneme_store GENERATED ALWAYS AS (ROW(v,0)::mneme_store) STORED)",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_class",
          218858,
          2,
          "pg_type",
          218824,
          0,
          "a",
          "column r of table outside_gen"
        ],
        [
          "pg_class",
          218858,
          2,
          "pg_type",
          218824,
          0,
          "n",
          "column r of table outside_gen"
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E037 — outside expression index row type

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE TABLE outside_expr(v text);
CREATE INDEX outside_idx ON outside_expr (((ROW(v,0)::mneme_store).tail));
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE TABLE outside_expr(v text)",
      "result": "OK"
    },
    {
      "sql": "CREATE INDEX outside_idx ON outside_expr (((ROW(v,0)::mneme_store).tail))",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_class",
          218913,
          0,
          "pg_class",
          218872,
          2,
          "n",
          "index outside_idx"
        ],
        [
          "pg_class",
          218913,
          0,
          "pg_type",
          218874,
          0,
          "n",
          "index outside_idx"
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E038 — outside policy row type

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE TABLE outside_policy(v text);
CREATE POLICY p ON outside_policy USING (ROW(v,0)::mneme_store IS NOT NULL);
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE TABLE outside_policy(v text)",
      "result": "OK"
    },
    {
      "sql": "CREATE POLICY p ON outside_policy USING (ROW(v,0)::mneme_store IS NOT NULL)",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_policy",
          218963,
          0,
          "pg_type",
          218924,
          0,
          "n",
          "policy p on table outside_policy"
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E039 — outside domain row type

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE DOMAIN outside_domain AS mneme_store;
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE DOMAIN outside_domain AS mneme_store",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_type",
          219009,
          0,
          "pg_type",
          218974,
          0,
          "n",
          "type outside_domain"
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E040 — outside view via row type array

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE VIEW outside_arr AS SELECT ARRAY[ROW('x',0)::mneme_store] AS v;
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE VIEW outside_arr AS SELECT ARRAY[ROW('x',0)::mneme_store] AS v",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_rewrite",
          219057,
          0,
          "pg_type",
          219020,
          0,
          "n",
          "rule _RETURN on view outside_arr"
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E041 — core-owned constraint trigger control

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE FUNCTION noop() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NEW; END$$;
CREATE CONSTRAINT TRIGGER direct_constraint AFTER INSERT ON mneme_store FOR EACH ROW EXECUTE FUNCTION noop();
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE FUNCTION noop() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NEW; END$$",
      "result": "OK"
    },
    {
      "sql": "CREATE CONSTRAINT TRIGGER direct_constraint AFTER INSERT ON mneme_store FOR EACH ROW EXECUTE FUNCTION noop()",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_constraint",
          219104,
          0,
          "pg_class",
          219066,
          0,
          "a",
          "constraint direct_constraint on table mneme_store"
        ],
        [
          "pg_trigger",
          219103,
          0,
          "pg_class",
          219066,
          0,
          "a",
          "trigger direct_constraint on table mneme_store"
        ]
      ],
      "removed": []
    },
    "triggers": {
      "added": [
        [
          {
            "oid": "219103",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "219102",
            "tgname": "direct_constraint",
            "tgqual": null,
            "tgtype": 5,
            "tgnargs": 0,
            "tgrelid": "219066",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "219104",
            "tgdeferrable": false,
            "tgisinternal": false,
            "tgconstrindid": "0",
            "tgconstrrelid": "0",
            "tginitdeferred": false
          }
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": "triggers",
  "public": {
    "error": {
      "type": "MnemeValidationError",
      "code": "persistence.schema_incompatible",
      "sqlstate": null,
      "message": "persistence.schema_incompatible: the mneme_ catalog of schema 'xe041' differs from v1 in its triggers"
    }
  }
}
```

### E042 — outside nonconstraint trigger function binds core

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE TABLE outside_t(sid text);
CREATE FUNCTION outside_effect() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN INSERT INTO mneme_store(store_id) VALUES(NEW.sid); RETURN NEW; END$$;
CREATE TRIGGER outside_trigger AFTER INSERT ON outside_t FOR EACH ROW EXECUTE FUNCTION outside_effect();
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE TABLE outside_t(sid text)",
      "result": "OK"
    },
    {
      "sql": "CREATE FUNCTION outside_effect() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN INSERT INTO mneme_store(store_id) VALUES(NEW.sid); RETURN NEW; END$$",
      "result": "OK"
    },
    {
      "sql": "CREATE TRIGGER outside_trigger AFTER INSERT ON outside_t FOR EACH ROW EXECUTE FUNCTION outside_effect()",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "triggers": {
      "added": [
        [
          {
            "oid": "219155",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "219154",
            "tgname": "outside_trigger",
            "tgqual": null,
            "tgtype": 5,
            "tgnargs": 0,
            "tgrelid": "219149",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "0",
            "tgdeferrable": false,
            "tgisinternal": false,
            "tgconstrindid": "0",
            "tgconstrrelid": "0",
            "tginitdeferred": false
          }
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E043 — outside FK not valid

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE TABLE outside_fk(sid text);
ALTER TABLE outside_fk ADD CONSTRAINT f FOREIGN KEY(sid) REFERENCES mneme_store NOT VALID;
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE TABLE outside_fk(sid text)",
      "result": "OK"
    },
    {
      "sql": "ALTER TABLE outside_fk ADD CONSTRAINT f FOREIGN KEY(sid) REFERENCES mneme_store NOT VALID",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_constraint",
          219205,
          0,
          "pg_class",
          219164,
          1,
          "n",
          "constraint f on table outside_fk"
        ]
      ],
      "removed": []
    },
    "triggers": {
      "added": [
        [
          {
            "oid": "219206",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "1654",
            "tgname": "RI_ConstraintTrigger_a_219206",
            "tgqual": null,
            "tgtype": 9,
            "tgnargs": 0,
            "tgrelid": "219164",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "219205",
            "tgdeferrable": false,
            "tgisinternal": true,
            "tgconstrindid": "219171",
            "tgconstrrelid": "219200",
            "tginitdeferred": false
          }
        ],
        [
          {
            "oid": "219207",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "1655",
            "tgname": "RI_ConstraintTrigger_a_219207",
            "tgqual": null,
            "tgtype": 17,
            "tgnargs": 0,
            "tgrelid": "219164",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "219205",
            "tgdeferrable": false,
            "tgisinternal": true,
            "tgconstrindid": "219171",
            "tgconstrrelid": "219200",
            "tginitdeferred": false
          }
        ],
        [
          {
            "oid": "219208",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "1644",
            "tgname": "RI_ConstraintTrigger_c_219208",
            "tgqual": null,
            "tgtype": 5,
            "tgnargs": 0,
            "tgrelid": "219200",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "219205",
            "tgdeferrable": false,
            "tgisinternal": true,
            "tgconstrindid": "219171",
            "tgconstrrelid": "219164",
            "tginitdeferred": false
          }
        ],
        [
          {
            "oid": "219209",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "1645",
            "tgname": "RI_ConstraintTrigger_c_219209",
            "tgqual": null,
            "tgtype": 17,
            "tgnargs": 0,
            "tgrelid": "219200",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "219205",
            "tgdeferrable": false,
            "tgisinternal": true,
            "tgconstrindid": "219171",
            "tgconstrrelid": "219164",
            "tginitdeferred": false
          }
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": "triggers",
  "public": {
    "error": {
      "type": "MnemeValidationError",
      "code": "persistence.schema_incompatible",
      "sqlstate": null,
      "message": "persistence.schema_incompatible: the mneme_ catalog of schema 'xe043' differs from v1 in its triggers"
    }
  }
}
```

### E044 — outside typed table

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE TABLE outside_t OF mneme_store;
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE TABLE outside_t OF mneme_store",
      "error": {
        "type": "WrongObjectType",
        "code": null,
        "sqlstate": "42809",
        "message": "type mneme_store is not a composite type"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

### E045 — outside partition attach attempt

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE TABLE outside_parent (LIKE mneme_store INCLUDING ALL) PARTITION BY LIST(store_id);
ALTER TABLE outside_parent ATTACH PARTITION mneme_store DEFAULT;
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE TABLE outside_parent (LIKE mneme_store INCLUDING ALL) PARTITION BY LIST(store_id)",
      "result": "OK"
    },
    {
      "sql": "ALTER TABLE outside_parent ATTACH PARTITION mneme_store DEFAULT",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "class": {
      "mneme_store": {
        "relispartition": [
          false,
          true
        ],
        "relpartbound": [
          null,
          "{PARTITIONBOUNDSPEC :strategy l :is_default true :modulus 0 :remainder 0 :listdatums <> :lowerdatums <> :upperdatums <> :location 56}"
        ]
      },
      "mneme_store_pkey": {
        "relispartition": [
          false,
          true
        ]
      }
    },
    "attribute": {
      "mneme_store.1": {
        "attislocal": [
          true,
          false
        ],
        "attinhcount": [
          0,
          1
        ]
      },
      "mneme_store.2": {
        "attislocal": [
          true,
          false
        ],
        "attinhcount": [
          0,
          1
        ]
      }
    },
    "inbound": {
      "added": [
        [
          "pg_class",
          219269,
          0,
          "pg_class",
          219262,
          0,
          "S",
          "index mneme_store_pkey"
        ],
        [
          "pg_constraint",
          219270,
          0,
          "pg_class",
          219262,
          0,
          "S",
          "constraint mneme_store_pkey on table mneme_store"
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": "relations",
  "public": {
    "error": {
      "type": "MnemeValidationError",
      "code": "persistence.schema_incompatible",
      "sqlstate": null,
      "message": "persistence.schema_incompatible: the mneme_ catalog of schema 'xe045' differs from v1 in its relations"
    }
  }
}
```

### E046 — renamed index identity

Setup starts with fresh public initialization; no pre-existing store data.

```sql
ALTER INDEX mneme_store_pkey RENAME TO outside_name;
```

```json
{
  "setup_results": [
    {
      "sql": "ALTER INDEX mneme_store_pkey RENAME TO outside_name",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "class": {
      "mneme_store_pkey": {
        "removed": {
          "oid": "219320",
          "relam": "403",
          "relacl": null,
          "relkind": "i",
          "relname": "mneme_store_pkey",
          "reltype": "0",
          "relnatts": 1,
          "relowner": "16901",
          "relpages": 1,
          "relchecks": 0,
          "reloftype": "0",
          "reltuples": 0,
          "relminmxid": "0",
          "reloptions": null,
          "relrewrite": "0",
          "relfilenode": "219320",
          "relhasindex": false,
          "relhasrules": false,
          "relisshared": false,
          "relfrozenxid": "0",
          "relnamespace": "219305",
          "relpartbound": null,
          "relreplident": "n",
          "relallvisible": 0,
          "reltablespace": "0",
          "reltoastrelid": "0",
          "relhassubclass": false,
          "relhastriggers": false,
          "relispartition": false,
          "relispopulated": true,
          "relpersistence": "p",
          "relrowsecurity": false,
          "relforcerowsecurity": false
        }
      },
      "outside_name": {
        "added": {
          "oid": "219320",
          "relam": "403",
          "relacl": null,
          "relkind": "i",
          "relname": "outside_name",
          "reltype": "0",
          "relnatts": 1,
          "relowner": "16901",
          "relpages": 1,
          "relchecks": 0,
          "reloftype": "0",
          "reltuples": 0,
          "relminmxid": "0",
          "reloptions": null,
          "relrewrite": "0",
          "relfilenode": "219320",
          "relhasindex": false,
          "relhasrules": false,
          "relisshared": false,
          "relfrozenxid": "0",
          "relnamespace": "219305",
          "relpartbound": null,
          "relreplident": "n",
          "relallvisible": 0,
          "reltablespace": "0",
          "reltoastrelid": "0",
          "relhassubclass": false,
          "relhastriggers": false,
          "relispartition": false,
          "relispopulated": true,
          "relpersistence": "p",
          "relrowsecurity": false,
          "relforcerowsecurity": false
        }
      }
    },
    "attribute": {
      "mneme_store_pkey.1": {
        "removed": {
          "attacl": null,
          "attlen": -1,
          "attnum": 1,
          "attname": "store_id",
          "attalign": "i",
          "attbyval": false,
          "attndims": 0,
          "attrelid": "219320",
          "atttypid": "25",
          "atthasdef": false,
          "atttypmod": -1,
          "attislocal": true,
          "attnotnull": false,
          "attoptions": null,
          "attstorage": "x",
          "attcacheoff": -1,
          "attidentity": "",
          "attinhcount": 0,
          "attcollation": "100",
          "attgenerated": "",
          "attisdropped": false,
          "attfdwoptions": null,
          "atthasmissing": false,
          "attstattarget": -1,
          "attcompression": "",
          "attmissingval": null
        }
      },
      "outside_name.1": {
        "added": {
          "attacl": null,
          "attlen": -1,
          "attnum": 1,
          "attname": "store_id",
          "attalign": "i",
          "attbyval": false,
          "attndims": 0,
          "attrelid": "219320",
          "atttypid": "25",
          "atthasdef": false,
          "atttypmod": -1,
          "attislocal": true,
          "attnotnull": false,
          "attoptions": null,
          "attstorage": "x",
          "attcacheoff": -1,
          "attidentity": "",
          "attinhcount": 0,
          "attcollation": "100",
          "attgenerated": "",
          "attisdropped": false,
          "attfdwoptions": null,
          "atthasmissing": false,
          "attstattarget": -1,
          "attcompression": "",
          "attmissingval": null
        }
      }
    },
    "index": {
      "mneme_store_pkey": {
        "removed": {
          "indkey": [
            1
          ],
          "indpred": null,
          "indclass": [
            "3126"
          ],
          "indexprs": null,
          "indnatts": 1,
          "indrelid": "219313",
          "indislive": true,
          "indoption": [
            0
          ],
          "indexrelid": "219320",
          "indisready": true,
          "indisvalid": true,
          "indisunique": true,
          "indnkeyatts": 1,
          "indcheckxmin": false,
          "indcollation": [
            "100"
          ],
          "indimmediate": true,
          "indisprimary": true,
          "indisclustered": false,
          "indisexclusion": false,
          "indisreplident": false
        }
      },
      "outside_name": {
        "added": {
          "indkey": [
            1
          ],
          "indpred": null,
          "indclass": [
            "3126"
          ],
          "indexprs": null,
          "indnatts": 1,
          "indrelid": "219313",
          "indislive": true,
          "indoption": [
            0
          ],
          "indexrelid": "219320",
          "indisready": true,
          "indisvalid": true,
          "indisunique": true,
          "indnkeyatts": 1,
          "indcheckxmin": false,
          "indcollation": [
            "100"
          ],
          "indimmediate": true,
          "indisprimary": true,
          "indisclustered": false,
          "indisexclusion": false,
          "indisreplident": false
        }
      }
    },
    "inbound": {
      "added": [
        [
          "pg_constraint",
          219321,
          0,
          "pg_class",
          219313,
          1,
          "a",
          "constraint outside_name on table mneme_store"
        ]
      ],
      "removed": [
        [
          "pg_constraint",
          219321,
          0,
          "pg_class",
          219313,
          1,
          "a",
          "constraint mneme_store_pkey on table mneme_store"
        ]
      ]
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E047 — extra index control

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE INDEX outside_index ON mneme_store(tail);
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE INDEX outside_index ON mneme_store(tail)",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "class": {
      "outside_index": {
        "added": {
          "oid": "219393",
          "relam": "403",
          "relacl": null,
          "relkind": "i",
          "relname": "outside_index",
          "reltype": "0",
          "relnatts": 1,
          "relowner": "16901",
          "relpages": 1,
          "relchecks": 0,
          "reloftype": "0",
          "reltuples": 0,
          "relminmxid": "0",
          "reloptions": null,
          "relrewrite": "0",
          "relfilenode": "219393",
          "relhasindex": false,
          "relhasrules": false,
          "relisshared": false,
          "relfrozenxid": "0",
          "relnamespace": "219349",
          "relpartbound": null,
          "relreplident": "n",
          "relallvisible": 0,
          "reltablespace": "0",
          "reltoastrelid": "0",
          "relhassubclass": false,
          "relhastriggers": false,
          "relispartition": false,
          "relispopulated": true,
          "relpersistence": "p",
          "relrowsecurity": false,
          "relforcerowsecurity": false
        }
      }
    },
    "attribute": {
      "outside_index.1": {
        "added": {
          "attacl": null,
          "attlen": 8,
          "attnum": 1,
          "attname": "tail",
          "attalign": "d",
          "attbyval": true,
          "attndims": 0,
          "attrelid": "219393",
          "atttypid": "20",
          "atthasdef": false,
          "atttypmod": -1,
          "attislocal": true,
          "attnotnull": false,
          "attoptions": null,
          "attstorage": "p",
          "attcacheoff": -1,
          "attidentity": "",
          "attinhcount": 0,
          "attcollation": "0",
          "attgenerated": "",
          "attisdropped": false,
          "attfdwoptions": null,
          "atthasmissing": false,
          "attstattarget": -1,
          "attcompression": "",
          "attmissingval": null
        }
      }
    },
    "index": {
      "outside_index": {
        "added": {
          "indkey": [
            2
          ],
          "indpred": null,
          "indclass": [
            "3124"
          ],
          "indexprs": null,
          "indnatts": 1,
          "indrelid": "219357",
          "indislive": true,
          "indoption": [
            0
          ],
          "indexrelid": "219393",
          "indisready": true,
          "indisvalid": true,
          "indisunique": false,
          "indnkeyatts": 1,
          "indcheckxmin": false,
          "indcollation": [
            "0"
          ],
          "indimmediate": true,
          "indisprimary": false,
          "indisclustered": false,
          "indisexclusion": false,
          "indisreplident": false
        }
      }
    },
    "inbound": {
      "added": [
        [
          "pg_class",
          219393,
          0,
          "pg_class",
          219357,
          2,
          "a",
          "index outside_index"
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": "indexes",
  "public": {
    "error": {
      "type": "MnemeValidationError",
      "code": "persistence.schema_incompatible",
      "sqlstate": null,
      "message": "persistence.schema_incompatible: the mneme_ catalog of schema 'xe047' differs from v1 in its indexes"
    }
  }
}
```

### E048 — catalog edit privilege boundary

Setup starts with fresh public initialization; no pre-existing store data.

```sql
UPDATE pg_catalog.pg_attribute SET attcacheoff=0 WHERE attrelid='mneme_store'::regclass AND attname='tail';
```

```json
{
  "setup_results": [
    {
      "sql": "UPDATE pg_catalog.pg_attribute SET attcacheoff=0 WHERE attrelid='mneme_store'::regclass AND attname='tail'",
      "error": {
        "type": "InsufficientPrivilege",
        "code": null,
        "sqlstate": "42501",
        "message": "permission denied for table pg_attribute"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

### E049 — baseline catalog routes and dependency closure

Setup starts with fresh public initialization; no pre-existing store data.

```sql
-- no variation
```

```json
{
  "setup_results": [],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E050 — outside FROM constraint on mneme_schema

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE TABLE outside_t(sid text);
CREATE FUNCTION noop() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NEW; END$$;
CREATE CONSTRAINT TRIGGER outside_constraint AFTER INSERT ON outside_t FROM mneme_schema FOR EACH ROW EXECUTE FUNCTION noop();
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE TABLE outside_t(sid text)",
      "result": "OK"
    },
    {
      "sql": "CREATE FUNCTION noop() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NEW; END$$",
      "result": "OK"
    },
    {
      "sql": "CREATE CONSTRAINT TRIGGER outside_constraint AFTER INSERT ON outside_t FROM mneme_schema FOR EACH ROW EXECUTE FUNCTION noop()",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_trigger",
          219533,
          0,
          "pg_class",
          219484,
          0,
          "a",
          "trigger outside_constraint on table outside_t"
        ]
      ],
      "removed": []
    },
    "triggers": {
      "added": [
        [
          {
            "oid": "219533",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "219532",
            "tgname": "outside_constraint",
            "tgqual": null,
            "tgtype": 5,
            "tgnargs": 0,
            "tgrelid": "219527",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "219534",
            "tgdeferrable": false,
            "tgisinternal": false,
            "tgconstrindid": "0",
            "tgconstrrelid": "219484",
            "tginitdeferred": false
          }
        ]
      ],
      "removed": []
    },
    "depend_closure": {
      "added": [
        [
          "pg_constraint",
          219534,
          "constraint outside_constraint on table outside_t"
        ],
        [
          "pg_trigger",
          219533,
          "trigger outside_constraint on table outside_t"
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E051 — outside FROM constraint on mneme_record

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE TABLE outside_t(sid text);
CREATE FUNCTION noop() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NEW; END$$;
CREATE CONSTRAINT TRIGGER outside_constraint AFTER INSERT ON outside_t FROM mneme_record FOR EACH ROW EXECUTE FUNCTION noop();
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE TABLE outside_t(sid text)",
      "result": "OK"
    },
    {
      "sql": "CREATE FUNCTION noop() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NEW; END$$",
      "result": "OK"
    },
    {
      "sql": "CREATE CONSTRAINT TRIGGER outside_constraint AFTER INSERT ON outside_t FROM mneme_record FOR EACH ROW EXECUTE FUNCTION noop()",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_trigger",
          219585,
          0,
          "pg_class",
          219552,
          0,
          "a",
          "trigger outside_constraint on table outside_t"
        ]
      ],
      "removed": []
    },
    "triggers": {
      "added": [
        [
          {
            "oid": "219585",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "219584",
            "tgname": "outside_constraint",
            "tgqual": null,
            "tgtype": 5,
            "tgnargs": 0,
            "tgrelid": "219579",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "219586",
            "tgdeferrable": false,
            "tgisinternal": false,
            "tgconstrindid": "0",
            "tgconstrrelid": "219552",
            "tginitdeferred": false
          }
        ]
      ],
      "removed": []
    },
    "depend_closure": {
      "added": [
        [
          "pg_constraint",
          219586,
          "constraint outside_constraint on table outside_t"
        ],
        [
          "pg_trigger",
          219585,
          "trigger outside_constraint on table outside_t"
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E052 — outside FROM constraint on mneme_operation

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE TABLE outside_t(sid text);
CREATE FUNCTION noop() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NEW; END$$;
CREATE CONSTRAINT TRIGGER outside_constraint AFTER INSERT ON outside_t FROM mneme_operation FOR EACH ROW EXECUTE FUNCTION noop();
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE TABLE outside_t(sid text)",
      "result": "OK"
    },
    {
      "sql": "CREATE FUNCTION noop() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NEW; END$$",
      "result": "OK"
    },
    {
      "sql": "CREATE CONSTRAINT TRIGGER outside_constraint AFTER INSERT ON outside_t FROM mneme_operation FOR EACH ROW EXECUTE FUNCTION noop()",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_trigger",
          219637,
          0,
          "pg_class",
          219619,
          0,
          "a",
          "trigger outside_constraint on table outside_t"
        ]
      ],
      "removed": []
    },
    "triggers": {
      "added": [
        [
          {
            "oid": "219637",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "219636",
            "tgname": "outside_constraint",
            "tgqual": null,
            "tgtype": 5,
            "tgnargs": 0,
            "tgrelid": "219631",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "219638",
            "tgdeferrable": false,
            "tgisinternal": false,
            "tgconstrindid": "0",
            "tgconstrrelid": "219619",
            "tginitdeferred": false
          }
        ]
      ],
      "removed": []
    },
    "depend_closure": {
      "added": [
        [
          "pg_constraint",
          219638,
          "constraint outside_constraint on table outside_t"
        ],
        [
          "pg_trigger",
          219637,
          "trigger outside_constraint on table outside_t"
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E053 — outside FK schema target

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE TABLE outside_fk(v boolean REFERENCES mneme_schema(singleton));
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE TABLE outside_fk(v boolean REFERENCES mneme_schema(singleton))",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "class": {
      "mneme_schema": {
        "relhastriggers": [
          false,
          true
        ]
      }
    },
    "inbound": {
      "added": [
        [
          "pg_constraint",
          219686,
          0,
          "pg_class",
          219640,
          1,
          "n",
          "constraint outside_fk_v_fkey on table outside_fk"
        ]
      ],
      "removed": []
    },
    "triggers": {
      "added": [
        [
          {
            "oid": "219687",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "1654",
            "tgname": "RI_ConstraintTrigger_a_219687",
            "tgqual": null,
            "tgtype": 9,
            "tgnargs": 0,
            "tgrelid": "219640",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "219686",
            "tgdeferrable": false,
            "tgisinternal": true,
            "tgconstrindid": "219645",
            "tgconstrrelid": "219683",
            "tginitdeferred": false
          }
        ],
        [
          {
            "oid": "219688",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "1655",
            "tgname": "RI_ConstraintTrigger_a_219688",
            "tgqual": null,
            "tgtype": 17,
            "tgnargs": 0,
            "tgrelid": "219640",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "219686",
            "tgdeferrable": false,
            "tgisinternal": true,
            "tgconstrindid": "219645",
            "tgconstrrelid": "219683",
            "tginitdeferred": false
          }
        ],
        [
          {
            "oid": "219689",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "1644",
            "tgname": "RI_ConstraintTrigger_c_219689",
            "tgqual": null,
            "tgtype": 5,
            "tgnargs": 0,
            "tgrelid": "219683",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "219686",
            "tgdeferrable": false,
            "tgisinternal": true,
            "tgconstrindid": "219645",
            "tgconstrrelid": "219640",
            "tginitdeferred": false
          }
        ],
        [
          {
            "oid": "219690",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "1645",
            "tgname": "RI_ConstraintTrigger_c_219690",
            "tgqual": null,
            "tgtype": 17,
            "tgnargs": 0,
            "tgrelid": "219683",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "219686",
            "tgdeferrable": false,
            "tgisinternal": true,
            "tgconstrindid": "219645",
            "tgconstrrelid": "219640",
            "tginitdeferred": false
          }
        ]
      ],
      "removed": []
    },
    "depend_closure": {
      "added": [
        [
          "pg_constraint",
          219686,
          "constraint outside_fk_v_fkey on table outside_fk"
        ],
        [
          "pg_trigger",
          219687,
          "trigger RI_ConstraintTrigger_a_219687 on table mneme_schema"
        ],
        [
          "pg_trigger",
          219688,
          "trigger RI_ConstraintTrigger_a_219688 on table mneme_schema"
        ],
        [
          "pg_trigger",
          219689,
          "trigger RI_ConstraintTrigger_c_219689 on table outside_fk"
        ],
        [
          "pg_trigger",
          219690,
          "trigger RI_ConstraintTrigger_c_219690 on table outside_fk"
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": "triggers",
  "public": {
    "error": {
      "type": "MnemeValidationError",
      "code": "persistence.schema_incompatible",
      "sqlstate": null,
      "message": "persistence.schema_incompatible: the mneme_ catalog of schema 'xe053' differs from v1 in its triggers"
    }
  }
}
```

### E054 — outside FK record target

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE TABLE outside_fk(s text,p bigint,FOREIGN KEY(s,p) REFERENCES mneme_record(store_id,position));
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE TABLE outside_fk(s text,p bigint,FOREIGN KEY(s,p) REFERENCES mneme_record(store_id,position))",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_constraint",
          219740,
          0,
          "pg_class",
          219708,
          1,
          "n",
          "constraint outside_fk_s_p_fkey on table outside_fk"
        ],
        [
          "pg_constraint",
          219740,
          0,
          "pg_class",
          219708,
          2,
          "n",
          "constraint outside_fk_s_p_fkey on table outside_fk"
        ]
      ],
      "removed": []
    },
    "triggers": {
      "added": [
        [
          {
            "oid": "219741",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "1654",
            "tgname": "RI_ConstraintTrigger_a_219741",
            "tgqual": null,
            "tgtype": 9,
            "tgnargs": 0,
            "tgrelid": "219708",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "219740",
            "tgdeferrable": false,
            "tgisinternal": true,
            "tgconstrindid": "219714",
            "tgconstrrelid": "219735",
            "tginitdeferred": false
          }
        ],
        [
          {
            "oid": "219742",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "1655",
            "tgname": "RI_ConstraintTrigger_a_219742",
            "tgqual": null,
            "tgtype": 17,
            "tgnargs": 0,
            "tgrelid": "219708",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "219740",
            "tgdeferrable": false,
            "tgisinternal": true,
            "tgconstrindid": "219714",
            "tgconstrrelid": "219735",
            "tginitdeferred": false
          }
        ],
        [
          {
            "oid": "219743",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "1644",
            "tgname": "RI_ConstraintTrigger_c_219743",
            "tgqual": null,
            "tgtype": 5,
            "tgnargs": 0,
            "tgrelid": "219735",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "219740",
            "tgdeferrable": false,
            "tgisinternal": true,
            "tgconstrindid": "219714",
            "tgconstrrelid": "219708",
            "tginitdeferred": false
          }
        ],
        [
          {
            "oid": "219744",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "1645",
            "tgname": "RI_ConstraintTrigger_c_219744",
            "tgqual": null,
            "tgtype": 17,
            "tgnargs": 0,
            "tgrelid": "219735",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "219740",
            "tgdeferrable": false,
            "tgisinternal": true,
            "tgconstrindid": "219714",
            "tgconstrrelid": "219708",
            "tginitdeferred": false
          }
        ]
      ],
      "removed": []
    },
    "depend_closure": {
      "added": [
        [
          "pg_constraint",
          219740,
          "constraint outside_fk_s_p_fkey on table outside_fk"
        ],
        [
          "pg_trigger",
          219741,
          "trigger RI_ConstraintTrigger_a_219741 on table mneme_record"
        ],
        [
          "pg_trigger",
          219742,
          "trigger RI_ConstraintTrigger_a_219742 on table mneme_record"
        ],
        [
          "pg_trigger",
          219743,
          "trigger RI_ConstraintTrigger_c_219743 on table outside_fk"
        ],
        [
          "pg_trigger",
          219744,
          "trigger RI_ConstraintTrigger_c_219744 on table outside_fk"
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": "triggers",
  "public": {
    "error": {
      "type": "MnemeValidationError",
      "code": "persistence.schema_incompatible",
      "sqlstate": null,
      "message": "persistence.schema_incompatible: the mneme_ catalog of schema 'xe054' differs from v1 in its triggers"
    }
  }
}
```

### E055 — outside FK operation target

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE TABLE outside_fk(s text,n text,i bytea,FOREIGN KEY(s,n,i) REFERENCES mneme_operation(store_id,source_namespace,source_operation_id));
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE TABLE outside_fk(s text,n text,i bytea,FOREIGN KEY(s,n,i) REFERENCES mneme_operation(store_id,source_namespace,source_operation_id))",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_constraint",
          219794,
          0,
          "pg_class",
          219777,
          1,
          "n",
          "constraint outside_fk_s_n_i_fkey on table outside_fk"
        ],
        [
          "pg_constraint",
          219794,
          0,
          "pg_class",
          219777,
          2,
          "n",
          "constraint outside_fk_s_n_i_fkey on table outside_fk"
        ],
        [
          "pg_constraint",
          219794,
          0,
          "pg_class",
          219777,
          3,
          "n",
          "constraint outside_fk_s_n_i_fkey on table outside_fk"
        ]
      ],
      "removed": []
    },
    "triggers": {
      "added": [
        [
          {
            "oid": "219795",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "1654",
            "tgname": "RI_ConstraintTrigger_a_219795",
            "tgqual": null,
            "tgtype": 9,
            "tgnargs": 0,
            "tgrelid": "219777",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "219794",
            "tgdeferrable": false,
            "tgisinternal": true,
            "tgconstrindid": "219782",
            "tgconstrrelid": "219789",
            "tginitdeferred": false
          }
        ],
        [
          {
            "oid": "219796",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "1655",
            "tgname": "RI_ConstraintTrigger_a_219796",
            "tgqual": null,
            "tgtype": 17,
            "tgnargs": 0,
            "tgrelid": "219777",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "219794",
            "tgdeferrable": false,
            "tgisinternal": true,
            "tgconstrindid": "219782",
            "tgconstrrelid": "219789",
            "tginitdeferred": false
          }
        ],
        [
          {
            "oid": "219797",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "1644",
            "tgname": "RI_ConstraintTrigger_c_219797",
            "tgqual": null,
            "tgtype": 5,
            "tgnargs": 0,
            "tgrelid": "219789",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "219794",
            "tgdeferrable": false,
            "tgisinternal": true,
            "tgconstrindid": "219782",
            "tgconstrrelid": "219777",
            "tginitdeferred": false
          }
        ],
        [
          {
            "oid": "219798",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "1645",
            "tgname": "RI_ConstraintTrigger_c_219798",
            "tgqual": null,
            "tgtype": 17,
            "tgnargs": 0,
            "tgrelid": "219789",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "219794",
            "tgdeferrable": false,
            "tgisinternal": true,
            "tgconstrindid": "219782",
            "tgconstrrelid": "219777",
            "tginitdeferred": false
          }
        ]
      ],
      "removed": []
    },
    "depend_closure": {
      "added": [
        [
          "pg_constraint",
          219794,
          "constraint outside_fk_s_n_i_fkey on table outside_fk"
        ],
        [
          "pg_trigger",
          219795,
          "trigger RI_ConstraintTrigger_a_219795 on table mneme_operation"
        ],
        [
          "pg_trigger",
          219796,
          "trigger RI_ConstraintTrigger_a_219796 on table mneme_operation"
        ],
        [
          "pg_trigger",
          219797,
          "trigger RI_ConstraintTrigger_c_219797 on table outside_fk"
        ],
        [
          "pg_trigger",
          219798,
          "trigger RI_ConstraintTrigger_c_219798 on table outside_fk"
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": "triggers",
  "public": {
    "error": {
      "type": "MnemeValidationError",
      "code": "persistence.schema_incompatible",
      "sqlstate": null,
      "message": "persistence.schema_incompatible: the mneme_ catalog of schema 'xe055' differs from v1 in its triggers"
    }
  }
}
```

### E056 — unrelated outside object positive

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE TABLE outside_unrelated(v text);
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE TABLE outside_unrelated(v text)",
      "result": "OK"
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E057 — transitive array and domain dependency

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE DOMAIN outside_domain AS mneme_store;
CREATE TABLE outside_arr(v outside_domain[]);
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE DOMAIN outside_domain AS mneme_store",
      "result": "OK"
    },
    {
      "sql": "CREATE TABLE outside_arr(v outside_domain[])",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_type",
          219893,
          0,
          "pg_type",
          219858,
          0,
          "n",
          "type outside_domain"
        ]
      ],
      "removed": []
    },
    "depend_closure": {
      "added": [
        [
          "pg_class",
          219894,
          "table outside_arr"
        ],
        [
          "pg_class",
          219897,
          "toast table pg_toast.pg_toast_219894"
        ],
        [
          "pg_class",
          219898,
          "index pg_toast.pg_toast_219894_index"
        ],
        [
          "pg_type",
          219892,
          "type outside_domain[]"
        ],
        [
          "pg_type",
          219893,
          "type outside_domain"
        ],
        [
          "pg_type",
          219895,
          "type outside_arr[]"
        ],
        [
          "pg_type",
          219896,
          "type outside_arr"
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E058 — function result dependency

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE FUNCTION outside_fun() RETURNS mneme_store LANGUAGE SQL AS $$ SELECT ROW('x',0)::mneme_store $$;
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE FUNCTION outside_fun() RETURNS mneme_store LANGUAGE SQL AS $$ SELECT ROW('x',0)::mneme_store $$",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_proc",
          219943,
          0,
          "pg_type",
          219909,
          0,
          "n",
          "function outside_fun()"
        ]
      ],
      "removed": []
    },
    "depend_closure": {
      "added": [
        [
          "pg_proc",
          219943,
          "function outside_fun()"
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E059 — aggregate type dependency

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE FUNCTION outside_state(mneme_store,mneme_store) RETURNS mneme_store LANGUAGE SQL AS $$ SELECT $1 $$;
CREATE AGGREGATE outside_agg(mneme_store) (SFUNC=outside_state,STYPE=mneme_store);
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE FUNCTION outside_state(mneme_store,mneme_store) RETURNS mneme_store LANGUAGE SQL AS $$ SELECT $1 $$",
      "result": "OK"
    },
    {
      "sql": "CREATE AGGREGATE outside_agg(mneme_store) (SFUNC=outside_state,STYPE=mneme_store)",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_proc",
          219988,
          0,
          "pg_type",
          219954,
          0,
          "n",
          "function outside_state(mneme_store,mneme_store)"
        ],
        [
          "pg_proc",
          219989,
          0,
          "pg_type",
          219954,
          0,
          "n",
          "function outside_agg(mneme_store)"
        ]
      ],
      "removed": []
    },
    "depend_closure": {
      "added": [
        [
          "pg_proc",
          219988,
          "function outside_state(mneme_store,mneme_store)"
        ],
        [
          "pg_proc",
          219989,
          "function outside_agg(mneme_store)"
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E060 — operator type dependency

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE FUNCTION outside_eq(mneme_store,mneme_store) RETURNS boolean LANGUAGE SQL IMMUTABLE AS $$ SELECT $1.store_id=$2.store_id $$;
CREATE OPERATOR === (LEFTARG=mneme_store,RIGHTARG=mneme_store,FUNCTION=outside_eq);
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE FUNCTION outside_eq(mneme_store,mneme_store) RETURNS boolean LANGUAGE SQL IMMUTABLE AS $$ SELECT $1.store_id=$2.store_id $$",
      "result": "OK"
    },
    {
      "sql": "CREATE OPERATOR === (LEFTARG=mneme_store,RIGHTARG=mneme_store,FUNCTION=outside_eq)",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_operator",
          220035,
          0,
          "pg_type",
          220000,
          0,
          "n",
          "operator ===(mneme_store,mneme_store)"
        ],
        [
          "pg_proc",
          220034,
          0,
          "pg_type",
          220000,
          0,
          "n",
          "function outside_eq(mneme_store,mneme_store)"
        ]
      ],
      "removed": []
    },
    "depend_closure": {
      "added": [
        [
          "pg_operator",
          220035,
          "operator ===(mneme_store,mneme_store)"
        ],
        [
          "pg_proc",
          220034,
          "function outside_eq(mneme_store,mneme_store)"
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E061 — cast type dependency

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE FUNCTION outside_cast(mneme_store) RETURNS text LANGUAGE SQL AS $$ SELECT $1.store_id $$;
CREATE CAST(mneme_store AS text) WITH FUNCTION outside_cast(mneme_store);
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE FUNCTION outside_cast(mneme_store) RETURNS text LANGUAGE SQL AS $$ SELECT $1.store_id $$",
      "result": "OK"
    },
    {
      "sql": "CREATE CAST(mneme_store AS text) WITH FUNCTION outside_cast(mneme_store)",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_cast",
          220081,
          0,
          "pg_type",
          220046,
          0,
          "n",
          "cast from mneme_store to text"
        ],
        [
          "pg_proc",
          220080,
          0,
          "pg_type",
          220046,
          0,
          "n",
          "function outside_cast(mneme_store)"
        ]
      ],
      "removed": []
    },
    "depend_closure": {
      "added": [
        [
          "pg_cast",
          220081,
          "cast from mneme_store to text"
        ],
        [
          "pg_proc",
          220080,
          "function outside_cast(mneme_store)"
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E062 — extension binding attempt

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE EXTENSION hstore;
ALTER EXTENSION hstore ADD TABLE mneme_store;
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE EXTENSION hstore",
      "result": "OK"
    },
    {
      "sql": "ALTER EXTENSION hstore ADD TABLE mneme_store",
      "result": "OK"
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E063 — event trigger privilege boundary

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE FUNCTION outside_event() RETURNS event_trigger LANGUAGE plpgsql AS $$ BEGIN NULL; END $$;
CREATE EVENT TRIGGER ce04_event ON ddl_command_end EXECUTE FUNCTION outside_event();
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE FUNCTION outside_event() RETURNS event_trigger LANGUAGE plpgsql AS $$ BEGIN NULL; END $$",
      "result": "OK"
    },
    {
      "sql": "CREATE EVENT TRIGGER ce04_event ON ddl_command_end EXECUTE FUNCTION outside_event()",
      "error": {
        "type": "InsufficientPrivilege",
        "code": null,
        "sqlstate": "42501",
        "message": "permission denied to create event trigger \"ce04_event\"\nHINT:  Must be superuser to create an event trigger."
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

### E064 — subscription privilege boundary

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE SUBSCRIPTION ce04_sub CONNECTION 'host=127.0.0.1 dbname=not_used' PUBLICATION not_used WITH(connect=false,create_slot=false,enabled=false);
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE SUBSCRIPTION ce04_sub CONNECTION 'host=127.0.0.1 dbname=not_used' PUBLICATION not_used WITH(connect=false,create_slot=false,enabled=false)",
      "error": {
        "type": "InsufficientPrivilege",
        "code": null,
        "sqlstate": "42501",
        "message": "must be superuser to create subscriptions"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

### E065 — foreign table metadata inconsistency attempt

Setup starts with fresh public initialization; no pre-existing store data.

```sql
UPDATE pg_foreign_table SET ftserver=0 WHERE ftrelid='mneme_store'::regclass;
```

```json
{
  "setup_results": [
    {
      "sql": "UPDATE pg_foreign_table SET ftserver=0 WHERE ftrelid='mneme_store'::regclass",
      "error": {
        "type": "InsufficientPrivilege",
        "code": null,
        "sqlstate": "42501",
        "message": "permission denied for table pg_foreign_table"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

### E066 — predicate construction boundary pg_attribute.attlen

Setup starts with fresh public initialization; no pre-existing store data.

```sql
UPDATE pg_catalog.pg_attribute SET attlen=0 WHERE attrelid='mneme_store_pkey'::regclass AND attnum=1;
```

```json
{
  "setup_results": [
    {
      "sql": "UPDATE pg_catalog.pg_attribute SET attlen=0 WHERE attrelid='mneme_store_pkey'::regclass AND attnum=1",
      "error": {
        "type": "InsufficientPrivilege",
        "code": null,
        "sqlstate": "42501",
        "message": "permission denied for table pg_attribute"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

**Predicate domain:** altered metadata is unconstructed. Proposed semantic inconsistency controls must later bind a supplied field to comparison; this baseline pass cannot count as a kill.

### E067 — predicate construction boundary pg_attribute.attcacheoff

Setup starts with fresh public initialization; no pre-existing store data.

```sql
UPDATE pg_catalog.pg_attribute SET attcacheoff=0 WHERE attrelid='mneme_store_pkey'::regclass AND attnum=1;
```

```json
{
  "setup_results": [
    {
      "sql": "UPDATE pg_catalog.pg_attribute SET attcacheoff=0 WHERE attrelid='mneme_store_pkey'::regclass AND attnum=1",
      "error": {
        "type": "InsufficientPrivilege",
        "code": null,
        "sqlstate": "42501",
        "message": "permission denied for table pg_attribute"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

**Predicate domain:** altered metadata is unconstructed. Proposed semantic inconsistency controls must later bind a supplied field to comparison; this baseline pass cannot count as a kill.

### E068 — predicate construction boundary pg_attribute.attbyval

Setup starts with fresh public initialization; no pre-existing store data.

```sql
UPDATE pg_catalog.pg_attribute SET attbyval=false WHERE attrelid='mneme_store_pkey'::regclass AND attnum=1;
```

```json
{
  "setup_results": [
    {
      "sql": "UPDATE pg_catalog.pg_attribute SET attbyval=false WHERE attrelid='mneme_store_pkey'::regclass AND attnum=1",
      "error": {
        "type": "InsufficientPrivilege",
        "code": null,
        "sqlstate": "42501",
        "message": "permission denied for table pg_attribute"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

**Predicate domain:** altered metadata is unconstructed. Proposed semantic inconsistency controls must later bind a supplied field to comparison; this baseline pass cannot count as a kill.

### E069 — predicate construction boundary pg_attribute.attalign

Setup starts with fresh public initialization; no pre-existing store data.

```sql
UPDATE pg_catalog.pg_attribute SET attalign='d' WHERE attrelid='mneme_store_pkey'::regclass AND attnum=1;
```

```json
{
  "setup_results": [
    {
      "sql": "UPDATE pg_catalog.pg_attribute SET attalign='d' WHERE attrelid='mneme_store_pkey'::regclass AND attnum=1",
      "error": {
        "type": "InsufficientPrivilege",
        "code": null,
        "sqlstate": "42501",
        "message": "permission denied for table pg_attribute"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

**Predicate domain:** altered metadata is unconstructed. Proposed semantic inconsistency controls must later bind a supplied field to comparison; this baseline pass cannot count as a kill.

### E070 — predicate construction boundary pg_attribute.attfdwoptions

Setup starts with fresh public initialization; no pre-existing store data.

```sql
UPDATE pg_catalog.pg_attribute SET attfdwoptions=ARRAY['x=y'] WHERE attrelid='mneme_store_pkey'::regclass AND attnum=1;
```

```json
{
  "setup_results": [
    {
      "sql": "UPDATE pg_catalog.pg_attribute SET attfdwoptions=ARRAY['x=y'] WHERE attrelid='mneme_store_pkey'::regclass AND attnum=1",
      "error": {
        "type": "InsufficientPrivilege",
        "code": null,
        "sqlstate": "42501",
        "message": "permission denied for table pg_attribute"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

**Predicate domain:** altered metadata is unconstructed. Proposed semantic inconsistency controls must later bind a supplied field to comparison; this baseline pass cannot count as a kill.

### E071 — predicate construction boundary pg_attribute.attmissingval

Setup starts with fresh public initialization; no pre-existing store data.

```sql
UPDATE pg_catalog.pg_attribute SET attmissingval=NULL WHERE attrelid='mneme_store_pkey'::regclass AND attnum=1;
```

```json
{
  "setup_results": [
    {
      "sql": "UPDATE pg_catalog.pg_attribute SET attmissingval=NULL WHERE attrelid='mneme_store_pkey'::regclass AND attnum=1",
      "error": {
        "type": "InsufficientPrivilege",
        "code": null,
        "sqlstate": "42501",
        "message": "permission denied for table pg_attribute"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

**Predicate domain:** altered metadata is unconstructed. Proposed semantic inconsistency controls must later bind a supplied field to comparison; this baseline pass cannot count as a kill.

### E072 — predicate construction boundary pg_class.relisshared

Setup starts with fresh public initialization; no pre-existing store data.

```sql
UPDATE pg_catalog.pg_class SET relisshared=true WHERE oid='mneme_store_pkey'::regclass;
```

```json
{
  "setup_results": [
    {
      "sql": "UPDATE pg_catalog.pg_class SET relisshared=true WHERE oid='mneme_store_pkey'::regclass",
      "error": {
        "type": "InsufficientPrivilege",
        "code": null,
        "sqlstate": "42501",
        "message": "permission denied for table pg_class"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

**Predicate domain:** altered metadata is unconstructed. Proposed semantic inconsistency controls must later bind a supplied field to comparison; this baseline pass cannot count as a kill.

### E073 — predicate construction boundary pg_class.relispopulated

Setup starts with fresh public initialization; no pre-existing store data.

```sql
UPDATE pg_catalog.pg_class SET relispopulated=false WHERE oid='mneme_store_pkey'::regclass;
```

```json
{
  "setup_results": [
    {
      "sql": "UPDATE pg_catalog.pg_class SET relispopulated=false WHERE oid='mneme_store_pkey'::regclass",
      "error": {
        "type": "InsufficientPrivilege",
        "code": null,
        "sqlstate": "42501",
        "message": "permission denied for table pg_class"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

**Predicate domain:** altered metadata is unconstructed. Proposed semantic inconsistency controls must later bind a supplied field to comparison; this baseline pass cannot count as a kill.

### E074 — predicate construction boundary pg_class.relrewrite

Setup starts with fresh public initialization; no pre-existing store data.

```sql
UPDATE pg_catalog.pg_class SET relrewrite=1 WHERE oid='mneme_store_pkey'::regclass;
```

```json
{
  "setup_results": [
    {
      "sql": "UPDATE pg_catalog.pg_class SET relrewrite=1 WHERE oid='mneme_store_pkey'::regclass",
      "error": {
        "type": "InsufficientPrivilege",
        "code": null,
        "sqlstate": "42501",
        "message": "permission denied for table pg_class"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

**Predicate domain:** altered metadata is unconstructed. Proposed semantic inconsistency controls must later bind a supplied field to comparison; this baseline pass cannot count as a kill.

### E075 — predicate construction boundary pg_class.relpartbound

Setup starts with fresh public initialization; no pre-existing store data.

```sql
UPDATE pg_catalog.pg_class SET relpartbound=NULL WHERE oid='mneme_store_pkey'::regclass;
```

```json
{
  "setup_results": [
    {
      "sql": "UPDATE pg_catalog.pg_class SET relpartbound=NULL WHERE oid='mneme_store_pkey'::regclass",
      "error": {
        "type": "InsufficientPrivilege",
        "code": null,
        "sqlstate": "42501",
        "message": "permission denied for table pg_class"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

**Predicate domain:** altered metadata is unconstructed. Proposed semantic inconsistency controls must later bind a supplied field to comparison; this baseline pass cannot count as a kill.

### E076 — predicate construction boundary pg_class.relkind

Setup starts with fresh public initialization; no pre-existing store data.

```sql
UPDATE pg_catalog.pg_class SET relkind='I' WHERE oid='mneme_store_pkey'::regclass;
```

```json
{
  "setup_results": [
    {
      "sql": "UPDATE pg_catalog.pg_class SET relkind='I' WHERE oid='mneme_store_pkey'::regclass",
      "error": {
        "type": "InsufficientPrivilege",
        "code": null,
        "sqlstate": "42501",
        "message": "permission denied for table pg_class"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

**Predicate domain:** altered metadata is unconstructed. Proposed semantic inconsistency controls must later bind a supplied field to comparison; this baseline pass cannot count as a kill.

### E077 — predicate construction boundary pg_class.relpersistence

Setup starts with fresh public initialization; no pre-existing store data.

```sql
UPDATE pg_catalog.pg_class SET relpersistence='u' WHERE oid='mneme_store_pkey'::regclass;
```

```json
{
  "setup_results": [
    {
      "sql": "UPDATE pg_catalog.pg_class SET relpersistence='u' WHERE oid='mneme_store_pkey'::regclass",
      "error": {
        "type": "InsufficientPrivilege",
        "code": null,
        "sqlstate": "42501",
        "message": "permission denied for table pg_class"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

**Predicate domain:** altered metadata is unconstructed. Proposed semantic inconsistency controls must later bind a supplied field to comparison; this baseline pass cannot count as a kill.

### E078 — predicate construction boundary pg_class.relispartition

Setup starts with fresh public initialization; no pre-existing store data.

```sql
UPDATE pg_catalog.pg_class SET relispartition=true WHERE oid='mneme_store_pkey'::regclass;
```

```json
{
  "setup_results": [
    {
      "sql": "UPDATE pg_catalog.pg_class SET relispartition=true WHERE oid='mneme_store_pkey'::regclass",
      "error": {
        "type": "InsufficientPrivilege",
        "code": null,
        "sqlstate": "42501",
        "message": "permission denied for table pg_class"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

**Predicate domain:** altered metadata is unconstructed. Proposed semantic inconsistency controls must later bind a supplied field to comparison; this baseline pass cannot count as a kill.

### E079 — predicate construction boundary pg_class.reloftype

Setup starts with fresh public initialization; no pre-existing store data.

```sql
UPDATE pg_catalog.pg_class SET reloftype=1 WHERE oid='mneme_store_pkey'::regclass;
```

```json
{
  "setup_results": [
    {
      "sql": "UPDATE pg_catalog.pg_class SET reloftype=1 WHERE oid='mneme_store_pkey'::regclass",
      "error": {
        "type": "InsufficientPrivilege",
        "code": null,
        "sqlstate": "42501",
        "message": "permission denied for table pg_class"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

**Predicate domain:** altered metadata is unconstructed. Proposed semantic inconsistency controls must later bind a supplied field to comparison; this baseline pass cannot count as a kill.

### E080 — predicate construction boundary pg_class.relrowsecurity

Setup starts with fresh public initialization; no pre-existing store data.

```sql
UPDATE pg_catalog.pg_class SET relrowsecurity=true WHERE oid='mneme_store_pkey'::regclass;
```

```json
{
  "setup_results": [
    {
      "sql": "UPDATE pg_catalog.pg_class SET relrowsecurity=true WHERE oid='mneme_store_pkey'::regclass",
      "error": {
        "type": "InsufficientPrivilege",
        "code": null,
        "sqlstate": "42501",
        "message": "permission denied for table pg_class"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

**Predicate domain:** altered metadata is unconstructed. Proposed semantic inconsistency controls must later bind a supplied field to comparison; this baseline pass cannot count as a kill.

### E081 — predicate construction boundary pg_class.relforcerowsecurity

Setup starts with fresh public initialization; no pre-existing store data.

```sql
UPDATE pg_catalog.pg_class SET relforcerowsecurity=true WHERE oid='mneme_store_pkey'::regclass;
```

```json
{
  "setup_results": [
    {
      "sql": "UPDATE pg_catalog.pg_class SET relforcerowsecurity=true WHERE oid='mneme_store_pkey'::regclass",
      "error": {
        "type": "InsufficientPrivilege",
        "code": null,
        "sqlstate": "42501",
        "message": "permission denied for table pg_class"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

**Predicate domain:** altered metadata is unconstructed. Proposed semantic inconsistency controls must later bind a supplied field to comparison; this baseline pass cannot count as a kill.

### E082 — predicate construction boundary pg_class.relreplident

Setup starts with fresh public initialization; no pre-existing store data.

```sql
UPDATE pg_catalog.pg_class SET relreplident='f' WHERE oid='mneme_store_pkey'::regclass;
```

```json
{
  "setup_results": [
    {
      "sql": "UPDATE pg_catalog.pg_class SET relreplident='f' WHERE oid='mneme_store_pkey'::regclass",
      "error": {
        "type": "InsufficientPrivilege",
        "code": null,
        "sqlstate": "42501",
        "message": "permission denied for table pg_class"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

**Predicate domain:** altered metadata is unconstructed. Proposed semantic inconsistency controls must later bind a supplied field to comparison; this baseline pass cannot count as a kill.

### E083 — predicate construction boundary pg_class.relnatts

Setup starts with fresh public initialization; no pre-existing store data.

```sql
UPDATE pg_catalog.pg_class SET relnatts=1 WHERE oid='mneme_store_pkey'::regclass;
```

```json
{
  "setup_results": [
    {
      "sql": "UPDATE pg_catalog.pg_class SET relnatts=1 WHERE oid='mneme_store_pkey'::regclass",
      "error": {
        "type": "InsufficientPrivilege",
        "code": null,
        "sqlstate": "42501",
        "message": "permission denied for table pg_class"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

**Predicate domain:** altered metadata is unconstructed. Proposed semantic inconsistency controls must later bind a supplied field to comparison; this baseline pass cannot count as a kill.

### E084 — predicate construction boundary pg_class.relchecks

Setup starts with fresh public initialization; no pre-existing store data.

```sql
UPDATE pg_catalog.pg_class SET relchecks=1 WHERE oid='mneme_store_pkey'::regclass;
```

```json
{
  "setup_results": [
    {
      "sql": "UPDATE pg_catalog.pg_class SET relchecks=1 WHERE oid='mneme_store_pkey'::regclass",
      "error": {
        "type": "InsufficientPrivilege",
        "code": null,
        "sqlstate": "42501",
        "message": "permission denied for table pg_class"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

**Predicate domain:** altered metadata is unconstructed. Proposed semantic inconsistency controls must later bind a supplied field to comparison; this baseline pass cannot count as a kill.

### E085 — predicate construction boundary pg_index.indcheckxmin

Setup starts with fresh public initialization; no pre-existing store data.

```sql
UPDATE pg_catalog.pg_index SET indcheckxmin=true WHERE indexrelid='mneme_store_pkey'::regclass;
```

```json
{
  "setup_results": [
    {
      "sql": "UPDATE pg_catalog.pg_index SET indcheckxmin=true WHERE indexrelid='mneme_store_pkey'::regclass",
      "error": {
        "type": "InsufficientPrivilege",
        "code": null,
        "sqlstate": "42501",
        "message": "permission denied for table pg_index"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

**Predicate domain:** altered metadata is unconstructed. Proposed semantic inconsistency controls must later bind a supplied field to comparison; this baseline pass cannot count as a kill.

### E086 — full catalog inventory and auxiliary baseline

Setup starts with fresh public initialization; no pre-existing store data.

```sql
-- no variation
```

```json
{
  "setup_results": [],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E087 — extension config dump construction limit

Setup starts with fresh public initialization; no pre-existing store data.

```sql
SELECT pg_extension_config_dump('mneme_store'::regclass,'');
```

```json
{
  "setup_results": [
    {
      "sql": "SELECT pg_extension_config_dump('mneme_store'::regclass,'')",
      "error": {
        "type": "FeatureNotSupported",
        "code": null,
        "sqlstate": "0A000",
        "message": "pg_extension_config_dump() can only be called from an SQL script executed by CREATE EXTENSION"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

### E088 — range over row type construction limit

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE TYPE outside_range AS RANGE (subtype=mneme_store);
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE TYPE outside_range AS RANGE (subtype=mneme_store)",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_proc",
          221405,
          0,
          "pg_type",
          221367,
          0,
          "n",
          "function outside_range(mneme_store,mneme_store)"
        ],
        [
          "pg_proc",
          221406,
          0,
          "pg_type",
          221367,
          0,
          "n",
          "function outside_range(mneme_store,mneme_store,text)"
        ],
        [
          "pg_type",
          221404,
          0,
          "pg_type",
          221367,
          0,
          "n",
          "type outside_range"
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E089 — operator class construction limit

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE OPERATOR CLASS outside_ops FOR TYPE mneme_store USING btree AS OPERATOR 1 <(text,text);
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE OPERATOR CLASS outside_ops FOR TYPE mneme_store USING btree AS OPERATOR 1 <(text,text)",
      "error": {
        "type": "InsufficientPrivilege",
        "code": null,
        "sqlstate": "42501",
        "message": "must be superuser to create an operator class"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

### E090 — sequence type construction limit

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE SEQUENCE outside_seq AS mneme_store;
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE SEQUENCE outside_seq AS mneme_store",
      "error": {
        "type": "InvalidParameterValue",
        "code": null,
        "sqlstate": "22023",
        "message": "sequence type must be smallint, integer, or bigint"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

### E091 — typed foreign table construction limit

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE FOREIGN TABLE outside_t (v mneme_store) SERVER absent;
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE FOREIGN TABLE outside_t (v mneme_store) SERVER absent",
      "error": {
        "type": "UndefinedObject",
        "code": null,
        "sqlstate": "42704",
        "message": "server \"absent\" does not exist"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

### E092 — transform reference construction limit

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE FUNCTION outside_fun(mneme_store) RETURNS text LANGUAGE plpgsql TRANSFORM FOR TYPE mneme_store AS $$ BEGIN RETURN 'x'; END $$;
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE FUNCTION outside_fun(mneme_store) RETURNS text LANGUAGE plpgsql TRANSFORM FOR TYPE mneme_store AS $$ BEGIN RETURN 'x'; END $$",
      "error": {
        "type": "UndefinedObject",
        "code": null,
        "sqlstate": "42704",
        "message": "transform for type mneme_store language \"plpgsql\" does not exist"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

### E093 — stored SQL procedure dependency

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE PROCEDURE outside_proc() LANGUAGE SQL BEGIN ATOMIC SELECT tail FROM mneme_store; END;
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE PROCEDURE outside_proc() LANGUAGE SQL BEGIN ATOMIC SELECT tail FROM mneme_store; END",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_proc",
          221634,
          0,
          "pg_class",
          221598,
          2,
          "n",
          "function outside_proc()"
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E094 — constraint trigger WHEN row-type reference

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE TABLE outside_t(v text);
CREATE FUNCTION noop() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NEW; END$$;
CREATE CONSTRAINT TRIGGER outside_constraint AFTER INSERT ON outside_t FOR EACH ROW WHEN (ROW(NEW.v,0)::mneme_store IS NOT NULL) EXECUTE FUNCTION noop();
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE TABLE outside_t(v text)",
      "result": "OK"
    },
    {
      "sql": "CREATE FUNCTION noop() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NEW; END$$",
      "result": "OK"
    },
    {
      "sql": "CREATE CONSTRAINT TRIGGER outside_constraint AFTER INSERT ON outside_t FOR EACH ROW WHEN (ROW(NEW.v,0)::mneme_store IS NOT NULL) EXECUTE FUNCTION noop()",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_trigger",
          221685,
          0,
          "pg_type",
          221645,
          0,
          "n",
          "trigger outside_constraint on table outside_t"
        ]
      ],
      "removed": []
    },
    "triggers": {
      "added": [
        [
          {
            "oid": "221685",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "221684",
            "tgname": "outside_constraint",
            "tgqual": "{NULLTEST :arg {ROW :args ({VAR :varno 2 :varattno 1 :vartype 25 :vartypmod -1 :varcollid 100 :varlevelsup 0 :varnosyn 2 :varattnosyn 1 :location 94} {FUNCEXPR :funcid 481 :funcresulttype 20 :funcretset false :funcvariadic false :funcformat 2 :funccollid 0 :inputcollid 0 :args ({CONST :consttype 23 :consttypmod -1 :constcollid 0 :constlen 4 :constbyval true :constisnull false :location 100 :constvalue 4 [ 0 0 0 0 0 0 0 0 ]}) :location -1}) :row_typeid 221645 :row_format 1 :colnames <> :location 102} :nulltesttype 1 :argisrow true :location 116}",
            "tgtype": 5,
            "tgnargs": 0,
            "tgrelid": "221679",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "221686",
            "tgdeferrable": false,
            "tgisinternal": false,
            "tgconstrindid": "0",
            "tgconstrrelid": "0",
            "tginitdeferred": false
          }
        ]
      ],
      "removed": []
    },
    "auxiliary": {
      "pg_init_privs": [],
      "pg_seclabel": [],
      "pg_shdepend": [
        [
          {
            "dbid": "221268",
            "objid": "221636",
            "classid": "1259",
            "deptype": "o",
            "objsubid": 0,
            "refobjid": "16901",
            "refclassid": "1260"
          }
        ],
        [
          {
            "dbid": "221268",
            "objid": "221643",
            "classid": "1259",
            "deptype": "o",
            "objsubid": 0,
            "refobjid": "16901",
            "refclassid": "1260"
          }
        ],
        [
          {
            "dbid": "221268",
            "objid": "221652",
            "classid": "1259",
            "deptype": "o",
            "objsubid": 0,
            "refobjid": "16901",
            "refclassid": "1260"
          }
        ],
        [
          {
            "dbid": "221268",
            "objid": "221667",
            "classid": "1259",
            "deptype": "o",
            "objsubid": 0,
            "refobjid": "16901",
            "refclassid": "1260"
          }
        ],
        [
          {
            "dbid": "221268",
            "objid": "221679",
            "classid": "1259",
            "deptype": "o",
            "objsubid": 0,
            "refobjid": "16901",
            "refclassid": "1260"
          }
        ]
      ],
      "pg_subscription_rel": [],
      "pg_extension": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E095 — outside FK to other namespace

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE SCHEMA outside_ns;
CREATE TABLE outside_ns.fk(sid text REFERENCES mneme_store);
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE SCHEMA outside_ns",
      "result": "OK"
    },
    {
      "sql": "CREATE TABLE outside_ns.fk(sid text REFERENCES mneme_store)",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_constraint",
          221738,
          0,
          "pg_class",
          221696,
          1,
          "n",
          "constraint fk_sid_fkey on table outside_ns.fk"
        ]
      ],
      "removed": []
    },
    "triggers": {
      "added": [
        [
          {
            "oid": "221739",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "1654",
            "tgname": "RI_ConstraintTrigger_a_221739",
            "tgqual": null,
            "tgtype": 9,
            "tgnargs": 0,
            "tgrelid": "221696",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "221738",
            "tgdeferrable": false,
            "tgisinternal": true,
            "tgconstrindid": "221703",
            "tgconstrrelid": "221733",
            "tginitdeferred": false
          }
        ],
        [
          {
            "oid": "221740",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "1655",
            "tgname": "RI_ConstraintTrigger_a_221740",
            "tgqual": null,
            "tgtype": 17,
            "tgnargs": 0,
            "tgrelid": "221696",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "221738",
            "tgdeferrable": false,
            "tgisinternal": true,
            "tgconstrindid": "221703",
            "tgconstrrelid": "221733",
            "tginitdeferred": false
          }
        ],
        [
          {
            "oid": "221741",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "1644",
            "tgname": "RI_ConstraintTrigger_c_221741",
            "tgqual": null,
            "tgtype": 5,
            "tgnargs": 0,
            "tgrelid": "221733",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "221738",
            "tgdeferrable": false,
            "tgisinternal": true,
            "tgconstrindid": "221703",
            "tgconstrrelid": "221696",
            "tginitdeferred": false
          }
        ],
        [
          {
            "oid": "221742",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "1645",
            "tgname": "RI_ConstraintTrigger_c_221742",
            "tgqual": null,
            "tgtype": 17,
            "tgnargs": 0,
            "tgrelid": "221733",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "221738",
            "tgdeferrable": false,
            "tgisinternal": true,
            "tgconstrindid": "221703",
            "tgconstrrelid": "221696",
            "tginitdeferred": false
          }
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": "triggers",
  "public": {
    "error": {
      "type": "MnemeValidationError",
      "code": "persistence.schema_incompatible",
      "sqlstate": null,
      "message": "persistence.schema_incompatible: the mneme_ catalog of schema 'xe095' differs from v1 in its triggers"
    }
  }
}
```

### E096 — outside FROM trigger in other namespace

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE SCHEMA outside_ns;
CREATE TABLE outside_ns.t(v text);
CREATE FUNCTION noop() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NEW; END$$;
CREATE CONSTRAINT TRIGGER outside_constraint AFTER INSERT ON outside_ns.t FROM mneme_store FOR EACH ROW EXECUTE FUNCTION noop();
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE SCHEMA outside_ns",
      "error": {
        "type": "DuplicateSchema",
        "code": null,
        "sqlstate": "42P06",
        "message": "schema \"outside_ns\" already exists"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

### E097 — outside FROM trigger in separate namespace

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE SCHEMA outside_ref;
CREATE TABLE outside_ref.t(v text);
CREATE FUNCTION noop() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NEW; END$$;
CREATE CONSTRAINT TRIGGER outside_constraint AFTER INSERT ON outside_ref.t FROM mneme_store FOR EACH ROW EXECUTE FUNCTION noop();
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE SCHEMA outside_ref",
      "result": "OK"
    },
    {
      "sql": "CREATE TABLE outside_ref.t(v text)",
      "result": "OK"
    },
    {
      "sql": "CREATE FUNCTION noop() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NEW; END$$",
      "result": "OK"
    },
    {
      "sql": "CREATE CONSTRAINT TRIGGER outside_constraint AFTER INSERT ON outside_ref.t FROM mneme_store FOR EACH ROW EXECUTE FUNCTION noop()",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_trigger",
          221839,
          0,
          "pg_class",
          221796,
          0,
          "a",
          "trigger outside_constraint on table outside_ref.t"
        ]
      ],
      "removed": []
    },
    "triggers": {
      "added": [
        [
          {
            "oid": "221839",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "221838",
            "tgname": "outside_constraint",
            "tgqual": null,
            "tgtype": 5,
            "tgnargs": 0,
            "tgrelid": "221833",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "221840",
            "tgdeferrable": false,
            "tgisinternal": false,
            "tgconstrindid": "0",
            "tgconstrrelid": "221796",
            "tginitdeferred": false
          }
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E098 — initial privilege catalog construction limit

Setup starts with fresh public initialization; no pre-existing store data.

```sql
UPDATE pg_init_privs SET privtype='e' WHERE false;
```

```json
{
  "setup_results": [
    {
      "sql": "UPDATE pg_init_privs SET privtype='e' WHERE false",
      "error": {
        "type": "InsufficientPrivilege",
        "code": null,
        "sqlstate": "42501",
        "message": "permission denied for table pg_init_privs"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

### E099 — security label catalog construction limit

Setup starts with fresh public initialization; no pre-existing store data.

```sql
UPDATE pg_seclabel SET label='probe' WHERE false;
```

```json
{
  "setup_results": [
    {
      "sql": "UPDATE pg_seclabel SET label='probe' WHERE false",
      "error": {
        "type": "InsufficientPrivilege",
        "code": null,
        "sqlstate": "42501",
        "message": "permission denied for table pg_seclabel"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

### E100 — subscription binding construction limit

Setup starts with fresh public initialization; no pre-existing store data.

```sql
UPDATE pg_subscription_rel SET srsubstate='r' WHERE false;
```

```json
{
  "setup_results": [
    {
      "sql": "UPDATE pg_subscription_rel SET srsubstate='r' WHERE false",
      "error": {
        "type": "InsufficientPrivilege",
        "code": null,
        "sqlstate": "42501",
        "message": "permission denied for table pg_subscription_rel"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

### E101 — transform binding construction limit

Setup starts with fresh public initialization; no pre-existing store data.

```sql
UPDATE pg_transform SET trftype='mneme_store'::regtype WHERE false;
```

```json
{
  "setup_results": [
    {
      "sql": "UPDATE pg_transform SET trftype='mneme_store'::regtype WHERE false",
      "error": {
        "type": "InsufficientPrivilege",
        "code": null,
        "sqlstate": "42501",
        "message": "permission denied for table pg_transform"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

### E102 — depend binding construction limit

Setup starts with fresh public initialization; no pre-existing store data.

```sql
UPDATE pg_depend SET deptype='e' WHERE false;
```

```json
{
  "setup_results": [
    {
      "sql": "UPDATE pg_depend SET deptype='e' WHERE false",
      "error": {
        "type": "InsufficientPrivilege",
        "code": null,
        "sqlstate": "42501",
        "message": "permission denied for table pg_depend"
      }
    }
  ],
  "catalog_changes": {},
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

**Construction limit:** observations above describe the actual residual state only. Intended failed variation was not constructed; no public outcome against it is claimed.

### E103 — outside domain CHECK indirect constraint

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE DOMAIN outside_domain AS mneme_store CHECK ((VALUE).tail >= 0);
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE DOMAIN outside_domain AS mneme_store CHECK ((VALUE).tail >= 0)",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_constraint",
          222109,
          0,
          "pg_class",
          222071,
          2,
          "n",
          "constraint outside_domain_check"
        ],
        [
          "pg_type",
          222108,
          0,
          "pg_type",
          222073,
          0,
          "n",
          "type outside_domain"
        ]
      ],
      "removed": []
    },
    "route_values": {
      "pg_type": {
        "added": [
          [
            {
              "oid": "222107",
              "typacl": null,
              "typlen": -1,
              "typelem": "222108",
              "typname": "_outside_domain",
              "typsend": "array_send",
              "typtype": "b",
              "typalign": "d",
              "typarray": "0",
              "typbyval": false,
              "typdelim": ",",
              "typinput": "array_in",
              "typmodin": "-",
              "typndims": 0,
              "typowner": "16901",
              "typrelid": "0",
              "typmodout": "-",
              "typoutput": "array_out",
              "typtypmod": -1,
              "typanalyze": "array_typanalyze",
              "typdefault": null,
              "typnotnull": false,
              "typreceive": "array_recv",
              "typstorage": "x",
              "typbasetype": "0",
              "typcategory": "A",
              "typcollation": "0",
              "typisdefined": true,
              "typnamespace": "222063",
              "typsubscript": "array_subscript_handler",
              "typdefaultbin": null,
              "typispreferred": false
            }
          ],
          [
            {
              "oid": "222108",
              "typacl": null,
              "typlen": -1,
              "typelem": "0",
              "typname": "outside_domain",
              "typsend": "record_send",
              "typtype": "d",
              "typalign": "d",
              "typarray": "222107",
              "typbyval": false,
              "typdelim": ",",
              "typinput": "domain_in",
              "typmodin": "-",
              "typndims": 0,
              "typowner": "16901",
              "typrelid": "0",
              "typmodout": "-",
              "typoutput": "record_out",
              "typtypmod": -1,
              "typanalyze": "-",
              "typdefault": null,
              "typnotnull": false,
              "typreceive": "domain_recv",
              "typstorage": "x",
              "typbasetype": "222073",
              "typcategory": "C",
              "typcollation": "0",
              "typisdefined": true,
              "typnamespace": "222063",
              "typsubscript": "-",
              "typdefaultbin": null,
              "typispreferred": false
            }
          ]
        ],
        "removed": []
      },
      "pg_constraint": {
        "added": [
          [
            {
              "oid": "222109",
              "conbin": "{OPEXPR :opno 430 :opfuncid 479 :opresulttype 16 :opretset false :opcollid 0 :inputcollid 0 :args ({FIELDSELECT :arg {COERCETODOMAINVALUE :typeId 222073 :typeMod -1 :collation 0 :location 52} :fieldnum 2 :resulttype 20 :resulttypmod -1 :resultcollid 0} {CONST :consttype 23 :consttypmod -1 :constcollid 0 :constlen 4 :constbyval true :constisnull false :location 67 :constvalue 4 [ 0 0 0 0 0 0 0 0 ]}) :location 64}",
              "conkey": null,
              "confkey": null,
              "conname": "outside_domain_check",
              "contype": "c",
              "conindid": "0",
              "conrelid": "0",
              "contypid": "222108",
              "conexclop": null,
              "conffeqop": null,
              "confrelid": "0",
              "conpfeqop": null,
              "conppeqop": null,
              "conislocal": true,
              "condeferred": false,
              "confdeltype": " ",
              "confupdtype": " ",
              "coninhcount": 0,
              "conparentid": "0",
              "connamespace": "222063",
              "connoinherit": false,
              "convalidated": true,
              "condeferrable": false,
              "confmatchtype": " "
            }
          ]
        ],
        "removed": []
      },
      "pg_depend": {
        "added": [
          [
            {
              "objid": "222109",
              "classid": "2606",
              "deptype": "n",
              "objsubid": 0,
              "refobjid": "222071",
              "refclassid": "1259",
              "refobjsubid": 2
            }
          ]
        ],
        "removed": []
      }
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E104 — variadic row-type-array signature

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE FUNCTION outside_variadic(VARIADIC v mneme_store[]) RETURNS integer LANGUAGE SQL AS $$ SELECT 1 $$;
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE FUNCTION outside_variadic(VARIADIC v mneme_store[]) RETURNS integer LANGUAGE SQL AS $$ SELECT 1 $$",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "route_values": {
      "pg_proc": {
        "added": [
          [
            {
              "oid": "222154",
              "proacl": null,
              "probin": null,
              "prosrc": " SELECT 1 ",
              "procost": 100,
              "prokind": "f",
              "prolang": "14",
              "proname": "outside_variadic",
              "prorows": 0,
              "pronargs": 1,
              "proowner": "16901",
              "proconfig": null,
              "proretset": false,
              "prosecdef": false,
              "prorettype": "23",
              "prosqlbody": null,
              "prosupport": "-",
              "proargmodes": [
                "v"
              ],
              "proargnames": [
                "v"
              ],
              "proargtypes": [
                "222119"
              ],
              "proisstrict": false,
              "proparallel": "u",
              "protrftypes": null,
              "provariadic": "222120",
              "provolatile": "v",
              "proleakproof": false,
              "pronamespace": "222110",
              "proallargtypes": [
                "222119"
              ],
              "proargdefaults": null,
              "pronargdefaults": 0
            }
          ]
        ],
        "removed": []
      }
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E105 — all-argument and INOUT row-type signature

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE FUNCTION outside_inout(v text,INOUT x mneme_store) LANGUAGE SQL AS $$ SELECT x $$;
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE FUNCTION outside_inout(v text,INOUT x mneme_store) LANGUAGE SQL AS $$ SELECT x $$",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_proc",
          222199,
          0,
          "pg_type",
          222165,
          0,
          "n",
          "function outside_inout(text,mneme_store)"
        ]
      ],
      "removed": []
    },
    "route_values": {
      "pg_proc": {
        "added": [
          [
            {
              "oid": "222199",
              "proacl": null,
              "probin": null,
              "prosrc": " SELECT x ",
              "procost": 100,
              "prokind": "f",
              "prolang": "14",
              "proname": "outside_inout",
              "prorows": 0,
              "pronargs": 2,
              "proowner": "16901",
              "proconfig": null,
              "proretset": false,
              "prosecdef": false,
              "prorettype": "222165",
              "prosqlbody": null,
              "prosupport": "-",
              "proargmodes": [
                "i",
                "b"
              ],
              "proargnames": [
                "v",
                "x"
              ],
              "proargtypes": [
                "25",
                "222165"
              ],
              "proisstrict": false,
              "proparallel": "u",
              "protrftypes": null,
              "provariadic": "0",
              "provolatile": "v",
              "proleakproof": false,
              "pronamespace": "222155",
              "proallargtypes": [
                "25",
                "222165"
              ],
              "proargdefaults": null,
              "pronargdefaults": 0
            }
          ]
        ],
        "removed": []
      }
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E106 — moving aggregate row-type-state

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE FUNCTION outside_state(mneme_store,mneme_store) RETURNS mneme_store LANGUAGE SQL AS $$ SELECT $1 $$;
CREATE AGGREGATE outside_agg(mneme_store) (SFUNC=outside_state,STYPE=mneme_store,MSFUNC=outside_state,MINVFUNC=outside_state,MSTYPE=mneme_store);
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE FUNCTION outside_state(mneme_store,mneme_store) RETURNS mneme_store LANGUAGE SQL AS $$ SELECT $1 $$",
      "result": "OK"
    },
    {
      "sql": "CREATE AGGREGATE outside_agg(mneme_store) (SFUNC=outside_state,STYPE=mneme_store,MSFUNC=outside_state,MINVFUNC=outside_state,MSTYPE=mneme_store)",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_proc",
          222244,
          0,
          "pg_type",
          222210,
          0,
          "n",
          "function outside_state(mneme_store,mneme_store)"
        ],
        [
          "pg_proc",
          222245,
          0,
          "pg_type",
          222210,
          0,
          "n",
          "function outside_agg(mneme_store)"
        ]
      ],
      "removed": []
    },
    "route_values": {
      "pg_proc": {
        "added": [
          [
            {
              "oid": "222244",
              "proacl": null,
              "probin": null,
              "prosrc": " SELECT $1 ",
              "procost": 100,
              "prokind": "f",
              "prolang": "14",
              "proname": "outside_state",
              "prorows": 0,
              "pronargs": 2,
              "proowner": "16901",
              "proconfig": null,
              "proretset": false,
              "prosecdef": false,
              "prorettype": "222210",
              "prosqlbody": null,
              "prosupport": "-",
              "proargmodes": null,
              "proargnames": null,
              "proargtypes": [
                "222210",
                "222210"
              ],
              "proisstrict": false,
              "proparallel": "u",
              "protrftypes": null,
              "provariadic": "0",
              "provolatile": "v",
              "proleakproof": false,
              "pronamespace": "222200",
              "proallargtypes": null,
              "proargdefaults": null,
              "pronargdefaults": 0
            }
          ],
          [
            {
              "oid": "222245",
              "proacl": null,
              "probin": null,
              "prosrc": "aggregate_dummy",
              "procost": 1,
              "prokind": "a",
              "prolang": "12",
              "proname": "outside_agg",
              "prorows": 0,
              "pronargs": 1,
              "proowner": "16901",
              "proconfig": null,
              "proretset": false,
              "prosecdef": false,
              "prorettype": "222210",
              "prosqlbody": null,
              "prosupport": "-",
              "proargmodes": null,
              "proargnames": null,
              "proargtypes": [
                "222210"
              ],
              "proisstrict": false,
              "proparallel": "u",
              "protrftypes": null,
              "provariadic": "0",
              "provolatile": "i",
              "proleakproof": false,
              "pronamespace": "222200",
              "proallargtypes": null,
              "proargdefaults": null,
              "pronargdefaults": 0
            }
          ]
        ],
        "removed": []
      }
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E107 — expression-index statistics target control

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE INDEX outside_expr ON mneme_store ((tail+1));
ALTER INDEX outside_expr ALTER COLUMN 1 SET STATISTICS 300;
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE INDEX outside_expr ON mneme_store ((tail+1))",
      "result": "OK"
    },
    {
      "sql": "ALTER INDEX outside_expr ALTER COLUMN 1 SET STATISTICS 300",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "class": {
      "outside_expr": {
        "added": {
          "oid": "222290",
          "relam": "403",
          "relacl": null,
          "relkind": "i",
          "relname": "outside_expr",
          "reltype": "0",
          "relnatts": 1,
          "relowner": "16901",
          "relpages": 1,
          "relchecks": 0,
          "reloftype": "0",
          "reltuples": 0,
          "relminmxid": "0",
          "reloptions": null,
          "relrewrite": "0",
          "relfilenode": "222290",
          "relhasindex": false,
          "relhasrules": false,
          "relisshared": false,
          "relfrozenxid": "0",
          "relnamespace": "222246",
          "relpartbound": null,
          "relreplident": "n",
          "relallvisible": 0,
          "reltablespace": "0",
          "reltoastrelid": "0",
          "relhassubclass": false,
          "relhastriggers": false,
          "relispartition": false,
          "relispopulated": true,
          "relpersistence": "p",
          "relrowsecurity": false,
          "relforcerowsecurity": false
        }
      }
    },
    "attribute": {
      "outside_expr.1": {
        "added": {
          "attacl": null,
          "attlen": 8,
          "attnum": 1,
          "attname": "expr",
          "attalign": "d",
          "attbyval": true,
          "attndims": 0,
          "attrelid": "222290",
          "atttypid": "20",
          "atthasdef": false,
          "atttypmod": -1,
          "attislocal": true,
          "attnotnull": false,
          "attoptions": null,
          "attstorage": "p",
          "attcacheoff": -1,
          "attidentity": "",
          "attinhcount": 0,
          "attcollation": "0",
          "attgenerated": "",
          "attisdropped": false,
          "attfdwoptions": null,
          "atthasmissing": false,
          "attstattarget": 300,
          "attcompression": "",
          "attmissingval": null
        }
      }
    },
    "index": {
      "outside_expr": {
        "added": {
          "indkey": [
            0
          ],
          "indpred": null,
          "indclass": [
            "3124"
          ],
          "indexprs": "({OPEXPR :opno 688 :opfuncid 1274 :opresulttype 20 :opretset false :opcollid 0 :inputcollid 0 :args ({VAR :varno 1 :varattno 2 :vartype 20 :vartypmod -1 :varcollid 0 :varlevelsup 0 :varnosyn 1 :varattnosyn 2 :location 43} {CONST :consttype 23 :consttypmod -1 :constcollid 0 :constlen 4 :constbyval true :constisnull false :location 48 :constvalue 4 [ 1 0 0 0 0 0 0 0 ]}) :location 47})",
          "indnatts": 1,
          "indrelid": "222254",
          "indislive": true,
          "indoption": [
            0
          ],
          "indexrelid": "222290",
          "indisready": true,
          "indisvalid": true,
          "indisunique": false,
          "indnkeyatts": 1,
          "indcheckxmin": false,
          "indcollation": [
            "0"
          ],
          "indimmediate": true,
          "indisprimary": false,
          "indisclustered": false,
          "indisexclusion": false,
          "indisreplident": false
        }
      }
    },
    "inbound": {
      "added": [
        [
          "pg_class",
          222290,
          0,
          "pg_class",
          222254,
          0,
          "a",
          "index outside_expr"
        ],
        [
          "pg_class",
          222290,
          0,
          "pg_class",
          222254,
          2,
          "a",
          "index outside_expr"
        ]
      ],
      "removed": []
    },
    "route_values": {
      "pg_depend": {
        "added": [
          [
            {
              "objid": "222290",
              "classid": "1259",
              "deptype": "a",
              "objsubid": 0,
              "refobjid": "222254",
              "refclassid": "1259",
              "refobjsubid": 0
            }
          ],
          [
            {
              "objid": "222290",
              "classid": "1259",
              "deptype": "a",
              "objsubid": 0,
              "refobjid": "222254",
              "refclassid": "1259",
              "refobjsubid": 2
            }
          ]
        ],
        "removed": []
      }
    }
  },
  "fetch_mismatch": "indexes",
  "public": {
    "error": {
      "type": "MnemeValidationError",
      "code": "persistence.schema_incompatible",
      "sqlstate": null,
      "message": "persistence.schema_incompatible: the mneme_ catalog of schema 'xe107' differs from v1 in its indexes"
    }
  }
}
```

### E108 — range subtype actual catalog row

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE TYPE outside_range AS RANGE (subtype=mneme_store);
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE TYPE outside_range AS RANGE (subtype=mneme_store)",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_proc",
          222340,
          0,
          "pg_type",
          222302,
          0,
          "n",
          "function outside_range(mneme_store,mneme_store)"
        ],
        [
          "pg_proc",
          222341,
          0,
          "pg_type",
          222302,
          0,
          "n",
          "function outside_range(mneme_store,mneme_store,text)"
        ],
        [
          "pg_type",
          222339,
          0,
          "pg_type",
          222302,
          0,
          "n",
          "type outside_range"
        ]
      ],
      "removed": []
    },
    "route_values": {
      "pg_proc": {
        "added": [
          [
            {
              "oid": "222340",
              "proacl": null,
              "probin": null,
              "prosrc": "range_constructor2",
              "procost": 1,
              "prokind": "f",
              "prolang": "12",
              "proname": "outside_range",
              "prorows": 0,
              "pronargs": 2,
              "proowner": "10",
              "proconfig": null,
              "proretset": false,
              "prosecdef": false,
              "prorettype": "222339",
              "prosqlbody": null,
              "prosupport": "-",
              "proargmodes": null,
              "proargnames": null,
              "proargtypes": [
                "222302",
                "222302"
              ],
              "proisstrict": false,
              "proparallel": "s",
              "protrftypes": null,
              "provariadic": "0",
              "provolatile": "i",
              "proleakproof": false,
              "pronamespace": "222291",
              "proallargtypes": null,
              "proargdefaults": null,
              "pronargdefaults": 0
            }
          ],
          [
            {
              "oid": "222341",
              "proacl": null,
              "probin": null,
              "prosrc": "range_constructor3",
              "procost": 1,
              "prokind": "f",
              "prolang": "12",
              "proname": "outside_range",
              "prorows": 0,
              "pronargs": 3,
              "proowner": "10",
              "proconfig": null,
              "proretset": false,
              "prosecdef": false,
              "prorettype": "222339",
              "prosqlbody": null,
              "prosupport": "-",
              "proargmodes": null,
              "proargnames": null,
              "proargtypes": [
                "222302",
                "222302",
                "25"
              ],
              "proisstrict": false,
              "proparallel": "s",
              "protrftypes": null,
              "provariadic": "0",
              "provolatile": "i",
              "proleakproof": false,
              "pronamespace": "222291",
              "proallargtypes": null,
              "proargdefaults": null,
              "pronargdefaults": 0
            }
          ],
          [
            {
              "oid": "222342",
              "proacl": null,
              "probin": null,
              "prosrc": "multirange_constructor0",
              "procost": 1,
              "prokind": "f",
              "prolang": "12",
              "proname": "outside_multirange",
              "prorows": 0,
              "pronargs": 0,
              "proowner": "10",
              "proconfig": null,
              "proretset": false,
              "prosecdef": false,
              "prorettype": "222337",
              "prosqlbody": null,
              "prosupport": "-",
              "proargmodes": null,
              "proargnames": null,
              "proargtypes": [],
              "proisstrict": true,
              "proparallel": "s",
              "protrftypes": null,
              "provariadic": "0",
              "provolatile": "i",
              "proleakproof": false,
              "pronamespace": "222291",
              "proallargtypes": null,
              "proargdefaults": null,
              "pronargdefaults": 0
            }
          ],
          [
            {
              "oid": "222343",
              "proacl": null,
              "probin": null,
              "prosrc": "multirange_constructor1",
              "procost": 1,
              "prokind": "f",
              "prolang": "12",
              "proname": "outside_multirange",
              "prorows": 0,
              "pronargs": 1,
              "proowner": "10",
              "proconfig": null,
              "proretset": false,
              "prosecdef": false,
              "prorettype": "222337",
              "prosqlbody": null,
              "prosupport": "-",
              "proargmodes": null,
              "proargnames": null,
              "proargtypes": [
                "222339"
              ],
              "proisstrict": true,
              "proparallel": "s",
              "protrftypes": null,
              "provariadic": "0",
              "provolatile": "i",
              "proleakproof": false,
              "pronamespace": "222291",
              "proallargtypes": null,
              "proargdefaults": null,
              "pronargdefaults": 0
            }
          ],
          [
            {
              "oid": "222344",
              "proacl": null,
              "probin": null,
              "prosrc": "multirange_constructor2",
              "procost": 1,
              "prokind": "f",
              "prolang": "12",
              "proname": "outside_multirange",
              "prorows": 0,
              "pronargs": 1,
              "proowner": "10",
              "proconfig": null,
              "proretset": false,
              "prosecdef": false,
              "prorettype": "222337",
              "prosqlbody": null,
              "prosupport": "-",
              "proargmodes": [
                "v"
              ],
              "proargnames": null,
              "proargtypes": [
                "222336"
              ],
              "proisstrict": true,
              "proparallel": "s",
              "protrftypes": null,
              "provariadic": "222339",
              "provolatile": "i",
              "proleakproof": false,
              "pronamespace": "222291",
              "proallargtypes": [
                "222336"
              ],
              "proargdefaults": null,
              "pronargdefaults": 0
            }
          ]
        ],
        "removed": []
      },
      "pg_range": {
        "added": [
          [
            {
              "rngtypid": "222339",
              "rngsubopc": "10034",
              "rngsubdiff": "-",
              "rngsubtype": "222302",
              "rngcanonical": "-",
              "rngcollation": "0",
              "rngmultitypid": "222337"
            }
          ]
        ],
        "removed": []
      },
      "pg_type": {
        "added": [
          [
            {
              "oid": "222336",
              "typacl": null,
              "typlen": -1,
              "typelem": "222339",
              "typname": "_outside_range",
              "typsend": "array_send",
              "typtype": "b",
              "typalign": "d",
              "typarray": "0",
              "typbyval": false,
              "typdelim": ",",
              "typinput": "array_in",
              "typmodin": "-",
              "typndims": 0,
              "typowner": "16901",
              "typrelid": "0",
              "typmodout": "-",
              "typoutput": "array_out",
              "typtypmod": -1,
              "typanalyze": "array_typanalyze",
              "typdefault": null,
              "typnotnull": false,
              "typreceive": "array_recv",
              "typstorage": "x",
              "typbasetype": "0",
              "typcategory": "A",
              "typcollation": "0",
              "typisdefined": true,
              "typnamespace": "222291",
              "typsubscript": "array_subscript_handler",
              "typdefaultbin": null,
              "typispreferred": false
            }
          ],
          [
            {
              "oid": "222337",
              "typacl": null,
              "typlen": -1,
              "typelem": "0",
              "typname": "outside_multirange",
              "typsend": "multirange_send",
              "typtype": "m",
              "typalign": "d",
              "typarray": "222338",
              "typbyval": false,
              "typdelim": ",",
              "typinput": "multirange_in",
              "typmodin": "-",
              "typndims": 0,
              "typowner": "16901",
              "typrelid": "0",
              "typmodout": "-",
              "typoutput": "multirange_out",
              "typtypmod": -1,
              "typanalyze": "multirange_typanalyze",
              "typdefault": null,
              "typnotnull": false,
              "typreceive": "multirange_recv",
              "typstorage": "x",
              "typbasetype": "0",
              "typcategory": "R",
              "typcollation": "0",
              "typisdefined": true,
              "typnamespace": "222291",
              "typsubscript": "-",
              "typdefaultbin": null,
              "typispreferred": false
            }
          ],
          [
            {
              "oid": "222338",
              "typacl": null,
              "typlen": -1,
              "typelem": "222337",
              "typname": "_outside_multirange",
              "typsend": "array_send",
              "typtype": "b",
              "typalign": "d",
              "typarray": "0",
              "typbyval": false,
              "typdelim": ",",
              "typinput": "array_in",
              "typmodin": "-",
              "typndims": 0,
              "typowner": "16901",
              "typrelid": "0",
              "typmodout": "-",
              "typoutput": "array_out",
              "typtypmod": -1,
              "typanalyze": "array_typanalyze",
              "typdefault": null,
              "typnotnull": false,
              "typreceive": "array_recv",
              "typstorage": "x",
              "typbasetype": "0",
              "typcategory": "A",
              "typcollation": "0",
              "typisdefined": true,
              "typnamespace": "222291",
              "typsubscript": "array_subscript_handler",
              "typdefaultbin": null,
              "typispreferred": false
            }
          ],
          [
            {
              "oid": "222339",
              "typacl": null,
              "typlen": -1,
              "typelem": "0",
              "typname": "outside_range",
              "typsend": "range_send",
              "typtype": "r",
              "typalign": "d",
              "typarray": "222336",
              "typbyval": false,
              "typdelim": ",",
              "typinput": "range_in",
              "typmodin": "-",
              "typndims": 0,
              "typowner": "16901",
              "typrelid": "0",
              "typmodout": "-",
              "typoutput": "range_out",
              "typtypmod": -1,
              "typanalyze": "range_typanalyze",
              "typdefault": null,
              "typnotnull": false,
              "typreceive": "range_recv",
              "typstorage": "x",
              "typbasetype": "0",
              "typcategory": "R",
              "typcollation": "0",
              "typisdefined": true,
              "typnamespace": "222291",
              "typsubscript": "-",
              "typdefaultbin": null,
              "typispreferred": false
            }
          ]
        ],
        "removed": []
      }
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E109 — extension membership actual outgoing edge

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE EXTENSION hstore;
ALTER EXTENSION hstore ADD TABLE mneme_store;
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE EXTENSION hstore",
      "result": "OK"
    },
    {
      "sql": "ALTER EXTENSION hstore ADD TABLE mneme_store",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "route_values": {
      "pg_extension": {
        "added": [
          [
            {
              "oid": "222390",
              "extname": "hstore",
              "extowner": "16901",
              "extconfig": null,
              "extversion": "1.8",
              "extcondition": null,
              "extnamespace": "222346",
              "extrelocatable": true
            }
          ]
        ],
        "removed": []
      },
      "pg_depend": {
        "added": [
          [
            {
              "objid": "222354",
              "classid": "1259",
              "deptype": "e",
              "objsubid": 0,
              "refobjid": "222390",
              "refclassid": "3079",
              "refobjsubid": 0
            }
          ]
        ],
        "removed": []
      }
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E110 — missing cache with exempt planner statistics

Setup starts with fresh public initialization; create_store("old") before closing the handle.

```sql
ALTER TABLE mneme_store ALTER COLUMN store_id SET STATISTICS 200;
ALTER TABLE mneme_store DROP COLUMN tail;
ALTER TABLE mneme_store ADD COLUMN tail bigint NOT NULL DEFAULT 1 CHECK(tail BETWEEN 0 AND 9007199254740991);
ALTER TABLE mneme_store ALTER COLUMN tail SET DEFAULT 0;
```

```json
{
  "setup_results": [
    {
      "sql": "ALTER TABLE mneme_store ALTER COLUMN store_id SET STATISTICS 200",
      "result": "OK"
    },
    {
      "sql": "ALTER TABLE mneme_store DROP COLUMN tail",
      "result": "OK"
    },
    {
      "sql": "ALTER TABLE mneme_store ADD COLUMN tail bigint NOT NULL DEFAULT 1 CHECK(tail BETWEEN 0 AND 9007199254740991)",
      "result": "OK"
    },
    {
      "sql": "ALTER TABLE mneme_store ALTER COLUMN tail SET DEFAULT 0",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "class": {
      "mneme_store": {
        "relnatts": [
          2,
          3
        ]
      }
    },
    "attribute": {
      "mneme_store.1": {
        "attstattarget": [
          -1,
          200
        ]
      },
      "mneme_store.2": {
        "attname": [
          "tail",
          "........pg.dropped.2........"
        ],
        "atttypid": [
          "20",
          "0"
        ],
        "attisdropped": [
          false,
          true
        ],
        "attstattarget": [
          -1,
          0
        ],
        "atthasdef": [
          true,
          false
        ],
        "attnotnull": [
          true,
          false
        ]
      },
      "mneme_store.3": {
        "added": {
          "attacl": null,
          "attlen": 8,
          "attnum": 3,
          "attname": "tail",
          "attalign": "d",
          "attbyval": true,
          "attndims": 0,
          "attrelid": "222527",
          "atttypid": "20",
          "atthasdef": true,
          "atttypmod": -1,
          "attislocal": true,
          "attnotnull": true,
          "attoptions": null,
          "attstorage": "p",
          "attcacheoff": -1,
          "attidentity": "",
          "attinhcount": 0,
          "attcollation": "0",
          "attgenerated": "",
          "attisdropped": false,
          "attfdwoptions": null,
          "atthasmissing": true,
          "attstattarget": -1,
          "attcompression": "",
          "attmissingval": "{1}"
        }
      }
    },
    "inbound": {
      "added": [
        [
          "pg_attrdef",
          222565,
          0,
          "pg_class",
          222527,
          3,
          "a",
          "default value for column tail of table mneme_store"
        ],
        [
          "pg_constraint",
          222564,
          0,
          "pg_class",
          222527,
          3,
          "a",
          "constraint mneme_store_tail_check on table mneme_store"
        ],
        [
          "pg_constraint",
          222564,
          0,
          "pg_class",
          222527,
          3,
          "n",
          "constraint mneme_store_tail_check on table mneme_store"
        ]
      ],
      "removed": [
        [
          "pg_attrdef",
          222530,
          0,
          "pg_class",
          222527,
          2,
          "a",
          "default value for column tail of table mneme_store"
        ],
        [
          "pg_constraint",
          222531,
          0,
          "pg_class",
          222527,
          2,
          "a",
          "constraint mneme_store_tail_check on table mneme_store"
        ],
        [
          "pg_constraint",
          222531,
          0,
          "pg_class",
          222527,
          2,
          "n",
          "constraint mneme_store_tail_check on table mneme_store"
        ]
      ]
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "old_tail": {
      "store_id": "old",
      "position": 1
    },
    "first": 2,
    "last": 3,
    "retry_equal": true,
    "positions": [
      2,
      3
    ],
    "tail": 3,
    "through": 3
  }
}
```

### E111 — outside FROM link with exempt grants

Setup starts with fresh public initialization; no pre-existing store data.

```sql
GRANT SELECT(tail) ON mneme_store TO PUBLIC;
CREATE TABLE outside_t(v text);
CREATE FUNCTION noop() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NEW; END$$;
CREATE CONSTRAINT TRIGGER outside_constraint AFTER INSERT ON outside_t FROM mneme_store FOR EACH ROW EXECUTE FUNCTION noop();
```

```json
{
  "setup_results": [
    {
      "sql": "GRANT SELECT(tail) ON mneme_store TO PUBLIC",
      "result": "OK"
    },
    {
      "sql": "CREATE TABLE outside_t(v text)",
      "result": "OK"
    },
    {
      "sql": "CREATE FUNCTION noop() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NEW; END$$",
      "result": "OK"
    },
    {
      "sql": "CREATE CONSTRAINT TRIGGER outside_constraint AFTER INSERT ON outside_t FROM mneme_store FOR EACH ROW EXECUTE FUNCTION noop()",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "attribute": {
      "mneme_store.2": {
        "attacl": [
          null,
          [
            "=r/mneme_dev"
          ]
        ]
      }
    },
    "inbound": {
      "added": [
        [
          "pg_trigger",
          222616,
          0,
          "pg_class",
          222574,
          0,
          "a",
          "trigger outside_constraint on table outside_t"
        ]
      ],
      "removed": []
    },
    "triggers": {
      "added": [
        [
          {
            "oid": "222616",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "222615",
            "tgname": "outside_constraint",
            "tgqual": null,
            "tgtype": 5,
            "tgnargs": 0,
            "tgrelid": "222610",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "222617",
            "tgdeferrable": false,
            "tgisinternal": false,
            "tgconstrindid": "0",
            "tgconstrrelid": "222574",
            "tginitdeferred": false
          }
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```

### E112 — outside same-name relation FROM link

Setup starts with fresh public initialization; no pre-existing store data.

```sql
CREATE SCHEMA elsewhere;
CREATE TABLE elsewhere.mneme_store(v text);
CREATE FUNCTION noop() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NEW; END$$;
CREATE CONSTRAINT TRIGGER outside_constraint AFTER INSERT ON elsewhere.mneme_store FROM mneme_store FOR EACH ROW EXECUTE FUNCTION noop();
```

```json
{
  "setup_results": [
    {
      "sql": "CREATE SCHEMA elsewhere",
      "result": "OK"
    },
    {
      "sql": "CREATE TABLE elsewhere.mneme_store(v text)",
      "result": "OK"
    },
    {
      "sql": "CREATE FUNCTION noop() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NEW; END$$",
      "result": "OK"
    },
    {
      "sql": "CREATE CONSTRAINT TRIGGER outside_constraint AFTER INSERT ON elsewhere.mneme_store FROM mneme_store FOR EACH ROW EXECUTE FUNCTION noop()",
      "result": "OK"
    }
  ],
  "catalog_changes": {
    "inbound": {
      "added": [
        [
          "pg_trigger",
          222669,
          0,
          "pg_class",
          222626,
          0,
          "a",
          "trigger outside_constraint on table elsewhere.mneme_store"
        ]
      ],
      "removed": []
    },
    "triggers": {
      "added": [
        [
          {
            "oid": "222669",
            "tgargs": "\\x",
            "tgattr": [],
            "tgfoid": "222668",
            "tgname": "outside_constraint",
            "tgqual": null,
            "tgtype": 5,
            "tgnargs": 0,
            "tgrelid": "222663",
            "tgenabled": "O",
            "tgnewtable": null,
            "tgoldtable": null,
            "tgparentid": "0",
            "tgconstraint": "222670",
            "tgdeferrable": false,
            "tgisinternal": false,
            "tgconstrindid": "0",
            "tgconstrrelid": "222626",
            "tginitdeferred": false
          }
        ]
      ],
      "removed": []
    }
  },
  "fetch_mismatch": null,
  "public": {
    "open": "ACCEPT",
    "first": 1,
    "last": 2,
    "retry_equal": true,
    "positions": [
      1,
      2
    ],
    "tail": 2,
    "through": 2
  }
}
```


## Executed observer definitions and reproduction

The following drivers contain no production replacement. They import the exact frozen checkout; only private databases/schemas are varied. Supply the project-managed interpreter, source project-environment.ps1 first, and run each serially. There are no credentials in these listings. Raw scratch files are hashed below; the committed matrix records the actual results even when a recipe's starting label proved wrong (E088) or its setup needed correction (E096/E097). `to_jsonb` catalog values are observations, not normative structured-compare choices. The observer queries run on a separate connection and need not obey the production fetch's qualification policy; the candidate's own fetch remains unchanged.

### probe.py

```python
import sys,json,uuid,re,dataclasses,hashlib
from pathlib import Path
import psycopg
from psycopg import sql
ROOT=Path('E:/AI/Projects/OpenMinds/Minions/Minion-Memory')
OUT=ROOT/'.tmp/work/codex/ce04-extension'
PKG=ROOT/'review-worktrees/code-wp04-ce1-closure/minion-memory-python'
sys.path.insert(0,str(PKG/'src'));sys.path.insert(0,str(PKG/'tests'))
import pgdb
from minion_memory.persistence import PostgresHistoryStore as Store
from minion_memory.persistence import catalog
from minion_memory.persistence._v1_catalog import V1_CATALOG
T='2026-10-11T08:00:00.000000Z'
W={'profile':'learning','recognized':[{'record_type':'attempt','schema_version':1}]}
O={'source_namespace':'app','source_operation_id':'one'}
def draft(i):return {'record_id':i,'profile':'learning','record_type':'attempt','schema_version':1,'compatibility':'required'}
def err(e):return {'type':type(e).__name__,'code':getattr(e,'code',None),'sqlstate':getattr(e,'sqlstate',None),'message':str(e)[:800]}
def cx(p):return psycopg.connect(autocommit=True,**p)
def snapshot(c):
    return {
      'class':c.execute("SELECT to_jsonb(c) FROM pg_catalog.pg_class c WHERE c.relnamespace=current_schema()::regnamespace AND (c.relname LIKE 'mneme_%' OR c.oid IN (SELECT indexrelid FROM pg_index WHERE indrelid IN (SELECT oid FROM pg_class WHERE relnamespace=current_schema()::regnamespace AND relname LIKE 'mneme_%'))) ORDER BY c.relname").fetchall(),
      'attribute':c.execute("SELECT c.relname,to_jsonb(a) - 'attmissingval',a.attmissingval::text FROM pg_attribute a JOIN pg_class c ON c.oid=a.attrelid WHERE c.relnamespace=current_schema()::regnamespace AND (c.relname LIKE 'mneme_%' OR c.oid IN (SELECT indexrelid FROM pg_index WHERE indrelid IN (SELECT oid FROM pg_class WHERE relnamespace=current_schema()::regnamespace AND relname LIKE 'mneme_%'))) ORDER BY c.relname,a.attnum").fetchall(),
      'index':c.execute("SELECT c.relname,to_jsonb(i) FROM pg_index i JOIN pg_class c ON c.oid=i.indexrelid WHERE i.indrelid IN (SELECT oid FROM pg_class WHERE relnamespace=current_schema()::regnamespace AND relname LIKE 'mneme_%') ORDER BY c.relname").fetchall(),
      'inbound':c.execute("WITH target AS (SELECT oid,reltype FROM pg_class WHERE relnamespace=current_schema()::regnamespace AND relname IN ('mneme_schema','mneme_store','mneme_record','mneme_operation')) SELECT d.classid::regclass::text,d.objid,d.objsubid,d.refclassid::regclass::text,d.refobjid,d.refobjsubid,d.deptype,pg_describe_object(d.classid,d.objid,d.objsubid) FROM pg_depend d WHERE (d.refclassid='pg_class'::regclass AND d.refobjid IN (SELECT oid FROM target)) OR (d.refclassid='pg_type'::regclass AND d.refobjid IN (SELECT reltype FROM target)) ORDER BY 1,2,3,4,5,6").fetchall(),
      'triggers':c.execute("SELECT to_jsonb(g) FROM pg_trigger g WHERE g.tgrelid IN (SELECT oid FROM pg_class WHERE relnamespace=current_schema()::regnamespace) OR g.tgconstrrelid IN (SELECT oid FROM pg_class WHERE relnamespace=current_schema()::regnamespace) ORDER BY g.tgrelid,g.tgname").fetchall(),
      'publication':c.execute("SELECT p.pubname,to_jsonb(p),to_jsonb(r) FROM pg_publication p LEFT JOIN pg_publication_rel r ON r.prpubid=p.oid WHERE r.prrelid IN (SELECT oid FROM pg_class WHERE relnamespace=current_schema()::regnamespace) OR p.puballtables").fetchall(),
      'annotations':c.execute("SELECT d.objoid,d.objsubid,d.description FROM pg_description d WHERE d.classoid='pg_class'::regclass AND d.objoid IN (SELECT oid FROM pg_class WHERE relnamespace=current_schema()::regnamespace)").fetchall(),
    }
def public(p,mode='N'):
    r={}
    try:
      with Store.open(p,lambda _:T) as s:
        r['open']='ACCEPT'
        if mode=='cache':
          r['old_tail']=s.store_tail('old');sid='old'
        else:sid='s';s.create_store(sid)
        receipt=s.commit_history(sid,W,O,[draft('r1'),draft('r2')]);retry=s.commit_history(sid,W,O,[draft('r1'),draft('r2')])
        page=s.read_history(sid,{'store_id':sid,'position':0},10)
        r.update(receipt=receipt,retry_equal=retry==receipt,page=page,tail=s.store_tail(sid))
    except Exception as e:r['error']=err(e)
    return r
CASES=[]
def add(id,dimension,setup,mode='N',before=None):CASES.append(dict(id=id,dimension=dimension,setup=setup,mode=mode,before=before))
add('E001','baseline',[])
add('E002','cached tail 1', ['ALTER TABLE mneme_store DROP COLUMN tail','ALTER TABLE mneme_store ADD COLUMN tail bigint NOT NULL DEFAULT 1 CHECK(tail BETWEEN 0 AND 9007199254740991)','ALTER TABLE mneme_store ALTER COLUMN tail SET DEFAULT 0'],'cache','old')
add('E003','cached tail 0', ['ALTER TABLE mneme_store DROP COLUMN tail','ALTER TABLE mneme_store ADD COLUMN tail bigint NOT NULL DEFAULT 0 CHECK(tail BETWEEN 0 AND 9007199254740991)'],'cache','old')
add('E004','cached tail cleared by rewrite',CASES[1]['setup']+['VACUUM FULL mneme_store'],'cache','old')
add('E005','cached schema version 2', ['ALTER TABLE mneme_schema DROP COLUMN version','ALTER TABLE mneme_schema ADD COLUMN version integer NOT NULL DEFAULT 2','ALTER TABLE mneme_schema ALTER COLUMN version DROP DEFAULT'])
add('E006','cached schema version 1', ['ALTER TABLE mneme_schema DROP COLUMN version','ALTER TABLE mneme_schema ADD COLUMN version integer NOT NULL DEFAULT 1','ALTER TABLE mneme_schema ALTER COLUMN version DROP DEFAULT'])
add('E007','table stats target/options', ['ALTER TABLE mneme_store ALTER COLUMN tail SET STATISTICS 300','ALTER TABLE mneme_store ALTER COLUMN tail SET (n_distinct=0.5,n_distinct_inherited=-0.7)','ANALYZE mneme_store'])
add('E008','index column stats target', ['ALTER INDEX mneme_store_pkey ALTER COLUMN 1 SET STATISTICS 300'])
add('E009','index column options attempt', ['ALTER INDEX mneme_store_pkey ALTER COLUMN 1 SET (n_distinct=0.5)'])
add('E010','foreign column options on heap attempt', ["ALTER TABLE mneme_store ALTER COLUMN tail OPTIONS (ADD anything 'x')"])
add('E011','planner stats/freeze progress', ['VACUUM (FREEZE,ANALYZE) mneme_schema','VACUUM (FREEZE,ANALYZE) mneme_store','VACUUM (FREEZE,ANALYZE) mneme_record','VACUUM (FREEZE,ANALYZE) mneme_operation'])
add('E012','physical file identity', ['REINDEX TABLE mneme_store','VACUUM FULL mneme_schema'])
add('E013','dropped-column residue', ['ALTER TABLE mneme_store ADD COLUMN gone text','ALTER TABLE mneme_store DROP COLUMN gone'])
add('E014','lazy trigger flag', ["CREATE FUNCTION noop() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NEW; END$$",'CREATE TRIGGER transient AFTER INSERT ON mneme_schema FOR EACH ROW EXECUTE FUNCTION noop()','DROP TRIGGER transient ON mneme_schema'])
add('E015','lazy rule flag', ['CREATE RULE transient AS ON INSERT TO mneme_schema DO ALSO NOTIFY probe','DROP RULE transient ON mneme_schema'])
add('E016','lazy inheritance flag', ['CREATE TABLE outside_child () INHERITS(mneme_store)','DROP TABLE outside_child'])
add('E017','column/table grants', ['GRANT SELECT(tail) ON mneme_store TO PUBLIC','GRANT SELECT ON mneme_record TO PUBLIC'])
add('E018','comments on table column index', ["COMMENT ON TABLE mneme_store IS 'review'","COMMENT ON COLUMN mneme_store.tail IS 'review'","COMMENT ON INDEX mneme_store_pkey IS 'review'"])
add('E019','security label provider absent', ["SECURITY LABEL FOR ce04_missing ON TABLE mneme_store IS 'x'"])
add('E020','extended stats exception', ['CREATE STATISTICS outside_stat (dependencies) ON store_id,tail FROM mneme_store'])
add('E021','unprefixed view dependency', ['CREATE VIEW outside_view AS SELECT * FROM mneme_store'])
add('E022','materialized view dependency', ['CREATE MATERIALIZED VIEW outside_mat AS SELECT * FROM mneme_store'])
add('E023','outside rewrite rule', ['CREATE TABLE outside_log(sid text)','CREATE RULE outside_rule AS ON INSERT TO outside_log DO ALSO INSERT INTO mneme_store(store_id) VALUES(NEW.sid)'])
add('E024','sequence ownership dependency', ['CREATE SEQUENCE outside_seq OWNED BY mneme_store.tail'])
add('E025','publication relation membership', ['CREATE PUBLICATION ce04_pub FOR TABLE mneme_store'])
add('E026','all tables publication attempt', ['CREATE PUBLICATION ce04_pub FOR ALL TABLES'])
add('E027','outside FK', ['CREATE TABLE outside_fk(sid text REFERENCES mneme_store)'])
add('E028','outside constraint trigger ref', ['CREATE TABLE outside_t(sid text)',"CREATE FUNCTION noop() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NEW; END$$",'CREATE CONSTRAINT TRIGGER outside_constraint AFTER INSERT ON outside_t FROM mneme_store DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION noop()'])
add('E029','inheritance route control', ['CREATE TABLE outside_child () INHERITS(mneme_store)'])
add('E030','row type dependency column', ['CREATE TABLE outside_row(v mneme_store)'])
add('E031','row type dependency function', ['CREATE FUNCTION outside_fun(mneme_store) RETURNS bigint LANGUAGE SQL AS $$ SELECT $1.tail $$'])
add('E032','SQL standard body dependency', ['CREATE FUNCTION outside_fun() RETURNS bigint LANGUAGE SQL BEGIN ATOMIC SELECT tail FROM mneme_store LIMIT 1; END'])
add('E033','SQL string body nondependency', ['CREATE FUNCTION outside_fun() RETURNS bigint LANGUAGE SQL AS $$ SELECT tail FROM mneme_store LIMIT 1 $$'])
add('E034','outside default to row type', ['CREATE TABLE outside_default(v mneme_store DEFAULT ROW(\'x\',0)::mneme_store)'])
add('E035','outside CHECK row type', ['CREATE TABLE outside_check(v text CHECK(ROW(v,0)::mneme_store IS NOT NULL))'])
add('E036','outside generated row type', ['CREATE TABLE outside_gen(v text,r mneme_store GENERATED ALWAYS AS (ROW(v,0)::mneme_store) STORED)'])
add('E037','outside expression index row type', ['CREATE TABLE outside_expr(v text)','CREATE INDEX outside_idx ON outside_expr (((ROW(v,0)::mneme_store).tail))'])
add('E038','outside policy row type', ['CREATE TABLE outside_policy(v text)','CREATE POLICY p ON outside_policy USING (ROW(v,0)::mneme_store IS NOT NULL)'])
add('E039','outside domain row type', ['CREATE DOMAIN outside_domain AS mneme_store'])
add('E040','outside view via row type array', ['CREATE VIEW outside_arr AS SELECT ARRAY[ROW(\'x\',0)::mneme_store] AS v'])
add('E041','core-owned constraint trigger control', ["CREATE FUNCTION noop() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NEW; END$$",'CREATE CONSTRAINT TRIGGER direct_constraint AFTER INSERT ON mneme_store FOR EACH ROW EXECUTE FUNCTION noop()'])
add('E042','outside nonconstraint trigger function binds core', ['CREATE TABLE outside_t(sid text)',"CREATE FUNCTION outside_effect() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN INSERT INTO mneme_store(store_id) VALUES(NEW.sid); RETURN NEW; END$$",'CREATE TRIGGER outside_trigger AFTER INSERT ON outside_t FOR EACH ROW EXECUTE FUNCTION outside_effect()'])
add('E043','outside FK not valid', ['CREATE TABLE outside_fk(sid text)','ALTER TABLE outside_fk ADD CONSTRAINT f FOREIGN KEY(sid) REFERENCES mneme_store NOT VALID'])
add('E044','outside typed table', ['CREATE TABLE outside_t OF mneme_store'])
add('E045','outside partition attach attempt', ['CREATE TABLE outside_parent (LIKE mneme_store INCLUDING ALL) PARTITION BY LIST(store_id)',"ALTER TABLE outside_parent ATTACH PARTITION mneme_store DEFAULT"])
add('E046','renamed index identity', ['ALTER INDEX mneme_store_pkey RENAME TO outside_name'])
add('E047','extra index control', ['CREATE INDEX outside_index ON mneme_store(tail)'])
add('E048','catalog edit privilege boundary', ['UPDATE pg_catalog.pg_attribute SET attcacheoff=0 WHERE attrelid=\'mneme_store\'::regclass AND attname=\'tail\''])

def run():
  values=pgdb.settings();admin=pgdb._params(values,values.get('PGDATABASE','postgres'));dbname='mneme_codex_ce04ext_'+uuid.uuid4().hex[:12];made=False;rows=[]
  try:
    with cx(admin) as c:c.execute(sql.SQL("CREATE DATABASE {} TEMPLATE template0 ENCODING 'UTF8' LC_COLLATE 'C' LC_CTYPE 'C' TABLESPACE mneme_ts").format(sql.Identifier(dbname)));made=True
    base=pgdb._params(values,dbname)
    with cx(base) as c:
      inv={name:c.execute("SELECT attname,format_type(atttypid,atttypmod) FROM pg_attribute WHERE attrelid=%s::regclass AND attnum>0 AND NOT attisdropped ORDER BY attnum",('pg_catalog.'+name,)).fetchall() for name in ('pg_attribute','pg_class','pg_index')}
      (OUT/'inventory.json').write_text(json.dumps(inv,indent=2),encoding='utf8')
      (OUT/'engine.json').write_text(json.dumps(c.execute("SELECT version(),current_user,rolsuper,rolcreatedb FROM pg_roles WHERE rolname=current_user").fetchone()),encoding='utf8')
    for case in CASES:
      row=case.copy();ns='x'+case['id'].lower();p=base|{'options':'-c search_path='+ns+' -c statement_timeout=60000 -c lock_timeout=2000'}
      with cx(base) as c:c.execute(sql.SQL('CREATE SCHEMA {}').format(sql.Identifier(ns)))
      try:
        with Store.open(p,lambda _:T) as s:
          if case['before']:s.create_store(case['before'])
        with cx(p) as c:
          row['baseline']=snapshot(c);row['setup_results']=[]
          for statement in case['setup']:
            try:c.execute(statement);row['setup_results'].append({'sql':statement,'result':'OK'})
            except Exception as e:row['setup_results'].append({'sql':statement,'error':err(e)});break
          row['observed']=snapshot(c)
          nsid=c.execute(catalog.NAMESPACE_SQL).fetchone()[0];found=catalog.fetch(c,nsid)
          row['mismatch']=catalog.mismatch(found,V1_CATALOG)
        row['public']=public(p,case['mode'])
      except Exception as e:row['probe_error']=err(e)
      finally:
        with cx(base) as c:
          if case['id'] in ('E025','E026'):c.execute('DROP PUBLICATION IF EXISTS ce04_pub')
          c.execute(sql.SQL('DROP SCHEMA {} CASCADE').format(sql.Identifier(ns)))
        rows.append(row);(OUT/'rows.json').write_text(json.dumps(rows,default=str,indent=2),encoding='utf8')
        print(json.dumps({k:row.get(k) for k in ('id','dimension','setup_results','mismatch','public','probe_error')},default=str),flush=True)
  finally:
    if made:
      with cx(admin) as c:c.execute(sql.SQL('DROP DATABASE {}').format(sql.Identifier(dbname)))
      (OUT/'cleanup.json').write_text(json.dumps({'database':dbname,'dropped':True}),encoding='utf8')
if __name__=='__main__':run()

```

### more.py

```python
import probe as p
import json
p.CASES=[]
old_snapshot=p.snapshot
def snapshot(c):
 r=old_snapshot(c)
 r['catalog_routes']=c.execute("SELECT fktable::text,fkcols,pktable::text,pkcols,is_array,is_opt FROM pg_get_catalog_foreign_keys() WHERE pktable IN ('pg_class'::regclass,'pg_type'::regclass,'pg_attribute'::regclass) ORDER BY 1,2").fetchall()
 r['depend_closure']=c.execute("WITH RECURSIVE roots AS (SELECT 'pg_class'::regclass::oid AS cls,oid AS obj FROM pg_class WHERE relnamespace=current_schema()::regnamespace AND relname IN ('mneme_schema','mneme_store','mneme_record','mneme_operation')), closure(cls,obj) AS (SELECT cls,obj FROM roots UNION SELECT d.classid,d.objid FROM pg_depend d JOIN closure r ON d.refclassid=r.cls AND d.refobjid=r.obj) SELECT cls::regclass::text,obj,pg_describe_object(cls,obj,0) FROM closure ORDER BY 1,2").fetchall()
 r['types']=c.execute("SELECT to_jsonb(t) FROM pg_type t WHERE t.typrelid IN (SELECT oid FROM pg_class WHERE relnamespace=current_schema()::regnamespace) ORDER BY t.typname").fetchall()
 return r
p.snapshot=snapshot
p.add('E049','baseline catalog routes and dependency closure',[])
for n,t in enumerate(('mneme_schema','mneme_record','mneme_operation'),50):
 p.add('E%03d'%n,'outside FROM constraint on '+t,['CREATE TABLE outside_t(sid text)',"CREATE FUNCTION noop() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NEW; END$$",'CREATE CONSTRAINT TRIGGER outside_constraint AFTER INSERT ON outside_t FROM '+t+' FOR EACH ROW EXECUTE FUNCTION noop()'])
p.add('E053','outside FK schema target',['CREATE TABLE outside_fk(v boolean REFERENCES mneme_schema(singleton))'])
p.add('E054','outside FK record target',['CREATE TABLE outside_fk(s text,p bigint,FOREIGN KEY(s,p) REFERENCES mneme_record(store_id,position))'])
p.add('E055','outside FK operation target',['CREATE TABLE outside_fk(s text,n text,i bytea,FOREIGN KEY(s,n,i) REFERENCES mneme_operation(store_id,source_namespace,source_operation_id))'])
p.add('E056','unrelated outside object positive',['CREATE TABLE outside_unrelated(v text)'])
p.add('E057','transitive array and domain dependency',['CREATE DOMAIN outside_domain AS mneme_store','CREATE TABLE outside_arr(v outside_domain[])'])
p.add('E058','function result dependency',['CREATE FUNCTION outside_fun() RETURNS mneme_store LANGUAGE SQL AS $$ SELECT ROW(\'x\',0)::mneme_store $$'])
p.add('E059','aggregate type dependency',['CREATE FUNCTION outside_state(mneme_store,mneme_store) RETURNS mneme_store LANGUAGE SQL AS $$ SELECT $1 $$','CREATE AGGREGATE outside_agg(mneme_store) (SFUNC=outside_state,STYPE=mneme_store)'])
p.add('E060','operator type dependency',['CREATE FUNCTION outside_eq(mneme_store,mneme_store) RETURNS boolean LANGUAGE SQL IMMUTABLE AS $$ SELECT $1.store_id=$2.store_id $$','CREATE OPERATOR === (LEFTARG=mneme_store,RIGHTARG=mneme_store,FUNCTION=outside_eq)'])
p.add('E061','cast type dependency',['CREATE FUNCTION outside_cast(mneme_store) RETURNS text LANGUAGE SQL AS $$ SELECT $1.store_id $$','CREATE CAST(mneme_store AS text) WITH FUNCTION outside_cast(mneme_store)'])
p.add('E062','extension binding attempt',['CREATE EXTENSION hstore','ALTER EXTENSION hstore ADD TABLE mneme_store'])
p.add('E063','event trigger privilege boundary',["CREATE FUNCTION outside_event() RETURNS event_trigger LANGUAGE plpgsql AS $$ BEGIN NULL; END $$",'CREATE EVENT TRIGGER ce04_event ON ddl_command_end EXECUTE FUNCTION outside_event()'])
p.add('E064','subscription privilege boundary',["CREATE SUBSCRIPTION ce04_sub CONNECTION 'host=127.0.0.1 dbname=not_used' PUBLICATION not_used WITH(connect=false,create_slot=false,enabled=false)"])
p.add('E065','foreign table metadata inconsistency attempt',["UPDATE pg_foreign_table SET ftserver=0 WHERE ftrelid='mneme_store'::regclass"])
# Actual ordinary-role attempts for predicate-domain properties: rejection leaves baseline state.
fields={
 'pg_attribute':{'attlen':'0','attcacheoff':'0','attbyval':'false','attalign':"'d'",'attfdwoptions':"ARRAY['x=y']",'attmissingval':"NULL"},
 'pg_class':{'relisshared':'true','relispopulated':'false','relrewrite':'1','relpartbound':"NULL",'relkind':"'I'",'relpersistence':"'u'",'relispartition':'true','reloftype':'1','relrowsecurity':'true','relforcerowsecurity':'true','relreplident':"'f'",'relnatts':'1','relchecks':'1'},
 'pg_index':{'indcheckxmin':'true'},
}
n=66
for cat,fs in fields.items():
 for field,value in fs.items():
  where={'pg_attribute':"attrelid='mneme_store_pkey'::regclass AND attnum=1",'pg_class':"oid='mneme_store_pkey'::regclass",'pg_index':"indexrelid='mneme_store_pkey'::regclass"}[cat]
  p.add('E%03d'%n,'predicate construction boundary '+cat+'.'+field,['UPDATE pg_catalog.'+cat+' SET '+field+'='+value+' WHERE '+where]);n+=1
p.run()
# Rename the second independent database's evidence; preserve first run.
for name in ('rows','cleanup','engine','inventory'):
 (p.OUT/(name+'2.json')).write_bytes((p.OUT/(name+'.json')).read_bytes())

```

### final_probes.py

```python
import probe as p
from psycopg import sql
p.CASES=[]
old=p.snapshot
def snap(c):
 r=old(c)
 r['auxiliary']={}
 for name,where in {
  'pg_init_privs':"classoid='pg_class'::regclass AND objoid IN (SELECT oid FROM pg_class WHERE relnamespace=current_schema()::regnamespace)",
  'pg_seclabel':"classoid='pg_class'::regclass AND objoid IN (SELECT oid FROM pg_class WHERE relnamespace=current_schema()::regnamespace)",
  'pg_shdepend':"dbid=(SELECT oid FROM pg_database WHERE datname=current_database()) AND classid='pg_class'::regclass AND objid IN (SELECT oid FROM pg_class WHERE relnamespace=current_schema()::regnamespace)",
  'pg_subscription_rel':"srrelid IN (SELECT oid FROM pg_class WHERE relnamespace=current_schema()::regnamespace)",
  'pg_extension':"extnamespace=current_schema()::regnamespace",
 }.items():r['auxiliary'][name]=c.execute('SELECT to_jsonb(x) FROM pg_catalog.'+name+' x WHERE '+where).fetchall()
 r['catalog_fields']=c.execute("SELECT c.relname,a.attname,format_type(a.atttypid,a.atttypmod) FROM pg_class c JOIN pg_attribute a ON a.attrelid=c.oid WHERE c.relnamespace='pg_catalog'::regnamespace AND c.relkind='r' AND a.attnum>0 AND NOT a.attisdropped ORDER BY 1,a.attnum").fetchall()
 return r
p.snapshot=snap
p.add('E086','full catalog inventory and auxiliary baseline',[])
p.add('E087','extension config dump construction limit',["SELECT pg_extension_config_dump('mneme_store'::regclass,'')"])
p.add('E088','range over row type construction limit',['CREATE TYPE outside_range AS RANGE (subtype=mneme_store)'])
p.add('E089','operator class construction limit',['CREATE OPERATOR CLASS outside_ops FOR TYPE mneme_store USING btree AS OPERATOR 1 <(text,text)'])
p.add('E090','sequence type construction limit',['CREATE SEQUENCE outside_seq AS mneme_store'])
p.add('E091','typed foreign table construction limit',['CREATE FOREIGN TABLE outside_t (v mneme_store) SERVER absent'])
p.add('E092','transform reference construction limit',["CREATE FUNCTION outside_fun(mneme_store) RETURNS text LANGUAGE plpgsql TRANSFORM FOR TYPE mneme_store AS $$ BEGIN RETURN 'x'; END $$"])
p.add('E093','stored SQL procedure dependency',['CREATE PROCEDURE outside_proc() LANGUAGE SQL BEGIN ATOMIC SELECT tail FROM mneme_store; END'])
p.add('E094','constraint trigger WHEN row-type reference',['CREATE TABLE outside_t(v text)',"CREATE FUNCTION noop() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NEW; END$$",'CREATE CONSTRAINT TRIGGER outside_constraint AFTER INSERT ON outside_t FOR EACH ROW WHEN (ROW(NEW.v,0)::mneme_store IS NOT NULL) EXECUTE FUNCTION noop()'])
p.add('E095','outside FK to other namespace',['CREATE SCHEMA outside_ns','CREATE TABLE outside_ns.fk(sid text REFERENCES mneme_store)'])
p.add('E096','outside FROM trigger in other namespace',['CREATE SCHEMA outside_ns','CREATE TABLE outside_ns.t(v text)',"CREATE FUNCTION noop() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NEW; END$$",'CREATE CONSTRAINT TRIGGER outside_constraint AFTER INSERT ON outside_ns.t FROM mneme_store FOR EACH ROW EXECUTE FUNCTION noop()'])
# p.run drops only its own schema; two outside_ns cells explicitly reverse at end of setup
# Instead retain independent namespace with a name below current_schema so probe cleanup CASCADE
# cannot own it: custom snapshot cleans it after public (ordinary role, project throwaway DB).
p.run()
for name in ('rows','cleanup','engine','inventory'):
 (p.OUT/(name+'3.json')).write_bytes((p.OUT/(name+'.json')).read_bytes())

```

### last.py

```python
import probe as p
p.CASES=[]
p.add('E097','outside FROM trigger in separate namespace',['CREATE SCHEMA outside_ref','CREATE TABLE outside_ref.t(v text)',"CREATE FUNCTION noop() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NEW; END$$",'CREATE CONSTRAINT TRIGGER outside_constraint AFTER INSERT ON outside_ref.t FROM mneme_store FOR EACH ROW EXECUTE FUNCTION noop()'])
p.add('E098','initial privilege catalog construction limit',["UPDATE pg_init_privs SET privtype='e' WHERE false"])
p.add('E099','security label catalog construction limit',["UPDATE pg_seclabel SET label='probe' WHERE false"])
p.add('E100','subscription binding construction limit',["UPDATE pg_subscription_rel SET srsubstate='r' WHERE false"])
p.add('E101','transform binding construction limit',["UPDATE pg_transform SET trftype='mneme_store'::regtype WHERE false"])
p.add('E102','depend binding construction limit',["UPDATE pg_depend SET deptype='e' WHERE false"])
p.run()
for name in ('rows','cleanup','engine','inventory'):
 (p.OUT/(name+'4.json')).write_bytes((p.OUT/(name+'.json')).read_bytes())

```

### routes.py

```python
import probe as p
p.CASES=[]
old=p.snapshot
def snap(c):
 r=old(c)
 r['route_values']={}
 for cat,where in {
  'pg_proc':"pronamespace=current_schema()::regnamespace",
  'pg_range':"rngtypid IN (SELECT oid FROM pg_type WHERE typnamespace=current_schema()::regnamespace)",
  'pg_type':"typnamespace=current_schema()::regnamespace",
  'pg_constraint':"connamespace=current_schema()::regnamespace",
  'pg_extension':"extnamespace=current_schema()::regnamespace",
  'pg_depend':"(classid='pg_class'::regclass AND objid IN (SELECT oid FROM pg_class WHERE relnamespace=current_schema()::regnamespace)) OR (refclassid='pg_class'::regclass AND refobjid IN (SELECT oid FROM pg_class WHERE relnamespace=current_schema()::regnamespace))",
 }.items():r['route_values'][cat]=c.execute('SELECT to_jsonb(x) FROM pg_catalog.'+cat+' x WHERE '+where).fetchall()
 return r
p.snapshot=snap
p.add('E103','outside domain CHECK indirect constraint',['CREATE DOMAIN outside_domain AS mneme_store CHECK ((VALUE).tail >= 0)'])
p.add('E104','variadic row-type-array signature',['CREATE FUNCTION outside_variadic(VARIADIC v mneme_store[]) RETURNS integer LANGUAGE SQL AS $$ SELECT 1 $$'])
p.add('E105','all-argument and INOUT row-type signature',['CREATE FUNCTION outside_inout(v text,INOUT x mneme_store) LANGUAGE SQL AS $$ SELECT x $$'])
p.add('E106','moving aggregate row-type-state',['CREATE FUNCTION outside_state(mneme_store,mneme_store) RETURNS mneme_store LANGUAGE SQL AS $$ SELECT $1 $$','CREATE AGGREGATE outside_agg(mneme_store) (SFUNC=outside_state,STYPE=mneme_store,MSFUNC=outside_state,MINVFUNC=outside_state,MSTYPE=mneme_store)'])
p.add('E107','expression-index statistics target control',['CREATE INDEX outside_expr ON mneme_store ((tail+1))','ALTER INDEX outside_expr ALTER COLUMN 1 SET STATISTICS 300'])
p.add('E108','range subtype actual catalog row',['CREATE TYPE outside_range AS RANGE (subtype=mneme_store)'])
p.add('E109','extension membership actual outgoing edge',['CREATE EXTENSION hstore','ALTER EXTENSION hstore ADD TABLE mneme_store'])
p.run()
for name in ('rows','cleanup','engine','inventory'):
 (p.OUT/(name+'5.json')).write_bytes((p.OUT/(name+'.json')).read_bytes())

```

### interactions.py

```python
import probe as p
p.CASES=[]
p.add('E110','missing cache with exempt planner statistics',['ALTER TABLE mneme_store ALTER COLUMN store_id SET STATISTICS 200','ALTER TABLE mneme_store DROP COLUMN tail','ALTER TABLE mneme_store ADD COLUMN tail bigint NOT NULL DEFAULT 1 CHECK(tail BETWEEN 0 AND 9007199254740991)','ALTER TABLE mneme_store ALTER COLUMN tail SET DEFAULT 0'],'cache','old')
p.add('E111','outside FROM link with exempt grants',['GRANT SELECT(tail) ON mneme_store TO PUBLIC','CREATE TABLE outside_t(v text)',"CREATE FUNCTION noop() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NEW; END$$",'CREATE CONSTRAINT TRIGGER outside_constraint AFTER INSERT ON outside_t FROM mneme_store FOR EACH ROW EXECUTE FUNCTION noop()'])
p.add('E112','outside same-name relation FROM link',['CREATE SCHEMA elsewhere','CREATE TABLE elsewhere.mneme_store(v text)',"CREATE FUNCTION noop() RETURNS trigger LANGUAGE plpgsql AS $$BEGIN RETURN NEW; END$$",'CREATE CONSTRAINT TRIGGER outside_constraint AFTER INSERT ON elsewhere.mneme_store FROM mneme_store FOR EACH ROW EXECUTE FUNCTION noop()'])
p.run()
for name in ('rows','cleanup','engine','inventory'):
 (p.OUT/(name+'6.json')).write_bytes((p.OUT/(name+'.json')).read_bytes())

```

## Evidence integrity and cleanup

- `rows1.json`: SHA-256 `fb8b348272d81d79ef97c59268e6c5a358697c775efab7236802c4d7314a7706`
- `rows2.json`: SHA-256 `c00a6f72b0f0179cfd5917d24f80dd1a937de28e2421e01d6cd39e62c1a60b53`
- `rows3.json`: SHA-256 `587ccf98b88f0e21c4bf8d4a72ec53f023518dcd8867bc03fdb12bbca396052f`
- `rows4.json`: SHA-256 `372d5a19952fdcab24d83b225f0226fe24d27bf38fbc6693a5e58d704a109218`
- `rows5.json`: SHA-256 `d31f51359e4b7a31649348aff38fab517eaaed8c51521fdaf04125d1f6d2a25e`
- `rows6.json`: SHA-256 `a9df826e4b5d55c03419eab8bc2dac416401f48f40f98192b1105335fca5c9f3`
- `cleanup1.json`: SHA-256 `39b95541f157cace3e162013e92e082bfdb1dd809f1c3ae1f728b626690278ce` — {"database":"mneme_codex_ce04ext_76520bad3221","dropped":true}
- `cleanup2.json`: SHA-256 `abf9d4dd6bfe7c325578da223554737e6c21658585df71288c4813fbd4120196` — {"database":"mneme_codex_ce04ext_f58591ca4e49","dropped":true}
- `cleanup3.json`: SHA-256 `8e8d3f9037b23d6f26bdaa19827063aabf97332ba2b16ce2626dd1ccf9d75c70` — {"database":"mneme_codex_ce04ext_90a8183681cf","dropped":true}
- `cleanup4.json`: SHA-256 `fd7496370448151ea96f59084d51a1ddbc4b233cdf5bcb1059d89225d53cecf1` — {"database":"mneme_codex_ce04ext_a75a7cf41630","dropped":true}
- `cleanup5.json`: SHA-256 `5cb1f39185991bdfc4a411a6a0c807039e32ad9f33884543d9465165ad04a35e` — {"database":"mneme_codex_ce04ext_86830f90ebb6","dropped":true}
- `cleanup6.json`: SHA-256 `d53e056ccca1d13f9d284827c70eb2e5f20db1efb20516cca2cb68503e37f1b5` — {"database":"mneme_codex_ce04ext_d0761d578e4e","dropped":true}
- `inventory.json`: SHA-256 `a7f4291c40e5441e8fdb85ad0b12d7b6ef058e8190b43e4c98a54437b2ecce53`
- `probe.py`: SHA-256 `a4b7dac2b9e9188e1024b3423eeb57af450ea309303335faaad3076460806a0a`
- `more.py`: SHA-256 `12193c15a5a6cd5d25a04ba322711e5a88736993ac467731641442037d81d464`
- `final_probes.py`: SHA-256 `f18789ffc4c8a6a32c48c831761b4938bb0117890f2b719c88ade3afbf74b255`
- `last.py`: SHA-256 `75f6b57fcbff8421be0b143a2913ac1fc03e343b19fc53c3998e4213e5d24e02`
- `routes.py`: SHA-256 `26ee8e30275edfbe8719828679ff7ba103c300992698ea1a3504b85dcebb1acc`
- `interactions.py`: SHA-256 `86b334332ce07dc9f6fd361b03c947dda154c278ca1d9039503b65896df30861`


No production change, main/state/registry edit or source-bundle edit was made. The only tracked artifact change is this extension. Six database drops completed; the one cross-schema fixture and the trusted extension were confined to the dropped databases. No new roles, provider, subscription, replication slot, event trigger or Docker batch was created. CR-009..011 remain closed; no whole-library regression or new implementation closure is asserted.

## Primary PostgreSQL references supporting interpretation

These links supply engine meaning, not replacement public evidence or authority to choose contract policy. All behavior cells above are executions. Attribute cached defaults and copied representation fields: [pg_attribute](https://www.postgresql.org/docs/14/catalog-pg-attribute.html). Relation identity, lazy summaries, vacuum horizons and rewrite state: [pg_class](https://www.postgresql.org/docs/14/catalog-pg-class.html). HOT-safety index gate: [pg_index](https://www.postgresql.org/docs/14/catalog-pg-index.html). Genuine dependencies and their direction: [pg_depend](https://www.postgresql.org/docs/14/catalog-pg-depend.html); parsed SQL bodies versus string bodies: [dependency tracking](https://www.postgresql.org/docs/14/ddl-depend.html). Rule ownership/action distinctions: [pg_rewrite](https://www.postgresql.org/docs/14/catalog-pg-rewrite.html). Publication mappings: [pg_publication_rel](https://www.postgresql.org/docs/14/catalog-pg-publication-rel.html), subscription binding: [pg_subscription_rel](https://www.postgresql.org/docs/14/catalog-pg-subscription-rel.html). Extension object ownership semantics: [ALTER EXTENSION](https://www.postgresql.org/docs/14/sql-alterextension.html). Initial grants, security labels and shared dependencies: [pg_init_privs](https://www.postgresql.org/docs/14/catalog-pg-init-privs.html), [pg_seclabel](https://www.postgresql.org/docs/14/catalog-pg-seclabel.html), [pg_shdepend](https://www.postgresql.org/docs/14/catalog-pg-shdepend.html).

The next step is Claude's per-row classification and completeness challenge, then a revised two-party checkpoint. No production repair is authorized by this characterization alone.
