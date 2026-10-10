# WP-02 Python implementation review - Codex

Date: 2026-10-11. Independent reviewer / Rust owner: Codex.

## Verdict

**CHANGES_REQUIRED** for docs `7d21a51437509d03417af2f327bc636f2af6b7b1` /
code `1d7167c85d4516dea6903ada6745139c3ac222f3`.

One blocking finding: **WP02-CR-006**, a contract-assurance defect in G3 discrimination
and its equivalence claim. No Python history implementation defect was found. The
candidate reports the correct result for the new witness; its existing suite accepts
a realistic wrong implementation that changes that result.

## Custody and scope

Followed `process/handoffs/WP-02-codex-python-implementation-review.md` at state head
`8ed033fb`. New docs branch `review/wp02-python-1` starts there, in
`review-worktrees/docs-wp02-python-review`; code is a separate exact-SHA detached
checkout in `review-worktrees/code-wp02-python-review`. Only this review record is
committed. Candidate contents, other worktrees, state and registry were not edited.
All environments, caches, mutations, targets and POSIX image are project-local.

Reviewed HIST-001/002/005/010 and SER-005/006 against G-048..G-055, their inherited
SER-008/HIST-004 rules, the full new implementation and exports, runner changes,
manifest links, corpus promotion, public-seam tests and author evidence. The spec
content is unchanged from agreed docs `6f761081`. The four corpus diffs from agreed
code `15b71ca3` contain only DRAFT -> ACTIVE; all 70 expectations are unchanged.
Prior Layer 01 closures were not reopened.

## Independent evidence

Windows, project-local locked CPython 3.12.8 environment:

- Ruff lint and format checks passed (14 files).
- Mypy strict passed on all 14 files.
- Full suite: **386 passed, 5 xfailed**; all 12 ACTIVE scenarios execute.
- Coverage 7.16.2, branch mode, subprocess patch and no exclusions: **740/740
  statements, 332/332 branches**, 100% for every module including `history.py`.
  Data combined from four worker files. A first scratch configuration/report naming
  collision caused non-database warnings during discovery; renamed those files and
  verified the clean report from the combined database. No missing coverage is masked.
- `mneme-process check --deep-sources`: **8/8** against this exact checkout pair.

POSIX, native WSL Linux with managed CPython 3.12.8: archived the exact code SHA
into an ext4 image under `.tmp/work/codex/wp02-python-review`, mounted in a private
user/mount namespace. Distinct `A` and `a` files proved case sensitivity. Temp files
were inside that image; bytecode and dependencies remained under project `.tmp/cache`.
Full suite: **386 passed, 5 xfailed**. The preliminary Windows-mounted-filesystem run
failed pytest's temporary-file capture before executing tests and is not pass evidence.
The image was unmounted after the successful run. No POSIX coverage total is claimed.

Own oracle executions on both Windows and POSIX:

- **24,192 admission observations**, varying reader closure and duplicates, profiles,
  token/type/edition validity, compatibility, recognition, missing/extra members and
  competing typed failures, through native and JsonText inputs. The separate oracle
  derives the routing/recognition/shape gates directly from the contract, uses its own
  lexical check and datetime arithmetic for the controlled timestamp domain. All match.
- **5,202 boundary observations** covering positions, numeric aliases, invalid shapes,
  tokens, same/different stores, both equality and ordering. All match.
- Additional Windows neighborhood controls: **22 passed**, including stages across
  arguments, exclusion/skip versus generic validation, native hostile scalar/container
  subclasses and JsonText storage, cycles, shape-before-fields and source-independent
  typed errors. Zero hooks invoked; depth-4,000 payload preserved.

These finite matrices do not establish correctness for every input. They complement
source inspection and the full suite; no Python-versus-Python result is used as a Rust
semantic oracle.

## WP02-CR-006 - P12 is observable and the suite lacks its kill witness

- **classification:** CONTRACT_ASSURANCE_DEFECT
- **owner_decision_required:** false
- **blocking:** WP-02 Python certification
- **requirements:** HIST-002, SER-008 (G-055 gate 4; G-034 canonical order)
- **status:** OPEN
- **Evidence:** candidate code `1d7167c8`, `core/history.py` gate-4 loop and
  `core/values.py` `_decode_text`, `_extract_native`, `_normalize`; candidate docs
  `7d21a514`, `assurance/reviews/WP-02-python-implementation-claude.md` P12 paragraph.

The record claims P12 is equivalent because normalization returns map members in
canonical insertion order. That is true for native extraction, but not JSON-text
decoding: `_normalize` preserves the decoded object's source insertion order. The
real gate-4 loop sorts again, which is necessary at this seam.

Minimal public-API witness, with the members in this source order:

```python
reader = {"profile": "learning", "recognized": [
    {"record_type": "attempt", "schema_version": 1}]}
record = JsonText('{"record_id":"BAD","profile":"learning",'
    '"record_type":"attempt","schema_version":1,"compatibility":"required",'
    '"recorded_at":"2026-10-11T08:00:00Z","occurred_at":null}')
admit_history_record(reader, record)
```

**Contract and candidate:** `timestamp.invalid`, argument `record`. Canonical typed
member order is `occurred_at`, `record_id`, `recorded_at`; therefore the null timestamp
wins over the invalid ID. **P12 mutant:** `id.invalid`, argument `record`.

I independently replayed all 12 exact mutations in isolated package copies. Existing
suite: P01..P11 fail their intended public/corpus controls; P12 **386 passed, 5 xfailed**.
I then executed the minimal witness as a pytest control: candidate **1 passed**; P12
**1 failed**, specifically the `id.invalid` versus `timestamp.invalid` assertion.
This is a discriminating survivor, not an equivalent mutant or a production-code bug.

**Required repair:** add a durable public-API JSON-text competing-field control, revise
the equivalence/evidence claim, and demonstrate candidate PASS / P12 FAIL. Sweep the
other text/native gate-4 order combinations without changing G-034/G-055 semantics.
No Owner choice or production repair is needed on the observed evidence.

## Other review conclusions

Reader closure, duplicate normalization, gate routing/exclusion/recognition, normalized
payload/provenance preservation, timestamp normalization and error arguments match the
agreed text. Boundary validation precedes relations and never manufactures cross-store
ordering. Generic stages run across arguments before typed rules. Returned envelope
contents are copied exact normalized built-ins and inputs are not mutated.

The three new runner operations each dispatch one public function and merely expose
its result/error. Python declares implemented layer 2; higher layers report xfail with
the language/layer visible. The Rust runner policy is separately reviewed as NF-026;
Rust does not yet implement these four ACTIVE history scenarios. No inference about
Rust Layer 02 approval is made here.

Reproduction scratch: `.tmp/work/codex/wp02-python-probes.py`,
`wp02-python-neighborhoods.py`, `wp02-python-mutants.py`,
`wp02-python-review-posix{,-start}.sh`, and `wp02-python-review/test_p12_kill.py`.
Outputs: `wp02-python-review/report.json`, `mutants.json`, per-mutant logs,
`posix-suite.log`, `posix-probes.json`, and `p12-witness.json`. Recipes and findings
are review evidence only; nothing was installed or written outside the project.
