# Hand-off — WP-03 Rust implementation (Codex)

**From:** Claude (coordinator). **To:** Codex (Rust owner). **State:** `RUST_IMPLEMENTATION`.

## Accepted baseline

WP-03 was accepted under G-009 on your APPROVED `165b07da`:
- **docs `main`:** `c36e0f5cb6dc2e7e92327bb9db358af0cdd31995`;
- **code `main`:** `dd55fb4f0abec262d7ba0dab64f28a74840b84c3`.

## Authority

Your authority is the **accepted contract and the canonical corpus**, not the Python
implementation:
- `spec/core.md`: HIST-006, HIST-007 (lineage), PROJ-001 (HistoryProjector) and PROJ-002;
- the SER-008 stage-table rows;
- Owner G-066…G-075;
- the two ACTIVE scenarios `conformance/core/projection-*.yaml` (54 steps);
- `assurance/layers/03-feasibility-matrix.md`.

The matrix's lower-layer and ordering tables list what Rust needs:
- the additive optional error `position`;
- the routing-triple detail for `unknown_required`;
- iterative graph checks;
- the early-versus-late lineage seam, with its paired-entry witness.

## Asked

1. Implement Layer 03 in `minion-memory-rust` on a new code branch `wp03/rust` from code `main`,
   with the project-local Cargo setup.
2. Add the `project_history` runner operation, including `position` in observations; raise Rust's
   `IMPLEMENTED_LAYER` to 3; add the Rust manifest locations.
3. Meet the Rust gates. Write an implementation record on a docs branch `wp03/rust` from docs
   `main`. Do not edit `process/state/` or the registry.
4. Hand the exact Rust candidate to Claude for CLOSURE_REVIEW.

Raise any contract gap as a finding, not a guess.
