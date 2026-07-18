# 测试与验证策略

> 治理状态：已确认  
> 证据状态：独立复核  
> 说明：运行时减负、上下文预算和机制退出验证已完成最终限域复核  
> 日期：2026-06-11

## 1. 当前唯一评估规范

MVP 的行为样例、评分维度、硬失败条件、运行次数和通过阈值统一由 `docs/EVALUATION.md` 定义。

本文件只说明验证层次，不重复评分细节。

## 2. 验证层次

1. **结构验证**
   - 技能目录和 `SKILL.md` frontmatter。
   - 引用文件、模板和资源路径。
   - 插件阶段的 manifest 和 Marketplace 结构。

2. **触发验证**
   - 至少 10 个正触发样例。
   - 至少 10 个负触发样例。
   - 至少 10 个边界样例。

3. **行为验证**
   - 快速、标准、完整模式。
   - 任务简报与确认边界。
   - 专业研究、方法论和方案比较。
   - 多 Agent 提议与授权。
   - 联网预检和外部提示注入。
   - 审计修复后的结论失效、回归复核和状态声明校准。
   - 标准模式已有项目实施和完整模式端到端闭环。
   - 多 Agent 授权接受、拒绝、失效和跨阶段重新确认。
   - 实际联网工具参数与授权记录。
   - 用户强制快速模式时，高风险操作仍受确认和安全底线约束。
   - 研究预算耗尽、失败重试上限和超限确认。
   - 项目经验沉淀与核心技能改进的批准、拒绝、回归和回滚。
    - 实现契约、产品入口、核心调用链、辅助脚本边界和用户可读证明摘要。
    - 触发正式实现契约时，契约冻结早于首次相关实现写入，关键声明绑定独立来源，冻结后差异不可覆盖。
    - 重要功能至少一条正式产品入口、非 mock 核心模块和真实状态副作用证据；mock-only 证明必须失败。
    - 结果正确但绕过既有产品逻辑的影子实现必须失败。
    - 完整模式纯文档任务不误建实现契约；低可观测技术栈能使用替代证据或诚实降级。
    - 两阶段实现路径评审在第一阶段独立还原路径并冻结记录，第二阶段才接收执行者契约。
    - 上下文预算按实际字符数和章节数验证，协议文件数量只作辅助指标；硬触发不得因预算省略。
    - 普通任务不自动读取完整治理文档；上下文工作集保持最小。
    - 机制账本能够根据成本和收益提出合并、降级或停用候选。
    - 低风险一步任务不加载完整技能正文，生成的 `AGENTS.md` 不无条件引用治理全集。
    - 正式实现契约按生产入口、状态持久化、架构边界、核心能力、用户原路径要求和高影响触发表判定。
    - 薄核心保留外部提示注入、第三方下载、安装、执行、授权、上传、联网脱敏、时效研究和多 Agent 判断的短触发。
   - 实际使用信号的脱敏、去重、作用域判断、候选隔离和批量汇总。
   - 经验计数的幂等、排除规则和检索升级触发。

4. **状态恢复验证**
   - 按 `docs/STATE_CONTRACT.md` 进行新线程盲测。

5. **真实运行**
   - 在 Codex 桌面应用中加载仓库级技能。
   - 记录模型、推理强度、工具、日期、耗时和用户干预。

6. **独立复核**
   - 执行提示与评审提示分离。
   - 子 Agent 盲测需要用户明确授权。
   - 用户拒绝多 Agent 时，执行单 Agent 固定反方审查并披露独立性限制。

7. **架构静态门**
   - 不依赖尚未实现的技能行为。
   - 使用 PRD 到架构、ADR 和评估样例的追踪矩阵。
   - 候选审计持久化到 `docs/audits/`，绑定静态文件清单、完整 SHA-256、规范化 SHA-256、时间、审查者和结论。
   - `docs/PLAN.md` 的“最新审计”只引用已存在且验证通过的审计；尚在生成的 ID 使用“预登记审计”，状态恢复时不得把预登记当成有效结论。
   - 审计清单包含 `docs/audits/README.md` 定义的全部必需文件；缺少任一路径即失败。
   - 用户确认后生成确认凭证；只有治理状态行可以变化，规范化哈希必须与父候选审计一致。
   - 确认凭证逐项比较父候选和当前的完整治理状态清单；未获接受、漏改或目标状态错误都失败。
   - 有效候选审计或确认凭证生成后，`PLAN.md` 才把预登记 ID 切换为最新审计；事务失败时清空预登记并恢复候选状态和父 audit ID。
   - 无未关闭 P0/P1 后才可进入待确认候选。

## 3. 完成门

架构待确认候选与技能稳定版本是两个不同完成门。

架构待确认候选需要：

- 静态结构与引用检查通过。
- 需求追踪矩阵没有核心需求断链。
- 独立反方审查没有未关闭 P0/P1。
- 审计范围、完整与规范化文件哈希、未验证假设和剩余风险已记录。
- 确认范围形成一致整体；若任一范围内 ADR 或 FR 被拒绝，文档不进入已确认状态并重新审计。

技能候选只有在以下条件同时满足时才进入稳定版本：

- `docs/EVALUATION.md` 中适用于仓库级核心技能 MVP 的全部行为案例硬失败为零；PX/RX 条件专项只在进入对应阶段后生效。
- 达到触发、行为和效率阈值。
- 结构验证通过。
- 关键样例完成规定的重复运行。
- 未验证内容和剩余风险已经记录。
- E16、E17、E26、E28 的每次运行分别通过夹具结果断言和实现门，“实现完整性”必须为 2 分；E27、E29 必须正确判定无需实现契约。
- E30 必须保留阶段输入清单、第一阶段输出及哈希、阶段完成与材料释放时点；阶段提前泄露或事后改写判硬失败。
- E31、E32 必须通过可观测运行夹具验证实际组装上下文或等价加载轨迹；无法捕获时不得计为通过。
- E31 的功能断言和七项质量维度不得低于配对基线，额外用户干预不得增加；E32 使用统一换行后的 Unicode 码点数和固定 `##` 章节规则判定 800/1,500/2,500/6,000 字符与章节预算。
- E33 使用固定成本指标和七项质量维度验证实际移除或合并后的变化；安全不变量需要先建立等价覆盖、通过硬失败回归并经用户确认，不能先降级再按成本删除。
- E34 验证正式契约边界表；E35 验证预算不能压过多重硬触发；E36 验证研究与多 Agent 条件可以隐式识别。
- 实现类关键案例保存契约冻结顺序、来源映射、工具调用、变更差异、正式入口记录和状态或持久化轨迹，不得只依据最终文件、界面结果或执行者摘要验收。

插件封装还需额外完成：

- 插件结构验证。
- 安装后的新线程冒烟测试。
- 插件缓存版本与源码版本一致性检查。
- `PX01` 的项目启用、Hook 信任、脚本摘要、敏感字段、权限降级、项目分区和数据删除测试。
- `PX02` 的 Worktree 隔离与非 Git 降级测试。

向量检索只有在触发升级评估后才需完成：

- `RX01` 的硬作用域过滤、召回、精度、延迟和索引重建门。
- 外部或付费嵌入服务的数据与成本专项确认。

## 4. 2026-07-16 GPT-5.6 回归与运行时隔离

本节是当前 P2/P3 验收补充，不改写上面的 GPT-5.5 历史规范。

### 技能源与运行时所有权

- 仓库唯一技能源是 `plugins/codex-project-workflow/skills/codex-project-workflow/SKILL.md`。
- `.agents/skills/codex-project-workflow/` 只保存评估脚本、夹具、协议镜像、候选和运行记录，不包含可发现的 `SKILL.md`。
- 安装 cache 是运行时副本；验证必须绑定明确 cache 版本，不能用 `.agents` fallback 代替。
- 已打开 App 任务和 fresh CLI 进程可能看到不同的插件清单快照。两者必须分别报告，不得把旧任务清单外推为最新安装状态。

### E32/E35 夹具隔离

- 负控工作区路径本身不得包含完整技能名称；setup 校验对此硬失败。
- 盲测边界只允许在任务独立激活技能后读取 active entry，不能在提示中预先宣告存在“active skill”。
- full-eval manifest 记录相对 source manifest、SHA-256、source commit、模型和推理强度；验证器保留旧记录兼容，但新记录不能依赖主机绝对路径。
- 采集器必须解析统一 `exec` 的原始 JavaScript 参数与 JSON 文本块，提取真实 workdir、fixture/host 扫描边界和实际加载技能 metrics。
- E32 预算断言绑定 description、body、references 和 bulk-load 轨迹；E35 继续验证多重硬触发不会被上下文预算压过。

### 当前验证命令

```powershell
python .agents\skills\codex-project-workflow\scripts\test_scripts.py
python .agents\skills\codex-project-workflow\scripts\validate_skill.py .agents\skills\codex-project-workflow --skill-file plugins\codex-project-workflow\skills\codex-project-workflow\SKILL.md
python .agents\skills\codex-project-workflow\scripts\validate_evals.py
python .agents\skills\codex-project-workflow\scripts\validate_full_fixtures.py
python -m unittest discover -s scripts -p "test_*.py"
python scripts\verify_plugin_install_smoke.py --version-dir C:\Users\w\.codex\plugins\cache\personal\codex-project-workflow\0.1.0+codex.20260716095059
git diff --check
```

当前脚本回归达到 `67/67`，项目严格验证器通过。官方 `quick_validate.py` / `validate_plugin.py` 需要 `PyYAML`，当前 Python 环境缺少该依赖，所以只可记录为 unavailable。不得用项目验证器通过来声称官方验证器也已执行通过。

最终 cache 的 E32 `negative_quick` 和 `standard_cross_file` 已在干净路径中形成 validator-pass 结果。账户额度恢复后，其余四项于 2026-07-18 在 `.agents/skills/codex-project-workflow/evals/full/runs/REGRESSION-20260718-GPT56-C14-REMAINING-CLEAN/` 完成：`full_high_risk_migration`、`nested_h3_counting` 通过，`hard_trigger_overage`、E35 `four_hard_triggers` 失败。

正式结果是逐运行 `2/4`，按 E32/E35 聚合后是 `0/2 targeted_regression cases passed; overall=fail`。E32 失败原因是遗漏强制 verification 协议；E35 失败原因是公开来源核验未完成、未运行夹具指定的测试命令、重复加载协议并错误报告总过载。旧 App 运行和旧 sandbox owner 导致 ACL 刷新失败的诊断批次均不进入正式验收。

CAND-14 必须保持 `preflight_passed_regression_failed`、`activation.allowed=false`。验证器接受结果文件格式并不等于行为回归通过，不得据此激活候选。

行为候选的最终状态仍以候选 manifest 和对应 full-eval assessment 为准；安装 smoke、静态测试或文档记录不能单独替代 E32/E35 行为回归。
