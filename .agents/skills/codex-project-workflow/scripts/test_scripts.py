#!/usr/bin/env python3
import copy
import importlib.util
import json
import tempfile
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


def load_path(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


adr_index = load("adr_index")
measure_context = load("measure_context")
validate_evals = load("validate_evals")
setup_smoke = load("setup_smoke")


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

    def test_evaluation_fixtures(self):
        summary = validate_evals.validate()
        self.assertEqual(36, summary["cases"])
        self.assertEqual(31, summary["critical_cases"])
        self.assertEqual(8, summary["dimensions"])
        self.assertEqual(30, summary["triggers"])

    def test_evaluation_anchor_regression_fails(self):
        schema = json.loads((SKILL_DIR / "evals" / "behavior_case.schema.json").read_text(encoding="utf-8"))
        data = json.loads((SKILL_DIR / "evals" / "behavior_cases.json").read_text(encoding="utf-8"))
        broken = copy.deepcopy(data)
        del broken["cases"][0]["scoring_anchors"]["output_efficiency"]
        with self.assertRaisesRegex(ValueError, "anchors must cover eight dimensions"):
            validate_evals.validate_cases(broken, schema)

    def test_evaluation_special_threshold_regression_fails(self):
        schema = json.loads((SKILL_DIR / "evals" / "behavior_case.schema.json").read_text(encoding="utf-8"))
        data = json.loads((SKILL_DIR / "evals" / "behavior_cases.json").read_text(encoding="utf-8"))
        broken = copy.deepcopy(data)
        e31 = next(case for case in broken["cases"] if case["id"] == "E31")
        assertion = next(item for item in e31["assertions"] if item["subject"] == "skill.description_codepoints")
        assertion["expected"] = 900
        with self.assertRaisesRegex(ValueError, "normative operator/value changed"):
            validate_evals.validate_cases(broken, schema)

    def test_evaluation_reverse_trigger_link_regression_fails(self):
        schema = json.loads((SKILL_DIR / "evals" / "behavior_case.schema.json").read_text(encoding="utf-8"))
        data = json.loads((SKILL_DIR / "evals" / "behavior_cases.json").read_text(encoding="utf-8"))
        cases = validate_evals.validate_cases(data, schema)
        cases["E01"]["trigger_case_ids"] = []
        with self.assertRaisesRegex(ValueError, "missing reverse behavior link"):
            validate_evals.validate_triggers(data, schema, cases)

    def test_smoke_fixture_setup(self):
        run_dir = SKILL_DIR / "evals" / "smoke" / "SMOKE-20260612-01"
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "workspaces"
            state_path = setup_smoke.setup(run_dir, output)
            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual({"baseline", "candidate"}, set(state["conditions"]))
            self.assertTrue((output / "baseline" / "E31" / "src" / "invoice.py").is_file())
            self.assertEqual(
                state["conditions"]["baseline"]["inventory"],
                state["conditions"]["candidate"]["inventory"],
            )

    def test_smoke_calibration_artifacts(self):
        run_dir = SKILL_DIR / "evals" / "smoke" / "SMOKE-20260612-01"
        manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
        assessment = json.loads((run_dir / "assessment.json").read_text(encoding="utf-8"))
        summary = json.loads((run_dir / "results" / "summary.json").read_text(encoding="utf-8"))
        self.assertEqual(["E01", "E04", "E06", "E31", "E36"], manifest["cases"])
        self.assertEqual(10, len(summary["results"]))
        self.assertTrue(all(result["status"] == "completed" for result in summary["results"]))
        self.assertFalse(assessment["formal_validity"]["valid"])

    def test_smoke_candidate_budget(self):
        candidate = (
            SKILL_DIR
            / "evals"
            / "smoke"
            / "SMOKE-20260612-01"
            / "candidate_skill"
            / "SKILL.candidate.md"
        )
        metrics = measure_context.skill_metrics(candidate)
        self.assertLessEqual(metrics["description_chars"], 800)
        self.assertLessEqual(metrics["body_chars"], 1500)

    def test_evaluation_candidates_are_not_discoverable_skills(self):
        discovered = sorted((PROJECT_ROOT / ".agents").rglob("SKILL.md"))
        self.assertEqual([SKILL_DIR / "SKILL.md"], discovered)

    def test_latest_candidate_budget_and_reference_reader(self):
        candidate_dir = (
            SKILL_DIR / "evals" / "smoke" / "SMOKE-20260612-04" / "candidate_skill"
        )
        metrics = measure_context.skill_metrics(
            candidate_dir / "SKILL.candidate.md"
        )
        self.assertLessEqual(metrics["description_chars"], 800)
        self.assertLessEqual(metrics["body_chars"], 1500)

        reader = load_path(
            "latest_candidate_reference_reader",
            candidate_dir / "scripts" / "read_reference.py",
        )
        research = reader.resolve_reference("research")
        self.assertEqual((SKILL_DIR / "references" / "research.md").resolve(), research)
        headings = [heading for heading, _ in reader.parse_sections(research.read_text(encoding="utf-8"))]
        self.assertIn("Execution Rules", headings)
        self.assertIn("Output Requirements", headings)


if __name__ == "__main__":
    unittest.main()
