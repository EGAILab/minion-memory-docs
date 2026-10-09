# Agent Memory Profile — MemoryRecord — DRAFT normalization

Conventions: `spec/README.md`. Profile for every requirement: **agent**.

### AMEM-001 — MemoryRecord is a derived durable artifact
<a id="amem-001"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R05 §5.2] [FND §G.4] [MVP §18.3]

A MemoryRecord is a derived durable long-term-memory artifact with stable identity, provenance,
scope, source lineage and supersession/consolidation history. It is not canonical conversation
history.

### AMEM-002 — Record taxonomy is provisional
<a id="amem-002"></a>
- **Profile:** agent · **Source status:** PROVISIONAL · **Sources:** [R05 §5.2] [R05 §17] [FND §G.7]

A MemoryRecord may represent a fact, preference, decision, project convention, procedure,
relationship, event summary or another profile-defined kind. The taxonomy is PROVISIONAL.

### AMEM-003 — Record evolution never rewrites sources
<a id="amem-003"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R05 §5.2] [R05 §5.4] [MVP §18.3]

A MemoryRecord may be superseded, merged, split or retired without rewriting source observations,
and canonical Minion-Agent session history is never rewritten.

### AMEM-004 — Extractor output is not canonical by default
<a id="amem-004"></a>
- **Profile:** agent · **Source status:** GUARDRAIL · **Sources:** [IAA §13] [IAA §patterns-still-deliberately-not-copied]

LLM-generated memories are not canonical merely because an extractor produced them.

### AMEM-005 — Canonical versus rebuildable agent data
<a id="amem-005"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R05 §12] [R04 §41.1] [R04 §42]

Canonical: AgentMemoryObservations and committed MemoryRecord lineage/consolidation history,
according to retention policy. Rebuildable: lexical/vector indexes, ranking caches, summaries,
embeddings (when their source/policy is retained) and AgentContextProjection caches unless audit
policy makes the exact projection durable. Deleting/rebuilding agent-memory indexes leaves source
observations and MemoryRecords intact.

*Note:* MemoryRecord is "derived" (AMEM-001) yet its committed lineage is "canonical" (this
requirement). Both statements are transcribed; how record versions relate to CORE-003 is open
(NF-012).
