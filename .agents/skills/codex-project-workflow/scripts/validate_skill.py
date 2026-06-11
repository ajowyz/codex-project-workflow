#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


def fail(message: str) -> None:
    raise ValueError(message)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_dir", type=Path)
    args = parser.parse_args()
    skill_dir = args.skill_dir
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8-sig")
    match = re.match(r"\A---\n(.*?)\n---\n(.*)\Z", text, re.S)
    if not match:
        fail("invalid SKILL.md frontmatter")
    frontmatter, body = match.groups()
    fields = {}
    for line in frontmatter.splitlines():
        key, separator, value = line.partition(":")
        if not separator:
            fail(f"invalid frontmatter line: {line}")
        fields[key.strip()] = value.strip()
    if set(fields) != {"name", "description"}:
        fail("frontmatter must contain only name and description")
    name = fields["name"]
    description = fields["description"]
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        fail("invalid skill name")
    if not description or len(description) > 1024 or "<" in description or ">" in description:
        fail("invalid description")
    if len(description) > 800:
        fail("description exceeds project budget")
    if len(body.rstrip("\n")) > 1500:
        fail("SKILL.md body exceeds project budget")
    for path in sorted((skill_dir / "references").glob("*.md")):
        reference = path.read_text(encoding="utf-8-sig")
        if len(re.findall(r"^# ", reference, re.M)) != 1:
            fail(f"{path.name} must have exactly one H1")
    ui = (skill_dir / "agents" / "openai.yaml").read_text(encoding="utf-8-sig")
    if f"$${name}" in ui or f"${name}" not in ui:
        fail("default_prompt must mention the skill")
    cases = json.loads((skill_dir / "evals" / "trigger_cases.json").read_text(encoding="utf-8"))
    for group in ("positive", "negative", "boundary"):
        if len(cases.get(group, [])) < 10:
            fail(f"{group} requires at least 10 cases")
    print("Skill structure is valid.")


if __name__ == "__main__":
    main()
