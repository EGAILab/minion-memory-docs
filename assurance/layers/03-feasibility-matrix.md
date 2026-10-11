# Cross-Language Feasibility Matrix — WP-03: HistoryProjector and lineage

**Status:** DRAFT for WP-03 CONTRACT_REVIEW. **Contract:** HIST-006/007 and PROJ-001/002 Layer 03
blocks; Owner G-066…G-070. **Builds on:** the certified Layers 01–02 (admission gates,
HistoryBoundary, value domain).

## 1. Value and seam matrix

| Value / seam | Contract | Python | Rust | Lossless? |
|---|---|---|---|---|
| stream | closed `{store_id, entries[{position, record}]}`; positions strictly increasing from 1 | list walk; `int` positions | `Vec` walk; `i128`/`u64` | YES |
| relations | closed triples; closed vocabulary of 4 kinds | dict/str checks | struct/enum | YES |
| lineage graph | endpoints are decoded IDs; no self-links or duplicates; acyclic over resolution-affecting kinds | iterative DFS / Kahn | iterative DFS / Kahn | YES |
| result | closed record; store-order presentation; set-valued `current` | dict/list | `Value` object/array | YES |
| error position | integer on entry errors | `MnemeValidationError.position` (new optional attribute) | `Error.position` (new optional field) | YES |

## 2. Determinism hazards

| Hazard | State | Reason |
|---|---|---|
| H5 ordering | AUDITED | result order is by store position and the documented relation sort; relation input order and host map order are never observable; no ordering selects among heads (G-069) |
| recursion depth | AUDITED | lineage graphs and payloads are walked iteratively (Layer 01 practice) |
| H8–H10 | NOT_APPLICABLE | no persistence; Layer 04 owns durable append |

## 3. Verdict

```text
FEASIBILITY
    FEASIBLE  Pure functions over Layers 01–02 in both languages. A small extension adds an optional
              position to both error types.
```
