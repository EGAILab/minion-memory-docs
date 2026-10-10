# Owner decision — WP-01 certification (2026-10-11)

Recorded verbatim by Claude from the Owner's AskUserQuestion answer. This is the governance source
for certifying Layer 01; acceptance onto `main` itself is under G-009.

## G-044 — Certify Layer 01 (Python + Rust, cross-language)

> **Q:** WP-01 (Layer 01) has independent approvals for both languages: Codex approved the Python
> (final review + re-review), I approved Codex's Rust, and Codex approved my corpus fix. All findings
> are closed and both suites pass on the final pair. I'll accept it onto main under G-009. Should
> the registry also mark Layer 01 CERTIFIED (Python + Rust, cross-language CERTIFIED_CLOSED)?
>
> **A:** Certify now (Recommended) — "Each language is certified on the other agent's independent
> approval, never its author's. I record your answer as the governance source and set Python/Rust
> CERTIFIED and cross-language CERTIFIED_CLOSED at the accepted pair."

**Scope.** WP-01 only, at the accepted pair: code `cc3c5d549a43f166bfa1d990d3363887d5e63774`, docs `71e2b12e65ae420ecd4fc9cd5579056e5d7d96a6`.

**Approvals relied on.** Each language's approval comes from the agent that did not author it:
- **Python:** Codex final review `e340e439` and re-review `2a4a4c69`. The Python code is unchanged
  since `bac6594e`.
- **Rust:** Claude closure review `b1065af9`, completed in `689efef9`.
- **Shared corpus repair:** Codex `c73593d6`.
