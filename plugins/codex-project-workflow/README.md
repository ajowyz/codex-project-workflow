# Codex Project Workflow Plugin

This plugin packages the `codex-project-workflow` skill as a portable, source-controlled Codex plugin.

## Contents

- `.codex-plugin/plugin.json`
- `skills/codex-project-workflow/SKILL.md`
- `skills/codex-project-workflow/references/research.md`
- `skills/codex-project-workflow/references/governance.md`
- `skills/codex-project-workflow/references/verification.md`
- `skills/codex-project-workflow/scripts/read_reference.py`
- `docs/USER_GUIDE.md`

## Scope

The first release is a pure skill plugin. It intentionally does not include hooks, MCP servers, app connectors, custom agent manifests, eval workspaces, run logs, personal memory, private paths, or project execution history.

## Runtime Notes

Use the helper from the loaded skill directory:

```text
python <skill_dir>/scripts/read_reference.py governance "Execution Rules" "Output Requirements"
```

The helper checks the plugin-local `references/` directory first. A development-repo fallback remains only for local source-tree use when `.agents/skills/codex-project-workflow/references/` exists in the current working directory.

## Validation

Before publishing or installing this plugin, validate the manifest, the packaged skill, the helper path, and the absence of excluded assets. The official plugin validator should be used when its Python dependencies are available.

From this repository root, the current verified package can be checked with:

```text
python scripts/verify_plugin_install_smoke.py
```

See the source repository docs for the full manual, task templates, install/update notes, and extension roadmap.
