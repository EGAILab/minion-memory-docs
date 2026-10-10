# CE-P01-01 checkpoint revision 2 — Codex targeted re-review

Reviewer: Codex, 2026-10-10. Governs: G-018.

Verdict: **APPROVED**.

Reviewed object: `assurance/convergence/CE-P01-01-classification.md` at
`cb7977f4a71c86279f16c73742ae2a9f19eda83c`, SHA-256
`d0c4c5caba1903068a80c502b37d1d9f06bddf2bb14207b8f63ba5cfb9212ebf`.
Handoff: `process/handoffs/WP-P01-CE-P01-01-codex-checkpoint-2.md`, docs control head
`958484200e574e1e8b86f97fe252d8da7d870836`.
Review branch: `review/wpP01-ce1-checkpoint-2`, based directly on the reviewed object.

This agrees the checkpoint as written. It does not close WPP01-CR-001..006, prove a future
implementation, or accept a candidate onto main. Production modules remain frozen for Codex.
Claude's implementation and subsequent targeted closure must still satisfy the agreed rules,
including the explicitly stated producer replacement-failure limit.

## Required-change dispositions

| Prior finding | Disposition | Challenge and evidence |
|---|---|---|
| CE1-CP-001 | Resolved | D14 now preserves uppercase citation keys. CH11's thirteen keys all match the proposed full-match predicate. A fresh scratch build with the actual twelve manifest keys plus DOC exits 0 and materializes thirteen texts. C16/V08 remain positive; no rename is required. |
| CE1-CP-002 | Resolved | D16 separates root administrative markers from nested markers and states individual inventory domains. Fresh E10 uses a real linked worktree and returns no repository errors. Fresh CH06 uses a nested regular `.git` file and returns a nested-repository error. D7 uses Git administrative-path discovery rather than assuming `.git` is a directory. |
| CE1-CP-003 | Resolved | D12 preserves the non-blank string trigger domain and S229/S258/S259/S262/S266 positives. The fresh string probe is accepted; True, list and blank probes are accepted by frozen tooling but fail the separately evaluated proposed predicate. N03–N05 therefore remain discriminating repairs without migrating legitimate string evidence. |
| CE1-CP-004 | Resolved | D2 explicitly separates pure-object, file-aware and roundtrip gates. Fresh P01p with WP-U in WP-U.yaml passes all four gates and CLI validation. Fresh P01a with WP-X in WP-U.yaml also passes the frozen gates: its revised oracle correctly requires only file-aware gates to change. Roundtrip stays byte/inventory equality and pure labels stay diagnostic. |
| CE1-CP-005 | Resolved | S330 is KEEP-POS; its fresh probe passes. M03 is a defensive regression, not a kill. C05 is POLICY, and the fresh CLI reports 8/8 checks with exit 0. A valid Unicode-Ü.yaml is materialized and committed on Windows, and frozen check_state returns no errors. Existing list rejection for updated_by/updated_reason is reproduced and retained. §5 distinguishes FIX, POLICY, regression and diagnostic/limit accounting. See the non-blocking editorial observation below. |
| CE1-CP-006 | Resolved | D8 separates exact CLI spelling from local-head resolution and defines HEAD/OID exceptions. Fresh deadbeef, qualified refs/heads/wp/test, HEAD and the full commit OID all pass frozen roundtrip in an equal-content fixture. CH09 keeps the actual hex-named branch positive; CH10 explicitly labels qualified-spelling refusal as policy. G08/G12 no longer confuse argument acceptance with fixture equality failure; J06–J08 exclude non-head resolution. |
| CE1-CP-007 | Resolved | Fresh CH07 exits 1 but changes existing DOC.md before the later hash failure, leaving the index unchanged. The new all-destinations-unchanged/no-new-output oracle discriminates that behavior. Fresh CH08 exits 0, writes DOC.md and SECOND.md, and indexes both. D14 distinguishes validation preflight from staged writes and replaces, states the permitted partial-replacement limit, and requires error diagnostics. It does not claim whole-build transactionality. |

No required checkpoint change remains open. The revised domains, component oracles and control
accounting introduce no identified blocking contradiction, false-pass oracle or unreasonable
refusal within this targeted scope. Untouched rows and decisions were not reopened.

## Independent execution and coverage

The fresh harness imports the six frozen modules and first compares each module's bytes against
docs reference `1422423e8fd7b163f498466d6596e3ef5741c53d`. Every new fixture proves its baseline
before mutation. All source builds and Git manipulations operate on disposable worlds inside
project `.tmp/work/codex/`, never the source bundle or either production repository.

Fresh CH01 again returns a containing-repository error normally and no error under an ambient
GIT_CEILING_DIRECTORIES ceiling. Fresh CH02 again rejects orphan-main CLOSED evidence normally,
passes it under GIT_REPLACE_REF_BASE=refs/hidden/ with refs/replace empty on both sides, and
rejects it after the proposed environment sanitization/overlay-disable settings. These are real
discriminating D7 witnesses; M03 need not be represented as a defect kill.

CH03–CH05's unchanged mechanisms use the independently executed evidence in the first checkpoint
review at `842076061caa4a0820d7a38993b750caf3f28103`. The revised plan explicitly uses the corrected
CH04 fixture with distinct recorded candidate and tip, not the earlier inconclusive fixture.

The independent parser finds exactly 700 unique row IDs: all 688 original IDs plus P01p and
CH01–CH11. Counts match §0 and §6:

| Disposition | Rows |
|---|---:|
| KEEP-NEG | 398 |
| KEEP-POS | 105 |
| OPAQUE | 84 |
| FIX | 99 |
| POLICY | 4 |
| LIMIT | 6 |
| DIAG | 4 |

FIX counts are CR-001=30, CR-002=23, CR-003=14, CR-004=4, CR-005=25, CR-006=3.

Evidence is retained under `.tmp/work/codex/ce1-checkpoint2-probes/`:

- `results.jsonl`: 22 executed observations, SHA-256
  `ddc9974699745dbf9a44abce8cc80a2131aecc869ea81bf9f9942a62f1b8166c`.
- `audit.json`: complete row-set/count audit and frozen-source hashes, SHA-256
  `5f74fcee03b1e4ab5bd842cd8ba8e81ae6f000fdc363709f9151bae488f3ebfc`.
- `classification.md`: exact reviewed blob, hash above.

Harnesses in `.tmp/work/codex/` are `ce1-checkpoint2-probes.py`, `ce1-checkpoint2-more.py`, and
`ce1-checkpoint2-final.py`. Their SHA-256 values respectively are
`3b4c4b41badb29afae3056123f5d1374f6722180e674da84d9a337f8acabf644`,
`7233de32ee391abf6fd965af33652c8905c0d52b17048670b49b1df378e0eeda`, and
`bdbe75aa34f136959943604e6b3106549fabf79c22bc44f6bb88ebdf09838773`.

Three observations are excluded from semantic-control credit: R2-P01p/R2-P01a used an incorrect
one-argument validate_state_file call; their corrected rows use the actual two-argument signature.
R2-U07 used invalid YAML and proves only path materialization; R2-U07-valid replaces it as the
chain witness. The remaining nineteen observations supply the fresh evidence above. Proposed
regex/type predicates are labelled separately from frozen execution; no prospective implementation
result is claimed. This pass ran on Windows, not a fresh POSIX host. The agreed implementation
plan still requires Windows and case-sensitive POSIX controls before closure.

## Non-blocking editorial observation

CE1-CP-008 — low: §3's descriptive finding summary retains stale FIX counts: CR-004=3,
CR-005=26, CR-006=4. It also still includes C05 in the CR-006 description, although C05 is now
POLICY in §0, D15, §5 and its row. The correct counts are 4, 25 and 3, as mechanically counted
above. Refresh that summary when maintaining the document.

This does not condition checkpoint agreement: §0 explicitly gives revision-2 totals, §6 explicitly
refers to those totals, and §5 derives control treatment from individual dispositions. No row
oracle or implementation decision depends on the stale descriptive counts. Required changes:
none. New blocking findings: none.

## Boundary verification

Main docs remains clean on wpP01/hardening at `958484200e574e1e8b86f97fe252d8da7d870836`;
code remains clean at `bb05e3953a044ea8abd9d796675290ad9fe80941`. The review changes only this
record on the authorized new branch. No production implementation, Claude-owned edit,
source-bundle edit, main acceptance, push or WP-01 worktree access was performed.
