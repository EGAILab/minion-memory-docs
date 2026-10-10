# Hand-off — WP-01 Rust implementation (Codex)

**From:** Claude (coordinator). **To:** Codex (Rust owner). **State:** `RUST_IMPLEMENTATION`.

## Accepted baseline

WP-01 was accepted onto `main` under G-009 after your APPROVED re-review `2a4a4c69`:

- **docs `main`:** `83c66c25d560accb3d57ba20be631d55faab72ff`;
- **code `main`:** `bac6594e06dd321e547e917cebeeefc6562a19b9`.

## Authority

Your authority is the **shared contract and the canonical corpus**, not the Python implementation
(`process/agent-workflow.md` §3, step 10):

- `spec/core.md`: CORE-001, CORE-002, CORE-003, CORE-011, CORE-012, HIST-004;
- `spec/serialization.md`: SER-008, SER-009;
- Owner decisions G-012…G-043 in `reference/governance/2026-10-10-owner-layer01-decisions.md`;
- the 8 ACTIVE scenarios in code `conformance/core/*.yaml` and `mneme-contract-manifest.yaml`;
- readiness guidance in `assurance/layers/01-feasibility-matrix.md`. This guidance includes the
  staged-decoder requirement with your witness `{"a":1e400,"b":1,"b":2}` → `value.duplicate_key`,
  UTF-16 member ordering, and the HIST-004 grammar placed in front of any time library.

Python is not an oracle. If the contract text is insufficient, raise a finding against the
contract rather than reading the answer from Python.

## Asked

1. Implement Layer 01 in `minion-memory-rust`, which currently holds only a README. Bootstrap the
   workspace/crate as you judge best, on a new code branch `wp01/rust` from code `main`. Use a
   worktree under `review-worktrees/`, with Cargo home and target kept project-local (OWN-001).
2. Build a thin Rust conformance runner over the same ACTIVE scenarios, and add the Rust locations
   to the manifest.
3. Meet the Rust gates in `process/gate-tiers.md` for a candidate going to CLOSURE_REVIEW.
4. Write an implementation record under `assurance/reviews/` on a docs branch `wp01/rust` from
   docs `main`. Do not edit `process/state/` or the registry; Claude updates them.
5. Hand the exact Rust candidate pair to Claude for `CLOSURE_REVIEW`. Claude did not author the
   Rust candidate, so Claude reviews it.

Out of scope: Layer 02+, persistence, provenance storage, durable commits, and any change to Python.

**Not delegated:** a semantic or scope question goes to the Owner through Claude.
