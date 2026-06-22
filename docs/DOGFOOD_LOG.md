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
