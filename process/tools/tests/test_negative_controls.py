"""One realistic mutation per rule; each must be caught by its intended check with the intended message.

`world` has already proven the unmutated baseline passes every check (conftest.py).
"""

from __future__ import annotations

import subprocess

import pytest
import yaml
from conftest import SCENARIO, World, dump, git

from mneme_process import checks


def only_failures(world: World) -> dict[str, list[str]]:
    return world.all_errors()


def assert_caught(world: World, check: str, fragment: str) -> None:
    errors = only_failures(world)
    assert check in errors, f"{check} did not fail; failures: {errors}"
    assert any(fragment in e for e in errors[check]), errors[check]


# ----------------------------------------------------------------- sources


def test_source_byte_change_is_caught(world: World) -> None:
    (world.bundle / "DOC.md").write_text("tampered\n", encoding="utf-8")
    assert_caught(world, "sources", "sha256 mismatch")


def test_hand_edited_derived_text_is_caught(world: World) -> None:
    path = world.docs / checks.SOURCE_TEXT_DIR / "DOC.md"
    path.write_text(path.read_text(encoding="utf-8") + "extra\n", encoding="utf-8")
    assert_caught(world, "sources", "does not match the index")


# ----------------------------------------------------------------- spec


def test_duplicate_requirement_id_is_caught(world: World) -> None:
    spec = world.docs / "spec" / "core.md"
    spec.write_text(spec.read_text(encoding="utf-8").replace("CORE-002 —", "CORE-001 —"), encoding="utf-8")
    assert_caught(world, "spec", "duplicate requirement id CORE-001")


def test_unresolvable_citation_is_caught(world: World) -> None:
    spec = world.docs / "spec" / "core.md"
    spec.write_text(spec.read_text(encoding="utf-8").replace("[DOC §2]", "[DOC §9]"), encoding="utf-8")
    assert_caught(world, "spec", "[DOC §9] does not resolve")


def test_anchor_mismatch_is_caught(world: World) -> None:
    spec = world.docs / "spec" / "core.md"
    spec.write_text(
        spec.read_text(encoding="utf-8").replace('id="core-002"', 'id="core-003"'), encoding="utf-8"
    )
    assert_caught(world, "spec", "does not match CORE-002")


def test_unregistered_finding_reference_is_caught(world: World) -> None:
    spec = world.docs / "spec" / "core.md"
    spec.write_text(spec.read_text(encoding="utf-8").replace("(NF-001)", "(NF-999)"), encoding="utf-8")
    assert_caught(world, "spec", "NF-999 is not a registered finding")


def test_citation_inside_inline_code_is_not_a_citation(world: World) -> None:
    spec = world.docs / "spec" / "core.md"
    spec.write_text(spec.read_text(encoding="utf-8") + "\nExample: `[KEY §anchor]`.\n", encoding="utf-8")
    assert "spec" not in only_failures(world)


# ----------------------------------------------------------------- manifest


def _rows(world: World) -> dict[str, object]:
    return yaml.safe_load((world.code / checks.MANIFEST).read_text(encoding="utf-8"))  # type: ignore[no-any-return]


def test_missing_manifest_row_is_caught(world: World) -> None:
    data = _rows(world)
    data["rows"] = data["rows"][:1]  # type: ignore[index]
    dump(world.code / checks.MANIFEST, data)
    assert_caught(world, "manifest", "no manifest row for spec requirement CORE-002")


def test_manifest_sources_drift_is_caught(world: World) -> None:
    data = _rows(world)
    data["rows"][1]["sources"] = ["[DOC §1]"]  # type: ignore[index]
    dump(world.code / checks.MANIFEST, data)
    assert_caught(world, "manifest", "CORE-002 sources differ")


def test_manifest_schema_violation_is_caught(world: World) -> None:
    data = _rows(world)
    data["rows"][0]["disposition"] = "maybe"  # type: ignore[index]
    dump(world.code / checks.MANIFEST, data)
    assert_caught(world, "manifest", "schema")


def test_manifest_unknown_scenario_is_caught(world: World) -> None:
    data = _rows(world)
    data["rows"][1]["scenarios"] = ["core.fixture.missing"]  # type: ignore[index]
    dump(world.code / checks.MANIFEST, data)
    assert_caught(world, "manifest", "unknown scenario core.fixture.missing")


# ----------------------------------------------------------------- conformance / YAML boundary


def test_duplicate_scenario_id_is_caught(world: World) -> None:
    dump(world.code / "conformance" / "core" / "copy.yaml", SCENARIO)
    assert_caught(world, "conformance", "duplicate scenario id")


def test_yaml11_ambiguous_scalar_is_caught(world: World) -> None:
    path = world.code / "conformance" / "core" / "first-rule.yaml"
    path.write_text(path.read_text(encoding="utf-8") + "notes: yes\n", encoding="utf-8")
    assert_caught(world, "conformance", "YAML 1.1 and YAML 1.2-core readings differ")


def test_yaml_duplicate_key_is_caught(world: World) -> None:
    path = world.code / "conformance" / "core" / "first-rule.yaml"
    path.write_text(path.read_text(encoding="utf-8") + "title: again\n", encoding="utf-8")
    assert_caught(world, "conformance", "duplicate key 'title'")


def test_active_scenario_with_placeholder_is_caught(world: World) -> None:
    dump(world.code / "conformance" / "core" / "first-rule.yaml", {**SCENARIO, "status": "ACTIVE"})
    assert_caught(world, "conformance", "ACTIVE scenario contains a TO_BE_ placeholder")


def test_scenario_not_backlinked_is_caught(world: World) -> None:
    dump(
        world.code / "conformance" / "core" / "first-rule.yaml",
        {**SCENARIO, "requirements": ["CORE-001", "CORE-002"]},
    )
    assert_caught(world, "conformance", "manifest row CORE-002 does not list scenario")


def test_scenario_family_directory_mismatch_is_caught(world: World) -> None:
    dump(world.code / "conformance" / "agent" / "misplaced.yaml", {**SCENARIO, "id": "core.fixture.other"})
    assert_caught(world, "conformance", "id/family/directory disagree")


# ----------------------------------------------------------------- state


def test_active_state_without_owner_is_caught(world: World) -> None:
    world.write_state(next_owner=None)
    assert_caught(world, "state", "needs next_owner")


def test_blocked_for_owner_must_name_owner(world: World) -> None:
    world.write_state(status="BLOCKED_FOR_OWNER", next_owner="Codex")
    assert_caught(world, "state", "BLOCKED_FOR_OWNER requires next_owner: Owner")


def test_unknown_status_is_caught(world: World) -> None:
    world.write_state(status="BLOCKED")
    assert_caught(world, "state", "unknown status 'BLOCKED'")


def test_nonexistent_candidate_sha_is_caught(world: World) -> None:
    state = world.state()
    state["workflow"]["current_candidate"]["code"]["sha"] = "0" * 40
    dump(world.docs / checks.STATE_DIR / "WP-T.yaml", state)
    assert_caught(world, "state", "does not exist in minion-memory")


def test_requirement_list_scalar_shape_is_caught(world: World) -> None:
    world.write_state(requirements="CORE-001")
    assert_caught(world, "state", "requirements must be a list")


def test_state_only_child_rule_is_caught(world: World) -> None:
    spec = world.docs / "spec" / "core.md"
    spec.write_text(spec.read_text(encoding="utf-8") + "\nLate edit.\n", encoding="utf-8")
    world.commit_all(world.docs, "content change after the reviewed candidate")
    assert_caught(world, "state", "state-only child rule")


def test_history_keys_in_state_are_caught(world: World) -> None:
    world.write_state(reviews=["r1"])
    assert_caught(world, "state", "history-shaped keys")


# ----------------------------------------------------------------- findings / registry


def test_unknown_classification_is_caught(world: World) -> None:
    path = world.docs / checks.FINDINGS_DIR / "F.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    data["findings"][0]["classification"] = "MINOR_ISSUE"
    dump(path, data)
    assert_caught(world, "findings", "not in the taxonomy")


def test_certified_closed_needs_both_languages(world: World) -> None:
    path = world.docs / checks.REGISTRY
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    data["work_packages"]["WP-T"]["cross_language"]["status"] = "CERTIFIED_CLOSED"
    dump(path, data)
    assert_caught(world, "registry", "requires both languages CERTIFIED")


# ----------------------------------------------------------------- repos


def test_nested_git_repo_is_caught(world: World) -> None:
    nested = world.code / "minion-memory-python"
    nested.mkdir()
    git(nested, "init", "-q")
    assert_caught(world, "repos", "nested git repository")


def test_scratch_inside_repo_is_caught(world: World) -> None:
    (world.docs / ".tmp").mkdir()
    assert_caught(world, "repos", "OWN-001")


def test_workspace_root_must_not_be_a_repo(world: World) -> None:
    subprocess.run(["git", "-C", str(world.root), "init", "-q"], check=True, capture_output=True)
    assert_caught(world, "repos", "inside a git repository")


@pytest.mark.parametrize("rel", [checks.MANIFEST_SCHEMA, checks.SCENARIO_SCHEMA])
def test_fixture_uses_the_real_schema_files(rel: str) -> None:
    from conftest import REAL_CODE

    assert (REAL_CODE / rel).is_file(), f"the fixture copies {rel} from the real code repo"
