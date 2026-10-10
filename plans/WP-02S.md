# WP-02S — Layer 02: MemoryScope

**Status:** `CONTRACT_REVIEW`. **Governance:** G-046, G-047 (`reference/governance/2026-10-11-owner-layer02-start.md`); G-056…G-063 (`reference/governance/2026-10-11-owner-wp02s-memoryscope.md`).
**State:** `process/state/WP-02S.yaml`.

## Scope

SCOPE-001…006 and NF-018. The sources fix that MemoryScope exists in the core, is structured and
extensible, has profile-owned vocabulary and is enforced before ranking. They do not fix identity,
equality, containment, inheritance, facet intersection, retrieval visibility, encoding or privacy
defaults.

## Plan (G-047)

1. Characterize: an authority audit of every cited source, recording what is decided (path A/B)
   and what is an observable choice (path C).
2. Prepare **one consolidated Owner-decision packet**: options, consequences and a recommendation
   for each path-C question.
3. Contract draft after the decisions.

WP-02S never blocks WP-02. Work that consumes scope semantics declares `blocked_by: WP-02S`.

## Progress

- **Characterization.** `assurance/layers/02s-memoryscope-characterization.md`: 93 verbatim
  passages; the key quotes were spot-checked.
- **Owner packet.** `assurance/layers/02s-owner-decision-packet.md` (D1–D8), decided as G-056…G-063.
- **Contract draft.** `spec/scope.md` Layer 02 MemoryScope contract: value, vocabulary, matching,
  errors and conformance. Also the path-A source omissions O1–O14 and the homonym note.
- **Corpus (DRAFT).** `core.scope.value-shape`, `applicability-matching` and
  `agent-isolation-six-dimensions`: 69 steps.
- **Feasibility.** `assurance/layers/02s-feasibility-matrix.md`.
- **Consumers.** The retrieval layers (06, 15), agent capture (13), agent consolidation (14) and the
  learning layers (07–12) consume these decisions and declare `blocked_by: WP-02S`.
