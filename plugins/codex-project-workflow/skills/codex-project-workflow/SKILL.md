---
name: codex-project-workflow
description: Never activate for simple questions or explicit low-risk one-step edits or commands, even inside a project or when routine local verification is requested. Excluded tasks must not load the skill body or references. Structure and govern Codex work for new or ambiguous projects, multi-step implementation, professional research, solution comparison, architecture and planning, third-party downloads, high-risk changes, project recovery, or requests for a rigorous workflow. Use when Codex must create, generate, export, or save a deliverable through an existing product or application, even if one step. For other work, activate only when research, confirmation, implementation-path verification, recovery, or coordination materially affects the result.
---

# Codex Project Workflow

## Route
1. Inspect goal/constraints/completion.
2. Use only `research`, `governance`, `verification`: implementation=>verification; research=>research; approval/dependency/coordination=>governance; high-impact/state/migration/path-proof=>governance+verification, even read-only.
3. Here `<skill_dir>` is this `SKILL.md`'s folder. Load each required protocol once/task via `python <skill_dir>/scripts/read_reference.py NAME "Execution Rules" "Output Requirements"`; use repo fallback `.agents/skills/codex-project-workflow/scripts/read_reference.py` only if present. All three: once each. No ref scans; failure waives no gate.
4. If research/dependency/implementation coexist, show one multi-agent proposal before web/install-sim/write/verify. Web/search/open/install-sim needs later exact approval for displayed action; changes need new approval; pre-runs never count. No decision/unrelated approval keeps agents `proposed`; main may continue displayed writes/verification.

## Gates
- Before writes map entry/state/owner/bypasses; edit the owner.
- Save `docs/IMPLEMENTATION_CONTRACT.md` before product-state runs; otherwise trace only. Create no unneeded governance docs.
- Run user/fixture verification commands verbatim; safety, authorization, verification override budgets.

## Finish
Sum helper-emitted NFC metrics for every load, including repeats; if any is unmeasured, report incomplete, never guess. Repeat the aggregate overage line.
