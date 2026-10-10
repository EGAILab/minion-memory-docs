"""WP-00 bootstrap validation checks across the docs and code repositories.

Each check returns a list of error strings; an empty list is PASS. Checks are total: malformed
input is reported, never raised. They validate mechanical well-formedness and traceability only.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

import jsonschema

from . import sources, transitions
from .spec import CITATION, PROFILES, SOURCE_STATUSES, SpecParse, inventory, parse_spec
from .yamlcore import load_core

BUNDLE_MANIFEST = "reference/mneme-v2.3-source-bundle.yaml"
SOURCE_TEXT_DIR = "reference/source-text"
SOURCE_INDEX = "reference/source-index.yaml"
SPEC_ROOT = "spec"
STATE_DIR = "process/state"
REGISTRY = "process/certification-registry.yaml"
FINDINGS_DIR = "assurance/findings"
MANIFEST = "mneme-contract-manifest.yaml"
MANIFEST_SCHEMA = "schemas/mneme-contract-manifest.schema.json"
SCENARIO_SCHEMA = "conformance/schema/scenario.schema.json"
SCENARIO_FAMILIES = ("core", "learning", "agent")
STATE_ONLY_PATHS = ("process/state/", "process/handoffs/", "process/certification-registry.yaml")

FAMILIES: dict[str, str] = {
    "ARCH": "core",
    "CORE": "core",
    "HIST": "core",
    "PROJ": "core",
    "RET": "core",
    "SCOPE": "core",
    "PERS": "core",
    "SER": "core",
    "BKP": "core",
    "PRIV": "core",
    "KNOW": "learning",
    "PKG": "learning",
    "LEARN": "learning",
    "OBS": "learning",
    "EVAL": "learning",
    "EVID": "learning",
    "LMEM": "learning",
    "SCHED": "learning",
    "MIG": "learning",
    "ACAP": "agent",
    "AMEM": "agent",
    "ACON": "agent",
    "ARET": "agent",
    "ACTX": "agent",
    "MINT": "agent",
}

CLASSIFICATIONS = frozenset(
    {
        "REQUIREMENT_UNCERTAIN",
        "CONTRACT_ASSURANCE_DEFECT",
        "IMPLEMENTATION_DEFECT",
        "CROSS_LANGUAGE_CONFORMANCE_DEFECT",
        "INTEGRATION_CONTRACT_DEFECT",
        "SEMANTICS_NEUTRAL_HARDENING",
        "OWNER_DECISION_REQUIRED",
        "CONTRACT_CONSTRAINED_RISK",
    }
)
FINDING_STATUSES = frozenset({"OPEN", "PROVISIONALLY_CLOSED", "CLOSED", "WITHDRAWN"})
LANG_STATUSES = frozenset({"NOT_IMPLEMENTED", "IN_PROGRESS", "APPROVED", "CERTIFIED", "REVALIDATE_REQUIRED"})
XL_STATUSES = frozenset({"NOT_CLOSED", "CERTIFIED_CLOSED"})
CONTRACT_STATUSES = frozenset({"DRAFT", "IN_REVIEW", "AGREED", "ACCEPTED"})
OWNERS = frozenset({"Claude", "Codex", "Owner"})
AGENTS = frozenset({"Claude", "Codex"})
# Operational tokens are complete ASCII tokens, always used with `fullmatch` (CE-P01-01 D11/D12):
# no `$`-before-newline leniency, no Unicode digits, no prefix matches.
SHA = re.compile(r"[0-9a-f]{40}", re.ASCII)
WP_ID = re.compile(r"WP-[A-Z0-9]{1,8}", re.ASCII)
REQ_ID = re.compile(r"(?P<family>[A-Z]{2,5})-[0-9]{3}", re.ASCII)
FINDING_ID = re.compile(r"NF-[0-9]{3}|WP[0-9A-Z]+-CR-[0-9]{3}", re.ASCII)
SOURCE_KEY = re.compile(r"[A-Z][A-Z0-9]{0,15}", re.ASCII)  # the citation key grammar (spec.CITATION)
STATE_FILE = re.compile(r"(?P<wp>WP-[A-Z0-9]{1,8})\.yaml", re.ASCII)  # D1: the only state entry
HISTORY_KEYS = frozenset({"reviews", "remediations", "review_history", "history_log"})
STATE_BUDGET = 8000
STATE_ONLY_DIRS = ("process/state/", "process/handoffs/")


def _is_str(value: Any) -> bool:
    return isinstance(value, str)


def _nonblank(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def is_requirement_id(value: Any) -> bool:
    match = REQ_ID.fullmatch(value) if isinstance(value, str) else None
    return bool(match) and match.group("family") in FAMILIES  # type: ignore[union-attr]


def is_finding_id(value: Any) -> bool:
    return isinstance(value, str) and bool(FINDING_ID.fullmatch(value))


@dataclass
class Context:
    docs: Path
    code: Path
    workspace: Path | None = None
    deep_sources: bool = False


# --------------------------------------------------------------------------- helpers


def _load(path: Path, errors: list[str], label: str | None = None) -> Any:
    label = label or path.as_posix()
    if not path.is_file():
        errors.append(f"{label}: missing")
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        errors.append(f"{label}: unreadable ({error})")
        return None
    result = load_core(text)
    errors.extend(f"{label}: {e}" for e in result.errors)
    return result.value


def _no_graft_file(repo: Path) -> Path:
    """The graft-file path given to Git: inside the project scratch root (OWN-001), never created.
    Its existence is itself a refused overlay (`_graph_overlays`)."""
    return repo.resolve().parent / ".tmp" / "mneme-process" / "no-grafts" / "absent"


def _git_env(repo: Path) -> dict[str, str]:
    """A hermetic Git environment (CE-P01-01 D7).

    Every inherited ``GIT_*`` variable is removed: repository/object/namespace selectors, ceiling
    directories, injected configuration and replacement-ref bases can never substitute another
    repository or graph for the one named by ``-C`` (M01-M04, CH01, CH02). Replacement objects and
    legacy grafts are disabled (``--no-replace-objects`` alone does not disable ``info/grafts``;
    CH03), so the object graph is the real one. Repositories carrying overlays are refused too.
    """
    env = {key: value for key, value in os.environ.items() if not key.upper().startswith("GIT_")}
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    env["GIT_GRAFT_FILE"] = str(_no_graft_file(repo))
    return env


def _run_git(repo: Path, *args: str) -> subprocess.CompletedProcess[bytes] | None:
    try:
        return subprocess.run(
            ["git", "-C", str(repo), *args], capture_output=True, check=False, timeout=60, env=_git_env(repo)
        )
    except (OSError, subprocess.TimeoutExpired):
        return None


def _git(repo: Path, *args: str) -> tuple[int, str]:
    done = _run_git(repo, *args)
    if done is None:
        return 1, "git could not be run"
    # Never the platform code page: git emits UTF-8 (paths, messages, file contents).
    return done.returncode, done.stdout.decode("utf-8", errors="replace").strip()


def _nul_records(data: bytes) -> list[bytes] | None:
    """Split NUL-terminated records (D4): non-empty output must end in NUL; no empty record."""
    if not data:
        return []
    if not data.endswith(b"\0"):
        return None
    records = data[:-1].split(b"\0")
    return None if any(not record for record in records) else records


def _git_paths(repo: Path, *args: str) -> tuple[int, list[str]]:
    """Run a git command that lists paths, losslessly (WPP01-CR-001, CE-P01-01 D4).

    Requests NUL-terminated output (`-z` must be among `args`) and decodes the raw path bytes as
    strict UTF-8, so `core.quotePath` display quoting (e.g. ``"WP-\\303\\234.yaml"``) never reaches
    a comparison. No trimming, case folding or normalization. Undecodable bytes or broken framing
    are reported as a failure, not guessed.
    """
    done = _run_git(repo, *args)
    if done is None:
        return 1, []
    if done.returncode != 0:
        return done.returncode, []
    records = _nul_records(done.stdout)
    if records is None:
        return 1, []
    try:
        return 0, [record.decode("utf-8") for record in records]
    except UnicodeDecodeError:
        return 1, []


# Candidate sides are bound to their canonical repositories (WPP01-CR-002).
SIDE_REPOS: dict[str, str] = {"code": "minion-memory", "docs": "minion-memory-docs"}
# A plain local branch name: no option-like, range, reflog or revision-suffix syntax.
BRANCH = re.compile(r"(?!-)(?!.*\.\.)(?!.*//)[A-Za-z0-9._/-]+(?<![./])", re.ASCII)


def plain_branch(text: Any) -> bool:
    """A candidate `ref` / roundtrip branch spelling (D5, D8): a plain name, resolved only as
    ``refs/heads/<name>``. Never ``HEAD``, a qualified ``refs/...`` spelling or a 40-hex form."""
    return (
        isinstance(text, str)
        and bool(BRANCH.fullmatch(text))
        and text != "HEAD"
        and not text.startswith("refs/")
        and not SHA.fullmatch(text)
    )


def valid_revision(text: Any) -> bool:
    """A roundtrip revision spelling (D8): exactly `HEAD`, a full 40-hex OID or a plain branch."""
    return text == "HEAD" or (isinstance(text, str) and bool(SHA.fullmatch(text))) or plain_branch(text)


def _object_type(repo: Path, oid: str) -> str | None:
    status, kind = _git(repo, "cat-file", "-t", oid)
    return kind if status == 0 else None


def _local_head(repo: Path, name: str) -> tuple[str | None, str | None]:
    """Resolve ``refs/heads/<name>`` once to a commit OID (D5, D8).

    Returns ``(oid, None)`` or ``(None, reason)``. A symbolic head is refused: following it could
    leave the local-branch namespace (J05). Tags, remotes and abbreviations are never consulted.
    """
    if not plain_branch(name):
        return None, "is not a plain local branch name"
    qualified = f"refs/heads/{name}"
    # `symbolic-ref -q`: exit 0 = symbolic, exit 1 = not symbolic; any other result is a failed
    # query and never evidence of a plain head (CL-002).
    status = _git(repo, "symbolic-ref", "-q", qualified)[0]
    if status == 0:
        return None, "is a symbolic ref (refused)"
    if status != 1:
        return None, "cannot determine whether it is a symbolic ref (query failed)"
    status, line = _git(repo, "show-ref", "--verify", qualified)
    parts = line.split(" ")
    if status != 0 or len(parts) != 2 or parts[1] != qualified or not SHA.fullmatch(parts[0]):
        return None, "is not a local branch"
    if _object_type(repo, parts[0]) != "commit":
        return None, "does not point at a commit"
    return parts[0], None


def _graph_overlays(repo: Path) -> list[str]:
    """Overlays that could make Git's graph differ from real object ancestry (D7) are refused."""
    found: list[str] = []
    status, common = _git(repo, "rev-parse", "--path-format=absolute", "--git-common-dir")
    if status != 0 or not common:
        return [f"{repo.name}: cannot locate the git administrative directory"]
    # A failed or unrecognized query is an error, never evidence of absence (CL-002).
    status, shallow = _git(repo, "rev-parse", "--is-shallow-repository")
    if status != 0 or shallow not in ("true", "false"):
        return [f"{repo.name}: cannot determine whether the repository is shallow; ancestry proofs refused"]
    if shallow == "true":
        found.append("shallow history")
    if (Path(common) / "info" / "grafts").exists():
        found.append("info/grafts")
    if _no_graft_file(repo).exists():
        found.append(f"graft file {_no_graft_file(repo)}")
    status, refs = _git(repo, "for-each-ref", "--format=%(refname)", "refs/replace/")
    if status != 0 or refs:
        found.append("replacement refs (refs/replace/)")
    if not found:
        return []
    return [f"{repo.name}: git graph overlay present ({', '.join(found)}); ancestry proofs refused"]


def _bundle(ctx: Context, errors: list[str]) -> dict[str, Any] | None:
    bundle = _load(ctx.docs / BUNDLE_MANIFEST, errors, BUNDLE_MANIFEST)
    if not isinstance(bundle, dict) or not isinstance(bundle.get("documents"), list):
        if bundle is not None:
            errors.append(f"{BUNDLE_MANIFEST}: documents must be a list")
        return None
    return bundle


def _index(ctx: Context, errors: list[str]) -> dict[str, set[str]]:
    index = _load(ctx.docs / SOURCE_INDEX, errors, SOURCE_INDEX)
    out: dict[str, set[str]] = {}
    if not isinstance(index, dict) or not isinstance(index.get("documents"), dict):
        if index is not None:
            errors.append(f"{SOURCE_INDEX}: documents must be a mapping")
        return out
    for key, doc in index["documents"].items():
        anchors = doc.get("anchors") if isinstance(doc, dict) else None
        if not isinstance(anchors, list):
            errors.append(f"{SOURCE_INDEX}: {key}.anchors must be a list")
            continue
        out[key] = {str(a.get("anchor")) for a in anchors if isinstance(a, dict)}
    return out


def _spec(ctx: Context) -> SpecParse:
    return parse_spec(ctx.docs / SPEC_ROOT, ctx.docs)


def _finding_ids(ctx: Context, errors: list[str]) -> dict[str, dict[str, Any]]:
    found: dict[str, dict[str, Any]] = {}
    directory = ctx.docs / FINDINGS_DIR
    paths, inventory_errors = (
        inventory(directory, ".yaml", ctx.docs, recursive=False) if directory.is_dir() else ([], [])
    )
    errors.extend(inventory_errors)
    for path in paths:
        label = path.relative_to(ctx.docs).as_posix()
        data = _load(path, errors, label)
        if data is None:
            continue
        items = data.get("findings") if isinstance(data, dict) else None
        if not isinstance(items, list):
            errors.append(f"{label}: findings must be a list")
            continue
        for item in items:
            if not isinstance(item, dict) or not isinstance(item.get("id"), str):
                errors.append(f"{label}: finding without string id")
                continue
            if item["id"] in found:
                errors.append(f"{label}: duplicate finding id {item['id']}")
            found[item["id"]] = item
    return found


def _manifest(ctx: Context, errors: list[str]) -> dict[str, Any] | None:
    data = _load(ctx.code / MANIFEST, errors, MANIFEST)
    if data is None:
        return None
    try:
        schema = json.loads((ctx.code / MANIFEST_SCHEMA).read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        errors.append(f"{MANIFEST_SCHEMA}: unreadable ({error})")
        return None
    validator = jsonschema.Draft202012Validator(schema)
    for issue in sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path)):
        path = "/".join(str(p) for p in issue.absolute_path)
        errors.append(f"{MANIFEST}: schema: {path}: {issue.message}")
    return data if isinstance(data, dict) else None


def _scenarios(ctx: Context, errors: list[str]) -> dict[str, tuple[str, dict[str, Any]]]:
    out: dict[str, tuple[str, dict[str, Any]]] = {}
    try:
        schema = json.loads((ctx.code / SCENARIO_SCHEMA).read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        errors.append(f"{SCENARIO_SCHEMA}: unreadable ({error})")
        return out
    validator = jsonschema.Draft202012Validator(schema)
    for family in SCENARIO_FAMILIES:
        directory = ctx.code / "conformance" / family
        if not directory.is_dir():
            errors.append(f"conformance/{family}: missing directory")
            continue
        paths, inventory_errors = inventory(
            directory, ".yaml", ctx.code, recursive=True, skip_names=frozenset({"README.md"})
        )
        errors.extend(f"{e} (canonical scenarios must be .yaml)" for e in inventory_errors)
        for path in paths:
            label = path.relative_to(ctx.code).as_posix()
            data = _load(path, errors, label)
            if data is None:
                continue
            schema_errors = list(validator.iter_errors(data))
            for issue in schema_errors:
                errors.append(f"{label}: schema: {'/'.join(map(str, issue.absolute_path))}: {issue.message}")
            if schema_errors or not isinstance(data, dict):
                continue
            sid = data["id"]
            if sid in out:
                errors.append(f"{label}: duplicate scenario id {sid} (also {out[sid][0]})")
            if data["family"] != family or not sid.startswith(family + "."):
                errors.append(f"{label}: id/family/directory disagree ({sid}, {data['family']}, {family})")
            out[sid] = (label, data)
    return out


def _has_placeholder(value: Any) -> bool:
    stack = [value]
    while stack:
        item = stack.pop()
        if isinstance(item, str) and item.startswith("TO_BE_"):
            return True
        if isinstance(item, dict):
            stack.extend(item.values())
        elif isinstance(item, list):
            stack.extend(item)
    return False


# --------------------------------------------------------------------------- checks


def _nested_markers(repo: Path) -> tuple[list[Path], list[str]]:
    """Directories below `repo` holding an entry named exactly `.git` (D16, CL-001), plus errors.

    An exact-name and location domain, identical on every host: `.GIT` is not a marker, the root's
    own `.git` (file or directory) is the administrative marker, and symlinked directories are not
    followed. A directory that cannot be read is a named error: an incomplete scan never reports
    the absence of a nested repository (D13, R1).
    """
    found: list[Path] = []
    unreadable: list[str] = []

    def failed(error: OSError) -> None:
        unreadable.append(f"cannot scan {error.filename or repo} for nested repositories ({error})")

    for current, dirs, files in os.walk(repo, onerror=failed):
        here = Path(current)
        if here != repo and (".git" in dirs or ".git" in files):
            found.append(here)
        dirs[:] = sorted(d for d in dirs if d != ".git")
    return sorted(found), unreadable


def check_repos(ctx: Context) -> list[str]:
    errors: list[str] = []
    docs, code = ctx.docs.resolve(), ctx.code.resolve()
    for name, repo in (("docs", docs), ("code", code)):
        if not (repo / ".git").exists():
            errors.append(f"{name} repo {repo} is not a git repository root")
            continue
        status, top = _git(repo, "rev-parse", "--show-toplevel")
        if status != 0 or Path(top).resolve() != repo:
            errors.append(f"{name} repo toplevel is {top!r}, expected {repo}")
        markers, scan_errors = _nested_markers(repo)
        errors.extend(f"nested git repository inside {name} repo: {nested}" for nested in markers)
        errors.extend(f"{name} repo: {error}" for error in scan_errors)
    if docs == code or docs in code.parents or code in docs.parents:
        errors.append("docs and code repositories must be disjoint siblings")
    parent = docs.parent
    done = _run_git(parent, "rev-parse", "--show-toplevel")
    if done is not None and done.returncode == 0:
        top = done.stdout.decode("utf-8", errors="replace").strip()
        errors.append(f"workspace root {parent} is inside a git repository ({top})")
    elif done is None or b"not a git repository" not in done.stderr:
        # Only git's own "not a git repository" answer proves absence; a failed query never does
        # (CL-002 neighborhood). A localized message therefore fails closed.
        errors.append(f"workspace root {parent}: cannot determine whether it is inside a git repository")
    for name, repo in (("docs", docs), ("code", code)):
        for forbidden in (".tmp", "review-worktrees"):
            if (repo / forbidden).exists():
                errors.append(
                    f"{name} repo contains {forbidden}/ (OWN-001: scratch lives in the project root)"
                )
    return errors


def _source_texts(ctx: Context) -> tuple[list[Path], list[str]]:
    directory = ctx.docs / SOURCE_TEXT_DIR
    if not directory.is_dir():
        return [], []
    return inventory(directory, ".md", ctx.docs, recursive=False)


def safe_relative_file(text: Any) -> bool:
    """D14: a bundle file is a relative path inside bundle_root: no '..', absolute or drive form."""
    if not isinstance(text, str) or not text or "\\" in text or "\0" in text:
        return False
    windows = PureWindowsPath(text)
    if PurePosixPath(text).is_absolute() or windows.is_absolute() or windows.drive or windows.root:
        return False
    return all(part not in ("", ".", "..") for part in text.split("/"))


def source_entry_errors(entry: Any) -> list[str]:
    """D14 shape of one `documents[]` entry: string key in the citation grammar, safe file, sha."""
    if not isinstance(entry, dict):
        return [f"{BUNDLE_MANIFEST}: document entry must be a mapping"]
    key = entry.get("key")
    errors: list[str] = []
    if not isinstance(key, str) or not SOURCE_KEY.fullmatch(key):
        errors.append(f"{BUNDLE_MANIFEST}: document key {key!r} must match [A-Z][A-Z0-9]{{0,15}}")
    if not safe_relative_file(entry.get("file")):
        errors.append(
            f"{BUNDLE_MANIFEST}: {key!r} file {entry.get('file')!r} must be a relative path "
            "inside bundle_root"
        )
    digest = entry.get("sha256")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest, re.ASCII):
        errors.append(f"{BUNDLE_MANIFEST}: {key!r} sha256 must be 64 lowercase hex")
    return errors


def check_sources(ctx: Context) -> list[str]:
    errors: list[str] = []
    errors.extend(_source_texts(ctx)[1])
    bundle = _bundle(ctx, errors)
    if bundle is None:
        return errors
    workspace = ctx.workspace or Path(str(bundle.get("workspace_root", "")))
    root = workspace / str(bundle.get("bundle_root", ""))
    expected: dict[str, str] = {}
    for entry in bundle["documents"]:
        if not isinstance(entry, dict):
            errors.append(f"{BUNDLE_MANIFEST}: document entry must be a mapping")
            continue
        missing = [
            k
            for k in (
                "key",
                "file",
                "sha256",
                "declared_version",
                "authority_rank",
                "authority_role",
                "normalization_target",
                "status",
            )
            if k not in entry
        ]
        if missing:
            errors.append(f"{BUNDLE_MANIFEST}: {entry.get('key')}: missing {missing}")
            continue
        entry_errors = source_entry_errors(entry)
        if entry_errors:
            errors.extend(entry_errors)
            continue
        key = entry["key"]
        if key in expected:
            errors.append(f"{BUNDLE_MANIFEST}: duplicate document key {key}")
        expected[key] = str(entry["sha256"])
        path = root / str(entry["file"])
        if not path.is_file():
            errors.append(f"{key}: source file missing: {path}")
        elif sources.sha256_file(path) != entry["sha256"]:
            errors.append(f"{key}: sha256 mismatch for {path}")
    zip_entry = bundle.get("bundle_zip")
    if isinstance(zip_entry, dict):
        path = workspace / str(zip_entry.get("path"))
        if not path.is_file() or sources.sha256_file(path) != zip_entry.get("sha256"):
            errors.append(f"bundle zip missing or sha256 mismatch: {path}")
    for entry in bundle.get("superseded") or []:
        path = workspace / str(entry.get("path"))
        if entry.get("sha256") and path.is_file() and sources.sha256_file(path) != entry["sha256"]:
            errors.append(f"superseded artifact sha256 mismatch: {path}")
    index = _load(ctx.docs / SOURCE_INDEX, errors, SOURCE_INDEX)
    if not isinstance(index, dict) or not isinstance(index.get("documents"), dict):
        return errors
    for key, doc in index["documents"].items():
        if not isinstance(doc, dict):
            errors.append(f"{SOURCE_INDEX}: {key} must be a mapping")
            continue
        if key not in expected:
            errors.append(f"{SOURCE_INDEX}: {key} not in the bundle manifest")
            continue
        if doc.get("source_sha256") != expected[key]:
            errors.append(f"{SOURCE_INDEX}: {key} indexes different source bytes than the manifest")
        text_path = ctx.docs / SOURCE_TEXT_DIR / f"{key}.md"
        if not text_path.is_file():
            errors.append(f"{SOURCE_TEXT_DIR}/{key}.md missing")
            continue
        parts = text_path.read_bytes().decode("utf-8", errors="replace").split("\n", 2)
        if len(parts) < 3:
            errors.append(f"{SOURCE_TEXT_DIR}/{key}.md has no derived header")
            continue
        body = parts[2]
        if hashlib.sha256(body.encode("utf-8")).hexdigest() != doc.get("derived_text_sha256"):
            errors.append(f"{SOURCE_TEXT_DIR}/{key}.md does not match the index (hand-edited?)")
        if [a.get("anchor") for a in doc.get("anchors", [])] != [a.anchor for a in sources.index_text(body)]:
            errors.append(f"{SOURCE_INDEX}: {key} anchors do not match the derived text")
        if ctx.deep_sources:
            entry = next(e for e in bundle["documents"] if e.get("key") == key)
            derived = sources.derive_text(root / str(entry["file"]))
            if derived != body:
                errors.append(f"{key}: re-derived text differs from {SOURCE_TEXT_DIR}/{key}.md")
    return errors


_TABLE_CELL_SPLIT = re.compile(r"(?<!\\)\|")
_FROZEN_LINE = re.compile(r"^FROZEN\s+[—-]\s")


def has_positive_frozen_label(text: str) -> bool:
    """Whether derived source text carries a *positive* FROZEN status label (WP00-CR-014).

    Positive forms observed in the bundle:
      * a table cell whose trimmed text is ``FROZEN`` or starts with ``FROZEN `` (e.g. a status box
        ``| FROZEN | ... |``, a status register ``| decision | FROZEN |``, or a scoped
        ``FROZEN boundary / PROVISIONAL vocabulary``);
      * a paragraph line starting ``FROZEN —`` (FND §8, §17).
    Not labels: ``NOT FROZEN``, a word inside prose or inside a cell (``Added FROZEN invariant``),
    and change records written with ``->`` (FND Appendix E ``FROZEN -> PROVISIONAL``), which
    describe a transition rather than a current status.
    """
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("|"):
            for cell in _TABLE_CELL_SPLIT.split(stripped.strip("|")):
                value = cell.strip()
                if (value == "FROZEN" or value.startswith("FROZEN ")) and "->" not in value:
                    return True
        elif _FROZEN_LINE.match(stripped):
            return True
    return False


def _frozen_labelled_sections(ctx: Context) -> set[tuple[str, str]]:
    """(document key, anchor) of every source section carrying a positive FROZEN status label.

    A necessary (not sufficient) condition for a requirement's FROZEN status: whether the label
    actually covers the requirement's main statement stays a reviewer judgment.
    """
    found: set[tuple[str, str]] = set()
    for path in _source_texts(ctx)[0]:
        try:
            parts = path.read_bytes().decode("utf-8").split("\n", 2)
        except (OSError, UnicodeDecodeError):
            continue  # reported by check_sources
        if len(parts) < 3:
            continue
        body = parts[2]
        lines = body.splitlines()
        anchors = sources.index_text(body)
        for i, anchor in enumerate(anchors):
            end = anchors[i + 1].line - 1 if i + 1 < len(anchors) else len(lines)
            if has_positive_frozen_label("\n".join(lines[anchor.line : end])):
                found.add((path.stem, anchor.anchor))
    return found


def check_spec(ctx: Context) -> list[str]:
    errors: list[str] = []
    index = _index(ctx, errors)
    parsed = _spec(ctx)
    errors.extend(parsed.errors)
    # The FROZEN-label guard consumes the source-text inventory: its violations are named here too,
    # not only by check_sources (original E05 caller, CL-001).
    errors.extend(_source_texts(ctx)[1])
    frozen_sections = _frozen_labelled_sections(ctx)
    for req in parsed.requirements:
        if req.source_status != "FROZEN":
            continue
        cited = {(m.group(1), m.group(2)) for m in (CITATION.fullmatch(s) for s in req.sources) if m}
        if not cited & frozen_sections:
            errors.append(
                f"{req.file}:{req.line}: {req.id} is FROZEN but cites no source section carrying a "
                "FROZEN label (spec/README.md §3)"
            )
    findings = _finding_ids(ctx, [])
    seen: dict[str, str] = {}
    for req in parsed.requirements:
        where = f"{req.file}:{req.line}"
        if req.id in seen:
            errors.append(f"{where}: duplicate requirement id {req.id} (first at {seen[req.id]})")
        seen.setdefault(req.id, where)
        family = req.id.split("-")[0]
        if family not in FAMILIES:
            errors.append(f"{where}: unknown family {family}")
        if req.anchor is not None and req.anchor != req.id.lower():
            errors.append(f"{where}: anchor {req.anchor!r} does not match {req.id}")
        if req.profile is not None and req.profile not in PROFILES:
            errors.append(f"{where}: {req.id} profile {req.profile!r} invalid")
        if req.source_status is not None and req.source_status not in SOURCE_STATUSES:
            errors.append(f"{where}: {req.id} source status {req.source_status!r} invalid")
        if req.profile is not None and not req.sources:
            errors.append(f"{where}: {req.id} cites no sources")
        if len(set(req.sources)) != len(req.sources):
            errors.append(f"{where}: {req.id} repeats a source citation")
    for file, line, key, anchor in parsed.citations:
        if key not in index:
            errors.append(f"{file}:{line}: citation [{key} §{anchor}] names an unknown document")
        elif anchor not in index[key]:
            errors.append(f"{file}:{line}: citation [{key} §{anchor}] does not resolve")
    for file, line, ref in parsed.finding_refs:
        if ref not in findings:
            errors.append(f"{file}:{line}: {ref} is not a registered finding")
    return errors


def check_manifest(ctx: Context) -> list[str]:
    errors: list[str] = []
    manifest = _manifest(ctx, errors)
    parsed = _spec(ctx)
    scenarios = _scenarios(ctx, [])
    findings = _finding_ids(ctx, [])
    if manifest is None or not isinstance(manifest.get("rows"), list):
        return errors
    spec_by_id = {r.id: r for r in parsed.requirements}
    rows: dict[str, dict[str, Any]] = {}
    for row in manifest["rows"]:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str):
            continue
        rid = row["id"]
        if rid in rows:
            errors.append(f"{MANIFEST}: duplicate row {rid}")
        rows[rid] = row
        req = spec_by_id.get(rid)
        if req is None:
            errors.append(f"{MANIFEST}: row {rid} has no requirement in spec/")
            continue
        if row.get("spec") != f"{req.file}#{rid.lower()}":
            errors.append(f"{MANIFEST}: {rid} spec anchor {row.get('spec')!r} != {req.file}#{rid.lower()}")
        if row.get("sources") != req.sources:
            errors.append(f"{MANIFEST}: {rid} sources differ from the spec block")
        if row.get("profile") != req.profile:
            errors.append(f"{MANIFEST}: {rid} profile differs from the spec block")
        if row.get("source_status") != req.source_status:
            errors.append(f"{MANIFEST}: {rid} source_status differs from the spec block")
        if row.get("title") != req.title:
            errors.append(f"{MANIFEST}: {rid} title differs from the spec heading")
        if row.get("family") != rid.split("-")[0]:
            errors.append(f"{MANIFEST}: {rid} family field disagrees with the id")
        for sid in row.get("scenarios") or []:
            if sid not in scenarios:
                errors.append(f"{MANIFEST}: {rid} lists unknown scenario {sid}")
        for fid in row.get("findings") or []:
            if fid not in findings:
                errors.append(f"{MANIFEST}: {rid} lists unknown finding {fid}")
    for rid in spec_by_id:
        if rid not in rows:
            errors.append(f"{MANIFEST}: no manifest row for spec requirement {rid}")
    return errors


def check_conformance(ctx: Context) -> list[str]:
    errors: list[str] = []
    scenarios = _scenarios(ctx, errors)
    manifest = _manifest(ctx, [])
    rows = {
        r["id"]: r
        for r in (manifest or {}).get("rows", [])
        if isinstance(r, dict) and isinstance(r.get("id"), str)
    }
    for sid, (label, data) in scenarios.items():
        placeholder = _has_placeholder(data)
        if data["status"] == "ACTIVE" and placeholder:
            errors.append(f"{label}: ACTIVE scenario contains a TO_BE_ placeholder")
        if data["status"] == "PLACEHOLDER" and not placeholder:
            errors.append(f"{label}: PLACEHOLDER scenario contains no TO_BE_ marker")
        for rid in data["requirements"]:
            row = rows.get(rid)
            if row is None:
                errors.append(f"{label}: requirement {rid} has no manifest row")
            elif sid not in (row.get("scenarios") or []):
                errors.append(f"{label}: manifest row {rid} does not list scenario {sid}")
    return errors


def _kind(path: Path) -> str:
    """Entry kind without following symlinks (D3)."""
    try:
        mode = os.lstat(path).st_mode
    except FileNotFoundError:
        return "missing"
    except OSError:
        return "unreadable"
    if stat.S_ISLNK(mode):
        return "symlink"
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    return "special file"


_GIT_KINDS = {
    b"100644": "file",
    b"100755": "file",
    b"120000": "symlink",
    b"040000": "directory",
    b"160000": "gitlink",
}


def _unsupported(name: str, kind: str, where: str) -> str:
    return (
        f"{STATE_DIR}/{name!r}: unsupported state entry ({kind}{where}); only regular "
        "<WP-ID>.yaml files may appear in the state area (CE-P01-01 D1/D3)"
    )


def _state_working(docs: Path) -> tuple[dict[str, Path], list[str]]:
    """Working state inventory: canonical members by name, plus one error per other entry (D1)."""
    directory = docs / STATE_DIR
    if _kind(directory) != "directory":
        return {}, []
    members: dict[str, Path] = {}
    errors: list[str] = []
    try:
        names = sorted(os.listdir(directory))
    except OSError as error:
        return {}, [f"{STATE_DIR}: cannot list the working state area ({error})"]
    for name in names:
        kind = _kind(directory / name)
        if kind == "file" and STATE_FILE.fullmatch(name):
            members[name] = directory / name
        else:
            errors.append(_unsupported(name, kind, " in the working tree"))
    return members, errors


def _state_committed(docs: Path, oid: str) -> tuple[dict[str, str] | None, list[str]]:
    """Committed state inventory at one commit OID: canonical members by name -> blob OID (D1/D3)."""
    done = _run_git(docs, "ls-tree", "-z", f"{oid}:{STATE_DIR}")
    records = _nul_records(done.stdout) if done is not None and done.returncode == 0 else None
    if records is None:
        return None, [f"{STATE_DIR}: cannot list committed state files in {oid[:12]}"]
    members: dict[str, str] = {}
    errors: list[str] = []
    for record in records:
        meta, tab, raw_name = record.partition(b"\t")
        fields = meta.split(b" ")
        if not tab or len(fields) != 3:
            return None, [f"{STATE_DIR}: malformed tree listing in {oid[:12]}"]
        kind = _GIT_KINDS.get(fields[0], "special entry")
        try:
            name = raw_name.decode("utf-8")
        except UnicodeDecodeError:
            errors.append(_unsupported(repr(raw_name), "non-UTF-8 name", f" committed in {oid[:12]}"))
            continue
        if kind == "file" and fields[1] == b"blob" and STATE_FILE.fullmatch(name):
            members[name] = fields[2].decode("ascii")
        else:
            errors.append(_unsupported(name, kind, f" committed in {oid[:12]}"))
    return members, errors


def validate_state(state: Any, label: str) -> list[str]:
    """Structural invariants of one state document (coordination-state.md §3).

    A pure-object gate: `label` is a diagnostic label, never a path. File identity (stem ==
    work_package) is enforced by the file-aware gates (CE-P01-01 D2).
    """
    errors: list[str] = []
    if not isinstance(state, dict) or not isinstance(state.get("workflow"), dict):
        return [f"{label}: top level must be a mapping with a 'workflow' mapping"]
    wf = state["workflow"]
    schema = wf.get("schema_version")
    if type(schema) is not int or schema != 2:  # D11: the integer 2, never 2.0 / True / "2"
        errors.append(f"{label}: schema_version must be 2")
    if not isinstance(wf.get("work_package"), str) or not WP_ID.fullmatch(wf["work_package"]):
        errors.append(f"{label}: work_package must be a WP-ID token (WP-[A-Z0-9]{{1,8}})")
    status = wf.get("status")
    if not isinstance(status, str) or status not in transitions.STATUSES:
        errors.append(f"{label}: unknown status {status!r}")
        status = None  # shape errors are reported, never raised (totality)
    for key in ("next_owner", "next_action", "updated_by", "updated_reason"):
        if key in wf and wf[key] is not None and not isinstance(wf[key], str):
            errors.append(f"{label}: {key} must be a string or null")
    # Membership is tested only on strings (D13): an unhashable value is a shape error, not a raise.
    owner = wf.get("next_owner") if isinstance(wf.get("next_owner"), str) else None
    for key, valid in (
        ("requirements", is_requirement_id),
        ("open_findings", is_finding_id),
        ("provisionally_closed", is_finding_id),
    ):
        value = wf.get(key)
        if not isinstance(value, list):
            errors.append(f"{label}: {key} must be a list")
            continue
        for item in value:
            if not valid(item):
                errors.append(f"{label}: {key} element {item!r} is not a valid ID for {key}")
    if status in transitions.ACTIVE:
        if owner not in OWNERS:
            errors.append(f"{label}: active status {status} needs next_owner in {sorted(OWNERS)}")
        if not _nonblank(wf.get("next_action")):
            errors.append(f"{label}: active status {status} needs a next_action")
    if status == "BLOCKED_FOR_OWNER" and owner != "Owner":
        errors.append(f"{label}: BLOCKED_FOR_OWNER requires next_owner: Owner")
    if status == "WAITING_FOR_TRIGGER" and (
        not _nonblank(wf.get("deferred_trigger"))
        or wf.get("next_owner") is not None
        or wf.get("next_action") is not None
    ):
        errors.append(
            f"{label}: WAITING_FOR_TRIGGER needs a non-blank string deferred_trigger and null owner/action"
        )
    if status == "CONTRACT_CONVERGENCE":
        conv = wf.get("convergence")
        findings = conv.get("open_findings") if isinstance(conv, dict) else None
        if (
            not isinstance(conv, dict)
            or not _nonblank(conv.get("episode"))
            or not isinstance(findings, list)
            or not findings
            or not all(is_finding_id(f) for f in findings)
        ):
            errors.append(
                f"{label}: CONTRACT_CONVERGENCE needs convergence.episode (non-blank string) and a "
                "non-empty convergence.open_findings list of finding IDs"
            )
    if status == "CLOSED":
        if wf.get("open_findings"):
            errors.append(f"{label}: CLOSED with open findings")
        # WPP01-CR-002: closure must name the exact accepted pair; absent, empty, null or partial
        # candidate records fail closed (their main ancestry is then checked by check_state).
        candidate_record = wf.get("current_candidate")
        complete = isinstance(candidate_record, dict) and all(
            isinstance(candidate_record.get(side), dict)
            and isinstance(candidate_record[side].get("sha"), str)
            and SHA.fullmatch(candidate_record[side]["sha"])
            for side in ("code", "docs")
        )
        if not complete:
            errors.append(
                f"{label}: CLOSED requires the exact accepted pair: current_candidate.code and "
                ".docs must both be recorded with a 40-hex sha"
            )
        if wf.get("requirements") == []:
            review = wf.get("scoping_review")
            if (
                not isinstance(review, dict)
                or review.get("outcome") != "APPROVED"
                or not _nonblank(review.get("verdict"))
                or not _nonblank(review.get("source"))
            ):
                errors.append(
                    f"{label}: a scoping/process-only WP closes only with scoping_review "
                    "{outcome: APPROVED, verdict, source} recorded"
                )
    candidate = wf.get("current_candidate")
    if candidate is not None:
        if not isinstance(candidate, dict) or not set(candidate) <= {"code", "docs"}:
            errors.append(f"{label}: current_candidate must map only code/docs")
        else:
            for side, value in candidate.items():
                if value is None:
                    continue
                if not isinstance(value, dict):
                    errors.append(f"{label}: current_candidate.{side} must be a mapping or null")
                    continue
                if not isinstance(value.get("sha"), str) or not SHA.fullmatch(value["sha"]):
                    errors.append(f"{label}: current_candidate.{side}.sha must be 40 lowercase hex")
                if value.get("repo") != SIDE_REPOS[side]:
                    errors.append(
                        f"{label}: current_candidate.{side}.repo must be {SIDE_REPOS[side]!r} "
                        f"(sides are bound to their repositories), got {value.get('repo')!r}"
                    )
                ref = value.get("ref")
                if not plain_branch(ref):
                    errors.append(
                        f"{label}: current_candidate.{side}.ref must be a plain local branch name "
                        f"(not HEAD, refs/..., a SHA, range or option), got {ref!r}"
                    )
                elif status == "CLOSED" and ref != "main":
                    errors.append(f"{label}: CLOSED requires current_candidate.{side}.ref == 'main'")
    quarantine = wf.get("quarantine")
    if not isinstance(quarantine, dict) or not isinstance(
        quarantine.get("derived_from_quarantined_artifact"), bool
    ):
        errors.append(f"{label}: quarantine.derived_from_quarantined_artifact must be a boolean")
    elif quarantine["derived_from_quarantined_artifact"] and owner in AGENTS:
        errors.append(
            f"{label}: a quarantined candidate authorizes no agent action (next_owner must be Owner or null)"
        )
    if status in transitions.NON_ACTIONABLE and (
        wf.get("next_owner") is not None or wf.get("next_action") is not None
    ):
        errors.append(
            f"{label}: {status} authorizes no owner/action (next_owner and next_action must be null)"
        )
    bad = HISTORY_KEYS & set(wf)
    if bad:
        errors.append(f"{label}: history-shaped keys not allowed in current state: {sorted(bad)}")
    return errors


def _state_file(path: Path, docs: Path | None) -> tuple[Any, list[str]]:
    """Read, parse and validate one state file exactly once (D9); file-aware gate (D2, D15).

    Returns the validated object (or None) and the errors; callers use this object, never a reread.
    """
    label = path.name
    if docs is not None:
        state_dir = (docs / STATE_DIR).resolve()
        if path.resolve().parent != state_dir:
            return None, [f"{label}: {path} is not a state file inside {state_dir} (--docs containment, D15)"]
    kind = _kind(path)
    if kind != "file":
        return None, [f"{label}: {'missing' if kind == 'missing' else f'not a regular file ({kind})'}"]
    try:
        text = path.read_bytes().decode("utf-8")
    except (OSError, UnicodeDecodeError) as error:
        return None, [f"{label}: unreadable ({error})"]
    result = load_core(text)
    errors = [f"{label}: {e}" for e in result.errors]
    if not result.ok:
        return None, errors
    data = result.value
    errors.extend(validate_state(data, label))
    match = STATE_FILE.fullmatch(path.name)
    wf = data.get("workflow") if isinstance(data, dict) else None
    work_package = wf.get("work_package") if isinstance(wf, dict) else None
    if match is None:
        errors.append(f"{label}: a state file is named <WP-ID>.yaml (D1)")
    elif isinstance(work_package, str) and work_package != match.group("wp"):
        errors.append(
            f"{label}: work_package {work_package!r} does not equal the file stem {match.group('wp')!r} (D2)"
        )
    if len(text) > STATE_BUDGET:
        errors.append(f"{label}: exceeds the {STATE_BUDGET}-character lean budget")
    return data, errors


def validate_state_file(path: Path, docs: Path | None) -> list[str]:
    return _state_file(path, docs)[1]


def check_state(ctx: Context) -> list[str]:
    errors: list[str] = []
    members, inventory_errors = _state_working(ctx.docs)
    errors.extend(inventory_errors)
    if not members:
        return [*errors, f"{STATE_DIR}: no work-package state file"]
    side_paths = {"code": ctx.code, "docs": ctx.docs}
    overlays: dict[str, list[str]] = {}
    for name, path in members.items():
        data, file_errors = _state_file(path, ctx.docs)  # one load per file (D9)
        errors.extend(file_errors)
        wf = data.get("workflow") if isinstance(data, dict) else None
        if not isinstance(wf, dict):
            continue
        status = wf.get("status")
        candidate = wf.get("current_candidate")
        for side, cand in candidate.items() if isinstance(candidate, dict) else []:
            if side not in side_paths or not isinstance(cand, dict):
                continue
            sha, ref = cand.get("sha"), cand.get("ref")
            # The repository is fixed by the side, never chosen by the record (WPP01-CR-002); shape
            # errors were reported by validate_state, so never resolve a malformed side.
            if cand.get("repo") != SIDE_REPOS[side] or not isinstance(sha, str) or not SHA.fullmatch(sha):
                continue
            if not isinstance(ref, str) or not plain_branch(ref):
                continue
            repo = side_paths[side]
            if side not in overlays:
                overlays[side] = _graph_overlays(repo)
                errors.extend(overlays[side])
            if overlays[side]:
                continue
            tip, reason = _local_head(repo, ref)  # resolved once; this OID is used throughout (D8)
            if tip is None:
                errors.append(f"{name}: {side}.ref {ref!r} {reason} in {repo.name}")
                continue
            kind = _object_type(repo, sha)
            if kind != "commit":  # D6: the recorded OID itself is a commit, never a peeled tag
                errors.append(
                    f"{name}: {side} candidate {sha} does not exist in {repo.name}"
                    if kind is None
                    else f"{name}: {side} candidate {sha} is a {kind} object, not a commit"
                )
                continue
            if _git(repo, "merge-base", "--is-ancestor", sha, tip)[0] != 0:
                errors.append(f"{name}: {side} candidate {sha} is not reachable from {ref}")
            if status == "CLOSED":
                main, main_reason = _local_head(repo, "main")
                if main is None or _git(repo, "merge-base", "--is-ancestor", sha, main)[0] != 0:
                    errors.append(
                        f"{name}: CLOSED but {side} candidate {sha[:12]} is not accepted on main"
                        + (f" (main {main_reason})" if main is None else "")
                    )
            # An accepted (CLOSED) candidate is protected by the main-ancestry check above, and
            # post-acceptance record commits may follow it (coordination-state §2). Otherwise every
            # commit after the docs candidate must be state-only.
            if side == "docs" and status != "CLOSED":
                errors.extend(_state_only_chain(name, repo, sha, tip, ref))
        work_package = wf.get("work_package")
        if status == "CLOSED" and wf.get("requirements") and isinstance(work_package, str):
            registry = _load(ctx.docs / REGISTRY, [], REGISTRY)
            packages = registry.get("work_packages") if isinstance(registry, dict) else None
            entry = packages.get(work_package) if isinstance(packages, dict) else None
            xl = entry.get("cross_language") if isinstance(entry, dict) else None
            if not isinstance(xl, dict) or xl.get("status") != "CERTIFIED_CLOSED":
                errors.append(f"{name}: a product WP closes only when the registry says CERTIFIED_CLOSED")
    return errors


def _state_only_path(path: str) -> bool:
    """D10: the two state directories by prefix, the registry by exact path only."""
    return path.startswith(STATE_ONLY_DIRS) or path == REGISTRY


def _state_only_chain(label: str, repo: Path, sha: str, tip: str, ref: str) -> list[str]:
    """Every commit in `sha..tip` is a single-parent commit touching only state-only paths (D10).

    `tip` is the OID that `ref` resolved to once (D8). Checked per commit, not on the endpoint
    diff: a content change followed by its revert must not pass (coordination-state.md §2).
    """
    errors: list[str] = []
    status, listing = _git(repo, "rev-list", "--reverse", "--parents", f"{sha}..{tip}")
    if status != 0:
        return [f"{label}: cannot list commits {sha[:12]}..{ref}"]
    for line in listing.splitlines():
        commit, *parents = line.split()
        if len(parents) != 1:
            errors.append(
                f"{label}: commit {commit[:12]} after docs candidate {sha[:12]} on {ref} has "
                f"{len(parents)} parents (state-only descendants form a linear chain)"
            )
        status, changed = _git_paths(
            repo, "diff-tree", "-z", "--no-commit-id", "--name-only", "-r", "-m", commit
        )
        if status != 0:
            errors.append(f"{label}: cannot list paths changed by commit {commit[:12]}")
            continue
        extra = sorted({f for f in changed if not _state_only_path(f)})
        if extra:
            errors.append(
                f"{label}: commit {commit[:12]} after docs candidate {sha[:12]} on {ref} changes "
                f"non-state paths {extra} (state-only descendant rule)"
            )
    return errors


def check_findings(ctx: Context) -> list[str]:
    errors: list[str] = []
    findings = _finding_ids(ctx, errors)
    index = _index(ctx, [])
    spec_ids = {r.id for r in _spec(ctx).requirements}
    for fid, item in findings.items():
        if not FINDING_ID.match(fid):
            errors.append(f"{fid}: malformed finding id")
        if item.get("classification") not in CLASSIFICATIONS:
            errors.append(f"{fid}: classification {item.get('classification')!r} not in the taxonomy")
        if item.get("status") not in FINDING_STATUSES:
            errors.append(f"{fid}: status {item.get('status')!r} invalid")
        if not isinstance(item.get("owner_decision_required"), bool):
            errors.append(f"{fid}: owner_decision_required must be a boolean")
        condition = item.get("escalation_condition")
        if condition is not None and (not isinstance(condition, str) or not condition.strip()):
            errors.append(f"{fid}: escalation_condition must be a non-empty string when present")
        if item.get("classification") == "REQUIREMENT_UNCERTAIN" and not (
            item.get("owner_decision_required") is True or isinstance(condition, str)
        ):
            errors.append(
                f"{fid}: REQUIREMENT_UNCERTAIN needs owner_decision_required: true or an "
                "escalation_condition (finding-taxonomy §1.1)"
            )
        for key in ("title", "summary", "recommendation"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                errors.append(f"{fid}: {key} must be a non-empty string")
        for key in ("sources", "requirements", "blocking"):
            if not isinstance(item.get(key), list):
                errors.append(f"{fid}: {key} must be a list")
        for rid in item.get("requirements") or []:
            if rid not in spec_ids:
                errors.append(f"{fid}: requirement {rid} does not exist")
        for citation in item.get("sources") or []:
            match = CITATION.fullmatch(str(citation))
            if not match or match.group(2) not in index.get(match.group(1), set()):
                errors.append(f"{fid}: source {citation!r} does not resolve")
    return errors


def check_registry(ctx: Context) -> list[str]:
    errors: list[str] = []
    data = _load(ctx.docs / REGISTRY, errors, REGISTRY)
    if data is None:
        return errors
    wps = data.get("work_packages") if isinstance(data, dict) else None
    if not isinstance(wps, dict):
        return [*errors, f"{REGISTRY}: work_packages must be a mapping"]
    spec_ids = {r.id for r in _spec(ctx).requirements}
    for name, wp in wps.items():
        if not isinstance(wp, dict):
            errors.append(f"{REGISTRY}: {name} must be a mapping")
            continue
        for rid in wp.get("requirements") or []:
            if rid not in spec_ids:
                errors.append(f"{REGISTRY}: {name} requirement {rid} does not exist")
        checks = (
            ("contract", CONTRACT_STATUSES),
            ("python", LANG_STATUSES),
            ("rust", LANG_STATUSES),
            ("cross_language", XL_STATUSES),
        )
        for side, allowed in checks:
            status = (wp.get(side) or {}).get("status") if isinstance(wp.get(side), dict) else None
            if status not in allowed:
                errors.append(f"{REGISTRY}: {name}.{side}.status {status!r} invalid")
        lang = {wp.get(s, {}).get("status") for s in ("python", "rust") if isinstance(wp.get(s), dict)}
        if (wp.get("cross_language") or {}).get("status") == "CERTIFIED_CLOSED" and lang != {"CERTIFIED"}:
            errors.append(f"{REGISTRY}: {name} CERTIFIED_CLOSED requires both languages CERTIFIED")
        evidence = wp.get("evidence")
        if evidence and not (ctx.docs / str(evidence)).exists():
            errors.append(f"{REGISTRY}: {name} evidence {evidence} does not exist")
    return errors


CHECKS: dict[str, Callable[[Context], list[str]]] = {
    "repos": check_repos,
    "sources": check_sources,
    "spec": check_spec,
    "manifest": check_manifest,
    "conformance": check_conformance,
    "findings": check_findings,
    "registry": check_registry,
    "state": check_state,
}
CHECK_NAMES: list[str] = list(CHECKS)


def run_all(ctx: Context, only: list[str] | None = None) -> dict[str, list[str]]:
    report: dict[str, list[str]] = {}
    for name, check in CHECKS.items():
        if only and name not in only:
            continue
        try:
            report[name] = check(ctx)
        except Exception as error:
            report[name] = [f"internal error: {type(error).__name__}: {error}"]
    return report


def _working_root(docs: Path) -> str | None:
    """D15: the roundtrip target must be a non-bare working-tree repository root."""
    status, bare = _git(docs, "rev-parse", "--is-bare-repository")
    if status != 0 or bare != "false":
        return f"docs {docs} is not a non-bare git working-tree root"
    status, top = _git(docs, "rev-parse", "--show-toplevel")
    if status != 0 or Path(top).resolve() != docs.resolve():
        return f"docs {docs} is not a git working-tree root (toplevel {top!r})"
    return None


def _resolve_revision(docs: Path, revision: str) -> tuple[str | None, str | None]:
    """D8: exactly three spellings, each resolved once to a commit OID."""
    if not valid_revision(revision):
        return None, f"revision {revision!r} must be HEAD, a 40-hex commit OID or a plain local branch name"
    if revision == "HEAD":
        status, head = _git(docs, "rev-parse", "--verify", "--quiet", "--end-of-options", "HEAD^{commit}")
        if status == 0 and SHA.fullmatch(head):
            return head, None
        return None, "revision 'HEAD' does not name a commit"
    if SHA.fullmatch(revision):
        if _object_type(docs, revision) == "commit":
            return revision, None
        return None, f"revision {revision!r} does not name a commit object"
    branch, reason = _local_head(docs, revision)
    return (branch, None) if branch else (None, f"revision {revision!r} {reason}")


def state_roundtrip(docs: Path, revision: str = "HEAD") -> list[str]:
    """Commit rule step 4 (coordination-state §4): every working-tree state file must equal, byte for
    byte and semantically, the copy stored in `revision`.

    The revision is resolved once to a commit OID; the committed inventory and every blob read come
    from that one tree listing (D8). Both inventories obey the same domain (D1/D3). Blobs are read
    as raw bytes and decoded as UTF-8 explicitly — never via the platform code page. Content
    identity (stem == work_package) is not checked here: the roundtrip proves equality only (D2).
    """
    root_error = _working_root(docs)
    if root_error:
        return [root_error]
    overlays = _graph_overlays(docs)
    if overlays:
        return overlays
    oid, reason = _resolve_revision(docs, revision)
    if oid is None:
        return [reason or f"revision {revision!r} does not name a commit"]
    committed, errors = _state_committed(docs, oid)
    if committed is None:
        return errors
    working, working_errors = _state_working(docs)
    errors.extend(working_errors)
    # Inventory first (WPP01-CR-001): a committed state missing from the working tree, or a working
    # state absent from the commit, is a failed round trip — never silently skipped.
    for name in sorted(set(committed) - set(working)):
        errors.append(f"{STATE_DIR}/{name}: committed in {revision} but missing from the working tree")
    for name in sorted(set(working) - set(committed)):
        errors.append(f"{STATE_DIR}/{name}: present in the working tree but not committed in {revision}")
    if not committed and not working and not errors:
        return [f"{STATE_DIR}: no state files"]
    for name in sorted(set(committed) & set(working)):
        rel = f"{STATE_DIR}/{name}"
        done = _run_git(docs, "cat-file", "blob", committed[name])
        if done is None or done.returncode != 0:
            errors.append(f"{rel}: cannot read the committed blob in {revision}")
            continue
        try:
            working_bytes = working[name].read_bytes()
        except OSError as error:
            errors.append(f"{rel}: unreadable in the working tree ({error})")
            continue
        committed_bytes = done.stdout
        # Line endings alone are a checkout/transport artifact (hazard H2; .gitattributes eol=lf),
        # not a different state; any other byte difference is a failed state commit.
        crlf, lf = b"\r\n", b"\n"
        if committed_bytes.replace(crlf, lf) != working_bytes.replace(crlf, lf):
            errors.append(f"{rel}: committed bytes in {revision} differ from the working tree")
        try:
            committed_doc = load_core(committed_bytes.decode("utf-8"))
            working_doc = load_core(working_bytes.decode("utf-8"))
        except UnicodeDecodeError as error:
            errors.append(f"{rel}: not valid UTF-8 ({error})")
            continue
        if not committed_doc.ok or not working_doc.ok or committed_doc.value != working_doc.value:
            errors.append(f"{rel}: committed and working states are not semantically equal")
    return errors
