# Plugin Install Smoke

## Current Acceptance Snapshot

Date: 2026-07-18

Current installed target:

- Version: `0.1.0+codex.cand-20260718-15-r6`
- Cache root: `C:\Users\w\.codex\plugins\cache\personal\codex-project-workflow\0.1.0+codex.cand-20260718-15-r6`
- Repository source owner: `D:\project\codex\codex_project_workflow\plugins\codex-project-workflow\skills\codex-project-workflow\SKILL.md`
- Project-local discoverable skill: absent; `.agents/skills/codex-project-workflow/` is evaluation/protocol infrastructure only.

Current acceptance facts:

- The explicit-version repository smoke passed for `0.1.0+codex.cand-20260718-15-r6` and loaded the skill, helper, and three protocol files from that one cache directory.
- Protocol metrics remain governance `2484/2`, research `1205/2`, and verification `2239/2`.
- Pre-activation fresh CLI R6 regressions loaded exactly one `codex-project-workflow:codex-project-workflow` entry; E32 negative control loaded no body/reference, while the standard case loaded only the candidate body and successful verification selection. A separate pre-activation fresh runtime inventory probe in thread `019f7481-73b0-71a1-895d-12e64fe3a0be` also found exactly one match, the R6 cache locator, and no matching `.agents` path.
- CAND-15 now records `activated` with `activation.allowed=true`; the evidence-bound user approval, not smoke alone, granted formal activation.
- The already-open Codex App task can retain its startup-time plugin inventory and may still report an older cache. That is a task-context refresh boundary, not proof that the new cache failed to install.
- Official Python plugin/skill validators were unavailable because the current Python runtimes do not include `PyYAML`. Project strict validators and install smoke passed; this record does not relabel the official validator as passed.

The 2026-07-13 sections below are retained as historical migration evidence. They do not describe the current installed version or the current `.agents` ownership model.

Date: 2026-07-13

## Status

Passed.

The `codex-project-workflow` plugin was migrated to the new computer through the personal plugin source and Codex App, then verified with the repository install smoke script and a fresh-thread pickup. The installed cache copy loaded instead of the project-local `.agents` copy.

## Verified Installed Source

- Version: `0.1.0+codex.20260712082233`
- Skill path: `C:\Users\w\.codex\plugins\cache\personal\codex-project-workflow\0.1.0+codex.20260712082233\skills\codex-project-workflow\SKILL.md`
- Helper path: `C:\Users\w\.codex\plugins\cache\personal\codex-project-workflow\0.1.0+codex.20260712082233\skills\codex-project-workflow\scripts\read_reference.py`
- References path: `C:\Users\w\.codex\plugins\cache\personal\codex-project-workflow\0.1.0+codex.20260712082233\skills\codex-project-workflow\references`
- Project-local copy present but not used for this smoke: `D:\project\codex\codex_project_workflow\.agents\skills\codex-project-workflow\SKILL.md`

## Prepared Assets

- Personal marketplace entry: `%USERPROFILE%/.agents/plugins/marketplace.json`
- Personal plugin source: `%USERPROFILE%/plugins/codex-project-workflow`
- Marketplace name: `personal`
- Plugin install target: `codex-project-workflow@personal`

## Installed Cache Checks

- The repository smoke script selected installed cache version `0.1.0+codex.20260712082233`.
- The skill path came from the plugin cache path.
- The helper path came from the plugin cache path.
- The helper reads plugin-local `references/` first through `Path(__file__).resolve().parent.parent / "references" / name`.
- The installed cache and repository plugin source matched SHA-256 for the 7 core files: skill, helper, three references, plugin README, and user guide.
- `governance` loaded `Execution Rules` and `Output Requirements`; metrics: `codepoints=2484 h2_sections=2`.
- `research` loaded `Execution Rules` and `Output Requirements`; metrics: `codepoints=1205 h2_sections=2`.
- `verification` loaded `Execution Rules` and `Output Requirements`; metrics: `codepoints=2239 h2_sections=2`.

## Fresh-Thread Pickup Checks

- Fresh-thread smoke thread: `019f5979-2a17-7c80-871e-8cecbcfa3c4e`.
- Thread status: completed and idle.
- The fresh thread reported that the visible `codex-project-workflow` skill came from installed plugin cache version `0.1.0+codex.20260712082233`.
- The reported skill path was `C:\Users\w\.codex\plugins\cache\personal\codex-project-workflow\0.1.0+codex.20260712082233\skills\codex-project-workflow\SKILL.md`.
- The fresh thread reported that helper execution and path evidence came from installed plugin cache, not the previous computer path and not the project `.agents` copy.
- The fresh thread ran the repository smoke with the new computer's Codex bundled Python; it passed with `PLUGIN INSTALL SMOKE: PASS`.
- Fresh-thread protocol metrics matched the installed cache check: `governance` `codepoints=2484 h2_sections=2`, `research` `codepoints=1205 h2_sections=2`, and `verification` `codepoints=2239 h2_sections=2`.
- Fresh-thread Git status showed a clean `master`; HEAD and local `origin/master` were both `2af7e23e3cfe20fff5cc81d37bbcd1965bc9efbf`, with `0/0` divergence.
- The smoke remained read-only and left the worktree clean.

## Repeatable Check

Run this read-only check after reinstalling or updating the plugin:

```text
python scripts/verify_plugin_install_smoke.py
```

On the current new computer, bare `python` in an ordinary PowerShell session may resolve to an invalid Microsoft Store alias. Use an available Python 3 executable, including the Codex bundled Python used by the verified smoke, before treating a command-launch failure as a plugin failure.

The script verifies that `SKILL.md`, `scripts/read_reference.py`, and `references/{governance,research,verification}.md` are all under the same installed plugin cache version directory, then runs the helper for all three references from a temporary directory so the project `.agents` fallback cannot satisfy the check.

Expected successful output includes:

- `PLUGIN INSTALL SMOKE`
- selected cache version and installed paths
- `fallback guard: helper is executed from a temporary directory`
- metrics for `governance`, `research`, and `verification`
- `PLUGIN INSTALL SMOKE: PASS`

Failures should print `PLUGIN INSTALL SMOKE: FAIL`, a reason, and next steps.

## Historical Note

The direct command below failed in the original desktop thread because the packaged Codex CLI executable returned `Access is denied`:

```text
codex plugin add codex-project-workflow@personal
```

That was a local executable permission issue, not a plugin package validation failure. Enabling through Codex App and verifying in a fresh thread completed the install smoke.

## Historical DOGFOOD-16 Source Update on the Previous Computer

This section preserves the previous computer's 2026-07-03 evidence. It is not the current new-computer installed state.

After DOGFOOD-16, the repository source was copied to the personal plugin source with:

```text
python scripts\prepare_plugin_update.py --apply --apply-cachebuster
```

Prepared and installed personal plugin source version:

```text
0.1.0+codex.20260703113254
```

The command validated the personal marketplace entry and did not modify marketplace or installed plugin cache. Reinstall through CLI was attempted with both `codex plugin list` and `codex plugin add codex-project-workflow@personal`, but the packaged WindowsApps `codex` executable returned `Access is denied`.

Codex App plugin page re-enable produced an installed cache that selects:

```text
0.1.0+codex.20260703113254
```

The repository install smoke and fresh-thread pickup smoke both passed for this version.

## Remaining Gates

- For the next source change, repeat `python scripts\prepare_plugin_update.py --apply --apply-cachebuster`, supported plugin reinstall, explicit-version `python scripts\verify_plugin_install_smoke.py --version-dir <cache-dir>`, and a fresh-process pickup check.
- If only the already-open App task shows an old path, start a genuinely new top-level App task or restart the App before claiming App pickup; do not rewrite the older task's evidence.
- Automatic recording, Hook, MCP, app connector, and silent self-update remain out of scope.
