---
name: codex-project-workflow
description: Never activate for simple questions or explicit low-risk one-step edits or commands, even inside a project or when routine local verification is requested. Excluded tasks must not load the skill body or references. Structure and govern Codex work for new or ambiguous projects, multi-step implementation, professional research, solution comparison, architecture and planning, third-party downloads, high-risk changes, project recovery, or requests for a rigorous workflow. Use when Codex must create, generate, export, or save a deliverable through an existing product or application, even if one step. For other work, activate only when research, confirmation, implementation-path verification, recovery, or coordination materially affects the result.
---

# Codex Project Workflow

## Route
1. Inspect goal/constraints/outcome.
2. Routes: implementation=>verification; research=>research; approval/dependency/coordination=>governance; high-impact/state/migration/path-proof=>governance+verification even read-only.
3. `<skill_dir>`=active `SKILL.md`'s directory, not version root. Load each required protocol once/task via `python <skill_dir>/scripts/read_reference.py NAME "Execution Rules" "Output Requirements"`; use repo fallback `.agents/skills/codex-project-workflow/scripts/read_reference.py` if present. Expose each helper's raw result separately; never JSON-wrap/bundle. No ref scans; failure waives no gate.
4. Research+dependency+implementation: show one multi-agent proposal before web/install-sim/write/verify. Web/search/open/install-sim needs later exact approval. Search approval excludes open; new query/source/URL/open needs new approval; pre-runs never count. No decision/unrelated approval keeps agents `proposed`; main may continue displayed writes/verification.

## Gates
- Before writes map entry/state/owner/bypasses; edit the owner.
- Save `docs/IMPLEMENTATION_CONTRACT.md` before product-state runs; otherwise trace only. Create no unneeded governance docs.
- Run user/fixture verification commands verbatim, no extra flags; safety/authorization/verification override budgets.

## Finish
Sum every helper-emitted NFC metric, including repeats; if any load is unmeasured, report incomplete, never guess. Repeat aggregate overage.
