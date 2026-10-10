# NF-026 Rust corpus runner implementation - Codex

Date: 2026-10-11. Implementation owner: Codex.
Status: **READY FOR INDEPENDENT REVIEW**. NF-026 closure belongs to Claude's review.

## Revised candidate and base

Code branch `wp02/rust-runner`, candidate
`b9f42d4227093cb3b9144e2d8ca2b068c8cb5876`, based on the Python implementation candidate
`1d7167c85d4516dea6903ada6745139c3ac222f3` on `wp02/contract`.
This supersedes the initially notified `f97530bb` candidate from main: the branch was
rebased to the requested Python candidate, then the Implemented layers rule was added.
The base's shared README text, four ACTIVE history scenarios and Python changes are
preserved unchanged. The base is not approved by this runner implementation record.

Companion docs branch: `wp02/rust-runner`, based on accepted docs main
`34c1b752d8d6d54a1181219eada48d07f792730f`. Only this record changes on that docs branch.
The cumulative code diff against the new base changes exactly two files:

- `minion-memory-rust/tests/conformance.rs`;
- `minion-memory-rust/README.md`.

No public Rust library, dependencies, canonical scenario contents, process state or
registry were changed. The shared README is exactly the version read at `1d7167c8`.

## Behavior

The runner declares `const IMPLEMENTED_LAYER: u8 = 1`. It moves only with the Rust
implementation candidate for a later layer. Schema validation precedes classification.
Every DRAFT reports an explicit xfail reason naming its layer and the README Drafts
rule; it never dispatches an operation. DRAFT with a placeholder gets the DRAFT reason.
An ACTIVE scenario above the declaration reports xfail naming its layer, Rust, the
implemented layer and the README Implemented layers rule. It never executes as evidence.
ACTIVE placeholders still fail before the layer gate, as required by the corpus rule.
Existing placeholder and retired behavior is retained.

At or below the declaration, every ACTIVE step calls the real library through the
unchanged thin operation adapter. Unsupported operations, wrong observations and
unequal step/expectation lengths fail. Inventory counts derive from scenarios actually
classified and steps actually executed, rather than the old `(8, 146, 5)` assertion;
the corpus must still exercise ACTIVE scenarios. The printed ACTIVE count means
executed ACTIVE scenarios; above-layer ACTIVE scenarios are counted as explicit xfails.

The previous DRAFT/promotion controls now use Layer 01 for eligible ACTIVE transitions.
The additional `implemented_layer_and_promotion` control asserts the production
Layer 01 declaration, the exact Layer 02/Rust reason, xfail for known and unknown
above-layer operations, and execution at layers 00/01. It exercises the identical
classification function with an implementation limit of 2: unsupported operations and
wrong results fail, while a corrected known-operation expectation executes one step.
An invalid layer and an above-layer ACTIVE placeholder fail rather than being hidden.

## Executed gates on this candidate

Both Windows and native WSL Ubuntu/Linux passed:

```text
cargo fmt --check
cargo clippy --locked --offline --workspace --all-targets -- -D warnings
cargo test --locked --offline -- --nocapture
RUSTDOCFLAGS=-D warnings cargo doc --locked --offline --no-deps
```

PowerShell uses environment-variable syntax for `RUSTDOCFLAGS`. Rust 1.97.1;
18 integration tests and 1 doctest passed on each platform. Both actual corpus runs
reported 8 executed ACTIVE scenarios / 146 executed steps / 9 explicit xfails:
5 existing placeholders plus all 4 promoted Layer 02 history scenarios. Each of the
four reasons literally names layer 02, Rust, implemented layer 01 and the rule.
The new promotion controls passed on both platforms. Native Linux ran on the E: mount;
this does not claim a case-sensitive checkout.

Every shell sourced the project environment; the current companion environment sets
Cargo homes and the managed Python pin. All caches, targets, worktrees and scratch
files remain project-local. No acceptance, finding closure or registry transition is
asserted by this author's implementation record.

## Prior DRAFT evidence and reproduction

Before the addendum, the original main-based candidate passed Windows/Linux gates,
the 8/146/5 base corpus, and a scratch overlay of all seven actual WP-02/WP-02S DRAFT
scenarios (8/146/12). The old runner failed that fixture on Windows. Synthetic wrong
DRAFT expectations remained xfail; their ACTIVE promotion exposed wrong results;
corrected ACTIVE promotion executed an extra scenario/step; malformed DRAFT envelopes
failed schema validation. Those are historical DRAFT evidence, not assertions that
Layer 02 ACTIVE operations should execute under the revised Layer 01 declaration.

Scratch recipes under `.tmp/work/codex/`: `nf026-fixture.py`, `nf026-scenario.py`,
`nf026-windows-controls.ps1`, `nf026-linux-fixture.sh` (prior DRAFT experiments), and
`nf026-addendum-linux.sh` (current candidate Linux gates). The original 8/8 mechanical
check predates this revised base and is not claimed as re-executed against the Python
implementation candidate. The Python implementation remains a separate review.

Preliminary fixture runs with stale artifacts were excluded: on Windows a copied source
retained its timestamp; on Linux a shared target reused a binary whose compiled
`CARGO_MANIFEST_DIR` named the base checkout. Valid historical evidence followed a
Windows timestamp refresh and a dedicated project-local Linux fixture target. Current
candidate runs explicitly name `review-worktrees/code-wp02-rust-runner` and report all
four real ACTIVE Layer 02 xfails. No candidate corpus was mutated for testing.
