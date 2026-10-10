# WP-01 — Python remediation 1 (Claude)

**Input:** Codex implementation review `716d7218` (CHANGES_REQUIRED) on docs `4c27bd5c` / code
`f10c7b4f`. **Owner decisions taken for its path-C items:** G-035 (PY-005) and G-036 (PY-006),
recorded verbatim in `reference/governance/2026-10-10-owner-layer01-decisions.md`.
**Remediated code:** `eb47635c6ea997f030d04b8099366044a2f702aa`.

## Reproduce first

`minion-memory-python/tests/core/test_layer01_remediation.py` was executed against the unchanged
candidate `f10c7b4f` before any fix.
- **Every discriminating control failed there.** These cover the PY-001…004 and PY-007
  witnesses and the G-035/G-036 cases.
- **The 7 that passed are preservation controls, which hold on both versions:**
  - a complete record with an absent version is `not_applicable`;
  - an invalid id after a valid shape is `id.invalid`;
  - an encoding defect is reported where it really is first;
  - `range`, generators, `bytearray` and `memoryview` stay unsupported.
- **Not kill-credited.** The PY-001 JSON-seam and PY-007 controls use the new public names
  `JsonText` and `raw_content_hash`, which did not exist on `f10c7b4f`. Their failures there show
  the capability was missing, not a behavioural kill. The native-argument PY-001 control is a
  behavioural kill.

## Resolutions

| Finding | Resolution |
|---|---|
| PY-001 cross-argument stages | `validate_arguments` runs stage 1 over **all** arguments, then stage 2 over all, before any stage-3 rule. JSON-text arguments enter as `core.JsonText`, so the library, not the runner, owns precedence. SER-008 now states this reading of G-031 explicitly ("Stages across arguments"). A new scenario case (`stage-1 failure in b outranks stage-2 failure in a`) pins it for both languages. |
| PY-002 typed-field order | After the G-035 shape check, present typed fields are validated in canonical member order (`artifact_version` before `stable_id`), never by a priority list. Scenario and unit controls include member-order permutations. |
| PY-003 stage-1 source order | The input is cut at its first representation defect (invalid UTF-8 byte, raw surrogate). Any parse failure reaching that point reports the cutoff error, so an earlier escaped surrogate or duplicate wins. The surrogate-pair lookahead no longer raises: an unpaired high escape is reported before a malformed following escape. All three review witnesses are controls; `"\ud800\uZZZZ"` is also a scenario case. |
| PY-004 diagnostics | No rejection detail uses `repr` of an arbitrary value. `errors.describe` is bounded and non-recursive (integer bit length, truncated strings, container sizes). `10**5000` and 100,000-deep wrong-type inputs keep their codes, and a 1,000,000-character ID gives a message under 500 characters. |
| PY-005 → G-035 | CORE-003's closed record: required `stable_id` and `projection`, optional `artifact_version`. Shape errors (non-object, missing or extra member) are `artifact.revision_invalid`; present fields are then validated in canonical order; `not_applicable` only after full validation. Contract text: CORE-003 and the SER-008 stage-3 row. Eight scenario cases. |
| PY-006 → G-036 | `list` and `tuple` are the Python native array binding; other sequences stay `value.unsupported_type`. Contract text: SER-008 "Native array binding". The old unit test expecting tuple rejection was updated to `range`. |
| PY-007 raw content hash | `core.raw_content_hash(bytes)` returns SHA-256 over bytes exactly as given, while `content_hash` keeps structured semantics. A new scenario `core.serialization.raw-content-hash` has 7 cases (CRLF vs LF, NFC vs NFD, empty, binary), with expectations from `hashlib`. |

**Reading 1** (extra operation-identity members rejected) was accepted by Codex as path A, and is
unchanged.

## Scenario generator hardening (found by the corpus gate during this pass)

- **Aliases.** A shared revision object was emitted as YAML anchors and aliases. Each document now
  round-trips through JSON before dumping.
- **Ambiguous plain scalars.** The JSON text `1e400` was emitted as a plain scalar that YAML
  1.2-core reads as infinity. Strings that YAML 1.2-core could resolve as non-strings are now
  quoted.
- **No expectation changed.** Both were caught by `check conformance`, and the corpus diff is
  insertions only.

## Evidence (Windows, project-local CPython 3.12.8)

- `ruff`, `ruff format --check` and `mypy --strict` are clean.
- `pytest`: **83 passed, 5 placeholder expected failures**. All 8 Layer 01 scenarios pass through
  the public API.
- `check --deep-sources` 8/8 against this docs tree.
- No POSIX run is claimed for this pass.
