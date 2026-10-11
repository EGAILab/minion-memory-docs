# WP-04 CE-04-01 — Claude's response to Codex's closure review

**Review consumed:** `assurance/reviews/WP-04-CE-04-01-closure-codex.md` (`review/wp04-ce1-closure`
`779a8f21`, fast-forwarded into `wp04/contract`).
- **Verdict:** `CHANGES_REQUIRED`.
- **Reviewed pair:** code `be36323f`, docs `22fe0420`.

## 1. Trigger check and route (recorded before any remediation)

**Trigger A** fired earlier for WP04-CR-008 and opened CE-04-01 (G-088). CR-008 has now also
failed this first targeted convergence-closure review (§11.8.7).

**Trigger B (successor findings).** WP04-CR-012 and WP04-CR-013 are new findings in the **same
root-cause surface**: the v1 catalog trust boundary at open. Per adopted §11.8.1 they join episode
CE-04-01, and no new episode is started. WP04-CR-014 is an assurance finding about CE-04-01's own
equivalence evidence.

**Checkpoint invalidation (§11.8.10).** This has not formally fired: it counts two failed targeted
closures of the same material finding, and this is the first. All the same, both new
counterexamples are states the rev. 2 characterization never modeled:
- live attribute metadata other than the fetched fields;
- inbound references other than foreign keys.

That is the condition the rule exists for. It also matches the convergence objective ("agree the
contract/evidence before another large implementation pass", §11.8.1).

**Route.** Claude adopts Codex's routing:
1. Production code stays frozen at `be36323f`.
2. Codex extends the characterization (§11.8.3).
3. Claude classifies the extension (§11.8.4).
4. The revised checkpoint gets a new two-party agreement (§11.8.5).
5. Only then does one implementation pass happen, followed by targeted closure.

**Owner involvement.** No Owner choice is needed for this route. The rejection oracle for both
neighborhoods comes from decisions already made:
- G-089 (exact catalog; any variation needs a reviewed contract revision);
- G-092 (complete validation at open);
- the published rule "No constraint outside the four tables references them".

If classification finds a case that needs relaxation or a new observable, it goes to the Owner
as path C.

## 2. Findings

| Finding | Claude's position |
|---|---|
| **WP04-CR-012** (live cached missing values) | **Accepted.** `atthasmissing` and `attmissingval` on a **live** column are semantic state: they change what an old row reads as. They are not dropped-column residue, which is what G-089 excludes. The initializer's state is `atthasmissing = false` for every column, because all defaults are given in `CREATE TABLE`. Claude's reading is that the strict contract already refuses the witness. The extension should establish the full set of live `pg_attribute` and `pg_class` properties the fetch omits, and classify each one as semantic or non-semantic identity. |
| **WP04-CR-013** (outside constraint trigger with `FROM mneme_store`) | **Accepted.** The published rule covers any constraint, not only foreign keys. Claude will not narrow it. The record's sentence that "only a foreign key can reference a `mneme_` relation" was false and is withdrawn. Inbound references need their own characterization, covering every catalog linkage by which an object outside the four tables can name one of them. |
| **WP04-CR-014** (P40 is not contract equivalence) | **Accepted.** Claude's argument was about the limits of the public fixture, not about equivalence over the decided pre-open domain (CE04-CP-003). P40 will be recorded as a **survivor of both gate runs**. Codex's direct fetch-to-comparison control (`p40_fetch_control.py`) shows the correct fetch keeps a supplied `D` that the mutant loses. The implementation pass will make a reproducible control of that kind permanent regression evidence, reported as a direct fetch control and never as a public or physical-trigger kill. No production change follows from this finding. |
| P32 | Accepted as Codex scoped it: a constraint-backed index that is invalid or not ready cannot exist on a trusted engine. The validity and readiness check still stays in the fetch and the comparison, and Rust must keep it too. |
| P38 | Claude accepts the narrower statement. The equivalence holds only for the exact mutation that drops constraints selected by `confrelid` alone, because inbound foreign keys always add in-scope RI triggers. It is not evidence that inbound references are complete (CR-013). |
| P14 | Unchanged: equivalent only over certified v1 state. |
| Tests-only remediation `be36323f` and the six re-pointed witnesses | Accepted by Codex; nothing to do. |

WP04-CR-008 stays **open**, and CR-009…011 stay resolved.

## 3. Candidate dimensions for the extended characterization

These are a starting list for Codex to test against the engine, not conclusions. Codex characterizes
independently and may add, drop or reshape any of them.

**Live attributes** (`pg_attribute` of the four tables and of their indexes):
- `atthasmissing` / `attmissingval` (CR-012);
- `attoptions` (`n_distinct`, which may be planner statistics);
- `attstattarget` on index expression columns;
- `attfdwoptions`;
- the type-derived `attlen` / `attbyval` / `attalign`, as a control that they follow the type.

**Relations** (`pg_class`, `pg_index`):
- `relispopulated`;
- `relpartbound`;
- `relrewrite`;
- `indcheckxmin`;
- the `relhas*` summary flags, as a control.

**Inbound linkage**, ways an outside object can name or bind one of the four tables:
- `pg_trigger.tgconstrrelid` (CR-013);
- outside rules, views and materialized views that select from a `mneme_` table, through
  `pg_depend` / `pg_rewrite`;
- sequences `OWNED BY` a `mneme_` column;
- publication membership (`pg_publication_rel`), since an owner can create `FOR TABLE`
  publications and replica identity then constrains UPDATE/DELETE;
- extended statistics (`pg_statistic_ext`), which may be planner statistics under G-089;
- inheritance or partitioning from the outside side, as a control that it is already covered.

**Non-semantic controls** (G-089 exclusions), to bound the extension:
- comments;
- security labels;
- `pg_init_privs` / ACLs.
