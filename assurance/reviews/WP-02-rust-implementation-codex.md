# Rust Layer 02 implementation — Codex (WP-02 and WP-02S)

**Status: candidate ready for Claude's complete CLOSURE_REVIEW.**

Date: 2026-10-11. This is author-run G3 evidence, not independent approval or certification.

## Exact candidate and authority

- Code `wp02/rust`: **`a5506d0ddd98af33be4d9ec87305b10000febf4d`**.
- Docs `wp02/rust`: the commit carrying this record; its exact SHA is in the loop-back.
- Accepted code base: `609dad7b5158d8821e4fb860d0f1e3bd2529eb49`.
- Accepted normative docs: `36d02298d6c1f479e9b4ce370531fccdd88f6a58`.
- Docs branch also fast-forwards through Claude's supplied control commit `34ae5891`,
  containing the already-authored post-acceptance/state records. No state, registry,
  finding register, plan or contract was edited by Codex in this implementation.

Initial authority was the WP-02 Rust handoff at `7c2c3f59`. Claude's subsequent task
update requires both accepted Layer 02 surfaces because a Rust implemented-layer
ceiling of 2 must execute all seven ACTIVE Layer 02 scenarios. Branches were rebased
before implementation changes to the specified newly accepted mains.

Authority read and used:
- `spec/core.md`: HIST-001/002/005/010 and the certified HIST-004 rules.
- `spec/serialization.md`: SER-005/006, SER-008 stage ordering and G-055's gates.
- `spec/scope.md`: agreed MemoryScope value, vocabulary, matching and error rules.
- Verbatim Owner G-047..G-055 in `reference/governance/2026-10-11-owner-layer02-start.md`;
  G-056..G-064 in `reference/governance/2026-10-11-owner-wp02s-memoryscope.md`.
- The unchanged four ACTIVE history scenarios (70 steps) and three ACTIVE scope
  scenarios (73 steps), plus both Layer 02 feasibility matrices.

Rust behavior and test expectations derive from these contracts and corpus, not
Mneme Python outputs or copied Python implementation behavior. Python used below is
only a project-local process driver for Cargo and scratch mutation orchestration.

## Implementation and binding

| Contract | Public Rust seam | Implementation |
|---|---|---|
| HIST-002/010, SER-005/006 | `admit_history_record(reader, record)` | `minion-memory-rust/src/history.rs` |
| HIST-005 | `compare_history_boundaries(a, b)`, `history_boundaries_equal(a, b)` | same |
| SCOPE-001/002 | `validate_scope(scope)`, `scopes_equal(a, b)` | `minion-memory-rust/src/scope.rs` |
| SCOPE-003/004/006 | `scope_visible(record, query)`, `AGENT_FACETS` | same |

All functions take the existing explicit `Input::Native`, `Text` or `Bytes` seams and
run generic stages across every argument before typed rules. The flat-arena `Value`
binding still prevents cycles, non-string keys and host hooks; it introduces no
language-dependent scope or envelope value domain.

`HistoryAdmission` is an owned enum with `Decode(Value)`, `Skip` and `Excluded`.
Only `Decode` can carry the normalized envelope, so impossible outcome/envelope pairs
are not representable. Schema recognition is a private HashSet of exact token/edition
pairs, populated only with duplicate rejection after generic numeric normalization.
Iteration order of the set is never exposed.

Envelope admission implements four ordered gates:
1. Every record must have a valid complete routing triple, even when foreign-profile.
2. Foreign profiles terminate before compatibility. Same-profile records validate
   compatibility, then unknown schemas skip or stop replay before known shape checks.
3. Recognized same-profile envelopes require their closed member set.
4. Remaining typed fields are visited in canonical member order, never JSON source
   order. `occurred_at` precedes `record_id`, which precedes `recorded_at`.

Payload and provenance stay as whole normalized arena values; they are not interpreted,
filtered, summarized or assigned a core origin vocabulary. Only timestamp string nodes
are replaced with the certified HIST-004 canonical spelling. Absent timestamps remain
absent; no chronology constraint between occurred and recorded times is invented.
Only scalar token/timestamp fields are copied for typed validation, avoiding repeated
whole-payload clones for each field.

Boundaries are validated completely in a/b order before relation handling. Ordering
requires a common store and compares exact normalized positions; equality compares
the entire pair. Position zero is admitted. These are pure relations, not persistence,
record counts, global ordering, causal order or cross-store sequences.

Scope is a normalized `Value` retaining the exact closed two-state record. Internally
unresolved is distinct from an empty resolved map. G-064 name validation uses two
ASCII segments, each 1–128 bytes, and one dot, without applying device-name exclusions.
Values reuse CORE-001. Unknown stored names survive validation but hide records;
queries may name only the six fixed Agent facets. The query is validated before a
hidden-record return. Matching requires every record constraint to be explicitly
present with the same token; omission never becomes a wildcard or inferred hierarchy.

Added exactly seven contract error codes. Argument validation errors are named;
`history.unknown_required` and `history.boundary_incomparable` are unnamed relations.
Single-argument scope validation names none. Existing identity semantics are unchanged:
`id_rule` is now crate-visible; `timestamp_rule` is extracted behind the unchanged
public staged timestamp function so envelopes reuse the certified typed rule.

## Integration and traceability

The thin canonical runner adds six operation mappings. It constructs public inputs,
invokes the library and converts normalized returned values/enum variants to the
corpus's observable JSON. It contains no routing, shape, timestamp, boundary or scope
rules. Raw `record_json` reaches the library decoder unchanged.

`IMPLEMENTED_LAYER = 2` now executes **15 ACTIVE scenarios / 289 steps**, including
all seven Layer 02 scenarios. Five future placeholders remain explicit expected
failures. The declaration/promotion self-control tests still prove that unknown
eligible operations and wrong expectations fail, while above-layer ACTIVE scenarios
remain xfail with their layer and language. Inventory counts are derived, not pinned.

The manifest adds ten Rust locations: HIST-002/005/010, SER-005/006 and
SCOPE-001/002/003/004/006. HIST-001's vocabulary/derived-artifact obligations and
SCOPE-005's deferred Learning adoption are not misrepresented as implemented consumer
features. Their null locations remain unchanged. All canonical files and expectations,
Python files, dependency versions and Cargo.lock are unchanged.

## Executed G3 evidence

Pinned rustc/cargo **1.97.1**, rustc `8bab26f4f` (2026-07-14), on Windows
`x86_64-pc-windows-msvc` and POSIX `x86_64-unknown-linux-gnu` (Ubuntu/WSL).
Final gate batches were run sequentially against the committed code candidate.

| Gate | Windows | POSIX |
|---|---|---|
| `cargo fmt --check` | PASS | PASS |
| `cargo clippy --locked --offline --workspace --all-targets -- -D warnings` | PASS | PASS |
| `cargo test --locked --offline -- --nocapture` | 32 integration tests + 1 doctest pass | same |
| Canonical corpus | 15 ACTIVE, 289 steps, 5 explicit xfails | same |
| `RUSTDOCFLAGS=-D warnings cargo doc --locked --offline --no-deps` | PASS | PASS |
| Full `mneme-process check --deep-sources` | 8/8, checked against the candidate pair | shared tooling run on Windows |

The docs main snapshot retained an obsolete WP-02 review candidate pin and initially
failed the live state-descendant check (7/8). Fast-forwarding the docs implementation
branch to the already-supplied `34ae5891` control commit resolved it without edits to
Claude-owned state. The final all-checks result is 8/8.

Rust has no numerical coverage floor in `process/gate-tiers.md`; no measured Rust
coverage percentage is claimed. Existing Layer 01 tests all remain green. Every new
public operation is exercised through its library seam, not a replica in the runner.
Claude should run Python's canonical runner on the shared manifest candidate at the
next owner pass, as G2 requires; it was not used as a Rust oracle here.

## Discrimination and neighborhoods

`tests/layer02.rs` has fourteen public-seam control tests, including:
- complete routing validation before foreign exclusion; compatibility not consulted
  for other profiles; unknown schema termination before closed shape;
- closed reader/config entries and duplicate numeric aliases;
- shape-before-fields and all seven invalid masks of occurred_at/record_id/recorded_at,
  in six source/member permutations on native, text and byte seams (126 observations);
- generic failures in later arguments outranking earlier typed errors, including the
  deferred-number/later-duplicate witness;
- normalized timestamps, no imposed chronology, optional absence and payload/provenance
  preservation, including a **20,000-level** payload;
- zero, normalized numeric aliases and maximum cursor positions; same-store ordering,
  cross-store equality/incomparability and validation before relations;
- closed scope states, no global/unresolved alias, G-064 segment boundaries, device
  names versus token values, unknown preservation, malformed queries on hidden records;
- **46,656** six-facet visibility cases against an independently written map predicate,
  plus 729 map-order equality controls, without implicit facet hierarchy.

An isolated scratch Cargo crate first passed all fourteen control tests, then the
same tests killed **22/22** planted violations (12 history, 10 scope). Each counted
kill is a named runtime test failure; compilation/setup failures are not counted.
The registry-addition mutation initially could not compile against a fixed-array
assertion, so that assertion was changed to slices. The replay then compiled and
failed both the registry and unknown-query controls. The resume driver also refreshes
source timestamps before its baseline so Cargo cannot reuse a previous mutant build.

The planted violations are: foreign profiles as errors; premature exclusion; unknown
required skip; unknown ignorable shape checking; recognized-pair deduplication; open
recognized envelopes; reversed typed order; an imposed occurred/recorded chronology;
zero schema editions; cross-store ordering; equality ignoring store; rejecting cursor
zero; device restrictions on names; extra namespace dots; multi-valued facets; visible
unresolved scopes; accepting unknown queries; dropping unknown record constraints;
query-omission wildcard; unresolved extra fields; premature Learning registry; and
named single-argument scope errors. Each is killed by its intended semantic witness.

## Reproduction, limits and ownership

Code and docs worktrees are `review-worktrees/code-wp02-rust` and `docs-wp02-rust`.
Source the root project environment, then the current docs environment, in every shell.
Windows uses project-local Cargo home and target; WSL uses the project-local Linux
Cargo/Rustup homes and target. No toolchain installation or external Python repair was
performed. All scratch/cache/build files stay under Minion-Memory (OWN-001).

Local recipes/evidence:
- `.tmp/work/codex/wp02-rust-windows.py`: sequential Windows gates and toolchain probe.
- `.tmp/work/codex/wp02-rust-linux.sh`: POSIX gates (`MNEME_ROOT` set to the mounted root).
- `.tmp/work/codex/wp02-rust-mutants.py`: baseline plus 22 literal production mutations
  in an isolated crate; default invocation replays all, optional numeric argument resumes.
- `.tmp/work/codex/wp02-rust/`: platform gate logs, mutation baseline, individual kill
  logs and `mutations.json` with named witnesses.

**New contract findings: none.** No unresolved semantics were filled by a guess.
No capture, persistence, retrieval privacy consumer, Learning adoption or Layer 03+
feature is introduced. Independent review, acceptance, shared state/registry updates
and certification remain with Claude/Owner under the workflow.