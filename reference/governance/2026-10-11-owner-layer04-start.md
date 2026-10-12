# Owner decisions — Layer 04 start, split, backend and positions (2026-10-11)

Recorded verbatim by Claude.

## G-077 — Start Layer 04

**Context.** Layer 03 was certified (G-076). Claude reported that Layer 04 (persistence) waits for
the Owner.

> **Owner:** "Go ahead"

## G-078 — Split Layer 04: canonical history store first

> **Q:** Layer 04 bundles two surfaces: (a) the canonical history store — atomic append, idempotent
> commit per operation identity, store-assigned positions, bounded since-boundary reads, crash
> safety, single writer, profile identity in shared storage (PERS-005..008, 012, 014, 015,
> HIST-008/009); and (b) storage tiers, capture-before-enrichment, local-first and asset file
> integrity (PERS-001..004, 013, 016). How should it run?
>
> **A:** "Choose 1 — split Layer 04 into WP-04 and WP-04T, with the canonical history store
> first.WP-04 owns the cross-language semantic contract for atomic append, durable operation
> idempotency, gapless store-local positions, bounded since-boundary reads, crash/restart behavior,
> single-writer ordering and shared-profile physical storage. It is implemented and certified
> independently.WP-04T owns storage tiers, capture-before-enrichment orchestration, local-first
> behavior and asset-file integrity. It consumes WP-04’s committed durability barrier and must not
> redefine store ordering, atomicity or idempotency. WP-04T may be scoped in parallel, but its
> contract and implementation follow the agreed/certified WP-04 seam.Closing WP-04 certifies the
> canonical-store surface only; Layer 04 overall remains partial until WP-04T is independently
> closed."

## G-079 — Backend: backend-neutral contract, PostgreSQL reference backend

> **Q1:** What durable backend do both languages implement the store on, and must they share it?
>
> **A1:** "PostgreSQL, one shared schema"
>
> **Q2 (follow-up):** You chose PostgreSQL with one shared schema. The sources say 'Offline-first
> local persistence is the default; no learner history requires a backend for core operation'
> (R04 §20) and recommend SQLite for the first implementation (R04 §5/§39). How should the backend
> relate to that?
>
> **A2:** "Backend-neutral + PostgreSQL"

**Effect.**
- The WP-04 contract is **backend-neutral**: it fixes repository semantics only.
- PostgreSQL, with **one shared schema**, is the reference backend that both languages implement
  and certify on.
- An embedded backend (for example SQLite, for offline-first clients) can be added later without
  changing the contract.

## G-080 — Gapless store-local positions

> **Q:** How does the store assign positions (the Layer 02 store-local cursor, G-051/G-054) to
> committed records?
>
> **A:** "Choose 1 — history positions are gapless and increase by exactly one for every physical
> committed record.A successful batch receives one consecutive range in declared record order.
> Failed, aborted or rejected commits consume no positions. An idempotent retry of an already
> committed operation returns the original assigned range and consumes no additional positions.
> Committed positions are permanent, backend-independent and never reused or reassigned."

## G-081 — PostgreSQL provisioning and access

> **Q1:** How should PostgreSQL be provisioned for development and tests, given OWN-001
> (temp/caches/data inside the E: project folder, never C:)?
>
> **A1:** "PostgreSQL already installed as windows service"
>
> **Q2:** How should the project connect to your PostgreSQL 14.12 service (localhost:5432)? Test
> databases must keep their data on E: (OWN-001), which needs a tablespace in the project folder
> (created by a superuser, with the service account allowed to write there).
>
> **A2:** "Superuser once, I set it up" — meaning: the Owner puts the postgres superuser password in
> `.tmp/work/pg-admin.env`. Claude uses it once to create the role `mneme_dev` and the tablespace
> on E:, showing the exact SQL first, and never uses the superuser again.

**Observed.** The service is `postgreSQL` (PostgreSQL 14.12), running as
`NT AUTHORITY\NetworkService`, with its data directory under `C:\Program Files\PostgreSQL\14\data`
(an executed tool already installed on C:).

All project test databases are created in the tablespace `mneme_ts` at `.tmp/pgdata` on E:.
Credentials live only under `.tmp/work`, never in the repositories.

## G-082 — The store owns recorded_at; retry identity excludes store-generated fields (WP-04)

> **Q:** Who sets recorded_at? G-049 defines it as 'when the local durable writer
> committed/recorded the history record'. This also decides what an idempotent retry compares (a
> retry after a crash naturally carries a later wall-clock time).
>
> **A:** "Choose 1 — the store owns recorded_at.Callers submit canonical record content without
> recorded_at. For a previously unseen durable operation, the store samples an injectable clock once
> during the atomic commit and assigns the resulting canonical UTC timestamp to every record in that
> batch.Idempotency compares the normalized canonical caller-supplied mutation, excluding
> store-generated recorded_at, positions, and receipt metadata. A matching retry returns the original
> records, timestamp, positions, and receipt; a differing mutation under the same operation identity
> is a visible conflict.Failed or aborted commits persist neither timestamps nor positions.
> recorded_at is wall-clock metadata and does not replace the store-local position order."

## G-083 — Commits require writer-schema recognition and store-unique record IDs (WP-04)

> **Q:** What does the store validate when a batch is committed?
>
> **A:** "Choose 1 — canonical commits require full writer-schema recognition and globally unique
> per-store record IDs.Every submitted record must belong to the writer’s declared profile, use a
> record type/schema version recognized by that writer, and pass the complete applicable Layer-02 and
> profile-owned validation before becoming canonical. excluded and skipped_ignorable are reader
> outcomes and are not acceptable write outcomes. Any invalid, foreign-profile, or unrecognized
> record rejects the entire atomic batch.record_id is unique across the logical store, including
> across profiles. Reuse under a different operation rejects the batch even when content is
> identical. An idempotent retry does not append again; it returns the original committed records,
> timestamp and positions.Unknown required/ignorable records remain possible when an older reader
> later encounters records validly committed by a newer writer. Ordinary append therefore remains
> strict without sacrificing forward compatibility."

## G-084 — Concurrent commits are safely serialized (WP-04, PERS-015)

> **Q:** PERS-015: the MVP assumes one local active writer. What must the store do if two writers
> commit to the same store concurrently?
>
> **A:** "Choose 1 — commits to one logical history store are safely serialized.Concurrent commits
> are linearized into a single store-local commit order. Each successful commit receives one gapless
> consecutive position range, and uniqueness/idempotency checks, position allocation, recorded_at
> assignment, append, receipt persistence and tail advancement occur under the same atomic
> serialization boundary.Concurrent retries of the same OperationIdentity and same canonical
> mutation produce exactly one physical commit and return the same original receipt to all callers.
> Conflicting mutations or duplicate record IDs never use last-write-wins.This is local concurrency
> safety only; it does not define distributed synchronization, cross-store merge, or cross-device
> ordering."

**Setup executed (2026-10-11).**
- `.tmp/pgdata` was created, and `NetworkService` was granted modify rights on it only.
- Using the superuser once, the role `mneme_dev` (LOGIN, CREATEDB) and the tablespace `mneme_ts` (owned by
  `mneme_dev`, at `.tmp/pgdata`) were created.
- `mneme_dev` credentials are in `.tmp/work/pg.env`. The superuser file `.tmp/work/pg-admin.env` is no
  longer used by Claude.
- The service's default template collation name (`English_World.1252`) fails a case-sensitive check on
  Windows, so databases are created from `template0` with UTF-8 and the `C` collation, as the contract
  records.

## G-085 — Aborted commits may have sampled the clock (WP04-CR-005)

> **Q:** WP04-CR-005: a commit samples the injectable clock under the store lock, but the
> transaction can still abort after sampling (e.g. crash or rollback). The database can undo the
> write but not 'un-call' the clock. What should the contract promise about clock samples?
>
> **A:** "Choose 1 — aborted commits may have sampled the clock.A new valid commit attempt may
> sample the injected clock once after validation/idempotency checks and under the store
> serialization boundary. If the transaction subsequently aborts or crashes, the clock read is not
> reversible, but no recorded_at, position, operation receipt, or history record is persisted. The
> sampled instant has no semantic status.Validation failures, already-committed idempotent retries,
> and pre-commit operation conflicts do not sample the clock. A later retry after an aborted
> attempt may sample a different instant; only the timestamp belonging to the eventually successful
> atomic commit becomes canonical."

## G-086 — A full store rejects only new commits that cannot fit (WP04-CR-006)

> **Q:** WP04-CR-006: positions are capped at 2^53−1 (the shared integer domain). What happens when
> a new batch would exceed it?
>
> **A:** "Choose 1 — reject only new commits that cannot fit; committed retries remain
> replayable.For an unseen operation, a batch of K records may commit only when K <= (2^53−1) -
> current_tail. Otherwise the store returns persistence.store_full atomically, without sampling the
> clock, allocating positions, persisting a receipt, or writing any records. Positions never wrap,
> clamp, reuse, or partially append.Operation-idempotency resolution precedes the capacity check: an
> identical retry of an already committed operation always returns its original receipt and
> assigned positions, even when the store is now full; reuse of that identity with different
> content returns the existing operation-conflict result."

## G-087 — PERS-007 decomposed with explicit owners (Codex WP-04 review Q2)

> **Q:** Codex's Q2: PERS-007 also asks for reads by container (e.g. an episode) or by target, and
> for memory-bounded incremental rebuild (checkpoint plus tail). WP-04 provides raw since-boundary
> paging only. Where should the rest be handled?
>
> **A:** "Choose 1 — defer with explicit owners.WP-04 owns only the generic canonical-store part of
> PERS-007: bounded since-boundary paging over physical committed history.Memory-bounded incremental
> rebuild belongs to Layer 05 together with ReplayCheckpoint, checkpoint compatibility, and
> checkpoint-plus-tail projection.Container- and target-oriented reads belong to the profile layers
> that define those semantic concepts; any associated indexes are derived/rebuildable read models
> rather than canonical-store semantics.Record all three dispositions explicitly in the
> requirement/feasibility matrix so PERS-007 is decomposed rather than left partially satisfied."

## G-088 — Route after convergence trigger A on WP04-CR-008

**Context.** WP04-CR-008 survived Codex's Python implementation reviews `bb3dfa2c` and `391fca64`.
After the first remediation, two incompatible schemas still pass open: an `UNLOGGED` records table,
and a non-deterministic collation on `store_id`. WP04-CR-009…011 are resolved.

> **Q:** Convergence trigger A has fired on WP-04 (WP04-CR-008 survived two independent reviews). My
> schema check at open matches column and constraint shapes, but Codex showed two incompatible schemas
> that still pass: an UNLOGGED records table (not crash-safe, so the durability barrier is void) and a
> non-bytewise collation on store_id (two distinct IDs collide). The other three findings are
> resolved. Per our workflow, convergence is the default; a targeted fix needs an explicit reason. How
> should WP-04 proceed? (Either route waits for the Minion-Agent host reservation before new test
> batches.)
>
> **A:** "Narrow convergence (Recommended)" — the selected option read: "As G-038: a convergence
> episode limited to the v1 catalog trust boundary (which catalog properties v1 durability and
> identity depend on: persistence, collations, indexes, triggers, rules, inheritance, generated
> columns, etc.). Codex characterizes it, I classify, Codex approves the checkpoint, I implement once,
> Codex closes. CR-009..011 stay closed."

## G-089…G-092 — CE-04-01 candidate path-C items C01, C04, C05, C06

**Context.** Codex's CE-04-01 characterization (`assurance/convergence/CE-04-01-characterization.md`,
`0f7ac1bf`) offered six candidate path-C items. Claude discharged C02 (namespace binding) and C03
(privileges) by authority reading, subject to Codex's checkpoint review, and put the other four to the
Owner in one question set. The answers below are the Owner's typed text, verbatim.

### G-089 — C01 — acceptance envelope of an existing v1 schema

> **Q:** WP-04 CE-04-01 (C01): when an existing mneme_ schema differs from what v1 initialization creates, but the difference can't break any guarantee (e.g., an extra plain index, a fillfactor, a renamed constraint), what should open do? Codex showed many differences that DO break guarantees (unlogged tables, rules, triggers, row security, nondeterministic collations, generated columns, expression indexes that reject valid IDs).
>
> **A:** Selected "Exact v1 only (Recommended)", with the Owner's text: "Choose 1 — v1 open() accepts only the finite catalog contract produced by the certified v1 initializer, modulo explicitly non-semantic catalog identity such as names, OIDs, ownership/grants, column order, dropped-column residue, and planner statistics.The validator must check all catalog properties capable of changing durability, visibility, accepted writes, identity/equality, uniqueness, append semantics, or transaction behavior, including relation persistence/kind, inheritance, RLS/policies, rules, triggers, access method/options, column type/collation/default/generated/identity properties, constraints, and the exact constraint-backed index semantics.Additional indexes or physical tuning are not implicitly tolerated in v1. If a later operational need justifies specific variations, add them through an explicit reviewed catalog-contract revision rather than an open-ended semantic-equivalence rule."

### G-090 — C04 — reference database environment at open

> **Q:** C04: the contract says reference databases are created UTF8 with C/C collation. Should open enforce that? (Today a SQL_ASCII database initializes, then refuses its own schema on the next open; a LATIN1 one works.)
>
> **A:** Selected "Enforce at open (Recommended)", with the Owner's text: "Choose 1 — enforce the reference database environment at every v1 open().Before accepting or creating the Mneme schema, open() MUST verify that the current PostgreSQL database uses UTF8 encoding and that both LC_COLLATE and LC_CTYPE are C or the equivalent POSIX. Any mismatch returns persistence.schema_incompatible and performs no durable schema/store mutation.The connection MUST also establish UTF8 client encoding itself rather than relying on ambient client settings. These checks are part of the finite v1 storage trust boundary, not merely deployment advice. No new normative error code is required."

### G-091 — C05 — supported PostgreSQL versions and structured comparison

> **Q:** C05: which PostgreSQL versions does the reference backend support? Only 14.12 has been executed, and the current check compares PostgreSQL's rendered constraint text, which varies by release (and already falsely refuses a valid schema under quote_all_identifiers).
>
> **A:** Selected "PostgreSQL 14 only (Recommended)", with the Owner's text: "Choose 1 — the reference PostgreSQL backend supports major version 14 only for v1. open() MUST reject every other server major with persistence.schema_incompatible before performing any durable change. Current certification evidence is explicitly pinned to PostgreSQL 14.12; the contract supports 14.x rather than claiming untested later majors.Catalog validation MUST use structured PostgreSQL catalog properties rather than rendered constraint/index SQL, so presentation settings such as quote_all_identifiers and semantically irrelevant formatting cannot alter acceptance. Adding another PostgreSQL major is a reviewed backend-compatibility delta requiring its own characterization and cross-platform evidence."

### G-092 — C06 — trust scope of the v1 guarantees

> **Q:** C06: what trust scope do the v1 guarantees assume? Open can only check the schema at open time; it can't stop an administrator changing the schema or editing rows later, and some broken states (disabled FK triggers, catalog edits) need superuser.
>
> **A:** Selected "Open-time, trusted engine (Recommended)", with the Owner's text: "Choose 1 — v1 uses an open-time validated, trusted-engine model.open() verifies the PostgreSQL environment and the complete certified v1 catalog contract before returning a usable store handle. Thereafter, WP-04 guarantees assume that the mneme_ schema and canonical rows are modified only through the certified Minion-Memory API and that PostgreSQL's genuine catalog/transaction semantics remain trustworthy.Out-of-band DDL, direct row edits, disabled internal constraints/triggers, manual catalog manipulation, and other administrator/superuser interference after open() are outside the certification boundary. The store does not revalidate the full schema on every operation or scan all historical rows at open.A later integrity-check/repair facility may explicitly audit stored data, but it is a separate capability and does not alter the v1 trust model."

## G-093 — CE-04-01 gates under the Minion-Agent host reservation

**Context.** The CE-04-01 single implementation pass is committed at code `b657081b`. Its gates
(about 150 fresh-schema witnesses, the full suite, planted violations, coverage) are heavy disk work,
and Minion-Agent asked that heavy batches wait for "host clear" while its Rust gates (#199) run.

> **Q1:** How should I proceed?
>
> **A1:** "Choose 1 — wait for host clear.Preserve the shared-host reservation. CE-04-01 moves to WAITING_FOR_TRIGGER with trigger host clear; do not start the ~150 fresh-schema witnesses, full suite, mutation batch, or coverage until the reservation is released. Use the wait to finalize the implementation record, exact gate commands, mutant/witness map, expected evidence format, and Rust handoff notes. Once host clear arrives, run the full declared gate set fresh at code b657081b and bind all evidence to that exact SHA."
>
> **Q2:** The validator rejects CONTRACT_CONVERGENCE -> WAITING_FOR_TRIGGER (and that state can only
> resume into SCOPING). How should I record the wait?
>
> **A2:** "Choose 1 — remain in CONTRACT_CONVERGENCE. Do not transition state. Record next_owner = Claude, bind the pending CE-04-01 gates to candidate b657081b, and add an explicit execution condition that the heavy gate batch may begin only after Minion-Agent reports host clear. This is an operational scheduling condition, not a workflow-state change or Owner blocker."

A2 refines A1's state wording; the status stays `CONTRACT_CONVERGENCE`.

## G-094…G-097 — CE-04-01 extension: candidate path-C items EC01…EC05

**Context.** Codex's closure review (`779a8f21`) found WP04-CR-012 and WP04-CR-013. Its
characterization extension (`d8262cf5`, 112 executed rows and an 85-row omitted-field inventory)
raised the packet EC01…EC05. Asked on 2026-10-12, after Codex finished, with the Owner's answers
recorded verbatim.

### G-094 — EC01 — outside objects that depend on the v1 tables

> **Q:** Outside objects that depend on the four mneme tables (views, matviews, owned sequences,
> publications, routines/aggregates/operators/casts/domains/ranges over a mneme row type, outside
> indexes/policies/defaults using a row type, extension membership). Today open accepts all of them.
> Which rule should open enforce?
>
> **A:** "Choose 1 — strict catalog closure.The PostgreSQL v1 backend accepts only the certified Mneme catalog dependency island. Except for explicitly exempt planner/extended-statistics objects and required pg_catalog/built-in dependencies, no object outside the v1 set may have a recorded catalog dependency on a v1 table, column, row/array type, index, constraint, or other certified object; conversely, no v1 object may depend on a user object outside the certified namespace.Any such edge yields persistence.schema_incompatible and open() performs no durable change. This includes views/materialized views, owned sequences, publications, functions/procedures/aggregates/operators/casts/domains/ranges involving Mneme row types, external policies/defaults/indexes, and extension membership.Dynamic SQL or other references with no PostgreSQL-recorded catalog dependency remain outside the v1 trust boundary under G-092. Future analytics/integration dependents require an explicit reviewed catalog-contract extension rather than an effect-based exception."

### G-095 — EC02 — row-type references in outside constraints

> **Q:** Does "No constraint outside the four tables references them" also cover outside constraints
> that reference a mneme row type (outside CHECK, domain CHECK, constraint-trigger WHEN)?
>
> **A:** "Choose 1 — row-type dependencies count as references to the Mneme table.The no-external-constraint rule covers not only direct relation-reference fields but also recorded dependencies on the table’s composite row type or array type. Outside CHECK constraints, domain constraints, constraint-trigger predicates, or equivalent catalog objects that depend on those types are incompatible with the v1 closed catalog island. Under EC01 strict closure, this is already implied; EC02 simply makes the constraint wording explicit."

### G-096 — EC03 — engine-maintained bookkeeping

> **Q:** Engine-maintained bookkeeping that changes under genuine operations (stale relhas* flags,
> relfrozenxid/relminmxid, relfilenode, indcheckxmin). How should open treat them?
>
> **A:** "Choose 1 — exempt engine-maintained bookkeeping from the v1 catalog comparison.open() does not compare cached relation flags such as relhasrules, relhastriggers, relhassubclass, or relhasindex; maintenance horizons such as relfrozenxid/relminmxid; physical identifiers such as relfilenode; or transient planner/MVCC safety state such as indcheckxmin. Instead it validates the authoritative catalog objects and semantic properties themselves.Genuine inconsistencies between those bookkeeping fields and PostgreSQL's authoritative catalogs fall under the trusted-engine/out-of-band corruption assumption in G-092 rather than becoming additional v1 schema predicates."

### G-097 — EC04/EC05 — comments and security labels

> **Q:** Annotations on v1 objects: COMMENT ON, and SECURITY LABEL (needs a superuser-installed
> provider). Neither is in G-089's exclusion list.
>
> **A:** Selected "Comments exempt, labels refused", with the Owner's text: "Choose 2 — comments are exempt; security labels are forbidden on v1 objects.COMMENT ON metadata is descriptive and does not alter certified store behavior, so comments join G-089's non-semantic exclusions.Any SECURITY LABEL attached to a certified v1 object causes persistence.schema_incompatible. Security labels are inputs to external security providers whose effects are outside the finite v1 catalog contract and cannot be reduced safely to ordinary PostgreSQL grant semantics. Supporting a specific provider such as sepgsql requires a separately reviewed backend-contract extension."
