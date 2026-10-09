# Learning Profile — Knowledge model and RecallForm — DRAFT normalization

Conventions: `spec/README.md`. Profile for every requirement: **learning**. ARCH-006 (layer
separation) applies throughout.

### KNOW-001 — KnowledgeUnit
<a id="know-001"></a>
- **Profile:** learning · **Source status:** FROZEN · **Sources:** [FND §4.1] [MVP §3] [R00 §4.1]

A KnowledgeUnit is an authored boundary for coherent presentation, review and provenance. It groups
or references KnowledgeComponents but does not define their identity, and it is not an atomic unit
of learner memory. Unit identity remains stable across ordinary content edits; material identity
changes require a new ID. It replaces the old core meaning of MemoryUnit.

### KNOW-002 — KnowledgeComponent
<a id="know-002"></a>
- **Profile:** learning · **Source status:** FROZEN · **Sources:** [FND §4.2] [FND §4.6] [R00 §4.2] [MVP §3]

A KnowledgeComponent is an authored, revisable modeling unit describing what should be retained or
made accessible: a stable assessable knowledge identity referenced by units. It is not an
objectively irreducible atom of knowledge; granularity is a modeling choice that may be revised
(split/merge per CORE-004). Knowledge-model evolution and learner-state migration are separate
problems.

### KNOW-003 — Component kinds
<a id="know-003"></a>
- **Profile:** learning · **Source status:** PROVISIONAL · **Sources:** [FND §4.3] [FND §4.4] [FND §4.5] [MVP §4.1] [MVP §4.2] [MVP §14] [R00 §4.3]

KnowledgeComponents require semantically distinct kinds. KnowledgePoint, KnowledgeStructure and
KnowledgeProcedure are the initial non-exhaustive taxonomy (PROVISIONAL). The MVP MUST implement
KnowledgePoint; the schema must permit additional kinds. KnowledgeStructure and KnowledgeProcedure
are schema reservations that may be rejected or ignored with explicit capability reporting until
renderers/evaluators exist.

### KNOW-004 — Cross-unit component reuse
<a id="know-004"></a>
- **Profile:** learning · **Source status:** FROZEN · **Sources:** [FND §4.2] [MVP §4.2] [R00 §4.1] [R01 §5] [FND §13.1]

The ontology permits a KnowledgeComponent to be referenced by several KnowledgeUnits; exact
canonicalization, deduplication and shared-identity rules remain PROVISIONAL. The MVP needs no
automatic deduplication or global canonicalization, and unit-local serialization of components does
not mean the unit owns their identity.

### KNOW-005 — KnowledgeStructure is not ComponentRelation
<a id="know-005"></a>
- **Profile:** learning · **Source status:** FROZEN · **Sources:** [FND §4.4] [FND §4.7] [FND §19]

A KnowledgeStructure is something the learner may need to remember (sequence, hierarchy, grid,
timeline, mapping...). A ComponentRelation is knowledge-model metadata. They are distinct;
remembering constituent facts does not imply remembering their structure and vice versa.

### KNOW-006 — Typed component relations
<a id="know-006"></a>
- **Profile:** learning · **Source status:** FROZEN · **Sources:** [FND §4.7] [FND §11] [MVP §4.2] [MVP §10] [R00 §4.4]

KnowledgeComponents may participate in typed semantic relations, separate from learner state and
scheduling; the concrete vocabulary is PROVISIONAL and extensible. Relations must not
automatically propagate mastery or memory state, and do not themselves constitute a learning plan
or scheduler. A relation graph is not required in the MVP, and Collection hierarchy is not a
substitute for it.

### KNOW-007 — Importance is Knowledge; difficulty is learner state
<a id="know-007"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R00 §4.2]

Importance belongs to Knowledge; learner difficulty/retention belongs to learner/model state.

### KNOW-008 — Collections are organization, not identity or mastery
<a id="know-008"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R00 §4.5] [R01 §7] [R00 §11] [FND §18] [R04 §8]

A Collection has a stable ID/version, optional key, name, optional parent (single parent in the
MVP), order and provenance where relevant. Unit–Collection membership is many-to-many, explicit
metadata, and never inferred from directory paths. Dynamic learner views (Due Today, Weak) are
filters, not Collections. Retiring a Collection never implicitly deletes a KnowledgeUnit or learner
history.

### KNOW-009 — Assets
<a id="know-009"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R00 §4.6] [R01 §8] [R04 §4]

Assets use stable identity/version or content hash, MIME/type, package-relative references and
integrity metadata. Canonical packages do not depend on remote URLs or base64 blobs; large media
may be externalized inside the package asset tree.

### KNOW-010 — LearningSupport is defined in Knowledge; usage is history
<a id="know-010"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R00 §4.6] [R03 §10]

LearningSupport (explanation, mnemonic, example, image, hint definitions) is authored Knowledge;
learner history records actual support exposure/usage.

### KNOW-011 — RecallForm is a semantic activity definition
<a id="know-011"></a>
- **Profile:** learning · **Source status:** FROZEN · **Sources:** [FND §5] [MVP §3] [R00 §5] [R01 §6] [FND §19]

A RecallForm is the authored semantic definition of a memory probe/activity, not a UI card:
stimulus/prompt, interaction(s)/response specification, evaluation spec or evaluator reference,
declarative EvidenceMapping(s) where declarative, learning support/hints, and declared
test/exposure semantics. Renderer implementation is not Knowledge ontology. The name RecallForm is
PROVISIONAL at Foundation level ("MemoryProbe" is a candidate) but is the normative implementation
term. The MVP uses self-assessed front/back and may support typed response where practical.

### KNOW-012 — RecallForm declares tests and exposes
<a id="know-012"></a>
- **Profile:** learning · **Source status:** FROZEN · **Sources:** [FND §5.1] [FND §5] [MVP §4.1] [R00 §5]

A RecallForm declares the components it is capable of testing and the knowledge it may expose.
Declared test coverage describes potential evidence, not evidence obtained in every attempt.

### KNOW-013 — Independent stable identities for Knowledge artifacts
<a id="know-013"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [MVP §4.1] [R01 §4] [R04 §22] [R04 §24]

KnowledgeUnit, KnowledgeComponent, RecallForm, Hint/Support, Collection and Asset (and versioned
support artifacts) each have independent stable IDs and versions. Component membership/reference
never derives identity from filesystem path or Collection hierarchy.

### KNOW-014 — Progressive-resolution presentation
<a id="know-014"></a>
- **Profile:** learning · **Source status:** GUARDRAIL · **Sources:** [IAA §A8]

Rich KnowledgeUnits may have multiple presentation resolutions or support layers; a rich stored
unit does not imply that every review displays all of its content.

### KNOW-015 — Current-version Knowledge storage
<a id="know-015"></a>
- **Profile:** learning · **Source status:** MVP_ONLY · **Sources:** [R04 §8] [MVP §8]

The MVP may keep only the current active Knowledge representation in main query storage, provided
historical records carry sufficient execution-snapshot/version references for interpretation and
full backup preserves the assets those snapshots require. Retired Knowledge remains interpretable
for historical events.

### KNOW-016 — Separation from Agent Memory
<a id="know-016"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R01 §1] [R01 §21] [R05 §17]

Agent Memory records are not Knowledge entities. Agent capture/consolidation must not silently mint
KnowledgeUnit identity from semantically similar MemoryRecords. Promotion of validated
agent-derived material into Knowledge is a future, explicit, provenance-preserving transformation,
never implicit consolidation (and automatic promotion is deferred).
