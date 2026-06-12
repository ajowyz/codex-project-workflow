import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class IsolationTests(unittest.TestCase):
    def test_stage_two_is_outside_stage_one_workspace(self):
        stage_one = ROOT / "workspace" / "isolated_release"
        self.assertFalse((stage_one / "release" / "stage2").exists())
        self.assertFalse((stage_one / "executor_contract.md").exists())
        self.assertTrue((ROOT / "restricted" / "stage2").is_dir())

    def test_stage_two_evidence_is_parseable(self):
        for name in ["tool_events.json", "runtime_evidence.json"]:
            path = ROOT / "restricted" / "stage2" / name
            json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
