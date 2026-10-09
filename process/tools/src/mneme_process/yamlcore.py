"""The one YAML entry point for every canonical/governance YAML artifact (hazard family H6).

Python's PyYAML resolves YAML 1.1 implicit types (``yes`` -> True, ``2026-10-09`` -> date,
``010`` -> 8). Rust YAML libraries resolve YAML 1.2. A document both languages read must therefore
mean the same thing under both rule sets. This loader enforces that mechanically:

* implicit scalars resolve only per the YAML 1.2 JSON schema subset (true/false, null/~/empty,
  decimal integers without leading zeros, decimal floats with ``.`` or an exponent);
* a document whose YAML 1.1 reading differs from its core reading is rejected: the ambiguous
  scalar must be quoted;
* duplicate mapping keys, anchors/aliases, explicit tags and non-finite floats are rejected;
* the loaded value must be an acyclic graph of JSON-domain nodes (str keys only).

Errors are returned, never raised, by :func:`load_core`.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Any

import yaml
from yaml.nodes import MappingNode, Node, ScalarNode, SequenceNode

_BOOL = re.compile(r"^(?:true|True|TRUE|false|False|FALSE)$")
_NULL = re.compile(r"^(?:~|null|Null|NULL|)$")
_INT = re.compile(r"^-?(?:0|[1-9][0-9]*)$")
_FLOAT = re.compile(r"^-?(?:0|[1-9][0-9]*)(?:\.[0-9]+(?:[eE][-+]?[0-9]+)?|[eE][-+]?[0-9]+)$")


class _CoreLoader(yaml.SafeLoader):
    """SafeLoader with YAML 1.2 JSON-schema implicit resolution only."""


_CoreLoader.yaml_implicit_resolvers = {}
_CoreLoader.add_implicit_resolver("tag:yaml.org,2002:bool", _BOOL, list("tTfF"))
_CoreLoader.add_implicit_resolver("tag:yaml.org,2002:null", _NULL, ["~", "n", "N", ""])
_CoreLoader.add_implicit_resolver("tag:yaml.org,2002:int", _INT, list("-0123456789"))
_CoreLoader.add_implicit_resolver("tag:yaml.org,2002:float", _FLOAT, list("-0123456789"))


def _core_bool(loader: yaml.SafeLoader, node: Node) -> bool:
    assert isinstance(node, ScalarNode)
    return str(node.value).lower() == "true"


_CoreLoader.add_constructor("tag:yaml.org,2002:bool", _core_bool)

_ALLOWED_TAGS = {
    "tag:yaml.org,2002:str",
    "tag:yaml.org,2002:int",
    "tag:yaml.org,2002:float",
    "tag:yaml.org,2002:bool",
    "tag:yaml.org,2002:null",
    "tag:yaml.org,2002:map",
    "tag:yaml.org,2002:seq",
}

MAX_DEPTH = 64
MAX_NODES = 200_000


@dataclass(frozen=True)
class YamlResult:
    value: Any
    errors: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.errors


def _walk_nodes(node: Node, errors: list[str], seen: set[int]) -> None:
    """Reject anchors/aliases (a node reached twice), explicit tags and duplicate keys."""
    stack: list[Node] = [node]
    while stack:
        current = stack.pop()
        if id(current) in seen:
            errors.append(f"line {current.start_mark.line + 1}: anchors/aliases are not allowed")
            continue
        seen.add(id(current))
        if current.tag not in _ALLOWED_TAGS:
            errors.append(f"line {current.start_mark.line + 1}: tag {current.tag!r} is not allowed")
        if isinstance(current, MappingNode):
            keys: set[str] = set()
            for key_node, value_node in current.value:
                if not isinstance(key_node, ScalarNode) or key_node.tag != "tag:yaml.org,2002:str":
                    errors.append(f"line {key_node.start_mark.line + 1}: mapping keys must be strings")
                else:
                    if key_node.value in keys:
                        errors.append(
                            f"line {key_node.start_mark.line + 1}: duplicate key {key_node.value!r}"
                        )
                    keys.add(key_node.value)
                stack.append(value_node)
        elif isinstance(current, SequenceNode):
            stack.extend(current.value)


def _has_surrogate(text: str) -> bool:
    """Python `str` can hold U+D800..U+DFFF; Rust `String` cannot (hazard H2). The portable profile
    admits Unicode scalar values only, explicitly rather than by PyYAML's incidental reader check."""
    return any(0xD800 <= ord(ch) <= 0xDFFF for ch in text)


def _check_domain(value: Any, errors: list[str]) -> None:
    """Iterative JSON-domain, depth and size check."""
    stack: list[tuple[Any, int]] = [(value, 1)]
    count = 0
    while stack:
        item, depth = stack.pop()
        count += 1
        if count > MAX_NODES:
            errors.append(f"document exceeds {MAX_NODES} nodes")
            return
        if isinstance(item, dict):
            if depth > MAX_DEPTH:
                errors.append(f"container depth exceeds {MAX_DEPTH}")
                return
            for key, child in item.items():
                if not isinstance(key, str):
                    errors.append(f"non-string key {key!r}")
                elif _has_surrogate(key):
                    errors.append(f"key {key!r} contains a surrogate code point")
                stack.append((child, depth + 1))
        elif isinstance(item, list):
            if depth > MAX_DEPTH:
                errors.append(f"container depth exceeds {MAX_DEPTH}")
                return
            stack.extend((child, depth + 1) for child in item)
        elif isinstance(item, float):
            if not math.isfinite(item):
                errors.append(f"non-finite float {item!r} is not allowed")
        elif isinstance(item, str):
            if _has_surrogate(item):
                errors.append("string contains a surrogate code point (not a Unicode scalar value)")
        elif item is None or isinstance(item, (bool, int)):
            continue
        else:
            errors.append(f"value of type {type(item).__name__} is outside the JSON domain")


def load_core(text: str) -> YamlResult:
    """Load one YAML document under the cross-language rules. Never raises on bad input."""
    errors: list[str] = []
    try:
        # Syntax-level check first: composition erases explicit-but-redundant syntax such as
        # `!!str x` or an unused `&anchor`, which the portable profile forbids outright.
        for token in yaml.scan(text, Loader=_CoreLoader):
            if isinstance(token, (yaml.TagToken, yaml.AnchorToken, yaml.AliasToken)):
                kind = type(token).__name__.removesuffix("Token").lower()
                errors.append(f"line {token.start_mark.line + 1}: {kind} syntax is not allowed")
        node = yaml.compose(text, Loader=_CoreLoader)
    except Exception as error:
        return YamlResult(None, (f"YAML parse error: {error}",))
    if errors:
        return YamlResult(None, tuple(errors))
    if node is None:
        return YamlResult(None, ("empty YAML document",))
    _walk_nodes(node, errors, set())
    if errors:
        return YamlResult(None, tuple(errors))
    try:
        core_value = yaml.load(text, Loader=_CoreLoader)
        legacy_value = yaml.safe_load(text)
    except Exception as error:
        return YamlResult(None, (f"YAML construct error: {error}",))
    if core_value != legacy_value or _types_differ(core_value, legacy_value):
        errors.append(
            "YAML 1.1 and YAML 1.2-core readings differ; quote the ambiguous scalar(s) "
            f"(first difference: {_first_difference(core_value, legacy_value)})"
        )
    _check_domain(core_value, errors)
    return YamlResult(core_value if not errors else None, tuple(errors))


def _types_differ(a: Any, b: Any) -> bool:
    """`1 == True` in Python; compare structure *and* scalar types."""
    stack: list[tuple[Any, Any]] = [(a, b)]
    while stack:
        x, y = stack.pop()
        if type(x) is not type(y):
            return True
        if isinstance(x, dict):
            if x.keys() != y.keys():
                return True
            stack.extend((x[k], y[k]) for k in x)
        elif isinstance(x, list):
            if len(x) != len(y):
                return True
            stack.extend(zip(x, y, strict=True))
    return False


def _first_difference(a: Any, b: Any, path: str = "$") -> str:
    if type(a) is not type(b):
        return f"{path}: core={a!r} yaml1.1={b!r}"
    if isinstance(a, dict):
        for key in a:
            if key not in b:
                return f"{path}.{key}: missing under YAML 1.1"
            if a[key] != b[key] or _types_differ(a[key], b[key]):
                return _first_difference(a[key], b[key], f"{path}.{key}")
    if isinstance(a, list):
        for i, (x, y) in enumerate(zip(a, b, strict=False)):
            if x != y or _types_differ(x, y):
                return _first_difference(x, y, f"{path}[{i}]")
    return f"{path}: core={a!r} yaml1.1={b!r}"
