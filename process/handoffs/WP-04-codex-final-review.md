# Hand-off — WP-04 final complete review (Codex)

**From:** Claude. **To:** Codex.
**Stage:** `FINAL_CONTRACT_REVIEW`. Convergence episode CE-04-01 is settled: every episode finding
is provisionally closed (adopted §11.8.8).

## Exact candidate

The pair is the one named in `process/state/WP-04.yaml` (`current_candidate`):
- **code:** `9d5a2d51c69987f799962868b8dc5175a11882d2` on `wp04/contract`. It is `03841628`, which
  you approved in closure review 2, plus a comment-only change for WP04-CR-015.
- **docs:** the content commit named there. The state-only commit after it follows the state-only
  chain rule.

## History you have already reviewed

- **Contract:** reviews `0cc23387`, `f9d8e7d4` and `59c3a1a0` (CR-001…007), then `67ba6632`
  APPROVED (contract agreed at docs `d857fcc2`); Owner G-077…G-087.
- **Python implementation:**
  - review 1 `bb3dfa2c` (CR-008…011);
  - review 2 `391fca64` (CR-009…011 resolved), where CR-008 fired trigger A and the Owner chose
    convergence (G-088).
- **CE-04-01:**
  - characterization `0f7ac1bf`, extension `d8262cf5`;
  - checkpoint reviews `1ffec311`, `bfb6cad3` (APPROVED), `1d158979`, `76908bc8`, `955d91f6`
    (APPROVED);
  - closure review 1 `779a8f21` (CHANGES_REQUIRED, CR-012…014);
  - closure review 2 `46514f00` (APPROVED; CR-008/012/013/014 closed; CR-015 open, non-blocking);
  - Owner G-089…G-098.

## Asked: one complete review of WP-04 at the exact pair

1. **Contract.** `spec/persistence.md`, "Layer 04 canonical history store contract", including the
   reference backend, read as one consistent text and faithful to G-077…G-098. Requirements:
   PERS-005, 006, 007, 008, 012, 014, 015; HIST-008, 009.
2. **Corpus.** The conformance scenarios, manifest and traceability for these requirements.
3. **Python.** `minion_memory.persistence` against the whole contract, and the gate evidence at the
   exact code: `assurance/reviews/WP-04-CE-04-01-implementation-claude-2.md` §5.3. Gate runs 3 and 4
   are kept as history.
4. **WP04-CR-015.** Is the repair (record §2 and the test comment) correct?
5. **Rust readiness** for Layer 04:
   - the shared pins;
   - the whole-row member rule and its exclusion list;
   - the [F] method;
   - the [IT] cross-language witnesses.
6. **Records.** Plan, feasibility and state are current.

Prior closures are not reopened without new evidence.

## Verdict

- Record `assurance/reviews/WP-04-final-review-codex.md` on `review/wp04-final`.
- Use exactly one of `APPROVED` or `CHANGES_REQUIRED`.
- On APPROVED, Claude accepts under G-009 and moves WP-04 to `RUST_IMPLEMENTATION`.
- When finished, notify Claude at w6:p1.
