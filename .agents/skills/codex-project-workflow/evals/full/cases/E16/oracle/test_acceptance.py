import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


WORKSPACE = Path(__file__).resolve().parents[1] / "workspace" / "default"
sys.path.insert(0, str(WORKSPACE))

from src.formatting import format_row, format_value
from src.report import render_report


class AcceptanceTests(unittest.TestCase):
    def test_include_zero_uses_existing_internal_path(self):
        records = [
            {"name": "alpha", "value": 3},
            {"name": "beta", "value": 0},
        ]
        self.assertEqual(
            render_report(records, include_zero=True),
            "alpha: 3\nbeta: ZERO",
        )
        self.assertEqual(format_value(0), "ZERO")
        with patch("src.report.format_row", wraps=format_row) as formatter:
            render_report(records, include_zero=True)
        self.assertEqual(formatter.call_count, 2)
        self.assertEqual(
            [call.args[0] for call in formatter.call_args_list],
            records,
        )

    def test_cli_behavior(self):
        result = subprocess.run(
            [
                sys.executable,
                "app.py",
                "data/sample.json",
                "--include-zero",
            ],
            cwd=WORKSPACE,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            result.stdout.strip(),
            "alpha: 3\nbeta: ZERO\ngamma: 2",
        )

    def test_fixture_input_is_stable(self):
        records = json.loads(
            (WORKSPACE / "data" / "sample.json").read_text(encoding="utf-8")
        )
        self.assertEqual(len(records), 3)


if __name__ == "__main__":
    unittest.main()
