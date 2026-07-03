#!/usr/bin/env python3
"""Focused tests for prepare_plugin_update.py."""

from __future__ import annotations

import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "prepare_plugin_update.py"


def load_update_module():
    spec = importlib.util.spec_from_file_location("prepare_plugin_update", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class PluginUpdatePrepTests(unittest.TestCase):
    def setUp(self) -> None:
        self.update = load_update_module()
        self.tmp = tempfile.TemporaryDirectory(prefix="dogfood-update-test-")
        self.addCleanup(self.tmp.cleanup)
        self.tmp_path = Path(self.tmp.name)

    def build_source(self) -> Path:
        source = self.tmp_path / "source" / self.update.PLUGIN_NAME
        for relative in self.update.REQUIRED_RELATIVE_PATHS:
            path = source / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"test file: {relative.as_posix()}\n", encoding="utf-8")
        return source

    def test_dry_run_reports_safety_and_next_steps(self) -> None:
        source = self.build_source()
        target = self.tmp_path / "target" / self.update.PLUGIN_NAME
        output = io.StringIO()

        with redirect_stdout(output):
            result = self.update.main(
                ["--source", str(source), "--target", str(target)]
            )

        text = output.getvalue()
        self.assertEqual(result, 0)
        self.assertIn("PLUGIN UPDATE PREP", text)
        self.assertIn("mode: dry-run", text)
        self.assertIn("action: no files copied", text)
        self.assertIn("marketplace file not modified", text)
        self.assertIn("installed plugin cache not modified", text)
        self.assertIn("PLUGIN UPDATE PREP: PASS", text)
        self.assertFalse(target.exists())

    def test_apply_copies_required_files(self) -> None:
        source = self.build_source()
        target = self.tmp_path / "target" / self.update.PLUGIN_NAME
        output = io.StringIO()

        with redirect_stdout(output):
            result = self.update.main(
                ["--source", str(source), "--target", str(target), "--apply"]
            )

        self.assertEqual(result, 0)
        self.assertIn("mode: apply", output.getvalue())
        for relative in self.update.REQUIRED_RELATIVE_PATHS:
            self.assertTrue((target / relative).is_file(), relative)

    def test_missing_required_file_fails_with_next_steps(self) -> None:
        source = self.build_source()
        (source / "README.md").unlink()

        with self.assertRaises(SystemExit) as raised:
            self.update.validate_source(source)

        message = str(raised.exception)
        self.assertIn("PLUGIN UPDATE PREP: FAIL", message)
        self.assertIn("plugin source is incomplete", message)
        self.assertIn("README.md", message)

    def test_target_inside_source_is_rejected(self) -> None:
        source = self.build_source()
        target = source / "nested-target"

        with self.assertRaises(SystemExit) as raised:
            self.update.validate_target(source, target)

        message = str(raised.exception)
        self.assertIn("target cannot be inside the source package", message)


if __name__ == "__main__":
    unittest.main()
