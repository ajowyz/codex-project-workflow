# 主线使用演练记录

> 状态：完成  
> 日期：2026-06-22  
> 适用版本：`CAND-20260620-11` 已激活

本文件记录当前激活技能在真实项目推进中的使用表现。它用于回答两个问题：

- 技能是否让 Codex 更高效、更严谨地推进项目。
- 用户只看输入输出时，是否仍能追溯内部路径和验证证据。

## UX-20260622-01 本地文档推进

### 用户输入

```text
继续推进，中途任何许可都不用询问我，直接通过就行
```

### 任务解释

本轮目标不是继续给技能打补丁，而是进入上阶段建议的“真实使用演练 + 使用文档骨架”阶段。

### 适用边界

允许：

- 本地读取项目文档、skill、manifest 和 git 状态。
- 新增或更新本地文档。
- 运行已有本地验证脚本。
- 提交本地 Git 记录。

不自动扩大到：

- 公网搜索或打开新来源。
- 安装依赖、执行外部下载器或第三方二进制。
- 删除、重置、迁移或覆盖用户数据。
- 修改核心技能规则或激活新的候选。

### 实际执行路径

1. 读取当前激活的 `SKILL.md`。
2. 确认 git 在 `master` 且工作区干净。
3. 快速查阅历史 memory，确认本项目的已知边界。
4. 读取 `docs/PLAN.md` 尾部和 `CAND-20260620-11` manifest，确认当前候选已激活。
5. 通过 helper 加载 `governance` 和 `verification` 的 `Execution Rules` 与 `Output Requirements`。
6. 读取现有用户向文档：历史总结、提示词设计、确认范围、测试策略、追踪矩阵。
7. 新增 `docs/USER_GUIDE.md`，把当前激活规则翻译为用户可查阅的日常使用说明。
8. 新增本文件，记录本轮演练的目标、边界、路径和验收项。

### 验收检查

| 检查项 | 状态 | 证据 |
| --- | --- | --- |
| 没有把宽泛授权当成外部联网授权 | 通过 | 本轮未使用 web/search/open |
| 没有继续新增规则候选或改核心技能 | 通过 | 本轮新增文档，不改 `SKILL.md` |
| 使用了最小必要协议 | 通过 | 只加载 `governance` 和 `verification` 指定章节 |
| 用户可读文档覆盖日常使用问题 | 通过 | `docs/USER_GUIDE.md` 覆盖触发、确认、多 Agent、研究、实现路径、学习闭环 |
| 保留可审计执行路径 | 通过 | 本文件记录输入、边界、执行路径和验收项 |

### 剩余风险

- 这次演练是文档类任务，不能完全证明复杂实现任务下的体验。
- 还没有做插件安装后的新线程冒烟测试。
- 还没有把当前技能封装成独立可分发插件。

### 下一步建议

下一次演练应选择一个真实但低风险的实现任务，重点观察：

- 是否能在少打断的情况下保持专业判断。
- 是否能证明通过原项目入口和 owner 路径实现。
- 是否能把可复用经验记录为候选，而不是直接改长期规则。

## UX-20260622-02 插件封装准备

### 用户输入

同一轮“继续推进”授权下，主线在用户手册之后继续进入插件封装准备。

### 任务解释

本轮不直接创建或安装插件，而是从已确认 PRD、架构和测试策略中抽取首版插件的封装边界、通过门和阻塞项。

### 实际执行路径

1. 查询 `docs/ARCHITECTURE.md`、`docs/PRD.md` 和 `docs/TESTING.md` 中与插件、Hook、`PLUGIN_DATA`、安装验证和用户数据隔离有关的条目。
2. 确认首版插件不应默认包含 Hook、自定义 Agent、MCP、应用连接、外部日志上传或向量数据库。
3. 识别封装前 P1 风险：当前 `SKILL.md` 中 helper 命令写死 `.agents/skills/codex-project-workflow/scripts/read_reference.py`，插件安装后可能无法定位。
4. 新增 `docs/PLUGIN_PACKAGING.md`，记录可封装资产、建议结构、阻塞项、通过门和安装后验收门。

### 验收检查

| 检查项 | 状态 | 证据 |
| --- | --- | --- |
| 没有直接写入插件安装目录 | 通过 | 本轮只新增项目文档 |
| 没有安装或启用 Hook | 通过 | `docs/PLUGIN_PACKAGING.md` 建议首版不含 Hook |
| 没有把个人项目数据列入插件资产 | 通过 | 封装清单排除 memory、PLAN 历史、rollout 和私有路径 |
| 发现实际封装风险 | 通过 | helper 路径不可移植被列为 P1 |
| 给出下一候选方向 | 通过 | 建议先做 helper 路径可移植候选 |

## UX-20260622-03 模型上下文升级策略

### 用户输入

```text
后面大模型更新，上下文变大了，应该怎么去兼容或者是改变
```

随后用户要求按建议执行。

### 任务解释

本轮目标是把“上下文变大后如何兼容”的建议落成可执行策略，而不是直接放宽当前 active skill 的上下文预算。

### 实际执行路径

1. 保持 active skill 不变。
2. 新增 `docs/MODEL_CONTEXT_STRATEGY.md`，定义 S/M/L/XL 能力档位、策略配置字段、升级校准流程和风险防护。
3. 更新 `docs/USER_GUIDE.md`，让使用者知道模型升级后不会自动触发更重流程。
4. 更新 `docs/PLAN.md`，把模型上下文策略登记为后续校准入口。

### 验收检查

| 检查项 | 状态 | 证据 |
| --- | --- | --- |
| 没有因为未来模型能力直接放宽 active skill | 通过 | `SKILL.md` 未作为本策略步骤的目标 |
| 保留薄核心和按需加载 | 通过 | `MODEL_CONTEXT_STRATEGY.md` 第 1、7 节 |
| 提供可调档位而非固定单点规则 | 通过 | S/M/L/XL 档位表 |
| 明确升级校准流程 | 通过 | 升级校准流程第 1-6 步 |
| 安全和实现路径确认门不降级 | 通过 | hard invariants 与风险防护表 |

## UX-20260622-04 CAND-12 helper 路径可移植预检

### 任务解释

插件封装准备发现 helper 调用说明写死仓库 `.agents` 路径。本轮创建隔离候选 `CAND-20260622-12`，只改变候选文件和测试指针，不修改 active skill。

### 实际执行路径

1. 创建 `CAND-20260622-12` 候选目录。
2. 新增候选 `SKILL.candidate.md`，把 helper 调用改为优先使用当前技能源目录 `<skill_dir>/scripts/read_reference.py`，仓库 `.agents` 路径只作为存在时 fallback。
3. 新增候选 `patch.diff` 和 `manifest.json`，绑定 active skill 基线哈希、候选哈希、patch 哈希和失效条件。
4. 更新脚本测试的当前候选指针，让预检验证 CAND-12。
5. 运行脚本单测、skill 结构验证、行为 fixture、full fixture 和最近激活回归结果验证。
6. 增加本地插件路径 smoke，验证复制到插件式技能源目录的 `read_reference.py` 优先读取同目录 `references/`，不会借用工作区 `.agents` fallback。

### 验收检查

| 检查项 | 状态 | 证据 |
| --- | --- | --- |
| active skill 未改变 | 通过 | 变更在 `evals/candidates/CAND-20260622-12` |
| 候选预算未超限 | 通过 | description 624，body 1491 |
| patch 绑定候选 | 通过 | manifest 记录 base/candidate/patch SHA-256 |
| 现有验证通过 | 通过 | 49 个脚本测试、skill、eval、fixture、active 回归结果校验通过 |
| 插件路径 smoke 通过 | 通过 | `test_reference_reader_prefers_script_source_dir` |
| 未直接激活 | 通过 | manifest 状态为 `preflight_passed_pending_isolated_evaluation` |

## UX-20260622-05 CAND-12 Targeted Regression Discipline

### User Input

```text
好的，按照你的建议执行，执行完之后再继续推进项目
```

### Task Interpretation

Continue the project by moving CAND-20260622-12 from preflight into isolated targeted regression, while preserving exact evaluation boundaries and evidence quality.

### Execution Path

1. Generated E32/E35 regression workspaces with `setup_full_eval.py`.
2. Started isolated Codex threads from `codex/cand-20260622-12-activation`.
3. Discarded the first collected run after machine collection showed `prompt_integrity=false`; root cause was orchestration contamination from extra prompt text and combined scripted replies.
4. Reset the fixture workspaces and reran with exact setup prompts.
5. Sent the E35 scripted replies as three separate messages.
6. Updated collector wording recognition for the valid phrase "proposed agents were not started" and covered it with a unit test.
7. Collected and assessed `REGRESSION-20260622-12`.

### Verification

| Check | Status | Evidence |
| --- | --- | --- |
| Prompt integrity | Passed | Summary shows both selected runs have `prompt_integrity.valid=true` |
| Hard-trigger overage | Passed | E32 reported `added_codepoints=4223`, `added_sections=3` |
| Multi-agent pending state | Passed | E35 summary records `pending_state=proposed` and no agent start calls |
| Implementation path | Passed | E35 changed only `src/client.py` and verified `python app.py --self-test` |
| Formal result validation | Passed | `validate_full_results.py` reported 2/2 targeted regression cases passed |

### Learning

The project mechanism caught a real process problem: a plausible-looking first run was not accepted because prompt integrity failed. This is exactly the kind of internal-path and orchestration verification the workflow is meant to preserve.
