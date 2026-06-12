#!/usr/bin/env python3
import argparse
import hashlib
import json
import shutil
from pathlib import Path

import validate_full_fixtures

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
FULL_DIR = SKILL_DIR / "evals" / "full"
CASES_DIR = FULL_DIR / "cases"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(root):
    return {
        str(path.relative_to(root)).replace("\\", "/"): {
            "sha256": sha256(path),
            "bytes": path.stat().st_size,
        }
        for path in sorted(root.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
    }


def load_case(case_id):
    return json.loads(
        (CASES_DIR / case_id / "case.json").read_text(encoding="utf-8")
    )


def select_variant(case, requested=None):
    variants = case["variants"]
    if requested is None:
        return variants[0]
    matches = [variant for variant in variants if variant["id"] == requested]
    if len(matches) != 1:
        raise ValueError(f"{case['case_id']}: unknown variant {requested}")
    return matches[0]


def setup(case_ids, output_root, requested_variants=None):
    validate_full_fixtures.validate()
    output_root.mkdir(parents=True, exist_ok=True)
    requested_variants = requested_variants or {}
    runs = []

    for case_id in case_ids:
        case = load_case(case_id)
        variant = select_variant(case, requested_variants.get(case_id))
        source = CASES_DIR / case_id / variant["workspace"]
        destination = output_root / case_id / variant["id"]
        if destination.exists():
            shutil.rmtree(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(
            source,
            destination,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        workspace = str(destination.resolve())
        prompt = variant["prompt"].replace("{workspace}", workspace)
        runs.append(
            {
                "case_id": case_id,
                "variant_id": variant["id"],
                "workspace": workspace,
                "permissions": variant["permissions"],
                "prompt": prompt,
                "scripted_user_replies": variant["scripted_user_replies"],
                "before_inventory": inventory(destination),
            }
        )

    state = {
        "format_version": "1.0",
        "source_commit": json.loads(
            (FULL_DIR / "batch_manifest.json").read_text(encoding="utf-8")
        )["activation_commit"],
        "output_root": str(output_root.resolve()),
        "runs": runs,
    }
    state_path = output_root / "setup-state.json"
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return state_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", action="append", dest="cases", required=True)
    parser.add_argument("--variant", action="append", default=[])
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()

    requested = {}
    for item in args.variant:
        if "=" not in item:
            raise SystemExit("--variant must use CASE=VARIANT")
        case_id, variant_id = item.split("=", 1)
        requested[case_id] = variant_id

    path = setup(args.cases, args.output_root.resolve(), requested)
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
