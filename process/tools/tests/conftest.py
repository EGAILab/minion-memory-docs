"""A minimal, fully valid two-repository world for negative-control tests.

Every test starts from `world`, whose fixture asserts the baseline passes all checks first (a
control runner proves its own baseline: agent-workflow §5 / Minion-Agent §9.7). Each negative
control then applies exactly one realistic mutation and asserts the intended check — and only the
intended rule — reports it.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest
import yaml

from mneme_process import checks, sources

TOOLS = Path(__file__).resolve().parents[1]
REAL_DOCS = TOOLS.parents[1]
REAL_CODE = REAL_DOCS.parent / "minion-memory"

GIT_ENV = {
    **os.environ,
    "GIT_AUTHOR_NAME": "fixture",
    "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
    "GIT_COMMITTER_NAME": "fixture",
    "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
}

DOC_TEXT = "# Fixture authority\n\n## 1. Intro\n\n| FROZEN | Text. |\n\n## 2. Rules\n\nMore text.\n"

SPEC = """# Fixture spec

### CORE-001 — First rule
<a id="core-001"></a>
- **Profile:** core · **Source status:** FROZEN · **Sources:** [DOC §1]

Statement one (NF-001).

### CORE-002 — Second rule
<a id="core-002"></a>
- **Profile:** core · **Source status:** NORMATIVE · **Sources:** [DOC §1] [DOC §2]

Statement two.
"""

SCENARIO = {
    "scenario_format": 1,
    "id": "core.fixture.first-rule",
    "family": "core",
    "layer": "01",
    "status": "PLACEHOLDER",
    "title": "fixture",
    "requirements": ["CORE-001"],
    "given": {"x": "TO_BE_DEFINED"},
    "when": [{"op": "TO_BE_DEFINED"}],
    "expect": {"y": "TO_BE_DEFINED"},
}


def git(repo: Path, *args: str) -> str:
    done = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, env=GIT_ENV, check=True
    )
    return done.stdout.strip()


def dump(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


class World:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.bundle = root / "bundle"
        self.docs = root / "minion-memory-docs"
        self.code = root / "minion-memory"

    @property
    def ctx(self) -> checks.Context:
        return checks.Context(docs=self.docs, code=self.code, workspace=self.root)

    def run(self, name: str) -> list[str]:
        return checks.run_all(self.ctx, only=[name])[name]

    def all_errors(self) -> dict[str, list[str]]:
        return {k: v for k, v in checks.run_all(self.ctx).items() if v}

    def build(self) -> None:
        self.bundle.mkdir(parents=True)
        (self.bundle / "DOC.md").write_text(DOC_TEXT, encoding="utf-8", newline="\n")
        digest = sources.sha256_file(self.bundle / "DOC.md")
        for repo in (self.docs, self.code):
            repo.mkdir()
            git(repo, "init", "-q", "-b", "wp/test")
        dump(
            self.docs / checks.BUNDLE_MANIFEST,
            {
                "bundle_format": 1,
                "workspace_root": self.root.as_posix(),
                "bundle_root": "bundle",
                "documents": [
                    {
                        "key": "DOC",
                        "file": "DOC.md",
                        "sha256": digest,
                        "declared_version": "1",
                        "authority_rank": 1,
                        "authority_role": "fixture",
                        "normalization_target": ["spec/core.md"],
                        "status": "CURRENT_AUTHORITY",
                    }
                ],
            },
        )
        text_dir = self.docs / checks.SOURCE_TEXT_DIR
        text_dir.mkdir(parents=True)
        (text_dir / "DOC.md").write_text("<!-- derived -->\n\n" + DOC_TEXT, encoding="utf-8", newline="\n")
        dump(self.docs / checks.SOURCE_INDEX, sources.build_index({"DOC": (digest, DOC_TEXT)}))
        (self.docs / "spec").mkdir()
        (self.docs / "spec" / "core.md").write_text(SPEC, encoding="utf-8", newline="\n")
        dump(
            self.docs / checks.FINDINGS_DIR / "F.yaml",
            {
                "register_version": 1,
                "findings": [
                    {
                        "id": "NF-001",
                        "title": "t",
                        "classification": "REQUIREMENT_UNCERTAIN",
                        "owner_decision_required": True,
                        "blocking": ["none"],
                        "status": "OPEN",
                        "sources": ["[DOC §2]"],
                        "requirements": ["CORE-001"],
                        "summary": "s",
                        "recommendation": "r",
                    }
                ],
            },
        )
        (self.docs / "plans").mkdir()
        (self.docs / "plans" / "WP.md").write_text("plan\n", encoding="utf-8")
        dump(
            self.docs / checks.REGISTRY,
            {
                "registry_version": 1,
                "work_packages": {
                    "WP-T": {
                        "requirements": [],
                        "contract": {"status": "DRAFT"},
                        "python": {"status": "NOT_IMPLEMENTED"},
                        "rust": {"status": "NOT_IMPLEMENTED"},
                        "cross_language": {"status": "NOT_CLOSED"},
                        "evidence": "plans/WP.md",
                    }
                },
            },
        )
        for rel in (checks.MANIFEST_SCHEMA, checks.SCENARIO_SCHEMA):
            target = self.code / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REAL_CODE / rel, target)
        rows = []
        for rid, title, status, cites in (
            ("CORE-001", "First rule", "FROZEN", ["[DOC §1]"]),
            ("CORE-002", "Second rule", "NORMATIVE", ["[DOC §1]", "[DOC §2]"]),
        ):
            rows.append(
                {
                    "id": rid,
                    "title": title,
                    "family": "CORE",
                    "profile": "core",
                    "layer": "01",
                    "sources": cites,
                    "spec": f"spec/core.md#{rid.lower()}",
                    "source_status": status,
                    "disposition": "adopted",
                    "scenarios": ["core.fixture.first-rule"] if rid == "CORE-001" else [],
                    "python": {"location": None},
                    "rust": {"location": None},
                    "evidence": [],
                    "findings": ["NF-001"] if rid == "CORE-001" else [],
                }
            )
        dump(
            self.code / checks.MANIFEST,
            {
                "manifest_version": 1,
                "contract": {
                    "bundle_id": "fixture",
                    "bundle_manifest": "x",
                    "spec_root": "x",
                    "status_registry": "x",
                },
                "rows": rows,
            },
        )
        for family in checks.SCENARIO_FAMILIES:
            (self.code / "conformance" / family).mkdir(parents=True, exist_ok=True)
        dump(self.code / "conformance" / "core" / "first-rule.yaml", SCENARIO)
        self.commit_all(self.code, "code")
        self.commit_all(self.docs, "docs")
        self.write_state()
        self.commit_all(self.docs, "state")

    def commit_all(self, repo: Path, message: str) -> str:
        git(repo, "add", "-A")
        git(repo, "commit", "-q", "--allow-empty", "-m", message)
        return git(repo, "rev-parse", "HEAD")

    def state(self, **overrides: Any) -> dict[str, Any]:
        code_sha = git(self.code, "rev-parse", "HEAD")
        docs_sha = git(self.docs, "rev-parse", "HEAD")
        workflow: dict[str, Any] = {
            "schema_version": 2,
            "work_package": "WP-T",
            "title": "fixture",
            "status": "SCOPING",
            "requirements": [],
            "current_candidate": {
                "code": {"repo": "minion-memory", "ref": "wp/test", "sha": code_sha},
                "docs": {"repo": "minion-memory-docs", "ref": "wp/test", "sha": docs_sha},
            },
            "open_findings": ["NF-001"],
            "provisionally_closed": [],
            "convergence": None,
            "governance_source": None,
            "deferred_trigger": None,
            "quarantine": {"derived_from_quarantined_artifact": False},
            "next_owner": "Codex",
            "next_action": "review",
            "updated_by": "Claude",
            "updated_reason": "fixture",
        }
        workflow.update(overrides)
        return {"workflow": workflow}

    def write_state(self, **overrides: Any) -> None:
        dump(self.docs / checks.STATE_DIR / "WP-T.yaml", self.state(**overrides))


@pytest.fixture
def world(tmp_path: Path) -> Iterator[World]:
    w = World(tmp_path / "ws")
    w.root.mkdir()
    w.build()
    baseline = w.all_errors()
    assert baseline == {}, f"baseline must pass before any mutation: {json.dumps(baseline, indent=1)}"
    yield w
