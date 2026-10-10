# WP-02 contract review round 2 — Codex

Date: 2026-10-11. Independent reviewer / Rust owner: Codex.

## Verdict

**APPROVED** for the requested contract/corpus re-review at docs
`6f761081dcabc3975e526b262b8d0c5e493ab9a5` / code
`15b71ca392384b447f4b2c0ca023a69538f977d8`.

WP02-CR-001..005 are resolved and closed in this review's dispositions. No new contract findings.
**NF-026 remains OPEN, owned by Codex:** the exact candidate's Rust canonical suite still fails
on DRAFT. This approval is the independent contract review, not Rust gate approval, NF-026 closure,
acceptance onto main or certification. The runner-alignment prerequisite remains outstanding; it
must be completed before declaring the prerequisite met or relying on Rust corpus gates.

## Scope and custody

Followed `process/handoffs/WP-02-codex-contract-review-2.md` at `268574e8`, which asks for finding
closure, new-control derivation and NF-026 status, and says not to edit the candidate. The new
branch `review/wp02-contract-2` starts at that state head in `review-worktrees/docs-wp02-review-2`.
Code is a separate detached checkout at the exact SHA in `review-worktrees/code-wp02-review-2`.
Only this review record is edited/committed. Probes, interpreter caches and Cargo outputs stay
inside the project. No production, state, registry or WP-02S changes.

Compared the round-1 pair to this pair, reviewed the response as a review object, read G-052..G-055
verbatim and compared the revised normative blocks independently. The imported round-1 Codex record
is unchanged: `git diff 42d3d03e 6f761081 -- assurance/reviews/WP-02-contract-review-codex.md` is empty.

## Per-finding dispositions

| Finding | Disposition | Independent basis |
|---|---|---|
| WP02-CR-001 | CLOSED | G-052 expressly chooses the CORE-001 lexical domain for profile/type vocabulary identifiers, exact comparison and integral schema editions 1..2^53-1; HIST-002 transcribes these and the identity triple without treating the identifiers as artifact IDs. Version zero is explicitly not a sentinel. |
| WP02-CR-002 | CLOSED | G-053 expressly closes the reader and entries, rejects missing/unknown members and duplicate normalized pairs, and permits internal set representation only after duplicate-free validation. SER-005 says the same. |
| WP02-CR-003 | CLOSED | G-054 expressly fixes integral positions 0..2^53-1, the before-first physical boundary and greater-than-N resume interpretation. HIST-005 retains the store-local restriction and does not equate position with record count or event causality. |
| WP02-CR-004 | CLOSED | The repaired gate 1 checks only the G-052 routing triple; gate 2 excludes a foreign profile before touching compatibility. Both HIST-002 and SER-005 consistently require compatibility only for admitted records. The two new foreign controls discriminate against the old rule. |
| WP02-CR-005 | CLOSED | G-055 expressly authorizes the four stage-3 gates. HIST-002 transcribes their order and SER-008 records the scoped exception beside G-035. Typed fields still use canonical traversal inside gate 4; other record kinds do not inherit this exception. |

### CR-004 authority reading

The author reading is sound under the combined decisions. G-052 expressly names the routing triple
and requires malformed tokens/versions to be envelope errors. G-050 makes compatibility a question
only after profile admission. G-055 terminates foreign records at exclusion before recognized shape
and remaining typed fields. Compatibility therefore cannot be added to gate 1 merely because it is
a required member of a recognized envelope. A foreign record with a valid triple and absent/bogus
compatibility is excluded; a foreign record with an invalid record_type/schema_version is rejected
at gate 1. This uses deciding text, not a new product choice.

Generic stages still precede all these gates: a non-finite number nested in a foreign payload, or
used as its compatibility value, is rejected at stage 2. That is portable-value validation, not
consulting compatibility semantics or decoding a profile payload schema. Likewise the boundary
out-of-range wording is read under its explicit generic-stages-first rule: numeric 2^53 gives
value.integer_out_of_range before typed boundary validation. The unchanged corpus pins that order.
Nothing in G-054 or the transcription removes the common stage precedence.

## Independent corpus derivation

The review scratch model imports neither production library. It uses independent token/number
checks, duplicate-aware JSON decoding and timestamp offset arithmetic. For round 2 I moved the
compatibility check from routing to the admitted-profile branch, as required by the new text;
all other derivation mechanics remain those independently used in round 1.

- **70/70** complete observations match the draft expectations, including normalized envelopes.
- Matched old/new cases by case label and compared both inputs and full expectations: **all 59
  earlier inputs and expectations are unchanged**; exactly 11 controls were added.
- The round-1 compatibility-first rule gives history.envelope_invalid on each new missing/bogus
  foreign compatibility case, so **both controls kill that old reading**. The revised rule gives
  excluded on both.
- **17** additional neighborhood assertions pass against the literal revised contract model:
  foreign compatibility null/bool/number/object/array/case variant; missing routing type; zero
  schema edition; generic non-finite payload/compatibility; same-profile missing compatibility;
  unknown required/ignorable early termination; shape-before-fields; canonical field priorities;
  and duplicate reader before record errors.

These executions derive contract expectations; they are not evidence that Layer-02 public library
operations have been implemented. No Python implementation is used as an oracle.

| New control (one-based step in revised scenario) | Independently derived result | Reason |
|---|---|---|
| boundary-local-cursor 6: max position vs 0 | greater | Both in G-054 domain; same store; max > 0. |
| envelope-admission-shape 22: zz_extra plus invalid occurred_at | history.envelope_invalid, record | G-055 gate 3 precedes gate 4; zz_extra sorts after the timestamp and makes the control discriminating. |
| envelope-admission-shape 23: invalid record_type plus invalid occurred_at | history.envelope_invalid, record | Gate 1 routing rejection precedes gate 4. |
| envelope-admission-shape 24: recognized record without compatibility | history.envelope_invalid, record | Admitted-profile gate 2 requires compatibility. |
| profile-exclusion 7: foreign invalid record_type | history.envelope_invalid, record | G-052 routing triple is validated before foreign exclusion. |
| profile-exclusion 8: foreign bogus compatibility | excluded | Valid triple; profile mismatch terminates before compatibility. |
| profile-exclusion 9: foreign missing compatibility | excluded | Same gate ordering; no compatibility default/inference. |
| replay-compatibility 12: reader missing recognized | history.reader_invalid, reader | G-053 required member absent. |
| replay-compatibility 13: extra member in recognized entry | history.reader_invalid, reader | G-053 closes each entry as well as the outer reader. |
| replay-compatibility 14: reader entry edition 0 | history.reader_invalid, reader | G-052 domain excludes zero; G-053 entries use that domain. |
| replay-compatibility 15: same-profile unknown schema, bogus compatibility | history.envelope_invalid, record | Gate 2 validates compatibility before deciding skip/unknown_required. |

Reproduction files under `.tmp/work/codex/`: `wp02-round2-derive.py`,
`wp02-round2-derived.json`, `wp02-round2-diff.py`, `wp02-round2-new-controls.json` and
`wp02-round2-neighborhood.py`. The old derivation is retained in `wp02-derive.py`.

## Gates and NF-026

| Own execution at the exact pair | Result |
|---|---|
| Independent revised-text oracle | 70/70 expectations; 59 originals unchanged; 11 additions |
| Old-rule negative controls | 2/2 foreign compatibility controls reject the old reading |
| Direct contract neighborhoods | 17/17 assertions |
| `mneme_process check --deep-sources` | 8/8 pass |
| Python canonical suite using project-local managed CPython 3.12.8 | 9 passed, 9 xfailed (8 ACTIVE scenarios + discovery; 5 placeholders + 4 drafts) |
| `cargo test --locked --offline --test conformance canonical_corpus -- --nocapture` | FAIL: tests/conformance.rs:118, DRAFT != ACTIVE |

NF-026 remains the already-recorded runner defect; no duplicate finding is raised. Runner source
and the hard-coded (8,146,5) assertion were not changed by this corpus-only code delta. The correct
draft inventory is 8 ACTIVE / 146 ACTIVE steps / 9 xfails, including four Layer-02 DRAFT scenarios
with 70 steps that must not run as implementation evidence. That differs from future promotion to
ACTIVE, which must execute those steps and fail on missing operations. Any alignment should preserve
those distinctions and loud failures on malformed/unsupported ACTIVE scenarios.

The exact-candidate no-edit instruction is honored: this review does not repair the runner or claim
that the failure is waived. NF-026 is my outstanding Rust task; it remains a prerequisite in the
feasibility matrix and its register recommendation. Claude can consume this contract approval while
retaining that prerequisite rather than reporting the full WP gate green.

## Direct regressions and readiness

No earlier expected result changed, and the revision does not modify production implementations,
Layer-01 scenarios or the accepted timestamp/value rules. G-047/G-051 store-local and split-work
constraints remain intact. Gate 4 still checks occurred_at before record_id before recorded_at;
unknown/foreign records do not get recognized-schema shape or timestamp checks. The HIST-001/HIST-010
later-layer assurance boundary from round 1 is unchanged.

The revised feasibility matrix is faithful to the approved domains and gates. Rust can implement
these as explicit passes over normalized Values with exact pair membership, token/timestamp reuse
and iterative payload preservation. An internal set must not erase duplicate declarations before
validation. No new representability problem, unrecorded path-C decision or contradiction requiring
contract repair was found in this targeted delta. This record does not update coordination state
or grant certification/acceptance authority.
