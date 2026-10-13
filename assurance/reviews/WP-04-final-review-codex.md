# WP-04 final complete review — Codex

**Verdict: CHANGES_REQUIRED**

Exact pair: code `9d5a2d51c69987f799962868b8dc5175a11882d2`, docs
`ef5c13ff4b5d48f41648d083b11aeafa0be7545f`. Review branch `review/wp04-final`
starts at state-only descendant `48092f11`. Its delta from the content candidate
is confined to `process/state/WP-04.yaml` and `WP-04T.yaml`.

I reviewed the whole WP-04 contract, five ACTIVE scenarios, manifest, Python
store and consumed lower-layer seams, Rust readiness, governance and records.
The runtime and corpus pass. **WP04-CR-015 is resolved.** The blocker is the
obsolete/incomplete current assurance package below, not a new Python defect.
CE-04-01 and CR-001..014 stay settled; no new semantic choice or production
implementation pass is requested.

## WP04-CR-016 — the final assurance index still describes the pre-convergence catalog surface

- Classification: **CONTRACT_ASSURANCE_DEFECT**; severity: **medium**.
- `owner_decision_required: false`; status: **OPEN**.
- Blocks **WP-04 final approval / transfer to Rust implementation**.
- Authority: this handoff items 5–6; G-094..G-098; the current reference-backend
  contract; `process/templates/cross-language-feasibility-matrix.md` (transitive
  path, current candidate/evidence, audited library premises and complete
  neighborhood record).
- Evidence: exact docs above, `plans/WP-04.md`,
  `assurance/layers/04-feasibility-matrix.md`, `spec/persistence.md#pers-008`,
  `assurance/findings/WP-00-findings.yaml`, and the committed closure history
  specified below. This is an executable-file/record inspection, not a
  speculative implementation counterexample.

Concrete discrepancies:

1. The plan's current status is **CONTRACT_CONVERGENCE**, its lead governance
   stops at **G-093**, and its matrix row calls the matrix a contract-stage draft
   with PLANNED rows. Its final historical row correctly says the episode is
   settled and the candidate goes to FINAL_CONTRACT_REVIEW. These are not one
   consistent current assurance index.
2. The matrix explicitly identifies its Python evidence as **`63462513`**, its
   contract as revision 3 / **`d857fcc2`**, and its governance as **G-077..G-087**.
   H8 schema-version assurance is still columns/constraints and ten damaged-shape
   controls. Its READY summary does not cover the dependency island, internal
   member certification, whole-row exclusions/normalizations/inventory,
   environment and genuine-object binding, or the [F] evidence method. Its
   neighborhood table omits the CE-04-01 characterization, extension, agreed
   checkpoint and closed counterexamples. Those are central Rust requirements,
   not merely later test totals. The evidence key [MU] describes P01–P20 although
   the status text claims 23; [PT] still says 20 tests. There is no current
   catalog-control/evidence index to reconcile these claims with the final
   candidate and run 5.
3. PERS-008 still says its representation depends on the **unresolved NF-016**.
   In this tree NF-016 is **OPEN**, without its recorded resolution; NF-026 is
   likewise OPEN although both runner rules are implemented/accepted. The prior
   post-acceptance commit **`3ba0607c8e935f118d2db7f7d2b879b8014feb42`** contains
   their CLOSED dispositions and resolutions, but is **not an ancestor** of
   this content candidate (verified with `git show` and `merge-base
   --is-ancestor`, exit 1). The current registry already marks WP-02 certified
   under G-065. This is missing/currently contradictory coordination evidence,
   not grounds to reopen HistoryBoundary semantics or the approved runner fix.

Required repair, under the existing authority:

- Make the plan and matrix a current, internally consistent assurance index
  through G-098. Identify the present candidate/evidence and explicitly label
  superseded stages/counts as history.
- Extend the matrix's value/capability/hazard/order/neighborhood coverage to the
  settled catalog surface, with exact spec/checkpoint anchors and current [P],
  [T], [E], [Pr], [F] witness locations. Include the shared pins, whole-row
  exclusion/association rules and inventory, cached-value versus E004 distinction,
  inbound/outbound dependencies and member certification, and genuine SQL binding.
  Preserve the actual cross-language [IT] obligations as due at the Rust candidate;
  do not mark them executed. Refer to the bounded P38/P14 conclusions accurately.
- Reconcile the already-decided NF-016/NF-026 dispositions with their recorded
  post-acceptance resolutions, and replace or explicitly historicize PERS-008's
  obsolete unresolved note. Do not change their settled semantics or invent a
  new Owner decision.

The classification/checkpoint and implementation record contain the underlying
evidence. Appending their history to the plan without updating the required
matrix's asserted current premises does not satisfy final assurance readiness.
No production change is needed to discharge this finding.

## Complete-review observations

| Surface | Conclusion |
|---|---|
| Contract / governance | The operative Layer 04 section follows G-077..G-098 and the consumed G-013/G-031/G-033/G-051/G-054/G-055 decisions. Strict writes, normalized draft mutation, idempotency-before-duplicates-before-capacity-before-clock, gapless allocation, one read snapshot, and receipt durability are consistent. PERS-007's deferred parts have explicit owners. The stale PERS-008 note is included in CR-016 rather than treated as a new semantic uncertainty. |
| Corpus / traceability | All **65** expectations follow the operative text: 14 gapless, 19 strict-writer, 12 retry, 4 no-dedup, 16 bounded-read. Clock consumption follows only new successful attempts in these scenarios; offset spellings canonicalize; wider writer recognition does not alter mutation; NUL identity bytes stay distinct; pages may split committed batches and keep the shared tail. JSON stage-1 failures precede typed failures. Manifest backlinks and Python locations validate. Crash/concurrency/capacity/catalog controls are outside the backend-neutral corpus as declared. |
| Python / runner | Reviewed the four operations, transaction lifecycle and per-handle lock, row-lock serialization, draft-mode admission, typed/generic precedence, canonical storage/retry reconstruction and snapshot reads. No new contract violation found. The stateful runner invokes the public store; its JSON store-ID decoding binds the clock fixture and does not perform store semantics. Python declares layer 4; Rust remains layer 3 and reports these ACTIVE scenarios as above-layer xfails until its implementation. |
| Catalog | Settled catalog/pin/control code is unchanged. The full suite exercises the agreed acceptance/refusal, transaction, engine, predicate, fetch and inventory controls. Whole-row members and boundary remain part of open validation; open performs no row audit and does not promise protection from post-open out-of-band edits or references with no recorded catalog dependency. |
| CR-015 | **Resolved.** Current record §2 correctly says 58 predicates and 18 field controls, identifies the internal RI trigger source, and explains the three-part index projection and P31's bounded first-part fetch kill. The changed test comment matches those measured observations. Historical failed runs remain historical failures. |
| Records | Current state has the correct exact pair and FINAL_CONTRACT_REVIEW; content-to-state descendant touches only state files. The implementation record identifies run 5 correctly. Plan/matrix and older finding-resolution reconciliation need CR-016's repair. |

## Rust readiness assessment

The operative contract, shared `reference-backend/postgres14-v1-catalog.json` and
agreed checkpoint are technically implementable; Python behavior is not the
oracle. The assurance matrix must document the same obligations before transfer.

- Reuse certified Layer 01 stages/canonical bytes and Layer 02 reader/boundary
  rules; add draft admission without reopening their semantic domains.
- Preserve exact UTF-8 operation-ID bytes in bytea; use bounded i64 positions,
  normalized caller-draft bytes for mutation, and canonical timestamp strings.
- Explicit Read Committed open with the shared single-bigint advisory lock first;
  qualified catalog/type/function/operator/aggregate/DDL bindings; initializer
  pins and pre-commit catalog postcondition; Repeatable Read read-only snapshots;
  one per-store row-lock boundary and a whole-operation handle lifecycle.
- Independently fetch every required part and compare shared pins, including
  index_columns, whole-row members, their finite exclusions and normalized
  backlinks/type copies/counts, and dependency/security-label boundary. Preserve
  PostgreSQL jsonb-text member documents as specified, rather than applying JCS
  to those embedded texts. Inventory must make omitted/new catalog fields visible.
- Port actual-fetch [F] controls over Rust's own query seam; do not claim
  unavailable privileged physical states as public executions. Retain the
  coupled-index control's measured scope and E004's separate row-trust oracle.
- [IT] remains due: Python→Rust and Rust→Python write/read/retry, exact canonical
  byte compatibility including NUL operation IDs, mixed concurrent first opens,
  and waiting openers with a Repeatable Read session default. Raise implemented
  layer only in the Rust candidate and pass every ACTIVE scenario through 4.

The synchronous rust-postgres API supplies explicit isolation/access-mode
transaction builders and bytea/String/i64 conversions; this is a documentation
feasibility check, **not** a compiled/audited Rust backend or a dependency pin.
Those premises need execution with the chosen pinned crate in the Rust pass.
[TransactionBuilder 0.19.14](https://docs.rs/postgres/0.19.14/postgres/struct.TransactionBuilder.html),
[FromSql 0.19.14](https://docs.rs/postgres/0.19.14/postgres/types/trait.FromSql.html).

## Independent evidence and limits

Own logs: `.tmp/work/codex/wp04-final/`.

- Fresh exact-code Windows static checks: ruff check/format and strict mypy,
  **26 files**, pass.
- Fresh full suite: **856 passed, 4 xfailed**, **237.80 s** (`windows-suite.log`).
- Fresh coverage: **1304/1304 statements, 490/490 branches**, zero misses, **100%**,
  no exclusions, subprocess patch and four combined data files (`coveragerc`,
  `coverage.json`, `coverage-report.txt`).
- Read-only process/schema/manifest/source validation of this content/state
  pair: **8/8**, including deep sources (`process-check.log`). Those mechanical
  checks do not detect the semantic freshness contradictions in CR-016.
- Inspected the final author's exact run-5 G0/G1/G2/G3/G4/G5 logs: their counts
  agree with record §5.3. My closure-2 independent mutation replay was **58/59**
  and **17/18** with only P38/P14, and its POSIX case-sensitive full suite was
  **856 passed, 4 xfailed**. Those are evidence at parent `03841628`, not newly
  executed mutation/POSIX batches at `9d5a2d51`. The complete code delta is a
  comment in one test file; production, pins, test executable statements and
  mutation bodies are unchanged, so no new contrary evidence reopens them.

Every shell sourced the project environment; interpreter/cache/temp outputs
stayed inside the project. The full Windows batch was already running when
the host queue asked for a hold; it was allowed to finish, then host-clear was
sent and new native/test/mutant/Docker batches were held. Subsequent work was
paper review and read-only document validation. No production, contract,
registry, state, remote or other worktree was edited. Only this review record
is committed.

Targeted follow-up: CR-016's documentary repair and its direct consistency
neighbors. CR-015 and the settled implementation closures need no new fix pass.
