# Learning Profile — legacy Flashcard migration — DRAFT normalization

Conventions: `spec/README.md`. Profile for every requirement: **learning**.

### MIG-001 — Legacy card mapping
<a id="mig-001"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [MVP §11] [MVP §13] [R00 §14] [R04 §15] [R04 §22]

A legacy Card maps to KnowledgeUnit + minimal KnowledgePoint + self-assessed front/back RecallForm;
a legacy Collection maps to a Collection. Existing collection names, memberships and front/back
content are preserved, and the existing UI stays usable throughout migration.

### MIG-002 — Stable IDs are generated once
<a id="mig-002"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [MVP §11] [R00 §14] [R04 §15] [R04 §16]

Stable IDs are generated once during migration and persisted thereafter; legacy IDs map
deterministically to the new IDs and the mapping is persisted. Migration code preserves stable
entity IDs and learner-history IDs.

### MIG-003 — Never fabricate history
<a id="mig-003"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [MVP §11] [R00 §14] [R02 §15] [R03 §21] [R04 §15] [R04 §22]

Learner history is not reset by normalization. Historical reviews migrate only to the extent the
observable fields exist; unavailable dimensions (hint history, raw answer, exact prompt snapshot)
stay unknown. If per-review data is unavailable, no LearningEvents are invented; aggregate counts
or last-review timestamps are kept as migration metadata or derived seed, not fabricated raw
observations. High-resolution evidence is never fabricated from coarse legacy history.

### MIG-004 — Legacy schedule state
<a id="mig-004"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R02 §15] [R04 §15]

Legacy per-card due/interval data migrates into FixedInterval current schedule state (with legacy
migration provenance) for continuity.

### MIG-005 — Migration is idempotent, transactional, forward-only
<a id="mig-005"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R04 §15] [R04 §16]

Migration is versioned and idempotent, or protected by a migration marker, so repeated startup
cannot duplicate Knowledge or history. Database migrations are forward-only in normal upgrades and
run transactionally where supported.

### MIG-006 — Legacy Markdown adapter
<a id="mig-006"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R01 §16] [FND §18]

Existing Markdown collections/cards remain importable through an adapter producing KnowledgeUnits,
KnowledgePoints, RecallForms and collection membership with generated stable IDs and provenance.
Re-import preserves stable IDs when the adapter can recover them deterministically.
