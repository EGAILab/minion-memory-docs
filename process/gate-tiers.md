# Minion-Memory — Gate tiers (G0–G3)

**Status:** PROPOSED (WP-00), pending independent review.
**Adapted from:** Minion-Agent `process/gate-tiers.md` @ `8744bd0`. Pi-specific items (pinned-Pi
authority harnesses, pinned Node/ICU) are removed; Mneme's authority is the hashed source bundle.

Each tier includes everything below it. All gate runs follow OWN-001 (temp/caches on E:, source
`process/environment/project-environment.*` first).

## 1. Tiers

**G0 — development.** Focused tests for the changed code and direct callers; lint/type checks of
changed files (`ruff`, `mypy --strict`; `cargo check`/`clippy` on the affected crate); every new or
changed witness executed.

**G1 — affected semantic surface.** G0 plus every test module owning the touched requirement IDs;
discriminating witnesses for each closed finding; realistic negative controls (known-bad → FAIL,
candidate → PASS) killed by their intended witness, with the control runner proving its own
baseline first (agent-workflow §9); directly dependent regressions.

**G2 — canonical integration.** G1 plus the canonical scenarios of every touched requirement and
dependency, through real public seams; cross-layer regressions for consumed lower-layer seams;
shared-schema/manifest validation (`mneme-process check`); where a shared artifact changed, the
other language's canonical runner for the touched scenarios, run **by that language's owner** at
its next pass. Python never runs as Rust's oracle, nor Rust as Python's.

**G3 — certification evidence.** G2 plus the full language suite; the full applicable conformance;
`mneme-process check` (all checks); coverage floor (Python: 100% of the certified surface —
inherited from Minion-Agent, re-confirmed at WP-01); formatting; strict types (`mypy --strict`,
`clippy -D warnings`); the pinned toolchain (`plans/toolchain-proposal.md`).

G3 is author-run **candidate evidence** at the exact candidate SHA pair. It is not independent
review. Certification needs G3 evidence **and** an independent complete review of that exact pair.

## 2. Minimum tier per stage

| Stage | Minimum tier |
|---|---|
| Development commits inside an owner's pass | G0 |
| Scoping / process-only hand-off (e.g. WP-00) | `mneme-process check` all checks + tool test suite with negative controls + lint/type of tooling |
| Contract / convergence checkpoint evidence | G1 characterization + feasibility matrix |
| Ordinary REMEDIATION returned for targeted closure | G0 + G1 |
| Targeted convergence closure | G1 + relevant G2 |
| First IMPLEMENTATION_REVIEW (complete) | G3 |
| FINAL_CONTRACT_REVIEW (complete) | G3 |
| Accepting (merging) an approved candidate | G3 already recorded at the exact approved SHAs + independent approval |
| Rust CLOSURE_REVIEW (complete) | G3 (Rust) |
| Documentary/status-only change | G0 + `mneme-process check` |

## 3. Reporting

Every hand-off reports the tier actually run, at the exact SHAs, with fresh counts; required
escalations are one line (`GATE: G2 (escalated from G1) — reason: ...`). A reviewer may require a
higher tier with a concrete blast-radius reason ("the SHA changed" is not one). De-escalation below
the stage minimum is never permitted. Gate batches run sequentially on a host; a result produced
under concurrent load is re-run, never credited.
