# WP-01 — Python Layer 01 implementation record (Claude)

**Contract:** the agreed checkpoint at docs `62adec5f` / code `860e91c1` (Codex APPROVED
`154b4164`). **Implementation:** code `f10c7b4f1c22b4daed4b6bc2f05028b5467a6ce9`, package
`minion_memory.core` in `minion-memory-python`.

This is an implementation record, not a review.

## Public API (`minion_memory.core`)

| Function | Contract |
|---|---|
| `decode_json(text)` | SER-008 stage 1 (strict RFC 8259, source order), then stage 2 |
| `validate_value(native)` | SER-008 stage 1 native kinds, then stage 2 |
| `canonical_bytes`, `content_hash` | SER-009, CORE-011 |
| `validate_stable_id` | CORE-001 (G-020) |
| `validate_version`, `compare_versions` | CORE-002 (G-012, G-023) |
| `compare_artifact_revisions` | CORE-003 Layer 01 comparison (G-021) |
| `operation_identity`, `compare_operation_identities`, `OperationIdentity` | CORE-012 (G-032, G-033) |
| `normalize_timestamp` | HIST-004 (G-022, G-026, G-028 to G-030) |

Every rejection is a `MnemeValidationError` with one stable `code`, plus `argument` for
multi-argument primitives (G-031, G-034). Runtime dependencies: none.

## Design notes

- **Own canonicalizer.** The RFC 8785 serializer is implemented in-package: UTF-16 code-unit key
  order and ECMAScript number formatting from the shortest round-trip digits. The `rfc8785`
  reference library is a **dev-only test oracle**: canonical bytes are compared with it on 20,000
  random binary64 values and 2,000 random string/key objects. It is never used to produce results.
- **Own decoder.** The JSON decoder is a strict, iterative RFC 8259 parser.
  - The stdlib `json` cannot report the first violation in source order: it decodes lone-surrogate
    escapes and resolves duplicates per object.
  - Raw surrogate code points in `str` input are `value.invalid_json`, the analogue of invalid UTF-8
    bytes.
- **Total on depth.** Decoding, the domain walk, normalization and serialization are iterative;
  100,000-deep nesting is a tested positive. (A recursive normalization step was caught by that test
  and replaced before commit.)
- **Stage order across arguments.** Stages 1-2 run over every argument (declared order) before any
  stage-3 rule.
- **Scenarios active.** The Layer 01 canonical scenarios are now `ACTIVE`. The runner maps each
  operation to one public function and implements no semantics.

## Implementation-level readings (please challenge)

These fill gaps the contract leaves open without a decision. Each one rejects rather than accepts,
and none is pinned by a canonical scenario:
1. An operation identity with **extra members** is `operation_identity.invalid`. I read "wrong shape"
   (CORE-012) as "exactly the two members".
2. A revision record (CORE-003 comparison input) missing `stable_id` or `projection` is `id.invalid`.
   The contract defines no code for a malformed comparison input; `projection` content itself is
   unrestricted.
3. **Native kinds.** A tuple is `value.unsupported_type` (only `list` is an array). A native map with
   a non-string key is reported at that map before its members, since canonical ordering is
   impossible there.

If any reading is judged an observable choice, it should go to the Owner (path C), not be kept
silently.

## Evidence (Windows, project-local CPython 3.12.8)

- **Python package:**
  - `ruff` and `ruff format --check` clean; `mypy --strict` clean (9 source files);
  - `pytest`: **46 passed, 5 expected failures**. The expected failures are the TO_BE_ placeholders
    of other layers. All 7 Layer 01 scenarios pass through the public API.
- **Docs validator:** `check --deep-sources` 8/8. The manifest records Python locations for
  CORE-001/002/003/011/012, SER-008/009 and HIST-004.
- **Not claimed:**
  - No POSIX run of the Python package.
  - No Layer-04 behaviour: persistence, retry and commit.
