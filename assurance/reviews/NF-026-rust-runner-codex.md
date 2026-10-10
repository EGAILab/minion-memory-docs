# NF-026 Rust corpus runner implementation - Codex

Date: 2026-10-11. Implementation owner: Codex.
Status: **READY FOR INDEPENDENT REVIEW**. NF-026 closure belongs to Claude's review.

## Candidate and scope

Code branch `wp02/rust-runner`, candidate
`f97530bb8324b14d5d0cd4e91862626b12da07a7`, based on accepted code main
`cc3c5d549a43f166bfa1d990d3363887d5e63774`.
This companion record is on docs branch `wp02/rust-runner`, based on docs main
`34c1b752d8d6d54a1181219eada48d07f792730f`.

The request is NF-026: conform the Rust runner to the shared DRAFT rule while keeping
later ACTIVE promotion observable. No public Rust library, dependencies, scenario
expectations, process state or registry were changed. The code commit changes only:

- `minion-memory-rust/tests/conformance.rs`;
- `conformance/README.md` (the agreed DRAFT paragraph);
- `minion-memory-rust/README.md` (runner behavior and inventory description).

## Resulting behavior

The runner still parses portable YAML and validates every scenario against the shared
JSON schema before status classification. A valid DRAFT reports an explicit xfail
reason naming its layer and the README Drafts rule, without executing its operations.
A DRAFT with a placeholder still receives the DRAFT reason. Existing placeholder and
retired handling is retained; ACTIVE placeholders remain errors.

ACTIVE scenarios dispatch through the existing thin public-API operation adapter and
compare every actual observation to the expected result. Unsupported operations,
wrong expectations and unequal step/result lengths fail. The fixed `(8, 146, 5)`
assertion is removed: inventory counts now derive from scenarios actually classified
and ACTIVE steps actually executed. The corpus must still exercise ACTIVE scenarios.
The README records the base inventory as an observation rather than a permanent limit.

`draft_rule_and_active_promotion` controls the status transition with both unknown and
known operations, checks wrong and corrected observations, a failing additional step,
length mismatch, retired handling and recursive placeholders. It checks that DRAFT
classification remains independent of operation support.

## Independent executions

Sourced the project environment in each shell, including the current companion docs
checkout for Cargo homes and the managed Python pin. All worktrees, scratch copies,
Cargo homes and targets remained under the project root. Rust 1.97.1 was used on
Windows and native WSL Ubuntu/Linux. The Linux checkout is on the E: mount; this is a
native POSIX run, not a claim of a case-sensitive filesystem run.

Both Windows and Linux passed these gates on the candidate:

```text
cargo fmt --check
cargo clippy --locked --offline --workspace --all-targets -- -D warnings
cargo test --locked --offline -- --nocapture
RUSTDOCFLAGS=-D warnings cargo doc --locked --offline --no-deps
```

PowerShell sets `RUSTDOCFLAGS` via its environment syntax for the last command.
Tests: 17 integration tests and 1 doctest passed on each platform. Base corpus:
8 ACTIVE scenarios, 146 executed steps and 5 explicit placeholder xfails.
The companion docs/code mechanical deep-source check passed 8/8.

A scratch corpus overlays the four actual WP-02 DRAFT scenarios from code
`15b71ca392384b447f4b2c0ca023a69538f977d8` (70 steps), and three actual WP-02S
DRAFT scenarios from `95d1df6022aac1e203e4b677652fb2a885d20185` (69 steps).
The old main runner fails this fixture on Windows because DRAFT is not ACTIVE.
The fixed runner passes all four conformance tests on Windows and Linux, reporting
8 ACTIVE / 146 steps / 12 explicit xfails. All seven new xfails name layer 02.

The following fixture mutations were also executed on both platforms:

| Control | Observation | Required outcome |
| --- | --- | --- |
| Promote the real scope shape scenario to ACTIVE | Unsupported `validate_scope`, step 0; exit 101 | Fail; promotion cannot hide missing implementation |
| Add a known-operation DRAFT with wrong expected output | Exit 0; 8 ACTIVE / 146 steps / 13 xfails | Xfail without evaluating the draft expectation |
| Promote that control with wrong output | Observed `less`, expected `greater`; exit 101 | Fail against the real public-API output |
| Correct its ACTIVE expectation | Exit 0; 9 ACTIVE / 147 steps / 12 xfails | Execute the added scenario and reflect promotion in counts |
| DRAFT missing required title | Shared-schema failure; exit 101 | Reject malformed corpus before DRAFT classification |

No mutation was made to a candidate corpus. Scratch fixture changes were restored.

## Reproduction and evidence limits

Project-local scratch recipes:

- `.tmp/work/codex/nf026-fixture.py`: fixture construction;
- `.tmp/work/codex/nf026-scenario.py`: real-scenario promotion and synthetic controls;
- `.tmp/work/codex/nf026-windows-controls.ps1`: Windows controls;
- `.tmp/work/codex/nf026-linux.sh`: Linux base gates;
- `.tmp/work/codex/nf026-linux-fixture.sh`: Linux fixture and five controls.

Two preliminary fixture attempts reused stale build artifacts and are excluded from
success evidence: a Windows copied source retained its old modification time, and
Linux initially shared a target directory with a checkout whose compiled
`CARGO_MANIFEST_DIR` pointed to the base corpus. Windows was rebuilt after refreshing
the copied source timestamp. Linux was rebuilt in the dedicated project-local target
`.tmp/cache/cargo-target/nf026-fixture-linux`; its output explicitly names the fixture
crate and demonstrates all seven DRAFT scenarios and all five controls above.

This is a runner-policy fix, not an implementation of Layer 02 or a contract approval.
The separate WP-02S review remains CHANGES_REQUIRED. No acceptance onto main, finding
closure, state transition or registry update is asserted by this implementation record.
