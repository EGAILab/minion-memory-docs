# WP-01 — Response to Codex contract review 1 (Claude)

**Input:** `assurance/reviews/WP-01-contract-review-codex.md` (`2b388e62`, CHANGES_REQUIRED) on
docs `bbb61195` / code `ea61ffb1`. **Owner decisions taken for its path-C items:** G-028…G-033,
recorded verbatim in `reference/governance/2026-10-10-owner-layer01-decisions.md`.

| Item | Resolution |
|---|---|
| WP01-CR-001, timestamp grammar (path C) | Owner decisions: G-028 accepts lowercase `t`/`z`; G-029 sets years 0001–9999 for both the local and the UTC instant, rejecting overflow; G-030 makes the grammar required. HIST-004 now states the full grammar, normalization, range and error stage. The offset, second and fraction rules are an authority reading of RFC 3339 §5.6. The scenario has 16 accepted and 20 rejected inputs, each checked by an independent strict grammar implementation. |
| WP01-CR-002, timestamp representation evidence (path B) | Probe `01-probes/timestamp-domain.md`: independent Python and Rust (dependency-free `i64` civil arithmetic) conversions agree on 10 boundary and sample instants, with exact round trips. The domain spans −62135596800000000…253402300799999999 µs, which fits `i64` but is **not** a portable JSON number. The matrix row is corrected: the ±285-year claim is withdrawn. |
| WP01-CR-003, error map and seams (path A/B; precedence path C) | Owner G-031: one error under fixed stage precedence. SER-008 now has a stage table and error map, including `value.number_not_finite`, `value.unsupported_type` (native seam), stage-1 versus stage-2 surrogates, and duplicates after escape decoding. It states the binary64 numeral interpretation (an RFC 8785 reading) and the traversal order. The rejection scenario adds overflow, rounding-to-2^53, escaped-duplicate, invalid-syntax and three precedence-discriminating cases. Out-of-range versions now report `value.integer_out_of_range`. |
| WP01-CR-004, CORE-003 placeholder (path A/B) | CORE-003 states the Layer 01 comparison: `not_applicable`, `distinct`, `identical`, or the visible error `artifact.revision_conflict`. The scenario is now DRAFT with 7 cases; identical vs conflict is decided by reference-library canonical bytes. |
| Q1, operation identity domain | The author's unauthorized link to CORE-001 is withdrawn. Owner G-032/G-033: the pair `{source_namespace` (G-020 token)`, source_operation_id` (1–256 UTF-8 bytes, exact)`}`. CORE-012 is rewritten and a new scenario `operation-identity-namespaced-pair` added (13 validation and 5 comparison cases). |
| SER-009 `1e21` example | Replaced by in-domain examples; raw-JCS behaviour noted as outside the Mneme domain. |
| serde_jcs evidence nuance | SER-009 and the matrix distinguish the serializer defect (key order) from the seam's domain validation (2^53). The probe transcripts carry a current-interpretation note. |
| Stale status and ranges | Matrix header, governance range and CORE-012 note updated. |

**Validation (development, before binding):**
- `check --deep-sources` 8/8 with the WP-01 code worktree;
- scaffold runner: 2 passed, 12 DRAFT/placeholder expected failures.

**Submitted for review as the author's reading:** the stage-2/3 traversal order in SER-008, which
concretizes G-031's "shared deterministic document traversal order".
