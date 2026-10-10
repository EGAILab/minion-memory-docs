# WP-01 — Rust Layer 01 CLOSURE_REVIEW (Claude)

**Verdict: CHANGES_REQUIRED.** One finding, WP01-CR-011. It is a shared-corpus gap owned by Claude;
no Rust implementation defect was found.

**Exact reviewed pair:**
- code `b07f33752fbc19b02c8de00e9ebbaa75d0a2f8ea` (`wp01/rust`);
- docs `97ab81bfa80377a16124e6d1aba3d6de531fd6b3` (`wp01/rust`), with state on
  `wp01/rust-state` at `01b51aca`.

**Author:** Codex. **Reviewer:** Claude, who did not author any Rust code (agent-workflow §3, step 11).
**Authority:** the accepted contract at docs `main` `83c66c25` (CORE-001/002/003/011/012, HIST-004,
SER-008/009, G-012…G-043) and the canonical corpus at code `main` `bac6594e`.

Python was not used as an oracle. Where the Python implementation appears below, it only generated
disagreements to adjudicate, and every expectation was taken from the contract text. None arose.

Codex's record `assurance/reviews/WP-01-rust-implementation-codex.md` was treated as claims to
reproduce, not as evidence.

## Executions (all project-local, OWN-001)

| Check | Result |
|---|---|
| Rust gates, Windows (rustc 1.97.1, separate target dir, clean detached checkout of `b07f3375`) | `cargo fmt --check` OK; `clippy --all-targets -D warnings` OK; `cargo test --locked --offline`: 16 integration tests and 1 doctest pass; `cargo doc -D warnings` OK |
| Rust gates, Linux (WSL Ubuntu, rustc 1.97.1, the same clean checkout) | fmt OK, clippy OK, 16 + 1 pass |
| Canonical corpus through the Rust runner | 8 ACTIVE / 146 steps / 5 explicit xfails |
| `mneme-process check --deep-sources` (code `b07f3375`, docs state `01b51aca`) | 8/8 |
| Python canonical runner at the candidate (G2: shared manifest changed; run by the Python owner) | 354 passed, 5 xfailed. Python and conformance are unchanged in the delta. |
| Differential probe at the JSON-bytes seam: 5 seeds, **187,236** generated cases; every public primitive, including mutated and invalid-UTF-8 JSON | **0** disagreements. Every error code and every success class was exercised. |
| Timestamps against an independent HIST-004 oracle (grammar regex plus ordinal-day/µs arithmetic, no datetime library): 20,000 inputs, 18,079 valid | **0** mismatches |
| Revisions against a G-021/G-035 oracle: 5,000 pairs covering identical / distinct / not_applicable / conflict | **0** mismatches |
| Operation-identity pairs: 5,000, exact pair equality, including NFC/NFD and byte-length cases | **0** mismatches |
| Native-seam assertions taken from SER-008/009: 40 checks | all pass |

The 40 native checks cover:
- NaN/±∞; −0 and integral floats becoming integers; the safe bound for native `i128` and `f64`; 1e21.
- Native duplicates outranking stage 2. Stage precedence across arguments: a later argument's
  stage-1 error beats an earlier argument's stage-2 error, and stage 2 beats an earlier argument's
  stage 3.
- No argument name on single-argument primitives.
- G-034 canonical first error regardless of insertion order; UTF-16 member order (`😀` before `｡`).
- RFC 8785 escapes; mixed Native/Text/Bytes seams.
- Native revision identical / conflict / not_applicable / shape / typed order.
- Raw hash of bytes as given.
- Invalid UTF-8 in source order: an earlier duplicate or surrogate wins, otherwise `value.invalid_json`.
- BOM rejection; 20,000-deep native nesting.

Probe sources are in `.tmp/work/claude/`: `rust-probe/`, `rust_closure_diff.py`,
`rust_closure_targeted.py`, `rust_mutants.py`, plus the results under `rust-closure/`.

## Reading against the contract

- **Staged decoder (SER-008, G-031/G-034).** The parser keeps numerals as text through stage 1 and
  detects duplicates after escape decoding, at the second occurrence. A surrogate escape is lone
  unless immediately followed by a low `\u` escape. Invalid UTF-8 is located at its byte offset, so
  an earlier violation in the valid prefix wins: this is the "first violation in source order" rule
  applied to the stage table's "not UTF-8" row. Stage 2 parses each numeral as the nearest binary64,
  which Rust's `f64::from_str` provides with correct rounding: overflow gives ∞, then
  `value.number_not_finite`; underflow gives 0. Stage 2 traverses in canonical order. Both checked
  against the witness `{"a":1e400,"b":1,"b":2}`.
- **Stages across arguments (G-031).** `validate_arguments` runs stage 1 over all arguments, then
  stage 2 over all; typed rules follow in declared order (`a`, then `b`).
- **Native binding (G-036–G-043).** Rust's typed arena makes non-string keys, cycles and host
  objects unconstructible. Duplicates are retained until native stage 1. Natural ordered types bind
  to one array kind. This is an acceptable representation (no observable outcome is lost); the
  vocabulary entries `value.unsupported_type` / `value.cyclic` are simply unreachable.
- **Serialization (SER-009).** UTF-16 ordering; lowercase `\u00xx` escapes for C0 controls only;
  ECMAScript shortest numbers via the pinned `ryu-js` (512 Node-generated vectors plus my
  differential); SHA-256 lowercase hex. `serde_jcs` is not used.
- **Typed rules.**
  - **CORE-001.** The ID grammar and device basename match, including the suffix form.
  - **CORE-002.** Editions are positive integers after normalization.
  - **CORE-012.** Namespace errors map to `operation_identity.invalid`; the operation ID's length is
    measured in UTF-8 bytes.
  - **CORE-003 (G-035).** Shape, then `artifact_version`, then `stable_id`. Both records are
    validated before `not_applicable`. Projections are compared as canonical bytes.
  - **HIST-004.** The full grammar is checked before chrono is called, with local and UTC ranges.
- **Runner thinness.** It only constructs inputs and calls public functions. Unknown or missing
  operations fail, and the five placeholders are explicit xfails.
- **Manifest.** Exactly the eight Rust locations were added.

## Discrimination check (planted contract violations)

16 single-point violations were planted in a scratch copy of the crate and the candidate suite run
on each. **14 were killed**: code-point ordering; no duplicate detection; eager numerals; per-argument
stages; no UTC range; extra revision member; trailing dot; character-count operation-ID length;
uppercase escape; safe-bound off-by-one; unbounded native integer; id-before-version order;
standalone-only device names; offset hour 24.

The 2 survivors:
- **M05: `:60` allowed by the grammar check.** An **equivalent mutant**: chrono's
  `and_hms_micro_opt` independently rejects second 60, so observable behaviour is unchanged. The
  corpus does contain `:60` witnesses.
- **M07: local year `0000` allowed.** **Not equivalent.** See WP01-CR-011.

## Finding

### WP01-CR-011: the canonical corpus has no witness for G-029's local-time lower bound

- **Classification:** `CONTRACT_ASSURANCE_DEFECT` (conformance incomplete). **Severity:** low.
- **Blocking:** WP-01 certification and closure (agent-workflow §8). It does not block the Rust
  implementation, which behaves correctly.
- **Owner decision required:** no; this is path A, applying the decided G-029. **Owner of repair:**
  Claude, as corpus and contract owner. **Status:** OPEN.
- **Authority:** HIST-004 "Range (G-029)": both the parsed local civil date-time and the normalized
  UTC instant must lie within `0001-01-01T00:00:00` … `9999-12-31T23:59:59.999999`.
- **Evidence.** Removing the local-year check (`time.rs`) leaves the whole Rust suite green. The
  only year-0000 witnesses are in `timestamp-seam-normalization.yaml` and `tests/layer01.rs`, and
  both use `0000-01-01T00:00:00Z`, which the UTC check also rejects.
  - The discriminating input `0000-12-31T23:30:00-01:00` has local year 0000 but a UTC instant in
    0001-01-01. It appears nowhere in the corpus, the Rust tests or the Python tests.
  - The correct result, `timestamp.invalid`, is produced by both implementations today.
- **Required repair.** Add `0000-12-31T23:30:00-01:00` → `timestamp.invalid` to the ACTIVE
  `timestamp-seam-normalization` scenario, with the authority comment, and run it through both
  runners. The Rust code needs no change. Codex independently reviews the corpus delta; then this
  closure review is completed on the resulting exact pair.

No other finding. The Rust implementation is found conformant with the accepted contract in
everything executed above.
