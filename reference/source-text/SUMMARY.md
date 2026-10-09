<!-- DERIVED, NON-AUTHORITATIVE reading aid. Source: UPDATE_SUMMARY.md sha256:eff957c5109cdb04ed8da9210383450537dc09da7efb0efbf77ac0d0f7ecb989. Regenerate with `mneme-process sources build`; never edit by hand. -->

# Project Mneme dual-profile documentation update — 2026-10

This revision promotes **Minion-Agent long-term memory** to a primary Project Mneme use case alongside human learning.

## Version set

- Foundation v2.3 — dual-profile architecture
- MVP Contract v1.2 — shared core + Learning and Agent Memory profiles
- Flashcard Requirements 00–03 v2.3 — explicitly Learning Profile
- Requirement 04 v1.3 — learning persistence + shared-core compatibility boundary
- Requirement 05 v1.0 — Agent Memory Profile & Minion-Agent Integration
- Implementation Architecture Amendments v1.3
- Codex Implementation Pack v1.3
- Bootstrap Prompt v1.1

## Core architecture change

Mneme is no longer rooted in learner-specific entities. Shared core is limited to cross-profile semantics such as identity/version/provenance/lineage, MemoryScope, canonical history, artifacts, projections/budgets, replay/checkpoints, retrieval primitives, persistence/backup/compatibility.

Learning-specific Knowledge/learning/evidence/scheduling semantics stay in the Learning Profile. Agent capture/consolidation/retrieval/context semantics stay in the Agent Memory Profile.

## Minion-Agent boundary

Minion-Agent authoritative SessionStorage/history remains separate from Minion-Memory long-term memory. Integration uses an adapter: pre-request scoped retrieval -> AgentContextProjection -> Minion-Agent prompt/header memory component; post-turn idempotent capture -> AgentMemoryObservation -> async consolidation/indexing. Injected/recalled memory is fenced to prevent recursive self-reinforcement.

## Implementation program

The Codex pack now targets a dual-language Python/Rust Minion-Memory engine using the Minion-Agent process discipline: shared normative contract, canonical conformance, Python-leading, independent review, Rust-independent implementation, exact-SHA handoffs, and G0-G3 gates.
