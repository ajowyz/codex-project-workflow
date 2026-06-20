# Governance Protocol

## Purpose

Control high-impact decisions, safety checks, multi-agent authorization, and durable behavior changes without interrupting routine work.

## Trigger Conditions

Use this protocol for third-party assets, installs, external execution, account authorization, uploads, internal-data networking, irreversible actions, architecture commitments, or durable rule changes. Assess multi-agent use for two domains, three parallel read-only streams, independent review, multiple milestones, high failure cost, or conflicting evidence.

## Required Input

Identify the action, affected scope, reversibility, data involved, permissions, alternatives, expected benefit, and the exact decision the user must make.

## Execution Rules

- Ask only when a decision blocks progress or has high impact. Continue safe independent work when allowed.
- Protocol records stay in trace/final, not project files, unless explicitly required.
- Before third-party use, record pass/fail/unknown for source, maintenance, license, integrity, necessity, risk.
- Before install/external execution/substitute, show exact command/scope and obtain explicit approval. One approval authorizes only that action.
- Send only approved, minimum, redacted internal data to approved destinations.
- When research, dependency, and implementation are all requested, show a multi-agent governance proposal; do not search, execute, install/sim, write, or verify before it. Prep reads only named budget, safety, task, dependency, path-fact files. Keep nonempty main work; until agents are accepted, main owns tracing, implementation, and final verification. Propose roles and mark state `proposed`; include boundaries, ownership, parallel work, benefit, costs/risks, fallback, and approval packets: exact sanitized query, public targets/fields/purpose/phase, command/scope. For PowerShell simulation, display `powershell -NoProfile -ExecutionPolicy Bypass -File tools/simulate_install.ps1`. Ask and wait. Web/search/open and install/sim must wait for a later exact action approval; an earlier or unapproved action cannot satisfy or be retroactively counted for that approval. No decision/unrelated approval is not action approval, refusal, unavailability, or fallback. Exact action approval lets main do only that action without agents. No-decision keeps agents `proposed`; displayed-scope main implementation/verification continue without another approval. Acceptance starts agents; refusal/unavailable selects fallback. Pending work is local reads/planning, displayed-scope main, independent, or action-approved work only.
- Keep durable rule changes in isolated candidates bound to target, scope, base, patch hash, evidence, and invalidation conditions.
- Safety/authorization override context or speed budgets.
- For hard-trigger overage, sum helper-emitted NFC metrics; never reconstruct text. Use `added_codepoints=max(0, actual_loaded_codepoints-budget_codepoints)` and `added_sections=max(0, emitted_H2_blocks-budget_H2_blocks)`. Count repeated/same-titled H2 outputs separately; H3s add no sections. Every final response, including acknowledgement-only and approval follow-ups, repeats one aggregate unquoted line; never replace it with a bare acknowledgement: `added_codepoints=N, added_sections=N, reason=TEXT, unknown_resolved=TEXT`.

## Stop Conditions

Stop governance work after the decision is recorded with scope and expiry, the action is declined, or a safe lower-impact alternative is selected.

## Output Requirements

Give the decision, recommendation, alternatives, consequences, and work allowed without approval.

## Failure And Degradation

If permissions, data classification, integrity, or approval cannot be verified, do not perform the risky action. Use a read-only analysis, local mock, reversible candidate, or explicit blocked status.
