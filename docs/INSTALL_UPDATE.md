# 安装、更新和复验

## 当前安装状态

`codex-project-workflow` 已通过 Codex App 启用，并在新线程完成安装 smoke。

已验证版本：

```text
0.1.0+codex.20260622112058
```

已验证插件 cache 路径：

```text
C:\Users\wang yazhou\.codex\plugins\cache\personal\codex-project-workflow\0.1.0+codex.20260622112058
```

## 关键路径

仓库源包：

```text
plugins/codex-project-workflow
```

个人插件源：

```text
C:\Users\wang yazhou\plugins\codex-project-workflow
```

个人 marketplace：

```text
C:\Users\wang yazhou\.agents\plugins\marketplace.json
```

安装目标：

```text
codex-project-workflow@personal
```

## 启用方式

优先使用 Codex App 插件页启用：

```text
codex://plugins/codex-project-workflow?marketplacePath=C%3A%5CUsers%5Cwang%20yazhou%5C.agents%5Cplugins%5Cmarketplace.json
```

如果当前环境能执行 Codex CLI，也可以使用：

```powershell
codex plugin add codex-project-workflow@personal
```

注意：在本项目的桌面线程中，打包的 `codex` CLI 曾返回 `Access is denied`。这不是插件包校验失败；当 CLI 被系统权限阻挡时，用 Codex App 插件页启用。

## 安装后必须新开线程

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

## 仓库内复验脚本

插件更新或重装后，在本仓库运行：

```powershell
python scripts\verify_plugin_install_smoke.py
```

这个脚本只读检查：

- `SKILL.md`
- `scripts/read_reference.py`
- `references/governance.md`
- `references/research.md`
- `references/verification.md`

它会确认这些文件都在同一个插件 cache 版本目录下，并从临时目录调用 helper，避免误走当前项目 `.agents` fallback。

## 更新插件源包

当仓库内 `plugins/codex-project-workflow` 有更新时，推荐流程：

1. 验证仓库源包。
2. 把仓库源包复制到个人插件源目录。
3. 使用 `update_plugin_cachebuster.py` 更新个人插件 manifest 的版本后缀。
4. 通过 Codex App 或 CLI 重装/启用。
5. 新开线程 smoke。
6. 运行 `python scripts\verify_plugin_install_smoke.py`。
7. 把结果记录到 `docs/PLUGIN_INSTALL_SMOKE.md`。

cachebuster 更新命令：

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
