# CE-04-01 — independent checkpoint review, revision 3 (Codex)

**Verdict: CHANGES_REQUIRED.**

Reviewed docs state **d3623c9040fb131ed8eb31e09b8645a6227a9e0b**, specifically classification
§8 and its persistence-contract transcription, against Owner G-088..G-097. The behavior reference
remains **be36323f56e61d87776d11c831ae1ef0573ea692**. This review does not authorize production
changes or acceptance onto main. CR-009..011 remain resolved. The earlier checkpoint's unchanged
parts are not reopened without new evidence.

Four findings block the revised checkpoint. CP-004 needs an Owner decision; the others are
contract/evidence repairs under existing authority. Production remains frozen pending a revised
two-party agreement.

## CE04-CP-004 — the 28-field “copies” exemption is not established by G-096

- Classification: **REQUIREMENT_UNCERTAIN**; path **C**; `owner_decision_required: true`.
- Blocking: CE-04-01 revision-3 checkpoint.
- Sources: reviewed classification §8.3, especially lines 374–395; persistence.md lines 403–417;
  governance G-096 at line 279, and G-089/G-092.

G-096 exempts engine bookkeeping and the inconsistencies of **those** fields. Its examples identify
lazy summaries, maintenance/physical identifiers and transient planner/MVCC state. The proposed
transcription adds another general class, then §8.3 exempts all 28 rows as copies whose
authoritative sources are supposedly checked. That conclusion has not been demonstrated for the
whole group.

The narrow inference for genuine type copies is plausible, but it does not establish the blanket
group. For example O003 `attcacheoff` is a stored offset-cache field, not a copy of pg_type's length,
by-value flag or alignment. Index O024/O036 are `atthasmissing`/`attmissingval`, and O035 is
`attfdwoptions`: the proposal does not identify a compared authoritative source for each. These
fields cannot all be justified by saying “the source key column is compared.” My fresh initializer
observation also shows `mneme_schema.singleton` has NOT NULL/default flags true/true whereas its
index attribute has false/false. They are different engine-generated descriptors, not literal
copies of those source-column properties.

PostgreSQL's [pg_attribute definition](https://www.postgresql.org/docs/14/catalog-pg-attribute.html)
separately identifies type copies, the stored offset-cache value, missing-value fallback and
foreign-column options. That engine distinction supports separating the rows; it does not decide
which additional exemptions the Owner intends.

This is not a claim that an ordinary role constructed corrupted type/index descriptors, or that
such corruption produced a public failure. Those altered states remain unconstructed. The
uncertainty is the proposed observable admission policy: G-092 previously required pre-open
semantic catalog variations to be refused; G-096 now exempts a specified bookkeeping class. The
agents should not silently enlarge that exemption to every engine-generated descriptor field.

**Resolution:** present a field-scoped Owner packet distinguishing actual type copies, static
engine-derived index descriptors, cache/fallback fields and relation counts. Either explicitly
exempt the proposed group (with its authoritative-source/invariant mapping), or retain the
non-exempt consistency predicates. Until then do not transcribe the blanket exemption as decided
G-096. This does not challenge its explicitly named 15 bookkeeping rows.

## CE04-CP-005 — discovering attached TOAST indexes is not certifying their v1 set

- Classification: **CONTRACT_ASSURANCE_DEFECT**; path **A**;
  `owner_decision_required: false`.
- Blocking: CE-04-01 revision-3 checkpoint.
- Sources: reviewed classification §8.1/§8.4 CH13/§8.5.3–4; persistence.md lines 439–454;
  G-089 exact v1 and G-094 **certified** dependency island.

The structural discovery adds all indexes attached to TOAST relations to the island. The retained
index comparison and §8.5.3 compare indexes attached to the four core tables. No obligation names
an authoritative v1 shape/count check for the newly included TOAST indexes before they are
considered certified. A boundary check cannot reject an extra object that its own discovery has
already absorbed.

I executed a bounded projected-catalog model using real ordinary-role catalog rows. A separate
ordinary table/index supplied a genuine unique btree index descriptor. The model projected its
parent, namespace and parent-column dependency endpoints to one core TOAST relation. It did not
modify any physical catalog. The structural membership rules then included this extra index:

```text
physical TOAST indexes on the selected relation: 1
projected TOAST indexes on that relation:        2
baseline island pg_class objects:              15
projected island pg_class objects:             16
crossing edges in either model:                 0
frozen core catalog mismatch in either model:   None
```

The ordinary physical CREATE INDEX attempt failed with SQLSTATE 42501 (permission denied for
pg_toast). **This is projected graph/fetch evidence, not a public execution of an extra TOAST
index and not a claim that a future implementation was run.** It discriminates the proposed
crossing-edge-only plan: all the new index's relevant edges terminate inside the discovered
island, while the core-only index pins do not inspect it.

**Resolution:** define how each engine-created internal member is certified before membership
grants it the boundary exception. In particular specify the admitted TOAST-index set and
authoritative shape check; add predicate/fetch-binding evidence for a changed or additional TOAST
index. Audit the same distinction for TOAST relations and row/array type associations. This need
not pin exempt names/OIDs, bookkeeping or tuple contents. It completes G-094's certified-set rule;
it does not introduce a new effect-based admission policy. CH13's valid baseline/large-payload
acceptance must stay as a positive control.

## CE04-CP-006 — §8.6 demands an impossible N oracle for E004

- Classification: **CONTRACT_ASSURANCE_DEFECT**; path **A**;
  `owner_decision_required: false`.
- Blocking: CE-04-01 revision-3 evidence agreement.
- Sources: reviewed classification §8.2 E004 (line 360) versus §8.6 (lines 457–458);
  characterization E004; persistence.md Trust scope; G-092.

§8.2 correctly accepts the catalog and does not audit the old row. §8.6 nevertheless includes
E004 among rows for which “protocol N holds.” Its actual characterized protocol uses `old`, whose
tail became 1 before open. I re-executed the exact DDL and public trace independently:

```text
after VACUUM FULL: live tail atthasmissing=false, attmissingval=NULL
catalog mismatch: None; crossing edges: none; public open: ACCEPT
old tail: 1; first/last receipt: 2/3; retry identical
read positions: [2,3]; tail: 3
```

N requires receipt 1/2, read [1,2] and tail 2. Requiring that outcome on this old-store fixture
would force repair/audit behavior that G-092 excludes.

**Resolution:** give E004 its own literal acceptance/unaudited-row oracle, preserving the above
trace. If N is also desired, run it on a separate new store and say so explicitly. Do not silently
reset away the old-row witness or credit it as N.

## CE04-CP-007 — CH17's valid boundary reading is not fully transcribed

- Classification: **CONTRACT_ASSURANCE_DEFECT**; path **A**;
  `owner_decision_required: false`.
- Blocking: CE-04-01 revision-3 shared contract.
- Sources: reviewed classification §8.4 CH17; persistence.md lines 458–466;
  governance G-094 at line 265.

I accept the **qualified** CH17 reading: G-094 expressly leaves dynamic SQL **or other references
with no recorded catalog dependency** outside this boundary. Its list of publications concerns
the forbidden edges, not an independent prohibition of every publication object. A FOR ALL
TABLES publication or global event trigger with no island dependency is therefore not refused
merely for that presence. Privilege alone does not supply this interpretation.

The shared spec instead states “publication membership” is incompatible and transcribes only a
**name in code text** as its no-dependency exception. An independent implementer could reasonably
check pg_publication.puballtables and reject global publication membership, following that text,
while §8.4 expects acceptance. A global publication is catalog state, not a name in function-body
text.

The [pg_publication catalog definition](https://www.postgresql.org/docs/14/catalog-pg-publication.html)
describes puballtables as automatic membership, including future tables. This is a catalog rule,
even though it creates no per-table dependency edge in the checkpoint's model.

**Resolution:** transcribe the broader recorded-dependency boundary and explicitly state the
CH17 cases, preserving rejection of actual island-crossing edges. No new Owner choice is needed
under the literal G-094 already recorded. If a broader global-hook/publication ban is wanted,
that would instead be a new path-C policy.

My ordinary-role FOR ALL TABLES attempt returned 42501. Its subsequent successful open was
against the unchanged baseline. I do **not** report a physical global-publication execution or a
public outcome against that unconstructed state.

## Accepted portions and independent checks

The §8.2 partitions are disjoint and cover all 112 characterized IDs (17+1+4+7+28+2+12+41).
The §8.3 inventory accounts for 85 IDs; 57 dispositions outside CP-004's 28-field group are
accepted, subject to completing internal-member certification rather than treating an OID as
proof of semantics. Cached values remain live semantic state; harmless-looking caches still
refuse. Comments are exempt and labels forbidden as G-097 decides. Construction failures remain
residual-state controls, not false credited kills.

Ten fresh-schema public/observer cases ran against the exact frozen code. These are checkpoint
probes, not new G3/G4 gates or executions of the unimplemented boundary validator:

| Case | Actual frozen public outcome | Independent proposed-boundary observation |
|---|---|---|
| baseline | N succeeds | zero crossing edges; required internal members retained |
| CH13 20KB payload | N succeeds; payload roundtrips | zero crossings before/after; internal TOAST objects retained |
| CH14 statistics alone | N succeeds | two exempt statistics edges, zero non-exempt crossings |
| CH14 statistics + owned sequence | frozen open accepts; N succeeds | one non-exempt sequence edge survives the statistics exemption; revised oracle rejects |
| outside domain CHECK over core row type | frozen open accepts; N succeeds | two non-exempt type/constraint-related crossings; G-094/G-095 require rejection |
| own-namespace user function as tail default | frozen open rejects in defaults | an outgoing user-function edge also exists; same namespace does not rescue the invalid default |
| E004 rewrite | accepts, old receipt/read 2/3 | no crossing; distinct unaudited-row oracle needed |
| CH17 FOR ALL TABLES denied setup | unchanged baseline N succeeds | no constructed global publication; no altered-state claim |
| outside array-type column | frozen open accepts; N succeeds | recorded dependency on certified array type; revised oracle rejects |
| comment | N succeeds | zero crossing edges; G-097 acceptance control |

The outgoing resolved-namespace allowance is necessary: removing it rejects the valid fresh
namespace. The builtin allowance distinguishes predefined PostgreSQL objects from new ordinary
user objects; numeric OIDs are identifiers rather than pinned schema values. The structure must
use class+object addresses (and correctly cover column subobjects), not names alone. The tested
baseline has eight type objects, fifteen relation/index/TOAST objects, ten constraints, two
defaults and eight RI triggers. These counts are observations of this initializer, not a proposal
to bypass property validation with counts.

## [F] is sound bounded evidence, with precise reporting

I independently executed the proposed relation-projection approach against the actual frozen
fetch. Correct fetch/comparison saw each injected field, and the exact historical query mutants
lost it:

| Supplied property in actual fetch SQL | Correct mismatch | Exact mutant mismatch |
|---|---|---|
| trigger tgenabled=D | triggers | None under P40 literal O |
| index indisvalid=false | indexes | None under P32 literal true/true |
| index indisready=false | indexes | None under P32 literal true/true |

The real catalog was v1 throughout. Query dictionaries were changed only transiently in the probe
process and restored in finally; no production file was edited. These are **[F] direct
fetch-binding kills**, not public physical-trigger/index kills. They substantiate the route for
CR-014 and strengthen dataflow assurance even where the exact public-domain equivalence differs.
Both historical gate runs must keep their recorded survivors. Pure comparator tests alone cannot
replace these binding checks.

The actual future boundary/label fetch is not yet implemented, so its [F] obligations remain
pending. Preserve tests that vary object class/address, column subobjects and the field value;
injection must exercise the actual query's joins/filters and final comparison. The intended
“atthasmissing not read” mutant deserves an [F] control with only that projected flag changed:
a physical active-cache fixture also changes attmissingval, whose required pin can mask loss of
the flag. The pre-gate whole-module diagnostic must expose this redundancy instead of borrowing
another failing test. This is an evidence clarification under the stated [F] method, not a new
public cache-state claim or separate finding.

## Provenance and cleanup

Project-managed CPython 3.12.8, psycopg 3.2.13, PostgreSQL 14.12, ordinary mneme_dev only.
Every shell sourced the project environment; all scratch, interpreter files and database files
remained under the E: project. Host was clear. No superuser configuration, privileged provider,
physical disabled RI trigger, physical corrupt index, service change, Docker batch or full-suite
gate was performed. The only tracked change is this review record.

Evidence under `.tmp/work/codex/ce04-checkpoint3/`:

- `probe.py`, `results.json`, `probe2.log`, `cleanup.json`: ten public/catalog observer cases and
  three [F] controls; the complete trace includes actual initializer attribute descriptors.
- `toast_model.py`, `toast-model.json`, `toast-model2.log`: projected extra-member countermodel,
  with denied physical attempt explicitly separated.
- `diagnostic-run1.json` and `diagnostic-toast1.json`: discarded probe runs with a reserved-name
  SQL error and a missing projection alias, respectively. They were corrected and rerun in fresh
  databases; neither is credited as validator/mutant evidence. Their databases also dropped.

Each database was created from template0 with UTF8/C/C in mneme_ts and dropped in finally. Final
cleanup and exact-source checks are recorded in `audit.json`. The next step is resolution of
CP-004 and repairs of CP-005..007, then targeted checkpoint re-review; production remains frozen.

Evidence SHA-256 bindings:

| File | SHA-256 |
|---|---|
| probe.py | 597a136d6f6b476a196d48458f8e74dc8e9240b4be6b2c110668dc9325770468 |
| results.json | 8384de1efbb2a2835c47e8aae2f3b2702388439965d94b3567180c541e62545e |
| cleanup.json | 8adfb9bee662281aa9e320b05995bca5d9104403d27f16c00178e3978f3f6a09 |
| toast_model.py | 158d7904af7280e42addb9674b2f493a954be8896f895230ef5db28841996b98 |
| toast-model.json | 809cbb1c43eb77ef94ef37956078fa56abd5f4f555cb24d929c79486aaacf3be |
