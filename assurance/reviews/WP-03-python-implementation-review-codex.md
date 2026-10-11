# WP-03 Python implementation review — Codex

Date: 2026-10-11. Independent reviewer / Rust owner: Codex.

## Verdict

**CHANGES_REQUIRED** for docs `0e4e1bceb1d4faf419cc161c82d2f24dc26fce4b` /
code `c86daf806fecb473c832ccecba5495b064b243ca`.

One blocking finding: **WP03-CR-006**, an implementation defect in unknown-required diagnostics.
G-070 requires the full routing identity; the error omits the profile. The implementation otherwise
matches the compared projection contract fields in the independent executions below. Passing
coverage and existing scenarios do not establish this omitted requirement.

## Custody and authority

Followed `process/handoffs/WP-03-codex-python-implementation-review.md` at control head `c2212b55`.
Review branch `review/wp03-python-1` starts there in `review-worktrees/docs-wp03-python-review`;
code is a separate detached exact-SHA checkout in `review-worktrees/code-wp03-python-review`.
The normative docs at the control head match the exact candidate. Only this record is committed.
No implementation/candidate, shared state, registry, source bundle or other agent worktree edits.
Every shell first sourced the project environment. Scratch copies, managed interpreters, caches,
coverage, test temporaries, Cargo output and the POSIX filesystem image stayed project-local.

Authority is the agreed docs `b514c16d` / code `619540ae`, G-067..G-075, and the previously
certified generic/admission seams. Read the full implementation and its diff, error extension,
Layer 02 helper contracts/code, new public-seam controls, runner and manifest changes, both complete
scenarios and the author evidence. The author record is not used as proof of conformance.

## WP03-CR-006 — Unknown-required projection errors omit the routing profile

- classification: **IMPLEMENTATION_DEFECT**
- owner_decision_required: **false**; the requirement is already explicit
- status: **OPEN**; raised_by: **Codex**; implementation owner: **Claude**
- blocking: **[WP-03]**
- requirements: **PROJ-001** (G-070)
- authority: G-070, `reference/governance/2026-10-11-owner-layer03-start.md:75`, and
  `spec/core.md:730–732` at docs `0e4e1bce`: the detail gives the routing identity
  **(profile, record_type, schema_version)**.
- implementation evidence at code `c86daf80`: `core/projection.py:168–169` forwards `str(stop)`;
  `core/history.py:111` constructs that stop with only type and edition;
  `tests/core/test_layer03_projection.py:82–87` checks type/edition but never profile.
  Code paths are beneath `minion-memory-python/src/minion_memory/` unless stated otherwise.

Executed this public-seam witness with each profile `p = learning` and `p = agent`:

```python
reader = {"profile": p, "recognized": []}
stream = {
    "store_id": "s-1",
    "entries": [{"position": 7, "record": {
        "record_id": "u", "profile": p, "record_type": "mystery",
        "schema_version": 4, "compatibility": "required",
        "recorded_at": "2026-10-11T08:00:00Z",
    }}],
}
project_history(reader, stream, [])
```

Both calls raise the same complete public attribute observation:

```text
code:     history.unknown_required
argument: None
position: 7
detail:   mystery v4 is required but not recognized
```

There is no profile/routing-identity attribute supplying the missing component either. Merely
knowing that a caller supplied a profile reader does not satisfy the explicit error-detail
contract. Position and atomic failure are correct; the missing identity component is the defect.

Reproduced **16/16 variants per platform**: two routing profiles times all eight native/JsonText
argument-seam combinations, on Windows and case-sensitive POSIX. The two profiles have identical
error observations, demonstrating that the diagnostic cannot distinguish their routing identities.
This is not a shell-escaping artifact or a hypothetical gap. No formatting preference is asserted:
any detail that faithfully identifies all three components can satisfy the requirement.

Required remediation: have the library-owned projection failure preserve the full normalized
routing triple, keep the no-argument convention and exact store position, and add a discriminating
public-API control that verifies the profile as well as type and edition. Include native and JSON
seams, more than one profile, and an unknown schema of a known type. The current named routing-
identity control must fail when the profile is omitted. Recheck early lineage errors still precede
this error and foreign-profile/ignorable records still terminate under the Layer 02 gates.

This does not reopen certified Layer 02: its public admission contract did not acquire the new
Layer 03 full-triple diagnostic requirement merely because the projector reused its internal stop.
There is no new Owner choice and no proposed production patch in this review.

## Whole implementation assessment

The joint generic pass precedes all typed checks. Reader and stream shape precede early lineage
checks; entries run in increasing store position. Canonical-envelope comparison happens after
admission and timestamp normalization, so repeated equivalent occurrences coalesce at their first
position and conflicting reuse fails before later entries or graph checks. Skip/excluded positions
advance the through-boundary without becoming available records. No semantic content similarity
deduplicates different IDs.

The three target variants remain typed; artifact targets are rejected early on resolution kinds.
Equal normalized relations collapse. Late checks require available sources and resolution targets,
reject record self-links, and check the resolution and derivation graphs separately and iteratively.
Unavailable derivations remain in both output lists, preserving their identities. Direct-only
interpretation membership and set-valued heads have no incidental selection. Result ordering uses
the specified first positions and typed target sort. No second profile payload decoder is invented.

The error position extension preserves code/detail/argument when cloning through `for_argument`
and `at_position`; defaults remain None for ordinary errors. Entry errors name stream; graph errors
name relations; unknown-required errors correctly name no argument. The identified profile omission
is the remaining exception to the new error contract.

The runner is thin: its new operation calls public `core.project_history` once and observes public
error attributes, including position. Python IMPLEMENTED_LAYER advances to 3 with this candidate.
The two scenario diffs change **DRAFT to ACTIVE only**; all 54 expectations are unchanged. Manifest
Python locations point to the production surface. Rust remains Layer 02 and reports Layer 03 as an
expected failure under the implemented-layer rule rather than claiming implementation.

## Independent executions beyond the authored scenarios

Driver: `.tmp/work/codex/wp03-python-probes.py`, using my own fixture-domain contract model from
contract review 3, not another language implementation or the author's projector as an oracle.
The model resolves cycles by iterative leaf elimination; production uses incoming-degree Kahn
elimination. Canonical-envelope equivalence in the model distinguishes booleans from numbers.
The generated domain uses valid routing/reader shapes, known UTC timestamps and small finite
payload numbers; it is not presented as an exhaustive arbitrary JSON decoder oracle.

On **each** platform:

- **432 public-seam controls**: every one of the 54 agreed expectations through all eight
  native/JsonText combinations, comparing complete projection results and code/argument/position.
- **12,000 deterministic generated cases**, including empty occurrence sets, decoded,
  skipped, excluded and unknown-required records, repeated identities with equal/conflicting
  complete content, relation repeats, all four kinds, missing endpoints, typed artifact targets,
  cycles and direct membership. Zero disagreements on the compared contract fields. These are
  the same 12,000 cases replayed on both platforms; diagnostics were checked separately, revealing
  CR-006 rather than being hidden by that result.
- Explicit stage-1/stage-2 failures in later arguments outrank earlier typed failures; reader
  shape outranks stream shape. Wrong artifact kind reaches early lineage failure before an
  unknown-required entry, not a late unavailable-target reading.
- Instrumented hostile dict/list/string subclasses produce the same result with **zero hooks**.
  Caller inputs remain unchanged, and mutating returned records does not mutate caller records.
- Equivalent integer/float payload spelling and offset/case timestamp spelling coalesce through
  canonical envelope comparison; conflicting complete content still fails at the later position.
- Error-cloning helpers preserve the new optional position and existing argument.
- CR-006's 16 missing-profile observations, including every argument seam.

Evidence JSON under `.tmp/work/codex/wp03-python-review/`:

| File | SHA-256 |
|---|---|
| independent-probes-windows.json | a13757e42a64fe01f9f826f0b2d06a69e973dfed9ffe898a78beab698a6d389b |
| independent-probes-posix.json | db65a0a0bf1091f38855af826bc88f25a84992c0efe29ea435f84a395793eeba |

## G3 gates and discrimination

- Windows managed CPython 3.12.8: **488 passed, 5 xfailed**.
- POSIX managed CPython 3.12.8, exact git archive on a project-local ext4/FUSE image:
  **488 passed, 5 xfailed**. Distinct `A` and `a` files proved case sensitivity. Test temporary
  paths were inside that image; the archive preserves the exact code candidate. No system Python.
- Independently reproduced coverage 7.16.2 over all minion_memory, with branch coverage,
  subprocess patching/combination, and no exclusions: **981/981 statements, 432/432 branches**.
  Report: `.tmp/work/codex/wp03-python-review/coverage.json`.
- Ruff check and format check: clean, **18 files**. Mypy `--strict .`: clean, **18 files**.
- Independent process check with `--deep-sources`: **8/8 PASS**.
- Rust `cargo test --locked --offline --test conformance`: **5/5 PASS**, including layer-promotion
  and runner controls for the newly ACTIVE scenarios. No Rust Layer 03 implementation is claimed.

Replayed the author's 12 disclosed violations in separate reviewer-owned package copies, verified
the imported module paths, and ran the conformance plus Layer 03 public-seam controls. The copied
unmodified baseline passes, and **12/12 disclosed violations are killed by runtime test failures**,
not syntax/import/collection failures. Evidence: `.tmp/work/codex/wp03-python-review/mutants/`.

Qualification: original Q07 also removes strict endpoint handling for reinterprets and is first
killed by a runtime KeyError on a dangling target, not by a cycle assertion. I therefore added a
narrower Q07 that omits only reinterprets cycle edges while preserving endpoint checks; the lineage
cycle oracle kills that by assertion too. This confirms the intended cycle discrimination instead
of crediting the broader mutant's unrelated failure alone. Q10 is killed specifically by
`test_artifact_target_on_a_resolution_kind_is_an_early_shape_error`, independently confirming the
author's correction of the initial survival claim. None of these results makes the missing-profile
requirement covered: the present identity test checks only two of its three components.

The overall first complete review found no other blocking implementation or contract issue.
Remediate CR-006 with its discriminating controls and return the exact candidate for targeted closure.
