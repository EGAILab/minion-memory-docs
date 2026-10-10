# WP-02S — Layer 02: MemoryScope

**Status:** `CLOSED`. Certified for Python and Rust, CERTIFIED_CLOSED, by Owner G-065 at code `a5506d0d` / docs `620c512c`.
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

## Assurance trail

| Step | Record |
|---|---|
| Contract reviews (Codex) | `2c2e1d08` (CHANGES_REQUIRED: CR-001, CR-002), `f3b86200` (CHANGES_REQUIRED: CR-003), `697e372c` (**APPROVED**) |
| Owner decisions | G-056…G-063 (packet), G-064 (facet names) |
| Python implementation | code `5d1a74a5`; `assurance/reviews/WP-02S-python-implementation-claude.md` |
| Python review (Codex) | `b24c9b8e` (APPROVED; S03 equivalence proven) |
| Rebase onto the accepted WP-02 mains | code `609dad7b`, docs `36d02298`; Codex confirmation `e45efdee` (APPROVED) |
| Acceptance | `main` = code `609dad7b` / docs `36d02298` (G-009); NF-018 closed |
| Rust Layer 02 (Codex) | code `a5506d0d`; `assurance/reviews/WP-02-rust-implementation-codex.md` |
| Rust CLOSURE_REVIEW (Claude) | `7283141d` (**APPROVED**); combined WP-02 + WP-02S |
| Acceptance and certification | `main` = code `a5506d0d` / docs `620c512c` (G-009); certified (G-065) after exact-tree containment checks |
