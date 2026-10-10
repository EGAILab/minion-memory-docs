# WP-01 Python Layer 01 implementation review — Codex

## Verdict and objects

**CHANGES_REQUIRED** for docs `4c27bd5c5183658f589e0d856adc9b5c641dd1ad` paired with
code `f10c7b4f1c22b4daed4b6bc2f05028b5467a6ce9`.

Contract authority: the agreed docs `62adec5fde8575818aa19f3c4025acc78a7240a5` / code
`860e91c1bfb08e834c1a62b0f1fc32dd4bfd7efd`, including G-031/G-034. Handoff: docs state
`14c74d932343591a9af4718e57ac5188e0b3c43f`. Record branch: `review/wp01-python-1`, based on
that state. Review used separate detached checkouts of the exact candidate pair; no production
or candidate file was changed. Classification follows `process/finding-taxonomy.md` §1.1.

The passing suite does not certify the contract: independent counterexamples expose incorrect
error precedence, traversal and rejection behavior, and implementation readings still require
resolution. Claude's implementation record was reviewed, not treated as closure evidence.

## Executed evidence

All evidence and drivers are project-local, under `.tmp/work/codex/`:
`wp01-python-probes.py`, `wp01-python-extra.py`, the POSIX shell drivers, and
`wp01-python-review/` outputs. Healthy project-managed CPython 3.12.8 was used on both hosts.

| Own execution | Result | Output in `wp01-python-review/` |
|---|---|---|
| Exact candidate Python suite, Windows | 46 passed, 5 placeholder xfails | `windows-tests.log` |
| Exact code archive, case-sensitive POSIX filesystem | 46 passed, 5 placeholder xfails | `posix-tests.log`, `posix-tests.xml`, `posix-host.json` |
| Independent public-API counterexamples and reading probes | The current 13 probes have matching Windows/Linux observations; nine fail the stated contract/capability expectation, four record implementation readings rather than establishing their authority | `windows-probes.json`, `posix-probes-current.json` |
| Initial Linux probes against the same case-sensitive archive | First 11 probes reproduce, including both host exceptions | `posix-probes.json` |
| Independent ECMAScript number-format challenge | 100,000 admitted finite binary64 samples match Node v22.15.1 `JSON.stringify`; no formatting mismatch found | `extra-results.json`, `extra-summary.log`, `node-numbers.json` |
| Runner mixed-stage witness | Reports stage-2 overflow before the second JSON argument's stage-1 duplicate | `extra-results.json` |
| Mechanical checks | sources, spec, manifest, conformance and findings: 5/5 pass with deep source verification | `mechanical.log` |

POSIX: Ubuntu under WSL, Linux 6.18.40.1. The suite's source and corpus were extracted with
`git archive` of the exact code SHA into an ext4 image stored inside this project's temporary
directory. Distinct `A` and `a` files were created and read to prove case sensitivity. Python,
dependencies, caches, temporary files, image and mount all stayed under the project root on E:.
The initial export attempt failed because Windows worktree pointers are not Linux Git paths;
the successful export used the main repository's object database. The test command passed;
an exit-trap unmount was busy because its shell remained inside the mount. The reviewer-owned
FUSE process was subsequently stopped. This cleanup issue did not affect the test results.

The serializer differential is against the actual ECMAScript runtime, independently of the
Python `rfc8785` reference used by the candidate's own random tests. It supports feasibility,
not an exhaustive proof of every binary64 serialization. No production serializer defect was
found by these checks. Timestamp grammar/range and the supplied canonical scenarios pass.

## Blocking findings

All findings below are OPEN and block WP-01 implementation certification.

### WP01-PY-001 — Stage 2 in an earlier argument hides stage 1 in a later argument

- **Classification:** `IMPLEMENTATION_DEFECT`; **severity:** high.
- **Path:** A (G-031/G-034); **owner_decision_required:** false.
- **Pinned code:** `core/identity.py:22–31`; runner `tests/conformance/test_canonical.py:74–78`.

`compare_versions(float('inf'), b'x')` reports `value.number_not_finite`, argument `a`.
The contract requires `value.unsupported_type`, argument `b`: stage 1 runs before stage 2 for the
whole primitive input, then arguments select the first violation within the stage. Likewise
`compare_versions(2**53, {1: 'x'})` incorrectly reports `value.integer_out_of_range` in `a`.
`_domain` calls complete stage-1-plus-stage-2 validation for each argument before visiting the
next argument. The unit test covers stage 2 versus stage 3, but not stage 1 versus stage 2 across
arguments. All three multi-argument primitives share this helper.

The JSON comparison adapter has the analogous integration problem. Executing its `_observe`
for `compare_operation_identities`, with `a_json: '1e400'` and
`b_json: '{"a":1,"a":2}'`, returns `value.number_not_finite`. The second argument's
`value.duplicate_key` must win at stage 1. Eagerly completing `decode_json(a)` prevents the
library comparison from seeing the later structural failure.

**Required repair:** apply each stage across all arguments before advancing to the next stage.
Have the runner delegate combined JSON-seam validation to the library; do not put precedence
or a competing validator in the adapter. Add cross-argument stage-1/stage-2 discriminators for
native and JSON seams, and run them against the known-bad candidate first.

### WP01-PY-002 — Revision typed fields are validated outside canonical order

- **Classification:** `IMPLEMENTATION_DEFECT`; **severity:** high.
- **Path:** A (SER-008/G-034); **owner_decision_required:** false.
- **Pinned code:** `core/identity.py:130–136`.

Compare `a = {'stable_id':'BAD', 'artifact_version':0, 'projection':None}` with a valid revision
`b`. The result is `id.invalid`, argument `a`. Both fields pass generic validation, but canonical
UTF-16 field order visits `artifact_version` before `stable_id`; the required first typed error
is `version.invalid`, argument `a`. `_revision_rule` instead checks the ID first. This is not a
new semantic choice: the Owner already fixed stage-3 object order in G-034.

**Required repair:** apply the agreed typed-field traversal and add a multiple-invalid-field
control, including member-order permutations. Do not repair it with a new error priority list.

### WP01-PY-003 — Eager representation checks and lookahead defeat stage-1 source order

- **Classification:** `IMPLEMENTATION_DEFECT`; **severity:** high.
- **Path:** A (SER-008/G-034); **owner_decision_required:** false.
- **Pinned code:** `core/values.py:212–229,233–247`.

Three independently executed witnesses return `value.invalid_json` incorrectly:

| Input construction | First source-ordered error |
|---|---|
| Python `'["\\ud800", "' + chr(0xd800) + '"]'` | `value.lone_surrogate` at the earlier escaped string |
| Python `b'[{"a":1,"a":2},"\xff"]'` | `value.duplicate_key` at the earlier second `a` |
| JSON text `"\ud800\uZZZZ"` | `value.lone_surrogate` at the valid but unpaired high-surrogate escape |

Whole-buffer UTF-8 decoding and raw-surrogate scanning report a later encoding defect before
the parser reaches an earlier defect. In the third case, `hex4` validates the malformed second
escape and raises before the already-unpaired high surrogate can be reported. The existing
tests only mix source-ordered defects after representation preprocessing succeeds.

**Required repair:** preserve source-order error selection across representation, JSON syntax,
duplicates and escaped-surrogate checks. Add all three discriminating neighborhoods; a blanket
encoding-first gate is not the agreed policy.

### WP01-PY-004 — Diagnostic formatting replaces stable errors with host exceptions

- **Classification:** `IMPLEMENTATION_DEFECT`; **severity:** high.
- **Path:** A (SER-008 codes/G-031); **owner_decision_required:** false.
- **Pinned code:** `core/values.py:308`; `core/identity.py:68`.

`validate_value(10**5000)` raises a plain `ValueError` from Python's 4,300-digit integer-to-string
limit while constructing the rejection detail; it must raise `MnemeValidationError` with
`value.integer_out_of_range`. A 100,000-deep nested list passed to `validate_version` reaches
the wrong-type check but raises `RecursionError` from `repr`; it must report `version.invalid`.
Both failures reproduce on Windows and Linux. The valid deep serialization test does not test
error construction. This also contradicts the record's claim that every rejection has the stable
error type/code.

**Required repair:** make diagnostic construction bounded and safe, and audit other rejection
details. Preserve error codes regardless of host formatting limits; do not change global limits
or narrow the accepted domain to hide this failure.

### WP01-PY-005 — Malformed revision-input policy and its code are not fixed by the contract

- **Classification:** `REQUIREMENT_UNCERTAIN`; **severity:** medium.
- **Path:** C; **owner_decision_required:** true.
- **Authority:** agreed `spec/core.md` CORE-003 comparison, SER-003, SER-008/G-031.
- **Pinned code:** `core/identity.py:130–136`; implementation record reading 2.

For `{'stable_id':'ok', 'artifact_version':1}` against a valid revision, the implementation reports
`id.invalid` even though the ID is valid: the absent projection causes the rejection. It also
rejects `{'stable_id':'ok'}` as `id.invalid` rather than reaching CORE-003's absent-version
`not_applicable` condition. The contract defines the comparison tuple and its normal outcomes,
but no malformed-record policy or code for a missing projection; SER-003 prevents treating
absence as invented content. The author acknowledges this gap.

**Interpretations/options:** require complete comparison records before considering applicability,
with an explicitly defined malformed-input code; or permit an absent-version input to return
`not_applicable` after the required generic checks, defining which other fields it needs. Error
mapping for missing identity and missing projection must also be explicit. These alternatives
produce different observable outcomes. The current `id.invalid` observation is evidence of the
implemented reading, not an independently authorized oracle.

**Required action/recommendation:** route the unresolved input policy to the Owner, record the
decision, and bind shape/error controls before keeping this implementation reading.

### WP01-PY-006 — Native array bindings silently exclude tuples

- **Classification:** `REQUIREMENT_UNCERTAIN`; **severity:** medium.
- **Path:** C; **owner_decision_required:** true.
- **Authority:** G-015's JSON-shaped containers and SER-008's arrays/native-kind seam.
- **Pinned code:** `core/values.py:250–261`; implementation record reading 3.

`validate_value((1, 2))` reports `value.unsupported_type`; `[1, 2]` is accepted. The contract
defines arrays abstractly and lists bytes, sets, date-time objects and non-string keys as examples
outside the native domain. It does not bind Python arrays specifically to `list`, or exclude
ordered immutable sequences. Tuple rejection is a new acceptance boundary, not made safe merely
because it rejects. Candidate-local types and unit tests cannot supply shared-contract authority.

**Interpretations/options:** explicitly bind the native array seam to lists only; or admit tuples
as arrays normalized to the same canonical values. State the corresponding native bindings in
both languages. **Required action/recommendation:** obtain the Owner choice for the unresolved
acceptance boundary, then add host-seam conformance controls.

### WP01-PY-007 — The required raw-content hash capability is missing

- **Classification:** `IMPLEMENTATION_DEFECT`; **severity:** medium.
- **Path:** A (CORE-011, SER-009, G-014); **owner_decision_required:** false.
- **Pinned evidence:** `core/values.py:461–468` and public exports; code manifest CORE-011 at
  `mneme-contract-manifest.yaml:1435–1453`, assigning it to Layer 01 and this implementation.

The contract requires both hashes of structured canonical values and hashes of text/binary
content as given. The package only exports the structured `content_hash`: passing `b'abc'`
returns `value.unsupported_type`. There is no raw-byte hash operation in the exported core.
The required raw digest, independently computed, is
`ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad`.
This probe demonstrates absent capability; it does not mean the existing structured function's
documented behavior is wrong or that a structured JSON string should lose its quotes.

**Required repair:** expose the raw-content hashing capability without altering structured hashing
semantics, and add byte-exact controls including line endings and normalization-sensitive text.
The existing fixtures exercise only structured content, leaving this part of CORE-011 untested.

## Other implementation readings and runner assessment

- **Reading 1, extra operation members:** accepted as path A for the current pair model.
  G-032 defines a pair, and CORE-012 explicitly rejects wrong shape. An extra member is outside
  that pair; rejecting it with `operation_identity.invalid` does not add a new identity choice.
  The own probe confirms the implemented result. A future metadata-bearing wrapper would need an
  explicit extension rather than silently becoming part of this pair.
- **Reading 2:** unresolved as WP01-PY-005 above. Missing `stable_id` and missing `projection`
  are not interchangeable authorities merely because one handler currently shares their code.
- **Reading 3:** tuple policy is WP01-PY-006. Reporting a non-string-key map at that map is
  acceptable for code selection: it is a stage-1 unsupported kind, and competing native-kind
  violations within the same argument have the same code. Ordering is impossible before the key
  kind is established. This does not excuse the cross-argument stage failure in PY-001.

The runner otherwise remains an adapter: decoding and serialization are library calls, results
are observed from the error object, comparisons contain no duplicate identity/time/JCS algorithm,
and unknown ACTIVE operations fail. Its eager multi-argument decoding nonetheless induces the
wrong precedence in PY-001 and must be repaired through a library-owned seam. Scenario lists of
`negative_controls` are labels, not executed mutation tests. Existing examples discriminate the
named lexical, key-order, numeric-bound and normalization mistakes, but passing them says nothing
about the additional counterexamples above. Repair tests should first kill this exact candidate.

## Next step

Repair the five implementation defects and resolve the two path-C input-policy questions before
certifying the Python implementation. This review does not authorize Rust implementation or
acceptance of the pair onto main. No production changes were made by Codex.
