#!/usr/bin/env python3
import copy
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import unicodedata
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = SKILL_DIR.parents[2]
PACKAGE_SKILL_DIR = (
    PROJECT_ROOT
    / "plugins"
    / "codex-project-workflow"
    / "skills"
    / "codex-project-workflow"
)
ACTIVE_SKILL_FILE = PACKAGE_SKILL_DIR / "SKILL.md"
CURRENT_CANDIDATE_ID = "CAND-20260718-15"


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
read_reference = load("read_reference")


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
        metrics = measure_context.skill_metrics(ACTIVE_SKILL_FILE)
        self.assertLessEqual(metrics["description_chars"], 800)
        self.assertLessEqual(metrics["body_chars"], 1500)
        self.assertIn(
            "deliverable through an existing product or application",
            ACTIVE_SKILL_FILE.read_text(encoding="utf-8"),
        )
        skill_text = ACTIVE_SKILL_FILE.read_text(encoding="utf-8")
        self.assertIn("Never activate for simple questions", skill_text)
        self.assertIn("routine local verification", skill_text)
        self.assertTrue(
            "Preserve ownership" in skill_text
            or "Change behavior in its existing owner" in skill_text
            or "Change behavior in existing owner" in skill_text
            or "edit existing owner" in skill_text
            or "edit the owner" in skill_text,
        )

    def test_plugin_package_is_the_only_discoverable_project_skill_owner(self):
        self.assertTrue(ACTIVE_SKILL_FILE.is_file())
        self.assertFalse((SKILL_DIR / "SKILL.md").exists())
        self.assertFalse((PROJECT_ROOT / ".codex" / "config.toml").exists())

    def test_evaluation_payload_matches_plugin_package(self):
        for relative in (
            Path("scripts") / "read_reference.py",
            Path("references") / "research.md",
            Path("references") / "governance.md",
            Path("references") / "verification.md",
        ):
            with self.subTest(relative=relative.as_posix()):
                self.assertEqual(
                    (SKILL_DIR / relative).read_bytes(),
                    (PACKAGE_SKILL_DIR / relative).read_bytes(),
                )

    def test_reference_contracts(self):
        governance = (SKILL_DIR / "references" / "governance.md").read_text(
            encoding="utf-8"
        )
        for field in (
            "added_codepoints",
            "added_sections",
            "reason",
            "unknown_resolved",
        ):
            self.assertIn(field, governance)
        for path in (SKILL_DIR / "references").glob("*.md"):
            self.assertEqual(1, measure_context.reference_metrics(path)["h1_count"])

    def test_current_candidate_budget_and_semantics(self):
        candidate_dir = (
            SKILL_DIR / "evals" / "candidates" / CURRENT_CANDIDATE_ID
        )
        skill_path = candidate_dir / "SKILL.candidate.md"
        metrics = measure_context.skill_metrics(skill_path)
        self.assertLessEqual(metrics["description_chars"], 800)
        self.assertLessEqual(metrics["body_chars"], 1500)

        skill_text = skill_path.read_text(encoding="utf-8")
        self.assertIn("multi-agent proposal", skill_text)
        self.assertIn("<skill_dir>/scripts/read_reference.py", skill_text)
        self.assertIn("later exact approval", skill_text)
        self.assertIn("changes need new approval", skill_text)
        self.assertIn("keeps agents `proposed`", skill_text)
        self.assertIn("main may continue displayed writes/verification", skill_text)
        self.assertIn("edit the owner", skill_text)
        self.assertIn("docs/IMPLEMENTATION_CONTRACT.md", skill_text)
        self.assertIn("Create no unneeded governance docs", skill_text)
        self.assertIn("high-impact/state/migration/path-proof", skill_text)
        self.assertIn("governance+verification, even read-only", skill_text)
        self.assertIn("Load each required protocol once/task", skill_text)
        self.assertIn("use the active `SKILL.md`'s directory", skill_text)
        self.assertIn("never the plugin version root", skill_text)
        self.assertIn("Run user/fixture verification commands verbatim", skill_text)
        self.assertIn("including repeats", skill_text)
        self.assertIn("report incomplete, never guess", skill_text)

        def reference_text(name):
            candidate_reference = candidate_dir / "references" / name
            if candidate_reference.is_file():
                return candidate_reference.read_text(encoding="utf-8")
            return (SKILL_DIR / "references" / name).read_text(encoding="utf-8")

        governance = reference_text("governance.md")
        verification = reference_text("verification.md")
        for text in (governance, verification):
            sections = dict(read_reference.parse_sections(text))
            selected = "\n\n".join(
                sections[name]
                for name in ("Execution Rules", "Output Requirements")
            )
            self.assertLessEqual(
                len(unicodedata.normalize("NFC", selected)),
                2500,
            )
        self.assertIn("refusal/unavailable picks fallback", governance)
        self.assertIn("Keep nonempty main work", governance)
        self.assertIn("before search, execution/install-sim, write, or verify", governance)
        self.assertIn("Propose roles, state `proposed`", governance)
        self.assertIn("approval packets", governance)
        self.assertIn("powershell -NoProfile -ExecutionPolicy Bypass -File tools/simulate_install.ps1", governance)
        self.assertIn("Ask and wait", governance)
        self.assertIn("pre-runs never count", governance)
        self.assertIn("Extra query/source/open needs new approval", governance)
        self.assertIn("No decision/unrelated approval is not action approval", governance)
        self.assertIn("Exact action approval lets main", governance)
        self.assertIn("displayed-scope main implementation/verification continue", governance)
        self.assertIn("local reads/planning", governance)
        self.assertIn("approval follow-up", governance)
        self.assertIn("aggregate unquoted line", governance)
        self.assertIn("added_codepoints=max(0, actual_loaded_codepoints-budget_codepoints)", governance)
        self.assertIn("helper-emitted NFC metrics", governance)
        self.assertIn("not files, unless required", governance)
        self.assertIn("A contract is not a project file by default", verification)
        self.assertIn("before the first product invocation", verification)
        self.assertIn("code-only owner-change contracts stay non-file", verification)
        self.assertIn("existing responsibility owner", verification)

    def test_current_candidate_bindings_and_patch(self):
        def canonical_hash_bytes(value):
            text = value.decode("utf-8-sig")
            text = text.replace("\r\n", "\n").replace("\r", "\n")
            normalized = unicodedata.normalize("NFC", text).encode("utf-8")
            return hashlib.sha256(normalized).hexdigest()

        candidate_dir = (
            SKILL_DIR / "evals" / "candidates" / CURRENT_CANDIDATE_ID
        )
        manifest = json.loads(
            (candidate_dir / "manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual("sha256-nfc-lf-utf8", manifest["hash_algorithm"])
        self.assertIn(
            manifest["status"],
            {
                "activated",
                "draft_pending_preflight",
                "preflight_passed_pending_isolated_evaluation",
                "preflight_passed_regression_blocked_infrastructure",
                "preflight_passed_regression_failed",
                "preflight_passed_regression_pending",
                "regression_passed_pending_activation_approval",
                "regression_failed",
            },
        )
        self.assertEqual(
            manifest["status"] == "activated",
            manifest["activation"]["allowed"],
        )

        active_states = set()
        for target in manifest["targets"]:
            active = PROJECT_ROOT / target["active_path"]
            candidate = PROJECT_ROOT / target["candidate_path"]
            active_hash = canonical_hash_bytes(active.read_bytes())
            self.assertIn(
                active_hash,
                {target["base_sha256"], target["candidate_sha256"]},
            )
            active_states.add(
                "base"
                if active_hash == target["base_sha256"]
                else "candidate"
            )
            self.assertEqual(
                target["candidate_sha256"],
                canonical_hash_bytes(candidate.read_bytes()),
            )
        for retired in manifest.get("retired_discovery_paths", []):
            retired_path = PROJECT_ROOT / retired["path"]
            self.assertFalse(retired_path.exists())
            baseline = subprocess.run(
                [
                    "git",
                    "show",
                    f"{manifest['base_commit']}:{retired['path']}",
                ],
                cwd=PROJECT_ROOT,
                capture_output=True,
                check=True,
            )
            self.assertEqual(
                retired["base_sha256"],
                canonical_hash_bytes(baseline.stdout),
            )
        self.assertEqual(1, len(active_states), "active targets are in a mixed state")
        patch_path = PROJECT_ROOT / manifest["patch"]["path"]
        self.assertEqual(
            manifest["patch"]["sha256"],
            canonical_hash_bytes(patch_path.read_bytes()),
        )

        with tempfile.TemporaryDirectory() as temporary:
            temporary_root = Path(temporary)
            for target in manifest["targets"]:
                destination = temporary_root / target["active_path"]
                destination.parent.mkdir(parents=True, exist_ok=True)
                baseline = subprocess.run(
                    [
                        "git",
                        "show",
                        f"{manifest['base_commit']}:{target['active_path']}",
                    ],
                    cwd=PROJECT_ROOT,
                    capture_output=True,
                    check=True,
                )
                self.assertEqual(
                    target["base_sha256"],
                    canonical_hash_bytes(baseline.stdout),
                )
                destination.write_bytes(baseline.stdout)
            for retired in manifest.get("retired_discovery_paths", []):
                destination = temporary_root / retired["path"]
                destination.parent.mkdir(parents=True, exist_ok=True)
                baseline = subprocess.run(
                    [
                        "git",
                        "show",
                        f"{manifest['base_commit']}:{retired['path']}",
                    ],
                    cwd=PROJECT_ROOT,
                    capture_output=True,
                    check=True,
                )
                destination.write_bytes(baseline.stdout)
            shutil.copyfile(patch_path, temporary_root / "patch.diff")
            result = subprocess.run(
                ["git", "apply", "--ignore-space-change", "patch.diff"],
                cwd=temporary_root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            for target in manifest["targets"]:
                self.assertEqual(
                    (PROJECT_ROOT / target["candidate_path"]).read_text(
                        encoding="utf-8"
                    ),
                    (temporary_root / target["active_path"]).read_text(
                        encoding="utf-8"
                    ),
                )
            for retired in manifest.get("retired_discovery_paths", []):
                self.assertFalse((temporary_root / retired["path"]).exists())

    def test_reference_reader_emits_exact_metrics(self):
        payload = "## Execution Rules\n\nalpha\n\n## Output Requirements\n\nbeta"
        rendered = read_reference.output_with_metrics(payload)
        summary = collect_smoke.output_summary(
            f"Exit code: 0\nOutput:\n{rendered}\n"
        )
        self.assertEqual(
            {
                "codepoints": len(payload),
                "h2_sections": 2,
            },
            summary["reference_metrics"],
        )
        self.assertEqual(len(payload), summary["content_codepoints"])
        self.assertEqual(2, summary["h2_sections"])

    def test_reference_reader_prefers_script_source_dir(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            plugin_skill = root / "plugin" / "skills" / "codex-project-workflow"
            plugin_script_dir = plugin_skill / "scripts"
            plugin_refs = plugin_skill / "references"
            plugin_script_dir.mkdir(parents=True)
            plugin_refs.mkdir()
            shutil.copyfile(
                SKILL_DIR / "scripts" / "read_reference.py",
                plugin_script_dir / "read_reference.py",
            )
            (plugin_refs / "governance.md").write_text(
                "# Governance\n\n## Execution Rules\n\nplugin-source\n",
                encoding="utf-8",
            )

            repo_like = (
                root
                / "workspace"
                / ".agents"
                / "skills"
                / "codex-project-workflow"
                / "references"
            )
            repo_like.mkdir(parents=True)
            (repo_like / "governance.md").write_text(
                "# Governance\n\n## Execution Rules\n\nrepo-fallback\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(plugin_script_dir / "read_reference.py"),
                    "governance",
                    "Execution Rules",
                ],
                cwd=root / "workspace",
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("plugin-source", result.stdout)
            self.assertNotIn("repo-fallback", result.stdout)

    def test_output_summary_sums_multiple_reference_metrics(self):
        first = "## Execution Rules\n\nalpha"
        second = "## Output Requirements\n\nbeta"
        output = (
            "Exit code: 0\nOutput:\n"
            f"{read_reference.output_with_metrics(first)}\n"
            f"{read_reference.output_with_metrics(second)}\n"
        )
        summary = collect_smoke.output_summary(output)
        self.assertEqual(
            {
                "codepoints": len(first) + len(second),
                "h2_sections": 2,
            },
            summary["reference_metrics"],
        )
        self.assertEqual(len(first) + len(second), summary["content_codepoints"])
        self.assertEqual(2, summary["h2_sections"])

    def test_output_summary_decodes_unified_exec_text_blocks(self):
        payload = "## Execution Rules\n\nalpha"
        wrapped = json.dumps(
            [
                {
                    "type": "input_text",
                    "text": read_reference.output_with_metrics(payload),
                }
            ]
        )
        summary = collect_smoke.output_summary(wrapped)
        self.assertEqual(len(payload), summary["content_codepoints"])
        self.assertEqual(1, summary["h2_sections"])

    def test_output_summary_extracts_emitted_skill_metrics(self):
        output = (
            "Script completed\nOutput:\n\n"
            "---\n"
            "name: codex-project-workflow\n"
            "description: fixture description\n"
            "---\n\n"
            "# Codex Project Workflow\n"
        )
        summary = collect_smoke.output_summary(output)
        self.assertEqual(
            {"description_chars": 19, "body_chars": 25},
            summary["skill_metrics"],
        )

    def test_overage_line_is_machine_readable_and_unquoted(self):
        parsed = collect_smoke.parse_reported_overage(
            "added_codepoints=1456, added_sections=5, "
            "reason=mandatory gates, unknown_resolved=entry and approval"
        )
        self.assertEqual(1456, parsed["added_codepoints"])
        self.assertEqual(5, parsed["added_sections"])
        self.assertIn("mandatory gates", parsed["reason"])
        self.assertIn("entry and approval", parsed["unknown_resolved"])

        quoted = collect_smoke.parse_reported_overage(
            "`added_codepoints`: `1456`, `added_sections`: `5`"
        )
        self.assertNotIn("added_codepoints", quoted)
        self.assertNotIn("added_sections", quoted)

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
        self.assertEqual([], discovered)

    def test_e23_approval_package_bindings_and_patch_contents(self):
        def committed_bytes(path):
            relative = path.relative_to(PROJECT_ROOT).as_posix()
            return subprocess.run(
                ["git", "show", f"HEAD:{relative}"],
                cwd=PROJECT_ROOT,
                capture_output=True,
                check=True,
            ).stdout

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
                base_bytes = committed_bytes(base)
                patch_bytes = committed_bytes(patch)
                candidate_bytes = committed_bytes(candidate)
                evaluation_bytes = committed_bytes(evaluation)

                base_bound = hashlib.sha256(base_bytes).hexdigest() == approval["base_hash"]
                patch_bound = hashlib.sha256(patch_bytes).hexdigest() == approval["patch_hash"]
                evaluation_bound = (
                    hashlib.sha256(evaluation_bytes).hexdigest()
                    == approval["evaluation_hash"]
                )

                with tempfile.TemporaryDirectory() as temporary:
                    temporary_root = Path(temporary)
                    (temporary_root / "active").mkdir()
                    (temporary_root / "candidate").mkdir()
                    (temporary_root / "active" / "SKILL.baseline.md").write_bytes(
                        base_bytes
                    )
                    (
                        temporary_root / "candidate" / "SKILL.candidate.md"
                    ).write_bytes(base_bytes)
                    (temporary_root / "patch.diff").write_bytes(patch_bytes)
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
                        (
                            temporary_root / "candidate" / "SKILL.candidate.md"
                        ).read_text(encoding="utf-8").replace("\r\n", "\n")
                        == candidate_bytes.decode("utf-8").replace("\r\n", "\n")
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
                    "cmd": (
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

    def test_smoke_collector_traces_combined_reference_reader_command(self):
        calls = [
            {
                "call_id": "combined",
                "name": "shell_command",
                "arguments": {
                    "command": (
                        "python .agents/skills/codex-project-workflow/scripts/"
                        "read_reference.py research \"Execution Rules\" "
                        "\"Output Requirements\"; "
                        "python .agents/skills/codex-project-workflow/scripts/"
                        "read_reference.py governance \"Execution Rules\" "
                        "\"Output Requirements\"; "
                        "python .agents/skills/codex-project-workflow/scripts/"
                        "read_reference.py verification \"Execution Rules\" "
                        "\"Output Requirements\""
                    )
                },
                "output": collect_smoke.output_summary(
                    "Exit code: 0\nOutput:\n"
                    "## Execution Rules\n\nresearch\n\n"
                    "<!-- codex-reference-metrics "
                    "codepoints=1205 h2_sections=2 -->\n"
                    "## Execution Rules\n\ngovernance\n\n"
                    "<!-- codex-reference-metrics "
                    "codepoints=2483 h2_sections=2 -->\n"
                    "## Execution Rules\n\nverification\n\n"
                    "<!-- codex-reference-metrics "
                    "codepoints=2239 h2_sections=2 -->\n"
                ),
            }
        ]
        trace = collect_smoke.reference_call_trace(calls, SKILL_DIR)
        self.assertEqual(["combined"], trace["reference_section_read_calls"])
        self.assertEqual(6, trace["reference_h2_sections"])
        self.assertEqual(5927, trace["reference_loaded_chars"])
        self.assertEqual(
            ["governance.md", "research.md", "verification.md"],
            trace["reference_files"],
        )

    def test_smoke_collector_traces_unified_exec_reference_loop(self):
        calls = [
            {
                "call_id": "unified",
                "name": "exec",
                "arguments": (
                    'const names = ["research", "governance", "verification"];\n'
                    "const results = await Promise.all(names.map(name => "
                    "tools.exec_command({cmd: `python read_reference.py ${name} "
                    '"Execution Rules" "Output Requirements"`})));'
                ),
                "output": collect_smoke.output_summary(
                    "## Execution Rules\n\nresearch\n\n"
                    "<!-- codex-reference-metrics "
                    "codepoints=1205 h2_sections=2 -->\n"
                    "## Execution Rules\n\ngovernance\n\n"
                    "<!-- codex-reference-metrics "
                    "codepoints=2484 h2_sections=2 -->\n"
                    "## Execution Rules\n\nverification\n\n"
                    "<!-- codex-reference-metrics "
                    "codepoints=2239 h2_sections=2 -->\n"
                ),
            }
        ]
        trace = collect_smoke.reference_call_trace(calls, SKILL_DIR)
        self.assertEqual(["unified"], trace["reference_section_read_calls"])
        self.assertEqual(6, trace["reference_h2_sections"])
        self.assertEqual(5928, trace["reference_loaded_chars"])
        self.assertEqual(
            ["governance.md", "research.md", "verification.md"],
            trace["reference_files"],
        )

    def test_smoke_collector_traces_unified_exec_template_commands(self):
        calls = [
            {
                "call_id": "templates",
                "name": "exec",
                "arguments": (
                    'const base = "scripts\\\\read_reference.py";\n'
                    "const cmds = [\n"
                    '  `python "${base}" governance "Execution Rules" '
                    '"Output Requirements"`,\n'
                    '  `python "${base}" verification "Execution Rules" '
                    '"Output Requirements"`\n'
                    "];"
                ),
                "output": collect_smoke.output_summary(
                    "## Execution Rules\n\ngovernance\n\n"
                    "<!-- codex-reference-metrics "
                    "codepoints=2484 h2_sections=2 -->\n"
                    "## Execution Rules\n\nverification\n\n"
                    "<!-- codex-reference-metrics "
                    "codepoints=2239 h2_sections=2 -->\n"
                ),
            }
        ]
        trace = collect_smoke.reference_call_trace(calls, SKILL_DIR)
        self.assertEqual(["templates"], trace["reference_section_read_calls"])
        self.assertEqual(4, trace["reference_h2_sections"])
        self.assertEqual(4723, trace["reference_loaded_chars"])
        self.assertEqual(
            ["governance.md", "verification.md"],
            trace["reference_files"],
        )

    def test_smoke_collector_counts_failed_emitted_reference_content(self):
        calls = [
            {
                "call_id": "timed-out",
                "name": "shell_command",
                "arguments": {
                    "command": (
                        "python .agents/skills/codex-project-workflow/"
                        "scripts/read_reference.py verification "
                        "\"Execution Rules\" \"Output Requirements\""
                    )
                },
                "output": collect_smoke.output_summary(
                    "Exit code: 124\nWall time: 10 seconds\nOutput:\n"
                    "## Execution Rules\n\nalpha\n\n"
                    "## Output Requirements\n\nbeta\n"
                ),
            },
        ]
        trace = collect_smoke.reference_call_trace(calls, SKILL_DIR)
        self.assertEqual(["timed-out"], trace["reference_failed_calls"])
        self.assertEqual(["timed-out"], trace["reference_section_read_calls"])
        self.assertEqual(2, trace["reference_h2_sections"])
        self.assertGreater(trace["reference_loaded_chars"], 0)

    def test_smoke_collector_marks_failed_nested_reference_load_incomplete(self):
        calls = [
            {
                "call_id": "nested-failure",
                "name": "exec",
                "arguments": (
                    'const names = ["research", "dependency", "verification"];\n'
                    "const results = await Promise.all(names.map(name => "
                    "tools.shell_command({command: `python read_reference.py ${name} "
                    '"Execution Rules" "Output Requirements"`})));'
                ),
                "output": collect_smoke.output_summary(
                    "Script failed\nOutput:\n\nScript error:\n"
                    "Exit code: 1\nOutput:\nunknown reference: dependency\n"
                ),
            }
        ]
        trace = collect_smoke.reference_call_trace(calls, SKILL_DIR)
        self.assertFalse(trace["reference_metric_measurement_complete"])
        self.assertEqual(
            ["nested-failure"],
            trace["unmeasured_reference_calls"],
        )

        fixture = (
            SKILL_DIR
            / "evals"
            / "full"
            / "cases"
            / "E35"
            / "workspace"
            / "four_hard_triggers"
        )
        overage = collect_smoke.context_overage_trace(
            fixture,
            trace,
            "added_codepoints=0, added_sections=0, "
            "reason=visible output only, unknown_resolved=none",
        )
        self.assertFalse(overage["measurement_complete"])
        self.assertIsNone(overage["actual_loaded_codepoints"])
        self.assertIsNone(overage["actual_h2_sections"])
        self.assertIsNone(overage["expected_added_codepoints"])
        self.assertIsNone(overage["expected_added_sections"])
        self.assertFalse(overage["values_accurate"])

    def test_smoke_collector_counts_visible_direct_helper_failure_as_zero(self):
        calls = [
            {
                "call_id": "direct-failure",
                "name": "command_execution",
                "arguments": (
                    "python C:/plugin/scripts/read_reference.py governance "
                    '"Execution Rules" "Output Requirements"'
                ),
                "output": collect_smoke.output_summary(
                    "Exit code: 1\nOutput:\nunknown reference: dependency\n"
                ),
            }
        ]
        trace = collect_smoke.reference_call_trace(calls, SKILL_DIR)
        self.assertTrue(trace["reference_metric_measurement_complete"])
        self.assertEqual([], trace["unmeasured_reference_calls"])
        self.assertEqual(["direct-failure"], trace["reference_failed_calls"])
        self.assertEqual(0, trace["reference_loaded_chars"])
        self.assertEqual(0, trace["reference_h2_sections"])

    def test_smoke_collector_ignores_null_token_info(self):
        self.assertIsNone(
            collect_smoke.token_usage_from_event(
                {"type": "token_count", "info": None}
            )
        )
        self.assertEqual(
            {"total_tokens": 42},
            collect_smoke.token_usage_from_event(
                {
                    "type": "token_count",
                    "info": {"total_token_usage": {"total_tokens": 42}},
                }
            ),
        )

    def test_full_eval_prompt_hides_evaluator_oracles(self):
        boundary = setup_full_eval.BLIND_EVAL_BOUNDARY
        self.assertIn("Do not inspect parent or peer threads", boundary)
        self.assertIn("If the task independently activates a skill", boundary)
        self.assertIn("evaluator definitions", boundary)
        self.assertNotIn("workspace, the active skill entry", boundary)
        self.assertNotIn("expected_changed_files", boundary)

    def test_full_eval_prompt_integrity_rejects_answer_hints(self):
        setup = {
            "prompt": "Original fixture prompt.",
            "scripted_user_replies": ["Approved."],
        }
        clean = collect_full_eval.prompt_integrity(
            [
                "<codex_delegation><input>Original fixture prompt.</input>"
                "</codex_delegation>",
                "<codex_delegation><input>Approved.</input>"
                "</codex_delegation>",
            ],
            setup,
        )
        self.assertTrue(clean["valid"])
        nested = collect_full_eval.prompt_integrity(
            [
                "<codex_delegation><input>&lt;codex_delegation&gt;"
                "&lt;input&gt;Original fixture prompt.&lt;/input&gt;"
                "&lt;/codex_delegation&gt;</input></codex_delegation>",
                "<codex_delegation><input>&lt;codex_delegation&gt;"
                "&lt;input&gt;Approved.&lt;/input&gt;"
                "&lt;/codex_delegation&gt;</input></codex_delegation>",
            ],
            setup,
        )
        self.assertTrue(nested["valid"])
        direct = collect_full_eval.prompt_integrity(
            ["Original fixture prompt.", "Approved."],
            setup,
        )
        self.assertTrue(direct["valid"])
        contaminated = collect_full_eval.prompt_integrity(
            [
                "<codex_delegation><input>Original fixture prompt.</input>"
                "</codex_delegation>",
                "<codex_delegation><input>Inspect formatting ownership.</input>"
                "</codex_delegation>",
            ],
            setup,
        )
        self.assertFalse(contaminated["valid"])

    def test_skill_description_supports_plugin_qualified_entry(self):
        description = collect_smoke.extract_skill_description(
            "- codex-project-workflow:codex-project-workflow: "
            "Never activate for simple questions. "
            "(file: C:/cache/codex-project-workflow/SKILL.md)"
        )
        self.assertEqual(
            "Never activate for simple questions.",
            description,
        )

    def test_collector_ignores_injected_user_context(self):
        self.assertTrue(
            collect_smoke.is_injected_user_context(
                "<recommended_plugins>...</recommended_plugins>\n"
                "<environment_context>...</environment_context>"
            )
        )
        self.assertFalse(
            collect_smoke.is_injected_user_context(
                "Blind evaluation boundary: use only the supplied workspace."
            )
        )

    def test_agent_no_decision_remains_proposed(self):
        clean = collect_smoke.agent_authorization_trace(
            [
                "<codex_delegation><input>No decision is given on the "
                "proposed agents. Keep the proposal pending.</input>"
                "</codex_delegation>"
            ],
            ["The agent proposal remains `proposed`; main-agent work continues."],
            "",
            [],
        )
        self.assertEqual("proposed", clean["pending_state"])
        alternate = collect_smoke.agent_authorization_trace(
            [
                "<codex_delegation><input>No decision is given on the "
                "proposed agents. Keep the proposal pending.</input>"
                "</codex_delegation>"
            ],
            ["The proposed agents remain pending and were not started."],
            "",
            [],
        )
        self.assertEqual("proposed", alternate["pending_state"])
        concise = collect_smoke.agent_authorization_trace(
            [
                "<codex_delegation><input>No decision is given on the "
                "proposed agents. Keep the proposal pending.</input>"
                "</codex_delegation>"
            ],
            ["Agents remain pending and were not started."],
            "",
            [],
        )
        self.assertEqual("proposed", concise["pending_state"])
        not_started = collect_smoke.agent_authorization_trace(
            [
                "<codex_delegation><input>No decision is given on the "
                "proposed agents. Keep the proposal pending.</input>"
                "</codex_delegation>"
            ],
            ["Completed the main-agent work only. The proposed agents were not started."],
            "",
            [],
        )
        self.assertEqual("proposed", not_started["pending_state"])
        fallback = collect_smoke.agent_authorization_trace(
            [
                "<codex_delegation><input>No decision is given on the "
                "proposed agents. Keep the proposal pending.</input>"
                "</codex_delegation>"
            ],
            ["I will keep the work single-agent because agents were not approved."],
            "",
            [],
        )
        self.assertEqual("invalid", fallback["pending_state"])

    def test_collector_detects_evaluator_oracle_access(self):
        project = str(PROJECT_ROOT)
        calls = [
            {
                "call_id": "parent",
                "name": "read_thread",
                "arguments": {"threadId": "parent-thread"},
            },
            {
                "call_id": "case",
                "name": "shell_command",
                "arguments": {
                    "command": (
                        "Get-Content .agents/skills/codex-project-workflow/"
                        "evals/full/cases/E02/case.json"
                    ),
                    "workdir": project,
                },
            },
            {
                "call_id": "scan",
                "name": "shell_command",
                "arguments": {
                    "command": "rg -n 'E02' .agents docs",
                    "workdir": project,
                },
            },
        ]
        trace = collect_smoke.evaluation_isolation_trace(
            calls,
            "evaluated-thread",
            project,
        )
        self.assertEqual(["parent"], trace["cross_thread_read_calls"])
        self.assertEqual(["case"], trace["evaluator_artifact_calls"])
        self.assertEqual(["scan"], trace["host_project_scan_calls"])
        self.assertTrue(trace["oracle_access_detected"])

    def test_collector_detects_unified_exec_host_scan(self):
        project = str(PROJECT_ROOT)
        escaped = project.replace("\\", "\\\\")
        calls = [
            {
                "call_id": "unified-scan",
                "name": "exec",
                "arguments": (
                    f'const wd = "{escaped}";\n'
                    'const r = await tools.exec_command({cmd: "rg -n TODO .agents docs", '
                    "workdir: wd});\ntext(r.output);"
                ),
            }
        ]
        trace = collect_smoke.evaluation_isolation_trace(
            calls,
            "evaluated-thread",
            project,
        )
        self.assertEqual(["unified-scan"], trace["host_project_scan_calls"])
        self.assertTrue(trace["oracle_access_detected"])

    def test_collector_allows_unified_exec_fixture_scan(self):
        project = str(PROJECT_ROOT)
        fixture = PROJECT_ROOT / ".agents" / "skills" / "fixture"
        escaped = str(fixture).replace("\\", "\\\\")
        calls = [
            {
                "call_id": "fixture-scan",
                "name": "exec",
                "arguments": (
                    f'const target = "{escaped}";\n'
                    'const r = await tools.exec_command({cmd: "rg --files .", '
                    "workdir: target});\ntext(r.output);"
                ),
            }
        ]
        trace = collect_smoke.evaluation_isolation_trace(
            calls,
            "evaluated-thread",
            project,
            str(fixture),
        )
        self.assertEqual([], trace["host_project_scan_calls"])
        self.assertFalse(trace["oracle_access_detected"])

    def test_collector_detects_evaluation_control_artifacts(self):
        calls = [
            {
                "call_id": "state",
                "name": "shell_command",
                "arguments": {"command": "Get-Content setup-state.json"},
            },
            {
                "call_id": "sessions",
                "name": "shell_command",
                "arguments": {
                    "command": "rg E35 C:/Users/test/.codex/sessions"
                },
            },
            {
                "call_id": "rollout",
                "name": "shell_command",
                "arguments": {"command": "Get-Content rollout-test.jsonl"},
            },
        ]
        trace = collect_smoke.evaluation_isolation_trace(
            calls,
            "evaluated-thread",
            str(PROJECT_ROOT),
        )
        self.assertEqual(
            ["state", "sessions", "rollout"],
            trace["evaluator_artifact_calls"],
        )
        self.assertTrue(trace["oracle_access_detected"])

    def test_collector_allows_skill_and_reference_reads(self):
        project = str(PROJECT_ROOT)
        calls = [
            {
                "call_id": "skill",
                "name": "shell_command",
                "arguments": {
                    "command": (
                        "Get-Content -Raw .agents/skills/"
                        "codex-project-workflow/SKILL.md"
                    ),
                    "workdir": project,
                },
            },
            {
                "call_id": "reference",
                "name": "shell_command",
                "arguments": {
                    "command": (
                        "python .agents/skills/codex-project-workflow/"
                        "scripts/read_reference.py verification "
                        "\"Execution Rules\" \"Output Requirements\""
                    ),
                    "workdir": project,
                },
            },
        ]
        trace = collect_smoke.evaluation_isolation_trace(
            calls,
            "evaluated-thread",
            project,
        )
        self.assertFalse(trace["oracle_access_detected"])

    def test_collector_allows_supplied_fixture_under_evals_run_path(self):
        project = str(PROJECT_ROOT)
        fixture = (
            PROJECT_ROOT
            / ".agents"
            / "skills"
            / "codex-project-workflow"
            / "evals"
            / "full"
            / "runs"
            / "RUN-1"
            / "workspaces"
            / "E35"
            / "four_hard_triggers"
        )
        calls = [
            {
                "call_id": "fixture",
                "name": "exec",
                "arguments": (
                    f'const ws = "{str(fixture).replace(chr(92), chr(92) * 2)}"; '
                    "const r = await tools.exec_command({"
                    "cmd: `Get-Content -Raw ${ws}\\task.json`, workdir: ws});"
                ),
            }
        ]
        trace = collect_smoke.evaluation_isolation_trace(
            calls,
            "evaluated-thread",
            project,
            fixture,
        )
        self.assertFalse(trace["oracle_access_detected"])

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

    def test_full_migration_fixture_expects_prewrite_contract(self):
        case = json.loads(
            (
                SKILL_DIR
                / "evals"
                / "full"
                / "cases"
                / "E32"
                / "case.json"
            ).read_text(encoding="utf-8")
        )
        variant = next(
            item
            for item in case["variants"]
            if item["id"] == "full_high_risk_migration"
        )
        self.assertIn(
            "docs/IMPLEMENTATION_CONTRACT.md",
            variant["expected"]["changed_files"],
        )

    def test_e35_fixture_has_bounded_page_open_approval(self):
        case = json.loads(
            (
                SKILL_DIR
                / "evals"
                / "full"
                / "cases"
                / "E35"
                / "case.json"
            ).read_text(encoding="utf-8")
        )
        variant = next(
            item for item in case["variants"] if item["id"] == "four_hard_triggers"
        )
        replies = variant["scripted_user_replies"]
        self.assertEqual(4, len(replies))
        page_open = next(
            item for item in replies if "page-open scope" in item["when"]
        )
        self.assertIn("exact candidate public source URLs", page_open["when"])
        self.assertIn("only the exact displayed public read-only URLs", page_open["reply"])
        for boundary in (
            "Do not follow links",
            "change domains",
            "submit forms",
            "send internal identifiers",
        ):
            self.assertIn(boundary, page_open["reply"])

    def test_external_workspace_fixtures_expose_their_paths(self):
        for case_id in ("E12", "E16", "E26"):
            case = json.loads(
                (
                    SKILL_DIR
                    / "evals"
                    / "full"
                    / "cases"
                    / case_id
                    / "case.json"
                ).read_text(encoding="utf-8")
            )
            for variant in case["variants"]:
                self.assertIn(
                    "{workspace}",
                    variant["prompt"],
                    f"{case_id}:{variant['id']} omits its workspace",
                )
                if case_id == "E12":
                    self.assertIn(
                        "{workspace}/scenarios",
                        variant["prompt"],
                        f"{case_id}:{variant['id']} omits its scenario root",
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

    def test_full_eval_targeted_selection_supports_multiple_variants(self):
        self.assertEqual(
            [
                ("E26", "product_path"),
                ("E26", "entry_bypass"),
                ("E32", None),
            ],
            setup_full_eval.targeted_selections(
                ["E26", "E32"],
                {
                    "E26": ["product_path", "entry_bypass"],
                },
            ),
        )

    def test_full_setup_accepts_isolated_source_commit(self):
        with tempfile.TemporaryDirectory() as temporary:
            state_path = setup_full_eval.setup(
                ["E02"],
                Path(temporary) / "workspaces",
                source_commit="candidate-commit",
            )
            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual("candidate-commit", state["source_commit"])

    def test_full_setup_requires_source_commit(self):
        with tempfile.TemporaryDirectory() as temporary:
            output_root = Path(temporary) / "workspaces"
            with self.assertRaisesRegex(ValueError, "source_commit is required"):
                setup_full_eval.setup(
                    ["E02"],
                    output_root,
                    source_commit=None,
                )
            self.assertFalse(output_root.exists())

    def test_full_setup_rejects_skill_name_in_negative_control_path(self):
        with self.assertRaisesRegex(
            ValueError,
            "negative control workspace path must not name",
        ):
            setup_full_eval.validate_negative_control_path(
                "negative_quick",
                Path("sandbox") / "codex-project-workflow" / "negative_quick",
            )
        setup_full_eval.validate_negative_control_path(
            "negative_quick",
            Path("sandbox") / "workflow-eval" / "negative_quick",
        )

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

    def test_full_eval_manifest_provenance_is_relative_and_hashed(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_root = Path(temporary) / "run"
            output_dir = run_root / "results"
            output_dir.mkdir(parents=True)
            manifest_path = run_root / "manifest.json"
            manifest_path.write_text('{"run_id":"RUN-1"}\n', encoding="utf-8")
            provenance = collect_full_eval.manifest_provenance(
                manifest_path,
                output_dir,
            )
            self.assertEqual("../manifest.json", provenance["path"])
            self.assertEqual(
                collect_smoke.sha256(manifest_path),
                provenance["sha256"],
            )

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

    def test_full_result_runtime_follows_manifest(self):
        manifest = {
            "model": "gpt-5.6-sol",
            "reasoning_effort": "ultra",
            "runs": [{"case_id": "E32", "variant_id": "negative_quick"}],
        }
        result = {
            "case_id": "E32",
            "variant_id": "negative_quick",
            "model": "gpt-5.6-sol",
            "reasoning_effort": "ultra",
        }
        validate_full_results.validate_runtime(result, manifest)
        for field, value, message in (
            ("model", "gpt-5.5", "wrong model"),
            ("reasoning_effort", "medium", "wrong reasoning effort"),
        ):
            with self.subTest(field=field):
                changed = dict(result)
                changed[field] = value
                with self.assertRaisesRegex(ValueError, message):
                    validate_full_results.validate_runtime(changed, manifest)

    def test_full_result_resolves_relative_and_legacy_manifest(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_root = Path(temporary) / "run"
            results_dir = run_root / "results"
            results_dir.mkdir(parents=True)
            manifest_path = run_root / "manifest.json"
            manifest_path.write_text(
                json.dumps({"run_id": "RUN-1", "runs": []}) + "\n",
                encoding="utf-8",
            )
            summary_path = results_dir / "summary.json"
            relative = {
                "run_id": "RUN-1",
                "source_manifest": "../manifest.json",
                "source_manifest_sha256": collect_smoke.sha256(manifest_path),
            }
            resolved, manifest = validate_full_results.resolve_source_manifest(
                summary_path,
                relative,
            )
            self.assertEqual(manifest_path.resolve(), resolved)
            self.assertEqual("RUN-1", manifest["run_id"])

            legacy = dict(relative)
            legacy.pop("source_manifest_sha256")
            legacy["source_manifest"] = "Z:/moved/run/manifest.json"
            resolved, _ = validate_full_results.resolve_source_manifest(
                summary_path,
                legacy,
            )
            self.assertEqual(manifest_path.resolve(), resolved)

            mismatched_run = dict(relative, run_id="RUN-2")
            with self.assertRaisesRegex(ValueError, "run_id"):
                validate_full_results.resolve_source_manifest(
                    summary_path,
                    mismatched_run,
                )
            mismatched_hash = dict(relative, source_manifest_sha256="0" * 64)
            with self.assertRaisesRegex(ValueError, "SHA-256"):
                validate_full_results.resolve_source_manifest(
                    summary_path,
                    mismatched_hash,
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

    def test_full_result_oracle_access_requires_hard_failure(self):
        validate_full_results.validate_evaluation_isolation(
            {"oracle_access_detected": True},
            ["evaluator_oracle_access"],
        )
        with self.assertRaisesRegex(
            ValueError,
            "must be recorded as evaluator_oracle_access",
        ):
            validate_full_results.validate_evaluation_isolation(
                {"oracle_access_detected": True},
                [],
            )
        with self.assertRaisesRegex(
            ValueError,
            "recorded without detected oracle access",
        ):
            validate_full_results.validate_evaluation_isolation(
                {"oracle_access_detected": False},
                ["evaluator_oracle_access"],
            )

    def test_full_result_prompt_contamination_requires_hard_failure(self):
        validate_full_results.validate_prompt_integrity(
            {"valid": False},
            ["evaluation_prompt_contamination"],
        )
        with self.assertRaisesRegex(
            ValueError,
            "must be recorded as evaluation_prompt_contamination",
        ):
            validate_full_results.validate_prompt_integrity(
                {"valid": False},
                [],
            )

    def test_full_result_overage_assertions_follow_machine_trace(self):
        result = {
            "context_overage": {
                "fields_complete": True,
                "values_accurate": False,
            }
        }
        assertions = {
            "hard_trigger_overage.fields": {
                "passed": True,
                "evidence": "all fields present",
            },
            "hard_trigger_overage.values_accurate": {
                "passed": False,
                "evidence": "values differ",
            },
        }
        validate_full_results.validate_machine_assertions(
            result,
            assertions,
        )
        assertions["hard_trigger_overage.values_accurate"]["passed"] = True
        with self.assertRaisesRegex(
            ValueError,
            "assessment disagrees with machine overage trace",
        ):
            validate_full_results.validate_machine_assertions(
                result,
                assertions,
            )

    def test_full_result_incomplete_context_measurement_cannot_pass(self):
        incomplete = {
            "measurement_complete": False,
            "actual_loaded_codepoints": None,
            "actual_h2_sections": None,
            "expected_added_codepoints": None,
            "expected_added_sections": None,
            "fields_complete": True,
            "values_accurate": False,
        }
        validate_full_results.validate_context_measurement(
            incomplete,
            ["context_measurement_incomplete"],
        )
        with self.assertRaisesRegex(
            ValueError,
            "must be recorded as context_measurement_incomplete",
        ):
            validate_full_results.validate_context_measurement(incomplete, [])

        guessed = dict(incomplete, actual_loaded_codepoints=2484)
        with self.assertRaisesRegex(
            ValueError,
            "must not guess actual or expected values",
        ):
            validate_full_results.validate_context_measurement(
                guessed,
                ["context_measurement_incomplete"],
            )

        result = {"context_overage": incomplete}
        assertions = {
            "budget_overage.values_accurate": {
                "passed": False,
                "evidence": "nested protocol output was not fully measurable",
            }
        }
        validate_full_results.validate_machine_assertions(result, assertions)
        assertions["budget_overage.values_accurate"]["passed"] = True
        with self.assertRaisesRegex(
            ValueError,
            "assessment disagrees with machine overage trace",
        ):
            validate_full_results.validate_machine_assertions(result, assertions)

    def test_full_result_context_budget_assertions_follow_machine_trace(self):
        result = {
            "context_trace": {
                "project_skill_listed": True,
                "project_skill_description_chars": 743,
                "skill_body_loaded_chars": 1483,
                "reference_loaded_chars": 4723,
                "reference_h2_sections": 4,
                "governance_read_calls": [],
            },
            "context_overage": None,
            "agent_authorization": None,
        }
        assertions = {
            "context_trace.verifiable": {
                "passed": True,
                "evidence": "trace fields are present",
            },
            "all_fixtures.skill_description_codepoints": {
                "passed": True,
                "evidence": "743 <= 800",
            },
            "explicit_quick_standard_full.core_body_codepoints": {
                "passed": True,
                "evidence": "1483 <= 1500",
            },
            "standard.reference_codepoints": {
                "passed": False,
                "evidence": "4723 > 2500",
            },
            "standard.reference_h2_sections": {
                "passed": False,
                "evidence": "4 > 2",
            },
            "governance_corpus.bulk_loaded": {
                "passed": True,
                "evidence": "no corpus reads",
            },
        }
        validate_full_results.validate_machine_assertions(result, assertions)
        assertions["standard.reference_codepoints"]["passed"] = True
        with self.assertRaisesRegex(
            ValueError,
            "assessment disagrees with machine context trace",
        ):
            validate_full_results.validate_machine_assertions(result, assertions)

        negative = dict(result)
        negative["context_trace"] = dict(result["context_trace"])
        negative["context_trace"]["reference_loaded_chars"] = 2239
        negative_assertions = {
            "negative_quick.body_and_reference_codepoints": {
                "passed": False,
                "evidence": "body and reference were loaded",
            }
        }
        validate_full_results.validate_machine_assertions(
            negative,
            negative_assertions,
        )

    def test_full_result_agent_state_follows_machine_trace(self):
        result = {
            "context_overage": None,
            "agent_authorization": {"pending_state": "invalid"},
        }
        assertions = {
            "multi_agent.pending_state": {
                "passed": False,
                "evidence": "fallback selected",
            }
        }
        validate_full_results.validate_machine_assertions(
            result,
            assertions,
        )
        assertions["multi_agent.pending_state"]["passed"] = True
        with self.assertRaisesRegex(
            ValueError,
            "assessment disagrees with machine authorization trace",
        ):
            validate_full_results.validate_machine_assertions(
                result,
                assertions,
            )

    def test_targeted_regression_expectations_follow_selected_runs(self):
        with tempfile.TemporaryDirectory() as temporary:
            manifest_path = Path(temporary) / "manifest.json"
            manifest_path.write_text(
                json.dumps(
                    {
                        "evaluation_scope": "targeted_regression",
                        "runs": [
                            {"case_id": "E02", "variant_id": "download"},
                            {"case_id": "E32", "variant_id": "nested_h3_counting"},
                        ],
                    }
                ),
                encoding="utf-8",
            )
            summary = {
                "source_manifest": str(manifest_path),
                "results": [
                    {
                        "case_id": "E02",
                        "variant_id": "download",
                        "expected_assertion_subjects": ["download.checks"],
                    },
                    {
                        "case_id": "E32",
                        "variant_id": "nested_h3_counting",
                        "expected_assertion_subjects": ["h2.count"],
                    },
                ],
            }
            scope, cases, subjects = (
                validate_full_results.evaluation_expectations(summary)
            )
            self.assertEqual("targeted_regression", scope)
            self.assertEqual({"E02", "E32"}, cases)
            self.assertEqual({"download.checks"}, subjects["E02"])
            self.assertEqual({"h2.count"}, subjects["E32"])


if __name__ == "__main__":
    unittest.main()
