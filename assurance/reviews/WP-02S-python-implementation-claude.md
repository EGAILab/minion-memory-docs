# WP-02S — Python implementation record (Claude)

**Agreed contract:** docs `c08c57e4` / code `0c569afb` (Codex APPROVED `697e372c`).
**Implementation:** code `5d1a74a56585c450fd5f6ce8fe7020318cbed914` on `wp02s/python`.
**Gate:** G3 (Python), author-run at the exact code. This record is evidence, not a review.

## Base

`wp02s/python` starts from WP-02 code `43e0984e`. That base carries the history module, the NF-026
runner rules and both runners' implemented-layer declarations. On top of it, the two agreed WP-02S
corpus commits are cherry-picked. They touch only the scope scenarios and the manifest, and apply
cleanly.

The dependency runs one way only: WP-02S code depends on WP-02 code, and WP-02 is never blocked by
WP-02S (G-047).

## Implementation (`minion_memory.core.scope`)

| Contract | Public seam | Notes |
|---|---|---|
| Value (G-056, G-064) | `validate_scope(scope)` | Accepts either closed record. The facet-name grammar is G-064's, with no device exclusion, and values use CORE-001. It returns a new normalized dict. Well-formed unknown facets are preserved. Errors name no argument. |
| Equality (G-056) | `scopes_equal(a, b)` | Structural; arguments are validated `a`, then `b`, and named. |
| Matching (G-058, G-061, G-062) | `scope_visible(record, query)` | `record` is validated before `query`. Unresolved records and records with unknown facets are hidden. A query naming an unknown facet (including any `learning.*` facet) or in unresolved form is `scope.query_invalid`. Visible means every declared record facet is equal in the query. |
| Registry (G-061) | `AGENT_FACETS` | The six canonical Agent names. |

## Corpus

The three scope scenarios (73 steps) are promoted to ACTIVE with unchanged expectations. The Python
runner gains three operations, each mapped to one public function. Rust declares Layer 01, so its
runner reports them as `xfail` under the implemented-layer rule.

## Gates (Windows, project-local CPython 3.12.8)

- `ruff`, `ruff format --check` and `mypy --strict` (16 files) are clean.
- **467 passed, 5 xfailed**. All 15 ACTIVE scenarios pass: 8 from Layer 01 and 7 from Layer 02.
- Coverage, statements and branches over all of `minion_memory` with no exclusions:
  **804/804 statements, 352/352 branches**.
- `mneme-process check --deep-sources`: 8/8.

## Discrimination

11 planted violations in `scope.py`; **10 were killed**:
- query-omitted facet treated as a wildcard;
- unresolved records visible;
- unknown query facets accepted;
- device names excluded from facet names;
- extra dots allowed;
- multi-valued facets accepted;
- an unresolved scope carrying facets;
- learning facets in the registry;
- equality comparing only `scope_state`;
- 129-byte segments.

**S03, "unknown record facets ignored", survived.** It is claimed to be **equivalent**, by this
argument:
- every `query` passes `_query_rule`, which rejects any facet outside the registry, and no public
  seam bypasses it;
- so the allowed map contains only registry facets;
- so for a record facet `k` outside the registry, `allowed.get(k)` is `None`, never equal to its
  string value, and the `all(...)` is already `false`.

The explicit check stays as defense in depth and documents G-061 fail-closed behaviour. **Please
challenge this claim**; the P12 lesson from WP02-CR-006 applies.

The script is `.tmp/work/claude/py_mutants_wp02s.py`. No POSIX run is claimed.
