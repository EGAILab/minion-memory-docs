# WP-01 Python targeted closure 2 — Codex

## Verdict and objects

**CHANGES_REQUIRED** for docs `81192e3adf29ef474ce1ecdd0096bb306543a5ae` paired with
code `eb47635c6ea997f030d04b8099366044a2f702aa`.

Handoff: `process/handoffs/WP-01-codex-implementation-review-2.md`, state
`1443e3fab7c7d2fe599c964b7e56231a1f0bbfb7`. Record branch: `review/wp01-python-2`, based on
that state. Separate detached checkouts of the exact pair were reviewed; both SHAs are ancestors
of the named `wp01/contract` refs. No candidate or production file was edited.

Scope: the G-035/G-036 contract delta, PY-001..007 repairs, their semantic dependencies and direct
regressions. The response record was a review object, not evidence of closure. Classification
follows `process/finding-taxonomy.md`. The original witnesses are repaired, but PY-004 survives
in its accepted-native-number diagnostic neighborhood, which also exposes PY-008.

## Contract delta and per-finding disposition

The contract delta is approved as contract text. CORE-003 faithfully transcribes G-035's closed
record, shape-before-fields rule, `artifact.revision_invalid`, canonical typed-field order, generic
error precedence and fully validated absent-version outcome. SER-008 faithfully transcribes
G-036's list/tuple binding and excluded other sequences. Its stages-across-arguments statement
faithfully expresses G-031/G-034 and the path-A reading used in PY-001. No new Owner choice was
found in these transcriptions.

| Finding | Disposition | Own evidence |
|---|---|---|
| WP01-PY-001 | Provisionally closed | All three comparison primitives select later stage-1 failures before earlier stage-2 failures, across native, JSON and mixed arguments. The runner now constructs `JsonText` wrappers and delegates combined validation to the library. |
| WP01-PY-002 | Provisionally closed | All six permutations of the invalid revision record report `version.invalid` before the invalid ID. Shape failures correctly precede these fields under G-035. |
| WP01-PY-003 | Provisionally closed | Original three witnesses and representation/escape neighborhoods pass: earlier duplicate/escaped-surrogate defects beat later invalid UTF-8/raw surrogates, and the reverse order retains `value.invalid_json`. Valid surrogate pairs still decode. |
| WP01-PY-004 | OPEN, refined witness | Huge integers and deep wrong-type arrays now retain their stable errors. A float subtype already admitted by the native-kind check still makes error construction invoke arbitrary `repr` and leak a host exception; details below. |
| WP01-PY-005 | Closed for the contract checkpoint; implementation provisionally closed | G-035 supplies the formerly unresolved choice. Shape, extra/missing members, non-object inputs, null present version, generic errors before shape, and full validation before `not_applicable` all reproduce. Historical classification remains REQUIREMENT_UNCERTAIN/path C, resolved by the Owner. |
| WP01-PY-006 | Closed for the contract checkpoint; implementation provisionally closed | G-036 supplies the binding. Nested tuples normalize as arrays, preserve index order and canonicalize identically to lists. Range, iterators, UserList, deque, bytearray and memoryview remain unsupported at the generic seam. Historical classification remains REQUIREMENT_UNCERTAIN/path C, resolved by the Owner. |
| WP01-PY-007 | Provisionally closed | All seven raw corpus digests are independently recomputed; additional bytes/bytearray/memoryview probes agree with SHA-256. Structured string hashing retains JSON quotes. |

The numeric-subtype witnesses below belong to the touched `_number`, normalization and diagnostic
surface. They are not unrelated domain expansion: the candidate's own native-kind check already
admits `int`/`float` instances of these subtypes, whose underlying numeric values are unambiguous.

## Own executions

Evidence is under `.tmp/work/codex/wp01-python-review-2/`; reviewer-authored drivers are
`wp01-python2-oracles.py`, `wp01-python2-probes.py`, `wp01-python2-refined.py`,
`wp01-python2-check.py` and the POSIX shell drivers under `.tmp/work/codex/`.

| Execution | Result | Evidence |
|---|---|---|
| Exact candidate suite, Windows | 83 passed, 5 placeholder xfails | `windows-tests.log` |
| Exact candidate suite, case-sensitive POSIX | 83 passed, 5 placeholder xfails | `posix-tests.log`, `posix-tests.xml`, `posix-host.json` |
| Independent corpus oracles | 146/146 expectations match across all eight ACTIVE Layer 01 scenarios | `oracles.json` |
| Original witnesses and direct neighborhoods | 105/105 assertions pass on Windows and Linux, with identical observations | `windows-probes.json`, `posix-probes.json`, `summary.json` |
| Refined accepted-number witnesses | Three contract mismatches reproduce on both hosts | `windows-refined.json`, `posix-refined.json` |
| Independent replay of candidate remediation controls on old `f10c7b4f` | 29 failures, 7 preservation passes | `negative-tests.log` |
| Refined witnesses on old `f10c7b4f` | Same three failures: these are surviving/pre-existing neighborhood defects, not falsely claimed new regressions | `negative-refined.json` |
| Corpus preservation and quoting | All 129 prior ACTIVE steps and expectations remain exact prefixes; placeholder unchanged; corpus Git delta contains zero deleted lines | `summary.json`; Git diff `f10c7b4f..eb47635c` |
| Mechanical checks | sources, spec, manifest, conformance and findings: 5/5 pass with deep source verification | `mechanical.log` |

The independent oracle uses its own source-order decoder, generic validation and typed rules;
it does not call Mneme or Claude's generator. Canonical bytes use `rfc8785` 0.1.4; raw digests
use `hashlib` over independently decoded hex. Counts: 13 positive canonical byte/hash cases,
21 value rejections, 15 revision comparisons, 19 operation-identity results, 7 raw hashes,
16 stable-ID results, 43 timestamps and 12 version results. No supplied expectation mismatch
was found. Parsed-corpus preservation plus the YAML profile gate confirms the quoting changes
did not change old meanings. I checked the generated corpus and did not run the author's generator.

The negative replay uses the candidate's unchanged remediation test file with the old package
selected through `PYTHONPATH`. Failures due to absent `JsonText`/`raw_content_hash` are capability
checks, not behavioral kills. Other failures discriminate old behavior, including binding choices
now specified by G-035/G-036; the seven passing controls are preservation evidence. This matches
the response's distinctions rather than crediting every failure as a repaired old-contract defect.

Both hosts used healthy project-managed CPython 3.12.8. For the suite, the exact code archive was
extracted into a project-local ext4 image; separate `A`/`a` files proved case sensitivity. The
105 probes also ran against that archive. The later refined Linux probes imported the same exact
detached checkout directly. All images, caches, dependencies, temporaries and outputs stayed
under this project on E:. The POSIX mount was successfully unmounted after returning its shell
to the project root. No system-Python repair or production edits were performed.

## Remaining blocking findings

### WP01-PY-004 — Accepted numeric subtypes still leak host exceptions during diagnostics

- **Classification:** `IMPLEMENTATION_DEFECT`; **severity:** high; **blocking:** WP-01.
- **Path:** A (SER-008/G-031); **owner_decision_required:** false; **status:** OPEN.
- **Pinned code:** candidate `core/errors.py:26–37`; `core/values.py:263–277,313–328`.
- **Executed evidence:** `windows-refined.json`, `posix-refined.json`, `negative-refined.json`.

Minimal executable witness:

```python
class BadDescription(float):
    def __repr__(self):
        raise RuntimeError("application float repr was called")

core.validate_value(BadDescription(float("inf")))
```

Actual: the application `RuntimeError` escapes. Required: `MnemeValidationError` with
`value.number_not_finite`. The stage-1 check admits the value as a float; generic validation
correctly identifies infinity, but `describe` calls the subtype's arbitrary `repr`. The original
huge-integer/deep-array fixes hold, yet the claim that diagnostic construction never replaces a
stable rejection remains false. This is the same material PY-004 finding, not a new ID for it.

**Required repair:** ensure diagnostics on admitted numeric values cannot invoke subtype display
hooks or replace the stable code. Sweep the accepted scalar-binding neighborhood, not only this
class. Add a discriminating control that first fails on this exact candidate.

### WP01-PY-008 — Admitted numeric subtypes serialize their display text instead of their values

- **Classification:** `IMPLEMENTATION_DEFECT`; **severity:** high; **blocking:** WP-01.
- **Path:** A/B (SER-008 numeric interpretation, G-023, SER-009).
- **owner_decision_required:** false; **status:** OPEN.
- **Pinned code:** candidate `core/values.py:313–350,430–440`.
- **Executed evidence:** refined logs above; identical old-candidate observations.
- **escalation_condition:** a proposed repair that newly rejects these admitted numeric subtypes
  instead of preserving their underlying numeric values is a native-binding acceptance choice and
  must be routed to the Owner as path C.

Minimal executable witnesses:

```python
class DisplayFloat(float):
    def __repr__(self):
        return "2.5"

class DisplayInt(int):
    def __str__(self):
        return "2"

core.canonical_bytes(DisplayFloat(1.5))  # actual b"2.5"; required b"1.5"
core.canonical_bytes(DisplayInt(1))     # actual b"2"; required b"1"
```

Both values pass the candidate's kind/domain checks. Normalization retains their numeric
subtypes, and `_format_number` then trusts overridden `repr`/`str`. Their underlying binary64
and exact-integer values are 1.5 and 1; display methods are not Mneme numeric semantics. The
result silently changes canonical content and consequently hashes and revision comparisons.
Built-in-number random/reference tests cannot kill this behavior.

**Required repair:** normalize admitted native numbers to trusted numeric representations and
derive bytes from the checked numeric values, preserving the established domain. Characterize
accepted scalar subtypes and their conversion/display hooks together with PY-004; do not repair
this by special-casing the two example classes.

## Convergence check and next coordination step

Trigger A has fired for PY-004: the same material stable-error/diagnostic finding survives the
initial independent implementation review `716d7218` and this independent targeted closure.
That is already two reviews, not merely approaching the threshold. The refined witness narrows
the remaining surface to admitted native scalar normalization, diagnostics and serialization.
PY-008 is one successor on that surface; two successor findings after remediation (trigger B)
are not established here. This targeted review must not be counted as a rejected complete review
for trigger C; three rejected complete contract reviews are not established by these records.

Under `process/agent-workflow.md` §6 and the adopted pin's §11.8, Claude must record the mandatory
trigger assessment before another remediation pass. Convergence is the default once A fires;
ordinary targeted repair instead requires an explicit reason grounded in the remaining surface.
Codex does not select the next project phase or amend coordination state in this review.

Close PY-004 and PY-008 before implementation certification or acceptance. The other findings'
provisional closures stand; no second complete work-package review is requested by this record.
