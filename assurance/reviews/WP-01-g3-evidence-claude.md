# WP-01 — G3 evidence and remediation of the final review (Claude)

**Responds to:** Codex final complete review `e340e439` (CHANGES_REQUIRED: WP01-CR-009, WP01-CR-010).
**Repaired code:** `bac6594e06dd321e547e917cebeeefc6562a19b9` (parent `4fe3ed34`). **Gate:**
`process/gate-tiers.md` G3. This is author-run evidence, not a review or a closure claim.

## WP01-CR-010 — coverage

Reproduced first: on `4fe3ed34` my own run gave the same 15 missing statements Codex listed.

**Configuration.** coverage 7.16.2, now pinned as a dev dependency in `pyproject.toml`/`uv.lock`.
`source = minion_memory`, `branch = true`, `patch = subprocess`, `parallel = true`, **no exclusions**
and no `pragma: no cover`. The suite was run with
`coverage run -m pytest tests`, then `coverage combine` and `coverage report -m`, with project-local
CPython 3.12.8 on Windows.

**Result at `bac6594e`:**

```text
Name                                 Stmts   Miss Branch BrPart  Cover
src\minion_memory\__init__.py            1      0      0      0   100%
src\minion_memory\core\__init__.py       5      0      0      0   100%
src\minion_memory\core\errors.py        21      0      8      0   100%
src\minion_memory\core\identity.py      83      0     26      0   100%
src\minion_memory\core\time.py          38      0     14      0   100%
src\minion_memory\core\values.py       470      0    234      0   100%
TOTAL                                  618      0    282      0   100%
```

The certified Python surface is the whole `minion_memory` package (the Layer 01 core and its
exports). It is unnarrowed: every statement and branch counts.

### Accounting of each line Codex listed

| Line(s) at `4fe3ed34` | Behaviour | Disposition |
|---|---|---|
| values 112, 135 | missing `,` / `:` → `value.invalid_json` | **reachable**: new public controls (4 cases) |
| values 362 | `decode_json` of a non-text input → `TypeError` | **reachable**: new controls (int, None, list, memoryview) |
| values 478, 481, 484 | `JsonText.text`, immutability, non-echoing repr | **reachable**: new control |
| values 493–494 | `JsonText` subclass that never stored text → `TypeError` | **reachable**: new control |
| values 512 | non-string argument name → `TypeError` | **reachable**: new controls; also a base-read `str` subclass name |
| values 666–669 | `raw_content_hash` of an exact `memoryview`; non-bytes → `TypeError` | **reachable**: new controls |
| values 564 | float `0` formatting | **unreachable**: after normalization zero is the integer `0` (G-017, G-023). Removed and replaced by a documenting assertion. |
| values 577 | integral-float formatting `digits + zeros` | **unreachable**: every integral value is an `int` after normalization (G-023/G-025). Removed and documented. |
| errors 42 | `describe()` fallback for a non-built-in | **unreachable**: native input is extracted to exact built-ins first (G-042). Replaced by an assertion. |

The removals change no observable behaviour. Evidence:
- the characterization driver re-run on `bac6594e` gives 25,470/25,470 OK, zero hooks and 0
  non-exact value returns;
- the 75 boundary observations are byte-identical to the `4fe3ed34` run;
- all 8 ACTIVE scenarios pass.

The new controls live in `minion-memory-python/tests/core/test_layer01_surface.py`. They exercise
the public API only. Every earlier discriminating control is kept.

**Gates at `bac6594e`:**
- `ruff` and `ruff format --check` are clean;
- `mypy --strict` is clean on 12 files;
- `pytest`: 354 passed, 5 placeholder expected failures (Layer 04 and later).

## WP01-CR-009 — readiness records

| Record | Repair |
|---|---|
| `assurance/layers/01-feasibility-matrix.md` | Rewritten for the final contract through G-043, with references to the checkpoints, the closure and this review. It now covers the native-binding, cycle, duplicate, byte/control and exact-return rows. It also states the **staged decoder requirement** with Codex's witness `{"a":1e400,"b":1,"b":2}` → `value.duplicate_key`: an eager numeric decode, with or without a duplicate-aware visitor, is insufficient. Historical probe transcripts are kept and declared historical. |
| `plans/WP-01.md` | Rewritten to the current status. It carries the G-012…G-043 decision map and an assurance trail through `e340e439`. Integers ≥ 2^53 are now stated as a SER-008 domain-validator responsibility, not a serializer defect. |
| `spec/serialization.md` §Layer 01 | The "DRAFT … not reviewed, not implementation-facing" sentence is replaced by the checkpoint status (approved, implementation-facing, not yet accepted onto `main`). The decision range is updated to G-012…G-043. |
| `spec/core.md`, `spec/serialization.md` | Stale `DRAFT` tags on the Layer 01 decision headings are removed. No normative text changed. |

No production semantics changed and no Owner decision is needed.
