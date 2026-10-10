"""CE-P01-01 targeted-closure controls (Codex review c7dadc07, CL-001..CL-004; Owner G-024).

Each control reproduces a closure witness against the already-agreed rules (D5/D7/D13/D14/D16).
They were executed against candidate db672edc first and failed there before any production fix.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any

import pytest
from conftest import World, git
from test_ce_p01_01 import STATE, dump

from mneme_process import checks, cli


def _build(world: World) -> int:
    return cli.main(["sources", "build", "--docs", str(world.docs), "--workspace", str(world.root)])


# ------------------------------------------------------------------- CL-001 (CR-001, D16)


@pytest.mark.parametrize(
    ("check", "directory"),
    [("spec", ("spec", "dir.MD")), ("conformance", ("conformance", "core", "dir.YAML"))],
    ids=["spec-dir.MD", "conformance-dir.YAML"],
)
def test_CL001_case_variant_member_directory_is_refused(
    world: World, check: str, directory: tuple[str, ...]
) -> None:
    """A directory named with a case-variant member suffix is a named error, not traversed silently."""
    root = world.code if check == "conformance" else world.docs
    root.joinpath(*directory).mkdir()
    assert any("(D16)" in e for e in world.run(check)), world.run(check)


def test_CL001_nested_marker_is_an_exact_name_on_every_host(world: World) -> None:
    """`.GIT` is not `.git`: the nested-repository scan compares the exact name (D16)."""
    nested = world.docs / "nested"
    nested.mkdir()
    (nested / ".GIT").write_text("not a marker\n", encoding="utf-8")
    assert world.run("repos") == []
    os.remove(nested / ".GIT")  # the genuine nested marker stays refused (CH06)
    (nested / ".git").write_text("gitdir: ../elsewhere\n", encoding="utf-8")
    assert any("nested git repository" in e for e in world.run("repos"))


def test_CL001_original_E05_named_by_its_original_caller(world: World) -> None:
    """Original E05 recipe: rename DOC.md -> DOC.MD; check_spec itself names the inventory error."""
    text_dir = world.docs / checks.SOURCE_TEXT_DIR
    (text_dir / "DOC.md").rename(text_dir / "DOC.MD.tmp")
    (text_dir / "DOC.MD.tmp").rename(text_dir / "DOC.MD")
    errors = world.run("spec")
    assert any("DOC.MD" in e and "(D16)" in e for e in errors), errors


# ------------------------------------------------------------------- CL-002 (CR-002, D5/D7/D13)


def _fail_query(monkeypatch: pytest.MonkeyPatch, marker: str) -> None:
    original = checks._git

    def failing(repo: Path, *args: str) -> tuple[int, str]:
        if marker in args:
            return 128, ""
        return original(repo, *args)

    monkeypatch.setattr(checks, "_git", failing)


def test_CL002_failed_shallow_query_never_authorizes(world: World, monkeypatch: pytest.MonkeyPatch) -> None:
    """A fatal --is-shallow-repository query is an error, never evidence of a non-shallow repo."""
    _fail_query(monkeypatch, "--is-shallow-repository")
    errors = world.all_errors().get("state", [])
    assert any("cannot determine" in e for e in errors), errors
    assert checks.state_roundtrip(world.docs) != []


def test_CL002_failed_symbolic_query_never_authorizes(world: World, monkeypatch: pytest.MonkeyPatch) -> None:
    """symbolic-ref -q: exit 0 = symbolic, exit 1 = not symbolic, anything else = error."""
    git(world.docs, "symbolic-ref", "refs/heads/symbolic", "refs/heads/wp/test")
    state: dict[str, Any] = world.state()
    state["workflow"]["current_candidate"]["docs"]["ref"] = "symbolic"
    dump(world.docs / STATE / "WP-T.yaml", state)
    assert any("symbolic ref" in e for e in world.all_errors().get("state", []))  # baseline refusal
    _fail_query(monkeypatch, "symbolic-ref")
    errors = world.all_errors().get("state", [])
    assert errors and any("cannot determine" in e for e in errors), errors


def test_CL002_plain_branch_still_passes_with_quiet_non_symbolic_result(world: World) -> None:
    assert world.all_errors() == {}


# ------------------------------------------------------------------- CL-003 (CR-003, D13/D14)


def test_CL003_cleanup_failure_stays_a_documented_error(
    world: World, monkeypatch: pytest.MonkeyPatch
) -> None:
    def fail_replace(temporary: Path, target: Path) -> None:
        raise OSError("injected replace failure")

    real_unlink = Path.unlink

    def fail_unlink(self: Path, missing_ok: bool = False) -> None:
        if self.name.endswith(".mneme-tmp"):
            raise OSError("injected cleanup failure")
        real_unlink(self, missing_ok=missing_ok)

    monkeypatch.setattr(cli, "_replace", fail_replace)
    monkeypatch.setattr(Path, "unlink", fail_unlink)
    assert _build(world) == 1


# ------------------------------------------------------------------- CL-004 (CR-004, D14/D16)


def test_CL004_staging_never_follows_a_symlink_outside(world: World) -> None:
    text_dir = world.docs / checks.SOURCE_TEXT_DIR
    outside = world.root / "escaped.md"
    outside.write_text("outside bytes\n", encoding="utf-8")
    try:
        os.symlink(outside, text_dir / ".DOC.md.mneme-tmp")
    except (OSError, NotImplementedError) as error:
        pytest.skip(f"DIAG: host cannot create symlinks ({error})")
    result = _build(world)
    assert outside.read_text(encoding="utf-8") == "outside bytes\n"
    final = text_dir / "DOC.md"
    assert not final.is_symlink() and final.resolve().parent == text_dir.resolve()
    if result == 0:
        assert "sources" not in world.all_errors()


def test_CL004_symlinked_output_directory_is_refused(world: World) -> None:
    """The producer boundary is the real reference/source-text directory, never a link elsewhere."""
    text_dir = world.docs / checks.SOURCE_TEXT_DIR
    elsewhere = world.root / "elsewhere"
    elsewhere.mkdir()
    for path in text_dir.iterdir():
        path.rename(elsewhere / path.name)
    text_dir.rmdir()
    try:
        os.symlink(elsewhere, text_dir, target_is_directory=True)
    except (OSError, NotImplementedError) as error:
        pytest.skip(f"DIAG: host cannot create symlinks ({error})")
    before = {p.name: p.read_bytes() for p in elsewhere.iterdir()}
    assert _build(world) == 1
    assert {p.name: p.read_bytes() for p in elsewhere.iterdir()} == before


def test_CL002_failed_containment_query_never_authorizes(
    world: World, monkeypatch: pytest.MonkeyPatch
) -> None:
    """CL-002 neighborhood: a fatal workspace-containment query is an error, not 'not inside a repo'."""
    real_run = subprocess.run
    workspace = str(world.docs.parent)

    def failing(argv: list[str], **kwargs: Any) -> Any:
        if argv[:3] == ["git", "-C", workspace] and "--show-toplevel" in argv:
            return subprocess.CompletedProcess(argv, 128, b"", b"fatal: injected failure\n")
        return real_run(argv, **kwargs)

    monkeypatch.setattr(checks.subprocess, "run", failing)
    assert any("cannot determine whether it is inside a git repository" in e for e in world.run("repos"))


# ------------------------------------------------------------- R1 (CR-001, D16 with D13; G-027)


def test_R1_unreadable_directory_in_nested_marker_scan_is_a_named_error(
    world: World, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Codex recheck R1: an incomplete nested-.git scan never reports success."""
    nested = world.docs / "nested"
    nested.mkdir()
    (nested / ".git").write_text("gitdir: ../elsewhere\n", encoding="utf-8")
    assert any("nested git repository" in e for e in world.run("repos"))  # baseline refusal
    real_scandir = os.scandir

    def failing(path: Any = ".") -> Any:
        if Path(path) == nested:
            raise PermissionError("injected unreadable nested directory")
        return real_scandir(path)

    monkeypatch.setattr(os, "scandir", failing)
    errors = checks.check_repos(world.ctx)
    assert any("cannot scan" in e and "nested" in e for e in errors), errors


def test_R1_complete_scan_without_marker_still_passes(world: World) -> None:
    (world.docs / "plain").mkdir()
    (world.docs / "plain" / "file.txt").write_text("x\n", encoding="utf-8")
    assert world.run("repos") == []
