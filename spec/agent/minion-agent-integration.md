# Agent Memory Profile — Minion-Agent integration — DRAFT normalization

Conventions: `spec/README.md`. Profile for every requirement: **agent**. Minion-Agent is
authoritative only for its own side of the seam. The WP-00 seam audit
(`assurance/layers/00-minion-agent-seam-audit.md`) found that the `memory` request-header component
is documented but not wired at the audited revision (NF-007); MINT-009 transcribes the sources and
does not resolve that.

### MINT-001 — Minion-Agent is a consumer, not authority
<a id="mint-001"></a>
- **Profile:** agent · **Source status:** FROZEN · **Sources:** [FND §G.5] [FND §G.7] [FND §G.8] [R05 §2] [R05 §3]

Minion-Agent is the primary Agent Memory consumer and integration target, not Mneme semantic
authority. Integration evidence is pinned to an exact Minion-Agent revision and is evidence, not
authority.

### MINT-002 — Session storage and long-term memory are separate
<a id="mint-002"></a>
- **Profile:** agent · **Source status:** FROZEN · **Sources:** [FND §G.5] [FND §G.7] [MVP §18.4] [R04 §41.2] [R05 §4] [IAA §A29]

Minion-Agent owns authoritative conversation/session execution history (messages, tool results,
request state, compaction, forks) with its own durability/replay requirements. Minion-Memory owns
long-term memory observations, records, indexes and projections. Minion-Agent SessionStorage is
not an implementation of Minion-Memory and is not absorbed or migrated into it as the canonical
long-term-memory store; an adapter may persist stable references between them, but neither
replaces the other.

### MINT-003 — Independent lifecycles
<a id="mint-003"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R05 §4] [R05 §16] [R04 §42]

Clearing/compacting a conversation is not deleting/consolidating long-term memory, and rebuilding
memory indexes cannot alter agent execution history. SessionStorage and Minion-Memory storage can
fail and recover independently without corrupting each other.

### MINT-004 — Adapter stages
<a id="mint-004"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R05 §10] [FND §G.5]

The adapter: pre-request — builds a RetrievalQuery and retrieves/projects memory within budget;
request assembly — provides the exact memory projection through a Minion-Agent prompt/header seam,
preserving projection identity and record-version references; post-turn — after authoritative
session history exists, captures source references and origin context idempotently; async — runs
extraction/consolidation/indexing without blocking critical agent operation; failure — fails open
for optional recall/enrichment and never corrupts or rewrites Minion-Agent session history.

### MINT-005 — Adapter, not framework coupling
<a id="mint-005"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R05 §10] [IAA §A33] [FND §G.5]

The adapter MAY be packaged as a Minion-Agent plugin/service provider. The Minion-Memory engine
itself MUST NOT require Minion-Agent/Cordis plugin infrastructure, service locators or plugin
internals and remains independently usable.

### MINT-006 — Request reconstruction
<a id="mint-006"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R05 §11] [R04 §42] [IAA §12]

When memory context is model-visible, the integration preserves projection identity or content
reference, selected MemoryRecord IDs/versions, policy/version, scope and budget, complementing
Minion-Agent's content-addressed request-header invariant, without copying the entire session log
into Minion-Memory.

### MINT-007 — Memory degradation is not fatal by default
<a id="mint-007"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R05 §14]

Minion-Agent remains functional if Minion-Memory is unavailable; memory degradation is observable
but not fatal unless the application explicitly configures memory as mandatory.

### MINT-008 — Event domains stay separate
<a id="mint-008"></a>
- **Profile:** agent · **Source status:** GUARDRAIL · **Sources:** [IAA §12] [IAA §13]

Adapter-specific audit/reference events MAY use Minion-Agent's open session-event namespace where
justified; agent session events are never reclassified as learning events.

### MINT-009 — Injection through the existing seam
<a id="mint-009"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R05 §10] [R05 §16] [IAA §12] [FND §G.5]

The adapter injects a scoped, budgeted memory projection through Minion-Agent's existing
request/prompt seam (request-header `memory` component and/or contributed prompt sections) and can
identify the exact records used.

*Note:* the sources name two candidate seams; using both would create two injection paths. Which
one is canonical, and the gap that the `memory` header component is not wired in the audited
driver, are open (NF-007, NF-008).
