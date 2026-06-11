#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

ADR_START = re.compile(r"^## (ADR-\d{3}) (.+)$", re.M)
STATE = re.compile(r"^- 治理状态：(建议确认|已确认|已废弃|已替代)$", re.M)
RELATION = re.compile(r"^- 替代关系：(无|replaces (ADR-\d{3}(?:, ADR-\d{3})*)|replaced-by (ADR-\d{3}))$", re.M)


def parse(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    starts = list(ADR_START.finditer(text))
    records = []
    for index, match in enumerate(starts):
        block = text[match.start() : starts[index + 1].start() if index + 1 < len(starts) else len(text)]
        states = STATE.findall(block)
        if len(states) != 1:
            raise ValueError(f"{match.group(1)} must contain one governance state")
        relation_lines = re.findall(r"^- 替代关系：.*$", block, re.M)
        relations = []
        for line in relation_lines:
            relation = RELATION.fullmatch(line)
            if not relation:
                raise ValueError(f"{match.group(1)} has invalid replacement syntax")
            relations.append(relation.groups())
        if len(relations) > 2:
            raise ValueError(f"{match.group(1)} has too many replacement lines")
        replaces, replaced_by, has_none = [], None, False
        for full, old_ids, new_id in relations:
            if full == "无":
                has_none = True
            elif full.startswith("replaces "):
                if replaces:
                    raise ValueError(f"{match.group(1)} repeats replaces")
                replaces = old_ids.split(", ")
                if replaces != sorted(replaces):
                    raise ValueError(f"{match.group(1)} replacement targets must be sorted")
            else:
                if replaced_by:
                    raise ValueError(f"{match.group(1)} repeats replaced-by")
                replaced_by = new_id
        if has_none and (replaces or replaced_by or len(relations) != 1):
            raise ValueError(f"{match.group(1)} mixes none with a relationship")
        records.append(
            {
                "id": match.group(1),
                "title": match.group(2),
                "governance_state": states[0],
                "replaces_ids": replaces,
                "replaced_by_id": replaced_by,
                "body_anchor": match.start(),
            }
        )
    validate(records)
    return records


def validate(records: list[dict]) -> None:
    by_id = {record["id"]: record for record in records}
    if len(by_id) != len(records):
        raise ValueError("duplicate ADR id")
    edges = set()
    for record in records:
        if record["replaced_by_id"] and record["governance_state"] != "已替代":
            raise ValueError(f"{record['id']} has replaced-by but is not 已替代")
        if record["governance_state"] == "已替代" and not record["replaced_by_id"]:
            raise ValueError(f"{record['id']} is 已替代 without replaced-by")
        for old_id in record["replaces_ids"]:
            if old_id not in by_id or old_id == record["id"]:
                raise ValueError(f"invalid replacement target {old_id}")
            if by_id[old_id]["replaced_by_id"] != record["id"]:
                raise ValueError(f"replacement edge {old_id} -> {record['id']} is not declared at both ends")
            edges.add((old_id, record["id"]))
        new_id = record["replaced_by_id"]
        if new_id:
            if new_id not in by_id or new_id == record["id"]:
                raise ValueError(f"invalid replacement target {new_id}")
            if record["id"] not in by_id[new_id]["replaces_ids"]:
                raise ValueError(f"replacement edge {record['id']} -> {new_id} is not declared at both ends")
            edges.add((record["id"], new_id))
    graph = {record["id"]: [] for record in records}
    for old_id, new_id in edges:
        graph[old_id].append(new_id)
    visiting, visited = set(), set()

    def visit(node: str) -> None:
        if node in visiting:
            raise ValueError("replacement cycle")
        if node in visited:
            return
        visiting.add(node)
        for target in graph[node]:
            visit(target)
        visiting.remove(node)
        visited.add(node)

    for node in graph:
        visit(node)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("decisions", type=Path)
    args = parser.parse_args()
    print(json.dumps(parse(args.decisions), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
