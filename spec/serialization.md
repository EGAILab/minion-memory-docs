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

**One numeric kind (Owner G-023, DRAFT).**
- **One kind.** Mneme canonical JSON has a single numeric semantic kind. Accepted numeric
  spellings that canonicalize to the same RFC 8785 number are the same value, and produce
  identical canonical content and hashes. So `1`, `1.0` and `1e0` are one value.
- **No hidden distinctions.** A numeric distinction that canonical serialization cannot observe is
  not preserved.
- **Other numeric domains.** A domain that genuinely needs one (arbitrary-precision integers, typed
  decimals) uses an explicit schema encoding, not an invisible JSON-number subtype.

**Whole-number values (Owner G-025, DRAFT).**
- **Spelling-independent bound.** The safe-integer bound applies after numeric normalization,
  whatever the token's integer, decimal or exponent spelling. Any numeric value that is integral
  must satisfy −(2^53−1) ≤ *v* ≤ 2^53−1. So `9007199254740992`, `9007199254740992.0`,
  `9.007199254740992e15` and `1e21` are all rejected.
- **Non-integral values.** They keep the finite binary64 domain. This is not a promise of
  arbitrarily large fractional magnitudes: above the safe-integer region every representable
  binary64 value is itself integral, so it falls under the bound.
- **Larger exact values.** Exact values outside this generic domain need an explicit schema type,
  never an alternate JSON-number spelling.

**Validation stages and error map (Owner G-031, DRAFT).** Every input is validated in three ordered
stages. A failure in an earlier stage stops validation, and exactly **one** error code is
reported. Python and Rust must report the same code for the same input, and later-stage errors
are never aggregated.

| Stage | Applies to | Code | Rejects |
|---|---|---|---|
| 1 — decoding | JSON text | `value.invalid_json` | text that is not UTF-8, or not one RFC 8259 JSON value: `NaN`/`Infinity` literals, comments, trailing commas, leading zeros, trailing content, empty text |
| 1 | JSON text | `value.lone_surrogate` | a `\u` escape, in a string or a member name, that yields an unpaired surrogate (raw surrogate bytes are invalid UTF-8, so `value.invalid_json`) |
| 1 | JSON text | `value.duplicate_key` | an object member whose name, **after escape decoding**, equals an earlier member's name in the same object (`{"a":1,"a":2}`); detected before any map discards it |
| 1 | native values | `value.unsupported_type` | a value or member name of a kind outside the JSON data model, e.g. byte strings, sets, date-time objects, non-string map keys, objects only spoofing an admitted `__class__` |
| 1 | native values | `value.duplicate_key` | two member names of one native map with equal base strings (G-039) |
| 1 | native values | `value.cyclic` | a native container that contains itself, directly or indirectly (G-040) |
| 2 — value domain | every decoded or native value | `value.number_not_finite` | a numeral whose binary64 value overflows (`1e400`), and a native NaN or ±Infinity |
| 2 | ″ | `value.integer_out_of_range` | an integral value outside ±(2^53−1), after the number interpretation below (G-025) |
| 2 | ″ | `value.lone_surrogate` | a native string or member name containing a surrogate code point |
| 3 — typed fields | typed arguments and fields | `version.invalid` / `id.invalid` / `timestamp.invalid` / `operation_identity.invalid` / `artifact.revision_invalid` | CORE-002 / CORE-001 / HIST-004 / CORE-012 rules / CORE-003 record shape (G-035) |

- **Order within a stage (Owner G-034).**
  - **Stage 1, JSON text.** Reports the violation that occurs first in the source text; a
    duplicate is located at its second occurrence.
  - **Stage 1, native values.** Follows canonical traversal (G-034). A map's duplicate base names
    are found while ordering that map's members, and an unsupported kind found earlier in that
    traversal wins (G-039). A cycle is reported where traversal re-enters an open container
    (G-040).
  - **Stages 2 and 3** operate on the decoded canonical value and use one shared traversal:
    depth-first; object members in SER-009 canonical order (names by UTF-16 code units); for each
    member, its name before its value; arrays by ascending index; a primitive's arguments in
    declared order.
  - **Host order never observable.** Host map iteration or insertion order is never observable.
    Equivalent JSON texts (members in any order) and equivalent native maps produce the same first
    error code.
- **Number interpretation (authority reading of RFC 8785 §3.2.2.3).**
  - A JSON numeral denotes the IEEE 754 binary64 value nearest its exact decimal value, ties to
    even. Hence `1.0000000000000001` is 1 and `5e-324` is kept.
  - `1e-400` is 0, and `-1e-400` is −0, which is normalized to 0 (G-017).
  - `9007199254740991.5` rounds to 2^53 and is rejected as `value.integer_out_of_range`.
  - A native integer is taken exactly, without rounding.
  - Accepting a value never depends on a host parser's integer/float tag or its overflow
    behaviour.
- **Stages across arguments.** For a primitive with several arguments, each stage runs over
  **all** arguments, in declared order, before the next stage starts (G-031). So a stage-1 failure
  in a later argument outranks a stage-2 failure in an earlier one. Arguments may arrive as JSON
  text or as native values.
- **Native array binding (Owner G-036).** At a native seam, a language binds its own natural
  ordered-array types to the one canonical array kind. In Python these are `list` and `tuple`,
  and no other sequence or iterable type (not `range`, generators, `bytes` or custom sequences);
  Rust binds e.g. `Vec`, slices and arrays. Both preserve order, are validated by ascending index
  and canonicalize identically. This is a binding rule, not a new value type: a tuple is always an
  array, never inferred as a typed record.
- **Native subclasses (Owner G-037).** A subclass of an admitted built-in family (`int`, `float`,
  `str`, `list`, `tuple`, `dict`) is accepted, but only its underlying built-in value is used:
  base-built-in semantics for scalar extraction, string contents, sequence elements and mapping
  entries.
  - **Never invoked.** Hashing, traversal, validation, diagnostics and error selection never invoke
    subclass overrides, such as `__repr__`, `__str__`, `__iter__`, `items`, conversion hooks or any
    other user-defined behaviour.
  - **Ignored.** Subclass-added attributes and state are ignored.
  - **Examples.** A `NamedTuple` is an array, an `OrderedDict` an object and an `IntEnum` member its
    underlying integer.
  - **Typed meaning.** Typed domain meaning requires an explicit typed adapter, never inference from
    the Python subclass.
- **Native binding completion (Owner G-039–G-042).**
  - **Not a subclass.** Only a genuine subclass is admitted. An object that merely reports an
    admitted `__class__` is `value.unsupported_type` (CE-01-01 challenge, authority reading of
    G-037).
  - **Duplicate names.** Two member names of one native map whose base strings are equal are
    `value.duplicate_key`, at native stage 1, found while ordering that map's members in canonical
    traversal (G-039).
  - **Cycles.** A native container that contains itself, directly or indirectly, is `value.cyclic`, at
    native stage 1, reported where traversal re-enters an open container. Shared non-cyclic
    references remain legal (G-040).
  - **Byte buffers and control objects.** The no-hook rule also covers byte-buffer subclasses at the
    raw-hash and JSON-bytes seams (their underlying bytes), `JsonText` (its stored text) and argument
    maps (base entries, declared order) (G-041).
  - **Returned values.** They are always exact built-ins (`None`, `bool`, `int`, `float`, `str`,
    `list`, `dict`) without subclass identity or added state (G-042).
  - **Argument maps.** An argument map passed to a validation entry point is a `dict` or a `dict`
    subclass, read through base entries. Any other mapping is a caller programming error: it raises
    `TypeError` immediately, before any argument is inspected and with no hook. It is outside the
    Mneme value-error vocabulary (G-043).
- **Precedence example.** An over-large version `9007199254740992` fails stage 2
  (`value.integer_out_of_range`), so it is never interpreted as a version. `0`, `-1`, `1.5` and
  `true` pass stage 2 and fail stage 3 (`version.invalid`).

*Note:* resolves NF-019 (G-015 as amended by G-016; G-017), NF-022 (G-023), NF-024 (G-025), the
precedence question of WP01-CR-003 (G-031) and the within-stage order of WP01-CR-005 (G-034).
- **Codes.** The codes name rejections the domain already fixes (representation, path B).
- **Native-value seam.** This seam is exercised by host-language conformance tests. JSON-text
  scenarios cannot construct native values.

### SER-009 — Canonical bytes and content hash
<a id="ser-009"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [MVP §18.1] [R04 §7] [R01 §8] [R01 §9] · **Governance:** G-014, G-016, G-017

The canonical bytes of a SER-008 value are its RFC 8785 (JSON Canonicalization Scheme)
serialization, encoded as UTF-8. In particular: object members are ordered by their names' UTF-16
code units (not code points, not UTF-8 bytes); numbers use the ECMAScript shortest round-trip form
(`1.0` → `1`, `1.5e-7` → `1.5e-7`, `0.000001` → `0.000001`); strings use RFC 8785 escaping; no
insignificant whitespace. (Raw JCS would also write `1e21` as `1e+21`, but `1e21` is outside the
Mneme value domain, G-025.)
The content hash of a value is the SHA-256 of its canonical bytes, written as 64 lowercase
hexadecimal digits. Text and binary content (e.g. Markdown files, assets) are hashed over their
bytes as given — no Unicode normalization (G-014) and no line-ending conversion.

*Note:* resolves NF-013. Executed feasibility evidence
(`assurance/layers/01-probes/`): the RFC 8785 reference implementation (`rfc8785` 0.1.4, Python)
and an off-the-shelf Rust crate (`serde_jcs` 0.1) **disagree**.
- **The serializer defect.** The crate orders object members by code point instead of UTF-16 code
  units, so it is not RFC 8785-conformant and must not be adopted unchanged.
- **Not a serializer defect.** The crate emitting 2^53 is no RFC defect (RFC 8785 Appendix B
  includes that binary64 value); such values are excluded by **Mneme's** domain (G-025), and that is
  the seam validator's job.

A conformant implementation needs:
- recursive ordering by UTF-16 code units;
- RFC 8785 string escaping and ECMAScript number formatting;
- duplicate-aware decoding before map construction;
- the SER-008 stage checks.

The canonical scenarios include the discriminating cases.
