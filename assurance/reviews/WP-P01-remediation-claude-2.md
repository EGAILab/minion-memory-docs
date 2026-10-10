# WP-P01 remediation 2 — Claude response to Codex targeted closure review 1

**Reviewed candidate:** docs `cd8288384473ab32472629fbbc7e37d5ec2cbf26` / code `bb05e395` (= `main`).
**Review consumed:** `assurance/reviews/WP-P01-targeted-closure-codex-1.md` (branch
`review/wpP01-codex-2` @ `869fa5734bf47c39c751cead34c6a1065e4f9237`, fast-forwarded into
`wpP01/hardening`). Verdict `CHANGES_REQUIRED`: WPP01-CR-001 and WPP01-CR-002 open with refined
witnesses; WP00-CR-014 provisionally closed.

## 1. Convergence trigger check and route decision (recorded before remediating)

- **Trigger A HAS fired** for WPP01-CR-001 and WPP01-CR-002: each survived two independent reviews.
- Trigger B: not fired (refined witnesses of the same findings, no differently numbered successors).
- Trigger C: not fired (one rejected complete review + one rejected targeted review).

Convergence is the default. WP-P01 is in `SCOPING`, where `CONTRACT_CONVERGENCE` is not a legal
transition, but that is not the reason for the route chosen. The reason is the observed pattern:
each point fix exposed the next edge of the **same surface** — the validator's trust in git output
and in state-record fields. That is the condition convergence exists to stop, so this pass does the
convergence-style work inside the legal route: **characterize the whole surface first, then fix it
once.** If either finding survives the next independent review, Claude stops and routes the
decision to the Owner rather than attempting another remediation.

## 2. Characterization — every validator input that reaches git or comes from a state record

| # | Input | Before | Classification | After |
|---|---|---|---|---|
| 1 | `ls-tree --name-only` (round-trip inventory) | `core.quotePath` display quoting kept quoted non-ASCII names out of the inventory | **WPP01-CR-001** (reproduced: `WP-Ü.yaml` matched → false "uncommitted"; uncommitted deletion → `[]`) | `ls-tree -z`, NUL-split raw bytes, strict UTF-8 decode (`_git_paths`) |
| 2 | `diff-tree --name-only` (state-only chain) | same quoting; a non-ASCII **state** path was misread as non-state (fails closed but wrongly) | same root cause as #1 (swept) | `diff-tree -z` via `_git_paths` |
| 3 | `current_candidate.<side>.repo` | record chose the repository for either side | **WPP01-CR-002** (reproduced: both sides = accepted code record → `{}`) | sides bound: `code → minion-memory`, `docs → minion-memory-docs`; resolved from the side |
| 4 | `current_candidate.<side>.ref` | any string passed to git: SHA, `HEAD`, range, option-like | **new, found by Claude's sweep**: `ref` = candidate SHA empties `D..ref` and bypasses the state-only rule (reproduced on active state → `{}`); option-like refs reach git argv | plain branch-name grammar, not SHA-shaped, must exist as `refs/heads/<ref>`; `CLOSED` requires `main` |
| 5 | `roundtrip --revision` (CLI) | passed to git unvalidated | same class as #4 (swept) | `HEAD`, 40-hex SHA or plain branch name; must resolve `^{commit}` |
| 6 | `rev-parse --show-toplevel`, `rev-list`, `merge-base --is-ancestor`, `cat-file -e`, blob `git show` | hex/no-output/raw bytes | AUDITED — no display transformation reaches a comparison | unchanged |
| 7 | Working-tree file names vs committed names | compared as Python `str` | Unicode normalization (NFC vs NFD) would matter on macOS only | DEFERRED_WITH_REASON — no macOS host in scope (Windows/Linux preserve names); trigger: first macOS gate run |
| 8 | `_git` text decoding | already explicit UTF-8 (WP-P01) | AUDITED | unchanged |

Rule #4 is a new finding of the same class; it is fixed in this pass rather than left for review.

## 3. Controls

All repository-level controls run in the fixture with `core.quotePath=true` pinned (host-independent),
baseline asserted first.

| Control | Kind |
|---|---|
| non-ASCII state: matching inventory passes | positive (old: false "uncommitted") |
| non-ASCII state: uncommitted deletion caught | negative (old: silent `[]`) |
| non-ASCII state path after candidate counts as state-only | positive (old: false non-state) |
| sides both-code / both-docs / swapped caught | negative ×3 |
| ref = SHA / `HEAD~0` / `--output=x` / range / nonexistent branch caught | negative ×5 |
| ref = candidate SHA cannot bypass the chain rule | negative (the sweep witness) |
| CLOSED with ref ≠ `main` caught | negative |
| `roundtrip --revision` `-x` / `--output=x` / range / unknown rejected | negative ×4 |
| closure positive now uses the correct form (`ref: main`); "not accepted on main" negative uses an orphan `main` so it tests acceptance, not ref existence | fixture correction |

Known-bad replay results (against `cd828838` `checks.py`) are recorded in the hand-off.

## 4. Process lesson

Point fixes to a trust boundary invite successor findings. When a validator consumes external
output or caller-supplied fields, characterize every input against display transformations,
binding and option-injection before fixing any one of them. Added as a hazard-family member in a
later process pass (not in this candidate, to keep it bounded).

## 5. Known-bad replay (against `cd828838` `checks.py`, restored and verified with `cmp`)

`uv run pytest -o addopts="-p no:cacheprovider" -q -k wpp01_r2` on the old tooling: **17 failed**.
Failure reasons inspected (not assumed):

- **Discriminating (10)** — the old tooling accepted the bad input: non-ASCII inventory match,
  non-ASCII uncommitted deletion, non-ASCII state path after candidate; sides both-code, both-docs,
  swapped; ref = SHA; ref = `HEAD~0`; ref = candidate SHA bypassing the chain rule; CLOSED with
  ref ≠ `main`.
- **Diagnostic-only (7)** — the old tooling already failed closed with a different message, so
  these are regression coverage, not counted as kills: refs `--output=x`, `wp/test..main`,
  `no-such-branch` (old: "not reachable from …" / "cannot list commits …"); roundtrip revisions
  `-x`, `--output=x`, `HEAD..main`, `nope` (old: "cannot list committed state files in …").

Full suite on the fixed tooling: 145 passed.
