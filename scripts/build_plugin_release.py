#!/usr/bin/env python3
"""Validate and build the public codex-project-workflow plugin archive."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

try:
    from prepare_plugin_update import PLUGIN_NAME, REQUIRED_RELATIVE_PATHS
except ModuleNotFoundError:  # Imported by the unit-test discovery process.
    from scripts.prepare_plugin_update import PLUGIN_NAME, REQUIRED_RELATIVE_PATHS


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = REPO_ROOT / "plugins" / PLUGIN_NAME
DEFAULT_MARKETPLACE = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"
DEFAULT_ROOT_LICENSE = REPO_ROOT / "LICENSE"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "dist"
EXPECTED_REPOSITORY = "https://github.com/ajowyz/codex-project-workflow"
EXPECTED_MARKETPLACE_NAME = "ajowyz-codex"
EXPECTED_MARKETPLACE_PATH = f"./plugins/{PLUGIN_NAME}"
SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z.-]+)?$"
)
FORBIDDEN_PATTERNS = (
    (
        "personal absolute path",
        re.compile(r"(?i)(?:[a-z]:\\users\\[^\\\s]+|/users/[^/\s]+|/home/[^/\s]+)"),
    ),
    (
        "private key",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ),
    (
        "GitHub token",
        re.compile(r"(?:ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})"),
    ),
    (
        "OpenAI-style secret key",
        re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    ),
)


def fail(reason: str) -> None:
    raise SystemExit(f"PLUGIN RELEASE BUILD: FAIL\nreason: {reason}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the public plugin boundary and build a deterministic ZIP."
    )
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--marketplace", default=str(DEFAULT_MARKETPLACE))
    parser.add_argument("--root-license", default=str(DEFAULT_ROOT_LICENSE))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    return parser.parse_args(argv)


def load_json(path: Path, label: str) -> dict[str, object]:
    if not path.is_file():
        fail(f"missing {label}: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"invalid {label}: {path}: {exc}")
    if not isinstance(payload, dict):
        fail(f"{label} must contain a JSON object: {path}")
    return payload


def package_files(source: Path) -> set[Path]:
    if not source.is_dir():
        fail(f"missing plugin source: {source}")
    symlinks = [path for path in source.rglob("*") if path.is_symlink()]
    if symlinks:
        fail(f"plugin source contains symlinks: {symlinks[0]}")
    return {
        path.relative_to(source)
        for path in source.rglob("*")
        if path.is_file()
    }


def validate_file_boundary(source: Path) -> list[Path]:
    expected = set(REQUIRED_RELATIVE_PATHS)
    actual = package_files(source)
    missing = sorted(expected - actual, key=lambda path: path.as_posix())
    extras = sorted(actual - expected, key=lambda path: path.as_posix())
    if missing:
        fail("missing package files: " + ", ".join(path.as_posix() for path in missing))
    if extras:
        fail("unexpected package files: " + ", ".join(path.as_posix() for path in extras))
    return sorted(actual, key=lambda path: path.as_posix())


def validate_manifest(source: Path) -> str:
    manifest_path = source / ".codex-plugin" / "plugin.json"
    manifest = load_json(manifest_path, "plugin manifest")
    if manifest.get("name") != PLUGIN_NAME:
        fail(f"manifest name must be {PLUGIN_NAME}")
    version = manifest.get("version")
    if not isinstance(version, str) or SEMVER_RE.fullmatch(version) is None:
        fail(f"manifest version must be strict semver without build metadata: {version!r}")
    if manifest.get("license") != "MIT":
        fail("manifest license must be MIT")
    if manifest.get("repository") != EXPECTED_REPOSITORY:
        fail(f"manifest repository must be {EXPECTED_REPOSITORY}")
    if manifest.get("homepage") != EXPECTED_REPOSITORY:
        fail(f"manifest homepage must be {EXPECTED_REPOSITORY}")
    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        fail("manifest interface must be an object")
    if interface.get("websiteURL") != EXPECTED_REPOSITORY:
        fail(f"manifest interface.websiteURL must be {EXPECTED_REPOSITORY}")
    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
        fail("manifest interface.defaultPrompt must contain one to three prompts")
    if any(not isinstance(prompt, str) or not prompt.strip() or len(prompt) > 128 for prompt in prompts):
        fail("each default prompt must be a non-empty string of at most 128 characters")
    return version


def validate_license(source: Path, root_license: Path) -> None:
    plugin_license = source / "LICENSE"
    if not root_license.is_file():
        fail(f"missing root license: {root_license}")
    if not plugin_license.is_file():
        fail(f"missing plugin license: {plugin_license}")
    root_bytes = root_license.read_bytes()
    if root_bytes != plugin_license.read_bytes():
        fail("root LICENSE and plugin LICENSE must be byte-identical")
    if not root_bytes.startswith(b"MIT License"):
        fail("license text must be the MIT License")


def validate_marketplace(marketplace_path: Path) -> None:
    marketplace = load_json(marketplace_path, "repository marketplace")
    if marketplace.get("name") != EXPECTED_MARKETPLACE_NAME:
        fail(f"marketplace name must be {EXPECTED_MARKETPLACE_NAME}")
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list):
        fail("marketplace plugins must be an array")
    matches = [
        entry
        for entry in plugins
        if isinstance(entry, dict) and entry.get("name") == PLUGIN_NAME
    ]
    if len(matches) != 1:
        fail(f"marketplace must contain exactly one {PLUGIN_NAME} entry")
    source = matches[0].get("source")
    if not isinstance(source, dict):
        fail("marketplace plugin source must be an object")
    if source.get("source") != "local" or source.get("path") != EXPECTED_MARKETPLACE_PATH:
        fail(f"marketplace source must point to {EXPECTED_MARKETPLACE_PATH}")
    policy = matches[0].get("policy")
    if not isinstance(policy, dict):
        fail("marketplace plugin policy must be an object")
    if policy.get("installation") != "AVAILABLE":
        fail("marketplace installation policy must be AVAILABLE")
    if policy.get("authentication") != "ON_INSTALL":
        fail("marketplace authentication policy must be ON_INSTALL")


def scan_public_files(source: Path, files: list[Path]) -> None:
    for relative in files:
        path = source / relative
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            fail(f"public package contains a non-UTF-8 file: {relative.as_posix()}")
        for label, pattern in FORBIDDEN_PATTERNS:
            if pattern.search(text):
                fail(f"{label} detected in {relative.as_posix()}")


def canonical_text_bytes(path: Path) -> bytes:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        fail(f"public package contains a non-UTF-8 file: {path}")
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def write_archive(source: Path, files: list[Path], output_dir: Path, version: str) -> tuple[Path, Path, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"{PLUGIN_NAME}-{version}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for relative in files:
            info = zipfile.ZipInfo(relative.as_posix(), date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o100644 & 0xFFFF) << 16
            bundle.writestr(
                info,
                canonical_text_bytes(source / relative),
                compresslevel=9,
            )
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    checksum = archive.with_suffix(archive.suffix + ".sha256")
    checksum.write_text(f"{digest}  {archive.name}\n", encoding="ascii", newline="\n")
    return archive, checksum, digest


def build_release(
    source: Path,
    marketplace: Path,
    root_license: Path,
    output_dir: Path,
) -> tuple[Path, Path, str, list[Path]]:
    files = validate_file_boundary(source)
    version = validate_manifest(source)
    validate_license(source, root_license)
    validate_marketplace(marketplace)
    scan_public_files(source, files)
    archive, checksum, digest = write_archive(source, files, output_dir, version)
    return archive, checksum, digest, files


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    source = Path(args.source).expanduser().resolve()
    marketplace = Path(args.marketplace).expanduser().resolve()
    root_license = Path(args.root_license).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    archive, checksum, digest, files = build_release(
        source, marketplace, root_license, output_dir
    )
    print("PLUGIN RELEASE BUILD")
    print(f"source: {source}")
    print(f"files: {len(files)}")
    print(f"archive: {archive}")
    print(f"checksum file: {checksum}")
    print(f"sha256: {digest}")
    print("archive root: plugin package")
    print("PLUGIN RELEASE BUILD: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
