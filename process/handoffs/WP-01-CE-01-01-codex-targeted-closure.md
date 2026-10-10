# Hand-off — WP-01 CE-01-01 targeted closure (Codex)

**From:** Claude. **To:** Codex.

## Exact candidate

- **docs:** `18bc390c2e8102113b3c152ff21d79fdc3201a15` on `wp01/contract`; the state-only descendants follow it.
- **code:** `4fe3ed34c29a6868a3f5050ecee95885b73bead0` on `wp01/contract`.

**Agreed checkpoint:** `assurance/convergence/CE-01-01-classification.md`, revision 3 (`8e8d30a8`;
your APPROVED `1d99bc2c`). **Implementation record:**
`assurance/reviews/WP-01-CE-01-01-implementation-claude.md`.

## Scope

Close WP01-CR-007 (= PY-004) and WP01-CR-008 (= PY-008) strictly against the agreed rows, decisions
G-037…G-043 and checkpoint §4–§5, with your own executions.

The recorded claims to verify:
- **Normative rows.** On the implementation, your driver with an exact-return observer gives
  25,470/25,470 OK with zero hooks, and 0 non-exact returns among 6,775 value rows.
- **Boundary rows.** All 75 meet their decided oracles.
- **Unit controls.** The 252 tests fail as recorded on `eb47635c` (128 failed) and all pass on the
  implementation.

Also in scope:
- the POSIX run;
- anything this pass broke elsewhere in `minion_memory.core`: the earlier Layer 01 scenarios and
  units, and the WP01-PY-001…007 closures.

## Verdict

Record `assurance/reviews/WP-01-CE-01-01-targeted-closure-codex.md` on a new branch
`review/wp01-ce1-closure` from the docs state head. Give per-finding dispositions and an overall
`APPROVED` or `CHANGES_REQUIRED` for the exact pair.

Approval is not acceptance. Do not modify production modules or the authoring worktrees.
