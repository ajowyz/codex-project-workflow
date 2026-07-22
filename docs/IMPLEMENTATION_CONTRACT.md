# Implementation Contract: Codex Development Handoff

Date: 2026-07-22

## User-visible action

Create one new top-level Codex task for all future `codex-project-workflow` development. This current task remains historical context and is not the continuation point.

## Formal product entry

- List saved Codex projects and select the project whose local checkout is `D:\project\codex\codex_project_workflow`.
- Create exactly one local-environment task through the Codex task-creation product entry.
- Give the task a clear continuation title and a self-contained prompt that does not depend on this conversation history.

## Persisted state and ownership

- Persist only the new Codex task, its title, and its initial handoff prompt.
- The new task begins read-only: it may inspect the repository and public GitHub state, then report recovery results and wait for future user direction.
- Task creation must not modify repository files, Git refs, plugin source, marketplace, manifest, personal source, installed cache, candidate evidence, Hook, MCP, or automatic recording behavior.

## Handoff payload

The prompt must identify the workspace, current public repository, completed P1-P5 state, CAND-15/R6 evidence, public `0.1.0` source status, release-package checksum, latest CI result, absence of a tag/Release, remaining clean-install gate, owner boundaries, and the standing requirement to consult both official and other network guidance for future work.

## Success and failure criteria

- Success: the product returns one task identifier; the task is named; its first run acknowledges the correct workspace and boundaries without modifying the repository.
- If creation returns an uncertain result, query the task list before any retry. Never create a duplicate solely because a response timed out.
- If the saved project cannot be identified, stop without creating a projectless substitute.
