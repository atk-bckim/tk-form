---
title: Designer Workflow
document_type: User Guide
created: 2026-07-16
last_updated: 2026-07-16
version: v1.0
status: Published
tags: [tk-form, workflow, export, preview]
---

# Designer Workflow

## Contents

- [Design Surface](#design-surface)
- [Core Workflow](#core-workflow)
- [Export Modes](#export-modes)
- [Python Runtime Configuration](#python-runtime-configuration)
- [Workspace Trust and File Safety](#workspace-trust-and-file-safety)
- [Related Documents](#related-documents)
- [Change History](#change-history)

## Design Surface

The `*.tkform.json` custom editor provides a canvas for Tkinter and ttk widgets, a property inspector, an object tree, and controls for menus, Tk variables, image resources, and non-visual components. Common design actions include drag, resize, align, snap, zoom, multi-selection, and editing properties or event code.

The bundled examples are **Login**, **Settings Panel**, and **Data Browser**. Use them as working reference designs rather than templates that must be kept unchanged.

## Core Workflow

1. **Design** — Place widgets, choose their parent container, set layout and properties, and add event logic where needed.
2. **Validate** — Run **TK-Form: Validate Project** to check the project structure, widget properties, layout rules, names, bindings, and event-handler syntax.
3. **Preview** — Run **TK-Form: Preview Project** to generate and open the interface with the selected local Python runtime. Use **TK-Form: Stop Preview** to terminate an active preview.
4. **Export** — Run **TK-Form: Export Python** and choose the destination inside the trusted workspace.

Use **TK-Form: Open Output** to inspect validation, preview, and export messages. **TK-Form: Copy Support Summary** copies a sanitized diagnostic summary for an issue report without project source or event code.

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
| Technical Scope | [technical-scope.md](./technical-scope.md) | Defines supported widgets, data-model features, and limits. |
| Troubleshooting and Feedback | [troubleshooting.md](./troubleshooting.md) | Provides recovery steps when a workflow action fails. |

## Change History

| Version | Date | Changes |
|---|---|---|
| v1.0 | 2026-07-16 | Initial English workflow guide for the public documentation repository. |
