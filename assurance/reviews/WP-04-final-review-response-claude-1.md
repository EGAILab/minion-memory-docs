# WP-04 final review — Claude's response 1

**Review consumed:** `assurance/reviews/WP-04-final-review-codex.md` (`review/wp04-final`
`eec44b3d`, fast-forwarded into `wp04/contract`). The verdict is `CHANGES_REQUIRED` on
**WP04-CR-016** (a documentary defect). WP04-CR-015 is resolved and CE-04-01 stays settled.

**Code is unchanged at `9d5a2d51`.** The repair is docs only.

## Trigger check

No convergence trigger fires.
- CR-016 is a documentary assurance-index defect with no semantic content (Case A narrow, adopted
  §11.8.8).
- No finding has failed twice.

The route follows the WP-03 precedent (WP03-CR-007):
- `FINAL_CONTRACT_REVIEW` → `REMEDIATION` → `IMPLEMENTATION_REVIEW`, with a targeted final re-review
  of CR-016.

## Repairs, one per discrepancy

| CR-016 item | Repair |
|---|---|
| 1. The plan's status, governance and matrix row were stale | **`plans/WP-04.md`:** <ul><li>The status line now gives the current state, code `9d5a2d51`, and governance through G-098.</li><li>The matrix row describes the matrix as the current index.</li><li>The test row cites [CT] and [CW] as executed at `9d5a2d51` (run 5), with [IT] due at the Rust candidate.</li><li>A new row records the final review and this repair.</li></ul> |
| 2. The matrix carried stale premises and lacked the catalog surface | **`assurance/layers/04-feasibility-matrix.md`** is rewritten as one current index: <ul><li>**Header:** governance through G-098, the current pair and the run-5 evidence. A labelled **History** paragraph holds the superseded stages: `63462513`, `d857fcc2`, the 20 tests, P01–P20/23, and the "10 damaged shapes" check.</li><li>**Evidence keys:** current counts (40 store tests, 315 catalog witnesses with the [P]/[T]/[E]/[Pr]/[F]/[INV]/[PIN] breakdown, and 59 + 18 planted violations).</li><li>**§1:** a value row for the shared pins. **§2:** a capability row for catalog validation.</li><li>**§3:** H2, H3 and H8 rows updated.</li><li>**New §3a:** the settled catalog surface. Each row gives exact spec and checkpoint anchors, the current Python witnesses by kind, and the Rust obligation. It covers the open order, environment, genuine objects, initialization, structured parts, cached values against E004, G-098 fields, `index_columns`, whole-row members with exclusions, normalizations and the inventory, the dependency island and labels, the exemptions, and the trust scope.</li><li>**§4:** open-order rows, and P01's barrier witness.</li><li>**§5:** the CE-04-01 neighborhoods (characterization, extension, gate run 3), with the bounded P38 and P14 conclusions as Codex scoped them.</li><li>**§6:** the verdict names every Rust requirement. [IT] is marked due, not executed.</li></ul> |
| 3. NF-016 and NF-026 were OPEN on this line, and PERS-008's note was obsolete | <ul><li>**The recorded post-acceptance commit `3ba0607c`** (WP-02: NF-016 and NF-026 CLOSED with their resolutions, and Codex's final re-review record) is **cherry-picked** with `-x` provenance. The `plans/WP-02.md` conflict was resolved by keeping the current CLOSED/certified status line and inserting the post-acceptance history rows in date order. No disposition or semantics changed.</li><li>**PERS-008's note** now records that NF-016 is resolved: HistoryBoundary is a store-local cursor (HIST-005; G-047, G-051, G-054), and Layer 04 realizes it as the gapless position. No new semantics.</li></ul> |

## Not changed

- The contract semantics.
- The CE-04-01 classification and evidence.
- Production code, pins and tests.
