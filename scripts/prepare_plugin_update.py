#!/usr/bin/env python3
"""Prepare a codex-project-workflow plugin source update.

The default mode is a dry run. Use --apply to copy the repository plugin source
package to the personal plugin source directory. Use --apply-cachebuster with
--apply to update the copied manifest version for a real reinstall cycle.

This script never edits the marketplace file or installed plugin cache.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path


PLUGIN_NAME = "codex-project-workflow"
DEFAULT_SOURCE = Path("plugins") / PLUGIN_NAME
DEFAULT_TARGET = Path.home() / "plugins" / PLUGIN_NAME
DEFAULT_MARKETPLACE = Path.home() / ".agents" / "plugins" / "marketplace.json"
EXPECTED_MARKETPLACE_PATH = f"./plugins/{PLUGIN_NAME}"
CACHEBUSTER_PREFIX = "codex"
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
    parser.add_argument(
        "--apply-cachebuster",
        action="store_true",
        help=(
            "After --apply, rewrite the target manifest version with a +codex "
            "cachebuster suffix. This modifies only the personal plugin source."
        ),
    )
    parser.add_argument(
        "--cachebuster",
        help="Optional cachebuster token. Defaults to a UTC timestamp when applying.",
    )
    parser.add_argument(
        "--marketplace",
        default=str(DEFAULT_MARKETPLACE),
        help="Personal marketplace file to validate when using the default target.",
    )
    parser.add_argument(
        "--skip-marketplace-check",
        action="store_true",
        help="Skip personal marketplace validation.",
    )
    return parser.parse_args(argv)


def manifest_path(plugin_root: Path) -> Path:
    return plugin_root / ".codex-plugin" / "plugin.json"


def load_manifest(plugin_root: Path) -> dict[str, object]:
    path = manifest_path(plugin_root)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid plugin manifest JSON: {path}", str(exc))
    if not isinstance(payload, dict):
        fail(f"plugin manifest must contain a JSON object: {path}")
    return payload


def plugin_version(plugin_root: Path) -> str:
    version = load_manifest(plugin_root).get("version")
    if not isinstance(version, str) or not version.strip():
        fail(
            f"plugin manifest has no non-empty string version: {manifest_path(plugin_root)}",
            "Fix .codex-plugin/plugin.json before updating the plugin source.",
        )
    return version


def sanitize_cachebuster(value: str) -> str:
    sanitized = re.sub(r"[^a-z0-9-]+", "-", value.strip().lower())
    sanitized = re.sub(r"-{2,}", "-", sanitized).strip("-")
    if not sanitized:
        fail(
            "cachebuster must contain at least one letter or digit",
            "Pass --cachebuster with a timestamp, commit id, or release token.",
        )
    return sanitized


def default_cachebuster() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


def with_cachebuster(version: str, cachebuster: str) -> str:
    version_prefix = version.split("+", 1)[0]
    return f"{version_prefix}+{CACHEBUSTER_PREFIX}.{sanitize_cachebuster(cachebuster)}"


def write_target_version(target: Path, next_version: str) -> tuple[str, str]:
    manifest = load_manifest(target)
    current_version = plugin_version(target)
    manifest["version"] = next_version
    manifest_path(target).write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return current_version, next_version


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


def should_validate_marketplace(
    target: Path,
    marketplace: Path,
    explicit_skip: bool,
) -> bool:
    if explicit_skip:
        return False
    if target.resolve() == DEFAULT_TARGET.resolve():
        return True
    return marketplace != DEFAULT_MARKETPLACE


def validate_marketplace(marketplace: Path) -> None:
    if not marketplace.is_file():
        fail(
            f"missing marketplace file: {marketplace}",
            "Create the personal marketplace entry or pass --skip-marketplace-check for a nonstandard target.",
        )
    try:
        payload = json.loads(marketplace.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid marketplace JSON: {marketplace}", str(exc))
    if not isinstance(payload, dict):
        fail(f"marketplace must contain a JSON object: {marketplace}")

    plugins = payload.get("plugins")
    if not isinstance(plugins, list):
        fail(f"marketplace has no plugins list: {marketplace}")

    matches = [
        entry
        for entry in plugins
        if isinstance(entry, dict) and entry.get("name") == PLUGIN_NAME
    ]
    if not matches:
        fail(
            f"marketplace has no {PLUGIN_NAME} entry: {marketplace}",
            "Add the personal plugin entry before reinstalling.",
        )

    source = matches[0].get("source")
    source_path = source.get("path") if isinstance(source, dict) else None
    source_kind = source.get("source") if isinstance(source, dict) else None
    if source_kind != "local" or source_path != EXPECTED_MARKETPLACE_PATH:
        fail(
            f"marketplace entry does not point to {EXPECTED_MARKETPLACE_PATH}",
            f"Observed source={source!r}",
            "Fix the marketplace entry before reinstalling.",
        )


def iter_relative_files(root: Path) -> set[Path]:
    if not root.exists():
        return set()
    return {
        path.relative_to(root)
        for path in root.rglob("*")
        if path.is_file()
    }


def target_extra_files(source: Path, target: Path) -> list[Path]:
    source_files = iter_relative_files(source)
    target_files = iter_relative_files(target)
    return sorted(target_files - source_files, key=lambda path: path.as_posix())


def validate_target_clean(source: Path, target: Path) -> list[Path]:
    extras = target_extra_files(source, target)
    if extras:
        fail(
            f"target contains files that are not in source: {target}",
            "Remove stale target files manually before applying a real update:",
            *(path.as_posix() for path in extras),
        )
    return extras


def copy_source(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target, dirs_exist_ok=True)


def print_report(
    source: Path,
    target: Path,
    apply: bool,
    source_version: str,
    target_version_before: str | None,
    planned_version: str | None,
    cachebuster_applied: tuple[str, str] | None,
    marketplace_checked: bool,
) -> None:
    mode = "apply" if apply else "dry-run"
    print("PLUGIN UPDATE PREP")
    print(f"mode: {mode}")
    print(f"source: {source}")
    print(f"target: {target}")
    print(f"source manifest version: {source_version}")
    print(f"target manifest version before: {target_version_before or 'missing'}")
    if planned_version:
        print(f"planned target version: {planned_version}")
    print(f"marketplace: {'checked' if marketplace_checked else 'skipped'}")
    print("required files:")
    for relative in REQUIRED_RELATIVE_PATHS:
        print(f"- ok {relative.as_posix()}")
    print("target stale-file guard: ok")
    if apply:
        print("action: copied repository plugin source to personal plugin source")
    else:
        print("action: no files copied; rerun with --apply to copy source files")
    if cachebuster_applied:
        before, after = cachebuster_applied
        print(f"cachebuster: updated target manifest version {before} -> {after}")
    elif planned_version:
        print("cachebuster: planned only; add --apply --apply-cachebuster to update target manifest")
    else:
        print("cachebuster: not requested")
    print("safety:")
    if marketplace_checked:
        print("- marketplace file validated but not modified")
    else:
        print("- marketplace file not modified")
    print("- installed plugin cache not modified")
    print("next steps:")
    if not apply:
        print("- run python scripts\\prepare_plugin_update.py --apply --apply-cachebuster")
    elif not cachebuster_applied:
        print("- update the target manifest cachebuster before reinstalling")
    print("- confirm this update is tied to an approved candidate, dogfood note, or explicit user request")
    print("- re-enable or reinstall the plugin through Codex App or CLI")
    print("- open a fresh Codex thread and run install smoke")
    print("- run python scripts\\verify_plugin_install_smoke.py")
    print("- record the cache version, smoke result, and any remaining manual step")
    print("PLUGIN UPDATE PREP: PASS")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    source = Path(args.source).expanduser().resolve()
    target = Path(args.target).expanduser().resolve()
    marketplace = Path(args.marketplace).expanduser().resolve()
    if args.apply_cachebuster and not args.apply:
        fail(
            "--apply-cachebuster requires --apply",
            "Use --apply --apply-cachebuster for a real update prep run.",
        )

    validate_source(source)
    validate_target(source, target)
    validate_target_clean(source, target)
    marketplace_checked = should_validate_marketplace(
        target,
        marketplace,
        args.skip_marketplace_check,
    )
    if marketplace_checked:
        validate_marketplace(marketplace)

    source_version = plugin_version(source)
    target_version_before = plugin_version(target) if target.exists() else None
    planned_version = (
        with_cachebuster(source_version, args.cachebuster or default_cachebuster())
        if args.cachebuster or args.apply_cachebuster
        else None
    )

    if args.apply:
        copy_source(source, target)
    cachebuster_applied = None
    if args.apply_cachebuster:
        assert planned_version is not None
        cachebuster_applied = write_target_version(target, planned_version)

    print_report(
        source,
        target,
        args.apply,
        source_version,
        target_version_before,
        planned_version,
        cachebuster_applied,
        marketplace_checked,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
