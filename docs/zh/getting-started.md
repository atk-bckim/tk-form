---
title: 快速上手
document_type: User Guide
created: 2026-09-06
last_updated: 2026-09-06
version: v1.0
status: Published
tags: [tk-form, vscode, tkinter, installation]
---

# 快速上手

## 目录

- [概述](#概述)
- [系统要求](#系统要求)
- [安装 VSIX](#安装-vsix)
- [创建第一个项目](#创建第一个项目)
- [检查 Python 与 Tkinter](#检查-python-与-tkinter)
- [相关文档](#相关文档)
- [变更历史](#变更历史)

## 概述

TK-Form 是一个用于可视化设计 Tkinter 界面的 VS Code 扩展。本指南以公开的 **v1.6.0** VSIX 发布版本为准，先通过示例项目确认本地 Python 运行时，再开始设计自己的界面。

## 系统要求

- VS Code **1.94 或更高版本**。
- 一个包含 Tkinter 的本地 Python 运行时，用于验证、预览（Preview）与导出（Export）。验证与代码生成引擎要求 **Python 3.9 以上**，ttkbootstrap 项目的预览要求 **Python 3.10 以上**。
- 若要预览 ttkbootstrap 项目，所选运行时需安装 `ttkbootstrap>=2,<3` 包（该可选依赖不随扩展打包）。
- 在使用执行 Python 的功能之前，先信任本地工作区。

在未信任的工作区中仍然可以打开、编辑和保存 `.tkform.json` 文件。但 Validate、代码生成、Export、预览以及 Python 运行时检查会执行本地 Python，因此在该环境中被禁用。

## 安装 VSIX

1. 从 [v1.6.0 发布页](https://github.com/atk-bckim/tk-form/releases/tag/v1.6.0)下载 `tk-form-1.6.0.vsix`，或选择其他需要的发布版本。
2. 在 VS Code 中打开 Extensions 视图。
3. 在 `...` 菜单中选择 **Install from VSIX...**，然后选择下载的文件。

也可以通过命令行安装：

```bash
code --install-extension tk-form-1.6.0.vsix
```

通过 VSIX 安装的扩展默认可能不会自动更新。需要更新时，请查看 [Releases](https://github.com/atk-bckim/tk-form/releases) 页面。

## 创建第一个项目

1. 在 VS Code 中打开一个本地文件夹并将其标记为受信任。
2. 在命令面板中运行 **TK-Form: Open Example Project**。
3. 选择一个示例。除 **Login**、**Settings Panel**、**Data Browser** 之外，还提供 ttkbootstrap 示例 **Ttkbootstrap Login**、**Ttkbootstrap Widgets** 和 **Ttkbootstrap Dialogs**。ttkbootstrap 示例需要 ttkbootstrap 包与 Python 3.10 以上运行时才能预览。
4. 保存生成的 `.tkform.json` 文件，TK-Form 自定义编辑器会随之打开。
5. 在设计器的 **Python** 面板中指定绝对 Python 可执行文件路径，或使用已配置的默认值。
6. 运行 **Check Python**，然后按 **Validate** → **Preview** → **Export** 的顺序进行。

如果想从空白设计开始，请运行 **TK-Form: New Project**。打开已有的 `.tkform.json` 文件会自动启动 TK-Form 自定义编辑器。

## 检查 Python 与 Tkinter

预览需要包含 Tkinter 的 Python 运行时。可以在终端中使用以下命令检查：

```bash
python3 -c "import tkinter; print(tkinter.TkVersion)"
```

如果该命令失败，请在设计器的 **Python** 面板中选择其他绝对 Python 可执行文件路径，或安装包含 Tkinter 的 Python 发行版。如果显示的版本低于 3.9，则不满足验证与代码生成引擎的要求；ttkbootstrap 项目应使用 3.10 以上的运行时进行预览。

## 相关文档

| 文档 | 路径 | 关系 |
|---|---|---|
| 设计器工作流 | [designer-workflow.md](./designer-workflow.md) | 介绍日常的设计与导出流程。 |
| ttkbootstrap 项目 | [ttkbootstrap.md](./ttkbootstrap.md) | 介绍 ttkbootstrap 主题、部件与运行时要求。 |
| 部件动画 | [animations.md](./animations.md) | 介绍当前的 preset、trigger 与生成的 Python API。 |
| 技术范围 | [technical-scope.md](./technical-scope.md) | 列出支持的功能与运行限制。 |
| 故障排除与反馈 | [troubleshooting.md](./troubleshooting.md) | 涵盖常见的配置问题与 Issue 提交方式。 |

## 变更历史

| 版本 | 日期 | 变更 |
|---|---|---|
| v1.0 | 2026-09-06 | 以 TK-Form v1.6.0 为准，将韩文快速上手指南翻译为简体中文并首次发布。 |
