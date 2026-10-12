# CE-04-01 — targeted checkpoint review, revision 4 (Codex)

**Verdict: CHANGES_REQUIRED.**

Reviewed docs **c1d65187a8ea564231147a687c72930161315c15**, classification §9 and its
`spec/persistence.md` transcription, against G-098 and the preceding authority. Behavior reference:
frozen code **be36323f56e61d87776d11c831ae1ef0573ea692**. The scope is CP-004..007 and direct
regressions of their repairs. No unrelated row, prior closure or operation semantics is reopened.

| Finding | Targeted disposition |
|---|---|
| CE04-CP-004 | Resolved for the checkpoint by G-098 and §9.1–2; implementation evidence remains due. |
| CE04-CP-005 | **Open, partially repaired.** Index cardinality now detects the original extra-member model; the specified member shape still omits stable TOAST-index properties. |
| CE04-CP-006 | Resolved: E004 has its own correct old-store oracle and a separately named new-store N trace. |
| CE04-CP-007 | Resolved: the spec now transcribes the broader no-recorded-dependency boundary and qualifies explicit FOR TABLE entries. |

Only **CE04-CP-005** blocks agreement. No new finding ID or unresolved path-C choice is raised.
Production remains frozen; this is not implementation approval or acceptance onto main.

## CP-004: G-098 is faithfully transcribed and accounted for

The general copies exemption is removed from the live spec. The closed G-096 exception stays
separate from G-098's consistency checks, static pins and relation-count invariants. §9 explicitly
supersedes §8's rejected 28-field classification; the historical text is not governing policy.

The §9.1 partition covers each O001..O085 exactly once:

- 18 retained fetch/pin rows;
- 6 type-consistency rows (O002/O004/O005 and O015/O020/O021);
- 18 static pins, including both attcacheoff rows and the index fallback/foreign fields;
- 4 count invariants;
- 10 planner-statistics, 6 ownership/grants, 8 identity and 15 named-bookkeeping exclusions.

Total **85**. The previously disputed **28** become 6 consistency + 18 static + 4 invariant rows,
not exemptions. Referencing the actual pg_type row avoids architecture-dependent byte pins;
checking genuine admitted type identity is still required by the retained column/index rules.
Index NOT NULL/default descriptors must use their own initializer state rather than heap flags.

I independently executed the type-copy consistency and count observations on a fresh initializer.
Every live heap/index attribute's length/by-value/alignment matched its actual pg_type. Every
selected relation/index satisfied highest-positive-attribute-number and CHECK-count invariants.
Adding then dropping a heap column changed mneme_store's relnatts/highest attribute number from
2/2 to 3/3: its actual live columns stayed the original two. The invariant remained true and
public N passed. A literal initial relnatts pin would wrongly reject this G-089 residue control.

Pure predicates and the prescribed fetch-binding controls remain future implementation obligations;
this observation does not pretend to execute the unimplemented G-098 fetch.

## CP-005 remains open: member discovery/count is repaired, shape is incomplete

- Classification remains **CONTRACT_ASSURANCE_DEFECT**; path **A**;
  `owner_decision_required: false`.
- Blocking: CE-04-01 revised checkpoint.
- Pinned sources: this reviewed head, classification §9.2.4 and §9.3; persistence.md
  “Internal members are certified, not only discovered”; G-089, G-094 and G-098.

The new members part explicitly counts TOAST indexes and compares the enumerated shape before
granting membership. I reran the original projected extra-index model: one index becomes two,
the specified members observation differs, and crossing edges remain empty. This closes that
**exact** model. It does not yet establish the promised exact initializer shape.

The listed TOAST-index fields are uniqueness/primary/validity/readiness/liveness, access method,
key attribute numbers, expression/predicate absence and persistence. They omit at least:

- the index relation's `reloptions` (physical tuning);
- `pg_index.indoption` (per-key ordering flags).

Neither is an identity, statistics, grant, comment or G-096 exemption. The existing core-index
comparison reads both, but it is scoped to indexes on the **four core tables**, not TOAST tables.
The new boundary compares dependency edges, which neither property needs to change.

I executed two **projected-catalog controls**, each varying only one field of a real TOAST index
through a SQL subquery projection. An observer implementing exactly §9.2.4's field list was compared
with its baseline:

| Projected TOAST-index variation | Specified members observation | Retained frozen core fetch | Crossing edges |
|---|---|---|---|
| reloptions: NULL → [fillfactor=70] | unchanged | no mismatch | none |
| indoption: 0 0 → 0 3 | unchanged | no mismatch | none |

Index count stays one, and every property in the proposed members list stays at its initializer
value. The extra-index control differs; these shape controls do not. Therefore an implementation
that only adds the listed members fields can still absorb a **differing** internal index, contrary
to the new spec's last sentence and the strict finite v1 rule. The row/edge check is not a substitute
for the omitted shape predicates.

**Evidence boundary:** no physical TOAST index was modified, no superuser credentials were used,
and no future production implementation was run. These are executed query-projection/member-model
observations, not public executions of the altered physical states. The frozen fetch result is
included only to show that the retained core-only checks do not fill the proposed gap. I do not
claim an executed store failure caused by descending chunks or physical tuning.

**Required repair:** complete the internal-member field inventory, or explicitly apply the
relevant existing relation/index/attribute checks to those internal members. Name the stable
TOAST-index options, ordering, operator classes/collations, key/include cardinalities and related
shape checks; audit the same finite-state coverage for the TOAST relation and type associations.
Distinguish G-089/G-096/G-098 exemptions from properties merely omitted from this list. Add literal
predicate/fetch-binding oracles for these two refinements, retaining the extra-index count kill
and CH13 positive controls. No new semantic policy is needed: the text already requires exact
initializer membership and refuses physical tuning unless explicitly reviewed.

PostgreSQL's [pg_index definition](https://www.postgresql.org/docs/14/catalog-pg-index.html)
identifies indoption as per-column access-method flags. The rejection oracle here comes from
the project's existing finite-state contract, not an unexecuted claim about downstream chunk reads.

## CP-006: both revised E004 traces reproduced

I re-executed the pre-open tail replacement/default restoration and VACUUM FULL, then the two
separate public traces in the **same schema**:

| Store | Observed result |
|---|---|
| old | open accepts; old tail 1; commit 2..3; identical retry; read [2,3], tail 3 |
| separately created s | commit 1..2; identical retry; read [1,2], tail 2 |

These match §9.3 exactly. The old-row result is not N; the new-store result is N. No audit, repair
or reset of the old stored value is introduced. G-092's open-time row-audit exclusion stays intact.

## CP-007 and retained evidence rules

The spec now states that a reference with no recorded dependency on an island object is outside
the boundary and its mere presence is not a refusal. It explicitly includes FOR ALL TABLES and
event triggers; explicit FOR TABLE entries remain prohibited recorded edges. This matches the
qualified CH17 reading already accepted in review 3. I did not construct a privileged global
publication or event trigger and claim a new public outcome.

The flag-only atthasmissing [F] control is now explicit. It prevents the attmissingval pin from
masking a fetch omission. Prior [F] obligations for P32/P40 and new predicate-domain fields stand;
historical survivor results must remain historical. The proposed pins, production queries, full
gates and final mutation evidence have not been executed and remain due after checkpoint agreement.

## Execution, provenance and cleanup

Project-managed CPython 3.12.8, psycopg 3.2.13, PostgreSQL 14.12, ordinary mneme_dev. Every shell
sourced project-environment.ps1. Host was clear. Two private databases were created from template0
with UTF8/C/C in mneme_ts and dropped in finally. All scratch and database files stayed under the
E: project. No production, state, registry, source-bundle or Claude-owned file was changed.

Own evidence: `.tmp/work/codex/ce04-checkpoint4/`:

- `probe.py`, `results.json`, `probe.log`, `cleanup.json`: G-098 observations/residue control,
  two omitted-property projections, and the two E004 public traces.
- `extra.py`, `extra.json`, `extra.log`: the original extra-TOAST-index model now differs under
  the planned members observation. It reuses only the prior scratch projection class, not a
  changed production module.
- `audit.json`: source cleanliness, row/accounting checks, evidence hashes and final database cleanup.

This targeted review closes the three repaired checkpoint issues and retains CP-005 with the two
executed shape refinements above. The next step is its field/evidence repair and targeted review;
production remains frozen until the revised checkpoint is agreed.

Evidence SHA-256 bindings:

| File | SHA-256 |
|---|---|
| probe.py | 13b66564a8f23e2f0a8804c335714b51d9c3ec11ebc1ae5e5b1e694fa6b34c10 |
| results.json | 25f4b4e85724702d400a730c7bb5d70370779f94bd526f82cfbde4ca9f1e6ae1 |
| cleanup.json | a871407a8e3f14e1c05735130e622fdfd1be5416314a6d0a4eda69b10ebc7263 |
| extra.py | 118c62042fb64e1160f4a215beffb6c07c68da1ef610779c208b8db90a6aa962 |
| extra.json | b930333b74d47e0336c609a0e272d054d3a0b78e4a343088a1e9025c501b9e60 |
