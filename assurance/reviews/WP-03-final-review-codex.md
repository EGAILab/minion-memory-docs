# WP-03 — final complete review (Codex)

**Verdict: CHANGES_REQUIRED**

**Exact pair:** docs `6fe9115d91715c3e8732235a43936bd1b29a9d76` / code
`dd55fb4f0abec262d7ba0dab64f28a74840b84c3`.
**Handoff:** `process/handoffs/WP-03-codex-final-review.md` at `36bb5726`.
**Reviewer:** Codex, independent reviewer and Rust implementation owner.
**Date:** 2026-10-11.

The complete contract, ACTIVE corpus and Python implementation are consistent with the recorded
Owner decisions. No new implementation defect was found. One blocking assurance finding remains:
the WP-03 plan and mandatory feasibility audit are not a current, complete handoff to Rust.
CR-001 through CR-006 remain closed; their semantic decisions are not reopened.

## WP03-CR-007 — incomplete and stale Rust assurance handoff

- **Classification:** CONTRACT_ASSURANCE_DEFECT.
- **Severity:** medium. **Status:** OPEN. **Blocking:** WP-03 final approval / Rust handoff.
- **Owner:** Claude. **owner_decision_required:** false.
- **Affected requirements:** PROJ-001/002, HIST-006/007; consumed SER-008/009 and HIST-004.
- **Resolution:** documentation and assurance repair; no new contract semantics proposed.

**Pinned evidence:** docs `6fe9115d91715c3e8732235a43936bd1b29a9d76`:

1. `plans/WP-03.md:3` still reports `CONTRACT_REVIEW` and G-066…G-070; lines 26–27 describe
   **31 DRAFT steps**. Its last history section ends with review 1 and 49 DRAFT steps. Lines 34–35
   still flag duplicate decoded record IDs as errors and duplicate relation triples as invalid,
   without explaining their subsequent disposition. The actual agreed contract requires identical
   canonical envelopes to coalesce (G-073), equal normalized relations to collapse (G-072), and
   the candidate contains **54 ACTIVE steps**. The plan is also the registry evidence pointer and
   the state's assurance index, so its current summary must distinguish the historical proposal
   from the agreed behavior and link the later reviews and implementation evidence.
2. `assurance/layers/03-feasibility-matrix.md:3–4` remains a DRAFT CONTRACT_REVIEW artifact through
   G-074, omitting G-075 from its authority range. Its relation row does not enumerate the two
   closed immutable artifact identities and their CORE-001/002/011 domains.
3. The matrix's entire hazard section (lines 18–24) contains only aggregate H5, recursion depth,
   and aggregate H8–H10 rows. It supplies no probe/output reference for the `AUDITED` claims,
   no lower-layer capability matrix, and no per-member dispositions for the transitive families
   reached by this WP. Concrete omitted seams include canonical envelope equality and hashing
   (H7), numeric normalization and cursor/edition bounds (H1), timestamp normalization before
   coalescing (H4), relation/identity integrity (H11), and inherited decoding/string boundaries
   (H2/H6). H5 itself is not expanded into its prescribed members.

This is a completeness issue under `process/agent-workflow.md` §3 step 5 and
`process/templates/cross-language-feasibility-matrix.md`: audit the transitive path, list touched
family members, record reviewed lower-layer seams and additive extensions, and attach evidence
to AUDITED claims. `process/hazard-families.md` explicitly requires every member of a touched
family. The template states that an incomplete matrix is a CONTRACT_ASSURANCE_DEFECT.

**Required repair:** refresh the plan as a current assurance index through G-075 and the completed
Python review history, retaining obsolete proposals only as clearly labeled history. Complete
the matrix with exact spec anchors, target identities, stage seams, bounds, lower-layer reuse,
the additive Rust error-position/code extensions, and per-member dispositions/evidence. Existing
certified lower-layer probes and these review executions may be cited with explicit applicability;
there is no need to implement Rust or repeat unrelated lower-layer characterization. In particular,
record the early-shape versus late-graph oracle and its paired-entry kill witness, not only the
phrase “early shape checks, then late graph checks.”

The state and registry's pre-acceptance language statuses are appropriate. This finding does not
require marking Python certified or accepting a candidate before independent approval.

## Complete contract and authority review

Read HIST-006/007, PROJ-001/002 and the consumed SER-008 stage rules as one contract, against the
verbatim G-066…G-075 record. Their semantic text is unchanged from the agreed `b514c16d` contract.

| Decisions | Verified contract behavior |
|---|---|
| G-066/067 | One purpose-neutral projector and shared lineage semantics; durable append remains Layer 04. |
| G-068 | Profile payload owns durable encoding; the core consumes decoder-produced typed relations and owns vocabulary/resolution. No closed-envelope extension. |
| G-069 | Current is set-valued; no time, ID or position tie-break. Presentation order selects no head. Purpose-specific selection is documented and versioned. |
| G-070 | Unknown-required admission fails atomically with position and full routing identity; no argument or partial projection. |
| G-071 | All record self-links invalid; combined resolution-family cycles and independent derivation cycles rejected; no extra cross-family rule. |
| G-072 | Strict available resolution endpoints, unavailable derivation targets retained, normalized duplicate relations collapse. |
| G-073 | Complete normalized canonical envelope equality coalesces repeated IDs at first occurrence; conflicts fail at the first later conflicting position; distinct IDs never semantically deduplicate. |
| G-074 | Interpretation membership is direct only; replacements inherit no observation association. |
| G-075 | External derivation target is exactly a versioned artifact pair or canonical content hash; invalid alternatives fail early; external targets remain unresolved. |

No new path-C choice or contradiction was found. Missing artifacts remain unresolved, not a reason
to invent a resolver; compatible checkpoints remain a Layer 05 extension. Prior contract closures
stand. The finding concerns the handoff's assurance completeness, not these agreed semantics.

## Corpus, traceability and runner

The two projection scenarios are ACTIVE, with **18 canonical-path + 36 lineage steps**. The
four owning manifest rows link their spec anchors, the scenarios and the real Python projector;
Rust locations correctly remain null before implementation. Back-links and the full corpus
pass the mechanical checks. All 54 expectations were independently derived in the prior contract
review and replayed against this exact implementation through every combination of native and
JsonText arguments (**432 comparisons per platform**).

Python declares layer 3. The projector operation in the runner is one library call; the runner
observes results and error code/argument/position without implementing lineage or admission.
Rust still declares layer 2 and reports the two layer-3 scenarios as explicit expected failures
under the implemented-layer rule; this is appropriate, not a missing Rust approval.

## Python implementation and G3 at the exact code

Reviewed the whole projector, error extension, public exports and runner, including the certified
admission and value seams it consumes. Global generic stages precede argument shapes; early
lineage validation precedes admission; admission and repeated-ID checks precede late graph
checks. Canonical bytes, not Python structural equality, determine complete-envelope equivalence.
Separate iterative graph checks implement the two families. Direct interpretation membership
and the four target presentation categories match the contract.

Fresh gate batches ran sequentially. All shells sourced the project environment first; Python
3.12.8, temporary directories, caches, build output and mutants remained project-local.

| Execution | Observed result |
|---|---|
| Windows full Python suite | **496 passed, 5 xfailed** |
| POSIX full Python suite | **496 passed, 5 xfailed** |
| Coverage 7.16.2, subprocesses included | **985/985 statements, 432/432 branches**, no exclusions or partial branches |
| Ruff check / format check | Clean; 18 files |
| Mypy `--strict .` | Clean; 18 files |
| All process checks, `--deep-sources` | **8/8 PASS** |
| Rust `cargo test --locked --offline --test conformance` | **5/5 PASS**, including promotion and runner controls |

The POSIX run used an exact git archive of `dd55fb4f` on a project-local ext4/FUSE image in WSL;
distinct `A` and `a` files prove case sensitivity. No system Python was used.

On both platforms, the independent projection model exercised the same deterministic 12,000
generated cases with zero disagreements on compared contract fields, plus the 432 public-seam
scenario comparisons. Diagnostics were checked separately: 16 full-triple observations, 48
additional routing boundary/seam controls and six hostile-subclass routing controls per platform.
No hooks were invoked. The targeted closure independently showed all eight routing controls fail
when the profile is omitted in a reviewer-owned copy. Input ownership, generic stage precedence,
canonical coalescing and error-position cloning controls continue to pass.

Fresh final-review controls add **360 comparisons per platform**: 11 early lineage shape defects
and four late graph defects paired with unknown-required, invalid-ID or invalid-timestamp entry
failures, through all eight argument seam combinations. Early defects always win as
`lineage.invalid/relations/no position`; late defects permit the entry failure to win with its
contract code, argument and position 7. This directly pins the early-versus-late Rust seam.

Also replayed all 12 disclosed violations against reviewer-owned copies of this exact code:
**12/12 killed by runtime test failures**, with a passing unmodified baseline and verified imported
module paths. Q02's source replacement was adapted to the CR-006 diagnostic refactor; its violation
remains continuing past an unknown-required record. The initial stale replacement was refused by
the driver's exact-match assertion and was not credited as a kill. Original Q07 removes endpoint
handling as well as reinterprets cycle handling and first dies with a host KeyError; a narrower Q07
retaining endpoint checks is killed by the cycle assertion. Q10 is killed specifically by the
paired early-artifact/entry-error control. No syntax, import or collection error is a credited kill.

## Rust readiness assessment

The semantic contract is implementable independently from the text and corpus. Existing Rust
`Input`, staged `validate_arguments`, flat-arena `Value`, timestamp normalization and canonical
serialization can express the domain without narrowing it. The implementation must reuse the
certified admission rules after global staging, adding access to internal normalized reader and
envelope admission as needed. Calling per-entry public APIs before whole-argument staging would
change error precedence and is not an acceptable shortcut.

Required additive work includes the stream/lineage/duplicate-ID error codes and a separate optional
store position on `Error`; the existing byte-offset diagnostic helper is not that field. Relations
need explicit record/versioned/hash target variants, normalized equality, separate iterative graph
checks and an explicit total presentation key. IDs and kind names are ASCII, while payload object
serialization retains the certified UTF-16 ordering. Canonical timestamp normalization must occur
before envelope equality. Raising Rust's implemented layer to 3 must pass both ACTIVE scenarios.

These are feasible implementation mechanics, not Owner choices or a lower-layer semantic reopening.
The missing recorded capability/hazard audit is nevertheless the blocking handoff defect above.

## Evidence and outcome

Reviewer-owned evidence/drivers under `.tmp/work/codex/`:

- `wp03-final-coverage.json`: fresh complete coverage report.
- `wp03-final-seams.py`, `wp03-final-seams-windows.json`, `wp03-final-seams-posix.json`: 360 seam controls.
- `wp03-final-posix.sh`: exact-archive, case-sensitive POSIX suite and independent probes.
- `wp03-final-mutants.py`, `wp03-final/mutants/summary.json` and per-copy logs: fresh baseline and
  disclosed/narrowed mutation controls at the exact code.
- `wp03-python-review-2/`: routing observations, independent model replay and missing-profile kill evidence.

No production modules, shared state, registry, source bundle or author-owned worktrees were edited.
Only this review record is committed. Open finding: **WP03-CR-007**. Repair the current assurance
handoff and return the documentary delta for targeted re-review; no Python remediation is requested.
