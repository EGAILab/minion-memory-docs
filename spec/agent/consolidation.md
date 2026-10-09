# Agent Memory Profile — consolidation — DRAFT normalization

Conventions: `spec/README.md`. Profile for every requirement: **agent**.

### ACON-001 — ConsolidationOutcome
<a id="acon-001"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R05 §5.4] [R05 §6] [MVP §18.3]

Consolidation is a derived interpretation over observations/records. A ConsolidationOutcome may
create, update-by-new-version, supersede, merge, split or retire MemoryRecords, with stable
identity, lineage, supersession and provenance.

### ACON-002 — Consolidation never touches source observations
<a id="acon-002"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R05 §5.4] [IAA §A31] [R05 §16]

Consolidation never deletes or semantically merges AgentMemoryObservation history. It may merge or
supersede derived MemoryRecords while preserving every source lineage.

### ACON-003 — Consolidation is attributable
<a id="acon-003"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R05 §5.4]

Every consolidation result records its policy, producer, version and source lineage.

### ACON-004 — Consolidation is not conversation compaction
<a id="acon-004"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [FND §G.5] [R05 §4] [R04 §42] [IAA §A29]

Conversation compaction is not memory consolidation. Memory consolidation must not rewrite
Minion-Agent session history, and clearing/compacting a conversation is not equivalent to
deleting/consolidating long-term memory. The two are independently testable and cannot rewrite each
other's canonical records.

### ACON-005 — Consolidation algorithm is provisional
<a id="acon-005"></a>
- **Profile:** agent · **Source status:** PROVISIONAL · **Sources:** [FND §G.7] [R05 §17]

The agent consolidation algorithm is PROVISIONAL; a learned consolidation model is deferred.

### ACON-006 — Consolidation runs asynchronously
<a id="acon-006"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R05 §6] [R05 §10]

Extraction/consolidation/indexing run asynchronously, without blocking critical agent operation,
and are retryable.

### ACON-007 — Agent consolidation does not change learning rules
<a id="acon-007"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R00 §21] [R03 §28] [IAA §13]

Agent Memory's consolidation of derived MemoryRecords under its own policy does not change the
Learning Profile rule that learning history is never semantically deduplicated, and agent
consolidation algorithms are not promoted into a theory of human memory.
