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
