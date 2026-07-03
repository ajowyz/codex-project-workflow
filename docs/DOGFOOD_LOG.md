# Dogfood Log

本文件记录用 `codex-project-workflow` 插件审查和优化本项目本身的过程。

## Boundary

Dogfood 的目标是发现项目可改进点，不是让插件证明自己正确。

固定边界：

- 可以审查文档、模板、安装流程、复验脚本和扩展路线。
- 可以提出或执行低风险文档修复。
- 不把插件输出当作插件正确性的证明。
- 不在没有候选、证据和回归的情况下修改 `SKILL.md`。
- 不修改 plugin manifest、marketplace、已安装 cache、Hook、MCP、app connector 或自定义 Agent manifest。

## DOGFOOD-01 Read-Only Review

Date: 2026-06-23

Scope: read-only review of project entry docs, productized docs, install/update docs, plugin package docs, and installed plugin smoke evidence.

Evidence:

- Installed plugin helper was used from plugin cache path.
- `python scripts\verify_plugin_install_smoke.py` passed.
- `git status` was clean before review.
- Review found status drift and entry-document ambiguity without modifying files.

Findings:

- Historical docs still contained old candidate or pre-install status.
- There were too many plausible entry documents for a new user.
- Install/update docs mixed current-machine paths with general install guidance.
- Plugin package README depended too much on source-repository docs.

Decision:

Proceed to DOGFOOD-02 as low-risk documentation optimization only.

## DOGFOOD-02 Documentation Optimization

Date: 2026-06-23

Scope: clarify document entry points, fix status drift, split local install state from general guidance, and make plugin package README more standalone.

Allowed changes:

- Add `docs/DOCUMENT_INDEX.md`.
- Update status notes in historical/development docs.
- Update install/update docs.
- Update plugin package README.

Disallowed changes:

- Active skill rules.
- Plugin manifest.
- Marketplace entry.
- Installed plugin cache.
- Hook, MCP, app connector, or custom Agent manifest.

## DOGFOOD-03 Real Low-Risk Template Exercise

Date: 2026-06-23

Scope: use the plugin workflow on a real low-risk task: review whether `docs/TASK_TEMPLATES.md` covers the user's repeated real workflows from this project.

Boundary:

- Allowed files: `docs/TASK_TEMPLATES.md` and this log.
- No active skill rule changes.
- No plugin manifest, marketplace, installed cache, Hook, MCP, app connector, or custom Agent manifest changes.
- Do not treat plugin output as proof that the plugin is correct; use file evidence and verification commands.

Evidence:

- Installed plugin helper loaded `governance` and `verification` from the plugin cache path.
- `docs/TASK_TEMPLATES.md` already covered new project startup, continuing current project, professional solution comparison, implementation-path proof, fewer interruptions, multi-agent judgment, network research, final acceptance, plugin smoke, and model/context upgrades.
- The project conversation repeatedly used additional workflows not directly represented as templates: progress and drift reports, pause/resume with usage limits, dogfood self-review, and candidate-improvement capture.

Action:

- Added templates for progress/drift reporting, pause/resume and budget boundaries, dogfood self-review, candidate-improvement capture, and document-entry/status consistency review.

Verification:

- Run plugin install smoke.
- Run existing script unit tests.
- Run whitespace diff check.

## DOGFOOD-04A Long Conversation Handoff Template

Date: 2026-06-23

Scope: add a reusable handoff template for moving a long project conversation into a fresh Codex thread, and surface the same behavior in product and plugin-package documentation.

Boundary:

- Allowed files: `docs/TASK_TEMPLATES.md`, `docs/PRODUCT_MANUAL.md`, `plugins/codex-project-workflow/README.md`, `plugins/codex-project-workflow/docs/USER_GUIDE.md`, and this log.
- No active skill rule changes.
- No reference protocol changes.
- No plugin manifest, marketplace, installed cache, Hook, MCP, app connector, or custom Agent manifest changes.
- Do not treat the new template as proof that recovery works; verify with file inspection and existing checks.

Evidence:

- The project already has `docs/STATE_CONTRACT.md` for minimal new-thread state reconstruction.
- Existing task templates covered continuing work and pause/resume, but did not provide a direct long-conversation-to-fresh-thread prompt.
- Long conversations can mix old decisions, compressed summaries, and current state; recovery should start from project files and git status.

Action:

- Added a "长对话转新线程交接" template to `docs/TASK_TEMPLATES.md`.
- Added a long conversation and fresh-thread handoff section to `docs/PRODUCT_MANUAL.md`.
- Added fresh-thread handoff guidance to the source plugin README and package user guide.

Verification:

- Run targeted text search for the new template and package docs.
- Run whitespace diff check.
- Run plugin install smoke to confirm packaging smoke remains unaffected.

## DOGFOOD-04B Handoff Verification Loop

Date: 2026-06-23

Scope: record a dogfood signal from DOGFOOD-04A: after documenting the long-conversation handoff template, Codex did not proactively call out that the template itself should be validated in a fresh thread.

Boundary:

- Allowed files: `docs/DOGFOOD_LOG.md`, `docs/TASK_TEMPLATES.md`, and `docs/PRODUCT_MANUAL.md`.
- No active skill rule changes.
- No reference protocol changes.
- No plugin manifest, marketplace, installed cache, Hook, MCP, app connector, or custom Agent manifest changes.
- Do not upgrade this directly into a core rule; treat it as a project dogfood and documentation acceptance-loop fix.

Finding:

- This is primarily an acceptance-loop gap, with a secondary execution-habit issue.
- It is not primarily a template-content gap: DOGFOOD-04A added a usable fresh-thread recovery prompt, but the verification checklist did not require trying or recommending a real fresh-thread recovery smoke.
- Documenting a workflow is not the same as proving that the workflow was exercised.

Minimal fix:

- Add a reminder to the long-conversation handoff template that changes to recovery or handoff guidance should be followed by a fresh-thread read-only recovery smoke.
- Add the same acceptance-loop reminder to the product manual.

Fresh-thread smoke:

- First broad recovery smoke thread completed after a slower run. It used the full DOGFOOD-04A/04B recovery prompt and reported current goal, completed work, next step, blockers, risks, git status, DOGFOOD-04A, and DOGFOOD-04B.
- A second minimal fresh-thread smoke also passed. It used current project files and git status only, with no old chat, file edits, commits, browsing, or agent startup.
- The minimal smoke recovered that DOGFOOD-04A added the long-conversation/fresh-thread handoff docs and DOGFOOD-04B added the verification-loop reminder.
- Evidence reported by the smoke: `docs/DOGFOOD_LOG.md` has DOGFOOD-04A and DOGFOOD-04B sections; `README.md` points to `docs/DOCUMENT_INDEX.md`; `docs/DOCUMENT_INDEX.md` lists `docs/DOGFOOD_LOG.md` as a current verification/status record; git modified files are `docs/DOGFOOD_LOG.md`, `docs/PRODUCT_MANUAL.md`, `docs/TASK_TEMPLATES.md`, `plugins/codex-project-workflow/README.md`, and `plugins/codex-project-workflow/docs/USER_GUIDE.md`.
- Smoke risk: the minimal smoke checked only the requested read-only sources and git status/name-status; it did not independently inspect every modified target document beyond the DOGFOOD log record.

## DOGFOOD-05 Plugin Smoke UX

Date: 2026-07-03

Scope: improve the user-facing output and documentation around `scripts/verify_plugin_install_smoke.py`.

Boundary:

- Allowed files: `scripts/verify_plugin_install_smoke.py`, `docs/PLUGIN_INSTALL_SMOKE.md`, `docs/INSTALL_UPDATE.md`, and this log.
- No active skill rule changes.
- No reference protocol changes.
- No plugin manifest, marketplace, installed cache, Hook, MCP, app connector, or custom Agent manifest changes.

Finding:

- The smoke script already verified the important path facts, but the output was terse.
- Success output did not explicitly frame itself as an acceptance report.
- Failure messages did not consistently include next-step guidance.
- The docs described what the script checks, but did not show what a user should look for in the output.

Action:

- Updated the smoke script to print a clear `PLUGIN INSTALL SMOKE` report, selected cache version, installed paths, fallback guard, reference metrics, and `PLUGIN INSTALL SMOKE: PASS`.
- Updated failure paths to print `PLUGIN INSTALL SMOKE: FAIL`, a reason, and next steps.
- Updated install/smoke docs with expected successful output and failure-reading guidance.

Verification:

- `python scripts\verify_plugin_install_smoke.py` passed and printed `PLUGIN INSTALL SMOKE: PASS`.
- Failure UX was checked with a missing cache root; it printed `PLUGIN INSTALL SMOKE: FAIL`, a reason, and next steps.
- `python -m unittest discover -s .agents\skills\codex-project-workflow\scripts -p test_scripts.py` passed 49 tests.
- `git diff --check` reported no whitespace errors; Git only warned that modified files will be normalized from LF to CRLF when touched.

## DOGFOOD-06A Smoke Script Focused Tests

Date: 2026-07-03

Scope: turn DOGFOOD-05's smoke UX changes into a low-risk code exercise with focused tests.

Boundary:

- Allowed files: `scripts/test_verify_plugin_install_smoke.py`, `docs/INSTALL_UPDATE.md`, and this log.
- No active skill rule changes.
- No reference protocol changes.
- No plugin manifest, marketplace, installed cache, Hook, MCP, app connector, or custom Agent manifest changes.
- Tests use temporary fake plugin cache directories and do not modify the real installed plugin cache.

Action:

- Added focused tests for the plugin install smoke script.
- Covered success report output, missing cache failure guidance, rejection of mixed install paths, and helper execution from a temporary directory.
- Added the new test command to the install/update local checks.

Verification:

- `python -m unittest discover -s scripts -p "test_*.py"` passed 4 tests.
- `python scripts\verify_plugin_install_smoke.py` passed and printed `PLUGIN INSTALL SMOKE: PASS`.
- `python -m unittest discover -s .agents\skills\codex-project-workflow\scripts -p test_scripts.py` passed 49 tests.
- `git diff --check` reported no whitespace errors; Git only warned that modified docs will be normalized from LF to CRLF when touched.

## DOGFOOD-07 Multi-Agent Decision Template Exercise

Date: 2026-07-03

Scope: use the plugin workflow on a real documentation task: calibrate the `docs/TASK_TEMPLATES.md` multi-agent judgment prompt against the governance output requirements.

Boundary:

- Allowed files: `docs/TASK_TEMPLATES.md` and this log.
- No active skill rule changes.
- No reference protocol changes.
- No plugin manifest, marketplace, installed cache, Hook, MCP, app connector, or custom Agent manifest changes.
- Do not start multi-agent workers; this is a single-agent template exercise.

Finding:

- The existing template asked for Agent roles, boundaries, costs, risks, and fallback.
- It did not explicitly ask for the governance protocol's decision, recommendation, alternatives, consequences, or work allowed without approval.
- It also did not explicitly require `proposed` status or state that silence/unrelated approval is not acceptance.

Action:

- Updated the multi-agent judgment template to request decision, recommendation, alternatives, consequences, allowed main-thread work, `proposed` state, and explicit acceptance semantics.

Verification:

- Targeted text search found the new decision, alternative, allowed-work, `proposed`, and explicit-acceptance wording.
- `git diff --check` reported no whitespace errors; Git only warned that modified docs will be normalized from LF to CRLF when touched.
- `python scripts\verify_plugin_install_smoke.py` passed and printed `PLUGIN INSTALL SMOKE: PASS`.

## DOGFOOD-08 Professional Comparison Template Exercise

Date: 2026-07-03

Scope: use the plugin workflow on a real documentation task: calibrate the `docs/TASK_TEMPLATES.md` professional-solution prompt against the research protocol output requirements without browsing.

Boundary:

- Allowed files: `docs/TASK_TEMPLATES.md` and this log.
- No active skill rule changes.
- No reference protocol changes.
- No plugin manifest, marketplace, installed cache, Hook, MCP, app connector, or custom Agent manifest changes.
- No web browsing; this is a local template exercise.

Finding:

- The existing professional-solution template asked what sources or methods would be used, which options would be compared, and why one option was recommended.
- It did not explicitly ask for recommendation-first output, evidence dates or versions, applicability limits, failure modes, reversibility, counterevidence, unresolved questions, or the next verification step.
- It did not explicitly require saying when the answer is based only on local project files and existing context because networking has not been approved.

Action:

- Updated the professional-solution template to request recommendation-first comparison, evidence dates or versions, applicability limits, failure modes, reversibility, counterevidence, unresolved questions, and next verification.
- Added a no-networking boundary sentence and kept networking behind an explicit research approval package.

Verification:

- Targeted text search found the new recommendation, evidence-date, failure-mode, reversibility, counterevidence, unresolved-question, next-verification, and no-networking wording.
- `git diff --check` reported no whitespace errors; Git only warned that modified docs will be normalized from LF to CRLF when touched.
- `python scripts\verify_plugin_install_smoke.py` passed and printed `PLUGIN INSTALL SMOKE: PASS`.

## DOGFOOD-09 Extension Roadmap Refresh

Date: 2026-07-03

Scope: update `docs/EXTENSION_ROADMAP.md` after DOGFOOD-05 through DOGFOOD-08 so the roadmap reflects completed P1 work and remaining gates.

Boundary:

- Allowed files: `docs/EXTENSION_ROADMAP.md` and this log.
- No active skill rule changes.
- No reference protocol changes.
- No plugin manifest, marketplace, installed cache, Hook, MCP, app connector, or custom Agent manifest changes.

Finding:

- The roadmap still listed P1 template, smoke, and real-project exercise work as generic future actions.
- It did not reflect completed DOGFOOD-05 smoke UX, DOGFOOD-06A smoke focused tests, DOGFOOD-07 multi-agent judgment template calibration, or DOGFOOD-08 professional-comparison template calibration.
- It also did not state what should remain before moving to P2 automation or candidate mechanisms.

Action:

- Added current-progress bullets under P1 template work and update/smoke stability.
- Split real-project exercises into completed and remaining items.
- Added a P2 entry gate: complete at least one new-project interview or implementation-path proof exercise before moving on.

Verification:

- Targeted text search found roadmap current-progress, completed exercise, remaining exercise, and P2 gate wording.
- `git diff --check` reported no whitespace errors; Git only warned that modified docs will be normalized from LF to CRLF when touched.
- `python scripts\verify_plugin_install_smoke.py` passed and printed `PLUGIN INSTALL SMOKE: PASS`.
