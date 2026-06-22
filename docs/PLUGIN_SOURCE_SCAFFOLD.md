# Plugin Source Scaffold

Date: 2026-06-22

## Status

The first repo-local plugin source package exists at `plugins/codex-project-workflow/`.

This document describes the source package in this repository. Installation status is tracked separately in `docs/PLUGIN_INSTALL_SMOKE.md`.

Current source package status: created and install-smoke verified through the personal plugin flow.

## Included

- `.codex-plugin/plugin.json`
- `skills/codex-project-workflow/SKILL.md`
- `skills/codex-project-workflow/references/research.md`
- `skills/codex-project-workflow/references/governance.md`
- `skills/codex-project-workflow/references/verification.md`
- `skills/codex-project-workflow/scripts/read_reference.py`
- `README.md`
- `docs/USER_GUIDE.md`

## Excluded

- Hooks
- MCP servers
- App connectors
- Custom agent manifests
- Personal marketplace entries
- Installed plugin cache changes
- Eval workspaces
- Regression run logs
- Rollout logs
- Personal memory
- Private paths
- Project execution history

## Completed Gates

- Validate plugin manifest shape.
- Validate packaged skill frontmatter and required references.
- Prove `read_reference.py` can read plugin-local references.
- Prove excluded assets are absent from the package.
- Run an install smoke in a fresh Codex thread before treating this as install-ready.

## Install Smoke Update

See `docs/PLUGIN_INSTALL_SMOKE.md` for the completed installation smoke. The plugin was enabled through Codex App and verified in a fresh thread from the plugin cache path, not the project-local `.agents` copy.

## Validator Note

The official `validate_plugin.py` script currently requires `PyYAML`. If that dependency is unavailable, use local structural checks as a temporary fallback and rerun the official validator once the dependency is available.
