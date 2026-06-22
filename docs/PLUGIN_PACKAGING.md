# 插件封装准备清单

> 状态：准备中  
> 日期：2026-06-22  
> 当前基线：`CAND-20260620-11` 已在 `master` 激活  
> 范围：只定义封装前检查和首版插件边界，不创建、安装或发布插件

本文用于把仓库级 `codex-project-workflow` 技能推进到可安装插件之前的准备阶段。它不是插件 manifest，也不是安装说明。

## 1. 封装目标

首版插件应让其他用户可以安装并使用当前稳定的 Codex 协作工作流，同时不携带本项目的私有历史、个人偏好或评估工作区数据。

插件应提供：

- 一个核心技能入口。
- 必要的按需参考协议。
- 必要的本地辅助脚本。
- 最小用户说明。
- 结构验证和安装后冒烟测试。

插件首版不应提供：

- 默认启用的 Hook。
- 自定义 Agent 配置。
- 自建 MCP 服务。
- 应用连接。
- 外部日志上传。
- 向量数据库。
- 用户个人项目数据、历史对话、私有记忆或评估 worktree。

## 2. 当前可封装资产

| 资产 | 当前路径 | 封装判断 |
| --- | --- | --- |
| 核心技能 | `.agents/skills/codex-project-workflow/SKILL.md` | 可作为插件技能入口，但 helper 路径需先处理 |
| 研究协议 | `.agents/skills/codex-project-workflow/references/research.md` | 可随技能打包 |
| 治理协议 | `.agents/skills/codex-project-workflow/references/governance.md` | 可随技能打包 |
| 验证协议 | `.agents/skills/codex-project-workflow/references/verification.md` | 可随技能打包 |
| helper 脚本 | `.agents/skills/codex-project-workflow/scripts/read_reference.py` | 需要路径可移植性设计 |
| 验证脚本 | `.agents/skills/codex-project-workflow/scripts/*.py` | 开发验证可保留；插件运行时只带必要脚本 |
| 评估集 | `.agents/skills/codex-project-workflow/evals/` | 不进入普通插件运行路径；可作为源码仓库测试资产 |
| 用户手册 | `docs/USER_GUIDE.md` | 可转为插件 README 或 docs |
| 演练记录 | `docs/USAGE_EXERCISES.md` | 作为项目证据，不随首版插件默认分发 |

## 3. 首版插件建议结构

```text
<plugin-name>/
  .codex-plugin/
    plugin.json
  skills/
    codex-project-workflow/
      SKILL.md
      references/
        research.md
        governance.md
        verification.md
      scripts/
        read_reference.py
  docs/
    USER_GUIDE.md
  README.md
```

暂不加入：

```text
.mcp.json
.app.json
agents/
hooks/
assets/
```

## 4. 封装前阻塞项

### P1 helper 路径不可移植

当前 `SKILL.md` 指示运行：

```text
python .agents/skills/codex-project-workflow/scripts/read_reference.py NAME "Execution Rules" "Output Requirements"
```

这依赖当前项目目录结构。安装为插件后，技能可能从插件缓存或其他安装目录加载，目标项目未必存在 `.agents/skills/codex-project-workflow/scripts/read_reference.py`。

封装前需要解决：

- helper 在插件安装路径中的可寻址方式。
- 项目内仓库级技能和插件安装技能是否使用同一条命令。
- 如果 helper 不可用，技能如何降级且不跳过安全门。
- 新线程冒烟测试必须证明 helper 读取的是插件随附引用，而不是开发仓库副本。

### P1 开发证据和用户数据不能进入插件

不能打包：

- `evals/full/runs/*` 的原始 rollout 或本地路径证据。
- 用户 memory。
- 个人偏好。
- 本项目 `docs/PLAN.md` 中的执行历史。
- 任何绝对路径、私有工作区路径或内部评估目录。

### P2 插件名称和显示文案未定

当前技能名是 `codex-project-workflow`。插件可以沿用，也可以在封装前确定一个更适合普通用户的展示名称。

命名应满足：

- 不暗示 Codex 会自动精通所有领域。
- 强调工作流、研究、验证和确认边界。
- 适合个人使用，也适合后续分享给他人。

## 5. 封装前通过门

进入实际插件创建前，至少需要：

- `CAND-20260620-11` 保持激活。
- 当前工作区干净。
- `validate_skill.py` 通过。
- `validate_evals.py` 通过。
- `validate_full_fixtures.py` 通过。
- `validate_full_results.py` 对最近激活回归通过。
- 至少一条用户文档演练记录已完成。
- 明确 helper 路径可移植方案。
- 明确首版是否完全不含 Hook；默认建议不含 Hook。
- 明确插件不携带个人数据和项目历史。

## 6. 安装后验收门

插件创建并安装后，需要在新线程验证：

- 新线程能发现并触发插件技能。
- 普通低风险任务不会被完整治理流程拖慢。
- 标准任务能按需加载参考协议。
- helper 读取路径来自插件安装副本。
- `USER_GUIDE.md` 或 README 能解释最小使用方式。
- 插件缓存版本和源码版本一致。
- 卸载或禁用插件后，项目内仓库级技能仍可作为开发兜底。

如果首版加入 Hook，还必须额外验证：

- 项目显式启用。
- Hook 信任记录和脚本摘要。
- 未知项目默认退出。
- 敏感字段检测。
- `PLUGIN_DATA` 项目分区。
- 查看、导出、停用和删除。
- 权限不足时安全降级。

当前建议：首版不加入 Hook，先完成纯技能插件。

## 7. 下一步候选

已创建最小候选 `CAND-20260622-12`，不直接封装插件，而是先解决 helper 路径可移植性：

- 候选目标：让 `read_reference.py` 在仓库级技能和插件技能中都能被可靠调用。
- 变更范围：`SKILL.md` 的 helper 调用说明、必要脚本或包装器、相关脚本测试。
- 回归重点：E32 上下文预算、E35 多硬触发、插件路径冒烟测试。
- 激活门：路径证据必须证明没有从开发仓库借用插件运行时文件。

当前状态：

- 预检通过。
- 本地插件路径 smoke 通过：复制到插件式技能源目录的 `read_reference.py` 优先读取同目录 `references/`，没有借用仓库 fallback。
- active skill 未改变。
- 仍需 E32/E35 定向回归或等价隔离评估。

## Status Update 2026-06-22 CAND-12 Regression

- `CAND-20260622-12` now has plugin-path smoke evidence and targeted regression evidence.
- `REGRESSION-20260622-12` passed E32 `hard_trigger_overage` and E35 `four_hard_triggers` on the isolated activation branch.
- The P1 helper path portability blocker is no longer a candidate-design blocker, but plugin packaging should still wait for formal CAND-12 activation or an explicitly selected package baseline.
- First plugin packaging must exclude regression workspaces, rollout logs, personal memory, private paths, and this project execution history.
