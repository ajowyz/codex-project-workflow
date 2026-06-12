import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class StateMatrixTests(unittest.TestCase):
    def test_all_declared_scenarios_have_plan_and_decisions(self):
        oracle = json.loads(
            (ROOT / "oracle" / "scenarios.json").read_text(encoding="utf-8")
        )
        scenarios = ROOT / "workspace" / "state_matrix" / "scenarios"
        self.assertEqual(
            set(oracle["scenarios"]),
            {path.name for path in scenarios.iterdir() if path.is_dir()},
        )
        for scenario in oracle["scenarios"]:
            docs = scenarios / scenario / "docs"
            self.assertTrue((docs / "PLAN.md").is_file())
            self.assertTrue((docs / "DECISIONS.md").is_file())

    def test_projection_field_contract_is_exact(self):
        oracle = json.loads(
            (ROOT / "oracle" / "scenarios.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            oracle["projection_fields"],
            [
                "id",
                "title",
                "governance_state",
                "replaces_ids",
                "replaced_by_id",
                "body_anchor",
            ],
        )

    def test_selective_loading_has_isolated_optional_material(self):
        docs = (
            ROOT
            / "workspace"
            / "state_matrix"
            / "scenarios"
            / "12-selective-loading"
            / "docs"
        )
        self.assertTrue((docs / "PRD.md").is_file())
        self.assertTrue((docs / "audits" / "ARCHIVE.md").is_file())


if __name__ == "__main__":
    unittest.main()
