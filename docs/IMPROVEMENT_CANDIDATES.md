# 改进候选台账

本文件记录 `codex-project-workflow` 在真实使用中暴露出的可改进信号。它不是生效规则，也不是自动更新记录；只有经过证据、回归和用户确认的改动，才可以进入插件源包或安装更新流程。

## 使用边界

- 记录问题、证据、影响、候选修复和验证门。
- 不保存完整聊天记录、私有源码或不必要的敏感上下文。
- 不因为记录了候选就自动修改 `SKILL.md`、reference、plugin manifest、marketplace 或已安装 cache。
- 可以把候选分流到文档、模板、脚本、测试或技能源包；分流前要说明范围和回归方式。

## 记录模板

```text
ID:
Date:
Trigger signal:
Scope: task | project | personal | plugin
Observed behavior:
Expected behavior:
Evidence:
Impact:
Candidate target: docs | template | script | test | skill source | reference | manifest
Minimal fix:
Regression gate:
Activation or update gate:
Invalidation:
Status:
```

## DOGFOOD-16 Local-Use Improvement Capture

Date: 2026-07-03

Trigger signal:

- 用户询问“插件在本地使用过程中发现了问题能不能自动更新，是否有这个功能”。

Scope:

- Project-level dogfood signal with plugin workflow implications.

Observed behavior:

- 项目已有“候选改进”模板和 P2 路线，但没有一个当前正式入口里的候选台账。
- 安装/更新脚本能准备真实更新，但没有把“本次更新是否来自候选或 dogfood 记录”作为显式收尾提醒。
- 源插件 `SKILL.md` 的收尾要求强调验证结果/路径，但没有明确要求在流程、模板、安装或更新类任务中检查真实验收动作是否已经完成。

Expected behavior:

- 本地使用中发现的问题先进入可审查候选。
- 低风险修复可以进入仓库源文件并回归验证。
- 安装或启用仍保持人工确认，不静默自更新。

Evidence:

- `README.md` 已把“可复用经验沉淀为候选改进，经过证据和回归后再激活”列为目标。
- `docs/TASK_TEMPLATES.md` 已有“候选改进沉淀”模板。
- `docs/EXTENSION_ROADMAP.md` 的 P2 改进候选机制要求记录失败、人工干预和重复模式，并明确“不让插件静默修改自己”。
- `docs/INSTALL_UPDATE.md` 和 `scripts/prepare_plugin_update.py` 已提供半自动更新准备流程。

Impact:

- 如果没有台账，问题容易留在对话里，后续更新时难以证明来源、范围和回归门。
- 如果把“自动捕获问题”和“自动更新插件”混在一起，可能绕过用户确认和安装 smoke。

Candidate target:

- `docs/IMPROVEMENT_CANDIDATES.md`
- `docs/TASK_TEMPLATES.md`
- `docs/DOCUMENT_INDEX.md`
- `docs/INSTALL_UPDATE.md`
- `docs/EXTENSION_ROADMAP.md`
- `plugins/codex-project-workflow/skills/codex-project-workflow/SKILL.md`
- `scripts/prepare_plugin_update.py`
- `scripts/test_prepare_plugin_update.py`

Minimal fix:

- 新增候选台账。
- 让候选沉淀模板要求写入台账或说明不写入原因。
- 让源插件收尾时检查流程/模板/安装/更新类任务的真实验收动作。
- 让更新准备脚本输出候选来源和验收记录提醒。

Regression gate:

- `python -m unittest discover -s scripts -p "test_*.py"`
- `python scripts\prepare_plugin_update.py`
- `python scripts\verify_plugin_install_smoke.py`
- `git diff --check`

Activation or update gate:

- 仓库修复通过后，若要让已安装插件生效，仍需运行 `python scripts\prepare_plugin_update.py --apply --apply-cachebuster`、通过 Codex App 或 CLI 重新启用插件、新开线程 smoke，并记录新 cache 版本。

Invalidation:

- 如果未来引入受控自动化，也不能跳过候选、回归、用户确认和安装 smoke；只能把自动化限定在生成候选、报告或待确认补丁。

Status:

- Applied to repository source and installed cache `0.1.0+codex.20260703113254`; fresh-thread pickup smoke passed in thread `019f27c3-179b-7220-a045-15094edcf86a`.
