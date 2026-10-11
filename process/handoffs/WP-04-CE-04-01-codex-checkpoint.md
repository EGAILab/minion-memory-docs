# Hand-off — WP-04 CE-04-01 checkpoint review (Codex)

**From:** Claude (coordinator). **To:** Codex (independent checkpoint review).
**Governs:**
- G-088 (narrow convergence);
- G-089…G-092 (the Owner's decisions on C01, C04, C05 and C06, in
  `reference/governance/2026-10-11-owner-layer04-start.md`);
- the agreed contract (docs `d857fcc2`).

## What to review

Review on the docs state head:
- `assurance/convergence/CE-04-01-classification.md`, revision 1;
- the contract transcription in `spec/persistence.md`, "Reference backend": "Open and initialize"
  steps 1–4, "v1 catalog contract", "Trust scope" and "Databases".

## Asked

An independent checkpoint verdict on this exact artifact:
- **The two discharges Claude made by authority reading, without the Owner:** C02 (namespace binding) and
  C03 (privileges). If either is really path C, say so and it goes to the Owner.
- **Faithfulness of the transcription to G-089…G-092.** It must neither add requirements the decisions do
  not make nor omit ones they do.
- **The §2 completeness additions:**
  - CH07: the frozen operations call a user `=` operator. This one was executed.
  - CH02, CH05 and CH06: executed, and accepted by the frozen code.
- **Every row disposition and the accounting**, with particular attention to:
  - R21 and C16, accepted as catalog-identical;
  - C05 and C06, explicit `"C"`/`"POSIX"` rejected as catalog-exact;
  - the NOT CREDITABLE set;
  - the X09 lock oracle.
- **The implementation constraints and evidence obligations (§5, §6):** are they sufficient to close
  WP04-CR-008 in one implementation pass?

`APPROVED` makes the checkpoint `AGREED FOR IMPLEMENTATION`; then Claude implements once and you
close. `CHANGES_REQUIRED` returns it to Claude. Mark anything the contract and G-089…G-092 still do
not decide as a candidate path-C item, never as a choice.

## Constraints

- Production code stays frozen at `634625135851cccc188fe726acb86990911ebddb`.
- **Host reservation:** Minion-Agent's Codex holds the host for #199. Run no new test, mutant or
  Docker batch until "host clear" is sent to w6:p2. Small throwaway-schema probes are at your
  judgement.

## Deliverable

`assurance/reviews/WP-04-CE-04-01-checkpoint-codex.md` on a new branch
`review/wp04-ce1-checkpoint`, from the docs state head.
