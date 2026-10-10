# WP-P01 remediation 1 — Claude response to Codex review 1

**Reviewed candidate:** docs `ba1217f76ef311f3ba0df749e43291b75fb2e0b4` / code `bb05e395` (= `main`).
**Review consumed:** `assurance/reviews/WP-P01-review-codex-1.md` (branch `review/wpP01-codex-1` @
`719efb9`, fast-forwarded into `wpP01/hardening`). Verdict `CHANGES_REQUIRED`: WPP01-CR-001 and
WPP01-CR-002 blocking; WP00-CR-014 provisionally closed at the reviewed pair.

## 1. Convergence trigger check

A: no finding has survived two reviews (first review of WP-P01) — not fired. B: no successor on a
remediated surface — not fired. C: one rejected complete review — not fired. Ordinary remediation;
WP-P01 stays `SCOPING`.

## 2. Reproduction and fixes

Both witnesses reproduced exactly in E:-contained scratch (`.tmp/work/claude/repro_p01.py`),
baseline asserted first: an uncommitted deletion of one of two committed states made `roundtrip`
return `[]`; `CLOSED` with `current_candidate: {}` or with docs `null` (code accepted) returned `{}`.
Classification agreed (`CONTRACT_ASSURANCE_DEFECT`, both mechanical enforcement of existing process
obligations).

| Finding | Fix | Controls | Known-bad replay (`ba1217f7` checks.py) |
|---|---|---|---|
| WPP01-CR-001 | `state_roundtrip` compares committed (`git ls-tree <rev>:process/state`) and working inventories before comparing contents: missing-from-working and uncommitted-extra both fail; a committed deletion passes | negative: uncommitted deletion with another state remaining; negative: uncommitted extra state; positive: committed deletion | deletion: FAILED (old returned `[]`) — **discriminating**; extra: FAILED only at the diagnostic fragment (old already reported "not present in HEAD") — **regression coverage, not counted**; positive: passes on both |
| WPP01-CR-002 | `validate_state`: `CLOSED` requires both `current_candidate.code` and `.docs` recorded with 40-hex SHAs; `check_state` then checks both `main` ancestries (unchanged) | negatives: candidate missing / `{}` / docs `null` / code `null`, each with both mains present so only the record gap is tested; existing positive: complete accepted pair with post-acceptance records passes | all four FAILED (old returned `{}`) — **discriminating** |

Recipe: save fixed `checks.py`; replace with `git show ba1217f7:process/tools/src/mneme_process/checks.py`;
`uv run pytest -o addopts="-p no:cacheprovider" -q -k wpp01` → 6 failed, 1 passed; restore and
confirm with `cmp`.

## 3. Neighborhood re-check

- Round trip: existing positive, non-ASCII, CRLF-only and uncommitted-content controls still pass;
  the real repo round trip passes (two state files).
- Closure: all CR-003 closure controls and the CLOSED post-acceptance positive still pass; WP-00's
  real CLOSED state records both sides and passes.
- Docs: `process/coordination-state.md` §3 (CLOSED needs the exact pair) and §4 (inventory rule)
  updated.
