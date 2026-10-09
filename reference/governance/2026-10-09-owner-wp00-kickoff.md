# Owner governance record — WP-00 kickoff and OWN-001 (2026-10-09)

**Source:** the Owner's messages to Claude in the controlling Claude Code conversation of
2026-10-09 (kickoff prompt "You are Claude Code, the PRIMARY CODE AGENT and PROCESS COORDINATOR
for Project Mneme / Minion-Memory", 37 sections; and a follow-up message during WP-00).
**Recorded by:** Claude, durably, per Minion-Agent agent-workflow §11.10 (an Owner message is a
governance source once recorded into project artifacts).
**Form:** excerpts of the decisions this project relies on, quoted from the kickoff with section
numbers. Excerpts are verbatim except whitespace; omitted text is marked `[...]`. Where the full
kickoff wording matters, it is the kickoff text itself, not this summary.

## G-001 — Execution model (kickoff §§1–4, §21)

> CLAUDE = primary agent = project/process coordinator = shared-contract owner = Python
> implementation owner = assigns bounded review/Rust tasks to Codex = integrates findings and
> drives the project forward
>
> CODEX = paired agent = independent contract / implementation reviewer = Rust implementation owner
> = cross-language challenger = receives explicitly scoped tasks/handoffs from Claude

> Claude MUST NOT treat Codex as a subordinate semantic oracle. [...] Claude/Python is never
> semantic authority for Codex/Rust. Codex/Rust is never semantic authority for Claude/Python. The
> shared reviewed contract is the authority.

## G-002 — Authority hierarchy (kickoff §8, §16)

> 1. Foundation 2. MVP Contract 3. normative Requirement documents 4. adopted Architecture
> Amendments 5. independently reviewed normalized Markdown contract 6. canonical conformance
>
> The implementation pack is guidance. Research projects are prior-art evidence, not authority.

> If authoritative Mneme documents conflict: STOP that semantic decision.

## G-003 — Read-only bundle (kickoff §1, §12)

> Treat this bundle as READ-ONLY upstream project authority. Do not edit, rename, move, normalize
> in place, or silently replace files in it.

## G-004 — Local repositories only (kickoff §11, §29)

> Do not publish or create remote repos unless separately authorized.

> If appropriate and no repository exists, Claude is authorized to initialize: [...]
> minion-memory and: [...] minion-memory-docs. Do not create remote repos. Do not push.
> Bootstrap commits are allowed only after internal validation. Record exact SHAs.

## G-005 — WP-00 scope and stop condition (kickoff §28, §34, §35)

WP-00 in scope / out of scope as listed in kickoff §28 (no real Python or Rust memory behavior,
no FSRS, scheduler, consolidation, production adapter, production SQLite schema, vector DB,
embedding provider, AI evaluator, Flutter migration or cloud sync).

> This Claude invocation stops at the first required independent review boundary. Return exactly
> one workflow outcome: BOOTSTRAP_READY_FOR_CODEX_REVIEW or BLOCKED_FOR_OWNER or
> BOOTSTRAP_INPUTS_MISSING [...] Do NOT claim: CERTIFIED APPROVED FROZEN from Claude's
> self-authored WP-00 pass.

> Do not begin WP-01 before that review is resolved.

## G-007 — Contract manifest (kickoff §15)

> Create: minion-memory/mneme-contract-manifest.yaml
>
> This is TRACEABILITY, not semantic authority.
>
> Map: upstream source -> requirement ID -> normative spec anchor -> canonical scenario(s) ->
> Python location/status -> Rust location/status -> assurance evidence -> disposition
>
> Python and Rust consume the same rows.

(Recorded verbatim in remediation 1 because WP00 Codex review 1 could not verify the
"location/status" wording cited by NF-021 from the excerpts alone.)

## G-006 — Phase distance (kickoff §20)

> Preferred phase distance: Python = N, Rust = N or N-1. Do not let Python run several layers ahead
> without explicit Owner approval.

## OWN-001 — Temporary files and caches on E: (Owner message during WP-00, 2026-10-09)

Verbatim:

> all one rule that all the temporary/cache files should be created within E: project folder
> instead of C:

Interpretation applied (consistent with the identical Minion-Agent Owner requirement in
`Minion-Agent/.agents/AGENTS.md`): every project-controlled temporary file, cache, build output,
cloned reference repository, scratch area and review worktree lives inside
`E:\AI\Projects\OpenMinds\Minions\Minion-Memory` — `.tmp/process-temp`, `.tmp/cache`, `.tmp/work`,
`review-worktrees/` — never on C:. Applies to Claude and Codex. Implementation:
`process/environment/project-environment.{ps1,sh}`. Pre-existing C:-installed tools may be executed;
toolchains are not installed and caches are not created on C:.
