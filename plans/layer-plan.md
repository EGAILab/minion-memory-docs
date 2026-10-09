# Layer and dependency plan — PROPOSED (WP-00)

**Inputs compared:** Owner kickoff §27 (candidate order), bundle bootstrap prompt v1.1 ("proposed
dependency-aware layers"), Implementation Pack v1.3 `IMPLEMENTATION_PLAN.md`. They disagree (NF-005).
**Method:** for each layer, list the requirements it owns (manifest `layer` field) and the lower
layers whose semantics those requirements consume. Not frozen; independent review pending.

## 1. Layers

| Layer | Surface | Owns (families / IDs) | Depends on |
|---|---|---|---|
| 00 | process, authority, normalization, conformance infrastructure | WP-00 (no product requirements) | — |
| 01 | identity, version, provenance, lineage, operation identity; **portable value domain & serialization basics** | CORE-*, SER-001..004, SER-007 | 00 |
| 02 | MemoryScope; history envelope vocabulary, occurred/recorded, no global order, information origin; compatibility envelope | SCOPE-*, HIST-001, HIST-002, HIST-004, HIST-005, HIST-010, SER-005, SER-006 | 01 |
| 03 | projection/normalization path; append-only reinterpretation | PROJ-001, PROJ-002, HIST-006, HIST-007 | 02 |
| 04 | persistence semantics: tiers, durability barrier, transactions, idempotent commit, bounded/incremental history, no-semantic-dedup enforcement | PERS-001..008, PERS-012..016, HIST-008, HIST-009 | 01–03 |
| 05 | ReplayCheckpoint | PERS-009..011 | 03, 04 |
| 06 | retrieval/index/progressive disclosure; ProjectionBudget | RET-*, PROJ-003..005 | 02–05 |
| 07 | learning knowledge (+ layer-separation invariant) | KNOW-*, ARCH-006 | 01–06 |
| 08 | learning interaction history, episode event order | LEARN-*, OBS-*, HIST-003 | 07 |
| 09 | learning evaluation/evidence/diagnostics | EVAL-*, EVID-* | 08 |
| 10 | LearnerMemoryModel, learner checkpoint dependencies, evaluation discipline | LMEM-* (incl. LMEM-014, LMEM-015) | 09, 05 |
| 11 | scheduling / RecallForm selection | SCHED-* | 10 |
| 12 | package import, legacy migration, learning backup | PKG-*, MIG-*, BKP-001..003, BKP-005..008 | 07–11 |
| 13 | agent observation, MemoryRecord, capture | ACAP-*, AMEM-*, PRIV-006 | 01–06 |
| 14 | agent consolidation | ACON-* | 13 |
| 15 | agent retrieval/ranking, AgentContextProjection, **context fencing** | ARET-*, ACTX-* | 13, 14, 06 |
| 16 | Minion-Agent integration | MINT-* | 15 (+ NF-007/NF-008 decisions) |
| 17 | cross-profile persistence/backup/interoperability | BKP-004 (+ cross-profile restore scenarios) | 12, 16 |
| 18 | integrated certification | — | all |
| cross-cutting | ARCH (except ARCH-006), PRIV-001..005 | verified at every layer review | — |

## 2. Changes against the kickoff candidate, with reasons

1. **Serialization basics move into Layer 01.** Every later layer's conformance compares serialized
   observable values; the value domain (integers, floats, strings, timestamps, null/unknown,
   canonical JSON) must be agreed before any scenario becomes ACTIVE (NF-019, NF-013, NF-015).
2. **Context fencing moves from Layer 14 to Layer 15.** ACTX-004 needs AgentContextProjection
   identity (ACTX-001), which Layer 15 introduces; Layer 13 carries only the `origin` vocabulary
   (ACAP-007). Testing fencing before projections exist would force a fake projection in the runner.
3. **HIST-008 (no semantic dedup) is certified in Layer 04**, where idempotent commit is
   implemented, so its negative control (dedup-by-similarity) has a real seam.
4. **Profiles are independent after Layer 06.** Learning (07–12) and Agent (13–16) share no
   dependency edges. Default order keeps the kickoff (learning first); the Owner may choose agent
   first or alternation before Layer 07 (NF-005). Python ≤ one layer ahead of Rust either way.

## 3. Compared with the bundle bootstrap order

The bundle order places persistence at L08 (after agent capture at L07). That contradicts the
dependency of capture idempotency (ACAP-003) and learning commit idempotency (LEARN-008) on the
persistence idempotency semantics (PERS-006). Kickoff order is kept.

## 4. Work packages

One WP per layer by default; a layer with several independent high-risk surfaces is split before
contract drafting (agent-workflow §3). Layer 02 is the first likely split: MemoryScope (Owner
decisions likely, NF-018) vs history envelope.
