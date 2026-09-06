---
title: 部件动画
document_type: User Guide
created: 2026-09-06
last_updated: 2026-09-06
version: v1.0
status: Published
tags: [tk-form, animation, tkinter, preview, export]
---

# 部件动画

## 目录

- [概述](#概述)
- [添加与编辑动画](#添加与编辑动画)
- [通用设置](#通用设置)
- [Preset 设置](#preset-设置)
- [Trigger 与手动控制](#trigger-与手动控制)
- [验证、预览与导出](#验证预览与导出)
- [生成的 Python API](#生成的-python-api)
- [限制与故障排除](#限制与故障排除)
- [相关文档](#相关文档)
- [变更历史](#变更历史)

## 概述

TK-Form 提供声明式部件动画，并通过 Tkinter 的 `after` 调度执行（v1.3.0 引入）。动画保存在项目文件的 `animations` 数组中，并在 Validate、Preview 以及 Function/Class/Split-file Export 中保持一致的行为。

创建动画之前，请先确定目标部件的最终位置与尺寸。空间类动画只能用于生成的 Python 中实际以 `place()` 布局的部件。

## 添加与编辑动画

1. 在画布或对象树中选择目标部件。
2. 在 Inspector 的 **Animations** 区域选择 **Add Animation**。
3. 输入一个唯一的 Python 标识符名称，例如 `show_panel`。
4. 选择 Preset 和 Trigger，并设置时长、重复以及 preset 专属参数。
5. 选择 **Save**，然后通过 **Validate** 和 **Preview** 检查效果。

已有条目可使用 **Edit** 修改、**Remove** 删除。名称在项目内必须唯一，且不能是 Python 保留字，也不能与 TK-Form 生成器的保留名称、事件 handler 或其他生成符号冲突。

## 通用设置

| 设置 | 允许的值 | 说明 |
|---|---|---|
| Name | 唯一的 Python 标识符 | 用于 `start_<name>()`、`stop_<name>()` API 的名称。 |
| Duration | 大于 0 且不超过 600,000 ms | 单次播放时长。 |
| Delay | 0–86,400,000 ms | 开始播放前的等待时间。 |
| Easing | `linear`, `easeIn`, `easeOut`, `easeInOut` | 进度缓动曲线。 |
| Repeat count | 1–10,000 | 整段播放的重复次数。 |
| Infinite repeat | 开/关 | 开启后持续重复，直到显式停止。 |

每个项目最多 500 个动画。新动画的默认值为 300 ms、延迟 0 ms、`easeOut`、重复 1 次。

## Preset 设置

| Preset | 参数 | 行为 |
|---|---|---|
| `slide` | `direction`: left/right/up/down, `distance`: 0–1,000,000 | 从指定方向的偏移位置移动到最终位置。 |
| `shake` | `axis`: x/y, `distance`: 0–1,000,000, `cycles`: 1–10,000 | 围绕最终位置做衰减振动。 |
| `bounce` | `direction`: left/right/up/down, `distance`: 0–1,000,000, `cycles`: 1–10,000 | 向指定方向弹起并回到最终位置。 |
| `pulse` | `scale`: 大于 0 且不超过 1,000 | 以部件中心为基准放大后恢复原尺寸。 |
| `color` | `property`: bg/fg, `to`: `#RGB` 或 `#RRGGBB` | 从当前颜色插值到指定颜色。 |

`slide`、`shake`、`bounce`、`pulse` 只支持以 `place()` 布局的部件。`color` 只能用于安全支持所选 `bg` 或 `fg` 属性的经典 Tk 部件。ttk 主题部件（ttkbootstrap 的 Button、Label、Entry、Frame 等）没有 `bg`/`fg` 选项，因此 `color` preset 会在验证时被拒绝。在 ttkbootstrap 项目中，`Text`、`Canvas`、`Listbox` 等经典 Tk 部件仍然可以使用 `color`。

## Trigger 与手动控制

| Trigger | 触发时机 |
|---|---|
| `load` | 生成的窗口初始 idle 处理时自动开始 |
| `click` | 鼠标点击目标部件 |
| `hoverEnter` / `hoverLeave` | 指针进入或离开目标部件 |
| `focusIn` / `focusOut` | 目标部件获得或失去键盘焦点 |
| `manual` | 不自动绑定，由生成的 Python API 调用 |

重新启动同一个动画会取消进行中的调度并替换为新的播放。`infinite` 重复请使用生成的 `stop_<name>()` API 停止。

## 验证、预览与导出

1. **Validate** 检查目标 ID、名称、布局、preset 参数、颜色支持以及生成符号冲突。
2. **Preview** 在所选的 Tkinter 运行时上执行真实的 `after` 回调与部件布局。
3. **Export** 生成通过验证的动画运行时和 start/stop API。

如果 Output Dock 或 VS Code Problems 报告错误，请通过 **Edit** 修改对应动画的取值。目标部件已删除的孤立动画可能会提供删除 Quick Fix。

## 生成的 Python API

名为 `show_panel` 的动画会生成以下 API：

```python
start_show_panel()
stop_show_panel()
```

- Function Export 生成同名函数，并以 `root.start_show_panel`、`root.stop_show_panel` 暴露。
- Class Export 生成 `App.start_show_panel()` 与 `App.stop_show_panel()` 方法。
- Split-file Export 的 UI 类提供相同的方法，可在 `app.py` 的实例上调用。

在 Event Editor 的 handler 中，请使用当前 export 模式提供的同名可调用对象。播放控制代码建议放在受保护的应用文件中，而不是会被重新生成的 `ui_<project>.py` 里。

## 限制与故障排除

- 真实的 `Notebook` 标签页在生成时是 Tk 管理的合成 `ttk.Frame`，不能作为动画目标；放在标签页内、以 `place()` 布局的普通子部件仍可作为目标。
- 空间类 preset 不支持 `grid` 部件、`Toplevel`，以及 `PanedWindow`/`TtkPanedWindow` 直接管理的窗格。
- 如果颜色 preset 被拒绝，请确认目标部件支持所选的 `bg`/`fg` 属性。
- 来自外部项目的非法值会原样显示在 Inspector 中，修正前无法保存。
- 如果预览没有动效，请先运行 **Validate**，并确认所选 Python 运行时包含 Tkinter。
- 避免动画 API 名称与部件、Tk 变量、资源、事件 handler、自动生成的菜单 handler 冲突。

## 相关文档

| 文档 | 路径 | 关系 |
|---|---|---|
| 快速上手 | [getting-started.md](./getting-started.md) | 介绍 v1.6.0 的安装与 Python 准备。 |
| 设计器工作流 | [designer-workflow.md](./designer-workflow.md) | 介绍 Validate、Preview、Export 的顺序。 |
| ttkbootstrap 项目 | [ttkbootstrap.md](./ttkbootstrap.md) | 包含 ttkbootstrap 项目中的动画限制。 |
| 技术范围 | [technical-scope.md](./technical-scope.md) | 定义项目格式、支持的功能与安全限制。 |
| 故障排除与反馈 | [troubleshooting.md](./troubleshooting.md) | 提供运行时与诊断问题的恢复方法。 |

## 变更历史

| 版本 | 日期 | 变更 |
|---|---|---|
| v1.0 | 2026-09-06 | 以 TK-Form v1.6.0 为准，将韩文部件动画指南翻译为简体中文并首次发布。 |
