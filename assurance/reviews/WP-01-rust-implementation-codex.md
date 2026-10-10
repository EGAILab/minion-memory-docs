# WP-01 — Rust Layer 01 implementation record (Codex)

**Author:** Codex, Rust implementation owner. **Date:** 2026-10-11.
**Gate:** G3 (Rust). **Disposition:** candidate ready for independent CLOSURE_REVIEW.
This is author-run candidate evidence, not independent approval or certification.

## Candidate and authority

- Code `wp01/rust`: **`b07f33752fbc19b02c8de00e9ebbaa75d0a2f8ea`**.
- Docs `wp01/rust`: the commit carrying this record, based on accepted
  **`83c66c25d560accb3d57ba20be631d55faab72ff`**. Its exact SHA is supplied in the hand-off.
- Code baseline: accepted **`bac6594e06dd321e547e917cebeeefc6562a19b9`**.
- Authority: `spec/core.md` CORE-001/002/003/011/012 and HIST-004;
  `spec/serialization.md` SER-008/009; Owner G-012–G-043;
  the unchanged eight ACTIVE canonical scenarios and their expectations.
- Readiness guidance: `assurance/layers/01-feasibility-matrix.md`.
- Worktrees: `review-worktrees/code-wp01-rust`, `review-worktrees/docs-wp01-rust`.

The shared contract and corpus were the implementation authority. No Mneme Python implementation
or Python output was used to derive Rust behavior. ECMAScript number controls were generated
independently with Node 22.15.1; fixed canonical scenario bytes/hashes remain the accepted corpus.

## Implementation and traceability

Single-package Cargo workspace at `minion-memory-rust/`, public crate `minion_memory`.
Rust **1.97.1** is pinned; direct dependencies and the transitive lockfile are committed.

| Contract | Public seam | Code location |
|---|---|---|
| CORE-001 / G-020 | `validate_stable_id` | `minion-memory-rust/src/identity.rs` |
| CORE-002 / G-012, G-023, G-025 | `validate_version`, `compare_versions` | `minion-memory-rust/src/identity.rs` |
| CORE-003 / G-021, G-035 | `compare_artifact_revisions` | `minion-memory-rust/src/identity.rs` |
| CORE-011 / G-014 | `content_hash`, `raw_content_hash` | `minion-memory-rust/src/values.rs` |
| CORE-012 / G-032, G-033 | `operation_identity`, `compare_operation_identities` | `minion-memory-rust/src/identity.rs` |
| HIST-004 / G-022, G-026, G-028–030 | `normalize_timestamp` | `minion-memory-rust/src/time.rs` |
| SER-008 / G-015–017, G-023, G-025, G-031, G-034–043 | `Value`, `Input`, `validate_value`, `validate_arguments`, `decode_text`, `decode_json` | `minion-memory-rust/src/values.rs`, `json.rs`, `errors.rs` |
| SER-009 / G-014, G-016, G-017 | `canonical_bytes`, `content_hash` | `minion-memory-rust/src/values.rs` |

The manifest delta adds precisely these eight Rust locations. No requirement metadata, scenario,
Python code, process state, certification registry or contract text was changed.

### Binding and validation stages

- `Value` stores an owned flat arena with private indices. Native constructors bind exact
  `i128` integers, binary64 values, strings, booleans, null, Vec/slice/array elements and
  string-keyed object entries. Duplicate names are retained until stage 1. Invalid numeric
  values are retained until stage 2.
- Rust UTF-8 strings cannot contain surrogate code points. Private arena indices and ownership
  prevent cycles, non-string member names, arbitrary host objects and malformed graphs from
  crossing this binding. `value.unsupported_type` and `value.cyclic` remain in the shared error
  vocabulary; this statically typed binding cannot construct their witnesses.
- There is no subclass identity, added host state, dynamic argument map or user conversion trait
  at a public input seam. Borrowed `Input::Native`, `Text` and `Bytes` explicitly select the
  boundary. Vec, slices and arrays use stored elements; raw hashing reads a byte slice directly.
  Caller misuse of the static Rust signature is a compile-time error, outside the value vocabulary.
- Normalization returns library-owned values and primitives, never caller container identity
  or hidden numeric distinctions. Whole-number floats and negative zero become exact integers.
  A native integer is checked exactly, without first rounding through binary64.
- The structural pass runs across **all** arguments before the numeric pass; typed rules follow
  both generic stages. Each comparison declares `a`, then `b`. Typed revision shape is checked
  before its fields; `artifact_version` precedes `stable_id` in canonical field order. Both records
  are fully valid before `not_applicable`, `distinct`, `identical` or conflict is determined.
- Exactly one stable error is returned. Errors within multi-argument validation name the argument.
  Diagnostic detail is bounded, does not stringify the input and is not an equality oracle.

### Decoder, canonical bytes and timestamp seam

- A strict, iterative RFC 8259 parser detects duplicate names after escape decoding and rejects
  unpaired surrogate escapes. It stores numeric token spellings without converting them during
  stage 1. Thus `{"a":1e400,"b":1,"b":2}` reports `value.duplicate_key`, not a host number error.
- Invalid UTF-8 is treated as a source-position violation: the valid prefix can reveal an earlier
  duplicate/surrogate; otherwise the encoding failure is `value.invalid_json`. No replacement
  character is inserted. Comments, NaN literals, trailing content/commas and malformed numerals
  are rejected. Stage 2 interprets numerals as binary64, applies integral bounds and walks the
  canonical value depth-first (UTF-16 object member order; ascending array indices).
- Serialization owns UTF-16 ordering and RFC 8785 string escaping. Pinned `ryu-js` 0.2.2 supplies
  ECMAScript shortest binary64 formatting; pinned `sha2` 0.10.9 supplies SHA-256 lowercase hex.
  `serde_jcs` is not used. Raw byte hashes perform no Unicode or line-ending normalization.
- HIST-004's ASCII grammar is checked before `chrono` 0.4.45 is called for calendar arithmetic:
  exactly four year digits, required time and zone, T/t and Z/z, seconds 00–59, fractional
  precision 1–6, offsets through 23:59. Calendar validity and both local/normalized UTC year
  bounds 0001–9999 are checked. Output always uses uppercase UTC and six fractional digits.
- Parsing, traversal, canonical serialization, clone, debug and drop do not recurse through the
  tree. The 100,000-level positive control passes on both platforms. This adds no contract depth
  cutoff. Memory exhaustion is still possible; repeatedly wrapping native arrays copies arenas.

## Thin canonical runner

`minion-memory-rust/tests/conformance.rs` discovers the unchanged corpus in the three family
directories. Every envelope is checked against the shared Draft 2020-12 JSON Schema.
`tests/support/mod.rs` reads the portable YAML profile at the event boundary: no anchors,
aliases, explicit tags, duplicate/non-string keys or non-finite floats; scalars with divergent
YAML 1.1/core readings require quotes. Quoted strings stay strings and native integers are
constructed exactly (Rust `i128`), without float conversion. Corpus JSON text is passed unchanged
to the library decoder.

The runner only constructs arguments, calls public functions, encodes observable enum/error
results and compares expectations. It contains no timestamp repair, number normalization,
canonical serialization, hashing, identity rules or revision policy. Missing arguments and
unknown ACTIVE operations fail. Recursive `TO_BE_` detection reports expected failures with
the corpus rule as its reason; an ACTIVE placeholder is an error. The five future-layer cases
are explicitly reported, not silently skipped.

## Executed evidence

G3 batches are sequential, with no network in the gates. Both hosts use rustc **1.97.1**
(`8bab26f4f`, 2026-07-14). Windows target: `x86_64-pc-windows-msvc`;
POSIX target: `x86_64-unknown-linux-gnu`, Ubuntu under WSL, reading the shared E: worktree.

| Gate | Windows | POSIX |
|---|---|---|
| `cargo fmt --check` | PASS | PASS |
| `cargo clippy --locked --offline --workspace --all-targets -- -D warnings` | PASS | PASS |
| `cargo test --locked --offline -- --nocapture` | 16 integration tests + 1 doctest passed | 16 integration tests + 1 doctest passed |
| Shared canonical runner | 8 ACTIVE / 146 steps; 5 explicit expected failures | 8 ACTIVE / 146 steps; 5 explicit expected failures |
| `RUSTDOCFLAGS=-D warnings cargo doc --locked --offline --no-deps` | PASS | PASS |
| `mneme-process check --deep-sources` against candidate worktrees | 8/8 PASS | shared check run on Windows |

Rust has no specified numerical coverage floor in `process/gate-tiers.md`; this record does not
claim a measured Rust coverage percentage. Every public Layer 01 operation is exercised through
public seams. No Python-language gate is claimed. The manifest is shared traceability; Claude
should run Python's canonical runner at the next owner pass as required by G2.

`tests/layer01.rs` executes structural/source/stage precedence, mixed argument seams, generic
numeric bounds, negative zero, subnormal/overflow/underflow and ties-to-even examples, native
duplicates, UTF-16 recursive ordering, all string escapes, byte-exact hashes, stable-ID and edition
neighborhoods, operation pair shape/byte lengths, closed revision records and timestamp grammar,
calendar and UTC-boundary controls. Diagnostics and the 100,000-deep tree are also exercised.

Independent ECMAScript controls in `tests/vectors/`: **512** fixed/seeded native binary64 rows,
with 24-significant-digit text spellings for finite rows. Both the native and decimal routes match
the independently generated expectations. Node 22.15.1 and a fixed generator are recorded;
Node is not needed at test time. Fixture SHA-256:
`4cda345fb58d7b9fe5a4686623571d4129869697bf15ea91651eff253ff98dda`.

### G1 known-bad controls

Each control first demonstrates the correct public-seam baseline, then rejects the wrong
observable behavior. These execute without modifying production code:

- code-point/UTF-8 object ordering versus UTF-16 (actual `serde_json` wrong-order output);
- last-key-wins JSON map construction (actual host parser admits the duplicate);
- parsing an out-of-domain integer without a Mneme bound (actual host parser admits 2^53);
- eager binary64 conversion before a later structural failure (actual host number overflow);
- a permissive host timestamp grammar accepting a space separator (actual chrono parser);
- pretty JSON or uppercase hash output (runner baseline passes, wrong observations fail);
- lexical editions, case-folded IDs, operation character-count limits, raw revision text equality,
  overwrite-before-comparison and line-ending-normalized hashing.

Runner controls also reject malformed YAML, ambiguous plain scalars, explicit tags, even unused
anchors, aliases, duplicates, non-string keys, multiple documents, unknown operations and missing
arguments. They prove recursive placeholder handling and a passing observation baseline.

## Reproduction and ownership

From the Rust crate directory, source the project environment first, then run the gate commands
above with the pinned toolchain. `README.md` documents the public binding and offline gate setup.
Local scripts `.tmp/work/codex/wp01-rust-windows.ps1` and `wp01-rust-linux.sh gate` record the
actual platform invocation. The completed record and code are frozen before the final exact-pair
gate replay; the hand-off reports their committed SHAs.

OWN-001: Windows Cargo home is `.tmp/cache/cargo-home`; Windows target is
`.tmp/cache/cargo-target/wp01-rust-windows`. POSIX Cargo/Rustup homes are
`.tmp/cache/cargo-home-linux` and `.tmp/cache/rustup-linux`; target is
`.tmp/cache/cargo-target/wp01-rust-linux`. Linux toolchain installation used `--no-modify-path`.
Process tooling uses the project-local managed CPython 3.12.8 environment. All scratch files,
dependencies, caches and build outputs remain inside the project on E:. No remotes or pushes.

**New contract findings:** none. The statically enforced Rust binding and constructor signatures
are implementation choices described above for independent challenge. No open contract choice
was filled by consulting Python or silently guessing a semantic rule.

This candidate implements Layer 01 only. Store-wide uniqueness, durable retry, operation commit
and per-profile semantic projections remain with their owning later layers. State and registry
updates and acceptance remain with Claude/Owner under the recorded workflow.
