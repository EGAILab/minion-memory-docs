"""WP-00 bootstrap validation checks across the docs and code repositories.

Each check returns a list of error strings; an empty list is PASS. Checks are total: malformed
input is reported, never raised. They validate mechanical well-formedness and traceability only.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import jsonschema

from . import sources, transitions
from .spec import CITATION, PROFILES, SOURCE_STATUSES, SpecParse, parse_spec
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
SHA = re.compile(r"^[0-9a-f]{40}$")
REQ_ID = re.compile(r"^[A-Z]{2,5}-\d{3}$")
FINDING_ID = re.compile(r"^[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3}$")
HISTORY_KEYS = frozenset({"reviews", "remediations", "review_history", "history_log"})
STATE_BUDGET = 8000


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


def _git(repo: Path, *args: str) -> tuple[int, str]:
    try:
        done = subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True,
            # Never the platform code page: git emits UTF-8 (paths, messages, file contents).
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return 1, str(error)
    return done.returncode, done.stdout.strip()


def _git_paths(repo: Path, *args: str) -> tuple[int, list[str]]:
    """Run a git command that lists paths, losslessly (WPP01-CR-001).

    Requests NUL-delimited output (`-z` must be among `args`) and decodes the raw path bytes as
    UTF-8, so `core.quotePath` display quoting (e.g. ``"WP-\\303\\234.yaml"``) never reaches a
    comparison. Undecodable bytes are reported as a failure, not guessed.
    """
    try:
        done = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, check=False, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return 1, []
    if done.returncode != 0:
        return done.returncode, []
    try:
        return 0, [part.decode("utf-8") for part in done.stdout.split(b"\0") if part]
    except UnicodeDecodeError:
        return 1, []


# Candidate sides are bound to their canonical repositories (WPP01-CR-002).
SIDE_REPOS: dict[str, str] = {"code": "minion-memory", "docs": "minion-memory-docs"}
# A candidate ref is a plain local branch name: no option-like or range syntax (WP-P01 sweep).
BRANCH = re.compile(r"^(?!-)(?!.*\.\.)(?!.*//)[A-Za-z0-9._/-]+(?<![./])$")


def valid_revision(text: str) -> bool:
    """A revision accepted from the CLI: HEAD, a full SHA, or a plain branch name."""
    return text == "HEAD" or bool(SHA.match(text)) or bool(BRANCH.match(text))


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
    for path in sorted(directory.glob("*.yaml")) if directory.is_dir() else []:
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
        for path in sorted(directory.rglob("*")):
            if not path.is_file() or path.name == "README.md":
                continue
            label = path.relative_to(ctx.code).as_posix()
            if path.suffix != ".yaml":
                errors.append(f"{label}: canonical scenarios must be .yaml")
                continue
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
        for nested in repo.rglob(".git"):
            if nested.parent != repo:
                errors.append(f"nested git repository inside {name} repo: {nested.parent}")
    if docs == code or docs in code.parents or code in docs.parents:
        errors.append("docs and code repositories must be disjoint siblings")
    parent = docs.parent
    status, top = _git(parent, "rev-parse", "--show-toplevel")
    if status == 0 and top:
        errors.append(f"workspace root {parent} is inside a git repository ({top})")
    for name, repo in (("docs", docs), ("code", code)):
        for forbidden in (".tmp", "review-worktrees"):
            if (repo / forbidden).exists():
                errors.append(
                    f"{name} repo contains {forbidden}/ (OWN-001: scratch lives in the project root)"
                )
    return errors


def check_sources(ctx: Context) -> list[str]:
    errors: list[str] = []
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
        key = str(entry["key"])
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
        if key not in expected:
            errors.append(f"{SOURCE_INDEX}: {key} not in the bundle manifest")
            continue
        if doc.get("source_sha256") != expected[key]:
            errors.append(f"{SOURCE_INDEX}: {key} indexes different source bytes than the manifest")
        text_path = ctx.docs / SOURCE_TEXT_DIR / f"{key}.md"
        if not text_path.is_file():
            errors.append(f"{SOURCE_TEXT_DIR}/{key}.md missing")
            continue
        body = text_path.read_text(encoding="utf-8").split("\n", 2)[2]
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
    directory = ctx.docs / SOURCE_TEXT_DIR
    for path in sorted(directory.glob("*.md")) if directory.is_dir() else []:
        parts = path.read_text(encoding="utf-8").split("\n", 2)
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


def validate_state(state: Any, label: str) -> list[str]:
    """Structural invariants of one state document (coordination-state.md §3)."""
    errors: list[str] = []
    if not isinstance(state, dict) or not isinstance(state.get("workflow"), dict):
        return [f"{label}: top level must be a mapping with a 'workflow' mapping"]
    wf = state["workflow"]
    if wf.get("schema_version") != 2:
        errors.append(f"{label}: schema_version must be 2")
    if not isinstance(wf.get("work_package"), str) or not wf["work_package"]:
        errors.append(f"{label}: work_package must be a non-empty string")
    status = wf.get("status")
    if not isinstance(status, str) or status not in transitions.STATUSES:
        errors.append(f"{label}: unknown status {status!r}")
        status = None  # shape errors are reported, never raised (totality)
    for key in ("next_owner", "next_action", "updated_by", "updated_reason"):
        if key in wf and wf[key] is not None and not isinstance(wf[key], str):
            errors.append(f"{label}: {key} must be a string or null")
    for key in ("requirements", "open_findings", "provisionally_closed"):
        value = wf.get(key)
        if not isinstance(value, list):
            errors.append(f"{label}: {key} must be a list")
            continue
        pattern = REQ_ID if key == "requirements" else FINDING_ID
        for item in value:
            if not isinstance(item, str) or not pattern.match(item):
                errors.append(f"{label}: {key} element {item!r} is not an ID")
    if status in transitions.ACTIVE:
        if wf.get("next_owner") not in OWNERS:
            errors.append(f"{label}: active status {status} needs next_owner in {sorted(OWNERS)}")
        if not isinstance(wf.get("next_action"), str) or not wf["next_action"].strip():
            errors.append(f"{label}: active status {status} needs a next_action")
    if status == "BLOCKED_FOR_OWNER" and wf.get("next_owner") != "Owner":
        errors.append(f"{label}: BLOCKED_FOR_OWNER requires next_owner: Owner")
    if status == "WAITING_FOR_TRIGGER" and (
        not wf.get("deferred_trigger")
        or wf.get("next_owner") is not None
        or wf.get("next_action") is not None
    ):
        errors.append(f"{label}: WAITING_FOR_TRIGGER needs deferred_trigger and null owner/action")
    if status == "CONTRACT_CONVERGENCE":
        conv = wf.get("convergence")
        if not isinstance(conv, dict) or not conv.get("episode") or not conv.get("open_findings"):
            errors.append(f"{label}: CONTRACT_CONVERGENCE needs convergence.episode and open_findings")
    if status == "CLOSED":
        if wf.get("open_findings"):
            errors.append(f"{label}: CLOSED with open findings")
        # WPP01-CR-002: closure must name the exact accepted pair; absent, empty, null or partial
        # candidate records fail closed (their main ancestry is then checked by check_state).
        candidate_record = wf.get("current_candidate")
        complete = isinstance(candidate_record, dict) and all(
            isinstance(candidate_record.get(side), dict)
            and isinstance(candidate_record[side].get("sha"), str)
            and SHA.match(candidate_record[side]["sha"])
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
                or not isinstance(review.get("verdict"), str)
                or not review["verdict"].strip()
                or not isinstance(review.get("source"), str)
                or not review["source"].strip()
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
                if not isinstance(value.get("sha"), str) or not SHA.match(value["sha"]):
                    errors.append(f"{label}: current_candidate.{side}.sha must be 40 lowercase hex")
                if value.get("repo") != SIDE_REPOS[side]:
                    errors.append(
                        f"{label}: current_candidate.{side}.repo must be {SIDE_REPOS[side]!r} "
                        f"(sides are bound to their repositories), got {value.get('repo')!r}"
                    )
                ref = value.get("ref")
                if not isinstance(ref, str) or not BRANCH.match(ref) or SHA.match(ref):
                    errors.append(
                        f"{label}: current_candidate.{side}.ref must be a plain local branch name "
                        f"(not a SHA, range or option), got {ref!r}"
                    )
                elif status == "CLOSED" and ref != "main":
                    errors.append(f"{label}: CLOSED requires current_candidate.{side}.ref == 'main'")
    quarantine = wf.get("quarantine")
    if not isinstance(quarantine, dict) or not isinstance(
        quarantine.get("derived_from_quarantined_artifact"), bool
    ):
        errors.append(f"{label}: quarantine.derived_from_quarantined_artifact must be a boolean")
    elif quarantine["derived_from_quarantined_artifact"] and wf.get("next_owner") in AGENTS:
        errors.append(
            f"{label}: a quarantined candidate authorizes no agent action (next_owner must be Owner or null)"
        )
    if status in transitions.NON_ACTIONABLE and wf.get("next_owner") is not None:
        errors.append(f"{label}: {status} authorizes no owner/action")
    bad = HISTORY_KEYS & set(wf)
    if bad:
        errors.append(f"{label}: history-shaped keys not allowed in current state: {sorted(bad)}")
    return errors


def validate_state_file(path: Path, docs: Path | None) -> list[str]:
    errors: list[str] = []
    data = _load(path, errors, path.name)
    if data is None:
        return errors
    errors.extend(validate_state(data, path.name))
    if len(path.read_text(encoding="utf-8")) > STATE_BUDGET:
        errors.append(f"{path.name}: exceeds the {STATE_BUDGET}-character lean budget")
    return errors


def check_state(ctx: Context) -> list[str]:
    errors: list[str] = []
    directory = ctx.docs / STATE_DIR
    files = sorted(directory.glob("*.yaml")) if directory.is_dir() else []
    if not files:
        return [f"{STATE_DIR}: no work-package state file"]
    side_paths = {"code": ctx.code, "docs": ctx.docs}
    for path in files:
        errors.extend(validate_state_file(path, ctx.docs))
        data = _load(path, [], path.name)
        wf = data.get("workflow") if isinstance(data, dict) else None
        if not isinstance(wf, dict) or not isinstance(wf.get("current_candidate"), dict):
            continue
        for side, cand in wf["current_candidate"].items():
            if side not in side_paths or not isinstance(cand, dict) or not isinstance(cand.get("sha"), str):
                continue
            # The repository is fixed by the side, never chosen by the record (WPP01-CR-002).
            if cand.get("repo") != SIDE_REPOS[side]:
                continue  # reported by validate_state; never resolve a mis-bound side
            repo = side_paths[side]
            sha, ref = cand["sha"], str(cand.get("ref"))
            if not BRANCH.match(ref) or SHA.match(ref):
                continue  # reported by validate_state
            if _git(repo, "show-ref", "--verify", "--quiet", f"refs/heads/{ref}")[0] != 0:
                errors.append(f"{path.name}: {side}.ref {ref!r} is not a local branch in {repo.name}")
                continue
            if _git(repo, "cat-file", "-e", f"{sha}^{{commit}}")[0] != 0:
                errors.append(f"{path.name}: {side} candidate {sha} does not exist in {repo.name}")
                continue
            if _git(repo, "merge-base", "--is-ancestor", sha, ref)[0] != 0:
                errors.append(f"{path.name}: {side} candidate {sha} is not reachable from {ref}")
            if (
                wf.get("status") == "CLOSED"
                and _git(repo, "merge-base", "--is-ancestor", sha, "main")[0] != 0
            ):
                errors.append(f"{path.name}: CLOSED but {side} candidate {sha[:12]} is not accepted on main")
            # An accepted (CLOSED) candidate is protected by the main-ancestry check above, and
            # post-acceptance record commits may follow it (coordination-state §2). Otherwise every
            # commit after the docs candidate must be state-only.
            if side == "docs" and wf.get("status") != "CLOSED":
                errors.extend(_state_only_chain(path.name, repo, sha, ref))
        if wf.get("status") == "CLOSED" and wf.get("requirements"):
            registry = _load(ctx.docs / REGISTRY, [], REGISTRY)
            entry = (registry or {}).get("work_packages", {}).get(wf.get("work_package"))
            xl = entry.get("cross_language") if isinstance(entry, dict) else None
            if not isinstance(xl, dict) or xl.get("status") != "CERTIFIED_CLOSED":
                errors.append(
                    f"{path.name}: a product WP closes only when the registry says CERTIFIED_CLOSED"
                )
    return errors


def _state_only_chain(label: str, repo: Path, sha: str, ref: str) -> list[str]:
    """Every commit after the docs candidate on `ref` touches only state-only paths.

    Checked per commit, not on the endpoint diff: a content change followed by its revert must not
    pass (coordination-state.md §2).
    """
    errors: list[str] = []
    status, commits = _git(repo, "rev-list", "--reverse", f"{sha}..{ref}")
    if status != 0:
        return [f"{label}: cannot list commits {sha[:12]}..{ref}"]
    for commit in commits.split():
        status, changed = _git_paths(
            repo, "diff-tree", "-z", "--no-commit-id", "--name-only", "-r", "-m", commit
        )
        if status != 0:
            errors.append(f"{label}: cannot list paths changed by commit {commit[:12]}")
            continue
        extra = sorted({f for f in changed if not f.startswith(STATE_ONLY_PATHS)})
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


def state_roundtrip(docs: Path, revision: str = "HEAD") -> list[str]:
    """Commit rule step 4 (coordination-state §4): every working-tree state file must equal, byte for
    byte and semantically, the copy stored in `revision`. Reads git blobs as raw bytes and decodes
    UTF-8 explicitly — never via the platform code page."""
    errors: list[str] = []
    directory = docs / STATE_DIR
    files = sorted(directory.glob("*.yaml")) if directory.is_dir() else []
    # Inventory first (WPP01-CR-001): a committed state missing from the working tree, or a working
    # state absent from the commit, is a failed round trip — never silently skipped.
    if not valid_revision(revision):
        return [f"revision {revision!r} must be HEAD, a 40-hex SHA or a plain branch name"]
    if _git(docs, "rev-parse", "--verify", "--quiet", f"{revision}^{{commit}}")[0] != 0:
        return [f"revision {revision!r} does not name a commit"]
    status, listing = _git_paths(docs, "ls-tree", "-z", "--name-only", f"{revision}:{STATE_DIR}")
    if status != 0:
        return [f"{STATE_DIR}: cannot list committed state files in {revision}"]
    committed_names = {name for name in listing if name.endswith(".yaml")}
    working_names = {path.name for path in files}
    for name in sorted(committed_names - working_names):
        errors.append(f"{STATE_DIR}/{name}: committed in {revision} but missing from the working tree")
    for name in sorted(working_names - committed_names):
        errors.append(f"{STATE_DIR}/{name}: present in the working tree but not committed in {revision}")
    if not committed_names and not working_names:
        return [*errors, f"{STATE_DIR}: no state files"]
    for path in files:
        if path.name not in committed_names:
            continue
        rel = path.relative_to(docs).as_posix()
        try:
            done = subprocess.run(
                ["git", "-C", str(docs), "show", f"{revision}:{rel}"],
                capture_output=True,
                check=False,
                timeout=60,
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            errors.append(f"{rel}: git show failed ({error})")
            continue
        if done.returncode != 0:
            errors.append(f"{rel}: not present in {revision}")
            continue
        committed_bytes, working_bytes = done.stdout, path.read_bytes()
        # Line endings alone are a checkout/transport artifact (hazard H2; .gitattributes eol=lf),
        # not a different state; any other byte difference is a failed state commit.
        crlf, lf = b"\r\n", b"\n"
        if committed_bytes.replace(crlf, lf) != working_bytes.replace(crlf, lf):
            errors.append(f"{rel}: committed bytes in {revision} differ from the working tree")
        try:
            committed = load_core(committed_bytes.decode("utf-8"))
            working = load_core(working_bytes.decode("utf-8"))
        except UnicodeDecodeError as error:
            errors.append(f"{rel}: not valid UTF-8 ({error})")
            continue
        if not committed.ok or not working.ok or committed.value != working.value:
            errors.append(f"{rel}: committed and working states are not semantically equal")
    return errors
