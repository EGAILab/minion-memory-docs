# Learning Profile — LearnerMemoryModel and learner state — DRAFT normalization

Conventions: `spec/README.md`. Profile for every requirement: **learning**. `MemoryModel` here means
`LearnerMemoryModel` (ARCH-004).

### LMEM-001 — No universal learner-state schema
<a id="lmem-001"></a>
- **Profile:** learning · **Source status:** FROZEN · **Sources:** [FND §9] [R00 §8] [R04 §12] [IAA §6]

Mneme defines a replaceable LearnerMemoryModel boundary, not one universal learner-state schema. A
model consumes Knowledge references, evidence history, context and optional prior model state, and
produces model-specific state and predictions. FSRS-like stability/difficulty, BKT-like
probabilities etc. are adapters/payloads, not universal fields; persisted model state carries model
ID/version plus a model-specific payload.

### LMEM-002 — Learner state is latent, model-specific and rebuildable
<a id="lmem-002"></a>
- **Profile:** learning · **Source status:** FROZEN · **Sources:** [FND §3] [FND §9] [FND §19] [R00 §8] [R02 §3] [R03 §16] [MVP §7.1]

Learner state is latent and model-specific; events are observations, not direct measurements of
memory truth. Model state is rebuildable/materialized inference, never the durable source of truth,
and any cached learner state may be discarded and recomputed from durable history.

### LMEM-003 — No fabricated uncertainty
<a id="lmem-003"></a>
- **Profile:** learning · **Source status:** FROZEN · **Sources:** [FND §19] [FND §App-E] [R00 §8] [R03 §16] [R02 §3]

A model exposes uncertainty/confidence only when it has a meaningful representation; deterministic
models must not invent fake confidence, and absence of uncertainty is not replaced by false
precision.

### LMEM-004 — Component-to-state mapping is model-defined
<a id="lmem-004"></a>
- **Profile:** learning · **Source status:** FROZEN · **Sources:** [FND §9]

A KnowledgeComponent may map to zero, one or multiple learner-state representations depending on
the model.

### LMEM-005 — Context-conditioned accessibility
<a id="lmem-005"></a>
- **Profile:** learning · **Source status:** PROVISIONAL · **Sources:** [FND §9.1] [MVP §10] [FND §19]

Context/retrieval-route-conditioned state is conceptually necessary but its identity and storage
are model-specific; Mneme must not assume context-free mastery. No route/context-specific state is
required in the MVP beyond retaining data needed for future analysis. MemoryAssembly is a research
candidate only.

### LMEM-006 — Priors are not evidence
<a id="lmem-006"></a>
- **Profile:** learning · **Source status:** FROZEN · **Sources:** [FND §10]

Cold start uses explicit priors (population/default, domain, content-derived, personalized fitted
parameters); priors are not learner evidence. Learner model instances may have lifecycles and be
recalibrated over time.

### LMEM-007 — Definition, instance, state and policy are distinct
<a id="lmem-007"></a>
- **Profile:** learning · **Source status:** FROZEN · **Sources:** [FND §14] [FND §15] [FND §19]

MemoryModelDefinition (id/version), MemoryModelInstance (definition, fitted parameters,
training/history boundary, provenance), LearnerState (derived predictions/state at a time) and
SchedulingPolicy are distinct. Every derived learner model is versionable, replayable, comparable
and replaceable without loss of learner history.

### LMEM-008 — Deterministic rebuild equivalence
<a id="lmem-008"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R02 §16] [R04 §12] [R04 §22] [MVP §13] [R00 §17] [R03 §22]

Deleting derived learner state and replaying durable history produces an equivalent current state
for deterministic models under the same history/model/config. Derived state records sufficient
derivation provenance/boundary (model/strategy, version) to detect staleness.

### LMEM-009 — Mastery and urgency are projections
<a id="lmem-009"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R02 §3] [R04 §12] [R00 §2.1] [R03 §16]

Overall mastery, urgency and similar analytics are convenience projections, never source of truth;
no universal mastery scalar is required or persisted as canonical.

### LMEM-010 — Learning phase vocabulary is MVP-only
<a id="lmem-010"></a>
- **Profile:** learning · **Source status:** MVP_ONLY · **Sources:** [FND §10] [FND §19] [MVP §7.1] [R00 §9]

If modeled, learning phase belongs to learner/application state, not Knowledge.
new/learning/review/relearning are MVP lifecycle labels, not Foundation ontology.

### LMEM-011 — Re-inference and rescheduling are separate operations
<a id="lmem-011"></a>
- **Profile:** learning · **Source status:** FROZEN · **Sources:** [FND §14] [R02 §12] [R04 §13]

Rebuilding learner state with a new model does not automatically rewrite historical scheduling
decisions or force immediate rescheduling. Observed history and counterfactual simulation are
explicitly distinguished.

### LMEM-012 — Learner state does not follow split/merge
<a id="lmem-012"></a>
- **Profile:** learning · **Source status:** FROZEN · **Sources:** [FND §4.6] [R00 §10] [R01 §11] [R04 §7]

Learner state is not automatically copied or averaged across Knowledge split/merge operations.

### LMEM-013 — Interpretable baseline model
<a id="lmem-013"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [FND §15.1]

A simple interpretable baseline model is maintained as a permanent fallback and regression
benchmark.
