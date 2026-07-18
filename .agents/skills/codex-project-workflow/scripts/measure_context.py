#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


def normalized_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def skill_metrics_text(text: str) -> dict:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    match = re.match(r"\A---\n(.*?)\n---\n?(.*)\Z", text, re.S)
    if not match:
        raise ValueError("SKILL.md must contain YAML frontmatter")
    frontmatter, body = match.groups()
    description = re.search(r"^description:\s*(.+)$", frontmatter, re.M)
    if not description:
        raise ValueError("frontmatter description is missing")
    return {
        "description_chars": len(description.group(1).strip()),
        "body_chars": len(body.rstrip("\n")),
    }


def skill_metrics(path: Path) -> dict:
    return skill_metrics_text(normalized_text(path))


def reference_metrics(path: Path) -> dict:
    text = normalized_text(path).rstrip("\n")
    h1_count = len(re.findall(r"^# ", text, re.M))
    starts = [m.start() for m in re.finditer(r"^## ", text, re.M)]
    sections = []
    if starts:
        for index, start in enumerate(starts):
            end = starts[index + 1] if index + 1 < len(starts) else len(text)
            chunk = text[start:end].rstrip("\n")
            sections.append({"heading": chunk.splitlines()[0][3:], "chars": len(chunk)})
    else:
        sections.append({"heading": "(body)", "chars": len(text)})
    return {"h1_count": h1_count, "sections": sections}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_dir", type=Path)
    args = parser.parse_args()
    result = {"skill": skill_metrics(args.skill_dir / "SKILL.md"), "references": {}}
    for path in sorted((args.skill_dir / "references").glob("*.md")):
        result["references"][path.name] = reference_metrics(path)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
