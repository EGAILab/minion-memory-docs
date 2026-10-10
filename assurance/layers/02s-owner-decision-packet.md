# WP-02S — MemoryScope: consolidated Owner-decision packet (NF-018)

**For:** the Owner (G-047: "prepare one consolidated Owner-decision packet").
**Basis:** `assurance/layers/02s-memoryscope-characterization.md`. It quotes 93 passages verbatim;
the quotes behind each recommendation below were spot-checked against the source text.
**Status:** options and recommendations only. No contract text is written until the Owner decides.
Each answer is recorded verbatim as a G-entry.

## Already decided by the sources (path A, transcribed in the contract later)

- MemoryScope is a core, **typed, structured, extensible** value, not a tag and not a ranking hint
  [FND §G.1] [FND §G.3] [R05 §5.3].
- The core owns its shape and composition rules, one rule for both profiles. Each profile owns its
  facet vocabulary, and facets are **namespaced** in persistence [FND §G.3] [R00 §21] [R04 §41.1].
- The agent profile supports at least principal/user, agent, workspace/project, conversation,
  session and task, "or an extensible equivalent" [IAA §A28] [R05 §5.3].
- A retrieval query carries an **allowed scope**, and a record carries the facets **applicable** to
  it [R05 §5.5] [R05 §5.1].
- Scope is enforced **before ranking**: similarity never admits an out-of-scope memory
  [R05 §5.3] [R05 §8] [R04 §42] [IAA §13].
- **Deferred by the sources:** cross-agent automatic memory sharing and global personal profile
  synthesis [R05 §17]. No default may create them.

## Decisions requested

### D1 — Scope value and equality (Q1, Q9)
**Recommended (A).** A scope is a JSON object mapping namespaced facet names (`"<profile>.<facet>"`,
e.g. `"agent.session"`) to single CORE-001 tokens. Equality is map equality: member order is
irrelevant, and an absent facet differs from a present one. The scope is immutable per record
version, so re-scoping creates a new version with lineage.
- **B.** Multi-valued facets, using a set of values per facet. A record can apply to two projects,
  but the matching rules become more complex.
- **C.** Scope as its own entity with an ID, compared by ID. Two structurally identical scopes are
  different unless deduplicated.

### D2 — Hierarchy between facets (Q2)
**Recommended (A).** Flat in the core: facets are independent dimensions with no implied
containment. A profile may later declare a *widening policy* in its own layer, recorded with its
lineage, but the core never infers parents.
- **B.** The core fixes a static order, such as principal ⊃ workspace ⊃ conversation ⊃ session ⊃
  task.
- **C.** Data-driven parent links between scope values.

### D3 — Visibility: matching a record scope against the allowed scope (Q3, Q4)
**Recommended (A), "applicability, fail-closed".**
- A record facet that is absent applies to all values of that facet.
- A record is visible only if every facet it specifies is present in the allowed scope with an
  equal value.
- So `{agent.principal: U}` is visible in `{principal: U, conversation: C, session: S}`, but a
  `{…, project: P}` record is invisible to a query that names project Q or omits the project facet.
  A missing query facet never widens anything.
- **B.** Exact match only: recall across sessions needs re-capture.
- **C.** The adapter enumerates an explicit allowed set of scopes, and visibility is set
  membership.
- **D.** A missing query facet is a wildcard. This widens recall, with a privacy risk.

### D4 — Out-of-scope outcome and direct ID lookup (Q5)
**Recommended (A).**
- Ranked or search retrieval silently filters out-of-scope candidates; at most a bounded,
  content-free count reaches telemetry [R05 §15].
- A scoped lookup by explicit ID treats an out-of-scope record as **absent**, indistinguishable
  from "not found", so its existence never leaks.
- Write-side rules, such as consolidation across scopes, are deferred to Layer 14 under one
  constraint: they never widen scope silently.
- **B.** Search filters, but an out-of-scope ID lookup is an explicit `scope.denied` error, which
  reveals that the record exists.
- **C.** Any scope violation is an error.

### D5 — Scope at capture: default and missing (Q6)
**Recommended (A).** Narrowest available context: a captured record carries every facet the
adapter knows at capture time, which is least privilege. If no facet at all is known, the record
is still captured durably (R05 §6 capture-first) but is **quarantined**: it is never visible until
it is re-scoped as a new version.
- **B.** Scope is mandatory at capture, and capture without it is rejected. This conflicts with
  capture-first durability.
- **C.** The default is principal + agent. Memories follow the user across conversations by
  default, which is wider exposure.

### D6 — Unknown facets and the slash-pair names (Q7)
**Recommended (A).**
- A stored record with a facet the reader doesn't know is **invisible** to that reader
  (fail-closed). A query naming an unknown facet is an error.
- The paired names are each **one facet with one canonical name** in the Minimum Viable Product
  (MVP): `principal` (for principal/user), `workspace` (for workspace/project), and in learning
  `course` and `collection`. Splitting one later is a vocabulary change through a new schema
  version.
- **B.** An unknown facet is ignored. This silently widens visibility.
- **C.** Each slash-pair is two distinct facets.

### D7 — Learning-profile binding (Q8)
**Recommended (A).** Defer to the learning layers (07–12) with a reservation. The core rule is
written now for any profile that uses scope; the Learning Profile adopts it, if at all, in its own
layers ("may be used", [R00 §21]). Until then the Flashcard MVP's learning operations are
unscoped.
- **B.** Uniform now: every learning retrieval enforces scope, so learning gets scope-isolation
  scenarios immediately.
- **C.** Learning uses scope only for learner isolation, with a single `learning.learner` facet.

### D8 — The agent isolation conformance set (O11)
The sources list six agent dimensions, but the R04 §42 isolation test names four:
principal/agent/project/conversation.
**Recommended (A).** Isolation scenarios cover all six dimensions; the four in R04 §42 are a
subset.
- **B.** Only the four named by the acceptance criterion.

## Spec omissions to fix with the contract (path A, no decision needed)

From characterization O1–O14:
- add the word "typed";
- state the learning "may";
- cross-reference the allowed scope (ARET-001), carried scope fields, scope-aware ranking, R01 §21,
  R05 §16 and the R05 §17 deferral;
- note "private records" (PRIV-006);
- link the profile boundary;
- add a disambiguation note that the package-sense "scope" is a different concept.

## Where each decision lands

| Decision | Contract that consumes it |
|---|---|
| D1, D2, D3, D6 | WP-02S core contract (Layer 02) |
| D3, D4, D8 | the RET/ARET retrieval enforcement layers (06, 15) |
| D5 | Agent capture (Layer 13) |
| D7 | Learning layers (07–12) |

All of these work packages declare `blocked_by: WP-02S`, as G-047 requires.
