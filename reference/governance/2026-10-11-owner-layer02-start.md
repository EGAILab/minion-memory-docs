# Owner decisions — Layer 02 start and split (2026-10-11)

Recorded verbatim by Claude.

## G-046 — Start Layer 02

**Context.** WP-01 and WP-P02 were closed and accepted. Claude reported that the workflow does not
start the next layer automatically.

> **Owner:** "Start next layer"

**Scope.** Authorizes starting Layer 02 per `plans/layer-plan.md`. Python is at most one layer
ahead of Rust: Rust is certified at Layer 01, so Python Layer 02 is allowed.

## G-047 — Split Layer 02; envelope first; NF-016 constraint

> **Q:** Layer 02 holds two fairly independent surfaces: MemoryScope (SCOPE-001..006; needs several
> of your product decisions on visibility/inheritance, NF-018) and the history/compatibility
> envelope (HIST-001/002/005/010, SER-005/006; mostly resolvable from the sources, NF-016). How
> should I run it?
>
> **A:** "Choose 1 — Split, envelope first.
> Create WP-02 for the history/compatibility envelope and let it proceed immediately through
> contract draft and independent review. Create sibling WP-02S for MemoryScope. Start WP-02S
> characterization and prepare one consolidated Owner-decision packet in parallel, but do not let
> unresolved MemoryScope semantics block WP-02.
> Keep the dependency explicit: later work that consumes scope semantics must wait for WP-02S,
> while history/compatibility work may close independently.
> For NF-016, a per-store durable append position is a valid candidate resolution only as a local
> persistence/read cursor; it must not be interpreted as a global causal or cross-device event
> order."

**Effect.**
- **WP-02** is the history/compatibility envelope: HIST-001, HIST-002, HIST-005, HIST-010, SER-005
  and SER-006. HIST-004's Layer 01 timestamp grammar is consumed, not reopened. It proceeds through
  contract draft, independent review and the rest of the workflow, and may close independently of
  WP-02S.
- **WP-02S** is MemoryScope: SCOPE-001…006, with NF-018 characterization and one consolidated
  Owner-decision packet. Anything that consumes scope semantics declares `blocked_by: WP-02S`.
- **NF-016 constraint.** A per-store durable append position may resolve NF-016 only as a local
  persistence/read cursor. The contract must state that it is not a global, causal or cross-device
  event order, and it must never be used as one.
