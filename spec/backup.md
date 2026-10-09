# Interchange protocols, backup and restore — DRAFT normalization

Conventions: `spec/README.md`.

### BKP-001 — Package, record export and backup are separate protocols
<a id="bkp-001"></a>
- **Profile:** core · **Source status:** FROZEN · **Sources:** [FND §13] [MVP §8] [R00 §11] [R01 §18]

Knowledge Package (content exchange), Learning Record Export (external analytics/research
projection) and Full Mneme Backup (lossless recovery) are separate protocols with separate
versions. An interchange package is not the runtime database format.

### BKP-002 — Native backup is lossless and layout-independent
<a id="bkp-002"></a>
- **Profile:** core · **Source status:** FROZEN · **Sources:** [FND §13] [R04 §17] [R04 §23] [R04 §24] [MVP §18.1]

Mneme-native portable backup is lossless for durable Mneme data and independent of the local
database layout; it is not merely a copy of a database file. Standards-based exports may be
intentional (lossy) projections.

### BKP-003 — Restore validates before writing
<a id="bkp-003"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [R00 §13] [R03 §19] [R04 §17] [R04 §11]

Restore validates backup format/schema versions and checksums before any destructive write; an
unsupported restore fails before partial writes. Restore verifies history counts and integrity
metadata.

### BKP-004 — Backup preserves profile/type/schema identity
<a id="bkp-004"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [R04 §41.1] [R04 §42]

Portable backup records profile/type/schema identity; restoring a mixed-profile backup preserves it
and never cross-decodes Agent Memory records as LearningEvents or vice versa.

### BKP-005 — Derived data is optional in backup
<a id="bkp-005"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [R04 §17] [IAA §5] [R04 §28]

Derived state (learner/schedule state, checkpoints, indexes) is optional/rebuildable in backup;
after restore it may be rebuilt rather than trusted blindly. Restore correctness must not depend on
checkpoints.

### BKP-006 — Historical assets survive backup
<a id="bkp-006"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [R04 §17] [R04 §8]

Any historical asset required to interpret recorded history remains available in the backup or is
represented by a durable historical snapshot/reference.

### BKP-007 — Restore mode for the MVP
<a id="bkp-007"></a>
- **Profile:** core · **Source status:** MVP_ONLY · **Sources:** [R04 §17] [MVP §13] [R00 §17]

Fresh-install/replace restore is the MVP priority; merge restore may remain future work. For the
Learning Profile, portable backup must restore Knowledge plus durable learner history and config
sufficient to reconstruct the MVP experience on a clean install.

### BKP-008 — Learning backup content (conceptual)
<a id="bkp-008"></a>
- **Profile:** learning · **Source status:** NORMATIVE · **Sources:** [R00 §13] [R04 §17]

The learning Full Backup conceptually contains Knowledge (units/components/recall forms, assets,
provenance), history (episodes/events/raw observations), config, retained historical
interpretations (evaluations/evidence) and optional rebuildable derived state. The layout is
conceptual, not a fixed file structure.
