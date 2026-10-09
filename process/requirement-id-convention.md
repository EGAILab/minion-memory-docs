# Minion-Memory — Requirement ID convention

**Status:** PROPOSED (WP-00), pending independent review.
**Adapted from:** Minion-Agent `process/requirement-id-convention.md` @ `8744bd0`.

## 1. Principle

Requirement IDs are **traceability identifiers**, not semantic definitions. The rule lives in the
upstream bundle and is transcribed in `spec/**`; for finite examples it is also executable in
canonical conformance. The ID is the join key for:

```text
upstream source (bundle KEY §anchor)
 -> normalized spec anchor (spec/<file>.md#<id>)
 -> canonical scenario(s)
 -> Python location
 -> Rust location
 -> assurance evidence
 -> disposition
```

(Minion-Agent's chain starts at Pi source → parity manifest. Mneme has no reference
implementation; the chain starts at the bundle.)

## 2. Families (validated in WP-00)

| Family | Scope | Notes on the decision |
|---|---|---|
| ARCH | cross-cutting architecture | **Added.** Admission rule, namespaces, seams, optional services, runtime-vs-durable events have no natural home in a data family. |
| CORE | identity/version/provenance/lineage/operation identity | kickoff + bundle |
| SCOPE | MemoryScope | kickoff + bundle |
| HIST | canonical history, order, append-only reinterpretation, information origin | kickoff + bundle |
| PROJ | projection path, purpose-specific projection, budget | kickoff + bundle (bundle folded checkpoints in; here they are PERS) |
| RET | retrieval primitives | kickoff `RET` chosen over bundle `RETR` |
| PERS | persistence, durability barrier, bounded history, ReplayCheckpoint | kickoff |
| SER | schema versions, compatibility, decoding | kickoff |
| BKP | protocols, backup/restore | kickoff |
| PRIV | privacy/retention | **Kept from the bundle** (kickoff omitted it). Privacy is FROZEN Foundation semantics (FND §17) and cross-profile. |
| KNOW | Knowledge model, RecallForm | kickoff + bundle |
| PKG | Knowledge Package import/reconciliation | **Kept from the bundle** (kickoff omitted it). R01 is a whole normative document; folding it into KNOW or MIG would hide it. |
| LEARN | LearningEpisode/LearningEvent | kickoff + bundle |
| OBS | RawObservation/exposure | kickoff |
| EVAL | EvaluationOutcome | kickoff + bundle |
| EVID | MemoryEvidence, contamination, diagnostics | kickoff; diagnostics folded in (R03 owns both) |
| LMEM | LearnerMemoryModel | kickoff `LMEM` over bundle `LMOD` |
| SCHED | scheduling/RecallForm selection | kickoff + bundle |
| MIG | legacy Flashcard migration | kickoff; scoped to learning legacy migration |
| ACAP / AMEM / ACON / ARET / ACTX | agent capture / records / consolidation / retrieval / context | kickoff split of the bundle's `AMEM`/`ACTX` |
| MINT | Minion-Agent integration | kickoff `MINT` over bundle `INT` (a future Flashcard adapter family can be added without renaming) |

Not used: bundle `LMOD`, `RETR`, `INT` (aliases recorded above). A family is added only through a
reviewed change to this table.

## 3. Form and location

- Form `FAMILY-NNN` (three digits, unique across the project).
- The requirement's home is a heading in `spec/**` with an explicit anchor:
  `### CORE-001 — Title` followed by `<a id="core-001"></a>` (`spec/README.md` §3).
- Every requirement has exactly one row in `minion-memory/mneme-contract-manifest.yaml`; the
  validator enforces the bijection and that the row's `sources` equal the spec block's citations.

## 4. Granularity

One ID = one independently testable rule or one tightly coupled rule cluster. Neither "everything
the scheduler does" nor one ID per field of one inseparable schema rule.

## 5. Stability

Once an ID appears in reviewed evidence: never reuse it, never renumber for aesthetics, mark removed
requirements `retired` with `superseded_by`, keep aliases during migrations. During WP-00 (before
any review) IDs may still be renumbered; the first reviewed normalization freezes them.

## 6. Conformance linkage

Every canonical scenario maps to ≥1 requirement ID. Every requirement reaching certification has
executable evidence: a canonical scenario, or an explicitly justified language-specific test.
