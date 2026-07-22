# Productization Status

Historical snapshot date: 2026-06-22

## Historical Status

The plugin install smoke has passed and the final productization documents have been added.

## Added Documents

- `README.md`
- `docs/PRODUCT_MANUAL.md`
- `docs/TASK_TEMPLATES.md`
- `docs/INSTALL_UPDATE.md`
- `docs/EXTENSION_ROADMAP.md`

## Historical Scope

This stage is documentation and source-package README work only.

No active skill rule, plugin manifest, marketplace entry, installed cache, Hook, MCP server, app connector, or custom agent manifest was changed.

## Historical Next Step

Use the plugin on real tasks and record only evidence-backed improvement candidates.

## DOGFOOD-02 Update

The project now has `docs/DOCUMENT_INDEX.md` as the document navigation entry and `docs/DOGFOOD_LOG.md` as the record for self-use reviews.

The current baseline treats `README.md`, `docs/PRODUCT_MANUAL.md`, `docs/TASK_TEMPLATES.md`, `docs/INSTALL_UPDATE.md`, and `docs/PLUGIN_INSTALL_SMOKE.md` as current-state documents. Older planning and packaging documents are retained as historical/development evidence.

## Public Release Preparation Update 2026-07-22

- The repository and plugin package now carry the MIT License.
- `.agents/plugins/marketplace.json` exposes the repository's single plugin source for public installation.
- `scripts/build_plugin_release.py` validates the package boundary and creates a deterministic ZIP plus SHA-256 file.
- GitHub validation workflow and issue templates are present in `.github/`.
- Local release build and repository tests pass.
- At this preparation checkpoint, commit, push, tag creation, remote CI, and the GitHub Release remained separate external actions.

## Current Public Repository State 2026-07-22

- GitHub confirms `ajowyz/codex-project-workflow` is public and uses `master` as its default branch.
- The repository marketplace `ajowyz-codex`, public plugin manifest `0.1.0`, MIT license, validation workflow, issue templates, release builder, and release instructions are present on `master`.
- The latest observed “Validate public plugin” workflow completed successfully and produced the release artifact; its Node.js 20 deprecation warning is a follow-up maintenance item rather than a failed validation.
- The deterministic local ZIP SHA-256 is `b1d2e3c6ff59804e8a8b5a4ba771ffea4f2f8e81d8a9ffff664a35c9e23e5732`, matching its generated checksum file.
- GitHub currently has no tag and no Release. `CHANGELOG.md` therefore correctly remains under `[Unreleased]`.
- A consumer-side clean install and fresh-task pickup from the public source remain unverified and must not be inferred from the maintainer's activated R6 cache or from CI success alone.
