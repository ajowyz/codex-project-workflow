# Governance Protocol

## Purpose

Control high-impact decisions, safety checks, multi-agent authorization, and durable behavior changes without interrupting routine work.

## Trigger Conditions

Use this protocol for third-party assets, installs, external execution, account authorization, uploads, internal-data networking, irreversible actions, architecture commitments, or durable rule changes. Assess multi-agent use for two domains, three parallel read-only streams, independent review, multiple milestones, high failure cost, or conflicting evidence.

## Required Input

Identify the action, affected scope, reversibility, data involved, permissions, alternatives, expected benefit, and the exact decision the user must make.

## Execution Rules

- Ask only when a decision blocks progress or has high impact. Continue safe independent work when allowed.
- Protocol records belong in the execution trace or final response, not project files, unless the user or project explicitly requires a file.
- Before third-party use, record pass, fail, or unknown for source, maintenance, license, integrity, necessity, and known risk.
- Before install, external execution, or a substitute, show the exact command and scope and obtain explicit approval. One approval authorizes only that action.
- Send only approved, minimum, redacted internal data to approved destinations.
- When research, dependency/execution, and implementation are all requested, first show a governance proposal; do not search, execute, install/simulate, write, or verify before it. Proposal prep may read only named budget, safety, task, dependency, and path-fact files. Keep a nonempty main work package; for writes, main owns tracing, implementation, and final verification until agents are accepted. State roles, boundaries, ownership, parallel work, benefit, cost/risks, fallback, and every approval packet: exact sanitized query, public targets/fields/purpose/phase, and exact command/scope. Ask explicitly. No decision or unrelated approval leaves agents `proposed`; it is not refusal, unavailability, or fallback. Exact action approval lets main do only that action without starting agents. Acceptance starts agents; refusal or unavailable agents selects fallback. Pending work is main-assigned, independent, or action-approved only.
- Keep durable rule changes in isolated candidates bound to target, scope, base, patch hash, evidence, and invalidation conditions.
- Safety and authorization checks override context or speed budgets.
- For hard-trigger overage, sum every helper's emitted NFC metrics; never reconstruct text. Compute `added_codepoints=max(0, actual_loaded_codepoints-budget_codepoints)` and `added_sections=max(0, emitted_H2_blocks-budget_H2_blocks)`. Count repeated outputs and same-titled H2 blocks separately; nested H3 headings do not add sections. Every final response, including later approval follow-ups, must repeat exactly one aggregate machine-readable line with unquoted numbers: `added_codepoints=N, added_sections=N, reason=TEXT, unknown_resolved=TEXT`.

## Stop Conditions

Stop governance work after the decision is recorded with scope and expiry, the action is declined, or a safe lower-impact alternative is selected.

## Output Requirements

Present the decision in plain language with the recommended option, alternatives, consequences, and what work can continue without approval.

## Failure And Degradation

If permissions, data classification, integrity, or approval cannot be verified, do not perform the risky action. Use a read-only analysis, local mock, reversible candidate, or explicit blocked status.
