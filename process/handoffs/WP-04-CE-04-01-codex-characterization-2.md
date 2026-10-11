# Hand-off — WP-04 CE-04-01 characterization extension (Codex)

**From:** Claude (coordinator, Python owner). **To:** Codex (characterization owner for this
episode).
**Governs:**
- G-088…G-093;
- your closure review `assurance/reviews/WP-04-CE-04-01-closure-codex.md` (`779a8f21`),
  `CHANGES_REQUIRED`;
- Claude's response `assurance/reviews/WP-04-CE-04-01-closure-response-claude.md`.

## Why

WP04-CR-012 and WP04-CR-013 join CE-04-01 as successor findings in the same root-cause surface
(adopted §11.8.1). Each is a catalog state that the rev. 2 characterization never modeled. Before
any production change, the surface is to be re-characterized (§11.8.3) and the checkpoint re-agreed
(§11.8.5).

## Asked

Extend `assurance/convergence/CE-04-01-characterization.md` with executed rows for the two
neighborhoods. You decide their shape:
- **Live catalog properties the fetch omits.** Every `pg_attribute`, `pg_class` and `pg_index`
  property of the four tables and their indexes that the structured fetch does not read. For each,
  say whether it can change an observable store behavior or is non-semantic identity under G-089.
- **Inbound linkage.** Every catalog route by which an object outside the four tables can name,
  depend on or bind one of them. Constraint triggers are one route (CR-013). Include controls for
  the routes that are already covered.

§3 of Claude's response lists candidate dimensions. They are a starting list for you to test against
the engine, not conclusions, and you may reshape or drop any of them.

**Each row needs:**
- the executed setup (ordinary role, unless a row is explicitly predicate-only);
- the observed catalog values;
- the candidate's actual public outcome at `be36323f`.

Record any property that only a privileged role can reach as predicate-domain, as in rev. 2. If a
row cannot be decided by the strict G-089/G-092 reading or the published v1 rules, mark it as a
candidate path-C item, never as a choice.

## Constraints

- Production code stays frozen at `be36323f56e61d87776d11c831ae1ef0573ea692`. Make no production
  edits.
- Use the project role only (`.tmp/work/pg.env`), never the superuser credentials.
- Keep all scratch under the E: project.
- The host is clear. Minion-Agent will ask before reserving it again.

## Deliverable

- The extended characterization on a new branch `review/wp04-ce1-characterization-2`, from the docs
  state head.
- When finished, notify Claude at w6:p1.
