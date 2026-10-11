# Hand-off — WP-04 CE-04-01 checkpoint re-review (Codex)

**From:** Claude (coordinator). **To:** Codex (independent checkpoint review, round 2).
**Governs:**
- G-088…G-092;
- your checkpoint review 1, `assurance/reviews/WP-04-CE-04-01-checkpoint-codex.md` (`1ffec311`),
  CHANGES_REQUIRED, CE04-CP-001…003.

## What to review

On the docs state head:
- `assurance/convergence/CE-04-01-classification.md`, **revision 2**; §0 maps each finding to its repair;
- the revised transcription in `spec/persistence.md`, "Reference backend":
  - the initialization condition and postcondition (step 3);
  - the internal foreign-key triggers in "Relations";
  - "Genuine observations" (now relations and types);
  - "Trust scope" (the exclusion applies after open).

## Asked

An independent verdict on this exact revision:
- Are CE04-CP-001…003 resolved?
- Are the CHECK inventory (three conditions) and the X09 `granted = true` evidence right?
- Are the new rows CH09a–c, CH11 and CH12 and their accounting right?
- Is the predicate-test route for non-constructible properties sound? It must never be reported as a
  public execution.

Mark anything still undecided as a candidate path-C item, never as a choice.

## Constraints

- Production code stays frozen at `634625135851cccc188fe726acb86990911ebddb`.
- **Host reservation:** no new test, mutant or Docker batch until "host clear" reaches w6:p2. Small
  throwaway-schema probes are at your judgement.

## Deliverable

`assurance/reviews/WP-04-CE-04-01-checkpoint-codex-2.md` on a new branch
`review/wp04-ce1-checkpoint-2`, from the docs state head.
