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

## CAND-20260716-13 GPT-5.6 Baseline Calibration

Date: 2026-07-16

Trigger signal:

- Codex App、CLI 和模型升级后，需要重新核对插件的触发精度、上下文成本、安装所有权和评估夹具是否仍符合当前运行时行为。

Observed behavior:

- GPT-5.6 基线校准共 6 个目标回归，4 个通过、2 个失败。
- E32 负控把本应排除的低风险一步任务误判为需要加载技能，实际加载了技能正文和 verification 协议。
- E32 标准任务同时加载 governance 与 verification，聚合上下文为 `4723` Unicode 码点、`4` 个二级章节，超过 `2500/2` 预算。
- 负控工作区和盲测提示本身包含技能名称或“active skill”措辞，构成评估污染；采集器对统一 `exec`、JSON 文本块和真实加载轨迹的解析也存在缺口。

Minimal fix considered:

- 用 exclusion-first 描述明确排除简单问题、明确低风险一步编辑和普通本地验证。
- 让 Route 2 的有界实现只加载 verification；没有批准、依赖、状态、协调或高影响触发时不加载 governance。
- 隔离评估工作区，移除负控路径和盲测边界中的技能名称污染，并修复采集器。

Status:

- Baseline calibration failed; not accepted as the final behavior candidate.
- 失败证据保留在候选和完整评估目录中，不以安装成功替代行为回归。

## CAND-20260716-14 Exclusion-First Routing and Harness Isolation

Date: 2026-07-16

Scope:

- Plugin source, routing description, bounded Route 2 behavior, E32/E35 regression harness, collection, and install acceptance.

Candidate behavior:

- 简单问题、明确低风险一步编辑/命令和普通本地验证不得激活技能，也不得加载正文或 references。
- 其他有界实现若需要路径验证，只加载 verification；没有治理触发时不加载 governance。
- 研究、依赖、实现路径、高风险、恢复或协调条件仍按原硬触发和授权边界处理，不能为了上下文预算省略安全门。

Harness corrections:

- 完整评估 manifest 使用相对来源路径和 SHA-256，并继续兼容旧记录。
- 负控工作区移到不包含技能名称的隔离路径；盲测边界改为“若任务独立激活技能，才使用 active entry”。
- 采集器支持统一 `exec` 的原始 JavaScript 参数、JSON 文本块、实际 workdir、fixture/host 扫描区分以及真实加载技能的 metrics。
- `.agents/skills/codex-project-workflow/` 仅保留评估夹具、协议镜像和工具，不再包含可发现的 `SKILL.md`。

Ownership and install evidence:

- `plugins/codex-project-workflow/skills/codex-project-workflow/SKILL.md` 是仓库内唯一技能源。
- 最终准备并安装的 cache 版本为 `0.1.0+codex.20260716095059`；安装 cache 是运行时副本，不是第二个源 owner。
- 当前已打开的 Codex App 任务可能保留启动时的旧插件清单；fresh CLI 进程已在前一安装候选 `0.1.0+codex.20260716093851` 上证明会重新加载新 cache，而最终 `0.1.0+codex.20260716095059` 已通过显式版本 smoke。旧任务清单不能作为最终版本 pickup 的反证或证明，前一候选的 CLI pickup 也不能冒充最终版本 pickup。

Verification boundary:

- 项目严格验证器通过；脚本单元回归达到 `67/67`。
- 官方插件/技能校验器依赖 `PyYAML`，当前可用 Python 环境缺少该依赖，因此记录为 unavailable，不声明官方校验已通过。
- 候选的最终激活结论仍以候选 manifest 和正式回归记录为准；本台账不替代评估结果。
- Final-cache clean CLI regressions for E32 `negative_quick` and `standard_cross_file` have validator-passing result packages under the tracked `.eval-workspaces/formal-results/` directory; their source manifests and collector diagnostics remain under the matching `.agents/skills/codex-project-workflow/evals/full/runs/` directories.
- The remaining four clean regressions ran on 2026-07-18 under `.agents/skills/codex-project-workflow/evals/full/runs/REGRESSION-20260718-GPT56-C14-REMAINING-CLEAN/`: `full_high_risk_migration` and `nested_h3_counting` passed; `hard_trigger_overage` and E35 `four_hard_triggers` failed. The formal validator accepted the evidence shape and reported `0/2 targeted_regression cases passed; overall=fail` because both the E32 aggregate and E35 case failed.
- The E32 failure omitted the mandatory verification protocol. E35 left public-source verification incomplete, used a different unit-test command from the required command, duplicated protocol loads, and misreported the resulting context overage.
- Earlier diagnostic launches against legacy sandbox-owned workspaces were discarded. The formal batch used newly generated host-owned workspaces and current matching App/CLI runtime files, so the two failures are recorded as current-model regressions rather than infrastructure failures.
- CAND-14 is `preflight_passed_regression_failed`, remains unactivated, and has `activation.allowed=false`. Its evidence must not be promoted as a successful acceptance result.

Out of scope:

- 自动记录、Hook、MCP、app connector、后台自更新和向量检索。

## CAND-20260718-15 Current-Model Protocol Routing Repair

Date: 2026-07-18

Trigger signal:

- CAND-14 的正式 GPT-5.6 回归显示：E32 高影响只读评估遗漏 verification；E35 未完成独立页面批准、未使用指定测试命令、重复加载协议并误报上下文总量。
- [官方 Skills 指南](https://learn.chatgpt.com/docs/build-skills)强调用精确 description、清晰边界和正负触发提示验证技能；[官方 Subagents 指南](https://learn.chatgpt.com/docs/agent-configuration/subagents)建议只把独立、读多写少的工作并行化，并谨慎处理并行写入。
- 社区实现信号继续表明不能只依赖配置或名称推断运行时所有权：[project-local filtering](https://github.com/openai/codex/issues/20210)、[重复技能名](https://github.com/openai/codex/issues/25324)和[续接会话与新鲜上下文差异](https://github.com/openai/codex/issues/17560)都需要本地 fresh-session 证据兜底。

Candidate behavior:

- 只允许 `research`、`governance`、`verification` 三个协议路由名；implementation 映射到 verification。
- 高影响、状态、迁移和实现路径证明即使只读，也必须加载 governance 与 verification。
- 每个必需协议每任务加载一次，分别暴露 helper 原始输出；无法计量时明确报告 incomplete，不猜测 overage。
- 用户或夹具指定的验证命令必须逐字执行，不追加 flags。
- 搜索批准不包含页面打开；每个新的 query、source、URL 或 open 都需要后续精确批准。
- 多 Agent 提案未获决定时保持 `proposed`；主 Agent 只继续已分配或独立工作。

Verification:

- Candidate SHA-256：`f8ee04f6ffb89286d630c9c725b7897ee258bbd4569bd78381c3388da273686a`；patch SHA-256：`77c812864c7176faf9e9ff96c5f66c8037dd739ea556f13b3cfb09f6bb142105`。
- 静态验证：脚本 `71/71`、根目录 `12/12`、评估夹具 `36 cases / 148 assertions`、完整夹具 `31/31 cases / 61 variants`，skill structure 与 diff check 通过。
- 定向回归 `REGRESSION-20260718-GPT56-C15-TARGETED-CLEAN7`：`2/2` run、`2/2` case、`overall=pass`。
- 完整回归 `REGRESSION-20260718-GPT56-C15-FULL`：`6/6` run、`2/2` case、`overall=pass`。
- R6 cache `0.1.0+codex.cand-20260718-15-r6` 安装 smoke 通过；仓库、个人源和 cache 的 7 个内容文件一致。fresh CLI probe `019f7481-73b0-71a1-895d-12e64fe3a0be` 仅发现 1 个精确名称匹配，来源是 R6 cache，匹配路径不含 `.agents`。
- 官方 Python quick validator 因已批准环境缺少 `PyYAML` 仍记为 unavailable；没有安装依赖，也不把项目验证器通过冒充官方 validator 通过。

Residual signal:

- E32 `standard_cross_file` 与 E35 `four_hard_triggers` 在加载正确协议前各自试探过不存在的 implementation 名称；失败调用没有加载协议正文，后续门、计量和结果完整，因此不构成本候选 hard failure，但可作为后续精简效率的真实使用信号。

Status:

- `activated`。
- 用户已显式批准绑定候选 ID、SHA-256 `f8ee04f6ffb89286d630c9c725b7897ee258bbd4569bd78381c3388da273686a`、R6 运行时、`6/6` / `2/2` / `overall=pass` 结果和不变范围；`activation.allowed=true`、`formal_activation_recorded=true`。
- 仓库 active path 的物理内容等于候选 SHA；patch 对 base commit 正向检查通过，对当前工作树反向检查通过。R6 由 `evaluation_copy` 转为正式 `activated_runtime`，未复制或改写候选字节。

Out of scope:

- 自动记录、Hook、MCP、app connector、后台自更新、向量检索和手工修改安装 cache。
