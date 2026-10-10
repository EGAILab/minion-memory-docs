# Minion-Memory — Coordination state

**Status:** PROPOSED (WP-00), pending independent review.
**Adapted from:** Minion-Agent `process/coordination-state.md` @ `8744bd0` (schema v2 "lean current
state", §10–§10.3 transitions, §13.5–§13.6 load boundary).
**Key adaptation:** Minion-Agent stores current state in a GitHub issue body and candidates in PRs.
Minion-Memory has **no authorized remotes** (Owner kickoff §11, §29). Current state therefore lives
in a versioned file in this repository, and candidates are exact local commits.

## 1. Principle

Current state (what WP is active, which exact candidate, which open findings, who acts next, what
exact action) is separate from history (reviews, rejected candidates, witnesses, decisions).

- **Current state:** `process/state/<WP-ID>.yaml` — one file per work package, lean (§3).
- **History/evidence:** `assurance/**` records and git history. A later record never silently
  supersedes a stale state file; the state file is updated in the same pass that changes it.
- **Status of requirements** (NOT_IMPLEMENTED … CERTIFIED): `process/certification-registry.yaml`,
  never prose in `spec/**` or the manifest (adopting Minion-Agent's certification-registry design
  from day one).

## 2. Repositories, branches and candidates

| Object | Minion-Agent | Minion-Memory |
|---|---|---|
| Control state | GitHub issue body | `minion-memory-docs/process/state/<WP>.yaml` |
| Candidate | PR head SHA | exact local commit SHA on a short-lived branch (`wpNN/<purpose>`) |
| Accepted milestone | default branch | `main` in each repo, advanced only by fast-forward to an independently approved SHA, under a recorded acceptance authority (§6) |
| Remote reachability | `git ls-remote` / GitHub API | `git cat-file -e <sha>^{commit}` in the named local repo, and reachable from the named branch |

`main` is never an ordinary work branch. Until a WP's first approval, `main` may be unborn.

**Self-reference rule.** A state file cannot contain the SHA of the commit that contains it. So:

1. the author commits the reviewed content → docs candidate `D`;
2. the author then commits one or more **state-only descendants** of `D` on the same ref (a
   linear chain `D → S1 → … → Sn`). **Every** commit in `D..ref` — checked per commit, not only
   on the endpoint diff — touches only `process/state/**`, `process/handoffs/**` (hand-off
   prompts and gate results run at the exact candidate) and, when a transition changes registry
   status, `process/certification-registry.yaml`;
3. the state file at the ref head names `D` (never an `Si`) as the docs candidate.

A reviewer verifies, for each commit `c` in `git rev-list D..<ref>`, that
`git diff-tree --no-commit-id --name-only -r -m c` ⊆ the state-only paths before trusting the
head. A content change followed by its exact revert therefore fails even though the endpoint
diff is empty. `mneme-process check state` enforces this per commit (WP00-CR-011).

Content that must follow a candidate (e.g. an independent review record) is **not** a
state-only commit: it becomes part of the next content candidate.

**After acceptance (WP-P01).** Once a WP is `CLOSED`, its candidates are protected by acceptance
instead: each candidate SHA must be an ancestor of `main` (machine-checked), its state names
`ref: main`, and the state-only descendant rule no longer applies to it. Post-acceptance record
commits (the approving review record, governance records, the closing state) may therefore follow
the accepted candidate; they reach `main` with the next accepted candidate that contains them.

## 3. State file shape (schema v2, adapted)

```yaml
workflow:
  schema_version: 2
  work_package: WP-00
  title: "Project / process / authority / contract bootstrap"
  layer: "00"
  status: SCOPING
  requirements: []                   # explicit [] = process/scoping-only WP
  current_candidate:
    code: {repo: minion-memory, ref: wp00/bootstrap, sha: "<40-hex>"}
    docs: {repo: minion-memory-docs, ref: wp00/bootstrap, sha: "<40-hex>"}
  authority:
    source_bundle: {id: mneme-v2.3-dual-profile, manifest: reference/mneme-v2.3-source-bundle.yaml}
    process_reference: {minion_agent_docs: "<40-hex>", minion_agent: "<40-hex>"}
  dependencies: {}                   # name -> {relation: blocked_by|independent_of|shares_artifact, status}
  open_findings: [NF-007]            # IDs only; details in assurance/findings/
  provisionally_closed: []
  convergence: null
  scoping_review: null               # {outcome: APPROVED|REJECTED, verdict, source} once reviewed
  governance_source: null
  deferred_trigger: null
  quarantine: {derived_from_quarantined_artifact: false}
  next_owner: Codex                  # Claude | Codex | Owner | null
  next_action: "<one concrete action>"
  updated_by: Claude
  updated_reason: "<one line>"
  history:
    assurance_index: plans/WP-00.md
```

Rules (validated by `mneme-process check state` and `state validate`):

- `status` ∈ SCOPING, CONTRACT_DRAFT, CONTRACT_REVIEW, PYTHON_IMPLEMENTATION, IMPLEMENTATION_REVIEW,
  REMEDIATION, CONTRACT_CONVERGENCE, FINAL_CONTRACT_REVIEW, RUST_IMPLEMENTATION, CLOSURE_REVIEW,
  WAITING_FOR_TRIGGER, CLOSED, INCIDENT, INVALID_UNAUTHORIZED, BLOCKED_FOR_OWNER.
- Active states require non-empty string `next_owner` ∈ {Claude, Codex, Owner} and `next_action`.
- `BLOCKED_FOR_OWNER` requires `next_owner: Owner`.
- `WAITING_FOR_TRIGGER` requires `deferred_trigger` and null `next_owner`/`next_action`.
- `CONTRACT_CONVERGENCE` requires `convergence.episode` and ≥1 `convergence.open_findings`.
- `INCIDENT` / `INVALID_UNAUTHORIZED` authorize nothing (no hand-off, review, acceptance).
- SHAs are 40 lowercase hex. `requirements`, `open_findings`, `provisionally_closed` are lists of IDs
  (container shape validated before elements).
- `CLOSED` requires no open findings, the exact accepted pair recorded (`current_candidate.code`
  and `.docs` both present with 40-hex SHAs — absent, empty, null or partial records fail closed,
  WPP01-CR-002), and every candidate SHA reachable from `main` (accepted).
  A scoping/process-only WP (`requirements: []`) additionally requires `scoping_review.outcome:
  APPROVED` (exact token; `approved`, `NOT APPROVED`, `CHANGES_REQUIRED`, null are refused) with
  non-empty `verdict`/`source`. A product WP additionally requires its registry entry to be
  `cross_language: CERTIFIED_CLOSED`. All three are machine-checked (WP00-CR-003); the validator
  checks recorded evidence, while the independence of the approving review remains the agent's
  verification duty.
- A quarantined candidate (`quarantine.derived_from_quarantined_artifact: true`) authorizes **no**
  agent action: `next_owner` must be `Owner` or null (WP00-CR-004).
- Lean budget: a state file SHOULD stay under 8,000 characters; history-shaped keys (`reviews`,
  `remediations`, `review_history`, `history_log`) draw a warning.
- The file is loaded through the YAML-1.2-core boundary (`process/hazard-families.md` H6): no
  aliases, tags, duplicate keys or YAML-1.1-only scalars; JSON-domain values; depth ≤ 64.

## 4. Commit rule (replaces the issue-body round-trip)

A state transition is committed only when, in order:

1. the intended state is constructed and passes `mneme-process state validate`;
2. the transition `FROM → TO` is legal (§5);
3. the state-only commit `S` is created (§2);
4. the state is re-read **from the git object** (`git show S:process/state/<WP>.yaml`), parsed with
   the same loader, and is semantically equal to the intended object — mechanically:
   `mneme-process state roundtrip --docs <docs> --revision S` (raw git bytes, explicit UTF-8,
   CRLF/LF differences ignored as a checkout artifact, any other byte difference fails; the
   committed and working state **inventories** must match first — a committed state missing from
   the working tree or an uncommitted extra state fails, while a committed deletion is legitimate,
   WPP01-CR-001);
5. only then is any dependent action taken (hand-off, review start, acceptance, closure).

A failed step 4 is a FAILED STATE COMMIT: no dependent action; repair by a new commit from the last
valid state plus the intended delta, then re-verify.

## 5. Legal transitions

Adopted unchanged from Minion-Agent §10, §10.1, §10.2, §10.3:

```text
SCOPING              -> CONTRACT_DRAFT | WAITING_FOR_TRIGGER | BLOCKED_FOR_OWNER | CLOSED (scoping-only, approved, accepted)
CONTRACT_DRAFT       -> CONTRACT_REVIEW
CONTRACT_REVIEW      -> PYTHON_IMPLEMENTATION | CONTRACT_DRAFT | CONTRACT_CONVERGENCE | FINAL_CONTRACT_REVIEW
PYTHON_IMPLEMENTATION-> IMPLEMENTATION_REVIEW
IMPLEMENTATION_REVIEW-> RUST_IMPLEMENTATION (clean first review; acceptance is part of the transition)
                      | FINAL_CONTRACT_REVIEW (this instance re-reviewed a remediated candidate)
                      | REMEDIATION | CONTRACT_CONVERGENCE
REMEDIATION          -> IMPLEMENTATION_REVIEW | CONTRACT_CONVERGENCE
CONTRACT_CONVERGENCE -> FINAL_CONTRACT_REVIEW (all episode findings provisionally closed)
FINAL_CONTRACT_REVIEW-> RUST_IMPLEMENTATION | REMEDIATION | CONTRACT_CONVERGENCE
                      | PYTHON_IMPLEMENTATION (contract-phase final review approved)
                      | CONTRACT_DRAFT (contract-phase final review rejected)
                      | CLOSED (process-only WP, requirements: [])
RUST_IMPLEMENTATION  -> CLOSURE_REVIEW
CLOSURE_REVIEW       -> CLOSED | RUST_IMPLEMENTATION
WAITING_FOR_TRIGGER  -> SCOPING (trigger fired)
any active state     -> BLOCKED_FOR_OWNER
BLOCKED_FOR_OWNER    -> the specifically authorized continuation (recorded governance_source)
```

Kept illegal (with the legal route): `CONTRACT_REVIEW ↔ REMEDIATION` (contract findings are fixed in
`CONTRACT_DRAFT`); `RUST_IMPLEMENTATION → IMPLEMENTATION_REVIEW` and `IMPLEMENTATION_REVIEW → CLOSED`
(Rust review is `CLOSURE_REVIEW`); `BLOCKED` is not a status. `mneme-process` encodes this table in
`transitions.py`.

## 6. Governance source

Required whenever a governed choice is in force. A recommendation, silence, an agent's own
assertion, or a "(Recommended)" option label is never a governance source. Valid sources: an Owner
message durably recorded in `reference/governance/`, or an existing project governance record
naming and scoping the decision.

```yaml
governance_source:
  artifact: reference/governance/2026-10-09-owner-wp00-kickoff.md
  decision: "<exact decision>"
  scope: ["<WP / requirement / transition>"]
```

**Approval and acceptance are separate acts (WP00-CR-001).** An independent review approves an
exact candidate; it never grants authority to accept it. Accepting a candidate onto `main` (and
any routine transition that depends on acceptance) requires a recorded acceptance authority:
either an explicit Owner decision for that candidate, or a standing delegation the Owner has
recorded in `reference/governance/`. No such delegation exists in Minion-Memory (Minion-Agent's
`minion-agent#75` does not transfer; NF-020). Until one is recorded, Claude does not advance `main`;
after an approval it records the approval and routes acceptance to the Owner (`next_owner: Owner`
with the exact SHAs to accept).
