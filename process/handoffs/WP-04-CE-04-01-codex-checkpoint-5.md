# Hand-off — WP-04 CE-04-01 checkpoint re-review, revision 5 (Codex)

**From:** Claude (coordinator, Python owner). **To:** Codex (independent checkpoint review, targeted).
**Governs:**
- G-088…G-098 (G-098 is the Owner's answer to CE04-CP-004, recorded verbatim);
- your checkpoint review 4 (`76908bc8`): CP-004, CP-006 and CP-007 resolved, CP-005 open.

## What to review

On the docs state head:
- `assurance/convergence/CE-04-01-classification.md` **§10, revision 5**. It completes
  CE04-CP-005; §9 otherwise stands.
- `spec/persistence.md`, "Internal members are certified, not only discovered" (the last paragraph,
  the whole-row rule).

## Asked

A targeted, independent verdict on CE04-CP-005 at this exact revision:
- Do the whole-row comparison of every internal member, the named exclusion list and the
  catalog-inventory test close the member-shape gap?
  - This includes your projected `reloptions` and `indoption` controls.
  - It covers TOAST relations, TOAST indexes, their attributes, and the row and array types.

Mark anything still undecided as a candidate path-C item, never as a choice.

## Constraints

- Production code stays frozen at `be36323f56e61d87776d11c831ae1ef0573ea692`.
- Use the project role only.
- Keep all scratch on E:.
- The host is clear.

## Deliverable

- `assurance/reviews/WP-04-CE-04-01-checkpoint-codex-5.md` on a new branch
  `review/wp04-ce1-checkpoint-5`, from the docs state head.
- When finished, notify Claude at w6:p1.
