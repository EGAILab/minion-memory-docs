# Agent Memory Profile — retrieval and ranking — DRAFT normalization

Conventions: `spec/README.md`. Profile for every requirement: **agent**.

### ARET-001 — RetrievalQuery
<a id="aret-001"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R05 §5.5] [R05 §10]

A RetrievalQuery carries purpose, allowed scope, structured filters, query text/embedding input
where used, and a projection budget. Pre-request queries are built from agent/user/workspace/
conversation/task context.

### ARET-002 — Candidate discovery
<a id="aret-002"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R05 §5.5] [R05 §8] [FND §G.4]

Candidate retrieval may combine exact identity, structured query, lexical search, semantic
similarity, recency/importance/utility signals and profile-specific ranking, in the authority order
of RET-001; similarity is discovery, never identity or authority.

### ARET-003 — Scope before ranking
<a id="aret-003"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R05 §8] [R05 §5.3] [R05 §16]

Hard scope/privacy constraints apply before ranking and cannot be overridden by similarity
(SCOPE-006).

### ARET-004 — Ranking signals; no frozen formula
<a id="aret-004"></a>
- **Profile:** agent · **Source status:** PROVISIONAL · **Sources:** [R05 §8] [R05 §17] [FND §G.7] [FND §deliberately-not-frozen]

Ranking MAY use recency, reinforcement/confirmation, utility, source quality, importance or domain
signals, but no universal score or ranking formula (including any ACT-R-inspired formula) is
frozen. A learned ranking model and a universal importance/trust/reinforcement score are deferred.

### ARET-005 — Pre-request retrieval is scoped and budgeted
<a id="aret-005"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R05 §10] [MVP §18.3] [R05 §9]

Agent-context retrieval is scope-aware and runs under an explicit context/projection budget.

### ARET-006 — Deterministic rebuild equivalence
<a id="aret-006"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R05 §16]

Deleting indexes/checkpoints and rebuilding produces equivalent discoverability and projections for
deterministic policies.

### ARET-007 — Agent policy is not learner scheduling
<a id="aret-007"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [IAA §A34] [R05 §18] [R02 §17]

Agent retrieval/ranking policy and learner scheduling policy are distinct capabilities even when
they reuse budgets, indexes or projection utilities.
