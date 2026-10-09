# WP-00 — Minion-Agent integration seam audit

**Author:** Claude (read-only audit). **Date:** 2026-10-09.
**Evidence pins** (fresh clones at `.tmp/work/ref/`, verified with `git ls-remote` the same day):

| Repo | Pinned SHA | Notes |
|---|---|---|
| `EGAILab/minion-agent` `main` | `3de4b75d0119b6c413dae651a3cba039873756c7` (2026-10-09 13:49 +1100) | kickoff observed `d461f81…` (ancestor; 1 newer commit: L08-D002 request-schema snapshot) |
| `EGAILab/minion-agent-docs` `master` | `8744bd019066f9c18d000c1a0ad19b435775300a` (2026-10-09 14:01 +1100) | kickoff observed `0834a93…` (ancestor; 2 newer commits) |
| bundle snapshot (FND §G.8, R05 §3, IAA §12) | `d37171d716fe8fc44b5c16fec9c69705f8c74760` | ancestor of `3de4b75` |

The local working copies under `Minion-Agent/` are on older feature branches
(`layer/12-ext-wp12e1-rust` @ `4301816`, `assurance/12-wp12e1-rust` @ `631aaab`) and were **not**
used as evidence or modified.

Minion-Agent is authority only for its side of the seam (MINT-001). Nothing below is Mneme
semantics.

## 1. Seam inventory at `3de4b75`

| Seam | Location | Observed | Mneme relevance |
|---|---|---|---|
| Content-addressed request header | `minion-agent-python/src/minion_agent/session/request_header.py` (`record_header`, `assemble_system`, `reconstruct_header`); Rust `crates/minion-agent/src/session/mod.rs:402,472` | Component **names are open**; each component stored by hash; header logs references; `assemble_system` joins components **sorted by name** (Python `sorted`, Rust `BTreeMap`) | Mechanism suits ACTX-003/MINT-006 reconstructability |
| Header publication in the agent loop | `agent_loop/driver.py:1095` | `components = {"system_base": self._system_text(decision, context)}` — the driver records **exactly one** component. Same at `d37171d` (line 1084) and since the driver's introduction (`65401dd`) | No way for an adapter to add a `memory` component today → **NF-007** |
| Design intent | `minion-agent-docs/design/2026-08-20-minion-agent-design.md` "Content-addressed request state" | Lists `system_base, skills, tools, memory, task` components; `2026-08-18-foundation-validation.md` names memory recall (~500 tokens, changes per turn) as the motivating dynamic component and a `request-header-component-reuse` scenario | Confirms the bundle's "documented memory component" is **design**, not runtime wiring |
| Prompt composition | `system_prompt/composer.py` (`PromptComposer`, `PromptConfiguration.sections`) installed as the driver's `prompt_assembler` | Contributed `sections` are joined into the single system text, which becomes `system_base` | A working injection path today, but memory would be indistinguishable inside `system_base` → **NF-007/NF-008** |
| Session event namespace | `session/events.py` | Open, validated names (`^[a-z][a-z0-9_]*(?:/[a-z][a-z0-9_-]*)*$`); plugin names allowed; core surface kinds fixed | Adapter audit/reference events possible (MINT-008) |
| Runtime services/plugins | `runtime/` (`Context`, `ServiceRegistry`, `PluginRegistry`, `Scope`, fibers) | Cordis-semantic scoped service/plugin runtime | Adapter may be a provider; Mneme engine must not depend on it (MINT-005) |
| Session history/compaction/forks | `session/log.py`, `derive.py`, `operations.py` | Authoritative append-only log; compaction/fork/reset are log operations | Capture references only (ACAP-008); compaction ≠ consolidation (ACON-004) |

## 2. Hypothesis check (kickoff §19)

> Known hypothesis to verify: request/header supports an open "memory" component suitable for
> reconstructed memory context injection.

**Partially confirmed.** The header *mechanism* supports any component name with
content-addressed reconstruction, and the master design names `memory`. The *runtime* does not let
any caller contribute a component: the driver hard-codes `system_base`. Injection today is only
possible through `PromptComposer` sections, which fold memory into `system_base` (one hash for base
prompt + memory; no component-level reuse or attribution in the header).

Kickoff §19 forbids introducing a second hidden injection path. The bundle (IAA §12) lists both
seams. Choosing exactly one is a Layer-16 contract decision (NF-008); enabling the header component
needs an additive Minion-Agent change through Minion-Agent's own process (NF-007, Owner decision).

**Ordering hazard:** with name-sorted assembly, a `memory` component precedes `system_base` in the
dispatched system prompt. Whether that placement is acceptable is a Minion-Agent-side product
question recorded in NF-008.

## 3. Drift since the bundle snapshot

`git diff --numstat d37171d..3de4b75` over the seam files: `session/request_header.py` +44/−3,
`agent_loop/driver.py` +13/−2 (L08-D002: tool-schema value snapshot at header publication). The seam
conclusions are unchanged; the evidence pin moves to `3de4b75` (NF-009). Layer 16 re-pins.

## 4. Boundary conclusions (kickoff §7) — evidence, not decisions

- SessionStorage/history and Minion-Memory remain separate stores; nothing observed requires
  Minion-Memory to read or rewrite the session log beyond stable references (MINT-002/003).
- Conversation compaction is a Minion-Agent log operation; memory consolidation must not be mapped
  onto it (ACON-004).
- Pre-request retrieval + post-turn capture fit the driver's per-step request build and turn
  lifecycle events; the precise hook points are a Layer-16 audit item.
