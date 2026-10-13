# Hand-off — WP-04 Rust implementation (Codex)

**From:** Claude (coordinator). **To:** Codex (Rust owner). **State:** `RUST_IMPLEMENTATION`.

## Accepted baseline

WP-04 was accepted under G-009 on your APPROVED final re-review `54d3f94b`, after final review
`eec44b3d` and CE-04-01 closure `46514f00`:
- **docs `main`:** `f887f6ac94973a9c2fa4f4413bc8b4a16b50acd8`;
- **code `main`:** `9d5a2d51c69987f799962868b8dc5175a11882d2`.

## Authority

Your authority is the **accepted contract, the shared pins and the canonical corpus**, not the
Python implementation:
- `spec/persistence.md`, "Layer 04 canonical history store contract (WP-04)", with its reference
  backend, the v1 catalog contract and the trust scope;
- the SER stage-table rows, and the notes under HIST-008 and HIST-009;
- Owner G-077…G-098, plus G-013, G-031, G-033, G-051, G-054 and G-055;
- the agreed CE-04-01 checkpoint (`assurance/convergence/CE-04-01-classification.md`, revisions
  2–5);
- `reference-backend/postgres14-v1-catalog.json`. Embed it and test the embedding.
- the five ACTIVE store scenarios (65 steps);
- `assurance/layers/04-feasibility-matrix.md`.

The matrix lists what Rust needs: §2 for capabilities, §3a for the catalog surface with each row's
Rust obligation, §4 for ordering, and §6 for the verdict. The main items are:
- the additive Layer 02 draft-admission mode;
- the open protocol;
- the v1 catalog validation, including the whole-row member rule with its named exclusions and
  normalizations, and member text rendered as `jsonb::text`;
- genuine-object SQL;
- the witness classes [P] [T] [E] [Pr] [F] [INV] [PIN];
- the [CT] and **[IT]** cross-language tests, which are due now.

Implementation records 1 §6 and 2 §6 hold the Rust notes, such as the row layouts and the pin
rendering. They are notes, not an oracle.

## Asked

1. Implement Layer 04 in `minion-memory-rust` on a new code branch `wp04/rust` from code `main`,
   with the project-local Cargo setup and the PostgreSQL 14 reference backend. Use the project role
   only, and keep scratch and databases on E:.
2. Add the store runner operations. Raise Rust's `IMPLEMENTED_LAYER` to 4. Add the Rust manifest
   locations.
3. Execute the [IT] witnesses against the Python store, in both directions:
   - a store written by one language is read and retried by the other;
   - mixed-language concurrent and waiting first opens;
   - a schema initialized by one language is opened by the other;
   - a retry committed by one language returns the same receipt in the other.
4. Meet the Rust gates, with planted violations for the catalog and protocol witnesses. Write an
   implementation record on a docs branch `wp04/rust` from docs `main`. Do not edit
   `process/state/` or the registry.
5. Hand the exact Rust candidate to Claude for CLOSURE_REVIEW.

Respect the shared-host queue: start heavy cargo, test, mutant or Docker batches only when the host
queue allows. The #224 hold on new batches applies until its batch-done.

Raise any contract gap as a finding, not a guess.
