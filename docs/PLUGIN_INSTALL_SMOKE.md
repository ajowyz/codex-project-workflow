# Plugin Install Smoke

Date: 2026-07-03

## Status

Passed.

The `codex-project-workflow` plugin was updated through the personal plugin source and Codex App, then verified with the repository install smoke script. The installed cache copy loaded instead of the project-local `.agents` copy.

## Verified Installed Source

- Version: `0.1.0+codex.20260703113254`
- Skill path: `C:\Users\wang yazhou\.codex\plugins\cache\personal\codex-project-workflow\0.1.0+codex.20260703113254\skills\codex-project-workflow\SKILL.md`
- Helper path: `C:\Users\wang yazhou\.codex\plugins\cache\personal\codex-project-workflow\0.1.0+codex.20260703113254\skills\codex-project-workflow\scripts\read_reference.py`
- References path: `C:\Users\wang yazhou\.codex\plugins\cache\personal\codex-project-workflow\0.1.0+codex.20260703113254\skills\codex-project-workflow\references`
- Project-local copy present but not used for this smoke: `D:\project\efficiently use codex\.agents\skills\codex-project-workflow\SKILL.md`

## Prepared Assets

- Personal marketplace entry: `%USERPROFILE%/.agents/plugins/marketplace.json`
- Personal plugin source: `%USERPROFILE%/plugins/codex-project-workflow`
- Marketplace name: `personal`
- Plugin install target: `codex-project-workflow@personal`

## Installed Cache Checks

- The repository smoke script selected installed cache version `0.1.0+codex.20260703113254`.
- The skill path came from the plugin cache path.
- The helper path came from the plugin cache path.
- The helper reads plugin-local `references/` first through `Path(__file__).resolve().parent.parent / "references" / name`.
- `governance` loaded `Execution Rules` and `Output Requirements`; metrics: `codepoints=2484 h2_sections=2`.
- `research` loaded `Execution Rules` and `Output Requirements`; metrics: `codepoints=1205 h2_sections=2`.
- `verification` loaded `Execution Rules` and `Output Requirements`; metrics: `codepoints=2239 h2_sections=2`.

## Fresh-Thread Pickup Checks

- Fresh-thread smoke thread: `019f27c3-179b-7220-a045-15094edcf86a`.
- Thread status: completed and idle.
- The fresh thread reported that the visible `codex-project-workflow` skill came from installed plugin cache version `0.1.0+codex.20260703113254`.
- The reported skill path was `C:\Users\wang yazhou\.codex\plugins\cache\personal\codex-project-workflow\0.1.0+codex.20260703113254\skills\codex-project-workflow\SKILL.md`.
- The fresh thread reported that helper execution and path evidence came from installed plugin cache, not the old `0.1.0+codex.20260703085220` cache and not the project `.agents` copy.
- The fresh thread also ran `python scripts\verify_plugin_install_smoke.py`; it passed with `PLUGIN INSTALL SMOKE: PASS`.
- Fresh-thread protocol metrics matched the installed cache check: `governance` `codepoints=2484 h2_sections=2`, `research` `codepoints=1205 h2_sections=2`, and `verification` `codepoints=2239 h2_sections=2`.
- Fresh-thread git status showed the existing uncommitted project changes and was unchanged by the read-only smoke.

## Repeatable Check

Run this read-only check after reinstalling or updating the plugin:

```text
python scripts/verify_plugin_install_smoke.py
```

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

## DOGFOOD-16 Source Update Completion

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

- For the next source change, repeat `python scripts\prepare_plugin_update.py --apply --apply-cachebuster`, Codex App re-enable, and `python scripts\verify_plugin_install_smoke.py`.
