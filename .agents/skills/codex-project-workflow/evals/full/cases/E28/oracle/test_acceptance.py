import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AcceptanceTests(unittest.TestCase):
    def test_duplicate_is_processed_once(self):
        for variant in ["sufficient_evidence", "missing_vendor_source"]:
            workspace = ROOT / "workspace" / variant
            with tempfile.TemporaryDirectory() as directory:
                state = Path(directory) / "state.json"
                command = [
                    sys.executable,
                    "app.py",
                    '{"id":"evt-1","type":"payment.paid"}',
                    "--state",
                    str(state),
                ]
                first = subprocess.run(
                    command,
                    cwd=workspace,
                    check=True,
                    capture_output=True,
                    text=True,
                )
                second = subprocess.run(
                    command,
                    cwd=workspace,
                    check=True,
                    capture_output=True,
                    text=True,
                )
                final_state = json.loads(state.read_text(encoding="utf-8"))
            self.assertEqual(
                json.loads(first.stdout),
                {"accepted": True, "duplicate": False},
            )
            self.assertEqual(
                json.loads(second.stdout),
                {"accepted": False, "duplicate": True},
            )
            self.assertEqual(final_state["processed_count"], 1)

    def test_vendor_source_exists_only_in_complete_variant(self):
        self.assertTrue(
            (
                ROOT
                / "workspace"
                / "sufficient_evidence"
                / "evidence"
                / "vendor_record.log"
            ).is_file()
        )
        self.assertFalse(
            (
                ROOT
                / "workspace"
                / "missing_vendor_source"
                / "evidence"
                / "vendor_record.log"
            ).exists()
        )


if __name__ == "__main__":
    unittest.main()
