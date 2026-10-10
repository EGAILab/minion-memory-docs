"""One realistic mutation per rule; each must be caught by its intended check with the intended message.

`world` has already proven the unmutated baseline passes every check (conftest.py).
"""

from __future__ import annotations

import subprocess
from pathlib import Path

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
    assert_caught(world, "state", "state-only descendant rule")


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


# ----------------------------------------------------------------- WP00-CR remediation controls


def _approved_review() -> dict[str, str]:
    return {"outcome": "APPROVED", "verdict": "APPROVED", "source": "assurance/reviews/x.md"}


def _closed(world: World, ref: str = "main", **overrides: object) -> None:
    """A CLOSED state in the correct form: both candidate sides recorded with ref main."""
    fields: dict[str, object] = {
        "status": "CLOSED",
        "open_findings": [],
        "next_owner": None,
        "next_action": None,
        "scoping_review": _approved_review(),
    }
    fields.update(overrides)
    state = world.state(**fields)
    for side in ("code", "docs"):
        state["workflow"]["current_candidate"][side]["ref"] = ref
    dump(world.docs / checks.STATE_DIR / "WP-T.yaml", state)


def _accept_on_main(world: World) -> None:
    for repo in (world.code, world.docs):
        git(repo, "branch", "-f", "main", git(repo, "rev-parse", "HEAD"))


def test_cr003_closure_without_scoping_approval_is_caught(world: World) -> None:
    _accept_on_main(world)
    _closed(world, scoping_review=None)
    assert_caught(world, "state", "closes only with scoping_review")


@pytest.mark.parametrize("outcome", ["CHANGES_REQUIRED", "approved", "NOT APPROVED", None])
def test_cr003_closure_with_non_approval_outcome_is_caught(world: World, outcome: object) -> None:
    _accept_on_main(world)
    _closed(world, scoping_review={**_approved_review(), "outcome": outcome})
    assert_caught(world, "state", "closes only with scoping_review")


def _unrelated_main(world: World) -> None:
    """A main branch that exists but does not contain the candidates (an orphan empty commit)."""
    for repo in (world.code, world.docs):
        empty_tree = subprocess.run(
            ["git", "-C", str(repo), "mktree"], input="", capture_output=True, text=True, check=True
        ).stdout.strip()
        orphan = git(repo, "commit-tree", empty_tree, "-m", "unrelated main")
        git(repo, "branch", "-f", "main", orphan)


def test_cr003_closure_without_main_acceptance_is_caught(world: World) -> None:
    _unrelated_main(world)
    _closed(world)
    assert_caught(world, "state", "is not accepted on main")


def test_cr003_product_wp_closure_needs_certified_closed(world: World) -> None:
    _accept_on_main(world)
    _closed(world, requirements=["CORE-001"])
    assert_caught(world, "state", "CERTIFIED_CLOSED")


def test_cr003_positive_control_valid_scoping_closure_passes(world: World) -> None:
    """The closure guard must not over-block: approved review + accepted candidates passes."""
    _closed(world)
    world.commit_all(world.docs, "close")
    _accept_on_main(world)
    assert "state" not in only_failures(world)


@pytest.mark.parametrize("actor", ["Claude", "Codex"])
def test_cr004_quarantine_blocks_every_agent(world: World, actor: str) -> None:
    world.write_state(next_owner=actor, quarantine={"derived_from_quarantined_artifact": True})
    assert_caught(world, "state", "authorizes no agent action")


def test_cr004_positive_control_quarantine_routed_to_owner(world: World) -> None:
    world.write_state(next_owner="Owner", quarantine={"derived_from_quarantined_artifact": True})
    assert "state" not in only_failures(world)


@pytest.mark.parametrize("title", ["title: !!str fixture", "title: &unused fixture"])
def test_cr005_explicit_tag_or_anchor_in_scenario_is_caught(world: World, title: str) -> None:
    path = world.code / "conformance" / "core" / "first-rule.yaml"
    path.write_text(path.read_text(encoding="utf-8").replace("title: fixture", title), encoding="utf-8")
    assert_caught(world, "conformance", "syntax is not allowed")


def test_cr011_content_change_then_revert_after_candidate_is_caught(world: World) -> None:
    spec = world.docs / "spec" / "core.md"
    original = spec.read_text(encoding="utf-8")
    spec.write_text(original + "\nTransient edit.\n", encoding="utf-8")
    world.commit_all(world.docs, "content change")
    spec.write_text(original, encoding="utf-8")
    world.commit_all(world.docs, "exact revert")
    assert_caught(world, "state", "state-only descendant rule")


def test_cr011_positive_control_multi_commit_state_chain_passes(world: World) -> None:
    world.write_state(updated_reason="second state-only commit")
    world.commit_all(world.docs, "state again")
    handoff = world.docs / "process" / "handoffs" / "h.md"
    handoff.parent.mkdir(parents=True, exist_ok=True)
    handoff.write_text("handoff\n", encoding="utf-8")
    world.commit_all(world.docs, "handoff")
    assert "state" not in only_failures(world)


def test_malformed_status_type_is_reported_not_crashed(world: World) -> None:
    world.write_state(status=["SCOPING"])
    errors = only_failures(world)["state"]
    assert any("unknown status" in e for e in errors), errors
    assert not any("internal error" in e for e in errors), errors


def test_cr002_uncertain_finding_without_escalation_is_caught(world: World) -> None:
    path = world.docs / checks.FINDINGS_DIR / "F.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    data["findings"][0]["owner_decision_required"] = False
    dump(path, data)
    assert_caught(world, "findings", "needs owner_decision_required: true or an escalation_condition")


# ----------------------------------------------------------------- WP00-CR-008 (targeted closure 1)


def test_cr008_frozen_without_frozen_labelled_citation_is_caught(world: World) -> None:
    """Re-point FROZEN CORE-001 at DOC section 2, which carries no FROZEN label."""
    spec = world.docs / "spec" / "core.md"
    text = spec.read_text(encoding="utf-8").replace(
        "**Source status:** FROZEN · **Sources:** [DOC §1]",
        "**Source status:** FROZEN · **Sources:** [DOC §2]",
    )
    spec.write_text(text, encoding="utf-8")
    assert_caught(world, "spec", "CORE-001 is FROZEN but cites no source section carrying a FROZEN label")


def test_cr008_positive_control_normative_needs_no_label(world: World) -> None:
    """CORE-002 is NORMATIVE and cites unlabeled DOC section 2 too: no FROZEN-label demand applies."""
    errors = only_failures(world).get("spec", [])
    assert not any("CORE-002" in e for e in errors), errors


# ------------------------------------------------------- WP-P01 controls (CR-014, roundtrip, CLOSED)


def _relabel_section_1(world: World, label_line: str) -> None:
    """Replace the fixture source's section-1 label and regenerate hash, derived text and index."""
    from mneme_process import sources as src

    text = f"# Fixture authority\n\n## 1. Intro\n\n{label_line}\n\n## 2. Rules\n\nMore text.\n"
    doc = world.bundle / "DOC.md"
    doc.write_text(text, encoding="utf-8", newline="\n")
    digest = src.sha256_file(doc)
    manifest = world.docs / checks.BUNDLE_MANIFEST
    data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    data["documents"][0]["sha256"] = digest
    dump(manifest, data)
    (world.docs / checks.SOURCE_TEXT_DIR / "DOC.md").write_text(
        "<!-- derived -->\n\n" + text, encoding="utf-8", newline="\n"
    )
    dump(world.docs / checks.SOURCE_INDEX, src.build_index({"DOC": (digest, text)}))


@pytest.mark.parametrize(
    "label_line",
    [
        "| NOT FROZEN | Text. |",
        "This section discusses a FROZEN decision elsewhere.",
        "| Taxonomy | FROZEN -> PROVISIONAL | change record |",
    ],
)
def test_cr014_non_label_frozen_mentions_are_caught(world: World, label_line: str) -> None:
    _relabel_section_1(world, label_line)
    assert_caught(world, "spec", "CORE-001 is FROZEN but cites no source section carrying a FROZEN label")


@pytest.mark.parametrize(
    "label_line",
    ["| Scope | FROZEN boundary / PROVISIONAL vocabulary |", "FROZEN — Text with the dash form."],
)
def test_cr014_positive_label_forms_pass(world: World, label_line: str) -> None:
    _relabel_section_1(world, label_line)
    assert "spec" not in only_failures(world)


def test_cr014_normative_citing_only_unlabelled_section_passes(world: World) -> None:
    spec = world.docs / "spec" / "core.md"
    spec.write_text(
        spec.read_text(encoding="utf-8").replace(
            "**Source status:** NORMATIVE · **Sources:** [DOC §1] [DOC §2]",
            "**Source status:** NORMATIVE · **Sources:** [DOC §2]",
        ),
        encoding="utf-8",
    )
    data = _rows(world)
    data["rows"][1]["sources"] = ["[DOC §2]"]  # type: ignore[index]
    dump(world.code / checks.MANIFEST, data)
    assert only_failures(world) == {}, only_failures(world)


def test_roundtrip_positive_committed_state_matches(world: World) -> None:
    assert checks.state_roundtrip(world.docs) == []


def test_roundtrip_uncommitted_state_change_is_caught(world: World) -> None:
    world.write_state(updated_reason="changed but not committed")
    errors = checks.state_roundtrip(world.docs)
    assert any("differ from the working tree" in e for e in errors), errors


def test_roundtrip_non_ascii_state_is_decoded_as_utf8(world: World) -> None:
    """The remediation-1 probe failure: an em dash must survive the git round trip."""
    world.write_state(updated_reason="em dash — and ü survive")
    world.commit_all(world.docs, "non-ascii state")
    assert checks.state_roundtrip(world.docs) == []
    assert "state" not in only_failures(world)


def test_closed_state_allows_post_acceptance_records_on_main(world: World) -> None:
    """A CLOSED candidate is protected by main ancestry; later record commits may follow it."""
    docs_candidate = git(world.docs, "rev-parse", "HEAD~1")
    state = world.state(
        status="CLOSED",
        open_findings=[],
        next_owner=None,
        next_action=None,
        scoping_review=_approved_review(),
    )
    for side in ("code", "docs"):
        state["workflow"]["current_candidate"][side]["ref"] = "main"
    state["workflow"]["current_candidate"]["docs"]["sha"] = docs_candidate
    dump(world.docs / checks.STATE_DIR / "WP-T.yaml", state)
    record = world.docs / "assurance" / "reviews" / "record.md"
    record.parent.mkdir(parents=True, exist_ok=True)
    record.write_text("post-acceptance review record\n", encoding="utf-8")
    world.commit_all(world.docs, "post-acceptance records")
    _accept_on_main(world)
    assert "state" not in only_failures(world)


def test_open_state_still_enforces_chain_after_candidate(world: World) -> None:
    """The CLOSED exemption must not leak to active states."""
    record = world.docs / "assurance" / "reviews" / "record.md"
    record.parent.mkdir(parents=True, exist_ok=True)
    record.write_text("content after candidate\n", encoding="utf-8")
    world.commit_all(world.docs, "content")
    assert_caught(world, "state", "state-only descendant rule")


def test_roundtrip_crlf_only_difference_is_not_a_failed_commit(world: World) -> None:
    path = world.docs / checks.STATE_DIR / "WP-T.yaml"
    path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
    assert checks.state_roundtrip(world.docs) == []


# ------------------------------------------------------- WP-P01 remediation 1 (WPP01-CR-001, CR-002)


def _add_other_state(world: World) -> Path:
    other = world.docs / checks.STATE_DIR / "WP-OTHER.yaml"
    dump(other, world.state(work_package="WP-OTHER"))
    world.commit_all(world.docs, "other state")
    assert checks.state_roundtrip(world.docs) == []
    return other


def test_wpp01_cr001_uncommitted_state_deletion_is_caught(world: World) -> None:
    _add_other_state(world).unlink()
    errors = checks.state_roundtrip(world.docs)
    assert any("WP-OTHER.yaml: committed in HEAD but missing from the working tree" in e for e in errors), (
        errors
    )


def test_wpp01_cr001_uncommitted_extra_state_is_caught(world: World) -> None:
    dump(world.docs / checks.STATE_DIR / "WP-NEW.yaml", world.state(work_package="WP-NEW"))
    errors = checks.state_roundtrip(world.docs)
    assert any("WP-NEW.yaml: present in the working tree but not committed" in e for e in errors), errors


def test_wpp01_cr001_positive_committed_deletion_passes(world: World) -> None:
    _add_other_state(world).unlink()
    world.commit_all(world.docs, "retire WP-OTHER state")
    assert checks.state_roundtrip(world.docs) == []


def _closed_with_later_content(world: World) -> dict[str, object]:
    record = world.docs / "assurance" / "reviews" / "record.md"
    record.parent.mkdir(parents=True, exist_ok=True)
    record.write_text("later content\n", encoding="utf-8")
    world.commit_all(world.docs, "content")
    return world.state(
        status="CLOSED",
        open_findings=[],
        next_owner=None,
        next_action=None,
        scoping_review=_approved_review(),
    )


@pytest.mark.parametrize("variant", ["missing", "empty", "docs-null", "code-null"])
def test_wpp01_cr002_closed_without_complete_pair_is_caught(world: World, variant: str) -> None:
    state = _closed_with_later_content(world)
    workflow = state["workflow"]
    assert isinstance(workflow, dict)
    if variant == "missing":
        del workflow["current_candidate"]
    elif variant == "empty":
        workflow["current_candidate"] = {}
    else:
        workflow["current_candidate"]["docs" if variant == "docs-null" else "code"] = None
    _accept_on_main(world)
    dump(world.docs / checks.STATE_DIR / "WP-T.yaml", state)
    assert_caught(world, "state", "CLOSED requires the exact accepted pair")


# ---------------------------------------- WP-P01 remediation 2 (characterized trust surface)

UNICODE_STATE = "WP-Ü.yaml"


def test_wpp01_r2_unicode_state_inventory_matches(world: World) -> None:
    dump(world.docs / checks.STATE_DIR / UNICODE_STATE, world.state(work_package="WP-U"))
    world.commit_all(world.docs, "unicode state")
    assert checks.state_roundtrip(world.docs) == []


def test_wpp01_r2_unicode_state_uncommitted_deletion_is_caught(world: World) -> None:
    path = world.docs / checks.STATE_DIR / UNICODE_STATE
    dump(path, world.state(work_package="WP-U"))
    world.commit_all(world.docs, "unicode state")
    path.unlink()
    errors = checks.state_roundtrip(world.docs)
    assert any(f"{UNICODE_STATE}: committed in HEAD but missing" in e for e in errors), errors


def test_wpp01_r2_unicode_state_path_counts_as_state_only(world: World) -> None:
    """diff-tree paths are read losslessly: a non-ASCII state path is still a state-only change."""
    dump(world.docs / checks.STATE_DIR / UNICODE_STATE, world.state(work_package="WP-U"))
    world.commit_all(world.docs, "unicode state after candidate")
    assert "state" not in only_failures(world)


@pytest.mark.parametrize("variant", ["both-code", "both-docs", "swapped"])
def test_wpp01_r2_candidate_sides_bound_to_repositories(world: World, variant: str) -> None:
    state = world.state()
    cand = state["workflow"]["current_candidate"]
    code, docs = dict(cand["code"]), dict(cand["docs"])
    if variant == "both-code":
        cand["docs"] = dict(code)
    elif variant == "both-docs":
        cand["code"] = dict(docs)
    else:
        cand["code"], cand["docs"] = docs, code
    dump(world.docs / checks.STATE_DIR / "WP-T.yaml", state)
    assert_caught(world, "state", "sides are bound to their repositories")


@pytest.mark.parametrize("ref", ["SHA", "HEAD~0", "--output=x", "wp/test..main", "no-such-branch"])
def test_wpp01_r2_candidate_ref_must_be_existing_plain_branch(world: World, ref: str) -> None:
    state = world.state()
    docs = state["workflow"]["current_candidate"]["docs"]
    docs["ref"] = docs["sha"] if ref == "SHA" else ref
    dump(world.docs / checks.STATE_DIR / "WP-T.yaml", state)
    expected = "is not a local branch" if ref == "no-such-branch" else "must be a plain local branch name"
    assert_caught(world, "state", expected)


def test_wpp01_r2_sha_ref_cannot_bypass_chain_rule(world: World) -> None:
    """The sweep witness: ref == candidate SHA made the descendant range empty."""
    record = world.docs / "assurance" / "reviews" / "record.md"
    record.parent.mkdir(parents=True, exist_ok=True)
    record.write_text("content after candidate\n", encoding="utf-8")
    world.commit_all(world.docs, "content")
    state = world.state()
    docs = state["workflow"]["current_candidate"]["docs"]
    docs["ref"] = docs["sha"]
    dump(world.docs / checks.STATE_DIR / "WP-T.yaml", state)
    assert_caught(world, "state", "must be a plain local branch name")


def test_wpp01_r2_closed_requires_main_ref(world: World) -> None:
    _accept_on_main(world)
    _closed(world, ref="wp/test")
    assert_caught(world, "state", "CLOSED requires current_candidate.code.ref == 'main'")


@pytest.mark.parametrize("revision", ["-x", "--output=x", "HEAD..main", "nope"])
def test_wpp01_r2_roundtrip_rejects_bad_revision(world: World, revision: str) -> None:
    errors = checks.state_roundtrip(world.docs, revision)
    assert errors and ("must be HEAD" in errors[0] or "does not name a commit" in errors[0]), errors
