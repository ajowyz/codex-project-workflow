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

## DOGFOOD-10 Implementation-Path Proof Template Exercise

Date: 2026-07-03

Scope: use the plugin workflow on a real documentation task: calibrate the `docs/TASK_TEMPLATES.md` implementation-path proof prompt against the verification protocol output requirements.

Boundary:

- Allowed files: `docs/TASK_TEMPLATES.md`, `docs/EXTENSION_ROADMAP.md`, and this log.
- No active skill rule changes.
- No reference protocol changes.
- No plugin manifest, marketplace, installed cache, Hook, MCP, app connector, or custom Agent manifest changes.

Finding:

- The existing implementation-path template covered user entry, owner module/function, owner-path edit, bypass risk, result verification, and path verification.
- It did not explicitly ask for state/persistence changes, result, tests, auxiliary scripts, deviations, or unverified paths.
- The roadmap still listed implementation-path proof as a remaining P1 exercise.

Action:

- Updated the implementation-path proof template to request state/persistence changes, result verification, tests, auxiliary scripts, deviations, and unverified paths.
- Added the explicit fallback phrase: `结果已验证，实现路径未验证`.
- Updated the roadmap to mark the implementation-path proof template exercise complete and keep new-project interview as the remaining recommended P1 exercise.

Verification:

- Targeted text search found the new state/persistence, save path, tests, auxiliary scripts, deviations, unverified-path, fallback-phrase, and roadmap-completion wording.
- `git diff --check` reported no whitespace errors; Git only warned that modified docs will be normalized from LF to CRLF when touched.
- `python scripts\verify_plugin_install_smoke.py` passed and printed `PLUGIN INSTALL SMOKE: PASS`.

## DOGFOOD-11 New Project Interview Template Exercise

Date: 2026-07-03

Scope: use the plugin workflow on a real documentation task: calibrate the `docs/TASK_TEMPLATES.md` new-project startup prompt against the product manual's goal, constraint, and completion-standard guidance.

Boundary:

- Allowed files: `docs/TASK_TEMPLATES.md`, `docs/EXTENSION_ROADMAP.md`, and this log.
- No active skill rule changes.
- No reference protocol changes.
- No plugin manifest, marketplace, installed cache, Hook, MCP, app connector, or custom Agent manifest changes.

Finding:

- The existing new-project template asked for understood goal, missing information, initial risk/boundary, and next collaboration mode.
- It did not explicitly ask for target users, scenarios, pain points, scope, non-goals, constraints, completion criteria, deliverables, data/security/compliance boundaries, or human-confirmation decisions.
- The roadmap still listed new-project interview as a remaining recommended P1 exercise.

Action:

- Expanded the new-project startup template to cover users, scenarios, pain points, scope/non-goals, constraints, completion standards, deliverables, missing information, risks, boundaries, human-confirmation decisions, and minimal clarifying questions.
- Updated the roadmap to mark the new-project interview template exercise complete and state that P2 can be considered while preserving sensitive configuration boundaries.

Verification:

- Targeted text search found target-user, scenario, pain-point, non-goal, completion-standard, deliverable, minimal-question, roadmap-completion, and install/update automation wording.
- `git diff --check` reported no whitespace errors; Git only warned that modified docs will be normalized from LF to CRLF when touched.
- `python scripts\verify_plugin_install_smoke.py` passed and printed `PLUGIN INSTALL SMOKE: PASS`.

## DOGFOOD-12 Plugin Update Prep Script

Date: 2026-07-03

Scope: start P2 install/update automation with a conservative repository script that validates and optionally copies the plugin source package.

Boundary:

- Allowed files: `scripts/prepare_plugin_update.py`, `scripts/test_prepare_plugin_update.py`, `docs/INSTALL_UPDATE.md`, `docs/EXTENSION_ROADMAP.md`, and this log.
- No active skill rule changes.
- No reference protocol changes.
- No plugin manifest, marketplace, installed cache, Hook, MCP, app connector, or custom Agent manifest changes.
- Do not run `--apply` in this dogfood step; tests may copy only temporary fake plugin packages.

Action:

- Added `scripts/prepare_plugin_update.py`.
- Default mode is dry-run: validate source package, report source/target/required files, state safety boundaries, and print next steps.
- `--apply` copies the repository plugin source package to the personal plugin source directory but still does not modify marketplace or installed plugin cache.
- Added focused tests using temporary fake plugin packages.
- Updated install/update docs and roadmap with the new script.

Verification:

- `python scripts\prepare_plugin_update.py` passed in dry-run mode and printed `PLUGIN UPDATE PREP: PASS`; no files were copied.
- `python -m unittest discover -s scripts -p "test_*.py"` passed 8 tests.
- `python scripts\verify_plugin_install_smoke.py` passed and printed `PLUGIN INSTALL SMOKE: PASS`.
- `python -m unittest discover -s .agents\skills\codex-project-workflow\scripts -p test_scripts.py` passed 49 tests.
- `git diff --check` reported no whitespace errors; Git only warned that modified docs will be normalized from LF to CRLF when touched.

## DOGFOOD-13 Real Update Readiness

Date: 2026-07-03

Scope: advance the P2 install/update automation from source-copy prep to a state where a real plugin update can be prepared with one explicit repository command before Codex App or CLI reinstall.

Boundary:

- Allowed files: `scripts/prepare_plugin_update.py`, `scripts/test_prepare_plugin_update.py`, `docs/INSTALL_UPDATE.md`, `docs/PLUGIN_INSTALL_SMOKE.md`, `docs/EXTENSION_ROADMAP.md`, and this log.
- No active skill rule changes.
- No reference protocol changes.
- No plugin manifest, marketplace, installed cache, Hook, MCP, app connector, or custom Agent manifest changes.
- Do not run a real reinstall in this dogfood step; stop at repository-verified readiness.

Finding:

- DOGFOOD-12 could copy the repository plugin source to the personal plugin source, but cachebuster update still depended on a separate manual command.
- The dry-run report did not yet validate the personal marketplace entry or guard against stale files left in the target plugin source.
- Without those checks, a real reinstall could use the wrong source path or carry stale target files forward.

Action:

- Extended `scripts/prepare_plugin_update.py` to validate the personal marketplace entry, report source and target manifest versions, and reject target files that are not present in the repository source package.
- Added explicit `--apply --apply-cachebuster` support to copy the repository plugin source and rewrite only the personal plugin source manifest version with a `+codex.<token>` suffix.
- Kept marketplace and installed plugin cache read-only.
- Added focused tests for marketplace validation, cachebuster application, missing `--apply`, and stale target file rejection.
- Updated install/update docs, install smoke notes, and the extension roadmap.

Verification:

- `python scripts\prepare_plugin_update.py` passed in dry-run mode and printed `marketplace: checked`, `target stale-file guard: ok`, and `PLUGIN UPDATE PREP: PASS`; no files were copied.
- `python scripts\prepare_plugin_update.py --cachebuster DOGFOOD-13` passed in dry-run mode and printed planned version `0.1.0+codex.dogfood-13`; no files were copied.
- `python -m unittest discover -s scripts -p "test_*.py"` passed 12 tests.

## DOGFOOD-14 Real Plugin Install Completion

Date: 2026-07-03

Scope: complete the real local plugin update after DOGFOOD-13 made the repository update path ready.

Boundary:

- Allowed files: `README.md`, `docs/INSTALL_UPDATE.md`, `docs/PLUGIN_INSTALL_SMOKE.md`, and this log.
- No active skill rule changes.
- No reference protocol changes.
- No repository plugin manifest changes.
- No manual marketplace edits.
- Do not manually edit installed plugin cache.

Action:

- Ran `python scripts\prepare_plugin_update.py --apply --apply-cachebuster`.
- The personal plugin source manifest was updated to `0.1.0+codex.20260703085220`.
- The script validated the personal marketplace entry and did not modify marketplace or installed cache.
- Tried `codex plugin add codex-project-workflow@personal`; it failed with `codex.exe: Access is denied`.
- Used Codex App plugin UI as the reinstall path.

Verification:

- `python scripts\verify_plugin_install_smoke.py` passed and selected installed cache version `0.1.0+codex.20260703085220`.
- Installed skill, helper, and references all came from `C:\Users\wang yazhou\.codex\plugins\cache\personal\codex-project-workflow\0.1.0+codex.20260703085220`.
- `governance`, `research`, and `verification` metrics matched the expected installed reference outputs.
- Fresh-thread pickup remained as a separate follow-up gate and was completed in DOGFOOD-15.

## DOGFOOD-15 Fresh-Thread Pickup Smoke

Date: 2026-07-03

Scope: verify that a newly created Codex project thread picks up the updated installed plugin cache after DOGFOOD-14.

Boundary:

- Allowed files: `docs/PLUGIN_INSTALL_SMOKE.md` and this log.
- No active skill rule changes.
- No reference protocol changes.
- No repository plugin manifest changes.
- No manual marketplace edits.
- Do not manually edit installed plugin cache.
- Fresh-thread smoke itself was read-only: no file edits, no commits, no browsing, and no multi-agent startup.

Action:

- Created fresh-thread pickup smoke thread `019f2736-4b2f-7032-80e4-5d74a0f72552`.
- Asked the fresh thread to verify automatic `codex-project-workflow` pickup, installed cache path, helper metrics, required project docs, git status, and `python scripts\verify_plugin_install_smoke.py`.

Verification:

- Fresh-thread conclusion: passed.
- The fresh thread reported the visible `codex-project-workflow` skill path as `C:\Users\wang yazhou\.codex\plugins\cache\personal\codex-project-workflow\0.1.0+codex.20260703085220\skills\codex-project-workflow\SKILL.md`.
- It explicitly rejected the old `0.1.0+codex.20260622112058` cache and project `.agents` copy as the evidence path.
- It reported protocol metrics: `governance codepoints=2484 h2_sections=2`, `research codepoints=1205 h2_sections=2`, and `verification codepoints=2239 h2_sections=2`.
- It ran `python scripts\verify_plugin_install_smoke.py`; the script selected `0.1.0+codex.20260703085220` and printed `PLUGIN INSTALL SMOKE: PASS`.
- It reported `git status --short --branch --untracked-files=all` as `## master`.

## DOGFOOD-16 Local-Use Improvement Capture

Date: 2026-07-03

Scope: respond to the local-use signal that the plugin can notice problems during use, but should not silently auto-update itself.

Boundary:

- Allowed files: `docs/IMPROVEMENT_CANDIDATES.md`, `docs/DOCUMENT_INDEX.md`, `docs/TASK_TEMPLATES.md`, `docs/INSTALL_UPDATE.md`, `docs/EXTENSION_ROADMAP.md`, `plugins/codex-project-workflow/skills/codex-project-workflow/SKILL.md`, `scripts/prepare_plugin_update.py`, `scripts/test_prepare_plugin_update.py`, and this log.
- No plugin manifest changes.
- No marketplace edits.
- No installed plugin cache edits.
- Do not run a real reinstall in this dogfood step; stop at repository-verified readiness.

Finding:

- This is an improvement-capture and acceptance-closure gap, not a request for silent self-update.
- The project already had a candidate-improvement template and update-prep script, but no current candidate ledger tying real-use problems to later updates.
- The update-prep script did not explicitly remind the user to bind the update to a candidate, dogfood note, or explicit request, then record the new cache version and smoke result.
- The source plugin finish rule did not explicitly call out the real acceptance action for workflow-template, install/update, package, or acceptance-record changes.

Action:

- Added `docs/IMPROVEMENT_CANDIDATES.md` with a stable record template and DOGFOOD-16 entry.
- Added the candidate ledger to the document index.
- Updated the candidate-improvement template to require deciding whether to write the ledger.
- Updated install/update docs and roadmap to describe the human-in-the-loop candidate-to-update path.
- Updated the source plugin `SKILL.md` finish rule with a narrow acceptance-closure check.
- Updated `scripts/prepare_plugin_update.py` and tests so update-prep output reminds users to bind updates to a candidate, dogfood note, or explicit request and record final smoke evidence.

Verification:

- Run focused script tests.
- Run dry-run update prep.
- Run installed plugin smoke.
- Run whitespace diff check.

Follow-up update prep:

- Ran `python scripts\prepare_plugin_update.py --apply --apply-cachebuster`.
- Personal plugin source was updated to `0.1.0+codex.20260703113254`.
- The script validated the personal marketplace entry and did not modify marketplace or installed cache.
- `codex plugin list` and the extensionless packaged `codex` executable both failed with `Access is denied`.
- Opened the Codex App plugin page and re-enabled the plugin there.
- `python scripts\verify_plugin_install_smoke.py` then selected installed cache version `0.1.0+codex.20260703113254` and printed `PLUGIN INSTALL SMOKE: PASS`.
- Fresh-thread pickup smoke thread `019f27c3-179b-7220-a045-15094edcf86a` passed. It reported the visible skill path as `C:\Users\wang yazhou\.codex\plugins\cache\personal\codex-project-workflow\0.1.0+codex.20260703113254\skills\codex-project-workflow\SKILL.md`, explicitly rejected old cache `0.1.0+codex.20260703085220` and project `.agents` as evidence paths, and reported protocol metrics `governance codepoints=2484 h2_sections=2`, `research codepoints=1205 h2_sections=2`, `verification codepoints=2239 h2_sections=2`.
- Remaining gate: none for DOGFOOD-16 install pickup. Future source changes still need source prep, Codex App re-enable, install smoke, fresh-thread pickup smoke, and record update.

## DOGFOOD-17 Roadmap Status Sync

Date: 2026-07-03

Scope: update the extension roadmap after DOGFOOD-16 completed the real local update loop.

Boundary:

- Allowed files: `docs/EXTENSION_ROADMAP.md` and this log.
- No active skill rule changes.
- No reference protocol changes.
- No plugin manifest, marketplace, installed cache, Hook, MCP, app connector, or custom Agent manifest changes.

Finding:

- `docs/EXTENSION_ROADMAP.md` still listed the real apply, re-enable, fresh-thread smoke, and cache-version recording as a future optional direction.
- DOGFOOD-16 had already completed that loop and installed cache `0.1.0+codex.20260703113254`.

Action:

- Updated the roadmap to mark the first real update loop complete.
- Reframed future update work as repeating the same candidate-bound, human-in-the-loop process for later source changes.
- Kept sensitive configuration boundaries unchanged.

Verification:

- Run roadmap text search for stale future wording.
- Run install smoke.
- Run whitespace diff check.

## DOGFOOD-18 GPT-5.6 Runtime and Evaluation Refresh

Date: 2026-07-16

Scope: re-evaluate the plugin after the Codex App, CLI, and active GPT model changed; remove duplicate skill ownership; repair the E32/E35 harness; prepare and smoke the resulting plugin package.

Boundary:

- Repository package is the only editable skill source.
- `.agents/skills/codex-project-workflow/` remains an evaluation and protocol-mirror area, not a discoverable project skill.
- Installation uses the supported plugin preparation and CLI install flow; marketplace and installed cache are not edited by hand.
- No automatic recording, Hook, MCP, app connector, dependency installation, background self-update, or vector database work.
- Historical GPT-5.5 entries remain unchanged and continue to describe their own evaluation period.

External research:

- Refreshed the current official guidance for [building skills](https://learn.chatgpt.com/docs/build-skills), [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), and [models](https://learn.chatgpt.com/docs/models).
- Compared the documented configuration contract with the current implementation report in [openai/codex issue #20210](https://github.com/openai/codex/issues/20210): project-local `skills.config` filtering is not reliable evidence of runtime exclusion in the affected implementation.
- Treated official documentation as the intended contract and fresh runtime traces as implementation evidence; no project-local config workaround was retained.

Findings:

- CAND-20260716-13 baseline calibration passed 4 of 6 target regressions, but failed E32 negative control and the E32 standard context budget.
- The negative-control path and blind-evaluation wording leaked the skill identity, while the collector did not fully decode current unified `exec` traces.
- A project-local discoverable skill created a second apparent owner beside the plugin package and made installed-runtime evidence harder to interpret.
- The current App task can retain a stale plugin inventory snapshot after reinstall. A fresh CLI process observed a newly installed candidate cache, so App task pickup, final-cache integrity, and final-cache pickup must be reported separately.

Action:

- Replaced the candidate description with exclusion-first routing and narrowed bounded Route 2 implementation to verification-only unless a governance trigger is present.
- Removed the project-local discoverable `SKILL.md` and ineffective project config; retained evaluation scripts, fixtures, protocol mirrors, and recorded evidence under `.agents`.
- Isolated negative-control workspaces and made the blind boundary conditional on independent skill activation.
- Updated full-evaluation setup, collection, validation, context measurement, and script tests for relative manifests, unified `exec`, JSON text blocks, actual workdirs, fixture isolation, and real loaded-skill metrics.
- Prepared and installed cache `0.1.0+codex.20260716095059` through the supported plugin flow.

Verification:

- Project script tests passed `67/67`.
- The repository's strict skill, eval, fixture, install-smoke, hash, and whitespace checks are the local acceptance gates.
- The official Python validators require `PyYAML`; no available Python runtime had it, so those validators are recorded as unavailable rather than passed.
- Fresh CLI runtime evidence first saw a single `codex-project-workflow:codex-project-workflow` entry from candidate cache `0.1.0+codex.20260716093851`; later clean negative and standard regressions loaded the final cache `0.1.0+codex.20260716095059`, which also passed explicit-version smoke. The already-open App task may still display its older inventory until a new top-level task or App restart.
- Formal candidate pass/fail remains in the candidate manifest and evaluation result records; this dogfood entry is an operational narrative, not a substitute verdict.
- At the close of this entry, final-cache clean CLI regressions had validator-passing formal result packages for E32 `negative_quick` and `standard_cross_file` under the tracked `.eval-workspaces/formal-results/` directory; their source manifests and collector diagnostics remain under the matching `.agents/skills/codex-project-workflow/evals/full/runs/` directories. The remaining four E32/E35 fixtures were prepared but blocked by the account Codex usage limit.
- That temporary quota block was cleared and the remaining batch was completed on 2026-07-18. See DOGFOOD-19 for the formal outcome; the contaminated App runs remain debugging evidence only.

## DOGFOOD-19 CAND-14 Remaining Clean Regression

Date: 2026-07-18

Scope: complete the four final-cache E32/E35 regressions that were previously blocked by the Codex usage limit, assess their formal evidence, and update CAND-14 without activating it.

Boundary:

- Used fresh, isolated CLI threads with `gpt-5.6-sol` / `xhigh`, App `26.715.3651.0`, CLI `0.145.0-alpha.18`, the installed final cache, exact fixture prompts, and only the scripted approvals.
- Did not edit the installed cache, marketplace, candidate body, candidate patch, or personal plugin source. Did not activate CAND-14.
- Discarded diagnostic attempts against legacy `CodexSandboxOffline`-owned workspaces after ACL refresh failed. Regenerated host-owned workspaces instead of weakening sandboxing or changing those ACLs.

Verification:

- Formal run: `.agents/skills/codex-project-workflow/evals/full/runs/REGRESSION-20260718-GPT56-C14-REMAINING-CLEAN/`.
- Passed: E32 `full_high_risk_migration` and `nested_h3_counting`.
- Failed: E32 `hard_trigger_overage` omitted the mandatory verification protocol; E35 `four_hard_triggers` left public-source verification incomplete, ran a different unit-test command, duplicated protocol loads, and reported the intended rather than actual aggregate overage.
- Per-run result is `2/4`; with E32 aggregated across three variants, the validated case result is `0/2 targeted_regression cases passed; overall=fail`.
- Candidate manifest now records `preflight_passed_regression_failed` and `activation.allowed=false`.

Outcome:

- The quota-dependent work is complete, but CAND-14 did not meet activation criteria. The next implementation cycle must use a new repair candidate and fresh targeted regressions; CAND-14 remains frozen as failed evidence.

## DOGFOOD-20 CAND-15 Repair and Clean Acceptance

Date: 2026-07-18

Scope: repair the two current-model regressions left by CAND-14, harden measurement and prompt-integrity gates, install an evaluation cache through the supported flow, complete fresh targeted and six-run clean regressions, and synchronize the project state without activating the candidate.

Boundary:

- Used repository source as the only editable owner; personal source was prepared by the supported update script and installed cache was not edited by hand.
- Used fresh isolated CLI sessions with `gpt-5.6-sol` / `xhigh`, App `26.715.3651.0`, CLI `0.145.0-alpha.18`, memory injection disabled, and exact fixture replies only.
- Kept automatic recording, Hook, MCP, app connectors, background updates, dependency installation, and marketplace edits out of scope.
- Did not activate CAND-15. The installed R6 directory is evaluation evidence, not activation authority.

External guidance:

- Rechecked [official skill-building guidance](https://learn.chatgpt.com/docs/build-skills) for precise trigger boundaries and positive/negative test prompts.
- Rechecked [official subagent guidance](https://learn.chatgpt.com/docs/agent-configuration/subagents) for independent parallel work and write-conflict limits.
- Compared local runtime evidence with community implementation reports on [project-local filtering](https://github.com/openai/codex/issues/20210), [duplicate skill names](https://github.com/openai/codex/issues/25324), and [resume versus fresh-session context](https://github.com/openai/codex/issues/17560).

Action:

- Created CAND-20260718-15 with explicit three-protocol routing, high-impact governance-plus-verification, load-once/raw-metric rules, exact verification commands, separate page-open approval, and pending-agent behavior.
- Hardened the collector and validator so incomplete nested measurements cannot be guessed or accepted, and added the fourth E35 page-open scripted reply.
- Iterated diagnostic prompts and cache revisions without promoting failed diagnostics; final evaluated cache is `0.1.0+codex.cand-20260718-15-r6`.

Verification:

- Static gates: `71/71` script tests, `12/12` root tests, `36 cases / 148 assertions`, `31/31 cases / 61 variants`, skill structure PASS, diff check PASS.
- R6 smoke PASS with governance `2484/2`, research `1205/2`, and verification `2239/2`; repo, personal source, and installed cache content parity passed.
- Targeted clean run `REGRESSION-20260718-GPT56-C15-TARGETED-CLEAN7`: `2/2` runs and `2/2` cases passed.
- Full clean run `REGRESSION-20260718-GPT56-C15-FULL`: all six runs passed; aggregate `2/2 targeted_regression cases passed; overall=pass`.
- Fresh runtime inventory probe thread `019f7481-73b0-71a1-895d-12e64fe3a0be` found exactly one `codex-project-workflow:codex-project-workflow` entry from R6 and no matching `.agents` path.
- `quick_validate.py` remains unavailable because the approved local Python runtimes lack `PyYAML`; no package installation was authorized or performed.

Outcome:

- Candidate status is `regression_passed_pending_activation_approval`.
- `activation.allowed=false` remains correct until a new evidence-bound explicit approval names CAND-15, its candidate hash, R6, the passing result, and the unchanged scope.
- The repository owner and R6 physically contain the candidate bytes for evaluation. The patch applies forward to the recorded base and reverse to the current worktree; this working-source state is deliberately distinct from the formal activation record.
- The prior CAND-14 failure evidence remains frozen and is not rewritten by this repair.

## DOGFOOD-21 CAND-15 Evidence-Bound Activation

Date: 2026-07-18

Scope: formally activate CAND-20260718-15 after the user approved the exact candidate ID, SHA-256, R6 runtime, `6/6` run and `2/2` case pass result, overall pass, and unchanged manifest scope.

Boundary:

- Changed only the candidate activation owner and current-state documentation.
- Did not change `SKILL.md`, candidate bytes, patch, R6 cache, personal plugin source, marketplace, automatic recording, Hook, MCP, or historical evaluation evidence.
- Reused the already installed and enabled R6 because its content hash exactly matched the approved candidate; no reinstall or new cachebuster was needed.

Official and implementation evidence:

- The current Codex manual confirms that plugins are installed reusable instruction/tool bundles and can be selected explicitly; the local CLI reports the approved R6 plugin installed and enabled.
- The previously frozen official Skills/Subagents guidance and community runtime reports remain the external basis for trigger precision, bounded delegation, single-owner checks, and fresh-session pickup. No new external scope was added during activation.

Verification:

- Candidate, active owner, personal source, and R6 skill SHA-256 all equal `f8ee04f6ffb89286d630c9c725b7897ee258bbd4569bd78381c3388da273686a`; patch SHA-256 remains `77c812864c7176faf9e9ff96c5f66c8037dd739ea556f13b3cfb09f6bb142105`.
- CLEAN7 remains `2/2` pass and FULL remains `6/6` runs, `2/2` cases, `overall=pass`.
- R6 is installed and enabled, explicit-version smoke passes, and the runtime inventory has one matching owner with no `.agents` skill path.

Outcome:

- Candidate status is `activated`.
- `activation.allowed=true`, `formal_activation_recorded=true`, and R6 is recorded as `activated_runtime`.
- The exact approval text and activation timestamp are stored in the candidate manifest.

## DOGFOOD-22 Post-Update R6 App Runtime Recheck

Date: 2026-07-22

Scope: complete the previously quota-blocked post-activation runtime-owner recheck after the Codex App updated to `26.715.9868.0` and the local CLI updated to `0.145.0-alpha.30`.

Boundary:

- Used one isolated, no-context App Agent for the runtime inventory and the main Agent for deterministic local verification.
- Did not rerun the six model cases; the accepted 2026-07-18 FULL batch remains the formal behavior baseline and was revalidated from its frozen artifacts.
- Did not change the candidate manifest, `SKILL.md`, personal plugin source, R6 cache, marketplace, Hook, MCP, or automatic recording behavior.
- Standalone CLI marketplace repair was explicitly out of scope.

Official and community evidence:

- The refreshed [official Codex manual](https://developers.openai.com/codex/codex-manual.md) states that plugins provide reusable instructions/connections, `codex plugin` operates on configured marketplace sources, and `CODEX_HOME` owns CLI/app-server state; its `codex exec` guidance assumes the invoked plugin has been provisioned in that run's `CODEX_HOME`.
- Rechecked the bounded community reports for [project-local filtering](https://github.com/openai/codex/issues/20210), [duplicate same-name skills](https://github.com/openai/codex/issues/25324), and [resume versus fresh-session context](https://github.com/openai/codex/issues/17560). They remain supporting reports rather than authoritative instructions.

Verification:

- The isolated App Agent reported `exact_name_matches=1`, the R6 cache skill locator, visible R6 runtime metadata, and `matching_agents_path=false`.
- Candidate, repository owner, and R6 normalized SHA-256 remain `f8ee04f6ffb89286d630c9c725b7897ee258bbd4569bd78381c3388da273686a`; repository, personal source, and cache retain seven-file parity.
- R6 explicit-version smoke passed with governance `2484/2`, research `1205/2`, and verification `2239/2`.
- Script tests passed `71/71`, root tests passed `12/12`, evaluation fixtures passed `36 cases / 148 assertions`, full fixtures passed `31/31 cases / 61 variants`, and skill structure remained valid.
- CLEAN7 and FULL frozen result artifacts both passed `validate_full_results.py`; FULL remains `6/6` runs, `2/2` cases, `overall=pass`.
- Standalone CLI reported zero installed/available plugins and zero `codex-project-workflow` prompt-input matches while the user config remained enabled and the R6 cache existed. This is an observed runtime-surface difference, not an App-owner failure.

Outcome:

- Post-update App runtime ownership passed with one R6 owner and no `.agents` duplicate.
- CAND-15 remains formally activated without manifest or runtime-byte changes.
- A future request may separately investigate standalone CLI marketplace / `CODEX_HOME` parity; this run did not authorize or perform that repair.
