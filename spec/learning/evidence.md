# Learning Profile — Evaluation, evidence and diagnostics — DRAFT normalization

Conventions: `spec/README.md`. Profile for every requirement: **learning**.

## EVAL — EvaluationOutcome

### EVAL-001 — EvaluationOutcome is the evaluator's conclusion
<a id="eval-001"></a>
- **Profile:** learning · **Source status:** FROZEN · **Sources:** [FND §7.2] [MVP §3] [R00 §7.2] [R03 §7] [R04 §10]

EvaluationOutcome records what a specific evaluator concluded about a response (exact/normalized
match, numeric tolerance, symbolic equivalence, test vector, partial correctness, invalid syntax,
self-rating interpretation, manual/AI assessment...), independent of memory attribution. Evaluator
identity/version and relevant normalization rules remain attributable, with enough structure for
future reinterpretation where practical.

### EVAL-002 — Evaluator kinds and provenance
<a id="eval-002"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R03 §7] [R03 §20] [MVP §7.1]

Self-assessment may produce a minimal outcome from Again/Hard/Good/Easy; deterministic evaluators
may produce richer structured outcomes; optional AI evaluators identify model/service/version
provenance where available. For current self-assessed cards a minimal outcome is sufficient.

### EVAL-003 — Evaluator changes never mutate historical outcomes
<a id="eval-003"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R03 §7] [R03 §13] [R04 §35]

Changing an evaluator does not mutate historical outcomes; a new evaluation may be derived from the
same raw observation and appended (HIST-007).

### EVAL-004 — Standards response processing maps to EvaluationOutcome
<a id="eval-004"></a>
- **Profile:** learning · **Source status:** FROZEN · **Sources:** [FND §13]

A QTI-like response evaluation corresponds to EvaluationOutcome; MemoryEvidence remains a separate
Mneme concern.

## EVID — MemoryEvidence, contamination, diagnostics

### EVID-001 — MemoryEvidence is interpretation, not fact
<a id="evid-001"></a>
- **Profile:** learning · **Source status:** FROZEN · **Sources:** [FND §7.3] [MVP §3] [R00 §7.3] [R03 §8]

MemoryEvidence is a versioned, provenance-bearing interpretation that an observation/outcome
supports, contradicts or is insufficient to assess a memory-relevant target under a particular
mapping. It is not the raw historical fact and not learner state.

### EVID-002 — Evidence directions and quality
<a id="evid-002"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [FND §7.3] [R03 §8] [R03 §8.1] [FND §App-D]

Evidence may be positive, negative/contradictory, ambiguous, insufficient or partial, and may carry
quality/confidence. Attribution may be ambiguous or insufficient; quality reflecting response mode,
assistance, evaluator reliability or ambiguity is a mapping/model concern, not a raw fact.

### EVID-003 — Missing evidence is unknown
<a id="evid-003"></a>
- **Profile:** learning · **Source status:** FROZEN · **Sources:** [FND §7.3] [FND §19] [MVP §6] [R00 §4.2] [R00 §7.3] [R03 §23]

Missing evidence remains unknown; it is semantically different from weak or forgotten and must
never be silently converted to failure, zero or forgotten. Absent/insufficient/ambiguous evidence
stays absent/insufficient/ambiguous.

### EVID-004 — Declared coverage is not obtained evidence
<a id="evid-004"></a>
- **Profile:** learning · **Source status:** FROZEN · **Sources:** [FND §5] [MVP §6] [R03 §8.1] [R03 §23]

A RecallForm's declared test coverage does not imply evidence was obtained for every declared
component, and a failed multi-target task must not automatically mark all declared targets as
failed.

### EVID-005 — Evidence mappings are versioned
<a id="evid-005"></a>
- **Profile:** learning · **Source status:** FROZEN · **Sources:** [FND §7.3] [FND §App-E] [R00 §7.3] [R01 §6] [MVP §6]

Evidence attribution rules or models are separately versioned and provenance-bearing. Declarative
EvidenceMappings authored with a RecallForm may live in Knowledge; learned/inferred mappers may
live in an inference layer. Historical evidence carries enough provenance to identify the
evaluator/mapping version that produced it.

### EVID-006 — Historical evidence is never rewritten
<a id="evid-006"></a>
- **Profile:** learning · **Source status:** FROZEN · **Sources:** [FND §8] [FND §14] [MVP §6] [R03 §8.1] [R03 §13] [R04 §35] [R04 §40]

Historical evidence retains its mapping/provenance/version and is not rewritten when mappings
improve; reinterpretation appends new evidence (HIST-007). The current LearnerMemoryModel may
choose the latest trusted evidence set without erasing previous interpretations.

### EVID-007 — Self-rating is an MVP signal
<a id="evid-007"></a>
- **Profile:** learning · **Source status:** MVP_ONLY · **Sources:** [MVP §6] [MVP §14] [R00 §7.3] [R03 §20]

Again/Hard/Good/Easy is an MVP self-assessment signal, not a universal evidence ontology. Minimal
versioned MemoryEvidence for declared KnowledgePoint targets is produced only when justified.

### EVID-008 — Exposure contamination qualifies evidence
<a id="evid-008"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R02 §8] [IAA §4] [FND §5.2] [R03 §27.2]

If a prior event/form exposed information required by a later form, that later performance is
marked or discounted according to policy rather than treated as independent unaided retrieval.
Information origin is an input to evidence/state reduction; an EvidenceMapper can discount or
qualify evidence without rewriting the observation.

### EVID-009 — Diagnostics are derived and uncertainty-preserving
<a id="evid-009"></a>
- **Profile:** learning · **Source status:** PROVISIONAL · **Sources:** [FND §12] [R02 §14] [R03 §15] [R03 §15.1] [R03 §15.2]

Diagnostics (repeated failure, hint dependence, contamination, latency, evaluator/self-rating
mismatch, form-specific weakness, leech/pathology) are derived, auditable views over history and
model output, never source-of-truth history or permanent Knowledge truth. They preserve
uncertainty: with ambiguous attribution or low coverage they report insufficient evidence rather
than invent a precise diagnosis.

### EVID-010 — Repeated failure triggers diagnostic suspicion
<a id="evid-010"></a>
- **Profile:** learning · **Source status:** FROZEN · **Sources:** [FND §12]

Repeated failure should trigger diagnostic suspicion (bad form, too-broad component, wrong mapping,
interference, missing prerequisite, content error, understanding problem) rather than infinite
interval shortening.

### EVID-011 — Model-validation feedback is meta-evidence
<a id="evid-011"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R03 §28]

Feedback validating an evaluator or diagnostic is meta-evidence about the model, not learner
MemoryEvidence and not Agent Memory truth.

### EVID-012 — Progressive diagnostic reads
<a id="evid-012"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R03 §27.5]

Diagnostics should retrieve history progressively (index/aggregate candidate → surrounding
episode/timeline context → selected full observations) and may use structured/lexical/semantic
discovery; retrieval indexes remain rebuildable and cannot determine learner truth.
