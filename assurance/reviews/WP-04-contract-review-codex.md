# WP-04 independent contract review — Codex

**Verdict: CHANGES_REQUIRED**

Date: 2026-10-11. This reviews the canonical-store surface only, not WP-04T or an
implementation. Six blocking findings follow; two require Owner decisions.

## Exact object, authority and method

- Normative docs candidate: `2d9cca7815bff12cd4b68c089bfb458cc3276e2b`.
- Code/corpus candidate: `e48c61e14ad936703bd8531b1f1eb76091fce195`.
- Review branch: `review/wp04-contract-1`, based on supplied state-only descendant
  `1424242805be6f1d709c3465c417535a647bed1f`. Its differences from the docs candidate
  are confined to `process/state/WP-04.yaml` and `WP-04T.yaml`.
- Separate checkouts: `review-worktrees/docs-wp04-review` and `code-wp04-review`.

Authority read: verbatim G-077..G-084, G-013, G-051/G-054 and the certified lower-layer
contracts. I checked the scoped persistence text, HIST-008/009 notes, SER-008 table,
plan, feasibility matrix, manifest and all five scenarios. Sources include R04
§11/14/18/19/22/24/32/34/40/41, IAA A13/A18/A19/A20/A27/A31 and R05 §6/12/14/16.
The source reading aids were checked against the bundle by deep source verification.
Content-addressed source anchors used here include R04
`b4c25d006e7db998feb5f955b55a9fcdc58ef589e72eae6cff742b9c0b92755f`, IAA
`436ea1a3a5ffa126d70a1c3cb8e1a8cc1e3d8baf1d50740df3a9098240daba33`, and R05
`a6c5dee570a5673a34fcd4a33057b2b3faeb1330847b2060235d903a99a4f240`.

All following candidate references are at those exact pins. Expectations were
independently derived; no Mneme implementation was used as an oracle. There is no
Layer 04 implementation to test or approve at these pins.

## Findings

### WP04-CR-001 — PostgreSQL text cannot represent the operation-identity domain

- Classification: `CONTRACT_ASSURANCE_DEFECT`; path A (preserve G-033).
- Severity: HIGH; blocking: WP-04; status: OPEN; owner_decision_required: false.
- Requirements: CORE-012, PERS-006, PERS-014.
- Evidence: `spec/core.md` CORE-012 admits any Unicode-scalar string of 1–256 exact
  UTF-8 bytes for `source_operation_id`, with no filename restriction or replacement.
  The normative DDL in `spec/persistence.md` lines 295 and 301–305 stores that field
  as `text` in both record and operation tables. Matrix H2 NUL incorrectly claims
  that only ID-grammar strings use text; the opaque operation ID is not such a token
  and is omitted from its value-domain rows.
- Discriminating witness: `{source_namespace:"app",source_operation_id:"\u0000"}`
  is an admitted one-byte operation identity. Executed server expression
  `convert_from(decode('00','hex'),'UTF8')` in the operation insert fails with SQLSTATE
  **22021**, `invalid byte sequence for encoding "UTF8": 0x00`. The bytea control
  returns exact `00`. `"a\u0000b"` is likewise within the domain, not an invalid ID.
- Required repair: define a lossless shared physical representation and equality
  rule for this field in both tables, preserving the exact identity pair. Raw UTF-8
  `bytea` is sufficient. Update the matrix and add a cross-language NUL identity
  commit/retry/conflict witness. Rejecting, trimming or hashing this valid domain is
  not an implementation workaround authorized by G-033.

### WP04-CR-002 — Scenario receipts and clocks contradict canonical HIST-004 timestamps

- Classification: `CONTRACT_ASSURANCE_DEFECT`; path A.
- Severity: HIGH; blocking: WP-04; status: OPEN; owner_decision_required: false.
- Requirements: PERS-005/006/014, HIST-004, SER-009.
- Evidence: all five scenario files contain clocks and expected persisted timestamps
  such as `2026-10-11T08:00:00Z`. HIST-004 requires emitted/stored timestamps exactly
  `YYYY-MM-DDTHH:MM:SS.ffffffZ`; G-082 requires canonical UTC recorded_at. The clock
  test seam additionally calls its finite list canonical, and matrix H4 calls a
  noncanonical clock value a harness error.
- Discriminating witness: the first two-record gapless receipt must stamp both
  records and the receipt with `2026-10-11T08:00:00.000000Z`, not the current expected
  string. This affects **39 expected recorded_at fields** in **16 result rows**, and
  all **13 clock-list instants** are noncanonical. The intentional caller-supplied
  recorded_at rejection case is separate; its input need not be canonical.
- Required repair: make the clock fixtures and all persisted expectations canonical,
  retaining HIST-004 unchanged. Add a control that kills preserving the clock/input
  spelling instead of canonical storage. Do not normalize observations inside the
  conformance runner to conceal an implementation's wrong returned bytes.

### WP04-CR-003 — The public seams and complete error precedence are not specified

- Classification: `CONTRACT_ASSURANCE_DEFECT`.
- Severity: HIGH; blocking: WP-04; status: OPEN; owner_decision_required: false.
- Requirements: PERS-005/008/012, SER-008, HIST-005.
- Evidence: commit declares `(store, writer, operation, records)` but its generic
  stages list only writer/operation/records. Scenarios pass `store_id`; the text does
  not say whether store is a validated handle or an input value, how an invalid
  store ID fails, or which argument name it uses. `create_store` and `store_tail`
  have no corresponding seam/check list. Read lists individual errors but no
  complete staged evaluation order. SER-008 requires stages over all structured
  arguments in declared order. The stage table places an in-batch duplicate after
  stage 3, whereas commit's argument checks detect it before store existence.
  The draft extension also does not locate its supplied-recorded_at rejection
  relative to the inherited G-055 gates.
- Minimal discriminating inputs an independent implementation cannot adjudicate:
  1. Commit with invalid store identifier plus invalid writer, or JSON duplicate
     keys in a later argument: does store participate in the staged seam?
  2. Read known store-1 with `since={store_id:"store-2",position:0}` and `limit=0`:
     `history.boundary_incomparable` or `persistence.limit_invalid`?
  3. A draft with `record_id:"BAD"` and a supplied recorded_at: routing `id.invalid`
     or the ownership/shape `history.envelope_invalid`? A supplied timestamp on a
     foreign-profile draft similarly competes with `persistence.record_unrecognized`.
  4. Unknown store plus an otherwise-valid batch containing repeated IDs: reconcile
     the numbered checks with the table, rather than letting each runner choose.
- Required repair: declare every public argument/seam and give ordered check lists
  for all four APIs, including generic stages, draft gates, duplicate detection,
  store lookup, boundary comparison/range, limit and transaction checks. Pin codes,
  arguments and whether position is absent. Add paired failures through native and
  JSON seams. Preserve the existing G-031/G-055 rules; identify any genuinely new
  semantic choice for the Owner rather than letting Rust supply one.

### WP04-CR-004 — Read atomicity, page truncation and snapshot consistency are ambiguous

- Classification: `CONTRACT_ASSURANCE_DEFECT`.
- Severity: HIGH; blocking: WP-04; status: OPEN; owner_decision_required: false.
- Requirements: PERS-005/007/008/015.
- Evidence: read says both “at most limit” and “A read never observes part of a batch.”
  `store-bounded-read` commits positions 1–3 together, then expects limit 2 to return
  1–2; its next page returns 3–4 from two different batches. Its negative control
  “a page splits or skips a position” adds to the ambiguity. The reference backend
  specifies the commit lock but no read snapshot rule for entries, through, tail and
  since-versus-tail validation.
- Witness A: that first limit-2 page contradicts literal batch-indivisible reads.
  Atomic visibility of a commit and truncating an already-committed batch are
  different properties. The latter is useful and follows the declared per-record
  limit, but the text must say so.
- Executed witness B: with default **Read Committed**, a reader selects tail 18,
  another transaction commits position 19, then the reader's next query obtains
  entry 19. A page built that way has through 19 and tail 18. Merely enclosing those
  queries in a transaction does not provide one snapshot. A Repeatable Read control
  obtains tail 19 and no entry 20 despite a concurrent commit, consistently.
- Required repair: distinguish visibility of uncommitted/half-written batches from
  slicing committed batches. Specify one coherent read snapshot and its relation to
  through/tail; ensure since-range checks use it too. A single statement, suitable
  snapshot isolation or a compatible store lock can implement it. Add concurrent
  read controls that check the entire result, not just absence of uncommitted rows.
  Keep record-based paging unless a different policy is taken to the Owner.

### WP04-CR-005 — “Failed commits consume no clock instant” adds unresolved semantics

- Classification: `REQUIREMENT_UNCERTAIN`; path C.
- Severity: HIGH; blocking: WP-04; status: OPEN; owner_decision_required: true.
- Requirements: PERS-005/015; G-082/G-084.
- Authority: G-082 samples the injectable clock during the atomic commit and says
  failed/aborted commits **persist** neither timestamps nor positions. The proposed
  clock seam and matrix H10 cancellation strengthen that to no consumed instant on
  any failed/cancelled commit, without defining a transactional clock protocol.
- Executed witness: under the store row lock, sample once, insert the batch/receipt,
  advance tail, then ROLLBACK. Persisted tail/record count/operation count are all 0,
  but the instrumented callback count is **1**. PostgreSQL rollback cannot rewind an
  arbitrary clock callback; a process death after sampling has the same boundary.
- Owner options: (a) allow sampling on aborted attempts while persisting nothing,
  with no sample for an already-committed retry or pre-sample rejection; (b) require
  a specified transactional/reservable clock seam, distinguishing invocation,
  reservation and successful consumption; (c) restrict the no-consumption claim to
  validation/retry paths, with an explicit rule for post-sample aborts.
- Recommendation: decide the distinction explicitly. Option (a) is implementable
  with an ordinary injected clock and retains durable G-082 behavior. Do not quietly
  change the contract or implement a hidden rewind protocol.

### WP04-CR-006 — Exhaustion of the canonical position domain has no outcome

- Classification: `REQUIREMENT_UNCERTAIN`; path C.
- Severity: MEDIUM; blocking: WP-04; status: OPEN; owner_decision_required: true.
- Requirements: PERS-005/007/008; G-054/G-080/G-082.
- Evidence: canonical boundaries stop at 2^53−1, and the matrix repeats this bound.
  Commit unconditionally allocates tail+1…tail+n; there is no full-store/capacity
  failure, precedence or code. PostgreSQL bigint is wider than the canonical domain.
- Executed witness: with a synthetic tail of **9007199254740991**, the prescribed
  unchecked allocation commits **9007199254740992**. PostgreSQL accepts it; canonical
  serialization rejects the resulting integer (`IntegerDomainError` in the
  independent RFC 8785 oracle). This is an arithmetic unit witness, not a claim that
  the tiny fixture physically contains that many records.
- Owner choice: define atomic rejection for insufficient remaining capacity, its
  error vocabulary and position in the checks. Decide whether a valid retry at a
  full store still returns its receipt before capacity is tested. Recommendation:
  preserve matching retries, reject a new oversized range before clock sampling,
  append or receipt effects; never wrap, clamp, reuse or partially append positions.
  The capacity code/outcome is not supplied by existing authority and must not be
  guessed by an implementer.

## Executed assurance and feasibility

Scratch driver: `.tmp/work/codex/wp04-probes.py`; output:
`.tmp/work/codex/wp04/probe-results.json`, `oracle-rows.json` and `probe-console.log`.
It imports no Mneme implementation. A small fixture-specific model independently
derives all **50** input/result rows: 10 + 15 + 8 + 4 + 13. It normalizes fixture clock
spellings to derive the intended canonical output; this does not bless those inputs
as a valid canonical clock seam. **34/50** literal results match; after correcting
expected recorded_at spelling only, **50/50** match. No other stated oracle mismatch
was found. The page results require the committed-batch truncation reading in CR-004.
This model is not a production store or proof of untested value domains.

The database probe copied the candidate DDL unchanged into one throwaway database
on local **PostgreSQL 14.12**, as non-superuser `mneme_dev`. Creation used template0,
UTF8, C/C collation and `TABLESPACE mneme_ts`; the observed location is the project's
`.tmp/pgdata`. Settings were Read Committed, synchronous_commit on, fsync on and
full_page_writes on. No admin credentials were used. Database absence after DROP was
queried and confirmed. Credentials were not logged.

With the row lock first and the later queries under Read Committed:

- Eight parallel distinct two-record operations produce positions exactly 1–16.
- Eight parallel matching retries produce one range 17–18 and seven identical
  original-range retries, with no extra physical records.
- A differing mutation conflicts; record-ID reuse under another operation rejects.
- A rollback leaves neither tail movement, records nor an operation receipt.

Thus the lock design can deliver G-080/G-084 on representable inputs; sequences are
not needed. These are SQL algorithm probes, not implementation crash certification
or cross-language interoperability. Other isolation levels require appropriate
serialization-failure handling; separate reads require CR-004's explicit snapshot.
PostgreSQL's primary documentation supports the observed limitations:
[character types](https://www.postgresql.org/docs/14/datatype-character.html),
[transaction isolation](https://www.postgresql.org/docs/14/transaction-iso.html), and
[WAL/durability settings](https://www.postgresql.org/docs/14/runtime-config-wal.html).

Rust feasibility is otherwise sound: certified staged validation, reader gates,
HIST-004 normalization and canonical bytes can be reused; a draft admission extension
is needed. A synchronous PostgreSQL client can bind bigint positions and bytea
canonical content. Receipt reconstruction is possible from the operation range and
immutable ordered records. The opaque identity representation, complete error order,
read snapshot, clock-abort policy and capacity decision must be settled first.
The matrix's PLANNED implementation evidence is appropriately not claimed executed,
but its operation-ID omission and clock assertions need correction above.

## Questions / required implementation-assurance follow-through

- Q1: the retry step labelled normalization uses identical drafts; only the writer's
  recognized-list order changes. Add actual occurred_at offset/case spellings and
  normalized numeric payloads to kill raw-draft-byte comparison, plus a writer with
  a genuinely different recognized set. These are assurance recommendations, not
  additional findings or a request to reopen lower-layer semantics.
- Q2: PERS-007/R04 §34 include container/target reads and bounded replay. The current
  APIs provide raw since-boundary paging only. Identify where container/target reads
  and a bounded incremental projector/checkpoint seam will be discharged. Layer 03's
  whole-stream projector alone does not supply an incremental accumulator: projecting
  a second page whose resolution link targets page one fails without earlier records.
  Concatenating every page and projecting all history proves output equality but not
  bounded replay memory. Do not label that capability exact merely because paging
  exists; give explicit deferrals/owning layers consistent with G-078.
- Q3: define shared-schema initialization/open validation (exactly one version row,
  absent/mismatched/malformed schema and safe concurrent initialization) in the
  implementation plan, and test durability settings and transaction failure paths.
  The current version table alone does not enforce a singleton. These are backend
  assurance questions, not evidence of an implemented defect.

`mneme-process check --deep-sources` passes **8/8** at the separate candidate
worktrees; these checks do not validate the semantic timestamp or SQL domains.
All temporary files, caches, venv and probes remain inside the E: project root.
The only authored repository change is this review record. No production, state,
registry, corpus, source bundle, remote or implementation edits were made.

Exactly one review verdict is issued above. This pair is not ready for contract
agreement until CR-001..006 are resolved; path-C CR-005/006 go to the Owner.
