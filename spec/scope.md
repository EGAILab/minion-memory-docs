# MemoryScope — DRAFT normalization

Conventions: `spec/README.md`.

> **Gap statement.** The sources fix that MemoryScope exists in the core, is structured,
> extensible, profile-vocabularied and enforced before ranking. They do **not** define scope
> identity, containment, inheritance, intersection, retrieval visibility across facets, or a
> cross-language representation. Those are recorded as `REQUIREMENT_UNCERTAIN` (NF-018) and must
> be resolved in Layer 02 by authority reading where the sources decide, and otherwise by Owner
> decision on an options packet (`process/finding-taxonomy.md` §1.1 path C) — not here.

### SCOPE-001 — MemoryScope is a shared-core concept
<a id="scope-001"></a>
- **Profile:** core · **Source status:** FROZEN · **Sources:** [FND §G.3] [FND §G.7] [MVP §18.1] [IAA §A28]

MemoryScope is a shared applicability and isolation mechanism, promoted to the core because both
profiles require explicit applicability and isolation boundaries. The core boundary is FROZEN; the
facet vocabularies are PROVISIONAL.

### SCOPE-002 — Core owns shape and composition; profiles own vocabulary
<a id="scope-002"></a>
- **Profile:** core · **Source status:** FROZEN · **Sources:** [FND §G.7] [FND §G.3] [R00 §21] [R04 §41.1] [MVP §18.1]

The core owns MemoryScope's shape and composition rules; each profile owns its scope facet
vocabulary. Learning scope facets must not define agent scope vocabulary (and vice versa).
Profile-specific facets remain namespaced in persistence.

*Note:* FROZEN applies to the boundary "MemoryScope exists in core; profile vocabularies remain
profile-owned" ([FND §G.7] status row: FROZEN boundary / PROVISIONAL vocabulary). The facet
vocabularies themselves are PROVISIONAL, and the namespacing-in-persistence sentence is normative
but unlabeled ([R04 §41.1]) (WP00-CR-008).

### SCOPE-003 — Scope is a correctness and privacy boundary
<a id="scope-003"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [FND §G.3] [R05 §5.3] [R05 §15]

Scope is structured and extensible; it is a correctness and privacy boundary, not a cosmetic tag
and not a ranking hint.

### SCOPE-004 — Agent scope dimensions
<a id="scope-004"></a>
- **Profile:** agent · **Source status:** NORMATIVE · **Sources:** [R05 §5.3] [IAA §A28] [FND §G.3]

The Agent Memory Profile MVP must support an extensible structured scope sufficient to express
principal/user, agent identity, workspace/project, conversation, session and task applicability (or
an extensible equivalent).

### SCOPE-005 — Learning scope facets (illustrative)
<a id="scope-005"></a>
- **Profile:** learning · **Source status:** PROVISIONAL · **Sources:** [FND §G.3]

Illustrative Learning Profile facets are learner, course/domain, collection/curriculum and context
family. The vocabulary is provisional; no learning-scope requirement beyond illustration is
stated by the sources.

*Note:* the kickoff's investigation list adds knowledge unit/component as candidate facets; the
sources do not, so they are not transcribed (NF-018).

### SCOPE-006 — Scope is enforced before ranking
<a id="scope-006"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [R05 §5.3] [R05 §8] [R05 §18] [R04 §42] [IAA §13]

Retrieval enforces hard scope and privacy constraints before semantic ranking can admit a
candidate; similarity cannot override them. A memory outside the allowed principal/agent/project/
conversation scope cannot be returned merely because its semantic similarity is high.

*Note:* stated for agent retrieval; whether learning retrieval is bound identically is not stated.
