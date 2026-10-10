# Cross-Language Feasibility Matrix — WP-02S: MemoryScope

**Template:** `process/templates/cross-language-feasibility-matrix.md`.
**Status:** DRAFT for WP-02S CONTRACT_REVIEW.
**Contract:** `spec/scope.md`, Layer 02 MemoryScope contract (Owner G-056…G-064).
**Builds on:** the certified Layer 01 (CORE-001 tokens; SER-008 value domain and stage precedence).

## 1. Value and seam matrix

| Value / seam | Contract domain | Python | Rust | Lossless? | Evidence |
|---|---|---|---|---|---|
| scope | closed `{scope_state: resolved, facets}` or `{scope_state: unresolved}` | normalized `dict` | normalized `Value` or an internal enum | YES | `core.scope.value-shape` |
| facet name | G-064: exactly two lowercase ASCII segments joined by one `.`; each segment 1–128 bytes, `[a-z0-9][a-z0-9_-]*`; **no** device-name exclusion (so `agent.con` is well formed and unknown) | `str` grammar check (not the CORE-001 stable-ID rule) | `&str` grammar check (not the CORE-001 rule) | YES (ASCII) | same; `agent.con`, 129-byte segment and non-ASCII controls |
| facet value | one CORE-001 token | `str` | `String` | YES | same |
| Agent registry | the six fixed names (G-061) | `frozenset` | `const` array / `phf` | YES | `core.scope.agent-isolation-six-dimensions` |
| query | resolved facet map; unknown facet is an error | `dict` | map | YES | `core.scope.applicability-matching` |
| `scope_visible` | for each record facet, the query has the same value; unresolved or unknown facets are hidden | iteration over record facets | same | YES | matching and isolation scenarios |

## 2. Order and hazards

| Hazard | State | Reason |
|---|---|---|
| H5 ordering | AUDITED | matching is set-based; host map order is never observable; errors are checked in declared argument order |
| H11 identifiers | AUDITED | facet **values** are CORE-001 tokens, including the device-name exclusion; facet **names** use the separate G-064 segment grammar, without device exclusion; both compared exactly; no aliasing inside the core |
| H3 Unicode | NOT_APPLICABLE | ASCII tokens only |
| H8–H10 | NOT_APPLICABLE | no persistence; capture, retrieval and ID lookup are consumed in Layers 06, 13 and 15 |

## 3. Verdict

```text
FEASIBILITY
    FEASIBLE  Pure functions over Layer 01 values; no host-dependent behaviour.
    Prerequisite shared with WP-02: NF-026 (Rust runner reports DRAFT scenarios as xfail).
```
