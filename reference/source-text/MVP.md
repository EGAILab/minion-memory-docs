<!-- DERIVED, NON-AUTHORITATIVE reading aid. Source: Project_Mneme_MVP_Contract_v1_2_Dual_Profile.docx sha256:5a28d40a0c3b859a5e81854d03a2480636c1833c9f5aa97cbac8bb393a650e2a. Regenerate with `mneme-process sources build`; never edit by hand. -->

PROJECT MNEME
MVP Contract v1.2
A General Memory Substrate with Learning and Agent Memory Profiles
Foundation-to-Implementation Boundary for the Minion-Memory Core and First Profile Integrations

| Purpose: Translate Project Mneme Foundation v2.3 into a deliberately small dual-profile implementation contract. The MVP proves the shared core through both the existing offline-first Flashcard learning experience and Minion-Agent long-term-memory integration without prematurely implementing every future memory capability. |
|---|


## 1. Contract Position
Project Mneme is broader than the current Flashcard App and broader than agent-memory retrieval. The implementation program now has two primary proving integrations: the Learning Profile used first by the Flashcard App, and the Agent Memory Profile used by Minion-Agent. The MVP contract therefore requires a small shared core plus profile-specific semantics; it does not require one universal memory object model.
Project Mneme Foundation v2.3
        ↓
MVP Contract v1.2
        ↓
Shared Memory Core
   ├─ Learning Profile → Flashcard Requirements 00–04
   └─ Agent Memory Profile → Requirement 05 / Minion-Agent adapter
        ↓
Python + Rust implementations / consumer integrations

### 1.1 Governing rule

| MVP rule: Simplify behavior, not semantics. A feature may be deferred, but the MVP must not encode assumptions that contradict or block the Foundation. |
|---|


## 2. MVP Product Goal
Deliver a robust offline-first Minion-Memory core with independently implementable Python and Rust semantics, while preserving the successful Flashcard review experience and enabling Minion-Agent to use the same core for durable long-term memory capture/retrieval through a separate Agent Memory Profile.
- Primary proving use case A: human learning, initially vocabulary and compact factual knowledge through the existing Flashcard App.
- Primary proving use case B: AI-agent long-term memory through Minion-Agent, including capture, scope, consolidation, retrieval, context projection, and anti-feedback provenance. Secondary learning examples remain formulas, timelines/ordered structures, and simple procedures.
- AI, Matrix integration, and Knowledge Builder remain optional producers/enhancements; none are required for core review or scheduling.
- The MVP optimizes for data durability, model replaceability, and migration safety before feature breadth.

## 3. Foundation Concepts the MVP MUST Implement

| Concept | MVP contract |
|---|---|
| KnowledgeUnit | Stable authored boundary for coherent presentation/review/provenance. Replaces the old core meaning of MemoryUnit. |
| KnowledgeComponent | Stable assessable knowledge identity referenced by a unit. MVP requires KnowledgePoint; schema must permit additional component kinds. |
| RecallForm | Authored retrieval activity semantics. MVP uses self-assessed front/back and may support typed response when already practical. |
| LearningEpisode | Bounded learner interaction session. A simple flashcard episode may contain only one substantive attempt. |
| LearningEvent | Ordered event record inside an episode. MVP needs a small typed vocabulary, not a universal event engine. |
| RawObservation | What the learner actually did/answered, retained when practical and privacy-appropriate. |
| EvaluationOutcome | What a deterministic/self evaluator concluded from the observation. |
| MemoryEvidence | Versioned/provenanced interpretation relevant to memory; must remain distinct from raw observation and learner state. |
| Stable identity/versioning | Opaque stable IDs; semantic edits use versions; semantic replacement/split creates new IDs and lineage where applicable. |
| Provenance | Knowledge and derived artifacts can record source/producer/generation/version information. |


## 4. MVP Knowledge Model
KnowledgeUnit
  ├─ references KnowledgeComponent[]
  │      └─ KnowledgePoint   ← implemented in MVP
  │
  ├─ RecallForm[]
  ├─ LearningSupport / Hint[]
  ├─ Collection membership[]
  └─ Asset references[]

### 4.1 Required now
- KnowledgePoint as the primary implemented component kind.
- Independent stable IDs for Unit, Component, RecallForm, Hint/Support, Collection, and Asset.
- Component membership/reference must not derive identity from filesystem path or Collection hierarchy.
- RecallForm declares the components it is capable of testing and the components it may expose.
- KnowledgeUnit and KnowledgeComponent semantics remain separate even if the first serializer stores unit-local components inline.

### 4.2 Reserved but not fully implemented
- KnowledgeStructure and KnowledgeProcedure are supported by the domain boundary but may be rejected/ignored with explicit capability reporting until renderers/evaluators exist.
- Cross-Unit canonical component reuse is permitted by the Foundation; the MVP does not need automatic deduplication or global canonicalization.
- Typed ComponentRelation graph is a future-compatible extension point; Collection hierarchy is not a substitute for it.

## 5. MVP Recall and Episode Model
RecallForm
   ↓ execute
LearningEpisode
   ├─ event #1 Prompt/Presentation context
   ├─ event #2 Attempt / Reveal / Rating
   └─ optional Hint / Exposure events
          ↓
RawObservation
   ↓
EvaluationOutcome
   ↓
MemoryEvidence
The MVP UI can remain the current simple front/back card. The domain record underneath it must nevertheless preserve the separation between authored activity, actual observation, evaluation, and memory evidence.

### 5.1 Minimum event vocabulary
- AttemptEvent — learner answer/rating submission.
- HintEvent — learner requested or system presented a hint.
- ExposureEvent — answer/support content was shown without claiming retrieval success.
- Completion/Abandon status — episode completion is distinguishable from skip/abandon.

| Ordering invariant: Events have deterministic sequence inside an Episode. occurred_at and recorded_at remain distinct concepts. The MVP does not require a global total order across devices or episodes. |
|---|


## 6. Evidence Contract
- A RecallForm's declared test coverage does not imply evidence was obtained for every declared component.
- Answer exposure is not successful retrieval evidence.
- Missing evidence remains unknown; it must never be silently converted to failure, zero, or forgotten.
- Again / Hard / Good / Easy is an MVP self-assessment signal, not a universal evidence ontology.
- Raw response should be retained for typed/structured interactions when practical and privacy-appropriate.
- Historical evidence carries enough provenance to identify the evaluator/evidence mapping version that produced it.
- Later reinterpretation may add new derived evidence; it does not rewrite the historical observation.

## 7. Learner Memory and Scheduling Contract
Durable learning history
       ↓
State Reducer / MemoryModel
       ↓
model-specific learner state
       ↓
SchedulingPolicy
       ↓
RecallForm / activity selection

### 7.1 MVP learner model
The initial implementation may retain simple point/unit-derived state and a fixed/adaptive scheduler. These are implementation models, not universal Mneme truth.
- Current learner state is rebuildable/materialized state, not historical source of truth.
- FixedIntervalStrategy remains supported for backward compatibility.
- Adaptive strategy may use Again/Hard/Good/Easy and locally derived retention state.
- Memory inference and scheduling policy remain separable even if one implementation module contains both initially.
- No AI dependency exists in the scheduling critical path.
- Unknown state is distinct from weak state.
- new / learning / review / relearning may be used as MVP lifecycle labels, but are not permanent Foundation ontology.

## 8. Import, Reconciliation, and Durability
Knowledge Package
  manifest.yaml
  memories/*.md   (MVP serializer name may remain for compatibility)
  assets/*
        ↓
Validate → Parse → Normalize Domain Model
        ↓
Match by stable ID → ChangeSet
        ↓
Transactional reconciliation → Local persistence
- Knowledge import is synchronization/reconciliation, never blind file overwrite.
- same ID + higher version → update; same ID + same version + same hash → unchanged; same ID + same version + different content → conflict.
- Absence only carries retirement/membership semantics within explicitly authoritative scope.
- Knowledge import cannot erase learner episodes/history.
- Retired knowledge remains interpretable for historical events.
- The external package is an interchange protocol, not the runtime database format.
- Knowledge Package, Learning Record Export, and Full Backup remain distinct protocols.

## 9. Privacy and Data-Minimization Boundary
Mneme values rich observations because future models can reinterpret them, but “store everything forever” is not a Foundation requirement. The MVP must preserve the richest observation reasonably useful for memory reconstruction while respecting explicit privacy, retention, and data-minimization choices.
- Do not require audio/video recording merely because future models might use it.
- Do not duplicate large binary assets per event; retain stable/versioned/checksummed references where sufficient.
- Free-text/work/professional content must remain local by default unless the user explicitly exports or enables an external evaluator.
- Derived caches may be deleted/rebuilt without deleting durable learner history.

## 10. Explicitly Deferred Foundation Capabilities

| Capability | MVP decision |
|---|---|
| KnowledgeStructure | Domain/schema extension point only; no requirement for rich grid/timeline/diagram renderer in MVP. |
| KnowledgeProcedure | Domain/schema extension point; no multi-step procedural tutoring engine. |
| ComponentRelation graph | No prerequisite/causal graph engine in MVP. |
| Cross-unit canonicalization | No global ontology deduplication service. |
| Learned EvidenceMapper | No ML/AI attribution model required. |
| MemoryAssembly | Research candidate only. |
| Context-conditioned learner models | No route/context-specific state required beyond data needed for future analysis. |
| QTI/xAPI/Caliper | Adapters deferred; internal model must not depend on them. |
| Model fitting/benchmark platform | Research infrastructure deferred. |
| General tutoring / understanding engine | Explicitly outside this MVP. |


## 11. Legacy Flashcard Mapping
Existing Card / Collection model
        ↓ migration adapter
KnowledgeUnit
  ├─ KnowledgePoint
  └─ self-assessed RecallForm

Existing review/schedule history
        ↓ conversion where reliable
LearningEpisode / historical events
        ↓
derived learner state
- Preserve existing Collection names and memberships.
- Generate stable IDs once during migration and persist them thereafter.
- Do not reset learner history merely because content is normalized into the new model.
- Where old data does not contain an observation dimension, preserve it as unknown rather than fabricate detail.
- Migration should keep the current front/back UI usable throughout the transition.

## 12. Implementation Sequence
- Align Requirements 00–03 terminology and semantics with Foundation v2.3 + this MVP Contract.
- Create Requirement 04 — Local Domain Model & Persistence Contract.
- Implement stable IDs/version/provenance for current knowledge entities.
- Implement package parser/validator and reconciliation ChangeSet without changing the review UI.
- Introduce LearningEpisode/event persistence under the existing flashcard interaction.
- Migrate legacy Card/Collection/history into the new domain model.
- Introduce rebuildable learner state and keep FixedIntervalStrategy working.
- Add local adaptive strategy and selector improvements only after history integrity is verified.
- Add richer component/RecallForm types incrementally behind capability/version boundaries.

## 13. MVP Acceptance Gate
- The app can represent an existing front/back card as KnowledgeUnit + KnowledgePoint + RecallForm without losing current UX.
- Re-importing the same stable knowledge does not reset learner history.
- Knowledge changes and learner history are persisted independently.
- One completed flashcard review produces a valid LearningEpisode/event history with deterministic event order.
- The history distinguishes retrieval evidence from answer exposure.
- Old/missing fields remain unknown rather than being fabricated.
- Current learner/schedule state can be rebuilt from durable history at least for the supported MVP model.
- Fixed scheduling remains usable and an adaptive strategy can be substituted without changing Knowledge identity.
- Backup preserves knowledge plus durable learning history sufficient to restore the MVP.
- No deferred Foundation capability is required for the app to function offline.

## 14. Status Matrix

| Status | Contract |
|---|---|
| MUST IMPLEMENT | KnowledgeUnit; KnowledgePoint; RecallForm; stable ID/version; provenance capability; Collection membership; assets; LearningEpisode/events; RawObservation; EvaluationOutcome; minimal MemoryEvidence; durable history; import/reconciliation; backup; fixed + local adaptive scheduling boundary. |
| INTERFACE / SCHEMA RESERVATION | KnowledgeStructure; KnowledgeProcedure; typed relations; richer interaction/evaluator types; cross-unit component reuse; context-conditioned state; external standard adapters. |
| MVP-ONLY CONVENTIONS | Front/back card renderer; Again/Hard/Good/Easy; initial lifecycle labels; unit-local component serialization where convenient. |
| NOT IN MVP | MemoryAssembly; generalized tutor; understanding mastery; learned evidence attribution; cloud-dependent scheduling; global knowledge ontology; research benchmark platform. |


## 15. Relationship to Foundation v2.3
This contract does not replace Project Mneme Foundation v2.3. The Foundation defines the long-term scientific and architectural boundaries; this contract defines the intentionally smaller implementation surface for the current Flashcard App.

| Change rule: If an MVP implementation shortcut conflicts with a FROZEN Foundation principle, change the implementation. If implementation pressure exposes a genuine flaw in the Foundation, record it as a research/architecture issue and revise the Foundation explicitly rather than silently coding around it. |
|---|


## 16. Next Specifications
- Requirement 00 — Mneme Flashcard Domain Foundation (aligned terminology and MVP projection).
- Requirement 01 — Knowledge Package Import, Reconciliation & Collections.
- Requirement 02 — Memory Inference, Review Scheduling & RecallForm Selection.
- Requirement 03 — Learning Episode, Observation, Evaluation & Evidence History.
- Requirement 04 — Local Domain Model & Persistence Contract.

## 17. Source-Code-Informed MVP Amendments (v1.1)
These amendments absorb implementation lessons that are mature enough to constrain the MVP without expanding its product scope.

### M1 — Durable commit before enrichment
The MVP must commit the learner’s canonical local episode/event/observation transaction before starting optional AI analysis, embedding generation, remote sync, or expensive diagnostics. A successful UI review action must never depend on those optional services.

### M2 — Artifact-specific consolidation
Knowledge and derived artifacts may have duplicate-detection workflows, but learner historical observations must not be semantically merged. The only automatic historical deduplication allowed in the MVP is idempotent retry detection for the same durable operation identity.

### M3 — Shared history projection path
Scheduling, diagnostics, backup/research export, and learner-state rebuild must consume a shared normalized historical view. No subsystem may invent a second incompatible interpretation of historical event envelopes.

### M4 — Exposure provenance
The MVP must preserve whether relevant information was system-provided before an attempt (prompt, hint, revealed answer, sibling card, prior support). The first implementation may store compact exposure references rather than a sophisticated InformationOrigin model.

### M5 — Replay scalability reservation
MVP storage/repository interfaces must support bounded history reads and history boundaries so a future ReplayCheckpoint can accelerate rebuilds. The MVP need not implement checkpoint creation if current data volumes do not justify it.

## 18. Dual-Profile MVP Amendment (v1.2)

### 18.1 Shared core MUST implement
- Opaque stable IDs, semantic versions, hashes where required, provenance, lineage, and compatibility envelopes.
- Typed/profile-owned canonical history with durable operation identity and idempotent retry semantics.
- MemoryScope as a shared applicability/isolation mechanism, with profile-specific scope facets.
- One canonical normalization/projection path per history family; derived projections/checkpoints/indexes are rebuildable.
- Bounded/incremental history access, portable backup/export, and safe schema evolution.
- Retrieval infrastructure that keeps deterministic identity/structured lookup authoritative and treats lexical/semantic retrieval as discovery.
- Purpose-specific ProjectionBudget and provenance for material projected context.

### 18.2 Learning Profile MUST implement
Requirements 00–04 remain the normative MVP projection for human learning. `MemoryModel` in those documents is interpreted as `LearnerMemoryModel`/`learning.MemoryModel`; its evidence and scheduling semantics are not imposed on the Agent Memory Profile.

### 18.3 Agent Memory Profile MUST implement
- Durable AgentMemoryObservation capture with source references, scope, provenance, and information-origin/context-fencing metadata.
- MemoryRecord derivation/consolidation with stable identity, lineage, supersession, and provenance; canonical Minion-Agent session history is never rewritten.
- Scope-aware retrieval and ranking under an explicit context/projection budget.
- AgentContextProjection that can be injected into Minion-Agent and traced back to selected MemoryRecord IDs/versions.
- Capture-first/enrich-later behavior: expensive extraction, embeddings, semantic indexing, remote sync, or AI analysis cannot make authoritative source history best-effort.
- Feedback-loop protection so recalled/injected memory is not re-learned as independent new memory without external corroboration.

### 18.4 Explicit non-goals
- Do not force Agent Memory into LearningEpisode, RecallForm, MemoryEvidence, or SchedulingPolicy.
- Do not make Minion-Agent SessionStorage an implementation of Minion-Memory.
- Do not make a vector database, embedding provider, LLM extractor, or dynamic plugin system mandatory to the core.
- Do not require the Flashcard App to understand agent-memory entities.

### 18.5 Dual-language certification target
The Python and Rust implementations consume the same shared core/profile contracts and canonical conformance. Neither language is semantic authority for the other. A profile is complete only when its applicable canonical semantics are independently implemented and cross-language reviewed under the Minion-Agent-style process.
