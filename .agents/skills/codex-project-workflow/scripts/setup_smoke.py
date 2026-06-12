#!/usr/bin/env python3
import argparse
import hashlib
import json
import shutil
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_RUN_DIR = SKILL_DIR / "evals" / "smoke" / "SMOKE-20260612-01"


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_condition(fixtures, destination):
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(fixtures, destination)


def build_inventory(root):
    return {
        str(path.relative_to(root)).replace("\\", "/"): {
            "sha256": file_hash(path),
            "bytes": path.stat().st_size,
        }
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def setup(run_dir, output_root):
    fixtures = run_dir / "fixtures"
    if not fixtures.is_dir():
        raise ValueError(f"missing fixtures: {fixtures}")

    output_root.mkdir(parents=True, exist_ok=True)
    conditions = {}
    for condition in ("baseline", "candidate"):
        destination = output_root / condition
        copy_condition(fixtures, destination)
        conditions[condition] = {
            "root": str(destination.resolve()),
            "inventory": build_inventory(destination),
        }

    state = {
        "run_id": run_dir.name,
        "source": str(run_dir.resolve()),
        "output_root": str(output_root.resolve()),
        "conditions": conditions,
    }
    state_path = output_root / "setup-state.json"
    state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
    return state_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()
    state_path = setup(args.run_dir.resolve(), args.output_root.resolve())
    print(state_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
