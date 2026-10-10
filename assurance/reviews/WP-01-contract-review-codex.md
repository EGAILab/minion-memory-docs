# WP-01 Layer 01 contract review — Codex

## Verdict and objects

**CHANGES_REQUIRED** for docs `bbb61195713ddc4ad3819dfd0844ec5a6f5c6f9c` paired with
code `ea61ffb19784a5cba2bbdacfa35f1e240fe0d412`.

Reviewed separate detached checkouts of those exact SHAs, not Claude's authoring worktrees.
This record's parent is docs state commit `bb9c09c282c2a682b3b797a5c7b7bd3b30a3b567`, on
`review/wp01-contract-1`. Authority: the handoff, G-019, the verbatim G-012–G-026 decisions,
the bundle authority chain and `process/finding-taxonomy.md` §1.1. Review is independent of
Claude's implementation/probes. It neither accepts the pair onto main nor authorizes Python
implementation against this unrepaired checkpoint.

The supplied DRAFT expectations reproduce correctly. The blockers are contract completeness
and authority gaps, not a failed supplied hash or a product implementation defect.

## Executed evidence

| Own execution | Result | Local evidence under `.tmp/work/codex/wp01-contract-review/` |
|---|---|---|
| All five DRAFT scenarios, independently derived | 54/54 expectations match: 9 canonical bytes/hashes, 9 domain rejections, 9 version cases, 16 ID cases, 11 timestamp cases | `python-results.json` |
| RFC 8785 reference | `rfc8785` 0.1.4 on managed CPython 3.12.8; all nine UTF-8 byte strings and SHA-256 digests independently recomputed | `python-results.json` |
| Independent Rust third-party probe | Reproduces UTF-16 ordering divergence; eight other positive canonical cases match; duplicate keys are lost by default parsing | `rust-results.log`, `rust/Cargo.lock`, `rust/src/main.rs` |
| Numeric/time neighborhood probes | Executed parser overflow, underflow, subnormal, rounding, decoded duplicate keys, lowercase time input, year zero and UTC year-boundary cases | Python JSON and Rust log above |
| Mechanical candidate checks | sources, spec, manifest, conformance and findings: 5/5 pass with deep source verification | `mechanical.log` |

The Python probe derives policy from decisions and computes bytes directly with the reference
library; it does not call a Mneme implementation or the candidate generator. Its timestamp
matcher uses the strict uppercase interpretation needed by the present fixtures. Those fixture
passes do not decide the missing grammar alternatives in CR-001. Host-parser neighborhood
results are explicitly observations, not adopted contract oracles.

Rust toolchain: rustc 1.97.1 / cargo 1.97.1; locked serde_json 1.0.151 with `float_roundtrip`,
serde_jcs 0.1.0, sha2 0.10.9 and chrono 0.4.45. The Rust program is a scratch third-party
feasibility probe, not a Minion-Memory implementation.

## Blocking findings

### WP01-CR-001 — Timestamp input grammar and boundary policy remain unresolved

- **Classification:** `REQUIREMENT_UNCERTAIN`.
- **Severity:** high; **blocking:** WP-01 / HIST-004 / NF-015, NF-025.
- **Path:** C where the contract elects an input restriction/option not determined by authority;
  an explicit authority reading may settle individual subcases as path A.
- **owner_decision_required:** true.
- **Evidence:** candidate docs `spec/core.md:340–365`, governance G-022/G-026; candidate code
  `conformance/core/timestamp-seam-normalization.yaml`; own time probes.

The text promises that the shared contract defines the accepted grammar, but supplies neither
a full grammar nor complete boundary rules. G-022 fixes canonical output, not every input
spelling. G-026 says APIs **MAY** accept the described RFC 3339 forms; the draft says APIs
accept them, without explaining whether that is a compulsory shared capability or an option.
RFC 3339 §5.6 permits lowercase `t`/`z` and permits applications to impose an uppercase limit.
It does not justify silently inheriting either host parser's limits.

Discriminating witnesses:

| Input | Observed host behavior | Contract question |
|---|---|---|
| `2026-10-10t05:30:00z` | chrono accepts and emits uppercase UTC; Python `fromisoformat` rejects | Does the public input grammar accept RFC lowercase forms or impose an explicit uppercase restriction? |
| `0000-01-01T00:00:00Z` | chrono accepts; Python datetime rejects | What is the supported calendar/year domain, independently of host limitations? |
| `0001-01-01T00:00:00+00:01` | chrono emits `0000-12-31T23:59:00.000000Z`; Python normalization fails | Is that canonical year admitted? |
| `9999-12-31T23:59:59-00:01` | chrono emits a year-10000 form; Python normalization overflows | What documented rejection handles a valid input whose UTC result cannot have the required four-digit output year? |

These are not implementation defects: no Mneme timestamp implementation exists. The current
eleven cases do not discriminate the alternatives. The space-separator rejection is compatible
with choosing the strict RFC grammar; it does not itself specify lowercase or range behavior.

**Resolution:** write the accepted grammar, valid calendar/range and normalized-output
postconditions, including numeric-offset bounds, case, empty fraction and output overflow.
Show which rules follow by authority reading. A host-driven narrowing, choosing among permitted
acceptance options, or widening canonical years is path C and must go to the Owner. My
recommendation is to preserve the referenced RFC input domain where authority settles it,
normalize only to G-022's canonical output, and reject unrepresentable output rather than invent
a wider spelling; present any remaining choices as an options packet. Add boundary scenarios
only after resolution. I have selected no new acceptance rule.

### WP01-CR-002 — H4 feasibility does not establish lossless time representation over the domain

- **Classification:** `CONTRACT_ASSURANCE_DEFECT`.
- **Severity:** medium; **blocking:** WP-01 / HIST-004 feasibility evidence.
- **Path:** B, representation evidence; **owner_decision_required:** false.
- **Escalation condition:** restricting accepted dates to fit a convenient representation is
  path C, owner_decision_required true, handled with CR-001.
- **Evidence:** candidate `assurance/layers/01-feasibility-matrix.md` §1 timestamp row and H4
  AUDITED claim, G-022, own year-boundary probes.

The timestamp row says lossless across all and supports that with safe-integer microseconds
covering approximately ±285 years. No such timestamp range was selected. A canonical
`9999-12-31T23:59:59.000000Z` corresponds to **253402300799000000** epoch microseconds in
the Rust probe: above the generic JSON safe-integer bound but within i64. The Python datetime
and Rust time types also disagree at year zero and normalization boundaries. The row has not
proved the advertised whole-domain capability.

**Resolution:** audit the resolved full timestamp domain, distinguish internal i64/time
representation from portable JSON numbers, and demonstrate exact canonical round trips at
both boundaries and fractional precision. G-022 permits internal microseconds only with
lossless round trip; it does not grant a ±285-year input restriction. Canonical strings and
an appropriate internal representation are feasible; this finding requests evidence and an
accurate matrix, not a narrower domain or a change of time semantics.

### WP01-CR-003 — Rejection vocabulary and seam ownership are incomplete

- **Classification:** `CONTRACT_ASSURANCE_DEFECT`.
- **Severity:** high; **blocking:** WP-01 / SER-008, SER-009 and public primitive errors.
- **Path:** A/B for transcribing existing rejection semantics and their representation;
  **owner_decision_required:** false.
- **Escalation condition:** changing acceptance/rounding semantics or choosing an observable
  multi-error precedence not derived from authority requires path C, owner_decision_required true.
- **Evidence:** candidate `spec/serialization.md:80–119`, five DRAFT scenarios, feasibility
  §2's “decode JSON text ... must be specified”, own numeric/parser probes.

The proposed codes cover the supplied examples, not the entire already-rejected domain:

- `1e400` is valid JSON number syntax. Python decodes it to infinity; serde_json rejects it
  as a number-range error. `Infinity` is invalid JSON syntax and has `value.invalid_json`,
  but no shared mapping covers valid-syntax binary64 overflow or a native API NaN/Infinity.
- Native API values can have non-string keys or non-JSON container/object kinds. SER-008
  rejects them but specifies no stable code/mapping. A JSON-text-only fixture cannot test that seam.
- serde_json rejects a lone surrogate during decoding, before constructing a String. Its
  generic parse error must still map to the scenario's `value.lone_surrogate`, rather than
  accidentally becoming `value.invalid_json`. Duplicate decoded member names must be checked
  before a map discards them (`{"a":1,"\u0061":2}` is rejected by my independent probe).
- The text does not make the primitive boundary/error map explicit for JSON decoding,
  native-value validation and typed ID/version/timestamp validation. For example, an oversized
  version has `version.invalid` in its typed scenario, but `value.integer_out_of_range` as a
  generic payload. A common prevalidator must not unintentionally select the wrong public error.

**Resolution:** provide a shared boundary table and exhaustive mapping for required rejection
categories, including native inputs and valid-JSON numeric overflow; specify error observations
for multiply invalid inputs, or explicitly the permitted alternatives. Define decode/normalize/
validate order before canonical bytes and hashing. RFC binary64 rounding can be documented by
authority reading: my probes round `1.0000000000000001` to 1, underflow `1e-400` to 0, retain
`5e-324`, and round `9007199254740991.5` to an out-of-bound integral value that G-025 rejects.
Do not infer acceptance, precision or error precedence from a host parser. Code names encoding
already-fixed outcomes can be representation mechanics; new observable policies cannot.

### WP01-CR-004 — The Layer-01 conflict scenario is still an undefined placeholder

- **Classification:** `CONTRACT_ASSURANCE_DEFECT`.
- **Severity:** medium; **blocking:** WP-01 / CORE-003, NF-012 assurance.
- **Path:** A/B; **owner_decision_required:** false.
- **Evidence:** docs `plans/WP-01-proposal.md` deliverable 3; code manifest CORE-003 row;
  `conformance/core/identity-same-version-different-content-conflicts.yaml` at the exact code SHA.

The plan requires promotion to DRAFT, but CORE-003's only linked scenario remains PLACEHOLDER
with `existing_artifact`, `offer_artifact` and outcome all `TO_BE_DEFINED_IN_LAYER_01`.
It still describes normalization/conflict observation as undefined. Thus the new core-wide
G-021 rule is not discriminated, and the operation/conflict vocabulary cannot be independently
implemented from this scenario. Passing hashes alone does not test a consumer's equality rule.

**Resolution:** define a Layer-01 pure comparison scenario using an explicit supplied
semantic-content projection: same ID/version with different bytes conflicts; canonical-equivalent
numeric spellings are equal; schema/model-version metadata alone does not invoke this rule.
Use the already-decided G-021 scope and a defined visible conflict observation. No database
or history implementation is requested. Layer-04 commit/idempotency fixtures may remain deferred,
but the Layer-01 comparison promise must be concrete. If the WP is intentionally dropping this
deliverable, record the scope decision rather than retaining an implicit placeholder.

## Fidelity, findings and Rust feasibility

| Decision / existing finding | Review conclusion |
|---|---|
| G-012, NF-011 | Positive integer edition and numeric ordering are faithful; the 2.0 positive follows G-023 after normalization. Booleans remain a distinct domain kind. |
| G-013, NF-014 | Per-store, cross-profile uniqueness and conflicting retry/no-write outcomes are transcribed. Layer-04 persistence behavior is correctly deferred; see question Q1 about identity scope. |
| G-014, NF-013 | Nine byte/hash fixtures verified; UTF-16 sorting and raw text/binary byte hashing are stated. |
| G-015/016/017, NF-019 | Scalar strings, JSON containers, finite binary64, safe integers and negative-zero normalization are transcribed; seam/error completion is CR-003. |
| G-020, NF-010 | All 16 ID fixtures follow lowercase ASCII, 1–128 bytes, no trailing dot and reserved basename exclusions; no case folding. Path projection is correctly not a second identity. |
| G-021, NF-012 | Immutable semantic revisions and per-type projections are scoped faithfully; scenario completion is CR-004. |
| G-022/026, NF-015/025 | Present eleven cases normalize correctly; complete input/range authority and feasibility are CR-001/002. |
| G-023/025, NF-022/024 | One numeric kind and post-normalization whole-number bound are faithful. Native int/float tags cannot determine validity or equality. |
| NF-023 | Nonblocking environment hardening remains accurate: environment scripts do not set CARGO_HOME. I set it explicitly for the probe. |

Rust can represent the adopted generic numeric domain losslessly with checked safe integers
and f64, or one normalized binary64 representation: every admitted integral value is exact in
binary64. `serde_json::Number` is a container, not the semantic contract: parser settings,
integrality checks and normalization are required. Its ordinary integer/float distinctions must
not leak into equality. Version validation must accept normalized whole floats while rejecting
booleans, zero, negatives and fractions.

For the supplied UTF-16 case, my serde_jcs probe emits the `｡` key before `😀` and hashes to
`f50c2f946813c36e29e1a1ee426edceeb0495f67f085bac5bd40937d0c991099`; reference/fixture order
hashes to `fd1c2455e650903b956c6ce4788b1766e7b4510c58b7ea25b563c79ed7fd122c`.
Thus serde_jcs 0.1.0 cannot be adopted as the canonicalizer unchanged. A conformant path needs
recursive ordering by decoded UTF-16 units, correct string escaping, ECMAScript number formatting,
finite/scalar/domain validation and duplicate-aware decoding before map construction. Rust's
UTF-16 iterators support the required ordering; language-native key sorting does not.
These requirements follow [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785).

Evidence nuance: emitting **2^53 alone** is not proof of RFC nonconformance; RFC 8785 Appendix B
includes that binary64 value. It is forbidden by **Mneme's** G-025 domain. The reference
library's stricter Python-int adapter is not a universal definition of RFC numeric acceptance.
The key-order witness independently establishes the crate defect. The feasibility text should
distinguish a bad serializer from missing Mneme seam validation.

Timestamp normalization is feasible with checked calendar arithmetic and a time/i64 type over
the resolved domain. chrono's parser alone is not the grammar or the canonical emitter: its
extended year output can violate the mandated four-digit form. Python datetime alone also
cannot supply the full boundary contract. The grammar alternatives are grounded in
[RFC 3339 §5.6](https://www.rfc-editor.org/rfc/rfc3339#section-5.6), not in either host.

## Questions and nonblocking corrections

- **Q1:** CORE-012 says operation identity follows CORE-001's lexical domain but also accepts
  an equivalent durable source identity; its note still calls NF-010 open. G-013 determines
  uniqueness/retry outcomes, not how external source identities map to this token. Explain
  whether the public value is always a Mneme stable ID and external identifiers are separate,
  or show the authority reading that unifies them. Bundle R04 §32 and R05 §6 require durable
  operation/source idempotency but do not supply that mapping. This is a question, not an
  evidenced acceptance defect. Any new identity equivalence/restriction would be path C.
- SER-009's `1e21 -> 1e+21` example describes raw JCS but is no longer a valid Mneme value.
  Label it as outside the adopted domain or use an accepted number. The rejection fixture is correct.
- Update feasibility/probe conclusions that still use 1e21 as a positive Mneme example, stale
  CONTRACT_DRAFT/not-yet-handed status, old governance ranges and CORE-012's “still open” note.
  Original probe transcripts should remain historical evidence, with current interpretation added.
- Findings may remain OPEN pending review as the governance record says; I am not demanding
  premature closure. Update their resolution/trace links when the repaired checkpoint is agreed.

## Evidence custody and changes

Source citations above are pinned by the exact pair; governance decision text is inside the
docs candidate. The deep source check verifies the bundle inventory hashes. Evidence/harness
fingerprints are in `.tmp/work/codex/wp01-contract-review/evidence-manifest.json`, SHA-256
`24141bf3a0635f667ff6e23b092ed7b29855f233c64765e9ee8a15f2a1d17bbd`.
The independent probe is `.tmp/work/codex/wp01-review-probes.py`.

Every shell first dot-sourced the project environment. Python uses a project-local managed
3.12.8 runtime, not the damaged system Python; rfc8785 was installed only into the Codex project
venv. Cargo registry/downloads and targets explicitly use project `.tmp/cache` paths. All
scratch artifacts and detached/review worktrees are inside the project on E:. No runtime/bin
installation on C: or changes to user/system environment settings were made.

Only this review record is committed. Exact candidate checkouts and main working trees remain
clean; Claude's WP-01 authoring worktrees, production modules and the source bundle were not
edited. The next step is Claude's independent consumption and authority-based repair/options
handling; path-C choices cannot be resolved by copying one language's behavior.
