# Minion-Memory — Cross-language hazard families

**Status:** PROPOSED (WP-00), pending independent review.
**Adapted from:** Minion-Agent `process/hazard-families.md` @ `8744bd0`. Minion-Agent's families
are JavaScript-runtime-derived (F1 JS Number, F2 UTF-16, F6 ECMAScript object order, F7 schema
runtime domain) because Pi is a TypeScript reference. Mneme has no reference runtime: the hazard is
Python ↔ Rust ↔ serialized-artifact agreement. The families below keep Minion-Agent's *method*
(pre-enumerated members, neighborhood expansion, AUDITED / NOT_APPLICABLE / DEFERRED_WITH_REASON)
and re-derive the *members* for Python/Rust/JSON/YAML/SQLite.

**Rules** (adopted): when a WP's semantic path touches a family, its feasibility matrix lists every
member; when a finding hits one member, the whole family is characterized before remediation; a new
generalizable hazard is added here as part of that finding's remediation. Families are probe
inputs, never semantic authority. Every premise about a library/engine is verified by an executed
probe at the pinned toolchain, not from documentation (agent-workflow §5).

## H1. Integers and floats

| Member | Probe |
|---|---|
| integer width | Python `int` is unbounded; Rust needs a declared type (i64/u64/...). Values beyond 2^53 in JSON; beyond i64; negative where unsigned is assumed |
| JSON number lexical forms | `1`, `1.0`, `1e3`, `-0`, leading zeros, very long mantissas: which are integers? |
| float policy | NaN, ±Infinity (not JSON), `-0.0`, rounding of decimal literals (e.g. importance `0.30`), equality/hash of floats |
| arithmetic | integer division/rounding direction, overflow (Rust panics/wraps in debug/release), float formatting round-trip |
| SQLite affinity | INTEGER vs REAL storage of the same value; 64-bit limit |

## H2. Strings and Unicode scalars

| Member | Probe |
|---|---|
| scalar domain | Python `str` can hold lone surrogates (`"\ud800"`); Rust `String` cannot. JSON `"\ud800"` escapes decode differently |
| encoding | UTF-8 only on disk; invalid bytes; BOM at file start |
| NUL | `"\u0000"` in text, in SQLite TEXT, in paths |
| length units | code points vs UTF-8 bytes vs UTF-16 units vs grapheme clusters — budgets and truncation (PROJ-003) depend on the unit |
| line endings | `\r\n` vs `\n` in Markdown/package content and hashed text (Windows checkouts, `core.autocrlf`) |

## H3. Unicode semantics

| Member | Probe |
|---|---|
| normalization | NFC/NFD of equal-looking text; normalization before hashing/matching (CORE-011, EVAL normalized match) |
| case mapping/folding | locale-free full case folding (`ß`, `İ`), Python `casefold` vs Rust `to_lowercase` |
| collation / sort | byte order vs code-point order vs locale collation for any deterministic ordering |
| Unicode version | Python's `unicodedata` version vs Rust crate data version; characters newer than one of them |
| lexical tokenization | word boundaries for FTS/lexical retrieval differ by engine |

## H4. Time

| Member | Probe |
|---|---|
| representation | RFC 3339 string vs epoch integer; mandatory offset/`Z`; precision (s/ms/µs/ns) and truncation vs rounding |
| unknown vs present | missing `occurred_at` stays unknown (SER-003), never "now" or epoch 0 |
| clocks | wall clock vs monotonic; clock going backwards; device clock skew (offline-first) |
| ordering | `occurred_at` never defines semantic order (HIST-003); ties |
| leap seconds / DST | parsing `23:59:60`; local-time inputs |

## H5. Ordering and collections

| Member | Probe |
|---|---|
| map iteration | Python dict insertion order vs Rust `HashMap` (random) vs `BTreeMap` (sorted) in any observable output |
| canonical key order | serialization and hashing of objects (sorted? by what comparison?) |
| sort stability and keys | ties; multi-key precedence; ≥2 discriminating entries in evidence |
| sets | observable order of set-valued outputs (scope facets, selected records) |
| pagination | stable cursor under concurrent append; page boundary at ties |

## H6. YAML/JSON parsing

| Member | Probe |
|---|---|
| YAML version | YAML 1.1 (PyYAML) vs 1.2 (Rust crates): `yes/no/on/off`, `2026-10-09`, `010`, `1_000`, `0x1F`, `~` |
| duplicate keys | last-wins silently (PyYAML, serde_json) vs error |
| anchors/aliases/tags/merge keys | supported unequally; alias bombs |
| big numbers | YAML/JSON integers beyond i64 |
| null vs missing vs empty | `key:` vs absent key vs `""` vs `[]` |
| enforcement | `mneme-process` loads every canonical/governance YAML through the YAML-1.2-core boundary and rejects any document whose YAML 1.1 reading differs |

## H7. Hashing and canonical bytes

| Member | Probe |
|---|---|
| algorithm and output | SHA-256 assumed by tooling; contract algorithm unspecified (NF-013); hex case |
| canonical form | which bytes are hashed: canonical JSON (key order, number form, escaping), normalized text, line endings |
| identity vs integrity | a content hash is integrity, never identity (CORE-001, CORE-013) |

## H8. Persistence and transactions

| Member | Probe |
|---|---|
| SQLite version and options | Python stdlib `sqlite3` links the platform/CPython build (3.45.3 observed on 3.12.8 Windows); Rust `rusqlite` usually bundles its own — feature/behavior drift |
| isolation and locking | implicit transactions in Python `sqlite3` (legacy `isolation_level`) vs explicit in Rust; WAL vs rollback journal; busy timeouts |
| crash points | crash after append before cache update (PERS-005); torn asset writes (PERS-016) |
| idempotency | unique constraint on operation identity; retry after commit returns the prior result (PERS-006) |
| JSONL backup | line framing, trailing newline, embedded newlines, partial last line |

## H9. Paths and filesystem

| Member | Probe |
|---|---|
| separators/drive letters/UNC | Windows vs POSIX in package-relative references |
| traversal | `..`, absolute paths, symlinks escaping the package root (PKG-003) |
| case sensitivity | NTFS case-insensitive vs Linux case-sensitive collisions |
| reserved names/length | `CON`, trailing dots/spaces, 260-char limits |
| atomic rename | rename-over-existing semantics differ on Windows |

## H10. Concurrency and retry

| Member | Probe |
|---|---|
| concurrent same-operation retry | two in-flight commits with one operation identity |
| async enrichment vs canonical commit | enrichment observing uncommitted state; enrichment failure after commit (ACAP-005) |
| single-writer assumption | second writer present (PERS-015) |
| cancellation | cancel between durable commit and acknowledgment |

## H11. Identifiers and structured scope

| Member | Probe |
|---|---|
| ID lexical domain | allowed characters, length, case sensitivity, Unicode in IDs (NF-010) |
| version domain | integer edition vs semantic-version string; comparison (NF-011) |
| scope encoding | facet names/values, ordering of facets, empty vs absent facet, canonical encoding for equality/hashing (NF-018) |
| reference integrity | dangling references across profiles; retired targets (CORE-009) |
