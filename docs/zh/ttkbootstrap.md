---
title: ttkbootstrap 项目
document_type: User Guide
created: 2026-09-06
last_updated: 2026-09-06
version: v1.0
status: Published
tags: [tk-form, ttkbootstrap, theme, widgets, dialogs]
---

# ttkbootstrap 项目

## 目录

- [概述](#概述)
- [将项目切换为 ttkbootstrap](#将项目切换为-ttkbootstrap)
- [主题与 bootstyle](#主题与-bootstyle)
- [provider 部件](#provider-部件)
- [对话框、Toast 与工具提示](#对话框toast-与工具提示)
- [运行时要求](#运行时要求)
- [画布近似与限制](#画布近似与限制)
- [相关文档](#相关文档)
- [变更历史](#变更历史)

## 概述

从 TK-Form v1.3.3 开始，每个项目都可以选择 **ttkbootstrap 2.x** 作为 UI 工具包。ttkbootstrap 项目提供 Bootstrap 风格的主题、bootstyle 属性、额外的 provider 部件，以及现代化的对话框、Toast 与工具提示组件，并且 Function/Class/Split-file 三种模式都导出基于 ttkbootstrap 的 Python 代码。

ttkbootstrap 是不随扩展打包的**可选依赖**。设计与导出只需要扩展本身；但预览和运行需要所选 Python 运行时中已安装 ttkbootstrap 包。

## 将项目切换为 ttkbootstrap

1. 使用 **TK-Form: New Project** 创建空白项目，或在 **TK-Form: Open Example Project** 中打开 **Ttkbootstrap Login**、**Ttkbootstrap Widgets**、**Ttkbootstrap Dialogs** 示例。
2. 在设计器的工具包设置中，将项目 UI 工具包设为 `ttkbootstrap`（majorVersion 2）。
3. 放置部件，编辑[主题与 bootstyle](#主题与-bootstyle)，然后按 Validate → Preview → Export 的顺序进行。

工具包是项目级属性。普通 Tkinter 项目与 ttkbootstrap 项目的编辑流程相同，只是可用的属性与组件不同。

## 主题与 bootstyle

- **主题（theme）** 是项目属性。项目声明一个 ttkbootstrap 主题，生成的 Python 会以该主题初始化窗口。
- **bootstyle** 是部件级属性。按钮、标签、输入框等 ttkbootstrap 支持的部件可以指定颜色与样式变体，在 Inspector 中编辑并反映到生成代码中。
- 在 ttkbootstrap 项目中，Inspector 会跟随每个部件实际使用的后端模块：支持 ttk 样式属性的部件显示 ttk 属性；回退为经典 tk 的 `Text`、`Canvas`、`Listbox`、`PanedWindow`、`Message` 等部件则显示 tk 样式属性。

## provider 部件

ttkbootstrap 项目可以使用以下 provider 部件。

| 部件 | 用途 |
|---|---|
| `DateEntry` | 日期选择输入框 |
| `LabeledScale` | 带标签的滑块 |
| `Meter` | 仪表盘式数值显示 |
| `Floodgauge` | 填充式进度仪表 |
| `Tableview` | 表格数据视图 |
| `ScrolledText` | 集成滚动的文本区域 |
| `ScrolledFrame` | 集成滚动的框架 |

provider 部件仅在 ttkbootstrap 项目中可用，普通 Tkinter 项目的部件面板中不会出现。

## 对话框、Toast 与工具提示

ttkbootstrap 项目可以使用以下非可视组件：

| 组件 | 用途 |
|---|---|
| `TtkMessagebox` | ttkbootstrap 风格的消息框 |
| `Querybox` | 请求用户输入的对话框 |
| `DatePickerDialog` | 日期选择对话框 |
| `ColorPickerDialog` | 颜色选择对话框 |
| `ToastNotification` | 在窗口边缘自动消失的通知 |
| `ToolTip` | 附加到部件上的工具提示 |

`FontDialog` 与 `Querybox.get_font` 不在当前范围内，导出的项目中也不会打包图标字体。

## 运行时要求

- 预览运行时必须是 **Python 3.10 以上**（普通 Tkinter 项目的验证与代码生成引擎要求 3.9 以上）。
- 在预览运行时中安装 `ttkbootstrap>=2,<3`，例如 `pip install "ttkbootstrap>=2,<3"`。
- **不支持 ttkbootstrap 3.x。** 生成代码以 Python 3.10 为目标。

## 画布近似与限制

- 画布中的 ttkbootstrap 颜色与 bootstyle 是 CSS 近似呈现，最终外观以 Preview 窗口为准。
- 部件图标在画布上以字母占位符渲染，真实图标在 Preview 中显示。
- provider 部件（`Meter`、`Floodgauge`、`Tableview`、`DateEntry`、`LabeledScale`、`ScrolledText`、`ScrolledFrame`）在画布上以草图预览渲染。
- 动画不会在画布上播放。
- `color` 动画 preset 在 ttk 主题部件（ttkbootstrap 的 Button、Label、Entry、Frame 等）上会被拒绝。`Text`、`Canvas`、`Listbox` 等经典 Tk 部件在 ttkbootstrap 项目中仍可使用 `color`。

## 相关文档

| 文档 | 路径 | 关系 |
|---|---|---|
| 快速上手 | [getting-started.md](./getting-started.md) | 介绍安装与 Python 运行时准备。 |
| 设计器工作流 | [designer-workflow.md](./designer-workflow.md) | 介绍共通的编辑、验证与导出流程。 |
| 部件动画 | [animations.md](./animations.md) | 包含 ttkbootstrap 项目中的动画限制。 |
| 技术范围 | [technical-scope.md](./technical-scope.md) | 定义支持的部件与运行限制。 |
| 故障排除与反馈 | [troubleshooting.md](./troubleshooting.md) | 提供 ttkbootstrap 运行时问题的恢复方法。 |

## 变更历史

| 版本 | 日期 | 变更 |
|---|---|---|
| v1.0 | 2026-09-06 | 以 TK-Form v1.6.0 为准，首次发布简体中文 ttkbootstrap 项目指南。 |
