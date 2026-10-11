# WP-03 — final review, targeted re-review 2 (Codex)

**Verdict: APPROVED**

**Exact candidate:** docs `c36e0f5cb6dc2e7e92327bb9db358af0cdd31995` / code
`dd55fb4f0abec262d7ba0dab64f28a74840b84c3`.
**Handoff:** `process/handoffs/WP-03-codex-final-review-2.md` at `84c768d1`.
**Reviewer:** Codex, independent reviewer and Rust implementation owner.
**Date:** 2026-10-11.
**Responds to:** final complete review `88b8bb3f8b30856a221f150b9c1ee8b635cf94e6`.

## Disposition

| Finding | Classification | Disposition |
|---|---|---|
| WP03-CR-007 — incomplete and stale Rust assurance handoff | CONTRACT_ASSURANCE_DEFECT; no Owner decision required | CLOSED |

Open findings: **none**. CR-001…006 remain closed. This approval is of the exact pair and does
not itself accept it onto main, implement Rust, or certify cross-language closure.

## Documentary closure

Read the response as a review object, then independently checked the changed plan and matrix
against the agreed text, the previous finding, actual evidence and the mandatory template.

The plan is now a current assurance index through G-075, with the contract review trail, Python
implementation and remediation trail, and the final review. Its current behavior summary correctly
states coalescing of identical canonical records, collapse of equal normalized relations, typed
external targets, strict resolution endpoints, retained unresolved derivations, independent graph
families and direct-only interpretation membership. Superseded first-draft proposals are explicitly
historical and mapped to their deciding governance. Both ACTIVE scenario inventories are correct:
**18 canonical-path + 36 lineage steps**.

The matrix now supplies the material missing audit:

- Closed versioned/hash artifact alternatives, their CORE-001/002/011 domains, cursor and edition
  bounds, and the separate optional store-error position.
- Reviewed lower-layer generic staging, reader validation, admission, timestamp normalization,
  canonical bytes and token/edition seams; the required Rust position extension is additive.
- Member-level dispositions for the touched hazard families, with inherited Layer 01/02 evidence
  explicitly limited to unchanged seams. Whole-family N/A dispositions for H8–H10 are appropriate
  because this layer has no persistence, paths, retry or concurrency. Pagination is explicitly
  deferred to Layer 05 with its trigger.
- Presentation ordering, canonical equality, reference integrity and diagnostic neighborhoods,
  with identifiable scenario/test references and the independent review executions.
- The early-shape versus late-graph oracle and paired-entry Q10 witness: an artifact target on
  `supersedes` must fail as early `lineage.invalid`, before an unknown-required entry. The matrix
  also identifies late-endpoint and conflicting-record controls.

I checked the named public controls in `test_layer03_projection.py` and their actual assertions,
the referenced scenario cases, and the prior review objects. Q10's intended control exists and
was independently killed at the exact code in the final review. The separate record, versioned
artifact and hash target forms can be represented losslessly in Rust; the matrix introduces no
new semantic restriction or Owner choice.

Two evidence descriptions need precise interpretation, recorded here rather than credited as
additional executions:

- The neighborhood summary's H5 “all 5” includes the explicitly deferred pagination member.
  Pagination has **not** been probed; the checklist's DEFERRED_WITH_REASON disposition governs.
- The H1 lexical-form row cites the canonical-path gaps step for `2.0`, but that step actually uses
  integer positions 2, 5 and 9. Its generic normalization claim is supported by the inherited seams
  and the fresh direct probes below; that scenario is evidence for gaps, not floating spelling.

These do not leave a domain or implementation decision unsupported: the explicit deferral and
the independently executed normalization evidence supply the required dispositions. No blocking
assurance gap survives.

## Delta and verification

Compared the pinned docs trees `6fe9115d` and `c36e0f5c`. Changes are the plan and matrix, response,
imported prior final review, handoffs and coordination state. **Spec and governance are unchanged.**
The code checkout remains exactly `dd55fb4f` and clean, so the corpus, expectations, runner and
production modules are unchanged. The review branch starts from the handoff's state-only descendant;
its only committed addition is this record.

Fresh independent process check using the candidate tooling and the exact code:
`mneme-process check --deep-sources`: **8/8 PASS**.

Fresh project-local CPython 3.12.8 public-API probes:

- Positions `2`, `2.0`, `2e0` normalize identically to integer 2.
- Three integer/decimal/exponent spellings of `9007199254740991` are accepted as exact integer
  cursors; the corresponding three spellings of `9007199254740992` fail at generic stage 2 with
  `value.integer_out_of_range`, argument `stream`, and no entry position.
- Integral `schema_version=1.0` normalizes to an exact built-in integer.
- Complete envelopes with equivalent offset/case timestamp spellings and integral numeric payload
  spellings coalesce, retaining the first record and later duplicate position.
- Independently parsed both scenario documents: ACTIVE, 18 and 36 steps.

Driver and observations: `.tmp/work/codex/wp03-final-2-audit.py` and
`.tmp/work/codex/wp03-final-2-audit.json`.

The final complete review's G3 at this **same unchanged code** remains applicable: Windows and
case-sensitive POSIX each **496 passed, 5 xfailed**; **985/985 statements and 432/432 branches**,
no exclusions; Ruff/format and strict mypy clean; Rust conformance **5/5 PASS** at declared layer 2.
Its 360 early/late seam comparisons per platform, 432 canonical public-seam comparisons per
platform, 12,000 deterministic generated cases replayed on each platform, routing witnesses and
exact-code mutation controls remain evidence. Those broad executions were not repeated for a
documentation-only repair.

No production, state, registry, source-bundle or author-owned file was edited. All scratch probes
and caches remained under the project root, with the project environment sourced before shell work.
The candidate is ready for coordinator acceptance under the recorded authority and the subsequent
Rust implementation handoff.
