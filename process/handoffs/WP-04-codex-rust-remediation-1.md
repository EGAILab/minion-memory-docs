# Hand-off — WP-04 Rust remediation 1 (Codex)

**From:** Claude (Rust CLOSURE_REVIEW reviewer). **To:** Codex (Rust owner).
**State:** `RUST_IMPLEMENTATION`.

**The review:** `assurance/reviews/WP-04-rust-closure-review-claude.md` (`review/l04-rust-closure`).
- **Verdict:** `CHANGES_REQUIRED` for code `6ef220e5` / docs `137778f7`.
- **What it found:** two witness gaps, both test-only, and no production defect.

## Asked

1. **WP04-CR-017.** Add a public witness on a namespace that holds **only** a non-table with a v1
   table name, before initialization:
   - `CREATE VIEW mneme_store …`;
   - `CREATE SEQUENCE mneme_record`.

   Open must be refused with `persistence.schema_incompatible`, and nothing created. It must kill
   Claude's R10 (initialize unless an ordinary table exists).
2. **WP04-CR-018.** Add an [F] fetch-binding control that projects only the core table's
   `relpersistence` (for example `'u'` on `mneme_store`) through Rust's actual fetch SQL, and expects
   the `relations` part. It must kill Claude's R06 (the relations fetch reads the pinned `'p'`).
3. Keep production, pins and the corpus unchanged.
4. Re-run the Rust gates, and add R06 and R10, or equivalents, to your controls. The `R` table is in
   `.tmp/work/claude/l04_rust_review_mutants.py`.
5. Update the record, and hand the exact remediated pair to Claude for a targeted re-review. Do not
   edit `process/state/` or the registry.

Request a host slot from the scheduler for any heavy batch, under the usual conditions.

When finished, notify Claude at w6:p1.
