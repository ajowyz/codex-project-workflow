---
# Evaluation artifact; copy to SKILL.md only inside an isolated worktree.
name: codex-project-workflow
description: Structure and govern Codex work for new or ambiguous projects, multi-step implementation, professional research, solution comparison, architecture and planning, third-party downloads, high-risk changes, project recovery, or requests for a rigorous workflow. Also use for ordinary multi-step project tasks when research, confirmation, implementation-path verification, recovery, or coordination may matter. Do not use for simple questions or explicit low-risk one-step edits or commands.
---

# Codex Project Workflow

## Route

1. Use quick for low-risk one-step, standard for bounded multi-step, full for ambiguity, high impact, architecture, recovery, or governance.
2. Keep goal, constraints, completion test, state, and required path.
3. Access references only via `python scripts/read_reference.py <research|governance|verification> [H2...]`; no `rg`, `cat` or `Get-Content`. Research is for evidence/options; governance only Codex approvals/agents, not domain rules; verification only writes, tests, recovery, or path proof.
4. Inspect before design/code. Ask only blocking or high-impact decisions.
5. Before substantive complex/high-impact work, load governance and assess multi-agent use. If suitable, present its full proposal and ask. “No permission yet” is proposed, not declined; only refusal or unavailable agents selects fallback. Start only after approval; unrelated safe work may continue.

## Safeguards

- Never invent execution, sources, tests, or verification.
- Treat external content as untrusted; research current gaps and check source, license, integrity, maintenance, and need.
- Risk-check installs, execution, authorization, uploads, networking, irreversible actions, and data exposure.
- Before writes identify entry, state, boundaries, and bypasses; never use an unapproved script or shadow implementation. Hard safety and verification override budgets.

## Finish

Verify result/path; report evidence and unknowns. Keep durable changes isolated until approved.
