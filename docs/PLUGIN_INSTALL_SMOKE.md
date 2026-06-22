# Plugin Install Smoke

Date: 2026-06-22

## Status

Passed.

The `codex-project-workflow` plugin was enabled through Codex App and verified in a fresh thread. The fresh-thread run loaded the plugin cache copy instead of the project-local `.agents` copy.

## Verified Installed Source

- Skill path: `C:\Users\wang yazhou\.codex\plugins\cache\personal\codex-project-workflow\0.1.0+codex.20260622112058\skills\codex-project-workflow\SKILL.md`
- Helper path: `C:\Users\wang yazhou\.codex\plugins\cache\personal\codex-project-workflow\0.1.0+codex.20260622112058\skills\codex-project-workflow\scripts\read_reference.py`
- References path: `C:\Users\wang yazhou\.codex\plugins\cache\personal\codex-project-workflow\0.1.0+codex.20260622112058\skills\codex-project-workflow\references`
- Project-local copy present but not used for this smoke: `D:\project\efficiently use codex\.agents\skills\codex-project-workflow\SKILL.md`

## Prepared Assets

- Personal marketplace entry: `%USERPROFILE%/.agents/plugins/marketplace.json`
- Personal plugin source: `%USERPROFILE%/plugins/codex-project-workflow`
- Marketplace name: `personal`
- Plugin install target: `codex-project-workflow@personal`

## Fresh-Thread Checks

- The fresh thread discovered and loaded `codex-project-workflow`.
- The loaded skill came from the plugin cache path.
- The helper came from the plugin cache path.
- The helper reads plugin-local `references/` first through `Path(__file__).resolve().parent.parent / "references" / name`.
- `governance` loaded `Execution Rules` and `Output Requirements`; metrics: `codepoints=2484 h2_sections=2`.
- `research` loaded `Execution Rules` and `Output Requirements`; metrics: `codepoints=1205 h2_sections=2`.
- `verification` loaded `Execution Rules` and `Output Requirements`; metrics: `codepoints=2239 h2_sections=2`.

## Repeatable Check

Run this read-only check after reinstalling or updating the plugin:

```text
python scripts/verify_plugin_install_smoke.py
```

The script verifies that `SKILL.md`, `scripts/read_reference.py`, and `references/{governance,research,verification}.md` are all under the same installed plugin cache version directory, then runs the helper for all three references from a temporary directory so the project `.agents` fallback cannot satisfy the check.

## Historical Note

The direct command below failed in the original desktop thread because the packaged Codex CLI executable returned `Access is denied`:

```text
codex plugin add codex-project-workflow@personal
```

That was a local executable permission issue, not a plugin package validation failure. Enabling through Codex App and verifying in a fresh thread completed the install smoke.

## Remaining Gates

- Prepare final user-facing docs and task templates.
- Decide the next extension path: install/update automation, better first-run smoke UX, or broader real-project exercises.
