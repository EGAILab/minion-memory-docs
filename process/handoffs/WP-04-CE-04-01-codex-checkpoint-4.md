# Hand-off — WP-04 CE-04-01 checkpoint re-review, revision 4 (Codex)

**From:** Claude (coordinator, Python owner). **To:** Codex (independent checkpoint review, targeted).
**Governs:**
- G-088…G-098 (G-098 is the Owner's answer to CE04-CP-004, recorded verbatim);
- your checkpoint review 3 (`1d158979`), `CHANGES_REQUIRED`, CE04-CP-004…007.

## What to review

On the docs state head:
- `assurance/convergence/CE-04-01-classification.md` **§9, revision 4**: §9.0 maps each finding to
  its resolution;
- `spec/persistence.md`, "v1 catalog contract":
  - the closed G-096 exemption and the G-098 rule;
  - the island paragraph (no-recorded-dependency references, the `FOR TABLE` entry);
  - "Internal members are certified, not only discovered".

## Asked

A targeted, independent verdict on this exact revision:
- Are CE04-CP-004…007 resolved?
- Is the §9.1 accounting right?
- Does the `members` part with its [F] controls close the extra-TOAST-index countermodel?
- Is the E004 oracle right?

Mark anything still undecided as a candidate path-C item, never as a choice.

## Constraints

- Production code stays frozen at `be36323f56e61d87776d11c831ae1ef0573ea692`.
- Use the project role only.
- Keep all scratch on E:.
- The host is clear.

## Deliverable

- `assurance/reviews/WP-04-CE-04-01-checkpoint-codex-4.md` on a new branch
  `review/wp04-ce1-checkpoint-4`, from the docs state head.
- When finished, notify Claude at w6:p1.
