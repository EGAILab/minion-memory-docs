# CODEX HANDOFF — WP-00 SCOPING REVIEW (independent)

**Issued by:** Claude (coordinator), 2026-10-09. **Task type:** `SCOPING_REVIEW` (a scoping-only,
process WP: `requirements: []`; process/coordination-state.md §5, Minion-Agent §10.3).

---

## Prompt (ready to run)

You are **Codex**, the paired agent for Minion-Memory (Project Mneme): **independent reviewer**,
Rust implementation owner and cross-language challenger. Claude authored everything you are about to
review. Your job is to evaluate it independently against the authority bundle and the Owner's
instructions — not to confirm it, and not to implement anything.

### 1. Exact candidate

| Item | Value |
|---|---|
| Code repo | `E:\AI\Projects\OpenMinds\Minions\Minion-Memory\minion-memory`, ref `wp00/bootstrap`, **SHA `a91db170b5e7827caf1a6ffd02546ec23a1d51fa`** |
| Docs repo | `E:\AI\Projects\OpenMinds\Minions\Minion-Memory\minion-memory-docs`, ref `wp00/bootstrap`, **content SHA `42f5193dda74b6d5134eab27f7038661c4e583f3`**; the state-only child commit on top of it carries this hand-off and `process/state/WP-00.yaml` |
| Source bundle | `mneme-v2.3-dual-profile` at `E:\AI\Projects\OpenMinds\Minions\Minion-Memory\artifacts\20261009\Project_Mneme_Documentation_Bundle_2026-10_v2_3_Dual_Profile\` (12 files; zip SHA-256 `9d999c1934e33b70100e884ed5cb60d0cbdb71150af59a8b2334604b4220251e`); per-file SHA-256 in `reference/mneme-v2.3-source-bundle.yaml` |
| Process reference pin | `EGAILab/minion-agent-docs` `8744bd019066f9c18d000c1a0ad19b435775300a`; `EGAILab/minion-agent` `3de4b75d0119b6c413dae651a3cba039873756c7` |
| Remotes | none exist; do not create or push any |

**Before anything else** verify: both SHAs exist (`git cat-file -e <sha>^{commit}`) and are reachable
from `wp00/bootstrap` in their repos; `git diff --name-only 42f5193d wp00/bootstrap` in the docs repo
lists only `process/state/**` and `process/handoffs/**`; both working trees are clean. If any check
fails, stop and report `HANDOFF_BLOCKED` with the failing check — no verdict.

### 2. Authorities you must read yourself

1. The bundle DOCX/MD files themselves (not only Claude's derived text in
   `reference/source-text/`, which is a non-authoritative reading aid). Order: Foundation v2.3 >
   MVP Contract v1.2 > Requirements 00–05 (R00 normative for R01–R04; R05 for agent) >
   Implementation Architecture Amendments v1.3 > Implementation Pack / Bootstrap Prompt (guidance).
2. The Owner's decisions: `reference/governance/2026-10-09-owner-wp00-kickoff.md` (G-001…G-006,
   OWN-001). If the Owner's full kickoff text is available to you, prefer it.
3. Minion-Agent process at the pin above (for judging the adaptation; fetch read-only into
   `E:\AI\Projects\OpenMinds\Minions\Minion-Memory\.tmp\work\`).

Claude's spec, manifest, process, plans and findings are **review objects, not authority**.
Python/Claude behavior is never semantic authority for you.

### 3. Review scope

1. **Source inventory** — every bundle file listed with correct SHA-256, version, authority role and
   status; duplicates (zip, pack `reference/`) correctly identified; superseded sets correct; nothing
   missing.
2. **Normalization fidelity** (`spec/**`, 222 requirements). For each family, check that each
   requirement (a) says what its cited sources say — no added, strengthened, weakened or lost
   semantics; (b) cites the right sections; (c) carries a defensible source-status label (`FROZEN`
   only under an explicit FROZEN label; see `spec/README.md` §3); (d) merges only rules that are
   really the same. Also check **coverage**: normative bundle statements that were not transcribed
   at all. Sample at minimum every requirement in `core.md`, `scope.md`, `persistence.md`,
   `serialization.md`, `agent/**`, and ≥1 in three of every five requirements elsewhere; say what
   you sampled.
3. **Findings NF-001…NF-021** (`assurance/findings/WP-00-findings.yaml`) — is each real, correctly
   classified (`process/finding-taxonomy.md`), correctly scoped, with the right resolution layer and
   Owner flag? What did Claude miss? Challenge any you disagree with.
4. **Requirement taxonomy** (`process/requirement-id-convention.md` §2) — accept or reject the
   proposed families (kickoff names + `ARCH`, `PRIV`, `PKG`), with reasons. IDs freeze after this
   review.
5. **Process adaptation** (`process/**`, `reference/minion-agent-process-adoption.md`) — is the
   Claude-led / Codex-paired model preserved without weakening independence? Are all Pi-specific
   and GitHub-specific rules removed or correctly replaced? Is the file-based coordination state
   sound — in particular the **state-only child commit** rule and git-object round trip? Is the
   added finding class `CONTRACT_CONSTRAINED_RISK` justified? Are gate tiers adequate?
6. **Formats** — manifest schema + traceability rules, canonical scenario envelope, `TO_BE_`
   placeholder rule, runner rule, the YAML-1.2-core profile (`process/tools/src/mneme_process/yamlcore.py`):
   **can a Rust runner implement each of these independently and identically?** Name any construct
   that would force Rust to copy Python mechanics.
7. **Dual-profile boundary** (`assurance/layers/00-dual-profile-boundary-review.md`) — anything
   admitted to core that distorts a profile, or kept out of core that both profiles need?
8. **Minion-Agent seam audit** (`assurance/layers/00-minion-agent-seam-audit.md`) — independently
   re-verify at `3de4b75` that the agent-loop driver records only `system_base`
   (`minion-agent-python/src/minion_agent/agent_loop/driver.py`), the name-sorted assembly, and the
   Rust equivalent. Is NF-007/NF-008 correctly characterized?
9. **Layer plan and WP-01 proposal** (`plans/layer-plan.md`, `plans/WP-01-proposal.md`) — are the
   dependency edges right? Is WP-01 bounded and the right first semantic package?
10. **Hazard inventory** (`assurance/layers/00-cross-language-hazard-inventory.md`,
    `process/hazard-families.md`) — missing families/members, especially Rust-side hazards.
11. **Validator** (`process/tools/`) — re-run it; are the negative controls realistic and killed by
    their intended assertion? Which bootstrap rule is claimed but not enforced?

### 4. Explicit non-scope

No implementation of any kind. Do **not** create the Rust workspace (that comes with your first
`RUST_IMPLEMENTATION` task). Do not edit `spec/**`, `process/**`, `plans/**`, `reference/**`,
`assurance/findings/**`, the manifest, schemas, conformance or Python — Claude remediates. Do not
touch `wp00/bootstrap` or `main` in either repo. Do not modify the bundle. Do not start WP-01.

### 5. Gates to re-run (sequentially, OWN-001 environment)

```sh
. /e/AI/Projects/OpenMinds/Minions/Minion-Memory/minion-memory-docs/process/environment/project-environment.sh
# (PowerShell: . E:\AI\Projects\OpenMinds\Minions\Minion-Memory\minion-memory-docs\process\environment\project-environment.ps1)
cd /e/AI/Projects/OpenMinds/Minions/Minion-Memory/minion-memory-docs/process/tools
export UV_PROJECT_ENVIRONMENT="$MNEME_VENV_ROOT/mneme-process-codex"
uv sync --python 3.12
uv run pytest                                   # Claude observed: 69 passed
uv run ruff check src tests && uv run ruff format --check src tests && uv run mypy src
uv run mneme-process check --docs ../.. --code ../../../minion-memory --deep-sources   # observed: 8/8
cd /e/AI/Projects/OpenMinds/Minions/Minion-Memory/minion-memory/minion-memory-python
export UV_PROJECT_ENVIRONMENT="$MNEME_VENV_ROOT/minion-memory-python-codex"
uv sync --python 3.12 && uv run pytest          # observed: 2 passed, 6 xfailed (placeholders)
```

Report your own fresh counts; do not quote these. Add any probe you need (e.g. a Rust YAML-1.2
loader against the corpus) under `E:\AI\Projects\OpenMinds\Minions\Minion-Memory\.tmp\work\codex\`.
**OWN-001:** every temp file, cache, venv, `CARGO_TARGET_DIR` and worktree stays inside
`E:\AI\Projects\OpenMinds\Minions\Minion-Memory` — never on C:.

### 6. Output

1. A review record committed on a **new branch `review/wp00-codex-1`** created from the current
   `wp00/bootstrap` head of the docs repo, adding exactly one file
   `assurance/reviews/WP-00-scoping-review-codex-1.md`. Report that commit's SHA.
2. The record states: reviewer role; the exact SHAs reviewed; bundle identity; process pin; what you
   read and sampled; gate commands with fresh results; findings; verdict; recommended next
   transition.
3. Findings use IDs `WP00-CR-001…` in this shape:

   ```yaml
   - id: WP00-CR-001
     title: ...
     classification: <one class from process/finding-taxonomy.md>
     blocking: true|false
     owner_decision_required: true|false
     sources: ["<bundle KEY §anchor + file SHA-256, or pinned commit:path:line>"]
     requirements: [<IDs>]
     observation: <what the candidate says/does>
     expected: <what the authority requires>
     witness: <minimal reproducer or exact text comparison>
     recommendation: ...
   ```

   A blocker needs a content-addressed source and a discriminating witness; a suspicion without
   evidence is a **question**, not a blocker. Positions on NF-001…NF-021 go in a separate table
   (agree / disagree / reclassify, with reason).
4. Exactly one verdict:
   - `APPROVED` — no blocking findings (non-blocking findings allowed);
   - `CHANGES_REQUIRED` — ≥1 blocking finding;
   - `HANDOFF_BLOCKED` — the hand-off or your environment is invalid (no verdict on content).

Do not update `process/state/WP-00.yaml`; Claude records your verdict after independently
reproducing any shared-contract finding. Do not use Python behavior as semantic authority.

---

## Candidate gate evidence (Claude, author-run; not a review)

Run at code `a91db170…` / docs `42f5193d…` with both trees clean, sequentially, under OWN-001
(Windows 11, Python 3.12.8 via uv 0.10.9, git 2.55.0):

| Gate | Result |
|---|---|
| `mneme-process` tests (`process/tools`, incl. 28 repository-level negative controls + 38 unit witnesses, baseline asserted before each control) | 69 passed |
| ruff check / ruff format --check / mypy --strict (tools) | clean / 11 files formatted / no issues (8 files) |
| `mneme-process check --deep-sources` (repos, sources, spec, manifest, conformance, findings, registry) | 7/7 passed (state check runs after this child commit) |
| Python scaffold pytest | 2 passed, 6 xfailed (all 6 PLACEHOLDER scenarios) |
| ruff / format / mypy --strict (Python scaffold) | clean / 3 files formatted / no issues |
| Trees clean after gates; C: session scratchpad empty | yes / yes |
