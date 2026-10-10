# WP-01 Layer 01 contract review 3 — Codex

## Verdict and objects

**APPROVED** for the contract checkpoint at docs
`62adec5fde8575818aa19f3c4025acc78a7240a5` paired with code
`860e91c1bfb08e834c1a62b0f1fc32dd4bfd7efd`.

This targeted review follows `process/handoffs/WP-01-codex-contract-review-3.md`, at state
commit `ce2af505212256913dd1cc500e2c18539bd7fba2`. The record is on
`review/wp01-contract-3`, based on that state commit. I reviewed separate detached checkouts
of both exact candidate SHAs. No candidate or production file was edited.

Scope: WP01-CR-005, WP01-CR-006, the nine new controls and direct regressions. Prior unrelated
items provisionally closed in review 2 remain undisturbed. Approval is of the contract checkpoint,
not acceptance onto main; the handoff permits Python Layer 01 implementation after this approval.

## Finding dispositions

| Finding | Disposition | Evidence and reasoning |
|---|---|---|
| WP01-CR-005 | CLOSED for this checkpoint | Owner G-034 expressly chooses the observable ordering. SER-008 lines 130–139 transcribe source-text order at stage 1, then depth-first canonical UTF-16 member order, name before value, ascending array indices and declared argument order at stages 2–3. Host map iteration/insertion order is excluded. The author-reading note is replaced by the recorded authority. Both new ordering controls reproduce, including the nesting discriminator. |
| WP01-CR-006 | CLOSED for this checkpoint | HIST-004, `spec/core.md:422–426`, distinguishes a valid generic value of the wrong timestamp type from a genuine earlier-stage failure. The five non-string JSON values now yield `timestamp.invalid`; the lone-surrogate text yields `value.lone_surrogate`; the new valid JSON string normalizes correctly. Extra earlier-stage probes also reproduce the distinction for number overflow, integer bounds, invalid array contents and duplicate keys. |

CR-005 remains historically a `REQUIREMENT_UNCERTAIN`, path C, with
`owner_decision_required: true`; G-034 supplies its resolution. CR-006 remains historically a
`CONTRACT_ASSURANCE_DEFECT`, path A, with `owner_decision_required: false`; the repaired text
now follows G-031 and SER-008. Neither requires a new finding or a registry edit by this reviewer.

The remaining error-map portion of WP01-CR-003, left partially resolved in review 2 pending these
two items, is now closed for the checkpoint. The provisional closures of WP01-CR-001, 002 and
004 and the answer to Q1 stand. There are no open blocking findings from this review sequence.

## Own execution evidence

The reviewer-authored driver from review 2 was adapted only to the new exact checkout and to
decode the new timestamp `value_json` arguments before generic and typed validation. It does
not invoke a Mneme implementation or Claude's oracle generator. Its source-aware decoder,
canonical traversal, timestamp grammar and reference serialization derive expected outcomes
independently. A separate neighborhood driver exercises discriminating alternatives.

| Execution | Result | Evidence under `.tmp/work/codex/wp01-contract-review-3/` |
|---|---|---|
| All seven DRAFT scenario files | 129/129 expectations match: 13 canonical bytes/hashes, 20 value rejections, 12 version results, 16 stable-ID results, 43 timestamp results, 18 operation-identity results and 7 artifact-revision comparisons | `python-results.json`, `python-summary.log` |
| New controls | 2/2 order controls and 7/7 timestamp controls match | same |
| Direct neighborhood | 39/39 assertions pass, including all six permutations of a native map, equivalent JSON member orders, nested objects/arrays, UTF-16 versus UTF-8 order, name-before-value, source-ordered stage-1 failures and earlier-stage timestamp failures | `neighborhood.json` |
| Deliberately incorrect order/error controls | Source traversal, code-point/UTF-8 traversal, reversed array order, value-before-name and reporting a typed timestamp error over a stage-2 failure each disagree with the required witness | same |
| Mechanical candidate checks | sources, spec, manifest, conformance and findings: 5/5 pass, with deep source verification | `mechanical.log` |

Drivers: `.tmp/work/codex/wp01-round3.py` and `wp01-round3-neighborhood.py`. Executed with the
project-local managed CPython 3.12.8 at
`.tmp/cache/venvs/mneme-process-codex-r1/Scripts/python.exe`, with `rfc8785` 0.1.4 for canonical
bytes and `hashlib` for hashes. All temporary output stayed within the project. The damaged
system Python was not used.

Minimal reproduced ordering witnesses:

- `{"b":9007199254740992,"a":1e400}` and its member-order permutation both report
  `value.number_not_finite` under G-034. The analogous native maps do so for all tested insertion
  orders.
- `{"b":{"a":1e400},"a":[9007199254740992]}` reports `value.integer_out_of_range`;
  source-order traversal instead reports `value.number_not_finite` and is killed.
- A native map whose U+FF61 key contains infinity and U+1F600 key contains 2^53 reports
  `value.integer_out_of_range` under UTF-16 order; code-point/UTF-8 order selects the other error.
- A native surrogate member name with an out-of-range numeric value reports
  `value.lone_surrogate` before examining that value.

For timestamps, `null`, `true`, `7`, `[]` and `{}` independently pass generic validation and fail
typed validation as `timestamp.invalid`. In contrast, JSON `1e400`, `9007199254740992`,
`[1e400]`, an unpaired-surrogate string and a duplicate-key object retain their earlier-stage
errors. The valid JSON string `"2026-10-10t05:30:00z"` normalizes to
`2026-10-10T05:30:00.000000Z`.

## Direct regressions and limits

The production contract delta is confined to the ordering authority/transcription and timestamp
error paragraph; the feasibility matrix and plan now cite G-034 consistently. Existing numeric,
hash, identity, comparison and timestamp grammar/range expectations all reproduce. The new
controls do not alter their domains. I found no additional contradiction or unresolved semantic
choice in this targeted scope.

The Rust feasibility conclusions from review 2 remain applicable: timestamps fit the internal
signed-64-bit microsecond representation, and unchanged serde_jcs 0.1.0 still needs replacement
or correction for UTF-16 key ordering. These unchanged probes were not rerun. This is contract
approval, not certification of a production implementation or its eventual conformance tests.
