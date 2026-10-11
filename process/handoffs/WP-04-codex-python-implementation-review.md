# Hand-off: WP-04 Python implementation review (Codex)

**Candidate:** code `afb36081fc569246e6055f2bde99ca9481ca5e8a` / docs `b94d0fde9118a33d5eba7055a0060c3531ea0327`, both on `wp04/contract`.
**Authority:**
- the agreed contract, docs `d857fcc2` / code `1f443876` (Codex APPROVED `67ba6632`);
- Owner G-077…G-087.

The Python implementation record is `assurance/reviews/WP-04-python-implementation-claude.md`. Its claims are to be
reproduced, not trusted.

**Task.** An independent IMPLEMENTATION_REVIEW of `minion_memory.persistence`, the D1–D4 draft mode in
`core/history.py`, the conformance-runner Layer 04 seams, `tests/pgdb.py` and `tests/core/test_layer04_store.py`, against
the contract text. The record lists three points offered for challenge:
- the new `persistence` package-root namespace and the widened scaffold gate;
- the shared, emptied test schema;
- the claim that P14 is an equivalent mutant.

Record APPROVED or CHANGES_REQUIRED on `review/wp04-python-1`.
