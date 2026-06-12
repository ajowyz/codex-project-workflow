#!/usr/bin/env python3
import argparse
import json
from pathlib import Path, PurePosixPath

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
EVAL_DIR = SKILL_DIR / "evals"
FULL_DIR = EVAL_DIR / "full"
CASES_DIR = FULL_DIR / "cases"


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path}: {exc}") from exc


def require(condition, message):
    if not condition:
        raise ValueError(message)


def require_keys(record, keys, label):
    missing = sorted(set(keys) - set(record))
    require(not missing, f"{label}: missing keys {missing}")


def safe_relative_path(value, label):
    require(isinstance(value, str) and value.strip(), f"{label}: path required")
    normalized = value.replace("\\", "/")
    path = PurePosixPath(normalized)
    require(not path.is_absolute(), f"{label}: absolute path is forbidden")
    require(".." not in path.parts, f"{label}: parent traversal is forbidden")
    require(path.parts, f"{label}: empty path")
    return Path(*path.parts)


def valid_scripted_reply(reply):
    if isinstance(reply, str):
        return bool(reply.strip())
    if not isinstance(reply, dict) or set(reply) != {"when", "reply"}:
        return False
    return all(
        isinstance(reply[field], str) and reply[field].strip()
        for field in ("when", "reply")
    )


def expected_case_map():
    data = load_json(EVAL_DIR / "behavior_cases.json")
    return {
        case["id"]: {
            "title": case["title"],
            "assertion_subjects": {
                assertion["subject"] for assertion in case["assertions"]
            },
        }
        for case in data["cases"]
    }


def validate_case(case_path, case_id, group_id, schema, expected):
    data = load_json(case_path)
    require_keys(data, schema["case_required"], case_id)
    require(data["format_version"] == schema["format_version"], f"{case_id}: bad format version")
    require(data["case_id"] == case_id, f"{case_id}: case_id mismatch")
    require(data["owner_group"] == group_id, f"{case_id}: owner group mismatch")
    require(isinstance(data["calibration_priority"], bool), f"{case_id}: calibration_priority must be boolean")
    require(isinstance(data["prompt"], str) and data["prompt"].strip(), f"{case_id}: prompt required")

    variants = data["variants"]
    require(isinstance(variants, list) and variants, f"{case_id}: variants required")
    variant_ids = [variant.get("id") for variant in variants]
    require(
        all(isinstance(value, str) and value.strip() for value in variant_ids),
        f"{case_id}: variant IDs must be non-empty strings",
    )
    require(len(variant_ids) == len(set(variant_ids)), f"{case_id}: duplicate variant ID")

    case_dir = case_path.parent.resolve()
    covered_subjects = set()
    for variant in variants:
        label = f"{case_id}.{variant['id']}"
        require_keys(variant, schema["variant_required"], label)
        relative_workspace = safe_relative_path(variant["workspace"], f"{label}.workspace")
        workspace = (case_dir / relative_workspace).resolve()
        require(
            workspace == case_dir or case_dir in workspace.parents,
            f"{label}: workspace escapes case directory",
        )
        require(workspace.is_dir(), f"{label}: workspace directory missing")
        require(
            variant["permissions"] in schema["permission_values"],
            f"{label}: unknown permission value",
        )
        require(
            isinstance(variant["prompt"], str) and variant["prompt"].strip(),
            f"{label}: prompt required",
        )
        replies = variant["scripted_user_replies"]
        require(
            isinstance(replies, list)
            and all(valid_scripted_reply(reply) for reply in replies),
            f"{label}: invalid scripted reply",
        )

        expected_data = variant["expected"]
        require_keys(expected_data, schema["expected_required"], f"{label}.expected")
        for field in (
            "changed_files",
            "forbidden_changes",
            "required_evidence",
            "forbidden_actions",
            "assertion_subjects",
        ):
            values = expected_data[field]
            require(isinstance(values, list), f"{label}.expected.{field}: list required")
            require(
                all(isinstance(value, str) and value.strip() for value in values),
                f"{label}.expected.{field}: values must be strings",
            )

        actual_subjects = set(expected_data["assertion_subjects"])
        require(
            actual_subjects <= expected["assertion_subjects"],
            f"{label}: unknown assertion subjects",
        )
        covered_subjects.update(actual_subjects)
        for changed in expected_data["changed_files"]:
            safe_relative_path(changed, f"{label}.expected.changed_files")
        for forbidden in expected_data["forbidden_changes"]:
            safe_relative_path(forbidden, f"{label}.expected.forbidden_changes")

        forbidden_suffixes = {".exe", ".dll", ".msi", ".so", ".dylib"}
        unsafe_files = [
            path
            for path in workspace.rglob("*")
            if path.is_file() and path.suffix.casefold() in forbidden_suffixes
        ]
        require(not unsafe_files, f"{label}: executable binary fixture is forbidden")

    require(
        covered_subjects == expected["assertion_subjects"],
        f"{case_id}: variant assertion subjects do not cover behavior_cases.json",
    )
    return {
        "variants": len(variants),
        "calibration_priority": data["calibration_priority"],
    }


def validate_manifest(schema, manifest, expected):
    require(schema["schema_type"] == "codex-project-executable-fixture/v1", "bad fixture schema")
    require(schema["format_version"] == "1.0", "bad fixture schema version")
    require(manifest["format_version"] == "1.0", "bad batch manifest version")

    groups = manifest["groups"]
    assigned = []
    owner_by_case = {}
    for group_id, group in groups.items():
        for case_id in group["case_ids"]:
            require(case_id not in owner_by_case, f"duplicate case assignment: {case_id}")
            owner_by_case[case_id] = group_id
            assigned.append(case_id)

    completed = {"E01", "E04", "E06", "E31", "E36"}
    remaining = sorted(set(expected) - completed)
    require(sorted(assigned) == remaining, "batch manifest must assign every remaining case exactly once")

    calibration = set(manifest["calibration_cases"])
    require(
        calibration == {"E02", "E12", "E16", "E19", "E23", "E26", "E32", "E35"},
        "calibration case set changed",
    )
    return assigned, owner_by_case, calibration


def validate(require_complete=True):
    schema = load_json(FULL_DIR / "fixture.schema.json")
    manifest = load_json(FULL_DIR / "batch_manifest.json")
    expected = expected_case_map()
    assigned, owner_by_case, calibration = validate_manifest(
        schema,
        manifest,
        expected,
    )

    results = {}
    missing = []
    for case_id in assigned:
        case_path = CASES_DIR / case_id / "case.json"
        if not case_path.is_file():
            missing.append(case_id)
            continue
        result = validate_case(
            case_path,
            case_id,
            owner_by_case[case_id],
            schema,
            expected[case_id],
        )
        require(
            result["calibration_priority"] == (case_id in calibration),
            f"{case_id}: calibration_priority mismatch",
        )
        results[case_id] = result

    if require_complete:
        require(not missing, f"missing executable fixtures: {missing}")

    return {
        "assigned_cases": len(assigned),
        "validated_cases": len(results),
        "missing_cases": missing,
        "variants": sum(result["variants"] for result in results.values()),
        "calibration_cases": len(calibration),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--allow-missing", action="store_true")
    args = parser.parse_args()
    try:
        summary = validate(require_complete=not args.allow_missing)
    except ValueError as exc:
        print(f"Full evaluation fixtures are invalid: {exc}")
        return 1
    print(
        "Full evaluation fixtures are valid: "
        f"{summary['validated_cases']}/{summary['assigned_cases']} cases, "
        f"{summary['variants']} variants, "
        f"{summary['calibration_cases']} calibration cases."
    )
    if summary["missing_cases"]:
        print("Missing:", ", ".join(summary["missing_cases"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
