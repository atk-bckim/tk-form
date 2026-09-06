---
name: tkform-author
description: Author and modify tkform project files (*.tkform.json) — JSON descriptions of Tkinter GUIs consumed by the tkform VS Code extension. Use whenever the user wants to create, edit, extend, or fix a Tkinter GUI defined as a .tkform.json file, generate a starter form/window/dialog/menu/table, add widgets or events or Tk variables to an existing tkform project, or asks "how do I write/structure a tkform.json". Also use when the user mentions tkinter GUI, login form, settings panel, dialog, data browser, or any UI authoring task against this repo's .tkform.json format — even if they don't say "tkform" explicitly.
---

# tkform-author

This skill helps you reliably write and edit `*.tkform.json` files for the tkform VS Code extension. A `.tkform.json` file is a single JSON document describing a Tkinter GUI — canvas size, UI toolkit, widgets, events, Tk variables, menus, non-visual components (Timer/FileDialog/etc.), image resources, and animations — that the extension turns into runnable Python.

**Structural correctness** comes from the bundled JSON Schema (`references/tkform.schema.json`; same content as the extension's `schema/tkform.schema.json`). **Behavioral correctness** comes from the engine validator (`scripts/validate_project.py`). Read the references on demand for details; this file is the routing hub.

Documents the **TK-Form v1.6.0** project format (schema version 4). The loader accepts v1–v3 files and normalizes them to v4 on save, but author new files as v4.

## The 30-second mental model

```jsonc
{
  "schemaVersion": 4,
  "name": "My Window",
  "canvasWidth": 800, "canvasHeight": 600,
  "toolkit": { "name": "tkinter", "theme": "default" },  // or ttkbootstrap (see ttkbootstrap.md)
  "widgets": [ /* one object per Tkinter widget */ ],
  "menuBar": null,                 // or { menus: [...] }
  "rootBg": "#ffffff",
  "rootResizable": true,
  "variables": [],                  // StringVar/IntVar/DoubleVar/BooleanVar
  "nonVisuals": [],                 // Timer/FileDialog/... (+ ttkbootstrap-only dialogs)
  "resources": [],                  // embedded base64 images
  "animations": []                  // slide/shake/bounce/pulse/color (see animations.md)
}
```

Optional root-window extras: `rootTitle`, `rootPosition` (`"default"` | `"screenCenter"`), `rootMinWidth`/`rootMinHeight`, `rootIconImageId` (a resource id used as the window icon).

Each widget has `id`, `type` (one of 32), `name` (Python identifier), `parentId` (container id or null), `x/y/width/height`, `props` (Tkinter options), optional `events`, layout fields, and `toolkitProps` (per-toolkit options such as ttkbootstrap `bootstyle`). See `references/widgets.md` for the per-type prop allow-list.

## Minimal valid project (anchor example)

```jsonc
{
  "schemaVersion": 4,
  "name": "Demo",
  "canvasWidth": 320, "canvasHeight": 160,
  "toolkit": { "name": "tkinter", "theme": "default" },
  "widgets": [
    { "id": "label-hello", "type": "Label", "name": "hello_label", "parentId": null,
      "x": 24, "y": 24, "width": 200, "height": 28,
      "props": { "text": "Hello, world", "anchor": "w" } },
    { "id": "button-ok", "type": "Button", "name": "ok_button", "parentId": null,
      "x": 24, "y": 72, "width": 96, "height": 32,
      "props": { "text": "OK" },
      "events": { "command": "print('clicked')" } }
  ],
  "menuBar": null, "rootBg": "#ffffff", "rootResizable": true,
  "variables": [], "nonVisuals": [], "resources": [], "animations": []
}
```

## ⚠️ Traps to never trip (read these first)

These are the mistakes that pass JSON parsing but fail validation or silently misbehave. Read the linked reference before writing the affected construct.

1. **`props.command` must be a Python identifier reference, NOT inline code.** Putting `props.command: "print('x')"` fails with `invalid_command_reference`. For inline code use `events.command` instead. → `references/events.md#the-big-trap`
2. **ttk widgets cannot use `bg`/`fg`/`padx`/`pady`.** ttk types are Notebook, Progressbar, Combobox, Treeview, Sizegrip, Separator, TtkPanedWindow. They are themed via the project's `toolkit.theme`, not colored directly. Their usable props are the non-tk-styling ones in their table row. → `references/widgets.md#critical-prop-rules`
3. **ttkbootstrap-only widgets and components require the ttkbootstrap toolkit.** `DateEntry`, `LabeledScale`, `Meter`, `Floodgauge`, `Tableview`, `ScrolledText`, `ScrolledFrame`, and the six ttkbootstrap dialogs fail under `toolkit.name: "tkinter"`. Previewing ttkbootstrap projects also needs Python 3.10+ with `ttkbootstrap>=2,<3` installed. → `references/ttkbootstrap.md`
4. **Don't mix `place`/`grid`/`pack` under one parent.** Exception: children of `Toplevel`, `PanedWindow`, `TtkPanedWindow` are exempt. → `references/layout.md#the-mixed-layout-rule`
5. **`Text` widgets cannot use `textvariable`/`variable`.** Use `initialText` for content and `.get()/.insert()/.delete()` in handlers. → `references/variables.md#text-widget-cannot-use-variables`
6. **A `Scrollbar` bound to an `Entry` must be `orient: "horizontal"`.** Vertical scrollbars on Entry fail with `invalid_scrollbar_entry_orientation`. → `references/complex-widgets.md#scrollbar`
7. **`x`/`y` under `place` are relative to the parent container**, not absolute to the canvas. A widget with `parentId: "frame-main"` and `x: 10, y: 10` sits 10px inside `frame-main`. (Under `grid`/`pack`, `x`/`y` are ignored design hints.) → `references/widgets.md` (universal fields table)
8. **`bg` does not inherit from `rootBg`.** Set `bg` explicitly on each non-ttk child that needs to match the window background; ttk children pick up the active theme automatically. → `references/widgets.md#critical-prop-rules`
9. **Spatial animation presets only work on `place()` targets.** `slide`/`shake`/`bounce`/`pulse`/`grow` are rejected on `grid`- or `pack`-managed widgets, `Toplevel`, panes, and real Notebook tabs (`invalid_animation_layout`). `color` only animates classic Tk `bg`/`fg` — it is rejected on ttk themed widgets. → `references/animations.md`
10. **`fill` animations need a value widget.** `fill` animates a `Progressbar` or `Floodgauge` value (`invalid_animation_value_target` otherwise) and requires a numeric `parameters.to`. The designer's Inspector palette offers five presets; `fill`/`grow` are engine-supported but must be authored in JSON by hand. → `references/animations.md`
11. **Name identifier rules differ by object.** Event `handlerName` accepts Unicode identifiers per PEP 3131 (e.g. `保存设置`, `저장하기`); widget, Tk variable, animation, and non-visual component names are ASCII-only. All must be non-keywords, and handler names must be NFKC-stable. → `references/events.md`, `references/validation.md`
12. **Use camelCase consistently.** snake_case is accepted by the loader, but mixing the two in one file is confusing and the examples all use camelCase. → field names throughout `references/`

## Routing table — read these on demand

Don't read everything. Read the file that matches the task.

| If the task is… | Read |
|---|---|
| Adding/placing a widget, picking props, choosing a widget type | `references/widgets.md` |
| Using ttkbootstrap: toolkit block, themes, bootstyle, provider widgets | `references/ttkbootstrap.md` |
| Adding declarative animations (slide/shake/bounce/pulse/color) | `references/animations.md` |
| Treeview, Notebook, PanedWindow, Canvas, Toplevel, or Scrollbar wiring | `references/complex-widgets.md` |
| Wiring up a click / hover / key handler, or anything with `events` | `references/events.md` |
| Adding StringVar/IntVar/etc., or wiring `variable`/`textvariable` | `references/variables.md` |
| Switching between `place`, `grid`, and `pack`, or hitting `mixed_layout_manager` | `references/layout.md` |
| Adding the menu bar / menus / menu items / shortcuts | `references/menus.md` |
| Adding a Timer / FileDialog / ColorChooser / MessageBox / ttkbootstrap dialogs | `references/non-visuals.md` |
| Embedding an image (logo, icon, illustration) | `references/resources.md` |
| A diagnostic came back and you don't know what it means | `references/validation.md` |
| You want the full list of limits / error codes | `references/validation.md` |

## Standard workflow

1. **Read** the existing file (if editing) or start from the **minimal valid project** above (if creating).
2. **Consult** the relevant reference from the routing table before writing unfamiliar constructs.
3. **Write** the change. Match the surrounding style (camelCase, id convention like `<type>-<slug>`).
4. **Validate** by running:
   ```bash
   python path/to/tkform-author/scripts/validate_project.py path/to/file.tkform.json
   ```
   If the script cannot find the extension engine, point it at it:
   ```bash
   python path/to/tkform-author/scripts/validate_project.py --engine-root /path/to/tkform/python path/to/file.tkform.json
   ```
5. **Fix** every error-severity diagnostic. Warnings are usually worth fixing too.
6. **Repeat** 4–5 until the script prints `OK`.
7. Report what you changed. Don't claim success until the validator passes.

The script uses the SAME engine the VS Code extension uses. It resolves Python in this order: `--python`, `TKFORM_ENGINE_PYTHON`, workspace `tkform.enginePythonPath`, workspace `tkform.pythonPath`, then `python3`/`python`. It resolves the engine root from `--engine-root`, `TKFORM_ENGINE_ROOT`, or a nearby `python/tkform_engine` directory. Structural validation of ttkbootstrap projects works without the ttkbootstrap package installed (only Preview needs it).

## Useful patterns from the examples

The extension ships six reference projects — open them with **TK-Form: Open Example Project** (Login, Settings Panel, Data Browser, Ttkbootstrap Login, Ttkbootstrap Widgets, Ttkbootstrap Dialogs) and read the generated `.tkform.json` when the user's request resembles one:

| Example | Pattern |
|---|---|
| `login.tkform.json` | Smallest. Frame + Label/Entry/Button, map-form `events.command`, password Entry with `show: "*"`. |
| `settings-panel.tkform.json` | Tk variables (StringVar + BooleanVar) bound via `textvariable`/`variable`, Combobox with values + default, Scale, **array-form events** with both `command` and `bind` kinds. |
| `data-browser.tkform.json` | Treeview with columns/rows, Text with `initialText`, **Scrollbar wiring** (`bindings.command`), menu bar with accelerator + acceleratorBinding, map-form event with `handlerName`. |
| `ttkbootstrap-login.tkform.json` | Same login shape under `toolkit: {name: "ttkbootstrap", majorVersion: 2}` with a themed look. |
| `ttkbootstrap-widgets.tkform.json` | Provider widgets (Meter, Floodgauge, Tableview, DateEntry, …) with `toolkitProps.ttkbootstrap.bootstyle`. |
| `ttkbootstrap-dialogs.tkform.json` | TtkMessagebox, Querybox, DatePickerDialog, ColorPickerDialog, ToastNotification, ToolTip components. |

## When NOT to use this skill

- The user is editing the extension itself (TypeScript/React/Python engine) — not authoring a `.tkform.json`.
- The user wants generated **Python** code (`.py`) directly — that's the export output, not the source format. The tkform source is always JSON.
- The user wants raw Tkinter code outside the tkform ecosystem.

In those cases, fall back to normal coding without this skill.
