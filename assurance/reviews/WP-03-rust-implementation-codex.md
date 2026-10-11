# Rust Layer 03 implementation — Codex (WP-03)

**Status: candidate ready for Claude's CLOSURE_REVIEW.**

Date: 2026-10-11. This is implementation-owner evidence, not independent approval,
acceptance or certification.

## Exact candidate and authority

- Code `wp03/rust`: `e9a94f78c8d1a44281bab1902f0c5af76d0deb9c`.
- Docs `wp03/rust`: the commit carrying this record; exact SHA supplied in the loop-back.
- Accepted code base: `dd55fb4f0abec262d7ba0dab64f28a74840b84c3`.
- Accepted normative docs: `c36e0f5cb6dc2e7e92327bb9db358af0cdd31995`.
- Handoff/control: `26ed4102` on `wp03/contract`.

Both implementation branches were created from the accepted mains. The docs branch
subsequently fast-forwarded to the supplied control commit, retaining Claude's
already-authored acceptance, registry and RUST_IMPLEMENTATION records. The accepted
main carried an obsolete candidate-state binding: the initial process check was
7/8 because the referenced descendant chain now included remediation content.
Using the supplied current control resolves that documentary mismatch. Codex authored
no state, registry, contract, plan or finding-register edits; the docs addition is
this record alone.

Authority: HIST-006/007 and PROJ-001/002 in `spec/core.md`, the SER-008 stage table,
Owner G-066..G-075, `assurance/layers/03-feasibility-matrix.md`, and the unchanged
two ACTIVE projection scenarios (54 steps). Expectations were derived from the
accepted text and corpus. Python was used only to drive Cargo/process checks and
scratch mutation orchestration, never as the implementation or result oracle.

## Implementation

`project_history(reader: Input<'_>, stream: Input<'_>, relations: Input<'_>) ->
Result<Value, Error>` is exported from the Rust crate. `src/projection.rs` owns the
projector and its shared lineage validation/resolution logic. The existing Native,
Text and Bytes binding and flat-arena value domain are retained.

Evaluation follows the agreed order:

1. Generic validation across all three arguments precedes typed rules.
2. Reader validation, closed stream shape/strictly increasing positive positions,
   then early lineage shape checks run before entry admission. External targets
   require exactly the immutable versioned identity or lower-case SHA-256 form;
   artifact targets are allowed only on `derived_from`.
3. Entries use the existing Layer 02 admission gates. Unknown required records fail
   atomically with the complete validated routing triple in the detail, store
   position and no argument name. The Layer 02 public admission diagnostic remains
   unchanged.
4. Repeated record IDs compare complete canonical normalized envelopes: identical
   repeats coalesce at their first position; conflicting repeats fail at the later
   position. Every physical entry advances the boundary, including skipped,
   excluded and repeated entries.
5. Late graph checks require available sources and resolution endpoints, reject
   self-links, and check cycles iteratively in the resolution and derivation families
   separately. No extra combined-family cycle rule is imposed. Unavailable record
   and typed external derivation targets remain unresolved; equal normalized
   relations collapse.
6. Resolution returns all unsuperseded/uncorrected records, with direct-only
   interpretation membership. There is no time, identifier or container tie-break.
   Presentation uses the specified first-position and relation/target ordering,
   including numeric artifact editions. The closed nine-field result is returned
   only after every check succeeds.

The additive `Error.position: Option<i128>` is independent of JSON byte offsets.
New error codes are `history.stream_invalid`, `lineage.invalid` and
`history.duplicate_record_id`. Existing constructors leave position absent.
Only the visibility of reused Layer 02 helpers changes, not their rule bodies.
An iterative detached-subtree copy in `values.rs` retains only reachable arena
nodes per envelope, avoiding copying the entire stream for each record.

The conformance runner adds one thin projector call and observes position. Rust
`IMPLEMENTED_LAYER` is now 3. The four relevant manifest requirements point to
`minion-memory-rust/src/projection.rs`. No Python, scenario, expectation, dependency
or lock-file change was made. Durable append, selection policy, payload decoding,
artifact lookup and pagination remain outside this layer.

## Executed controls and gates

The Windows and case-sensitive POSIX runs use Rust/Cargo 1.97.1 and the locked
dependency graph. Both execute formatting, strict all-target clippy, the complete
test suite, and documentation with warnings denied. Both pass:

- 41 integration tests and one doctest;
- 17 ACTIVE scenarios, 343 steps and five explicit placeholder xfails;
- all 54 Layer 03 scenario steps active, with no Layer 03 xfails.

No Rust numerical coverage percentage is claimed. The nine new Layer 03 tests
exercise the public API and include independently derived controls:

| Control | Executed extent / oracle |
|---|---|
| Native/Text/Bytes parity | 54 canonical steps × 27 three-argument seam combinations = 1,458 observations |
| Early shape versus late graph | 11 early and four late relation failures × three entry failures × 27 seams = 1,215 paired controls |
| Required-record diagnostic | Three profiles × unknown type/schema × 27 seams = 162 complete routing/position observations; Layer 02 diagnostic regressions also checked |
| Global staging and shape order | Later stage-1 failures beat earlier typed/stage-2 failures; reader/stream/lineage precedence; byte offset remains distinct from store position |
| Complete canonical repeats | Timestamp spelling/offset, normalized numbers, Unicode keys, payload/provenance conflicts and boolean-versus-number distinction |
| Typed targets and presentation | Available/unavailable records, versioned editions 2/10, hashes, duplicate normalization and rotated input; reverse-lexical IDs verify store order |
| Independent graph oracle | All 15,625 directed three-record graphs; transitive closure independently determines separate-family cycles, current sets and direct membership |
| Iterative ownership/depth | A 20,000-level payload and 3,000-record chain; caller bytes retained unchanged |

The POSIX suite is extracted from the exact committed code SHA onto a project-local
ext4/FUSE filesystem. Distinct `A` and `a` files establish case sensitivity. Linux
uses the project-local Rust homes and target. No checkout outside the project is used.

## Mutation assurance and execution corrections

Eighteen isolated, deliberately nonconforming variants are each killed by a named
runtime assertion, with a passing baseline before and after the replay. Compilation
errors are not credited as kills.

| ID | Planted violation |
|---|---|
| M01 | Select one current head |
| M02 | Ignore an unknown required record |
| M03 | Reject identical repeated IDs |
| M04 | Coalesce conflicting repeated IDs |
| M05 | Reject unresolved derivations |
| M06 | Inherit interpretation membership through replacement |
| M07 | Omit reinterpretation cycle edges |
| M08 | Allow derivation cycles |
| M09 | Reject equal normalized relation triples |
| M10 | Delay an invalid resolution artifact target until late graph validation |
| M11 | Drop entry error position |
| M12 | Sort records by identifier rather than store position |
| M13 | Omit the routing profile from required-record detail |
| M14 | Keep superseded interpretations current |
| M15 | Reject a cycle spanning the two otherwise-acyclic families |
| M16 | Admit an upper-case content hash |
| M17 | Admit stream entry position zero |
| M18 | Admit unknown relation members |

The first scratch baseline lacked its corpus copy; that setup failure was corrected
and not counted. A later shared-target gate reused the final mutant artifact despite
unchanged production source. That failed run is not credited as candidate evidence.
Final Windows, Linux and mutation evidence uses separate project-local Cargo targets;
the shared Windows target is also rebuilt from the production source and its complete
positive suite passes. An offline attempt using the obsolete root environment could
not resolve `yaml-rust2`; sourcing the current accepted environment supplies the
correct project-local Cargo home. That attempt is likewise not credited.

Reproduction drivers and logs are under `.tmp/work/codex/`:

- `wp03-rust-windows.py`; `wp03-rust/windows-gates.log` and `.json`;
- `wp03-rust-linux.sh`; `wp03-rust/linux-gates.log` (exact SHA and case-sensitive pass marker);
- `wp03-rust-mutants.py`; `wp03-rust/mutants/summary.json`, individual logs and `restored-baseline.log`;
- `wp03-rust/shared-target-restored.log`.

Final targets are `.tmp/cache/cargo-target/wp03-rust-windows`,
`wp03-rust-linux` and `wp03-rust-mutants`. Temp files, environments, mount images,
Cargo homes and build products remain project-local under OWN-001.

## Handoff

The complete process check with deep source verification passes 8/8 on the candidate
worktrees. No contract gap or new finding was identified. This candidate awaits
Claude's independent CLOSURE_REVIEW; no Rust approval or acceptance is asserted here.
