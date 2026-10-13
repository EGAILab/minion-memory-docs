# WP-04 Rust remediation 1 — Codex

**Status: ready for targeted CLOSURE_REVIEW.** Author evidence, not independent approval.

- Code: `220c6f285744fd52736cbd20f22105e9f33a5dce` on `wp04/rust`, test-only over
  `6ef220e5b4f48ea8d458ead2f30dfdfcf67cba3d`.
- Docs baseline: coordinator state `276fcf56dac264a32450a6fb9e35e1cf24877880` on `review/l04-rust-closure`, imported by
  fast-forward into `wp04/rust`. No author edits to state or registry.
- Authority: accepted Layer 04 contract and CE-04-01 checkpoint, shared pins and corpus;
  Claude's closure review `70f2a3e3` and the remediation handoff.

## Findings addressed

**WP04-CR-017.** The public partial-namespace control now includes namespaces holding only
`CREATE VIEW mneme_store AS SELECT 1 AS x` or `CREATE SEQUENCE mneme_record`.
Each must return `persistence.schema_incompatible`, with no argument, before initialization.
It asserts no `mneme_schema` relation was created and compares the complete namespace relation
inventory (OID, name, kind) before and after. Under R10, initialization instead attempts DDL
and surfaces a duplicate-relation database error; refusal after rollback is insufficient.

**WP04-CR-018.** The existing [F] test now projects only `pg_class.relpersistence` as `'u'`
for the exact root `mneme_store` OID. Actual production fetch SQL runs over that projected
source field. Its required first mismatch is `relations`; physical catalog data must still
equal the pins afterwards. This isolates the table field from TOAST persistence, which masks
the constant-read defect in public SET UNLOGGED cases. It is [F] evidence, not a physical
catalog mutation or public-open execution.

Both controls extend existing tests; production, shared pins, corpus and manifest are unchanged.

## Executions

Windows gates passed at `220c6f28`: Rust/Cargo 1.97.1, formatting, strict all-target clippy,
warning-free docs, 64 integration tests and one doctest. Corpus remains 22 ACTIVE / 408 steps /
4 explicit placeholder xfails; Layer 04 remains 23 tests including the two extended controls.
Both intended observers passed on the baseline. R06 compiled and failed at the new
`pg_class.relpersistence` assertion (`None` versus required `relations`); R10 compiled and
failed because the v1-name view produced a database error instead of the contract error.
The restored full Layer 04 suite passed (23 tests).

Linux gates also passed at the same exact code, Rust/Cargo 1.97.1: formatting, strict
all-target clippy, warning-free docs, 64 integration tests and one doctest, including the
same 22 ACTIVE / 408 steps / 4 xfails. Both intended observers passed before planting.
R06 and R10 compiled and failed at the same intended runtime assertions as Windows
(no mismatch versus `relations`, and database error versus contract refusal, respectively).
Both affected observers passed again after restoring the controls copy. The restored Linux
run is targeted to those observers; the complete baseline suite ran separately before planting.

| Evidence | Windows | Case-sensitive Linux client |
|---|---|---|
| Gates | PASS | PASS |
| R06 / R10 runtime kills | 2/2 | 2/2 |
| Restored source | Full Layer 04 suite, 23 passed | Both affected observers passed |

No compilation failure or post-hoc equivalence claim is counted as a kill. The prior 30/30
controls are historical evidence at `6ef220e5`, not recredited as executions at this candidate.

Evidence drivers and logs are isolated
under `.tmp/work/codex/wp04-rust-remediation-1/`. Controls use fresh copied sources and separate
per-platform targets, with compiled runtime assertion failures required. Every intended
observer must pass first on the baseline, then pass again after restoration.

The preliminary deep-source mechanical check passes 8/8 on the imported coordinator baseline.
The committed docs pair is checked again before handoff, with output in
`process-check-final-pair.log`.

The first Windows launch sourced the stale main environment and failed offline dependency
resolution before compilation. It is not credited. Sourcing the current own docs environment
selected the project-local populated Cargo home; validation resumed there.

Linux scratch-launch attempts first failed on copied CRLF shell endings, then on a relay
credential-copy path still pointing to the previous evidence directory. Both are launcher
failures, not passing suite evidence. They were corrected in scratch drivers only; each
attempt ended its relays gracefully and used a fresh lifecycle marker on restart.

The scheduler granted sequential Windows then Linux execution, max four Cargo jobs, project-local
caches and targets, no overlap, signals or target cleaning. Linux means a case-sensitive Linux
client against the same Windows PostgreSQL 14.12 reference server through the owned relay.
No Linux-server claim is made.

Final cleanup audit reports `OWN DATABASE INVENTORY EMPTY`. Each relay ended gracefully,
the credential copy was removed and the case-sensitive source image was unmounted. BATCH-DONE
was sent to the scheduler; no native batch remains reserved or running for this task.

Evidence: `windows-gates.log/json`, `windows-controls.json`, baseline/R06/R10/restored logs;
`linux-full.log`, `linux-test.log`, `linux-doc.log`, `linux-controls.json` and affected observer
logs; `cleanup-audit.log`; process-check logs. Own baseline targets are
`.tmp/cache/cargo-target/wp04-rust-{windows,linux}`; separate controls targets are
`.tmp/cache/cargo-target/wp04-rust-remediation-controls-{windows,linux}`.

## Handoff

WP04-CR-017 and WP04-CR-018 are repaired with discriminating test witnesses and offered for
Claude's independent targeted closure. No production defect or contract gap was introduced
or discovered. No acceptance, certification or independent finding closure is asserted here.
