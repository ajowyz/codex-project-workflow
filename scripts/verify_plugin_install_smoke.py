#!/usr/bin/env python3
"""Read-only smoke test for the installed codex-project-workflow plugin."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path


PLUGIN_NAME = "codex-project-workflow"
REFERENCE_NAMES = ("governance", "research", "verification")
METRICS_RE = re.compile(
    r"<!-- codex-reference-metrics codepoints=(\d+) h2_sections=(\d+) -->"
)


def fail(reason: str, *next_steps: str) -> None:
    message = ["PLUGIN INSTALL SMOKE: FAIL", f"reason: {reason}"]
    if next_steps:
        message.append("next steps:")
        message.extend(f"- {step}" for step in next_steps)
    raise SystemExit("\n".join(message))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify the installed codex-project-workflow plugin cache."
    )
    parser.add_argument(
        "--cache-root",
        default=str(
            Path.home()
            / ".codex"
            / "plugins"
            / "cache"
            / "personal"
            / PLUGIN_NAME
        ),
        help="Plugin cache root that contains version subdirectories.",
    )
    parser.add_argument(
        "--version-dir",
        help="Specific plugin cache version directory to verify.",
    )
    return parser.parse_args()


def choose_version_dir(cache_root: Path, explicit: str | None) -> Path:
    if explicit:
        candidate = Path(explicit).expanduser().resolve()
        if not candidate.is_dir():
            fail(
                f"missing version directory: {candidate}",
                "Confirm the plugin is installed through Codex App or CLI.",
                "Pass --version-dir with the installed cache version directory.",
            )
        return candidate

    if not cache_root.is_dir():
        fail(
            f"missing plugin cache root: {cache_root}",
            "Enable codex-project-workflow from Codex App plugins.",
            "If the cache root is elsewhere, rerun with --cache-root.",
        )

    versions = [path for path in cache_root.iterdir() if path.is_dir()]
    if not versions:
        fail(
            f"no plugin cache versions found under: {cache_root}",
            "Reinstall or re-enable the plugin, then open a fresh Codex thread.",
        )
    return max(versions, key=lambda path: path.stat().st_mtime).resolve()


def require_file(path: Path) -> None:
    if not path.is_file():
        fail(
            f"missing required file: {path}",
            "Rebuild or reinstall the plugin package.",
            "Verify the source package includes SKILL.md, read_reference.py, and all references.",
        )


def require_inside(path: Path, root: Path) -> None:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError as exc:
        fail(
            f"path is outside plugin cache version: {path}",
            "Do not accept a mixed install that borrows files from the project .agents copy.",
            "Reinstall the plugin and rerun this smoke.",
        )


def run_reference(helper: Path, reference: str) -> tuple[int, int]:
    with tempfile.TemporaryDirectory(prefix="codex-plugin-smoke-") as tmp:
        result = subprocess.run(
            [
                sys.executable,
                str(helper),
                reference,
                "Execution Rules",
                "Output Requirements",
            ],
            cwd=tmp,
            text=True,
            capture_output=True,
            encoding="utf-8",
        )
    if result.returncode != 0:
        fail(
            f"helper failed for {reference}: {result.stderr.strip() or result.stdout.strip()}",
            "Open a fresh Codex thread and confirm the installed skill path.",
            "Check that the installed helper can read plugin-local references.",
        )
    output = result.stdout
    if "## Execution Rules" not in output:
        fail(f"{reference}: missing Execution Rules output")
    if "## Output Requirements" not in output:
        fail(f"{reference}: missing Output Requirements output")
    match = METRICS_RE.search(output)
    if match is None:
        fail(f"{reference}: missing codex-reference-metrics marker")
    return int(match.group(1)), int(match.group(2))


def main() -> int:
    args = parse_args()
    cache_root = Path(args.cache_root).expanduser().resolve()
    version_dir = choose_version_dir(cache_root, args.version_dir)

    print("PLUGIN INSTALL SMOKE")
    print(f"cache root: {cache_root}")
    print(f"selected version: {version_dir.name}")

    skill_root = version_dir / "skills" / PLUGIN_NAME
    skill_md = skill_root / "SKILL.md"
    helper = skill_root / "scripts" / "read_reference.py"
    references_dir = skill_root / "references"

    required_files = [skill_md, helper]
    required_files.extend(references_dir / f"{name}.md" for name in REFERENCE_NAMES)
    for path in required_files:
        require_file(path)
        require_inside(path, version_dir)

    print("installed paths:")
    print(f"- plugin version dir: {version_dir}")
    print(f"- skill: {skill_md}")
    print(f"- helper: {helper}")
    print(f"- references: {references_dir}")
    print("fallback guard: helper is executed from a temporary directory")

    print("reference metrics:")
    for reference in REFERENCE_NAMES:
        codepoints, h2_sections = run_reference(helper, reference)
        print(
            f"- {reference}: ok "
            f"codepoints={codepoints} h2_sections={h2_sections}"
        )

    print("PLUGIN INSTALL SMOKE: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
