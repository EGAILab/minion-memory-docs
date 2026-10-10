# Hand-off — WP-01 CE-01-01 characterization: Python native binding surface (Codex)

**From:** Claude (coordinator). **To:** Codex (independent characterization).
**Governs:**
- G-038, narrow convergence after trigger A;
- G-037, the subclass binding rule, now transcribed in SER-008 "Native subclasses";
- G-036, list/tuple arrays.

All are recorded verbatim in `reference/governance/2026-10-10-owner-layer01-decisions.md`.

**Findings in this episode:**

| Episode alias | Your finding | Review |
|---|---|---|
| WP01-CR-007 | WP01-PY-004 (diagnostics on admitted values) | `716d7218`, `2f50acc0` |
| WP01-CR-008 | WP01-PY-008 (subtypes serialize display text) | `2f50acc0` |

The aliases exist only because the state validator's agreed finding grammar (CE-P01-01 D12) is
`NF-NNN | WP…-CR-NNN`; your IDs stay authoritative in your records.

**Behaviour reference** (frozen during the episode):
- code: `eb47635c6ea997f030d04b8099366044a2f702aa` (`minion_memory.core`);
- contract: docs `wp01/contract` head, at the state commit carrying this hand-off.

Production code stays frozen until the checkpoint is AGREED.

## Asked: an exhaustive executed characterization of the native binding surface

Produce a behaviour matrix whose current cells are all executed against `eb47635c`, crossing:
- **Kinds:**
  - every admitted family (None, bool, `int`, `float`, `str`, `list`, `tuple`, `dict`);
  - representative standard subclasses (`IntEnum`, `IntFlag`, `NamedTuple`, `OrderedDict`,
    `defaultdict`, `str` enums);
  - hostile subclasses that override or raise in each relevant hook: `__repr__`, `__str__`,
    `__format__`, `__int__`, `__index__`, `__float__`, `__hash__`, `__eq__`, `__lt__`,
    `__iter__`, `__len__`, `__getitem__`, `items`, `keys`, `values`, `__contains__`,
    `__bool__`, `encode`, `is_integer`, `__abs__`, `__neg__`;
  - subclasses that add attributes or `__slots__`.
- **Operations:**
  - `validate_value` (stages 1–2, including error selection and canonical order);
  - normalization, canonical bytes and both hashes;
  - typed primitives receiving subclass values (version, stable ID, timestamp, operation
    identity, revision records), including their diagnostics;
  - `JsonText` paths where relevant.
- **Outcomes:** value or code; whether any user hook was invoked (instrumented); host exceptions;
  canonical-byte divergence from the base value.

For each row give the required behaviour under G-037/G-036 and SER-008, the realistic wrong
implementation, and the discriminating witness. Do not propose or make production changes. Record
anything G-037 does not decide as a candidate path-C item, not as a choice.

## Deliverable

`assurance/convergence/CE-01-01-characterization.md` on a new branch
`review/wp01-ce1-characterization` from the docs state head. Then I challenge its completeness and
classify every row; your separate approval of my classification makes it AGREED FOR
IMPLEMENTATION.
