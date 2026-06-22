# Codex Project Workflow User Guide

`codex-project-workflow` helps Codex collaborate more efficiently and rigorously on complex or ambiguous work. It does not make Codex pre-trained for every domain. Instead, it tells Codex when to inspect the project, load the right local protocol, request scoped research approval, compare options, verify the implementation path, and report remaining risk.

## When To Use It

Use this skill for new projects, unclear requirements, multi-step implementation, architecture or PRD work, professional research, solution comparison, high-risk changes, third-party downloads, project recovery, or tasks where a correct output is not enough and the implementation path also matters.

Do not use the full workflow for simple facts, one low-risk command, a tiny text replacement, or an explicit quick explanation that does not depend on project state.

## Good User Input

Natural language is fine. For important tasks, the most useful structure is:

```text
Goal: what I want done.
Scope: what can and cannot change.
Done: what result counts as complete.
Risk: what must stay stable.
Verification: how I want the result proven.
```

## Long Conversations And Fresh Threads

For long projects, do not treat the chat transcript as the only project memory. Before switching threads, keep the current goal, stage, completed work, next step, blockers, risks, and validation evidence in project files such as `README.md`, `docs/PLAN.md`, or another visible status document.

In a fresh thread, ask Codex to recover state before editing:

```text
I am continuing a long project in a fresh thread. First read the project entry docs, plan or status docs, and git status. Report the current goal, completed work, next step, blockers, risks, and missing evidence before modifying files.
```

Recovery does not expand prior authorization. External research, dependency installation, destructive operations, high-impact decisions, and multi-agent activation still need fresh scoped confirmation.

## Confirmation Boundaries

Codex can normally proceed with local read-only inspection, local non-destructive edits, nearby tests, documentation updates, and local commits inside an approved stage.

Codex should stop for confirmation before external research that sends project context, dependency installation, third-party binary use, destructive file operations, high-impact product decisions, multi-agent activation, or turning one experience into a long-term rule.

## Multi-Agent Work

Codex should propose multi-agent work when a task crosses several professional boundaries, has independent review value, or has enough parallel research or audit work to justify the extra coordination cost. Without explicit approval, proposed agents stay proposed and the main agent continues only the work that does not depend on them.

## Research

Research is scoped. Codex should state the purpose, planned queries or source types, fields to extract, and any information sent outside the workspace. Each approval covers only the shown phase and scope.

## Verification

For implementation tasks, Codex should verify both the result and the path. A good final report should answer:

```text
Was the result verified?
Was the original project entry or owner path used?
What risk or evidence gap remains?
```

## Learning And Improvement

The skill can improve through usage, but not by silently rewriting itself. Reusable lessons should become candidate changes with a scope, evidence, regression checks, and explicit activation before they become durable behavior.
