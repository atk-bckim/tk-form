---
title: ttkbootstrap Projects
document_type: User Guide
created: 2026-09-06
last_updated: 2026-09-06
version: v1.0
status: Published
tags: [tk-form, ttkbootstrap, theme, widgets, dialogs]
---

# ttkbootstrap Projects

## Contents

- [Overview](#overview)
- [Switch a Project to ttkbootstrap](#switch-a-project-to-ttkbootstrap)
- [Themes and Bootstyles](#themes-and-bootstyles)
- [Provider Widgets](#provider-widgets)
- [Dialogs, Toasts, and Tooltips](#dialogs-toasts-and-tooltips)
- [Runtime Requirements](#runtime-requirements)
- [Canvas Approximation and Limits](#canvas-approximation-and-limits)
- [Related Documents](#related-documents)
- [Change History](#change-history)

## Overview

Since TK-Form v1.3.3, each project can select **ttkbootstrap 2.x** as its UI toolkit. A ttkbootstrap project brings Bootstrap-style themes, per-widget bootstyle properties, additional provider widgets, and modern dialog, toast, and tooltip components, and exports ttkbootstrap-based Python code in Function, Class, and Split-file modes.

ttkbootstrap is an **optional dependency** that ships outside the extension. Designing and exporting need only the extension, but Preview and execution require the ttkbootstrap package in the selected Python runtime.

## Switch a Project to ttkbootstrap

1. Create a blank project with **TK-Form: New Project**, or open the **Ttkbootstrap Login**, **Ttkbootstrap Widgets**, or **Ttkbootstrap Dialogs** example from **TK-Form: Open Example Project**.
2. In the designer's toolkit settings, set the project UI toolkit to `ttkbootstrap` (majorVersion 2).
3. Place widgets, edit the [theme and bootstyles](#themes-and-bootstyles), then follow the Validate → Preview → Export sequence.

The toolkit is a project-level property. The editing workflow is the same as for plain Tkinter projects, but the available properties and components change.

## Themes and Bootstyles

- The **theme** is a project property. The project declares one ttkbootstrap theme, and the generated Python initializes the window with it.
- The **bootstyle** is a per-widget property. Color and style variants supported by ttkbootstrap for buttons, labels, entries, and similar widgets are edited in the Inspector and carried into generated code.
- In ttkbootstrap projects the Inspector follows each widget's real backend module. Widgets that support ttk style properties show ttk properties, while widgets that fall back to classic tk — such as `Text`, `Canvas`, `Listbox`, `PanedWindow`, and `Message` — expose their tk style properties.

## Provider Widgets

The following provider widgets are available in ttkbootstrap projects.

| Widget | Purpose |
|---|---|
| `DateEntry` | Date picker entry field |
| `LabeledScale` | Slider with an attached label |
| `Meter` | Gauge-style value display |
| `Floodgauge` | Filling progress gauge |
| `Tableview` | Tabular data view |
| `ScrolledText` | Text area with integrated scrolling |
| `ScrolledFrame` | Frame with integrated scrolling |

Provider widgets exist only in ttkbootstrap projects and are absent from the palette of plain Tkinter projects.

## Dialogs, Toasts, and Tooltips

ttkbootstrap projects can use these non-visual components:

| Component | Purpose |
|---|---|
| `TtkMessagebox` | ttkbootstrap-styled message boxes |
| `Querybox` | Dialogs that ask for user input |
| `DatePickerDialog` | Date selection dialog |
| `ColorPickerDialog` | Color selection dialog |
| `ToastNotification` | Timed notifications at the window edge |
| `ToolTip` | Tooltips attached to widgets |

`FontDialog` and `Querybox.get_font` are outside the current scope, and no icon font is bundled with exported projects.

## Runtime Requirements

- The Preview runtime must be **Python 3.10 or later** (the validation and code-generation engine floor is 3.9+ for plain Tkinter projects).
- Install `ttkbootstrap>=2,<3` in the Preview runtime, for example `pip install "ttkbootstrap>=2,<3"`.
- **ttkbootstrap 3.x is not supported.** Generated code targets Python 3.10.

## Canvas Approximation and Limits

- Canvas colors and bootstyles for ttkbootstrap are CSS approximations; the Preview window is the authority for the final appearance.
- Widget icons render as letter placeholders on the canvas; real icons appear in Preview.
- Provider widgets (`Meter`, `Floodgauge`, `Tableview`, `DateEntry`, `LabeledScale`, `ScrolledText`, `ScrolledFrame`) render as sketch previews on the canvas.
- Animations do not play on the canvas.
- The `color` animation preset is rejected on ttk themed widgets (ttkbootstrap Button, Label, Entry, Frame, and similar). Classic Tk widgets such as `Text`, `Canvas`, and `Listbox` remain usable with `color` in ttkbootstrap projects.

## Related Documents

| Document | Path | Relationship |
|---|---|---|
| Getting Started | [getting-started.md](./getting-started.md) | Covers installation and Python runtime preparation. |
| Designer Workflow | [designer-workflow.md](./designer-workflow.md) | Explains the shared edit, validate, and export flow. |
| Widget Animations | [animations.md](./animations.md) | Includes animation restrictions in ttkbootstrap projects. |
| Technical Scope | [technical-scope.md](./technical-scope.md) | Defines supported widgets and operating limits. |
| Troubleshooting and Feedback | [troubleshooting.md](./troubleshooting.md) | Provides recovery steps for ttkbootstrap runtime problems. |

## Change History

| Version | Date | Changes |
|---|---|---|
| v1.0 | 2026-09-06 | Initial ttkbootstrap project guide for TK-Form v1.6.0. |
