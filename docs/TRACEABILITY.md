# 需求追踪矩阵

> 治理状态：已确认  
> 证据状态：独立复核  
> 说明：32 条 FR 的设计与验证入口已完成最终限域复核  
> 日期：2026-06-11

本矩阵用于架构静态门。它证明需求具有设计落点和验证入口，但不等于技能行为已经通过真实运行。

| 需求 | 主要设计落点 | 验证入口 | 阶段 |
| --- | --- | --- | --- |
| FR-01 自然语言任务整理 | `ARCHITECTURE.md` 4.2、5.1；`PROMPTING.md` L6 | E03、E16、E17 | MVP |
| FR-02 主动完整性扫描 | `ARCHITECTURE.md` 4.2、5.1 | E03、E04、E17 | MVP |
| FR-03 任务风险分级 | `ARCHITECTURE.md` 4.2、5.1；`PROMPTING.md` L4 | E01、E02、E03、E16、E17 | MVP |
| FR-04 专业调研 | `ARCHITECTURE.md` 4.6、5.2；`PROMPTING.md` L5 | E04、E05、E11、E19 | MVP |
| FR-04A 方法论发现与裁剪 | `ARCHITECTURE.md` 5.2；ADR-016 | E14 | MVP |
| FR-05 方案空间与专业建议 | `ARCHITECTURE.md` 5.2 | E04、E14 | MVP |
| FR-06 人工确认边界 | `ARCHITECTURE.md` 4.2、7；`PROMPTING.md` L4-L5 | E06、E08、E10、E17、E18 | MVP |
| FR-07 单 Agent 与多 Agent 策略 | `ARCHITECTURE.md` 4.7；ADR-005 | E06、E07、E18 | MVP |
| FR-08 项目文档生成与维护 | `ARCHITECTURE.md` 4.4；`STATE_CONTRACT.md` | E12、E17 | MVP |
| FR-09 实施、验证与审查 | `ARCHITECTURE.md` 9；`TESTING.md` | E16、E17 | MVP |
| FR-10 纠偏与经验沉淀 | `ARCHITECTURE.md` 5.3 | E08、E22 | MVP |
| FR-11 自动触发与显式控制 | `PROMPTING.md` L2、L9 | 10/10/10 正负边界触发集 | MVP |
| FR-12 人类查阅文档 | `PROMPTING.md` 7；MVP 交付清单 | 用户文档内容验收 | MVP |
| FR-13 可扩展机制 | `ARCHITECTURE.md` 4.3、4.9 | 结构校验和后续模块新增演练 | MVP |
| FR-14 持续学习与自我完善闭环 | `ARCHITECTURE.md` 5.2、5.3 | E05、E11、E14、E22、E23、E24 | MVP |
| FR-15 可选周期性资料跟踪 | `ARCHITECTURE.md` 后续扩展边界 | 自动化专项验收 | MVP 后 |
| FR-16 上下文与完整线程恢复 | `STATE_CONTRACT.md`；ADR-017 | E12；完整历史恢复专项 | MVP 最小版 / 后续增强 |
| FR-17 模型、工具与资源策略 | `ARCHITECTURE.md` 4.6、5.2、8 | E01、E02、E05、E15 | MVP |
| FR-18 研究完整性与认知偏差控制 | `ARCHITECTURE.md` 5.2、12 | E04、E11、E14、E21 | MVP |
| FR-19 失败、降级与恢复 | `ARCHITECTURE.md` 8 | E12、E15 | MVP |
| FR-20 效果评估与回归测试 | `ARCHITECTURE.md` 4.8；`EVALUATION.md` | 全部评估集 | MVP |
| FR-21 规则、知识与版本治理 | `ARCHITECTURE.md` 4.4、4.8、5.3、10 | E22、E23、E24 | MVP 基础版 |
| FR-22 交互输出协议 | `PROMPTING.md` L6-L9 | E01、E03、E06、E16 | MVP |
| FR-23 技能自身改进治理 | `ARCHITECTURE.md` 4.8、5.3；ADR-023 | E23、E24；插件阶段 PX01、PX02 | MVP 核心 / 插件增强 |
| FR-24 外部内容与供应链安全 | `ARCHITECTURE.md` 7 | E09、E10、E19、E20 | MVP 基础版 |
| FR-25 个性化、共享与配置分层 | `ARCHITECTURE.md` 4.9、6 | 插件安装与隐私专项 | MVP 后完整实现 |
| FR-26 提示词与任务协议 | `PROMPTING.md` L1-L9 | E03、E06、E16、E17 | MVP |
| FR-27 持久化规则变更确认 | `ARCHITECTURE.md` 4.4、5.3 | E22、E23 | MVP |
| FR-28 审计闭环与结论校准 | `ARCHITECTURE.md` 9.5；ADR-022 | 架构静态审计；E13 行为回归 | MVP |
| FR-29 经验记忆与检索演进 | `ARCHITECTURE.md` 4.8；ADR-024 | E25；触发后 RX01 | MVP 结构化记录 / 条件升级 |
| FR-30 实现完整性与架构符合性 | `ARCHITECTURE.md` 5.4；`PROMPTING.md` L6-L8；ADR-025 | E16、E17、E26、E27、E28、E29、E30、E34 | MVP |
| FR-31 运行时减负与上下文预算 | `ARCHITECTURE.md` 4.2-4.4、5.5；`PROMPTING.md` L2-L6；ADR-026 | E01、E02、E12、E16、E27、E29、E31、E32、E33、E34、E35、E36 | MVP |

## 静态门判定

- 每条已确认或建议纳入 MVP 的需求必须存在主要设计落点。
- 每条 MVP 需求必须存在行为样例、结构检查、人工验收或明确的实现后专项验证入口。
- 标记为 MVP 后的需求允许不阻塞首版，但必须明确延期边界。
- 需求、架构或评估变化时同步更新本矩阵；未同步时审计证据失效。
