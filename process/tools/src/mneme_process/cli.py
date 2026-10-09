"""`mneme-process` command line.

    mneme-process sources build  --docs <docs-repo> [--workspace <root>]
    mneme-process check         --docs <docs-repo> --code <code-repo> [--workspace <root>]
                                 [--only NAME ...] [--deep-sources]
    mneme-process state validate <state.yaml> [--docs <docs-repo>]

Exit status: 0 when every selected check passes, 1 when any reports an error, 2 on usage error.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

from . import checks, sources, transitions
from .yamlcore import load_core


def _bundle(docs: Path) -> dict[str, object]:
    result = load_core((docs / checks.BUNDLE_MANIFEST).read_text(encoding="utf-8"))
    if not result.ok:
        raise SystemExit("source bundle manifest invalid: " + "; ".join(result.errors))
    assert isinstance(result.value, dict)
    return result.value


def _cmd_sources_build(args: argparse.Namespace) -> int:
    docs = Path(args.docs).resolve()
    bundle = _bundle(docs)
    workspace = Path(args.workspace or str(bundle["workspace_root"]))
    root = workspace / str(bundle["bundle_root"])
    out_dir = docs / checks.SOURCE_TEXT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    derived: dict[str, tuple[str, str]] = {}
    documents = bundle["documents"]
    assert isinstance(documents, list)
    for entry in documents:
        key, file = str(entry["key"]), str(entry["file"])
        if not file.endswith((".docx", ".md")):
            continue
        path = root / file
        digest = sources.sha256_file(path)
        if digest != entry["sha256"]:
            print(f"ERROR {key}: sha256 mismatch for {path}", file=sys.stderr)
            return 1
        text = sources.derive_text(path)
        header = (
            f"<!-- DERIVED, NON-AUTHORITATIVE reading aid. Source: {file} sha256:{digest}. "
            "Regenerate with `mneme-process sources build`; never edit by hand. -->\n\n"
        )
        (out_dir / f"{key}.md").write_text(header + text, encoding="utf-8", newline="\n")
        derived[key] = (digest, text)
    index = sources.build_index(derived)
    (docs / checks.SOURCE_INDEX).write_text(
        "# DERIVED, NON-AUTHORITATIVE section-anchor index. Regenerate with "
        "`mneme-process sources build`.\n"
        + yaml.safe_dump(index, sort_keys=False, allow_unicode=True, width=1000),
        encoding="utf-8",
        newline="\n",
    )
    print(f"wrote {len(derived)} derived texts and {checks.SOURCE_INDEX}")
    return 0


def _cmd_check(args: argparse.Namespace) -> int:
    ctx = checks.Context(
        docs=Path(args.docs).resolve(),
        code=Path(args.code).resolve(),
        workspace=Path(args.workspace).resolve() if args.workspace else None,
        deep_sources=args.deep_sources,
    )
    report = checks.run_all(ctx, only=args.only)
    for name, errors in report.items():
        status = "PASS" if not errors else f"FAIL ({len(errors)})"
        print(f"[{status}] {name}")
        for error in errors:
            print(f"    - {error}")
    failed = [name for name, errors in report.items() if errors]
    print(f"\n{len(report) - len(failed)}/{len(report)} checks passed")
    return 1 if failed else 0


def _cmd_state_validate(args: argparse.Namespace) -> int:
    docs = Path(args.docs).resolve() if args.docs else None
    errors = checks.validate_state_file(Path(args.path), docs)
    for error in errors:
        print(f"ERROR {error}")
    print("state VALID" if not errors else "state INVALID")
    return 1 if errors else 0


def _cmd_transition_check(args: argparse.Namespace) -> int:
    legal = transitions.is_legal(args.source, args.target)
    print(f"{args.source} -> {args.target}: {'LEGAL' if legal else 'ILLEGAL'}")
    return 0 if legal else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="mneme-process")
    sub = parser.add_subparsers(dest="command", required=True)

    src = sub.add_parser("sources").add_subparsers(dest="sources_command", required=True)
    build = src.add_parser("build")
    build.add_argument("--docs", required=True)
    build.add_argument("--workspace")
    build.set_defaults(func=_cmd_sources_build)

    check = sub.add_parser("check")
    check.add_argument("--docs", required=True)
    check.add_argument("--code", required=True)
    check.add_argument("--workspace")
    check.add_argument("--only", nargs="*", choices=checks.CHECK_NAMES)
    check.add_argument("--deep-sources", action="store_true")
    check.set_defaults(func=_cmd_check)

    state = sub.add_parser("state").add_subparsers(dest="state_command", required=True)
    validate = state.add_parser("validate")
    validate.add_argument("path")
    validate.add_argument("--docs")
    validate.set_defaults(func=_cmd_state_validate)

    transition = state.add_parser("transition-check")
    transition.add_argument("source")
    transition.add_argument("target")
    transition.set_defaults(func=_cmd_transition_check)

    args = parser.parse_args(argv)
    result: int = args.func(args)
    return result


if __name__ == "__main__":
    sys.exit(main())
