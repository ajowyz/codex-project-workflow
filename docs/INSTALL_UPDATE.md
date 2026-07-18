# 安装、更新和复验

本文件分为两部分：通用流程和当前本机状态。分享给他人时，优先使用通用流程；排查这台机器时，再看当前本机状态。

## 通用流程

### 1. 准备插件源包

插件源包结构应包含：

```text
<plugin-root>/
  .codex-plugin/plugin.json
  skills/codex-project-workflow/SKILL.md
  skills/codex-project-workflow/scripts/read_reference.py
  skills/codex-project-workflow/references/governance.md
  skills/codex-project-workflow/references/research.md
  skills/codex-project-workflow/references/verification.md
  README.md
  docs/USER_GUIDE.md
```

首版保持纯技能插件，不包含 Hook、MCP、app connector 或自定义 Agent manifest。

### 2. 配置 marketplace

默认个人 marketplace 文件位于：

```text
%USERPROFILE%\.agents\plugins\marketplace.json
```

插件源通常位于：

```text
%USERPROFILE%\plugins\codex-project-workflow
```

marketplace entry 的路径保持相对形式：

```text
./plugins/codex-project-workflow
```

### 3. 启用插件

优先使用 Codex App 插件页启用。

如果当前环境能执行 Codex CLI，也可以使用：

```powershell
codex plugin add codex-project-workflow@personal
```

如果 CLI 因系统权限失败，不要把它当作插件包失败；改用 Codex App 插件页启用。

### 4. 新开线程

插件启用、更新或重装后，需要新开 Codex 线程。旧线程通常不会自动加载新技能。

新线程中先做 smoke：

```text
请做 codex-project-workflow 插件安装 smoke 验收：
1. 确认当前加载的技能路径。
2. 确认是否来自插件 cache，而不是项目 .agents。
3. 使用插件 helper 读取 governance、research、verification 的 Execution Rules 和 Output Requirements。
4. 报告 metrics 和失败点。
5. 不修改文件。
```

### 5. 复验

在源仓库运行只读复验：

```powershell
python scripts\verify_plugin_install_smoke.py
```

这个脚本会确认 `SKILL.md`、`scripts/read_reference.py` 和三份 `references/*.md` 都在同一个已安装插件 cache 版本目录下，并从临时目录调用 helper，避免误走当前项目 `.agents` fallback。

通过时应看到 `PLUGIN INSTALL SMOKE: PASS`，并确认输出里有：

- selected cache version
- skill、helper、references 三个 installed paths
- `fallback guard: helper is executed from a temporary directory`
- governance、research、verification 三组 metrics

失败时不要只看退出码；同时查看 `PLUGIN INSTALL SMOKE: FAIL` 后面的 reason 和 next steps。

## 当前本机状态

### 2026-07-16 当前验收状态

当前仓库的唯一技能源是：

```text
D:\project\codex\codex_project_workflow\plugins\codex-project-workflow\skills\codex-project-workflow\SKILL.md
```

`.agents/skills/codex-project-workflow/` 只保留评估夹具、协议镜像和验证工具，不包含可发现的 `SKILL.md`。不要再用项目本地技能副本覆盖或证明插件运行时。

当前已准备并安装的插件 cache：

```text
0.1.0+codex.cand-20260718-15-r6
```

```text
C:\Users\w\.codex\plugins\cache\personal\codex-project-workflow\0.1.0+codex.cand-20260718-15-r6
```

该目录是 CAND-15 的已评估测试安装态；候选仍等待证据绑定的显式激活批准，不能仅凭安装或 smoke 把它描述为正式激活。

仓库源包、个人插件源和安装 cache 的 7 个内容文件应保持一致；manifest 允许个人源/安装 cache 带 cachebuster，而仓库 manifest 保持源版本。更新只能通过 `prepare_plugin_update.py` 和受支持的插件安装流程完成，不手工编辑 marketplace 或安装 cache。

当前 App 任务的技能清单可能是在任务启动时冻结的，重装后仍显示旧 cache 路径。判断最新安装时应分别检查：

- `python scripts\verify_plugin_install_smoke.py --version-dir <exact-cache-dir>` 的 cache 完整性；
- fresh CLI 进程或真正新建的顶层 App 任务的 pickup；
- 当前旧 App 任务只作为“清单可能陈旧”的边界证据，不能代替 fresh pickup。

本轮项目严格验证器通过。官方插件/技能 Python 校验器依赖 `PyYAML`；当前可用 Python 环境缺少该依赖，因此状态是 **unavailable**，不是 passed，也不要求为本轮额外安装仓库依赖。

自动记录、Hook、MCP、app connector 和后台自更新不属于当前插件安装范围。

### 2026-07-13 迁移验收基线（历史）

当前新电脑上的 `codex-project-workflow` 已通过 Codex App 启用，并于 2026-07-13 通过安装 smoke 和 fresh-thread pickup smoke。

已验证版本：

```text
0.1.0+codex.20260712082233
```

已验证插件 cache 路径：

```text
C:\Users\w\.codex\plugins\cache\personal\codex-project-workflow\0.1.0+codex.20260712082233
```

最近一次更新说明：

```text
python scripts\prepare_plugin_update.py --apply --apply-cachebuster
```

该命令把个人插件源准备到 `0.1.0+codex.20260712082233`。当前 `codex` CLI 在 WindowsApps 包目录下返回 `Access is denied`；本次通过 Codex App 插件页启用后，安装 smoke 和 fresh-thread pickup smoke 均已通过。

个人插件源：

```text
C:\Users\w\plugins\codex-project-workflow
```

个人 marketplace：

```text
C:\Users\w\.agents\plugins\marketplace.json
```

Codex App 插件页：

```text
codex://plugins/codex-project-workflow?marketplacePath=C%3A%5CUsers%5Cw%5C.agents%5Cplugins%5Cmarketplace.json
```

新电脑 fresh-thread pickup smoke 任务为 `019f5979-2a17-7c80-871e-8cecbcfa3c4e`。该任务确认技能来自上述 installed cache，三份协议 metrics 分别为 governance `2484/2`、research `1205/2`、verification `2239/2`，仓库 smoke 输出 `PLUGIN INSTALL SMOKE: PASS`，且 7 个核心文件与仓库插件源包 SHA-256 一致。

当前仓库路径为 `D:\project\codex\codex_project_workflow`；迁移验收输入快照为 `2af7e23e3cfe20fff5cc81d37bbcd1965bc9efbf`，当时工作树干净，且本地 `master` 与本地 `origin/master` 跟踪引用对齐。验收未联网；后续提交的实时 HEAD、ahead/behind 和服务器远端状态应分别用 Git 状态命令与明确的联网核对确认，不在本文档中硬编码为当前值。

环境备注：普通 PowerShell 的裸 `python` 当前命中无效的 Microsoft Store 别名；Codex bundled Python 可以正常运行 smoke。CLI 的 `Access is denied` 和裸 `python` 入口问题都不是插件包校验失败。

## 更新插件源包

当仓库内 `plugins/codex-project-workflow` 有更新时，推荐流程：

1. 验证仓库源包。
2. 把仓库源包复制到个人插件源目录。
3. 更新个人插件源 manifest 的 cachebuster 后缀。
4. 通过 Codex App 或 CLI 重装/启用。
5. 新开线程 smoke。
6. 运行 `python scripts\verify_plugin_install_smoke.py`。
7. 把结果记录到 `docs/PLUGIN_INSTALL_SMOKE.md`。

可以先用仓库脚本做干跑计划：

```powershell
python scripts\prepare_plugin_update.py
```

输出里应确认：

- `marketplace: checked`
- `target stale-file guard: ok`
- source 和 target manifest version 符合预期
- safety 说明 marketplace 和 installed plugin cache 不会被修改

如需先预览下一版 cachebuster，可以传入固定 token：

```powershell
python scripts\prepare_plugin_update.py --cachebuster DOGFOOD-13
```

确认无误后，再显式复制到个人插件源目录并更新目标 manifest 版本：

```powershell
python scripts\prepare_plugin_update.py --apply --apply-cachebuster
```

如果需要可复现的版本后缀，可以同时传入 `--cachebuster <token>`。

这个脚本会修改个人插件源目录，但不修改 marketplace，也不修改已安装 plugin cache。完成后仍需要通过 Codex App 或 CLI 重新启用插件、新开线程 smoke，并运行 `python scripts\verify_plugin_install_smoke.py`。

如果这次更新来自本地使用中发现的问题，先确认它已经记录到 `docs/IMPROVEMENT_CANDIDATES.md` 或 `docs/DOGFOOD_LOG.md`。更新完成后记录新 cache 版本、smoke 结果和仍需人工完成的步骤；不要把脚本准备成功当作插件已经启用。

## 校验命令

常用本地校验：

```powershell
python scripts\verify_plugin_install_smoke.py
python scripts\prepare_plugin_update.py
python -m unittest discover -s scripts -p "test_*.py"
python -m unittest discover -s .agents\skills\codex-project-workflow\scripts -p test_scripts.py
git diff --check
```

官方插件校验脚本需要 `PyYAML`。如果当前 Python 环境缺少该依赖，应记录原因，不要假装官方校验已通过。

当前包还应运行显式版本 smoke，避免“自动选择最新目录”掩盖目标版本错误：

```powershell
python scripts\verify_plugin_install_smoke.py --version-dir C:\Users\w\.codex\plugins\cache\personal\codex-project-workflow\0.1.0+codex.cand-20260718-15-r6
```

若 App 当前任务仍显示旧清单，先完成上述只读 cache smoke，再用 fresh CLI 或新顶层 App 任务验证 pickup；不要删除旧任务证据，也不要把重启 App 说成已经执行。
