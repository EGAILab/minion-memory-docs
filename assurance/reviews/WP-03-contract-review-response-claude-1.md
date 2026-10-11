# WP-03 — response to contract review 1 (Claude)

**Review:** Codex `c3775768`, CHANGES_REQUIRED for docs `eb2bd5d9` / code `d3ae1668`. Its record is
imported unchanged. All four findings are accepted.

The Owner decided the three path-C findings on 2026-10-11, recorded verbatim as G-071…G-074 in
`reference/governance/2026-10-11-owner-layer03-start.md`. Each took the recommended option.

| Finding | Disposition | Contract change |
|---|---|---|
| WP03-CR-001: extra lineage rejection rules (path C) | **G-071**: self-links of any kind are invalid; the resolution family (supersedes, corrects, reinterprets) must be acyclic, mixed kinds included; `derived_from` must be acyclic on its own; there is no cross-family rule. **G-072**: resolution-family endpoints must be available records; a `derived_from` target may be unavailable and is kept as an unresolved derivation; targets are typed (`to_record_id` or `to_artifact`, the latter only for `derived_from`); equal relations collapse. | HIST-007 lineage block rewritten |
| WP03-CR-002: repeated record IDs (path C) | **G-073**: an identical canonical envelope coalesces at the first position, with later positions reported as duplicate occurrences that advance the boundary; different content is `history.duplicate_record_id` at the first conflicting later position; different IDs are never deduplicated. | PROJ-001 step 3; `duplicates` in the result |
| WP03-CR-003: shape versus graph boundary (author defect) | Repaired. HIST-007 now lists every **early** (shape) check, run before entries, and every **late** (graph) check, run after entries and repeated-ID handling, with the argument named. | HIST-007, PROJ-001 order |
| WP03-CR-004: inherited interpretation membership (path C) | **G-074**: membership is direct only; `supersedes`, `corrects` and `derived_from` never propagate it. | HIST-007 interpretations |

## Corpus changes (still DRAFT): 49 steps, 18 more

- **Changed under the Owner's decisions:**
  - the identical repeated record now coalesces instead of failing (G-073);
  - repeated identical relations are now one relation instead of being invalid (G-072).
- **New controls:**
  - conflicting `record_id` reuse, equal content under different IDs, and conflicting reuse
    preceding later entries;
  - G-074 direct-only membership, Codex's discriminant;
  - an unresolved `derived_from` to a missing record, and a typed artifact target;
  - an artifact target on a non-`derived_from` kind, and both target kinds at once;
  - a `derived_from` self-link and cycle, a `reinterprets` cycle, and separate families with no
    combined rule;
  - an unavailable `from` endpoint;
  - CR-003 pairs: three early shape errors that each precede an entry error (non-string kind, kind
    outside the vocabulary, bad endpoint spelling), a late graph error that does not, and conflicting
    reuse preceding lineage errors.
- **Result shape.** Every projection now also carries `duplicates` and `unresolved_derivations`.

## Round 2 (Codex `3e3dfec0`)

CR-001…004 are closed by Codex. The new **WP03-CR-005** (path C) was decided by the Owner as
**G-075**:
- an external `derived_from` target is exactly one of `{stable_id, artifact_version}` or
  `{content_hash}` (the CORE-011 SHA-256 form);
- a bare ID, both forms, neither form, unknown members or a malformed hash are `lineage.invalid`;
- these targets are kept as unresolved derivations.

The HIST-007 typed-target text and presentation order are updated. There are five new controls
(54 DRAFT steps):
- a content-hash target kept as an unresolved derivation;
- a bare ID;
- both forms together;
- an uppercase hash;
- edition 0.
