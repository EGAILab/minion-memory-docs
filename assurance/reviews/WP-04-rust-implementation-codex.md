# Rust Layer 04 implementation — Codex (WP-04)

**Status: ready for independent CLOSURE_REVIEW.** Author-run implementation evidence,
not independent approval or acceptance.

## Exact scope and authority

- Code candidate: `6ef220e5b4f48ea8d458ead2f30dfdfcf67cba3d`, branch `wp04/rust`,
  from accepted main `9d5a2d51c69987f799962868b8dc5175a11882d2`.
- Docs branch: `wp04/rust`, from reconciled coordinator main
  `42a7d4fa21528c5d7a489fc090d8b7c7e9c829b3`. Accepted content remains its ancestor
  `f887f6ac94973a9c2fa4f4413bc8b4a16b50acd8`; the intervening coordination records
  were imported by fast-forward. This implementation record is the only authored docs change.
- Authority: the accepted Layer 04 section of `spec/persistence.md`, its SER stage rows,
  HIST-008/009, G-077…G-098, G-013/G-031/G-033/G-051/G-054/G-055; the settled CE-04-01
  checkpoint revisions 2–5; `assurance/layers/04-feasibility-matrix.md` §3a; the shared
  `reference-backend/postgres14-v1-catalog.json`; and the five ACTIVE store scenarios.

The Rust SQL, catalog builder and protocol implementation were derived from that authority.
The Python implementation is used only as the other participant in interoperability tests.
The implementation notes' row layouts and the Codex characterization stimuli are reference
data, not a replacement oracle. No shared expectation, Python implementation, state file,
registry, source bundle or main branch is changed.

## Public binding and implementation

`minion_memory::persistence::PostgresHistoryStore::open(conninfo, clock)` creates a private
PostgreSQL connection. Its methods are `create_store`, `store_tail`, `commit_history` and
`read_history`. Each declared value argument accepts the certified native/text/UTF-8-byte
`Input` seams. The clock is `FnMut(&str) -> Value + Send`, sampled for the validated store ID.
There is no reconnect or automatic replay that could introduce another clock sample.

`StoreError::Validation` carries the stable code/argument and no entry position.
`Database` retains the genuine driver error. Invalid injected clock results and a handle
poisoned by a caller panic are binding failures (`Clock`, `Poisoned`), outside the store
value-error vocabulary. Dropping the handle closes its private connection.

The additive Layer 02 draft mode reuses the same four admission gates. It removes
`recorded_at` from the required and allowed caller members; a supplied value fails D3.
Replay admission retains its previous behavior. Visibility changes to existing typed helpers
are crate-private.

Generic stages run across all arguments before typed rules. Commit follows the specified
store/writer/operation/batch order, per-record draft gates in array order and in-batch ID
uniqueness before any database effect. Under the store-row lock it checks operation retry
identity against canonical normalized draft-array bytes, then persisted record IDs, then
capacity. Only then does it sample the clock once, stamp the normalized instant, insert the
consecutive records and original receipt metadata, advance the tail and commit durably.
The writer is not part of mutation identity. Operation IDs are exact UTF-8 `bytea`, including
NUL. Envelopes and mutations are canonical bytes, not server-reencoded text.

A handle mutex spans each whole transaction lifecycle. Independent handles serialize writes
through `SELECT … FOR UPDATE`. Writes explicitly use Read Committed/read-write, and reads
use one Repeatable Read/read-only snapshot. A page counts records and may slice a committed
batch; `through` is the last returned position, or the supplied boundary for an empty page.

The crate pins `postgres` 0.19.14 and uses its synchronous NoTls connection for the local
reference backend; TLS transport is not claimed by this binding. `regex` 1.13.1 performs only the
catalog expression-tree normalization. Existing content hashing, canonicalization, decoding
and timestamp seams remain library-owned. The full graph is locked in Cargo.lock.

## Catalog trust boundary and matrix §3a

Open begins explicitly in Read Committed/read-write. Its first statement obtains the shared
single-bigint advisory lock `-4695452043516644990`, held until commit/rollback. It then checks
major version 14, UTF8, C/POSIX and the resolved current schema. The handle pins client UTF8
and synchronous commit. A missing current schema remains a genuine engine error.

Initialization occurs only when there is no `mneme_` non-index relation. It pins storage
defaults, uses catalog-qualified declarations in the quoted concrete namespace, and checks
the complete catalog postcondition before commit. Otherwise comparison precedes checking
the single supported schema row. DDL and availability failures are never caught as schema
incompatibility.

`catalog.rs` embeds the exact shared pins. Its twelve structured parts retain row multiplicity
and compare in the checkpoint order. Expression locations are removed and attribute numbers
are normalized to names; rendered SQL is not an oracle. `index_columns` and all internal
members retain PostgreSQL's own `jsonb::text` documents. The whole-row exclusions are exactly
the named lists; G-098 type copies are checked against pg_type, and relation counts are
checked by invariant. New catalog columns cannot disappear silently: the live inventory test
checks every field against the member documents and exclusion list.

The island includes root relations, their indexes, TOAST relations/indexes, row/array types,
root constraints/defaults/triggers and subobjects by parent identity. Recorded crossing
dependencies and security labels are refused, with only the agreed namespace/builtin and
planner-statistics exemptions. The implementation does not scan stored rows or infer
unrecorded references, and does not extend open-time certification to later out-of-band edits.

| Obligation / witness kind | Rust evidence in `tests/layer04.rs` |
|---|---|
| [PIN] exact shared data, normative DDL and initializer | `normative_pins_initializer_and_embedding`: independently declared normative DDL equals every shared part; Rust initialization equals the same pins; embedded bytes equal the shared file |
| [P] relation/column/constraint/index properties and exemptions | `classified_public_catalog_witnesses`: 174 accepted checkpoint fixtures from Codex's own characterization stimuli; refusals are positionless schema errors; accepted cases perform real repository operations; catalog remains unchanged |
| [P] cached-value rewrite distinction | E004 has its own old-store oracle: existing tail 1, new range 2…3, identical retry; a separate new store executes protocol N. It is never credited as N on the rewritten old state |
| [P]/[Pr] environment | real SQL_ASCII throwaway DB refused; a LATIN1 client default is reset for Unicode roundtrip; major/encoding/collation/ctype predicate controls |
| [T] open ordering and initialization | granted=true single-bigint key observation; key independently re-derived with SHA-256; prefixed view/sequence/table/materialized-view partial schemas refused without initialization; waiting opener under Repeatable Read default |
| [E] genuine objects / private session | hostile ordinary namespace operator, function, relation and type names followed by public open and protocol; poisoned temporary catalog names passed through actual Rust fetch SQL; private sessions cannot inherit that caller session |
| [F] fetch-binding | actual catalog queries execute over projected source columns, not substituted normalized answers: root caches/type copies/flags, relation counts, internal trigger flag, index readiness, TOAST options/order and row-type input function; donor inheritance/policy/rule/index attachments; labels on root, attribute, TOAST and row type |
| [Pr] exact parts and whole-row fields | 1,097 independently changed pin cells plus missing/extra rows and part inventory; 893 individually changed whole-row properties, re-rendered by PostgreSQL with a no-op rendering identity check |
| [INV] every live field | PostgreSQL 14 layouts: pg_class 33, pg_index 20, pg_attribute 26 and pg_type 32 fields; each member field compared or explicitly excluded, never both |
| [CT] transaction and read ordering | six pre-opened writers × ten two-record commits, exact union 1…120; eight same-handle identical retries; five conflicting writers with exactly one winner; gated clock and mixed handle operations; killed transaction/invalid clock consume nothing; snapshot reads during 35 two-record commits and record-counted pages |
| [IT] shared backend | both initializer directions and both writer directions; byte-exact mutation/envelope storage, normalized native/text retries, Unicode/large payload/NUL operation ID; mixed-language waiting concurrent first opens under Repeatable Read session defaults and a mixed identical-operation race |

Pure predicate and projected-field executions are explicitly labelled [Pr] and [F]. They are
not physical catalog mutations or public-open executions. The non-constructible other-
tablespace CH11 case is not claimed: only the project E: tablespace is used. Its reltablespace
predicate is tested. The synthetic MAX-tail capacity fixture is an isolated algorithm control,
not a claim about an ordinary reachable gapless history.

## Canonical runner and traceability

The runner delegates all four store operations to the real public library. Its backend/clock
map supplies test configuration only. The clock fixture for a successful JSON-only create is
bound using the library-decoded store ID, after the actual create succeeds. Raw `<name>_json`
strings are passed through untouched; it does not implement admission, stamping, retry,
position allocation, paging, normalization or error selection.

Rust declares `IMPLEMENTED_LAYER = 4`. DRAFT/higher-layer/placeholder rules and dynamic
promotion controls are retained. The suite discovers **22 ACTIVE scenarios / 408 steps**, with
**4 explicit placeholder xfails**; all five Layer 04 scenarios' **65 steps** execute. Corpus
bytes and expectations are unchanged. Rust manifest locations are added for HIST-008/009 and
PERS-005/006/007/008/012/014/015.

## Gates and execution status

GATE: G3 — first Rust CLOSURE_REVIEW, including certified lower-layer regressions.

Both platforms passed at exact code `6ef220e5b4f48ea8d458ead2f30dfdfcf67cba3d`, with
Rust/Cargo 1.97.1, fresh sources, separate project-local targets and at most four Cargo jobs:

| Gate | Windows | POSIX / case-sensitive Linux |
|---|---|---|
| `cargo fmt --check` | PASS | PASS |
| `cargo clippy --locked --offline --workspace --all-targets -- -D warnings` | PASS | PASS |
| `cargo test --locked --offline -- --nocapture --test-threads=1` | 64 integration tests + 1 doctest passed | 64 integration tests + 1 doctest passed |
| Canonical corpus | 22 ACTIVE / 408 steps / 4 explicit placeholder xfails | Same |
| `cargo doc --locked --offline --no-deps`, `RUSTDOCFLAGS=-Dwarnings` | PASS | PASS |
| Planted violations | 30/30 compiled runtime kills | 30/30 compiled runtime kills |
| Restored Layer 04 baseline after controls | 23 passed | 23 passed |

Every intended control observer has a passing baseline. The catalog, transaction and
cross-language witnesses above executed on both platforms. The Linux run is client-platform
evidence against the same PostgreSQL 14.12 server, as qualified below.

The initial mechanical check on the stale docs baseline passed 7/8 and failed state checks;
it is not credited. Claude reconciled main to `42a7d4fa`, with RUST_IMPLEMENTATION and no
current candidate. After importing that coordinator baseline, the deep-source mechanical
check passed **8/8** (`process-check-reconciled.log`), without author edits to state or registry.

No Rust numeric coverage percentage is claimed. The workflow's numerical coverage floor
applies to Python. Rust certification evidence is the complete suite, canonical integration,
strict all-target clippy, formatting, warning-free public docs and discriminating controls.

## Planted violations and evidence limits

| IDs | Planted wrong implementation | Intended observer |
|---|---|---|
| M01–M02 | omit empty-batch / in-batch duplicate rejection | draft gates before missing-store lookup |
| M03–M05 | omit mutation conflict / persisted ID checks; reject the last available position | capacity, retry, conflict and clock-order control |
| M06 | rollback while returning a successful receipt | normative initializer's real read after commit |
| M07 | remove the store-row lock | pre-opened concurrent writers' gapless union |
| M08 | read separate Read Committed snapshots | concurrent page entries disagree with returned tail |
| M09 | omit exact supported version-row check | public open on version 2 / empty header |
| M10–M11 | wrong shared key; Repeatable Read open | derived-key assertion; real waiting-opener initialization |
| M12–M16 | hardcode offset cache, type-copy consistency or trigger internal flag | source-field projection through actual fetch SQL |
| M17–M28 | omit each of the twelve comparison parts | isolated changed-cell / row-multiplicity predicate observers |
| M29–M30 | admit a later major version / wrong database encoding | environment predicate controls |

Compilation errors never count as kills. Twelve part-omission kills are [Pr] witnesses, not
claims of public false passes through overlapping catalog parts. This is a Rust replay of its
own variants, not a replay/credit of Claude's Python mutant counts. No new equivalence claim
is used to close a survivor.

The development pass corrected its own absent-reference vector rendering (`null` → `[]`),
explicit read-write settings, and fixture transport/setup issues (Windows Python stdin UTF8;
S10/V01 description text replaced with executable session/version observations). Failed
development runs are not submitted as gate evidence. The accepted expectations did not change.

## Reproduction and handoff

Own drivers/logs: `.tmp/work/codex/wp04-rust/`:

- `windows-gates.py`, `windows-gates.log`, `windows-gates.json`;
- `controls.py`, `resume-windows/windows-controls.json`, per-variant logs and restored baseline;
- `linux.sh`, `run-linux.py`, `linux-gates.py`, `linux-full.log`, test/doc/control logs;
- `reverse-relay.py`: owned relay processes shut down through a stop-file protocol, with no OS
  signals; its credential copy is removed after use.
- `cleanup-audit.py`, `cleanup-audit.log`: final exact-owned-database cleanup and inventory;
- `process-check-reconciled.log`: all eight mechanical checks against the reconciled baseline.

Windows/Linux Cargo targets and dedicated controls targets are under
`.tmp/cache/cargo-target/wp04-rust-{windows,linux,controls-windows,controls-linux}`.
Cargo homes, Rustup's Linux home, images, sources, Python, all temporary paths and databases
are project-contained. Only the ordinary mneme_dev role and the E: mneme_ts tablespace are
used; owned throwaway databases are dropped after each run. The POSIX source archive lives
on an E:-backed ext4/FUSE image, with distinct A/a proof files. Its PostgreSQL engine is the
same Windows PostgreSQL 14.12 server through the relay: Linux-client evidence is not a claim
of a Linux PostgreSQL server run.

The final cleanup audit found one SQL_ASCII auxiliary database left by a best-effort fixture
destructor. It was dropped explicitly using the ordinary project role; the final owned
database inventory is empty. This cleanup correction was reported to the host scheduler.
Fixture destructor success alone is not credited as cleanup evidence.

The resumed host reservation runs batches sequentially with at most four Cargo jobs and no
Agent targets, target cleaning or OS signals. All native batches have ended and BATCH-DONE
was reported; the reservation is released. No contract gap or surviving planted violation
remains from this implementation pass. The exact pair is offered for independent
CLOSURE_REVIEW; no candidate approval or acceptance is asserted.
