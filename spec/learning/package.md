# Learning Profile — Knowledge Package import and reconciliation — DRAFT normalization

Conventions: `spec/README.md`. Profile for every requirement: **learning**.

### PKG-001 — Package shape and field ownership
<a id="pkg-001"></a>
- **Profile:** learning · **Source status:** MVP_ONLY · **Sources:** [R01 §3] [R00 §11] [MVP §8] [FND §13.1]

The MVP canonical interchange is `manifest.yaml` + one Markdown file per KnowledgeUnit + `assets/`.
Entity files own KnowledgeUnit semantics; the manifest owns package semantics (scope,
producer/provenance, entry integrity, schema version, authoritative flag and package-level shared
definitions such as Collections). Two authoritative copies of the same field are not maintained.

*Note:* the unit-file directory is `units/*.md` in [R01 §3] but `memories/*.md` (retained for MVP
compatibility) in [R00 §11] and [MVP §8] — unresolved (NF-001).

### PKG-002 — A package is an interchange protocol
<a id="pkg-002"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R00 §11] [MVP §8] [R01 §1]

The Knowledge Package is a versioned interchange protocol for authored learning content, not the
runtime database format and not a generic agent-memory import format.

### PKG-003 — Validate before mutating
<a id="pkg-003"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R01 §9] [R01 §19] [R04 §14]

Import proceeds: structural validation → semantic validation → parse into the normalized domain
model → compute ChangeSet → transactional reconciliation. Invalid IDs/versions, path traversal,
checksum failures, malformed semantic references and unsupported required schema features are
rejected before mutating local state. A package can be validated without mutation.

### PKG-004 — Reconciliation by stable ID
<a id="pkg-004"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R00 §12] [R01 §10] [MVP §8] [R04 §7]

Matching is strictly by stable ID, never blind file overwrite. Outcomes: local ID absent → Added;
same ID with higher incoming version → Updated after validation; same ID, same version, same hash
→ Unchanged; same ID, same version, different content → Conflict (never silently overwritten);
lower incoming version → ignored/rejected as stale, never overwriting the newer local version.
Reconciliation states include Added, Updated, Unchanged, Missing, Conflict and Retired.

### PKG-005 — Meaning of absence
<a id="pkg-005"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R00 §12] [R01 §10] [R04 §14] [MVP §8]

Absence from a non-authoritative package has no meaning. Absence inside an explicitly declared
authoritative scope means membership removal or retirement candidate only — never blind hard delete
of an entity with history; entities outside that scope are unchanged.

### PKG-006 — Import is transactional
<a id="pkg-006"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R04 §14] [R04 §22] [R01 §17]

Reconciliation runs in one transaction: validate, stage, match, build ChangeSet, check
versions/conflicts/scope, apply Knowledge and membership changes, record the import run; any
failure rolls back. No partial import is visible and a failed import leaves prior Knowledge
unchanged.

### PKG-007 — Import never owns learner history
<a id="pkg-007"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [MVP §8] [MVP §13] [R00 §12] [R01 §1] [R01 §17] [R04 §11] [R04 §14]

Knowledge import/update never deletes, rewrites or resets learner episodes, events, observations,
evidence or their historical interpretability; learner-history storage is outside import's write
scope. Retirement changes only current Knowledge lifecycle/membership.

### PKG-008 — Identical re-import is idempotent
<a id="pkg-008"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R00 §17] [R01 §19] [MVP §13]

Re-importing identical stable knowledge is idempotent and does not reset learner history.

### PKG-009 — Duplicate detection is advisory
<a id="pkg-009"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R01 §13] [IAA §A20] [R04 §36] [MVP §M2]

Stable ID is authoritative. Controlled exact semantic keys may support deterministic checks inside
a namespace; lexical/semantic similarity produces duplicate candidates/warnings only and never
auto-merges distinct Knowledge identities. Rare discriminating differences are a reason to avoid
automatic merge.

### PKG-010 — Import audit records
<a id="pkg-010"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R04 §14] [R04 §4]

Import records retain enough metadata (package identity, versions, producer/provenance, scope,
change summary) to diagnose which package/version produced a Knowledge update.

### PKG-011 — Package compatibility
<a id="pkg-011"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R01 §18]

The package schema version is separate from database, event, backup, model and evaluator/mapper
versions. Unknown required Knowledge semantics fail safely; explicitly ignorable metadata may be
skipped.
