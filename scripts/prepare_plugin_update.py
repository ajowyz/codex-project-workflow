#!/usr/bin/env python3
"""Prepare a codex-project-workflow plugin source update.

The default mode is a dry run. Use --apply to copy the repository plugin source
package to the personal plugin source directory. This script never edits the
marketplace file or installed plugin cache.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


PLUGIN_NAME = "codex-project-workflow"
DEFAULT_SOURCE = Path("plugins") / PLUGIN_NAME
DEFAULT_TARGET = Path.home() / "plugins" / PLUGIN_NAME
REQUIRED_RELATIVE_PATHS = (
    Path(".codex-plugin") / "plugin.json",
    Path("skills") / PLUGIN_NAME / "SKILL.md",
    Path("skills") / PLUGIN_NAME / "scripts" / "read_reference.py",
    Path("skills") / PLUGIN_NAME / "references" / "governance.md",
    Path("skills") / PLUGIN_NAME / "references" / "research.md",
    Path("skills") / PLUGIN_NAME / "references" / "verification.md",
    Path("README.md"),
    Path("docs") / "USER_GUIDE.md",
)


def fail(reason: str, *next_steps: str) -> None:
    message = ["PLUGIN UPDATE PREP: FAIL", f"reason: {reason}"]
    if next_steps:
        message.append("next steps:")
        message.extend(f"- {step}" for step in next_steps)
    raise SystemExit("\n".join(message))


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate and optionally copy the plugin source package."
    )
    parser.add_argument(
        "--source",
        default=str(DEFAULT_SOURCE),
        help="Repository plugin source package directory.",
    )
    parser.add_argument(
        "--target",
        default=str(DEFAULT_TARGET),
        help="Personal plugin source directory to update.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Copy source files to target. Without this flag, print a dry-run plan.",
    )
    return parser.parse_args(argv)


def validate_source(source: Path) -> None:
    if not source.is_dir():
        fail(
            f"missing plugin source directory: {source}",
            "Run from the repository root or pass --source.",
        )

    missing = [relative for relative in REQUIRED_RELATIVE_PATHS if not (source / relative).is_file()]
    if missing:
        fail(
            f"plugin source is incomplete: {source}",
            "Missing required files:",
            *(str(path) for path in missing),
        )


def validate_target(source: Path, target: Path) -> None:
    source_resolved = source.resolve()
    target_resolved = target.resolve()
    if target_resolved == source_resolved:
        fail(
            "target must be different from source",
            "Pass --target with the personal plugin source directory.",
        )
    if source_resolved in target_resolved.parents:
        fail(
            "target cannot be inside the source package",
            "Choose a target outside the repository plugin source tree.",
        )


def copy_source(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target, dirs_exist_ok=True)


def print_report(source: Path, target: Path, apply: bool) -> None:
    mode = "apply" if apply else "dry-run"
    print("PLUGIN UPDATE PREP")
    print(f"mode: {mode}")
    print(f"source: {source}")
    print(f"target: {target}")
    print("required files:")
    for relative in REQUIRED_RELATIVE_PATHS:
        print(f"- ok {relative.as_posix()}")
    if apply:
        print("action: copied repository plugin source to personal plugin source")
    else:
        print("action: no files copied; rerun with --apply to copy source files")
    print("safety:")
    print("- marketplace file not modified")
    print("- installed plugin cache not modified")
    print("next steps:")
    print("- update the personal plugin cachebuster if the source changed")
    print("- re-enable or reinstall the plugin through Codex App or CLI")
    print("- open a fresh Codex thread and run install smoke")
    print("- run python scripts\\verify_plugin_install_smoke.py")
    print("PLUGIN UPDATE PREP: PASS")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    source = Path(args.source).expanduser().resolve()
    target = Path(args.target).expanduser().resolve()

    validate_source(source)
    validate_target(source, target)
    if args.apply:
        copy_source(source, target)
    print_report(source, target, args.apply)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
