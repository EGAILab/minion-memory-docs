# Cross-Language Feasibility Matrix — WP-01: Core identity, versions, canonical bytes, value domain

**Template:** `process/templates/cross-language-feasibility-matrix.md`. **Status:** DRAFT, revised
after Codex contract reviews 1 (`2b388e62`) and 2 (`1d25e434`), for re-review.
**Authority bundle:** `mneme-v2.3-dual-profile`; **Owner decisions:** G-012…G-034.
**Author:** Claude. **Independent checkpoint reviewer:** Codex.
**Toolchains probed:** CPython 3.12.8 (project-local); rustc 1.97.1; `rfc8785` 0.1.4 (Python
reference); `serde_jcs` 0.1.0 and `serde_json` 1 (Rust, off-the-shelf); dependency-free Rust `i64`
civil-time arithmetic. Evidence: `assurance/layers/01-probes/`. The original probe transcripts are
kept as historical evidence; their current interpretation is stated here.

## 1. Value-domain matrix

| Value / field | Contract domain | Python repr | Rust repr | Canonical serialization | Lossless across all? | Evidence / witness |
|---|---|---|---|---|---|---|
| number (one kind) | finite binary64 with every integral value within ±(2^53−1) (SER-008; G-016, G-023, G-025); −0 → 0 (G-017) | `int`/`float`, unified at the seam | `serde_json::Number` as a container only; checked integrality and a normalized `f64` or checked safe integer | ECMAScript shortest form | YES: every admitted integral value is exact in binary64; host int/float tags never decide validity or equality | AUDITED: reference library; scenarios `canonical-bytes-and-content-hash` (rounding, underflow, subnormal) and `portable-value-domain-rejections` (2^53 in every spelling, `1e400`) |
| numeral interpretation | nearest binary64, ties to even (RFC 8785 §3.2.2.3) | `json` float parsing gives nearest; overflow gives `inf`, which must be rejected | `serde_json` with `float_roundtrip`; its overflow error must map to `value.number_not_finite` | — | YES once each host's overflow outcome is mapped | Codex probes (`2b388e62`): `1.0000000000000001`→1, `1e-400`→0, `5e-324` kept, `9007199254740991.5`→2^53 |
| string | Unicode scalar values | `str` can hold lone surrogates, so it must be checked | `String` cannot; serde_json's decode error must map to `value.lone_surrogate` | RFC 8785 escaping | YES within the domain | AUDITED |
| object member names | unique **after escape decoding**; ordered by UTF-16 code units | `dict` is last-key-wins on decode, so `object_pairs_hook` is needed | `Map` is last-key-wins, so duplicate-aware decoding is needed before map construction | RFC 8785 member order | YES only with UTF-16 ordering and pre-map duplicate rejection | AUDITED: serde_jcs orders by code point and **diverges**; scenarios include `｡` vs `😀` and `{"a":1,"a":2}` |
| version | positive integer edition 1…2^53−1 (G-012); `2.0` is edition 2 (G-023) | number, unified | number, unified | number | YES | scenario `version-integer-edition-ordering` (stage precedence: out-of-range is `value.integer_out_of_range`) |
| content hash | SHA-256, lowercase hex (G-014) | `hashlib` | `sha2` | 64 hex characters | YES | AUDITED (Codex re-derived all nine) |
| stable ID (CORE-001) | lowercase portable ASCII token, 1–128 bytes, no trailing `.`, no Windows device basenames (G-020) | `str` with the ASCII grammar | `String` with the ASCII grammar | bytes as given | YES (ASCII only) | scenario `stable-id-lexical-domain` |
| operation identity (CORE-012) | `{source_namespace` (G-020 token)`, source_operation_id` (1–256 UTF-8 bytes, exact)`}` (G-032, G-033) | two `str` fields | two `String` fields | an object with two members | YES (exact bytes; no normalization) | scenario `operation-identity-namespaced-pair` |
| timestamp (HIST-004) | shared grammar (G-026, G-028, G-030) normalized to `YYYY-MM-DDTHH:MM:SS.ffffffZ`; local and UTC instants within 0001-01-01…9999-12-31 (G-029) | canonical `str`; `datetime` behind the grammar and range checks | canonical `String`; `i64` epoch µs plus civil arithmetic | the canonical string | YES: the whole domain (−62135596800000000…253402300799999999 µs) fits `i64` with exact round trips in both languages. The internal µs value is **not** a portable JSON number, because it exceeds 2^53−1 | probe `01-probes/timestamp-domain.md`; scenario `timestamp-seam-normalization` |

## 2. Lower-layer capability matrix

| Operation | Owning layer | Seam | Expresses contract? | Python | Rust | Extension? |
|---|---|---|---|---|---|---|
| decode JSON text and validate stages 1–2 (SER-008, G-031) | 01 (new) | public payload seam | YES: stage table and error map | stdlib `json` alone is insufficient (accepts `Infinity`, last-key-wins, lone surrogates); hooks plus checks are needed | `serde_json` alone is insufficient (last-key-wins, error mapping); a duplicate-aware visitor plus checks are needed | additive, Layer 01 |
| validate native values (stage 1 `value.unsupported_type`, stage 2) | 01 (new) | native API seam | YES | type dispatch | typed values plus checks | additive |
| canonicalize | 01 (new) | — | SER-009 | the reference library is conformant | serde_jcs is **non-conformant** (key order); a conformant UTF-16-ordered serializer is needed | additive |
| hash | 01 | — | SER-009 | yes | yes | — |
| compare versions, revisions and operation identities | 01 | — | CORE-002, CORE-003, CORE-012 | yes | yes | — |
| normalize timestamp | 01 | public seam | HIST-004 grammar | a regex grammar plus `datetime` arithmetic | grammar plus `i64` civil arithmetic | additive |

## 3. Hazard checklist (families touched)

| Hazard | State | Evidence / reason |
|---|---|---|
| H1 integer width / float specials | AUDITED | one numeric kind; whole-number bound; overflow, underflow and subnormal cases; stage-2 codes |
| H2 scalar domain / encoding / line endings | AUDITED | surrogates (decoded and native); SER-009 hashes bytes as given |
| H3 Unicode normalization | AUDITED | never applied: IDs, operation identities and hashed text are exact bytes; an NFC vs NFD fixture shows two distinct operation identities |
| H4 time | AUDITED | full grammar, range and overflow rules (G-028…G-030); domain fits `i64` µs in both languages (probe); host parsers are not relied on |
| H5 key order | AUDITED | UTF-16 order; serde_jcs divergence fixtured |
| H6 YAML/JSON | AUDITED | scenarios carry JSON text in single-quoted YAML (YAML-1.2-core profile) |
| H7 hashing | AUDITED | SHA-256 over JCS bytes, lowercase hex |
| H8–H10 | NOT_APPLICABLE | no persistence, paths or concurrency in Layer 01 (operation-identity *behaviour* is Layer 04) |
| H11 identifiers | AUDITED | G-020 token, path projection pinned; G-032 operation identity kept separate from stable IDs |

## 4. Concurrency / order

NOT_APPLICABLE — Layer 01 operations are pure functions. Error selection is deterministic: stage
precedence (G-031) and canonical within-stage order (G-034); host map order is never observable.

## 5. Neighbourhood expansion

| Family | Members probed | Source | New rows / findings |
|---|---|---|---|
| H1 | 2^53−1, 2^53 (integer, decimal and exponent spellings), `9007199254740991.5`, `1e400`, `1e-400`, `5e-324`, `1.0000000000000001`, −0 | reference library; Codex probes | G-025 bound after rounding; `value.number_not_finite` |
| H4 | year 0001/9999 boundaries, offset overflow both ways, century leap days, letter case, offset and fraction grammar | strict grammar checker; Python and Rust domain probes | G-028…G-030; timestamp-domain probe |
| H5 | ASCII, BMP high (`｡` U+FF61), astral (`😀`) | probes | UTF-16 order fixture; serde_jcs divergence |

## 6. Verdict

```text
FEASIBILITY
    FEASIBLE (DRAFT)  no open path-C decision for Layer 01 (G-012..G-034; within-stage
                      error order decided by G-034, WP01-CR-005). Rust needs its own
                      UTF-16-ordered RFC 8785 serializer (serde_jcs 0.1 orders by code point),
                      duplicate-aware decoding and the SER-008 stage checks; timestamps need the
                      contract grammar in front of any host time library. For re-review by Codex.
```
