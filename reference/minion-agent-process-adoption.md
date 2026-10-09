# Minion-Agent process adoption record (WP-00)

**Adopted pin:** `EGAILab/minion-agent-docs` `master` @ `8744bd019066f9c18d000c1a0ad19b435775300a`
(2026-10-09 14:01 +1100); implementation reference `EGAILab/minion-agent` `main` @
`3de4b75d0119b6c413dae651a3cba039873756c7` (2026-10-09 13:49 +1100). Both verified with
`git ls-remote` and fresh clones (`.tmp/work/ref/`), 2026-10-09.

**Kickoff pins verified:** `0834a937…` (docs) and `d461f812…` (code) exist and are ancestors of the
adopted pins. **Delta since the kickoff pin:** docs gained 2 commits; the only `process/` change is
`agent-workflow.md` §9.7 +6 lines — "a control runner proves its own baseline (selection, pending
markers, recipe)" (#272). It is process-semantic and was adopted (Mneme agent-workflow §5; the
validator's test fixture asserts the baseline before each negative control). Code gained 1 commit
(L08-D002 request-schema snapshot at header publication, #181) — relevant only to the seam audit.

**Local copies** under `Minion-Agent/` are on older feature branches and were not used.

**Substitutions applied to everything adopted by reference** are listed at the top of
`process/agent-workflow.md`.

## Per-document record

| Minion-Agent source @ `8744bd0` | Mneme target | Reused | Removed (Pi-specific or GitHub-specific) | Modified for Mneme | Rationale |
|---|---|---|---|---|---|
| `process/agent-workflow.md` | `process/agent-workflow.md` | Claude/Codex roles, layer workflow, contract-first checkpoint, feasibility audit, WP slicing, scope discipline, contract-quality rule, runner rule, discriminating evidence §9.1–9.8 (incl. new §9.7 baseline rule), exact-SHA invariant, ownership flow, convergence protocol §11.8–11.8.11, subagent boundary, governance provenance, handoff validation, quarantine, deferred work, parallel work, certification gate, retrospective, final report | Pi-fidelity goal (§1), Pi baseline SHA, `PI_*`/`PARITY_*` taxonomy, Pi divergence governance (§6.1), pinned-Pi characterization probes as authority, GitHub issue/PR control plane (§11.1–11.2, §12 remote push), standing delegation `minion-agent#75` | Authority chain starts at the hashed bundle; Claude explicitly coordinator; Codex hand-off contents (§6.1); local-only repository discipline; OWN-001; no delegation until Owner grants (NF-020) | Kickoff §10; no reference implementation; no remotes authorized |
| `process/coordination-state.md` | `process/coordination-state.md` | Current-vs-history split, schema v2 lean state, active/deferred/closed/incident invariants, legal transition table §10–§10.3, convergence record retention, discriminating-witness record, governance source, YAML load boundary §13.6 | `pinned_pi`, PR fields, issue-body round trip | State file in the docs repo; exact local SHAs + refs; **state-only child commit** rule (self-reference); git-object round trip replaces re-fetch | No GitHub control plane authorized |
| `process/gate-tiers.md` | `process/gate-tiers.md` | G0–G3 definitions, stage minimums, escalation, no de-escalation, "G3 is evidence, not review" | pinned-Pi harnesses, pinned Node/ICU | Scoping/process hand-off row; `mneme-process check` as manifest/schema gate | Authority is the bundle |
| `process/requirement-id-convention.md` | `process/requirement-id-convention.md` | Principle, location, granularity, stability, conformance linkage | Pi prefixes (RT, LLM, …), parity-row mapping | Mneme families validated against kickoff + bundle (adds ARCH, PRIV, PKG); bijection with manifest enforced | Kickoff §14 asked for validation |
| `process/implementation-conformance-workflow.md` | `process/agent-workflow.md` §2–§5, §8 | One contract/one corpus, Python-leading cadence, runner rule, `TO_BE_` placeholders, post-certification delta audit, risk register discipline | Pi drift workflow (§21), post-parity hardening (§22), Pi-specific CI items | Families `core/learning/agent`; contract-constrained risk replaces parity-constrained risk | Kickoff §10 |
| `process/hazard-families.md` | `process/hazard-families.md` | Method (pre-enumerated members, neighborhood expansion, AUDITED/NA/DEFERRED) | JS Number/UTF-16/ECMAScript-order/schema-runtime families as written | Families re-derived for Python/Rust/JSON/YAML/SQLite (H1–H11) | No JS reference runtime |
| `process/templates/cross-language-feasibility-matrix.md` | same path | Structure, silence-is-not-an-answer, gap-is-a-finding, concurrency matrix with realistic wrong implementations | Pi wire/runtime columns, JS hazard checklist | Contract-domain/Python/Rust/serialized columns; H1–H11 checklist | Same |
| `process/certification-registry-design.md` | `process/certification-registry.yaml` + coordination-state §1 | Registry as single status source, status vocabularies, invariants | migration from spec status lines (nothing to migrate) | Adopted from day one; manifest carries locations only (NF-021) | Avoids status-only churn Minion-Agent documents |
| `process/authority-dependencies.md` | — (principle in agent-workflow §5 via §9.3) | "verify and execute the authority; bytes may come from anywhere if digest-verified" | npm/Docker specifics | Applies to the bundle: SHA-256 verified by `mneme-process check sources` | Mneme's authority is documents, not executables |
| `process/minion-process-cli-design.md` | `process/tools/` (`mneme-process`) | Principle "agents decide semantics, the tool decides mechanical legality"; fail-closed control data; YAML load boundary; never approves | GitHub `gh` commands, PR merge, issue apply/repair | Local checks: sources, spec, manifest, conformance, findings, registry, state, repos; transition-check | No GitHub |
| `.claude/CLAUDE.md`, `.agents/AGENTS.md` (local workspace, not in the docs repo) | `process/roles/claude-role.md`, `process/roles/codex-role.md` | Role boundaries, review-mode independence order, "Python is not the oracle", temp/cache-on-E: rule | GitHub remote handoff rules | Claude coordinates; Codex acts on Claude hand-offs; OWN-001 | Kickoff §1–§4 |

Process documents present at the pin but **not** adopted (historical reviews/proposals):
`2026-08-2*-*.md`, `agent-workflow-revision-proposal.md`,
`implementation-conformance-workflow-review-feedback.md`, `shared-contract-reviewer-policy-proposal.md`
(its adopted rule — semantic-owner approval for shared-contract changes — is already implied by the
Mneme review flow).
