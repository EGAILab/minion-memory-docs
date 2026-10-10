# WP-01 — CE-01-01 implementation record (Claude)

**Agreed checkpoint:** `assurance/convergence/CE-01-01-classification.md` revision 3 (`8e8d30a8`),
APPROVED by Codex (`1d99bc2c`). **Implementation, a single pass:** code
`4fe3ed34c29a6868a3f5050ecee95885b73bead0`. **Frozen reference:** `eb47635c`. **Episode findings:**
WP01-CR-007 (= WP01-PY-004) and WP01-CR-008 (= WP01-PY-008).

This is an implementation record, not a review or a closure claim.

## What changed (`minion_memory.core`)

| Constraint (checkpoint §4) | Implementation |
|---|---|
| 1. Kind by genuine ancestry | `values._native_family`: `x is None`, `type(x) is bool`, then `issubclass(type(x), B)` for the admitted bases. No `isinstance` and no `__mro__` on any input. |
| 2. Extract, never dispatch | `values._extract_native` is one iterative stage-1 pass that builds exact built-ins. Scalars come via `int.__int__`, `float.__float__`, `str.__str__`, sequences via `list`/`tuple` `__len__`/`__getitem__` on the bases, maps via `dict.items`. Byte buffers come via `bytes.__bytes__` / `bytearray.copy` / exact `memoryview.tobytes`. Stage-1 diagnostics never name or format a caller object. |
| 3. Framework-owned state | `JsonText` stores its text in a base `__slots__` slot, written and read only through the base's own member descriptor, so subclass `text`, `__dict__` and `__getattribute__` are never invoked. `validate_arguments` requires `issubclass(type(m), dict)` and reads `dict.items`; anything else raises `TypeError` before any argument is inspected (G-043). |
| 4. Normalize first | Extraction detects cycles by container identity on the active path (`value.cyclic`, G-040) and duplicate base names per map while ordering members canonically (`value.duplicate_key`, G-039); shared aliases are copied. Stages 2–3, serialization, hashing and diagnostics then see exact built-ins only (G-042). |
| 5. No rejection-only shortcut | Hostile admitted subclasses, including custom-metaclass ones, return their base values. |

`decode_json` reads `str`, `bytes` and `bytearray` families by base protocol (G-041); other inputs
raise `TypeError`.

## Kill evidence

**Unit controls.** `minion-memory-python/tests/core/test_ce0101_native_binding.py` has 252 tests:
- every subclassable family crossed with every hook, with `ALL`, each hook raising if called;
- the CH01–CH05, M01/M02, D01/D02, B066 and CM01/CM02 controls;
- byte-buffer hooks, duplicates, cycles (run in a subprocess with a timeout), shared aliases, G-042
  exact returns, conflict diagnostics and stages across arguments.

| Code | Result |
|---|---|
| Frozen `eb47635c` | **128 failed, 124 passed**. Every named witness failed; the passing tests are the hook/family combinations the frozen code never reached, i.e. KEEP rows. |
| Implementation `4fe3ed34` | all 252 pass |

**Characterization re-execution.** Codex's embedded driver with the G-042 observer, run on Windows
with project-local CPython 3.12.8:

| Measure | Frozen `eb47635c` | Implementation `4fe3ed34` |
|---|---|---|
| Normative rows OK | 21,925 / 25,470 | **25,470 / 25,470** |
| Rows with any user hook fired | many | **0** (empty hook histogram) |
| Value-returning rows with non-exact returns | 570 | **0** of 6,775 |
| Boundary rows meeting the decided oracle | 50 / 75 | **75 / 75**, including `value.cyclic` for all three cycles |

Every one of the 4,116 FIX rows is therefore killed.

## Gates

- `ruff`, `ruff format --check` and `mypy --strict` are clean (11 source files).
- `pytest`: **335 passed, 5 placeholder expected failures**.

No POSIX run is claimed; Codex's targeted closure covers it.
