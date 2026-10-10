# WP-02 final complete review - Codex

Date: 2026-10-11. Independent reviewer / Rust implementation owner: Codex.

## Verdict

**CHANGES_REQUIRED** for docs `d603683a67243cb60d6c747e6d6afb5192634076` /
code `43e0984e585975719231ba53466a9c78eba796e7`.

One new blocker: **WP02-CR-007**, Python's DRAFT-plus-placeholder reason omits the
layer required by the shared NF-026 rule. It is a runner reporting defect, not a
history implementation defect. WP02-CR-001..006 remain closed; no prior semantic
closure is reopened. Do not close NF-026 or accept this pair on this verdict.

## Custody and complete scope

Read the final-review handoff at state head `8daa4f74`. New docs branch
`review/wp02-final` starts there in `review-worktrees/docs-wp02-final`; the clean
separate code checkout `review-worktrees/code-wp02-python-review-2` remains at the
exact candidate SHA. Only this record is committed. Candidate contents, process
state, registry and other worktrees were not edited. Scratch fixtures and caches
remain project-local; each shell first sourced the project environment.

Read the whole WP-02 contract, inherited value/time constraints, verbatim G-047..G-055,
all four scenarios, manifest, README runner policies, both runner implementations,
Python history module/exports/tests, feasibility matrix, plan, registry, state and
assurance trail. The docs state-only descendants add handoffs and state updates,
not a new content candidate. This is the one final complete review at the stated pair.

## Contract and authority

HIST-001/002/005/010 and SER-005/006 are consistent when read with the ordered generic
stages and explicit G-055 stage-3 gates:

- G-047 splits MemoryScope into WP-02S and keeps positions local cursors, never causal
  or global order; no WP-02 dependency on WP-02S is invented.
- G-048 closes only recognized envelopes; unrecognized pairs terminate at compatibility.
- G-049 requires recorded_at, treats missing occurred_at as unknown and present null as
  invalid, and imposes no clock relation between the timestamps.
- G-050 excludes other profiles after valid routing identity, before compatibility,
  recognized-schema shape or typed fields. Generic stages still run first over all inputs.
- G-051 defines same-store ordering and whole-pair equality; cross-store order is an
  argument-free error, while equality is false.
- G-052 fixes token/type/schema identity domains, including edition >=1.
- G-053 requires closed duplicate-free readers before internal set membership.
- G-054 fixes position 0..2^53-1, with 0 before the first physical record.
- G-055 fixes routing, admission/recognition, shape, then canonical typed-field order.

The later-stage table does not override these explicit early-termination gates. All
reader/record or a/b error naming is specified. Payload/provenance are exact normalized
SER-008 values; no shared origin vocabulary or profile payload schema is invented.
HIST-001 rebuildability and derived-artifact replacement behavior remain consumer
obligations in Layers 03-05, not capabilities falsely claimed by this pure envelope API.
No unrecorded path-C choice or new Rust representability gap was found.

## Corpus and traceability

The four scenarios are ACTIVE, with **70 steps**. Re-executed the independent
contract oracle against this exact corpus: **70/70** full expectations derive from
the normative text. Their only change from the agreed contract corpus is promotion
from DRAFT to ACTIVE; the 11 contract-remediation controls remain present. Manifest
spec/scenario links and Python locations are valid; Rust history locations remain
unset because Layer 02 Rust has not yet been implemented.

Exact checkout-pair `mneme-process check --deep-sources`: **8/8**. The corpus is
shared unchanged between the runners. Future DRAFT and above-language-layer scenarios
must be explicit xfails; the new permitted-input witness below shows one reporting
edge where Python falls short. No successful xfail is counted as implementation evidence.

## Python implementation and G3

Reviewed the entire history module against the contract: generic stages across all
arguments, closed reader and duplicate aliases, four envelope gates, typed canonical
order, timestamp normalization, preserved payload/provenance, copied normalized
outputs, store-local boundary relations and argument errors. The runner's three
history operations each call one public function and expose its observation; they
implement no history semantics.

Retained the independent exact-code evidence executed immediately before this final
review in `cb439331` rather than rerunning unchanged successful suites:

- Windows and case-sensitive native POSIX suites: **435 passed, 5 xfailed** each.
- Windows lint/format and strict mypy: clean, 14 files.
- Coverage 7.16.2, branches/subprocesses/no exclusions: **740/740 statements and
  332/332 branches**, every module 100%.
- New canonical-order controls: candidate **49 passed**; P12 **9 failed, 40 passed**.
  Original mutation replay: **12/12** killed by intended assertions.

The full earlier review also executed 24,192 admission and 5,202 boundary observations
against independent contract models on Windows/POSIX, plus 22 native/depth/precedence
controls with zero hooks. Python production is byte-identical to that reviewed code.
These are finite witnesses plus inspection, not an exhaustive proof. P12's corrected
record preserves the historical claim and explicitly withdraws it; CR-006 stays closed.

## Rust integration and readiness

Re-executed at this exact code on Windows and native WSL Linux:
`cargo fmt --check`, locked/offline clippy all targets with warnings denied, full tests,
and documentation with warnings denied. All pass: **18 integration tests and 1 doctest**
on each platform. Corpus reports **8 executed ACTIVE / 146 steps / 9 explicit xfails**:
the four Layer 02 ACTIVE scenarios name layer 02, Rust and implemented layer 01;
the five remaining placeholders name their rule.

Rust source/tests are byte-identical to independently approved NF-026 `b9f42d42`.
Its declaration and promotion controls pass, including DRAFT with a placeholder
naming the layer. That approval is not reopened by a defect in the Python runner.

Rust Layer 02 can be built from this text and corpus alone. Use the existing staged
Input/Value validation over reader then record or a then b; validated normalized
integers fit the declared bounds without casts from unchecked floats. Use exact
profile/token comparison, reject reader pair duplicates before set conversion, run
explicit gates, and reuse the accepted timestamp grammar/normalizer only at gate 4.
Canonical member order must hold even for decoded JSON insertion order. Preserve
arbitrary nested payload/provenance through the flat arena without recursive traversal.
The three result outcomes and boundary relation errors require ordinary typed Rust
representations, not a contract change. Python is not the Rust semantic oracle.

## WP02-CR-007 - Python placeholder detection suppresses the required DRAFT layer reason

- **classification:** IMPLEMENTATION_DEFECT
- **owner_decision_required:** false
- **blocking:** WP-02 final acceptance / NF-026 closure
- **status:** OPEN
- **authority:** code `43e0984e`, `conformance/README.md:37-40` (every DRAFT xfail
  reason references the rule and its scenario layer).
- **implementation:** same commit, `minion-memory-python/tests/conformance/test_canonical.py:118-122`.

The runner calls `_has_placeholder` and xfails before testing DRAFT status. For a
DRAFT that also contains a legal `TO_BE_` string, the reason is exactly:

```text
TO_BE_ placeholder scenario (conformance/README.md)
```

It omits the owning layer. This is not an invalid ACTIVE placeholder: DRAFT plus
placeholder is permitted by the schema and mechanical policy. Rust already reports
DRAFT with its layer in this case, as its passing control demonstrates.

Minimal witness: copy the actual `core.history.replay-compatibility` scenario,
change status to DRAFT, and set `given: {note: TO_BE_CONTEXT}`. Leave its layer 02,
identity, requirements, operations and expectations intact. Executed in an isolated
scratch corpus with the unchanged manifest: **manifest and conformance 2/2 PASS**.
The candidate Python runner xfails with the layer-free reason above. The same draft
without the note reports `DRAFT scenario, layer 02 contract not yet reviewed (...)`.
A direct diagnostic assertion gives **1 passed / 1 failed**, failing only for the
DRAFT-plus-placeholder case. Both paths still xfail; no false memory result is alleged.

Required repair: ensure every DRAFT reason includes its layer even when a placeholder
is present, while retaining explicit expected-failure and rule reporting. Add durable
controls for the combined and ordinary cases and preserve ACTIVE execution/implemented-
layer behavior. This needs no new semantic decision or production history change.

Reproduction: `.tmp/work/codex/wp02-final-runner-probe.py`,
`wp02-final-runner-fixture.py`, and `wp02-final/test_draft_reason.py`; permitted scratch
corpus is `wp02-final/fixture-code`. Only scratch copies were changed.

## Records and limits

The control state correctly names FINAL_CONTRACT_REVIEW and the exact pair, keeps the
six review findings provisional pending acceptance, and retains NF-016/NF-026 until
acceptance. Registry AGREED / Python IN_PROGRESS / Rust NOT_IMPLEMENTED is not
certification. G-009 acceptance authority exists, but this negative verdict does not
activate acceptance.

The feasibility matrix's behavioral rows are current through G-055; its DRAFT/round-2
heading and NF-026 prerequisite describe its authoring stage. The plan's Contract draft
paragraph still reports the initial 59 DRAFT steps and its assurance index stops at
the first implementation record; the README's Current contents (WP-00) paragraph is
also historical. Current inventory is 12 ACTIVE scenarios, 216 total ACTIVE steps,
with Python implementing both layers and Rust one. Refresh these progress/index
summaries with the next content candidate. They do not contradict the normative
schema, domains or ordered gates and are not additional blockers here.

No implementation, state transition, registry update, main acceptance or Rust Layer 02
work was performed. Review artifacts and verified full-suite evidence remain under
`.tmp/work/codex/`; the final corpus oracle is `wp02-final-derive.py` with
`wp02-final/corpus-derived.json`, and the Linux Rust gate recipe is
`wp02-final-rust-linux.sh`.
