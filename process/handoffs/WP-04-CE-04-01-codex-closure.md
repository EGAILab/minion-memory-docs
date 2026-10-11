# Hand-off — WP-04 CE-04-01 implementation closure review (Codex)

**From:** Claude (coordinator, Python owner). **To:** Codex (independent closure review).
**Governs:**
- G-088…G-093;
- the agreed checkpoint `assurance/convergence/CE-04-01-classification.md` rev. 2 (your
  `APPROVED`, `bfb6cad3`).

## What to review

The exact pair:
- **code:** `be36323f56e61d87776d11c831ae1ef0573ea692` on `wp04/contract`;
- **docs:** the state head carrying this hand-off.

`be36323f` is a tests-only commit over the single implementation pass `b657081b`.

Claude's record is `assurance/reviews/WP-04-CE-04-01-implementation-claude.md`. It reports:
- **gate run 1** at `b657081b`, which failed G4;
- the diagnostic of its survivors;
- **gate run 2** at `be36323f`.

The logs are in `.tmp/work/claude/ce0401-gates/` (run 1) and `ce0401-gates-be36323f/` (run 2).

## Asked

An independent verdict, from the checkpoint, the contract and your own executions, not from
Claude's record:
- **Every classified row.** Does each one behave as classified at `be36323f`? Is each evidence kind
  reported correctly: public, transaction control, direct engine control, or predicate? Predicate
  evidence must never count as a public execution.
- **The equivalence claims.** Do they hold?
  - P32 and P40 were predicted before any run.
  - P38 was claimed only after run 1. The argument is that a foreign key from outside always puts
    in-scope internal RI triggers on the referenced `mneme_` table. Look for a constructible
    counterexample.
- **The remediation.** Is a tests-only remediation after a failed gate run acceptable under the
  checkpoint's "implement once"? Are the six re-pointed intended witnesses legitimate, or do any
  of them amount to choosing the witness after seeing the result?
- **What the gates missed.** Is anything wrong or missing?

Mark anything that needs an Owner choice as a candidate path-C item, never as a choice.

## Constraints

- No production edits.
- The host is clear (Minion-Agent, 2026-10-12). Minion-Agent will ask before any new reservation.

## Deliverable

- `assurance/reviews/WP-04-CE-04-01-closure-codex.md` on a new branch `review/wp04-ce1-closure`,
  from the docs state head.
- When finished, notify Claude at w6:p1.
