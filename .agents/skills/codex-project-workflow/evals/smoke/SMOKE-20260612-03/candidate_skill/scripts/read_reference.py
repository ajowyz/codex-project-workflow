#!/usr/bin/env python3
import argparse
from pathlib import Path


def sections(text):
    lines = text.splitlines()
    result = []
    current = None
    body = []
    for line in lines:
        if line.startswith("## "):
            if current is not None:
                result.append((current, "\n".join(body).rstrip()))
            current = line[3:].strip()
            body = [line]
        elif current is not None:
            body.append(line)
    if current is not None:
        result.append((current, "\n".join(body).rstrip()))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("reference", type=Path)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", action="store_true")
    group.add_argument("--section", action="append")
    args = parser.parse_args()

    reference = args.reference.resolve()
    parsed = sections(reference.read_text(encoding="utf-8"))
    if args.list:
        print("\n".join(heading for heading, _ in parsed))
        return 0

    by_heading = {heading.casefold(): body for heading, body in parsed}
    missing = [name for name in args.section if name.casefold() not in by_heading]
    if missing:
        raise SystemExit(f"unknown section: {', '.join(missing)}")
    print("\n\n".join(by_heading[name.casefold()] for name in args.section))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
