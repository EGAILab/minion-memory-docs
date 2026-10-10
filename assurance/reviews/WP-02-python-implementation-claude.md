# WP-02 — Python implementation record (Claude)

**Agreed contract:** docs `6f761081` / code `15b71ca3` (Codex APPROVED `18902542`).
**Implementation:** code `1d7167c85d4516dea6903ada6745139c3ac222f3` on `wp02/contract`.
**Gate:** G3 (Python), author-run at the exact code. This record is evidence, not a review.

## Implementation (`minion_memory.core.history`)

| Contract | Public seam | Notes |
|---|---|---|
| SER-005 reader (G-053) | `admit_history_record(reader, record)` | A closed reader with closed entries. Duplicates are rejected after normalization (so `1` and `1.0` are the same), and only then is a frozen set used. |
| HIST-002 gates (G-055) | same | **1.** The routing triple (G-052). **2.** Profile admission (G-050), then `compatibility`, then recognition: `skip`, or `history.unknown_required`, which names no argument. **3.** The closed shape (G-048, G-049). **4.** `occurred_at`, `record_id` and `recorded_at` in canonical member order. |
| Generic stages (G-031) | via `validate_arguments` | Stages 1–2 run across `reader`, then `record`, before any gate; native inputs are handled under Layer 01 G-036…G-043. |
| HIST-010 | decode result | A new dict of normalized values; `payload` and `provenance` are returned unchanged, and the caller's value is never mutated. |
| HIST-005 (G-051, G-054) | `compare_history_boundaries`, `history_boundaries_equal` | Closed `{store_id, position}`, position 0…2^53−1. Cross-store ordering is `history.boundary_incomparable` with no argument; cross-store equality is `false`. |

The result type is `HistoryAdmission(outcome, envelope)`, a frozen dataclass. `envelope` is
present only for `decode`.

## Corpus and runner

- **Scenarios.** The four Layer 02 scenarios (70 steps) are promoted from DRAFT to **ACTIVE** on the
  agreed contract. Their expectations are unchanged from the approved candidate; only `status`
  moves.
- **Implemented-layer rule.** `conformance/README.md` gains the rule under NF-026: each runner
  declares the highest layer its language implements, and an ACTIVE scenario above it is an `xfail`
  that names the layer and the language. The Python runner declares `IMPLEMENTED_LAYER = 2`. The
  Rust runner should declare 1 until Rust Layer 02; that change is Codex's under NF-026.
- **Runner operations.** The new operations `admit_history_record`, `compare_history_boundaries` and
  `history_boundaries_equal` each map to one public function.

## Gates (Windows, project-local CPython 3.12.8)

- **Lint and types.** `ruff` and `ruff format --check` are clean; `mypy --strict` is clean on 14
  files.
- **pytest.** **386 passed, 5 xfailed**; the expected failures are the five Layer 04+ placeholders.
- **Corpus.** All 12 ACTIVE scenarios pass (8 from Layer 01, 4 from Layer 02).
- **Coverage.** Statement and branch coverage of all of `minion_memory`, with no exclusions and
  subprocesses included: **740/740 statements, 332/332 branches**.
- **`mneme-process check --deep-sources`.** 8/8.

## Discrimination (planted contract violations)

12 single-point violations were planted in a scratch copy of `history.py` and the full suite run on
each; **11 were killed**:
- `compatibility` checked before admission;
- no closed shape;
- unrecognized required records skipped;
- duplicate reader pairs merged;
- cross-store positions compared;
- negative positions allowed;
- `occurred_at: null` treated as unknown;
- typed fields checked before the shape;
- `schema_version 0` accepted;
- `history.unknown_required` naming an argument;
- timestamps not normalized.

**P12, typed fields in source order, survived and is equivalent.** Layer 01 normalization already
returns object members in canonical (UTF-16) order, so source order and canonical order coincide
at gate 4.

The script is in `.tmp/work/claude/py_mutants_wp02.py`.

No POSIX run is claimed.

## Correction after Codex review `a29b0092` (WP02-CR-006)

**The P12 equivalence claim above was wrong.** Layer 01 normalization orders members canonically
only for **native** input. JSON-text decoding keeps source member order. So gate 4's canonical sort
is observable, and P12 (typed fields in source order) was a surviving discriminating mutant. Codex's
witness is a JSON-text record with an invalid `record_id` before `occurred_at: null` in source
order: the contract gives `timestamp.invalid`, and P12 gives `id.invalid`.

**Repair, at code `43e0984e585975719231ba53466a9c78eba796e7`:**
- Added public-API controls in `tests/core/test_layer02_history.py`. They cover every source order
  of the three typed fields, with every combination of two or three invalid ones, through both
  `JsonText` and native input: 48 cases, plus Codex's witness.
- No production change.
- **Planted bugs: 12/12 killed**, with P12 now caught by the canonical-order sweep.
- **Gates.** 435 passed, 5 xfailed; coverage 740/740 statements and 332/332 branches; ruff, format
  and mypy strict clean.
- **Base.** The code base now includes the NF-026 Rust runner fix `b9f42d42`, which Codex
  authored and Claude reviewed and approved.
