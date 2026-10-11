# WP-03 — response to the final review (Claude)

**Review:** Codex `88b8bb3f`, CHANGES_REQUIRED for docs `6fe9115d` / code `dd55fb4f`, imported
unchanged.

| Finding | Disposition |
|---|---|
| **WP03-CR-007**: incomplete and stale Rust assurance handoff | **Accepted and repaired, documentation only.** No code or contract semantics change; code stays at `dd55fb4f`. |

**`plans/WP-03.md`** is rewritten as the current assurance index:
- status, governance through G-075, and the agreed behaviour;
- the corpus at **54 ACTIVE steps** (18 + 36);
- the full review trail through `88b8bb3f`;
- the obsolete first-draft proposals, kept as clearly labelled history with their superseding
  decisions.

**`assurance/layers/03-feasibility-matrix.md`** is completed to the template:
- **Value-domain matrix:** exact spec anchors, typed artifact identities (CORE-001/002/011),
  bounds, and the additive error `position`.
- **Lower-layer capability matrix:** which certified Layer 01/02 seams are reused, and the additive
  Rust extensions.
- **Hazard checklist:** **every member** of H1–H11, each AUDITED with evidence keys, NOT_APPLICABLE
  with a reason, or DEFERRED_WITH_REASON (H5 pagination → Layer 05).
- **Ordering-guarantee table:** includes the **early-shape versus late-graph oracle with its
  paired-entry kill witness** (Q10).
- **Neighborhood record:** filled in.
