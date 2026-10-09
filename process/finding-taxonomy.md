# Minion-Memory — Finding taxonomy

**Status:** PROPOSED (WP-00), pending independent review.
**Adapted from:** Minion-Agent `process/agent-workflow.md` §6 and `process/implementation-conformance-workflow.md` §4 @ `8744bd0` (see `reference/minion-agent-process-adoption.md`).

Every material issue carries **exactly one classification**. Escalation to the Owner is a separate
flag (`owner_decision_required`), not a classification, except for pure governance choices
(class 7). Do not invent softer labels to avoid a blocker.

## 1. Classes

| # | Class | Meaning | Required action | Risk-register debt? |
|---|---|---|---|---|
| 1 | `REQUIREMENT_UNCERTAIN` | The authoritative bundle is silent, ambiguous or self-contradictory for a semantic decision. (Replaces Minion-Agent's `PI_BEHAVIOR_UNCERTAIN`: the authority is the Mneme bundle, not Pi.) | Stop that semantic decision. Record the exact source text, interpretations, affected requirements, recommendation. Resolve by authority reading, or by Owner decision when sources conflict or are silent on a semantic choice. | No |
| 2 | `CONTRACT_ASSURANCE_DEFECT` | Our normalized spec, manifest, conformance, process or evidence is incomplete, contradictory, unfaithful to its sources, or insufficient for independent implementation. | Repair before certification. | No |
| 3 | `IMPLEMENTATION_DEFECT` | One implementation violates the reviewed shared contract. (Replaces `PI_PARITY_DEFECT`.) | Fix before certification. | No |
| 4 | `CROSS_LANGUAGE_CONFORMANCE_DEFECT` | Python and Rust disagree on a canonical scenario or contract-observable behavior, or one language cannot represent a contract value the other can. | Reproduce independently against the contract; then either an `IMPLEMENTATION_DEFECT` in one language, or a contract gap (class 1/2). Never resolved by copying the other language. | No |
| 5 | `INTEGRATION_CONTRACT_DEFECT` | A consumer seam (Minion-Agent, Flashcard App) does not provide, or contradicts, what the Mneme integration contract assumes. Minion-Agent is authority only for its own side. | Characterize at a pinned consumer revision; adjust the Mneme adapter contract, or request a consumer-side extension through that project's own process; Owner decision when it changes scope. | No |
| 6 | `SEMANTICS_NEUTRAL_HARDENING` | Quality improvement that preserves contract-observable semantics (security, robustness, diagnostics, documentation accuracy). (Replaces `PARITY_NEUTRAL_HARDENING`.) | Normally fix in the current phase. | No |
| 7 | `OWNER_DECISION_REQUIRED` | A governance choice among valid options with no defect: priority, scope, layer order, product trade-off, process exception. | `BLOCKED_FOR_OWNER` for the affected decision only. | No |
| 8 | `CONTRACT_CONSTRAINED_RISK` | A real production risk whose fix would change reviewed contract semantics, and the contract is not wrong. (Replaces `PARITY_CONSTRAINED_RISK`.) | Keep the contract; record in `assurance/risk-register.md` with the future decision path; Owner decides any change. | Yes |

Class 8 is a WP-00 refinement beyond the kickoff's seven: without it, "the contract is right but
risky" has no honest home, and Minion-Agent's experience is that such items otherwise get
mislabeled as hardening.

## 2. Classification order

```text
Is the authority (bundle) unclear/silent/contradictory for this decision?   -> REQUIREMENT_UNCERTAIN
Is our spec/manifest/conformance/evidence/process unfaithful or incomplete? -> CONTRACT_ASSURANCE_DEFECT
Is it a consumer seam mismatch?                                             -> INTEGRATION_CONTRACT_DEFECT
Do the two implementations disagree, or can one not represent a value?      -> CROSS_LANGUAGE_CONFORMANCE_DEFECT
Does one implementation violate the reviewed contract?                      -> IMPLEMENTATION_DEFECT
Otherwise: does the fix preserve contract semantics?   yes -> SEMANTICS_NEUTRAL_HARDENING
                                                        no -> CONTRACT_CONSTRAINED_RISK
Pure governance choice with no defect?                                      -> OWNER_DECISION_REQUIRED
```

## 3. Finding record

Machine-readable registers live in `assurance/findings/*.yaml` and are validated by
`mneme-process check findings`.

```yaml
- id: NF-001                      # unique across the project; never reused
  title: ...
  classification: REQUIREMENT_UNCERTAIN
  owner_decision_required: true|false
  blocking: [WP-00 | WP-01 | Layer-NN | none]   # what it blocks; "none" when it blocks nothing now
  status: OPEN | PROVISIONALLY_CLOSED | CLOSED | WITHDRAWN
  raised_by: Claude | Codex | Owner
  sources: ["[R01 §3]", "[R00 §11]"]            # exact authority locations
  requirements: [PKG-001]
  summary: ...
  interpretations: [...]          # for classes 1, 5, 7
  recommendation: ...
  resolution_layer: "12"          # the layer whose contract must resolve it
```

## 4. Independence of findings

- A finding raised by Codex does not become accepted truth. Claude independently reproduces and
  classifies any shared-contract finding before changing the contract. Likewise Codex may
  challenge any Claude finding.
- Reviewer factual-evidence rule (Minion-Agent §9.2.1, adopted): a blocker cites the exact
  content-addressed source (bundle `KEY §anchor` with the bundle SHA-256, or a pinned commit) and a
  minimal discriminating witness when executable. A suspicion without evidence is filed as a
  **question**, not a blocker.
- Executable closure needs a negative control killed by its intended witness (agent-workflow §9).
