# Owner decision — Layer 04 certification (2026-10-13)

Recorded verbatim by Claude. This is the governance source for certifying Layer 04 (WP-04, the
canonical history store). Acceptance onto `main` is under G-009. WP-04T (storage tiers, enrichment
ordering, local-first, assets) remains its own open work package.

## G-099 — Certify Layer 04 (WP-04; Python + Rust, cross-language)

> **Q:** Layer 04 (WP-04, canonical history store) now has:
> - contract and Python accepted (main 9d5a2d51 / f887f6ac, Codex final re-review 54d3f94b);
> - Rust APPROVED by my independent closure review 2 (996154b3) and accepted onto main under G-009
>   (code 220c6f28 / docs b45018d6).
>
> All 18 WP-04 findings are closed, and CE-04-01 is settled under G-088..G-098. The [IT]
> cross-language tests passed in both directions. Should WP-04 be certified for Python and Rust and
> closed (as G-076 did for Layer 03)?
>
> **A:** "Certify and close (Recommended)"

**Accepted pair (G-009):** code `220c6f285744fd52736cbd20f22105e9f33a5dce`, docs
`b45018d67f2e5e861ec6aa458b3d94efd968e7e2`.

**Exact-tree containment checks, run before certification:**
- **Python, corpus and pins.** In code `220c6f28`, `minion-memory-python/` (tree `f2b5617416dd`),
  `conformance/` (tree `a4eb09669561`) and `reference-backend/` (tree `557651f3745a`) are identical
  to the accepted WP-04 code `9d5a2d51`.
- **Rust.** `minion-memory-rust/` (tree `f8a532e2afe4`) is the tree at the code Claude's closure
  review 2 approved (`996154b3`).
- **Manifest.** Its delta touches only Rust `location` fields: 9 requirements, `null` →
  `minion-memory-rust/src/persistence/mod.rs`.
- **Docs.** In docs `b45018d6`, `spec/` (tree `8f845985a8d7`) and `reference/` (tree
  `fe39178f6687`) are identical to the accepted contract docs `f887f6ac`. The rest of the delta is
  records only.

**Approvals relied on, each from the agent that did not author the work:**
- **Contract:** Codex `67ba6632`, then the CE-04-01 checkpoint (`bfb6cad3`, `955d91f6`).
- **Python:**
  - Codex implementation reviews `bb3dfa2c` and `391fca64`;
  - CE-04-01 closures `779a8f21` and `46514f00`;
  - final review `eec44b3d`, then `54d3f94b`.
- **Rust:** Claude closure reviews `70f2a3e3` (CHANGES_REQUIRED: WP04-CR-017/018), then `996154b3`
  (APPROVED).
