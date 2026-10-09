# Learning Profile — LearningEpisode, LearningEvent and RawObservation — DRAFT normalization

Conventions: `spec/README.md`. Profile for every requirement: **learning**.

## LEARN — interaction history

### LEARN-001 — LearningEpisode
<a id="learn-001"></a>
- **Profile:** learning · **Source status:** FROZEN · **Sources:** [FND §6] [MVP §3] [R00 §6] [R03 §4]

A bounded learning/review interaction is a LearningEpisode containing deterministically ordered
LearningEvents (HIST-003). Episode identity is stable and unique. Episode context records the
actual execution context, not authored RecallForm semantics.

### LEARN-002 — Event vocabulary
<a id="learn-002"></a>
- **Profile:** learning · **Source status:** PROVISIONAL · **Sources:** [FND §6] [FND §19] [FND §App-E] [MVP §5.1] [R00 §6] [R03 §5]

Ordered typed events are FROZEN; the subtype vocabulary is PROVISIONAL and extensible. The MVP
minimum vocabulary is: AttemptEvent (answer/rating submission), HintEvent (requested or presented
hint), ExposureEvent (content shown without claiming retrieval success) and a distinguishable
Completion versus Skip/Abandon status.

*Note:* [R03 §5] illustrates PromptPresented/Attempt/Reveal-or-Exposure/Rating/Completion;
[FND §6] adds Feedback/Skip/Abandon. Both are illustrative vocabularies.

### LEARN-003 — Flashcard projection of an episode
<a id="learn-003"></a>
- **Profile:** learning · **Source status:** MVP_ONLY · **Sources:** [FND §6] [FND §18] [MVP §5] [R03 §5] [R03 §20]

A flashcard review may be one LearningEpisode with one main attempt plus reveal/rating-related
events. The MVP may serialize several event semantics in one append-only record provided the domain
distinctions remain explicit.

### LEARN-004 — Event envelope
<a id="learn-004"></a>
- **Profile:** learning · **Source status:** GUARDRAIL · **Sources:** [R04 §9] [R04 §27] [IAA §3]

A serialized LearningEvent envelope conceptually carries: event_id, episode_id, sequence_no,
event_type, schema_version, compatibility (`required | ignorable`), occurred_at, recorded_at,
payload and provenance. Exact field names are implementation-specific; the envelope exists for
durable compatibility independent of each language's typed event hierarchy.

### LEARN-005 — Completed episodes are never lost; review sessions are runtime
<a id="learn-005"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R04 §29] [R00 §17] [MVP §13]

A runtime ReviewSession (queue, current index, reveal/UI state, filters) may be reconstructed or
discarded; completed durable LearningEpisodes must not be lost. One completed flashcard review
produces a valid LearningEpisode with deterministic event order.

### LEARN-006 — Abandonment is not negative evidence
<a id="learn-006"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R03 §5] [R00 §7.1]

A missing answer or an abandoned episode must not automatically become negative memory evidence.

### LEARN-007 — Historical execution snapshot
<a id="learn-007"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R03 §11] [FND §8] [IAA §A3] [R04 §10]

Each completed episode preserves enough immutable historical semantics to explain what the learner
actually encountered after Knowledge evolves: RecallForm ID+version; relevant Knowledge target
IDs+versions; the prompt/stimulus actually shown when needed; the expected response/evaluation
definition or evaluator reference/version; the EvidenceMapping reference/version used; hints
actually available/used when relevant; asset ID/version/checksum references; and the execution
context needed to interpret the observation. Snapshots follow semantic sufficiency, not complete
duplication.

### LEARN-008 — Interaction commits carry operation identity
<a id="learn-008"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R00 §20.2] [R04 §32] [R04 §40] [IAA §A18]

A completed learner interaction commit carries a durable operation/submission identity; retrying
the same operation identity produces one historical interaction (CORE-012, PERS-006).

### LEARN-009 — No extra learner burden in the MVP flow
<a id="learn-009"></a>
- **Profile:** learning · **Source status:** MVP_ONLY · **Sources:** [R03 §20] [R03 §23] [MVP §13] [R00 §2]

The current prompt → recall → reveal → Again/Hard/Good/Easy flow stays usable without additional
required learner prompts: no extra confidence question, no request to classify error cause; timing
and exposure metadata are captured automatically.

### LEARN-010 — Corrections reference originals
<a id="learn-010"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R03 §14] [R04 §9]

If the learner or app must correct accidental input, a correction record references the original
event (target event, reason, replacement semantics) instead of mutating it in place.

## OBS — raw observation and exposure

### OBS-001 — RawObservation is the strongest historical authority
<a id="obs-001"></a>
- **Profile:** learning · **Source status:** FROZEN · **Sources:** [FND §7] [FND §8] [MVP §3] [R00 §7.1] [R03 §6] [R04 §10]

RawObservation records what the learner actually did or submitted, or what the app directly
observed, before inferring what it means. RawObservation, EvaluationOutcome and MemoryEvidence are
separate concepts that remain semantically distinct even when stored together.

### OBS-002 — Rich raw capture when practical
<a id="obs-002"></a>
- **Profile:** learning · **Source status:** FROZEN · **Sources:** [FND §7.1] [R00 §7.1] [R03 §6.1] [MVP §6]

Persist the richest raw observation necessary for future interpretation whenever practical,
subject to PRIV-001/PRIV-002 — e.g. typed text/numeric expressions, selected choices, submitted
code, ordering manipulations, timing, hint use, skip/abandon behavior. Raw responses are retained
for typed/structured interactions when practical.

### OBS-003 — Signals are observations, not verdicts
<a id="obs-003"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R00 §7.1] [R03 §6.1] [R02 §9]

Response time, hint requests/presentation, exposure, skips, retries and self-ratings are
observations/signals. None automatically equals memory success or failure, response time is not a
direct memory-strength measurement, and none directly mutates a universal mastery variable; their
interpretation belongs to EvidenceMapping/LearnerMemoryModel.

### OBS-004 — Unknown is never defaulted
<a id="obs-004"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R03 §6.1] [FND §7.3] [R00 §7.3]

Unknown or absent information remains unknown; it is never defaulted to false, zero or failure.

### OBS-005 — Raw observations are immutable
<a id="obs-005"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R04 §10] [R04 §35] [R03 §13] [R04 §40]

RawObservation fields are never overwritten by later evaluation; re-evaluation appends (HIST-007).

### OBS-006 — Exposure provenance
<a id="obs-006"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [MVP §M4] [R00 §20.3] [R03 §27.2] [IAA §4] [IAA §A7] [R04 §30]

Information the system exposed before an attempt is part of historical context: prompt
content/version, hints, answer reveal, sibling/related RecallForms, worked examples or other
assistance. Enough provenance is preserved to distinguish independent retrieval from performance
after system-provided information, and it survives into later evidence interpretation. The MVP may
store compact exposure references rather than a sophisticated information-origin model.

### OBS-007 — Exposure is not retrieval
<a id="obs-007"></a>
- **Profile:** learning · **Source status:** FROZEN · **Sources:** [FND §5.1] [MVP §6] [MVP §13] [R00 §5] [R03 §9] [R03 §23]

Active retrieval and exposure-only must be distinguishable. Exposure may inform future models but
is never recorded as successful retrieval merely because content was displayed.

### OBS-008 — Hint progression
<a id="obs-008"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R03 §10]

Hint usage is learner history and the sequence of assistance is preserved when available. The MVP
may record only whether a hint was used, but the schema must not assume a single hint count is the
final semantic model.
