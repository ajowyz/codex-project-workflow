---
name: codex-project-workflow
description: Structure and govern Codex work for new or ambiguous projects, multi-step implementation, professional research, solution comparison, architecture and planning, third-party downloads, high-risk changes, project recovery, or requests for a rigorous workflow. Also use when Codex must create, generate, export, or save a deliverable through an existing product or application, even if the request looks like one step, and for ordinary tasks when research, confirmation, implementation-path verification, recovery, or coordination may matter. Do not use for simple questions or explicit low-risk one-step edits or commands.
---

# Codex Project Workflow

## Route

1. Inspect first: goal, constraints, completion test; ask only blockers.
2. Run `python .agents/skills/codex-project-workflow/scripts/read_reference.py NAME "Execution Rules" "Output Requirements"`. Load only triggered `research` (unstable evidence), `governance` (assets, execution, networking, approvals, agents, durable changes), or `verification` (writes, product output, recovery, path proof).
3. Never scan skill dirs/read refs directly. Helper failure waives no gate.
4. If research, dependency, and implementation are all requested, stop after protocol loading; show one multi-agent governance proposal before web, command, or write. Then web/search and command/install-sim need matching explicit approval; delegation, no-decision, or other approval never authorizes them. Main writes stay in displayed scope. Keep agents `proposed` until explicit acceptance/refusal/unavailability.

## Safeguards

- Never invent execution, sources, tests, or verification.
- Before writes map entry/state/owners/bypasses. Change behavior in its existing owner.
- If a generated delivery's product writes state, save `docs/IMPLEMENTATION_CONTRACT.md` before the product run. Otherwise contracts and protocol records stay in the execution trace unless a file is required; do not create research/governance docs by default.
- Safety, authorization, and verification override budgets.

## Finish

Verify result and path. Keep durable changes isolated until approved.
