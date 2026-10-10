# Cross-Language Feasibility Matrix — WP-01: Core identity, versions, canonical bytes, value domain

**Template:** `process/templates/cross-language-feasibility-matrix.md`. **Status:** DRAFT (WP-01
`CONTRACT_DRAFT`; per Owner G-019 not yet handed to review — validator results are development
feedback only). **Authority bundle:** `mneme-v2.3-dual-profile`; **Owner decisions:** G-012…G-017.
**Author:** Claude. **Independent checkpoint reviewer:** Codex (after WP-P01 closes).
**Toolchains probed:** CPython 3.12.8; rustc 1.97.1; `rfc8785` 0.1.4 (Python reference);
`serde_jcs` 0.1.0 + `serde_json` 1 (Rust, off-the-shelf). Evidence: `assurance/layers/01-probes/`.

## 1. Value-domain matrix

| Value / field | Contract domain | Python repr | Rust repr | Canonical serialization | Lossless across all? | Evidence / witness |
|---|---|---|---|---|---|---|
| integer | ±(2^53−1) (SER-008, G-016) | `int` (unbounded → must range-check) | `i64` (wider → must range-check) | RFC 8785 decimal | YES within domain; both hosts can hold out-of-domain values → **seam check required in both** | AUDITED: reference rejects ≥2^53; serde_jcs emits them (probe) → scenario `portable-value-domain-rejections` |
| float | finite binary64; −0 → 0 (G-017) | `float` | `f64` | ECMAScript shortest form | YES (probe: 1.0, 1e21, 0.1 identical bytes/hash) | AUDITED; NaN/Inf rejected (json text `Infinity` → `value.invalid_json`) |
| integer vs whole float | **undecided** (1 vs 1.0) | `int` vs `float` distinct | `i64` vs `f64` distinct (serde_json Number) | both → `1` | **NO — hash cannot distinguish** | **Finding NF-022 (path C, Owner)** |
| string | Unicode scalar values | `str` (can hold lone surrogates → must check) | `String` (cannot) | RFC 8785 escaping | YES within domain | AUDITED: serde_json rejects `"\ud800"` at parse; Python `json` accepts → seam check in Python |
| object keys | unique strings; order by UTF-16 code units | `dict` (last-key-wins on decode) | `Map` (last-key-wins on decode) | RFC 8785 member order | YES only if both implement UTF-16 order and duplicate rejection | AUDITED: serde_jcs uses code-point order (**diverges**); scenario includes `｡` vs `😀` |
| version | positive integer 1…2^53−1 (G-012) | `int` | `u64`/`i64` | integer | YES | scenario `version-integer-edition-ordering` |
| content hash | SHA-256 lowercase hex (G-014) | `hashlib` | `sha2` | 64 hex chars | YES (identical digests in probe) | AUDITED |
| ID (CORE-001) | **undecided** lexical domain | `str` | `String` | — | depends on NF-010 | **NF-010 residual (path C)**; IDs appear in package file names (R00 §11: `memories/<knowledge-unit-id>.md`) → H9 path safety and Windows case-insensitive collisions |
| timestamps (HIST-004) | **undecided** | — | — | — | — | **NF-015 (path C)**; G-016 caps integer timestamps at µs since epoch |

## 2. Lower-layer capability matrix

| Operation | Owning layer | Seam | Expresses contract? | Python | Rust | Extension? |
|---|---|---|---|---|---|---|
| decode JSON text → domain value with rejection | 01 (new) | none yet | must be specified (SER-008) | stdlib `json` insufficient alone (accepts `Infinity`, last-key-wins, lone surrogates) | `serde_json` insufficient alone (last-key-wins; i64 range) | additive, Layer 01 |
| canonicalize | 01 (new) | none yet | SER-009 | reference lib conformant | serde_jcs **non-conformant** | additive; Rust must not use serde_jcs 0.1 unverified |
| hash | 01 | — | SER-009 | yes | yes | — |
| compare versions | 01 | — | CORE-002 | yes | yes | — |

## 3. Hazard checklist (families touched)

| Hazard | State | Evidence / reason |
|---|---|---|
| H1 integer width / float specials | AUDITED | probes; SER-008 seam rule |
| H2 scalar domain / encoding / line endings | AUDITED | surrogates; SER-009 hashes bytes as given (CRLF ≠ LF by design) |
| H3 Unicode normalization | AUDITED | none applied (G-014); NF-010 must not introduce it implicitly |
| H4 time | DEFERRED_WITH_REASON | NF-015 awaits Owner; no Layer 01 rule depends on it beyond HIST-004 encoding |
| H5 key order | AUDITED | UTF-16 order; divergence found and fixtured |
| H6 YAML/JSON | AUDITED | scenarios carry JSON text in single-quoted YAML (escapes preserved; YAML-1.2-core profile) |
| H7 hashing | AUDITED | SHA-256 over JCS bytes, lowercase hex |
| H8–H10 | NOT_APPLICABLE | no persistence/paths/concurrency in Layer 01 (operation-identity *behavior* is Layer 04) |
| H11 identifiers | DEFERRED_WITH_REASON | NF-010 residual awaits Owner |

## 4. Concurrency / order

NOT_APPLICABLE — Layer 01 operations are pure functions.

## 5. Neighborhood expansion

| Family | Members probed | Source | New rows / findings |
|---|---|---|---|
| H1 | 2^53−1, 2^53, 2^53+1, i64 max/min, 1.0, 1e21, 0.1, −0.0 | probes | integer-range seam rule; NF-022 (int vs float) |
| H5 | ASCII, BMP high (`｡` U+FF61), astral (`😀`) | probes | UTF-16 order fixture; serde_jcs divergence |

## 6. Verdict

```text
FEASIBILITY
    BLOCKED   open: NF-010 residual (ID lexical domain), NF-012 (scope of CORE-003),
              NF-015 (timestamps), NF-022 (integer vs whole-number float) — all path C,
              awaiting Owner; to be asked while Codex is idle.
```
