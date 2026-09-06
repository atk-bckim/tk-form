---
title: 设计器工作流
document_type: User Guide
created: 2026-09-06
last_updated: 2026-09-06
version: v1.0
status: Published
tags: [tk-form, workflow, export, preview]
---

# 设计器工作流

## 目录

- [设计界面](#设计界面)
- [核心工作流](#核心工作流)
- [布局管理器](#布局管理器)
- [Export 模式](#export-模式)
- [Python 运行时配置](#python-运行时配置)
- [工作区信任与文件安全](#工作区信任与文件安全)
- [相关文档](#相关文档)
- [变更历史](#变更历史)

## 设计界面

`*.tkform.json` 自定义编辑器提供放置 Tkinter 与 ttk 部件的画布、属性检查器（Inspector）、对象树，以及菜单、Tk 变量、图片资源和非可视组件的控制区。常用的设计操作包括拖拽、调整大小、对齐、吸附、缩放、多选，以及编辑属性和事件代码。

每个项目都会选择自己的 UI 工具包（toolkit）。默认为标准 Tkinter；将项目设置为 **ttkbootstrap** 后即可编辑主题与部件级 bootstyle。详见 [ttkbootstrap 项目](./ttkbootstrap.md)。

响应式的图标化命令栏让常用操作始终可见，次要操作则归入溢出菜单。每个操作都有可供访问性工具识别的提示。Inspector 的各个分区是可用键盘导航的图标标签页，并带有诊断徽标和用于部件动画的 **Motion** 标签页。

Event Editor 的 Python 代码编辑器提供自动补全。当前 handler 作用域内的名称（部件、Tk 变量、非可视组件，以及 `event`、`value`、`result`、`self` 等 handler 参数）会随输入实时建议；输入点号（`.`）后，编辑器会根据部件类型建议对应的 Tk/ttk 方法与属性。随时可用 `Ctrl+Space` 打开补全列表，编辑器上方的一行 **In scope** 提示会列出当前 handler 中可用的名称。

内置示例包括 **Login**、**Settings Panel**、**Data Browser**，以及 ttkbootstrap 示例 **Ttkbootstrap Login**、**Ttkbootstrap Widgets** 和 **Ttkbootstrap Dialogs**。请把它们当作可运行的参考设计，而不是必须保持原样的模板。

## 核心工作流

1. **Design** — 放置部件，选择父容器，设置布局与属性，并在需要时添加事件逻辑。
2. **Validate** — 运行 **TK-Form: Validate Project**，检查项目结构、部件属性、布局规则、名称、绑定与事件 handler 语法。
3. **Preview** — 运行 **TK-Form: Preview Project**，使用所选的本地 Python 运行时生成并打开界面。正在运行的预览可用 **TK-Form: Stop Preview** 终止。
4. **Export** — 运行 **TK-Form: Export Python**，并在受信任的工作区内选择保存位置。

画布是 Tk 布局的近似呈现，在 ttkbootstrap 主题与 `pack` 布局下差异尤为明显。设计器中也会持续显示 "canvas approximation, preview is final" 状态提示。最终的尺寸与摆放请始终以 Validate 和 Preview 的结果为准。

通过 **TK-Form: Open Output** 可以查看验证、预览与导出消息。**TK-Form: Copy Support Summary** 会复制一份不含项目源码与事件代码的脱敏诊断摘要，便于提交 Issue。

## 布局管理器

支持 `place`、`grid`、`pack` 三种布局管理器。

| 管理器 | 配置方式 | 适用场景 |
|---|---|---|
| `place` | 部件级 x/y 坐标与尺寸 | 基于像素的固定摆放 |
| `grid` | 行列网格单元 | 表单类对话框与界面 |
| `pack` | side/fill/expand/padx/pady/anchor | 工具栏等单向堆叠的流式布局 |

`pack` 的部件级 `packSide`（`top`/`bottom`/`left`/`right`）、`packFill`、`packExpand`、`packPadX`、`packPadY`、`packAnchor` 可在 Layout 标签页中编辑。画布将 pack 近似为弹性行列（flexbox）布局，因此 Preview 才是最终渲染效果。pack 的堆叠顺序遵循兄弟部件顺序，因此 pack 子部件不提供 z-order 操作。

同一个父容器的子部件必须使用同一种管理器，但 `Toplevel`、`PanedWindow`、`TtkPanedWindow` 之下可以混用。在其他位置混用管理器时，验证会给出提示。

## Export 模式

| 模式 | 输出 | 适用场景 |
|---|---|---|
| Function | 包含 `create_window()` 的单文件脚本 | 简洁直接的应用入口。命名部件可通过 `root._tkform_widgets` 访问。 |
| Class | 单文件 `App(tk.Tk)` 类 | 基于类的 UI。命名部件与 Tk 变量会成为 `self.<name>` 属性。 |
| Split-file | 重新生成的 `ui_<project>.py` 与独立的 `app.py` 入口 | 将应用逻辑放在重新生成的 UI 文件之外。`app.py` 仅在不存在时创建。 |

生成的 UI 代码是可编辑的起点，而不是双向同步系统。重新导出可能替换已生成的文件。请将自定义逻辑放在重新生成的 UI 文件之外，使用 Split-file 模式时尤其如此。

## Python 运行时配置

可以在设计器的 **Python** 面板中设置预览解释器，或使用以下 VS Code 设置：

| 设置 | 用途 |
|---|---|
| `tkform.pythonPath` | 预览使用的绝对 Python 可执行文件路径。 |
| `tkform.enginePythonPath` | 用于验证与代码生成的可选 Python 可执行文件路径。 |
| `tkform.previewInheritPythonPath` | 启用后，会把项目文件夹放在前面并继承现有的 `PYTHONPATH`；默认关闭。 |

预览的解释器选择顺序为：设计器面板 → `tkform.pythonPath` → `TKFORM_PREVIEW_PYTHON` → 引擎运行时。验证与代码生成的选择顺序为：`TKFORM_ENGINE_PYTHON` → `tkform.enginePythonPath` → macOS/Linux 的 `python3` 或 Windows 的 `python`。

## 工作区信任与文件安全

执行 Python 的操作需要受信任的本地工作区。显式指定的导出目标必须是受信任工作区文件夹内的绝对路径。这可以避免 Python 执行与文件导出在未信任或无关的位置运行。

## 相关文档

| 文档 | 路径 | 关系 |
|---|---|---|
| 快速上手 | [getting-started.md](./getting-started.md) | 涵盖安装与首次运行配置。 |
| ttkbootstrap 项目 | [ttkbootstrap.md](./ttkbootstrap.md) | 涵盖 ttkbootstrap 主题、bootstyle 与 provider 部件。 |
| 部件动画 | [animations.md](./animations.md) | 介绍在 Inspector 中配置动画并贯穿 Preview 与 Export。 |
| 技术范围 | [technical-scope.md](./technical-scope.md) | 定义支持的部件、数据模型功能与限制。 |
| 故障排除与反馈 | [troubleshooting.md](./troubleshooting.md) | 提供工作流失败时的恢复方法。 |

## 变更历史

| 版本 | 日期 | 变更 |
|---|---|---|
| v1.0 | 2026-09-06 | 以 TK-Form v1.6.0 为准，将韩文设计器工作流指南翻译为简体中文并首次发布。 |
