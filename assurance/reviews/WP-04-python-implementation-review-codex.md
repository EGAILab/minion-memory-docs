# WP-04 independent Python implementation review — Codex

**Verdict: CHANGES_REQUIRED**

Date: 2026-10-11. Four blocking findings, WP04-CR-008..011, are described below.
This reviews the implementation candidate; it does not accept it onto main or
certify Layer 04. The agreed contract and the closure of WP04-CR-001..007 stand.

## Review object and authority

- Code: `afb36081fc569246e6055f2bde99ca9481ca5e8a`.
- Docs content: `b94d0fde9118a33d5eba7055a0060c3531ea0327`.
- Review branch: `review/wp04-python-1`, based on the supplied state descendant
  `53068d0aab6e10c9f17f6354e2d9ee3ab12d2b86`.
- Authority: agreed docs `d857fcc27d54a44738d870473062f16ba3af493c`, agreed
  corpus `1f4438763c91fb95a4e88d86ac96302d9830cdb3`, Owner G-077..G-087
  (and the referenced G-013/G-051/G-054), and the adopted G3 gate.
- Separate checkouts: `review-worktrees/code-wp04-python-review` and
  `review-worktrees/docs-wp04-python-review`. Only this review record is authored
  in a repository. Production, registry and state files are unchanged.

The state descendant adds the handoff and changes the WP-04/WP-04T state files;
it is not production evidence. The normative spec is unchanged from the agreed
contract. Each of the five scenario diffs changes only DRAFT to ACTIVE: the
63 expectations independently derived in contract review 2 are unchanged.
Python declares implemented layer 4. Lower-layer closures were checked for
direct regressions, not reopened on the basis of suspicion.

## Executions

Own notes and drivers: `.tmp/work/codex/wp04-python-review/`. Commands sourced
the project environment; the venv, caches, pytest temporaries, coverage data,
mutation copies and POSIX filesystem image are project-local. Python is
uv-managed CPython 3.12.8; a new review venv was synchronized with the candidate's
lock. In particular psycopg/psycopg-binary are 3.2.13 and coverage is 7.16.2.
PostgreSQL reports 14.12, `mneme_dev`, not superuser, `synchronous_commit=on`
and `fsync=on`. Throwaway databases use template0, UTF-8, C/C and mneme_ts.

| Execution | Independent result |
|---|---|
| Windows full suite, exact code | 521 passed, 4 xfailed |
| Full certified Python coverage, branches and subprocesses included, no exclusions | 1,154/1,156 statements; 470/470 branches; FAIL against G3's 100% floor |
| Ruff check / format check | clean; 23 files formatted |
| Strict mypy, src and tests | clean, 23 source files |
| `mneme-process check --deep-sources`, exact review objects | 8/8 |
| Mutation baseline, original store/conformance slice | 25 passed, 23 deselected |
| P01..P20 from scratch source copies | 19 killed; only P14 survives, equivalent on valid gapless snapshots |
| Independent paging controls through JsonText | 196 cases, exact positions/through/tail, including MAX limit |
| Tuple/native retry of the same JSON-written mutation and NUL operation identity | original receipt, one clock call |
| Independent generic/typed/draft precedence controls | six expected codes/arguments, all with no position |
| Abort injected at operation insertion, after record insertion | no additional tail, record or operation persisted; retry receives positions 2..3 |
| POSIX full suite, exact archived code on a case-sensitive ext4 image | 521 passed, 4 xfailed |
| Rust canonical runner on the promoted corpus, implemented layer remains 3 | 5 tests passed; 17 ACTIVE / 343 steps; 9 explicit xfails, including all five layer-4 scenarios with layer/language reasons |

Evidence files: `pytest.log`, `coverage.json`, `ruff.log`, `format.log`,
`mypy.log`, `process.log`, `probe-results.json`, `additional-results.json`,
`mutant-results.json`, `mutant-followup.json`, `posix-suite.log`,
`rust-conformance-final.log`, and per-mutant logs.
Coverage was measured before executing the reviewer-added controls; those
controls cannot inflate the candidate-suite coverage result.

The POSIX run used the project-local managed Linux Python and psycopg 3.2.13
wheel with the existing project-local test dependencies. Distinct `A` and `a`
files confirmed case sensitivity. WSL loopback could not reach the Windows
service: the first run's 25 backend connection failures are retained separately
and are not candidate defects. A direct relay also could not be reached and that
attempt was interrupted. A temporary reverse TCP relay, using Windows-initiated
connections to the WSL listener, then passed a connection preflight reporting
PostgreSQL 14.12 / mneme_dev and the full suite. It changes transport only, not
the backend, role, schema rules or tests. No firewall or service configuration
was changed. Both relay helpers were stopped, the private temporary connection
file removed, and the image unmounted. The final database inventory contains no
mneme_test databases or sessions (`cleanup.log`).

The mutation data was read without executing Claude's driver. The source copies
were mutated under own notes, while tests/corpus remained the exact candidate.
Each kill is a pytest assertion failure, not an import failure or timeout. The
first focused P10 selection used an already canonical clock and therefore
survived. Replaying P10 against the baseline-proven full store slice kills it
in the gapless-position scenario with the offset-spelled clock. That initial
selection miss is retained in the logs, not presented as a second survivor.
P04 is independently killed once; Claude's claimed three-run rate is not claimed
as a reviewer execution.

## Blocking findings

### WP04-CR-008 — Schema open admits an unusable v1 shape or leaks a catalog error

- Classification: `IMPLEMENTATION_DEFECT`.
- Severity: high. Status: OPEN. Blocking: WP-04.
- `owner_decision_required: false`.
- Authority: agreed `spec/persistence.md`, Reference backend DDL and Open and
  initialize; candidate code `persistence/postgres.py:149-168`.
- Also affected: matrix H8's AUDITED incompatible/malformed-schema evidence.

Execute these separately against fresh, correctly initialized throwaway backends:

```sql
ALTER TABLE mneme_schema RENAME COLUMN version TO revision;
-- or, on the second backend:
ALTER TABLE mneme_store DROP COLUMN tail;
```

Then call the public `PostgresHistoryStore.open(params, clock)`.

The first backend raises raw `psycopg.errors.UndefinedColumn` from
`SELECT array_agg(version) FROM mneme_schema`, rather than the specified
`persistence.schema_incompatible`. The second backend is accepted. On that
returned handle, `create_store('s')` succeeds, then `store_tail('s')` raises
`UndefinedColumn` because tail is absent. This is not an I/O outage: all queries
use the same live service and role as the passing baseline. It is a deterministic
schema incompatibility.

The check observes only four names and the aggregated version value, not the
structural preconditions of the normative v1 tables. Both malformed examples
retain the four names, and the second retains the valid singleton version row.
The existing four incompatibility controls (version 2, absent row, extra table,
missing table) do not discriminate these examples. H8 additionally names
two-row evidence, but no corresponding control is present in the candidate tests.

Required repair: reject incompatible v1 structure at open with the specified
schema error and no schema/data changes. Characterize the required columns,
types and constraints against the declared schema, rather than equating a
matching name/version inventory with that schema. Preserve the agreed lock and
explicit Read Committed protocol; do not hide genuine DDL or availability errors
under a blanket exception handler. Add public-open controls and correct the
H8 evidence to name what was actually executed.

Executed witness: `probes.py`, `probe-results.json`, keys
`missing_version_column` and `missing_tail_column`.

### WP04-CR-009 — Concurrent identical retries on one handle do not share the receipt

- Classification: `IMPLEMENTATION_DEFECT`.
- Severity: high. Status: OPEN. Blocking: WP-04.
- `owner_decision_required: false`.
- Authority: G-084, verbatim at the candidate's governance record; agreed
  `spec/persistence.md`, commit steps 9..13 and concurrent-identical-retry rule.
- Code: `persistence/postgres.py:183-186`, and its transaction consumers.

Minimal coordinated witness using only valid public calls:

1. Open one handle and create store `s`.
2. Start `commit_history('s', writer, op('same'), [draft('same-record')])` in a
   thread. Its clock signals that sampling has begun and waits on an event.
3. While that attempt is inside its transaction, call **the same commit with the
   same normalized mutation** from the second thread through the same handle.
4. Release the first clock and join the first thread. Retry again afterwards.

The overlapping retry raises:

```text
ProgrammingError: can't change 'isolation_level' now:
connection.transaction() context in progress
```

The first caller succeeds at position 1, and the later non-overlapping retry
returns exactly that original receipt. A separate witness with distinct valid
operations has the same overlapping-call failure. The clock is a valid injected
clock; its wait only fixes the interleaving. No private connection mutation or
database damage is involved.

`_transaction` changes the shared connection's isolation/read-only settings
without handle-level coordination. The database row lock consequently cannot
serialize all callers: the second call fails before reaching it. G-084 says
concurrent identical retries produce one physical commit and return the same
original receipt to **all callers**; neither the contract nor this public API
states a one-handle-per-caller restriction. Separate-handle tests do not discharge
that rule for the shipped handle.

Required repair: coordinate the complete connection transaction lifecycle for
overlapping public operations on a handle, including isolation/read-only setup,
while preserving validation precedence, snapshot isolation, and return-after-
durability. Add same-handle identical-retry and mixed-operation controls, as well
as the existing separate-handle controls. Silently restricting the accepted API
to avoid the witness would change the contract, not close this finding.

Executed witnesses: `probes.py` (`same_handle_second`) and `additional.py`
(`concurrent_identical_retry`, `first_commit`, `later_retry`).

### WP04-CR-010 — The conformance runner fails valid JSON-only store creation

- Classification: `CONTRACT_ASSURANCE_DEFECT`.
- Severity: medium. Status: OPEN. Blocking: WP-04.
- `owner_decision_required: false`.
- Authority: agreed `spec/persistence.md`, Scenario and test seams, JSON seams.
- Code: `tests/conformance/test_canonical.py:132-134`.

Execute the runner's actual observation path with a clean initialized backend:

```python
_observe('create_store', {'store_id_json': '"s"', 'clock': [T]}, run)
```

Expected: `{'result': 'created'}`, with the clock fixture installed for store s.
Observed: `KeyError: 'store_id'`. A subsequent public `store_tail('s')` confirms
the library already created the empty store. `_arg` correctly constructs the
JsonText argument for the public call, but the next line indexes the absent
native `params['store_id']` to install the fixture. Thus a legal scenario seam
fails in the harness after successful library execution. No production defect
in JSON-only `create_store` is alleged.

Required repair: bind the fixture to the store ID represented by the supplied
argument, through the reviewed value seam; cover both native and JSON-only
creation, followed by a real commit. Keep invalid-ID and duplicate-store
observations on the public library path. Current ACTIVE scenarios miss this
combination, so their pass result cannot stand as evidence for the general seam.

Executed witness: `probes.py`, keys `runner_json_create` and
`runner_created_tail` in `probe-results.json`.

### WP04-CR-011 — The claimed G3 candidate omits two reachable statements

- Classification: `CONTRACT_ASSURANCE_DEFECT`.
- Severity: medium. Status: OPEN. Blocking: WP-04.
- `owner_decision_required: false`.
- Authority: candidate `process/gate-tiers.md`, G3 and first complete
  IMPLEMENTATION_REVIEW minimum; the accepted 100% Python floor.
- Code: `persistence/postgres.py:319-320`; implementation record Executions.

Coverage 7.16.2 over all `src/minion_memory`, with branches, subprocess patching/
combination and no exclusions, reports **1,154/1,156 statements** and
**470/470 branches**. Both missed statements catch a typed malformed boundary
and attach `argument='since'` in `read_history`. They are reachable:

```python
store.read_history('s', {'store_id': 's'}, 1)
# history.boundary_invalid, argument='since', position=None
```

The reviewer executed this control through the public API. It is absent from
the candidate suite. The record labels the author run G3 but supplies no coverage
result, and the measured candidate is below that stage's required floor.

Required repair: add meaningful public controls for malformed boundaries and
their generic/typed precedence and argument diagnostic, then record fresh G3
coverage at the resulting exact pair. Do not exclude reachable code or count
reviewer scratch probes as candidate-suite evidence. The G3 floor is assurance,
not a substitute for the independent semantic witnesses above.

Evidence: `coverage.json` and `additional-results.json`, key `malformed_since`.

## Disposition of the offered challenges and other reviewed seams

1. **Persistence namespace: acceptable.** The package exposes the backend adapter
   separately from core and does not add a universal memory entity or a
   profile-specific meaning to the shared core. Core does not import psycopg or
   persistence. The scaffold allowlist still limits the package root to explicit
   core/persistence namespaces. This is representation/organization, not a new
   observable semantic choice.
2. **Shared emptied test schema: acceptable for the executed sequential suite.**
   The reset deletes records, operations and stores in one committed transaction
   before use, leaving the initialized schema/version. Concurrency tests share
   only parameters and use their intended handles; threads finish before the
   next reset. Open tests use fresh schemas. This preserves the stateful
   scenario requirement of a backend holding no stores; it does not substitute
   an emptied schema for the fresh-schema open witnesses. The new reviewer
   schema probes also used fresh schemas.
3. **P14: equivalent on valid gapless history.** At one snapshot with
   `0 <= since <= tail`, page length is `min(limit, tail-since)`. Its last
   position, or since for an empty page, is therefore
   `since + min(limit, tail-since) = min(since+limit, tail)`. Native/JsonText
   inputs reach the same validated integers. The reviewer checked every since
   0..27 with seven limits including MAX, and arithmetic at tail 0, 1, 27,
   MAX-1 and MAX. Python's unbounded intermediate addition creates no overflow
   exception. The equivalent mutant survives its paging controls. Malformed or
   externally damaged database states do not invalidate this valid-state proof;
   schema-open defects are addressed separately by CR-008.

The reviewed `_admit(..., draft=True)` difference is confined to the D3 closed
member set; default replay admission is unchanged. Native/JSON global stages,
typed argument order, strict recognition, supplied recorded_at rejection,
timestamp-before-ID order, normalized retry mutation and NUL bytea roundtrip
matched the accepted text in the executed controls. Original tests reproduced
capacity-after-idempotency, serialized separate-handle writes, atomic snapshot
reads, waiting opens under a Repeatable Read session default, and abort/kill
behaviour. The additional operation-insertion failure proves rollback after
records have already been inserted, not just before the first write.

The 63 unchanged expectations remain valid and all five scenarios pass.
Mixed-language [IT] witnesses are correctly still due at the Rust candidate;
this review neither claims their execution nor takes Python as a Rust oracle.
The plan's assurance index still describes these scenarios as DRAFT and the
matrix retains some “to add” Python capability cells; update those status
descriptions with the remediation evidence.

Required next step: remedy CR-008..011, run the discriminating controls and the
applicable G3 evidence, then hand off the exact pair for independent closure.
