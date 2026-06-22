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
            raise SystemExit(f"missing version directory: {candidate}")
        return candidate

    if not cache_root.is_dir():
        raise SystemExit(f"missing plugin cache root: {cache_root}")

    versions = [path for path in cache_root.iterdir() if path.is_dir()]
    if not versions:
        raise SystemExit(f"no plugin cache versions found under: {cache_root}")
    return max(versions, key=lambda path: path.stat().st_mtime).resolve()


def require_file(path: Path) -> None:
    if not path.is_file():
        raise SystemExit(f"missing required file: {path}")


def require_inside(path: Path, root: Path) -> None:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError as exc:
        raise SystemExit(f"path is outside plugin cache version: {path}") from exc


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
        raise SystemExit(
            f"helper failed for {reference}: {result.stderr.strip() or result.stdout.strip()}"
        )
    output = result.stdout
    if "## Execution Rules" not in output:
        raise SystemExit(f"{reference}: missing Execution Rules output")
    if "## Output Requirements" not in output:
        raise SystemExit(f"{reference}: missing Output Requirements output")
    match = METRICS_RE.search(output)
    if match is None:
        raise SystemExit(f"{reference}: missing codex-reference-metrics marker")
    return int(match.group(1)), int(match.group(2))


def main() -> int:
    args = parse_args()
    cache_root = Path(args.cache_root).expanduser().resolve()
    version_dir = choose_version_dir(cache_root, args.version_dir)

    skill_root = version_dir / "skills" / PLUGIN_NAME
    skill_md = skill_root / "SKILL.md"
    helper = skill_root / "scripts" / "read_reference.py"
    references_dir = skill_root / "references"

    required_files = [skill_md, helper]
    required_files.extend(references_dir / f"{name}.md" for name in REFERENCE_NAMES)
    for path in required_files:
        require_file(path)
        require_inside(path, version_dir)

    print(f"plugin version dir: {version_dir}")
    print(f"skill: {skill_md}")
    print(f"helper: {helper}")
    print(f"references: {references_dir}")

    for reference in REFERENCE_NAMES:
        codepoints, h2_sections = run_reference(helper, reference)
        print(
            f"{reference}: ok "
            f"codepoints={codepoints} h2_sections={h2_sections}"
        )

    print("plugin install smoke passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
