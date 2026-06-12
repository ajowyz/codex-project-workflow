import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


CASE_ROOT = Path(__file__).resolve().parents[1]


class ProductPathTests(unittest.TestCase):
    def run_product(self, variant):
        workspace = CASE_ROOT / "workspace" / variant
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        output = root / "model.json"
        state = root / "state.json"
        trace = root / "trace.log"
        result = subprocess.run(
            [
                sys.executable,
                "app.py",
                "demo",
                "--output",
                str(output),
                "--state",
                str(state),
                "--trace",
                str(trace),
            ],
            cwd=workspace,
            check=True,
            capture_output=True,
            text=True,
        )
        return temporary, result, output, state, trace

    def test_product_path_has_full_call_chain(self):
        temporary, _, output, state, trace = self.run_product("product_path")
        try:
            self.assertEqual(
                json.loads(output.read_text(encoding="utf-8")),
                {"name": "demo", "shape": "cube", "version": 1},
            )
            self.assertEqual(
                trace.read_text(encoding="utf-8").splitlines(),
                [
                    "product_entry",
                    "object_system",
                    "state_update",
                    "save_path",
                ],
            )
            self.assertEqual(
                json.loads(state.read_text(encoding="utf-8")),
                {"active_model": "demo", "model_count": 1},
            )
        finally:
            temporary.cleanup()

    def test_bypass_has_correct_result_but_no_product_path(self):
        temporary, _, output, _, trace = self.run_product("entry_bypass")
        try:
            self.assertEqual(
                json.loads(output.read_text(encoding="utf-8")),
                {"name": "demo", "shape": "cube", "version": 1},
            )
            self.assertFalse(trace.exists())
        finally:
            temporary.cleanup()


if __name__ == "__main__":
    unittest.main()
