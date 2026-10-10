# Hand-off — WP-01 Layer 01 CONTRACT_REVIEW (Codex)

**From:** Claude (contract author). **To:** Codex (independent reviewer, Rust owner).
**Governs:**
- G-019: parallel authoring, serial governance. WP-P01 is now CLOSED, so this review may start.
- G-012…G-026: Owner Layer 01 decisions, recorded verbatim in
  `reference/governance/2026-10-10-owner-layer01-decisions.md`.

## Exact candidate

- **docs:** `bbb61195713ddc4ad3819dfd0844ec5a6f5c6f9c` on `wp01/contract`, rebased onto the closed
  WP-P01 process (`5660f160`); the state-only descendants follow it.
- **code:** `ea61ffb19784a5cba2bbdacfa35f1e240fe0d412` on `wp01/contract`, branched from code
  `main` (`bb05e395`).

The worktrees are `review-worktrees/docs-wp01` and `review-worktrees/code-wp01`. Please review a
separate checkout of the exact SHAs, not those worktrees.

## Scope

Layer 01 contract only, as listed in `plans/WP-01.md`:
- `spec/core.md`: CORE-001, CORE-002, CORE-003, CORE-011, CORE-012 and HIST-004;
- `spec/serialization.md`: SER-008 and SER-009;
- the DRAFT canonical scenarios in `conformance/core/` and their manifest rows;
- `assurance/layers/01-feasibility-matrix.md` and `assurance/layers/01-probes/`;
- findings NF-010…015, NF-019 and NF-022…025.

## What is asked

Challenge the contract; do not confirm it. In particular:
1. **Fidelity.** Does each contract paragraph state exactly what its Owner decision says, without
   narrowing it, widening it or adding a choice? An addition the Owner never made is a path-C
   defect, not a convenience.
2. **Completeness for two independent implementations.** Could a Rust implementer build
   CORE-001/002/011/012, HIST-004, SER-008 and SER-009 from the text and scenarios alone, without
   reading Python? Name every place where a reader would have to guess.
3. **Scenario oracles.**
   - Canonical bytes and hashes come from the RFC 8785 reference library (`rfc8785` 0.1.4)
     and SHA-256. Re-derive them yourself; do not trust the generator.
   - The ID, version and timestamp expectations come from the decision text. Check each one
     against the decision.
   - The error codes (`value.*`, `version.invalid`, `id.invalid`, `timestamp.invalid`) are a
     proposed vocabulary. Is it sufficient and unambiguous?
4. **Cross-language feasibility, as Rust owner.**
   - `serde_jcs` 0.1 is recorded as non-conformant. Verify, and say what a conformant Rust
     canonicalizer needs.
   - Check whether the one-numeric-kind, whole-number-bound and timestamp-normalization rules are
     expressible losslessly in Rust (`serde_json` `Number`, `i64`/`f64`, a time type).
5. **Seams.** Does the contract say at which seam each rejection or normalization happens?

## Verdict

Record `assurance/reviews/WP-01-contract-review-codex.md` on a new branch
`review/wp01-contract-1` from the docs state head. Use exactly one of:
- `APPROVED`: contract checkpoint; Python may then implement Layer 01 against it;
- `CHANGES_REQUIRED`: findings classified per `process/finding-taxonomy.md`, path C marked
  `owner_decision_required`.

Approval is not acceptance. Do not edit the candidate.
