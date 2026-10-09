# Agent Memory Profile — AgentMemoryObservation capture — DRAFT normalization

Conventions: `spec/README.md`. Profile for every requirement: **agent**. The Agent Memory Profile is
not a vector-database wrapper and not a copy of Hermes/Mem0/claude-mem ([FND §G.4]).

### ACAP-001 — AgentMemoryObservation
<a id="acap-001"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R05 §5.1] [FND §G.4] [MVP §18.3]

An AgentMemoryObservation is a durable source observation about agent-relevant information. It
records what source material was observed and enough provenance to reason about its origin, without
claiming the extracted content is already a trusted memory fact. Field families: id/version (stable
opaque identity; schema/semantic version as applicable); source_ref (stable reference to the
Minion-Agent session/turn/message/tool/artifact where available); occurred_at/recorded_at (source
time vs durable-capture time); scope (MemoryScope facets); origin; payload/content_ref
(privacy-bounded raw/structured observation or content-addressed reference); provenance (producer,
adapter version, capture policy/version).

### ACAP-002 — Capture order
<a id="acap-002"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R05 §6] [R05 §10] [R04 §41.3] [MVP §18.3]

Capture follows an authoritative Minion-Agent turn/session commit. The adapter durably captures the
source reference plus origin and scope (the durability barrier, PERS-004) before any optional
extraction, consolidation, embedding, LLM summarization, remote sync or AI enrichment, which may run
later. Expensive work cannot make authoritative source history best-effort.

### ACAP-003 — Capture is idempotent
<a id="acap-003"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R05 §6] [R05 §14] [R05 §10]

Capture is idempotent by durable operation/source identity: crash/retry of the same capture
operation/source identity cannot create duplicate source observations (CORE-012).

### ACAP-004 — Capture stays off the agent's critical path
<a id="acap-004"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R05 §6] [R05 §10] [R05 §16]

The adapter must not block the agent request/turn critical path on optional enrichment. Optional
extraction/vector/AI failure does not block the authoritative session commit or durable source
capture.

### ACAP-005 — Recoverable pending enrichment
<a id="acap-005"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R05 §14] [R04 §41.3]

Failure after source capture but before extraction leaves a recoverable pending-enrichment state;
the source reference is not lost. Agent-memory derived work is asynchronous and retryable, and loss
of optional derived state must not corrupt Minion-Agent session history.

### ACAP-006 — Similar observations remain distinct
<a id="acap-006"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R05 §16] [IAA §A31] [R03 §28]

Two source observations with similar (even identical) text at different times remain distinct
observations; consolidation may relate them without deleting lineage (HIST-008).

### ACAP-007 — Origin distinguishes recalled from external information
<a id="acap-007"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R05 §5.1] [R05 §7] [IAA §A30] [FND §G.4]

`origin` distinguishes external/user/tool/environment information from recalled/injected/
system-generated context, recording which injected projection/records were involved (e.g.
`recalled_projection=P12 / record=R7`) so later processing can fence it (ACTX-004).

### ACAP-008 — Capture references session history; it does not copy or replace it
<a id="acap-008"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R05 §4] [R04 §42] [R04 §41.2]

Capture stores stable source references and provenance. It does not replace Minion-Agent session
history and does not copy the entire session log into Minion-Memory; the two stores may reference
each other.
