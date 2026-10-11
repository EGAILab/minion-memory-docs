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
