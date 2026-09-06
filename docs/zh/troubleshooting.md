---
title: 故障排除与反馈
document_type: User Guide
created: 2026-09-06
last_updated: 2026-09-06
version: v1.0
status: Published
tags: [tk-form, troubleshooting, support, feedback]
---

# 故障排除与反馈

## 目录

- [收集有用的诊断信息](#收集有用的诊断信息)
- [常见问题](#常见问题)
- [提交 Issue](#提交-issue)
- [相关文档](#相关文档)
- [变更历史](#变更历史)

## 收集有用的诊断信息

报告问题之前，请打开 **View: Toggle Output** 并选择 **TK-Form**，然后运行 **TK-Form: Copy Support Summary**。该命令会生成一份脱敏的诊断摘要，适合贴在公开 Issue 中，且不包含项目源码与事件代码。

## 常见问题

| 问题 | 可能原因 | 解决方法 |
|---|---|---|
| Validate、Export、Preview、Python Check 被禁用 | 工作区未被信任。 | 打开一个受信任的本地文件夹，并在 VS Code 工作区信任设置中信任它。未信任时仍可编辑。 |
| Python Check 或预览提示找不到 Tkinter | 所选 Python 运行时不含 Tkinter。 | 运行 `python3 -c "import tkinter; print(tkinter.TkVersion)"`，然后选择其他绝对 Python 路径或安装 Tkinter。 |
| 引擎提示 Python 版本不受支持 | 验证与代码生成引擎要求 Python 3.9 以上。 | 选择 3.9 以上运行时。ttkbootstrap 项目预览要求 3.10 以上。 |
| ttkbootstrap 项目预览失败 | 运行时缺少 ttkbootstrap，或版本不符。 | 在预览运行时中执行 `pip install "ttkbootstrap>=2,<3"`。不支持 ttkbootstrap 3.x。 |
| 提示 Python 路径必须为绝对路径 | 显式指定了 `python`、`python3` 这类相对可执行文件。 | 用 `python3 -c "import sys; print(sys.executable)"` 查看完整可执行路径并填入，或留空以使用已配置的默认值。 |
| `.tkform.json` 文件无法打开 | JSON 无效，或在设计器之外被部分编辑。 | 以文本方式打开修正 JSON 后重新打开。可与 **Open Example Project** 中的正常项目对比。 |
| 验证后 Export 被阻止 | 引擎发现了验证错误。 | 运行 **Validate**，修正部件、属性、布局、事件或名称相关错误后重新导出。 |
| 预览启动后立即退出 | 生成的 Python 抛出异常或进程被关闭。 | 查看 TK-Form Output 通道，并用相同的 Python 运行时复现。可与 Login 示例对比。 |
| 导出后自定义修改消失 | 生成的 UI 文件被重新生成。 | Split-file 模式下请把自定义逻辑放在 `app.py` 中；不要依赖 `ui_<project>.py` 等重新生成文件里的编辑。 |
| pack 部件的上移/下移（z-order）操作无效 | pack 的堆叠顺序遵循兄弟部件顺序。 | 在对象树中调整兄弟部件顺序，或更换布局管理器。pack 子部件不提供 z-order 操作。 |
| Event Editor 的补全列表不出现 | 光标位于字符串或注释内，或补全尚未触发。 | 按 `Ctrl+Space` 打开列表。补全只在代码位置生效；编辑器上方的 In scope 提示列出了可用名称。 |
| 韩文、中文等 Unicode handler 名称被拒绝 | 名称在 NFKC 归一化后不稳定，是 Python 保留字，或与现有名称重复。 | 请使用 NFKC 归一化后形态不变且唯一的名称。部件、Tk 变量、动画与非可视组件名称必须为 ASCII。 |

## 提交 Issue

Bug 与功能建议请通过 [GitHub Issues](https://github.com/atk-bckim/tk-form/issues) 提交。建议包含：

- 简明的复现步骤
- VS Code 版本与操作系统
- 设计器或 `tkform.pythonPath` 中显示的 Python 版本与运行时路径
- 工作区是否受信任
- 相关的 TK-Form Output 行与 **TK-Form: Copy Support Summary** 的结果

首次 Issue 请不要包含项目源码或事件代码。如确需项目文件或生成的 Python，请在我们提出请求后提供最小化或脱敏的复现示例。

商业授权或购买咨询请发送邮件至 `bckim7639@gmail.com`。

## 相关文档

| 文档 | 路径 | 关系 |
|---|---|---|
| 快速上手 | [getting-started.md](./getting-started.md) | 解决安装与 Python 配置问题。 |
| 设计器工作流 | [designer-workflow.md](./designer-workflow.md) | 说明 Validate、Preview、Export 的行为。 |
| ttkbootstrap 项目 | [ttkbootstrap.md](./ttkbootstrap.md) | 说明 ttkbootstrap 的运行时要求。 |
| 技术范围 | [technical-scope.md](./technical-scope.md) | 定义产品限制与受支持的行为。 |

## 变更历史

| 版本 | 日期 | 变更 |
|---|---|---|
| v1.0 | 2026-09-06 | 以 TK-Form v1.6.0 为准，将韩文故障排除与反馈指南翻译为简体中文并首次发布。 |
