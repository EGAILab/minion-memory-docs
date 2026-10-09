"""Source-bundle provenance: hashes, derived plain text and the section-anchor index.

The DOCX/MD files in the upstream bundle are the authority. Everything this module writes
(`reference/source-text/*.md`, `reference/source-index.yaml`) is a *derived, non-authoritative*
reading aid whose only job is to make `[KEY §anchor]` citations in `spec/**` mechanically
resolvable. Derivation is deterministic: the same DOCX bytes always yield the same text and index.

Anchor rule (normative for citations, `spec/README.md` §3):
  heading text "4.1 KnowledgeUnit"            -> "4.1"
  heading text "G.3 MemoryScope"              -> "G.3"
  heading text "A26 — Dual-profile core"      -> "A26"
  heading text "Appendix G - Dual-Profile..." -> "App-G"
  any other heading                           -> slug of the heading text
  a repeated anchor within one document       -> "<anchor>~2", "<anchor>~3", ...
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_NUMBERED = re.compile(r"^(\d+(?:\.\d+)*)\.?(?:\s|$)")
_LETTERED = re.compile(r"^([A-Z]\.\d+)(?:\s|$)")
_AMENDMENT = re.compile(r"^([AM]\d+)\s+[—-]")
_APPENDIX = re.compile(r"^Appendix ([A-Z])\b")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def slug(text: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", text.lower())).strip("-")


def anchor_for(heading: str) -> str:
    for pattern, render in (
        (_NUMBERED, lambda m: m.group(1)),
        (_LETTERED, lambda m: m.group(1)),
        (_AMENDMENT, lambda m: m.group(1)),
        (_APPENDIX, lambda m: f"App-{m.group(1)}"),
    ):
        match = pattern.match(heading)
        if match:
            return str(render(match))
    return slug(heading)


@dataclass(frozen=True)
class Anchor:
    anchor: str
    heading: str
    level: int
    line: int


def index_text(text: str) -> list[Anchor]:
    """Anchors for every Markdown heading in derived text, in document order."""
    anchors: list[Anchor] = []
    counts: dict[str, int] = {}
    for number, line in enumerate(text.splitlines(), start=1):
        match = re.match(r"^(#{1,6})\s+(.*\S)\s*$", line)
        if not match:
            continue
        heading = match.group(2)
        base = anchor_for(heading)
        counts[base] = counts.get(base, 0) + 1
        anchor = base if counts[base] == 1 else f"{base}~{counts[base]}"
        anchors.append(Anchor(anchor, heading, len(match.group(1)), number))
    return anchors


def extract_docx(path: Path) -> str:
    """Headings, paragraphs and tables in body order. Requires python-docx (extra `sources`)."""
    from docx import Document
    from docx.table import Table
    from docx.text.paragraph import Paragraph

    document = Document(str(path))
    lines: list[str] = []
    for child in document.element.body.iterchildren():
        tag = child.tag.rsplit("}", 1)[-1]
        if tag == "p":
            paragraph = Paragraph(child, document)
            text = paragraph.text.strip()
            if not text:
                continue
            style = paragraph.style.name if paragraph.style is not None else ""
            if style.startswith("Heading"):
                try:
                    level = int(style.split()[-1])
                except ValueError:
                    level = 1
                lines.append("")
                lines.append("#" * min(level + 1, 6) + " " + text)
            elif style == "Title":
                lines.append("# " + text)
            elif "List" in style:
                lines.append("- " + text)
            else:
                lines.append(text)
        elif tag == "tbl":
            table = Table(child, document)
            rows = []
            for row in table.rows:
                cells = [cell.text.strip().replace("\n", " <br> ").replace("|", "\\|") for cell in row.cells]
                rows.append("| " + " | ".join(cells) + " |")
            if rows:
                columns = rows[0].count(" | ") + 1
                rows.insert(1, "|" + "---|" * columns)
                lines.append("")
                lines.extend(rows)
                lines.append("")
    return "\n".join(lines).strip() + "\n"


def derive_text(path: Path) -> str:
    if path.suffix.lower() == ".docx":
        return extract_docx(path)
    return path.read_text(encoding="utf-8")


def build_index(documents: dict[str, tuple[str, str]]) -> dict[str, Any]:
    """`documents`: key -> (sha256 of the authoritative file, derived text)."""
    out: dict[str, Any] = {"index_version": 1, "documents": {}}
    for key in sorted(documents):
        digest, text = documents[key]
        out["documents"][key] = {
            "source_sha256": digest,
            "derived_text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "anchors": [
                {"anchor": a.anchor, "heading": a.heading, "level": a.level, "line": a.line}
                for a in index_text(text)
            ],
        }
    return out
