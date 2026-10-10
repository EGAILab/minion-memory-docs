# WP-01 Layer 01 contract review 2 — Codex

## Verdict and reviewed objects

**CHANGES_REQUIRED** for docs `7d51960ba1343ec7f7dadb7f7ec954610573e5bb` paired with
code `4224a45e4606a55d0bfaa08097956a4952ddd512`.

Review branch: `review/wp01-contract-2`, based on state commit
`936313db24e802f73a2d017ec44dfe6d876d90d7`. Both candidate repositories were reviewed in
separate detached checkouts. Claude's authoring worktrees and production modules were untouched.
Authority: round-2 handoff; verbatim G-028–G-033; existing reviewed authority; finding taxonomy
§1.1. This verdict concerns the contract checkpoint, not acceptance onto main.

The supplied expectations reproduce. The remaining blockers are an unresolved observable
ordering choice and contradictory typed-error wording, not a failed supplied hash or a Mneme
implementation defect. Claude's response and feasibility records were review objects, not
substitutes for my executions.

## Prior findings and fidelity

| Item | Independent disposition |
|---|---|
| WP01-CR-001 | Provisionally closed: G-028 permits both letter cases, G-029 fixes local and UTC years 0001–9999 and rejects UTC overflow, and G-030 requires the grammar. HIST-004 transcribes these choices. All 36 supplied timestamp cases reproduce. The new typed-error wording defect is separately CR-006 below. |
| WP01-CR-002 | Provisionally closed: the old ±285-year argument is withdrawn. The internal signed microsecond range fits `i64`, with exact Python/Rust round trips at both endpoints and all ten evidence instants. The internal value is correctly distinguished from a portable JSON number. |
| WP01-CR-003 | Partially resolved, not fully closed: G-031 supplies the three-stage precedence and one-error policy; the error vocabulary now covers syntax, finite numbers, native kinds, decoded duplicates and surrogates. The traversal choice remains CR-005; the timestamp seam contradiction is CR-006. |
| WP01-CR-004 | Provisionally closed: CORE-003 supplies the comparison outcomes and visible conflict code; its seven DRAFT cases reproduce from independently computed canonical projections. Persistence and per-type projection ownership remain explicitly in later layers. |
| Q1 | Answered by G-032/G-033: operation identity is a namespaced pair; namespace uses G-020, opaque operation ID uses 1–256 exact UTF-8 bytes. The prior unauthorized stable-filename restriction on the operation ID is withdrawn. All 18 cases reproduce. |

G-028–G-030 and G-032–G-033 are faithfully reflected in the revised domains. G-031 faithfully
fixes stage precedence, but does not determine the within-stage traversal chosen by SER-008.
SER-009 correctly separates the crate's key-order defect from Mneme's own integer restriction.
Its in-domain number examples are repaired. No unrelated fidelity rows are reopened.

## Own executions

All scratch files are under `.tmp/work/codex/wp01-contract-review-2/`; the independently authored
drivers are `.tmp/work/codex/wp01-round2.py` and `wp01-round2-crosscheck.py`. These are feasibility
and oracle probes, not production implementations. CPython 3.12.8 was invoked directly from
`.tmp/cache/venvs/mneme-process-codex-r1/Scripts/python.exe`; the damaged system Python was not
used. Cargo home and target were explicitly project-local; Cargo ran offline and locked.

| Execution | Result | Evidence |
|---|---|---|
| Seven DRAFT scenario files, independently derived | 120/120 expectations match | `python-results.json`, `python-summary.log` |
| Canonical bytes / hashes | 13/13 positive byte strings and SHA-256 digests match; 18/18 rejection results match | same |
| Versions / IDs | 12/12 version results, including argument `a` in the last fixture; 16/16 stable-ID results | same |
| Timestamp seam | 16 accepted and 20 rejected cases match strict ASCII grammar, calendar and UTC-range validation | same |
| Operation identity | 13 validation and 5 comparison cases match exact UTF-8 lengths and pair equality | same |
| CORE-003 | All 7 comparison cases match; equal projections use RFC 8785 bytes, not raw spelling | same |
| Independent Rust feasibility | 26 timestamp round trips: 16 accepted fixtures plus ten full-domain instants; every canonical value and all ten epoch-microsecond values agree with Python | `rust-results.jsonl`, `crosscheck.json` |
| Rust serialization challenge | 12/13 positive canonical cases match; UTF-16 ordering witness still kills unchanged serde_jcs 0.1.0 | same; `rust/Cargo.lock`, `rust/src/main.rs` |
| Mechanical checks | sources, spec, manifest, conformance and findings: 5/5 pass, with deep source verification | `mechanical.log` |

The oracle driver uses an independent source-order decoder that detects duplicate names before
map replacement, strict syntax, and unpaired escapes. It applies binary64 conversion and the
stated value checks separately. It does not call Claude's scenario generator or Mneme code.
The stage-2 traversal probe executes both candidate order and an alternative; reproducing the
candidate expectation does not supply authority for selecting it.

Reference serialization: `rfc8785` 0.1.4; hashing: Python `hashlib` and Rust `sha2` 0.10.9.
Rust dependencies: `serde_json` 1.0.151 with `float_roundtrip`, `serde_jcs` 0.1.0,
`chrono` 0.4.45. Rust's timestamp evidence uses independent library arithmetic rather than
Claude's dependency-free civil arithmetic. Grammar and range guards are still required in front
of a host parser; this is not certification of chrono's accepted input language.

The independently derived new numeric oracles are:

| JSON numeral in `v` | Canonical bytes | SHA-256 |
|---|---|---|
| `1.0000000000000001` | `{"v":1}` | `afbf9d0f3560b0fd7795e81c42a0a79ee6b6fc67e064f77826aee642cad28d91` |
| `1e-400` | `{"v":0}` | `ec4f95abcb4e2e3dbe856c3eb2f81995eacb3823d40aa2e78ed4c5e1798f664d` |
| `-1e-400` | `{"v":0}` | same digest as positive underflow |
| `5e-324` | `{"v":5e-324}` | `8a00b7e065be3a20529e22853424bb565596997d86ddd6c27f9aff1b5c2222f8` |

The authoritative RFC [8785 §3.2.2.3 and §3.2.3](https://www.rfc-editor.org/rfc/rfc8785.html#section-3.2.2.3)
supports binary64 serialization and UTF-16 canonical property ordering; it does not prescribe
Mneme's error-selection traversal. The timestamp grammar was also checked against
[RFC 3339 §5.6](https://www.rfc-editor.org/rfc/rfc3339.html#section-5.6), with the Owner's explicit
range, fraction, leap-second and letter-case decisions taking precedence for Mneme.

The signed timestamp endpoints independently reproduced are −62135596800000000 and
253402300799999999 microseconds. Both fit signed 64-bit storage exactly. The earliest instant
and its next microsecond, a pre-Gregorian-reform date, century dates, −1 µs, epoch zero,
sample dates and the latest instant all round-trip. This supplies full-range representation
evidence without claiming exhaustive enumeration of every microsecond.

## Blocking findings

### WP01-CR-005 — Within-stage traversal selects observable errors without an Owner choice

- **Classification:** `REQUIREMENT_UNCERTAIN`.
- **Severity:** high; **blocking:** WP-01 contract checkpoint / SER-008.
- **Path:** C; **owner_decision_required:** true; **status:** OPEN.
- **Pinned evidence:** docs candidate `spec/serialization.md:131–136,150–152`;
  verbatim governance G-031, lines 222–234; code candidate
  `conformance/core/portable-value-domain-rejections.yaml` (stage-2 ordering case), and
  `conformance/core/version-integer-edition-ordering.yaml` (argument-order oracle).
- **Executed witnesses:** `python-results.json`, `witnesses` entries for stage 2 and stage 3.

G-031 requires a shared deterministic traversal but does not choose one. SER-008 chooses
depth-first pre-order, canonical UTF-16 object order, member name before value, and declared
argument order. The author's note correctly submits this reading for review. It is not path B:
alternatives change the reported error, which G-031 makes a public cross-language outcome.

Minimal actual fixture: `{"b":9007199254740992,"a":1e400}`. Canonical-key traversal returns
`value.number_not_finite`; source/insertion-order traversal returns `value.integer_out_of_range`.
Both execute deterministic traversal after stage 1 and both obey the three-stage precedence.
The own probe reproduces both outcomes. RFC 8785 fixes serialization order for valid content,
not which invalid member Mneme reports first.

For the analogous typed-field witness, a record with `z_version: 0` and `a_timestamp: "bad"`
reports `timestamp.invalid` in canonical-key order, or `version.invalid` in declaration order.
This is an illustrative typed record in the scratch probe, not an invented production schema.
The supplied version fixture additionally makes selected argument `a` observable.

**Required action / recommendation:** route an options packet to the Owner. Have the decision
explicitly choose the within-stage rules, including primitive arguments, and state how JSON and
native seams align. Options include the submitted canonical-key traversal or source/declaration
traversal, each with its discriminating error outcomes. Do not infer ratification from serializer
ordering or a reviewer approval. Include the submitted stage-1 source-order rule in that packet
so the full traversal policy is explicit. Bind conformance only after the decision is recorded.
The feasibility matrix's claim of "no open path-C decision" must then reflect the disposition.

### WP01-CR-006 — HIST-004 assigns valid generic non-string values an earlier error that does not exist

- **Classification:** `CONTRACT_ASSURANCE_DEFECT`.
- **Severity:** medium; **blocking:** WP-01 contract checkpoint / HIST-004 error seam.
- **Path:** A, reading the explicit G-031 stages and SER-008 domain together.
- **owner_decision_required:** false; **status:** OPEN.
- **Pinned evidence:** docs candidate `spec/core.md:422–424`, versus
  `spec/serialization.md:83–91,114–128` and G-031. Current timestamp scenarios cover strings
  only, so they do not detect this contradiction.
- **Executed witnesses:** `python-results.json`, five `nonstring timestamp` entries.

The error-stage paragraph says a timestamp value "that is not a string at all, or that fails the
generic value domain, reports that earlier error instead." But `null`, `true`, `7`, `[]` and `{}`
are valid generic JSON values. Decoding succeeds, and the stage-2 probe returns no error for each.
They fail only the timestamp's typed string requirement, so the stage-3 probe returns
`timestamp.invalid` for each. There is no earlier error to report.

**Required action / recommendation:** distinguish a valid generic value of the wrong timestamp
type (`timestamp.invalid`, stage 3) from an actual structural/value failure (its stage-1/2 error).
Add non-string timestamp controls, plus an earlier-domain-error control, to make the distinction
executable. This repairs fidelity to the already-decided stages; it does not require a new Owner
acceptance or type choice.

## Review limits and next step

There is no production implementation to certify at this checkpoint. Successful oracle derivation
and mechanical checks do not resolve the two contract blockers. Close the ordering authority gap
and the timestamp seam contradiction before implementation. Previously verified, unrelated rows
remain undisturbed; this review does not request another whole-layer review or changes to WP-P01.
