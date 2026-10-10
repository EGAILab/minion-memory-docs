# WP-02S contract review 3 - Codex

Date: 2026-10-11. Independent reviewer / Rust owner: Codex.

## Verdict

**APPROVED** for docs `c08c57e46c0c972d0e497f74df311e0241cb8b5c` /
code `0c569afba20477e0687a1de837b70e4b8996fa1e`.

**WP02S-CR-003 is closed by this candidate.** CR-001/002 remain closed. No open
blocking finding or new semantic contradiction remains in this targeted delta.
Approval agrees the contract candidate only; it does not certify an implementation
or grant acceptance onto main.

## Scope and custody

Followed the handoff at state `456ee710`. New branch `review/wp02s-contract-3`
starts there in `review-worktrees/docs-wp02s-review-3`. Reused the unchanged,
clean exact-SHA code checkout `review-worktrees/code-wp02s-review-2`.
Only this record is committed; no production, candidate, state, registry or
other worktree changes. Each shell sourced the project environment. Scratch
and caches remain project-local.

This is targeted closure of CR-003 and the matrix correction's direct regressions.
The earlier complete review and CR-001/002 closures stand. Verified the normative
spec and G-064 governance text are byte-identical to `acb57251`; code is unchanged.
The semantic-document delta is the three corrected matrix lines: governance range,
facet-name domain and H11 explanation. Imported reviews, response and coordination
records are not treated as behavioral closure evidence.

## Independent closure evidence

Read the corrected matrix against the verbatim G-064 decision and the scope spec.
The facet-name row now states exactly two lowercase ASCII segments separated by
one dot; each segment is 1-128 bytes with `[a-z0-9][a-z0-9_-]*`, with no reserved
device-name exclusion. Both language columns explicitly prohibit reusing the
CORE-001 stable-ID rule for names. H11 now preserves CORE-001, including device
exclusion, for facet **values**, and the separate G-064 grammar for facet **names**.
The governance range includes G-064.

Re-executed the discriminating contract controls using the independent spec model:

| Input | G-064 and corrected matrix interpretation |
| --- | --- |
| Name `agent.con`, value `c-1` | Valid, preserve the facet; unknown registry name remains hidden |
| Name `con.prn`, value `v` | Well-formed unknown facet; no device exclusion for either segment |
| Name `agent.session.x` | `scope.invalid` |
| 128-byte namespace plus dot plus 128-byte facet | Valid (257 bytes total) |
| Either segment 129 bytes, uppercase, Unicode or malformed initial character | Invalid |
| Valid name with facet value `con` | `scope.invalid` under CORE-001 |

The former matrix's segment-as-stable-ID interpretation rejects `agent.con`; the
corrected matrix admits it, so the original contradictory advice is removed. No
meaning, normalization, vocabulary or privacy policy was added by this correction.
The same direct controls also preserve unknown-query rejection and error naming.

Own executions: **19 direct grammar/value/naming controls passed** and **73/73
corpus observations re-derived** (24 value/shape, 18 matching, 31 isolation).
`mneme-process check --deep-sources` against this exact pair: **8/8**.
Recipes and observations: `.tmp/work/codex/wp02s2-derive.py`,
`wp02s2-derived.json`, `wp02s2-grammar-controls.json`. These executed models establish
contract derivations, not production MemoryScope behavior.

The plan's progress paragraph still carries the initial 69-step inventory; the
current response, unchanged corpus and executed derivation establish 73. Refresh
that historical count when advancing the plan. It does not change acceptance,
implementation instructions or the closure of the contradictory grammar, and is
not a blocker on agreement of this exact contract.
