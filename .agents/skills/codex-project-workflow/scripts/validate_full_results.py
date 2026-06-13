#!/usr/bin/env python3
import argparse
import fnmatch
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


def validate_machine_assertions(result, assertion_results):
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


def evaluation_expectations(summary):
    manifest = load_json(Path(summary["source_manifest"]))
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
    scope, expected_cases, expected_subjects = evaluation_expectations(summary)

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
        require(result["model"] == "gpt-5.5", f"{case_id}: wrong model")
        require(result["reasoning_effort"] == "medium", f"{case_id}: wrong reasoning effort")
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
