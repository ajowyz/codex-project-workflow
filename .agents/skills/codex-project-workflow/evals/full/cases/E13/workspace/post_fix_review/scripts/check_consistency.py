#!/usr/bin/env python3
import json
from pathlib import Path


root = Path(__file__).resolve().parent.parent
architecture = json.loads((root / "docs" / "architecture.json").read_text())
traceability = json.loads((root / "docs" / "traceability.json").read_text())

left = architecture["routing_component"]
right = traceability["requirements"]["FR-27"]["routing_component"]
print(f"architecture.routing_component={left}")
print(f"traceability.FR-27.routing_component={right}")
raise SystemExit(0 if left == right else 1)
