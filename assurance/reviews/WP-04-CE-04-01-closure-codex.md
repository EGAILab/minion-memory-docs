# WP-04 CE-04-01 implementation closure review — Codex

**Verdict: CHANGES_REQUIRED**

Exact pair: code `be36323f56e61d87776d11c831ae1ef0573ea692`, docs `22fe042080ce491a50ad02a7606246f3e853d7ab`. Authority: the agreed CE-04-01 revision-2 checkpoint approved at `bfb6cad3`, the reference-backend contract, and G-088..G-093. Reviewed separate checkouts. No production code, shared contract, registry or state was edited.

The implementation meets the original classified witnesses exercised below, and the tests-only evidence repair is legitimate. **WP04-CR-008 remains OPEN overall**: two executed catalog neighborhoods outside the finite fetch/pin inventory still pass. They require characterization/classification extension and a reviewed checkpoint before production remediation; this record does not authorize another unreviewed implementation pass. CR-009..011 stay resolved.

## Blocking findings

### WP04-CR-012 — live-column cached missing values escape the finite catalog comparison

- Classification: **IMPLEMENTATION_DEFECT**; severity: **high**.
- `owner_decision_required: false`; blocks WP-04 / CE-04-01 closure.
- Sources: exact code above, `minion-memory-python/src/minion_memory/persistence/catalog.py`, columns query and normalization; `_v1_catalog.py` and `reference-backend/postgres14-v1-catalog.json`; exact docs above, `spec/persistence.md`, v1 catalog contract and Trust scope; G-089/G-092.

The fetch reads the visible default and atthasdef but omits live-column `atthasmissing` / `attmissingval`. PostgreSQL can cache an ADD COLUMN default in column metadata for older tuples, independently of the subsequent visible default. Those fields influence reads; they are not merely the ignored ordinal or residue of a **dropped** column. [PostgreSQL 14 pg_attribute](https://www.postgresql.org/docs/14/catalog-pg-attribute.html), [ALTER TABLE](https://www.postgresql.org/docs/14/sql-altertable.html)

Executed minimal witness, with ordinary role mneme_dev, private schema and no usable handle during the DDL:

1. Initialize normally, create empty store `old`, close the handle.
2. Execute:

```sql
ALTER TABLE mneme_store DROP COLUMN tail;
ALTER TABLE mneme_store ADD COLUMN tail bigint NOT NULL DEFAULT 1
  CHECK (tail BETWEEN 0 AND 9007199254740991);
ALTER TABLE mneme_store ALTER COLUMN tail SET DEFAULT 0;
```

3. Query live metadata: `mneme_store.tail`, atthasmissing **true**, attmissingval **{1}**. The visible default is again the required 0; the live type, nullability, CHECK, column-name normalization and constraint-backed indexes match the embedded inventory.
4. Actual `mismatch(fetch(...), V1_CATALOG)` is **None**. Public reopen **accepts**.
5. Actual `store_tail('old')` is position **1** despite no records. First valid one-record append receives **2..2**; read from zero returns only position **[2]** and tail 2.

This is a pre-open catalog-state counterexample, not a request for a historical-row scan or protection against DDL made after the reviewed open returns. The same initialize/close/alter/reopen pattern is used by the agreed malformed-catalog witnesses. G-092 requires complete catalog validation at this new open; G-089 does not authorize semantic cached values as dropped-column identity. The changed catalog property is directly observable without scanning records. The operation trace illustrates its significance; the blocker is acceptance of a differing live semantic catalog state.

Required disposition under the existing strict contract: this pre-open state is schema_incompatible, unchanged. Extend the characterization/classification to live missing-value flags/cache versus dropped-column residue, with the finite initializer state and explicit controls; retain C20/C22's permitted identity cases. A legitimate operational migration needing a different live catalog state is a reviewed catalog-contract variation per G-089, not implicit tolerance. The fetch and shared pins must represent the agreed property at closure. No production patch is proposed here.

### WP04-CR-013 — an outside constraint trigger references a v1 relation without an outside FK row

- Classification: **IMPLEMENTATION_DEFECT**; severity: **medium**.
- `owner_decision_required: false`; blocks WP-04 / CE-04-01 closure.
- Sources: exact code above, catalog constraints query (conrelid/confrelid scope) and triggers query (tgrelid scope); exact docs above, spec/persistence.md v1 Relations: **“No constraint outside the four tables references them.”**

Executed ordinary-role witness beside an otherwise v1 schema:

```sql
CREATE TABLE outside(sid text);
CREATE FUNCTION probe.noop() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN RETURN NEW; END$$;
CREATE CONSTRAINT TRIGGER outside_constraint AFTER INSERT ON outside
  FROM mneme_store DEFERRABLE INITIALLY DEFERRED
  FOR EACH ROW EXECUTE FUNCTION probe.noop();
```

The actual constraint is contype **t**, conrelid **outside**, confrelid **0**. Its trigger has tgrelid **outside**, tgconstrrelid **mneme_store**, tgisinternal **false**. The explicit FROM reference is real engine metadata; PostgreSQL permits this constraint-trigger form with ordinary trigger/function privileges. [PostgreSQL 14 CREATE TRIGGER](https://www.postgresql.org/docs/14/sql-createtrigger.html)

The candidate fetch sees eight in-scope RI triggers, no differing constraint, and mismatch **None**. Public open **accepts**. The constraint lives outside but explicitly references the core table, contrary to the stated catalog rule. That this no-op fixture leaves ordinary store operations unchanged does not grant an exemption from the decided finite catalog rule; the same strictness rejects harmless outside FKs and indexes.

Required disposition: reject this pre-open constraint reference with schema_incompatible and no change. Characterize inbound constraint-trigger references separately from FKs and outgoing/in-scope triggers, then classify their oracle in the extended checkpoint. If Claude proposes limiting the published prohibition to foreign keys instead, that would change observable acceptance and requires Owner routing, not an author reinterpretation during implementation.

This is **not a kill of P38**: both the candidate and its exact P38 query variant accept it, because both queries miss the tgconstrrelid-only reference. The distinction is central to the equivalence assessment below.

### WP04-CR-014 — P40's public-fixture limitation is not contract equivalence

- Classification: **CONTRACT_ASSURANCE_DEFECT**; severity: **medium**.
- `owner_decision_required: false`; blocks closure assurance, not a new production repair.
- Sources: exact implementation record §4 and §5, the agreed checkpoint §0/§4.4/§5.3, G-092 and CE04-CP-003.

The record predicts and then accepts P40, which replaces the fetched activation with literal O, as an engine-constrained equivalent because an ordinary role cannot disable internal RI triggers. That is a limit of the **public fixture**, not equivalence over the decided open-time input domain. CE04-CP-003 specifically requires rejection of a pre-open disabled internal trigger however it arose; a genuine engine can contain that state after a privileged ALTER before the reviewed open. This review never used superuser credentials or constructed that physical state.

I executed a **direct fetch/predicate control**, keeping the physical initializer unchanged: a connection proxy substitutes a real SQL subquery projection for pg_catalog.pg_trigger in the actual fetch query, projecting D for the record INSERT-check trigger while retaining its genuine remaining catalog fields. Current fetch returns that D and mismatch=triggers; the actual `_open_locked` flow raises schema_incompatible. The **exact P40 projection** (SELECT literal O in place of g.tgenabled) loses it: mismatch=None and `_open_locked` returns the namespace. Pure comparator predicates alone still pass under P40 because they bypass this loss during fetch.

This is **not a public disabled-trigger execution**; it is a bounded dataflow control proving that the required read must not substitute an expected constant for a supplied semantic property. It kills P40's claimed equivalence on the already-decided predicate domain without inventing an administrator fixture. Evidence is in `p40_fetch_control.py` / `p40-fetch-control.json`, with actual current-versus-mutant observations and restored runtime query text.

Required repair: correct the equivalence claim and preserve a reproducible fetch-to-comparison control for trigger activation, reported in its actual evidence category. The current production fetch is correct for this control and needs no production edit for this finding. Do not credit its original public witness as a kill; the declared gate run still had the survivor. The mere fact that a prediction preceded the gate does not make its contract-domain argument valid.

## Independent executions and row dispositions

Executed independently against the exact candidate, with managed CPython 3.12.8 and psycopg 3.2.13. Host clear was in effect. Every shell sourced the project environment; all scratch, venv, image, cache and output files stayed under the E: project.

| Check | Independent result |
| --- | --- |
| Windows full suite, final sequential run | **713 passed, 4 xfailed**, 180.92 s; placeholders only |
| Windows coverage, branches and subprocesses, no exclusions | **1265/1265 statements, 490/490 branches**, zero missing or excluded lines |
| Ruff / format / strict mypy | pass; 26 files already formatted, no type errors |
| POSIX full suite, sequential rerun | **713 passed, 4 xfailed**, 184.37 s; managed Linux Python on an E:-backed, case-sensitive ext4 image (separate A/a proof), through a temporary relay to the same Windows PostgreSQL 14.12 service. This is not a separate Linux PostgreSQL-server execution. |
| CE-04-01 mutations, own isolated scratch copy, baseline before each intended witness | **39 killed / 42**, survivors P32/P38/P40, matching the reported set; no syntax/collection failures credited |
| Legacy WP-04 mutations, sequential after CE controls | **17 killed / 18**, survivor P14; the two owning modules were the declared witness set |
| Extra P40 fetch-to-comparison control | current code rejects projected D; exact P40 loses D and passes `_open_locked`; bounded direct fetch/predicate evidence, not a public physical-trigger execution |
| mneme-process check, all checks with deep sources | **8/8 passed** at the exact checkouts |

An initial POSIX/mutation overlap was diagnostic only: I stopped my own mutation driver, allowed its current child to finish, restored the isolated scratch sources, retained its partial logs under `diagnostic-overlap/`, then reran POSIX and all 60 controls sequentially. The final Windows suite/coverage/static batch was also run sequentially after the controls. No overlapping batch result is credited above. The 60 baseline results, intended failures and final source restoration were checked by `final_audit.py`.

The original 136 rows and 14 challenge additions retain their evidence kinds: public schema/open controls; direct engine CH12; transaction controls X09/initialization; pure predicates for nonconstructible states. No synthesized row set is counted as a public execution. The formerly timed-out sequence is now covered by a constructed public control. Matrix exceptions (R21/C16 identical catalog states; C05/C06 explicit non-default column collations; identity/statistics exemptions; construction limits) were checked against the agreed classification, not inferred from pytest's aggregate alone.

The fresh-namespace public controls, no-mutation snapshots, prefix objects before initialization, real inherited-row witness, RLS activation independent of policy presence, default-value changes independent of atthasdef, trigger/rule coverage on each table, CH07/CH07b, initialized metadata pins, environment/client encoding, CH12 poison baseline, internal-trigger predicates and gated X09 all exercise their declared scope. Initialization postcondition/pins are transaction controls with deliberate test instrumentation, correctly labelled; they are not public construction of another tablespace or extension.

Own notes are under `.tmp/work/codex/ce04-closure/`. `additional.py` / `additional-results.json` contain the cached-value witness and four actual outside-FK challenges. `p38_counterexample.py` / `p38-counterexample.json` contain the outside constraint-trigger observation and the exact P38 SQL variant. Despite the exploratory filename, its result is explicitly **not** a P38 kill. All corresponding own probe databases were dropped with ordinary DROP of known own names.

The full-suite/control fixtures use the candidate's own throwaway-database cleanup helpers. The explicit probe database prefixes were independently checked absent; source bytes in the mutation scratch copy match the candidate again. The temporary relay processes were stopped by their verified own command lines, their temporary credential copy was removed, and the ext4 image was unmounted. No unrelated process/database or service setting was changed.

Content-addressed retained evidence (SHA-256):

| File | SHA-256 |
| --- | --- |
| mutation-results.json | 9e767c7a62165b239a23b816788970c26d6cf3eb1bc7459acb34ec2428467bde |
| additional-results.json | c7e56b98e8b2063894efa2e9dd987b5aa205f14e6d2474cbac0e26408adc836a |
| p38-counterexample.json | 51c86acdbc35e49877540e7eb89478fa28bcd171b6df84de38d0e4443660b2f9 |
| p40-fetch-control.json | 92177857efc0a89085525481f75fc3e0a33e112fc124c1929cf3cb3c30b6b66a |
| coverage.json | 8db6912ad9170922a19a1b864978790d0e0b7bce7aa9e3e87526051ea42d8724 |
| windows-sequential-suite.log | 34fb0376e12104a8a291b4575038d0759e84158c1191165158e849b09ec71463 |
| posix-suite.log | 42ede4c11c97ea86a6cbf90b719abfd8b2f3604c410173ed1fd2f2fc320eae22 |

## Equivalence claims

**P32:** accepted as the stated trusted-engine-constrained fetch equivalence: constructing an invalid/not-ready **constraint-backed** index would require breaking the engine's constraint/index invariants. Constructible extra indexes are refused by their existence regardless. This does not exempt the explicit validity/readiness predicate or permit Rust to omit it. The engine restriction is narrower than a generic opening-role restriction.

**P40:** not accepted as contract equivalence, for WP04-CR-014's reasons. Ordinary-role fixture inability does not remove pre-open disabled internal triggers from the domain CP-003 expressly decided. The correct current fetch passes my added direct fetch/predicate control; the mutant does not. This control is not retroactively a kill in either author gate run.

**P38:** the post-hoc argument needs a narrower statement. For the exact mutation that omits constraints selected solely by **confrelid**, the missed standard catalog rows are inbound FKs. Their target-side RI triggers are fetched independently and make the catalog incompatible. I challenged this with ordinary, NOT VALID, initially deferred and partitioned outside FKs: each produced ten in-scope triggers instead of eight and a triggers mismatch even after the outside constraint rows were omitted. Public open refused each.

The broader record sentence that only a foreign key can reference a mneme_ relation is false: WP04-CR-013's constraint trigger uses another linkage. That linkage is absent from both versions, so it does not refute equivalence of the **exact P38 mutant**; it refutes completeness of the inbound-reference characterization. Correct the proof's scope rather than counting this as a killed P38 or using the equivalence claim to dismiss the uncovered dependency. [PostgreSQL 14 pg_constraint](https://www.postgresql.org/docs/14/catalog-pg-constraint.html) describes confrelid separately from CREATE TRIGGER's FROM relation.

**P14:** arithmetic through=min(since+limit,tail) is equivalent for valid gapless history in one snapshot, with record-counted limits. WP04-CR-012 demonstrates an accepted catalog that can cease to satisfy that premise; it does not justify extending the equivalence beyond certified v1 state. The catalog gap is the blocker, not a request to change bounded-read semantics.

## Tests-only remediation and six revised intended witnesses

The be36323f delta is exactly **24 lines in tests/core/test_layer04_catalog.py**, no production file. The three new control families exercise already-decided requirements. “Implement once” forbids a further unreviewed production/semantic pass; it does not forbid repairing assurance before the candidate is submitted, preserving the failed run and executing fresh gates. I accept this tests-only remediation. The record honestly keeps run 1 FAILED instead of retrospectively counting its survivors as kills.

| Re-pointed entry | Assessment |
| --- | --- |
| P24-columns → C13 | Legitimate isolation: storage changes the columns part; C01 also changes backing-index collation, so the original intended witness did not isolate this omission. |
| P24-constraints → K03 | Legitimate isolation: CHECK validation differs without the FK-trigger changes of K05. |
| P24-defaults → DEFAULT-tail | Legitimate new negative control: existing default changes value, while atthasdef remains true. C11 added a default and was caught by columns regardless. |
| P29 → RLS-enabled / RLS-forced | Legitimate independent states: no policy is created, so the policy inventory cannot mask omission of relation activation flags. Both states are forbidden already. |
| P33 → R05 | Legitimate isolation: an inherited child affects the scoped inheritance relationship; R06 also changed inherited column metadata. |
| P46 → prefixed non-table with a v1 table name | Legitimate required-error discriminator: the mutant's initialization branch collides with the object and leaks an engine error; a mneme_extra view was still refused by the postcondition. No oracle was changed to match the candidate. |

The corrected labels/witness declarations govern run 2 and the independent replay, not run 1. Selecting a newly isolating witness after diagnosing a failed intended witness is legitimate when the oracle is unchanged and the failure is retained. It would be illegitimate to claim the original witness killed the mutant, conceal a gap, count another random failure, or silently relax an acceptance rule; none of those is needed for these six changes. Baseline success, valid mutation anchors and failure origin were checked in the independent runner; collection/syntax failures are not kills.

## Closure and convergence disposition

Passing the declared witnesses and statement/branch floor does not establish completeness of a catalog trust boundary. The two new public observations remain outside the recorded finite inventory and gate controls. Extend the executed matrix and two-party checkpoint for those neighborhoods before production remediation; do not guess an equivalence rule for live cached values or silently redefine external constraints. The existing strict source supplies the rejection oracle; no new Owner choice is selected by Codex. Any proposed relaxation goes to the Owner as path C.

My original characterization also lacked discriminating rows for these two neighborhoods. That is a completeness gap in the episode, not evidence that the implementation was permitted to widen the finite contract. WP04-CR-014 additionally requires truthful assurance and a fetch-binding control; it does not authorize another production pass.

No acceptance onto main, WP-04 closure, or Rust implementation is authorized by this review. Only this record is committed on review/wp04-ce1-closure from the exact docs candidate. Source checkouts remain unchanged.
