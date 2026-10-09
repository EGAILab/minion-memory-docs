# Minion-Memory — Agent workflow

**Status:** PROPOSED (WP-00), pending independent review.
**Adapted from:** Minion-Agent `process/agent-workflow.md` and `process/implementation-conformance-workflow.md`
@ `8744bd019066f9c18d000c1a0ad19b435775300a`. Section-by-section provenance and every removed
Pi-specific rule: `reference/minion-agent-process-adoption.md`.

**Adoption by reference.** Where this file says *adopted by reference*, the cited Minion-Agent
section at the pinned SHA is normative for Minion-Memory with these substitutions applied
throughout: "pinned Pi / Pi source" → "the hashed authority bundle (`reference/mneme-v2.3-source-bundle.yaml`)";
"parity manifest" → `mneme-contract-manifest.yaml`; "`PI_*` / `PARITY_*` classes" → the classes in
`process/finding-taxonomy.md`; "GitHub issue / PR / remote-reachable" → the file-based state and
local exact-SHA rules of `process/coordination-state.md`; "minion-agent#75 standing delegation" →
none (§9). A later change at Minion-Agent does not change Mneme until re-adopted by a reviewed
pin bump.

## 1. Execution model

```text
Claude = primary agent, project/process coordinator, shared-contract owner (spec, manifest,
         conformance, schemas), Python implementation owner; assigns bounded tasks to Codex;
         integrates findings; maintains coordination state.
Codex  = paired agent: independent contract/implementation reviewer, Rust implementation owner,
         cross-language challenger; acts on explicit Claude-written handoffs.
Owner  = governance authority.
```

Coordination is not semantic authority. Claude may decide that Codex is next owner and may scope
the exact review; Claude never predetermines Codex's verdict ("approve so I can continue", "copy
Python", "port these classes" are forbidden handoff wording). Codex evaluates the shared contract
and evidence independently and does not choose the next project phase. Python is never Rust's
oracle; Rust is never Python's. Neither agent self-approves.

Role entry points: `process/roles/claude-role.md`, `process/roles/codex-role.md`.

## 2. Authority

```text
authority bundle (Foundation > MVP Contract > R00..R05 > IAA)
  -> normalized spec (spec/**, after independent review)
  -> canonical conformance (finite examples)
  -> implementations
```

The manifest is traceability, not authority. Assurance records evidence and status, never
semantics. A contradiction among bundle, spec and conformance is release-blocking: stop that
semantic decision and record a finding; never silently pick a side. Minion-Agent behavior is
authoritative only for Minion-Agent's side of an integration seam.

## 3. Standard layer workflow

Each work package owns a bounded semantic surface (adopted by reference: §4.2 work-package
slicing, including the SCOPING semantic-risk map). Default sequence:

1. Record actual starting SHAs of both repos; inspect working trees; preserve unrelated work.
2. Read the WP's state file, assurance history and exact scope/non-scope.
3. Audit the authority bundle for the surface first (not a generalized design checked afterwards).
4. Repair the shared contract before implementing around a bad contract.
5. Draft contract: spec deltas, manifest rows, canonical scenarios, cross-language feasibility
   matrix (`process/templates/cross-language-feasibility-matrix.md`, mandatory for every WP touching
   values, strings, numbers, time, ordering, hashing, persistence or concurrency).
6. `CONTRACT_REVIEW` by Codex. Contract checkpoint before implementation (adopted by reference:
   §4.1, §4.1.1).
7. Python implementation through real public seams; focused tests; canonical runner.
8. Gates per `process/gate-tiers.md`; hand-off for `IMPLEMENTATION_REVIEW`.
9. Remediation / convergence (§6) until approval; acceptance by fast-forward of `main`.
10. `RUST_IMPLEMENTATION` by Codex against the accepted shared contract and canonical corpus — not
    against Python.
11. `CLOSURE_REVIEW` by Claude (who did not author the Rust candidate).
12. Certify only when the gate in §8 is satisfied. Stop; never start the next layer automatically.

Cadence: Python phase N, Rust phase N or N−1. Python must not run more than one layer ahead
without explicit Owner approval. `NOT_IMPLEMENTED` in the lagging language is valid, not a defect.

Scope discipline, contract-quality rule and "do not reopen a certified lower layer for convenience":
adopted by reference (§5, §7; implementation-conformance-workflow §4.6).

## 4. Shared artifacts and conformance

Single-source, never forked by language: `spec/**`, `mneme-contract-manifest.yaml`,
`conformance/**`, `schemas/**`, `process/**`, assurance as history.

Canonical conformance has three behavior families — `conformance/core`, `conformance/learning`,
`conformance/agent` — plus `conformance/schema` (support infrastructure, not a family). Format:
`conformance/README.md`.

**Runner rule.** A language runner may parse scenarios, construct public values, invoke the real
implementation, normalize observable output and compare to the expectation. It may **not**
implement missing semantics, repair ordering, infer evidence, perform consolidation, resolve scope,
simulate idempotency, repair serialization or decide expected results. If a runner could make an
incorrect implementation pass by supplying semantics itself, the runner is invalid. Placeholder
values beginning `TO_BE_` mark a scenario expected-failure, detected recursively by both runners;
never skipped silently, never by a hard-coded name list (adopted by reference:
implementation-conformance-workflow §9, §10.1).

When an observation turns an unordered collection into a list, the contract names the sort key;
evidence includes ≥2 entries that distinguish plausible keys (adopted by reference: §9).

## 5. Evidence discipline

Adopted by reference, unchanged in substance: §9.1 discriminating evidence; §9.2 reviewer witness
rule; §9.2.1 reviewer factual-evidence rule (content-addressed: bundle `KEY §anchor` + document
SHA-256, or a pinned commit); §9.3 "verify engine/platform premises by execution" (e.g. SQLite,
Unicode, YAML/JSON library behavior is probed, not assumed from documentation) and "expected
results come from the authority, not from the construction under review"; §9.4 semantic-neighborhood
expansion and re-check after every fix, using `process/hazard-families.md`; §9.6 event-driven
witnesses; §9.7 a negative control counts only when killed by its intended witness, and **a control
runner proves its own baseline first** (process 9.7, docs `8744bd0`); §9.8 reproducible platform
evidence and no shared host load.

Cross-language contract hazards (adopted by reference §10) are enumerated for Mneme in
`process/hazard-families.md` and audited per WP in the feasibility matrix.

## 6. Coordination, hand-offs and convergence

- Current state: `process/state/<WP>.yaml` per `process/coordination-state.md`; exactly one
  `next_owner` and one concrete `next_action` for active states; updated in the same pass.
- Exact-SHA invariant (adopted by reference §11.3): an approval binds the exact `(code.sha,
  docs.sha)` pair; any change makes it stale. Reviewers verify the SHAs exist in the named local
  repos before starting and never review prose descriptions of state.
- Ownership flow, targeted closure after remediation, one final complete review, Rust from the
  accepted contract only (adopted by reference §11.4, §11.5 with `main` as the milestone branch).
- Contract convergence protocol, triggers A–D, mandatory trigger check, two-party checkpoint
  (`PROPOSED FOR IMPLEMENTATION` → reviewer `APPROVED` → `AGREED FOR IMPLEMENTATION`), negative-
  control gate, checkpoint invalidation, cross-language revalidation (`REVALIDATE_REQUIRED`):
  adopted by reference §11.8–§11.8.11.
- Post-certification delta audit: a later-language implementation that finds a shared-contract
  ambiguity, a cross-language mismatch, a certified-implementation violation or a conformance
  workaround triggers a delta audit of the owning layer before the finding may be classified as
  local hardening (adopted by reference: implementation-conformance-workflow §4.6).
- Handoff validation (adopted by reference §11.11, local form): state valid; status not
  INCIDENT/INVALID_UNAUTHORIZED/BLOCKED_FOR_OWNER; owner/action present; candidate SHAs exist in the
  named repos and on the named refs; state-only commit rule satisfied; governance-dependent choices
  carry a governance source; not derived from a quarantined artifact. Any failure:
  `HANDOFF_BLOCKED`. Reviewer environment loss is `HANDOFF_BLOCKED`, never a verdict.
- Subagent capability boundary, governance-decision provenance, quarantine semantics, deferred
  work (`WAITING_FOR_TRIGGER`), current-state vs history, parallel work and dependency edges:
  adopted by reference §11.9, §11.10, §11.12, §11.13, §11.14, §11.15.

### 6.1 Codex handoff contents (Owner kickoff §2, §21)

Every Claude → Codex hand-off is a ready-to-run prompt stating: task title and type
(`CONTRACT_REVIEW` | `IMPLEMENTATION_REVIEW` | `TARGETED_FINDING_REVIEW` | `FINAL_CONTRACT_REVIEW` |
`RUST_IMPLEMENTATION` | `CLOSURE` / `DELTA_REVIEW` | `SCOPING_REVIEW`); role; exact scope and
non-scope; exact candidate SHAs and refs; source-bundle identity; process reference pin;
requirement IDs; artifacts to inspect; gates/commands to re-run; expected output, findings format
and allowed verdicts; what the agent may and may not modify; OWN-001; and an explicit instruction
not to use the other language's behavior as semantic authority.

## 7. Repository discipline (local-only)

- No remote repositories exist or may be created/pushed without Owner authorization. Candidates are
  local commits; "remote-reachable" in Minion-Agent rules reads "exists in the named local repo and
  is reachable from the named ref".
- Start each pass from actual repo state (`git status`, HEADs); never reset or overwrite unrelated
  work. Commit task-owned changes in coherent commits before any hand-off; report exact SHAs.
- No force-pushes or history rewrites of reviewed/accepted commits. Historical rejections stay in
  history; never rewritten into approvals.
- No nested git repositories inside either repo; neither repo is nested in the other.
- **OWN-001 (Owner rule, 2026-10-09):** every project-controlled temporary file, cache, build output,
  cloned reference repo, scratch area and review worktree lives on E: inside
  `E:\AI\Projects\OpenMinds\Minions\Minion-Memory` (`.tmp/process-temp`, `.tmp/cache`, `.tmp/work`,
  `review-worktrees/`), never on C:. Source `process/environment/project-environment.{ps1,sh}` in
  every shell that may create such files. Tools already installed on C: may be executed; toolchains
  are not installed and caches are not created there. Docker/WSL mounts map writable paths to the
  project folder.

## 8. Certification gate

Adopted by reference (§13 and implementation-conformance-workflow §5.9) with Mneme substitutions:
authority audit complete; manifest/spec/conformance complete and consistent; G3 evidence at the
exact pair; applicable canonical scenarios green through real seams; every finding classified; no
open `REQUIREMENT_UNCERTAIN`, `IMPLEMENTATION_DEFECT`, `CROSS_LANGUAGE_CONFORMANCE_DEFECT`,
`INTEGRATION_CONTRACT_DEFECT` or `CONTRACT_ASSURANCE_DEFECT` on the certified surface; risks in the
risk register; one independent complete review of the exact final candidate; registry updated in
the same pass. Approval of a shared contract is not implementation certification. A layer is not
cross-language closed until both languages are certified and closure is recorded on `main`.

## 9. Owner role

The Owner is governance authority. Escalate: authority conflicts or silence on a semantic choice;
Foundation/MVP/Requirement revisions; scope or layer-order changes; unresolved Claude/Codex
disagreement; consumer-side (Minion-Agent) changes; remote creation/publishing; destructive history
operations; standing delegation. Minion-Agent's standing delegation (`minion-agent#75`) does not
apply here; no delegation exists until the Owner records one.

## 10. Retrospective and final report

Workflow retrospectives and process metrics: adopted by reference (§14). Standard final report
(adopted by reference §15) with `REMOTE STATE` replaced by `REPOSITORY STATE` (local refs and exact
SHAs). Respect the stop condition of the current task.
