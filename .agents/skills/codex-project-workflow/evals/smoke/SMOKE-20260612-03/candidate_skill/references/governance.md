# Governance Protocol

## Purpose

Control high-impact decisions, safety checks, multi-agent authorization, and durable behavior changes without interrupting routine work.

## Trigger Conditions

Use this protocol for third-party assets, installs, external execution, account authorization, uploads, internal-data networking, irreversible actions, architecture commitments, or durable rule changes. Assess multi-agent use for two domains, three parallel read-only streams, independent review, multiple milestones, high failure cost, or conflicting evidence.

## Required Input

Identify the action, affected scope, reversibility, data involved, permissions, alternatives, expected benefit, and the exact decision the user must make.

## Execution Rules

- Ask only when the decision blocks progress or has high impact. Continue safe, independent work while waiting when possible.
- For third-party downloads, check source, maintenance, license, integrity, necessity, and known risk before use.
- For internal data, send only the minimum approved, redacted content to approved destinations.
- Suitable multi-agent work enters `proposed` even when permission has not yet been granted. Present count and roles, task boundaries, read/write ownership, parallel and main-agent work, benefit, token/time/coordination cost, conflict/context/duplication risk, and the single-agent alternative. Ask for an explicit decision. Only explicit acceptance authorizes startup; only explicit refusal or unavailable agents selects fallback.
- Durable rule changes remain isolated candidates. Bind approval to target, scope, base version, patch hash, evaluation evidence, and invalidation conditions.
- Never let context or speed budgets suppress a triggered safety or authorization check.

## Stop Conditions

Stop governance work after the decision is recorded with scope and expiry, the action is declined, or a safe lower-impact alternative is selected.

## Output Requirements

Present the decision in plain language with the recommended option, alternatives, consequences, and what work can continue without approval.

## Failure And Degradation

If permissions, data classification, integrity, or approval cannot be verified, do not perform the risky action. Use a read-only analysis, local mock, reversible candidate, or explicit blocked status.
