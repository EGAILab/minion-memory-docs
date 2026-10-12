# Hand-off — WP-04 CE-04-01 checkpoint review, revision 3 (Codex)

**From:** Claude (coordinator, Python owner). **To:** Codex (independent checkpoint review).
**Governs:**
- G-088…G-097 (G-094…G-097 are the Owner's answers to your EC01…EC05 packet, recorded verbatim in
  `reference/governance/2026-10-11-owner-layer04-start.md`);
- your closure review (`779a8f21`) and your characterization extension (`d8262cf5`).

## What to review

On the docs state head:
- `assurance/convergence/CE-04-01-classification.md` **§8, revision 3**: the dispositions of
  E001…E112 and O001…O085, the challenge rows CH13…CH18, the amended implementation constraints,
  the new evidence kind [F], and the obligations;
- the transcription in `spec/persistence.md`, "v1 catalog contract":
  - the exclusions (comments, engine bookkeeping);
  - Columns (cached missing values);
  - Indexes;
  - "Closed dependency island";
  - "Security labels";
  - "Trust scope" (stored rows are not audited).

## Asked

An independent verdict on this exact revision:
- Are the dispositions right?
- Is the "engine-maintained copies" reading of G-096 (§8.3) valid? If it needs the Owner, say so,
  and Claude will route it.
- Is CH17 (privileged routes with no recorded dependency) inside G-094's boundary statement?
- Is the structural island definition complete, and are the outgoing built-in and namespace
  allowances correct?
- Do [F] and the obligations satisfy CR-014 and discriminate P32 and P40?

Mark anything still undecided as a candidate path-C item, never as a choice.

## Constraints

- Production code stays frozen at `be36323f56e61d87776d11c831ae1ef0573ea692`.
- Use the project role only.
- Keep all scratch on E:.
- The host is clear.

## Deliverable

- `assurance/reviews/WP-04-CE-04-01-checkpoint-codex-3.md` on a new branch
  `review/wp04-ce1-checkpoint-3`, from the docs state head.
- When finished, notify Claude at w6:p1.
