# WP-01 final complete review — Codex

**Verdict: CHANGES_REQUIRED**

Exact reviewed pair: docs `18bc390c2e8102113b3c152ff21d79fdc3201a15` / code
`4fe3ed34c29a6868a3f5050ecee95885b73bead0`.
Review branch: `review/wp01-final`, from docs state
`1830e12f0c8525b4f28d5cf2e221c85e9deb0498`.

Two new assurance findings block this final review: WP01-CR-009 (current readiness records) and
WP01-CR-010 (required G3 coverage evidence). No new implementation counterexample or unresolved
Owner semantic choice was found in the executed scope. Neither finding reopens a prior closure.
This verdict does not authorize acceptance onto main or Rust implementation.

## Complete-review conclusions

| Requested surface | Independent conclusion |
|---|---|
| Contract as a whole | CORE-001/002/003/011/012, HIST-004, SER-008/009 express mutually compatible semantic rules after the deltas. Required timestamp input differs explicitly from canonical output. Revision shape precedes typed fields; generic stages precede every typed rule across every argument. Numeric normalization, exact identity and canonical projection comparison agree. Current review/status prose and feasibility claims require CR-009 repair. |
| Owner fidelity | The semantic decisions through G-043 are faithfully transcribed; see mapping below. No new path-C determination was made by this reviewer. Process/routing decisions remain governance, not new payload rules. |
| ACTIVE corpus / traceability | Eight ACTIVE Layer 01 files, 146 operation steps. Every expectation independently re-derived; all match. Manifest links resolve and Python locations identify real library files. Five placeholder xfails belong to future behavior, including durable idempotent commits; none masks an ACTIVE Layer 01 case. |
| Python against the whole contract | Read all six core source files and the runner, unit/remediation/CE tests. The entire suite passes on Windows and case-sensitive POSIX. Fresh independent numerical, text, time, identity and serialization probes find no behavioral contradiction. The passing suite does not meet the recorded coverage floor (CR-010). |
| Runner thinness | It loads and schema-validates cases, constructs `JsonText`/native values or raw byte inputs, calls public core functions and compares observations. It does not repair serialization, typed rules or error precedence. Its hash calculation is an assertion against the library result, not a substitute for it. Unknown ACTIVE operations fail loudly. |
| Rust readiness | The semantic text and finite corpus provide enough to start an independent implementation once the assurance blockers are repaired. Rust must retain decoding/structural failures ahead of numeric conversion failures, use UTF-16 member ordering and checked binary64 semantics, and guard the timestamp grammar/range. Python is not the oracle. No Rust production code was written. |
| Records current | Not yet: the maintained feasibility matrix and WP plan describe an older contract checkpoint and parser route. Existing implementation/response/review records retain their historical meaning and must not be rewritten as new evidence. |

The wider CORE/SER requirements assigned to Layer 01 in the manifest remain architectural
constraints: identity is not a title/path, lineage does not rewrite history, schema versions are
not semantic editions, missing fields are not invented. The reviewed callable contract is the
bounded surface explicitly named by the handoff. This review does not claim provenance storage,
migrations, replay, durable commits or per-artifact semantic projection definitions are implemented.
Those are not supplied by this Python package or by a runner workaround.

### Decision fidelity map

| Decisions | Resulting contract / check |
|---|---|
| G-012 | CORE-002 positive numeric edition, bounded by the generic domain; bool/fractional values fail the typed rule. |
| G-013 | CORE-012 per-store uniqueness, identical retry vs conflicting content; durable writes explicitly belong to Layer 04. |
| G-014 | CORE-011/SER-009 structured SHA-256 over JCS bytes; raw text/binary bytes have no normalization. |
| G-015 amended by G-016, G-017, G-023, G-025 | SER-008 scalar strings, JSON-shaped values, binary64 interpretation, safe integral bound independent of spelling, one numeric kind and zero normalization. Native integers remain exact. |
| G-020 | CORE-001 lowercase portable token, 1–128 ASCII bytes, no trailing dot/device basename; path is a projection. |
| G-021 | CORE-003 immutable semantic revisions, explicit per-type projection, identical/distinct/not_applicable and visible conflict. |
| G-022/G-026/G-028/G-029/G-030 | HIST-004 canonical six-digit UTC spelling; required offset/fraction/case grammar; proleptic Gregorian years 0001–9999 for local and UTC instants; overflow rejection. |
| G-031/G-034 | SER-008 exactly one error; structural, generic, then typed stages across all arguments; source order for JSON decoding and canonical traversal otherwise. |
| G-032/G-033 | CORE-012 namespaced pair, stable-token namespace and exact opaque operation ID of 1–256 UTF-8 bytes. |
| G-035 | CORE-003 closed revision shape, required members, typed fields only after valid shape, absence of version never bypasses validation. |
| G-036/G-037 | SER-008 list/tuple arrays, admitted genuine subclasses extracted through base semantics, no caller hooks or added state. |
| G-039/G-040 | Native duplicate base names and active-path cycles are stage-1 errors; shared acyclic references remain legal. |
| G-041/G-042/G-043 | Base-protocol byte/control inputs, exact built-in value outputs, dict-only argument maps; non-dict call shapes raise TypeError before reading data, outside the data-error vocabulary. |
| G-018/G-019 and intervening process rulings, G-038 | Governance/routing decisions, not additions to the portable value domain. The current final-review handoff is authorized after WP-P01 and CE-01-01 closure. |

Prior CR-001..006 and the Python remediation findings remain at their previously established
dispositions. CR-007/008 remain closed for this exact pair by `dc9f9aaaf1bf9849cac8c177d76b1035cf20624f`.
The independent 25,470 normative rows, 75 boundary oracles, 6,775 exact-value returns, zero hooks,
and 128 killed frozen controls from that immediately preceding review apply to these unchanged
SHAs. I did not substitute Claude's reported counts or rerun the frozen episode unnecessarily.

## Fresh executions

Healthy project-managed CPython 3.12.8 was used; the damaged system Python was not invoked.
Scratch, dependencies, coverage data, Cargo home/target and the POSIX image stayed project-local.
Windows source checkout is the clean detached code candidate. The review docs branch adds only
this record; candidate-to-state changes are two handoffs plus state, with no contract/tool changes.

| Own execution | Result |
|---|---|
| Full Windows suite | 335 passed, 5 placeholder xfails; 340 collected cases. |
| Full case-sensitive POSIX suite | 335 passed, 5 placeholder xfails in 7.73 s. WSL Ubuntu, project-local ext4/FUSE archive of the same code SHA; source byte comparison to the detached candidate passes. Existing distinct `A`/`a` files prove case sensitivity. |
| All repository checks, deep sources | repos/sources/spec/manifest/conformance/findings/registry/state: 8/8 pass. |
| Lint/format/types | ruff clean; 11 files formatted; mypy strict clean on six source files. |
| Independent ACTIVE expectations | 146/146 match, including stage selection, typed shapes, identities, timestamps, canonical bytes and raw/structured digests. |
| ECMAScript challenge | 60,000 deterministic admitted binary64 samples match Node v22.15.1 `JSON.stringify`. |
| Stable-ID oracle | 5,000 generated tokens match an independent character/length/device-name predicate. |
| Timestamp arithmetic oracle | 5,000 generated inputs match independent ordinal-day/integer-microsecond UTC arithmetic. |
| Generated JSON/JCS | 4,000 trees decode correctly and match rfc8785 0.1.4 canonical bytes; 4,000 punctuation/control mutations match acceptance or the permitted structural rejection category. The mutation oracle does not claim precise source-error precedence when a surrogate defect and syntax defect coexist. |
| Supplied byte/hash oracles | All 13 positive canonical byte strings and SHA-256 digests re-derived; seven raw digests re-derived. |
| Rust feasibility probe | rustc 1.97.1; offline/locked serde_json 1.0.151 (`float_roundtrip`), serde_jcs 0.1.0, chrono 0.4.45. Rounding/underflow/subnormal cases reproduce; timestamp endpoints, −1 µs and epoch round-trip. UTF-16 ordering still kills unchanged serde_jcs. New stage-precedence witness below demonstrates the limitation of eager overflow mapping. |
| Coverage, subprocesses included | 606/621 statements, 97.584541% (rounded display 98%), no exclusions; CR-010. All tests pass under instrumentation. |
| Uncovered reachable-path checks | Ten reviewer probes pass for missing commas/colons, invalid text types, raw memoryview/text inputs, stored JsonText access/representation/immutability, uninitialized JsonText and invalid argument names. They are correct behaviors missing from the recorded suite, not new implementation defects. |

POSIX wrapper limitation: the pytest invocation completed successfully and its XML/log record
335/5. The wrapper's final `tail` command failed because of a trailing CR; this did not change the
test result. The EXIT trap ran, and a subsequent correctly rooted environment check verified the
FUSE mount is unmounted. No successful wrapper exit is claimed.

Primary standards checked: [RFC 8785 §§3.2.2–3.2.3](https://www.rfc-editor.org/rfc/rfc8785.html#section-3.2.2)
for ECMAScript serialization/UTF-16 member order and
[RFC 3339 §5.6](https://www.rfc-editor.org/rfc/rfc3339.html#section-5.6) for the timestamp grammar.
Mneme's narrower acceptance, stage precedence and error vocabulary come from the Owner decisions,
not those standards. The official [serde_json documentation](https://docs.rs/serde_json/1.0.151/serde_json/)
was consulted as library information, not semantic authority.

## New blocking findings

### WP01-CR-009 — Maintained readiness records omit the final contract and describe an insufficient decoder route

- **Classification:** CONTRACT_ASSURANCE_DEFECT.
- **Severity:** medium; **blocking:** WP-01 final review / current readiness evidence.
- **owner_decision_required:** false; **status:** OPEN. Repair is fidelity to already decided semantics, path A; no new acceptance/error choice.
- **Pinned evidence:** docs `18bc390c`, `assurance/layers/01-feasibility-matrix.md:3–5,17,19,30–31,68–72`; `plans/WP-01.md:3,15,42–44`; `spec/serialization.md:74`.

The maintained matrix still ends at G-034 and says it is for the earlier re-review. It describes
Python object_pairs_hook/hooks plus checks as needed, rather than the actual strict iterative
decoder and extract-first native pass. It omits G-035..G-043's revision shape, native binding,
cycles, duplicate base names, byte/control-object rules and exact returns, and supplies no current
checkpoint/closure references. Its numeral row says losslessness is achieved once a Rust overflow
error is mapped. That condition is insufficient under the complete stage contract.

**Executed witness:** `{"a":1e400,"b":1,"b":2}`. Required result is stage-1
`value.duplicate_key`. Current Python returns that result. Eager serde_json decoding fails at the
first numeral with `number out of range at line 1 column 10`, before the later duplicate can be
observed. Mapping that error to `value.number_not_finite` would return a stage-2 error incorrectly.
A duplicate-aware visitor added to the same eager numeric decode cannot by itself solve this;
structural decoding must preserve/defer numeric interpretation or use an equivalent staging design.
This is a challenge to the readiness advice, not a defect in a nonexistent Rust implementation.

The plan still claims CONTRACT_REVIEW round 3 and DRAFT scenarios and calls emission of integers
at/above 2^53 a serializer defect. SER-009 correctly states that this is a Mneme-domain validator
responsibility, not a JCS defect. The unqualified “not reviewed, not implementation-facing” sentence
in the serialization introduction also contradicts the completed checkpoints/ACTIVE corpus.

**Required repair:** refresh the maintained matrix/plan and Layer 01 status guidance to the complete
contract through G-043, distinguish historical transcripts from current conclusions, reference the
agreed checkpoints and independent closure, and state the staged decoder requirement with the
witness above. Preserve the historical probe/review records. No new production semantics are needed.

### WP01-CR-010 — Required author-run G3 coverage evidence is absent and the suite is below the recorded floor

- **Classification:** CONTRACT_ASSURANCE_DEFECT.
- **Severity:** medium; **blocking:** WP-01 final review / acceptance gate.
- **owner_decision_required:** false; **status:** OPEN. Applying the existing gate changes no payload semantics. Changing the agreed floor would require separate governance, not an agent workaround.
- **Pinned evidence:** docs `18bc390c`, `process/gate-tiers.md:27–33,45–46`; `assurance/reviews/WP-01-CE-01-01-implementation-claude.md:48–51`; code `4fe3ed34`, `minion-memory-python/src/minion_memory/core/` and its tests.

The gate specifies G3 for FINAL_CONTRACT_REVIEW and before acceptance, including **100% of the
certified Python surface**, and requires author-run evidence at the exact pair. The candidate
record reports lint, format, typing and 335 tests, but no coverage evidence or surface/exclusion
accounting. My full-suite measurement with subprocess tracing is 606/621 statements covered,
15 missing, no exclusions. This is not simply a cycle-test subprocess being overlooked: enabling
subprocess tracing adds the cycle rejection, but leaves real callable paths untested.

Missing statements: errors.py `42`; values.py `112,135,362,478,481,484,493–494,512,564,577,666–669`.
For example, `decode_json('[1 2]')` and `decode_json('{"a" 1}')` correctly report invalid JSON,
and `raw_content_hash(memoryview(b'abc'))` correctly matches SHA-256, but the corresponding lines
are not executed by the full suite. Ten independent checks confirm reachable uncovered behavior.
Some other missing branches appear unreachable after normalization (e.g. serializer branches for
floating zero/integral formatting), so this finding does **not** prescribe arbitrary tests of private
functions merely to move a counter, nor blanket coverage exclusions.

**Required repair:** add meaningful controls for reachable missing behavior; explicitly account for
any genuinely unreachable/internal code or exclusions without silently narrowing the public surface;
then record author-run G3 evidence at the repaired exact pair, with the required floor satisfied.
Keep the existing discriminating controls. Passing counts alone are not the coverage gate.

Reproduction (all paths relative to project root; source project-environment.ps1 first):

```powershell
$env:PYTHONPATH=(Resolve-Path review-worktrees/code-wp01-ce1-closure/minion-memory-python/src).Path
# coverage 7.16.2, project-local reviewer environment; rcfile content below
& .tmp/cache/venvs/mneme-process-codex-r1/Scripts/python.exe -m coverage run --rcfile=.tmp/work/codex/wp01-final.coveragerc -m pytest review-worktrees/code-wp01-ce1-closure/minion-memory-python/tests --basetemp=.tmp/work/codex/wp01-final-coverage-child-tests -p no:cacheprovider
& .tmp/cache/venvs/mneme-process-codex-r1/Scripts/python.exe -m coverage combine --rcfile=.tmp/work/codex/wp01-final.coveragerc
& .tmp/cache/venvs/mneme-process-codex-r1/Scripts/python.exe -m coverage report --rcfile=.tmp/work/codex/wp01-final.coveragerc -m
```

```ini
[run]
source = E:/AI/Projects/OpenMinds/Minions/Minion-Memory/review-worktrees/code-wp01-ce1-closure/minion-memory-python/src/minion_memory/core
data_file = E:/AI/Projects/OpenMinds/Minions/Minion-Memory/.tmp/work/codex/wp01-final-subprocess.coverage
patch = subprocess
parallel = true
```

## Evidence inventory and stopping point

Reviewer artifacts under `.tmp/work/codex/`: `wp01-final-probes.py/.json/.log` (fresh generated
probes), `wp01-final-oracles.py/.json` (146 independent expectations; imports only the earlier
reviewer's oracle definitions, not production code), `wp01-final-rust/` and
`wp01-final-rust-results.jsonl`, `wp01-final-tests.xml`, `wp01-final-posix/tests.xml` and
`tests.log`, `wp01-final.coveragerc`, `wp01-final-coverage-child.json`,
`wp01-final-coverage-witnesses.py/.json`. The independent earlier oracle definitions are in
`.tmp/work/codex/wp01-round2.py`. These files are review scratch, not candidate edits.

Only this review record is committed. No source, shared contract, corpus, registry, state,
authoring worktree or remote was changed by Codex. No Rust implementation work began.
Claude should reproduce/classify CR-009/010 and return the repaired exact pair with the missing
readiness/G3 evidence for the next authorized review step. No convergence reopening or new Owner
semantic decision is requested by these findings.
