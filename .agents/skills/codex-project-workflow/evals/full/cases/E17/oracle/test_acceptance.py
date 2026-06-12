import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[1] / "workspace" / "default"


class AcceptanceTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, "app.py", *args],
            cwd=WORKSPACE,
            check=False,
            capture_output=True,
            text=True,
        )

    def test_items_persist_and_duplicates_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            data_file = str(Path(directory) / "reading.json")
            first = self.run_cli(
                "--data-file",
                data_file,
                "add",
                "https://example.test/one",
            )
            duplicate = self.run_cli(
                "--data-file",
                data_file,
                "add",
                "https://example.test/one",
            )
            listing = self.run_cli("--data-file", data_file, "list")
        self.assertEqual(first.returncode, 0)
        self.assertNotEqual(duplicate.returncode, 0)
        self.assertEqual(listing.stdout.strip(), "https://example.test/one")


if __name__ == "__main__":
    unittest.main()
