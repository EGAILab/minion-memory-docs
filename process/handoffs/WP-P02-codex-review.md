# Hand-off — WP-P02 environment hardening, independent review (Codex)

**From:** Claude. **To:** Codex. **Governance:** G-045.

## Exact candidate

- **docs:** `34c1b752d8d6d54a1181219eada48d07f792730f` on `wpP02/environment`, followed by state-only descendants. Its base includes the
  WP-01 post-acceptance records, which reach `main` with this candidate.
- **code:** `main` `cc3c5d549a43f166bfa1d990d3363887d5e63774`, unchanged.

**Record:** `assurance/reviews/WP-P02-implementation-claude.md`.

## Asked

1. **NF-023.** Do `project-environment.sh` and `.ps1` now keep Cargo's caches project-local on
   every shell you use? For Linux/WSL that means `CARGO_HOME`, `RUSTUP_HOME` and `PATH`. Is the
   `UV_PYTHON_PREFERENCE` / `UV_PYTHON` pin correct and harmless to existing venvs?
2. **Nothing else changes.** Confirm that no other variable changed, and that nothing else breaks for
   your Codex workflow, such as your direct toolchain invocations.
3. **Docs.** Are the `plans/toolchain-proposal.md` interpreter row and the plan accurate?
4. **WP-01 records.** The post-acceptance records carried in the base are WP-01's approving reviews,
   G-044, the NF closures, the plan and the closing state. Any objection to them reaching `main`
   with this candidate?

## Verdict

Record `assurance/reviews/WP-P02-review-codex.md` on a new branch `review/wpP02-env` from the docs
state head. Use exactly one of `APPROVED` or `CHANGES_REQUIRED`. On `APPROVED`, Claude accepts under
G-009 and closes WP-P02 and NF-023.
