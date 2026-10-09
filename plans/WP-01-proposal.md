# WP-01 proposal — Core identity, version, provenance, lineage, operation identity and portable value domain

**Status:** PROPOSAL only. WP-01 does not start until the WP-00 independent review is resolved
(kickoff §34).

## Scope (Layer 01)

Requirements: CORE-001..CORE-013, SER-001..SER-004, SER-007 (manifest `layer: "01"`).
Open findings it must resolve: NF-010 (ID lexical domain), NF-011 (version domain), NF-012 (scope of
the conflict rule), NF-013 (hash algorithm + canonical bytes), NF-014 (operation identity domain and
conflicting retry), NF-015 (timestamps), NF-019 (portable value domain).

Deliverables:
1. Contract deltas in `spec/core.md` / `spec/serialization.md` that settle the findings above **from
   the sources where they speak**, and as explicit options for the Owner where they are silent and
   the choice is product semantics (expected: few — most are engineering-domain choices consistent
   with "opaque"/"versioned"/"hash").
2. Cross-language feasibility matrix (template) with executed probes on the pinned toolchain for
   H1, H2, H3 (normalization only), H4, H6, H7, H11.
3. Canonical scenarios (`conformance/core/`) promoting
   `core.identity.same-version-different-content-conflicts` from PLACEHOLDER to DRAFT and adding:
   ID round-trip/opacity, version comparison, content-hash fixtures (byte-exact, with ≥2 entries
   distinguishing plausible canonicalizations), provenance/lineage shape, operation-identity shape,
   missing-is-unknown decoding, value-domain rejection cases.
4. Python package skeleton for the public core types only after `CONTRACT_REVIEW` approval.

## Non-scope

MemoryScope (Layer 02), history envelopes and ordering (02), persistence/idempotent commit behavior
(04), any learning or agent entity, SQLite.

## Ownership and flow

`SCOPING (Claude) → CONTRACT_DRAFT (Claude) → CONTRACT_REVIEW (Codex) → PYTHON_IMPLEMENTATION
(Claude) → IMPLEMENTATION_REVIEW (Codex) → … → RUST_IMPLEMENTATION (Codex) → CLOSURE_REVIEW (Claude)`.
High-risk (value domain, hashing): contract-first checkpoint is mandatory (agent-workflow §3 step 6).

## Risks

- Hash canonicalization chosen too early constrains Knowledge package hashing (Layer 07/12): keep
  the canonical-bytes rule general, with package-specific normalization layered later.
- Python `str` lone surrogates: the contract must reject them at the seam, not let Python accept
  what Rust cannot represent.
