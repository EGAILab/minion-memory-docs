# Owner governance record — Layer 01 observable-semantics decisions (2026-10-10)

**Source:** the Owner's explicit answers in the controlling Claude Code conversation to an options
packet Claude presented for WP-01 (path-C choices, `process/finding-taxonomy.md` §1.1). Recorded
verbatim by Claude per Minion-Agent agent-workflow §11.10. "(Recommended)" marks were Claude's
recommendations; these are decisions because the Owner selected them. They are **not** delegated
decisions (G-009 excludes path-C choices).

The WP-01 contract must transcribe each decision into `spec/**` citing this record; until that
contract is independently reviewed, the corresponding findings remain OPEN with this resolution.

## G-012 — Artifact version semantics (NF-011)

> **Q:** NF-011 — What is an artifact `version`? The sources show integers (`version: 4`) and
> require ordering (higher version updates, lower is stale), but MVP §18.1 says "semantic
> versions".
>
> **A:** Integer edition (Recommended) — "Positive integer, compared numerically. Matches every
> example and the higher/lower reconciliation rule; simplest across Python, Rust and Dart."

## G-013 — Conflicting retry and operation-identity scope (NF-014)

> **Q:** NF-014 — A canonical commit is retried with the same operation_id. If the retried content
> is identical, the sources require returning the prior result. What happens when the content
> differs, and how wide is uniqueness?
>
> **A:** Reject as conflict (Recommended) — "operation_id is unique within one Minion-Memory store
> (all profiles). Identical retry returns the prior result; a different payload is a visible
> conflict error and nothing is written. Same spirit as the same-ID-same-version conflict rule."

## G-014 — Content-hash algorithm and canonical bytes (NF-013)

> **Q:** NF-013 — Content hashes are observable (package entry integrity, same-version conflict
> detection). Which algorithm and byte form?
>
> **A:** SHA-256 + canonical JSON (Recommended) — "SHA-256, lowercase hex, over a defined canonical
> byte form (RFC 8785 JSON Canonicalization for structured content; UTF-8 text as given, no
> Unicode normalization). Formatting changes don't create false conflicts."

## G-015 — Portable value domain (NF-019)

> **Q:** NF-019 — Portable value domain for payloads both implementations must accept identically.
> Lone surrogates are representable in Python but not Rust. Which domain?
>
> **A:** Strict, 64-bit ints (Recommended) — "Integers within signed 64-bit; finite binary64 floats
> only (no NaN/±Inf); strings are Unicode scalar values (lone surrogates rejected at the seam);
> JSON-shaped containers with string keys."

## Still open for Layer 01

NF-010 (ID lexical domain), NF-012 (scope of the conflict rule) and NF-015 (timestamps) carry
escalation conditions; the WP-01 contract either resolves them by path A/B or returns with options.
Note for the contract: RFC 8785 serializes numbers in ECMAScript form; combined with G-015
(signed 64-bit integers beyond 2^53) this interaction must be characterized in the WP-01
feasibility matrix and, if it forces a choice, returned to the Owner.

## G-016 — Integer domain amended to JS-safe integers (amends G-015; resolves G-014/G-015 conflict)

Executed premise probe (`assurance/layers/01-probes/rfc8785-int-domain.md`): the reference RFC 8785
implementation (`rfc8785` 0.1.4, Python 3.12.8) raises `IntegerDomainError` for every integer of
magnitude ≥ 2^53, including 2^53 and the signed-64-bit limits G-015 allowed.

> **Q:** Probe result: RFC 8785 (your G-014 hashing choice) cannot represent integers of magnitude
> ≥ 2^53. The reference library raises an error for every value from 2^53 up to the signed-64-bit
> limits that G-015 allows. How should Layer 01 resolve this conflict?
>
> **A:** JS-safe integers (Recommended) — "Amend G-015: integers limited to ±(2^53−1) everywhere.
> Hashing stays strict, standard RFC 8785, so Python and Rust can each use or check against
> independent off-the-shelf implementations. Consequence: integer timestamps can be at most
> microsecond precision since epoch."

Effect: G-015's integer bound becomes ±(2^53−1); the rest of G-015 (finite binary64 floats, Unicode
scalar strings, JSON-shaped containers with string keys) is unchanged.

## G-017 — Negative zero normalized

Executed probe: RFC 8785 serializes `-0.0` and `0.0` to identical bytes.

> **Q:** Probe result: canonical JSON writes -0.0 and 0.0 as the same bytes, so the content hash
> cannot tell them apart. Under G-015 (finite floats allowed), how should negative zero be treated?
>
> **A:** Normalize -0 to 0 (Recommended) — "Values are normalized at the seam: -0.0 is stored and
> returned as 0.0. The domain then matches what hashing can see, and nothing differs invisibly."

## Contract fact recorded with G-014 (authority reading, path A — not a new decision)

RFC 8785 orders object members by UTF-16 code units, not code points (probe: `"\U0001F600"` sorts
before `"｡"`, the reverse of code-point / UTF-8 byte order). This follows from G-014's choice of
RFC 8785; the WP-01 contract states it and canonical fixtures must include a discriminating pair.

## G-020 — Stable ID lexical domain (NF-010)

> **Q:** NF-010 — What characters may a stable ID contain? IDs become package file names
> (`memories/<knowledge-unit-id>.md`), and Windows file names are case-insensitive.
>
> **A:** "Choose 1 — Lowercase portable token, with two contract corrections.Adopt a 1–128-byte
> ASCII stable ID, beginning with a-z or 0-9, followed only by a-z, 0-9, ., _, -, compared
> byte-for-byte. For filename portability, additionally forbid a trailing . and reject Windows
> reserved device basenames such as con, prn, aux, nul, com1–com9, and lpt1–lpt9, including those
> followed by an extension-like suffix. No Unicode normalization or case folding is ever part of
> stable-ID identity. Human-readable Unicode belongs in titles/labels/source keys, not stable
> IDs.Also pin that memories/<id>.md is a deterministic path projection of the stable ID, not a
> second identity namespace."

## G-021 — Scope of the same-ID-same-version conflict rule (NF-012)

> **Q:** NF-012 — "Same ID + same version + different content = conflict" is stated in the sources
> only for Knowledge. Should it apply to every versioned artifact?
>
> **A:** "Choose 1 — Core-wide, with the rule scoped to immutable semantically versioned
> artifacts.For every artifact whose (stable_id, artifact_version) denotes an immutable semantic
> revision, that pair MUST resolve to exactly one canonical content value. Encountering the same ID
> and same artifact version with different canonical content is a visible conflict;
> implementations MUST NOT silently overwrite, merge, normalize away, or choose one side.This rule
> does not apply merely because something has a schema_version, model_version,
> database_schema_version, or checkpoint-format version. Each artifact type must define its
> canonical semantic-content projection. Mutable counters, access history,
> reinforcement/retrieval observations and derived state should normally live outside the
> immutable versioned artifact rather than mutate it under the same version."

## G-022 — Timestamp representation (NF-015)

> **Q:** NF-015 — How are timestamps (occurred_at, recorded_at) represented? G-016 limits integer
> timestamps to microsecond precision.
>
> **A:** "Choose 1 — RFC 3339 UTC with exactly six fractional digits.Make
> YYYY-MM-DDTHH:MM:SS.ffffffZ the sole canonical persisted/wire spelling. UTC Z is mandatory;
> equivalent local-offset spellings, omitted/shorter/greater fractional precision, and leap-second
> :60 forms are non-canonical. Unknown time is represented by field absence, never null, epoch, or
> another sentinel.occurred_at and recorded_at retain distinct semantics, and timestamps MUST NOT
> substitute for explicit semantic ordering such as episode sequence_no. If local wall-clock/time-zone
> context is later required, represent it separately from the canonical instant.Physical storage
> MAY use integer microseconds internally if and only if canonical round-trip is lossless."

## G-023 — One numeric kind (NF-022)

> **Q:** NF-022 — Canonical JSON writes the integer 1 and the float 1.0 identically, so the hash
> can't tell them apart. Are they the same value?
>
> **A:** "Choose 1 — Same value.Mneme canonical JSON has one numeric semantic kind. Any accepted
> numeric spellings that canonicalize to the same canonical JSON number represent the same value;
> therefore 1, 1.0, 1e0, etc. are semantically identical after the canonical boundary and MUST
> produce identical canonical content and hashes.Do not preserve numeric distinctions that
> canonical serialization cannot observe. If a future domain genuinely requires distinctions such
> as arbitrary-precision integers or typed decimal values, represent those with an explicit
> domain/schema encoding rather than an invisible JSON-number subtype.Pin the interoperable numeric
> domain and its precision limits separately, including finite-only behavior and the handling of
> -0."

## G-025 — Whole-number values under one numeric kind (NF-024)

> **Q:** NF-024: You chose one numeric kind (G-023), and integers are capped at ±(2^53−1) (G-016).
> Is a whole number above that cap valid when written as a float, e.g. 1e21 or
> 9007199254740992.0? Both spellings now mean the same value, so they need one answer.
>
> **A:** "Choose 1 — Cap every whole numeric value, independent of spelling.Apply the safe-integer
> constraint after numeric normalization, not based on whether the source token used integer,
> decimal, or exponent syntax. Any canonical numeric value that is integral MUST lie within
> ±(2^53−1). Therefore 9007199254740992, 9007199254740992.0, 9.007199254740992e15, and 1e21 are all
> rejected.Non-integral finite values remain governed by the adopted canonical binary64 numeric
> domain. Do not claim that this preserves arbitrary large fractional magnitudes: above the binary64
> safe-integer region, representable values are themselves integral-valued and therefore fall under
> this rule.Exact numeric values outside the generic number domain require an explicit schema type
> rather than an alternate JSON-number spelling."

## G-026 — Timestamp input at the public seam (NF-025)

> **Q:** NF-025: Your timestamp rule (G-022) makes RFC 3339 UTC with exactly 6 fractional digits
> the only canonical form. What happens when a public API receives a non-canonical one, e.g.
> '2026-10-10T16:30:00+11:00' or '...05:30:00.5Z'?
>
> **A:** "Choose 2 — Normalize lossless forms at the public seam.Distinguish accepted timestamp
> input from canonical timestamp representation. Public APIs MAY accept RFC 3339 timestamps with an
> explicit Z or ±HH:MM offset and zero through six fractional-second digits. They MUST normalize the
> instant to UTC and emit/store exactly YYYY-MM-DDTHH:MM:SS.ffffffZ; shorter fractions are
> right-padded with zeroes.Reject timezone-less timestamps, leap-second :60, invalid calendar
> values, and any input with more than six fractional digits. Do not rely on whatever forms a
> host-language datetime parser happens to accept; the shared contract defines the accepted
> grammar.Equality, hashing, persistence, conflict detection and cross-language conformance operate
> only on the normalized canonical value. Original offset/spelling is not part of timestamp
> semantics; local-time context, if needed, is separate metadata."

## G-028 — Timestamp input letter case (WP01-CR-001a)

> **Q:** WP01-CR-001a: RFC 3339 allows lowercase 't' and 'z' in timestamps (e.g.
> 2026-10-10t05:30:00z) but lets an application require uppercase. Which does the Mneme input
> grammar accept?
>
> **A:** "Choose 2 — Accept lowercase t/z and normalize them.Mneme’s public timestamp input grammar
> accepts both uppercase and lowercase RFC 3339 T/Z designators. Lowercase carries no semantic
> distinction, so rejecting it would only narrow interoperability without protecting any Mneme
> invariant. Canonical persisted/wire output remains uppercase T and Z with exactly six fractional
> digits.This does not mean “accept whatever the host datetime parser accepts”; only the explicitly
> specified Mneme grammar is valid."

## G-029 — Timestamp year range and UTC overflow (WP01-CR-001b)

> **Q:** WP01-CR-001b: Which calendar years are valid, and what happens when converting an offset to
> UTC lands outside them (e.g. 9999-12-31T23:59:59-00:01 becomes year 10000)?
>
> **A:** "Choose 1 — years 0001 through 9999, with UTC-overflow rejection.Mneme timestamps use the
> proleptic Gregorian calendar and do not admit year 0000. Both the parsed local civil timestamp and
> the UTC instant produced after offset normalization must lie within 0001-01-01 through 9999-12-31.
> If applying the offset crosses either boundary, reject the timestamp as timestamp.invalid; do not
> clamp, wrap, or preserve an otherwise non-representable offset form.This keeps the canonical YYYY
> contract exact and avoids introducing astronomical year-zero semantics that neither Mneme profile
> requires."

## G-030 — Timestamp input grammar is required, not optional (WP01-CR-001c)

> **Q:** WP01-CR-001c: Your G-026 says public APIs MAY accept non-canonical RFC 3339 forms (offsets,
> 0–5 fractional digits). For two implementations to agree, is that acceptance required or
> optional?
>
> **A:** "Choose 1 — Required.Replace the permissive “MAY accept” language with a normative shared
> input grammar. Every conforming implementation MUST accept every spelling explicitly included in
> that grammar and normalize it to the same canonical YYYY-MM-DDTHH:MM:SS.ffffffZ value. Every
> explicitly excluded form MUST be rejected consistently.Conformance must exercise both accepted
> non-canonical forms and agreed rejection cases in Python and Rust. Acceptance behavior is part of
> the cross-language public contract, not an implementation option."

## G-031 — One error under a fixed validation precedence (WP01-CR-003)

> **Q:** WP01-CR-003: When one input is invalid in several ways (e.g. a duplicate key AND an
> out-of-range integer, or a version that is both a generic out-of-range number and an invalid
> version), which error must be reported?
>
> **A:** "Choose 1 — exactly one error under a fixed validation precedence.Define three ordered
> stages: (1) JSON/structural decoding, including duplicate keys; (2) generic Mneme value-domain
> validation; (3) typed/domain-field validation such as version, stable ID, and timestamp rules. A
> failure in an earlier stage prevents later-stage interpretation.Within one stage, return the first
> violation under a shared deterministic document traversal order. Python and Rust MUST return the
> same error code for the same invalid input.Do not aggregate downstream errors from an input whose
> earlier structural/value interpretation is already invalid."

## G-032 — Operation identity is a namespaced pair (WP-01 review Q1)

> **Q:** Q1 (CORE-012): A canonical commit carries a durable operation identity (operation_id /
> submission identity / durable source identity, e.g. a Minion-Agent capture ID or a Flashcard
> submission ID). My draft said it 'follows CORE-001's ID domain' — that was my addition, not your
> decision. What is an operation identity's domain?
>
> **A:** "Choose 3 — Namespaced pair.Define OperationIdentity as {source_namespace,
> source_operation_id}. source_namespace uses the G-020 portable stable-token domain and identifies
> the producer uniqueness domain. source_operation_id is a bounded, non-empty opaque string supplied
> by that producer and compared exactly, with no normalization, case folding, trimming, parsing, or
> filename restrictions.Uniqueness and idempotency apply to the pair, not either field separately.
> Do not concatenate the fields into a delimiter-based string in the canonical model.Repeating the
> same pair for the same logical mutation is an idempotent retry; reusing the same pair for
> materially different canonical mutation content is a visible conflict, not last-write-wins.If a
> producer's IDs are only unique within a deployment/instance, its source_namespace must identify
> that uniqueness domain rather than claiming a broader namespace."

## G-033 — source_operation_id length bound (G-032 follow-up)

> **Q:** G-032 follow-up: what is the length bound for source_operation_id (the opaque
> producer-supplied string)?
>
> **A:** "Choose 1 — 1–256 UTF-8 bytes.Measure the bound on the exact UTF-8 encoding of the opaque
> producer-supplied string. Reject empty values and values over 256 bytes; never truncate or
> silently replace the ID with a digest. This bound is intentionally larger than G-020’s stable-ID
> limit because operation IDs are not filenames and may be composite or URL-like, while still
> keeping idempotency/index keys bounded across Python, Rust, storage, and exports."

## G-034 — Within-stage traversal order (WP01-CR-005)

> **Q:** WP01-CR-005: G-031 says 'first violation under a shared deterministic traversal order' but
> doesn't fix the order. It's observable: for {"b":9007199254740992,"a":1e400}, canonical order
> reports value.number_not_finite, source order reports value.integer_out_of_range. Which
> within-stage order?
>
> **A:** "Choose 1 — Canonical order.Stage 1 representation/JSON-decoding failures are selected in
> source-text order, because representation defects such as duplicate keys exist only there. Once
> decoding succeeds, Stages 2 and 3 operate on the canonical Mneme value and MUST use one shared
> deterministic traversal: depth-first; object members in SER-009 canonical UTF-16 key order; for
> each member, name/key before its value; arrays by ascending index; primitive/declared arguments
> in declared order.Host map iteration/insertion order is never observable. Equivalent JSON texts
> and equivalent native maps must therefore produce the same first error code."

## G-035 — CORE-003 revision record shape (WP01-PY-005)

> **Q:** WP01-PY-005: The CORE-003 comparison takes revision records {stable_id, artifact_version?,
> projection}. The contract doesn't say what happens with a malformed record (missing stable_id or
> projection, extra members) or which error code it gets. What policy?
>
> **A:** "Choose 1 — strict shape with artifact.revision_invalid.CORE-003 accepts a closed
> RevisionRecord containing required stable_id and projection, plus optional artifact_version.
> Non-object input, missing required members, or unknown extra members are rejected as
> artifact.revision_invalid. Only after the record shape is valid are present typed fields
> validated; an invalid stable_id yields id.invalid, and an invalid present artifact_version yields
> version.invalid. Generic invalid values remain Stage-2 errors.Absence of artifact_version yields
> not_applicable only after the complete record has otherwise validated. It must not bypass
> missing-field or extra-member validation."

## G-036 — Native array binding: list and tuple (WP01-PY-006)

> **Q:** WP01-PY-006: At the native (in-process) API, should a Python tuple be accepted as a JSON
> array? Lists are accepted; the contract lists bytes, sets, dates and non-string keys as
> unsupported but doesn't mention tuples.
>
> **A:** "Choose 1 — accept Python list and tuple as the same canonical array kind.This is a
> language-binding rule, not a new Mneme value type. Both preserve element order, are recursively
> validated by ascending index, and canonicalize identically; Python mutability versus immutability
> is not part of Mneme semantics. Do not generalize acceptance to arbitrary Sequence/iterable types
> such as range, generators, bytes, or custom sequence objects.Other language bindings may accept
> their own natural ordered-array representations (for Rust, e.g. Vec, slices, or arrays) while
> exposing the same canonical array semantics. A tuple at the generic seam is always an array and
> must never be inferred as a typed domain record."
