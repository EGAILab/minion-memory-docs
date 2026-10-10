# Cross-Language Feasibility Matrix — WP-01: Core identity, versions, canonical bytes, value domain

**Template:** `process/templates/cross-language-feasibility-matrix.md`.
**Status:** current for the final Layer 01 contract (Owner decisions G-012…G-043), revised for
WP01-CR-009 after Codex's final complete review (`e340e439`).

**Checkpoints:**
- contract review `154b4164`;
- deltas `2f50acc0`;
- native-binding convergence CE-01-01 agreed `1d99bc2c`, closed `dc9f9aaa`.

**Python implementation:** `minion_memory.core`. **Rust:** not started; this matrix is its
readiness guidance.

**Historical evidence:** `assurance/layers/01-probes/`. Those transcripts keep their original
meaning; their current interpretation is stated here.

## 1. Value-domain and binding matrix

| Value / seam | Contract domain | Python binding (implemented) | Rust requirement | Canonical form | Lossless? | Evidence |
|---|---|---|---|---|---|---|
| number (one kind) | finite binary64; every integral value within ±(2^53−1) whatever its spelling; −0 → 0 (SER-008; G-016, G-017, G-023, G-025) | numeral token kept as text through stage 1, then `float(text)` (nearest binary64, ties to even) and the integral check; native integers exact | **defer numeric interpretation until stage 2** (see §2), then checked integrality with a normalized `f64` or checked safe integer; `serde_json::Number`'s int/float tag never decides validity or equality | ECMAScript shortest form | YES: every admitted integral value is exact in binary64 | scenarios `canonical-bytes-and-content-hash`, `portable-value-domain-rejections`; Codex: 60,000 samples match Node `JSON.stringify` |
| string | Unicode scalar values | escaped lone surrogate is a stage-1 error in JSON text; raw surrogate is `value.invalid_json`; a native surrogate is a stage-2 error | `String` cannot hold surrogates, but an escaped lone surrogate must map to `value.lone_surrogate` at its source position, not to a generic parse error | RFC 8785 escaping | YES | scenarios; WP01-PY-003 controls |
| object member names | unique after escape decoding (JSON text) or as base strings (native, G-039); ordered by UTF-16 code units | duplicate detected at the second occurrence in source order; native duplicates detected while ordering a map | duplicate-aware structural decoding **before** any map is built; UTF-16 code-unit ordering (not code point) | RFC 8785 member order | YES with both | serde_jcs code-point order fails the `｡` vs `😀` case (Codex `e340e439`) |
| arrays | ordered sequences | `list` and `tuple` (G-036); no other sequence or iterable | natural ordered types (`Vec`, slices, arrays) bind to one array kind (G-036) | JSON array | YES | G-036 controls |
| native subclasses | admitted families read by base semantics only, no user hooks, exact built-in returns (G-037, G-042) | genuine-ancestry `issubclass(type(x), base)`; extraction via base slots to exact built-ins | the Rust native seam binds its own types; there is no analogue of Python subclass dispatch, but values returned to callers must be plain portable values | — | YES | CE-01-01: 25,470/25,470 rows, zero hooks |
| cycles / shared references | cycles `value.cyclic`; shared acyclic references legal (G-040) | active-path identity tracking | needed only if the Rust seam accepts shared or reference-counted graphs; otherwise unrepresentable | — | — | CE-01-01 boundary rows |
| byte and control inputs | byte buffers read as underlying bytes; JsonText as stored text; argument maps dict-only, else `TypeError` (G-041, G-043) | base-protocol reads; slot-stored `JsonText` | `&[u8]`/`Vec<u8>` and `&str` seams; no hookable wrappers | — | YES | CE-01-01 controls |
| version | positive integer edition 1…2^53−1 (G-012); `2.0` is edition 2 (G-023) | typed rule after stages 1–2 | same; typed rule after generic stages | number | YES | `version-integer-edition-ordering` |
| stable ID (CORE-001) | lowercase portable ASCII token, 1–128 bytes, no trailing `.`, no Windows device basename (G-020) | grammar plus device check | same grammar | bytes as given | YES (ASCII) | `stable-id-lexical-domain`; Codex: 5,000 generated tokens |
| operation identity (CORE-012) | `{source_namespace, source_operation_id}`; 1–256 UTF-8 bytes; exact comparison (G-032, G-033) | two exact strings | two `String` fields; no normalization | object with two members | YES | `operation-identity-namespaced-pair` |
| revision record (CORE-003) | closed `{stable_id, projection, artifact_version?}`; shape before fields (G-035) | `artifact.revision_invalid`, then canonical-order typed fields | same | — | YES | `identity-same-version-different-content-conflicts` |
| timestamp (HIST-004) | required input grammar (case, offsets, 0–6 fraction digits); local and UTC instants within 0001–9999; canonical `…ffffffZ` (G-022, G-026, G-028–G-030) | contract grammar, then `datetime` arithmetic over 1–9999 | contract grammar in front of any time library (chrono accepts year 0 and extended years); `i64` epoch µs | canonical string | YES: −62135596800000000…253402300799999999 µs fits `i64` but **not** a JSON number | `01-probes/timestamp-domain.md`; Codex: 5,000 generated inputs |
| content hash | SHA-256 lowercase hex of canonical bytes; raw content hashed over bytes as given (G-014) | `content_hash`, `raw_content_hash` | `sha2` | 64 hex characters | YES | scenario `raw-content-hash` |

## 2. Lower-layer capability matrix

| Operation | Seam | Python | Rust requirement |
|---|---|---|---|
| decode JSON text (stage 1) | public payload seam | strict iterative RFC 8259 parser; first violation in source order; numerals kept as text | **staged decoding:** structural parse (syntax, escaped surrogates, duplicates in source order) must complete before any numeric conversion can fail. **Witness:** `{"a":1e400,"b":1,"b":2}` must be `value.duplicate_key`. Eager `serde_json` decoding fails first with "number out of range" at the first numeral, and mapping that to `value.number_not_finite` would report a stage-2 error. A duplicate-aware visitor over the same eager numeric decode does not fix this (Codex `e340e439`). |
| validate generic domain (stage 2) | all seams | canonical traversal over exact values | canonical traversal (G-034); host map order never observable |
| canonicalize / hash | SER-009 | own RFC 8785 serializer (UTF-16 order, ECMAScript numbers) | own conformant serializer, or a verified one; `serde_jcs` 0.1 unchanged fails UTF-16 ordering |
| typed rules (stage 3) | primitives | after stages 1–2 over all arguments | same precedence across arguments (G-031) |

## 3. Hazard checklist

| Hazard | State | Evidence / reason |
|---|---|---|
| H1 integer width / float specials | AUDITED | one numeric kind; whole-number bound after rounding; overflow, underflow and subnormal; staged decoding |
| H2 scalar domain / encoding / line endings | AUDITED | surrogates (escaped, raw, native); raw content hashed as given |
| H3 Unicode normalization | AUDITED | never applied to IDs, operation identities or hashed content |
| H4 time | AUDITED | contract grammar, range and overflow (G-028–G-030); `i64` µs domain probe |
| H5 key order | AUDITED | UTF-16 order; serde_jcs divergence fixtured |
| H6 YAML/JSON | AUDITED | corpus gate (aliases, YAML-1.2-core ambiguity) |
| H7 hashing | AUDITED | SHA-256 over JCS bytes; raw-content scenario |
| H8–H10 | NOT_APPLICABLE | no persistence, paths or concurrency in Layer 01 (operation-identity behaviour is Layer 04) |
| H11 identifiers | AUDITED | G-020 token; G-032 pair kept separate from stable IDs |

## 4. Concurrency / order

NOT_APPLICABLE: pure functions. Error selection is deterministic: stage precedence across all
arguments (G-031), canonical within-stage order (G-034), and source order for JSON-text stage 1.

## 5. Verdict

```text
FEASIBILITY
    FEASIBLE  for the final Layer 01 contract (G-012..G-043). Rust requires: staged JSON decoding
              (numeric interpretation deferred past structural stage 1), a UTF-16-ordered RFC 8785
              serializer (serde_jcs 0.1 is not usable unchanged), the SER-008 stage checks, and the
              HIST-004 grammar in front of any time library.
```
