#!/usr/bin/env python3
import argparse
import hashlib
import itertools
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


def minimal_variant_cover(case):
    variants = case["variants"]
    subjects = {
        variant["id"]: set(variant["expected"]["assertion_subjects"])
        for variant in variants
    }
    universe = set().union(*subjects.values())
    for count in range(1, len(variants) + 1):
        for combination in itertools.combinations(
            [variant["id"] for variant in variants],
            count,
        ):
            covered = set().union(*(subjects[item] for item in combination))
            if covered == universe:
                return list(combination)
    raise ValueError(f"{case['case_id']}: no assertion-covering variant set")


def setup_selected(selections, output_root):
    validate_full_fixtures.validate()
    output_root.mkdir(parents=True, exist_ok=True)
    runs = []

    for case_id, variant_id in selections:
        case = load_case(case_id)
        variant = select_variant(case, variant_id)
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


def targeted_selections(case_ids, requested_variants=None):
    requested_variants = requested_variants or {}
    selections = []
    for case_id in dict.fromkeys(case_ids):
        variants = requested_variants.get(case_id)
        if variants is None:
            selections.append((case_id, None))
            continue
        if isinstance(variants, str):
            variants = [variants]
        selections.extend((case_id, variant_id) for variant_id in variants)
    return selections


def setup(case_ids, output_root, requested_variants=None):
    selections = targeted_selections(case_ids, requested_variants)
    return setup_selected(selections, output_root)


def calibration_selections():
    manifest = json.loads(
        (FULL_DIR / "batch_manifest.json").read_text(encoding="utf-8")
    )
    selections = []
    for case_id in manifest["calibration_cases"]:
        case = load_case(case_id)
        selections.extend(
            (case_id, variant_id)
            for variant_id in minimal_variant_cover(case)
        )
    return selections


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", action="append", dest="cases")
    parser.add_argument("--calibration", action="store_true")
    parser.add_argument("--variant", action="append", default=[])
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()

    requested = {}
    for item in args.variant:
        if "=" not in item:
            raise SystemExit("--variant must use CASE=VARIANT")
        case_id, variant_id = item.split("=", 1)
        requested.setdefault(case_id, []).append(variant_id)

    if args.calibration:
        if args.cases or requested:
            raise SystemExit("--calibration cannot be combined with --case or --variant")
        path = setup_selected(
            calibration_selections(),
            args.output_root.resolve(),
        )
    else:
        if not args.cases:
            raise SystemExit("provide --case or --calibration")
        unknown_cases = set(requested) - set(args.cases)
        if unknown_cases:
            raise SystemExit(
                "--variant case must also be selected with --case: "
                + ", ".join(sorted(unknown_cases))
            )
        path = setup(args.cases, args.output_root.resolve(), requested)
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
