# WP-00 — Dual-profile architecture review (kickoff §6, §17, §18)

**Author:** Claude. Self-authored scoping analysis; independent review pending.

## 1. Core admission test

Each candidate core concept, tested against ARCH-002 ("both profiles consume it without
distortion; reuse alone is insufficient"):

| Concept | Learning use | Agent use | Distortion risk | Verdict | Spec |
|---|---|---|---|---|---|
| Stable identity / version / provenance / lineage | Knowledge artifacts, episodes, interpretations | observations, MemoryRecords, projections | Conflict rule (CORE-003) is stated only for Knowledge; MemoryRecord versioning semantics differ (NF-012) | CORE, with the conflict rule's scope open | CORE-001..011 |
| Operation identity / idempotency | review commit | capture by operation/source identity | none observed; domain open (NF-014) | CORE | CORE-012, PERS-006 |
| MemoryScope | learner/course/collection facets | principal/agent/workspace/conversation/session/task | real: agent scope is a privacy boundary; learning scope is illustrative only. Shape shared, vocabulary profile-owned | CORE (shape only) | SCOPE-001..006 |
| Canonical history + order + append-only reinterpretation | LearningEpisode/Event, evaluations, evidence | AgentMemoryObservation; consolidation lineage | "No semantic dedup" must not be weakened by agent consolidation (ACON-007) | CORE | HIST-001..010 |
| Information origin | exposure provenance (hints, reveals) | context fencing (recalled/injected memory) | Must not merge into one type (ARCH-005); principle shared, mechanisms profile-owned | CORE principle + profile mechanisms | HIST-010, OBS-006, ACTX-004 |
| Projection path / purpose-specific projection / ProjectionBudget | scheduling/diagnostics views | AgentContextProjection | Budget units (tokens) are consumer-specific (NF-017) | CORE | PROJ-001..005 |
| Retrieval primitives / indexes / progressive disclosure | Knowledge lookup, diagnostics | memory retrieval | Semantic search must not substitute for learner truth (RET-006) | CORE | RET-001..006 |
| Persistence tiers, durability barrier, bounded history, checkpoints | review history | capture | Checkpoints must never cross profiles (PERS-011) | CORE | PERS-001..016 |
| Backup / serialization / privacy | full backup | memory export | profile/type identity explicit (SER-006, BKP-004) | CORE | SER, BKP, PRIV |

**Rejected as core** (stay profile-owned, per FND §G.1 and ARCH-003): KnowledgeUnit/Component,
RecallForm, LearningEpisode, RawObservation, EvaluationOutcome, MemoryEvidence, LearnerMemoryModel,
SchedulingPolicy (learning); AgentMemoryObservation, MemoryRecord, ConsolidationOutcome,
RetrievalQuery ranking policy, AgentContextProjection (agent). No universal `Memory` entity.

## 2. Invariant protection (kickoff §17 U, V)

- **U (core needs no learner semantics):** no CORE/HIST/PERS/RET requirement references a
  learning-only type except as an example; ARCH-006 (layer separation) is profile `learning`.
- **V (agent simplification must not weaken learning):** HIST-008 binds both profiles; ACON-007
  states consolidation of derived MemoryRecords never relaxes it; ARCH-002 requires shared
  primitives to preserve the richer provenance of both.

## 3. MemoryScope investigation (kickoff §18)

The sources answer only *existence*, *structure/extensibility*, *profile-owned vocabulary*, the
*agent dimensions* and *enforcement before ranking*. They do not answer identity, containment,
inheritance, intersection, retrieval visibility, persistence encoding, privacy defaults or
cross-language representation — and do not say whether hierarchy exists. Per the kickoff ("do not
assume hierarchy until reviewed") nothing was assumed; NF-018 carries the full question list into
Layer 02, which should run a contract-first checkpoint with an options packet for the Owner.

## 4. Dependency observation

Agent layers (13–16) consume only core layers (01–06). Learning layers (07–12) likewise. The two
profiles are therefore independently schedulable after Layer 06 (NF-005).
