#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
from pathlib import Path

import measure_context

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_RUN_DIR = SKILL_DIR / "evals" / "smoke" / "SMOKE-20260612-01"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def locate_rollout(sessions_root, thread_id):
    matches = list(sessions_root.rglob(f"*{thread_id}.jsonl"))
    if len(matches) != 1:
        raise ValueError(f"expected one rollout for {thread_id}, found {len(matches)}")
    return matches[0]


def parse_jsonl(path):
    records = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: {exc}") from exc
    return records


def extract_input_text(message):
    return "\n".join(
        item.get("text", "")
        for item in message.get("content", [])
        if item.get("type") in {"input_text", "output_text"}
    )


def parse_arguments(raw):
    if not isinstance(raw, str):
        return raw
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def output_summary(output):
    if not isinstance(output, str):
        output = json.dumps(output, ensure_ascii=False, sort_keys=True)
    return {
        "chars": len(output),
        "h2_sections": len(re.findall(r"(?m)^## ", output)),
        "sha256": hashlib.sha256(output.encode("utf-8")).hexdigest(),
        "preview": output[:2000],
    }


def normalize_path_text(value):
    return re.sub(r"/+", "/", value.replace("\\", "/"))


def reference_call_trace(tool_calls, trace_skill_dir):
    reference_paths = sorted((trace_skill_dir / "references").glob("*.md"))
    path_by_stem = {path.stem.casefold(): path for path in reference_paths}
    result = {
        "reference_read_calls": [],
        "reference_list_calls": [],
        "reference_section_read_calls": [],
        "reference_failed_calls": [],
        "reference_files": [],
        "reference_loaded_chars": 0,
        "reference_tool_output_chars": 0,
        "reference_h2_sections": 0,
    }
    loaded_references = set()

    for call in tool_calls:
        arguments = call.get("arguments")
        serialized = normalize_path_text(json.dumps(arguments, ensure_ascii=False))
        output = call.get("output")
        command = arguments.get("command", "") if isinstance(arguments, dict) else ""
        helper_match = re.search(
            r"read_reference\.py[\"']?\s+([A-Za-z0-9_.-]+)",
            command,
            flags=re.IGNORECASE,
        )
        direct_paths = [
            path
            for path in reference_paths
            if normalize_path_text(f"references/{path.name}").lower()
            in serialized.lower()
        ]
        helper_path = (
            path_by_stem.get(Path(helper_match.group(1)).stem.casefold())
            if helper_match
            else None
        )
        if not direct_paths and helper_path is None:
            continue

        result["reference_read_calls"].append(call["call_id"])
        if output:
            result["reference_tool_output_chars"] += output["chars"]
            result["reference_h2_sections"] += output["h2_sections"]
        failed = bool(
            output
            and re.search(r"(?m)^Exit code:\s*[1-9]\d*$", output.get("preview", ""))
        )
        if failed:
            result["reference_failed_calls"].append(call["call_id"])
            continue

        if helper_path is not None:
            loaded_references.add(helper_path)
            sections = measure_context.reference_metrics(helper_path)["sections"]
            selected = [
                section
                for section in sections
                if re.search(
                    rf"(?<!\w){re.escape(section['heading'])}(?!\w)",
                    command,
                    flags=re.IGNORECASE,
                )
            ]
            if output and output["h2_sections"]:
                result["reference_section_read_calls"].append(call["call_id"])
                result["reference_loaded_chars"] += sum(
                    section["chars"] for section in selected
                )
            else:
                result["reference_list_calls"].append(call["call_id"])
            continue

        result["reference_section_read_calls"].append(call["call_id"])
        for path in direct_paths:
            loaded_references.add(path)
            result["reference_loaded_chars"] += len(
                measure_context.normalized_text(path).rstrip("\n")
            )

    result["reference_files"] = [
        path.name for path in sorted(loaded_references)
    ]
    return result


def extract_skill_description(developer_text):
    pattern = re.compile(
        r"^- codex-project-workflow: (.+?) \(file: .+?codex-project-workflow/SKILL\.md\)$",
        flags=re.MULTILINE,
    )
    match = pattern.search(normalize_path_text(developer_text))
    return match.group(1) if match else None


def path_inventory(root):
    if not root.is_dir():
        return {}
    inventory = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        relative = str(path.relative_to(root)).replace("\\", "/")
        inventory[relative] = {"bytes": path.stat().st_size, "sha256": sha256(path)}
    return inventory


def changed_files(before, after):
    names = sorted(set(before) | set(after))
    return [
        {
            "path": name,
            "before": before.get(name),
            "after": after.get(name),
        }
        for name in names
        if before.get(name) != after.get(name)
    ]


def parse_rollout(
    path,
    case_id,
    condition,
    fixture_root,
    before_inventory,
    project_root=None,
):
    records = parse_jsonl(path)
    result = {
        "case_id": case_id,
        "condition": condition,
        "thread_id": None,
        "rollout": {"path": str(path), "sha256": sha256(path)},
        "status": "incomplete",
        "model": None,
        "reasoning_effort": None,
        "started_at": None,
        "completed_at": None,
        "duration_ms": None,
        "time_to_first_token_ms": None,
        "raw_user_messages": [],
        "commentary": [],
        "final_response": "",
        "final_response_chars": 0,
        "tool_calls": [],
        "token_usage": None,
        "context_trace": {
            "project_skill_listed": False,
            "project_skill_description_chars": 0,
            "skill_body_read_calls": [],
            "skill_body_loaded_chars": 0,
            "skill_tool_output_chars": 0,
            "reference_read_calls": [],
            "reference_list_calls": [],
            "reference_section_read_calls": [],
            "reference_failed_calls": [],
            "reference_files": [],
            "reference_loaded_chars": 0,
            "reference_tool_output_chars": 0,
            "reference_h2_sections": 0,
            "governance_read_calls": [],
        },
        "fixture": {
            "root": str(fixture_root),
            "before_inventory": before_inventory,
            "after_inventory": {},
            "changed_files": [],
        },
    }
    developer_texts = []
    output_by_call = {}

    for record in records:
        record_type = record.get("type")
        payload = record.get("payload", {})
        if record_type == "session_meta":
            result["thread_id"] = payload.get("id")
        elif record_type == "turn_context":
            result["model"] = payload.get("model")
            result["reasoning_effort"] = payload.get("effort")
        elif record_type == "event_msg":
            event_type = payload.get("type")
            if event_type == "task_started":
                result["started_at"] = payload.get("started_at")
            elif event_type == "task_complete":
                result["status"] = "completed"
                result["completed_at"] = payload.get("completed_at")
                result["duration_ms"] = payload.get("duration_ms")
                result["time_to_first_token_ms"] = payload.get("time_to_first_token_ms")
            elif event_type == "token_count":
                usage = token_usage_from_event(payload)
                if usage:
                    result["token_usage"] = usage
        elif record_type == "response_item":
            item_type = payload.get("type")
            if item_type == "message":
                role = payload.get("role")
                text = extract_input_text(payload)
                phase = payload.get("phase")
                if role == "developer":
                    developer_texts.append(text)
                elif role == "user" and "<codex_delegation>" in text:
                    result["raw_user_messages"].append(text)
                elif role == "assistant" and phase == "commentary":
                    result["commentary"].append(text)
                elif role == "assistant" and phase == "final_answer":
                    result["final_response"] = text
            elif item_type in {"function_call", "custom_tool_call"}:
                result["tool_calls"].append(
                    {
                        "call_id": payload.get("call_id"),
                        "name": payload.get("name"),
                        "arguments": parse_arguments(
                            payload.get("arguments", payload.get("input"))
                        ),
                    }
                )
            elif item_type in {"function_call_output", "custom_tool_call_output"}:
                output_by_call[payload.get("call_id")] = output_summary(payload.get("output", ""))
            elif item_type == "tool_search_call":
                result["tool_calls"].append(
                    {
                        "call_id": payload.get("call_id"),
                        "name": "tool_search",
                        "arguments": payload.get("arguments", {}),
                    }
                )
            elif item_type == "tool_search_output":
                output_by_call[payload.get("call_id")] = output_summary(
                    payload.get("tools", [])
                )
            elif item_type == "web_search_call":
                result["tool_calls"].append(
                    {
                        "call_id": f"web_search_{len(result['tool_calls']) + 1}",
                        "name": "web_search",
                        "arguments": payload.get("action", {}),
                    }
                )

    for call in result["tool_calls"]:
        call["output"] = output_by_call.get(call["call_id"])

    developer_text = "\n".join(developer_texts)
    description = extract_skill_description(developer_text)
    if description is not None:
        result["context_trace"]["project_skill_listed"] = True
        result["context_trace"]["project_skill_description_chars"] = len(description)

    skill_path = "codex-project-workflow"
    trace_skill_dir = (
        Path(project_root) / ".agents" / "skills" / "codex-project-workflow"
        if project_root
        else SKILL_DIR
    )
    for call in result["tool_calls"]:
        serialized = normalize_path_text(
            json.dumps(call["arguments"], ensure_ascii=False)
        )
        if skill_path not in serialized:
            continue
        if re.search(r"codex-project-workflow/SKILL\.md", serialized, flags=re.IGNORECASE):
            result["context_trace"]["skill_body_read_calls"].append(call["call_id"])

    if result["context_trace"]["skill_body_read_calls"]:
        skill_file = trace_skill_dir / "SKILL.md"
        if skill_file.is_file():
            result["context_trace"]["skill_body_loaded_chars"] = (
                measure_context.skill_metrics(skill_file)["body_chars"]
            )
        result["context_trace"]["skill_tool_output_chars"] = sum(
            call["output"]["chars"]
            for call in result["tool_calls"]
            if call["call_id"] in result["context_trace"]["skill_body_read_calls"]
            and call["output"]
        )
    result["context_trace"].update(
        reference_call_trace(result["tool_calls"], trace_skill_dir)
    )

    governance_names = (
        "PRD.md",
        "ARCHITECTURE.md",
        "DECISIONS.md",
        "EVALUATION.md",
        "TRACEABILITY.md",
    )
    for call in result["tool_calls"]:
        serialized = normalize_path_text(
            json.dumps(call["arguments"], ensure_ascii=False)
        )
        if any(name in serialized for name in governance_names):
            result["context_trace"]["governance_read_calls"].append(call["call_id"])

    result["final_response_chars"] = len(result["final_response"])
    after_inventory = path_inventory(fixture_root)
    result["fixture"]["after_inventory"] = after_inventory
    result["fixture"]["changed_files"] = changed_files(before_inventory, after_inventory)
    return result


def token_usage_from_event(payload):
    info = payload.get("info") or {}
    return info.get("total_token_usage")


def collect(run_dir, sessions_root, workspace_root, output_dir):
    manifest = load_json(run_dir / "manifest.json")
    setup_state = load_json(workspace_root / "setup-state.json")
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = output_dir / "runs"
    raw_dir.mkdir(exist_ok=True)

    results = []
    for case_id in manifest["cases"]:
        for condition in manifest["conditions"]:
            thread_id = manifest["threads"][case_id][condition]
            rollout = locate_rollout(sessions_root, thread_id)
            fixture_root = workspace_root / condition / case_id
            prefix = f"{case_id}/"
            before_inventory = {
                path[len(prefix):]: value
                for path, value in setup_state["conditions"][condition]["inventory"].items()
                if path.startswith(prefix)
            }
            result = parse_rollout(
                rollout,
                case_id,
                condition,
                fixture_root,
                before_inventory,
                manifest.get("project_roots", {}).get(condition),
            )
            results.append(result)
            (raw_dir / f"{case_id}-{condition}.json").write_text(
                json.dumps(result, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

    summary = {
        "run_id": manifest["run_id"],
        "source_manifest": str((run_dir / "manifest.json").resolve()),
        "results": [
            {
                "case_id": item["case_id"],
                "condition": item["condition"],
                "thread_id": item["thread_id"],
                "status": item["status"],
                "model": item["model"],
                "reasoning_effort": item["reasoning_effort"],
                "duration_ms": item["duration_ms"],
                "time_to_first_token_ms": item["time_to_first_token_ms"],
                "final_response_chars": item["final_response_chars"],
                "total_tokens": (
                    item["token_usage"]["total_tokens"]
                    if item["token_usage"]
                    else None
                ),
                "tool_call_count": len(item["tool_calls"]),
                "changed_file_count": len(item["fixture"]["changed_files"]),
                "context_trace": item["context_trace"],
                "rollout_sha256": item["rollout"]["sha256"],
            }
            for item in results
        ],
    }
    summary_path = output_dir / "summary.json"
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(summary_path)
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    parser.add_argument("--sessions-root", type=Path, required=True)
    parser.add_argument("--workspace-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    collect(
        args.run_dir.resolve(),
        args.sessions_root.resolve(),
        args.workspace_root.resolve(),
        args.output_dir.resolve(),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
