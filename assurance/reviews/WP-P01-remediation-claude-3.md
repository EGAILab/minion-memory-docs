# WP-P01 — Remediation 3: implementation of the agreed CE-P01-01 checkpoint (Claude)

**Governs:** G-018. **Checkpoint:** `assurance/convergence/CE-P01-01-classification.md`, revision 2
(`cb7977f4`), AGREED FOR IMPLEMENTATION by Codex `APPROVED` (`1845aa9b`). This is a single
implementation pass. It is not a review, not a closure claim and not acceptance. Targeted closure
of WPP01-CR-001…006 is Codex's.

## Scope implemented

The changed surface is the four production modules the agreed decisions touch:
- `checks.py`
- `cli.py`
- `spec.py`, which now holds the D16 inventory walker.

`yamlcore.py`, `transitions.py` and `sources.py` are unchanged.

Supporting changes:
- `process/coordination-state.md` §2–§4 now state D1–D16, so the written contract and the
  validator move together.
- The tests changed as listed under "Test changes".

| Decision | Where |
|---|---|
| D1–D3 state inventory, kinds | `checks._state_working`, `checks._state_committed` (shared by `check_state` and `state_roundtrip`) |
| D2 identity gates | `checks._state_file` (file-aware); `validate_state` stays pure-object |
| D4 transport | `checks._nul_records`, `checks._git_paths` |
| D5/D6/D8 refs, object kind, one resolution | `checks.plain_branch`, `_local_head`, `_object_type`, `_resolve_revision` |
| D7 hermetic Git | `checks._git_env`, `_run_git`, `_graph_overlays` (via `--git-common-dir`; linked roots supported) |
| D9 one load | `check_state` uses the object returned by `_state_file` |
| D10 chain | `_state_only_chain` (parents per commit, exact registry path) |
| D11/D12 tokens, evidence | `validate_state`, `is_requirement_id`, `is_finding_id`, `WP_ID` |
| D13 totality | type before membership; IO/kind failures reported; `sources build` has no raises |
| D14 producer | `cli._sources_plan` (preflight), staged write + `_replace`; `checks.source_entry_errors`, `safe_relative_file` |
| D15 CLI scope | `--only` with `nargs="+"`; `_state_file` containment; `_working_root` |
| D16 inventories | `spec.inventory` for findings, spec, source text and conformance; the nested-repository scan is unchanged (it already matched D16) |

One deviation was caught and corrected before testing. My first draft pointed `GIT_GRAFT_FILE` at an
`os.devnull`-based path. The agreed text says "a non-existent path inside the project `.tmp`", so it
now uses `<workspace>/.tmp/mneme-process/no-grafts/absent`. If that path ever exists, the repository
is refused as an overlay.

## Controls and kill evidence

`process/tools/tests/test_ce_p01_01.py` has 115 tests. Every test ID starts with its matrix row.

| Run | Code under test | Result |
|---|---|---|
| Implementation, new controls | this candidate | 110 passed, 5 skipped |
| Implementation, full suite | this candidate | **255 passed, 5 skipped**, no warnings |
| Kill run, new controls | frozen modules, byte-identical to `1422423e` (detached worktree at `0ea471f`) | **100 failed, 10 passed, 5 skipped** |
| Real repositories | `check --deep-sources` on this docs tree plus code `main` | 8/8 PASS; state roundtrip OK |

Accounting follows checkpoint §5:
- **Passing on the frozen code.** All 10 are regression controls with unchanged oracles: S330,
  three declared-ID-kind positives, the string trigger, P01p, CH06, CH09, E10 and CH08. **No FIX
  or POLICY control passes on the frozen code.**
- **Failing on the frozen code.** 98 failing tests are kill-credited FIX controls or deliberate
  POLICY changes (C05, G02, M05, CH10).
  - Two more failures are **not** kill-credited: CH11, the key grammar, and the injected
    replace-failure limit. Both test helpers that are new in this implementation, so they fail on
    the frozen code only because the helpers don't exist there.
  - Rows sharing one oracle share a parametrized test, so test counts are not row counts.
- **Skipped (DIAG).** The 5 skips are rows P09a–P13a on Windows: `quote"`, tab, newline, `NUL`
  and `CON` names cannot be created. They are skipped with a recorded reason and never counted.
  Their POSIX cells are executable as written.
- **Not yet executed.** The POSIX/case-sensitive host run of these controls has not been executed
  in this pass. That is stated, not claimed.

## Test changes to pre-existing tests (oracle changes the checkpoint requires)

- `test_wpp01_r2_unicode_state_inventory_matches` became `…_unicode_state_name_is_named_in_both_views`.
  Under D1 (row P06a), `WP-Ü.yaml` is an unsupported entry. The test now asserts that the exact
  decoded name is reported in both views, so the lossless-transport purpose is kept.
- `…_unicode_state_uncommitted_deletion_is_caught`: the oracle now names the committed
  unsupported entry.
- `…_unicode_state_path_counts_as_state_only` became `…_unicode_state_only_path_…`. Lossless
  `diff-tree` decoding is now shown with a non-ASCII hand-off path, which stays state-only.
- `test_wpp01_r2_roundtrip_rejects_bad_revision[nope]` also accepts the D8 refusal wording
  "is not a local branch".
- `conftest.py`: `MNEME_CODE_REPO` optionally names the code repository, for docs worktrees that
  are not its sibling (the default is unchanged). The fixture `git()` now decodes UTF-8, which
  removes a code-page reader-thread warning on non-ASCII names.

## Convergence records carried into this candidate

These records lived on review branches and are now part of this candidate:
- the characterization (`281b81a`);
- the classification, revision 2 (`cb7977f`);
- both Codex checkpoint reviews (`8420760`, `1845aa9b`).

Including them keeps the state-only descendant rule intact for the new candidate.
