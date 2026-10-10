# Hand-off — WP-02 Rust implementation (Codex)

**From:** Claude (coordinator). **To:** Codex (Rust owner). **State:** `RUST_IMPLEMENTATION`.

## Accepted baseline

WP-02 was accepted under G-009 on your APPROVED `80d01123`:
- **docs `main`:** `6541f33a989da531cc2f21c6b3169b962c45d808`;
- **code `main`:** `ff9d132ada35a604c6f4bc7f11504b229afece6e`.

## Authority

Your authority is the **shared contract and the canonical corpus**, not the Python implementation:
- `spec/core.md`: HIST-001, HIST-002 (envelope and gates), HIST-005 (HistoryBoundary), HIST-010;
- `spec/serialization.md`: SER-005 (reader, replay admission) and SER-006, plus the SER-008 stage
  table rows and the G-055 gated rule;
- Owner G-047…G-055 in `reference/governance/2026-10-11-owner-layer02-start.md`;
- the four ACTIVE scenarios `conformance/core/history-*.yaml` (70 steps);
- readiness guidance in `assurance/layers/02-feasibility-matrix.md`.

## Asked

1. Implement Layer 02 in `minion-memory-rust` on a new code branch `wp02/rust` from code `main`,
   using the project-local Cargo setup.
2. Add the three runner operations, raise the Rust runner's `IMPLEMENTED_LAYER` to 2, and add the
   Rust manifest locations.
3. Meet the Rust gates. Write an implementation record on a docs branch `wp02/rust` from docs
   `main`. Do not edit `process/state/` or the registry.
4. Hand the exact Rust candidate to Claude for CLOSURE_REVIEW.

Out of scope: MemoryScope (WP-02S, still in Python review) and Layer 03+. Raise any contract gap as a
finding, not a guess.
