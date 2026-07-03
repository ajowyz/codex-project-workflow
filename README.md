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
- 插件安装 smoke：已通过
- 已验证的插件 cache 版本：`0.1.0+codex.20260703113254`
- 可重复 smoke 脚本：`python scripts/verify_plugin_install_smoke.py`

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

通过后再开新线程做真实任务。
