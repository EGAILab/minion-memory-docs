# Minion-Memory normalized contract — DRAFT

> **Status: NORMALIZATION DRAFT (WP-00).** This tree transcribes the Project Mneme v2.3
> dual-profile bundle into requirement-ID-bearing Markdown. It has **not** been independently
> reviewed. It is not yet implementation-facing: a layer's requirements become
> implementation-facing only after that layer's own `CONTRACT_REVIEW` (process/agent-workflow.md
> §4). Certification status never lives here; see `process/certification-registry.yaml`.

## 1. Authority

The normalized contract is a **transcription**, not a new authority. Precedence (Owner kickoff §8,
recorded in `reference/governance/2026-10-09-owner-wp00-kickoff.md`):

1. Foundation v2.3 (`FND`)
2. MVP Contract v1.2 (`MVP`)
3. normative Requirements: `R00` (normative for R01–R04), `R01`–`R04` (Learning Profile; R04
   also shared persistence compatibility), `R05` (Agent Memory Profile)
4. Implementation Architecture Amendments v1.3 (`IAA`)
5. this normalized Markdown contract, after independent review
6. canonical conformance (`minion-memory/conformance/**`) for the finite cases it covers

If a requirement here disagrees with its cited sources, **the source wins** and the disagreement is
a `CONTRACT_ASSURANCE_DEFECT` against this tree. If sources disagree with each other, the semantic
decision stops and a finding is recorded (`assurance/findings/`), never resolved silently here.

Python is not Rust's oracle; Rust is not Python's. Minion-Agent is authoritative only for its own
side of the integration seam. Research projects, the Flashcard App, external memory providers and
the Implementation Pack are evidence or guidance, never authority.

## 2. Normalization rules

- Preserve upstream semantics and modal strength (MUST/SHOULD/MAY, FROZEN/PROVISIONAL, ...).
- No new semantics during transcription. Where a source is silent, the requirement says so and
  links a `REQUIREMENT_UNCERTAIN` finding instead of filling the gap.
- One requirement = one independently testable rule or one tightly coupled rule cluster
  (`process/requirement-id-convention.md` §4).
- Rules that several documents state are merged into one requirement citing every source. A
  merge never strengthens or weakens any source; where sources differ in strength, the note says
  which applies to what.
- Informative rationale (research citations, prior art) is not transcribed as requirements.

## 3. Requirement block format

```markdown
### CORE-001 — Title
<a id="core-001"></a>
- **Profile:** core | learning | agent · **Source status:** <status> · **Sources:** [FND §16] [R00 §10]

Normative statement.

*Note:* optional transcription note, finding links (NF-###).
```

- **IDs** are `FAMILY-NNN`, unique across the whole tree, never reused (`process/requirement-id-convention.md`).
- **Citations** are `[KEY §anchor]`. `KEY` is a document key from
  `reference/mneme-v2.3-source-bundle.yaml`; `anchor` is a section anchor from
  `reference/source-index.yaml` (derived mechanically from the DOCX headings: `4.1`, `G.3`, `A26`,
  `App-G`, else a heading slug; a repeated anchor gets `~2`). `mneme-process check` rejects any
  citation that does not resolve.
- **Source status** vocabulary: `FROZEN`, `PROVISIONAL`, `RESEARCH_CANDIDATE`, `MVP_ONLY`,
  `SCHEMA_RESERVATION`, `NOT_IN_MVP` (explicit Foundation/MVP labels), `NORMATIVE` (normative
  text that carries no explicit status label — requirement documents, unlabeled Foundation prose
  such as Appendix F "architecture constraints" and Appendix G, MVP §18), `GUARDRAIL` (an adopted
  IAA amendment with no stronger source). `FROZEN` is used **only** where a cited source places the
  requirement's main statement under an explicit FROZEN label. When a merged requirement has several
  labels, the label of its main statement is shown and any narrower label is stated in the text.

## 4. Families and files

| Family | Meaning | Profile | File |
|---|---|---|---|
| ARCH | cross-cutting architecture: admission rule, namespaces, seams, optional services | core | `core.md` |
| CORE | identity, version, provenance, lineage, operation identity | core | `core.md` |
| HIST | canonical history, order, append-only reinterpretation, information origin | core | `core.md` |
| PROJ | projection path, purpose-specific projection, ProjectionBudget | core | `core.md` |
| RET | retrieval/index primitives, progressive disclosure | core | `core.md` |
| SCOPE | MemoryScope | core | `scope.md` |
| PERS | persistence tiers, transactions, durability barrier, bounded history, ReplayCheckpoint | core | `persistence.md` |
| SER | schema versions, compatibility, decoding, profile/type identity | core | `serialization.md` |
| BKP | protocols, portable backup/restore | core | `backup.md` |
| PRIV | privacy, retention, minimization | core | `privacy.md` |
| KNOW | Knowledge model, RecallForm | learning | `learning/knowledge.md` |
| PKG | Knowledge Package import/reconciliation | learning | `learning/package.md` |
| LEARN | LearningEpisode / LearningEvent | learning | `learning/interaction.md` |
| OBS | RawObservation, exposure provenance | learning | `learning/interaction.md` |
| EVAL | EvaluationOutcome | learning | `learning/evidence.md` |
| EVID | MemoryEvidence, contamination, diagnostics | learning | `learning/evidence.md` |
| LMEM | LearnerMemoryModel, learner state | learning | `learning/inference.md` |
| SCHED | scheduling, RecallForm selection | learning | `learning/scheduling.md` |
| MIG | legacy Flashcard migration | learning | `learning/migration.md` |
| ACAP | AgentMemoryObservation capture | agent | `agent/capture.md` |
| AMEM | MemoryRecord | agent | `agent/records.md` |
| ACON | consolidation | agent | `agent/consolidation.md` |
| ARET | agent retrieval / ranking | agent | `agent/retrieval.md` |
| ACTX | AgentContextProjection, context fencing | agent | `agent/context.md` |
| MINT | Minion-Agent integration | agent | `agent/minion-agent-integration.md` |

The taxonomy is a WP-00 **proposal** (`process/requirement-id-convention.md` §2 records how it
differs from the kickoff and bundle candidates, and why).

## 5. Kickoff invariants A–V → requirements

| Kickoff invariant | Requirements |
|---|---|
| A canonical history is durable | HIST-001, PERS-001, PERS-002 |
| B derived state is rebuildable | HIST-001, PERS-001, LMEM-008, RET-002 |
| C lossy projections never replace history | HIST-001, PROJ-003 |
| D runtime events are not durable domain events | ARCH-010 |
| E raw fact and interpretation are distinct | OBS-001, EVAL-001, EVID-001, HIST-007 |
| F unknown != weak | SER-003, OBS-004, EVID-003 |
| G exposure provenance is preserved | HIST-010, OBS-006 |
| H recalled agent memory is not new observation | ACTX-004, ACAP-007 |
| I learner events never semantically deduplicated | HIST-008 |
| J same operation_id retry may collapse | CORE-012, PERS-006, ACAP-003 |
| K semantic similarity is never identity | CORE-013 |
| L reinterpretation is append-only/superseding | HIST-006, HIST-007 |
| M one shared projection/normalization path | PROJ-001 |
| N ReplayCheckpoint is an accelerator | PERS-009 |
| O bounded/incremental replay | PERS-007 |
| P exact identity precedes discovery | RET-001 |
| Q purpose-specific projection | PROJ-002 |
| R durable capture precedes enrichment | PERS-004 |
| S AI/embedding/remote not mandatory critical path | ARCH-008 |
| T no everything-is-a-plugin | ARCH-007 |
| U shared core requires no learner-specific semantics | ARCH-002, ARCH-003 |
| V agent simplification must not weaken learning evidence | ARCH-002, ACON-007 |
