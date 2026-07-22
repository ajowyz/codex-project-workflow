#!/usr/bin/env python3
"""Focused tests for build_plugin_release.py."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "build_plugin_release.py"


def load_release_module():
    spec = importlib.util.spec_from_file_location("build_plugin_release", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class PluginReleaseBuildTests(unittest.TestCase):
    def setUp(self) -> None:
        self.release = load_release_module()
        self.tmp = tempfile.TemporaryDirectory(prefix="plugin-release-test-")
        self.addCleanup(self.tmp.cleanup)
        self.tmp_path = Path(self.tmp.name)

    def build_fixture(self, license_name: str = "MIT") -> tuple[Path, Path, Path]:
        source = self.tmp_path / "plugins" / self.release.PLUGIN_NAME
        manifest = {
            "name": self.release.PLUGIN_NAME,
            "version": "0.1.0",
            "description": "Test plugin",
            "author": {"name": "Test"},
            "homepage": self.release.EXPECTED_REPOSITORY,
            "repository": self.release.EXPECTED_REPOSITORY,
            "license": license_name,
            "skills": "./skills/",
            "interface": {
                "displayName": "Test",
                "shortDescription": "Test",
                "longDescription": "Test",
                "developerName": "Test",
                "category": "Productivity",
                "websiteURL": self.release.EXPECTED_REPOSITORY,
                "capabilities": ["Test"],
                "defaultPrompt": ["Test this plugin."],
            },
        }
        license_text = "MIT License\n\nCopyright (c) 2026 Test\n"
        for relative in self.release.REQUIRED_RELATIVE_PATHS:
            path = source / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            if relative == Path(".codex-plugin") / "plugin.json":
                path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
            elif relative == Path("LICENSE"):
                path.write_text(license_text, encoding="utf-8", newline="\n")
            else:
                path.write_text(f"test file: {relative.as_posix()}\n", encoding="utf-8")

        root_license = self.tmp_path / "LICENSE"
        root_license.write_text(license_text, encoding="utf-8", newline="\n")
        marketplace = self.tmp_path / "marketplace.json"
        marketplace.write_text(
            json.dumps(
                {
                    "name": self.release.EXPECTED_MARKETPLACE_NAME,
                    "interface": {"displayName": "Test"},
                    "plugins": [
                        {
                            "name": self.release.PLUGIN_NAME,
                            "source": {
                                "source": "local",
                                "path": self.release.EXPECTED_MARKETPLACE_PATH,
                            },
                            "policy": {
                                "installation": "AVAILABLE",
                                "authentication": "ON_INSTALL",
                            },
                            "category": "Productivity",
                        }
                    ],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        return source, marketplace, root_license

    def test_builds_deterministic_rooted_archive_and_checksum(self) -> None:
        source, marketplace, root_license = self.build_fixture()
        output = self.tmp_path / "dist"

        archive, checksum, digest, files = self.release.build_release(
            source, marketplace, root_license, output
        )

        self.assertTrue(archive.is_file())
        self.assertTrue(checksum.is_file())
        self.assertIn(digest, checksum.read_text(encoding="ascii"))
        with zipfile.ZipFile(archive) as bundle:
            self.assertEqual(bundle.namelist(), [path.as_posix() for path in files])
            self.assertIn(".codex-plugin/plugin.json", bundle.namelist())
            self.assertIn("LICENSE", bundle.namelist())
            self.assertFalse(any(name.startswith("plugins/") for name in bundle.namelist()))

        second = self.tmp_path / "second"
        second_archive, _, second_digest, _ = self.release.build_release(
            source, marketplace, root_license, second
        )
        self.assertEqual(digest, second_digest)
        self.assertEqual(archive.read_bytes(), second_archive.read_bytes())

    def test_rejects_unlicensed_manifest(self) -> None:
        source, marketplace, root_license = self.build_fixture("UNLICENSED")
        with self.assertRaises(SystemExit) as raised:
            self.release.build_release(
                source, marketplace, root_license, self.tmp_path / "dist"
            )
        self.assertIn("manifest license must be MIT", str(raised.exception))

    def test_rejects_unexpected_package_file(self) -> None:
        source, marketplace, root_license = self.build_fixture()
        (source / "private-notes.txt").write_text("private\n", encoding="utf-8")
        with self.assertRaises(SystemExit) as raised:
            self.release.build_release(
                source, marketplace, root_license, self.tmp_path / "dist"
            )
        self.assertIn("unexpected package files", str(raised.exception))

    def test_rejects_personal_absolute_path(self) -> None:
        source, marketplace, root_license = self.build_fixture()
        (source / "README.md").write_text(
            "Do not publish C:\\Users\\someone\\private.txt\n", encoding="utf-8"
        )
        with self.assertRaises(SystemExit) as raised:
            self.release.build_release(
                source, marketplace, root_license, self.tmp_path / "dist"
            )
        self.assertIn("personal absolute path", str(raised.exception))

    def test_normalizes_text_line_endings_in_archive(self) -> None:
        source, marketplace, root_license = self.build_fixture()
        readme = source / "README.md"
        readme.write_bytes(b"first\r\nsecond\r\n")
        crlf_archive, _, crlf_digest, _ = self.release.build_release(
            source, marketplace, root_license, self.tmp_path / "crlf"
        )

        readme.write_bytes(b"first\nsecond\n")
        lf_archive, _, lf_digest, _ = self.release.build_release(
            source, marketplace, root_license, self.tmp_path / "lf"
        )

        self.assertEqual(crlf_digest, lf_digest)
        self.assertEqual(crlf_archive.read_bytes(), lf_archive.read_bytes())


if __name__ == "__main__":
    unittest.main()
