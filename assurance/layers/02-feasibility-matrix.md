# Cross-Language Feasibility Matrix — WP-02: history and compatibility envelope

**Template:** `process/templates/cross-language-feasibility-matrix.md`.
**Status:** DRAFT for WP-02 CONTRACT_REVIEW round 2. All domains are now Owner-decided (G-052 to G-055).
**Contract:** HIST-002, HIST-005, HIST-010, SER-005 and SER-006 Layer 02 blocks; Owner G-047…G-055.
**Builds on:** the certified Layer 01 (code `cc3c5d54`): value domain, canonical order, stage
precedence, CORE-001 tokens and HIST-004 timestamps. Both languages already implement these, and
they are consumed unchanged.

## 1. Value and seam matrix

| Value / seam | Contract domain | Python binding | Rust binding | Lossless? | Evidence |
|---|---|---|---|---|---|
| envelope | closed object for a recognized pair (G-048); schema-identity triple always validated (G-052); four ordered gates (G-055) | `dict` after the Layer 01 extraction; member-set check | `Value` object after Layer 01 normalization; member-set check | YES | `history-envelope-admission-shape` |
| `profile`, `record_type` | CORE-001 token domain; vocabulary owned by the profile | `str`, Layer 01 token rule | `String`, Layer 01 token rule | YES (ASCII) | same; `history-profile-exclusion` |
| `schema_version` | integral value 1…2^53−1; 0 is never a sentinel (G-052) | exact `int` after normalization | `i128`/`u64` after normalization | YES | `schema_version 1.0` case |
| `compatibility` | `"required"` \| `"ignorable"`; validated only after profile admission (G-050) | exact string compare | enum from exact string | YES | replay cases |
| `record_id` | CORE-001 | Layer 01 `validate_stable_id` rule | Layer 01 rule | YES | `id.invalid` case |
| `recorded_at` (required), `occurred_at` (optional) | HIST-004 grammar and range; absence means unknown; `null` is invalid (G-049) | Layer 01 normalizer | Layer 01 normalizer | YES | timestamp cases |
| `payload`, `provenance` | any SER-008 value, returned normalized | normalized exact built-ins | normalized `Value` | YES | HIST-010 case |
| reader | closed `{profile, recognized[]}` with closed entries; duplicates after normalization rejected (G-053) | set of `(str, int)` | `HashSet<(String, i128)>` or a sorted `Vec` | YES | reader cases |
| HistoryBoundary | closed `{store_id, position}`; position 0…2^53−1, 0 = before the first physical record (G-054) | `(str, int)` | `(String, u64)` | YES | `history-boundary-local-cursor` |

## 2. Decision-order matrix (no host behaviour may leak)

| Step | Rule | Python | Rust | Hazard |
|---|---|---|---|---|
| 1–2 | generic stages across all arguments in declared order (G-031) | `validate_arguments` with declared order | `validate_arguments` slice order | — |
| 3a | reader shape (G-053), then gate 1: the record's schema-identity triple (G-052) | explicit checks; no exceptions from dict lookups | explicit pattern match | H11 |
| 3b | gate 2: profile admission, then compatibility, then recognition (G-050, G-055) | compare normalized strings | same | — |
| 3c | recognition is exact pair membership after normalization | `(type, int)` membership | same | H1 (`1.0` vs `1`) |
| 3d | gate 3: closed shape; gate 4: typed fields in canonical member order (G-055) | iterate UTF-16-sorted members | same | H5 |
| relation | `unknown_required` / `boundary_incomparable` only after the argument stages; no argument named | explicit | explicit | — |

## 3. Hazard checklist

| Hazard | State | Reason |
|---|---|---|
| H1 numbers | AUDITED | edition and position are integers; `1.0` and `2.0` normalize via Layer 01 |
| H2 strings | AUDITED | all tokens use the Layer 01 ASCII grammar; payload strings use the SER-008 domain |
| H4 time | AUDITED | Layer 01 HIST-004 reused; no order between the two timestamps (G-049) |
| H5 ordering | AUDITED | typed-field order is canonical UTF-16 member order; the boundary order is store-local only (G-051) |
| H8–H10 | NOT_APPLICABLE | no persistence, paths or concurrency in Layer 02; cursor storage is Layer 04 |
| H11 identifiers | AUDITED | `store_id`, `profile` and `record_type` are CORE-001 tokens, compared exactly |

## 4. Concurrency and order

The store-local position is a read cursor only (G-047, G-051). It implies no global, causal or
cross-device order, and nothing in Layer 02 orders records by time.

## 5. Verdict

```text
FEASIBILITY
    FEASIBLE  Pure functions over Layer 01 values in both languages; no new host-dependent behaviour.
    Prerequisite: NF-026 (the Rust runner must report DRAFT scenarios as xfail, per the corpus rule).
```
