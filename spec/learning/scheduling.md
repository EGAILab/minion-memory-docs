# Learning Profile — scheduling and RecallForm selection — DRAFT normalization

Conventions: `spec/README.md`. Profile for every requirement: **learning**.

### SCHED-001 — Prediction is not policy
<a id="sched-001"></a>
- **Profile:** learning · **Source status:** FROZEN · **Sources:** [FND §11] [FND §19] [R00 §9] [R02 §2] [MVP §7.1]

Memory prediction and scheduling policy are separate layers, even if one module implements both
initially. The canonical pipeline is: history → shared HistoryProjector → evaluation/evidence →
LearnerMemoryModel → predictions/state → SchedulingPolicy → target selection → RecallForm
selector. The scheduler decides WHEN/what deserves review; the selector decides HOW to obtain
useful evidence.

### SCHED-002 — Policy is not a single scalar
<a id="sched-002"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [FND §11] [R02 §5] [IAA §A25]

Scheduling consumes model predictions plus policy inputs (importance, desired retention,
workload/time budget, goals/deadlines, product constraints). A single scalar score must not be
assumed; policies may combine hard constraints, reserved categories/quotas and ranking within
candidate groups.

### SCHED-003 — Budgets are not only item counts
<a id="sched-003"></a>
- **Profile:** learning · **Source status:** PROVISIONAL · **Sources:** [R02 §6] [FND §11]

The MVP may keep simple daily limits, but interfaces must not make "N cards" the only budget
representation; general scheduling reasons about estimated learning-opportunity cost/time.
LearningOpportunity is PROVISIONAL and not required by the MVP.

### SCHED-004 — FixedInterval and adaptive strategies
<a id="sched-004"></a>
- **Profile:** learning · **Source status:** MVP_ONLY · **Sources:** [MVP §7.1] [MVP §13] [R00 §9] [R02 §4] [R02 §16]

FixedIntervalStrategy remains a first-class compatibility strategy that reproduces legacy
behavior. A local interpretable adaptive strategy may use Again/Hard/Good/Easy plus elapsed time
and history, and may be substituted behind the policy boundary without changing Knowledge identity
or canonical history.

### SCHED-005 — Offline, AI-free scheduling critical path
<a id="sched-005"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [MVP §7.1] [R00 §9] [R02 §4] [R02 §13] [FND §18]

No AI dependency is permitted on the normal scheduling critical path. Next-review decisions needed
for normal use are possible from the local store; remote fitting, embeddings, sync or AI
diagnostics run asynchronously and fail open.

### SCHED-006 — Strategy selection is configuration
<a id="sched-006"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R02 §4] [R04 §4] [R04 §13]

Strategy selection and parameters belong to learner/app configuration, not Knowledge. Changing
strategy configuration must not mutate historical events.

### SCHED-007 — RecallForm selection
<a id="sched-007"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R02 §7] [R00 §9]

The selector chooses how to test a due/selected target; it may prefer forms that generate evidence
for weak or under-observed targets while respecting contamination/sibling suppression. RecallForm
identity does not itself define a unique memory trace.

### SCHED-008 — Sibling and contamination suppression
<a id="sched-008"></a>
- **Profile:** learning · **Source status:** FROZEN · **Sources:** [FND §5.2] [R00 §5] [R02 §7] [R02 §16]

Activity selection should suppress or discount follow-up probes whose tested targets were just
exposed by a related probe; recent answer exposure can suppress/discount sibling forms.

### SCHED-009 — Schedule state is replaceable
<a id="sched-009"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R04 §13] [R03 §17] [FND §14]

Schedule state (due timestamps, intervals, strategy caches) is materialized, replaceable decision
state, not learner-history truth. Historical scheduling decisions may be captured in a decision
snapshot for audit and are not rewritten when a later model would decide differently.

### SCHED-010 — Graph relations are features, not a scheduler
<a id="sched-010"></a>
- **Profile:** learning · **Source status:** FROZEN · **Sources:** [FND §11]

Knowledge graph relations may inform scheduling features but do not themselves constitute a
learning plan or scheduler.

### SCHED-011 — Learning scheduling is not agent ranking
<a id="sched-011"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R02 §17] [IAA §A34]

Prediction ≠ scheduling remains a Learning Profile invariant. AgentContextProjection budgets are
analogous engineering projections but are not learning schedules and produce no MemoryEvidence.
