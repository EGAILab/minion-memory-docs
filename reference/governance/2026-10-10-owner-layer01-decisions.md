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
