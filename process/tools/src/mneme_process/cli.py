"""`mneme-process` command line.

    mneme-process sources build  --docs <docs-repo> [--workspace <root>]
    mneme-process check         --docs <docs-repo> --code <code-repo> [--workspace <root>]
                                 [--only NAME ...] [--deep-sources]
    mneme-process state validate <state.yaml> [--docs <docs-repo>]
    mneme-process state roundtrip --docs <docs-repo> [--revision HEAD]
    mneme-process state transition-check FROM TO

Exit status: 0 when every selected check passes, 1 when any reports an error, 2 on usage error.
"""

from __future__ import annotations

import argparse
import os
import stat
import sys
from pathlib import Path

import yaml

from . import checks, sources, transitions
from .yamlcore import load_core


def _fail(errors: list[str]) -> int:
    for error in errors:
        print(f"ERROR {error}", file=sys.stderr)
    return 1


def _sources_plan(args: argparse.Namespace) -> tuple[dict[Path, str], int, list[str]]:
    """Preflight (CE-P01-01 D14): validate every entry, hash and output path before any write.

    Returns the complete set of outputs (path -> text), the derived-text count and the errors.
    """
    docs = Path(args.docs).resolve()
    manifest = docs / checks.BUNDLE_MANIFEST
    try:
        result = load_core(manifest.read_bytes().decode("utf-8"))
    except (OSError, UnicodeDecodeError) as error:
        return {}, 0, [f"{checks.BUNDLE_MANIFEST}: unreadable ({error})"]
    if not result.ok:
        return {}, 0, [f"{checks.BUNDLE_MANIFEST}: {e}" for e in result.errors]
    bundle = result.value
    documents = bundle.get("documents") if isinstance(bundle, dict) else None
    if not isinstance(documents, list):
        return {}, 0, [f"{checks.BUNDLE_MANIFEST}: documents must be a list"]
    workspace_root = args.workspace or bundle.get("workspace_root")
    bundle_root = bundle.get("bundle_root")
    if not isinstance(workspace_root, str) or not checks.safe_relative_file(bundle_root):
        return {}, 0, [f"{checks.BUNDLE_MANIFEST}: workspace_root and a relative bundle_root are required"]
    root = Path(workspace_root) / bundle_root
    # The producer boundary is the real directory chain under docs: a symlinked (or non-directory)
    # `reference` / `reference/source-text` would redirect every write (CL-004).
    errors: list[str] = []
    current = docs
    for part in Path(checks.SOURCE_TEXT_DIR).parts:
        current = current / part
        try:
            mode = os.lstat(current).st_mode
        except FileNotFoundError:
            continue  # created as a real directory in the write phase
        except OSError as error:
            return {}, 0, [f"{current}: unreadable ({error})"]
        if not stat.S_ISDIR(mode):
            return (
                {},
                0,
                [f"{current}: the derived-output directory must be a real directory, not a symlink or file"],
            )
    out_dir = (docs / checks.SOURCE_TEXT_DIR).resolve()
    outputs: dict[Path, str] = {}
    derived: dict[str, tuple[str, str]] = {}
    for entry in documents:
        entry_errors = checks.source_entry_errors(entry)
        if entry_errors:
            errors.extend(entry_errors)
            continue
        key, file = entry["key"], entry["file"]
        if not file.endswith((".docx", ".md")):
            continue
        if key in derived:
            errors.append(f"{key}: duplicate document key")
            continue
        target = (out_dir / f"{key}.md").resolve()
        if target.parent != out_dir:
            errors.append(f"{key}: derived output {target} escapes {out_dir}")
            continue
        path = root / file
        try:
            digest = sources.sha256_file(path)
        except OSError as error:
            errors.append(f"{key}: source unreadable: {path} ({error})")
            continue
        if digest != entry["sha256"]:
            errors.append(f"{key}: sha256 mismatch for {path}")
            continue
        try:
            text = sources.derive_text(path)
        except Exception as error:  # a failed derivation is a reported error, never a partial build
            errors.append(f"{key}: derivation failed ({type(error).__name__}: {error})")
            continue
        header = (
            f"<!-- DERIVED, NON-AUTHORITATIVE reading aid. Source: {file} sha256:{digest}. "
            "Regenerate with `mneme-process sources build`; never edit by hand. -->\n\n"
        )
        outputs[target] = header + text
        derived[key] = (digest, text)
    outputs[(docs / checks.SOURCE_INDEX).resolve()] = (
        "# DERIVED, NON-AUTHORITATIVE section-anchor index. Regenerate with "
        "`mneme-process sources build`.\n"
        + yaml.safe_dump(sources.build_index(derived), sort_keys=False, allow_unicode=True, width=1000)
    )
    return outputs, len(derived), errors


def _replace(temporary: Path, target: Path) -> None:
    os.replace(temporary, target)


def _stage(temporary: Path, text: str) -> None:
    """Write a staging file without ever following a link (CL-004).

    A stale staging entry (regular file or symlink) is removed itself — never its target — and the
    new file is created exclusively, so a link planted between the two steps makes creation fail.
    """
    try:
        mode = os.lstat(temporary).st_mode
    except FileNotFoundError:
        pass
    else:
        if stat.S_ISDIR(mode):
            raise OSError(f"staging path {temporary} is a directory")
        os.unlink(temporary)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(temporary, flags, 0o644)
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(text.encode("utf-8"))


def _discard(paths: list[Path]) -> list[str]:
    """Remove staging files; a cleanup failure is reported, never raised (CL-003)."""
    failures: list[str] = []
    for path in paths:
        try:
            path.unlink(missing_ok=True)
        except OSError as error:
            failures.append(f"could not remove staging file {path} ({error})")
    return failures


def _cmd_sources_build(args: argparse.Namespace) -> int:
    outputs, count, errors = _sources_plan(args)
    if errors:  # validation failure: nothing has been written (D14)
        return _fail(errors)
    # Write phase: stage every output beside its target, then replace in turn. An OS failure while
    # replacing can leave a mix of old and new files: the build then exits 1 naming every file
    # already replaced (a stated limit, not a transactional claim).
    staged: list[tuple[Path, Path]] = []
    try:
        for target, text in outputs.items():
            target.parent.mkdir(parents=True, exist_ok=True)
            temporary = target.with_name(f".{target.name}.mneme-tmp")
            _stage(temporary, text)
            staged.append((temporary, target))
    except OSError as error:
        cleanup = _discard([temporary for temporary, _ in staged])
        return _fail([f"staging derived outputs failed before any replacement ({error})", *cleanup])
    replaced: list[str] = []
    for index, (temporary, target) in enumerate(staged):
        try:
            _replace(temporary, target)
        except OSError as error:
            cleanup = _discard([leftover for leftover, _ in staged[index:]])
            done = ", ".join(replaced) or "none"
            return _fail(
                [f"replacing {target} failed ({error}); already replaced: {done}; rerun the build", *cleanup]
            )
        replaced.append(str(target))
    print(f"wrote {count} derived texts and {checks.SOURCE_INDEX}")
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


def _cmd_state_roundtrip(args: argparse.Namespace) -> int:
    errors = checks.state_roundtrip(Path(args.docs).resolve(), args.revision)
    for error in errors:
        print(f"ERROR {error}")
    print("state ROUNDTRIP OK" if not errors else "state ROUNDTRIP FAILED (failed state commit)")
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
    # D15: `--only` names at least one check; a bare `--only` is a usage error, never "all checks".
    check.add_argument("--only", nargs="+", choices=checks.CHECK_NAMES)
    check.add_argument("--deep-sources", action="store_true")
    check.set_defaults(func=_cmd_check)

    state = sub.add_parser("state").add_subparsers(dest="state_command", required=True)
    validate = state.add_parser("validate")
    validate.add_argument("path")
    validate.add_argument("--docs")
    validate.set_defaults(func=_cmd_state_validate)

    roundtrip = state.add_parser("roundtrip")
    roundtrip.add_argument("--docs", required=True)
    roundtrip.add_argument("--revision", default="HEAD")
    roundtrip.set_defaults(func=_cmd_state_roundtrip)

    transition = state.add_parser("transition-check")
    transition.add_argument("source")
    transition.add_argument("target")
    transition.set_defaults(func=_cmd_transition_check)

    args = parser.parse_args(argv)
    result: int = args.func(args)
    return result


if __name__ == "__main__":
    sys.exit(main())
