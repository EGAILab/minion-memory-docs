# Cross-Language Feasibility Matrix — WP-03: canonical HistoryProjector and lineage resolution

**Required by:** `process/agent-workflow.md` §3 step 5. **Template:**
`process/templates/cross-language-feasibility-matrix.md`.
**Authority bundle:** `mneme-v2.3-dual-profile`. **Author:** Claude (shared-contract owner).
**Independent reviewer:** Codex.

**Contract:** agreed contract docs `b514c16d` / code `619540ae` (Codex APPROVED `ea4abfd2`). The
semantics are unchanged since then:
- HIST-006 (corrections append);
- HIST-007 (lineage), `spec/core.md` "Lineage (Owner G-068, G-069, G-071…G-075)";
- PROJ-001, "Canonical HistoryProjector (Owner G-067, G-070, G-073)";
- PROJ-002.

**Governance:** G-066…G-075, in `reference/governance/2026-10-11-owner-layer03-start.md`.
**Candidate evidence:** Python implementation code `dd55fb4f`, approved by Codex in `2df90f22`.
**Toolchains:** Python CPython 3.12.8 (uv-managed, project-local) and Rust 1.97.1. SQLite is not
used in this layer.

**Status:** complete for the Rust handoff; revised for WP03-CR-007 after Codex's final review
`88b8bb3f`.

Evidence keys used below:
- **[PT]** `minion-memory-python/tests/core/test_layer03_projection.py` at `dd55fb4f`;
- **[CP]** and **[LH]** the ACTIVE scenarios `conformance/core/projection-canonical-path.yaml` and
  `projection-lineage-current-heads.yaml` (54 steps);
- **[MU]** Claude's planted-violation run `.tmp/work/claude/py_mutants_wp03.py` (12/12 killed);
- **[CX]** Codex's review executions: contract oracles `.tmp/work/codex/wp03-oracles*.py`,
  `2df90f22`, and the final review `88b8bb3f`;
- **[L1]** and **[L2]** the certified Layer 01 and Layer 02 evidence (G-044, G-065), cited only for
  seams this WP consumes unchanged.

## 1. Value-domain matrix

| Observable value / field | Contract domain (spec anchor) | Python repr | Rust repr (required) | Canonical serialization | Lossless across all? | Witness |
|---|---|---|---|---|---|---|
| `stream` | closed `{store_id, entries}` (PROJ-001) | `dict` | `Value` object with explicit member checks | JSON object | YES | [CP] shape steps; [PT] `test_stream_shapes` |
| `store_id` | CORE-001 stable ID | `str` | `String` via the L01 `id_rule` | JSON string | YES (ASCII) | [CP] "store_id outside the stable-ID domain" |
| `entries[].position` | integral, strictly increasing from 1, at most 2^53−1; 0 is never an entry (G-054) | `int`, with `bool` rejected | `i128` / `u64` after L01 normalization | JSON number (`2.0` → 2) | YES | [CP] non-increasing, equal and 0 steps; [PT] bool and 1.5 |
| `entries[].record` | Layer 02 envelope (HIST-002) | normalized `dict` | normalized `Value` | JSON object | YES | [L2] admission corpus |
| relation `from_record_id` / `to_record_id` | CORE-001 IDs; available/unavailable per G-072 | `str` | `String` | JSON string | YES | [LH] endpoint steps; [PT] early shapes |
| relation `relation` | exactly one of 4 strings (HIST-007) | exact `str` compare | enum via exact string match, never numeric or case-folded | JSON string | YES | [LH] "non-string relation kind", "outside the vocabulary" |
| `to_artifact` versioned | `{stable_id, artifact_version}`: CORE-001 + CORE-002 edition (G-075) | tuple | struct | JSON object | YES | [LH] edition 0, bare ID, both forms |
| `to_artifact` hash | `{content_hash}`: 64 lowercase hex, the CORE-011 form (G-075) | `str` + regex | `String` + exact lowercase-hex check | JSON string | YES | [LH] uppercase hash; content-hash control |
| `duplicates` | `{position, record_id}` per later identical occurrence (G-073) | `list[dict]` | `Vec` | JSON array | YES | [CP] coalesce step |
| `relations`, `unresolved_derivations` | distinct relations, in the presentation order of PROJ-001 | sorted `list` | sorted `Vec`; never `HashSet` iteration order | JSON array | YES | [PT] `test_presentation_order_of_relation_targets`; [LH] |
| `current`, `interpretations` | set-valued, presented in store-position order (G-069, G-074) | `list` | `Vec` | JSON array | YES | [LH]; [PT] interpretation order |
| `through` | HistoryBoundary `{store_id, position}`; 0 for an empty stream | `dict` | struct | JSON object | YES | [CP] empty stream |
| error `position` | entry errors only, including `unknown_required`; absent otherwise (PROJ-001) | `MnemeValidationError.position: int | None` | **additive** `Error.position: Option<i128>` | runner observation key `position` | YES | [CP] position steps; [PT] routing-identity controls |
| `unknown_required` detail | the full routing triple `(profile, record_type, schema_version)` (G-070) | formatted string | formatted string; diagnostic, not compared byte-for-byte | not part of the corpus | YES | [PT] 8 routing controls, killed when the profile is omitted ([CX] `2df90f22`) |

## 2. Lower-layer capability matrix

| Required semantic operation | Owning layer | Existing reviewed seam | Exact? | Python | Rust | Additive extension? | Reopen? |
|---|---|---|---|---|---|---|---|
| generic stages across 3 arguments (G-031) | 01 | `validate_arguments` | yes | yes | yes (`staged`) | no | no |
| envelope admission and the gates (G-055) | 02 | `_admit` / `envelope_rule` | yes | yes | yes | no | no |
| reader validation (G-053) | 02 | `_reader_rule` / `reader_rule` | yes | yes | yes | no | no |
| timestamp normalization before comparing repeats (G-073) | 01/02 | HIST-004 rule inside gate 4 | yes | yes | yes | no | no |
| canonical envelope equality (G-073) | 01 | SER-009 canonical bytes | yes | yes | yes | no | no |
| CORE-001 tokens, CORE-002 editions | 01 | `_stable_id_rule` / `id_rule`; `_is_edition` / `integer` | yes | yes | yes | no | no |
| CORE-011 hash form | 01 | `raw_content_hash` output form | yes | regex | exact check | no | no |
| error `position` | 01 error type | `MnemeValidationError` / `Error` | — | added (`at_position`) | to add | **yes, additive** (optional field; Layer 01/02 errors carry none) | no |
| routing-triple detail | 03 | built from the gate-1-validated record | yes | yes | to add | no (Layer 02's detail is untouched) | no |
| iterative graph checks | 03 | Kahn per family | yes | yes | to add (iterative) | no | no |

## 3. Hazard checklist (every member of each touched family)

| Hazard (family/member) | State | Evidence / reason |
|---|---|---|
| H1 integer width | AUDITED | positions and editions use the L01 safe bound; 2^53 fails at generic stage 2 ([L2] boundary corpus); [PT] long-chain positions up to 3000 |
| H1 JSON number lexical forms | AUDITED | `2.0` positions and editions normalize via L01 ([CP] gaps step; [L2] `schema_version 1.0`) |
| H1 float policy | AUDITED | positions and editions are integral; `1.5` is invalid ([PT] stream shapes); payload floats normalize in L01 ([L1]) |
| H1 arithmetic | NOT_APPLICABLE | no arithmetic on positions or editions; only comparisons |
| H1 SQLite affinity | NOT_APPLICABLE | no persistence in Layer 03 (Layer 04) |
| H2 scalar domain | AUDITED | inherited L01 decoding ([L1]); IDs and tokens are ASCII |
| H2 encoding | AUDITED | inherited L01 UTF-8 decoding ([L1]); `JsonText` seams in [PT] |
| H2 NUL | AUDITED | NUL is rejected by the ID and token grammars; payload strings use the L01 domain ([L1]) |
| H2 length units | AUDITED | ID and hash lengths are ASCII bytes, so the units coincide |
| H2 line endings | NOT_APPLICABLE | no text is hashed or compared outside canonical JSON |
| H3 normalization | NOT_APPLICABLE | no Unicode normalization anywhere (CORE-001 exact compare) |
| H3 case mapping/folding | AUDITED | relation kinds and hashes are case-sensitive exact matches ([LH] uppercase hash, non-string kind) |
| H3 collation/sort | AUDITED | presentation order uses store positions and ASCII ID or hash comparison, never locale ([PT] presentation-order test) |
| H3 Unicode version | NOT_APPLICABLE | no Unicode data tables used |
| H3 lexical tokenization | NOT_APPLICABLE | no lexical retrieval |
| H4 representation | AUDITED | `recorded_at` and `occurred_at` are normalized by the L02 gate 4 before canonical comparison, so equal instants in different spellings coalesce |
| H4 unknown vs present | AUDITED | inherited G-049 ([L2]) |
| H4 clocks | NOT_APPLICABLE | the projector reads no clock |
| H4 ordering | AUDITED | timestamps never order or select (G-069); [LH] "relation order never changes" and the divergent heads |
| H4 leap seconds/DST | AUDITED | inherited HIST-004 rejects `:60` ([L1]) |
| H5 map iteration | AUDITED | no host map order is observable; [PT] `test_relation_order_and_member_order_never_change_the_result` (25 shuffles plus member reversal) |
| H5 canonical key order | AUDITED | the G-073 comparison uses SER-009 bytes (UTF-16 key order) ([L1]) |
| H5 sort stability and keys | AUDITED | the relation presentation key is total (from position, kind, typed target key); [PT] presentation test |
| H5 sets | AUDITED | `current` and `interpretations` are set-valued and presented by position, never selected (G-069); relation collapse (G-072) in [LH] |
| H5 pagination | DEFERRED_WITH_REASON | bounded and incremental projection is Layer 05 (PERS-007/008, checkpoints); trigger WP-05 |
| H6 YAML version | AUDITED | corpus gate ([L1] corpus discipline); `mneme-process check` |
| H6 duplicate keys | AUDITED | `value.duplicate_key` in relations precedes reader errors ([PT] generic-stage control) |
| H6 anchors/aliases | AUDITED | corpus gate rejects them ([L1]) |
| H6 big numbers | AUDITED | generic stage 2 ([L1]) |
| H6 null vs missing | AUDITED | a missing target member vs `to_artifact` vs both is closed shape ([LH] both-targets step); `occurred_at: null` is invalid ([L2]) |
| H6 enforcement | AUDITED | `mneme-process check --deep-sources` 8/8 at every candidate |
| H7 algorithm and output | AUDITED | `content_hash` targets must be the CORE-011 lowercase SHA-256 form ([LH] uppercase rejected) |
| H7 canonical form | AUDITED | identical-repeat detection compares SER-009 canonical bytes of normalized envelopes; [CP] coalesce vs conflicting steps; [MU] Q03/Q04 killed |
| H7 identity vs integrity | AUDITED | a hash identifies an external artifact only as a reference target and never as a record identity; records with equal content but different IDs are not deduplicated ([CP] "equal content under different ids") |
| H8 (all members) | NOT_APPLICABLE | no persistence or transactions in Layer 03; durable append enforcement is Layer 04 (G-067) |
| H9 (all members) | NOT_APPLICABLE | no filesystem paths |
| H10 (all members) | NOT_APPLICABLE | pure synchronous function; no retry or concurrency |
| H11 ID lexical domain | AUDITED | CORE-001 for record IDs, endpoints, `store_id` and artifact `stable_id` ([LH] bad endpoint spelling; [CP] `store_id`) |
| H11 version domain | AUDITED | `artifact_version` is a CORE-002 edition ([LH] edition 0) |
| H11 scope encoding | NOT_APPLICABLE | the projector does not use MemoryScope (WP-02S) |
| H11 reference integrity | AUDITED | resolution-family endpoints must be available, while `derived_from` may be unresolved (G-072); typed targets (G-075); [LH] unknown, excluded and unavailable endpoints; [MU] Q05, Q10 |

## 4. Concurrency / order matrix

NOT_APPLICABLE for concurrency: the projector is a pure function. The ordering guarantees it does
make:

| Ordering guarantee | Realistic wrong implementation | Witness that kills it |
|---|---|---|
| no tie-break among current heads (G-069) | keep only the latest head | [LH] divergent heads; [MU] Q01 |
| atomic failure (G-070) | return records projected before the failure | [CP] unknown-required step; [MU] Q02 |
| first failing entry wins | report a later error | [CP] "earliest failing position wins" |
| **early shape checks precede entries; late graph checks follow them** (HIST-007, CR-003) | check `to_artifact`-on-a-resolution-kind late, as an unavailable endpoint | the paired-entry witness: a `supersedes` relation with `to_artifact` plus an unknown-required entry must give `lineage.invalid` (early). The late reading gives `history.unknown_required` at position 1. [PT] `test_artifact_target_on_a_resolution_kind_is_an_early_shape_error`; [MU] Q10 (survived until this control was added) |
| late graph checks follow entries | check endpoint availability early | [LH] "late graph: an unavailable from endpoint does not precede entry errors"; "a conflicting record reuse precedes lineage errors" |
| relation order is irrelevant | output in input order | [LH] relation-order step; [MU] Q12 |

## 5. Neighborhood expansion record

| Family | Members probed | Probe source | New rows / findings |
|---|---|---|---|
| H5 sets/order | all 5 | [PT] shuffle test; [MU] Q01, Q12 | none |
| H11 reference integrity | endpoint kinds × available/excluded/unknown/artifact | [LH]; [MU] Q05, Q10 | Q10 showed early-vs-late was undertested; a control was added (record `WP-03-python-implementation-claude.md`) |
| H7 canonical form | identical vs conflicting repeats, equal content under different IDs | [CP]; [MU] Q03/Q04 | none |
| error-diagnostic completeness | routing triple × 2 profiles × 2 cases × 2 seams | [PT]; [CX] `7d328f95` / `2df90f22` | WP03-CR-006 (fixed) |

## 6. Verdict

```text
FEASIBILITY
    READY     every row AUDITED / NOT_APPLICABLE / DEFERRED_WITH_REASON (H5 pagination → Layer 05);
              no open finding apart from WP03-CR-007, which this revision repairs. Rust needs only the
              additive optional error position, the routing-triple detail, and an iterative graph
              check over the certified Layer 01/02 seams.
```
