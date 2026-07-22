# 公开发布流程

本文供项目维护者使用。普通用户从根目录 `README.md` 的快速安装开始。

## 发布边界

- 唯一插件源：`plugins/codex-project-workflow/`
- 发布产物：`dist/codex-project-workflow-<version>.zip`
- 校验和：同名 `.sha256` 文件
- 压缩包根目录直接包含 `.codex-plugin/plugin.json`、`skills/`、`docs/`、`README.md` 和 `LICENSE`
- `.agents/` 评估资产、仓库历史文档、运行记录和个人路径不得进入发布包

## 1. 发布前检查

在仓库根目录运行：

```powershell
python -m unittest discover -s scripts -p "test_*.py"
python .agents\skills\codex-project-workflow\scripts\validate_skill.py .agents\skills\codex-project-workflow --skill-file plugins\codex-project-workflow\skills\codex-project-workflow\SKILL.md
python scripts\build_plugin_release.py
```

构建脚本会验证：

- manifest 名称、严格语义版本、MIT 许可证和公开仓库地址
- 根许可证与插件包许可证完全一致
- repository marketplace 指向唯一插件源
- 发布文件集合没有缺失或额外文件
- 文本文件中没有个人绝对路径、常见访问令牌或私钥特征
- ZIP 内文件位于插件根，而不是多套一层仓库目录

## 2. 人工检查

```powershell
Get-ChildItem dist
Get-FileHash dist\codex-project-workflow-0.1.0.zip -Algorithm SHA256
```

确认脚本输出的 SHA-256 与 `.sha256` 文件一致，并人工阅读 Release 说明。不要把本机 cache 目录、marketplace 文件或评估工作区作为发布附件。

## 3. 提交和发布

只有在本地验证通过、工作树范围确认无误后，才提交、推送和创建 Release。推荐标签与 manifest 版本一致：

```text
v0.1.0
```

可在 GitHub 网页创建 Release，也可以在已认证的 GitHub CLI 中使用：

```powershell
gh release create v0.1.0 dist\codex-project-workflow-0.1.0.zip dist\codex-project-workflow-0.1.0.zip.sha256 --title "codex-project-workflow v0.1.0" --generate-notes
```

提交、推送、标签和 `gh release create` 都会改变外部仓库状态，不属于只读验证；执行前应再次确认目标分支、标签、附件和 Release 标题。

## 4. 发布后验证

1. 从 Release 页面下载 ZIP 和 `.sha256`。
2. 重新计算 SHA-256 并比较。
3. 从公开仓库 marketplace 或下载包完成一次全新安装。
4. 新开顶层 Codex 任务，确认技能来自新安装版本。
5. 记录仍未验证的 Codex App/CLI 版本差异。
