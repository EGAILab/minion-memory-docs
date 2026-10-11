# Owner decision — Layer 03 certification (2026-10-11)

Recorded verbatim by Claude. This is the governance source for certifying Layer 03 (WP-03).
Acceptance onto `main` is under G-009.

## G-076 — Certify Layer 03 (WP-03; Python + Rust, cross-language)

> **Q:** Layer 03 (WP-03: canonical HistoryProjector + lineage) is complete in both languages.
> Python was approved by Codex (implementation review + re-review, final review + re-review); I
> approved Codex's Rust Layer 03 (0 disagreements in 140k generated cases incl. 47k successful
> projections; 12/12 of my planted bugs killed; Windows + Linux). I'll accept the Rust pair onto
> main under G-009 after the same exact-tree containment checks as Layer 02. Certify Layer 03 and
> close WP-03?
>
> **A:** "Certify and close (Recommended)"

**Accepted pair (G-009):** code `e9a94f78c8d1a44281bab1902f0c5af76d0deb9c`, docs `ce904f4f6d63edfa864effe2bc6aebbdec5f4817`.

**Exact-tree containment checks, run before certification:**
- **Python and corpus.** In code `e9a94f78`, `minion-memory-python/` (tree `557a5a4ff707`) and
  `conformance/` (tree `a2f11b8b53e5`) are identical to the accepted WP-03 code `dd55fb4f`.
- **Rust.** `minion-memory-rust/` (tree `ccca43817078`) is the tree Claude's closure review
  approved (`afe48dc5`).
- **Manifest.** Its delta touches only Rust `location` fields.
- **Docs.** In docs `ce904f4f`, `spec/` and `reference/` are identical to the accepted contract docs
  `c36e0f5c`. The rest of the delta is records only.

**Approvals relied on, each from the agent that did not author the work:**
- **Python:** Codex `7d328f95`, then `2df90f22`; final review `88b8bb3f`, then `165b07da`.
- **Rust:** Claude `afe48dc5`.
