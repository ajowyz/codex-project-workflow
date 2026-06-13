# Governance Protocol

## Purpose

Control high-impact decisions, safety checks, multi-agent authorization, and durable behavior changes without interrupting routine work.

## Trigger Conditions

Use this protocol for third-party assets, installs, external execution, account authorization, uploads, internal-data networking, irreversible actions, architecture commitments, or durable rule changes. Assess multi-agent use for two domains, three parallel read-only streams, independent review, multiple milestones, high failure cost, or conflicting evidence.

## Required Input

Identify the action, affected scope, reversibility, data involved, permissions, alternatives, expected benefit, and the exact decision the user must make.

## Execution Rules

- Ask only when the decision blocks progress or has high impact. Continue safe, independent work while waiting when possible.
- For third-party downloads, record a pass, fail, or unknown outcome for source, maintenance, license, integrity, necessity, and known risk before use.
- Before an install, external execution, or requested install substitute, show the exact command and scope and obtain explicit approval. Approval for one action does not authorize another.
- For internal data, send only the minimum approved, redacted content to approved destinations.
- Three distinct requested streams require a proposal before executing any stream. Other suitable multi-agent work enters `proposed` before permission. Present count and roles, task boundaries, read/write ownership, parallel and main-agent work, benefit, token/time/coordination cost, conflict/context/duplication risk, and the single-agent alternative; then ask explicitly. Silence, deferral, `no decision`, or approval of unrelated actions leaves it `proposed`. Do not start agents or perform their assigned work as fallback. Only explicit acceptance authorizes startup; only explicit refusal or unavailable agents selects fallback. While pending, continue only work already assigned to the main agent or independent of the proposal.
- Durable rule changes remain isolated candidates. Bind approval to target, scope, base version, patch hash, evaluation evidence, and invalidation conditions.
- Never let context or speed budgets suppress a triggered safety or authorization check.
- When hard triggers exceed a stated context budget, compute from the NFC-normalized content of every reference extraction actually emitted: `added_codepoints=max(0, actual_loaded_codepoints-budget_codepoints)` and `added_sections=max(0, emitted_H2_blocks-budget_H2_blocks)`. Measure the captured helper `Output` payload directly; never reconstruct or retype it. Same-titled H2 blocks from different protocols and repeated outputs each count; nested H3 headings do not. Report these values with `reason` and `unknown_resolved`, and carry the current four fields into the final completion response.

## Stop Conditions

Stop governance work after the decision is recorded with scope and expiry, the action is declined, or a safe lower-impact alternative is selected.

## Output Requirements

Present the decision in plain language with the recommended option, alternatives, consequences, and what work can continue without approval.

## Failure And Degradation

If permissions, data classification, integrity, or approval cannot be verified, do not perform the risky action. Use a read-only analysis, local mock, reversible candidate, or explicit blocked status.
