# 文档索引

这个项目已经有两类文档：当前正式使用文档，以及开发过程和历史证据文档。日常使用时优先看正式文档，只有排查原因或继续开发插件时再看历史文档。

## 当前正式入口

- `README.md`：项目总入口，先从这里看。
- `docs/PRODUCT_MANUAL.md`：最终使用手册，解释插件解决什么问题、什么时候使用、如何验收。
- `docs/TASK_TEMPLATES.md`：常用任务模板，可以直接复制到启用插件的新线程。
- `docs/INSTALL_UPDATE.md`：安装、更新、复验说明，区分通用流程和当前本机已验证状态。
- `docs/EXTENSION_ROADMAP.md`：后续扩展路线，说明哪些方向值得做、哪些不建议做。

## 插件包内文档

- `plugins/codex-project-workflow/README.md`：插件包自带说明，适合只拿到插件包的人快速理解。
- `plugins/codex-project-workflow/docs/USER_GUIDE.md`：插件包内的精简用户手册。

## 当前验证和状态记录

- `docs/PLUGIN_INSTALL_SMOKE.md`：已安装插件的 smoke 验收证据。
- `docs/PLUGIN_SOURCE_SCAFFOLD.md`：仓库内插件源包结构和封装状态。
- `docs/PRODUCTIZATION_STATUS.md`：产品化文档阶段状态。
- `docs/DOGFOOD_LOG.md`：用本插件审查和优化本项目的记录。

## 历史/开发记录

这些文档保留项目演进证据，不作为普通用户的第一入口：

- `docs/USER_GUIDE.md`：早期仓库级使用手册，部分版本说明可能是历史状态。
- `docs/PLUGIN_PACKAGING.md`：插件封装准备和候选激活过程记录，部分章节描述的是当时状态。
- `docs/PLAN.md`：项目推进历史。
- `docs/USAGE_EXERCISES.md`：使用演练记录。
- `docs/ARCHITECTURE.md`、`docs/DECISIONS.md`、`docs/TRACEABILITY.md` 等：开发过程中的设计和追踪文档。

## 推荐阅读顺序

1. `README.md`
2. `docs/PRODUCT_MANUAL.md`
3. `docs/TASK_TEMPLATES.md`
4. `docs/INSTALL_UPDATE.md`
5. 需要扩展时再读 `docs/EXTENSION_ROADMAP.md`

## 注意事项

- 如果文档之间出现状态冲突，以 `README.md`、`docs/PRODUCT_MANUAL.md`、`docs/INSTALL_UPDATE.md`、`docs/PLUGIN_INSTALL_SMOKE.md` 的当前状态为准。
- 历史文档中的候选编号、旧激活状态和早期阻塞项用于追溯，不代表当前产品状态。
