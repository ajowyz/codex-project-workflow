# 更高效严谨地使用 Codex

本项目产出一个可安装的 Codex 插件 `codex-project-workflow`，以及一套配套文档，用来让 Codex 在复杂项目中更快、更准、更专业地工作。

它的目标不是让 Codex 预先精通所有领域，而是让 Codex 在具体任务中更稳定地完成这些动作：

- 先理解目标、范围、约束和完成标准。
- 主动判断是否需要研究、方案比较、多 Agent 或人工确认。
- 在需要专业判断时获取资料、比较方案和说明依据。
- 实现时验证结果，也验证有没有绕过项目原有入口和 owner 路径。
- 把可复用经验沉淀为候选改进，经过证据和回归后再激活。

## 当前状态

- 插件源包：`plugins/codex-project-workflow/`
- 当前模型与推理强度：`gpt-5.6-sol` / `xhigh`
- 当前正式回归运行环境：Codex App `26.715.3651.0`，Codex CLI `0.145.0-alpha.18`
- 已验证的候选插件 cache 版本：`0.1.0+codex.cand-20260718-15-r6`
- 已验证的候选插件 cache 根目录：`C:\Users\w\.codex\plugins\cache\personal\codex-project-workflow\0.1.0+codex.cand-20260718-15-r6`
- 当前仓库：`D:\project\codex\codex_project_workflow`；实时 HEAD 与分支同步状态以 `git status --short --branch` 和 `git rev-parse HEAD` 为准，不在本文档中硬编码为当前值。
- 可重复 smoke 脚本：`python scripts/verify_plugin_install_smoke.py`

源与运行时的所有权关系已经收敛：仓库内 `plugins/codex-project-workflow/` 是唯一源；installed cache 是由正式安装流程生成的运行时副本；`.agents/skills/codex-project-workflow/` 只保留评估夹具和协议镜像，不再包含可发现的 `SKILL.md`。

[官方 Skills 文档](https://learn.chatgpt.com/docs/build-skills)给出的 project config 与 `skills.config` 是预期配置契约，但当前运行时不能依赖 project-local skill filtering；本项目的实测与 [openai/codex#20210](https://github.com/openai/codex/issues/20210) 一致，因此采用“移除重复发现入口”的单一所有者方案。当前已经运行的 Codex App 任务可能保留旧插件清单快照；fresh CLI 进程已看到上述新 cache。需要核对 App UI 时，应新开顶层任务或重启 App，再检查清单，不能把旧任务快照当成安装失败。

本轮 P1 已完成单一源与运行时所有权收敛；P2 的修复候选 `CAND-20260718-15` 已完成 2 项定向和 6 项完整 GPT-5.6 干净回归，逐运行 `6/6`、聚合 `2/2`、`overall=pass`。fresh CLI 只发现 1 个匹配入口，R6 安装 smoke 通过。仓库唯一 owner 与 R6 当前都承载候选哈希用于评估，但治理状态仍是 `regression_passed_pending_activation_approval`、`activation.allowed=false`；物理候选内容和测试安装态不能描述为正式激活。P3 文档同步已完成。自动记录、Hook 与 MCP 均未加入本轮范围，当前记录能力仍是显式、人工触发的文档记录。

当前普通 PowerShell 的裸 `python` 可能命中无效的 Microsoft Store 别名。若裸命令失败，应先使用可执行的 Python 3 路径，不要把环境入口问题误判为插件失败。

## 从这里开始

如果不知道该看哪个文档，先看：`docs/DOCUMENT_INDEX.md`

1. 阅读最终使用手册：`docs/PRODUCT_MANUAL.md`
2. 复制常用任务模板：`docs/TASK_TEMPLATES.md`
3. 安装、更新或复验插件：`docs/INSTALL_UPDATE.md`
4. 查看后续扩展路线：`docs/EXTENSION_ROADMAP.md`

## 最常用的启动方式

在启用了插件的新 Codex 线程中，可以直接这样说：

```text
继续推进当前项目。先复核当前状态、计划和 git 状态，再判断下一步。
```

或者在新项目中这样说：

```text
我要启动一个新项目。请先帮我做需求访谈、风险判断和下一步计划，不要直接给最终方案。
```

如果你担心 Codex 绕过原项目逻辑，可以明确加上：

```text
完成后请证明不是只生成了正确输出，而是通过项目原有入口和 owner 路径实现。
```

## 复验插件

插件更新、重装或模型环境变化后，先运行：

```powershell
python scripts\verify_plugin_install_smoke.py
```

通过后再开新任务做真实任务。若当前 App 任务仍显示旧 cache，先新开顶层任务或重启 App 以刷新插件清单；fresh CLI 进程的运行时所有者检查可作为独立复验。
