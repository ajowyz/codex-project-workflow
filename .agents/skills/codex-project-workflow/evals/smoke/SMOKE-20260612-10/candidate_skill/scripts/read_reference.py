#!/usr/bin/env python3
import argparse
from pathlib import Path


def parse_sections(text):
    result = []
    heading = None
    body = []
    for line in text.splitlines():
        if line.startswith("## "):
            if heading is not None:
                result.append((heading, "\n".join(body).rstrip()))
            heading = line[3:].strip()
            body = [line]
        elif heading is not None:
            body.append(line)
    if heading is not None:
        result.append((heading, "\n".join(body).rstrip()))
    return result


def resolve_reference(value):
    requested = Path(value)
    if requested.is_file():
        return requested.resolve()
    name = requested.name
    if not name.endswith(".md"):
        name += ".md"
    candidates = [
        Path(__file__).resolve().parent.parent / "references" / name,
        Path.cwd()
        / ".agents"
        / "skills"
        / "codex-project-workflow"
        / "references"
        / name,
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    raise SystemExit(f"unknown reference: {value}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("reference")
    parser.add_argument("headings", nargs="+")
    args = parser.parse_args()

    parsed = parse_sections(
        resolve_reference(args.reference).read_text(encoding="utf-8")
    )
    by_heading = {heading.casefold(): body for heading, body in parsed}
    missing = [
        name for name in args.headings if name.casefold() not in by_heading
    ]
    if missing:
        raise SystemExit(f"unknown section: {', '.join(missing)}")
    print(
        "\n\n".join(
            by_heading[name.casefold()] for name in args.headings
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
