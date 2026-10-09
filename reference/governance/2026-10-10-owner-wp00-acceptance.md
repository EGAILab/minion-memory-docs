# Owner governance record — WP-00 acceptance, delegation, status split, closure (2026-10-10)

**Source:** the Owner's explicit answers in the controlling Claude Code conversation, given to four
questions Claude asked after Codex targeted closure review 2 (`review/wp00-codex-3` @
`4293b797da7f3334bf4f630b46f19bb55f89efa8`) APPROVED the WP-00 pair. Recorded by Claude, durably,
per Minion-Agent agent-workflow §11.10. Questions and answers are verbatim; Claude's "(Recommended)"
marks were recommendations only — these are decisions because the Owner selected them.

## G-008 — Acceptance of the WP-00 pair

> **Q:** Codex APPROVED the WP-00 bootstrap (code bb05e395 / docs 237948fe). Accept that exact pair
> onto `main` in both repos?
>
> **A:** Accept onto main (Recommended) — "I fast-forward `main` to bb05e395 (code) and 237948fe
> (docs) only, record your decision in reference/governance/, and file post-acceptance records
> (Codex's review record, state) on top."

Scope: exactly code `bb05e3953a044ea8abd9d796675290ad9fe80941` and docs
`237948fee550b691d0e83defb6c49186a27af3b8`.

## G-009 — Standing delegation of routine governance (resolves NF-020)

> **Q:** NF-020: grant me a standing delegation for routine acceptance, like Minion-Agent's #75?
> It would cover exact-SHA acceptance after an independent APPROVED review, status/registry
> updates and ordinary hand-offs. Semantic, scope and Owner-flagged decisions would still come to
> you.
>
> **A:** Grant routine delegation (Recommended) — "Lets the Claude↔Codex loop run without you
> relaying every acceptance; independence and exact-SHA rules unchanged. I record it verbatim in
> reference/governance/."

**Delegation text (as granted, scope exactly as asked):** Claude may, without a fresh Owner
response, (1) accept onto `main` an exact candidate SHA pair that an independent review recorded
`APPROVED` with no blocking findings; (2) make status, registry and coordination-state updates
that follow from process-defined transitions; (3) perform ordinary hand-offs. **Not delegated:**
semantic or scope decisions; any path-C choice (`process/finding-taxonomy.md` §1.1); any finding
flagged `owner_decision_required`; changes to governance, authority or this delegation; remote
creation/publishing; destructive history operations. The delegation never weakens reviewer
independence, exact-SHA approval, negative controls, required reviews or the state commit rule.
Decisions Claude makes under it are recorded as
`standing_delegation: reference/governance/2026-10-10-owner-wp00-acceptance.md#g-009` and are not
described as Owner decisions on the specific item. Only the Owner amends or revokes it.

## G-010 — Status registry split (resolves NF-021)

> **Q:** NF-021: keep implementation/certification status in the separate registry
> (process/certification-registry.yaml), with the manifest holding locations only? The kickoff
> asked the manifest to map 'location/status'.
>
> **A:** Registry split (Recommended) — "Status lives in one registry, so the manifest needs no
> status-only edits after every closure (the problem Minion-Agent documents)."

This amends kickoff §15 (G-007): status is mapped through the registry; manifest rows carry
locations.

## G-011 — WP-00 closure route

> **Q:** How should WP-00 close, given the non-blocking WP00-CR-014 (the FROZEN-citation guard is
> lexical only) and the NF findings owned by later layers?
>
> **A:** Close now, carry forward (Recommended) — "Close WP-00 on the accepted pair. CR-014 and the
> remaining process items (e.g. a UTF-8-safe state round-trip command) become a small
> process-hardening WP. NF findings move to the layers that resolve them."
