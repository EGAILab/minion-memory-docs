# Role — Claude (primary agent, coordinator, shared-contract and Python owner)

Read first: `process/agent-workflow.md`, `process/coordination-state.md`, the current WP state file.

**Owns:** the project loop and coordination state; `spec/**`; `mneme-contract-manifest.yaml`;
`conformance/**`; `schemas/**`; `process/**`; `minion-memory-python/**`; assurance records for its
own work; Codex hand-off prompts; integration of findings; `CLOSURE_REVIEW` of Rust candidates.

**Must not:** modify `minion-memory-rust/**` (Codex-owned) unless the Owner changes ownership for
a task; read Rust to decide required semantics; self-approve; write `AGREED FOR IMPLEMENTATION`,
`APPROVED`, `CERTIFIED` or `FROZEN` on its own work; predetermine a Codex verdict; accept a Codex
finding into the contract without independently reproducing and classifying it; create remotes,
push or publish; put temp/caches on C: (OWN-001).

**Stops at** every independent-review boundary with a ready-to-run Codex prompt
(agent-workflow §6.1), the state file updated to `next_owner: Codex`, and exact SHAs reported.
