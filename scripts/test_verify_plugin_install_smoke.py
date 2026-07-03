#!/usr/bin/env python3
"""Focused tests for verify_plugin_install_smoke.py."""

from __future__ import annotations

import importlib.util
import io
import os
import sys
import tempfile
import textwrap
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "verify_plugin_install_smoke.py"


def load_smoke_module():
    spec = importlib.util.spec_from_file_location("verify_plugin_install_smoke", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class PluginInstallSmokeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.smoke = load_smoke_module()
        self.tmp = tempfile.TemporaryDirectory(prefix="dogfood-smoke-test-")
        self.addCleanup(self.tmp.cleanup)
        self.tmp_path = Path(self.tmp.name)

    def build_cache(self) -> Path:
        version_dir = self.tmp_path / "cache" / "0.1.0-test"
        skill_root = version_dir / "skills" / self.smoke.PLUGIN_NAME
        helper = skill_root / "scripts" / "read_reference.py"
        references = skill_root / "references"

        helper.parent.mkdir(parents=True)
        references.mkdir(parents=True)
        (skill_root / "SKILL.md").write_text("# Test Skill\n", encoding="utf-8")
        for name in self.smoke.REFERENCE_NAMES:
            (references / f"{name}.md").write_text("# Test Reference\n", encoding="utf-8")

        helper.write_text(
            textwrap.dedent(
                """
                import os
                from pathlib import Path

                marker = os.environ.get("DOGFOOD_SMOKE_CWD_FILE")
                if marker:
                    Path(marker).write_text(os.getcwd(), encoding="utf-8")

                print("## Execution Rules")
                print("ok")
                print()
                print("## Output Requirements")
                print("ok")
                print()
                print("<!-- codex-reference-metrics codepoints=12 h2_sections=2 -->")
                """
            ).lstrip(),
            encoding="utf-8",
        )
        return version_dir

    def test_success_output_is_an_acceptance_report(self) -> None:
        version_dir = self.build_cache()
        cache_root = version_dir.parent
        output = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["verify_plugin_install_smoke.py", "--cache-root", str(cache_root)],
        ):
            with redirect_stdout(output):
                result = self.smoke.main()

        text = output.getvalue()
        self.assertEqual(result, 0)
        self.assertIn("PLUGIN INSTALL SMOKE", text)
        self.assertIn("selected version: 0.1.0-test", text)
        self.assertIn("installed paths:", text)
        self.assertIn("fallback guard: helper is executed from a temporary directory", text)
        self.assertIn("- governance: ok codepoints=12 h2_sections=2", text)
        self.assertIn("- research: ok codepoints=12 h2_sections=2", text)
        self.assertIn("- verification: ok codepoints=12 h2_sections=2", text)
        self.assertIn("PLUGIN INSTALL SMOKE: PASS", text)

    def test_missing_cache_root_failure_has_next_steps(self) -> None:
        missing = self.tmp_path / "missing-cache"

        with self.assertRaises(SystemExit) as raised:
            self.smoke.choose_version_dir(missing, None)

        message = str(raised.exception)
        self.assertIn("PLUGIN INSTALL SMOKE: FAIL", message)
        self.assertIn("reason: missing plugin cache root:", message)
        self.assertIn("next steps:", message)
        self.assertIn("Enable codex-project-workflow from Codex App plugins.", message)
        self.assertIn("rerun with --cache-root", message)

    def test_mixed_install_paths_are_rejected(self) -> None:
        version_dir = self.build_cache()
        outside = self.tmp_path / "outside" / "SKILL.md"
        outside.parent.mkdir()
        outside.write_text("# outside\n", encoding="utf-8")

        with self.assertRaises(SystemExit) as raised:
            self.smoke.require_inside(outside, version_dir)

        message = str(raised.exception)
        self.assertIn("path is outside plugin cache version", message)
        self.assertIn("Do not accept a mixed install", message)
        self.assertIn("Reinstall the plugin and rerun this smoke.", message)

    def test_helper_runs_from_temporary_directory(self) -> None:
        version_dir = self.build_cache()
        helper = (
            version_dir
            / "skills"
            / self.smoke.PLUGIN_NAME
            / "scripts"
            / "read_reference.py"
        )
        marker = self.tmp_path / "helper-cwd.txt"

        with patch.dict(os.environ, {"DOGFOOD_SMOKE_CWD_FILE": str(marker)}):
            metrics = self.smoke.run_reference(helper, "governance")

        helper_cwd = marker.read_text(encoding="utf-8")
        self.assertEqual(metrics, (12, 2))
        self.assertIn("codex-plugin-smoke-", helper_cwd)
        self.assertNotEqual(Path(helper_cwd).resolve(), REPO_ROOT)


if __name__ == "__main__":
    unittest.main()
