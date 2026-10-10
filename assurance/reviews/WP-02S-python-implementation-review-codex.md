# WP-02S Python implementation review — Codex

**Verdict: APPROVED**

Date: 2026-10-11. Independent first complete G3 implementation review, following
`process/handoffs/WP-02S-codex-python-implementation-review.md` at state commit
`6881eb2265bc8d028158f6362c9ae5df1da08263`.

## Exact review objects and authority

- Docs: `e8b5695a62db902ee9cb6419ad07595c378ae696`.
- Code: `5d1a74a56585c450fd5f6ce8fe7020318cbed914`.
- Agreed contract: docs `c08c57e46c0c972d0e497f74df311e0241cb8b5c`, code
  `0c569afba20477e0687a1de837b70e4b8996fa1e`; prior approval `697e372c`.
- Authority: G-056..G-064, recorded verbatim in
  `reference/governance/2026-10-11-owner-wp02s-memoryscope.md`, the Layer 02 MemoryScope
  contract in `spec/scope.md`, and SER-008's generic stages and scope error rows.
- Claude's `assurance/reviews/WP-02S-python-implementation-claude.md` was a challenge
  object; its observations were independently checked below.

Reviewed in separate worktrees: detached code at the exact SHA, docs review branch
`review/wp02s-python-1` from the handoff state. No production changes, candidate commits,
state edits, registry edits or source-bundle edits were made. All environments, caches,
probe copies and POSIX filesystem images stayed under the project root (OWN-001).

This approves the requested WP-02S implementation review scope. It neither accepts the
pair onto main nor closes WP-02. The inherited WP02-CR-007 Python runner order defect
remains covered by that existing finding, as explicitly directed in the task; this
review does not duplicate or close it. Carry its repair into the eventual integration.

## Contract and implementation challenge

Read the whole new `core/scope.py`, its public exports, tests, runner mappings, manifest
changes, normative contract and Owner decisions. The scope implementation matches the
agreed text without a new observable author choice:

| Surface | Assessment |
|---|---|
| Scope value and equality | Only the two closed records are admitted; empty resolved scope is global; unresolved is distinct. Exact map equality preserves absent versus present facets and ignores member order. Validation returns fresh exact built-in containers. |
| Facet names and values | Names implement G-064's two 1–128-byte ASCII segments and one dot, with no device restriction. Values use CORE-001, including its device and trailing-dot exclusions. `agent.con` is preserved as an unknown facet; it is not a malformed name. |
| Registry and matching | Exactly the six Agent facets, without aliases, inferred hierarchy or Learning adoption. Every record facet must explicitly match; extra known query facets do not narrow broader records. Unresolved and unknown-facet records are hidden. |
| Errors and seams | All arguments pass generic stages before typed scope validation. Typed errors check record then query, or a then b, with those argument names. Single-argument `validate_scope` names none. An invalid query is rejected even when the record would be hidden. |
| Deferred obligations | Capture completeness, immutable record revisions, retrieval absence/privacy and Learning adoption remain at their documented consumer layers. The matcher does not claim to implement those consumers. |

The runner adds exactly three operation dispatch entries, each calling one public
function and wrapping the result. It does not implement scope semantics or alter
expectations. Existing Layer 01 and history production modules are unchanged from
WP-02 `43e0984e`.

## Independently executed evidence

Project-managed CPython 3.12.8 with candidate-locked dependencies was used on Windows.
Tests imported the exact candidate source, rather than another editable checkout.

| Check | Result |
|---|---|
| Whole Windows Python suite, including subprocesses | 467 passed, 5 xfailed |
| Whole POSIX Python suite | 467 passed, 5 xfailed |
| Coverage 7.16.2, no exclusions, subprocess coverage combined | 804/804 statements and 352/352 branches; scope.py 63/63 statements and 20/20 branches |
| Ruff check / format check | Clean; all 16 files formatted |
| Mypy strict | Clean, 16 source files |
| Deep process checks | 8/8 passed: repos, sources, spec, manifest, conformance, findings, registry, state |
| Corpus promotion comparison | All three YAML scenarios differ from agreed `0c569afb` only in DRAFT → ACTIVE; 73 expectations unchanged |
| Independently derived corpus oracles | 73/73, then 146/146 public observations across native and JsonText seams |
| Six-facet matching cross-product | 46,656/46,656: each record facet absent / v / w, each query facet absent / v |
| Equality and member order | 729/729 independently generated resolved records |
| Generic precedence and typed diagnostics | 20 direct rejection controls passed, including later-argument duplicate, nonfinite, cyclic and out-of-range failures outranking an earlier typed scope error |
| Hostile scope/query dicts and string keys/values | Zero subclass hooks; exact returned containers and strings; validator, equality and matcher checked on candidate and S03 |

The independent contract model also checks 19 grammar/value/naming controls, including
the 257-byte full name and the separation between reserved names and reserved values.

The POSIX run used managed Linux CPython 3.12.8 and a Git archive of the exact candidate
on a project-local ext4 image mounted inside a user mount namespace. Distinct `A` and
`a` files confirmed case sensitivity. Temporary files, image, dependencies and logs
remained under the project; there was no write to the system Python installation.

## S03 equivalence challenged, not assumed

Independently replayed all eleven literal mutations from Claude's driver in separate
scratch source trees against the candidate's entire Python suite. S01, S02 and
S04..S11 each failed an actual conformance test; S03 alone passed. Test failures were
checked for named failing tests, so import/setup failures were not counted as kills.

The label “unknown record facets ignored” overstates what S03 changes. The actual
mutation only removes the explicit unknown-facet rejection guard; it leaves every
facet in the final `all(...)` comparison. It does not filter the record map.

The equivalence follows for all admitted inputs, not just the sampled corpus:

1. Generic validation extracts exact built-ins before either typed rule. Subclass
   equality, lookup and iteration hooks cannot change subsequent comparisons.
2. Record validation requires every facet value to be a portable-token string.
3. Query validation rejects every key outside the fixed registry before matching,
   even for unresolved or unknown-facet records.
4. Hence an unknown record key is absent from any valid query. Its lookup yields
   `None`, which cannot equal the required string. The unchanged conjunction is
   false, just as the explicit guard requires.
5. Unresolved records return false before that guard in both versions; earlier generic
   or typed errors are unchanged.

Executed 640 independently derived native/text comparisons against both the original
and S03 (1,280 observed calls), sweeping five unknown names, eight valid/invalid
values, optional known constraints and four valid/invalid queries. They agreed with
the contract model. Hostile subclass controls also passed with zero hooks on both.

As a discriminating control, I planted the genuinely different behavior: remove the
guard and filter unknown keys out of `facets` before matching. The candidate corpus
killed it in `core/scope-applicability-matching.yaml`. This verifies that preserving
unknown constraints is tested; accepting S03's equivalence does not excuse dropping
unknown facets. There is no analogue of WP-02 P12's surviving source-order defect here.

## Evidence locations and disposition

Scratch evidence, outside both candidate repositories:

- `.tmp/work/codex/wp02s-python-probes.py` and `wp02s-python-neighborhoods.py`:
  independent derivation, public observations, combination sweep, hooks and controls.
- `.tmp/work/codex/wp02s-python-mutants.py`: reviewer-owned mutation replay.
- `.tmp/work/codex/wp02s-python-review/`: `derived.json`, `grammar-controls.json`,
  `probe-summary.json`, `neighborhoods.json`, `mutants.json`, individual mutation logs,
  `drop-unknown.log`, coverage `settings.ini` / `report.json` / `run.coverage`, and
  `posix-suite.log`.
- `.tmp/work/codex/wp02s-python-posix.sh` and its starter: POSIX reproduction recipe.

No new finding, no new path-C question and no reopening of prior scope closures.
The scope G3 evidence is reproduced. S03 is equivalent as literally planted, and the
true unknown-dropping violation is discriminated. The existing WP02-CR-007 remains
open outside this scope review's disposition.