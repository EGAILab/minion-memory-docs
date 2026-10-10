# Serialization, compatibility and schema evolution — DRAFT normalization

Conventions: `spec/README.md`.

> **Gap statement.** The sources define compatibility *semantics* but no cross-language value
> domain: integer width, float policy, string/Unicode domain, canonical byte form for hashing,
> timestamp encoding and JSON/YAML profile are unspecified. These are hazard rows in
> `assurance/layers/00-cross-language-hazard-inventory.md` and findings NF-013/NF-015/NF-019, to
> be resolved in Layer 01: lossless representation by the contract (path B), every observable
> domain choice by Owner decision (`process/finding-taxonomy.md` §1.1 path C).

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

---

## Layer 01 contract — DRAFT (WP-01)

The requirements below transcribe **Owner decisions** that resolve findings the sources leave
open (`reference/governance/2026-10-10-owner-layer01-decisions.md`, G-012…G-017). Their bundle
citations name where the sources require the capability; the decision record supplies the choice.
They are DRAFT contract text: not reviewed, not implementation-facing.

### SER-008 — Portable value domain
<a id="ser-008"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [R04 §6] [R03 §6] [R05 §5.1] [MVP §18.1] · **Governance:** G-015, G-016, G-017

Every structured payload value that crosses a Minion-Memory seam (public API input, persistence,
canonical serialization) belongs to the portable value domain, identically in every implementation:

- `null`, `true`, `false`;
- integers *n* with −(2^53−1) ≤ *n* ≤ 2^53−1;
- finite IEEE-754 binary64 numbers; NaN and ±Infinity are not values; negative zero is
  normalized to zero at the seam (G-017);
- strings of Unicode scalar values (no surrogate code points);
- arrays of values;
- objects whose member names are strings (as above), unique within the object.

A value outside the domain is **rejected at the seam** with a validation error; it is never
coerced, replaced (e.g. by U+FFFD), clamped or silently deduplicated (last-key-wins).

*Note:* resolves NF-019 (G-015 as amended by G-016; G-017). Whether a whole-number float (`1.0`)
and the integer `1` are distinct values is **not** decided: RFC 8785 serializes both as `1`
(NF-022, open). Stable error codes are proposed in the canonical scenarios
(`value.integer_out_of_range`, `value.lone_surrogate`, `value.duplicate_key`, `value.invalid_json`)
for review.

### SER-009 — Canonical bytes and content hash
<a id="ser-009"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [MVP §18.1] [R04 §7] [R01 §8] [R01 §9] · **Governance:** G-014, G-016, G-017

The canonical bytes of a SER-008 value are its RFC 8785 (JSON Canonicalization Scheme)
serialization, encoded as UTF-8. In particular: object members are ordered by their names' UTF-16
code units (not code points, not UTF-8 bytes); numbers use the ECMAScript shortest round-trip form
(`1.0` → `1`, `1e21` → `1e+21`); strings use RFC 8785 escaping; no insignificant whitespace.
The content hash of a value is the SHA-256 of its canonical bytes, written as 64 lowercase
hexadecimal digits. Text and binary content (e.g. Markdown files, assets) are hashed over their
bytes as given — no Unicode normalization (G-014) and no line-ending conversion.

*Note:* resolves NF-013. Executed feasibility evidence
(`assurance/layers/01-probes/`): the RFC 8785 reference implementation (`rfc8785` 0.1.4, Python)
and an off-the-shelf Rust crate (`serde_jcs` 0.1) **disagree**: the crate orders keys by code point
and emits integers ≥ 2^53, so an implementation must not rely on it unverified. The canonical
scenarios include the discriminating cases.
