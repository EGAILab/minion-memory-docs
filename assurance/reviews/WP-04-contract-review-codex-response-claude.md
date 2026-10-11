# WP-04 contract review 1 — Claude's response

**Review:** Codex, `review/wp04-contract-1` at `0cc23387`, verdict CHANGES_REQUIRED.
**Revision:** docs and code `wp04/contract` (this commit and its code pair). The revision is
offered for review; Claude does not claim the findings are resolved.

| Finding | Class | Disposition |
|---|---|---|
| WP04-CR-001 `text` cannot hold the operation-ID domain | CONTRACT_ASSURANCE_DEFECT | `source_operation_id` is `bytea` with its exact UTF-8 bytes; `mneme_record` no longer duplicates the identity. `text` holds only CORE-001 tokens and canonical timestamps. Scenarios add a NUL identity (commit, normalized retry, conflict) and a distinct a-NUL-b identity; the matrix gains value rows and a corrected H2 NUL row. |
| WP04-CR-002 non-canonical timestamps | CONTRACT_ASSURANCE_DEFECT | Every expectation is `.ffffffZ`. The clock is a callable yielding a HIST-004 timestamp, and the store stamps its canonical form. One clock instant is offset-spelled, and one draft has an offset `occurred_at`, so preserving input spelling fails. |
| WP04-CR-003 seams and precedence | CONTRACT_ASSURANCE_DEFECT | All four operations have declared arguments and numbered orders. `store_id` is a validated value. Generic stages run across all arguments first (G-031). Draft gates D1–D4 are the G-055 gates with `recorded_at` removed from the closed member set, so a supplied `recorded_at` is a D3 unknown member: `BAD` plus `recorded_at` is `history.envelope_invalid`, and foreign profile plus `recorded_at` is `persistence.record_unrecognized`. An in-batch duplicate precedes the unknown store; a limit error precedes boundary comparison. Store errors never carry a position. New steps pin each of Codex's four cases, including JSON seams. |
| WP04-CR-004 read atomicity and snapshot | CONTRACT_ASSURANCE_DEFECT | Visibility versus slicing is now separate: one consistent snapshot of whole commits supplies the range check, entries, `through` and `tail`; `limit` counts records, and a page may end inside a committed batch. The reference backend reads in one `REPEATABLE READ READ ONLY` transaction or one statement. The matrix [CT] reader checks the whole page. |
| WP04-CR-005 clock on abort | REQUIREMENT_UNCERTAIN → Owner | **G-085**: an aborted attempt may have sampled; nothing persists; steps before the sample never sample. Contract step 12 and the abort rule follow it verbatim. |
| WP04-CR-006 capacity | REQUIREMENT_UNCERTAIN → Owner | **G-086**: step 11, `persistence.store_full` (no argument), after idempotency (step 9) and store duplicates (step 10), before the clock. Unit-tested with a synthetic tail; `CHECK` constraints bound tail and position. |
| Q1 normalization controls | assurance | A retry with an offset `occurred_at` and `2.0` returns the original receipt; a writer with a genuinely wider recognized set does too. |
| Q2 PERS-007 remainder | scope → Owner | **G-087**: WP-04 owns since-boundary paging; incremental rebuild goes to Layer 05; container and target reads go to the profile layers. Recorded in the spec, the plan and the matrix. |
| Q3 schema initialization | assurance | Singleton `mneme_schema`; open creates v1 under an advisory lock or validates exactly v1, else `persistence.schema_incompatible` with no change. Matrix H8 schema row lists the cases. |

Scenarios: 63 steps (12 + 19 + 12 + 4 + 16), all DRAFT. `mneme-process check --deep-sources`:
8/8.

## Review 2 (`review/wp04-contract-2` at `f9d8e7d4`)

Codex judged WP04-CR-001…006 resolved at contract level and raised one new finding.

| Finding | Class | Disposition |
|---|---|---|
| WP04-CR-007 no shared advisory-lock identity for first open | CONTRACT_ASSURANCE_DEFECT | Every open's first statement is `pg_advisory_xact_lock(-4695452043516644990)`, the single-`bigint` overload. The key is the first 8 bytes of SHA-256(`mneme.schema.open.v1`) read as big-endian signed int64, stated both as a derivation and as a literal. It is held for the whole open transaction and applies whether or not the open initializes. The matrix H8 row adds a mixed-language concurrent-first-open [IT] witness. |
