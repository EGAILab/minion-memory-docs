# Owner decision — Layer 02 certification (2026-10-11)

Recorded verbatim by Claude. This is the governance source for certifying Layer 02 (WP-02 and
WP-02S). Acceptance onto `main` itself is under G-009.

## G-065 — Certify Layer 02 (WP-02 and WP-02S; Python + Rust, cross-language)

> **Q:** Layer 02 is complete in both languages: WP-02 (history envelope) and WP-02S (MemoryScope).
> Python was approved by Codex (final review + re-review for WP-02; review + rebase confirmation for
> WP-02S); I approved Codex's combined Rust Layer 02 (0 disagreements in 240k generated cases, 13/14
> planted bugs killed, the 14th proven equivalent; Windows + Linux). I'll accept the Rust pair onto
> main under G-009. Should Layer 02 be marked CERTIFIED (Python + Rust, cross-language
> CERTIFIED_CLOSED) and both WPs closed?
>
> **A:** "Approve Option 1.After the G-009 acceptance and exact-tree containment checks, certify and
> close WP-02 and WP-02S in both languages. Record Python and Rust as CERTIFIED, each WP’s
> cross-language state as CERTIFIED_CLOSED, and Layer 02 overall as cross-language CERTIFIED_CLOSED
> at the exact accepted code/docs pair.Downstream retrieval, capture, consolidation and integration
> work is not a prerequisite for Layer 02 certification. Any later evidence of a shared-contract
> defect triggers a narrowly scoped post-certification delta audit rather than preventing present
> closure."

**Accepted pair (G-009):** code `a5506d0ddd98af33be4d9ec87305b10000febf4d`, docs
`620c512c5d19cb3e3ff73037d6016b50a1a605cc`.

**Exact-tree containment checks, run before certification:**
- **Python and corpus.** In code `a5506d0d`, `minion-memory-python/` (tree `47c9e8b0cfcd`) and
  `conformance/` (tree `a1b6fbd0a7de`) are identical to the approved and accepted WP-02S code
  `609dad7b`. That code contains WP-02's approved `ff9d132a` plus WP-02S, unchanged.
- **Rust.** `minion-memory-rust/` (tree `eee0b1941d1d`) is the tree Claude's closure review
  approved (`7283141d`).
- **Manifest.** Its delta from `609dad7b` touches only Rust `location` fields.
- **Docs.** In docs `620c512c`, `spec/` and `reference/` are identical to the accepted contract
  docs `36d02298`. The remaining delta is records only: the Codex implementation record, the WP-02S
  post-acceptance records and state.

**Approvals relied on, each from the agent that did not author the work:**
- **WP-02 Python:** Codex `b910a244`, then `80d01123`.
- **WP-02S Python:** Codex `b24c9b8e`, then `e45efdee`.
- **Rust Layer 02 (both WPs):** Claude `7283141d`.
