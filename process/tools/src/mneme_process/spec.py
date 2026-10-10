"""Parse requirement blocks and citations out of `spec/**/*.md` (spec/README.md §3)."""

from __future__ import annotations

import os
import re
import stat
from dataclasses import dataclass, field
from pathlib import Path

HEADING = re.compile(r"^(#{2,4}) ([A-Z]{2,5}-\d{3}) — (\S.*)$")
ANCHOR = re.compile(r'^<a id="([a-z]+-\d{3})"></a>$')
METADATA = re.compile(
    r"^- \*\*Profile:\*\* (?P<profile>\S+) · \*\*Source status:\*\* (?P<status>\S+) · "
    r"\*\*Sources:\*\* (?P<sources>.+)$"
)
CITATION = re.compile(r"\[([A-Z][A-Z0-9]*) §([^\]\s][^\]]*)\]")
FINDING_REF = re.compile(r"\bNF-\d{3}\b")

PROFILES = frozenset({"core", "learning", "agent"})
SOURCE_STATUSES = frozenset(
    {
        "FROZEN",
        "PROVISIONAL",
        "RESEARCH_CANDIDATE",
        "MVP_ONLY",
        "SCHEMA_RESERVATION",
        "NOT_IN_MVP",
        "NORMATIVE",
        "GUARDRAIL",
    }
)


@dataclass
class Requirement:
    id: str
    title: str
    file: str
    line: int
    anchor: str | None = None
    profile: str | None = None
    source_status: str | None = None
    sources: list[str] = field(default_factory=list)


@dataclass
class SpecParse:
    requirements: list[Requirement]
    citations: list[tuple[str, int, str, str]]  # file, line, key, anchor
    finding_refs: list[tuple[str, int, str]]
    errors: list[str]


def inventory(
    directory: Path,
    suffix: str,
    repo_root: Path,
    *,
    recursive: bool,
    other_files: str = "error",
    skip_names: frozenset[str] = frozenset(),
) -> tuple[list[Path], list[str]]:
    """One validator inventory (CE-P01-01 D16), identical on every host.

    Members are regular files whose name ends with `suffix`, compared case-sensitively and
    byte-exactly. Kinds come from `lstat` (symlinks are never followed and are errors). A directory
    is traversed only when `recursive`; a directory named like a member, a nested directory in a flat
    inventory, a case-variant suffix and any special file are named errors, never silent skips.
    `other_files` is "error" (every other file is an error) or "ignore" (only case variants are).
    """
    members: list[Path] = []
    errors: list[str] = []

    def label(path: Path) -> str:
        return path.relative_to(repo_root).as_posix()

    def walk(current: Path) -> None:
        try:
            names = sorted(os.listdir(current))
        except OSError as error:
            errors.append(f"{label(current)}: cannot list ({error})")
            return
        for name in names:
            path = current / name
            try:
                mode = os.lstat(path).st_mode
            except OSError as error:
                errors.append(f"{label(path)}: unreadable entry ({error})")
                continue
            if name in skip_names and stat.S_ISREG(mode):
                continue
            if stat.S_ISLNK(mode):
                errors.append(f"{label(path)}: symlinks are not allowed in this inventory (D16)")
            elif stat.S_ISDIR(mode):
                if name.endswith(suffix) or not recursive:
                    errors.append(f"{label(path)}: unsupported directory in this inventory (D16)")
                else:
                    walk(path)
            elif not stat.S_ISREG(mode):
                errors.append(f"{label(path)}: unsupported special file (D16)")
            elif name.endswith(suffix):
                members.append(path)
            elif other_files == "error" or name.lower().endswith(suffix.lower()):
                errors.append(
                    f"{label(path)}: members of this inventory must be regular *{suffix} files (D16)"
                )

    walk(directory)
    return members, errors


def parse_spec(spec_root: Path, repo_root: Path) -> SpecParse:
    requirements: list[Requirement] = []
    citations: list[tuple[str, int, str, str]] = []
    finding_refs: list[tuple[str, int, str]] = []
    errors: list[str] = []
    paths, inventory_errors = (
        inventory(spec_root, ".md", repo_root, recursive=True, other_files="ignore")
        if spec_root.is_dir()
        else ([], [])
    )
    errors.extend(inventory_errors)
    for path in paths:
        rel = path.relative_to(repo_root).as_posix()
        try:
            lines = path.read_bytes().decode("utf-8").splitlines()
        except (OSError, UnicodeDecodeError) as error:
            errors.append(f"{rel}: unreadable ({error})")
            continue
        current: Requirement | None = None
        expect = ""  # "anchor" then "metadata"
        in_code = False
        for number, line in enumerate(lines, start=1):
            if line.startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            prose = re.sub(r"`[^`]*`", "", line)  # citations inside inline code are examples
            for match in CITATION.finditer(prose):
                citations.append((rel, number, match.group(1), match.group(2)))
            for match in FINDING_REF.finditer(line):
                finding_refs.append((rel, number, match.group(0)))
            heading = HEADING.match(line)
            if heading:
                current = Requirement(heading.group(2), heading.group(3), rel, number)
                requirements.append(current)
                expect = "anchor"
                continue
            if current is None or not expect or not line.strip():
                continue
            if expect == "anchor":
                anchor = ANCHOR.match(line)
                if anchor:
                    current.anchor = anchor.group(1)
                else:
                    errors.append(f"{rel}:{number}: {current.id} heading not followed by its anchor")
                expect = "metadata"
                continue
            if expect == "metadata":
                meta = METADATA.match(line)
                if meta:
                    current.profile = meta.group("profile")
                    current.source_status = meta.group("status")
                    current.sources = [
                        f"[{m.group(1)} §{m.group(2)}]" for m in CITATION.finditer(meta.group("sources"))
                    ]
                else:
                    errors.append(f"{rel}:{number}: {current.id} has no metadata line")
                expect = ""
    return SpecParse(requirements, citations, finding_refs, errors)
