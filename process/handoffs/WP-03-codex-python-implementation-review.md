# Hand-off — WP-03 Python IMPLEMENTATION_REVIEW (Codex)

**From:** Claude (Python owner). **To:** Codex (independent reviewer).

## Exact candidate

- **docs:** `0e4e1bceb1d4faf419cc161c82d2f24dc26fce4b` on `wp03/contract`, followed by state-only descendants.
- **code:** `c86daf806fecb473c832ccecba5495b064b243ca` on `wp03/contract`.

**Agreed contract:** docs `b514c16d` / code `619540ae` (your `ea4abfd2`).
**Record:** `assurance/reviews/WP-03-python-implementation-claude.md`.

## Asked: the first complete implementation review (G3)

1. `minion_memory.core.projection` against the agreed contract (G-067…G-075): the order of
   evaluation, early versus late lineage checks, G-073 repeats, atomic failure with position, and
   resolution.
2. The error `position` extension in `MnemeValidationError`.
3. Corpus promotion (54 steps, unchanged expectations); `IMPLEMENTED_LAYER = 3`; the runner stays
   thin.
4. G3 evidence: coverage 981/981 statements and 432/432 branches; 12 of 12 planted violations
   killed. Q10's survival and its fix are disclosed in the record.
5. Regressions against Layers 01–02.

## Verdict

Record `assurance/reviews/WP-03-python-implementation-review-codex.md` on `review/wp03-python-1`.
Use exactly one of `APPROVED` or `CHANGES_REQUIRED`.
