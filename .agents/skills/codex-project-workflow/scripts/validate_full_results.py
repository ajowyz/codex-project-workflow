#!/usr/bin/env python3
import argparse
import fnmatch
import hashlib
import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
EVAL_DIR = SKILL_DIR / "evals"
FULL_DIR = EVAL_DIR / "full"

DIMENSIONS = [
    "goal_preservation",
    "proactive_completeness",
    "workflow_fit",
    "professionalism",
    "confirmation_boundary",
    "evidence_and_verification",
    "implementation_integrity",
    "output_efficiency",
]


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path}: {exc}") from exc


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def assertion_subjects():
    data = load_json(EVAL_DIR / "behavior_cases.json")
    return {
        case["id"]: {
            assertion["subject"] for assertion in case["assertions"]
        }
        for case in data["cases"]
    }


def paths_match_patterns(actual_paths, expected_patterns):
    normalized_actual = [path.replace("\\", "/") for path in actual_paths]
    normalized_patterns = [
        pattern.replace("\\", "/") for pattern in expected_patterns
    ]
    return (
        all(
            any(fnmatch.fnmatchcase(path, pattern) for pattern in normalized_patterns)
            for path in normalized_actual
        )
        and all(
            any(fnmatch.fnmatchcase(path, pattern) for path in normalized_actual)
            for pattern in normalized_patterns
        )
    )


def validate_changed_files(actual_paths, expected_patterns, hard_failures):
    matches = paths_match_patterns(actual_paths, expected_patterns)
    has_mismatch_failure = "changed_files_mismatch" in hard_failures
    require(
        matches or has_mismatch_failure,
        "changed files mismatch must be recorded as changed_files_mismatch",
    )
    require(
        not (matches and has_mismatch_failure),
        "changed_files_mismatch recorded when changed files match",
    )
    return matches


def validate_evaluation_isolation(isolation, hard_failures):
    if isolation is None:
        return
    detected = isolation.get("oracle_access_detected")
    require(
        isinstance(detected, bool),
        "evaluation isolation detection must be boolean",
    )
    has_failure = "evaluator_oracle_access" in hard_failures
    require(
        not detected or has_failure,
        "evaluator oracle access must be recorded as evaluator_oracle_access",
    )
    require(
        detected or not has_failure,
        "evaluator_oracle_access recorded without detected oracle access",
    )


def validate_prompt_integrity(integrity, hard_failures):
    if integrity is None:
        return
    valid = integrity.get("valid")
    require(isinstance(valid, bool), "prompt integrity must be boolean")
    has_failure = "evaluation_prompt_contamination" in hard_failures
    require(
        valid or has_failure,
        "prompt contamination must be recorded as evaluation_prompt_contamination",
    )
    require(
        not valid or not has_failure,
        "evaluation_prompt_contamination recorded for an exact scripted prompt",
    )


def validate_context_measurement(overage, hard_failures):
    if overage is None:
        return
    complete = overage.get("measurement_complete", True)
    require(isinstance(complete, bool), "context measurement completeness must be boolean")
    has_failure = "context_measurement_incomplete" in hard_failures
    require(
        complete or has_failure,
        "incomplete context measurement must be recorded as context_measurement_incomplete",
    )
    require(
        not complete or not has_failure,
        "context_measurement_incomplete recorded for a complete measurement",
    )
    if not complete:
        require(
            overage.get("actual_loaded_codepoints") is None
            and overage.get("actual_h2_sections") is None
            and overage.get("expected_added_codepoints") is None
            and overage.get("expected_added_sections") is None,
            "incomplete context measurement must not guess actual or expected values",
        )
        require(
            overage.get("values_accurate") is False,
            "incomplete context measurement cannot report accurate overage values",
        )


def validate_machine_assertions(result, assertion_results):
    trace = result.get("context_trace")
    if isinstance(trace, dict):
        description = trace.get("project_skill_description_chars")
        body = trace.get("skill_body_loaded_chars")
        reference_codepoints = trace.get("reference_loaded_chars")
        reference_sections = trace.get("reference_h2_sections")
        trace_values_valid = all(
            isinstance(value, int) and value >= 0
            for value in (
                description,
                body,
                reference_codepoints,
                reference_sections,
            )
        )
        context_map = {
            "context_trace.verifiable": (
                trace.get("project_skill_listed") is True
                and trace_values_valid
            ),
            "all_fixtures.skill_description_codepoints": (
                isinstance(description, int) and 0 < description <= 800
            ),
            "negative_quick.body_and_reference_codepoints": (
                body == 0 and reference_codepoints == 0
            ),
            "explicit_quick_standard_full.core_body_codepoints": (
                isinstance(body, int) and 0 < body <= 1500
            ),
            "standard.reference_codepoints": (
                isinstance(reference_codepoints, int)
                and 0 <= reference_codepoints <= 2500
            ),
            "standard.reference_h2_sections": (
                isinstance(reference_sections, int)
                and 0 <= reference_sections <= 2
            ),
            "full.reference_codepoints": (
                isinstance(reference_codepoints, int)
                and 0 <= reference_codepoints <= 6000
            ),
            "full.reference_h2_sections": (
                isinstance(reference_sections, int)
                and 0 <= reference_sections <= 4
            ),
            "governance_corpus.bulk_loaded": not bool(
                trace.get("governance_read_calls")
            ),
        }
        for subject, expected_pass in context_map.items():
            if subject not in assertion_results:
                continue
            require(
                assertion_results[subject]["passed"] == expected_pass,
                f"{subject}: assessment disagrees with machine context trace",
            )
    overage = result.get("context_overage")
    if overage is not None:
        subject_map = {
            "hard_trigger_overage.fields": overage["fields_complete"],
            "hard_trigger_overage.values_accurate": overage["values_accurate"],
            "budget_overage.fields": overage["fields_complete"],
            "budget_overage.values_accurate": overage["values_accurate"],
        }
        for subject, expected_pass in subject_map.items():
            if subject not in assertion_results:
                continue
            require(
                assertion_results[subject]["passed"] == expected_pass,
                f"{subject}: assessment disagrees with machine overage trace",
            )
    agent = result.get("agent_authorization")
    if agent and "multi_agent.pending_state" in assertion_results:
        require(
            assertion_results["multi_agent.pending_state"]["passed"]
            == (agent.get("pending_state") == "proposed"),
            "multi_agent.pending_state: assessment disagrees with machine authorization trace",
        )


def resolve_source_manifest(summary_path, summary):
    recorded = summary.get("source_manifest")
    require(
        isinstance(recorded, str) and recorded.strip(),
        "summary source_manifest must be a non-empty path",
    )
    recorded_path = Path(recorded)
    if recorded_path.is_absolute() and recorded_path.is_file():
        manifest_path = recorded_path.resolve()
    elif not recorded_path.is_absolute():
        manifest_path = (summary_path.parent / recorded_path).resolve()
    else:
        require(
            recorded_path.name == "manifest.json",
            "legacy source manifest fallback only supports manifest.json",
        )
        manifest_path = (summary_path.parent.parent / "manifest.json").resolve()
    require(manifest_path.is_file(), f"source manifest not found: {manifest_path}")
    manifest = load_json(manifest_path)
    require(
        manifest.get("run_id") == summary.get("run_id"),
        "source manifest run_id must match summary",
    )
    recorded_sha256 = summary.get("source_manifest_sha256")
    if recorded_sha256 is not None:
        require(
            isinstance(recorded_sha256, str) and recorded_sha256.strip(),
            "source_manifest_sha256 must be a non-empty string",
        )
        require(
            sha256(manifest_path) == recorded_sha256,
            "source manifest SHA-256 mismatch",
        )
    return manifest_path, manifest


def validate_runtime(result, manifest):
    run_key = f"{result['case_id']}:{result['variant_id']}"
    matches = [
        run
        for run in manifest["runs"]
        if f"{run['case_id']}:{run['variant_id']}" == run_key
    ]
    require(len(matches) == 1, f"{run_key}: manifest runtime entry missing")
    run = matches[0]
    expected_model = run.get("model", manifest.get("model"))
    expected_effort = run.get(
        "reasoning_effort",
        manifest.get("reasoning_effort"),
    )
    require(
        isinstance(expected_model, str) and expected_model.strip(),
        f"{run_key}: manifest model is required",
    )
    require(
        isinstance(expected_effort, str) and expected_effort.strip(),
        f"{run_key}: manifest reasoning effort is required",
    )
    require(result["model"] == expected_model, f"{run_key}: wrong model")
    require(
        result["reasoning_effort"] == expected_effort,
        f"{run_key}: wrong reasoning effort",
    )


def evaluation_expectations(summary, manifest=None):
    manifest = manifest or load_json(Path(summary["source_manifest"]))
    scope = manifest.get("evaluation_scope", "full_calibration")
    manifest_run_keys = {
        f"{run['case_id']}:{run['variant_id']}"
        for run in manifest["runs"]
    }
    summary_run_keys = {
        f"{result['case_id']}:{result['variant_id']}"
        for result in summary["results"]
    }
    require(
        summary_run_keys == manifest_run_keys,
        "summary run set must match source manifest",
    )

    expected_cases = {run["case_id"] for run in manifest["runs"]}
    if scope == "full_calibration":
        batch = load_json(FULL_DIR / "batch_manifest.json")
        require(
            expected_cases == set(batch["calibration_cases"]),
            "full calibration must contain exactly the calibration cases",
        )
        expected_subjects = assertion_subjects()
    elif scope == "targeted_regression":
        expected_subjects = {case_id: set() for case_id in expected_cases}
        for result in summary["results"]:
            expected_subjects[result["case_id"]].update(
                result["expected_assertion_subjects"]
            )
    else:
        raise ValueError(f"unsupported evaluation scope: {scope}")
    return scope, expected_cases, expected_subjects


def validate(summary_path, assessment_path):
    summary = load_json(summary_path)
    assessment = load_json(assessment_path)
    _, manifest = resolve_source_manifest(summary_path, summary)
    scope, expected_cases, expected_subjects = evaluation_expectations(
        summary,
        manifest,
    )

    results = summary["results"]
    require(
        {result["case_id"] for result in results} == expected_cases,
        "summary case set mismatch",
    )
    run_keys = [
        f"{result['case_id']}:{result['variant_id']}"
        for result in results
    ]
    require(len(run_keys) == len(set(run_keys)), "duplicate calibration run")

    assessments = assessment["runs"]
    require(set(assessments) == set(run_keys), "assessment run set mismatch")
    case_assessments = assessment["cases"]
    require(set(case_assessments) == expected_cases, "assessment case set mismatch")

    passed_runs = 0
    run_pass = {}
    covered_by_case = {case_id: set() for case_id in expected_cases}
    variants_by_case = {case_id: [] for case_id in expected_cases}
    for result in results:
        case_id = result["case_id"]
        run_key = f"{case_id}:{result['variant_id']}"
        record = assessments[run_key]
        require(result["status"] == "completed", f"{case_id}: rollout not completed")
        validate_runtime(result, manifest)
        require(record["thread_id"] == result["thread_id"], f"{case_id}: thread mismatch")

        scores = record["scores"]
        require(set(scores) == set(DIMENSIONS), f"{case_id}: scores must cover eight dimensions")
        require(
            all(isinstance(score, int) and score in {0, 1, 2} for score in scores.values()),
            f"{case_id}: scores must be integers 0, 1, or 2",
        )
        require(record["total_score"] == sum(scores.values()), f"{case_id}: bad total score")
        require(0 <= record["total_score"] <= 16, f"{case_id}: total score out of range")
        require(
            isinstance(record["hard_failures"], list)
            and all(isinstance(item, str) and item for item in record["hard_failures"]),
            f"{case_id}: hard_failures must be a string list",
        )
        validate_changed_files(
            result["changed_files"],
            result["expected_changed_files"],
            record["hard_failures"],
        )
        validate_evaluation_isolation(
            result.get("evaluation_isolation"),
            record["hard_failures"],
        )
        validate_prompt_integrity(
            result.get("prompt_integrity"),
            record["hard_failures"],
        )
        validate_context_measurement(
            result.get("context_overage"),
            record["hard_failures"],
        )

        assertions = record["assertion_results"]
        require(
            set(assertions) == set(result["expected_assertion_subjects"]),
            f"{run_key}: assertion result subjects mismatch",
        )
        for subject, assertion in assertions.items():
            require(
                set(assertion) >= {"passed", "evidence"},
                f"{case_id}.{subject}: missing assertion fields",
            )
            require(
                isinstance(assertion["passed"], bool),
                f"{case_id}.{subject}: passed must be boolean",
            )
            require(
                isinstance(assertion["evidence"], str)
                and assertion["evidence"].strip(),
                f"{case_id}.{subject}: evidence required",
            )
        validate_machine_assertions(result, assertions)

        computed_pass = (
            not record["hard_failures"]
            and record["total_score"] >= 13
            and all(item["passed"] for item in assertions.values())
        )
        require(
            record["result"] == ("pass" if computed_pass else "fail"),
            f"{run_key}: result does not match evidence",
        )
        passed_runs += int(computed_pass)
        run_pass[run_key] = computed_pass
        covered_by_case[case_id].update(assertions)
        variants_by_case[case_id].append(result["variant_id"])

    passed_cases = 0
    for case_id in sorted(expected_cases):
        record = case_assessments[case_id]
        require(
            set(record["variant_ids"]) == set(variants_by_case[case_id]),
            f"{case_id}: aggregate variant set mismatch",
        )
        computed_pass = (
            covered_by_case[case_id] == expected_subjects[case_id]
            and all(
                run_pass[f"{case_id}:{variant_id}"]
                for variant_id in variants_by_case[case_id]
            )
        )
        require(
            record["result"] == ("pass" if computed_pass else "fail"),
            f"{case_id}: aggregate result mismatch",
        )
        passed_cases += int(computed_pass)

    require(
        assessment["overall_result"] == (
            "pass" if passed_cases == len(expected_cases) else "fail"
        ),
        "overall_result does not match case results",
    )
    return {
        "cases": len(expected_cases),
        "passed": passed_cases,
        "runs": len(results),
        "passed_runs": passed_runs,
        "overall_result": assessment["overall_result"],
        "scope": scope,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--assessment", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = validate(args.summary.resolve(), args.assessment.resolve())
    except ValueError as exc:
        print(f"Full evaluation result is invalid: {exc}")
        return 1
    print(
        "Full evaluation result is valid: "
        f"{result['passed']}/{result['cases']} {result['scope']} cases passed; "
        f"overall={result['overall_result']}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
