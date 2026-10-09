# Cross-Language Feasibility Matrix — `<WP id>`: `<title>`

**Required by:** `process/agent-workflow.md` §3 step 5, for every WP whose contract touches values,
strings, numbers, time, ordering, hashing, persistence or concurrency, before its contract
checkpoint. **Adapted from:** Minion-Agent `process/templates/cross-language-feasibility-matrix.md`
@ `8744bd0` (Pi columns replaced by authority/Python/Rust/serialized columns).

**Authority bundle:** `mneme-v2.3-dual-profile` (`reference/mneme-v2.3-source-bundle.yaml`).
**Author:** `<shared-contract owner>`. **Independent checkpoint reviewer:** `<other agent>`.
**Candidate:** docs `<sha>` / code `<sha>`. **Toolchains:** Python `<version>`, Rust `<version>`,
SQLite (Python) `<version>`, SQLite (Rust) `<version>`.

## How to fill this in

- **Silence is not an answer.** Every row ends `AUDITED` (with evidence: probe path + output),
  `NOT_APPLICABLE` (one-line reason) or `DEFERRED_WITH_REASON` (reason + trigger/owner).
- Audit the **transitive** semantic path: from the public input through validation, persistence,
  replay/decoding, projection and every serialization boundary the WP's observable surface reaches.
- Copy the member list of every touched family from `process/hazard-families.md`; do not re-derive.
- A row with "lossless across all? = NO" or "representation sufficient = NO" is a **finding**
  (`process/finding-taxonomy.md`), resolved before the checkpoint.
- Premises about libraries/engines (SQLite, YAML/JSON crates, Unicode data) are AUDITED only by an
  executed probe on the pinned toolchain, recorded with its output.

## 1. Value-domain matrix

| Observable value / field | Contract domain (spec anchor) | Python repr | Rust repr | Canonical serialization (JSON/YAML/SQLite/JSONL) | Lossless across all? | Witness needed |
|---|---|---|---|---|---|---|
| `<field>` | | | | | | |

Consider and record, per value: null vs missing vs unknown vs empty; integer width/sign; float
specials; Unicode scalar domain and normalization; length units; timestamp form and precision;
ID/version lexical domain; scope encoding.

## 2. Lower-layer capability matrix

| Required semantic operation | Owning layer | Existing reviewed seam | Expresses the contract exactly? | Python sufficient? | Rust sufficient? | Additive extension needed? | Non-additive reopen needed? |
|---|---|---|---|---|---|---|---|
| `<operation>` | | | | | | | |

A non-additive reopen of a certified layer is Owner-only → `BLOCKED_FOR_OWNER`.

## 3. Hazard checklist

| Hazard (family/member) | State | Evidence / reason |
|---|---|---|
| H1 integer width / JSON number forms / float specials | | |
| H2 scalar domain / encoding / NUL / length units / line endings | | |
| H3 normalization / case folding / collation / Unicode version | | |
| H4 timestamp form / precision / unknown / clocks | | |
| H5 map order / canonical key order / sort keys / pagination | | |
| H6 YAML 1.1 vs 1.2 / duplicate keys / null vs missing | | |
| H7 hash algorithm / canonical bytes | | |
| H8 SQLite version / isolation / crash points / idempotency / JSONL | | |
| H9 paths / traversal / case / atomic rename | | |
| H10 concurrent retry / async enrichment / cancellation | | |
| H11 ID / version / scope encoding / reference integrity | | |

## 4. Concurrency / order matrix (async or concurrent WPs)

| Operation | Start | Durable commit point | Await/abort points | Failure points | Settle | Observable ordering |
|---|---|---|---|---|---|---|
| `<op>` | | | | | | |

| Ordering guarantee | Realistic wrong implementation | Witness that kills it |
|---|---|---|
| `<guarantee>` | | |

## 5. Neighborhood expansion record

| Family | Members probed | Probe source | New rows / findings |
|---|---|---|---|

## 6. Verdict

```text
FEASIBILITY
    READY     every row AUDITED / NOT_APPLICABLE / DEFERRED_WITH_REASON; no open finding
  or
    BLOCKED   open finding(s): <IDs> (classification, owner, resolution path)
```

The independent checkpoint reviewer verifies this matrix; an incomplete matrix is a
`CONTRACT_ASSURANCE_DEFECT` against the checkpoint.
