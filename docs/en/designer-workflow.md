---
title: Designer Workflow
document_type: User Guide
created: 2026-07-16
last_updated: 2026-09-06
version: v1.3
status: Published
tags: [tk-form, workflow, export, preview]
---

# Designer Workflow

## Contents

- [Design Surface](#design-surface)
- [Core Workflow](#core-workflow)
- [Layout Managers](#layout-managers)
- [Export Modes](#export-modes)
- [Python Runtime Configuration](#python-runtime-configuration)
- [Workspace Trust and File Safety](#workspace-trust-and-file-safety)
- [Related Documents](#related-documents)
- [Change History](#change-history)

## Design Surface

The `*.tkform.json` custom editor provides a canvas for Tkinter and ttk widgets, a property inspector, an object tree, and controls for menus, Tk variables, image resources, and non-visual components. Common design actions include drag, resize, align, snap, zoom, multi-selection, and editing properties or event code.

Each project selects its UI toolkit. The default is standard Tkinter; setting a project to **ttkbootstrap** enables theme and per-widget bootstyle editing. See [ttkbootstrap Projects](./ttkbootstrap.md) for details.

The responsive, icon-first command bar keeps common actions visible and groups secondary actions in overflow menus. Accessible tooltips identify each action. Inspector sections are keyboard-navigable icon tabs, show diagnostic badges, and include the **Motion** tab for widget animations.

The Event Editor's Python code editor offers autocompletion. Names in the current handler scope (widgets, Tk variables, non-visual components, and handler parameters such as `event`, `value`, `result`, and `self`) are suggested as you type, and after a dot (`.`) the editor suggests Tk/ttk methods and attributes that match the widget type. Use `Ctrl+Space` to open the list at any time, and check the one-line **In scope** hint above the editor for the names available in the current handler.

The bundled examples are **Login**, **Settings Panel**, and **Data Browser**, plus the ttkbootstrap examples **Ttkbootstrap Login**, **Ttkbootstrap Widgets**, and **Ttkbootstrap Dialogs**. Use them as working reference designs rather than templates that must be kept unchanged.

## Core Workflow

1. **Design** — Place widgets, choose their parent container, set layout and properties, and add event logic where needed.
2. **Validate** — Run **TK-Form: Validate Project** to check the project structure, widget properties, layout rules, names, bindings, and event-handler syntax.
3. **Preview** — Run **TK-Form: Preview Project** to generate and open the interface with the selected local Python runtime. Use **TK-Form: Stop Preview** to terminate an active preview.
4. **Export** — Run **TK-Form: Export Python** and choose the destination inside the trusted workspace.

The canvas approximates Tk layout, most notably for ttkbootstrap theming and `pack` arrangements. The designer shows a persistent "canvas approximation, preview is final" status notice. Always confirm final sizing and placement with Validate and Preview.

Use **TK-Form: Open Output** to inspect validation, preview, and export messages. **TK-Form: Copy Support Summary** copies a sanitized diagnostic summary for an issue report without project source or event code.

## Layout Managers

Three layout managers are supported: `place`, `grid`, and `pack`.

| Manager | Configuration | Best suited for |
|---|---|---|
| `place` | Per-widget x/y coordinates and size | Fixed, pixel-accurate placement |
| `grid` | Row and column cells | Spreadsheet-like dialogs and forms |
| `pack` | side/fill/expand/padx/pady/anchor | Flowing toolbars and stacked one-direction layouts |

For `pack`, the Layout tab edits per-widget `packSide` (`top`/`bottom`/`left`/`right`), `packFill`, `packExpand`, `packPadX`, `packPadY`, and `packAnchor`. The canvas approximates pack as a flexible row/column (flexbox), so Preview remains the authoritative rendering. Pack order follows sibling order, so z-order actions are unavailable for packed children.

Children of the same parent must use a single manager, except under `Toplevel`, `PanedWindow`, and `TtkPanedWindow`, where managers may be mixed. Validation flags mixed-manager use elsewhere.

## Export Modes

| Mode | Output | Intended use |
|---|---|---|
| Function | A single-file script with `create_window()` | A direct, small application starting point. Named widgets are exposed through `root._tkform_widgets`. |
| Class | A single-file `App(tk.Tk)` class | A class-based UI. Named widgets and Tk variables become `self.<name>` attributes. |
| Split-file | Regenerated `ui_<project>.py` plus a separate `app.py` entry point | Keep custom application logic outside the regenerated UI file. `app.py` is created only when absent. |

Generated UI code is an editable starting point, not a two-way synchronization system. Re-exporting can replace generated files. Keep custom logic outside regenerated UI files, especially when using Split-file export.

## Python Runtime Configuration

Set the preview interpreter from the designer's **Python** panel, or configure these VS Code settings:

| Setting | Purpose |
|---|---|
| `tkform.pythonPath` | Absolute Python executable for Preview. |
| `tkform.enginePythonPath` | Optional Python executable for validation and code generation. |
| `tkform.previewInheritPythonPath` | When enabled, prepends the project folder and inherits the existing `PYTHONPATH`; disabled by default. |

Preview resolution order: the designer panel, `tkform.pythonPath`, `TKFORM_PREVIEW_PYTHON`, then the engine runtime. Validation and code generation use `TKFORM_ENGINE_PYTHON`, then `tkform.enginePythonPath`, then `python3` on macOS/Linux or `python` on Windows.

## Workspace Trust and File Safety

Python-backed actions require a trusted local workspace. Explicit export destinations must be absolute paths inside a trusted workspace folder. This prevents Python execution and file export from operating in an untrusted or unrelated location.

## Related Documents

| Document | Path | Relationship |
|---|---|---|
| Getting Started | [getting-started.md](./getting-started.md) | Covers installation and first-run setup. |
| ttkbootstrap Projects | [ttkbootstrap.md](./ttkbootstrap.md) | Covers ttkbootstrap themes, bootstyles, and provider widgets. |
| Widget Animations | [animations.md](./animations.md) | Configures animations in the Inspector and carries them through Preview and Export. |
| Technical Scope | [technical-scope.md](./technical-scope.md) | Defines supported widgets, data-model features, and limits. |
| Troubleshooting and Feedback | [troubleshooting.md](./troubleshooting.md) | Provides recovery steps when a workflow action fails. |

## Change History

| Version | Date | Changes |
|---|---|---|
| v1.3 | 2026-09-06 | Added pack layout, Event Editor autocompletion, canvas-approximation notice, and the ttkbootstrap link for v1.6.0. |
| v1.2 | 2026-07-21 | Documented the responsive command bar and keyboard-navigable Inspector tabs in v1.3.1. |
| v1.1 | 2026-07-19 | Added the v1.3.0 widget-animation guide link. |
| v1.0 | 2026-07-16 | Initial English workflow guide for the public documentation repository. |
