# WP-02 (Layer 02) — MemoryScope authority characterization

Status: READ-ONLY research input for the Layer 02 contract-first checkpoint (NF-018). Not a
decision, not a spec. Prepared by Claude.

Sources searched (all of them, case-insensitive): `reference/source-text/{FND,MVP,R00..R05,IAA,BOOT,SUMMARY}.md`
for: scope, MemoryScope, applicab, isolat, facet, principal, workspace, project, conversation,
session, task, tenant, user, visib/visible, inherit, contain, hierarch, namespac, cross-scope,
cross-agent, leak, privacy/private, learner, course, curriculum, collection, context family,
owner, device, consent. R05, IAA, BOOT, SUMMARY and FND App. F/G, MVP §8–§18, R00 §20–§21,
R01 (all), R02 §16–§17, R03 §18–§28 and R04 §20/§29–§42 were read in full; the rest was covered by
term search plus context reads.

Citation keys = file stems; anchors = `reference/source-index.yaml` anchors. Quotes are verbatim
from the derived Markdown (which is itself a non-authoritative reading aid of the DOCX).

Spec cross-read: `spec/scope.md` (SCOPE-001..006), NF-018, `spec/agent/{capture,records,retrieval,context,minion-agent-integration}.md`,
`spec/privacy.md`, `spec/core.md` (ARCH-003, CORE-013, RET-006), `spec/learning/package.md`,
`assurance/layers/00-dual-profile-boundary-review.md` §3.

---

## Part 1 — Passage register (verbatim)

Tags: **[S]** = MemoryScope proper; **[A]** = adjacent (bears on scope/isolation/privacy semantics);
**[H]** = homonym — the word "scope" in a different sense (must NOT be conflated with MemoryScope).

### 1.1 Foundation v2.3 (FND) — highest authority

| # | Tag | Quote | Cite |
|---|---|---|---|
| P01 | S | "it freezes a small shared core for identity, provenance, durable history, scopes, projections, retrieval, replay, and persistence, while keeping learner-specific evidence/scheduling semantics and agent-specific capture/consolidation/context semantics in separate profiles." | [FND §executive-summary] |
| P02 | S | "SHARED MEMORY CORE … Typed scope + canonical durable history" | [FND §executive-summary] |
| P03 | S | "AGENT MEMORY PROFILE … MemoryRecord + scope + provenance + supersession" | [FND §executive-summary] |
| P04 | S | "Second, it must support durable long-term memory for an AI agent, including capture, scope, consolidation, retrieval, context projection, and anti-feedback provenance." | [FND §1] |
| P05 | S | "Shared core: opaque stable identity, semantic versioning, provenance/lineage, typed scope, canonical durable history, artifacts, derived indexes, purpose-specific projections, …" | [FND §G.1] |
| P06 | A | "A shared term must not smuggle one profile's semantics into the other. Namespacing is preferred over artificially universal entities." | [FND §G.1] |
| P07 | S | "Memory Core / Identity / Version / Provenance / Lineage / MemoryScope / CanonicalHistory<T profile record> …" (core architecture diagram) | [FND §G.2] |
| P08 | S | "MemoryScope is promoted as a shared-core concept because both profiles require explicit applicability and isolation boundaries. The core owns the shape and composition rules; each profile owns its scope vocabulary. Agent-memory scope is correctness- and privacy-relevant, not a cosmetic tag." | [FND §G.3] |
| P09 | S | "\| Profile \| Illustrative scope facets \| … \| Learning \| learner, course/domain, collection/curriculum, context family \| \| Agent \| principal/user, agent, workspace/project, conversation, session, task \|" | [FND §G.3] |
| P10 | S | "It defines durable semantics for capturing what happened, deriving candidate memories, consolidating them with provenance, retrieving under scope and budget, and projecting selected memory into an agent request." | [FND §G.4] |
| P11 | S | "AgentMemoryObservation preserves source identity (session/turn/tool/message references where available), occurred/recorded time, producer, scope, and information-origin context." | [FND §G.4] |
| P12 | S | "MemoryRecord is a derived durable memory artifact with stable identity, provenance, scope, lineage, and supersession/consolidation history; it is not canonical conversation history." | [FND §G.4] |
| P13 | S | "Retrieval uses identity and structured scope first; lexical/semantic retrieval discovers candidates but does not define identity or truth." | [FND §G.4] |
| P14 | S | "AgentMemoryObservation -> MemoryRecord/indexes … \| retrieve(scope, query, budget) … AgentContextProjection" (diagram) | [FND §G.5] |
| P15 | H | "Current Minion-Agent already exposes clean seams: … an open session-event namespace, and a scoped runtime service/plugin system." | [FND §G.5] |
| P16 | A | "Conversation/session history is authoritative execution history; long-term memory is a selected/interpreted layer derived from observations." | [FND §G.5] |
| P17 | A | "New code and normalized specifications should prefer `LearnerMemoryModel` or the namespaced form `learning.MemoryModel`." | [FND §G.6] |
| P18 | S | "\| MemoryScope exists in core; profile vocabularies remain profile-owned \| FROZEN boundary / PROVISIONAL vocabulary \|" | [FND §G.7] |
| P19 | S | "The strongest core is the intersection of stable engineering semantics - identity, provenance, history, scope, projection, retrieval, replay, durability and compatibility - with profile-specific meaning remaining at the edges." | [FND §v2-3-closing-position] |
| P20 | A | "Retrieval/context-conditioned state is conceptually necessary, but exact identity and storage remain model-specific." … "KnowledgeComponent + cue/context family + response/performance mode v context-conditioned accessibility estimate" | [FND §9.1] |
| P21 | A | "Collection hierarchy is organizational, not learner-memory truth." | [FND §18] |
| P22 | A | "FROZEN — Data durability is constrained by privacy and minimization: research value does not justify retaining unnecessary sensitive raw data indefinitely." | [FND §17] |
| P23 | A | "Deliberately not frozen … A single global learner summary/profile." | [FND §deliberately-not-frozen] |

### 1.2 MVP Contract v1.2 (MVP)

| # | Tag | Quote | Cite |
|---|---|---|---|
| P24 | S | "Primary proving use case B: AI-agent long-term memory through Minion-Agent, including capture, scope, consolidation, retrieval, context projection, and anti-feedback provenance." | [MVP §2] |
| P25 | S | "MemoryScope as a shared applicability/isolation mechanism, with profile-specific scope facets." | [MVP §18.1] |
| P26 | S | "Durable AgentMemoryObservation capture with source references, scope, provenance, and information-origin/context-fencing metadata." | [MVP §18.3] |
| P27 | S | "Scope-aware retrieval and ranking under an explicit context/projection budget." | [MVP §18.3] |
| P28 | A | "Retrieval infrastructure that keeps deterministic identity/structured lookup authoritative and treats lexical/semantic retrieval as discovery." | [MVP §18.1] |
| P29 | A | "The Python and Rust implementations consume the same shared core/profile contracts and canonical conformance. Neither language is semantic authority for the other." | [MVP §18.5] |
| P30 | A | "Free-text/work/professional content must remain local by default unless the user explicitly exports or enables an external evaluator." | [MVP §9] |
| P31 | A | "\| Context-conditioned learner models \| No route/context-specific state required beyond data needed for future analysis. \|" | [MVP §10] |
| P32 | H | "Absence only carries retirement/membership semantics within explicitly authoritative scope." | [MVP §8] |

### 1.3 Requirement 00 (R00)

| # | Tag | Quote | Cite |
|---|---|---|---|
| P33 | S | "Shared-core concepts (identity, provenance, scope, canonical history, projection, retrieval, replay, persistence) must remain compatible with Requirement 05 without forcing learner-specific entities into the shared core." | [R00 §1] |
| P34 | S | "Shared MemoryScope may be used by the Learning Profile, but its learning scope facets are profile-owned and must not define agent scope vocabulary." | [R00 §21] |
| P35 | A | "Implementation namespaces SHOULD make this explicit (`learning.*` or equivalently named types)." | [R00 §21] |
| P36 | A | "Any shared persistence/retrieval primitive must preserve the richer provenance needed by both profiles rather than degrading one to fit the other." | [R00 §21] |
| P37 | A | "Collection is organization/navigation metadata, not knowledge identity or learner mastery. - Collection has stable ID/version, optional key, name, optional parent_id, order, and provenance where relevant." | [R00 §4.5] |
| P38 | A | "Dynamic learner views such as Due Today or Weak are filters, not Knowledge Collections." | [R00 §4.5] |
| P39 | H | "\| Absent inside explicit authoritative scope \| Membership removal / retirement candidate; never blind hard delete \|" | [R00 §12] |

### 1.4 Requirement 01 (R01)

| # | Tag | Quote | Cite |
|---|---|---|---|
| P40 | A | "Collections are lightweight organization/navigation metadata, many-to-many with KnowledgeUnits, with stable IDs and optional single-parent hierarchy for MVP." | [R01 §7] |
| P41 | A | "Controlled exact semantic keys may support deterministic checks inside a namespace, but lexical/semantic similarity can only produce duplicate candidates/warnings." | [R01 §13] |
| P42 | S | "Shared retrieval infrastructure may index Knowledge and Agent Memory, but namespaces/scopes and stable identities remain distinct." | [R01 §21] |
| P43 | H | "manifest owns package semantics, scope, producer/provenance, entry integrity, schema version, authoritative flag, …" | [R01 §3] |
| P44 | H | "Authoritative absence has meaning only inside declared scope and normally removes membership/candidate-retires rather than hard-deleting an entity with history." | [R01 §10] |
| P45 | H | "authoritative scope does not delete unrelated entities" | [R01 §19] |

### 1.5 Requirement 02 (R02)

| # | Tag | Quote | Cite |
|---|---|---|---|
| P46 | A | "`MemoryModel` in this requirement is learner-specific and SHOULD be exposed as `LearnerMemoryModel` or namespaced `learning.MemoryModel`." | [R02 §17] |
| P47 | A | "Shared retrieval/index infrastructure may be reused, but semantic search never substitutes for structured learner state or stable Knowledge identity." | [R02 §17] |

### 1.6 Requirement 03 (R03)

| # | Tag | Quote | Cite |
|---|---|---|---|
| P48 | A | "Backup and export must preserve user control over learner history. - External analytics/export adapters are future work and must not silently transmit private learning history." | [R03 §18] |
| P49 | A | "If shared storage is used, profile/type boundaries must remain explicit in serialization and replay." | [R03 §28] |

### 1.7 Requirement 04 (R04)

| # | Tag | Quote | Cite |
|---|---|---|---|
| P50 | S | "reserving shared-core primitives (identity, provenance, scope, replay boundaries, projections, indexes, backup compatibility) that Requirement 05 can reuse without sharing learner-specific tables or semantics." | [R04 §1] |
| P51 | S | "MemoryScope and HistoryBoundary are shared concepts; profile-specific scope facets and event payloads remain namespaced." | [R04 §41.1] |
| P52 | A | "Stable IDs/version/provenance/lineage and integrity metadata may share physical persistence libraries or schemas only when profile/type identity remains explicit." | [R04 §41.1] |
| P53 | A | "Portable backup must record profile/type/schema identity so a restore never interprets Agent Memory records as LearningEvents or vice versa." | [R04 §41.1] |
| P54 | S | "Scope isolation tests prove that a memory outside the allowed principal/agent/project/conversation scope cannot be returned merely because semantic similarity is high." | [R04 §42] |
| P55 | A | "Restoring a mixed-profile backup preserves profile/type identity and never cross-decodes records." | [R04 §42] |
| P56 | A | "Offline-first local persistence is the default; no learner history requires a backend for core operation." | [R04 §20] |
| P57 | A | "Logs/debug exports must not unintentionally include full raw responses or private Knowledge content unless explicitly requested." | [R04 §20] |
| P58 | H | "KnowledgePackageRecord — imported package identity, package/schema versions, producer/provenance, authoritative scope and import metadata." | [R04 §4] |
| P59 | H | "Authoritative absence has meaning only inside the package’s declared authoritative scope. - Missing entities outside an authoritative scope are unchanged." | [R04 §14] |

### 1.8 Requirement 05 (R05) — Agent profile authority

| # | Tag | Quote | Cite |
|---|---|---|---|
| P60 | S | "The profile covers durable long-term memory capture, scope, derivation/consolidation, retrieval, context projection, provenance, feedback-loop prevention, and adapter boundaries." | [R05 §1] |
| P61 | S | "Minion-Memory Agent Memory Profile … retrieve under scope + budget" (diagram) | [R05 §4] |
| P62 | S | "\| scope \| MemoryScope facets applicable to this observation \|" (AgentMemoryObservation field family) | [R05 §5.1] |
| P63 | S | "Scope is a correctness/privacy boundary, not a ranking hint. The MVP must support an extensible structured scope sufficient to express principal/user, agent identity, workspace/project, conversation, session, and task applicability. Retrieval must enforce scope before semantic ranking can admit a candidate." | [R05 §5.3] |
| P64 | S | "RetrievalQuery carries purpose, allowed scope, structured filters, query text/embedding input where used, and a projection budget." | [R05 §5.5] |
| P65 | S | "It records projection policy/version, selected record IDs/versions, scope, budget/cost, and a stable projection identity/content reference when needed for request reconstruction." (AgentContextProjection) | [R05 §5.6] |
| P66 | S | "Agent adapter capture ↓ durable source reference + origin/scope AgentMemoryObservation" (diagram) | [R05 §6] |
| P67 | S | "Authority order: stable identity / explicit record reference first; structured scope/filter next; lexical/semantic search for discovery." | [R05 §8] |
| P68 | S | "Hard scope/privacy constraints apply before ranking and cannot be overridden by similarity." | [R05 §8] |
| P69 | S | "\| Pre-request \| Build RetrievalQuery from agent/user/workspace/conversation/task context; retrieve and project memory within budget. \|" | [R05 §10] |
| P70 | A | "\| Failure \| Fail open for optional memory recall/enrichment; never corrupt or rewrite Minion-Agent session history. \|" | [R05 §10] |
| P71 | S | "the integration must preserve enough information to explain/reconstruct the memory projection that was dispatched: projection identity or content reference, selected MemoryRecord IDs/versions, policy/version, scope, and relevant budget." | [R05 §11] |
| P72 | A | "These correspondences are architectural analogies only. They are not type aliases and do not authorize one profile to interpret the other’s data." | [R05 §13] |
| P73 | A | "Unknown required record/event schema fails safely rather than silently omitting semantics." | [R05 §14] |
| P74 | A | "Minion-Agent remains functional if Minion-Memory is unavailable; memory degradation is observable but not fatal unless the application explicitly configures memory as mandatory." | [R05 §14] |
| P75 | S | "Agent memory may contain user, project, tool, workplace, or other sensitive context. Scope enforcement, retention, deletion/retirement semantics, raw-content minimization, and auditability are therefore first-class. Telemetry must prefer bounded metadata over content. A projection may omit private records even when semantically relevant." | [R05 §15] |
| P76 | S | "A Minion-Agent adapter can inject a scoped/budgeted memory projection through the existing request/prompt seam and identify the exact records used." | [R05 §16] |
| P77 | S | "Scope isolation blocks an out-of-scope semantically similar memory." | [R05 §16] |
| P78 | A | "Exact/structured lookup continues to work with semantic indexing disabled." | [R05 §16] |
| P79 | A | "Deferred / Provisional … Cross-agent automatic memory sharing policy. … Global personal profile synthesis." | [R05 §17] |
| P80 | S | "Scope is enforced before ranking." (Final invariant) | [R05 §18] |

### 1.9 Implementation Architecture Amendments v1.3 (IAA)

| # | Tag | Quote | Cite |
|---|---|---|---|
| P81 | A | "Hermes Agent memory providers: Multiple memory philosophies; provider lifecycle; non-blocking optional capture; context fencing; hierarchical resolution; hybrid retrieval; provenance/trust." (traceability only) | [IAA §8] |
| P82 | A | "RESEARCH CANDIDATE: richer information-origin inference, learned evidence mapping, cross-context retrieval-state models." | [IAA §9] |
| P83 | A | "Learner-specific concepts remain in the Learning Profile; agent capture/consolidation/context concepts remain in the Agent Memory Profile. Prefer explicit namespaces over a universal `Memory` entity." | [IAA §A27] |
| P84 | S | "Promote scope/applicability/isolation to the shared core. Agent scope must support at least principal/user, agent, workspace/project, conversation, session, and task dimensions or an extensible equivalent." | [IAA §A28] |
| P85 | H | "scoped runtime services/plugins" (Minion-Agent seam) | [IAA §12] |
| P86 | S | "Vector similarity never bypasses scope/isolation or establishes stable identity." | [IAA §13] |

### 1.10 Bootstrap prompt v1.1 (BOOT) and Update Summary (SUMMARY) — process/summary, not in the semantic authority order

| # | Tag | Quote | Cite |
|---|---|---|---|
| P87 | S | "`SCOPE-###` MemoryScope/isolation" | [BOOT §contract-model] |
| P88 | S | "Expected shared-core candidates: … - MemoryScope" | [BOOT §core-admission-rule] |
| P89 | S | "Pre-request retrieval is scope-aware and budgeted." | [BOOT §minion-agent-integration-invariants] |
| P90 | S | "1. core identity/version/provenance/lineage + MemoryScope" | [BOOT §proposed-dependency-aware-layers-validate-do-not-blindly-implement] |
| P91 | S | "identify cross-language hazards (Unicode, numeric domains, timestamps/order, SQLite transaction behavior, JSON/YAML, hashes, paths, operation IDs, scope encoding, …)" | [BOOT §first-work-package-wp-00-only] |
| P92 | S | "Shared core is limited to cross-profile semantics such as identity/version/provenance/lineage, MemoryScope, canonical history, …" | [SUMMARY §core-architecture-change] |
| P93 | S | "Integration uses an adapter: pre-request scoped retrieval -> AgentContextProjection -> Minion-Agent prompt/header memory component" | [SUMMARY §minion-agent-boundary] |

Note: the IAA preamble banner "Scope: These amendments refine implementation guardrails …" is a
document-scope homonym with no index anchor; excluded.

**Count:** 93 registered passages — 49 MemoryScope-proper [S], 35 adjacent [A], 9 homonym [H]
(the package-reconciliation "authoritative scope" and Minion-Agent "scoped runtime services").
No source mentions: tenant, cross-scope, leak (other than FND §15.1 "avoid leakage from future
learner data", an evaluation-protocol sense), containment/inheritance of scope, scope equality,
"visibility" of memories, default scope, or a scope wildcard.

---

## Part 2 — Characterization by open question

Legend: **A** = path A (authority reading: sources decide, transcribe). **C** = path C (sources
silent or ambiguous where conforming implementations would differ observably → Owner decision on
an options packet). **A+C** = partially decided.

### Q1 — Scope identity and equality — **C** (frame decided: A)

Decided (path A):
- MemoryScope is a *typed*, *structured*, *extensible* value, not a tag: "typed scope" [FND §G.1]
  (P05; also P02), "an extensible structured scope" [R05 §5.3] (P63), "not a cosmetic tag" [FND §G.3]
  (P08), "not a ranking hint" [R05 §5.3].
- It is composed of *facets* / *dimensions*: "Illustrative scope facets" [FND §G.3] (P09);
  "dimensions or an extensible equivalent" [IAA §A28] (P84).
- The *shape* is core-owned and single: "The core owns the shape and composition rules" [FND §G.3].
  ⇒ one core equality rule for both profiles; a profile may not redefine equality.
- Facets are profile-namespaced in persistence [R04 §41.1] (P51) ⇒ a learning facet and an agent
  facet with the same local name are different facets.

Open (path C): what value represents a scope; when two scopes are equal; whether facet *values*
are opaque stable IDs (CORE-001 domain), arbitrary strings, or typed values; whether an
empty/absent facet equals an explicitly "unset" facet; ordering/canonical form.

Candidate options:
1. **Canonical facet map** — scope = map {namespaced facet name → value}; equality = equality of
   canonical maps (absent ≠ present). Observable: two scopes differing only by key order are equal;
   a scope with an extra facet is different. Straightforward cross-language encoding.
2. **Fixed core slots + extension map** — typed slots for the profile's declared facets plus an
   `extensions` map. Observable: unknown extensions compare by value; adding a declared facet is a
   schema change.
3. **Scope as an identified entity** — scope has its own opaque ID; records reference it; equality =
   ID equality. Observable: two structurally identical scopes created separately are *different*
   unless deduplicated; enables hierarchy by reference (see Q2).
4. **Set of (namespace, facet, value) triples** — allows multi-valued facets (e.g. a record
   applicable to two projects). Observable: a record can be in-scope for several values of one facet.

Lean: "typed"/"structured"/"namespaced" rule out an opaque free-text tag; nothing chooses among 1, 2
or 4. Option 3 sits awkwardly with "structured scope" being directly expressible [R05 §5.3] but is
not excluded. Facet values probably fall under the SER-008 portable value domain (G-015..017);
whether they must be CORE-001 stable-ID tokens is open.

### Q2 — Containment / hierarchy between facets — **C**

Decided: nothing. No source states any containment relation (user ⊃ project ⊃ conversation ⊃
session ⊃ task, or learner ⊃ course ⊃ collection). The agent facets are called "dimensions"
[IAA §A28] (P84) and listed flat [FND §G.3] (P09).

Adjacent facts that a decision must respect:
- In the learning profile, *Collections* have "optional single-parent hierarchy for MVP" [R01 §7]
  (P40) / "optional parent_id" [R00 §4.5] (P37), but "Collection hierarchy is organizational, not
  learner-memory truth" [FND §18] (P21). So if the `collection/curriculum` facet reuses Collection
  IDs, the source does not say whether the facet inherits the Collection parent tree.
- The only "hierarchical" agent-memory mention is reviewed-implementation traceability: Hermes
  "hierarchical resolution" [IAA §8] (P81). IAA §9's ADOPT NOW list does not include it. Not normative.
- Minion-Agent sessions belong to conversations in the integration target, but Minion-Agent "is a
  primary proving consumer, not semantic authority" [FND §G.5].

Candidate options:
1. **Flat, independent facets** (no containment). Observable: a record scoped `{user:U, project:P}`
   and a query `{user:U, project:P, conversation:C}` relate only by the Q3/Q4 matching rule;
   no implicit parent lookup.
2. **Declared static partial order in the profile vocabulary** (e.g. agent: principal ⊃ workspace ⊃
   conversation ⊃ session ⊃ task; agent identity orthogonal). Observable: a narrower facet implies
   its ancestors; a query can be resolved upward.
3. **Data-driven containment** (scope values carry parent links, e.g. session→conversation).
   Observable: containment depends on stored relationships; requires a resolution step and
   consistency rules.
4. **Flat in core, hierarchy as profile policy** — core compares facets flat; the agent profile's
   retrieval policy may widen a query along a declared order.

Lean: "dimensions … or an extensible equivalent" and the absence of any hierarchy language lean
toward option 1 or 4 in the core. Nothing excludes 2/3 for a profile vocabulary.

### Q3 — Inheritance / visibility across facets — **C**

Decided (path A):
- A memory outside the *allowed* scope must not be returned because of similarity [R04 §42] (P54),
  [R05 §16] (P77), [IAA §13] (P86).
- The query, not the record, carries the *allowed scope*: "RetrievalQuery carries purpose, allowed
  scope, …" [R05 §5.5] (P64).
- A record's/observation's scope expresses the facets *applicable* to it: "MemoryScope facets
  applicable to this observation" [R05 §5.1] (P62); "applicability and isolation boundaries"
  [FND §G.3].
- A projection may hide private records even if in-scope and relevant [R05 §15] (P75).

Open (path C): whether a user/principal-level record is visible in a session of that user; whether
a project-level record is visible in a conversation of that project; whether one agent sees another
agent's memories for the same principal. The sources do not define the matching relation between
the allowed scope and a record scope.

Explicitly deferred related policy: "Cross-agent automatic memory sharing policy" and "Global
personal profile synthesis" [R05 §17] (P79). This means the Owner decision for the `agent` facet
must not create *automatic* cross-agent sharing as an MVP semantic (that is deferred), though it
does not by itself fix the default.

Candidate options:
1. **Exact match only** — a record is visible iff its scope equals the allowed scope. Observable:
   a user-level preference is invisible in every session unless captured with that session's full
   scope; very isolating, poor recall.
2. **Applicability (broader-is-visible)** — a record facet that is *absent* means "applies to all
   values"; a record is visible iff every facet the record specifies matches the query. Observable:
   `{principal:U}` record is visible in `{principal:U, conversation:C, session:S}`; a
   `{principal:U, project:P}` record is invisible in project Q. Matches the word "applicable".
3. **Explicit allowed-set** — the query's allowed scope is an explicit set/union of scopes the
   adapter enumerates (e.g. this session, this conversation, this user's global); visible iff the
   record scope is a member (or matches one member under rule 1/2). Observable: visibility is
   entirely adapter-controlled and auditable through the recorded projection scope [R05 §11].
4. **Hierarchy inheritance** — visibility follows a Q2 containment order upward only (narrow
   context sees broader records, never sibling/narrower). Depends on Q2 option 2/3.

Lean: the word "applicable" [R05 §5.1] and the requirement to express "applicability" [R05 §5.3]
favor option 2 or 3 over 1; the privacy-boundary framing [R05 §15] favors whichever is
fail-closed on unknowns. No source picks one.

### Q4 — Combination of facets in a query; missing facets — **C** (ownership decided: A)

Decided (path A):
- Composition rules are core-owned, single for both profiles: "The core owns the shape and
  composition rules" [FND §G.3] (P08). So intersection/combination is a core rule, not per profile.
- The adapter builds the query from context: "Build RetrievalQuery from agent/user/workspace/
  conversation/task context" [R05 §10] (P69). (Note: `session` and `principal` vs `user` naming
  differ from [R05 §5.3]; see Q10.)
- Scope is combined with other structured filters, and ahead of discovery [R05 §8] (P67).

Open (path C): conjunction vs. disjunction of facets; multi-valued facets; what a query with a
missing facet means; what a *record* with a missing facet means (overlaps Q3).

Candidate options for a missing query facet:
1. **Wildcard** — missing facet matches any value. Observable: a query without `conversation`
   retrieves memories from all of that user's conversations (wide; privacy risk).
2. **Unscoped-only** — missing facet matches only records that also lack that facet. Observable:
   such a query sees only "global for that facet" records.
3. **Reject** — a query must specify every facet the profile declares mandatory, else error.
   Observable: malformed adapter queries fail visibly.
4. **Profile-declared requiredness** — each facet is declared required/optional by the profile;
   required missing ⇒ reject, optional missing ⇒ option 2.

Lean: scope as a privacy boundary [R05 §5.3][R05 §15] leans away from option 1 (fail-open
widening). Nothing decides between 2, 3 and 4.

### Q5 — Enforcement point and failure mode — **A** (point) + **C** (failure mode, ID-lookup)

Decided (path A):
- Point: before semantic ranking can admit a candidate [R05 §5.3] (P63); "Hard scope/privacy
  constraints apply before ranking and cannot be overridden by similarity" [R05 §8] (P68);
  "Scope is enforced before ranking" [R05 §18] (P80); "Vector similarity never bypasses
  scope/isolation" [IAA §13] (P86).
- Ranking itself is scope-aware: "Scope-aware retrieval and ranking" [MVP §18.3] (P27).
- Observable acceptance: out-of-scope semantically similar memory "cannot be returned"
  [R04 §42] (P54), "Scope isolation blocks …" [R05 §16] (P77).
- Scope is recorded on the projection and in request reconstruction [R05 §5.6] (P65),
  [R05 §11] (P71), so enforcement outcome is auditable.
- Optional recall fails open at the adapter [R05 §10] (P70); memory unavailability is
  "observable but not fatal" [R05 §14] (P74). (This is about *availability*, not scope violation.)

Open (path C):
- **Violation result:** a candidate that is out of scope — silently filtered (empty/shorter
  result) vs. error vs. filtered with an observable audit count.
- **Exact-ID / explicit-reference lookup:** the authority order puts "stable identity / explicit
  record reference first; structured scope/filter next" [R05 §8] (P67). The sources do not say
  whether a direct ID lookup of an out-of-scope record is refused. "Hard scope/privacy constraints
  apply before ranking" covers ranked retrieval; ID lookup is not ranked.
- **Write-side enforcement:** whether capture/consolidation validates scope (e.g. consolidation
  merging records of different scopes; superseding across scopes). The sources are silent.
- **Malformed/unknown scope on a stored record:** "Unknown required record/event schema fails
  safely" [R05 §14] (P73) gives a direction but not the observable.

Candidate options (violation result): (1) silent filter — out-of-scope never appears, query
succeeds; (2) silent filter + bounded-metadata audit (count only, per "Telemetry must prefer
bounded metadata over content" [R05 §15]); (3) error on any attempt to fetch an out-of-scope record
by ID, silent filter for ranked/search retrieval; (4) error always. Lean: P75 ("may omit private
records") and P70 (fail open for recall) lean toward (1)/(2) for search; (3) is the natural
privacy reading for ID lookup but is not stated.

Candidate options (consolidation across scopes): (a) forbidden — consolidation inputs must share
one scope; (b) allowed, result scope = intersection/narrowest; (c) allowed, result scope = explicit
policy output recorded with lineage. Sources silent.

### Q6 — Privacy defaults — **C** (principles decided: A)

Decided (path A):
- Scope is a privacy boundary and scope enforcement is first-class [R05 §5.3] (P63), [R05 §15] (P75).
- Scope is attached at capture, at the durability barrier: "durable source reference +
  origin/scope" [R05 §6] (P66); every observation and record carries scope [FND §G.4] (P11, P12).
- Projections may omit private records [R05 §15].
- Locality defaults: content "must remain local by default" [MVP §9] (P30); "Offline-first local
  persistence is the default" [R04 §20] (P56); no silent transmission [R03 §18] (P48).

Open (path C): the default scope assigned when the adapter omits facets; default visibility of a
new record; whether "private" is a facet/flag distinct from scope (P75 uses "private records"
without defining it); least-privilege is not stated as a rule.

Candidate options:
1. **No default — scope required at capture** (missing ⇒ capture rejected). Observable: adapter bugs
   fail loudly; conflicts with fail-open capture if rejection loses the source reference.
2. **Narrowest available context** (default = all facets known at capture time, e.g. down to
   session/task). Observable: least privilege; recall across sessions requires later widening by
   consolidation/policy.
3. **Principal-level default** (default = principal/user + agent). Observable: memories follow the
   user across conversations by default; wider exposure.
4. **Quarantine** — unscoped records are stored but never retrievable until scoped. Observable:
   durability preserved, zero visibility.

Lean: privacy-first framing leans to 2 or 4 (least privilege); the capture-first durability rule
[R05 §6][R04 §41.3] leans against outright rejection (1) if rejection would drop the source
reference. Not decided.

### Q7 — Profile vocabulary and namespacing — **A** (mostly) + **C** (mechanics)

Decided (path A):
- Core owns shape/composition; each profile owns its vocabulary [FND §G.3] (P08).
- Boundary FROZEN; vocabulary PROVISIONAL [FND §G.7] (P18).
- "learning scope facets are profile-owned and must not define agent scope vocabulary" [R00 §21] (P34).
- "profile-specific scope facets and event payloads remain namespaced" [R04 §41.1] (P51).
- "namespaces/scopes and stable identities remain distinct" in shared retrieval infrastructure
  [R01 §21] (P42); namespacing preferred over universal entities [FND §G.1] (P06), [IAA §A27] (P83).
- Agent vocabulary minimum: principal/user, agent, workspace/project, conversation, session, task
  "or an extensible equivalent" [IAA §A28] (P84), [R05 §5.3] (P63) — extensibility is required.
- Learning vocabulary: illustrative only (learner, course/domain, collection/curriculum, context
  family) [FND §G.3] (P09).
- Cross-profile: no profile may interpret the other's data [R05 §13] (P72); backup/restore never
  cross-decodes [R04 §41.1] (P53), [R04 §42] (P55).

Open (path C): namespace syntax (`agent.session` vs nested map vs (profile, facet) pair); whether
the paired names "principal/user", "workspace/project", "course/domain", "collection/curriculum"
are one facet with two names or two facets; who may extend the vocabulary (profile spec only,
consumer/app at runtime, or both); handling of an unknown facet in a stored record or a query.

Candidate options (unknown facet): (1) fail safely — reject/stop like an unknown required schema
[R05 §14] (P73), [IAA §A4]; (2) treat as non-matching (record invisible); (3) ignore (ignorable
facet). Lean: P73 + privacy framing favor (1) or (2); (3) would widen visibility silently.
Candidate options (slash-pairs): (a) one facet, alias names; (b) two distinct facets; (c) one
facet in MVP, split reserved. Not decided.

### Q8 — Learning-profile binding — **C**

Decided (path A):
- Both profiles "require explicit applicability and isolation boundaries" [FND §G.3] (P08).
- But the learning profile's use is permissive: "Shared MemoryScope **may** be used by the Learning
  Profile" [R00 §21] (P34). No learning document (R00–R04) states a learning scope requirement,
  a learning retrieval enforcement rule, or a learning acceptance test for scope isolation.
- Learning "context family" exists as a learner-model concept: "cue/context family" [FND §9.1]
  (P20), PROVISIONAL; context-conditioned state not required in MVP [MVP §10] (P31); cross-context
  retrieval-state models are a RESEARCH CANDIDATE [IAA §9] (P82).
- Enforcement-before-ranking text is agent-located ([R05 §5.3], [R05 §8], [R04 §42] names agent
  facets); [IAA §13] is in the Minion-Agent section.

Open (path C): whether learning retrieval/projection (scheduling selection, diagnostics, knowledge
lookup) must enforce MemoryScope identically; whether the Flashcard MVP needs any scope at all
(single local learner).

Candidate options:
1. **Uniform core enforcement** — any retrieval that receives a MemoryScope enforces it with the core
   rule regardless of profile. Observable: learning conformance gets scope-isolation scenarios.
2. **Opt-in per profile** — core provides the mechanism; Learning Profile adopts it later; MVP
   learning operations are unscoped (single learner). Observable: no learning scope tests now.
3. **Learning uses scope only for learner isolation** (one facet, `learner`), other facets illustrative.
4. **Defer** the learning binding to the Learning layers (07–12) with a reservation.

Lean: "may be used" [R00 §21] leans toward 2/4 for MVP; "core owns composition rules" [FND §G.3]
means that *if* learning uses scope, the core rule (1) applies — not a learning-specific variant.

### Q9 — Persistence / encoding / cross-language representation — **A** (constraints) + **C** (encoding)

Decided (path A):
- Scope is stored on: AgentMemoryObservation [R05 §5.1] (P62); MemoryRecord [FND §G.4] (P12);
  AgentContextProjection [R05 §5.6] (P65); request-reconstruction record [R05 §11] (P71).
- Captured durably at the barrier with the source reference [R05 §6] (P66).
- Profile-specific facets namespaced in persistence [R04 §41.1] (P51); profile/type identity
  explicit in shared storage, serialization, replay and backup [R03 §28] (P49), [R04 §41.1] (P52, P53).
- Python and Rust consume the same contracts; neither is oracle [MVP §18.5] (P29).
- "scope encoding" is a named cross-language hazard [BOOT §first-work-package-wp-00-only] (P91)
  (process input, tracked as H11 in the hazard inventory).
- Backend is not semantic authority [R05 §12].

Open (path C): canonical serialized form (JSON object shape, key ordering, facet-value types,
absent vs null vs empty), indexability requirement (scope must be filterable without semantic
index — implied by [R05 §16] "Exact/structured lookup continues to work with semantic indexing
disabled" (P78) and [R05 §8] structured-first), whether scope is versioned (a scope schema version
separate from record schema version), and whether scope is immutable on a record or can change
(re-scoping) — and if it can, whether that is a new record version.

Candidate options (encoding): (1) canonical JSON object under SER-008 domain, keys
`"<profile>.<facet>"`, sorted; (2) array of `{ns, facet, value}` triples sorted; (3) scope entity
with its own ID + facet rows (relational). Candidate options (mutability): (a) scope immutable per
record version, re-scope = new version with lineage; (b) scope immutable for the record identity,
re-scope = new record + supersession; (c) mutable metadata. Lean: CORE-003 (same ID + version ⇒
same content) + append-only lineage culture lean to (a)/(b); not stated for scope.

### Q10 — Source requirements not yet transcribed in spec/scope.md (possible omissions)

| # | Possible omission | Source | Where it currently lives (if anywhere) |
|---|---|---|---|
| O1 | Scope is **typed** ("typed scope") — scope.md says "structured and extensible" only | [FND §G.1] [FND §executive-summary] | nowhere |
| O2 | Learning use of MemoryScope is **optional** ("may be used by the Learning Profile"); SCOPE-005's note does not state the "may" | [R00 §21] | SCOPE-002 cites R00 §21 for the vocabulary rule only |
| O3 | RetrievalQuery carries an **allowed scope** (the query-side half of enforcement) | [R05 §5.5] | ARET-001; not referenced from scope.md |
| O4 | Scope is a carried field of observations, records, projections and request reconstruction; captured at the durability barrier | [R05 §5.1] [FND §G.4] [R05 §5.6] [R05 §11] [R05 §6] | ACAP-001/002, AMEM-001, ACTX-001/003, MINT-006; no SCOPE-* cross-ref |
| O5 | **Ranking** is also scope-aware ("Scope-aware retrieval and ranking") | [MVP §18.3] | ARET-005 (retrieval only wording) |
| O6 | Shared retrieval infrastructure keeps **namespaces/scopes** distinct across Knowledge and Agent Memory | [R01 §21] | RET-006; scope.md does not cite R01 §21 |
| O7 | Scope-isolation **acceptance criterion** (R05 §16) is not cited by SCOPE-006 (it cites R05 §5.3/§8/§18, R04 §42, IAA §13) | [R05 §16] | ARET-003 cites it |
| O8 | **Deferred:** cross-agent automatic memory sharing policy; global personal profile synthesis — directly bounds Q3 visibility for the `agent` facet | [R05 §17] | not transcribed anywhere in spec (grep: no match) |
| O9 | Projection may omit **private** records even when relevant (a visibility rule beyond scope) | [R05 §15] | PRIV-006, ACTX-005; scope.md cites R05 §15 only for "privacy boundary" |
| O10 | No profile may interpret the other's data; profile/type identity explicit in serialization, replay, backup — the profile boundary is itself an isolation boundary above scope | [R05 §13] [R03 §28] [R04 §41.1] [R04 §42] | ARCH-005, HIST-002, persistence; not linked to SCOPE |
| O11 | Facet-list **inconsistency to record**: R05 §5.3/IAA §A28 list six agent dimensions (principal/user, agent, workspace/project, conversation, session, task); R04 §42 acceptance names four (principal/agent/project/conversation); R05 §10 adapter context names agent/user/workspace/conversation/task (no session, "user" not "principal"). Not a conflict (minimum vs test subset), but the conformance scope of the isolation test should be fixed. | [R05 §5.3] [IAA §A28] [R04 §42] [R05 §10] | SCOPE-004/006 transcribe the texts but do not note the subset |
| O12 | **Homonym hazard**: "authoritative scope" (Knowledge package reconciliation) and Minion-Agent "scoped runtime services" are unrelated to MemoryScope; spec/learning/package.md uses "scope" in the package sense. A one-line disambiguation note in scope.md (or README glossary) would prevent conflation. | [MVP §8] [R00 §12] [R01 §3] [R01 §10] [R01 §19] [R04 §4] [R04 §14] [FND §G.5] [IAA §12] | not disambiguated |
| O13 | ID/explicit-reference lookup precedes scope filter in the authority order; whether hard scope applies to it is not stated (see Q5) — scope.md's SCOPE-006 speaks only of ranking | [R05 §8] | gap, should be listed in NF-018 question set |
| O14 | Learning "context family" facet relates to the PROVISIONAL learner-model "cue/context family" concept; SCOPE-005 could note the link (and that context-conditioned state is not required in MVP) | [FND §9.1] [MVP §10] [IAA §9] | not noted |

Kickoff candidates "knowledge unit/component" as learning facets: confirmed absent from all sources
(SCOPE-005 note is correct).

---

## Part 3 — Summary matrix

| Q | Topic | Disposition | Key authority |
|---|---|---|---|
| Q1 | identity/equality | C (frame A: typed, structured, extensible, faceted, core-owned shape, namespaced) | FND §G.1, §G.3; R05 §5.3; R04 §41.1 |
| Q2 | containment/hierarchy | C (no source; "dimensions" leans flat) | IAA §A28; FND §G.3; FND §18; R01 §7 |
| Q3 | inheritance/visibility | C (deferred cross-agent sharing bounds it) | R05 §5.1, §5.5, §15, §17; R04 §42 |
| Q4 | facet combination/missing facets | C (core owns the rule) | FND §G.3; R05 §10 |
| Q5 | enforcement point / failure | A for point; C for violation result, ID lookup, write-side | R05 §5.3, §8, §16, §18; IAA §13; R04 §42 |
| Q6 | privacy defaults | C (principles A) | R05 §6, §15; MVP §9; R04 §20 |
| Q7 | vocabulary/namespacing | A for ownership/namespacing/extensibility; C for syntax, slash-pairs, unknown facets | FND §G.3, §G.7; R00 §21; R04 §41.1; IAA §A28 |
| Q8 | learning binding | C ("may be used") | R00 §21; FND §G.3 |
| Q9 | persistence/encoding | A for where/that it is stored & profile identity; C for encoding, mutability, versioning | R05 §5.1, §5.6, §6, §11; R04 §41.1; R03 §28; MVP §18.5 |
| Q10 | omissions | 14 items (O1–O14) | see table |
