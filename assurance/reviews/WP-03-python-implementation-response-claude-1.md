# WP-03 — response to Python implementation review 1 (Claude)

**Review:** Codex `7d328f95`, CHANGES_REQUIRED for docs `0e4e1bce` / code `c86daf80`, imported
unchanged.

| Finding | Disposition |
|---|---|
| **WP03-CR-006**: unknown_required projection errors omitted the routing profile | **Accepted and fixed** at code `dd55fb4f0abec262d7ba0dab64f28a74840b84c3`. The projector now builds the detail from the gate-1-validated record, as `(profile, record_type, schema_version) is required but not recognized`. The certified Layer 02 admission is unchanged, so this is not a Layer 02 reopening. |

**New controls** (`test_unknown_required_carries_position_and_full_routing_identity`):
- two profiles (`learning`, `agent`), each with an unknown type and with an unknown schema of a
  known type, across both the native and `JsonText` seams;
- each asserts position 7, no argument, and the exact triple;
- a separate control checks that early lineage errors still precede.

**Proof the controls discriminate.** With the profile omitted from the detail, **all 8 routing
controls fail**.

**Gates.** 496 passed, 5 xfailed; 985/985 statements and 432/432 branches; ruff and mypy strict
clean.
