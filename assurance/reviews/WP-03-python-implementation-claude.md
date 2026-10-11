# WP-03 — Python implementation record (Claude)

**Agreed contract:** docs `b514c16d` / code `619540ae` (Codex APPROVED `ea4abfd2`).
**Implementation:** code `c86daf806fecb473c832ccecba5495b064b243ca` on `wp03/contract`.
**Gate:** G3 (Python), author-run at the exact code. This record is evidence, not a review.

## Implementation (`minion_memory.core.projection`)

`project_history(reader, stream, relations)` follows PROJ-001's order of evaluation:

1. **Generic stages** across `reader`, `stream` and `relations` (`validate_arguments`, G-031).
2. **Argument shapes.** The reader (Layer 02 `_reader_rule`), then the stream: closed, with a
   CORE-001 `store_id`, closed entries and strictly increasing integral positions from 1. Then the
   **early** lineage checks:
   - closed relations;
   - CORE-001 endpoints;
   - the vocabulary as an exact string match;
   - exactly one typed target;
   - `to_artifact` only for `derived_from`, as exactly `{stable_id, artifact_version}` or
     `{content_hash}` (lowercase 64-hex) (G-072, G-075).

   Equal normalized relations collapse to one, keeping the first occurrence for determinism.
3. **Entries** in position order through the Layer 02 `_admit` gates. Any error fails the
   projection: an argument error names `stream` and carries the position; `unknown_required` names
   no argument, carries the position, and its detail gives the routing triple (G-070). A repeated
   `record_id` compares the SER-009 canonical bytes of the normalized envelopes: identical bytes
   become a duplicate occurrence; different bytes raise `history.duplicate_record_id` at that
   position (G-073).
4. **Late** checks:
   - the `from` endpoint must be available;
   - no self-links;
   - resolution-family targets must be available;
   - `derived_from` targets that are unavailable are kept as unresolved derivations;
   - Kahn's algorithm, run iteratively, checks acyclicity of the resolution family and, separately,
     of `derived_from` between available records (G-071).
5. **Resolution.**
   - `current` holds the decoded records targeted by no `supersedes` or `corrects` relation, in
     first-position order (presentation only).
   - `interpretations` uses direct `reinterprets` links only (G-074).
   - Relations and unresolved derivations are sorted by the contract's presentation key.

`MnemeValidationError` gains an optional `position`, preserved by `for_argument` and set by
`at_position`.

## Corpus and runner

- **Scenarios.** The two Layer 03 scenarios (54 steps) are promoted to ACTIVE with unchanged
  expectations.
- **Python runner.** It declares `IMPLEMENTED_LAYER = 3`, adds the `project_history` operation, and
  reports `position` whenever an error carries one.
- **Rust.** It declares Layer 02, so its runner reports the Layer 03 scenarios as `xfail` under the
  implemented-layer rule.

## Gates (Windows, project-local CPython 3.12.8)

- `ruff`, `ruff format --check` and `mypy --strict` (18 files) are clean.
- **488 passed, 5 xfailed**. All 17 ACTIVE scenarios pass.
- Coverage, statements and branches over all of `minion_memory` with no exclusions:
  **981/981 statements, 432/432 branches**.
- `mneme-process check --deep-sources`: 8/8.

## Discrimination

12 planted violations in `projection.py`, and **12 are killed**:
- a tie-break keeping only the last head;
- a partial projection past `unknown_required`;
- identical repeats failing;
- conflicting reuse coalesced;
- dangling `derived_from` failing;
- interpretations inherited along `supersedes`;
- `reinterprets` excluded from cycles;
- `derived_from` cycles allowed;
- repeated relations invalid;
- an artifact target allowed on `supersedes`;
- entry errors losing their position;
- relations output unsorted.

**Q10 (artifact target on `supersedes`) initially survived and was not equivalent.** Without the
early rule, the relation still failed late as an unavailable endpoint, with the same code but at a
different stage. So paired with an entry error, the reported error changes. A dedicated control was
added (`test_artifact_target_on_a_resolution_kind_is_an_early_shape_error`). The same early-versus-
late seam deserves a check in Rust.

The script is `.tmp/work/claude/py_mutants_wp03.py`. No POSIX run is claimed.
