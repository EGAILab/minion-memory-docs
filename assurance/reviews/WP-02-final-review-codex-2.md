# WP-02 final remediation re-review — Codex

**Verdict: APPROVED**

Date: 2026-10-11. Targeted re-review following
`process/handoffs/WP-02-codex-final-review-2.md` at state commit
`b7e475db`. The preceding complete final review remains authoritative outside this delta.

## Exact pair and scope

- Docs: `6541f33a989da531cc2f21c6b3169b962c45d808`.
- Code: `ff9d132ada35a604c6f4bc7f11504b229afece6e`.
- Responds to `b910a24472997cffded5c24fbba1a02dc24086a4`, specifically WP02-CR-007.
- Author response: `assurance/reviews/WP-02-final-review-response-claude-1.md`.

Reviewed in separate worktrees: code detached at the exact SHA; docs branch
`review/wp02-final-2` from the handoff state. Candidate source and shared state were
not modified. This review commits only this record; all scratch probes, environments,
caches and POSIX filesystem image stayed project-local under OWN-001.

Compared the entire code delta from `43e0984e`: only
`minion-memory-python/tests/conformance/test_canonical.py` changes. No library, corpus,
Rust runner, dependency or implemented-layer declaration changes. The docs delta adds
review/response/handoff/state records, without a normative contract change. Read the
response and the actual corpus README, and challenged the disposition function through
the real `test_canonical_scenario` entry point rather than merely calling its helper.

## WP02-CR-007 disposition

**Closed by independent verification for this candidate.** Classification remains
`IMPLEMENTATION_DEFECT`; `owner_decision_required: false`. No new finding.

The original schema-valid witness uses the Layer 02 history-replay scenario, changes
its status to DRAFT, and sets `given` to `{"note":"TO_BE_CONTEXT"}`. It now raises
pytest's expected-failure outcome with a reason naming **layer 02** and the **Drafts
rule**, rather than the old layerless placeholder reason. It is not executed as
conformance evidence.

The new rule order is faithful to `conformance/README.md`:

1. Every valid DRAFT scenario returns the Drafts-rule reason with its layer, including
   when a placeholder also exists or the layer exceeds Python's declaration.
2. An ACTIVE scenario containing a recursive `TO_BE_` value fails loudly, including
   above the implemented layer; it cannot be mislabeled as an expected failure.
3. Other recursive placeholders receive a reason naming their layer and the README
   placeholder rule.
4. An ACTIVE scenario above the implemented layer receives a reason naming its layer,
   Python and the Implemented-layers rule.
5. Eligible scenarios reach normal operation dispatch and comparison. An unknown
   operation in an eligible ACTIVE scenario remains an error.

The disposition function handles status only; the runner remains thin and does not
implement history semantics. Schema validation still precedes disposition.

## Reviewer executions

| Check | Result |
|---|---|
| Whole candidate suite on Windows, managed CPython 3.12.8 | 436 passed, 5 xfailed |
| Whole candidate suite on POSIX, managed CPython 3.12.8 | 436 passed, 5 xfailed |
| Independent real-runner disposition controls | 77 passed |
| Restored old order in scratch, candidate self-control | Killed: `test_runner_dispositions` fails on missing `layer 02` in the old placeholder reason |
| Actual corpus dispositions | 17 discovered; all 12 ACTIVE scenarios execute; all 5 placeholder reasons name their respective layer |
| Ruff check and format check | Clean; 14 files formatted |
| Mypy strict | Clean, 14 source files |
| Deep process checks | 8/8 passed |

The independent controls cross DRAFT / PLACEHOLDER / ACTIVE, layers 00 / 01 / 02 / 03 /
99, and no placeholder versus placeholders nested in `given`, `when`, `expect` or
`notes`: 75 combinations. Two further controls execute the original witness and
verify that an unknown eligible ACTIVE operation fails rather than being hidden.
Each fabricated document passes the runner's real schema validation before its
expected disposition is observed.

The old-order mutation restores the former placeholder-first logic and old reason,
while retaining the new candidate self-controls. Its failure is an actual pytest
assertion failure, not an import or setup failure.

POSIX tests ran a Git archive of the exact code on a project-local ext4 image in a
user mount namespace. Distinct `A` and `a` files verified case sensitivity. All
temporary files and the image stayed under the project root. No system Python repair
or external environment edit was performed.

Scratch reproduction evidence:

- `.tmp/work/codex/wp02-final-2/test_dispositions.py` — 77 independent controls.
- `.tmp/work/codex/wp02-final2-mutant.py` and
  `.tmp/work/codex/wp02-final-2/old-order.log` — negative control and failing witness.
- `.tmp/work/codex/wp02-final2-reasons.py` and
  `.tmp/work/codex/wp02-final-2/corpus-dispositions.json` — every actual reason.
- `.tmp/work/codex/wp02-final2-posix.sh`, its starter, and
  `.tmp/work/codex/wp02-final-2/posix-suite.log` — POSIX recipe and suite result.

## Coordination boundary

WP02-CR-001..006 retain their prior closures. The targeted delta resolves the final
review's sole blocker without a direct regression. This approval is of the exact
candidate pair; it does not itself perform acceptance, close NF-016/NF-026 in the
register, change shared state, or begin Rust Layer 02. Those are the next coordination
steps described in the handoff. WP-02S's old-base inheritance must still be rebased
onto this repaired runner before that candidate's acceptance, as the response records.