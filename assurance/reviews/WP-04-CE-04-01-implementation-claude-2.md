# WP-04 CE-04-01 — Claude's implementation record 2 (the pass for checkpoint revisions 2–5)

**Status: targeted closure APPROVED by Codex** (`assurance/reviews/WP-04-CE-04-01-closure-codex-2.md`,
`46514f00`).
- **Closed by Codex:** WP04-CR-008, CR-012, CR-013 and CR-014.
- **CR-015** (documentary, non-blocking): repaired in §2 and in the test comment (code `9d5a2d51`,
  comment only). It is left for Codex to verify in the final complete review.

The frozen candidate's gates are in §5.3.

**Authority:**
- the agreed checkpoint `assurance/convergence/CE-04-01-classification.md`, revisions 2–5 (Codex
  `APPROVED` `bfb6cad3` and `955d91f6`);
- `spec/persistence.md`, "v1 catalog contract" and "Trust scope";
- Owner G-088…G-098.

**Findings addressed:**
- WP04-CR-008 (open), with its successors WP04-CR-012 and WP04-CR-013;
- WP04-CR-014, an assurance finding.

**Candidate:** code `038416286631a34846f99bd53b7c4d6ed41d30cf` on `wp04/contract`. It is four
commits over `be36323f`:

| Commit | What |
|---|---|
| `6d0fb41d` | the implementation pass: production, pins and witnesses |
| `6cda5b46` | the 55 extension predicates collected (tests only) |
| `426f14f3` | a fetch-binding control for a cached value alone (tests only) |
| `03841628` | single-part witnesses after gate run 3 failed G4, and the P01 barrier (tests only) |

Where the tests-only commits came from:
- `6cda5b46` and `426f14f3` came from Claude's **pre-gate witness diagnostic** (§4), before any gate
  ran.
- `03841628` came from **gate run 3**, which failed (§5.1).

The submitted gate evidence is run 4 at `03841628` (§5.2). Run 3 is kept as the record of its
failure.

## 1. What changed

| File | Change |
|---|---|
| `persistence/catalog.py` | <ul><li>**Columns:** `atthasmissing`, `attmissingval`, `attfdwoptions`, `attcacheoff`, and the type copies checked for consistency with the column's `pg_type` (WP04-CR-012, G-098).</li><li>**Relations and indexes:** the remaining authoritative flags of §8.5.2–3, with `relnatts` and `relchecks` as invariants (G-098).</li><li>**New part `index_columns`:** whole index-attribute rows.</li><li>**New part `members`:** TOAST relations, TOAST indexes, their attributes, row and array types, each as `to_jsonb(row)` minus `MEMBER_EXCLUSIONS`, with associations normalized (`NORMALIZED`) (§10).</li><li>**New part `boundary`:** `pg_depend` edges crossing the structurally computed island, both inbound (planner statistics exempt by dependent class) and outbound (namespace and built-ins allowed), plus `pg_seclabel` rows on the island (WP04-CR-013, G-094, G-095, G-097).</li><li>Every SQL text stays `pg_catalog`-qualified. `COALESCE` is syntax, not a function, and cannot be shadowed.</li></ul> |
| `reference-backend/postgres14-v1-catalog.json`, `_v1_catalog.py` | Pins derived again by executing the **normative DDL** of the spec. On the baseline, `boundary` is empty, `members` has 29 rows and `index_columns` 9. |
| `tests/core/test_layer04_catalog.py` | The witnesses of §2. Production operations, transactions and locking are unchanged. |

## 2. Witness map (evidence kinds: [P] public, [T] transaction, [E] engine, [Pr] predicate, [F] fetch binding)

| Rows | Witness |
|---|---|
| E002 E003 E005 E006 E110 (cache); E028 E050 E051 E052 E097 E111 E112 (CR-013); the 28 dependency rows of §8.2; E062 E109; CH14 | [P] `test_public_open_refuses_an_incompatible_catalog_and_changes_nothing[<row>]`, with the characterization's literal setups. The extra schema and publication names are prefixed by the test schema's name. |
| E011–E018, E020, E033, E042, E046, E056 | [P] `test_public_open_accepts_a_v1_catalog_and_protocol_n_holds[<row>]` |
| E004 | [P] `test_public_e004_…`, with its own oracle: the old store reads tail 1, a commit receives 2..3, reads return [2, 3] and the tail is 3, with an identical retry. Protocol N is run separately on a new store. |
| CH13 | the baseline and large-payload rows (unchanged) |
| the 18 new pinned fields of §8.3 and the 28 G-098 rows of §9.1; the members' row layouts; CH16; CH18 | [Pr] `test_predicate_an_extension_difference_is_refused[…]` (58 cases at the candidate: 55 added in `6cda5b46` and 3 single-part added in `03841628`; with a collection guard); the residue positive control `test_predicate_dropped_column_residue_keeps_the_relnatts_invariant` |
| CR-014 and the predicate-domain properties | [F] `test_fetch_binding_control_the_fetch_reports_a_supplied_field[…]` (18, including `table persistence`) and `…_supplied_row[…]` (2): `tgenabled` (P40), `indisvalid` and `indisready` (P32), `atthasmissing` alone, a cached value alone, a type copy, `attcacheoff`, an index descriptor, an index's persistence, TOAST-index options, ordering, operator class and uniqueness, an extra TOAST index, TOAST-relation options (refused by `relations`) and persistence, a row-type field, an array backlink, a security label |
| Single-part witnesses after run 3 | [Pr] `…extension_difference_is_refused[part inheritance alone / part policies alone / part rules alone]`; [F] `…supplied_field[table persistence]`; [F] `test_fetch_binding_control_the_fetch_reports_a_supplied_patched_row[…]` (5): a genuine catalog row copied with one field changed so it names a v1 table, and no dependency row added. Isolation as measured by Codex (closure review 2, WP04-CR-015): <ul><li>**rule, policy and inheritance rows** come from unrelated objects; only `rules`, `policies` and `inheritance` differ respectively.</li><li>**The trigger row** copies a core internal RI trigger with `tgisinternal` false; only `triggers` differs.</li><li>**The index row** is redirected into the island, so `indexes`, `index_columns` and `boundary` all differ. P31's kill is a bounded fetch kill: losing the `indexes` read moves the first mismatch to `index_columns`. It is not a single-part projection.</li></ul> |
| §10.3 inventory | `test_every_member_catalog_column_is_compared_or_named_as_excluded`: the live columns of the four catalogs equal compared ∪ excluded, the two are disjoint, and the normalized columns are among those compared |

How the [F] controls work:
- A connection proxy replaces `pg_catalog.<catalog> ` in the store's **actual** fetch SQL with a
  projection.
- The projection lists every live column, with a `CASE` on the overridden one, or adds a row with
  `UNION ALL`.
- Each control asserts that the genuine catalog is v1 first, that at least one query was rewritten,
  and the expected part.
- These are never public or physical executions.

## 3. Planted violations

| Set | Script | Contents |
|---|---|---|
| G4 | `py_mutants_ce0401.py` (59) | <ul><li>The 42 of the earlier record, with P32 and P40 now aimed at their [F] controls.</li><li>P24 for `index_columns`, `members` and `boundary`.</li><li>P55–P68.</li></ul>The table as it stood at `be36323f` is kept as `py_mutants_ce0401.be36323f.py`. |
| G5 | `py_mutants_wp04.py` | unchanged; P14 is the known equivalent |

After run 3, the intended witnesses were re-pointed as §5.1 states (no mutant body changed, except
P31's filter field), and P01's witness gained a barrier. P38 remains the one claimed
engine-constrained equivalent, in Codex's narrower scope (checkpoint
review 1).

## 4. Pre-gate witness diagnostic (classification rev. 3 §8.6; not gate evidence)

`ce0401_witness_diag.py` applied each of the 19 new or re-pointed mutants and ran the whole witness
module. The log is `ce0401-gates-rev5/diag-witnesses*.log`. It found three things, each fixed before
any gate ran:

| Finding | Fix |
|---|---|
| The 55 extension predicates were never collected. `PREDICATES.update()` ran after the decorator had read its argument list. | `6cda5b46`: their own parametrized test, plus a guard |
| P67 dropped the `indoption` key, so every schema was refused: a vacuous kill. | Redesigned to read the pinned constant `[0, 0]`. Only its [F] control fails. |
| P68 (`attmissingval` not read) survived. Its predicate witness never runs the fetch, and the public cache rows also set the flag. | `426f14f3`: [F] "cached value only" |

At `426f14f3`, every one of the 19 is caught by its intended witness. Where a mutant leaves every
schema refused (P60–P62, the island's own members), the intended witness is the baseline accept
row B01. That is the stated oracle for those mutants: the island must never refuse its own members.

## 5. Gates (`ce0401_gates.sh`)

### 5.1 Run 3 at `426f14f3`: G4 FAILED (logs `.tmp/work/claude/ce0401-gates-426f14f3/`)

| Gate | Result |
|---|---|
| G0 | candidate clean |
| G1 | exit 0 |
| G2 | exit 0: 847 passed, 4 xfailed |
| G3 | 1304 statements, 490 branches, 0 missed: 100 % |
| G4 | **FAILED**: 44 killed, 15 survived. The survivors were P38 (claimed equivalent), **P01**, P24 for relations, inheritance, policies, rules, triggers and indexes, and P25, P27, P28, P30, P31, P33. |
| G5 | 17 killed; P14 survived (known equivalent) |
| post | tree clean |

Two causes, both Claude's.

**Overlapping parts.** The new `boundary`, `members` and `index_columns` parts also refuse the
earlier public witnesses of those six parts:
- a rule, trigger, policy or inheritance child on a core table records a dependency edge;
- an unlogged table's TOAST relation is unlogged too;
- an extra index adds index-column rows.

So a mutant that skips or blinds one older part was masked. §4's pre-gate diagnostic had covered
only the new mutants, not the old ones whose witnesses the new parts overlap. P31 was also broken: its
filter read the row's last field, which is no longer the backing-constraint list.

**P01 (no store-row lock).** It survived 5 of 5 reruns. Opens are serialized by the schema-open
lock and are now slower, so each parallel writer finished before the next one had opened, and the
witness never raced.

**Fixed in `03841628` (tests only; production unchanged):**
- **Single-part witnesses:** a predicate with a single inheritance, policy or rule row. P24 for
  relations, triggers and indexes uses an existing single-part predicate.
- **[F] controls:**
  - a table's persistence;
  - patched rows: a genuine row of an unrelated object, redirected to a v1 table, for triggers, rules,
    policies, indexes and inheritance. No dependency row is added, so only the part that reads that
    catalog differs.
- **P31:** its filter now reads the backing-constraint field.
- **P01:** the parallel writers open first and then commit together at a barrier. Killed 3 of 3.
- **The run 3 table** is kept as `py_mutants_ce0401.426f14f3.py`.
- **Before run 4:** a dry run of the **complete** table (`ce0401-gates-rev5/dryrun-g4.log`), not
  gate evidence.

### 5.2 Run 4 at `03841628` (logs `.tmp/work/claude/ce0401-gates-03841628/`)

| Gate | Result |
|---|---|
| G0 | `candidate 038416286631a34846f99bd53b7c4d6ed41d30cf clean` |
| G1 | exit 0 (ruff check, ruff format --check, mypy --strict) |
| G2 | exit 0: **856 passed, 4 xfailed** in 194.31 s. The xfails are the layer 08/15 placeholder scenarios. |
| G3 | **1304 statements, 490 branches, 0 missed: 100 %** (all of `minion_memory`, branches, subprocesses, no exclusions) |
| G4 | **58 killed of 59**. The one survivor is P38, the claimed engine-constrained equivalent in Codex's narrower scope. P32 and P40 were killed by their [F] controls, never by public executions. |
| G5 | 17 killed of 18. P14 survived (the known equivalent). |
| post | `tree clean at 038416286631a34846f99bd53b7c4d6ed41d30cf` |

Before run 4, a dry run of the complete table gave the same 58 of 59 (`dryrun-g4.log`, not
evidence).

### 5.3 Run 5: the frozen final candidate `9d5a2d51` (adopted §11.8.8; logs `ce0401-gates-9d5a2d51/`)

`9d5a2d51` is `03841628` (approved in closure review 2) plus the comment-only WP04-CR-015 repair.

| Gate | Result |
|---|---|
| G0 | `candidate 9d5a2d51c69987f799962868b8dc5175a11882d2 clean` |
| G1 | exit 0 |
| G2 | exit 0: **856 passed, 4 xfailed** in 216.69 s |
| G3 | **1304 statements, 490 branches, 0 missed: 100 %** |
| G4 | **58 killed of 59**; P38 survived (claimed equivalent) |
| G5 | 17 killed of 18; P14 survived (known equivalent) |
| post | `tree clean at 9d5a2d51c69987f799962868b8dc5175a11882d2` |

Earlier runs are kept:
- run 1 at `b657081b` (G4 failed);
- run 2 at `be36323f`;
- run 3 above.

Runs 1 and 2 recorded P32 and P40 as survivors, and those records stand.

## 6. Rust notes (amending record 1 §6)

- Embed the regenerated shared pins. The `members` documents are `jsonb` texts and must be produced
  with the same key set: every catalog column minus `MEMBER_EXCLUSIONS`, with `NORMALIZED` columns
  replaced by their stated normalizations. The pinned text is PostgreSQL's own `jsonb::text` output,
  which orders keys canonically. It is data serialization, not rendered SQL (G-091), so Rust's fetch
  must take the same `::pg_catalog.text` rendering.
- Port the [F] method over Rust's own fetch SQL, the inventory test, and the island and boundary
  witnesses.
