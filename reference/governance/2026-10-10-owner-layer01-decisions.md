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
