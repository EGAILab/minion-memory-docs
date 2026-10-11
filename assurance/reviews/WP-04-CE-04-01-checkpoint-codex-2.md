# WP-04 CE-04-01 checkpoint re-review — Codex

**Verdict: APPROVED**

Reviewed the exact docs state `4f3ceaa381906064687d3e99a896c1a7aa1b5c1d`: `assurance/convergence/CE-04-01-classification.md` revision 2, its §0 response, the revised reference-backend transcription in `spec/persistence.md`, the handoff and plan delta. Authority remains G-088..G-092 and the agreed contract. Frozen behavior reference is code `634625135851cccc188fe726acb86990911ebddb`.

This approval makes **this exact checkpoint AGREED FOR IMPLEMENTATION**. It is not approval of an implemented candidate, closure of WP04-CR-008, or acceptance onto main. Codex has made no production change. CR-009..011 remain resolved and outside the episode.

## Finding dispositions

| Finding | Disposition | Independent assessment |
| --- | --- | --- |
| CE04-CP-001 | RESOLVED | §5.2 removes the false pg_temp assertion and requires explicit engine qualification of catalog relations, types, functions, operators and aggregates, including casts and initialization DDL column types. Namespace is resolved first and store tables are qualified by it. CH12 is a direct SQL-text control, not an imaginary public-open execution. The private-session invariant is stated as an implementation obligation with evidence; it does not substitute for genuine lookup. |
| CE04-CP-002 | RESOLVED | The initial branch now requires no prefixed non-index relation, so a lone prefixed view cannot authorize initialization. The created catalog is checked before commit and a failed postcondition rolls back. CH09a/c preserve both independently executed witnesses from review 1 as FIX reject. CH09b explicitly retains the prior timeout as uncredited and requires a future constructed witness. The extra-row accounting is corrected. |
| CE04-CP-003 | RESOLVED | G-092's exclusion now expressly applies after open. A pre-open disabled internal trigger is incompatible. The RI oracle specifies the initialized internal/enabled state, constraint linkage, genuine built-in functions, relation placement and event masks. R32 remains construction-limited as a public kill, but the property is validated at open and receives bounded predicate evidence. |

No surviving blocker or new candidate path-C choice was identified in this targeted re-review. The previously accepted C02/C03 authority readings remain accepted; neither has been silently expanded into a new semantic choice. The repairs implement G-089..G-092 rather than changing those decisions.

## New and corrected controls

- **CH09a–c:** all three decided oracles are rejection with no mutation. The view-beside-tables and first-open-view cases were independently executed in review 1; the sequence setup timeout remains a limit, not a pass or rejection. A newly constructed sequence control is due with the implementation.
- **CH11:** resetting default_tablespace to the database default and default_table_access_method to heap, together with the same catalog postcondition before commit, prevents ambient settings from determining an uncertified initializer state. Creating a second non-default tablespace is not authorized, and writing through pg_default would violate OWN-001 on this host. The lack of that public execution is stated honestly. Predicate rejection of a nonzero reltablespace tests comparison only; the implementation evidence must separately demonstrate that initialization invokes the postcondition before commit and establishes its pins. A synthesized comparison row must not be reported as proof of that transaction control flow or a public CH11 execution.
- **CH12:** runs the implementation's actual SQL in a poisoned temporary-object session and compares with clean results. This is specifically a direct engine/SQL-text control: the specific CH12 obligation governs the generic §6 wording about public FIX witnesses. It covers types and catalog relations as well as the store table lookup; the actual DDL must use qualified types too. Unrelated temporary objects are not a compatibility-refusal reason.
- **CHECK inventory:** singleton, tail range and position range are all named, plus the two defaults. The three conditions must survive independently in the shared structured pins and controls; count alone is not expression validation.
- **X09/X10:** the revised lock evidence requires the exact key and single-bigint overload, opening pid, granted=true at an observation gate after acquisition, and release at transaction end. It excludes a merely waiting lock. X10 remains attached observation, not another open.

Original 136-row accounting was rechecked against the retained executed IDs: 24 KEEP accept, 5 FIX accept, 62 FIX reject, 26 KEEP reject, 7 engine errors, 1 FIX lock, 1 observer, 10 NOT CREDITABLE. The sets are disjoint and cover every original ID exactly once. The revised additions total **14**: 1 FIX accept, 7 FIX reject, 1 FIX direct-engine control, 1 KEEP accept, 1 KEEP reject and 3 construction-limited/predicate-tested rows. No extra view is incorrectly credited as KEEP reject.

R21/C16 remain catalog-identical accepts. C05/C06 remain explicit-column-collation FIX rejects under G-089; that is separate from G-090's database C/POSIX acceptance. The original NOT CREDITABLE set is retained without treating setup errors as validator kills. CH04's author-probe entry still says unexecuted; my independent execution is already recorded in review 1 and confirms its FIX reject disposition. Its implementation witness remains due.

## Independent execution in this re-review

One small throwaway-database catalog probe was executed on PostgreSQL 14.12 using the project-managed CPython 3.12.8 and psycopg 3.2.13 against the separate frozen code checkout. Every shell first sourced the project environment. Database creation used template0, UTF8/C/C and mneme_ts; a fresh private schema was initialized by the frozen public open. No production module was modified or remediation prototyped.

I independently fetched the actual RI trigger linkage, functions, activation and event masks of that initializer. The result is **eight** internal triggers: four for each of the two foreign keys, matching the revised oracle:

| Function in pg_catalog | Relation | tgtype | Enabled / internal | Deferrable / initially deferred |
| --- | --- | --- | --- | --- |
| RI_FKey_check_ins | referencing mneme_record or mneme_operation | 5 | O / true | false / false |
| RI_FKey_check_upd | referencing mneme_record or mneme_operation | 17 | O / true | false / false |
| RI_FKey_noaction_del | referenced mneme_store, once per FK | 9 | O / true | false / false |
| RI_FKey_noaction_upd | referenced mneme_store, once per FK | 17 | O / true | false / false |

Each tgconstraint joined to its actual foreign-key constraint. Argument count was zero, argument bytes empty and qualifier absent. These are actual initializer observations; their run-local object names/OIDs are not shared equality pins. The complete initializer state, not merely a matching function name, remains the finite comparison oracle.

Separately, in a direct engine transaction I acquired the exact qualified single-bigint advisory lock and observed:

```text
classid = 3201722174       # 0xbed6673e
objid = 1984885122        # 0x764ef182
objsubid = 1
granted = true
```

The row was absent after rollback. SET LOCAL default_tablespace='' and default_table_access_method=heap produced the actual settings `('', 'heap')`. This validates the specified engine fields and setting syntax. It is **not** an execution of the future implementation's second-session gated X09 witness, CH11 adversarial initialization, or synthesized disabled-trigger predicate. Those remain implementation evidence obligations.

The database was dropped in the probe's finally block. No superuser credentials, non-project tablespace writes, foreign-session termination or service changes were used. All notes and outputs remain under `.tmp/work/codex/ce04-01/`:

- `checkpoint2_catalog_probe.py`, `checkpoint2-catalog-observation.json`, `checkpoint2-catalog-probe.log`;
- `checkpoint_accounting.py`, verifying the original 136-ID partition;
- prior characterization and checkpoint-1 executions, unchanged.

## Predicate evidence and implementation boundary

The fetch/compare split is a sound bounded route for nonconstructible properties. Begin with actual accepted initializer rows, vary one semantic property, verify the pure comparator's decided result, and report it as predicate evidence. POSIX database locale variants and exempt ownership are acceptance controls, not rejection kills. For properties the trusted engine cannot expose through permitted DDL, this does not claim the corrupted state was publicly constructed.

Predicate tests do not replace evidence that fetching includes the property, links it to the correct object, and passes the complete state to comparison. The existing public malformed-catalog controls, fresh initialization/existing-open branches, private-session evidence and planted violations must cover that integration. Mutation evidence must distinguish a direct-predicate kill from a public-open kill and explain any engine-constrained equivalence. In particular, P44 must establish initialization pins/postcondition behavior rather than borrow a comparator-only rejection.

The revised structured-comparison and shared-pin obligations, public controls for constructible FIX rows, direct controls for CH12, bounded predicates, cross-language initialization/open witnesses and gates are sufficient to proceed to the single implementation pass. Actual pins, SQL texts, transaction behavior, G3 and mutation results are due at implementation closure; this checkpoint does not invent their results.

The host reservation remains in force. No new suite, mutant batch, Docker/POSIX run or G3 run was started in this re-review. The full implementation gates wait for host clear as specified. Only this review record is committed on `review/wp04-ce1-checkpoint-2` from the exact reviewed docs state.
