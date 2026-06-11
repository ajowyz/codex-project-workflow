#!/usr/bin/env python3
import importlib.util
import json
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = SKILL_DIR.parents[2]


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPT_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


adr_index = load("adr_index")
measure_context = load("measure_context")


class ScriptTests(unittest.TestCase):
    def test_current_decisions(self):
        records = adr_index.parse(PROJECT_ROOT / "docs" / "DECISIONS.md")
        self.assertEqual(26, len(records))
        self.assertEqual("ADR-001", records[0]["id"])
        self.assertEqual("ADR-026", records[-1]["id"])

    def test_unpaired_replacement_fails(self):
        records = [
            {"id": "ADR-001", "governance_state": "已替代", "replaces_ids": [], "replaced_by_id": "ADR-002"},
            {"id": "ADR-002", "governance_state": "已确认", "replaces_ids": [], "replaced_by_id": None},
        ]
        with self.assertRaisesRegex(ValueError, "not declared at both ends"):
            adr_index.validate(records)

    def test_replacement_cycle_fails(self):
        records = [
            {"id": "ADR-001", "governance_state": "已替代", "replaces_ids": ["ADR-002"], "replaced_by_id": "ADR-002"},
            {"id": "ADR-002", "governance_state": "已替代", "replaces_ids": ["ADR-001"], "replaced_by_id": "ADR-001"},
        ]
        with self.assertRaisesRegex(ValueError, "replacement cycle"):
            adr_index.validate(records)

    def test_context_budgets(self):
        metrics = measure_context.skill_metrics(SKILL_DIR / "SKILL.md")
        self.assertLessEqual(metrics["description_chars"], 800)
        self.assertLessEqual(metrics["body_chars"], 1500)
        for path in (SKILL_DIR / "references").glob("*.md"):
            self.assertEqual(1, measure_context.reference_metrics(path)["h1_count"])

    def test_trigger_case_counts(self):
        cases = json.loads((SKILL_DIR / "evals" / "trigger_cases.json").read_text(encoding="utf-8"))
        self.assertEqual({"positive", "negative", "boundary"}, set(cases))
        self.assertTrue(all(len(cases[group]) >= 10 for group in cases))


if __name__ == "__main__":
    unittest.main()
