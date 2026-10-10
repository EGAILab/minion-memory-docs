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
   linear chain `D → S1 → … → Sn`: every commit in the chain has exactly one parent, so a merge
   is refused). **Every** commit in `D..ref` — checked per commit, not only on the endpoint
   diff — touches only `process/state/**`, `process/handoffs/**` (directory prefixes; hand-off
   prompts and gate results run at the exact candidate) and, when a transition changes registry
   status, exactly the path `process/certification-registry.yaml` (look-alikes such as
   `…registry.yaml.bak` are not state-only; CE-P01-01 D10);
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
- `WAITING_FOR_TRIGGER` requires a non-blank **string** `deferred_trigger` and null
  `next_owner`/`next_action`.
- `CONTRACT_CONVERGENCE` requires a mapping `convergence` with a non-blank string `episode` and a
  non-empty list `open_findings` of finding IDs (truthy booleans, numbers or text are refused).
- `INCIDENT` / `INVALID_UNAUTHORIZED` authorize nothing (no hand-off, review, acceptance):
  `next_owner` **and** `next_action` are null.
- Operational tokens are complete ASCII tokens (CE-P01-01 D11/D12; full match, no trailing
  newline, no non-ASCII digits): `schema_version` is the integer `2` (not `2.0`, `true` or `"2"`);
  `work_package` matches `WP-[A-Z0-9]{1,8}`; SHAs are 40 lowercase hex; `requirements` elements are
  `<FAMILY>-NNN` with a declared family; `open_findings` / `provisionally_closed` elements are
  `NF-NNN` or `WP…-CR-NNN`. Container shape is validated before elements, and owner/action
  membership only after the type test, so malformed input is reported, never raised (D13).
- Optional metadata (`title`, `layer`, `authority`, `dependencies`, `history`, `governance_source`,
  `updated_by`, `updated_reason`, and `scoping_review` / `deferred_trigger` / `convergence` outside
  the status that governs them) is opaque and confers **no** authority; existing type guards
  (`updated_by` / `updated_reason` string-or-null) remain.
- **State inventory (D1–D3).** Every immediate entry of `process/state/`, in the working tree and in
  any committed tree, must be a regular file named `<WP-ID>.yaml` (literal lowercase suffix, byte
  exact). Any other entry — another name, a case variant, a nested directory, a symlink, a gitlink,
  a non-UTF-8 name — is an error naming its exact identity; it is never silently included or
  skipped. The file-aware gates (`state validate`, `check state`) require the file stem to equal
  `work_package`; the pure-object validator only checks the token, and `state roundtrip` proves
  byte/inventory equality only.
- Candidate sides are **bound to their repositories**: `code.repo` must be `minion-memory` and
  `docs.repo` must be `minion-memory-docs`; the validator resolves each side's repository from the
  side, never from the record (WPP01-CR-002).
- A candidate `ref` is a **plain local branch name** that exists as `refs/heads/<ref>` — not a SHA,
  `HEAD`, a qualified `refs/…` spelling, a range, or option-like text (otherwise a `ref` equal to
  the candidate SHA would make the state-only descendant range empty). A `CLOSED` state uses
  `ref: main` on both sides. A symbolic `refs/heads/<ref>` is refused (D5).
- **One resolution per proof (D6, D8).** Each side resolves `refs/heads/<ref>` once to a commit
  OID and uses that OID for ancestry, the descendant listing and every per-commit path listing;
  CLOSED resolves `refs/heads/main` the same way. Tags, remotes and abbreviations are never
  consulted. The candidate `sha` must itself be a commit object (an annotated tag that peels to a
  commit is refused). Each state file is read and parsed once per check (D9).
- **Hermetic Git (D7).** Every validator Git call runs with all inherited `GIT_*` variables
  removed, replacement objects disabled and the graft file pointed at a path that never exists.
  A repository that is shallow, or carries `refs/replace/*` or `info/grafts`, is refused for
  ancestry proofs: only real object ancestry proves a candidate or an acceptance.
- Every path list read from git is NUL-terminated (`-z`) raw bytes decoded as strict UTF-8, with no
  trimming, case folding or normalization, so `core.quotePath` display quoting never reaches a
  comparison (WPP01-CR-001); an unterminated record is a framing error (D4).
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
   WPP01-CR-001). `--docs` must be a non-bare working-tree root. `--revision` accepts exactly
   `HEAD`, a full 40-hex commit OID, or a plain local branch name resolved only as
   `refs/heads/<name>` (never a tag, remote, abbreviation or qualified `refs/…` spelling); it is
   resolved once, and that commit supplies the inventory and every blob (CE-P01-01 D8, D15);
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
