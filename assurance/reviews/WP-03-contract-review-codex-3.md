# WP-03 contract review 3 — Codex

Date: 2026-10-11. Independent reviewer / Rust owner: Codex.

## Verdict

**APPROVED** for docs `b514c16d2822f610a93d71368606f89ff91a4745` /
code `619540ae8ef15d7e8f639fd2c10e86c036888124`.

**WP03-CR-005: CLOSED.** No open blocking findings. WP03-CR-001..004 remain closed; the
targeted changes introduce no evidence contradicting those closures. This approves the exact
contract/corpus candidate, not acceptance onto main or any future implementation.

## Custody and scope

Followed `process/handoffs/WP-03-codex-contract-review-3.md` at control head `2ddca1d1`.
New branch `review/wp03-contract-3` starts there in `review-worktrees/docs-wp03-review-3`;
code is a separate detached exact-SHA checkout in `review-worktrees/code-wp03-review-3`.
Only this record is committed. Candidate, production, shared state, registry, source bundle
and other worktrees were not edited. Every shell first sourced the project environment; scratch,
managed Python, Cargo home/cache/target and worktrees remain inside the project.

Read G-075 verbatim, the response addition, complete changed HIST-007/PROJ-001 text and
both corpus files. Compared the exact revision-2 and revision-3 candidates. The code delta is
the five new lineage controls and description updates in the two projection scenarios; no
library, runner, manifest or earlier-layer corpus change. The normative docs delta is the
artifact-target domain, its early validation and presentation order. Review/control records
also advance as expected. The earlier uncertainty was decided by the Owner, not inferred from
the author response.

## WP03-CR-005 resolution and authority fidelity

G-075 expressly chooses two closed, mutually exclusive immutable target identities:
`{stable_id, artifact_version}` and `{content_hash}`. HIST-007 transcribes both, retains
CORE-001/CORE-002 validation for versioned targets and requires the exact CORE-011 hash spelling
for hash targets: 64 lowercase ASCII hexadecimal characters.

Bare stable IDs, absent editions, combined forms, neither form, unknown members and invalid
hashes are early `lineage.invalid`, argument `relations`, subject to the established generic
stages running first. No absent edition is inferred, and invalid hashes are not case-folded or
rewritten. Only `derived_from` can carry either artifact form. Layer 03 has no artifact-resolver
argument; both forms remain in `relations` and `unresolved_derivations` and never affect heads.
This is faithful to G-075's unresolved behavior when no explicit resolver is available.

The revised total presentation order is available record positions, unavailable record IDs,
versioned artifact `(stable_id, artifact_version)` pairs, then content hashes, after the
common from-position and relation-kind keys. This losslessly renders the decided target
variants. It neither changes reference identity nor chooses a preferred head and needs no
additional path-C decision. Artifact versions compare numerically, not lexically.

## Independent executed evidence

Executed `.tmp/work/codex/wp03-oracles-3.py` on project-local CPython 3.12.8. It extends my own
round-2 fixture-domain derivation only for the newly decided target union and its total sort.
It imports YAML and standard-library helpers, not either production implementation. No Layer 03
implementation is proposed or exercised by this derivation.

**54/54 complete expectations match the literal contract.** The earlier 49 named cases retain
their complete expectations. Compared normalized retained envelopes, through-boundaries,
duplicate metadata, relations, unresolved derivations, head/group membership and error
code/argument/position. The supplied hashes are reference identities, not claimed hashes of a
corpus payload: validating their canonical spelling does not require inventing content to hash.

New lineage controls and independently derived oracles:

| Step | Input distinction | Derived outcome |
|---|---|---|
| 17 | Hash-only artifact, 63 `a` characters followed by `b` | Preserve the exact typed relation in relations and unresolved_derivations; all five heads unchanged, no interpretation group |
| 18 | Bare stable_id | lineage.invalid, argument relations |
| 19 | Versioned identity plus content_hash in the same object | lineage.invalid, argument relations |
| 20 | Uppercase hash | lineage.invalid, argument relations; no case normalization |
| 21 | artifact_version 0 | lineage.invalid, argument relations |

Additional executed target neighborhoods: **5 valid and 22 invalid**, all meeting the explicit
rules. Valid cases include zero-filled and mixed-digit hashes, edition 1, the maximum admitted
edition 2^53−1 and its normalized integral-float alias. Invalid cases cover neither identity,
missing fields, null/bool/zero/fractional editions, extra fields, combined forms, hash lengths
0/63/65, uppercase/non-hex/fullwidth text, trailing newline, and non-string generic hash values.
Generic-stage failures such as non-finite values are not mislabeled by these typed-only probes.

Executed **100 deterministic mixed-target permutations** containing an available record,
two unavailable records, editions 2 and 10, and two different content hashes. Every permutation
produces the same complete result, including the unresolved subset order. The old version-only
shape predicate rejects the valid hash-only witness while the revised predicate accepts it:
the intended old-rule negative control is discriminated. This is a contract-model control,
not a claimed production mutation score.

Evidence: `.tmp/work/codex/wp03-oracles-3.json`, SHA-256
`0ccab261dc8c1649880524c50563a691b0dc91c8c0031b315323b889810c7e3f`.

## Direct regressions and Rust readiness

The complete 54-case derivation rechecks the previously closed occurrence, stage, graph-family
and direct-membership rules. No prior expectation changed. Existing typed record targets remain
distinct from both external-artifact identities. Duplicate normalized relations retain typed
identity, and hash targets remain external rather than being inserted into the available-record
graph merely because a record has the same string spelling.

Rust can represent the target union with explicit record/versioned-artifact/hash variants after
generic and shape validation, preserving exact ASCII hash strings. Existing iterative graph and
canonical-envelope comparison guidance remains valid. No new dependency, narrowing of the value
domain, implicit edition or host-deserializer error selection is needed.

Executed the independent process tool against these checkouts with `--deep-sources`:
**8/8 PASS**. Executed Windows Rust `cargo test --locked --offline --test conformance`:
**5/5 PASS**, including canonical corpus and DRAFT/promotion controls. This verifies runner
integration for the new DRAFT inputs; it does not claim they are implemented. The unchanged
production modules' full regression suite passed in round 2 and was not redundantly rerun.
No POSIX or Layer 03 production test execution is claimed in this targeted contract review.

The earlier non-blocking assurance suggestions remain suggestions; no new blocking finding or
unrecorded semantic choice was found within the revised target domain.
