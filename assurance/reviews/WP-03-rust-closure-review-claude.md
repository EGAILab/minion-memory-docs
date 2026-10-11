# WP-03 (Layer 03) — Rust CLOSURE_REVIEW (Claude)

**Verdict: APPROVED.** There are no findings.

**Exact pair:**
- code `e9a94f78c8d1a44281bab1902f0c5af76d0deb9c` (`wp03/rust`, from code `main` `dd55fb4f`);
- docs `ce904f4f6d63edfa864effe2bc6aebbdec5f4817`, with state on `wp03/rust-state` at `512e1772`.

**Author:** Codex. **Reviewer:** Claude, who did not author any Rust code.
**Authority:** the accepted WP-03 contract (HIST-006/007, PROJ-001/002, G-066…G-075), the two ACTIVE
projection scenarios, and the feasibility matrix.

Python generated disagreements only to adjudicate against the text, and none arose. Codex's record
was treated as claims to reproduce.

## Reading against the contract

- **Order of evaluation (`projection.rs`).** Generic stages across `reader`, `stream` and
  `relations`, then the reader, the stream (closed; positions strictly increasing from 1) and the
  **early** lineage checks.
  - **Early checks:** exactly 3 members, a CORE-001 source, an exact-string kind, exactly one typed
    target, `to_artifact` only for `derived_from`, and the versioned or lowercase-64-hex identities.
  - **Equal relations collapse** through a `BTreeSet`.
- **Entries, in position order.**
  - `unknown_required` has the full routing triple in its detail, taken from the record before
    admission; it names no argument and carries the position (G-070).
  - Every other entry error names `stream` and carries the position.
  - A repeated record ID compares canonical bytes: identical coalesces, different content fails
    (G-073).
- **Late checks.** The source must be available; no record self-links; resolution targets must be
  available; an unavailable `derived_from` target goes to unresolved derivations; iterative Kahn
  checks per family (G-071, G-072).
- **Resolution.** Current heads are set-valued, presented in index order (= first-position order);
  interpretations come from direct `reinterprets` only (G-069, G-074).
- **Presentation key.** It equals the contract's: the `Kind` variant order is the lexical
  relation-kind order, and target keys go record by position, then record by ID, then versioned,
  then hash.
- **Layer 01/02 changes, all additive.** Three new error codes; `Error.position:
  Option<i128>`, `None` by default and displayed only when set; Layer 02 helpers made
  crate-visible; a new iterative `Value::detached`. Layer 01/02 behaviour is unchanged, and their 15
  ACTIVE scenarios still pass.

## Executions (project-local; rustc 1.97.1)

| Check | Result |
|---|---|
| Windows: fmt, clippy `-D warnings`, rustdoc `-D warnings` | clean |
| Windows: `cargo test --locked --offline` | all pass; **17 ACTIVE, 343 steps**, 5 placeholder `xfail`s |
| Linux (WSL), the same checkout | fmt and clippy clean; the same 17 / 343; all pass |
| Python at the candidate (G2) | no Python or corpus delta; 496 passed, 5 xfailed |
| `mneme-process check --deep-sources` | 8/8 |
| Differential, 5 seeds × 20,000 random streams and relation lists (JSON bytes) | **0** disagreements; every Layer 03 error code plus 10,408 successful projections |
| Targeted pass: 40,000 valid streams with valid-kind relations, including identical repeats, artifacts and unresolved links | **0** disagreements; 36,615 successful projections |
| Planted violations: Claude's own 12, independent of Codex's 18 | **12/12 killed** |

The 12 planted violations:
- a last-head tie-break;
- `unknown_required` naming an argument;
- identical repeats rejected;
- conflicting reuse coalesced;
- an unavailable `derived_from` rejected;
- `to_artifact` allowed on resolution kinds — the early-versus-late seam, killed by Codex's
  dedicated paired-entry test;
- interpretations including replaced records;
- derivation cycles allowed;
- `corrects` not replacing;
- entry errors losing their position;
- an empty stream reporting `through` position 1;
- uppercase hex accepted.

The scripts are in `.tmp/work/claude/`: `rust-probe-l03/`, `l03_closure_diff.py`,
`l03_closure_targeted.py`, `l03_rust_mutants.py` and `l03-closure-linux.sh`.

## Disposition

Rust Layer 03 is approved. Acceptance follows under G-009; certification needs the Owner's
decision.
