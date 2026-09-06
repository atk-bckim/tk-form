---
title: 技术范围
document_type: Reference
created: 2026-09-06
last_updated: 2026-09-06
version: v1.0
status: Published
tags: [tk-form, architecture, tkinter, scope]
---

# 技术范围

## 目录

- [发布范围](#发布范围)
- [架构与数据流](#架构与数据流)
- [项目模型](#项目模型)
- [支持的设计功能](#支持的设计功能)
- [支持的部件类型](#支持的部件类型)
- [验证与安全限制](#验证与安全限制)
- [当前边界](#当前边界)
- [相关文档](#相关文档)
- [变更历史](#变更历史)

## 发布范围

本文档描述公开的 **TK-Form v1.6.0** VSIX 发布版本。TK-Form 是面向实用 Tkinter 应用的可视化创作与代码生成工具，不是通用 IDE，也不提供与手写 Python 的双向编辑。

## 架构与数据流

| 层 | 当前实现 |
|---|---|
| VS Code 集成 | TypeScript 扩展宿主、`*.tkform.json` 自定义编辑器、扩展命令、工作区信任控制、输出、预览进程管理、导出文件访问。 |
| 设计器 webview | React、Vite、Tailwind CSS、Zustand 状态管理、`dnd-kit` 交互支持，以及带作用域感知自动补全的 CodeMirror Python 编辑。 |
| 项目格式 | `*.tkform.json` 的 JSON Schema draft-07；新文件使用 schema version 4。 |
| Python 引擎 | 随扩展打包的 `tkform_engine` 包，使用 Python 标准库与 Tkinter/ttk 负责验证、Python 生成与预览。运行时下限为 Python 3.9 以上。 |

常规数据流如下：

```text
*.tkform.json → TK-Form 自定义编辑器 → 扩展宿主 → 随包 Python 引擎
                                            ├─ 诊断与输出
                                            ├─ 预览进程
                                            └─ 生成的 Python 文件
```

设计器与 Python 引擎以相同的规则将加载的项目归一化到 schema version 4。旧版本文件可以打开，保存时按版本逐步迁移。旧版扩展会把 `pack` 项目降级为 `place` 读取。项目限制由 schema 与两个运行时从单一来源（`schema/project-limits.json`）共享。

## 项目模型

项目描述一个根窗口以及部件、菜单、Tk 变量、图片资源、非可视组件和动画。项目同时声明 UI 工具包（`tkinter`，或 majorVersion 2 的 `ttkbootstrap`）与 ttkbootstrap 主题。部件 ID 是稳定的内部引用；部件与动画名称必须是有效且唯一的 Python 标识符，并成为生成 Python 中的名称。

模型支持：

- 根窗口尺寸、背景、是否可调整大小、ttk 主题选择。
- `place`、`grid`、`pack` 三种布局管理器。同一父容器的子部件必须使用同一种管理器，`Toplevel`、`PanedWindow`、`TtkPanedWindow` 之下除外。
- 用于 `command` handler 与 `<Button-1>`、`<Key>` 等 Tk 绑定序列的 Event Editor。事件 handler 名称遵循 PEP 3131，允许 Unicode 标识符（例如 `저장하기`、`保存设置`），但仍须满足 NFKC 稳定、非保留字且唯一的要求。部件、Tk 变量、动画与非可视组件名称仍限 ASCII 标识符。
- 菜单层级、菜单命令与快捷键绑定。
- `StringVar`、`IntVar`、`DoubleVar`、`BooleanVar` 声明。
- 通过部件 ID 引用的 Base64 图片资源。
- `Timer`、`FileDialog`、`ColorChooser`、`MessageBox` 非可视组件；ttkbootstrap 项目额外提供 `TtkMessagebox`、`Querybox`、`DatePickerDialog`、`ColorPickerDialog`、`ToastNotification`、`ToolTip`。
- 使用 `slide`、`shake`、`bounce`、`pulse`、`color` preset 与 load/click/hover/focus/manual trigger 的部件动画。
- 通过 `bindings.command` 的标准 Scrollbar 绑定；为兼容起见也接受 `xscrollcommand`、`yscrollcommand`。

Scrollbar 的横向目标为 `Text`、`Listbox`、`Entry`、`Treeview`、`Canvas`；纵向目标为 `Text`、`Listbox`、`Treeview`、`Canvas`。

## 支持的设计功能

可视化编辑器支持画布摆放、拖拽与调整大小、对齐、吸附、缩放、多选、对象树、属性编辑、菜单、变量、资源、非可视组件和动画。响应式图标化命令栏提供可访问的工具提示与分组溢出操作；可用键盘导航的 Inspector 标签页带有诊断徽标与 Motion 编辑器。项目验证器会在代码生成之前检查交叉引用、重复或保留名称、属性兼容性、布局一致性、绑定、动画参数与生成符号、载荷限制以及事件 handler 语法。

旧版部件 `props.command` 字段只接受 Python 函数引用。内联 Python 逻辑请写入 Event Editor；两者同时存在时，Event Editor 的 command 优先。

## 支持的部件类型

| 分类 | 部件类型 |
|---|---|
| 常规控件 | `Button`, `Label`, `Entry`, `Text`, `Checkbutton`, `Radiobutton`, `Listbox`, `Scale`, `OptionMenu`, `Spinbox`, `Scrollbar`, `Menubutton`, `Message` |
| 容器与布局 | `Frame`, `LabelFrame`, `Canvas`, `PanedWindow`, `TtkPanedWindow`, `Notebook`, `Toplevel` |
| ttk 附加部件 | `Progressbar`, `Combobox`, `Treeview`, `Sizegrip`, `Separator` |
| ttkbootstrap provider 部件（仅限 ttkbootstrap 项目） | `DateEntry`, `LabeledScale`, `Meter`, `Floodgauge`, `Tableview`, `ScrolledText`, `ScrolledFrame` |

`Notebook`、`Progressbar`、`Combobox`、`Treeview`、`Sizegrip`、`Separator`、`TtkPanedWindow` 使用 ttk 构造器。它们支持的属性与经典 Tk 部件不同，例如 `bg`、`fg`、`padx`、`pady` 等经典视觉属性并不以相同方式支持。在 ttkbootstrap 项目中，Inspector 会跟随每个部件的实际后端模块，因此回退为经典 tk 的 `Text`、`Canvas`、`Listbox`、`PanedWindow`、`Message` 等部件会显示其 tk 样式属性。

## 验证与安全限制

| 限制 | 最大值 |
|---|---:|
| 项目载荷 | 8 MiB |
| 图片上传 | 每张 5 MiB |
| 部件 | 2,000 个 |
| 资源 | 200 个 |
| Tk 变量 | 500 个 |
| 非可视组件 | 500 个 |
| 动画 | 500 个 |
| 部件与菜单嵌套 | 64 层 |

执行 Python 的操作需要受信任的本地工作区。显式指定的导出目标必须是受信任工作区文件夹内的绝对路径。预览需要包含 Tkinter 的本地 Python 运行时；验证与代码生成引擎要求 Python 3.9 以上；ttkbootstrap 预览要求 Python 3.10 以上并安装 `ttkbootstrap>=2,<3`。生成的 tkinter 代码以 Python 3.4 为目标，ttkbootstrap 生成代码以 Python 3.10 为目标。

## 当前边界

- 生成的 Python 只是起点。TK-Form 不会保留重新生成文件中的手工修改，也不提供与手写 Python 的双向同步。
- 画布是 Tk 布局的近似呈现。在把设计画布当作最终运行时布局之前，请先运行 Validate 与 Preview；对 ttkbootstrap 主题与 `pack` 布局而言，Preview 尤其是权威渲染。
- pack 的堆叠顺序遵循兄弟部件顺序，因此 pack 子部件不提供 z-order 操作。
- Split-file Export 会保护已有的 `app.py`，但后续导出会重写 `ui_<project>.py`。
- 旧版 `command` 属性不能包含内联 Python 代码，请使用 Event Editor。
- `Text` 不支持 `textvariable`。
- `Entry` 只支持横向 Scrollbar 绑定。
- 空间类动画只能用于生成 Python 中实际以 `place()` 布局的部件。真实的 `Notebook` 标签页、`grid` 部件、`Toplevel` 以及窗格管理的部件不能作为目标。
- 颜色动画只应用于目标部件安全支持的 `bg` 或 `fg` 属性；在 ttk 主题部件（ttkbootstrap 的 Button、Label、Entry、Frame 等）上会被拒绝。
- 事件 handler 名称允许 Unicode（PEP 3131）标识符，但部件、Tk 变量、动画与非可视组件名称仍为 ASCII。
- 产品聚焦于实用、常用的单窗口表单与内部工具；不包含自动授权、应用内账户管理或大范围的企业自助服务。

## 相关文档

| 文档 | 路径 | 关系 |
|---|---|---|
| 快速上手 | [getting-started.md](./getting-started.md) | 安装发布版本并准备运行时。 |
| 设计器工作流 | [designer-workflow.md](./designer-workflow.md) | 在设计、预览与导出中应用这些能力。 |
| ttkbootstrap 项目 | [ttkbootstrap.md](./ttkbootstrap.md) | 描述 ttkbootstrap 部件、对话框与约束。 |
| 部件动画 | [animations.md](./animations.md) | 介绍 preset、trigger、生成 API 与目标限制。 |
| 故障排除与反馈 | [troubleshooting.md](./troubleshooting.md) | 帮助诊断限制与验证失败。 |

## 变更历史

| 版本 | 日期 | 变更 |
|---|---|---|
| v1.0 | 2026-09-06 | 以 TK-Form v1.6.0 为准，将韩文技术范围参考翻译为简体中文并首次发布。 |
