#!/usr/bin/env python3
import copy
import hashlib
import importlib.util
import json
import shutil
import subprocess
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
collect_smoke = load("collect_smoke")
validate_full_fixtures = load("validate_full_fixtures")
setup_full_eval = load("setup_full_eval")
collect_full_eval = load("collect_full_eval")
validate_full_results = load("validate_full_results")


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

    def test_e23_approval_package_bindings_and_patch_contents(self):
        root = SKILL_DIR / "evals" / "full" / "cases" / "E23" / "workspace"
        expected = {
            "valid_approval_package": (True, True, True, True, True, True),
            "candidate_mutated_after_approval": (True, False, True, True, True, True),
            "baseline_mutated_after_approval": (False, True, True, False, False, True),
            "regressed_candidate": (True, True, True, True, True, True),
            "rejected_candidate": (True, True, True, True, True, False),
        }

        for variant, expected_status in expected.items():
            with self.subTest(variant=variant):
                workspace = root / variant
                approval = json.loads(
                    (workspace / "approval.json").read_text(encoding="utf-8")
                )
                base = workspace / "active" / "SKILL.baseline.md"
                patch = workspace / "candidate" / "patch.diff"
                candidate = workspace / "candidate" / "SKILL.candidate.md"
                evaluation = workspace / "evaluations" / "comparison.json"

                base_bound = hashlib.sha256(base.read_bytes()).hexdigest() == approval["base_hash"]
                patch_bound = hashlib.sha256(patch.read_bytes()).hexdigest() == approval["patch_hash"]
                evaluation_bound = (
                    hashlib.sha256(evaluation.read_bytes()).hexdigest()
                    == approval["evaluation_hash"]
                )

                with tempfile.TemporaryDirectory() as temporary:
                    temporary_root = Path(temporary)
                    (temporary_root / "active").mkdir()
                    (temporary_root / "candidate").mkdir()
                    shutil.copyfile(base, temporary_root / "active" / "SKILL.baseline.md")
                    shutil.copyfile(base, temporary_root / "candidate" / "SKILL.candidate.md")
                    shutil.copyfile(patch, temporary_root / "patch.diff")
                    result = subprocess.run(
                        [
                            "git",
                            "apply",
                            "-p0",
                            "--ignore-space-change",
                            "--ignore-whitespace",
                            "patch.diff",
                        ],
                        cwd=temporary_root,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    patch_applies = result.returncode == 0
                    patch_matches_candidate = patch_applies and (
                        (temporary_root / "candidate" / "SKILL.candidate.md").read_text(
                            encoding="utf-8"
                        )
                        == candidate.read_text(encoding="utf-8")
                    )

                self.assertEqual(
                    expected_status,
                    (
                        base_bound,
                        patch_bound,
                        evaluation_bound,
                        patch_applies,
                        patch_matches_candidate,
                        approval["decision"] == "approved",
                    ),
                )

    def test_latest_candidate_budget_and_reference_reader(self):
        candidate_dir = (
            SKILL_DIR / "evals" / "smoke" / "SMOKE-20260612-10" / "candidate_skill"
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
        candidate_text = (candidate_dir / "SKILL.candidate.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "python .agents/skills/codex-project-workflow/scripts/"
            'read_reference.py research "Execution Rules" "Output Requirements"',
            candidate_text,
        )
        self.assertIn("Never list headings", candidate_text)
        self.assertIn("Do not run proposed streams in main", candidate_text)

    def test_smoke_collector_traces_reference_reader_sections(self):
        calls = [
            {
                "call_id": "list",
                "name": "shell_command",
                "arguments": {
                    "command": (
                        "python .agents/skills/codex-project-workflow/"
                        "scripts/read_reference.py research"
                    )
                },
                "output": {
                    "chars": 100,
                    "h2_sections": 0,
                    "preview": "Exit code: 0\nOutput:\nExecution Rules\nOutput Requirements",
                },
            },
            {
                "call_id": "sections",
                "name": "shell_command",
                "arguments": {
                    "command": (
                        "python .agents/skills/codex-project-workflow/"
                        "scripts/read_reference.py research "
                        "'Execution Rules' 'Output Requirements'"
                    )
                },
                "output": {
                    "chars": 900,
                    "h2_sections": 2,
                    "preview": "Exit code: 0\nOutput:\n## Execution Rules",
                },
            },
            {
                "call_id": "failed",
                "name": "shell_command",
                "arguments": {
                    "command": "python scripts/read_reference.py governance"
                },
                "output": {
                    "chars": 200,
                    "h2_sections": 0,
                    "preview": "Exit code: 1\nOutput:\ncan't open file",
                },
            },
        ]
        trace = collect_smoke.reference_call_trace(calls, SKILL_DIR)
        self.assertEqual(["failed"], trace["reference_failed_calls"])
        self.assertEqual(["list"], trace["reference_list_calls"])
        self.assertEqual(["sections"], trace["reference_section_read_calls"])
        self.assertEqual(2, trace["reference_h2_sections"])
        self.assertEqual(["research.md"], trace["reference_files"])
        self.assertGreater(trace["reference_loaded_chars"], 0)

    def test_full_fixture_manifest_assigns_remaining_cases(self):
        schema = json.loads(
            (
                SKILL_DIR / "evals" / "full" / "fixture.schema.json"
            ).read_text(encoding="utf-8")
        )
        manifest = json.loads(
            (
                SKILL_DIR / "evals" / "full" / "batch_manifest.json"
            ).read_text(encoding="utf-8")
        )
        expected = validate_full_fixtures.expected_case_map()
        assigned, _, calibration = validate_full_fixtures.validate_manifest(
            schema,
            manifest,
            expected,
        )
        self.assertEqual(31, len(assigned))
        self.assertEqual(8, len(calibration))

    def test_full_fixture_path_escape_fails(self):
        with self.assertRaisesRegex(ValueError, "parent traversal"):
            validate_full_fixtures.safe_relative_path(
                "../outside",
                "fixture.workspace",
            )

    def test_full_fixture_structured_reply(self):
        self.assertTrue(
            validate_full_fixtures.valid_scripted_reply(
                {
                    "when": "The assistant asks for a storage decision.",
                    "reply": "Use a local JSON file.",
                }
            )
        )
        self.assertFalse(
            validate_full_fixtures.valid_scripted_reply(
                {"reply": "Missing trigger."}
            )
        )

    def test_full_eval_variant_selection(self):
        case = {
            "case_id": "E99",
            "variants": [
                {"id": "first"},
                {"id": "second"},
            ],
        }
        self.assertEqual(
            "first",
            setup_full_eval.select_variant(case)["id"],
        )
        self.assertEqual(
            "second",
            setup_full_eval.select_variant(case, "second")["id"],
        )
        with self.assertRaisesRegex(ValueError, "unknown variant"):
            setup_full_eval.select_variant(case, "missing")

    def test_full_eval_minimal_variant_cover(self):
        case = {
            "case_id": "E99",
            "variants": [
                {
                    "id": "a",
                    "expected": {"assertion_subjects": ["one"]},
                },
                {
                    "id": "b",
                    "expected": {"assertion_subjects": ["two", "three"]},
                },
                {
                    "id": "c",
                    "expected": {"assertion_subjects": ["three"]},
                },
            ],
        }
        self.assertEqual(
            ["a", "b"],
            setup_full_eval.minimal_variant_cover(case),
        )

    def test_full_eval_expected_variant_selection(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            original = collect_full_eval.CASES_DIR
            try:
                collect_full_eval.CASES_DIR = root
                case_dir = root / "E99"
                case_dir.mkdir()
                (case_dir / "case.json").write_text(
                    json.dumps(
                        {
                            "variants": [
                                {
                                    "id": "one",
                                    "expected": {"changed_files": ["one.txt"]},
                                },
                                {
                                    "id": "two",
                                    "expected": {"changed_files": ["two.txt"]},
                                },
                            ]
                        }
                    ),
                    encoding="utf-8",
                )
                expected = collect_full_eval.load_expected("E99", "two")
                self.assertEqual(["two.txt"], expected["changed_files"])
            finally:
                collect_full_eval.CASES_DIR = original

    def test_full_result_dimensions_are_stable(self):
        self.assertEqual(
            [
                "goal_preservation",
                "proactive_completeness",
                "workflow_fit",
                "professionalism",
                "confirmation_boundary",
                "evidence_and_verification",
                "implementation_integrity",
                "output_efficiency",
            ],
            validate_full_results.DIMENSIONS,
        )

    def test_full_result_changed_file_patterns(self):
        self.assertTrue(
            validate_full_results.paths_match_patterns(
                ["src/app.py", "tests/test_app.py"],
                ["src/app.py", "tests/**"],
            )
        )
        self.assertFalse(
            validate_full_results.paths_match_patterns(
                ["src/app.py", "secrets.txt"],
                ["src/app.py", "tests/**"],
            )
        )

    def test_full_result_changed_file_mismatch_is_a_hard_failure(self):
        self.assertFalse(
            validate_full_results.validate_changed_files(
                ["output/model.json"],
                [],
                ["changed_files_mismatch"],
            )
        )
        with self.assertRaisesRegex(
            ValueError,
            "changed files mismatch must be recorded",
        ):
            validate_full_results.validate_changed_files(
                ["output/model.json"],
                [],
                [],
            )


if __name__ == "__main__":
    unittest.main()
