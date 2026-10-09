# WP-00 — Cross-language hazard inventory (kickoff §23)

**Author:** Claude. **Scope:** bootstrap inventory, not a WP feasibility matrix. Each WP that owns a
surface fills `process/templates/cross-language-feasibility-matrix.md` with executed probes.
**States:** `AUDITED` (examined in WP-00 with evidence), `NOT_APPLICABLE`, `DEFERRED_WITH_REASON`
(reason + owning layer). Families: `process/hazard-families.md`.

**Toolchain facts observed (probe, 2026-10-09, Windows 11):** Python 3.12.8 (uv-managed interpreter
at `E:\AI\Python\Python312`), stdlib `sqlite3` → SQLite 3.45.3; Rust 1.97.1 / Cargo 1.97.1; uv 0.10.9;
git 2.55.0.windows.1. Rust SQLite version: not probed (no Rust crate yet; Codex records it).

| Row | Family | State | Evidence / reason |
|---|---|---|---|
| IDs | H11 | DEFERRED_WITH_REASON | No lexical domain in sources (NF-010). Layer 01 contract. |
| versions | H11 | DEFERRED_WITH_REASON | Integer edition vs "semantic version" (NF-011). Layer 01. |
| null / missing / unknown | H6, SER-003 | DEFERRED_WITH_REASON | Sources require missing = unknown, never defaulted; encoding of "unknown" vs JSON null vs absent key is a Layer 01 serialization decision. |
| integers | H1 | DEFERRED_WITH_REASON | Python unbounded vs Rust fixed width; sequence numbers, counts, timings (`response_time_ms`). Layer 01 value domain (NF-019). |
| floats | H1 | DEFERRED_WITH_REASON | Importance (`0.30`), quality/confidence values; NaN/Inf policy. Layer 01 (NF-019). |
| hashing | H7 | DEFERRED_WITH_REASON | Algorithm + canonical bytes unspecified (NF-013). Layer 01. Tooling-only use of SHA-256 for bundle provenance is AUDITED (validator `sources` check). |
| JSON/YAML | H6 | **AUDITED** | PyYAML resolves YAML 1.1 (`yes`→bool, `2026-10-09`→date, `010`→8); Rust crates resolve 1.2. WP-00 enforces a YAML-1.2-core profile that rejects any document whose 1.1 reading differs, plus duplicate keys, anchor/alias/tag syntax at the token level (remediation 1, WP00-CR-005), surrogate code points (explicitly, not via PyYAML incidental behavior), non-finite floats (`process/tools/src/mneme_process/yamlcore.py`; 15 parametrized unit witnesses + 2 corpus negative controls in `tests/`). The Rust runner must load with an equivalent profile (Codex to confirm in its first Rust pass). |
| Unicode | H2, H3 | DEFERRED_WITH_REASON | Lone surrogates representable in Python `str`, not Rust `String`; normalization for matching/hashing; casefold differences. Layer 01 value domain + Layer 09 evaluators. |
| Markdown/text | H2 | DEFERRED_WITH_REASON | Package unit Markdown and line endings (CRLF on Windows checkouts) matter for content hashes. Layer 07/12. Repos set `.gitattributes` `* text=auto eol=lf` now (AUDITED for the corpus). |
| timestamps | H4 | DEFERRED_WITH_REASON | Representation/precision/offset unspecified (NF-015). Layer 01. |
| occurred_at vs recorded_at | H4 | DEFERRED_WITH_REASON | Distinct by contract (HIST-004); encoding with the timestamp decision. Layer 01/02. |
| event sequence | H5 | DEFERRED_WITH_REASON | Per-container deterministic sequence (HIST-003); durable append order vs "no global order" (NF-016). Layer 02. |
| operation_id | H10, H11 | DEFERRED_WITH_REASON | Domain + conflicting-retry semantics open (NF-014). Layer 01/04. |
| transactions | H8 | DEFERRED_WITH_REASON | Python `sqlite3` implicit transaction behavior vs Rust explicit; isolation; Layer 04 probes on pinned versions. |
| crash recovery | H8 | DEFERRED_WITH_REASON | Append-then-cache crash point (PERS-005), torn asset writes (PERS-016). Layer 04. |
| MemoryScope | H11 | DEFERRED_WITH_REASON | Semantics and canonical encoding unspecified (NF-018). Layer 02, likely Owner decisions. |
| append-only reinterpretation | H5 | DEFERRED_WITH_REASON | Supersession chains and "current preferred" projection ordering. Layer 03. |
| checkpoints | H7, H11 | DEFERRED_WITH_REASON | Dependency-boundary encoding and compatibility comparison. Layer 05. |
| bounded replay | H5 | DEFERRED_WITH_REASON | Bounded == full replay equivalence (PERS-007). Layer 04/05. |
| pagination | H5 | DEFERRED_WITH_REASON | Stable cursors under append; ties. Layer 04/06. |
| JSONL backup | H8 | DEFERRED_WITH_REASON | Framing, trailing newline, partial last line; profile/type identity (BKP-004). Layer 12/17. |
| SQLite | H8 | DEFERRED_WITH_REASON | Version drift between Python's linked SQLite (3.45.3 observed) and Rust's bundled one; production schema out of WP-00 scope. Layer 04. |
| paths | H9 | DEFERRED_WITH_REASON | Package-relative refs, traversal rejection (PKG-003), Windows/POSIX. Layer 12. Tooling paths AUDITED only for the validator (POSIX-style relative paths, `Path` resolution). |
| concurrency | H10 | DEFERRED_WITH_REASON | Single-writer assumption (PERS-015); concurrent same-operation retry; async enrichment (ACAP-005). Layer 04/13. |
| provenance/reference integrity | H11 | DEFERRED_WITH_REASON | Dangling/retired references (CORE-009), cross-profile references. Layer 01/02. |

**Verdict for WP-00:** every row has a state; no row is `NOT_APPLICABLE` silently. The deferred
rows are the input checklist for the WP-01 feasibility matrix (`plans/WP-01-proposal.md`).
