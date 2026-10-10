"""CE-P01-01 agreed checkpoint controls (assurance/convergence/CE-P01-01-classification.md, rev. 2).

Every test id starts with its matrix row. FIX rows are kill-credited: the frozen tooling
(docs 1422423e) produces the recorded wrong result and fails the control. POLICY rows show a
deliberate change. KEEP rows added by the checkpoint (P01p, E10, CH05, CH06, CH08, CH09, CH11)
are regression controls with unchanged oracles. Host-unrepresentable inputs skip with a recorded
reason (DIAG) and are never counted.
"""

from __future__ import annotations

import copy
import os
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
import yaml
from conftest import GIT_ENV, World, dump, git

from mneme_process import checks, cli, sources

WINDOWS = sys.platform == "win32"
STATE = checks.STATE_DIR


# --------------------------------------------------------------------------- helpers


def base_state(**overrides: Any) -> dict[str, Any]:
    """A valid pure-object state (validate_state never consults Git)."""
    workflow: dict[str, Any] = {
        "schema_version": 2,
        "work_package": "WP-T",
        "status": "SCOPING",
        "requirements": [],
        "current_candidate": None,
        "open_findings": ["NF-001"],
        "provisionally_closed": [],
        "quarantine": {"derived_from_quarantined_artifact": False},
        "next_owner": "Codex",
        "next_action": "review",
    }
    workflow.update(overrides)
    return {"workflow": workflow}


def object_errors(**overrides: Any) -> list[str]:
    return checks.validate_state(base_state(**overrides), "probe.yaml")


def git_input(repo: Path, data: bytes, *args: str) -> str:
    done = subprocess.run(
        ["git", "-C", str(repo), *args], input=data, capture_output=True, env=GIT_ENV, check=True
    )
    return done.stdout.decode("utf-8").strip()


def orphan_main(repo: Path) -> str:
    tree = git_input(repo, b"", "mktree")
    oid = git(repo, "commit-tree", tree, "-m", "orphan main")
    git(repo, "branch", "-f", "main", oid)
    return oid


def closed_state(world: World) -> dict[str, Any]:
    state = world.state(
        status="CLOSED",
        open_findings=[],
        next_owner=None,
        next_action=None,
        scoping_review={"outcome": "APPROVED", "verdict": "APPROVED", "source": "fixture"},
    )
    for side in ("code", "docs"):
        state["workflow"]["current_candidate"][side]["ref"] = "main"
    return state


def write_closed_with_orphan_mains(world: World) -> dict[str, str]:
    """CLOSED evidence whose candidates are NOT on the (orphan) mains: must always be refused."""
    orphans = {}
    for side, repo in (("code", world.code), ("docs", world.docs)):
        orphans[side] = orphan_main(repo)
    dump(world.docs / STATE / "WP-T.yaml", closed_state(world))
    errors = world.all_errors().get("state", [])
    assert any("not accepted on main" in e for e in errors), errors  # baseline refusal
    return orphans


def candidate(world: World, side: str) -> str:
    """The candidate recorded in the current state file (not a recomputed HEAD)."""
    recorded = yaml.safe_load((world.docs / STATE / "WP-T.yaml").read_text(encoding="utf-8"))
    return str(recorded["workflow"]["current_candidate"][side]["sha"])


def committed_state_names(world: World) -> list[str]:
    """Raw NUL-delimited UTF-8 listing: no code-page decoding, no stripping."""
    done = subprocess.run(
        ["git", "-C", str(world.docs), "ls-tree", "-z", "--name-only", f"HEAD:{STATE}"],
        capture_output=True,
        env=GIT_ENV,
        check=True,
    )
    return [n.decode("utf-8") for n in done.stdout.split(b"\0") if n]


def state_errors(world: World) -> list[str]:
    return world.all_errors().get("state", [])


def add_state_entry(world: World, name: str, content: str | None = None) -> Path:
    path = world.docs / STATE / name
    try:
        path.write_text(
            content or yaml.safe_dump(world.state(work_package="WP-U")), encoding="utf-8", newline="\n"
        )
    except (OSError, ValueError) as error:
        pytest.skip(f"DIAG: host cannot materialize {name!r} ({error})")
    return path


def symlink_or_skip(link: Path, target: Path | str) -> None:
    try:
        os.symlink(target, link)
    except (OSError, NotImplementedError) as error:
        pytest.skip(f"DIAG: host cannot create symlinks ({error})")


def assert_named(errors: list[str], name: str, *fragments: str) -> None:
    assert any(repr(name) in e and all(f in e for f in fragments) for e in errors), errors


# --------------------------------------------------------- S / X / Q / N : exact shapes, totality


@pytest.mark.parametrize(
    ("row", "overrides"),
    [
        ("S052", {"next_owner": {}}),
        ("S053", {"next_owner": []}),
        ("S239", {"status": "SCOPING", "next_owner": {}}),
        ("S240", {"status": "SCOPING", "next_owner": []}),
        ("S275", {"status": "BLOCKED_FOR_OWNER", "next_owner": {}}),
        ("S276", {"status": "BLOCKED_FOR_OWNER", "next_owner": []}),
        (
            "S287",
            {
                "status": "CONTRACT_CONVERGENCE",
                "next_owner": {},
                "convergence": {"episode": "CE", "open_findings": ["NF-001"]},
            },
        ),
        (
            "S288",
            {
                "status": "CONTRACT_CONVERGENCE",
                "next_owner": [],
                "convergence": {"episode": "CE", "open_findings": ["NF-001"]},
            },
        ),
    ],
)
def test_unhashable_owner_is_a_shape_error_never_a_raise(row: str, overrides: dict[str, Any]) -> None:
    """D13 (CR-003): membership is tested only after the type test."""
    errors = object_errors(**overrides)
    assert any("next_owner must be a string or null" in e for e in errors), (row, errors)


def _convergence(episode: Any = "CE-P01-01", findings: Any = None) -> dict[str, Any]:
    return {
        "status": "CONTRACT_CONVERGENCE",
        "convergence": {"episode": episode, "open_findings": ["NF-001"] if findings is None else findings},
    }


@pytest.mark.parametrize(
    ("row", "overrides"),
    [
        ("S326", _convergence(episode=True)),
        ("S329", _convergence(episode=7)),
        ("S333", _convergence(findings=True)),
        ("S336", _convergence(findings=7)),
        ("S337", _convergence(findings="finding")),
        ("N06", _convergence(episode="   ", findings=["bad"])),
    ],
)
def test_convergence_evidence_has_exact_shape(row: str, overrides: dict[str, Any]) -> None:
    """D12 (CR-005): truthy wrong types are not convergence evidence."""
    assert any("CONTRACT_CONVERGENCE needs" in e for e in object_errors(**overrides)), row


def test_S330_nonblank_episode_string_is_valid_evidence() -> None:
    assert object_errors(**_convergence(episode="finding")) == []


@pytest.mark.parametrize(
    ("row", "key", "value"),
    [
        ("X080", "requirements", ["CORE-001\n"]),
        ("X081", "requirements", ["NF-001"]),
        ("X082", "requirements", ["NF-001\n"]),
        ("Q08", "requirements", ["CORE-\u0660\u0660\u0661"]),  # Arabic-Indic digits
        ("X089", "open_findings", ["CORE-001"]),
        ("X090", "open_findings", ["CORE-001\n"]),
        ("X092", "open_findings", ["NF-001\n"]),
        ("Q09", "open_findings", ["NF-\u0660\u0660\u0661"]),  # Arabic-Indic digits
        ("Q10", "open_findings", ["NF-001\n"]),
        ("X099", "provisionally_closed", ["CORE-001"]),
        ("X100", "provisionally_closed", ["CORE-001\n"]),
        ("X102", "provisionally_closed", ["NF-001\n"]),
    ],
)
def test_ids_are_full_ascii_tokens_of_their_own_kind(row: str, key: str, value: list[str]) -> None:
    """D11/D12 (CR-005)."""
    assert any(f"{key} element" in e for e in object_errors(**{key: value})), row


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("requirements", ["CORE-001"]),
        ("open_findings", ["NF-001", "WPP01-CR-006"]),
        ("provisionally_closed", ["NF-001"]),
    ],
)
def test_declared_id_kinds_remain_valid(key: str, value: list[str]) -> None:
    assert object_errors(**{key: value}) == []


def test_Q03_schema_version_is_the_integer_2() -> None:
    assert any("schema_version must be 2" in e for e in object_errors(schema_version=2.0))


def test_X008_work_package_is_a_wp_id_token() -> None:
    assert any("work_package must be a WP-ID token" in e for e in object_errors(work_package="text"))


@pytest.mark.parametrize(("row", "status"), [("N01", "INCIDENT"), ("N02", "INVALID_UNAUTHORIZED")])
def test_non_actionable_status_carries_no_action(row: str, status: str) -> None:
    errors = object_errors(status=status, next_owner=None, next_action="do something")
    assert any("authorizes no owner/action" in e for e in errors), row


@pytest.mark.parametrize(("row", "trigger"), [("N03", True), ("N04", ["trigger"]), ("N05", "   ")])
def test_deferred_trigger_is_a_nonblank_string(row: str, trigger: Any) -> None:
    errors = object_errors(
        status="WAITING_FOR_TRIGGER", next_owner=None, next_action=None, deferred_trigger=trigger
    )
    assert any("WAITING_FOR_TRIGGER needs" in e for e in errors), row


def test_string_deferred_trigger_remains_valid() -> None:
    """CE1-CP-003: the established string domain is kept (S229/S258)."""
    assert (
        object_errors(status="WAITING_FOR_TRIGGER", next_owner=None, next_action=None, deferred_trigger="t")
        == []
    )


def test_X103_cli_validate_reports_unhashable_owner(world: World) -> None:
    world.write_state(next_owner=[])
    assert cli.main(["state", "validate", str(world.docs / STATE / "WP-T.yaml")]) == 1


# -------------------------------------------------------------- P / K / U / Z04 : state inventory

STATE_NAMES = [
    ("P02", "WP-UP.YAML"),
    ("P03", "WP-Mix.YaMl"),
    ("P04", ".hidden.yaml"),
    ("P05", " leading.yaml"),
    ("P06", "WP-Ü.yaml"),
    ("P07", "WP-é.yaml"),
    ("P08", "WP-é.yaml"),
    ("P09", 'quote".yaml'),
    ("P10", "tab\t.yaml"),
    ("P11", "line\n.yaml"),
    ("P12", "NUL.yaml"),
    ("P13", "CON.yaml"),
    ("P14", "trail .yaml"),
    ("P15", "trailing.yaml "),
]


@pytest.mark.parametrize(("row", "name"), STATE_NAMES, ids=[f"{r}a" for r, _ in STATE_NAMES])
def test_noncanonical_state_entry_is_reported_in_both_views(world: World, row: str, name: str) -> None:
    """D1 (CR-001), `a` variant: a matching non-canonical entry is an error on every host."""
    if WINDOWS and row in ("P09", "P10", "P11", "P12", "P13"):
        pytest.skip(f"DIAG: Windows cannot materialize {name!r}")
    add_state_entry(world, name)
    world.commit_all(world.docs, "non-canonical state entry")
    actual = next(n for n in committed_state_names(world) if n != "WP-T.yaml")  # host may alter it
    roundtrip = checks.state_roundtrip(world.docs)
    assert_named(roundtrip, actual, "committed in")
    assert any("unsupported state entry" in e for e in state_errors(world)), state_errors(world)


@pytest.mark.parametrize(
    ("row", "name"), [("P02b", "WP-UP.YAML"), ("P03b", "WP-Mix.YaMl"), ("P15b", "trailing.yaml ")]
)
def test_deleted_noncanonical_committed_entry_fails_roundtrip(world: World, row: str, name: str) -> None:
    path = add_state_entry(world, name)
    world.commit_all(world.docs, "non-canonical state entry")
    actual = next(n for n in committed_state_names(world) if n != "WP-T.yaml")
    path.unlink() if path.exists() else (world.docs / STATE / actual).unlink()
    assert_named(checks.state_roundtrip(world.docs), actual, "committed in")


def test_P01a_file_identity_is_enforced_by_file_aware_gates_only(world: World) -> None:
    """D2 (CR-001): roundtrip proves equality only; check_state / validate_state_file refuse."""
    add_state_entry(world, "WP-U.yaml", yaml.safe_dump(world.state(work_package="WP-X")))
    world.commit_all(world.docs, "WP-X in WP-U.yaml")
    assert checks.state_roundtrip(world.docs) == []
    assert any("does not equal the file stem" in e for e in state_errors(world))
    errors = checks.validate_state_file(world.docs / STATE / "WP-U.yaml", world.docs)
    assert any("does not equal the file stem" in e for e in errors)
    assert checks.validate_state(world.state(work_package="WP-X"), "WP-U.yaml") == []  # pure label


def test_P01p_matching_identity_passes_every_gate(world: World) -> None:
    add_state_entry(world, "WP-U.yaml", yaml.safe_dump(world.state(work_package="WP-U")))
    world.commit_all(world.docs, "WP-U")
    assert checks.state_roundtrip(world.docs) == []
    assert "state" not in world.all_errors()


def test_Z04_duplicate_work_package_is_refused(world: World) -> None:
    add_state_entry(world, "WP-U.yaml", yaml.safe_dump(world.state(work_package="WP-T")))
    world.commit_all(world.docs, "duplicate")
    assert any("does not equal the file stem" in e for e in state_errors(world))


def test_K08_duplicate_under_a_non_canonical_name_is_refused(world: World) -> None:
    add_state_entry(world, "DUP.yaml", yaml.safe_dump(world.state()))
    world.commit_all(world.docs, "dup")
    assert_named(state_errors(world), "DUP.yaml", "unsupported state entry")


def test_K02_nested_state_is_refused(world: World) -> None:
    dump(world.docs / STATE / "sub" / "WP-N.yaml", world.state(work_package="WP-N"))
    world.commit_all(world.docs, "nested")
    assert_named(state_errors(world), "sub", "directory")
    assert_named(checks.state_roundtrip(world.docs), "sub", "directory", "committed in")


@pytest.mark.parametrize("row", ["K05", "K07"])
def test_symlink_state_entry_is_refused(world: World, tmp_path: Path, row: str) -> None:
    """D3 (CR-001): a symlink is never followed, from check_state as well as roundtrip."""
    target = world.docs / STATE / "WP-T.yaml" if row == "K05" else tmp_path / "outside.yaml"
    if row == "K07":
        target.write_text(yaml.safe_dump(world.state(work_package="WP-L")), encoding="utf-8")
    symlink_or_skip(world.docs / STATE / "WP-L.yaml", target)
    assert_named(state_errors(world), "WP-L.yaml", "symlink")


def test_K06_dangling_symlink_is_reported_not_raised(world: World) -> None:
    symlink_or_skip(world.docs / STATE / "WP-L.yaml", world.docs / "nowhere.yaml")
    assert_named(state_errors(world), "WP-L.yaml", "symlink")
    assert any("WP-L.yaml" in e for e in checks.state_roundtrip(world.docs))


def test_F01_tracked_directory_named_like_state_is_reported(world: World) -> None:
    dump(world.docs / STATE / "WP-D.yaml" / "inner.yaml", {"x": 1})
    world.commit_all(world.docs, "directory named like a state file")
    assert_named(state_errors(world), "WP-D.yaml", "directory")
    assert_named(checks.state_roundtrip(world.docs), "WP-D.yaml", "directory", "committed in")


def test_U12_case_distinct_git_names_are_reported_on_every_host(world: World) -> None:
    """Both names are committed through the index, whatever the host can materialize."""
    for name in ("A.yaml", "a.yaml"):
        blob = git_input(world.docs, name.encode(), "hash-object", "-w", "--stdin")
        git(world.docs, "update-index", "--add", "--cacheinfo", f"100644,{blob},{STATE}/{name}")
    git(world.docs, "commit", "-q", "-m", "case-distinct names")
    errors = checks.state_roundtrip(world.docs)
    assert_named(errors, "A.yaml", "committed in")
    assert_named(errors, "a.yaml", "committed in")


# ------------------------------------------- A / O / F / J / G / M / Q / CH : proof binding (CR-002)


def _content_after_candidate(world: World) -> str:
    cand = candidate(world, "docs")
    record = world.docs / "assurance" / "record.md"
    record.parent.mkdir(parents=True, exist_ok=True)
    record.write_text("content after candidate\n", encoding="utf-8")
    world.commit_all(world.docs, "non-state content")
    state = world.state()
    state["workflow"]["current_candidate"]["docs"]["sha"] = cand
    dump(world.docs / STATE / "WP-T.yaml", state)
    assert any("non-state paths" in e for e in state_errors(world))  # baseline refusal
    return cand


@pytest.mark.parametrize("row", ["A01", "A02"])
def test_tag_named_like_the_branch_cannot_hide_descendants(world: World, row: str) -> None:
    cand = _content_after_candidate(world)
    git(world.docs, "tag", "wp/test", cand)
    if row == "A02":
        git(world.docs, "pack-refs", "--all")
    assert any("non-state paths" in e for e in state_errors(world))


def test_A03_tags_named_main_cannot_fake_acceptance(world: World) -> None:
    write_closed_with_orphan_mains(world)
    for side, repo in (("code", world.code), ("docs", world.docs)):
        git(
            repo,
            "tag",
            "main",
            candidate(world, side) if side == "code" else git(repo, "rev-parse", "wp/test"),
        )
    assert any("not accepted on main" in e for e in state_errors(world))


def test_A06_branch_moving_after_resolution_does_not_mix_snapshots(
    world: World, monkeypatch: pytest.MonkeyPatch
) -> None:
    """D8: the proof uses the OID resolved once; a later branch move is not credited or mixed in."""
    original: Callable[..., tuple[int, str]] = checks._git
    moved = []

    def racing(repo: Path, *args: str) -> tuple[int, str]:
        result = original(repo, *args)
        if not moved and Path(repo) == world.docs and "show-ref" in args:
            moved.append(True)
            (world.docs / "late.md").write_text("late non-state content\n", encoding="utf-8")
            world.commit_all(world.docs, "moved after resolution")
        return result

    monkeypatch.setattr(checks, "_git", racing)
    assert checks.check_state(world.ctx) == []
    assert moved


def test_F04_roundtrip_reads_the_commit_it_resolved(world: World, monkeypatch: pytest.MonkeyPatch) -> None:
    original: Callable[..., tuple[int, str]] = checks._git
    moved = []

    def racing(repo: Path, *args: str) -> tuple[int, str]:
        result = original(repo, *args)
        if not moved and "HEAD^{commit}" in args[-1]:
            moved.append(True)
            world.write_state(updated_reason="moved after resolution")
            world.commit_all(world.docs, "moved")
        return result

    monkeypatch.setattr(checks, "_git", racing)
    errors = checks.state_roundtrip(world.docs)
    assert moved and any("differ from the working tree" in e for e in errors), errors


def test_F05_state_is_validated_and_used_from_one_read(world: World, monkeypatch: pytest.MonkeyPatch) -> None:
    """D9: after the first read the file is replaced; the verdict must be about the object read."""
    path = world.docs / STATE / "WP-T.yaml"
    bad = yaml.safe_dump(world.state(status="CLOSED", next_owner=None, next_action=None)).encode()
    reads: list[str] = []
    real_text, real_bytes = Path.read_text, Path.read_bytes

    def mutate_after_first_read(self: Path) -> None:
        if self == path:
            reads.append("read")
            if len(reads) == 1:
                real_write(self, bad)

    real_write = Path.write_bytes

    def read_text(self: Path, *a: Any, **k: Any) -> str:
        text = real_text(self, *a, **k)
        mutate_after_first_read(self)
        return text

    def read_bytes(self: Path) -> bytes:
        data = real_bytes(self)
        mutate_after_first_read(self)
        return data

    monkeypatch.setattr(Path, "read_text", read_text)
    monkeypatch.setattr(Path, "read_bytes", read_bytes)
    assert checks.check_state(world.ctx) == []
    assert len(reads) == 1, reads


def test_F06_merge_is_not_a_linear_state_only_chain(world: World) -> None:
    git(world.docs, "checkout", "-q", "-b", "side", "HEAD~1")
    note = world.docs / "process" / "handoffs" / "note.md"
    note.parent.mkdir(parents=True, exist_ok=True)
    note.write_text("note\n", encoding="utf-8")
    world.commit_all(world.docs, "side")
    git(world.docs, "checkout", "-q", "wp/test")
    git(world.docs, "merge", "-q", "--no-ff", "-m", "merge", "side")
    assert any("linear chain" in e for e in state_errors(world))


def test_O02_annotated_tag_oid_is_not_a_commit_candidate(world: World) -> None:
    git(world.docs, "tag", "-a", "ann", "-m", "x", candidate(world, "docs"))
    state = world.state()
    state["workflow"]["current_candidate"]["docs"]["sha"] = git(world.docs, "rev-parse", "ann")
    dump(world.docs / STATE / "WP-T.yaml", state)
    assert any("is a tag object, not a commit" in e for e in state_errors(world))


@pytest.mark.parametrize(
    ("row", "path"),
    [
        ("J01", "process/certification-registry.yaml.backup"),
        ("J02", "process/certification-registry.yaml-extra"),
    ],
)
def test_registry_is_an_exact_path(world: World, row: str, path: str) -> None:
    (world.docs / path).write_text("x\n", encoding="utf-8")
    world.commit_all(world.docs, row)
    assert any("non-state paths" in e for e in state_errors(world)), row


@pytest.mark.parametrize(("row", "target"), [("M05", "refs/heads/wp/test"), ("J05", "refs/tags/target-tag")])
def test_symbolic_candidate_ref_is_refused(world: World, row: str, target: str) -> None:
    git(world.docs, "tag", "target-tag", candidate(world, "docs"))
    git(world.docs, "symbolic-ref", "refs/heads/symbolic", target)
    state = world.state()
    state["workflow"]["current_candidate"]["docs"]["ref"] = "symbolic"
    dump(world.docs / STATE / "WP-T.yaml", state)
    assert any("symbolic ref" in e for e in state_errors(world)), row


@pytest.mark.parametrize(
    ("row", "revision"),
    [
        ("J06", "matching-tag"),
        ("J07", "ABBREV"),
        ("J08", "refs/remotes/origin/matching"),
        ("CH10", "refs/heads/wp/test"),
    ],
)
def test_roundtrip_spellings_are_exact(world: World, row: str, revision: str) -> None:
    head = git(world.docs, "rev-parse", "HEAD")
    git(world.docs, "tag", "matching-tag", head)
    git(world.docs, "update-ref", "refs/remotes/origin/matching", head)
    revision = head[:8] if revision == "ABBREV" else revision
    assert checks.state_roundtrip(world.docs, "HEAD") == []
    assert checks.state_roundtrip(world.docs, revision) != [], row


def test_G02_symbolic_branch_spelling_is_refused_by_roundtrip(world: World) -> None:
    git(world.docs, "symbolic-ref", "refs/heads/symbolic", "refs/heads/wp/test")
    assert any("symbolic ref" in e for e in checks.state_roundtrip(world.docs, "symbolic"))


def test_CH09_hex_named_local_branch_is_a_branch(world: World) -> None:
    git(world.docs, "branch", "deadbeef", "HEAD")
    assert checks.state_roundtrip(world.docs, "deadbeef") == []
    assert checks.state_roundtrip(world.docs, git(world.docs, "rev-parse", "HEAD")) == []


@pytest.mark.parametrize("row", ["M01", "M02", "M04"])
def test_ambient_git_selectors_are_ignored(world: World, monkeypatch: pytest.MonkeyPatch, row: str) -> None:
    """D7 (CR-002): the valid world passes exactly as with no environment."""
    other = world.code / ".git"
    variable, value = {
        "M01": ("GIT_DIR", str(other)),
        "M02": ("GIT_WORK_TREE", str(world.code)),
        "M04": ("GIT_OBJECT_DIRECTORY", str(other / "objects")),
    }[row]
    monkeypatch.setenv(variable, value)
    assert world.all_errors() == {}


def test_CH01_ceiling_directories_cannot_hide_a_containing_repository(
    world: World, monkeypatch: pytest.MonkeyPatch
) -> None:
    git(world.root.parent, "init", "-q")
    assert any("inside a git repository" in e for e in world.all_errors().get("repos", []))
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(world.root.parent))
    assert any("inside a git repository" in e for e in world.all_errors().get("repos", []))


def _graft_to_candidates(world: World, orphans: dict[str, str]) -> None:
    for side, repo in (("code", world.code), ("docs", world.docs)):
        git(
            repo, "replace", "--graft", orphans[side], candidate(world, side) if side == "code" else "wp/test"
        )


def test_Q01_replacement_refs_cannot_create_acceptance(world: World) -> None:
    _graft_to_candidates(world, write_closed_with_orphan_mains(world))
    assert any("overlay" in e or "not accepted on main" in e for e in state_errors(world))


def test_CH02_hidden_replacement_base_cannot_create_acceptance(
    world: World, monkeypatch: pytest.MonkeyPatch
) -> None:
    orphans = write_closed_with_orphan_mains(world)
    _graft_to_candidates(world, orphans)
    for side, repo in (("code", world.code), ("docs", world.docs)):
        moved = git(repo, "rev-parse", f"refs/replace/{orphans[side]}")
        git(repo, "update-ref", "-d", f"refs/replace/{orphans[side]}")
        git(repo, "update-ref", f"refs/hidden/{orphans[side]}", moved)
    monkeypatch.setenv("GIT_REPLACE_REF_BASE", "refs/hidden/")
    assert any("not accepted on main" in e for e in state_errors(world))


@pytest.mark.parametrize("row", ["Q02", "CH03"])
def test_legacy_grafts_cannot_create_acceptance(
    world: World, monkeypatch: pytest.MonkeyPatch, row: str
) -> None:
    orphans = write_closed_with_orphan_mains(world)
    for side, repo in (("code", world.code), ("docs", world.docs)):
        parent = candidate(world, side) if side == "code" else git(repo, "rev-parse", "wp/test")
        grafts = (
            Path(git(repo, "rev-parse", "--path-format=absolute", "--git-common-dir")) / "info" / "grafts"
        )
        grafts.parent.mkdir(parents=True, exist_ok=True)
        grafts.write_text(f"{orphans[side]} {parent}\n", encoding="utf-8")
    if row == "CH03":  # the insufficient fix: replace objects disabled, grafts still honoured
        monkeypatch.setenv("GIT_NO_REPLACE_OBJECTS", "1")
    errors = state_errors(world)
    assert any("overlay" in e and "info/grafts" in e for e in errors), errors


def test_CH04_shallow_repository_is_refused_with_a_named_diagnostic(world: World) -> None:
    tip = git(world.docs, "rev-parse", "wp/test")
    assert tip != candidate(world, "docs")
    common = Path(git(world.docs, "rev-parse", "--path-format=absolute", "--git-common-dir"))
    (common / "shallow").write_text(tip + "\n", encoding="utf-8")
    assert any("shallow history" in e for e in state_errors(world))


def test_I07_unterminated_path_record_is_a_framing_error(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    def fake_run(argv: list[str], **kwargs: Any) -> subprocess.CompletedProcess[bytes]:
        return subprocess.CompletedProcess(argv, 0, b"A.yaml", b"")

    monkeypatch.setattr(checks.subprocess, "run", fake_run)
    status, names = checks._git_paths(tmp_path, "ls-tree", "-z", "--name-only", "HEAD")
    assert status != 0 and names == []


# ----------------------------------------------------------- E / CH06 / E10 : other inventories


def _findings_entry(world: World, rel: str) -> None:
    path = world.docs / checks.FINDINGS_DIR / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("register_version: 1\nfindings: []\n", encoding="utf-8")


@pytest.mark.parametrize(
    ("row", "check", "setup"),
    [
        ("E01", "findings", lambda w: _findings_entry(w, "G.YAML")),
        ("E02", "findings", lambda w: _findings_entry(w, "sub/x.yaml")),
        ("E03", "spec", lambda w: (w.docs / "spec" / "extra.MD").write_text("# x\n", encoding="utf-8")),
        ("E04", "spec", lambda w: (w.docs / "spec" / "dir.md").mkdir()),
        (
            "E05",
            "sources",
            lambda w: (w.docs / checks.SOURCE_TEXT_DIR / "EXTRA.MD").write_text("x\n", encoding="utf-8"),
        ),
        ("E08", "conformance", lambda w: (w.code / "conformance" / "core" / "dir.yaml").mkdir()),
    ],
)
def test_inventories_report_unsupported_entries_on_every_host(
    world: World, row: str, check: str, setup: Callable[[World], Any]
) -> None:
    """D16 (CR-001/CR-003): named errors, identical on W/L/C, never 'internal error' or a skip."""
    setup(world)
    errors = world.run(check)
    assert any("(D16)" in e for e in errors), (row, errors)
    assert not any("internal error" in e for e in errors), errors


def test_CH06_nested_git_file_is_a_nested_repository(world: World) -> None:
    nested = world.docs / "nested"
    nested.mkdir()
    (nested / ".git").write_text("gitdir: ../elsewhere\n", encoding="utf-8")
    assert any("nested git repository" in e for e in world.run("repos"))


def test_E10_linked_worktree_root_is_a_valid_repository(world: World) -> None:
    linked = world.root / "linked-docs"
    git(world.docs, "worktree", "add", "-q", "-b", "linked", str(linked))
    ctx = checks.Context(docs=linked, code=world.code, workspace=world.root)
    assert checks.check_repos(ctx) == []


# -------------------------------------------- E12 / Z / V / CH07 / CH08 / CH11 : source producer


def _bundle_manifest(world: World) -> dict[str, Any]:
    data = yaml.safe_load((world.docs / checks.BUNDLE_MANIFEST).read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def _build(world: World) -> int:
    return cli.main(["sources", "build", "--docs", str(world.docs), "--workspace", str(world.root)])


def test_E12_source_file_cannot_traverse(world: World) -> None:
    data = _bundle_manifest(world)
    data["documents"][0]["file"] = "../bundle/DOC.md"
    dump(world.docs / checks.BUNDLE_MANIFEST, data)
    assert any("relative path inside bundle_root" in e for e in world.run("sources"))


@pytest.mark.parametrize(("row", "key"), [("Z06", "../escaped-marker"), ("Z07", 7)])
def test_source_key_cannot_choose_an_output_path(world: World, row: str, key: Any) -> None:
    data = _bundle_manifest(world)
    data["documents"][0]["key"] = key
    dump(world.docs / checks.BUNDLE_MANIFEST, data)
    assert _build(world) == 1, row
    assert not (world.docs / "reference" / "escaped-marker.md").exists()


def test_Z08_malformed_document_entry_is_reported(world: World) -> None:
    data = _bundle_manifest(world)
    data["documents"].append(7)
    dump(world.docs / checks.BUNDLE_MANIFEST, data)
    assert _build(world) == 1


def test_V07_missing_docs_is_a_reported_failure(world: World) -> None:
    assert cli.main(["sources", "build", "--docs", str(world.root / "missing")]) == 1


def _second_document(world: World, digest: str | None = None) -> dict[str, Any]:
    (world.bundle / "SECOND.md").write_text(
        "# Second\n\n## 1. Part\n\nText.\n", encoding="utf-8", newline="\n"
    )
    data = _bundle_manifest(world)
    entry = copy.deepcopy(data["documents"][0])  # a shared nested list would be dumped as a YAML alias
    entry.update(
        key="SECOND", file="SECOND.md", sha256=digest or sources.sha256_file(world.bundle / "SECOND.md")
    )
    data["documents"].append(entry)
    dump(world.docs / checks.BUNDLE_MANIFEST, data)
    return data


def test_CH07_failed_later_entry_leaves_every_output_byte_unchanged(world: World) -> None:
    _second_document(world, digest="0" * 64)
    text_dir = world.docs / checks.SOURCE_TEXT_DIR
    before = {p.name: p.read_bytes() for p in text_dir.iterdir()}
    index_before = (world.docs / checks.SOURCE_INDEX).read_bytes()
    assert _build(world) == 1
    assert {p.name: p.read_bytes() for p in text_dir.iterdir()} == before
    assert (world.docs / checks.SOURCE_INDEX).read_bytes() == index_before


def test_CH08_all_valid_multi_entry_build_writes_every_output(world: World) -> None:
    _second_document(world)
    assert _build(world) == 0
    names = {p.name for p in (world.docs / checks.SOURCE_TEXT_DIR).iterdir()}
    assert names == {"DOC.md", "SECOND.md"}
    index = yaml.safe_load((world.docs / checks.SOURCE_INDEX).read_text(encoding="utf-8"))
    assert set(index["documents"]) == {"DOC", "SECOND"}


def test_CH11_every_established_source_key_is_valid() -> None:
    keys = ["FND", "MVP", "R00", "R01", "R02", "R03", "R04", "R05", "IAA", "BOOT", "SUMMARY", "PACK", "DOC"]
    assert all(checks.SOURCE_KEY.fullmatch(k) for k in keys)
    assert not any(checks.SOURCE_KEY.fullmatch(k) for k in ("../x", "doc", "DOC.md", "", "A" * 17))


def test_failed_replace_reports_what_was_replaced(world: World, monkeypatch: pytest.MonkeyPatch) -> None:
    """D14 stated limit: one injected failure on the first replace exits 1 with the diagnostic."""

    def fail(temporary: Path, target: Path) -> None:
        raise OSError("injected replace failure")

    monkeypatch.setattr(cli, "_replace", fail)
    assert _build(world) == 1


# ------------------------------------------------------------- C05 / V12 / Z10 / F08 : CLI scope


def test_C05_bare_only_is_a_usage_error(world: World) -> None:
    with pytest.raises(SystemExit) as raised:
        cli.main(["check", "--docs", str(world.docs), "--code", str(world.code), "--only"])
    assert raised.value.code == 2


@pytest.mark.parametrize("row", ["V12", "Z10"])
def test_validate_with_docs_refuses_paths_outside_the_state_area(world: World, row: str) -> None:
    outside = world.root / "outside" / "WP-T.yaml"
    outside.parent.mkdir()
    outside.write_bytes((world.docs / STATE / "WP-T.yaml").read_bytes())
    assert cli.main(["state", "validate", str(outside), "--docs", str(world.docs)]) == 1, row
    assert cli.main(["state", "validate", str(outside)]) == 0  # without --docs: object validity only


def test_F08_roundtrip_names_a_bare_repository(world: World) -> None:
    bare = world.root / "bare.git"
    git(world.root, "clone", "-q", "--bare", str(world.docs), str(bare))
    assert any("non-bare" in e for e in checks.state_roundtrip(bare))
