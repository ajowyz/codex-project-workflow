#!/usr/bin/env python3
import argparse
import html
import importlib.util
import json
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
FULL_DIR = SKILL_DIR / "evals" / "full"
CASES_DIR = FULL_DIR / "cases"


def load_module(name):
    spec = importlib.util.spec_from_file_location(
        name,
        SCRIPT_DIR / f"{name}.py",
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


collect_smoke = load_module("collect_smoke")
validate_full_fixtures = load_module("validate_full_fixtures")


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_expected(case_id, variant_id):
    case = load_json(CASES_DIR / case_id / "case.json")
    variants = [
        variant for variant in case["variants"] if variant["id"] == variant_id
    ]
    if len(variants) != 1:
        raise ValueError(f"{case_id}: expected one variant {variant_id}")
    return variants[0]["expected"]


def delegation_input(message):
    current = message
    for _ in range(4):
        match = re.search(r"<input>(.*?)</input>", current, flags=re.DOTALL)
        if not match:
            return None if current == message else current.strip()
        current = html.unescape(match.group(1).strip())
    return current.strip()


def delegation_inputs(raw_messages):
    result = []
    for message in raw_messages:
        value = delegation_input(message)
        if value is not None:
            result.append(value)
    return result


def reply_text(reply):
    return reply["reply"] if isinstance(reply, dict) else reply


def prompt_integrity(raw_messages, setup):
    inputs = delegation_inputs(raw_messages)
    expected_prompt = setup["prompt"].strip()
    expected_replies = [
        reply_text(reply).strip()
        for reply in setup["scripted_user_replies"]
    ]
    observed_prompt = inputs[0] if inputs else None
    observed_replies = inputs[1:]
    unexpected = [
        message for message in observed_replies
        if message not in expected_replies
    ]
    return {
        "initial_prompt_matches": observed_prompt == expected_prompt,
        "expected_reply_count": len(expected_replies),
        "observed_scripted_replies": [
            message for message in observed_replies
            if message in expected_replies
        ],
        "unexpected_user_messages": unexpected,
        "valid": (
            observed_prompt == expected_prompt
            and not unexpected
        ),
    }


def collect(manifest_path, sessions_root, setup_state_path, output_dir):
    validate_full_fixtures.validate()
    manifest = load_json(manifest_path)
    setup_state = load_json(setup_state_path)
    setup_by_case = {
        (run["case_id"], run["variant_id"]): run
        for run in setup_state["runs"]
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = output_dir / "runs"
    raw_dir.mkdir(exist_ok=True)

    results = []
    for run in manifest["runs"]:
        key = (run["case_id"], run["variant_id"])
        if key not in setup_by_case:
            raise ValueError(f"missing setup state for {key}")
        setup = setup_by_case[key]
        rollout = collect_smoke.locate_rollout(
            sessions_root,
            run["thread_id"],
        )
        parsed = collect_smoke.parse_rollout(
            rollout,
            run["case_id"],
            "candidate",
            Path(setup["workspace"]),
            setup["before_inventory"],
            run.get("project_root"),
        )
        parsed["variant_id"] = run["variant_id"]
        parsed["permissions"] = setup["permissions"]
        parsed["expected"] = load_expected(*key)
        parsed["prompt_integrity"] = prompt_integrity(
            parsed["raw_user_messages"],
            setup,
        )
        results.append(parsed)
        (raw_dir / f"{run['case_id']}-{run['variant_id']}.json").write_text(
            json.dumps(parsed, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    summary = {
        "format_version": "1.0",
        "run_id": manifest["run_id"],
        "source_manifest": str(manifest_path.resolve()),
        "source_setup_state": str(setup_state_path.resolve()),
        "results": [
            {
                "case_id": result["case_id"],
                "variant_id": result["variant_id"],
                "thread_id": result["thread_id"],
                "status": result["status"],
                "model": result["model"],
                "reasoning_effort": result["reasoning_effort"],
                "duration_ms": result["duration_ms"],
                "time_to_first_token_ms": result["time_to_first_token_ms"],
                "final_response_chars": result["final_response_chars"],
                "total_tokens": (
                    result["token_usage"]["total_tokens"]
                    if result["token_usage"]
                    else None
                ),
                "tool_call_count": len(result["tool_calls"]),
                "changed_files": [
                    change["path"]
                    for change in result["fixture"]["changed_files"]
                ],
                "expected_changed_files": result["expected"]["changed_files"],
                "expected_assertion_subjects": result["expected"]["assertion_subjects"],
                "context_trace": result["context_trace"],
                "evaluation_isolation": result["evaluation_isolation"],
                "context_overage": result["context_overage"],
                "agent_authorization": result["agent_authorization"],
                "prompt_integrity": result["prompt_integrity"],
                "rollout_sha256": result["rollout"]["sha256"],
            }
            for result in results
        ],
    }
    summary_path = output_dir / "summary.json"
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return summary_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--sessions-root", type=Path, required=True)
    parser.add_argument("--setup-state", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    path = collect(
        args.manifest.resolve(),
        args.sessions_root.resolve(),
        args.setup_state.resolve(),
        args.output_dir.resolve(),
    )
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
