#!/usr/bin/env python3
import json
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "accounts.json"
BACKUP = ROOT / "data" / "accounts.backup.json"
RESULT = ROOT / "migration" / "result.json"


def migrate():
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1:
        raise SystemExit("expected schema version 1")
    shutil.copyfile(DATA, BACKUP)
    payload["schema_version"] = 2
    for account in payload["accounts"]:
        account["display_name"] = account.pop("name")
    DATA.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(
        json.dumps(
            {
                "status": "migrated",
                "record_ids": [item["id"] for item in payload["accounts"]],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def validate():
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    valid = (
        payload.get("schema_version") == 2
        and BACKUP.is_file()
        and RESULT.is_file()
        and all(
            "display_name" in item and "name" not in item
            for item in payload.get("accounts", [])
        )
    )
    print("PASS" if valid else "FAIL")
    raise SystemExit(0 if valid else 1)


if __name__ == "__main__":
    if sys.argv[1:] == ["migrate"]:
        migrate()
    elif sys.argv[1:] == ["validate"]:
        validate()
    else:
        raise SystemExit("usage: entrypoint.py migrate|validate")
