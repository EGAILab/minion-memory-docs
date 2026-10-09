<!-- DERIVED, NON-AUTHORITATIVE reading aid. Source: Project_Mneme_Minion_Memory_Bootstrap_Prompt_v1_1.md sha256:bbf988e8558d170966601828286ae03fec3839e3bb2a8bf68af094d8de3253c4. Regenerate with `mneme-process sources build`; never edit by hand. -->

# Minion-Memory bootstrap prompt v1.1 — dual-profile project

You are bootstrapping **Minion-Memory** in:

`E:\AI\Projects\OpenMinds\Minions\Minion-Memory`

The end product is a production-quality, language-independent Project Mneme memory engine with **two independently implemented language versions (Python and Rust)** and **two primary proving profiles**:

1. **Human Learning Profile** — first consumer: the existing Flashcard App.
2. **Agent Memory Profile** — first consumer: `EGAILab/minion-agent`.

The shared core must be genuinely shared. Do not force learner-specific semantics into agent memory, and do not weaken learner evidence semantics merely to reuse code.

## Process

Follow the governance and assurance discipline used by `EGAILab/minion-agent-docs/process`, especially:

- `process/agent-workflow.md`
- `process/coordination-state.md`
- `process/implementation-conformance-workflow.md`
- `process/requirement-id-convention.md`
- `process/gate-tiers.md`
- `process/hazard-families.md`
- `process/templates/cross-language-feasibility-matrix.md`
- `process/minion-process-cli-design.md`

Reuse the workflow discipline, exact-SHA handoffs, independent review, G0-G3 gate tiers, shared canonical conformance, and Python-leading/Rust-independent cadence. Do **not** copy Pi-specific semantic authority rules: Minion-Memory has no Pi-like reference implementation.

## Semantic authority order

1. Project Mneme Foundation v2.3 — Dual-Profile Architecture
2. Project Mneme MVP Contract v1.2 — Dual Profile
3. Flashcard Requirement 00 v2.3
4. Flashcard Requirement 01 v2.3
5. Flashcard Requirement 02 v2.3
6. Flashcard Requirement 03 v2.3
7. Flashcard Requirement 04 v1.3
8. Requirement 05 — Agent Memory Profile & Minion-Agent Integration v1.0
9. Implementation Architecture Amendments v1.3
10. Codex/implementation pack guidance

If authorities conflict, classify a `CONTRACT_ASSURANCE_DEFECT`, identify the exact conflict, propose the smallest coherent resolution, and stop that semantic decision for Owner review.

## Integration target

During WP-00, inspect the **current** `EGAILab/minion-agent` and `EGAILab/minion-agent-docs` rather than relying on this prompt's snapshot. The 2026-10-09 verification found clean seams in request-header components (`memory` is already a documented component), prompt contributed sections, open session-event names, and the runtime service/plugin layer. Treat Minion-Agent as a primary consumer/integration target, **not semantic authority**.

Keep Minion-Agent authoritative SessionStorage/history separate from Minion-Memory long-term memory. Memory capture stores stable source references/provenance; it does not replace conversation/session history.

## Proposed repo topology

Unless the existing workspace establishes a better compatible structure, propose:

```text
Minion-Memory/
├── minion-memory/
│   ├── conformance/
│   ├── schemas/
│   ├── minion-memory-python/
│   └── minion-memory-rust/
└── minion-memory-docs/
    ├── design/
    ├── spec/
    ├── process/
    ├── assurance/
    ├── plans/
    └── reference/
```

Do not destructively rearrange the workspace or create/publish remote repositories without Owner approval.

## Contract model

Propose `mneme-contract-manifest.yaml` as a traceability artifact, not semantic authority:

`requirement ID -> authoritative source -> normalized spec anchor -> canonical scenario -> Python location -> Rust location -> assurance evidence -> status/disposition`

Suggested requirement families (confirm in SCOPING):

- `CORE-###` identity/provenance/lineage/compatibility
- `SCOPE-###` MemoryScope/isolation
- `HIST-###` canonical history/idempotency/replay
- `PROJ-###` projections/budgets/checkpoints
- `RETR-###` lookup/index/retrieval primitives
- `KNOW-###` learning Knowledge model
- `LEARN-###` LearningEpisode/RecallForm
- `EVAL-###` EvaluationOutcome/MemoryEvidence
- `LMOD-###` LearnerMemoryModel
- `SCHED-###` scheduling/recall selection
- `AMEM-###` AgentMemoryObservation/MemoryRecord/consolidation
- `ACTX-###` AgentContextProjection/context fencing
- `PKG-###` Knowledge package/import
- `PERS-###` persistence/backup/migration
- `INT-###` integrations/adapters
- `PRIV-###` privacy/retention

## Core admission rule

A concept belongs in `core` only if both profiles can use it without semantic distortion.

Expected shared-core candidates:

- stable identity / version / provenance / lineage
- MemoryScope
- canonical typed history primitives
- durable operation identity/idempotency
- HistoryBoundary / ReplayCheckpoint
- artifacts and derived indexes
- retrieval primitives
- purpose-specific Projection / ProjectionBudget
- persistence/backup/compatibility

Expected Learning Profile concepts:

- KnowledgeUnit / KnowledgeComponent / RecallForm
- LearningEpisode / LearningEvent / RawObservation
- EvaluationOutcome / MemoryEvidence
- LearnerMemoryModel
- SchedulingPolicy

Expected Agent Memory Profile concepts:

- AgentMemoryObservation
- MemoryRecord
- ConsolidationOutcome/policy
- Retrieval/ranking policy
- AgentContextProjection
- context fencing / injected-memory provenance

Do not create a universal `Memory` entity merely to make the diagrams symmetric.

## Minion-Agent integration invariants

- Minion-Agent session/conversation history remains authoritative execution history.
- Minion-Memory stores long-term memory observations/records and source references.
- Conversation compaction != memory consolidation.
- Agent-memory indexing/embedding caches are rebuildable and cannot become identity authority.
- Pre-request retrieval is scope-aware and budgeted.
- The exact model-visible memory projection must be attributable to MemoryRecord IDs/versions and projection policy when it materially affects behavior.
- Post-turn capture knows which memory was injected so repeated recalled information is not captured as independent new memory.
- Capture source/provenance durably first; extraction/consolidation/embedding/AI enrichment may run asynchronously.
- Minion-Agent may integrate via its service/plugin seam; Minion-Memory itself must not require that framework.

## Workflow

Use the Minion-Agent state progression:

`SCOPING -> CONTRACT_DRAFT -> CONTRACT_REVIEW -> PYTHON_IMPLEMENTATION -> IMPLEMENTATION_REVIEW -> REMEDIATION / CONTRACT_CONVERGENCE -> FINAL_CONTRACT_REVIEW -> RUST_IMPLEMENTATION -> CLOSURE_REVIEW -> CLOSED`

Retain `BLOCKED_FOR_OWNER`, `WAITING_FOR_TRIGGER`, `INCIDENT`, and `INVALID_UNAUTHORIZED`.

Python may lead by roughly half to one layer. Python is never the semantic oracle for Rust; Rust is never the semantic oracle for Python. Both consume the same reviewed spec and canonical conformance.

## Proposed dependency-aware layers (validate, do not blindly implement)

0. process, authority, requirement IDs, manifest, canonical-conformance infrastructure
1. core identity/version/provenance/lineage + MemoryScope
2. canonical history/event envelope + operation idempotency + compatibility
3. artifacts/projections/budgets/replay boundaries/checkpoints
4. retrieval/read-model primitives + rebuildable indexes
5. Learning Profile knowledge + RecallForm
6. Learning Profile interactions/evaluation/evidence
7. Agent Memory capture + MemoryRecord/consolidation
8. local persistence/transactions/bounded replay/backup
9. LearnerMemoryModel + scheduling
10. Agent retrieval/ranking + AgentContextProjection/context fencing
11. Knowledge package/import/reconciliation + migrations
12. Flashcard adapter/integration
13. Minion-Agent adapter/integration
14. cross-profile integrated certification

Change this ordering when dependency analysis proves a better one; document the reason.

## First work package — WP-00 only

**Do not implement production memory behavior yet.**

WP-00 must:

- audit the complete local workspace/repository state;
- inventory all current authoritative Mneme documents;
- inspect current Minion-Agent integration seams and pin the exact commit used for evidence;
- propose repo boundaries/topology;
- normalize the DOCX contract into provenance-preserving Markdown specs without inventing semantics;
- propose requirement IDs and `mneme-contract-manifest.yaml` schema;
- propose canonical-conformance scenario format and thin Python/Rust runners;
- adapt Minion-Agent coordination-state, gate-tier, independent-review, and cross-language feasibility process;
- validate the shared-core vs Learning Profile vs Agent Memory Profile boundary;
- identify cross-language hazards (Unicode, numeric domains, timestamps/order, SQLite transaction behavior, JSON/YAML, hashes, paths, operation IDs, scope encoding, pagination/bounded replay, checkpoint compatibility, backup JSONL);
- propose the first semantic work package;
- record explicit Owner decisions rather than silently guessing.

Create WP-00 state with `STATUS: SCOPING`, scope/non-scope, candidates, findings, next owner, and next action.

## Output of this invocation

Return:

A. Workspace audit
B. Authority inventory and missing inputs
C. Proposed repo boundaries
D. Process adaptation
E. Requirement-ID/manifest scheme
F. Shared-core/profile boundary review
G. Dependency/layer map
H. Minion-Agent integration seam audit
I. Cross-language hazard inventory
J. WP-00 coordination state
K. Exact next action
L. Owner decisions required

End with exactly one of:

`BOOTSTRAP_READY_FOR_CONTRACT_DRAFT`

`BLOCKED_FOR_OWNER`

`BOOTSTRAP_INPUTS_MISSING`

The goal is to make the project difficult to implement incorrectly, not to maximize code written in the first pass.
