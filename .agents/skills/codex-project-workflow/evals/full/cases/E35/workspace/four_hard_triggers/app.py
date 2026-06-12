import argparse
import json

from src.client import normalize_event


def run(payload):
    return normalize_event(payload)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    payload = {"data": {"event": {"id": "evt-7", "status": "ready"}}}
    result = run(payload)
    print(json.dumps(result, sort_keys=True))

    if args.self_test:
        assert result == {"id": "evt-7", "status": "ready"}


if __name__ == "__main__":
    main()
