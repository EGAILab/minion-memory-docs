# MemoryScope — DRAFT normalization

Conventions: `spec/README.md`.

> **Gap statement (resolved for Layer 02).** The sources fix that MemoryScope exists in the core,
> is typed, structured, extensible, profile-vocabularied and enforced before ranking. The questions
> they leave open (NF-018) were put to the Owner as one packet and decided as G-056…G-063
> (`reference/governance/2026-10-11-owner-wp02s-memoryscope.md`). The Layer 02 contract is at the end of this file.

> **Homonym.** "Scope" in the Knowledge-package sense ("authoritative scope" of a package
> reconciliation, `spec/learning/package.md`) and Minion-Agent's "scoped runtime services" are
> unrelated to MemoryScope [MVP §8] [R01 §3] [FND §G.5].

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

*Additional sources (transcribed for Layer 02):*
- A retrieval query carries an **allowed scope** [R05 §5.5] (ARET-001), and ranking is scope-aware
  [MVP §18.3].
- Scope isolation is an MVP acceptance criterion [R05 §16].
- Shared retrieval infrastructure keeps namespaces and scopes distinct [R01 §21].
- A projection may omit private records even when in scope and relevant [R05 §15] (PRIV-006).
- Scope is carried by observations, records, projections and request reconstruction, and is
  captured at the durability barrier [R05 §5.1] [FND §G.4] [R05 §5.6] [R05 §11] [R05 §6].
- The profile boundary sits above scope: no profile interprets the other's records [R05 §13]
  (SER-006).
- **Deferred by the sources:** cross-agent automatic memory sharing and global personal profile
  synthesis [R05 §17]. No scope rule may create them.

---

## Layer 02 MemoryScope contract (WP-02S)

The Owner decided this contract as G-056…G-064 (`reference/governance/2026-10-11-owner-wp02s-memoryscope.md`). Only the representation choices below are
made by the contract author, under path B, and they are flagged where they occur.

### Scope value (G-056, G-057)

A **scope** is exactly one of two closed records:

```text
{"scope_state": "resolved",   "facets": {"<profile>.<facet>": "<token>", ...}}
{"scope_state": "unresolved"}
```

- **Facet names (G-064).** A facet name is exactly two non-empty lowercase ASCII segments joined by
  one literal `.`. Each segment is 1–128 bytes, starts with `a`–`z` or `0`–`9`, and otherwise contains
  only `a`–`z`, `0`–`9`, `_` and `-`.
  - Additional dots, Unicode, uppercase or a malformed segment give `scope.invalid`.
  - Windows device names are **not** excluded, because facet names are not paths. So `agent.con` is a
    well-formed facet name, unknown and hidden under G-061, while `agent.session.x` is invalid.
  - The dotted spelling is lexical only, and the core infers no hierarchy from it (G-057).
  - The two-state scope envelope itself is a representation choice (path B).
- **Facet values.** Each value is one CORE-001 portable token; multi-valued facets do not exist.
- **Global.** The empty resolved map `{}` is explicitly global scope.
- **Unresolved.** `unresolved` means the scope is unknown (G-060). It is never empty, global or
  partially widened, and it is hidden from ordinary reads (G-058).
- **Equality.** Scope equality is exact equality of the records: member order is irrelevant, and an
  absent facet differs from a present one. Two unresolved scopes are equal as values; equality says
  nothing about visibility.
- **Part of the record.** A scope belongs to its record's immutable canonical content. Changing it
  takes a new artifact revision (CORE-003) or an explicit, append-only superseding interpretation
  with lineage (HIST-007).
- **No hierarchy (G-057).** Facets are flat and independent: the core infers no parent,
  containment, inheritance or widening. A profile may later define an explicit, versioned widening
  policy that turns source context into an effective query scope *before* core matching. Such a
  policy never changes stored scopes.

### Vocabulary (G-061, G-062)

- **Facet registry.** The core holds the reviewed facet vocabularies of the profiles that have
  adopted scope. The only vocabulary in Layer 02 is the **Agent registry**: `agent.principal`,
  `agent.agent`, `agent.workspace`, `agent.conversation`, `agent.session` and `agent.task`.
- **Source terms.** The integration adapter maps "user" to `principal` and "project" to
  `workspace`. Aliases never enter the core.
- **Unknown facets.** A facet name that is well formed but absent from the registry is unknown,
  including every `learning.*` name.
  - A capture API rejects unknown facets; that rule is consumed by Layer 13.
  - A stored or imported record that carries one stays preserved, with no constraint dropped, but
    is invisible to ordinary reads.
  - A query that names one is rejected.
- **Changing the vocabulary.** Any addition, rename, alias or split is a versioned vocabulary
  change.
- **Learning Profile (G-062).** Learning does not participate in scope semantics yet: its records
  carry neither a resolved nor an unresolved scope, and learning retrieval never calls the matcher.
  Learning adoption requires its own versioned profile contract in Layers 07–12. A multi-learner or
  shared-store feature triggers that contract before it ships.

### Matching (G-058, G-059)

`scope_visible(record, query)` takes `record`, a scope, and `query`, the allowed scope: a resolved
facet map, given as the bare map `{"<profile>.<facet>": "<token>"}`. It returns `true` or `false`.
- **Visible.** A resolved record is visible exactly when every facet it declares appears in `query`
  with the same value.
  - Facets the record omits are unconstrained.
  - Facets the query omits never widen visibility.
  - Extra facets in the query are allowed.
  - So an empty record scope (global) is visible to every query, and an empty query sees only
    global records.
- **Hidden.** An `unresolved` record is never visible (`false`), and neither is a record with any
  unknown facet.
- **Not visible means absent.** Callers treat a record that is not visible as absent. Search,
  ranking, projection, counts and diagnostics behave as if it did not exist. A scoped lookup by ID
  returns the same `not_found` as a missing ID, with no denial or existence signal and no
  hidden-record count in public responses. That retrieval behaviour is consumed in Layers 06 and 15
  (RET, ARET).
- **Audit.** Privileged audit tooling is a separate authorized interface. Internal telemetry is
  limited to bounded, content-free aggregates.
- **Consolidation.** Cross-scope consolidation is deferred to Layer 14 and must never widen
  visibility silently.

`scopes_equal(a, b)` returns structural equality (G-056). Its arguments are validated in declared
order, `a` then `b`.

`validate_scope(scope)` validates one scope value and returns it normalized: exact SER-008 values,
with facet names and values unchanged. A well-formed but unknown facet name is preserved and never
dropped (G-061). The value rules are those of "Scope value" above. It takes one argument, so like
every single-argument primitive (Layer 01 convention) its errors name no argument.

### Errors (stage 3, SER-008 G-031)

- **Generic stages first.** The generic stages run across all arguments first, in declared order.
- **`scope.invalid`.** For a `scope`, `record`, `a` or `b` argument that is a non-object, has a missing or
  other member, has a `scope_state` other than `resolved` or `unresolved`, a malformed facet name,
  or a facet value outside the token domain.
- **`scope.query_invalid` (G-061).** For a `query` that is not a facet map of well-formed names and
  token values, or that names an **unknown** facet. A query has no unresolved form.
- **Order and naming.** Argument errors are checked in declared order: `record` then `query` for
  `scope_visible`, `a` then `b` for `scopes_equal`. The multi-argument primitives name the failing
  argument; `validate_scope` names none.
- **Stage table.** Both codes are stage-3 rows of the SER-008 stage table.

### Conformance (G-063)

Agent isolation scenarios cover all six dimensions. Each has match, mismatch, record-omission and
query-omission evidence, plus composed cases showing that a mismatch in any one declared facet
hides the record. R04 §42's four dimensions are a required subset; its "project" is `workspace`.

