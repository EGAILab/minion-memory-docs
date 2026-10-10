# Owner governance record — WP-P01 convergence route; WP-01 parallel authoring (2026-10-10)

**Source:** the Owner's explicit answers in the controlling Claude Code conversation, after Codex
targeted closure review 2 of WP-P01 (`review/wpP01-codex-3` @
`dc576a97caa1929c00489203b7a80b8c24383f05`) left WPP01-CR-001/002 open a third time and WP-P01 was
routed `BLOCKED_FOR_OWNER`. Recorded verbatim by Claude per Minion-Agent agent-workflow §11.10.

## G-018 — WP-P01: Codex-led convergence

> **Q:** WP-P01: WPP01-CR-001/002 survived three independent reviews. Each round, Codex found a
> narrower edge on the same surface: how the validator trusts git output and state-file fields.
> How should I route it?
>
> **A:** "Choose 1 — Codex-led convergence.Treat WPP01-CR-001/002 as evidence that the current
> characterization of the validator trust boundary is incomplete, not as two isolated witness
> defects. Freeze production edits on that surface. Have Codex produce the exhaustive
> characterization matrix covering every relevant input source × path-eligibility rule × state
> field × git ref namespace × resolution path and all malformed/ambiguous cases. Claude
> independently challenges completeness and classifies each row. Only after convergence should
> Claude implement the resulting contract once; Codex then performs targeted closure against the
> agreed matrix. Do not reopen already-proven unrelated WP-P01 semantics unless the
> characterization produces contradictory evidence."

Applied as: `BLOCKED_FOR_OWNER → CONTRACT_CONVERGENCE` (Owner-authorized continuation), episode
`CE-P01-01`; characterization by Codex (adopted Minion-Agent §11.8.3), challenge and row
classification by Claude (§11.8.4), two-party checkpoint (§11.8.5: Claude records `PROPOSED FOR
IMPLEMENTATION`, Codex's separate `APPROVED` makes it `AGREED FOR IMPLEMENTATION`), one
implementation pass, then Codex targeted closure (§11.8.7) against the agreed matrix.

## G-019 — WP-01: parallel authoring, serial governance

> **Q:** Should WP-01 (the Layer 01 contract draft: identity, versions, hashing, value domain
> under G-012…G-017) start in its own worktree while WP-P01 is resolved?
>
> **A:** "Choose 1 — Start WP-01 in parallel.Treat this as parallel authoring but serial
> governance. Create review-worktrees/docs-wp01 and begin only the Layer-01 CONTRACT_DRAFT work for
> identity, versions, hashing, and value-domain requirements G-012…G-017. Do not modify
> WP-P01-owned process/tooling surfaces, do not transition WP-01 to CONTRACT_REVIEW, and do not
> hand it to Codex while WP-P01 convergence is active. Any validator results produced meanwhile are
> development feedback only, not assurance evidence.After WP-P01 closes, rebase/reconcile WP-01
> against the final process candidate, rerun the applicable validation under the corrected
> validator, resolve any process-induced deltas, bind the candidate to exact SHAs, and only then
> assign the WP-01 independent contract review to Codex."
