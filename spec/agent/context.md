# Agent Memory Profile — AgentContextProjection and context fencing — DRAFT normalization

Conventions: `spec/README.md`. Profile for every requirement: **agent**.

### ACTX-001 — AgentContextProjection
<a id="actx-001"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R05 §5.6] [FND §G.4] [MVP §18.3]

An AgentContextProjection is a lossy, purpose-specific, budgeted representation of selected
MemoryRecords for one agent request. It records projection policy/version, selected record
IDs/versions, scope, budget/cost, and a stable projection identity/content reference when needed for
request reconstruction.

### ACTX-002 — Projection budget
<a id="actx-002"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R05 §9] [R04 §38]

Agent-context projection is budgeted by actual resource cost where feasible (characters, tokens,
records, latency), not merely a fixed count. Degradation/removal applies only to the projection;
observations and MemoryRecords are unchanged (PROJ-003, PROJ-004).

### ACTX-003 — Model-visible projections are reconstructable
<a id="actx-003"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R05 §11] [FND §G.4] [IAA §A32] [MVP §18.3]

When memory context is model-visible, enough is preserved to explain/reconstruct the memory
projection that was dispatched: projection identity or content reference, selected MemoryRecord
IDs/versions, policy/version, scope and relevant budget.

*Note:* [FND §G.4] and [IAA §A32] state the obligation for projections that "materially affect
behavior"; that is the Foundation minimum. The more specific agent-profile rule [R05 §11] applies to
every model-visible memory projection, without a materiality exemption, matching MINT-006
(WP00-CR-009).

### ACTX-004 — Context fencing
<a id="actx-004"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [FND §G.4] [R05 §7] [MVP §18.3] [IAA §A30] [R05 §16] [R05 §18]

Context fencing is mandatory. Memory injected into an agent request is attributable to specific
MemoryRecord/projection identities, and subsequent capture knows which information was
system-provided. An assistant repetition of injected memory is not captured or reinforced as
independent new memory unless new external evidence corroborates it.

### ACTX-005 — Private records may be omitted
<a id="actx-005"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R05 §15]

A projection may omit private records even when they are semantically relevant (PRIV-006).
