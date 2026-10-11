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
