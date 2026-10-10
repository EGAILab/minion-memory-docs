# CE-P01-01 — completeness challenge, row classification, checkpoint proposal

Claude, 2026-10-10. Governs: G-018. Input: Codex characterization
`assurance/convergence/CE-P01-01-characterization.md` at `281b81a3281ede7dc41a3f2913ae3a4b0b199625`
(688 rows, reference docs `1422423e`, code `bb05e395`). Production surface is still frozen; this
artifact changes no code.

**Checkpoint status: `PROPOSED FOR IMPLEMENTATION` — revision 2.**
- Revision 1 (`de153c0`) received `CHANGES_REQUIRED` from Codex
  (`assurance/reviews/WP-P01-CE-P01-01-checkpoint-codex.md` at `8420760`). All seven required
  changes are accepted; §0 maps each one to its resolution.
- This revision is still not agreed. It becomes `AGREED FOR IMPLEMENTATION` only after Codex
  records a separate `APPROVED` on this exact artifact. Until then, nothing on the frozen surface
  is edited.

## 0. Response to checkpoint review (revision 1 → 2)

| Required change | Resolution in this revision |
|---|---|
| CE1-CP-001 source-key domain | Verified: all 12 bundle keys are uppercase, and `spec.py` `CITATION` uses `[A-Z][A-Z0-9]*`. D14's key grammar is now that citation grammar, bounded at 16 characters: `[A-Z][A-Z0-9]{0,15}`. No key or citation is renamed. New positive control CH11 covers all 12 keys plus `DOC`. C16/V08 keep their success oracle. |
| CE1-CP-002 linked roots vs nested markers | E10 is now a **KEEP-POS** positive control: a root `.git` file is the linked worktree's own administrative marker. New CH06 (a nested `.git` **file** in a docs subdirectory) was executed and is refused today, so it is a KEEP-NEG control that must stay refused. D16 now states a domain for each inventory. D7 locates `shallow`, `info/grafts` and replace refs through `git rev-parse --git-common-dir` / `--git-path`, never by assuming `<root>/.git/`. |
| CE1-CP-003 trigger shape | Kept the string domain: `deferred_trigger` is a non-blank string. S229/S258/S259/S262/S266 remain KEEP-POS unchanged. N03–N05 (True, list, blank) remain FIX. No shape migration. |
| CE1-CP-004 identity gate | D2 now names its gates. File-aware gates enforce stem == `work_package`: `validate_state_file`, `check_state`, `state validate`. Pure-object `validate_state(obj, label)` does not; its label is diagnostic only. `state roundtrip` stays equality-only for content and applies only D1's name/kind domain to inventories. P01a becomes FIX with component oracles. New P01p is a matching-ID positive. |
| CE1-CP-005 repair vs preserved | S330 → KEEP-POS. M03 → KEEP-POS, defensive with no kill credit; CH01/CH02 are D7's discriminating witnesses. C05 → POLICY: today it runs all eight checks honestly. U07 → accepted on W/L/C, with the DIAG carve-out removed. OPAQUE keeps the existing string-or-null guards. §5 now separates kill-credited controls from regression controls. |
| CE1-CP-006 revision spellings | D8 now defines accepted CLI spellings separately from the resolution namespace. Composite G rows carry candidate and roundtrip component oracles. CH09 (a local branch named `deadbeef`) is accepted. CH10 (spelling `refs/heads/wp/test`) is POLICY-refused. |
| CE1-CP-007 cross-entry producer failure | Added CH07 (valid first entry, bad later hash, from Codex's `CP-later-entry-corrected`) as FIX with an all-bytes-unchanged oracle, and CH08 (all-valid multi-entry) as a positive. D14 now states its write-failure scope and limit. |

Revision-2 totals over 700 rows (688 original plus 12 new controls):
- KEEP-NEG 398, KEEP-POS 105, OPAQUE 84, FIX 99, POLICY 4, LIMIT 6, DIAG 4.
- FIX by finding: CR-001 30, CR-002 23, CR-003 14, CR-004 4, CR-005 25, CR-006 3.

## 1. Independent reproduction (challenge, not trust)

I re-executed 12 headline witnesses myself against the frozen modules on Windows. Each ran in a
fresh disposable World fixture (`.tmp/work/claude/challenge_witnesses.py`), and the frozen tooling
was confirmed byte-identical to `1422423e` first. All 12 reproduce Codex's false pass:

| Row | Independent result |
|---|---|
| A03 | CLOSED with orphan mains refused; adding tags named `main` → `{}` (accepted) |
| A01 | non-state descendant refused; tag `wp/test` at the candidate → `{}` |
| O02 | annotated-tag OID (`cat-file -t` = `tag`) accepted as candidate → `{}` |
| F06 | merge of a state-only side branch accepted in the "linear" chain → `{}` |
| J01 | `process/certification-registry.yaml.bak` accepted as state-only → `{}` |
| Q03 / Q08 / Q10 / N01 | `schema_version: 2.0`, Arabic-Indic digits, trailing newline, INCIDENT with action → all `[]` |
| P02 | committed `WP-UP.YAML` deleted from working tree → roundtrip `[]` |
| K02 | nested committed state file → roundtrip `[]` and all checks `{}` |
| Z06 | `sources build` with key `../escaped-marker` → exit 0, file written outside `reference/source-text` |

My first F06 fixture was wrong: it added an invalid state file, so it was rejected for the wrong
reason. It was redone with a valid state-only path before being counted. A05 remains a
non-witness, and Q01 is the real graph witness; that distinction is kept.

## 2. Completeness challenge — additions to the matrix

| ID | Gap | Executed evidence (frozen validator unless stated) | Effect on contract |
|---|---|---|---|
| CH01 | Ambient `GIT_CEILING_DIRECTORIES` is not among M01–M04 | Workspace inside a git repo: refused (`workspace root … is inside a git repository`). With `GIT_CEILING_DIRECTORIES=<outer>` the same check passes. **False pass.** | D7: sanitize **every** `GIT_*` variable, not a list of four |
| CH02 | Replacement refs outside `refs/replace/` | Replacement graft stored under `refs/hidden/`, `refs/replace/` verified empty. CLOSED with orphan mains is refused without env, and passes `{}` with `GIT_REPLACE_REF_BASE=refs/hidden/`. **False pass.** It defeats a fix that only checks `refs/replace/*`. | D7 |
| CH03 | `--no-replace-objects` does not disable legacy grafts | git 2.55 (git-level): with `.git/info/grafts` present, `merge-base --is-ancestor <orphan> main` exits 0 both with and without `--no-replace-objects`. Only `GIT_GRAFT_FILE=<nonexistent>` restores exit 1. | D7: a fix using only `--no-replace-objects` leaves Q02 a false pass; Q02 must be retained as its own control |
| CH04 | Shallow repositories | Fixture inconclusive: it set main equal to the candidate, so the shallow boundary could not hide ancestry. Shallow history can only *remove* parents, so the risk is a false refusal, not a false pass. | D7 refuses shallow repos with a named diagnostic; no false-pass claim made |
| CH05 | `textconv`/smudge attributes on blob reads | git-level: `git show <rev>:<path>` returned raw blob bytes with both a `diff.textconv` and a `filter.smudge` attribute configured. **Not a gap**, recorded so it is not re-probed. | none |

Deferred with reason (no false pass possible): object alternates. A candidate must still be
reachable from the resolved branch OID, so borrowed objects cannot create ancestry.

## 3. Findings

All are `CONTRACT_ASSURANCE_DEFECT` for the routing and evidence paths.
`SEMANTICS_NEUTRAL_HARDENING` applies only where noted. None is path C: these are process-tooling
contracts owned by coordinator and reviewer, with no product semantics.

| Finding | Classification | Rows (FIX) |
|---|---|---|
| WPP01-CR-001 inventory eligibility/identity | CONTRACT_ASSURANCE_DEFECT | 30 |
| WPP01-CR-002 proof binding (repo, object, namespace, graph, snapshot, chain) | CONTRACT_ASSURANCE_DEFECT | 20 + CH01–CH03 |
| WPP01-CR-003 malformed-input totality | SEMANTICS_NEUTRAL_HARDENING. Every listed row already blocks action through an exception or nonzero exit, and none produces a success result. | 14 |
| WPP01-CR-004 producer output/input bound | CONTRACT_ASSURANCE_DEFECT, priority high (Z06 writes outside its destination) | 3 |
| WPP01-CR-005 permissive tokens/truthiness | CONTRACT_ASSURANCE_DEFECT for routing/evidence fields | 26 |
| **WPP01-CR-006 (new)** CLI context claims exceed what is verified: empty `--only` (C05), `validate --docs` that does not contain (V12/Z10), bare repo diagnosed as a state deletion (F08) | SEMANTICS_NEUTRAL_HARDENING (each already exits correctly or reports its scope) | 4 |

## 4. Checkpoint decisions (proposed; Codex approval makes them agreed)

- **D1. State inventory domain.**
  - Working and committed views use one rule on every host. Every immediate entry of
    `process/state/` must be a regular file named `<WP-ID>.yaml`, with the literal lowercase
    suffix, compared byte-exactly.
  - Any other entry, in either view, is an error naming the exact identity in escaped form:
    another name, a case-variant suffix, a nested directory, a symlink, a gitlink or a non-UTF-8
    name. It never silently becomes authority and never silently disappears.
  - Matching, uncommitted extras and working deletions keep today's semantics. A committed
    deletion stays legitimate.
- **D2. Work-package identity.** `work_package` full-matches the ASCII pattern `WP-[A-Z0-9]{1,8}`.
  Existing `WP-00`, `WP-P01` and `WP-01` conform. Uppercase-only IDs prevent case collisions on
  case-insensitive hosts, and Windows device names cannot match.
  - **Gates.** The *file-aware* gates require file stem == `work_package`: `validate_state_file`,
    `check_state` and `state validate`. This makes one file per work package and makes duplicates
    impossible.
  - Pure-object `validate_state(obj, label)` checks the token only; its label is diagnostic and
    never treated as a path.
  - `state roundtrip` compares committed and working bytes and inventories. It applies D1's
    name/kind domain, but no content identity rule.
- **D3. Path kinds.**
  - Committed entries must have mode `100644` or `100755`. Working entries must be regular files
    (`lstat`; symlinks are not followed).
  - Directories, symlinks and gitlinks are errors with a kind-naming diagnostic, never an
    exception.
- **D4. Git path transport.**
  - Raw `-z` bytes and strict UTF-8, with no trim, casefold or normalization.
  - Non-empty output must end in NUL; an unterminated final record (I07) is a framing error.
  - Raw framing unit controls I01–I07 are kept as separately identified tests.
- **D5. Candidate refs.**
  - A `ref` is a plain branch name resolved only as the fully qualified `refs/heads/<ref>`.
  - A symbolic ref there is refused (G02, M05, J05). No current workflow uses symbolic branch
    refs, and allowing them reopens J05.
  - Packed and loose refs behave identically through git plumbing.
- **D6. Exact object kind.** The candidate `sha` names an object whose own type is `commit`.
  Peeling a tag to a commit is refused (O02).
- **D7. Hermetic Git environment.** Every validator git subprocess:
  - runs with all inherited `GIT_*` variables removed;
  - sets `GIT_NO_REPLACE_OBJECTS=1` and `GIT_GRAFT_FILE` to a non-existent path inside the
    project `.tmp`;
  - refuses, with a named diagnostic, a repository that is shallow or carries `refs/replace/*`
    or `info/grafts`. These are located through `git rev-parse --is-shallow-repository`,
    `--git-common-dir` and `--git-path info/grafts`, so linked-worktree roots whose `.git` is a
    file are handled.

  Canonical ancestry is real object ancestry only (Q01, Q02, CH01–CH04, M01–M04).
- **D8. One resolution per proof.**
  - Each side resolves `refs/heads/<ref>` once to an OID. Ancestry, `rev-list` and per-commit
    `diff-tree` all use that OID. CLOSED resolves `refs/heads/main` the same way.
  - **Accepted roundtrip `--revision` spellings** (exactly three):
    1. the literal `HEAD`;
    2. exactly 40 lowercase hex, always treated as an OID whose own type must be `commit`;
    3. a plain branch name in the candidate-ref grammar, which excludes `refs/…`, `HEAD`,
       40-hex forms and option-like or range text.
  - **Resolution namespace.** A plain name resolves **only** as `refs/heads/<name>`, through
    the D5 non-symbolic rule. A name that is not a local head is refused. It is never resolved
    as a tag, a remote or an object abbreviation (J06–J08, G13).
  - An existing local branch whose name happens to be hex (`deadbeef`, CH09) is accepted as a
    branch. Qualified spellings such as `refs/heads/wp/test` (CH10) and `refs/remotes/…` are
    refused.
  - The spelling is resolved once to an OID, and that OID is used for the inventory and every
    blob read (F04, A01–A03, A06).
  - **Composite rows** state two components: candidate-ref acceptance (D5/D11) and roundtrip
    argument acceptance (this rule). An accepted argument can still fail roundtrip equality on a
    fixture-intended byte delta (G01, G08, G12); that is reported as equality failure, not
    argument refusal.
- **D9. One load per object.** Each state file is read and parsed once per check invocation, and
  every later check uses that validated object (F05).
- **D10. State-only chain.**
  - Every commit in `candidate..tip` has exactly one parent (F06).
  - Allowed paths are the directory prefixes `process/state/` and `process/handoffs/`, plus the
    exact path `process/certification-registry.yaml` (J01, J02).
  - The per-commit check, including reverted changes, and the CLOSED exemption after canonical
    acceptance are unchanged.
- **D11. Exact operational tokens.**
  - `schema_version` is `type(x) is int and x == 2`.
  - `sha`, `ref`, `repo` and ID patterns use full-match with `re.ASCII`. No `$` end-anchor
    leniency (trailing newline), no Unicode digits.
- **D12. Status evidence.**
  - `requirements` elements full-match `<FAMILY>-\d{3}`, where FAMILY is one of the 25 declared
    families. `open_findings` and `provisionally_closed` elements full-match
    `NF-\d{3}|WP[0-9A-Z]+-CR-\d{3}`.
  - CONTRACT_CONVERGENCE: `convergence` is a mapping with a non-blank string `episode` and a
    non-empty list of finding IDs.
  - CONTRACT_CONVERGENCE: no episode grammar beyond the non-blank string (S330 is valid).
  - WAITING_FOR_TRIGGER: `deferred_trigger` is a non-blank string, the established domain.
    `True`, lists and blank strings are refused.
  - INCIDENT and INVALID_UNAUTHORIZED: `next_owner` **and** `next_action` are null.
  - Owner/action membership is tested only after the type test.
- **D13. Totality.**
  - Every direct entry point returns its documented error for malformed input: `validate_state`,
    `validate_state_file`, `state_roundtrip`, each `check_*` and each CLI command.
  - No uncaught exception, partial success or success-empty inventory. The `run_all`
    internal-error guard stays as a backstop only.
  - Host setup inability (W cells of P09–P13 and U05/U06/U08/U09; P16 on all hosts) is
    diagnostic-only, never a killed control.
- **D14. Source producer bound.**
  - `documents[].key` full-matches the established citation grammar, bounded at 16 characters:
    `[A-Z][A-Z0-9]{0,15}`. The 12 bundle keys and fixture `DOC` all match (CH11). No separator
    or dot is possible, so no key can escape (Z06, Z07).
  - `documents[].file` is a relative path inside `bundle_root` with no `..` and no absolute or
    drive form (E12).
  - **Preflight.** Every entry (types, key, file, hash) is validated, and every output path is
    resolved and confirmed inside `reference/source-text`, **before the first write**. Any
    validation failure exits 1 with every existing destination and index byte unchanged and no
    new file (CH07; Z09).
  - **Write phase.** Outputs and index are written to sibling temporary files, then replaced in
    turn.
  - **Stated limit.** An OS failure *during the replace phase* can leave a mix of old and new
    files. The build then exits 1, naming every file it had replaced, and a rerun is required.
    This is not claimed transactional. No control simulates OS write failure beyond one injected
    failure on the first replace, which must exit 1 with the diagnostic.
- **D15. CLI scope honesty.**
  - `--only` with zero names becomes a usage error. This is a policy change: today it honestly
    runs and reports all eight checks, so it is not a false pass (C05).
  - `state validate --docs D` refuses a path outside `D/process/state`.
  - `state roundtrip` verifies that `--docs` is a non-bare working-tree root before any
    inventory, and the diagnostic says so.
  - Partial commands (C04, U13–U17) keep reporting only their own scope.
- **D16. Other inventories — one domain per inventory.** Suffixes are compared case-sensitively
  and byte-exactly on every host. Results are identical on W/L/C. Kinds are checked with `lstat`
  (no symlink following):
  - **Findings** (`assurance/findings/`):
    - immediate entries only;
    - members are regular files ending in `.yaml`;
    - any other entry is an error: a directory, a symlink, or a case-variant such as `.YAML`
      (E01, E02).
  - **Spec** (`spec/`):
    - recursive;
    - members are regular files ending in `.md`, including the existing `README.md`;
    - a directory named `*.md`, a symlink or a case-variant suffix is an error;
    - subdirectories not named `*.md` are traversed (E03, E04).
  - **Source text** (`reference/source-text/`):
    - immediate entries only;
    - members are regular files ending in `.md`;
    - any other entry is an error, so `.MD` is refused on every host (E05).
  - **Conformance** (`conformance/<family>/`):
    - recursive;
    - members are regular files ending in `.yaml`;
    - the existing `README.md` exception is retained;
    - hidden `.yaml` files are ordinary members (E07);
    - a directory named `*.yaml`, a symlink or another suffix is an error (E06, E08).
  - **Nested-repository scan.** This is an exact-name and location domain, not a suffix
    inventory. Any entry named exactly `.git` (file or directory) *below* a repository root is a
    nested repository (E09, CH06). Each repository root's own `.git`, file or directory, is its
    administrative marker and is valid (E10). The existing temp/worktree exclusions are
    unchanged.
- **Opaque metadata (no change).** These fields keep today's acceptance and are explicitly
  documented as conferring no authority: `title`, `layer`, `authority`, `dependencies`,
  `history`, `governance_source`, `updated_by`, `updated_reason`, `scoping_review` outside a
  process-only CLOSED, `deferred_trigger` outside WAITING_FOR_TRIGGER, and `convergence` outside
  CONTRACT_CONVERGENCE. CLOSED `verdict`/`source` stay free text; `outcome` is the gate token.
  Tightening any of them is not part of this episode.

`coordination-state.md` §2–§4 will be amended to state D1–D16 in the same implementation commit,
so the written contract and validator move together.

## 5. Implementation and closure plan (once agreed)

1. One implementation pass on `wpP01/hardening`, starting from `281b81a`. It touches only the six
   frozen modules, their tests and `coordination-state.md`.
2. Tests: every FIX and POLICY row becomes an executed control with the oracle below. Every
   KEEP-* and OPAQUE row is retained as a positive or negative control. DIAG and LIMIT rows are
   labelled as such.
   - Controls run on Windows and on a case-sensitive POSIX filesystem; host-unrepresentable cells
     are skipped with a recorded reason, never counted.
   - CH01–CH03 are added as controls; CH03 is checked against the actual `GIT_GRAFT_FILE`
     mechanism.
3. **Control accounting.**
   - Only **FIX** rows are kill-credited. For each one, the frozen tooling must produce the
     recorded wrong result and the implementation must produce the oracle. Both are executed
     through the control runner's own baseline.
   - **POLICY** rows show a deliberate change: old acceptance, new refusal. They are not counted
     as defect kills.
   - **KEEP-POS / KEEP-NEG / OPAQUE** rows are regression controls with unchanged oracles, and
     earn no kill credit (M03 and CH06 included).
   - **LIMIT / DIAG** rows are labelled and never counted.
   - Each control records its discriminating property: the input dimension that separates the
     right implementation from the named wrong one.
4. Hand-off to Codex for targeted closure against this matrix only. Unrelated WP-P01 semantics
   are not reopened (G-018).

## 6. Row classification (revision 2: 688 original plus 12 new controls = 700)

Totals are as given in §0. The table is generated by `.tmp/work/claude/ce1_classify.py` (revision 2) from the parsed
matrix. The script asserts that every row is classified exactly once. Rows `P01p` and `CH01`–`CH11` are new controls
added by this challenge and the checkpoint review.

| ID | Input / case | Disposition | Finding / decision | Agreed oracle |
|---|---|---|---|---|
| `B01` | all validator call sites / valid World | KEEP-POS | - | valid world passes every check and roundtrip |
| `B02` | roundtrip git calls / matching HEAD inventory | KEEP-POS | - | valid world passes every check and roundtrip |
| `S001` | state.workflow / missing | KEEP-NEG | - | refused |
| `S002` | state.workflow / null | KEEP-NEG | - | refused |
| `S003` | state.workflow / empty-map | KEEP-NEG | - | refused |
| `S004` | state.workflow / list | KEEP-NEG | - | refused |
| `S005` | state.workflow / integer | KEEP-NEG | - | refused |
| `S006` | state.workflow / boolean | KEEP-NEG | - | refused |
| `S007` | state.workflow / empty-string | KEEP-NEG | - | refused |
| `S008` | state.workflow.schema_version / missing | KEEP-NEG | - | refused |
| `S009` | state.workflow.schema_version / null | KEEP-NEG | - | refused |
| `S010` | state.workflow.schema_version / empty-map | KEEP-NEG | - | refused |
| `S011` | state.workflow.schema_version / list | KEEP-NEG | - | refused |
| `S012` | state.workflow.schema_version / integer | KEEP-NEG | - | refused |
| `S013` | state.workflow.schema_version / boolean | KEEP-NEG | - | refused |
| `S014` | state.workflow.schema_version / empty-string | KEEP-NEG | - | refused |
| `S015` | state.workflow.status / missing | KEEP-NEG | - | refused |
| `S016` | state.workflow.status / null | KEEP-NEG | - | refused |
| `S017` | state.workflow.status / empty-map | KEEP-NEG | - | refused |
| `S018` | state.workflow.status / list | KEEP-NEG | - | refused |
| `S019` | state.workflow.status / integer | KEEP-NEG | - | refused |
| `S020` | state.workflow.status / boolean | KEEP-NEG | - | refused |
| `S021` | state.workflow.status / empty-string | KEEP-NEG | - | refused |
| `S022` | state.workflow.requirements / missing | KEEP-NEG | - | refused |
| `S023` | state.workflow.requirements / null | KEEP-NEG | - | refused |
| `S024` | state.workflow.requirements / empty-map | KEEP-NEG | - | refused |
| `S025` | state.workflow.requirements / list | KEEP-POS | - | valid shape accepted (pre-candidate / null-owner where the status allows) |
| `S026` | state.workflow.requirements / integer | KEEP-NEG | - | refused |
| `S027` | state.workflow.requirements / boolean | KEEP-NEG | - | refused |
| `S028` | state.workflow.requirements / empty-string | KEEP-NEG | - | refused |
| `S029` | state.workflow.open_findings / missing | KEEP-NEG | - | refused |
| `S030` | state.workflow.open_findings / null | KEEP-NEG | - | refused |
| `S031` | state.workflow.open_findings / empty-map | KEEP-NEG | - | refused |
| `S032` | state.workflow.open_findings / list | KEEP-POS | - | valid shape accepted (pre-candidate / null-owner where the status allows) |
| `S033` | state.workflow.open_findings / integer | KEEP-NEG | - | refused |
| `S034` | state.workflow.open_findings / boolean | KEEP-NEG | - | refused |
| `S035` | state.workflow.open_findings / empty-string | KEEP-NEG | - | refused |
| `S036` | state.workflow.provisionally_closed / missing | KEEP-NEG | - | refused |
| `S037` | state.workflow.provisionally_closed / null | KEEP-NEG | - | refused |
| `S038` | state.workflow.provisionally_closed / empty-map | KEEP-NEG | - | refused |
| `S039` | state.workflow.provisionally_closed / list | KEEP-POS | - | valid shape accepted (pre-candidate / null-owner where the status allows) |
| `S040` | state.workflow.provisionally_closed / integer | KEEP-NEG | - | refused |
| `S041` | state.workflow.provisionally_closed / boolean | KEEP-NEG | - | refused |
| `S042` | state.workflow.provisionally_closed / empty-string | KEEP-NEG | - | refused |
| `S043` | state.workflow.current_candidate / missing | KEEP-POS | - | valid shape accepted (pre-candidate / null-owner where the status allows) |
| `S044` | state.workflow.current_candidate / null | KEEP-POS | - | valid shape accepted (pre-candidate / null-owner where the status allows) |
| `S045` | state.workflow.current_candidate / empty-map | KEEP-POS | - | valid shape accepted (pre-candidate / null-owner where the status allows) |
| `S046` | state.workflow.current_candidate / list | KEEP-NEG | - | refused |
| `S047` | state.workflow.current_candidate / integer | KEEP-NEG | - | refused |
| `S048` | state.workflow.current_candidate / boolean | KEEP-NEG | - | refused |
| `S049` | state.workflow.current_candidate / empty-string | KEEP-NEG | - | refused |
| `S050` | state.workflow.next_owner / missing | KEEP-NEG | - | refused |
| `S051` | state.workflow.next_owner / null | KEEP-NEG | - | refused |
| `S052` | state.workflow.next_owner / empty-map | FIX | CR-003 | D13: non-hashable owner -> 'must be a string or null' error, never TypeError |
| `S053` | state.workflow.next_owner / list | FIX | CR-003 | D13: non-hashable owner -> 'must be a string or null' error, never TypeError |
| `S054` | state.workflow.next_owner / integer | KEEP-NEG | - | refused |
| `S055` | state.workflow.next_owner / boolean | KEEP-NEG | - | refused |
| `S056` | state.workflow.next_owner / empty-string | KEEP-NEG | - | refused |
| `S057` | state.workflow.next_action / missing | KEEP-NEG | - | refused |
| `S058` | state.workflow.next_action / null | KEEP-NEG | - | refused |
| `S059` | state.workflow.next_action / empty-map | KEEP-NEG | - | refused |
| `S060` | state.workflow.next_action / list | KEEP-NEG | - | refused |
| `S061` | state.workflow.next_action / integer | KEEP-NEG | - | refused |
| `S062` | state.workflow.next_action / boolean | KEEP-NEG | - | refused |
| `S063` | state.workflow.next_action / empty-string | KEEP-NEG | - | refused |
| `S064` | state.workflow.updated_by / missing | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `S065` | state.workflow.updated_by / null | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `S066` | state.workflow.updated_by / empty-map | KEEP-NEG | - | refused |
| `S067` | state.workflow.updated_by / list | KEEP-NEG | - | refused |
| `S068` | state.workflow.updated_by / integer | KEEP-NEG | - | refused |
| `S069` | state.workflow.updated_by / boolean | KEEP-NEG | - | refused |
| `S070` | state.workflow.updated_by / empty-string | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `S071` | state.workflow.updated_reason / missing | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `S072` | state.workflow.updated_reason / null | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `S073` | state.workflow.updated_reason / empty-map | KEEP-NEG | - | refused |
| `S074` | state.workflow.updated_reason / list | KEEP-NEG | - | refused |
| `S075` | state.workflow.updated_reason / integer | KEEP-NEG | - | refused |
| `S076` | state.workflow.updated_reason / boolean | KEEP-NEG | - | refused |
| `S077` | state.workflow.updated_reason / empty-string | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `S078` | state.workflow.quarantine / missing | KEEP-NEG | - | refused |
| `S079` | state.workflow.quarantine / null | KEEP-NEG | - | refused |
| `S080` | state.workflow.quarantine / empty-map | KEEP-NEG | - | refused |
| `S081` | state.workflow.quarantine / list | KEEP-NEG | - | refused |
| `S082` | state.workflow.quarantine / integer | KEEP-NEG | - | refused |
| `S083` | state.workflow.quarantine / boolean | KEEP-NEG | - | refused |
| `S084` | state.workflow.quarantine / empty-string | KEEP-NEG | - | refused |
| `S085` | state.workflow.convergence / missing | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `S086` | state.workflow.convergence / null | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `S087` | state.workflow.convergence / empty-map | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `S088` | state.workflow.convergence / list | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `S089` | state.workflow.convergence / integer | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `S090` | state.workflow.convergence / boolean | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `S091` | state.workflow.convergence / empty-string | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `S092` | state.workflow.governance_source / missing | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `S093` | state.workflow.governance_source / null | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `S094` | state.workflow.governance_source / empty-map | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `S095` | state.workflow.governance_source / list | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `S096` | state.workflow.governance_source / integer | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `S097` | state.workflow.governance_source / boolean | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `S098` | state.workflow.governance_source / empty-string | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `S099` | state.workflow.history / missing | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `S100` | state.workflow.history / null | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `S101` | state.workflow.history / empty-map | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `S102` | state.workflow.history / list | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `S103` | state.workflow.history / integer | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `S104` | state.workflow.history / boolean | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `S105` | state.workflow.history / empty-string | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `S106` | candidate.code.repo / missing | KEEP-NEG | - | refused |
| `S107` | candidate.code.repo / null | KEEP-NEG | - | refused |
| `S108` | candidate.code.repo / empty-map | KEEP-NEG | - | refused |
| `S109` | candidate.code.repo / list | KEEP-NEG | - | refused |
| `S110` | candidate.code.repo / integer | KEEP-NEG | - | refused |
| `S111` | candidate.code.repo / boolean | KEEP-NEG | - | refused |
| `S112` | candidate.code.repo / empty-string | KEEP-NEG | - | refused |
| `S113` | candidate.code.ref / missing | KEEP-NEG | - | refused |
| `S114` | candidate.code.ref / null | KEEP-NEG | - | refused |
| `S115` | candidate.code.ref / empty-map | KEEP-NEG | - | refused |
| `S116` | candidate.code.ref / list | KEEP-NEG | - | refused |
| `S117` | candidate.code.ref / integer | KEEP-NEG | - | refused |
| `S118` | candidate.code.ref / boolean | KEEP-NEG | - | refused |
| `S119` | candidate.code.ref / empty-string | KEEP-NEG | - | refused |
| `S120` | candidate.code.sha / missing | KEEP-NEG | - | refused |
| `S121` | candidate.code.sha / null | KEEP-NEG | - | refused |
| `S122` | candidate.code.sha / empty-map | KEEP-NEG | - | refused |
| `S123` | candidate.code.sha / list | KEEP-NEG | - | refused |
| `S124` | candidate.code.sha / integer | KEEP-NEG | - | refused |
| `S125` | candidate.code.sha / boolean | KEEP-NEG | - | refused |
| `S126` | candidate.code.sha / empty-string | KEEP-NEG | - | refused |
| `S127` | candidate.docs.repo / missing | KEEP-NEG | - | refused |
| `S128` | candidate.docs.repo / null | KEEP-NEG | - | refused |
| `S129` | candidate.docs.repo / empty-map | KEEP-NEG | - | refused |
| `S130` | candidate.docs.repo / list | KEEP-NEG | - | refused |
| `S131` | candidate.docs.repo / integer | KEEP-NEG | - | refused |
| `S132` | candidate.docs.repo / boolean | KEEP-NEG | - | refused |
| `S133` | candidate.docs.repo / empty-string | KEEP-NEG | - | refused |
| `S134` | candidate.docs.ref / missing | KEEP-NEG | - | refused |
| `S135` | candidate.docs.ref / null | KEEP-NEG | - | refused |
| `S136` | candidate.docs.ref / empty-map | KEEP-NEG | - | refused |
| `S137` | candidate.docs.ref / list | KEEP-NEG | - | refused |
| `S138` | candidate.docs.ref / integer | KEEP-NEG | - | refused |
| `S139` | candidate.docs.ref / boolean | KEEP-NEG | - | refused |
| `S140` | candidate.docs.ref / empty-string | KEEP-NEG | - | refused |
| `S141` | candidate.docs.sha / missing | KEEP-NEG | - | refused |
| `S142` | candidate.docs.sha / null | KEEP-NEG | - | refused |
| `S143` | candidate.docs.sha / empty-map | KEEP-NEG | - | refused |
| `S144` | candidate.docs.sha / list | KEEP-NEG | - | refused |
| `S145` | candidate.docs.sha / integer | KEEP-NEG | - | refused |
| `S146` | candidate.docs.sha / boolean | KEEP-NEG | - | refused |
| `S147` | candidate.docs.sha / empty-string | KEEP-NEG | - | refused |
| `S148` | candidate.code / missing | KEEP-POS | - | valid shape accepted (pre-candidate / null-owner where the status allows) |
| `S149` | candidate.code / null | KEEP-POS | - | valid shape accepted (pre-candidate / null-owner where the status allows) |
| `S150` | candidate.code / empty-map | KEEP-NEG | - | refused |
| `S151` | candidate.code / list | KEEP-NEG | - | refused |
| `S152` | candidate.code / integer | KEEP-NEG | - | refused |
| `S153` | candidate.code / boolean | KEEP-NEG | - | refused |
| `S154` | candidate.code / empty-string | KEEP-NEG | - | refused |
| `S155` | candidate.docs / missing | KEEP-POS | - | valid shape accepted (pre-candidate / null-owner where the status allows) |
| `S156` | candidate.docs / null | KEEP-POS | - | valid shape accepted (pre-candidate / null-owner where the status allows) |
| `S157` | candidate.docs / empty-map | KEEP-NEG | - | refused |
| `S158` | candidate.docs / list | KEEP-NEG | - | refused |
| `S159` | candidate.docs / integer | KEEP-NEG | - | refused |
| `S160` | candidate.docs / boolean | KEEP-NEG | - | refused |
| `S161` | candidate.docs / empty-string | KEEP-NEG | - | refused |
| `S162` | candidate sides / unknown extra | KEEP-NEG | - | refused |
| `S163` | candidate sides / unknown CODE | KEEP-NEG | - | refused |
| `S164` | candidate sides / unknown Docs | KEEP-NEG | - | refused |
| `S165` | candidate.code.repo / 'minion-memory-docs' | KEEP-NEG | - | refused |
| `S166` | candidate.code.repo / 'MINION-MEMORY' | KEEP-NEG | - | refused |
| `S167` | candidate.code.repo / '../other' | KEEP-NEG | - | refused |
| `S168` | candidate.code.sha / '0000000000000000000000000000000000000000' | KEEP-NEG | - | refused |
| `S169` | candidate.code.sha / 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' | KEEP-NEG | - | refused |
| `S170` | candidate.code.sha / 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' | KEEP-NEG | - | refused |
| `S171` | candidate.code.sha / 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' | KEEP-NEG | - | refused |
| `S172` | candidate.code.sha / 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n' | KEEP-NEG | - | refused |
| `S173` | candidate.code.sha / '-x' | KEEP-NEG | - | refused |
| `S174` | candidate.code.sha / 'HEAD' | KEEP-NEG | - | refused |
| `S175` | candidate.code.sha / 'HEAD~0' | KEEP-NEG | - | refused |
| `S176` | candidate.code.ref / 'HEAD' | KEEP-NEG | - | refused |
| `S177` | candidate.code.ref / '@' | KEEP-NEG | - | refused |
| `S178` | candidate.code.ref / 'HEAD@{0}' | KEEP-NEG | - | refused |
| `S179` | candidate.code.ref / 'HEAD~0' | KEEP-NEG | - | refused |
| `S180` | candidate.code.ref / 'HEAD^' | KEEP-NEG | - | refused |
| `S181` | candidate.code.ref / 'wp/test..main' | KEEP-NEG | - | refused |
| `S182` | candidate.code.ref / '--output=x' | KEEP-NEG | - | refused |
| `S183` | candidate.code.ref / 'refs/heads/wp/test' | KEEP-NEG | - | refused |
| `S184` | candidate.code.ref / 'wp//test' | KEEP-NEG | - | refused |
| `S185` | candidate.code.ref / '/wp/test' | KEEP-NEG | - | refused |
| `S186` | candidate.code.ref / 'wp/.hidden' | KEEP-NEG | - | refused |
| `S187` | candidate.code.ref / 'wp/test.lock' | KEEP-NEG | - | refused |
| `S188` | candidate.code.ref / 'wp/test\n' | KEEP-NEG | - | refused |
| `S189` | candidate.code.ref / 'wp/Ü' | KEEP-NEG | - | refused |
| `S190` | candidate.code.ref / 'no-such-branch' | KEEP-NEG | - | refused |
| `S191` | candidate.code.ref / '0000000000000000000000000000000000000000' | KEEP-NEG | - | refused |
| `S192` | candidate.docs.repo / 'minion-memory' | KEEP-NEG | - | refused |
| `S193` | candidate.docs.repo / 'MINION-MEMORY' | KEEP-NEG | - | refused |
| `S194` | candidate.docs.repo / '../other' | KEEP-NEG | - | refused |
| `S195` | candidate.docs.sha / '0000000000000000000000000000000000000000' | KEEP-NEG | - | refused |
| `S196` | candidate.docs.sha / 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' | KEEP-NEG | - | refused |
| `S197` | candidate.docs.sha / 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' | KEEP-NEG | - | refused |
| `S198` | candidate.docs.sha / 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' | KEEP-NEG | - | refused |
| `S199` | candidate.docs.sha / 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n' | KEEP-NEG | - | refused |
| `S200` | candidate.docs.sha / '-x' | KEEP-NEG | - | refused |
| `S201` | candidate.docs.sha / 'HEAD' | KEEP-NEG | - | refused |
| `S202` | candidate.docs.sha / 'HEAD~0' | KEEP-NEG | - | refused |
| `S203` | candidate.docs.ref / 'HEAD' | KEEP-NEG | - | refused |
| `S204` | candidate.docs.ref / '@' | KEEP-NEG | - | refused |
| `S205` | candidate.docs.ref / 'HEAD@{0}' | KEEP-NEG | - | refused |
| `S206` | candidate.docs.ref / 'HEAD~0' | KEEP-NEG | - | refused |
| `S207` | candidate.docs.ref / 'HEAD^' | KEEP-NEG | - | refused |
| `S208` | candidate.docs.ref / 'wp/test..main' | KEEP-NEG | - | refused |
| `S209` | candidate.docs.ref / '--output=x' | KEEP-NEG | - | refused |
| `S210` | candidate.docs.ref / 'refs/heads/wp/test' | KEEP-NEG | - | refused |
| `S211` | candidate.docs.ref / 'wp//test' | KEEP-NEG | - | refused |
| `S212` | candidate.docs.ref / '/wp/test' | KEEP-NEG | - | refused |
| `S213` | candidate.docs.ref / 'wp/.hidden' | KEEP-NEG | - | refused |
| `S214` | candidate.docs.ref / 'wp/test.lock' | KEEP-NEG | - | refused |
| `S215` | candidate.docs.ref / 'wp/test\n' | KEEP-NEG | - | refused |
| `S216` | candidate.docs.ref / 'wp/Ü' | KEEP-NEG | - | refused |
| `S217` | candidate.docs.ref / 'no-such-branch' | KEEP-NEG | - | refused |
| `S218` | candidate.docs.ref / '0000000000000000000000000000000000000000' | KEEP-NEG | - | refused |
| `S219` | state.status / SCOPING valid evidence | KEEP-POS | - | status-specific valid evidence accepted |
| `S220` | state.status / CONTRACT_DRAFT valid evidence | KEEP-POS | - | status-specific valid evidence accepted |
| `S221` | state.status / CONTRACT_REVIEW valid evidence | KEEP-POS | - | status-specific valid evidence accepted |
| `S222` | state.status / PYTHON_IMPLEMENTATION valid evidence | KEEP-POS | - | status-specific valid evidence accepted |
| `S223` | state.status / IMPLEMENTATION_REVIEW valid evidence | KEEP-POS | - | status-specific valid evidence accepted |
| `S224` | state.status / REMEDIATION valid evidence | KEEP-POS | - | status-specific valid evidence accepted |
| `S225` | state.status / CONTRACT_CONVERGENCE valid evidence | KEEP-POS | - | status-specific valid evidence accepted |
| `S226` | state.status / FINAL_CONTRACT_REVIEW valid evidence | KEEP-POS | - | status-specific valid evidence accepted |
| `S227` | state.status / RUST_IMPLEMENTATION valid evidence | KEEP-POS | - | status-specific valid evidence accepted |
| `S228` | state.status / CLOSURE_REVIEW valid evidence | KEEP-POS | - | status-specific valid evidence accepted |
| `S229` | state.status / WAITING_FOR_TRIGGER valid evidence | KEEP-POS | - | status-specific valid evidence accepted |
| `S230` | state.status / CLOSED valid evidence | KEEP-POS | - | status-specific valid evidence accepted |
| `S231` | state.status / INCIDENT valid evidence | KEEP-POS | - | status-specific valid evidence accepted |
| `S232` | state.status / INVALID_UNAUTHORIZED valid evidence | KEEP-POS | - | status-specific valid evidence accepted |
| `S233` | state.status / BLOCKED_FOR_OWNER valid evidence | KEEP-POS | - | status-specific valid evidence accepted |
| `S234` | SCOPING.current_candidate / None | KEEP-POS | - | valid shape accepted (pre-candidate / null-owner where the status allows) |
| `S235` | SCOPING.current_candidate / {} | KEEP-POS | - | valid shape accepted (pre-candidate / null-owner where the status allows) |
| `S236` | SCOPING.current_candidate / [] | KEEP-NEG | - | refused |
| `S237` | SCOPING.current_candidate / False | KEEP-NEG | - | refused |
| `S238` | SCOPING.next_owner / None | KEEP-NEG | - | refused |
| `S239` | SCOPING.next_owner / {} | FIX | CR-003 | D13: non-hashable owner -> 'must be a string or null' error, never TypeError |
| `S240` | SCOPING.next_owner / [] | FIX | CR-003 | D13: non-hashable owner -> 'must be a string or null' error, never TypeError |
| `S241` | SCOPING.next_owner / False | KEEP-NEG | - | refused |
| `S242` | SCOPING.next_action / None | KEEP-NEG | - | refused |
| `S243` | SCOPING.next_action / {} | KEEP-NEG | - | refused |
| `S244` | SCOPING.next_action / [] | KEEP-NEG | - | refused |
| `S245` | SCOPING.next_action / False | KEEP-NEG | - | refused |
| `S246` | CLOSED.current_candidate / None | KEEP-NEG | - | refused |
| `S247` | CLOSED.current_candidate / {} | KEEP-NEG | - | refused |
| `S248` | CLOSED.current_candidate / [] | KEEP-NEG | - | refused |
| `S249` | CLOSED.current_candidate / False | KEEP-NEG | - | refused |
| `S250` | CLOSED.next_owner / None | KEEP-POS | - | valid shape accepted (pre-candidate / null-owner where the status allows) |
| `S251` | CLOSED.next_owner / {} | KEEP-NEG | - | refused |
| `S252` | CLOSED.next_owner / [] | KEEP-NEG | - | refused |
| `S253` | CLOSED.next_owner / False | KEEP-NEG | - | refused |
| `S254` | CLOSED.next_action / None | KEEP-POS | - | valid shape accepted (pre-candidate / null-owner where the status allows) |
| `S255` | CLOSED.next_action / {} | KEEP-NEG | - | refused |
| `S256` | CLOSED.next_action / [] | KEEP-NEG | - | refused |
| `S257` | CLOSED.next_action / False | KEEP-NEG | - | refused |
| `S258` | WAITING_FOR_TRIGGER.current_candidate / None | KEEP-POS | - | valid shape accepted (pre-candidate / null-owner where the status allows) |
| `S259` | WAITING_FOR_TRIGGER.current_candidate / {} | KEEP-POS | - | valid shape accepted (pre-candidate / null-owner where the status allows) |
| `S260` | WAITING_FOR_TRIGGER.current_candidate / [] | KEEP-NEG | - | refused |
| `S261` | WAITING_FOR_TRIGGER.current_candidate / False | KEEP-NEG | - | refused |
| `S262` | WAITING_FOR_TRIGGER.next_owner / None | KEEP-POS | - | valid shape accepted (pre-candidate / null-owner where the status allows) |
| `S263` | WAITING_FOR_TRIGGER.next_owner / {} | KEEP-NEG | - | refused |
| `S264` | WAITING_FOR_TRIGGER.next_owner / [] | KEEP-NEG | - | refused |
| `S265` | WAITING_FOR_TRIGGER.next_owner / False | KEEP-NEG | - | refused |
| `S266` | WAITING_FOR_TRIGGER.next_action / None | KEEP-POS | - | valid shape accepted (pre-candidate / null-owner where the status allows) |
| `S267` | WAITING_FOR_TRIGGER.next_action / {} | KEEP-NEG | - | refused |
| `S268` | WAITING_FOR_TRIGGER.next_action / [] | KEEP-NEG | - | refused |
| `S269` | WAITING_FOR_TRIGGER.next_action / False | KEEP-NEG | - | refused |
| `S270` | BLOCKED_FOR_OWNER.current_candidate / None | KEEP-POS | - | valid shape accepted (pre-candidate / null-owner where the status allows) |
| `S271` | BLOCKED_FOR_OWNER.current_candidate / {} | KEEP-POS | - | valid shape accepted (pre-candidate / null-owner where the status allows) |
| `S272` | BLOCKED_FOR_OWNER.current_candidate / [] | KEEP-NEG | - | refused |
| `S273` | BLOCKED_FOR_OWNER.current_candidate / False | KEEP-NEG | - | refused |
| `S274` | BLOCKED_FOR_OWNER.next_owner / None | KEEP-NEG | - | refused |
| `S275` | BLOCKED_FOR_OWNER.next_owner / {} | FIX | CR-003 | D13: non-hashable owner -> 'must be a string or null' error, never TypeError |
| `S276` | BLOCKED_FOR_OWNER.next_owner / [] | FIX | CR-003 | D13: non-hashable owner -> 'must be a string or null' error, never TypeError |
| `S277` | BLOCKED_FOR_OWNER.next_owner / False | KEEP-NEG | - | refused |
| `S278` | BLOCKED_FOR_OWNER.next_action / None | KEEP-NEG | - | refused |
| `S279` | BLOCKED_FOR_OWNER.next_action / {} | KEEP-NEG | - | refused |
| `S280` | BLOCKED_FOR_OWNER.next_action / [] | KEEP-NEG | - | refused |
| `S281` | BLOCKED_FOR_OWNER.next_action / False | KEEP-NEG | - | refused |
| `S282` | CONTRACT_CONVERGENCE.current_candidate / None | KEEP-POS | - | valid shape accepted (pre-candidate / null-owner where the status allows) |
| `S283` | CONTRACT_CONVERGENCE.current_candidate / {} | KEEP-POS | - | valid shape accepted (pre-candidate / null-owner where the status allows) |
| `S284` | CONTRACT_CONVERGENCE.current_candidate / [] | KEEP-NEG | - | refused |
| `S285` | CONTRACT_CONVERGENCE.current_candidate / False | KEEP-NEG | - | refused |
| `S286` | CONTRACT_CONVERGENCE.next_owner / None | KEEP-NEG | - | refused |
| `S287` | CONTRACT_CONVERGENCE.next_owner / {} | FIX | CR-003 | D13: non-hashable owner -> 'must be a string or null' error, never TypeError |
| `S288` | CONTRACT_CONVERGENCE.next_owner / [] | FIX | CR-003 | D13: non-hashable owner -> 'must be a string or null' error, never TypeError |
| `S289` | CONTRACT_CONVERGENCE.next_owner / False | KEEP-NEG | - | refused |
| `S290` | CONTRACT_CONVERGENCE.next_action / None | KEEP-NEG | - | refused |
| `S291` | CONTRACT_CONVERGENCE.next_action / {} | KEEP-NEG | - | refused |
| `S292` | CONTRACT_CONVERGENCE.next_action / [] | KEEP-NEG | - | refused |
| `S293` | CONTRACT_CONVERGENCE.next_action / False | KEEP-NEG | - | refused |
| `S294` | INCIDENT.current_candidate / None | KEEP-POS | - | valid shape accepted (pre-candidate / null-owner where the status allows) |
| `S295` | INCIDENT.current_candidate / {} | KEEP-POS | - | valid shape accepted (pre-candidate / null-owner where the status allows) |
| `S296` | INCIDENT.current_candidate / [] | KEEP-NEG | - | refused |
| `S297` | INCIDENT.current_candidate / False | KEEP-NEG | - | refused |
| `S298` | INCIDENT.next_owner / None | KEEP-POS | - | valid shape accepted (pre-candidate / null-owner where the status allows) |
| `S299` | INCIDENT.next_owner / {} | KEEP-NEG | - | refused |
| `S300` | INCIDENT.next_owner / [] | KEEP-NEG | - | refused |
| `S301` | INCIDENT.next_owner / False | KEEP-NEG | - | refused |
| `S302` | INCIDENT.next_action / None | KEEP-POS | - | valid shape accepted (pre-candidate / null-owner where the status allows) |
| `S303` | INCIDENT.next_action / {} | KEEP-NEG | - | refused |
| `S304` | INCIDENT.next_action / [] | KEEP-NEG | - | refused |
| `S305` | INCIDENT.next_action / False | KEEP-NEG | - | refused |
| `S306` | CLOSED.review.outcome / None | KEEP-NEG | - | refused |
| `S307` | CLOSED.review.outcome / [] | KEEP-NEG | - | refused |
| `S308` | CLOSED.review.outcome / True | KEEP-NEG | - | refused |
| `S309` | CLOSED.review.outcome / '' | KEEP-NEG | - | refused |
| `S310` | CLOSED.review.outcome / 'NOT APPROVED' | KEEP-NEG | - | refused |
| `S311` | CLOSED.review.outcome / 'APPROVED' | KEEP-POS | - | coordination-state §3: outcome is the only gate token; verdict/source are non-blank free text (independence stays an agent duty) |
| `S312` | CLOSED.review.verdict / None | KEEP-NEG | - | refused |
| `S313` | CLOSED.review.verdict / [] | KEEP-NEG | - | refused |
| `S314` | CLOSED.review.verdict / True | KEEP-NEG | - | refused |
| `S315` | CLOSED.review.verdict / '' | KEEP-NEG | - | refused |
| `S316` | CLOSED.review.verdict / 'NOT APPROVED' | KEEP-POS | - | coordination-state §3: outcome is the only gate token; verdict/source are non-blank free text (independence stays an agent duty) |
| `S317` | CLOSED.review.verdict / 'APPROVED' | KEEP-POS | - | coordination-state §3: outcome is the only gate token; verdict/source are non-blank free text (independence stays an agent duty) |
| `S318` | CLOSED.review.source / None | KEEP-NEG | - | refused |
| `S319` | CLOSED.review.source / [] | KEEP-NEG | - | refused |
| `S320` | CLOSED.review.source / True | KEEP-NEG | - | refused |
| `S321` | CLOSED.review.source / '' | KEEP-NEG | - | refused |
| `S322` | CLOSED.review.source / 'NOT APPROVED' | KEEP-POS | - | coordination-state §3: outcome is the only gate token; verdict/source are non-blank free text (independence stays an agent duty) |
| `S323` | CLOSED.review.source / 'APPROVED' | KEEP-POS | - | coordination-state §3: outcome is the only gate token; verdict/source are non-blank free text (independence stays an agent duty) |
| `S324` | convergence.episode / None | KEEP-NEG | - | refused |
| `S325` | convergence.episode / [] | KEEP-NEG | - | refused |
| `S326` | convergence.episode / True | FIX | CR-005 | D12: episode non-blank string; open_findings non-empty list of finding IDs |
| `S327` | convergence.episode / {} | KEEP-NEG | - | refused |
| `S328` | convergence.episode / '' | KEEP-NEG | - | refused |
| `S329` | convergence.episode / 7 | FIX | CR-005 | D12: episode non-blank string; open_findings non-empty list of finding IDs |
| `S330` | convergence.episode / 'finding' | KEEP-POS | - | non-blank string episode with valid findings: accepted under D12 |
| `S331` | convergence.open_findings / None | KEEP-NEG | - | refused |
| `S332` | convergence.open_findings / [] | KEEP-NEG | - | refused |
| `S333` | convergence.open_findings / True | FIX | CR-005 | D12: episode non-blank string; open_findings non-empty list of finding IDs |
| `S334` | convergence.open_findings / {} | KEEP-NEG | - | refused |
| `S335` | convergence.open_findings / '' | KEEP-NEG | - | refused |
| `S336` | convergence.open_findings / 7 | FIX | CR-005 | D12: episode non-blank string; open_findings non-empty list of finding IDs |
| `S337` | convergence.open_findings / 'finding' | FIX | CR-005 | D12: episode non-blank string; open_findings non-empty list of finding IDs |
| `Y01` | YAML boundary / duplicate-root | KEEP-NEG | - | core loader refuses before business logic |
| `Y02` | YAML boundary / duplicate-side | KEEP-NEG | - | core loader refuses before business logic |
| `Y03` | YAML boundary / alias | KEEP-NEG | - | core loader refuses before business logic |
| `Y04` | YAML boundary / unused-anchor | KEEP-NEG | - | core loader refuses before business logic |
| `Y05` | YAML boundary / explicit-tag | KEEP-NEG | - | core loader refuses before business logic |
| `Y06` | YAML boundary / nonstring-key | KEEP-NEG | - | core loader refuses before business logic |
| `Y07` | YAML boundary / multiple-docs | KEEP-NEG | - | core loader refuses before business logic |
| `Y08` | YAML boundary / empty | KEEP-NEG | - | core loader refuses before business logic |
| `Y09` | YAML boundary / yaml11-yes | KEEP-NEG | - | core loader refuses before business logic |
| `Y10` | YAML boundary / yaml11-date | KEEP-NEG | - | core loader refuses before business logic |
| `Y11` | YAML boundary / nan | KEEP-NEG | - | core loader refuses before business logic |
| `Y12` | YAML boundary / surrogate | KEEP-NEG | - | core loader refuses before business logic |
| `Y13` | YAML boundary / quoted-ambiguous | KEEP-POS | - | accepted core value (BOM tolerated by loader; roundtrip still byte-compares) |
| `Y14` | YAML boundary / bom | KEEP-POS | - | accepted core value (BOM tolerated by loader; roundtrip still byte-compares) |
| `Y15` | YAML boundary / nul | KEEP-NEG | - | core loader refuses before business logic |
| `Y16` | YAML boundary / tab-indent | KEEP-NEG | - | core loader refuses before business logic |
| `Y17` | YAML boundary / valid-null | KEEP-POS | - | accepted core value (BOM tolerated by loader; roundtrip still byte-compares) |
| `Y18` | YAML boundary / depth-65 | KEEP-NEG | - | core loader refuses before business logic |
| `C01` | CLI arguments / check/default | KEEP-POS | - | documented success for the stated scope |
| `C02` | CLI arguments / check/workspace | KEEP-POS | - | documented success for the stated scope |
| `C03` | CLI arguments / check/deep | KEEP-POS | - | documented success for the stated scope |
| `C04` | CLI arguments / check/only-state | LIMIT | - | --only state reports 1/1: honest partial scope, never an approval |
| `C05` | CLI arguments / check/empty-only | POLICY | D15 | today runs and reports all 8 checks (no false pass); D15 makes a bare '--only' a usage error, exit 2 |
| `C06` | CLI arguments / check/unknown-only | KEEP-NEG | - | documented usage/validation failure |
| `C07` | CLI arguments / validate/default | KEEP-POS | - | documented success for the stated scope |
| `C08` | CLI arguments / validate/docs | KEEP-POS | - | documented success for the stated scope |
| `C09` | CLI arguments / validate/missing | KEEP-NEG | - | documented usage/validation failure |
| `C10` | CLI arguments / roundtrip/default | KEEP-POS | - | documented success for the stated scope |
| `C11` | CLI arguments / roundtrip/HEAD | KEEP-POS | - | documented success for the stated scope |
| `C12` | CLI arguments / roundtrip/sha | KEEP-POS | - | documented success for the stated scope |
| `C13` | CLI arguments / transition/legal | KEEP-POS | - | documented success for the stated scope |
| `C14` | CLI arguments / transition/illegal | KEEP-NEG | - | documented usage/validation failure |
| `C15` | CLI arguments / transition/unknown | KEEP-NEG | - | documented usage/validation failure |
| `C16` | CLI arguments / sources/docs | KEEP-POS | - | documented success for the stated scope |
| `C17` | CLI arguments / usage/no-subcommand | KEEP-NEG | - | documented usage/validation failure |
| `C18` | CLI arguments / usage/missing-code | KEEP-NEG | - | documented usage/validation failure |
| `C19` | CLI arguments / usage/missing-docs | KEEP-NEG | - | documented usage/validation failure |
| `C20` | CLI arguments / usage/unknown-option | KEEP-NEG | - | documented usage/validation failure |
| `P01a` | state inventory filename / 'WP-U.yaml' matching | FIX | CR-001 | components: roundtrip [] (byte/inventory equality only); check_state and validate_state_file refuse work_package WP-X in WP-U.yaml (D2) |
| `P01b` | state inventory filename / 'WP-U.yaml' deleted | KEEP-NEG | - | uncommitted deletion of a canonical state file fails roundtrip |
| `P01c` | state inventory filename / 'WP-U.yaml' committed deletion | KEEP-POS | - | committed deletion passes |
| `P02a` | state inventory filename / 'WP-UP.YAML' matching | FIX | CR-001 | D1/D2: non-canonical entry in process/state -> 'unsupported state entry' error on every host |
| `P02b` | state inventory filename / 'WP-UP.YAML' deleted | FIX | CR-001 | committed non-canonical entry reported (and its working deletion fails) on every host |
| `P02c` | state inventory filename / 'WP-UP.YAML' committed deletion | KEEP-POS | - | committed deletion removes the entry from both views: passes |
| `P03a` | state inventory filename / 'WP-Mix.YaMl' matching | FIX | CR-001 | D1/D2: non-canonical entry in process/state -> 'unsupported state entry' error on every host |
| `P03b` | state inventory filename / 'WP-Mix.YaMl' deleted | FIX | CR-001 | committed non-canonical entry reported (and its working deletion fails) on every host |
| `P03c` | state inventory filename / 'WP-Mix.YaMl' committed deletion | KEEP-POS | - | committed deletion removes the entry from both views: passes |
| `P04a` | state inventory filename / '.hidden.yaml' matching | FIX | CR-001 | D1/D2: non-canonical entry in process/state -> 'unsupported state entry' error on every host |
| `P04b` | state inventory filename / '.hidden.yaml' deleted | KEEP-NEG | - | committed non-canonical entry reported (and its working deletion fails) on every host |
| `P04c` | state inventory filename / '.hidden.yaml' committed deletion | KEEP-POS | - | committed deletion removes the entry from both views: passes |
| `P05a` | state inventory filename / ' leading.yaml' matching | FIX | CR-001 | D1/D2: non-canonical entry in process/state -> 'unsupported state entry' error on every host |
| `P05b` | state inventory filename / ' leading.yaml' deleted | KEEP-NEG | - | committed non-canonical entry reported (and its working deletion fails) on every host |
| `P05c` | state inventory filename / ' leading.yaml' committed deletion | KEEP-POS | - | committed deletion removes the entry from both views: passes |
| `P06a` | state inventory filename / 'WP-Ü.yaml' matching | FIX | CR-001 | D1/D2: non-canonical entry in process/state -> 'unsupported state entry' error on every host |
| `P06b` | state inventory filename / 'WP-Ü.yaml' deleted | KEEP-NEG | - | committed non-canonical entry reported (and its working deletion fails) on every host |
| `P06c` | state inventory filename / 'WP-Ü.yaml' committed deletion | KEEP-POS | - | committed deletion removes the entry from both views: passes |
| `P07a` | state inventory filename / 'WP-é.yaml' matching | FIX | CR-001 | D1/D2: non-canonical entry in process/state -> 'unsupported state entry' error on every host |
| `P07b` | state inventory filename / 'WP-é.yaml' deleted | KEEP-NEG | - | committed non-canonical entry reported (and its working deletion fails) on every host |
| `P07c` | state inventory filename / 'WP-é.yaml' committed deletion | KEEP-POS | - | committed deletion removes the entry from both views: passes |
| `P08a` | state inventory filename / 'WP-é.yaml' matching | FIX | CR-001 | D1/D2: non-canonical entry in process/state -> 'unsupported state entry' error on every host |
| `P08b` | state inventory filename / 'WP-é.yaml' deleted | KEEP-NEG | - | committed non-canonical entry reported (and its working deletion fails) on every host |
| `P08c` | state inventory filename / 'WP-é.yaml' committed deletion | KEEP-POS | - | committed deletion removes the entry from both views: passes |
| `P09a` | state inventory filename / 'quote".yaml' matching | FIX | CR-001 | W: DIAG (name unrepresentable); L/C: 'unsupported state entry' error (today passes) |
| `P10a` | state inventory filename / 'tab\t.yaml' matching | FIX | CR-001 | W: DIAG (name unrepresentable); L/C: 'unsupported state entry' error (today passes) |
| `P11a` | state inventory filename / 'line\n.yaml' matching | FIX | CR-001 | W: DIAG (name unrepresentable); L/C: 'unsupported state entry' error (today passes) |
| `P12a` | state inventory filename / 'NUL.yaml' matching | FIX | CR-001 | W: DIAG (name unrepresentable); L/C: 'unsupported state entry' error (today passes) |
| `P13a` | state inventory filename / 'CON.yaml' matching | FIX | CR-001 | W: DIAG (name unrepresentable); L/C: 'unsupported state entry' error (today passes) |
| `P14a` | state inventory filename / 'trail .yaml' matching | FIX | CR-001 | D1/D2: non-canonical entry in process/state -> 'unsupported state entry' error on every host |
| `P14b` | state inventory filename / 'trail .yaml' deleted | KEEP-NEG | - | committed non-canonical entry reported (and its working deletion fails) on every host |
| `P14c` | state inventory filename / 'trail .yaml' committed deletion | KEEP-POS | - | committed deletion removes the entry from both views: passes |
| `P15a` | state inventory filename / 'trailing.yaml ' matching | FIX | CR-001 | D1/D2: non-canonical entry in process/state -> 'unsupported state entry' error on every host |
| `P15b` | state inventory filename / 'trailing.yaml ' deleted | FIX | CR-001 | committed non-canonical entry reported (and its working deletion fails) on every host |
| `P15c` | state inventory filename / 'trailing.yaml ' committed deletion | KEEP-POS | - | committed deletion removes the entry from both views: passes |
| `P16a` | state inventory filename / 'nul\x00.yaml' matching | DIAG | - | NUL cannot occur in a Git or host filename on any host |
| `K01` | state path kind / directory.yaml | KEEP-NEG | - | fails; D3 requires the diagnostic to name the unsupported kind |
| `K02` | state path kind / nested-state | FIX | CR-001 | D1/D2: nested entry / filename != work_package -> error |
| `K03` | state path kind / no-state-directory | KEEP-NEG | - | fails; D3 requires the diagnostic to name the unsupported kind |
| `K04` | state path kind / state-dir-is-file | KEEP-NEG | - | fails; D3 requires the diagnostic to name the unsupported kind |
| `K05` | state path kind / symlink-inside | FIX | CR-001 | D3: symlink in state area -> unsupported-kind error from check state too (today state passes) |
| `K06` | state path kind / symlink-dangling | FIX | CR-003 | D3/D13: dangling symlink -> documented error, never an exception |
| `K07` | state path kind / symlink-outside | FIX | CR-001 | D3: symlink in state area -> unsupported-kind error from check state too (today state passes) |
| `K08` | state path kind / duplicate-work-package | FIX | CR-001 | D1/D2: nested entry / filename != work_package -> error |
| `E01` | other validator enumeration / findings-upper | FIX | CR-001 | D16: every validator inventory enumerates by exact case-sensitive suffix on all hosts; variant/nested/kind entries are errors |
| `E02` | other validator enumeration / findings-nested | FIX | CR-001 | D16: every validator inventory enumerates by exact case-sensitive suffix on all hosts; variant/nested/kind entries are errors |
| `E03` | other validator enumeration / spec-upper | FIX | CR-001 | D16: every validator inventory enumerates by exact case-sensitive suffix on all hosts; variant/nested/kind entries are errors |
| `E04` | other validator enumeration / spec-directory-md | FIX | CR-003 | D16/D13: directory named *.md -> named error, not 'internal error' |
| `E05` | other validator enumeration / source-upper | FIX | CR-001 | D16: every validator inventory enumerates by exact case-sensitive suffix on all hosts; variant/nested/kind entries are errors |
| `E06` | other validator enumeration / scenario-upper | KEEP-NEG | - | refused |
| `E07` | other validator enumeration / scenario-hidden | KEEP-POS | - | hidden but well-formed .yaml scenario is an ordinary corpus member |
| `E08` | other validator enumeration / scenario-directory-yaml | FIX | CR-001 | D16: every validator inventory enumerates by exact case-sensitive suffix on all hosts; variant/nested/kind entries are errors |
| `E09` | other validator enumeration / nested-git-dir | KEEP-NEG | - | refused |
| `E10` | other validator enumeration / git-file-worktree | KEEP-POS | - | linked-worktree root: its own root .git file is the administrative marker, valid (D16 root exception) |
| `E11` | other validator enumeration / docs-equals-code | KEEP-NEG | - | refused |
| `E12` | other validator enumeration / source-file-traversal | FIX | CR-004 | D14: documents[].file is a relative path inside bundle_root (no '..', no absolute) |
| `G01` | candidate/CLI ref / 'good' | KEEP-POS | - | candidate: accepted; roundtrip: argument accepted, equality fails on the fixture-intended byte delta |
| `G02` | candidate/CLI ref / 'symbolic' | POLICY | D5 | candidate: symbolic head refused; roundtrip: same refusal for a symbolic refs/heads name |
| `G03` | candidate/CLI ref / 'tag-only' | KEEP-NEG | - | candidate and roundtrip both refused (G17 at the full-token shape gate, D11) |
| `G04` | candidate/CLI ref / 'annotated' | KEEP-NEG | - | candidate and roundtrip both refused (G17 at the full-token shape gate, D11) |
| `G05` | candidate/CLI ref / 'origin/good' | KEEP-NEG | - | candidate and roundtrip both refused (G17 at the full-token shape gate, D11) |
| `G06` | candidate/CLI ref / 'refs/remotes/origin/good' | KEEP-NEG | - | candidate refused; roundtrip refuses the qualified spelling (D8 accepts plain names only) |
| `G07` | candidate/CLI ref / 'refs/heads/good' | KEEP-NEG | - | candidate refused; roundtrip refuses the qualified spelling (D8 accepts plain names only) |
| `G08` | candidate/CLI ref / 'HEAD' | KEEP-NEG | - | candidate: HEAD refused; roundtrip: argument HEAD accepted, equality fails on the fixture byte delta |
| `G09` | candidate/CLI ref / '@' | KEEP-NEG | - | candidate and roundtrip both refused (G17 at the full-token shape gate, D11) |
| `G10` | candidate/CLI ref / 'HEAD@{0}' | KEEP-NEG | - | candidate and roundtrip both refused (G17 at the full-token shape gate, D11) |
| `G11` | candidate/CLI ref / 'HEAD~0' | KEEP-NEG | - | candidate and roundtrip both refused (G17 at the full-token shape gate, D11) |
| `G12` | candidate/CLI ref / full fixture candidate OID | KEEP-NEG | - | candidate: SHA-shaped ref refused at shape; roundtrip: full commit OID accepted, fixture inventory fails at that commit |
| `G13` | candidate/CLI ref / 8-hex fixture candidate abbreviation | KEEP-NEG | - | candidate and roundtrip refused: no refs/heads/<abbr> exists; an abbreviation is never resolved as an object (D8) |
| `G14` | candidate/CLI ref / 'missing' | KEEP-NEG | - | candidate and roundtrip both refused (G17 at the full-token shape gate, D11) |
| `G15` | candidate/CLI ref / '-x' | KEEP-NEG | - | candidate and roundtrip both refused (G17 at the full-token shape gate, D11) |
| `G16` | candidate/CLI ref / 'HEAD..good' | KEEP-NEG | - | candidate and roundtrip both refused (G17 at the full-token shape gate, D11) |
| `G17` | candidate/CLI ref / 'good\n' | KEEP-NEG | - | candidate and roundtrip both refused (G17 at the full-token shape gate, D11) |
| `G18` | candidate/CLI ref / 'good^' | KEEP-NEG | - | candidate and roundtrip both refused (G17 at the full-token shape gate, D11) |
| `G19` | candidate/CLI ref / 'good~' | KEEP-NEG | - | candidate and roundtrip both refused (G17 at the full-token shape gate, D11) |
| `G20` | candidate/CLI ref / 'good.lock' | KEEP-NEG | - | candidate and roundtrip both refused (G17 at the full-token shape gate, D11) |
| `G21` | candidate/CLI ref / 'good//bad' | KEEP-NEG | - | candidate and roundtrip both refused (G17 at the full-token shape gate, D11) |
| `O01` | candidate SHA object / exact commit OID from fixture | KEEP-POS | - | exact commit OID passes |
| `O02` | candidate SHA object / annotated-tag object OID from fixture | FIX | CR-002 | D6: candidate OID must name a commit object itself (cat-file -t == commit); tag OID refused |
| `O03` | candidate SHA object / blob object OID from fixture | KEEP-NEG | - | refused (O05 at the shape gate under D11) |
| `O04` | candidate SHA object / 40 zero hex (absent) | KEEP-NEG | - | refused (O05 at the shape gate under D11) |
| `O05` | candidate SHA object / candidate OID plus newline | KEEP-NEG | - | refused (O05 at the shape gate under D11) |
| `O06` | candidate SHA object / uppercase candidate OID | KEEP-NEG | - | refused (O05 at the shape gate under D11) |
| `A01` | checked branch -> descendant use / loose branch/tag collision | FIX | CR-002 | D8: refs/heads/<ref> resolved once to an OID used for every later query |
| `A02` | checked branch -> descendant use / packed branch/tag collision | FIX | CR-002 | D8: refs/heads/<ref> resolved once to an OID used for every later query |
| `A03` | CLOSED main proof / tag substitution | FIX | CR-002 | D8: CLOSED proof uses refs/heads/main resolved to an OID, never bare 'main' |
| `A04` | CLOSED main proof / remote substitution | KEEP-NEG | - | orphan mains refused (A05 is a non-witness: replacement there did not fake ancestry) |
| `A05` | CLOSED main proof / replacement substitution | KEEP-NEG | - | orphan mains refused (A05 is a non-witness: replacement there did not fake ancestry) |
| `A06` | check-then-use ref / branch moves after show-ref | FIX | CR-002 | D8: refs/heads/<ref> resolved once to an OID used for every later query |
| `H01` | Git host configuration / core.quotePath=true | KEEP-NEG | - | deletion reported identically under every core.* display/case/precompose setting |
| `H02` | Git host configuration / core.quotePath=false | KEEP-NEG | - | deletion reported identically under every core.* display/case/precompose setting |
| `H03` | Git host configuration / core.ignorecase=true | KEEP-NEG | - | deletion reported identically under every core.* display/case/precompose setting |
| `H04` | Git host configuration / core.ignorecase=false | KEEP-NEG | - | deletion reported identically under every core.* display/case/precompose setting |
| `H05` | Git host configuration / core.precomposeunicode=true | KEEP-NEG | - | deletion reported identically under every core.* display/case/precompose setting |
| `H06` | Git host configuration / core.precomposeunicode=false | KEEP-NEG | - | deletion reported identically under every core.* display/case/precompose setting |
| `H07` | host filesystem capability / distinct case names | DIAG | - | host case-sensitivity capability probe; selects which cells are physically representable |
| `I01` | Git path bytes / b'A.yaml\x00' | KEEP-POS | - | exact NUL-framed UTF-8 identity preserved (I05: undecodable name -> listing failure) |
| `I02` | Git path bytes / b' A.yaml\x00' | KEEP-POS | - | exact NUL-framed UTF-8 identity preserved (I05: undecodable name -> listing failure) |
| `I03` | Git path bytes / b'line\n.yaml\x00' | KEEP-POS | - | exact NUL-framed UTF-8 identity preserved (I05: undecodable name -> listing failure) |
| `I04` | Git path bytes / b'quote".yaml\x00' | KEEP-POS | - | exact NUL-framed UTF-8 identity preserved (I05: undecodable name -> listing failure) |
| `I05` | Git path bytes / b'\xff.yaml\x00' | KEEP-NEG | - | undecodable path bytes -> listing failure, fail closed |
| `I06` | Git path bytes / b'A.yaml\x00B.yaml\x00' | KEEP-POS | - | exact NUL-framed UTF-8 identity preserved (I05: undecodable name -> listing failure) |
| `I07` | Git path bytes / b'A.yaml' | FIX | CR-001 | D4: unterminated final record is a framing error (git -z always NUL-terminates) |
| `I08` | Git transport failure / OSError | KEEP-NEG | - | transport failure -> documented error, no success-empty inventory |
| `I09` | Git transport failure / TimeoutExpired | KEEP-NEG | - | transport failure -> documented error, no success-empty inventory |
| `T01` | state file bytes / invalid-utf8 | KEEP-NEG | - | roundtrip fails on any non-CRLF byte delta / invalid bytes |
| `T02` | state file bytes / invalid-yaml | KEEP-NEG | - | roundtrip fails on any non-CRLF byte delta / invalid bytes |
| `T03` | state file bytes / crlf-checkout | KEEP-POS | - | CRLF checkout artifact only: roundtrip OK |
| `T04` | state file bytes / escaped-value-change | KEEP-NEG | - | roundtrip fails on any non-CRLF byte delta / invalid bytes |
| `T05` | state file bytes / byte-only-comment | KEEP-NEG | - | roundtrip fails on any non-CRLF byte delta / invalid bytes |
| `X001` | state.work_package / missing | KEEP-NEG | - | refused |
| `X002` | state.work_package / null | KEEP-NEG | - | refused |
| `X003` | state.work_package / map | KEEP-NEG | - | refused |
| `X004` | state.work_package / list | KEEP-NEG | - | refused |
| `X005` | state.work_package / int | KEEP-NEG | - | refused |
| `X006` | state.work_package / bool | KEEP-NEG | - | refused |
| `X007` | state.work_package / empty | KEEP-NEG | - | refused |
| `X008` | state.work_package / text | FIX | CR-005 | D2: work_package is a WP-ID token equal to the file stem |
| `X009` | state.title / missing | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X010` | state.title / null | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X011` | state.title / map | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X012` | state.title / list | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X013` | state.title / int | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X014` | state.title / bool | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X015` | state.title / empty | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X016` | state.title / text | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X017` | state.layer / missing | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X018` | state.layer / null | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X019` | state.layer / map | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X020` | state.layer / list | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X021` | state.layer / int | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X022` | state.layer / bool | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X023` | state.layer / empty | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X024` | state.layer / text | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X025` | state.authority / missing | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X026` | state.authority / null | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X027` | state.authority / map | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X028` | state.authority / list | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X029` | state.authority / int | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X030` | state.authority / bool | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X031` | state.authority / empty | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X032` | state.authority / text | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X033` | state.dependencies / missing | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X034` | state.dependencies / null | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X035` | state.dependencies / map | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X036` | state.dependencies / list | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X037` | state.dependencies / int | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X038` | state.dependencies / bool | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X039` | state.dependencies / empty | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X040` | state.dependencies / text | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X041` | state.scoping_review / missing | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X042` | state.scoping_review / null | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X043` | state.scoping_review / map | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X044` | state.scoping_review / list | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X045` | state.scoping_review / int | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X046` | state.scoping_review / bool | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X047` | state.scoping_review / empty | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X048` | state.scoping_review / text | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X049` | state.deferred_trigger / missing | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X050` | state.deferred_trigger / null | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X051` | state.deferred_trigger / map | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X052` | state.deferred_trigger / list | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X053` | state.deferred_trigger / int | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X054` | state.deferred_trigger / bool | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X055` | state.deferred_trigger / empty | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X056` | state.deferred_trigger / text | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X057` | state.quarantine.derived_from_quarantined_artifact / missing | KEEP-NEG | - | refused |
| `X058` | state.quarantine.derived_from_quarantined_artifact / null | KEEP-NEG | - | refused |
| `X059` | state.quarantine.derived_from_quarantined_artifact / map | KEEP-NEG | - | refused |
| `X060` | state.quarantine.derived_from_quarantined_artifact / list | KEEP-NEG | - | refused |
| `X061` | state.quarantine.derived_from_quarantined_artifact / int | KEEP-NEG | - | refused |
| `X062` | state.quarantine.derived_from_quarantined_artifact / bool | KEEP-NEG | - | refused |
| `X063` | state.quarantine.derived_from_quarantined_artifact / empty | KEEP-NEG | - | refused |
| `X064` | state.quarantine.derived_from_quarantined_artifact / text | KEEP-NEG | - | refused |
| `X065` | state.history.assurance_index / missing | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X066` | state.history.assurance_index / null | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X067` | state.history.assurance_index / map | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X068` | state.history.assurance_index / list | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X069` | state.history.assurance_index / int | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X070` | state.history.assurance_index / bool | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X071` | state.history.assurance_index / empty | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X072` | state.history.assurance_index / text | OPAQUE | - | optional metadata: confers no authority; existing type guards (updated_by/updated_reason string-or-null) retained |
| `X073` | state.requirements / [None] | KEEP-NEG | - | refused |
| `X074` | state.requirements / [True] | KEEP-NEG | - | refused |
| `X075` | state.requirements / [7] | KEEP-NEG | - | refused |
| `X076` | state.requirements / [{}] | KEEP-NEG | - | refused |
| `X077` | state.requirements / [[]] | KEEP-NEG | - | refused |
| `X078` | state.requirements / ['bad'] | KEEP-NEG | - | refused |
| `X079` | state.requirements / ['CORE-001'] | KEEP-POS | - | declared ID kind accepted |
| `X080` | state.requirements / ['CORE-001\n'] | FIX | CR-005 | D12: full-match token of the field's own ID kind |
| `X081` | state.requirements / ['NF-001'] | FIX | CR-005 | D12: full-match token of the field's own ID kind |
| `X082` | state.requirements / ['NF-001\n'] | FIX | CR-005 | D12: full-match token of the field's own ID kind |
| `X083` | state.open_findings / [None] | KEEP-NEG | - | refused |
| `X084` | state.open_findings / [True] | KEEP-NEG | - | refused |
| `X085` | state.open_findings / [7] | KEEP-NEG | - | refused |
| `X086` | state.open_findings / [{}] | KEEP-NEG | - | refused |
| `X087` | state.open_findings / [[]] | KEEP-NEG | - | refused |
| `X088` | state.open_findings / ['bad'] | KEEP-NEG | - | refused |
| `X089` | state.open_findings / ['CORE-001'] | FIX | CR-005 | D12: full-match token of the field's own ID kind |
| `X090` | state.open_findings / ['CORE-001\n'] | FIX | CR-005 | D12: full-match token of the field's own ID kind |
| `X091` | state.open_findings / ['NF-001'] | KEEP-POS | - | declared ID kind accepted |
| `X092` | state.open_findings / ['NF-001\n'] | FIX | CR-005 | D12: full-match token of the field's own ID kind |
| `X093` | state.provisionally_closed / [None] | KEEP-NEG | - | refused |
| `X094` | state.provisionally_closed / [True] | KEEP-NEG | - | refused |
| `X095` | state.provisionally_closed / [7] | KEEP-NEG | - | refused |
| `X096` | state.provisionally_closed / [{}] | KEEP-NEG | - | refused |
| `X097` | state.provisionally_closed / [[]] | KEEP-NEG | - | refused |
| `X098` | state.provisionally_closed / ['bad'] | KEEP-NEG | - | refused |
| `X099` | state.provisionally_closed / ['CORE-001'] | FIX | CR-005 | D12: full-match token of the field's own ID kind |
| `X100` | state.provisionally_closed / ['CORE-001\n'] | FIX | CR-005 | D12: full-match token of the field's own ID kind |
| `X101` | state.provisionally_closed / ['NF-001'] | KEEP-POS | - | declared ID kind accepted |
| `X102` | state.provisionally_closed / ['NF-001\n'] | FIX | CR-005 | D12: full-match token of the field's own ID kind |
| `X103` | CLI state validate malformed actor / next_owner=[] | FIX | CR-003 | D13: non-hashable owner -> 'must be a string or null' error, never TypeError |
| `X104` | CLI state validate malformed actor / next_action=[] | KEEP-NEG | - | refused |
| `Z01` | state/CLI remaining input / product-no-cert | KEEP-NEG | - | product closure needs CERTIFIED_CLOSED |
| `Z02` | state/CLI remaining input / product-certified | KEEP-POS | - | certified product closure passes |
| `Z03` | state/CLI remaining input / product-unknown-wp | KEEP-NEG | - | product closure needs CERTIFIED_CLOSED |
| `Z04` | state/CLI remaining input / duplicate-work-package-id | FIX | CR-001 | D2: duplicate work_package (filename != work_package) refused |
| `Z05` | state/CLI remaining input / directory-roundtrip-cli | KEEP-NEG | - | directory state entry fails roundtrip (D3 names the kind) |
| `Z06` | state/CLI remaining input / source-key-traversal | FIX | CR-004 | D14: source key is a full-match token; no write occurs outside reference/source-text |
| `Z07` | state/CLI remaining input / source-key-wrong-type | FIX | CR-004 | D14: source key is a full-match token; no write occurs outside reference/source-text |
| `Z08` | state/CLI remaining input / source-entry-wrong-type | FIX | CR-003 | D13/D14: malformed documents[] entry -> error exit 1 before any write |
| `Z09` | state/CLI remaining input / source-override-hash-fails | KEEP-NEG | - | hash mismatch refuses before writing |
| `Z10` | state/CLI remaining input / path-outside-docs | FIX | CR-006 | D15: with --docs, validate refuses a path outside <docs>/process/state |
| `V01` | CLI path/option interpretation / ['check', '--docs', 'E:\\AI\\Projects | KEEP-NEG | - | documented failure, exit 1 |
| `V02` | CLI path/option interpretation / ['check', '--docs', 'missing', '--cod | KEEP-NEG | - | documented failure, exit 1 |
| `V03` | CLI path/option interpretation / ['check', '--docs', 'E:\\AI\\Projects | KEEP-NEG | - | documented failure, exit 1 |
| `V04` | CLI path/option interpretation / ['check', '--docs', '', '--code', 'E: | KEEP-NEG | - | documented failure, exit 1 |
| `V05` | CLI path/option interpretation / ['check', '--docs', 'E:\\AI\\Projects | KEEP-NEG | - | documented failure, exit 1 |
| `V06` | CLI path/option interpretation / ['check', '--docs=-x', '--code', 'E:\ | KEEP-NEG | - | documented failure, exit 1 |
| `V07` | CLI path/option interpretation / ['sources', 'build', '--docs', 'missi | FIX | CR-003 | D13: sources build with missing --docs -> error exit 1, no exception |
| `V08` | CLI path/option interpretation / ['sources', 'build', '--docs', 'E:\\A | KEEP-POS | - | source build within declared destination succeeds |
| `V09` | CLI path/option interpretation / ['state', 'roundtrip', '--docs', 'mis | KEEP-NEG | - | documented failure, exit 1 |
| `V10` | CLI path/option interpretation / ['state', 'roundtrip', '--docs', 'E:\ | KEEP-NEG | - | documented failure, exit 1 |
| `V11` | CLI path/option interpretation / ['state', 'validate', 'E:\\AI\\Projec | KEEP-NEG | - | documented failure, exit 1 |
| `V12` | CLI path/option interpretation / ['state', 'validate', 'E:\\AI\\Projec | FIX | CR-006 | D15: with --docs, validate refuses a path outside <docs>/process/state |
| `M01` | Git ambient repository selector / GIT_DIR | FIX | CR-002 | D7: validator Git runs in a sanitized environment; result equals the no-environment run (valid world passes) |
| `M02` | Git ambient repository selector / GIT_WORK_TREE | FIX | CR-002 | D7: validator Git runs in a sanitized environment; result equals the no-environment run (valid world passes) |
| `M03` | Git ambient repository selector / GIT_NAMESPACE | KEEP-POS | - | already equals the sanitized result; defensive control only, no kill credit (CH01/CH02 discriminate D7) |
| `M04` | Git ambient repository selector / GIT_OBJECT_DIRECTORY | FIX | CR-002 | D7: validator Git runs in a sanitized environment; result equals the no-environment run (valid world passes) |
| `M05` | local symbolic branch / live symbolic target | POLICY | D5 | symbolic refs/heads entries are refused as candidate refs |
| `M06` | local symbolic branch / dangling symbolic target | KEEP-NEG | - | dangling symbolic ref refused |
| `M07` | Git nonzero exit / 1 | KEEP-NEG | - | nonzero git exit -> documented error |
| `M08` | Git nonzero exit / 128 | KEEP-NEG | - | nonzero git exit -> documented error |
| `P09b` | state inventory filename / 'quote".yaml' deleted | KEEP-NEG | - | W: DIAG; L/C: fails (committed entry missing) and must also name it unsupported |
| `P09c` | state inventory filename / 'quote".yaml' committed deletion | KEEP-POS | - | W: DIAG; L/C: committed deletion passes |
| `P10b` | state inventory filename / 'tab\t.yaml' deleted | KEEP-NEG | - | W: DIAG; L/C: fails (committed entry missing) and must also name it unsupported |
| `P10c` | state inventory filename / 'tab\t.yaml' committed deletion | KEEP-POS | - | W: DIAG; L/C: committed deletion passes |
| `P11b` | state inventory filename / 'line\n.yaml' deleted | KEEP-NEG | - | W: DIAG; L/C: fails (committed entry missing) and must also name it unsupported |
| `P11c` | state inventory filename / 'line\n.yaml' committed deletion | KEEP-POS | - | W: DIAG; L/C: committed deletion passes |
| `P12b` | state inventory filename / 'NUL.yaml' deleted | KEEP-NEG | - | W: DIAG; L/C: fails (committed entry missing) and must also name it unsupported |
| `P12c` | state inventory filename / 'NUL.yaml' committed deletion | KEEP-POS | - | W: DIAG; L/C: committed deletion passes |
| `P13b` | state inventory filename / 'CON.yaml' deleted | KEEP-NEG | - | W: DIAG; L/C: fails (committed entry missing) and must also name it unsupported |
| `P13c` | state inventory filename / 'CON.yaml' committed deletion | KEEP-POS | - | W: DIAG; L/C: committed deletion passes |
| `P16b` | state inventory filename / 'nul\x00.yaml' deleted | DIAG | - | NUL cannot occur in a Git or host filename on any host |
| `P16c` | state inventory filename / 'nul\x00.yaml' committed deletion | DIAG | - | NUL cannot occur in a Git or host filename on any host |
| `D01` | committed raw filename / b'NUL.yaml' | KEEP-NEG | - | committed non-canonical names fail; D1 names them unsupported with exact identity |
| `D02` | committed raw filename / b'quote".yaml' | KEEP-NEG | - | committed non-canonical names fail; D1 names them unsupported with exact identity |
| `D03` | committed raw filename / b'line\n.yaml' | KEEP-NEG | - | committed non-canonical names fail; D1 names them unsupported with exact identity |
| `D04` | committed raw filename / b'\xff.yaml' | KEEP-NEG | - | non-UTF-8 committed name -> listing failure, fail closed |
| `F01` | remaining resolution/IO binding / tracked-directory-yaml | FIX | CR-003 | D3/D13: tracked directory named *.yaml -> unsupported-kind error, never an exception |
| `F02` | remaining resolution/IO binding / cli-invalid-utf8 | KEEP-NEG | - | documented failure |
| `F03` | remaining resolution/IO binding / alternate-docs-root | KEEP-NEG | - | documented failure |
| `F04` | remaining resolution/IO binding / head-moves-after-verification | FIX | CR-002 | D8: revision resolved once to an OID; inventory and every blob read use that OID |
| `F05` | remaining resolution/IO binding / state-moves-after-validation | FIX | CR-002 | D9: one load per state file per check; downstream checks use the validated object |
| `F06` | remaining resolution/IO binding / linear-chain-merge | FIX | CR-002 | D10: every commit in candidate..tip has exactly one parent (linear chain) |
| `F07` | remaining resolution/IO binding / unborn-head | KEEP-NEG | - | documented failure |
| `F08` | remaining resolution/IO binding / bare-repository | FIX | CR-006 | D15: roundtrip first verifies docs is a non-bare working-tree root; diagnostic names that |
| `Q01` | canonical Git graph / replace-parent | FIX | CR-002 | D7: replace refs, GIT_REPLACE_REF_BASE and info/grafts can never create ancestry |
| `Q02` | canonical Git graph / grafts-parent | FIX | CR-002 | D7: replace refs, GIT_REPLACE_REF_BASE and info/grafts can never create ancestry |
| `Q03` | state.schema_version exact type / 2.0 | FIX | CR-005 | D11: schema_version is the integer 2 (type int, not bool/float) |
| `Q04` | state.schema_version exact type / True | KEEP-NEG | - | refused |
| `Q05` | state.schema_version exact type / '2' | KEEP-NEG | - | refused |
| `Q06` | state.schema_version exact type / '2\n' | KEEP-NEG | - | refused |
| `Q07` | state.schema_version exact type / 2 | KEEP-POS | - | integer 2 accepted |
| `Q08` | state ID full token / 'CORE-٠٠١' | FIX | CR-005 | D12: IDs are full-match ASCII tokens |
| `Q09` | state ID full token / 'NF-٠٠١' | FIX | CR-005 | D12: IDs are full-match ASCII tokens |
| `Q10` | state ID full token / 'NF-001\n' | FIX | CR-005 | D12: IDs are full-match ASCII tokens |
| `U01` | state-only changed-path comparison / 'process/state/extra.yaml' | KEEP-POS | - | permitted state-only paths pass the chain rule |
| `U02` | state-only changed-path comparison / 'process/handoffs/x.md' | KEEP-POS | - | permitted state-only paths pass the chain rule |
| `U03` | state-only changed-path comparison / 'process/certification-registry.y | KEEP-POS | - | permitted state-only paths pass the chain rule |
| `U04` | state-only changed-path comparison / 'process/stateevil/x.yaml' | KEEP-NEG | - | non-state path anywhere in the chain fails (per commit, incl. reverted) |
| `U05` | state-only changed-path comparison / 'process/state/quote".yaml' | KEEP-POS | - | W: DIAG (unrepresentable); L/C: chain rule is path-prefix only; the name is refused by inventory rule D1, not the chain |
| `U06` | state-only changed-path comparison / 'process/state/line\n.yaml' | KEEP-POS | - | W: DIAG (unrepresentable); L/C: chain rule is path-prefix only; the name is refused by inventory rule D1, not the chain |
| `U07` | state-only changed-path comparison / 'process/state/Unicode-Ü.yaml' | KEEP-POS | - | accepted on W/L/C: chain rule is path-prefix only; the name is refused by inventory rule D1, not the chain |
| `U08` | state-only changed-path comparison / 'other/line\n.md' | KEEP-NEG | - | W: DIAG; L/C: non-state path fails with exact identity |
| `U09` | state-only changed-path comparison / 'other/quote".md' | KEEP-NEG | - | W: DIAG; L/C: non-state path fails with exact identity |
| `U10` | state-only changed-path comparison / 'other/Unicode-Ü.md' | KEEP-NEG | - | non-state path anywhere in the chain fails (per commit, incl. reverted) |
| `U11` | state-only per-commit comparison / nonstate change then revert | KEEP-NEG | - | non-state path anywhere in the chain fails (per commit, incl. reverted) |
| `U12` | case-sensitive inventory identity / two tracked names A.yaml and a.yam | FIX | CR-001 | D1/D2: 'A.yaml'/'a.yaml' are not <WP-ID>.yaml -> error on every host (today C passes) |
| `U13` | transition-check evidence boundary / BLOCKED_FOR_OWNER -> SCOPING | LIMIT | - | transition-check proves edge legality only; it never proves authority/trigger (documented, exit codes kept) |
| `U14` | transition-check evidence boundary / CONTRACT_CONVERGENCE -> FINAL_CON | LIMIT | - | transition-check proves edge legality only; it never proves authority/trigger (documented, exit codes kept) |
| `U15` | transition-check evidence boundary / WAITING_FOR_TRIGGER -> SCOPING | LIMIT | - | transition-check proves edge legality only; it never proves authority/trigger (documented, exit codes kept) |
| `U16` | transition-check evidence boundary / INCIDENT -> SCOPING | LIMIT | - | transition-check proves edge legality only; it never proves authority/trigger (documented, exit codes kept) |
| `U17` | transition-check evidence boundary / INVALID_UNAUTHORIZED -> SCOPING | LIMIT | - | transition-check proves edge legality only; it never proves authority/trigger (documented, exit codes kept) |
| `N01` | status routing evidence / INCIDENT.next_action='do something' | FIX | CR-005 | D12: INCIDENT/INVALID_UNAUTHORIZED require next_owner and next_action null |
| `N02` | status routing evidence / INVALID_UNAUTHORIZED.next_action='do somethi | FIX | CR-005 | D12: INCIDENT/INVALID_UNAUTHORIZED require next_owner and next_action null |
| `N03` | status routing evidence / WAITING_FOR_TRIGGER.deferred_trigger=True | FIX | CR-005 | D12: deferred_trigger is a non-blank string (True / list / blank refused) |
| `N04` | status routing evidence / WAITING_FOR_TRIGGER.deferred_trigger=['trigg | FIX | CR-005 | D12: deferred_trigger is a non-blank string (True / list / blank refused) |
| `N05` | status routing evidence / WAITING_FOR_TRIGGER.deferred_trigger='   ' | FIX | CR-005 | D12: deferred_trigger is a non-blank string (True / list / blank refused) |
| `N06` | status routing evidence / CONTRACT_CONVERGENCE.convergence={'episode': | FIX | CR-005 | D12: convergence.episode non-blank token; open_findings non-empty list of finding IDs |
| `N07` | status routing evidence / SCOPING.next_action='   ' | KEEP-NEG | - | blank next_action refused |
| `N08` | status routing evidence / BLOCKED_FOR_OWNER.governance_source=None | OPAQUE | - | governance_source carries no machine authority (documented) |
| `J01` | state-only exact file/domain identity / process/certification-registry | FIX | CR-002 | D10: registry is the exact path process/certification-registry.yaml |
| `J02` | state-only exact file/domain identity / process/certification-registry | FIX | CR-002 | D10: registry is the exact path process/certification-registry.yaml |
| `J03` | state-only exact file/domain identity / process/state-extra/file.yaml | KEEP-NEG | - | directory look-alike refused |
| `J04` | state-only exact file/domain identity / process/handoffs-extra/file.md | KEEP-NEG | - | directory look-alike refused |
| `J05` | symbolic local ref namespace / heads/symbolic -> tags/target-tag | FIX | CR-002 | D5: symbolic refs refused (so heads/x -> tags/y cannot be followed) |
| `J06` | roundtrip revision namespace / matching matching-tag | FIX | CR-002 | D8: roundtrip refuses tag (J06), abbreviation without a local head (J07), qualified remote spelling (J08) |
| `J07` | roundtrip revision namespace / matching 8-hex HEAD abbreviation | FIX | CR-002 | D8: roundtrip refuses tag (J06), abbreviation without a local head (J07), qualified remote spelling (J08) |
| `J08` | roundtrip revision namespace / matching refs/remotes/origin/matching | FIX | CR-002 | D8: roundtrip refuses tag (J06), abbreviation without a local head (J07), qualified remote spelling (J08) |
| `P01p` | state inventory / 'WP-U.yaml' with work_package WP-U | KEEP-POS | - | matching-ID canonical file: roundtrip [] and check_state [] (new positive) |
| `CH01` | env / GIT_CEILING_DIRECTORIES hides containing repo | FIX | CR-002 | D7: containing repository still refused |
| `CH02` | env / GIT_REPLACE_REF_BASE hidden replacement | FIX | CR-002 | D7: orphan-main CLOSED still refused |
| `CH03` | graph / info/grafts with --no-replace-objects only | FIX | CR-002 | D7: graft cannot create ancestry (GIT_GRAFT_FILE disabled + refusal) |
| `CH04` | graph / shallow boundary removes true ancestry | FIX | CR-002 | D7: shallow repository refused with named diagnostic (Codex CP-CH04-corrected) |
| `CH05` | blob read / textconv + smudge configured | KEEP-POS | - | raw blob bytes unchanged (git-level; not a gap) |
| `CH06` | repos / nested .git FILE in a docs subdirectory | KEEP-NEG | - | refused as nested repository (executed: refused today; must stay refused) |
| `CH07` | sources build / valid first entry, bad hash on later entry | FIX | CR-004 | D14: exit 1; every destination and index byte unchanged; no new output (Codex CP-later-entry-corrected) |
| `CH08` | sources build / all-valid multi-entry | KEEP-POS | - | exit 0; one derived text per entry plus index |
| `CH09` | roundtrip / local branch named 'deadbeef' | KEEP-POS | - | plain local branch accepted (resolved as refs/heads/deadbeef), equal content passes |
| `CH10` | roundtrip / spelling 'refs/heads/wp/test' | POLICY | D8 | accepted today; D8 refuses qualified spellings (plain names only) |
| `CH11` | sources build / all twelve bundle keys + DOC | KEEP-POS | - | D14 key grammar [A-Z][A-Z0-9]{0,15} accepts every established key |
