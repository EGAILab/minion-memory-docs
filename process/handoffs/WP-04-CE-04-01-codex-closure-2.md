# Hand-off — WP-04 CE-04-01 targeted closure review 2 (Codex)

**From:** Claude (coordinator, Python owner). **To:** Codex (independent targeted closure review,
adopted §11.8.7).
**Governs:**
- the agreed checkpoint `assurance/convergence/CE-04-01-classification.md`, revisions 2–5 (your
  `APPROVED` `bfb6cad3` and `955d91f6`);
- G-088…G-098.

## What to review

The exact pair:
- **code:** `038416286631a34846f99bd53b7c4d6ed41d30cf` on `wp04/contract`;
- **docs:** the state head carrying this hand-off.

Claude's record is `assurance/reviews/WP-04-CE-04-01-implementation-claude-2.md`.
- It reports the pre-gate witness diagnostic (§4).
- It reports gate run 3 at `426f14f3`, which **failed G4** and is kept (§5.1).
- Run 4 at `03841628` is the submitted evidence (§5.2).

The logs are in `.tmp/work/claude/ce0401-gates-426f14f3/` and `ce0401-gates-03841628/`.

## Asked

An independent targeted verdict on WP04-CR-008, CR-012, CR-013 and CR-014, from the checkpoint and
your own executions:
- Does each classified row of §8–§10 behave as agreed at this candidate?
- Is each evidence kind reported truthfully ([P], [T], [E], [Pr], [F])?
- Does the whole-row member comparison, with its inventory test, hold on the live catalog?
- Is the island and boundary check complete for the routes you characterized?
- Are the re-pointed intended witnesses after run 3 legitimate? These are the single-part
  predicates, the [F] patched-row controls, and the P01 barrier.
- Does P38 still hold as an equivalent in your narrower scope?

Mark anything that needs an Owner choice as a candidate path-C item, never as a choice.

## Constraints

- No production edits.
- Use the project role only.
- Keep all scratch on E:.
- The host is clear.

## Deliverable

- `assurance/reviews/WP-04-CE-04-01-closure-codex-2.md` on a new branch
  `review/wp04-ce1-closure-2`, from the docs state head.
- When finished, notify Claude at w6:p1.
