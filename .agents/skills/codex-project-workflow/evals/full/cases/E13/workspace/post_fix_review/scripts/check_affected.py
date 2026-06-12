#!/usr/bin/env python3
import json
from pathlib import Path


root = Path(__file__).resolve().parent.parent
changes = json.loads((root / "changes" / "p1_fixes.json").read_text())
architecture = json.loads((root / "docs" / "architecture.json").read_text())
traceability = json.loads((root / "docs" / "traceability.json").read_text())

checks = {
    "revision_matches_architecture": changes["revision"] == architecture["revision"],
    "revision_matches_traceability": changes["revision"] == traceability["revision"],
    "approval_owner_matches": (
        architecture["approval_owner"]
        == traceability["requirements"]["FR-27"]["approval_owner"]
    ),
}

for name, passed in checks.items():
    print(f"{name}: {'PASS' if passed else 'FAIL'}")

raise SystemExit(0 if all(checks.values()) else 1)
