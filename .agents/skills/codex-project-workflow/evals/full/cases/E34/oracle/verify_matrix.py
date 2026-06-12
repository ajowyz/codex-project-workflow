import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class MatrixTests(unittest.TestCase):
    def test_matrix_has_ten_scenarios_and_six_rows(self):
        oracle = json.loads(
            (ROOT / "oracle" / "decisions.json").read_text(encoding="utf-8")
        )
        self.assertEqual(len(oracle["trigger_rows"]), 6)
        self.assertEqual(len(oracle["scenarios"]), 10)
        for scenario, decision in oracle["scenarios"].items():
            self.assertEqual(len(decision["values"]), 6)
            self.assertTrue(
                (
                    ROOT
                    / "workspace"
                    / "decision_matrix"
                    / "scenarios"
                    / scenario
                    / "task.md"
                ).is_file()
            )

    def test_expected_distribution(self):
        oracle = json.loads(
            (ROOT / "oracle" / "decisions.json").read_text(encoding="utf-8")
        )
        artifacts = [
            item["artifact"] for item in oracle["scenarios"].values()
        ]
        self.assertEqual(artifacts.count("formal_contract"), 7)
        self.assertEqual(artifacts.count("path_constraint"), 3)


if __name__ == "__main__":
    unittest.main()
