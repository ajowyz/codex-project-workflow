# Plugin Install Smoke

Date: 2026-06-22

## Status

The personal plugin source and default personal marketplace entry have been prepared.

The install command is currently blocked by the local Codex Desktop CLI executable returning `Access is denied`.

## Prepared Assets

- Personal marketplace entry: `%USERPROFILE%/.agents/plugins/marketplace.json`
- Personal plugin source: `%USERPROFILE%/plugins/codex-project-workflow`
- Marketplace name: `personal`
- Plugin install target: `codex-project-workflow@personal`

## Completed Checks

- The marketplace entry points to `./plugins/codex-project-workflow`.
- The personal plugin manifest is valid JSON.
- The personal plugin version has a Codex cachebuster suffix.
- The packaged helper reads plugin-local `references/`.
- Exclusion scan found no eval workspaces, regression run markers, candidate history, smoke/calibration logs, TODO placeholders, or absolute Windows paths.
- The official plugin validator core path passed with a temporary YAML shim.

## Blocked Check

The following command could not run in this desktop thread:

```text
codex plugin add codex-project-workflow@personal
```

Observed result:

```text
Access is denied
```

This appears to be a local executable permission issue for the Codex Desktop packaged CLI, not a plugin package validation failure.

## Remaining Gates

- Install or enable the plugin through the Codex app or a CLI environment that can execute `codex`.
- Start a new Codex thread after installation.
- Verify the new thread discovers `codex-project-workflow` from the installed plugin.
- Verify the installed skill can load `governance`, `research`, and `verification` through plugin-local `read_reference.py`.
