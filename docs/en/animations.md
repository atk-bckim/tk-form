---
title: Widget Animations
document_type: User Guide
created: 2026-07-19
last_updated: 2026-09-06
version: v1.2
status: Published
tags: [tk-form, animation, tkinter, preview, export]
---

# Widget Animations

## Contents

- [Overview](#overview)
- [Add and Edit an Animation](#add-and-edit-an-animation)
- [Common Settings](#common-settings)
- [Preset Settings](#preset-settings)
- [Triggers and Manual Control](#triggers-and-manual-control)
- [Validate, Preview, and Export](#validate-preview-and-export)
- [Generated Python API](#generated-python-api)
- [Limits and Troubleshooting](#limits-and-troubleshooting)
- [Related Documents](#related-documents)
- [Change History](#change-history)

## Overview

TK-Form provides declarative widget animations scheduled through Tkinter `after` callbacks (introduced in v1.3.0). Animations are stored in the project file's `animations` array and participate in the same Validate, Preview, and Function/Class/Split-file Export workflows.

Set the target widget's final position and size before creating an animation. Spatial animations require a widget that is actually emitted with `place()` in generated Python.

## Add and Edit an Animation

1. Select the target widget on the canvas or in the object tree.
2. In the Inspector, open **Animations** and select **Add Animation**.
3. Enter a unique Python identifier for the name, such as `show_panel`.
4. Choose a preset and trigger, then configure timing, repeats, and preset-specific values.
5. Select **Save**, then run **Validate** and **Preview**.

Use **Edit** to change an existing item and **Remove** to delete it. Names must be unique within the project and cannot collide with Python keywords, TK-Form generator-reserved names, event handlers, or other generated symbols.

## Common Settings

| Setting | Accepted values | Purpose |
|---|---|---|
| Name | Unique Python identifier | Forms the `start_<name>()` and `stop_<name>()` APIs. |
| Duration | Greater than 0, up to 600,000 ms | Time for one playback iteration. |
| Delay | 0–86,400,000 ms | Time to wait before playback starts. |
| Easing | `linear`, `easeIn`, `easeOut`, `easeInOut` | Progress curve. |
| Repeat count | 1–10,000 | Total playback iterations. |
| Infinite repeat | On/off | Repeats until explicitly stopped. |

A project can contain up to 500 animations. New animations default to 300 ms, no delay, `easeOut`, and one iteration.

## Preset Settings

| Preset | Parameters | Behavior |
|---|---|---|
| `slide` | `direction`: left/right/up/down, `distance`: 0–1,000,000 | Moves from the directional offset to the final position. |
| `shake` | `axis`: x/y, `distance`: 0–1,000,000, `cycles`: 1–10,000 | Applies a decaying oscillation around the final position. |
| `bounce` | `direction`: left/right/up/down, `distance`: 0–1,000,000, `cycles`: 1–10,000 | Moves in the selected direction and returns to the final position. |
| `pulse` | `scale`: greater than 0, up to 1,000 | Grows around the widget center and returns to its final size. |
| `color` | `property`: bg/fg, `to`: `#RGB` or `#RRGGBB` | Interpolates from the current color to the target color. |

`slide`, `shake`, `bounce`, and `pulse` require widgets emitted with `place()`. `color` is available only for classic Tk widgets that safely support the selected `bg` or `fg` property. ttk themed widgets (ttkbootstrap Button, Label, Entry, Frame, and similar) have no `bg`/`fg` options, so the `color` preset is rejected during validation. Classic Tk widgets such as `Text`, `Canvas`, and `Listbox` remain usable with `color` in ttkbootstrap projects.

## Triggers and Manual Control

| Trigger | Start condition |
|---|---|
| `load` | Starts during the generated window's initial idle processing. |
| `click` | Mouse click on the target widget. |
| `hoverEnter` / `hoverLeave` | Pointer enters or leaves the target widget. |
| `focusIn` / `focusOut` | Target widget gains or loses keyboard focus. |
| `manual` | No automatic binding; application code calls the generated API. |

Starting the same animation again cancels its pending callback and replaces the active playback. Stop an `infinite` animation with the generated `stop_<name>()` API.

## Validate, Preview, and Export

1. **Validate** checks target IDs, names, layout, preset parameters, color support, and generated-symbol collisions.
2. **Preview** runs the real `after` callbacks and widget layout with the selected Tkinter runtime.
3. **Export** emits the validated animation runtime and start/stop APIs.

If the Output Dock or VS Code Problems reports an error, use **Edit** to correct that animation. An orphan animation whose target widget was removed may provide a removal Quick Fix.

## Generated Python API

An animation named `show_panel` produces:

```python
start_show_panel()
stop_show_panel()
```

- Function Export creates the functions and also exposes them as `root.start_show_panel` and `root.stop_show_panel`.
- Class Export creates `App.start_show_panel()` and `App.stop_show_panel()` methods.
- Split-file Export provides the same methods on the generated UI class, callable from its instance in `app.py`.

Inside an Event Editor handler, call the same-named callable provided by that export mode. Keep application playback logic in a preserved application file instead of regenerated `ui_<project>.py`.

## Limits and Troubleshooting

- A real `Notebook` tab is emitted as a synthetic `ttk.Frame` managed by Tk and cannot be an animation target. A normal child placed inside that tab can be animated.
- Spatial presets do not support `grid` widgets, `Toplevel`, or panes directly managed by `PanedWindow`/`TtkPanedWindow`.
- If a color preset is rejected, confirm that the target widget supports the selected `bg` or `fg` property.
- Invalid values preserved from an external project remain visible in the Inspector and block Save until corrected.
- If Preview does not move the widget, run **Validate** first and confirm the selected Python runtime includes Tkinter.
- Avoid name collisions with widgets, Tk variables, resources, event handlers, generated menu handlers, and other animation APIs.

## Related Documents

| Document | Path | Relationship |
|---|---|---|
| Getting Started | [getting-started.md](./getting-started.md) | Installs v1.6.0 and prepares Python. |
| Designer Workflow | [designer-workflow.md](./designer-workflow.md) | Covers the Validate, Preview, and Export sequence. |
| ttkbootstrap Projects | [ttkbootstrap.md](./ttkbootstrap.md) | Includes animation restrictions in ttkbootstrap projects. |
| Technical Scope | [technical-scope.md](./technical-scope.md) | Defines the project format, supported features, and safety limits. |
| Troubleshooting and Feedback | [troubleshooting.md](./troubleshooting.md) | Provides runtime and diagnostic recovery steps. |

## Change History

| Version | Date | Changes |
|---|---|---|
| v1.2 | 2026-09-06 | Added the ttk themed color-preset rejection rule and the ttkbootstrap link for v1.6.0. |
| v1.1 | 2026-07-21 | Updated the release reference for v1.3.1. |
| v1.0 | 2026-07-19 | Added the TK-Form v1.3.0 widget-animation guide. |
