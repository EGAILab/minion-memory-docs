<!-- DERIVED, NON-AUTHORITATIVE reading aid. Source: Project_Mneme_Implementation_Architecture_Amendments_v1_3.docx sha256:436ea1a3a5ffa126d70a1c3cb8e1a8cc1e3d8baf1d50740df3a9098240daba33. Regenerate with `mneme-process sources build`; never edit by hand. -->

Project Mneme
Implementation Architecture Amendments v1.3
Source-code informed amendments from DeepSeek Harness / Cordis, Hermes Agent memory providers, Pi 1.0, claude-mem, and Minion-Agent integration analysis

| Scope: These amendments refine implementation guardrails without changing the scientific ontology in Project Mneme Foundation v2.1. They borrow architecture patterns selectively and explicitly reject framework-specific mechanisms that do not fit an offline-first Flutter memory application. |
|---|


## 1. Why this amendment exists
The Mneme foundation already separates Knowledge, interaction history, observation, evaluation, evidence, learner-state inference, and scheduling. Recent source-code reviews provide practical implementation patterns that repeatedly reinforce those boundaries. This document records only the patterns that are mature enough to guide engineering before the first Mneme persistence implementation.

### A1 — Canonical history vs projections
Learner observation history is canonical durable data. Learner state, diagnostics, scheduling state, summaries, and checkpoints are projections or rebuild accelerators. Lossy projections never replace canonical history.

### A2 — Durable domain events vs runtime events
LearningEvents represent durable domain facts. UI lifecycle events, timers, loading states, cache invalidation, renderer events, and internal coordination signals belong to a separate runtime event domain.

### A3 — Historical reconstructability
If information materially affected a historical interpretation, the system must preserve enough versioned references/snapshots/provenance to explain that interpretation later.

### A4 — Required vs ignorable event compatibility
Unknown historical event types that may affect semantics must fail safely. Only event types explicitly declared ignorable may be skipped by an older reader.

### A5 — Persisted does not imply active
A persisted artifact is not automatically an input to learner-state inference or scheduling. Every durable derived artifact must have explicit consumers and participation semantics.

### A6 — Capability seams, not universal plugins
Replaceable capabilities should expose explicit Definition → Provider → Consumer boundaries. Mneme should not adopt an everything-is-a-plugin runtime or general service-locator architecture.

### A7 — System exposure provenance / anti-feedback contamination
Information shown by the system—hints, answer reveals, sibling forms, worked examples, partial cues—must retain provenance so subsequent correct responses are not mistaken for independent recall.

### A8 — Progressive-resolution knowledge presentation
Rich KnowledgeUnits may have multiple presentation resolutions or support layers. A rich stored unit does not imply that every review displays all content.

### A9 — Retrieval is multi-modal, not semantic-search-only
Future retrieval should support exact identity, structured filters, lexical search, and semantic search. Stable identity and deterministic navigation remain primary where available.

### A10 — Replay checkpoints
Long histories may use model-specific replay checkpoints. A checkpoint records model/version, state snapshot, history boundary, and provenance, and can always be discarded in favor of canonical replay.

### A11 — Purpose-specific projections
Do not create one universal LearnerSummary blob. Scheduling, diagnostics, progress UI, reporting, and research may derive different projections from the same history.

### A12 — Semantic order is explicit
Episode sequence is a semantic ordering. Wall-clock completion order or asynchronous evaluator completion order must not silently define event meaning.

### A13 — Durability barrier before lossy compaction
Any compaction, pruning, or archival operation must first ensure irrecoverable learner observations and required historical context are durably persisted.

### A14 — Optional remote/AI processing fails open
AI diagnostics, remote evaluators, semantic indexing, and optional backends must not block or endanger the local review critical path. Canonical local history persistence remains synchronous/durable; optional processing may be asynchronous.

## 2. Recommended implementation vocabulary
CanonicalHistory
  LearningEpisode[]
  LearningEvent[]
  RawObservation[]

HistoricalInterpretation
  EvaluationOutcome[]
  MemoryEvidence[]

DerivedProjection
  LearnerStateEstimate
  DiagnosticsProjection
  ProgressProjection
  ScheduleState

ReplayCheckpoint
  model_id / model_version
  model_parameters_hash
  state_snapshot
  history_through_event
  evidence_boundary
  created_at
  provenance

## 3. Event compatibility envelope
The serialized LearningEvent envelope should support compatibility semantics independent of the typed Dart hierarchy. Exact field names remain implementation-specific.
LearningEventEnvelope
  event_id
  episode_id
  sequence_no
  event_type
  schema_version
  compatibility: required | ignorable
  occurred_at
  recorded_at
  payload
- Core learner observations, attempts, hints/exposures that affect evidence, corrections, and completion semantics are normally required.
- Purely informational telemetry may be ignorable only if skipping it cannot change reconstruction of learner-relevant meaning.
- A decoder encountering an unknown required event must stop semantic replay and report an unsupported schema/event rather than silently producing a misleading learner state.

## 4. Exposure contamination contract
System-provided information
  PromptPresented
  HintPresented
  AnswerRevealed
  WorkedExampleShown
  RelatedRecallFormShown
        ↓
SystemExposureContext
        ↓
Later Attempt
        ↓
EvidenceMapper can discount / qualify evidence
without rewriting the observation
The app does not claim to know the learner’s internal information source. It records what the system itself exposed before the attempt so later models can reason conservatively about cue contamination.

## 5. Replay checkpoint contract
- Checkpoint state is model-specific and never canonical learner truth.
- A checkpoint must declare the exact history boundary it summarizes.
- Incompatible checkpoints are ignored, not migrated by inventing meaning.
- A deterministic model replaying the same compatible checkpoint + subsequent events must reproduce an equivalent state.
- Portable backup may include checkpoints as acceleration data, but restore correctness must not depend on them.

## 6. Capability seam discipline
Capability: MemoryModel
Definition: interface / semantic contract
Providers: SimpleAdaptive, FSRS adapter, future experimental model
Consumers: SchedulingPolicy, diagnostics, progress projection

Capability: Evaluator
Definition: observation → EvaluationOutcome
Providers: self-assessment, deterministic text, numeric, symbolic, optional AI
Consumers: EvidenceMapper

Capability: EvidenceMapper
Definition: observation/outcome/context → MemoryEvidence
Providers: declarative mapping, future learned mapper
Consumers: MemoryModel / diagnostics
The implementation should use ordinary explicit dependency injection. Dynamic plugin loading, service registries, and hot-swappable provider discovery are out of scope for the MVP.

## 7. Patterns deliberately not copied
- Do not adopt DeepSeek Harness/Cordis “everything is a plugin” architecture.
- Do not use an agent-style shared context/service locator as the main Flutter dependency pattern.
- Do not treat agent memory providers (Mem0/Honcho/Hindsight/etc.) as models of human memory.
- Do not make semantic/vector retrieval the canonical identity mechanism for Knowledge.
- Do not make remote memory writes best-effort for canonical learner history; local history durability is stronger than agent-memory durability requirements.
- Do not rewrite old semantic LearningEvents in place merely to match the newest event schema; decode old formats conservatively.
- Do not event-source ordinary UI settings or all Knowledge edits simply because learner history is event-oriented.

## 8. Traceability to reviewed implementations
DeepSeek Harness / Cordis: Append-only typed session history, derived views, live vs durable events, provider seams, compatibility discipline.
Sources: https://github.com/deepseek-ai/deepseek-harness ; https://github.com/cordiverse/cordis
Hermes Agent memory providers: Multiple memory philosophies; provider lifecycle; non-blocking optional capture; context fencing; hierarchical resolution; hybrid retrieval; provenance/trust.
Sources: https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers ; https://github.com/NousResearch/hermes-agent
Pi: JSONL durable sessions, parent/lineage structure, lossy compaction without deleting full history, custom persisted entries, runtime event stream separation, extension seams.
Sources: https://github.com/earendil-works/pi ; https://pi.dev/docs/latest/compaction

## 9. Implementation adoption status
- ADOPT NOW: canonical history/projection split; runtime-vs-durable events; event compatibility; explicit capability seams; exposure provenance; purpose-specific projections.
- ADOPT AS SCHEMA/INTERFACE RESERVATION: ReplayCheckpoint; progressive-resolution knowledge rendering; hybrid retrieval architecture.
- RESEARCH CANDIDATE: richer information-origin inference, learned evidence mapping, cross-context retrieval-state models.
- REJECT FOR MVP: universal plugin runtime, dynamic external memory provider framework, cloud-dependent core persistence.

## 10. Pi 1.0 and claude-mem Amendments (v1.2)
These amendments extend the v1 source-code review with newer Pi durable/projection patterns and claude-mem capture, retrieval, deduplication, reinforcement and context-budget implementation lessons.

### A15 — ReplayCheckpoint semantic dependency boundary
Pi 1.0 strengthens the checkpoint pattern: a useful checkpoint must preserve not only model state and a history boundary but also the semantic dependencies required to interpret that state. Mneme checkpoints therefore carry model/version/parameters and relevant schema/artifact/evidence interpretation boundaries. A checkpoint remains rebuildable and non-authoritative.

### A16 — Append-only interpretation overlays
Pi’s append-only context-edit/projection pattern reinforces Mneme’s “reinterpret without rewrite” rule. New evaluator/evidence interpretations append lineage/supersession metadata; current interpretation is a projection over immutable observations and historical interpretations.

### A17 — One canonical history projection path
Pi’s projection-path drift problems demonstrate a concrete failure mode when normal context, compaction, or other consumers independently interpret historical entries. Mneme must provide one HistoryProjector/normalizer contract reused by MemoryModels, scheduler, diagnostics and exports.

### A18 — Durable operation idempotency
Durable harness retry semantics motivate operation_id/submission_id on learner commits. A successful review commit followed by crash/retry must not create a second LearningEpisode/event.

### A19 — Bounded replay and heap discipline
Long-lived histories must not require loading every LearningEvent into memory. Repositories support bounded reads and checkpoint + tail replay. This is a scalability constraint, not a change to canonical history semantics.

### A20 — Artifact-class-specific consolidation
claude-mem’s exact/candidate/none duplicate tiers expose a critical Mneme distinction: repeated Knowledge/derived text may be redundant, while repeated learner performance is usually evidence. Knowledge can have duplicate-candidate workflows; learner historical observations are never semantically deduplicated.

### A21 — Progressive disclosure read architecture
claude-mem’s Search → Timeline → Full observation flow and OpenViking’s progressive resolution independently support Index → Context → Detail retrieval. Mneme should keep canonical artifacts rich and let read projections fetch/display only the resolution needed for the current purpose.

### A22 — Budgeted purpose-specific projections
claude-mem measures actual context size and degrades by policy rather than assuming a fixed item count. Mneme projections/activity selection should support real resource budgets and explicit degradation priorities; canonical records are never truncated to satisfy a view budget.

### A23 — Hybrid retrieval is discovery, not authority
SQLite/structured filters, FTS and semantic/vector retrieval may coexist. Stable IDs and structured domain data remain authoritative. Embeddings are discovery/index artifacts and may be absent, stale or rebuilt without changing Knowledge identity or learner truth.

### A24 — Capture-first, enrich-later
claude-mem separates fast capture from expensive background compression. Mneme adopts the stronger variant: commit canonical learner observation/history synchronously first; run optional AI evaluation, semantic indexing, diagnostics or remote sync asynchronously.

### A25 — Policy should not be one universal score
claude-mem preserves a recency head before reinforcement re-ranking, illustrating that one score may not express all policy constraints. Mneme SchedulingPolicy may combine hard constraints, reserved categories, budgets and ranking instead of assuming one scalar score/top-N mechanism.

### Patterns still deliberately not copied
- LLM-generated compressed observations as the canonical learner record.
- Semantic duplicate collapse of learning events.
- ACT-R-inspired observation ranking as a human learner-memory model.
- Chroma/vector infrastructure as a required runtime dependency.
- HTTP worker/process topology inside the Flutter MVP.
- Pi session-format migration semantics applied wholesale to long-lived learner history.

## 11. Minion-Agent Primary-Use-Case Amendments (v1.3)

### A26 — Dual-profile core
Minion-Memory has two primary proving profiles: Human Learning and Agent Memory. Shared-core abstractions are admitted only when both profiles can use them without semantic distortion.

### A27 — Profile namespaces
Learner-specific concepts remain in the Learning Profile; agent capture/consolidation/context concepts remain in the Agent Memory Profile. Prefer explicit namespaces over a universal `Memory` entity.

### A28 — MemoryScope
Promote scope/applicability/isolation to the shared core. Agent scope must support at least principal/user, agent, workspace/project, conversation, session, and task dimensions or an extensible equivalent.

### A29 — Session history is not long-term memory
Minion-Agent session/conversation history remains authoritative execution history. Minion-Memory stores selected/interpreted long-term memory and source references; it does not replace SessionStorage.

### A30 — Context fencing across agent turns
A retrieval projection records which memories were injected. Subsequent capture must distinguish injected/recalled information from newly observed external information to prevent recursive reinforcement.

### A31 — Capture vs consolidation
Canonical AgentMemoryObservation capture and derived MemoryRecord consolidation are separate stages. Consolidation may merge/supersede derived records but cannot semantic-deduplicate source observations.

### A32 — Request projection reconstructability
When memory materially affects an agent request, retain enough projection identity/record-version references to reconstruct or audit the memory context that was injected.

### A33 — Adapter, not framework coupling
Integrate Minion-Agent through an adapter using its existing prompt/header/session/runtime seams. Minion-Memory itself must not depend on Cordis-style service locators or Minion-Agent plugin internals.

### A34 — Profile-specific policy
Learner scheduling policy and agent retrieval/ranking policy are distinct capabilities even when they reuse budgets, indexes, or projection utilities.

## 12. Verified Minion-Agent Integration Seams
Verified against EGAILab/minion-agent main at d37171d716fe8fc44b5c16fec9c69705f8c74760. Current implementation/design provides: open request-header component names with content-addressed reconstruction; documented `memory` header component; contributed prompt sections; open session-event names; scoped runtime services/plugins; and a product requirement for per-turn memory recall. These make a separate Minion-Memory adapter feasible without redesigning the core agent loop.

| Minion-Agent seam | Mneme use |
|---|---|
| request_header components / `memory` | Persist exact memory projection as request-visible state |
| PromptComposer contributed sections | Inject budgeted agent-memory context |
| open session event namespace | Record adapter-specific audit/reference events where justified |
| runtime service/plugin seam | Install an adapter/provider without making Mneme itself a plugin framework |
| session/turn/tool history | Source references for AgentMemoryObservation capture |


## 13. Patterns deliberately not copied (v1.3)
- Minion-Agent SessionStorage is not absorbed into Minion-Memory.
- Agent session events are not reclassified as learning events.
- LLM-generated memories are not canonical merely because an extractor produced them.
- Vector similarity never bypasses scope/isolation or establishes stable identity.
- Agent-memory consolidation algorithms are not promoted into a theory of human memory.
