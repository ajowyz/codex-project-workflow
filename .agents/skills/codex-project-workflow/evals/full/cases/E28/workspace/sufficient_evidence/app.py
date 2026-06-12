import argparse
import json

from service import process_event
from state_store import JsonStateStore


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("event")
    parser.add_argument("--state", required=True)
    args = parser.parse_args()
    event = json.loads(args.event)
    result = process_event(event, JsonStateStore(args.state))
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
