# Serialization, compatibility and schema evolution — DRAFT normalization

Conventions: `spec/README.md`.

> **Gap statement.** The sources define compatibility *semantics* but no cross-language value
> domain: integer width, float policy, string/Unicode domain, canonical byte form for hashing,
> timestamp encoding and JSON/YAML profile are unspecified. These are hazard rows in
> `assurance/layers/00-cross-language-hazard-inventory.md` and findings NF-013/NF-015/NF-019, to
> be settled in the Layer 01 contract.

### SER-001 — Explicit schema versions; declared read window
<a id="ser-001"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [R00 §15] [R03 §19] [R04 §16] [MVP §18.1]

Durable record families carry explicit schema versions. The application writes current schema
versions while reading a declared supported window of historical versions. Domain schemas are
durable contracts; database schemas are implementation details.

### SER-002 — Old records decode through version-specific readers
<a id="ser-002"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [FND §16] [R00 §15] [R03 §19] [IAA §7] [R04 §16]

Old persisted records are decoded through version-specific readers into the current normalized
domain semantics. They are not repeatedly rewritten in place to match the newest schema.

### SER-003 — Missing is unknown
<a id="ser-003"></a>
- **Profile:** core · **Source status:** FROZEN · **Sources:** [FND §16] [R00 §15] [R03 §19] [R04 §16] [MVP §13]

Fields missing from old data remain absent/unknown; they never receive invented or misleading
defaults.

### SER-004 — No silent change of stored meaning
<a id="ser-004"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [R00 §15] [R03 §19] [R04 §16] [R04 §22]

Semantic breaking changes use new fields, types, payload versions or IDs; the meaning of an
existing persisted field never changes silently. Future richer payloads are added without
redefining existing stored semantics.

### SER-005 — Required versus ignorable compatibility
<a id="ser-005"></a>
- **Profile:** core · **Source status:** GUARDRAIL · **Sources:** [IAA §A4] [IAA §3] [R04 §27] [R04 §30] [R01 §18] [R05 §14]

Serialized history records declare compatibility `required | ignorable`. A decoder encountering an
unknown required record type/semantics stops semantic replay with a clear compatibility error
rather than producing a misleading state or silently omitting semantics; only types explicitly
declared ignorable may be skipped. Purely informational telemetry may be ignorable only if
skipping it cannot change reconstruction of meaning; records that affect evidence, corrections or
completion are normally required. Unknown required package semantics also fail safely.

### SER-006 — Profile and type identity are explicit
<a id="ser-006"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [R03 §28] [R04 §41.1] [R04 §42] [MVP §18.1]

If shared storage or serialization is used, profile/type/schema identity is explicit so a reader
never interprets Agent Memory records as LearningEvents or vice versa.

### SER-007 — Migration fixtures per supported version
<a id="ser-007"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [R00 §15] [R04 §16]

Migration/decoding fixtures exist for legacy data and for each supported shipped schema version
(event, package, database, backup).
