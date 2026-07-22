# Codex Project Workflow Plugin

This plugin packages the `codex-project-workflow` skill as a portable, source-controlled Codex plugin.

## Install From The Public Repository

Clone the repository, then add its local marketplace and install the plugin:

```text
git clone https://github.com/ajowyz/codex-project-workflow.git
codex plugin marketplace add <absolute-path-to-cloned-repository>
codex plugin add codex-project-workflow@ajowyz-codex
```

Start a new top-level Codex thread after installing or updating so the new thread picks up the current plugin. The repository root README contains the shortest installation smoke prompt.

## License

This plugin is released under the [MIT License](LICENSE).

## Contents

- `.codex-plugin/plugin.json`
- `skills/codex-project-workflow/SKILL.md`
- `skills/codex-project-workflow/references/research.md`
- `skills/codex-project-workflow/references/governance.md`
- `skills/codex-project-workflow/references/verification.md`
- `skills/codex-project-workflow/scripts/read_reference.py`
- `docs/USER_GUIDE.md`
- `LICENSE`

## Scope

The first release is a pure skill plugin. It intentionally does not include hooks, MCP servers, app connectors, custom agent manifests, eval workspaces, run logs, personal memory, private paths, or project execution history.

## Runtime Notes

Use the helper from the loaded skill directory:

```text
python <skill_dir>/scripts/read_reference.py governance "Execution Rules" "Output Requirements"
```

The helper checks the plugin-local `references/` directory first. A development-repo fallback remains only for local source-tree use when `.agents/skills/codex-project-workflow/references/` exists in the current working directory.

## Minimal Use

After enabling the plugin, start a new Codex thread and describe the task naturally. For example:

```text
Continue this project. First review the current state, plan, and git status, then decide the next step.
```

For implementation tasks where the path matters, add:

```text
After finishing, prove that the result went through the original project entry and owner path.
```

For professional research or solution comparison, add:

```text
First explain what sources, methods, and alternatives you will compare. Ask before browsing.
```

For a long conversation or a handoff to a fresh thread, use:

```text
I am moving a long project conversation into this fresh thread. Do not rely only on the old chat or a compact summary. First recover the project state from the project entry docs, plan or status docs, and git status. Report the current goal, completed work, next step, blockers, risks, and any missing or conflicting evidence before editing files.
```

## Install Smoke

After install or update, use a fresh Codex thread to verify that the loaded skill path comes from the plugin cache and that `governance`, `research`, and `verification` can be read through the plugin-local helper.

## Validation

Before publishing or installing this plugin, validate the manifest, the packaged skill, the helper path, and the absence of excluded assets. The official plugin validator should be used when its Python dependencies are available.

From this repository root, the current verified package can be checked with:

```text
python scripts/verify_plugin_install_smoke.py
```

If the full source repository is available, see `docs/DOCUMENT_INDEX.md` for the manual, task templates, install/update notes, and extension roadmap.
