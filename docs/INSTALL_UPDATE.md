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

## 当前本机状态

当前这台机器上的 `codex-project-workflow` 已通过 Codex App 启用，并在新线程完成安装 smoke。

已验证版本：

```text
0.1.0+codex.20260622112058
```

已验证插件 cache 路径：

```text
C:\Users\wang yazhou\.codex\plugins\cache\personal\codex-project-workflow\0.1.0+codex.20260622112058
```

个人插件源：

```text
C:\Users\wang yazhou\plugins\codex-project-workflow
```

个人 marketplace：

```text
C:\Users\wang yazhou\.agents\plugins\marketplace.json
```

Codex App 插件页：

```text
codex://plugins/codex-project-workflow?marketplacePath=C%3A%5CUsers%5Cwang%20yazhou%5C.agents%5Cplugins%5Cmarketplace.json
```

历史备注：在本项目的一个桌面线程中，打包的 `codex` CLI 曾返回 `Access is denied`。这不是插件包校验失败；启用插件页和新线程 smoke 已经完成安装验证。

## 更新插件源包

当仓库内 `plugins/codex-project-workflow` 有更新时，推荐流程：

1. 验证仓库源包。
2. 把仓库源包复制到个人插件源目录。
3. 使用 `update_plugin_cachebuster.py` 更新个人插件 manifest 的版本后缀。
4. 通过 Codex App 或 CLI 重装/启用。
5. 新开线程 smoke。
6. 运行 `python scripts\verify_plugin_install_smoke.py`。
7. 把结果记录到 `docs/PLUGIN_INSTALL_SMOKE.md`。

当前本机 cachebuster 更新命令：

```powershell
python "C:\Users\wang yazhou\.codex\skills\.system\plugin-creator\scripts\update_plugin_cachebuster.py" "C:\Users\wang yazhou\plugins\codex-project-workflow"
```

## 校验命令

常用本地校验：

```powershell
python scripts\verify_plugin_install_smoke.py
python -m unittest discover -s .agents\skills\codex-project-workflow\scripts -p test_scripts.py
git diff --check
```

官方插件校验脚本需要 `PyYAML`。如果当前 Python 环境缺少该依赖，应记录原因，不要假装官方校验已通过。
