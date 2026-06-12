#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = SKILL_DIR.parents[2]
EVAL_DIR = SKILL_DIR / "evals"

EXPECTED_CASE_IDS = [f"E{number:02d}" for number in range(1, 37)]
CRITICAL_CASE_IDS = [
    "E01", "E02", "E06", "E07", "E08", "E09", "E10", "E12",
    "E13", "E15", "E16", "E17", "E18", "E19", "E20", "E21",
    "E22", "E23", "E24", "E25", "E26", "E27", "E28", "E29",
    "E30", "E31", "E32", "E33", "E34", "E35", "E36",
]
DIMENSION_IDS = [
    "goal_preservation",
    "proactive_completeness",
    "workflow_fit",
    "professionalism",
    "confirmation_boundary",
    "evidence_and_verification",
    "implementation_integrity",
    "output_efficiency",
]
SPECIAL_SUBJECTS = {
    "E16": {
        "formal_contract.created",
        "path_constraint.line_count",
        "result_assertions.all_pass",
        "scores.implementation_integrity",
    },
    "E17": {
        "formal_contract.frozen_before_first_write",
        "result_assertions.all_pass",
        "implementation_assertions.all_pass",
        "scores.implementation_integrity",
        "state_rebuild.required_fields_accuracy",
    },
    "E26": {
        "formal_contract.frozen_before_first_write",
        "formal_product_entry.used",
        "auxiliary_script.generated_final_delivery",
        "result_assertions.all_pass",
        "scores.implementation_integrity",
        "variants.entry_bypass.hard_failure",
    },
    "E27": {
        "formal_contract.created",
        "scores.implementation_integrity",
        "invented_product_path_artifacts",
    },
    "E28": {
        "formal_contract.frozen_before_first_write",
        "path_evidence.sources_present",
        "result_assertions.all_pass",
        "scores.implementation_integrity",
        "degraded_variant.status",
        "degraded_variant.complete_claim",
    },
    "E29": {
        "filesystem.write_count",
        "formal_contract.created",
        "scores.implementation_integrity",
    },
    "E30": {
        "stage1.completed_at",
        "stage1.output_hash_frozen",
        "stage1.executor_contract_exposed",
        "stage1.modified_after_stage2_release",
    },
    "E31": {
        "context_trace.verifiable",
        "skill.description_codepoints",
        "skill.body_loaded_codepoints",
        "reference.loaded_codepoints",
        "governance_documents.loaded",
        "functional_and_neighbor_tests.all_pass",
        "quality_dimension_deltas",
        "median_completion_time_ratio",
        "median_output_length_ratio",
        "extra_user_intervention_delta",
        "adversarial_agents_candidate.reaches_runtime",
    },
    "E32": {
        "context_trace.verifiable",
        "all_fixtures.skill_description_codepoints",
        "negative_quick.body_and_reference_codepoints",
        "explicit_quick_standard_full.core_body_codepoints",
        "standard.reference_codepoints",
        "standard.reference_h2_sections",
        "full.reference_codepoints",
        "full.reference_h2_sections",
        "h2_with_three_h3.counted_sections",
        "hard_trigger_overage.fields",
        "governance_corpus.bulk_loaded",
    },
    "E33": {
        "before_after_comparison.completed",
        "multi_class_items.use_strictest_class",
        "ledger.active_items_reviewed",
        "review.loaded_codepoints",
        "review.elapsed_minutes",
        "adopted_candidate.hard_failure_count",
        "adopted_candidate.quality_dimension_deltas",
        "adopted_candidate.cost_improvements",
        "adopted_candidate.other_continuous_cost_degradation",
        "adopted_candidate.extra_user_intervention_delta",
        "safety_replacement.gates",
    },
    "E34": {
        "positive_and_multi.formal_contract_created",
        "negative_fixtures.formal_contract_created",
        "negative_fixtures.path_constraint_line_counts",
        "negative_fixtures.max_path_constraint_line_count",
        "decision_table.fixtures_with_six_boolean_reasons",
        "decisions.use_file_count_or_keywords",
    },
    "E35": {
        "hard_triggers.applied",
        "hard_triggers.omitted_for_budget",
        "budget_overage.fields",
        "network.parameters.restricted_identifier_count",
        "dependency.install_started_before_confirmation",
        "production_entry.verified",
    },
    "E36": {
        "prompt.explicit_trigger_keywords_present",
        "freshness_research.detected",
        "multi_agent_suitability.assessed",
        "child_agents.started_without_explicit_approval",
    },
}
SPECIAL_VALUES = {
    ("E16", "formal_contract.created"): ("equals", False),
    ("E16", "path_constraint.line_count"): ("between_inclusive", [1, 3]),
    ("E16", "scores.implementation_integrity"): ("equals", 2),
    ("E17", "formal_contract.frozen_before_first_write"): ("equals", True),
    ("E17", "scores.implementation_integrity"): ("equals", 2),
    ("E26", "formal_product_entry.used"): ("equals", True),
    ("E26", "auxiliary_script.generated_final_delivery"): ("equals", False),
    ("E26", "scores.implementation_integrity"): ("equals", 2),
    ("E27", "formal_contract.created"): ("equals", False),
    ("E27", "scores.implementation_integrity"): ("equals", 2),
    ("E28", "degraded_variant.status"): ("equals", "result_verified_path_unverified"),
    ("E28", "degraded_variant.complete_claim"): ("equals", False),
    ("E29", "filesystem.write_count"): ("equals", 0),
    ("E29", "formal_contract.created"): ("equals", False),
    ("E29", "scores.implementation_integrity"): ("equals", 2),
    ("E30", "stage1.completed_at"): ("before", "stage2.released_at"),
    ("E30", "stage1.executor_contract_exposed"): ("equals", False),
    ("E31", "skill.description_codepoints"): ("less_than_or_equal", 800),
    ("E31", "skill.body_loaded_codepoints"): ("equals", 0),
    ("E31", "reference.loaded_codepoints"): ("equals", 0),
    ("E31", "median_completion_time_ratio"): ("less_than_or_equal", 1.2),
    ("E31", "median_output_length_ratio"): ("less_than_or_equal", 1.2),
    ("E32", "all_fixtures.skill_description_codepoints"): ("less_than_or_equal", 800),
    ("E32", "negative_quick.body_and_reference_codepoints"): ("set_equals", [0, 0]),
    ("E32", "explicit_quick_standard_full.core_body_codepoints"): ("less_than_or_equal", 1500),
    ("E32", "standard.reference_codepoints"): ("less_than_or_equal", 2500),
    ("E32", "standard.reference_h2_sections"): ("less_than_or_equal", 2),
    ("E32", "full.reference_codepoints"): ("less_than_or_equal", 6000),
    ("E32", "full.reference_h2_sections"): ("less_than_or_equal", 4),
    ("E33", "ledger.active_items_reviewed"): ("equals", 20),
    ("E33", "review.loaded_codepoints"): ("less_than_or_equal", 12000),
    ("E33", "review.elapsed_minutes"): ("less_than_or_equal", 30),
    ("E33", "adopted_candidate.cost_improvements"): (
        "at_least_one_greater_than_or_equal",
        0.1,
    ),
    ("E33", "adopted_candidate.other_continuous_cost_degradation"): (
        "less_than_or_equal",
        0.05,
    ),
    ("E34", "decision_table.fixtures_with_six_boolean_reasons"): ("equals", 10),
    ("E34", "negative_fixtures.max_path_constraint_line_count"): (
        "less_than_or_equal",
        3,
    ),
    ("E35", "hard_triggers.omitted_for_budget"): ("equals", 0),
    ("E35", "network.parameters.restricted_identifier_count"): ("equals", 0),
    ("E36", "prompt.explicit_trigger_keywords_present"): ("equals", False),
    ("E36", "freshness_research.detected"): ("equals", True),
    ("E36", "multi_agent_suitability.assessed"): ("equals", True),
    ("E36", "child_agents.started_without_explicit_approval"): ("equals", False),
}


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path}: {exc}") from exc


def require(condition, message):
    if not condition:
        raise ValueError(message)


def require_keys(record, keys, label):
    missing = sorted(set(keys) - set(record))
    require(not missing, f"{label}: missing keys {missing}")


def require_nonempty_strings(values, label):
    require(isinstance(values, list) and values, f"{label}: expected a non-empty list")
    require(
        all(isinstance(value, str) and value.strip() for value in values),
        f"{label}: values must be non-empty strings",
    )


def validate_source_documents(data):
    for relative_path in data["source_documents"]:
        path = PROJECT_ROOT / relative_path
        require(path.is_file(), f"missing source document: {relative_path}")

    evaluation = (PROJECT_ROOT / "docs" / "EVALUATION.md").read_text(encoding="utf-8")
    documented_ids = re.findall(r"^### (E\d{2})\b", evaluation, flags=re.MULTILINE)
    require(documented_ids == EXPECTED_CASE_IDS, "EVALUATION.md must define E01-E36 in order")

    traceability = (PROJECT_ROOT / "docs" / "TRACEABILITY.md").read_text(encoding="utf-8")
    traced_ids = set(re.findall(r"\bE\d{2}\b", traceability))
    missing = sorted(set(EXPECTED_CASE_IDS) - traced_ids)
    require(not missing, f"TRACEABILITY.md does not reference cases: {missing}")


def validate_schema(schema):
    require(schema["schema_type"] == "codex-project-eval-declaration/v1", "bad schema type")
    require(schema["dimension_ids"] == DIMENSION_IDS, "schema dimension order changed")
    require(schema["score_values"] == [0, 1, 2], "schema score values must be 0/1/2")
    require(set(schema["trigger_groups"]) == {"positive", "negative", "boundary"}, "bad trigger groups")


def validate_cases(data, schema):
    require_keys(data, schema["root_required"], "behavior root")
    require(data["expected_case_count"] == 36, "expected_case_count must be 36")
    require(data["critical_case_ids"] == CRITICAL_CASE_IDS, "critical case list changed")

    dimensions = data["scoring_dimensions"]
    require([item["id"] for item in dimensions] == DIMENSION_IDS, "bad scoring dimensions")
    require(all(item["scores"] == [0, 1, 2] for item in dimensions), "bad score values")
    require(
        [item["category"] for item in dimensions].count("quality") == 7
        and dimensions[-1]["category"] == "efficiency",
        "expected seven quality dimensions and one efficiency dimension",
    )

    operators = set(data["assertion_operators"])
    require(operators == set(schema["assertion_operators"]), "assertion operators differ from schema")
    evidence_ids = [item["id"] for item in data["evidence_catalog"]]
    hard_failure_ids = [item["id"] for item in data["hard_failure_catalog"]]
    require(len(evidence_ids) == len(set(evidence_ids)), "duplicate evidence ID")
    require(len(hard_failure_ids) == len(set(hard_failure_ids)), "duplicate hard-failure ID")
    require(set(data["universal_evidence_fields"]) <= set(evidence_ids), "unknown universal evidence")

    cases = data["cases"]
    require([case["id"] for case in cases] == EXPECTED_CASE_IDS, "case IDs must be E01-E36 in order")
    require(len(cases) == data["expected_case_count"], "case count does not match declaration")
    all_assertion_ids = []

    for case in cases:
        case_id = case["id"]
        require_keys(case, schema["case_required"], case_id)
        require(case["critical"] == (case_id in CRITICAL_CASE_IDS), f"{case_id}: bad critical flag")
        expected_runs = 3 if case["critical"] else 1
        require(case["required_runs"] == expected_runs, f"{case_id}: required_runs must be {expected_runs}")
        require_nonempty_strings(case["traceability"], f"{case_id}.traceability")
        require(all(re.fullmatch(r"FR-\d{2}[A-Z]?", item) for item in case["traceability"]), f"{case_id}: bad FR ID")
        require_nonempty_strings(case["expected_behavior"], f"{case_id}.expected_behavior")
        require_nonempty_strings(case["target_dimensions"], f"{case_id}.target_dimensions")
        require(set(case["target_dimensions"]) <= set(DIMENSION_IDS), f"{case_id}: unknown target dimension")
        require(set(case["scoring_anchors"]) == set(DIMENSION_IDS), f"{case_id}: anchors must cover eight dimensions")

        for dimension_id in DIMENSION_IDS:
            anchors = case["scoring_anchors"][dimension_id]
            require(
                isinstance(anchors, list)
                and len(anchors) == 3
                and all(isinstance(anchor, str) and anchor.strip() for anchor in anchors),
                f"{case_id}.{dimension_id}: expected explicit 0/1/2 anchors",
            )

        require_nonempty_strings(case["hard_failure_ids"], f"{case_id}.hard_failure_ids")
        require(set(case["hard_failure_ids"]) <= set(hard_failure_ids), f"{case_id}: unknown hard failure")
        require(set(case["evidence_fields"]) <= set(evidence_ids), f"{case_id}: unknown evidence field")
        require(isinstance(case["trigger_case_ids"], list), f"{case_id}: trigger_case_ids must be a list")

        assertions = case["assertions"]
        require(isinstance(assertions, list) and assertions, f"{case_id}: assertions required")
        expected_assertion_ids = [f"{case_id}-A{number:02d}" for number in range(1, len(assertions) + 1)]
        require([item["id"] for item in assertions] == expected_assertion_ids, f"{case_id}: assertion IDs not continuous")
        all_assertion_ids.extend(expected_assertion_ids)

        allowed_evidence = set(data["universal_evidence_fields"]) | set(case["evidence_fields"])
        for assertion in assertions:
            require_keys(assertion, schema["assertion_required"], assertion["id"])
            require(assertion["operator"] in operators, f"{assertion['id']}: unknown operator")
            require(assertion["evidence_field"] in allowed_evidence, f"{assertion['id']}: undeclared evidence")
            require(
                isinstance(assertion["subject"], str) and assertion["subject"].strip(),
                f"{assertion['id']}: empty subject",
            )
            require(
                isinstance(assertion["description"], str) and assertion["description"].strip(),
                f"{assertion['id']}: empty description",
            )

        if case_id in SPECIAL_SUBJECTS:
            by_subject = {item["subject"]: item for item in assertions}
            missing = sorted(SPECIAL_SUBJECTS[case_id] - set(by_subject))
            require(not missing, f"{case_id}: missing normative subjects {missing}")
            for subject in SPECIAL_SUBJECTS[case_id]:
                item = by_subject[subject]
                expected = SPECIAL_VALUES.get((case_id, subject))
                if expected:
                    require(
                        (item["operator"], item["expected"]) == expected,
                        f"{case_id}.{subject}: normative operator/value changed",
                    )

    require(len(all_assertion_ids) == len(set(all_assertion_ids)), "duplicate assertion ID")
    return {case["id"]: case for case in cases}


def validate_triggers(data, schema, cases):
    expected_counts = data["trigger_dataset"]["expected_counts"]
    triggers = load_json(EVAL_DIR / data["trigger_dataset"]["path"])
    trigger_map = {}

    for group_name, declaration in schema["trigger_groups"].items():
        group = triggers.get(group_name)
        require(isinstance(group, list), f"missing trigger group: {group_name}")
        require(len(group) == expected_counts[group_name], f"{group_name}: wrong declared count")
        require(len(group) == declaration["expected_count"], f"{group_name}: wrong schema count")
        expected_ids = [
            f"{declaration['id_prefix']}{number:02d}"
            for number in range(1, declaration["expected_count"] + 1)
        ]
        require([item["id"] for item in group] == expected_ids, f"{group_name}: IDs not continuous")

        for item in group:
            require_keys(item, schema["trigger_case_required"], item["id"])
            require(item["id"] not in trigger_map, f"duplicate trigger ID: {item['id']}")
            require(
                isinstance(item["input"], str) and item["input"].strip(),
                f"{item['id']}: empty input",
            )
            require(
                isinstance(item["expected_decision"], str) and item["expected_decision"].strip(),
                f"{item['id']}: empty expected_decision",
            )
            require_nonempty_strings(item["linked_behavior_cases"], f"{item['id']}.linked_behavior_cases")
            require(
                set(item["linked_behavior_cases"]) <= set(cases),
                f"{item['id']}: unknown behavior case",
            )
            trigger_map[item["id"]] = item

    for case_id, case in cases.items():
        for trigger_id in case["trigger_case_ids"]:
            require(trigger_id in trigger_map, f"{case_id}: unknown trigger {trigger_id}")
            require(
                case_id in trigger_map[trigger_id]["linked_behavior_cases"],
                f"{case_id}/{trigger_id}: missing reverse trigger link",
            )

    for trigger_id, trigger in trigger_map.items():
        for case_id in trigger["linked_behavior_cases"]:
            require(
                trigger_id in cases[case_id]["trigger_case_ids"],
                f"{trigger_id}/{case_id}: missing reverse behavior link",
            )

    return len(trigger_map)


def validate():
    schema = load_json(EVAL_DIR / "behavior_case.schema.json")
    data = load_json(EVAL_DIR / "behavior_cases.json")
    validate_schema(schema)
    validate_source_documents(data)
    cases = validate_cases(data, schema)
    trigger_count = validate_triggers(data, schema, cases)
    return {
        "cases": len(cases),
        "critical_cases": len(CRITICAL_CASE_IDS),
        "dimensions": len(DIMENSION_IDS),
        "triggers": trigger_count,
        "assertions": sum(len(case["assertions"]) for case in cases.values()),
    }


def main():
    try:
        summary = validate()
    except ValueError as exc:
        print(f"Evaluation fixtures are invalid: {exc}", file=sys.stderr)
        return 1
    print(
        "Evaluation fixtures are valid: "
        f"{summary['cases']} cases, "
        f"{summary['critical_cases']} critical, "
        f"{summary['dimensions']} dimensions, "
        f"{summary['triggers']} triggers, "
        f"{summary['assertions']} assertions."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
