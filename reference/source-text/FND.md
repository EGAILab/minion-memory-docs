<!-- DERIVED, NON-AUTHORITATIVE reading aid. Source: Project_Mneme_Foundation_v2_3_Dual_Profile_Architecture.docx sha256:f3352b902e7c6b5654c379254d464d55f519a7f933b823faf2576cf6f081b5d6. Regenerate with `mneme-process sources build`; never edit by hand. -->

PROJECT MNEME
Foundation v2.3
A General Memory Substrate for Learning, Knowledge, and Agents
Research Synthesis & Architecture Specification
Phase I synthesis: Research Rounds 1-9 + implementation-source validation + dual-profile scope review

| Research thesis: Mneme should model stable knowledge semantics, durable learner observations, and replaceable memory inference without pretending that a knowledge component is a literal atom in the brain. The current Flashcard MVP is the first proving ground, not the boundary of the foundation. |
|---|


## Document Status Legend

| FROZEN | High-confidence foundation decision. Change only when new evidence materially falsifies or improves the assumption. |
|---|---|


| PROVISIONAL | Strong current direction, deliberately designed for revision as research or implementation evidence accumulates. |
|---|---|


| RESEARCH CANDIDATE | Potential abstraction or mechanism worth investigating; not a contract for implementation. |
|---|---|


| MVP-ONLY | A deliberate simplification for the current Flashcard implementation; must not be mistaken for the general Mneme model. |
|---|---|


## Executive Summary
Project Mneme is a research and architecture project for a general-purpose durable memory substrate with two primary proving profiles: human learning and AI-agent long-term memory. It does not claim that these profiles share one cognitive ontology. Instead, it freezes a small shared core for identity, provenance, durable history, scopes, projections, retrieval, replay, and persistence, while keeping learner-specific evidence/scheduling semantics and agent-specific capture/consolidation/context semantics in separate profiles. The current Flashcard App is the first learning-profile consumer; Minion-Agent is the first agent-memory consumer.
SHARED MEMORY CORE
Stable identity / version / provenance / lineage
Typed scope + canonical durable history
Artifacts / indexes / projections / replay checkpoints
Exact + structured + lexical + semantic discovery
Purpose-specific ProjectionBudget

LEARNING PROFILE
KnowledgeUnit / KnowledgeComponent / RecallForm
LearningEpisode -> RawObservation -> EvaluationOutcome -> MemoryEvidence
LearnerMemoryModel -> SchedulingPolicy / activity selection

AGENT MEMORY PROFILE
AgentMemoryObservation -> capture / extraction / consolidation
MemoryRecord + scope + provenance + supersession
RetrievalQuery -> ranking -> AgentContextProjection
Context fencing prevents recalled memory from becoming false new memory

CONSUMERS
Flashcard App <-> Learning Profile
Minion-Agent <-> Agent Memory Profile

## 1. Vision and Scope

| FROZEN | Mneme is a general memory foundation, not a vocabulary or flashcard model. |
|---|---|

The research scope now has two primary proving domains. First, it must cover durable human knowledge ranging from middle-school subjects through university study and later professional work. Second, it must support durable long-term memory for an AI agent, including capture, scope, consolidation, retrieval, context projection, and anti-feedback provenance. Vocabulary remains a useful simple learning test case, while Minion-Agent provides a materially different systems test. Shared abstractions enter the core only when both profiles can use them without semantic distortion.

| MVP-ONLY | The first implementation may remain a simple offline-first flashcard experience using prompt -> recall -> reveal -> Again/Hard/Good/Easy. |
|---|---|


| FROZEN | General foundation does not imply general MVP. The MVP may implement only the simplest projection of the foundation. |
|---|---|


### 1.1 Explicit non-goals
- Mneme does not claim to model total human competence, intelligence, reasoning, attention, motivation, or understanding.
- Mneme does not claim that a KnowledgeComponent corresponds one-to-one with a neural or cognitive memory representation.
- Mneme does not require AI, cloud services, or a backend for core memory operation.
- Mneme is not an LMS, a general intelligent tutor, or a standards implementation such as QTI/xAPI.
- Mneme does not treat current performance as identical to durable learning.

## 2. Research Methodology

| FROZEN | Foundation decisions should be supported by both scientific literature and implementation evidence when practical. |
|---|---|

- Cross-domain stress test: abstractions should be tested against at least three materially different knowledge domains before entering the foundation.
- Source-code analysis: inspect data structures, state transitions, versioning, event histories, evaluators, and scheduling boundaries in mature open-source systems rather than relying only on product descriptions.
- Falsification-first rounds: actively seek cases that break the proposed ontology, especially open-ended, multi-step, procedural, and context-sensitive tasks.
- Longitudinal discipline: prefer data designs that preserve future reinterpretability, model replay, and replacement.
- MVP discipline: distinguish implementation shortcuts from foundation semantics.

## 3. Scientific Boundary: Knowledge Is Not Memory Is Not Performance

| FROZEN | Knowledge ontology, learner-memory inference, and observed performance are separate layers. |
|---|---|

Retrieval-practice research shows that active retrieval is both an assessment and a learning event, and that delayed retention can differ sharply from immediate study performance [R1]. Bjork & Bjork distinguish storage strength from current retrieval strength and emphasize the influence of situational cues [R2]. Expertise research further suggests that effective retrieval structures and chunks change with experience [R3]. Mneme therefore avoids making authored knowledge objects equivalent to literal memory traces.
Observed Performance
      v
Raw Observation
      v
Memory-relevant Evidence
      v
Model-specific inference
      v
Estimated Learner Memory State

Performance != Memory Truth

| FROZEN | Learner state is latent. Events are observations, not direct measurements of memory truth. |
|---|---|


## 4. Knowledge Model

### 4.1 KnowledgeUnit

| FROZEN | KnowledgeUnit is an authored boundary for coherent presentation, review, and provenance; it groups or references components but does not define their identity. |
|---|---|

Examples include "Quadratic Formula", "Causes of World War I", "Binary Search", "Periodic Table", or "Production Database Incident Response". A KnowledgeUnit is a useful human/content boundary, not a claim about the smallest unit of learner memory.

### 4.2 KnowledgeComponent

| FROZEN | KnowledgeComponent is an authored modeling unit describing what should be retained or made accessible; it is not an objectively irreducible atom of human knowledge. |
|---|---|


| FROZEN | The ontology must permit KnowledgeComponents to be referenced across multiple KnowledgeUnits; exact canonicalization, deduplication, and shared-identity rules remain PROVISIONAL. |
|---|---|

KnowledgeComponent
|-── KnowledgePoint
|-── KnowledgeStructure
`-── KnowledgeProcedure

### 4.3 KnowledgePoint
A KnowledgePoint is an independently useful assessable aspect such as a fact, definition, property, condition, rule, meaning, symbol role, or other compact declarative target.

### 4.4 KnowledgeStructure

| FROZEN | KnowledgeStructure represents a structure the learner may itself need to remember; it is not the same as metadata relationships in the knowledge graph. |
|---|---|

Examples include a sequence, hierarchy, grid, causal network, timeline, mapping, spatial arrangement, or relation pattern. Remembering all constituent facts does not imply remembering their structure, and vice versa.

### 4.5 KnowledgeProcedure

| PROVISIONAL | KnowledgeComponents require semantically distinct component kinds. Point, Structure, and Procedure are the initial PROVISIONAL taxonomy; the foundation does not claim these three are exhaustive. |
|---|---|

A procedure may include ordered steps, conditions, branches, goals, alternatives, and exceptions. Procedure recall does not imply total task competence; actual performance may also depend on perception, reasoning, attention, or environment state. Corbett & Anderson's Knowledge Tracing work explicitly modeled acquisition of procedural knowledge [R4].

### 4.6 Component granularity and evolution

| FROZEN | Component granularity is a modeling choice that may be revised; "atomic" is not a universal property. |
|---|---|

- A broad component may later split into several better-supported components.
- Several components may later merge if evidence shows the distinction is not useful.
- Split/merge creates new identities and lineage rather than pretending to be a simple content edit.
- Learner state is not automatically copied or averaged across split/merge operations.
- Knowledge-model evolution and learner-state migration are separate problems.

### 4.7 Component relations

| FROZEN | KnowledgeComponents may participate in typed semantic relations; relations are separate from learner state and scheduling. The concrete relation vocabulary is PROVISIONAL and extensible. |
|---|---|

- learning_prerequisite
- logical_dependency
- procedural_precondition
- part_of / composition
- uses
- causes
- contrasts_with
- generalizes / specializes
- commonly_confused_with

| FROZEN | KnowledgeStructure (an object of memory) and ComponentRelation (knowledge-model metadata) are semantically distinct. |
|---|---|


| FROZEN | Graph relations must not automatically propagate mastery or memory state. |
|---|---|


## 5. RecallForm / Probe Model

| PROVISIONAL | Keep the name RecallForm for current implementation; "MemoryProbe" remains a future naming candidate if it better captures multi-step memory observation without broadening Mneme into an LMS. |
|---|---|

Anki separates content notes from generated cards, and sibling cards can carry separate scheduling behavior [S1][S2]. QTI and STACK show that richer assessment requires interactions and response-processing logic beyond a single expected answer [S6][S7]. Mneme therefore treats a RecallForm as semantic activity definition rather than a UI card.
RecallForm
|-── Stimulus / Prompt
|-── Interaction[]
|-── EvaluationSpec
|-── EvidenceMapping[]
|-── LearningSupport / Hint definitions
`-── declared test/exposure semantics

| FROZEN | Renderer implementation is not Knowledge ontology. The KB specifies semantic interactions; Flutter or another runtime chooses concrete UI. |
|---|---|


| FROZEN | Declared test coverage describes potential evidence, not evidence actually obtained in every attempt. |
|---|---|


### 5.1 Retrieval and exposure

| FROZEN | Active retrieval and exposure-only must be distinguishable. |
|---|---|

Retrieval practice produces durable learning effects that are not equivalent to restudy [R1]. If a spelling prompt reveals meaning, synonyms, or examples, those components may have been exposed without being actively retrieved. Exposure may influence a future model, but must not silently become successful retrieval evidence.

| FROZEN | RecallForm semantics should be able to declare both targets it may test and knowledge it may expose. |
|---|---|


### 5.2 Sibling / contamination protection

| FROZEN | Activity selection should suppress or discount follow-up probes whose tested targets were just exposed by a related probe. |
|---|---|

Anki provides sibling burying to avoid closely related cards appearing together [S2]. Mneme generalizes this as a measurement-validity issue: a recent answer exposure can make a later response reflect working-memory contamination rather than durable recall.

## 6. LearningEpisode and LearningEvent

| FROZEN | A bounded learning/review interaction is represented as a LearningEpisode containing deterministically ordered LearningEvents. |
|---|---|

Moodle's question engine stores complete question-attempt histories as ordered attempt steps rather than only a final answer [S8]. OATutor models multi-step problems and hint pathways [S5]. This generalizes cleanly from one-turn flashcards to multi-step mathematics, code, diagnosis, and procedures.
LearningEpisode
|-── context
`-── LearningEvent[]
    |-── AttemptEvent
    |-── HintEvent
    |-── ExposureEvent
    |-── FeedbackEvent
    |-── SkipEvent
    |-── AbandonEvent
    `-── CompletionEvent

| MVP-ONLY | A flashcard review may be implemented as one LearningEpisode with one main AttemptEvent plus reveal/rating metadata. |
|---|---|


| FROZEN | Episode event order must be deterministic independently of wall-clock timestamps. |
|---|---|


| FROZEN | occurred_at and recorded_at/sync time are distinct, supporting offline-first operation and later synchronization. |
|---|---|


## 7. Observation, EvaluationOutcome, and Evidence

| FROZEN | RawObservation, EvaluationOutcome, and MemoryEvidence are separate concepts. |
|---|---|

RawObservation
    v
Evaluator
    v
EvaluationOutcome
    v
EvidenceMapper
    v
Evidence
CodeRunner preserves submitted program behavior and test outcomes rather than reducing everything to a single answer [S4]. STACK can maintain multiple inputs and Potential Response Trees and can emit structured response summaries for offline analysis [S6]. These implementations support preserving diagnostic structure before learner-memory inference.

### 7.1 RawObservation

| FROZEN | Persist the richest raw observation necessary for future interpretation whenever practical, subject to explicit privacy, retention, and data-minimization boundaries. |
|---|---|

- typed text or numeric expression
- selected choices
- spoken-response metadata where available
- submitted source code
- sequence/order manipulation
- timing
- hint request/use
- skip/abandon behavior
- environment-state transition references

### 7.2 EvaluationOutcome

| FROZEN | EvaluationOutcome represents what an evaluator concluded about the response, independent of memory attribution. |
|---|---|

- exact/normalized text match
- numeric tolerance result
- symbolic equivalence
- test-case vector
- partial correctness
- invalid syntax
- manual or AI assessment outcome

### 7.3 Evidence

| FROZEN | Evidence is interpretation-relative and provenance-bearing; it is not the raw historical fact. |
|---|---|

Evidence connects an observed/evaluated outcome to one or more knowledge targets or memory hypotheses. It must allow positive, negative, ambiguous, insufficient, partial, and quality/confidence-bearing interpretations rather than assuming every final error identifies a particular component failure.

| FROZEN | Missing evidence remains unknown. Unknown is semantically different from weak or forgotten. |
|---|---|


| FROZEN | Evidence attribution rules or models must be separately versioned and provenance-bearing. Declarative EvidenceMappings authored with a RecallForm may live in Knowledge; learned/inferred mappers may live in an inference layer. |
|---|---|


## 8. Historical Integrity and Provenance
FROZEN — Every durable authored knowledge artifact must be able to carry provenance, including producer/source, generation method where relevant, timestamps, and lineage sufficient for later audit or correction.

| FROZEN | Evolution adds interpretations; it does not rewrite learner history. |
|---|---|

Raw Observation          strongest historical authority
Historical Evaluation     what evaluator concluded then
Historical Evidence       what evidence mapping concluded then
Current Learner State     derived / rebuildable
- Knowledge entities use stable opaque IDs plus versions; semantic keys are optional and mutable.
- Same ID + same version must imply semantically identical content; differing content is a conflict.
- Historical execution snapshots preserve enough authored semantics to interpret the event after later content changes.
- Large assets should be referenced by stable ID/version/checksum rather than duplicated per event.
- Provenance should identify producer/evaluator/evidence mapper/model and their versions where relevant.

## 9. Learner Memory Model Interface

| FROZEN | Mneme does not define one universal learner-state schema. |
|---|---|

FSRS models card-level memory using model-specific state and optimizable parameters [S3]. BKT estimates latent skill knowledge with parameters such as learn, forget, guess, and slip; pyBKT supports item/resource/student variants and model evaluation [S9]. Mneme should therefore define a replaceable MemoryModel boundary rather than universalizing FSRS stability, BKT P(known), or another model's internals.
MemoryModel
  consume:
    Knowledge references
    Evidence history
    context
    optional previous model state

  produce:
    model-specific LearnerState
    predictions
    optional uncertainty / confidence information when the model defines it meaningfully

| FROZEN | Model-specific learner state is rebuildable/materialized inference, not the durable learner-history source of truth. |
|---|---|


| FROZEN | A KnowledgeComponent may map to zero, one, or multiple learner-state representations depending on the MemoryModel. |
|---|---|


### 9.1 Context-conditioned accessibility

| PROVISIONAL | Retrieval/context-conditioned state is conceptually necessary, but exact identity and storage remain model-specific. |
|---|---|

Anki's content-note/card separation and card-specific scheduling demonstrate that different retrieval directions can behave differently [S1]. Bjork's distinction between durable storage and cue-sensitive retrieval accessibility provides compatible theoretical support [R2]. Mneme must not assume context-free mastery.
KnowledgeComponent
   + cue/context family
   + response/performance mode
        v
context-conditioned accessibility estimate

| RESEARCH CANDIDATE | MemoryAssembly: learner-specific higher-order grouping/chunking of multiple KnowledgeComponents as expertise develops. Retain as a research hypothesis, not a required runtime entity. |
|---|---|


## 10. Learning Phase, Priors, and Cold Start

| PROVISIONAL | Learning phase, if modeled, belongs to learner/application state rather than Knowledge. The specific new / learning / review / relearning vocabulary is MVP-oriented and PROVISIONAL. |
|---|---|


| FROZEN | Cold start uses explicit priors; priors are not learner evidence. |
|---|---|

- population/default prior
- domain prior
- content-derived prior
- learner-personalized fitted parameters

| FROZEN | Learner model instances may have lifecycles and be recalibrated as the learner, domain, or behavior changes over years. |
|---|---|


## 11. Scheduling and Activity Selection

| FROZEN | Memory prediction and scheduling policy are separate layers. |
|---|---|

MemoryModel
  -> predicts memory / uncertainty

SchedulingPolicy
  consumes:
    predictions
    importance
    desired retention
    goals/deadlines
    workload budget

ActivitySelector
  chooses what/how to practice next
Anki/FSRS expose desired retention as a workload/retention trade-off [S2][S3]. Mneme generalizes this beyond individual due timestamps: the long-term problem is constrained allocation of learner time among possible activities.

| PROVISIONAL | LearningOpportunity: a candidate combination of target knowledge, probe/activity, execution context, expected evidence value, and learner cost. Useful for future general scheduling, but not required by the Flashcard MVP. |
|---|---|


| FROZEN | Knowledge graph relations inform scheduling features but do not themselves constitute a learning plan or scheduler. |
|---|---|


## 12. Diagnostics and Pathology

| FROZEN | Repeated failure should trigger diagnostic suspicion, not infinite interval shortening. |
|---|---|

- bad or ambiguous RecallForm
- component granularity too broad
- incorrect EvidenceMapping
- interference/confusion with related knowledge
- missing prerequisite or weak contextual route
- content error
- understanding problem outside Mneme's direct scope

| PROVISIONAL | Leech/pathology flags are derived diagnostics and should be auditable from evidence/history, not permanent Knowledge truth. |
|---|---|


## 13. Knowledge Packages, Interchange, and Backup

| FROZEN | Knowledge Package, Learning Record Export, and Full Backup are separate protocols. |
|---|---|

Knowledge Package
  content exchange / Knowledge Builder -> app

Learning Record Export
  external analytics / research projection

Full Mneme Backup
  lossless learner-system recovery

| FROZEN | External standards are adapters, not Mneme ontology. |
|---|---|

QTI supports assessment item/test and result interoperability [S10]; xAPI communicates learner activities/experiences using statements [S11]; Caliper provides domain-specific metric profiles [S12]. Mneme can map to these standards while retaining stronger internal semantics for memory evidence and inference.

| FROZEN | A QTI-like response evaluation corresponds to EvaluationOutcome; MemoryEvidence remains a separate Mneme concern. |
|---|---|


| FROZEN | Mneme-native backup must be lossless. Standards-based exports may be intentional projections. |
|---|---|


### 13.1 Package representation

| MVP-ONLY | Current canonical interchange may remain manifest.yaml + one Unit Markdown file + assets, with unit-local components carrying stable IDs. |
|---|---|


| PROVISIONAL | Long-term packages should permit shared package-level KnowledgeComponents when cross-Unit reuse becomes necessary; serialization may evolve without changing the ontology. |
|---|---|


## 14. Longitudinal Evolution

| FROZEN | History must support both state replay and future model fitting where practical. |
|---|---|


| FROZEN | Model definition, fitted model instance, current learner state, and scheduling policy are distinct. |
|---|---|

MemoryModelDefinition
  id/version

MemoryModelInstance
  model definition
  fitted parameters
  training/history boundary
  provenance

LearnerState
  derived predictions/state at a time

SchedulingPolicy
  separate decision policy
- Re-inference and rescheduling are separate operations.
- Historical scheduling decisions are not rewritten when a later model would have made a different choice.
- Observed history and counterfactual simulation are explicitly distinguished.
- Knowledge splits/merges may permit conservative reinterpretation of old observations, but old raw observations remain unchanged.
- New evidence generations may be appended with provenance rather than replacing historical evidence.

## 15. Validation Framework

| FROZEN | Every derived learner model should be versionable, replayable, comparable, and replaceable without loss of learner history. |
|---|---|

pyBKT provides fit/predict/evaluate/cross-validation workflows [S9], while FSRS includes an optimizer fitted to review history [S3]. Mneme needs a broader validation protocol because accurate next-response prediction alone does not prove better long-term memory scheduling.

| Validation Dimension | Question |
|---|---|
| Predictive quality | Can the model predict future unaided retrieval? |
| Calibration | When it predicts 90%, do roughly 90% of comparable events succeed? |
| Delayed retention | Does it improve future retrieval after meaningful delays? |
| Efficiency | How much learner time/review cost is required for a retention target? |
| Cold start | How does it behave with little or no personal history? |
| Longitudinal stability | Does performance degrade or drift over months/years? |
| Cross-context | Does it generalize across cue and response modes? |
| Cross-domain | Does it remain useful beyond vocabulary/simple cards? |
| Robustness | How does it handle hints, skips, noisy self-rating, partial outcomes? |
| Auditability / replay | Can predictions be reconstructed and explained from durable history? |


### 15.1 Evaluation protocol discipline
- Prefer temporal train->future-test splits for longitudinal claims; avoid leakage from future learner data.
- Use learner holdout when testing cold-start generalization.
- Use knowledge/domain holdout when claiming cross-content generalization.
- Distinguish offline retrospective evaluation from prospective causal learning experiments.
- Maintain a simple interpretable baseline model as a permanent fallback and regression benchmark.

## 16. Identity, Versioning, and Schema

| FROZEN | Core IDs are opaque, immutable, and producer-generated; IDs must not encode mutable semantics. |
|---|---|


| FROZEN | ID answers "which entity"; optional key answers "how humans refer to it"; version answers "which edition". |
|---|---|


| FROZEN | Schema versions and artifact/model versions are distinct. |
|---|---|

Global/schema evolution:
  knowledge_schema_version
  event_schema_version
  evidence_schema_version
  backup_format_version

Artifact/model evolution:
  KnowledgeUnit.version
  KnowledgeComponent.version
  RecallForm.version
  Evaluator.version
  EvidenceMapping.version
  MemoryModel.version
  SchedulingPolicy.version

| FROZEN | Old durable records are decoded into current normalized domain semantics; missing historical fields remain unknown rather than receiving invented defaults. |
|---|---|


## 17. Durability Hierarchy
FROZEN — Data durability is constrained by privacy and minimization: research value does not justify retaining unnecessary sensitive raw data indefinitely. Retention policy is separate from evidential authority.

| FROZEN | Persist observations richly; persist interpretations lightly. |
|---|---|

Highest protection
  Knowledge provenance/history
  Raw learning-event history

Highly valuable
  Historical evaluator outcomes
  Historical evidence + provenance

Rebuildable
  Learner model state
  predictions
  schedule state / caches

| FROZEN | Conceptual separation does not require one database table per concept. Domain semantics are durable; storage normalization is replaceable implementation detail. |
|---|---|


## 18. Flashcard MVP Projection

| MVP-ONLY | The current app implements the smallest useful projection of Mneme. |
|---|---|

KnowledgeUnit
  |-─ KnowledgePoint[]
  `-─ RecallForm
       prompt -> reveal -> rating

LearningEpisode
  `-─ Attempt / rating observation

Evidence
  self-assessed recall outcome

MemoryModel
  FixedIntervalStrategy first
  optional local adaptive model later

UI terminology may continue to say "Card".
- Offline-first and deterministic core.
- AI is optional for authoring/evaluation/diagnostics, never required for core scheduling.
- Backward-compatible import from existing Markdown/card collections.
- Collection hierarchy is organizational, not learner-memory truth.
- Existing successful front/back experience should be preserved while the domain model evolves underneath.

## 19. Status Register - Foundation v2.3

| Status | Decision |
|---|---|
| FROZEN | Knowledge / interaction / observation / inference / decision are separate layers. |
| FROZEN | KnowledgeUnit and KnowledgeComponent are distinct; the ontology permits cross-Unit reuse, while canonical shared-identity rules remain provisional. |
| PROVISIONAL | KnowledgeComponent requires semantically distinct kinds; Point / Structure / Procedure are the initial non-exhaustive taxonomy. |
| FROZEN | KnowledgeStructure != ComponentRelation. |
| FROZEN | LearningEpisode with ordered LearningEvents. |
| FROZEN | RawObservation -> EvaluationOutcome -> Evidence separation. |
| FROZEN | Learner state is latent, model-specific, and rebuildable; uncertainty is exposed only when the model provides a meaningful representation. |
| FROZEN | Unknown != weak/forgotten. |
| FROZEN | Memory prediction != scheduling policy. |
| FROZEN | External standards are adapters. |
| FROZEN | Evolution appends interpretations rather than rewriting observation history. |
| PROVISIONAL | RecallForm name; MemoryProbe is a naming candidate. |
| PROVISIONAL | Context/retrieval-route conditioned learner state semantics. |
| PROVISIONAL | LearningOpportunity abstraction for general scheduling. |
| RESEARCH CANDIDATE | MemoryAssembly / emergent learner chunk representation. |
| MVP-ONLY | Single-turn self-assessed flashcard as primary interaction and fixed/local adaptive scheduling. |
| FROZEN | Knowledge provenance is first-class for durable authored artifacts. |
| FROZEN | Raw-observation retention is bounded by privacy, retention, and data minimization. |
| PROVISIONAL | Specific ComponentRelation vocabulary is extensible; only typed semantic relations are frozen. |
| PROVISIONAL | Specific LearningEvent subtype vocabulary is extensible; ordered typed events are frozen. |
| MVP-ONLY | new / learning / review / relearning is the current SRS-oriented phase vocabulary, not a universal Mneme lifecycle. |


## 20. Research Questions for Phase II
- What minimal typed ComponentRelation vocabulary produces measurable learning value without turning Mneme into a general ontology system?
- When does context-conditioned state materially outperform component-only memory state?
- Can MemoryAssembly/chunk formation be detected reliably from learner behavior, and is it useful for scheduling?
- How should memory evidence from complex procedures be summarized without confusing memory with general performance?
- How should learner-state uncertainty be exposed to scheduling and UI without false precision?
- How should Knowledge Builder proposals for split/merge/evidence mapping be validated against longitudinal learner data?
- What scheduling objective best balances desired retention, importance, deadlines, and learner-time budget across heterogeneous activities?

## Appendix A - Research-to-Architecture Traceability

| Finding | Evidence | Mneme Design Consequence |
|---|---|---|
| Retrieval != exposure; current performance != durable retention | R1, R2 | Separate ExposureEvent / retrieval evidence; delayed validation. |
| Context affects accessibility | R2, S1, S2 | Context-conditioned/retrieval-route state remains possible; contamination suppression. |
| Expertise changes effective retrieval organization | R3 | Do not assume fixed KC = permanent learner memory unit; MemoryAssembly candidate. |
| Procedural knowledge needs explicit treatment | R4, S5 | KnowledgeProcedure component family; multi-step Episodes. |
| Shared skill/KC across problems | S5, S9 | KnowledgeUnit<->KnowledgeComponent non-exclusive relationship. |
| Question/assessment can contain multiple inputs/outcomes | S6, S10 | RecallForm supports Interaction[] + Evaluator + EvidenceMapping. |
| Raw structured outcomes are valuable | S4, S6, S8 | RawObservation and EvaluationOutcome are durable layers. |
| Latent learner state is model-specific | S3, S9, R5 | MemoryModel plugin boundary; no universal mastery scalar. |
| Attempt history is ordered and replayable | S8 | LearningEpisode with ordered events. |
| Standards separate content/activity exchange concerns | S10, S11, S12 | QTI/xAPI/Caliper adapters; no standards-driven internal ontology. |
| Prediction depends on history and model parameters | S3, S9 | Versioned model instances, training boundaries, replay/validation. |


## Appendix B - Source-Code Evidence

| ID | Project / Standard | Code/Design Evidence | Canonical Source |
|---|---|---|---|
| S1 | Anki | Content notes generate cards; card-side scheduling state demonstrates content/retrieval separation. | https://github.com/ankitects/anki |
| S2 | Anki Manual - Deck Options | Sibling burying and desired retention are first-class scheduling behaviors. | https://docs.ankiweb.net/deck-options.html |
| S3 | FSRS / fsrs-rs / fsrs4anki | Separate scheduler/optimizer; review history is used to fit memory parameters; D/S/R is model-specific state. | https://github.com/open-spaced-repetition/fsrs-rs |
| S4 | Moodle CodeRunner | Runs submitted code against tests; preserves structured execution/grading outcomes rather than only an answer string. | https://github.com/trampgeek/moodle-qtype_coderunner |
| S5 | OATutor | Problem->skill mappings, BKT parameters, multi-step problem folders, and tutoring/hint pathways. | https://github.com/CAHLR/OATutor |
| S6 | STACK | Multiple inputs and Potential Response Trees; structured response/result summaries for offline analysis. | https://github.com/maths/moodle-qtype_stack/blob/master/question.php |
| S7 | CoqGym | Proof-oriented environments motivate state/action/state observations for complex procedural performance. | https://github.com/princeton-vl/CoqGym |
| S8 | Moodle Question Engine | Question attempts consist of complete ordered histories of attempt steps with state, score, timestamp, and submitted data. | https://docs.moodle.org/dev/Overview_of_the_Moodle_question_engine |
| S9 | pyBKT | Fits latent skill models with student/item/resource variants and evaluation/cross-validation workflows. | https://github.com/CAHLR/pyBKT |
| S10 | QTI 3 | Assessment content/results interchange with explicit item/interaction/response-processing semantics. | https://www.1edtech.org/standards/qti/index |
| S11 | xAPI | Learner-experience Statements separate actor/verb/object and allow result/context/timestamp; useful as an external event projection. | https://github.com/adlnet/xAPI-Spec |
| S12 | Caliper Analytics | Metric Profiles use activity-specific event vocabularies rather than a single untyped universal event. | https://www.1edtech.org/standards/caliper |


## Appendix C - Scientific Literature
[R1] Roediger, H. L., & Karpicke, J. D. (2006), "Test-Enhanced Learning: Taking Memory Tests Improves Long-Term Retention". Psychological Science, 17(3), 249-255. PMID 16507066. Demonstrates that retrieval practice improves delayed retention relative to restudy. https://pubmed.ncbi.nlm.nih.gov/16507066/
[R2] Bjork, E. L., & Bjork, R. A. (2011), "Making Things Hard on Yourself, But in a Good Way: Creating Desirable Difficulties to Enhance Learning". Introduces the storage-strength / retrieval-strength distinction and emphasizes current accessibility, cue/context effects, spacing, and desirable difficulties. https://bjorklab.psych.ucla.edu/wp-content/uploads/sites/13/2016/04/EBjork_RBjork_2011.pdf
[R3] Ericsson, K. A., & Kintsch, W. (1995), "Long-Term Working Memory". Psychological Review, 102(2), 211-245. DOI 10.1037/0033-295X.102.2.211. Expertise-oriented account of retrieval structures and long-term memory access in skilled activity. https://pubmed.ncbi.nlm.nih.gov/7740089/
[R4] Corbett, A. T., & Anderson, J. R. (1995), "Knowledge Tracing: Modeling the Acquisition of Procedural Knowledge". User Modeling and User-Adapted Interaction. Models evolving learner knowledge during procedural skill acquisition and underpins Bayesian Knowledge Tracing. https://act-r.psy.cmu.edu/wordpress/wp-content/uploads/2012/12/893CorbettAnderson1995.pdf
[R5] Khajah, M., Lindsey, R. V., & Mozer, M. C. (2016), "How Deep Is Knowledge Tracing?". Examines recency, contextualized trial sequence, inter-skill similarity, and individual variation; argues for caution in attributing predictive gains to a particular latent representation. https://arxiv.org/abs/1604.02416

## Appendix D - Design Invariants (Compact)
- Knowledge != learner state != observed performance.
- KnowledgeUnit is an authored coherence/provenance boundary, not a brain atom.
- KnowledgeComponent is a revisable modeling hypothesis.
- KnowledgeComponent supports semantically distinct kinds; Point, Structure, and Procedure are the current provisional taxonomy.
- The ontology permits cross-Unit component reuse; exact canonical shared-identity rules remain provisional.
- KnowledgeStructure != ComponentRelation.
- LearningEpisode preserves ordered interaction history.
- RawObservation != EvaluationOutcome != Evidence.
- Unknown != weak/forgotten.
- Evidence attribution may be ambiguous or insufficient.
- Learner state is latent, model-specific, and rebuildable; uncertainty is exposed only when the model provides a meaningful representation.
- Context can affect accessibility; no assumption of context-free mastery.
- Prediction != scheduling policy.
- External standards are adapters, not internal ontology.
- Evolution appends versions/interpretations rather than rewriting observation history.
- General foundation does not require a general MVP.

## Closing Position

| Foundation v2.2 position: Mneme should preserve stable knowledge semantics and rich learner history while keeping evaluators, evidence mappings, memory models, and scheduling strategies replaceable. This lets the Flashcard MVP remain simple today without making today's flashcard assumptions permanent architecture. |
|---|


## Appendix E - Architecture Review Changes (v2 -> v2.1)
Purpose: distinguish durable architectural boundaries from taxonomies and implementation vocabularies that were frozen too early in Foundation v2.2. This appendix records the rationale so later research can challenge assumptions without losing design history.

| Area | v2.1 Change | Rationale |
|---|---|---|
| Component taxonomy | FROZEN -> PROVISIONAL | The need for semantically distinct component kinds remains stable, but Point / Structure / Procedure are not proven exhaustive across all future domains. |
| Cross-Unit component reuse | Clarified | Cross-Unit reuse is supported by the ontology, but canonicalization and whether two authored components share one durable identity remain contextual modeling decisions. |
| ComponentRelation vocabulary | FROZEN principle / PROVISIONAL vocabulary | Typed semantic relations remain required; the concrete registry of prerequisite, uses, causes, contrasts, etc. is intentionally extensible. |
| EvidenceMapping placement | Relaxed | Evidence attribution must be versioned and provenance-bearing. Declarative mappings may be Knowledge artifacts; learned mappers may instead be inference artifacts. |
| LearningEvent taxonomy | FROZEN structure / PROVISIONAL subtypes | A LearningEpisode contains deterministically ordered typed events, but Attempt/Hint/Exposure/Feedback/etc. are an initial vocabulary, not an exhaustive ontology. |
| Learning phases | FROZEN boundary -> PROVISIONAL vocabulary | If a phase is modeled it belongs to learner/application state. new/learning/review/relearning is retained for the Flashcard MVP, not treated as universal. |
| Uncertainty | Interface relaxed | Learner state remains latent and model-specific. Models should expose uncertainty when meaningful, but simple deterministic baselines must not fabricate confidence values. |
| Privacy and minimization | Added FROZEN invariant | Rich raw observations are valuable, but storage must be bounded by explicit privacy, retention, and data-minimization rules. |
| Knowledge provenance | Strengthened to FROZEN | Durable authored knowledge must support source/producer/generation/lineage provenance, especially for AI-generated or externally imported content. |
| Event ordering | Clarified | Ordering is deterministic inside an Episode; no total global order across devices/episodes is assumed by the foundation. |


### E.1 Revised Freeze Policy
- Freeze architectural boundaries and invariants when they survive cross-domain and falsification testing.
- Keep taxonomies, naming vocabularies, canonicalization rules, and model-specific state shapes provisional unless evidence shows they are necessary and stable.
- MVP vocabulary may remain deliberately narrow without being elevated into the general foundation.
- Future research should challenge a named assumption and update its status with evidence rather than silently altering semantics.

## v2.2 Historical Closing Position
Foundation v2.2 freezes the boundaries that have survived nine research rounds and an architecture review, while deliberately loosening taxonomies that remain empirical hypotheses. Mneme should preserve stable knowledge semantics and provenance, rich but privacy-bounded learner observations, versioned evaluation/evidence interpretations, and replaceable memory inference—without hard-coding one flashcard taxonomy, one cognitive theory, or one scheduler into the durable foundation.

## Appendix F - Implementation-Informed Constraints (Pi 1.0 / claude-mem / Harness / Hermes)
This appendix records only cross-implementation constraints that reinforce existing Mneme boundaries. It does not turn agent-memory implementation patterns into cognitive theory.

### Cross-implementation evidence
Source-code reviews of DeepSeek Harness/Cordis, Hermes Agent memory providers, Pi 1.0, and claude-mem independently converge on several architecture patterns that are compatible with Mneme’s research conclusions. These patterns are implementation evidence, not claims about human cognition.
- Durable history remains canonical while current context/state is a projection.
- Compression and summaries are lossy views, not replacements for original history.
- Runtime coordination signals and durable historical facts are separate event domains.
- Stable seams permit replaceable inference/selection implementations without turning the whole system into a plugin runtime.
- System-injected context can contaminate later observations unless information origin is preserved.
- Large histories require bounded replay/checkpoints and progressive retrieval, not full in-memory replay.

### Foundation-level clarifications
The following are promoted as architecture constraints because they protect the epistemic boundary already frozen in the Foundation. They do not prescribe SQLite, vector databases, HTTP workers, plugin frameworks, or any specific implementation.
- Canonical learner history is never replaced by a lossy summary, model state, checkpoint, diagnostic, or semantic index.
- Learner historical events are never semantically deduplicated. Duplicate suppression is allowed only for accidental retry of the same durable operation identity.
- System-provided information (prompt, hint, answer reveal, sibling exposure, worked example, prior injected context) must retain provenance so later success is not misclassified as independent retrieval.
- All downstream consumers must obtain historical semantics through one shared normalization/projection path rather than independently parsing raw event payloads.
- Derived state may be checkpointed for bounded replay, but a checkpoint is an accelerator with an explicit history and semantic-dependency boundary, not authoritative history.

### Deliberately not frozen
- Any particular ACT-R-inspired ranking formula used by an agent-memory product.
- A universal vector-store or semantic-search representation.
- A single global learner summary/profile.
- A universal plugin/provider runtime.
- A specific checkpoint serialization or storage backend.

## Appendix G - Dual-Profile Generalization (v2.3)
Foundation v2.3 adds AI-agent long-term memory as a primary proving use case and refactors the root architecture so learner-specific concepts are no longer implied to be universal memory concepts. This is a scope generalization, not a claim that human and agent memory are scientifically equivalent.

### G.1 Shared-core rule
A concept belongs in the shared Memory Core only when the Learning Profile and Agent Memory Profile can both consume it without weakening or distorting either profile. Reuse alone is not sufficient justification.
- Shared core: opaque stable identity, semantic versioning, provenance/lineage, typed scope, canonical durable history, artifacts, derived indexes, purpose-specific projections, replay boundaries/checkpoints, local-first persistence, compatibility envelopes, and retrieval infrastructure.
- Learning-only by default: KnowledgeUnit/KnowledgeComponent, RecallForm, LearningEpisode semantics, EvaluationOutcome, MemoryEvidence, LearnerMemoryModel, SchedulingPolicy, learning diagnostics, and exposure-as-learning evidence.
- Agent-only by default: agent capture policy, AgentMemoryObservation, MemoryRecord/consolidation, retrieval ranking for context, AgentContextProjection, context-injection provenance, and memory feedback/utility signals.
- A shared term must not smuggle one profile's semantics into the other. Namespacing is preferred over artificially universal entities.

### G.2 Core architecture
Memory Core
  Identity / Version / Provenance / Lineage
  MemoryScope
  CanonicalHistory<T profile record>
  Artifact + DerivedIndex
  HistoryBoundary / ReplayCheckpoint
  Retrieval primitives
  Projection + ProjectionBudget
  Persistence / backup / compatibility

Learning Profile
  Knowledge -> Learning interaction -> Evaluation -> Evidence
  -> LearnerMemoryModel -> Scheduling / Recall selection

Agent Memory Profile
  Agent/session activity -> AgentMemoryObservation
  -> extraction/consolidation -> MemoryRecord
  -> retrieval/ranking -> AgentContextProjection

### G.3 MemoryScope
MemoryScope is promoted as a shared-core concept because both profiles require explicit applicability and isolation boundaries. The core owns the shape and composition rules; each profile owns its scope vocabulary. Agent-memory scope is correctness- and privacy-relevant, not a cosmetic tag.

| Profile | Illustrative scope facets |
|---|---|
| Learning | learner, course/domain, collection/curriculum, context family |
| Agent | principal/user, agent, workspace/project, conversation, session, task |


### G.4 Agent Memory Profile
The Agent Memory Profile is not a vector database wrapper and not a copy of Hermes/Mem0/claude-mem. It defines durable semantics for capturing what happened, deriving candidate memories, consolidating them with provenance, retrieving under scope and budget, and projecting selected memory into an agent request. Exact memory taxonomies and ranking formulas remain provisional.
- AgentMemoryObservation preserves source identity (session/turn/tool/message references where available), occurred/recorded time, producer, scope, and information-origin context.
- MemoryRecord is a derived durable memory artifact with stable identity, provenance, scope, lineage, and supersession/consolidation history; it is not canonical conversation history.
- Context fencing is mandatory: information recalled by the system and injected into an agent request cannot later be captured as independent new evidence merely because the assistant repeats it.
- Retrieval uses identity and structured scope first; lexical/semantic retrieval discovers candidates but does not define identity or truth.
- AgentContextProjection is a purpose-specific, budgeted, lossy view. The exact projection injected into a model request must be reconstructable/auditable when it materially affects behavior.

### G.5 Minion-Agent integration boundary
Minion-Agent is a primary proving consumer, not semantic authority for Mneme. Current Minion-Agent already exposes clean seams: open request-header components (including a documented memory component), prompt-section composition, an open session-event namespace, and a scoped runtime service/plugin system. Mneme integrates through an adapter; Mneme itself does not adopt Minion-Agent's runtime framework.
Minion-Agent authoritative session history
        | capture references
        v
Minion-Memory Agent Adapter
        v
AgentMemoryObservation -> MemoryRecord/indexes
        |
        | retrieve(scope, query, budget)
        v
AgentContextProjection
        |
        v
Minion-Agent request/header["memory"] -> model request
Minion-Agent SessionStorage remains separate from Minion-Memory. Conversation/session history is authoritative execution history; long-term memory is a selected/interpreted layer derived from observations. Compaction of a conversation is not memory consolidation, and memory consolidation must not rewrite Minion-Agent session history.

### G.6 Renaming and namespace clarification
The term MemoryModel in the learning documents is learner-specific. New code and normalized specifications should prefer `LearnerMemoryModel` or the namespaced form `learning.MemoryModel`. Existing references may remain as compatibility aliases during migration.

### G.7 v2.3 status

| Decision | Status |
|---|---|
| Two primary proving profiles: Human Learning + Agent Memory | FROZEN |
| Shared-core admission rule: no semantic distortion | FROZEN |
| Minion-Agent as primary Agent Memory integration | FROZEN |
| SessionStorage and long-term memory remain distinct | FROZEN |
| MemoryScope exists in core; profile vocabularies remain profile-owned | FROZEN boundary / PROVISIONAL vocabulary |
| Agent Memory record taxonomy | PROVISIONAL |
| Agent retrieval/ranking formula | PROVISIONAL |
| Specific embedding/vector backend | NOT FROZEN |
| Agent consolidation algorithm | PROVISIONAL |


### G.8 Implementation-reference snapshot
Integration feasibility was verified against EGAILab/minion-agent main at commit d37171d716fe8fc44b5c16fec9c69705f8c74760 (2026-10-09). Relevant seams include `minion-agent-python/src/minion_agent/session/request_header.py`, `system_prompt/composer.py`, `session/events.py`, and the runtime service/context layer. Minion-Agent design documentation already models request-header components such as `memory` and identifies per-turn memory recall as product behavior. This snapshot is integration evidence, not Mneme semantic authority.
Reference: https://github.com/EGAILab/minion-agent and https://github.com/EGAILab/minion-agent-docs

## v2.3 Closing Position
Project Mneme is now intentionally dual-profile. The durable core should be general enough to support both a scientifically cautious learner-memory model and a practical agent long-term-memory system, while refusing to pretend those domains are identical. The strongest core is the intersection of stable engineering semantics - identity, provenance, history, scope, projection, retrieval, replay, durability and compatibility - with profile-specific meaning remaining at the edges.
