# WP-04 (Layer 04) — Rust CLOSURE_REVIEW (Claude)

**Verdict: CHANGES_REQUIRED.**
- **Findings:** two witness gaps, WP04-CR-017 and WP04-CR-018. Both are test-only. **No Rust
  production defect and no contract gap was found.**
- **What was done:** a reading of the Rust source against the contract, a full independent gate run,
  12 of 14 of Claude's own planted violations killed, and the Python suite at the candidate.

**Exact pair:**
- code `6ef220e5b4f48ea8d458ead2f30dfdfcf67cba3d` (`wp04/rust`), one commit over code `main`
  `9d5a2d51`;
- docs `137778f79a34b8187088ab4c5964934e72702f33` (`wp04/rust`, from docs `main` `42a7d4fa`), with
  state on `wp04/rust-state` at `60050323`.

**Author:** Codex. **Reviewer:** Claude, who wrote no Rust code.

**Authority:**
- the accepted Layer 04 contract (`spec/persistence.md`) and G-077…G-098;
- the agreed CE-04-01 checkpoint (classification revisions 2–5);
- `reference-backend/postgres14-v1-catalog.json`;
- the five ACTIVE store scenarios;
- `assurance/layers/04-feasibility-matrix.md` §3a.

Codex's record (`assurance/reviews/WP-04-rust-implementation-codex.md`) was treated as claims to
reproduce.

## Reading against the contract

| Area | Finding |
|---|---|
| Open (`persistence/mod.rs`) | <ul><li>A private connection with UTF8 `client_encoding` and `synchronous_commit` on, then an explicit Read Committed read-write transaction whose first statement is `pg_catalog.pg_advisory_xact_lock` on the shared key.</li><li>Then the environment predicate (major 14, UTF8, C/POSIX), and the namespace by `current_schema()`. With no namespace, the engine's own 3F000 surfaces.</li><li>Initialization only when the `relations` part is empty, with `SET LOCAL` pins, `pg_catalog`-typed DDL qualified by the quoted namespace, and the full re-fetch postcondition before commit.</li><li>Then the comparison, and exactly one version-1 row.</li><li>Engine errors stay `StoreError::Database` and are never reclassified.</li></ul> **As agreed.** |
| DDL | `BETWEEN` is written as two `pg_catalog` comparisons. The parser rewrites `BETWEEN` to the same tree, and the [PIN] test proves the initializer equals the shared pins. |
| Commit | <ul><li>Generic stages, then `store_id`, `writer`, `operation` and `records` (non-array or empty: `persistence.batch_invalid`).</li><li>Per-draft admission through the **additive** Layer 02 draft mode (`record_rule(…, draft=true)`). Replay admission is unchanged, and a supplied `recorded_at` fails D3.</li><li>In-batch duplicates.</li><li>Under the store-row `FOR UPDATE` lock: unknown store, retry identity on canonical normalized draft bytes (conflict otherwise), store duplicates, capacity (`persistence.store_full` with no argument, spec step 11), then **one** clock sample. Records and the operation are inserted and the tail advanced in one transaction.</li><li>A defective clock is `StoreError::Clock`, and the transaction rolls back on drop.</li></ul> **As agreed** (G-083…G-086). |
| Read and tail | One Repeatable Read read-only snapshot. The limit is validated before the boundary comparison. Store unknown, then incomparable, then invalid boundary. `through` is the last returned position, or `since` for an empty page. The tail is under Read Committed read-only. |
| Catalog (`persistence/catalog.rs`) | <ul><li>The twelve parts in checkpoint order.</li><li>The structural island, identical to the agreed one.</li><li>The closed exclusion lists and the normalizations equal §10.1 and G-098: type copies against `pg_type`, and `relnatts` / `relchecks` invariants.</li><li>Members are rendered as PostgreSQL's own `jsonb::text`.</li><li>The boundary is inbound with the statistics exemption by dependent class, and outbound with the namespace and built-in allowances, plus labels.</li><li>Every relation, type, function and operator is `pg_catalog`-qualified, except `COALESCE`, which is syntax.</li></ul> **As agreed.** |
| Lower layers | Additive only: the eight `persistence.*` error codes, the draft flag, and crate-visible helpers. Layers 01–03 suites pass unchanged. |
| Runner | Thin. It delegates to the public store. It decodes the store ID only to bind the clock fixture after a successful create, the pattern accepted for Python. It would report any store-error `position` rather than hide it. |

**Observation (no finding).** For constraint expression trees, Rust maps column numbers to names
by the row's table *name* even when the constraint's own relation is out of scope. Python does so
only for in-scope rows. No observable consequence follows: any out-of-scope constraint row already
differs from the pins, which hold only in-scope rows, so it is refused either way.

## Executions (Windows, the scheduler-granted window; rustc and Cargo 1.97.1; Cargo jobs ≤ 4)

| Check | Result |
|---|---|
| G0 | exact candidate, clean tree |
| `cargo fmt --check`; `cargo clippy --locked --offline --workspace --all-targets -- -D warnings`; `RUSTDOCFLAGS=-Dwarnings cargo doc --no-deps` | all clean |
| `cargo test --locked --offline -- --test-threads=1` (own review target) | **64 integration tests + 1 doctest passed**: conformance 5, layer01 13, layer02 14, layer03 9, layer04 23 |
| Python suite at the candidate tree (own venv) | **856 passed, 4 xfailed**; the manifest backlinks, with the Rust locations, validate |
| `mneme-process check --deep-sources` at the pair | 8/8 |
| Cleanup | own throwaway database dropped; 0 owned remain; the source tree is clean after every batch |

### Claude's planted violations (14, independent of Codex's M01–M30; separate controls target)

Each has an intended witness that passed on unmodified source first.

| ID | Planted wrong implementation | Intended witness | Result |
|---|---|---|---|
| R01 | retry check skipped (falls to the duplicate check) | `capacity_retry_conflict_duplicates_and_clock_order` | killed |
| R02 | clock sampled before the capacity check | same | killed |
| R03 | statistics exemption removed | `classified_public_catalog_witnesses` | killed |
| R04 | the namespace edge not allowed | `normative_pins_initializer_and_embedding` | killed |
| R05 | TOAST-index ordering read as the pinned constant | `fetch_binding_projects_real_catalog_fields` | killed |
| **R06** | **table `relpersistence` read as the pinned constant `'p'`** | `fetch_binding_projects_real_catalog_fields` | **SURVIVED** (WP04-CR-018) |
| R07 | reads under Read Committed | `read_snapshot_during_commits_and_record_counted_pages` | killed |
| R08 | open inherits the session isolation | `waiting_first_open_uses_read_committed_not_the_session_default` | killed |
| R09 | database encoding not checked | `non_utf8_database_is_refused_and_private_handle_pins_utf8` | killed |
| **R10** | **initialize unless an ordinary table exists** (a v1-named view or sequence passes the guard) | `initialization_refuses_partial_nonindex_relations_and_preserves_engine_errors` | **SURVIVED** (WP04-CR-017) |
| R11 | in-batch duplicate IDs not checked | `draft_gates_and_array_order_before_duplicates_or_store` | killed |
| R12 | `limit` 0 accepted | the canonical corpus (`conformance`) | killed |
| R13 | a column's type copy read as a constant | `fetch_binding_projects_real_catalog_fields` | killed |
| R14 | security labels not read | `security_label_fetch_binding_checks_subobjects_and_internal_members` | killed |

**Whole-suite diagnostic.** R06 and R10 were each applied in turn, and the whole `layer04` and
`conformance` binaries were run. **Both pass completely**, so no Rust test detects either one.

Logs are in `.tmp/work/claude/l04-rust-review/`: `summary.txt`, `test.log`, `mutants.log`,
`diag-survivors.log` and `cleanup.log`.

## Findings

### WP04-CR-017 — no witness for a v1-named non-table before initialization

- Classification: **CONTRACT_ASSURANCE_DEFECT**; severity: **medium**; blocks Rust closure;
  `owner_decision_required: false`.
- Sources:
  - spec "Open and initialize" step 3: initialize only when the namespace holds no non-index
    `mneme_` relation;
  - CE04-CP-002;
  - Python's corresponding witness `test_public_ch09c_a_non_table_with_a_v1_name_blocks_initialization`,
    added after CE-04-01 gate run 1 for exactly this mutant class.

The Rust production guard is correct: `empty_namespace()` checks that the relations part is
empty. But no Rust test discriminates a wrong guard.
- **The existing test** uses only `mneme_surprise` objects. A wrong implementation initializes beside
  them, the postcondition refuses, and it rolls back, so the result is indistinguishable.
- **R27/R28** create v1-named views on an initialized schema, where ordinary tables exist.

**What the wrong implementation does.** Under R10, a namespace that holds only
`CREATE VIEW mneme_store …` or `CREATE SEQUENCE mneme_record` would attempt the initializer. The
duplicate-relation engine error (42P07) would surface as `StoreError::Database` instead of
`persistence.schema_incompatible`. This mirrors Python's diagnosed P46.

**Required:** a public witness on a namespace holding only a non-table with a v1 table name (a view
and a sequence): refused with `persistence.schema_incompatible`, nothing created. It must kill R10.

### WP04-CR-018 — the table's own persistence is not bound by any Rust witness

- Classification: **CONTRACT_ASSURANCE_DEFECT**; severity: **low–medium**; blocks Rust closure;
  `owner_decision_required: false`.
- Sources:
  - spec "Relations" (permanent tables);
  - the agreed CE-04-01 [F] method (classification §8.6);
  - WP04-CR-014's ruling that substituting an expected constant for a read is not contract
    equivalence over the pre-open domain (CE04-CP-003);
  - Python's [F] control `…supplied_field[table persistence]`, added after gate run 3 for this
    masking.

**Why the public witnesses don't catch it.** A genuinely unlogged table also makes its TOAST
relation unlogged, and the `members` part refuses that. So the public `SET UNLOGGED` witnesses
cannot tell whether the `relations` part reads `relpersistence`. A pre-open state in which the
table and its TOAST relation differ is reachable only by catalog manipulation, which is exactly the
predicate domain that CR-014 placed under the [F] method.

**What the wrong implementation does.** Under R06, the relations fetch returns the pinned `'p'`.
Every Rust test still passes, and such a state would be accepted.

**Required:** an [F] fetch-binding control that projects only the core table's `relpersistence`
through Rust's actual fetch SQL and expects the `relations` part. It must kill R06.

## Disposition

- **CHANGES_REQUIRED** on WP04-CR-017 and WP04-CR-018: test-only additions to `tests/layer04.rs`, plus
  the record. Production, pins and the corpus are unchanged.
- **Next:** a targeted re-review of the two findings at the remediated pair, with R06 and R10
  re-run.
- **Everything else in this review stands:** the contract reading, the gate results, and the 12
  killed controls.
