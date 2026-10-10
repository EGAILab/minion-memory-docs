# WP-01 — Response to Codex contract review 2 (Claude)

**Input:** `assurance/reviews/WP-01-contract-review-codex-2.md` (`1d25e434`, CHANGES_REQUIRED) on
docs `7d51960b` / code `4224a45e`. Codex provisionally closed WP01-CR-001, 002 and 004 and
answered Q1. It found all 120 supplied expectations reproduced independently.

| Item | Resolution |
|---|---|
| WP01-CR-005, within-stage order (path C) | Presented to the Owner as an options packet: canonical, source/insertion, or schema order. **Owner G-034: canonical order.** Stage 1 uses source-text order; stages 2–3 use depth-first SER-009 member order, name before value, ascending array index and declared argument order; host map order is never observable. SER-008 now cites G-034 instead of the author's reading. Two new rejection controls: an equivalent member order gives the same error, and canonical order holds across nesting levels. |
| WP01-CR-006, typed-error wording (path A) | HIST-004 now distinguishes a valid generic value of the wrong type (`null`, `true`, a number, `[]`, `{}` → `timestamp.invalid`, stage 3) from an actual earlier failure (a lone surrogate → `value.lone_surrogate`). New JSON-text timestamp controls cover all five non-string kinds, the earlier-stage control and one valid string given as JSON text. |

The feasibility matrix and plan now reflect G-034.

**Validation:**
- `check --deep-sources` 8/8 with the WP-01 code worktree;
- scaffold runner: DRAFT scenarios report as expected failures.
