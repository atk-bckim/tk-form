---
title: Technical Scope
document_type: Reference
created: 2026-07-16
last_updated: 2026-07-16
version: v1.0
status: Published
tags: [tk-form, architecture, tkinter, scope]
---

# Technical Scope

## Contents

- [Release Scope](#release-scope)
- [Architecture and Data Flow](#architecture-and-data-flow)
- [Project Model](#project-model)
- [Supported Design Features](#supported-design-features)
- [Supported Widget Types](#supported-widget-types)
- [Validation and Safety Limits](#validation-and-safety-limits)
- [Current Boundaries](#current-boundaries)
- [Related Documents](#related-documents)
- [Change History](#change-history)

## Release Scope

This reference describes the public **TK-Form v1.2.1** VSIX release. It is a visual authoring and code-generation tool for practical Tkinter applications, not a general-purpose IDE or a two-way editor for handwritten Python.

## Architecture and Data Flow

| Layer | Current implementation |
|---|---|
| VS Code integration | TypeScript extension host, a `*.tkform.json` custom editor, extension commands, workspace-trust enforcement, output, Preview process management, and export file access. |
| Designer webview | React, Vite, Tailwind CSS, Zustand state management, `dnd-kit` interaction support, and CodeMirror Python editing support. |
| Project format | JSON Schema draft-07 for `*.tkform.json`; new files use schema version 2. |
| Python engine | Bundled `tkform_engine` package using the Python standard library and Tkinter/ttk for validation, Python generation, and Preview. |

The normal data path is:

```text
*.tkform.json → TK-Form custom editor → extension host → bundled Python engine
                                              ├─ diagnostics and output
                                              ├─ Preview process
                                              └─ generated Python files
```

The designer normalizes loaded projects to schema version 2. Files written as version 1 are accepted and migrated when saved.

## Project Model

A project describes a root window plus widgets, menus, Tk variables, image resources, and non-visual components. Widget IDs are stable internal references; widget names must be valid, unique Python identifiers and become names in generated Python.

The model supports:

- Root-window dimensions, background, resize behavior, and ttk theme selection.
- `place` and `grid` layout managers. Children of the same parent must use one manager, except under `Toplevel`, `PanedWindow`, and `TtkPanedWindow`.
- An Event Editor for `command` handlers and Tk binding sequences such as `<Button-1>` or `<Key>`.
- Menu hierarchies, menu commands, and accelerator bindings.
- `StringVar`, `IntVar`, `DoubleVar`, and `BooleanVar` declarations.
- Base64 image resources referenced by widget ID.
- `Timer`, `FileDialog`, `ColorChooser`, and `MessageBox` non-visual components.
- Canonical Scrollbar bindings through `bindings.command`; legacy `xscrollcommand` and `yscrollcommand` are accepted for compatibility.

For a Scrollbar, horizontal targets are `Text`, `Listbox`, `Entry`, `Treeview`, and `Canvas`; vertical targets are `Text`, `Listbox`, `Treeview`, and `Canvas`.

## Supported Design Features

The visual editor supports canvas placement, drag and resize, alignment, snapping, zoom, multi-selection, an object tree, property editing, menus, variables, resources, and non-visual components. The project validator checks cross-references, duplicate or reserved names, property compatibility, layout consistency, bindings, payload limits, and event-handler syntax before code generation.

The legacy widget `props.command` field accepts a Python function reference only. Put inline Python logic in the Event Editor; when both are present, the Event Editor command takes precedence.

## Supported Widget Types

| Group | Widget types |
|---|---|
| Common controls | `Button`, `Label`, `Entry`, `Text`, `Checkbutton`, `Radiobutton`, `Listbox`, `Scale`, `OptionMenu`, `Spinbox`, `Scrollbar`, `Menubutton`, `Message` |
| Containers and layout | `Frame`, `LabelFrame`, `Canvas`, `PanedWindow`, `TtkPanedWindow`, `Notebook`, `Toplevel` |
| ttk additions | `Progressbar`, `Combobox`, `Treeview`, `Sizegrip`, `Separator` |

`Notebook`, `Progressbar`, `Combobox`, `Treeview`, `Sizegrip`, `Separator`, and `TtkPanedWindow` use ttk constructors. Their supported properties differ from classic Tk widgets; for example, classic visual properties such as `bg`, `fg`, `padx`, and `pady` are not supported in the same way.

## Validation and Safety Limits

| Limit | Maximum |
|---|---:|
| Project payload | 8 MiB |
| Image upload | 5 MiB per image |
| Widgets | 2,000 |
| Resources | 200 |
| Tk variables | 500 |
| Non-visual components | 500 |
| Widget and menu nesting | 64 levels |

Python-backed actions require a trusted local workspace. Explicit Export destinations must be absolute paths inside a trusted workspace folder. Preview requires a local Python runtime with Tkinter.

## Current Boundaries

- Generated Python is a starting point. TK-Form does not preserve manual edits inside files that it regenerates and does not provide two-way synchronization with handwritten Python.
- The canvas approximates Tk layout. Validate and Preview before treating the design canvas as final runtime layout.
- Split-file export protects an existing `app.py`, but rewrites `ui_<project>.py` on subsequent export.
- The legacy `command` property cannot hold inline Python code; use the Event Editor.
- `Text` does not support `textvariable`.
- `Entry` supports horizontal Scrollbar binding only.
- The product focuses on practical, commonly used single-window forms and internal tools; automated licensing, in-app account management, and broad enterprise self-service are not included.

## Related Documents

| Document | Path | Relationship |
|---|---|---|
| Getting Started | [getting-started.md](./getting-started.md) | Installs the release and prepares the runtime. |
| Designer Workflow | [designer-workflow.md](./designer-workflow.md) | Applies these capabilities during design, Preview, and Export. |
| Troubleshooting and Feedback | [troubleshooting.md](./troubleshooting.md) | Helps diagnose limits and validation failures. |

## Change History

| Version | Date | Changes |
|---|---|---|
| v1.0 | 2026-07-16 | Initial technical-scope reference for the public documentation repository. |
