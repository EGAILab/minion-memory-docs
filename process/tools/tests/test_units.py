"""Unit tests for the YAML boundary, anchor derivation and the transition table."""

from __future__ import annotations

import pytest

from mneme_process import sources, transitions
from mneme_process.yamlcore import load_core


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("a: 1\nb: true\nc: null\nd: 1.5\ne: text\n", {"a": 1, "b": True, "c": None, "d": 1.5, "e": "text"}),
        ('a: "yes"\nb: "2026-10-09"\nc: "010"\n', {"a": "yes", "b": "2026-10-09", "c": "010"}),
        ("a: [1, 2]\n", {"a": [1, 2]}),
    ],
)
def test_core_yaml_accepts_portable_documents(text: str, expected: object) -> None:
    result = load_core(text)
    assert result.ok, result.errors
    assert result.value == expected


@pytest.mark.parametrize(
    ("text", "fragment"),
    [
        ("a: yes\n", "readings differ"),
        ("a: 2026-10-09\n", "readings differ"),
        ("a: 010\n", "readings differ"),
        ("a: 0x1F\n", "readings differ"),
        ("on: 1\n", "readings differ"),
        ("a: 1\na: 2\n", "duplicate key"),
        ("a: &x 1\nb: *x\n", "anchors/aliases"),
        ("a: !!binary aGk=\n", "tag"),
        ("a: .inf\n", "readings differ"),
        ("{a: [\n", "parse error"),
        ("", "empty"),
        ("1: x\n", "mapping keys must be strings"),
    ],
)
def test_core_yaml_rejects_nonportable_documents(text: str, fragment: str) -> None:
    result = load_core(text)
    assert not result.ok
    assert any(fragment in e for e in result.errors), result.errors


def test_core_yaml_rejects_excessive_depth() -> None:
    text = "a: " + "[" * 70 + "]" * 70 + "\n"
    result = load_core(text)
    assert any("depth" in e for e in result.errors)


@pytest.mark.parametrize(
    ("heading", "anchor"),
    [
        ("4.1 KnowledgeUnit", "4.1"),
        ("31. Canonical HistoryProjector / normalizer", "31"),
        ("G.3 MemoryScope", "G.3"),
        ("A26 — Dual-profile core", "A26"),
        ("M1 — Durable commit before enrichment", "M1"),
        ("Appendix G - Dual-Profile Generalization (v2.3)", "App-G"),
        ("Document Status Legend", "document-status-legend"),
    ],
)
def test_anchor_rule(heading: str, anchor: str) -> None:
    assert sources.anchor_for(heading) == anchor


def test_repeated_anchor_is_disambiguated() -> None:
    anchors = [a.anchor for a in sources.index_text("## 31. A\n\n### 31. B\n\n## 32. C\n")]
    assert anchors == ["31", "31~2", "32"]


@pytest.mark.parametrize(
    ("source", "target", "legal"),
    [
        ("SCOPING", "CONTRACT_DRAFT", True),
        ("SCOPING", "CLOSED", True),
        ("CONTRACT_REVIEW", "REMEDIATION", False),
        ("REMEDIATION", "CONTRACT_REVIEW", False),
        ("RUST_IMPLEMENTATION", "IMPLEMENTATION_REVIEW", False),
        ("IMPLEMENTATION_REVIEW", "CLOSED", False),
        ("IMPLEMENTATION_REVIEW", "RUST_IMPLEMENTATION", True),
        ("CONTRACT_CONVERGENCE", "FINAL_CONTRACT_REVIEW", True),
        ("CLOSURE_REVIEW", "CLOSED", True),
        ("PYTHON_IMPLEMENTATION", "BLOCKED_FOR_OWNER", True),
        ("BLOCKED_FOR_OWNER", "SCOPING", True),
        ("BLOCKED_FOR_OWNER", "CLOSED", False),
        ("INCIDENT", "SCOPING", False),
        ("SCOPING", "BLOCKED", False),
    ],
)
def test_transition_table(source: str, target: str, legal: bool) -> None:
    assert transitions.is_legal(source, target) is legal
