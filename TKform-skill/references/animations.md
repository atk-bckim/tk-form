# Animations

Declarative widget animations stored in the top-level `animations[]` array and executed in generated Python via Tkinter `after` callbacks. Introduced in v1.3.0; validated by `python/tkform_engine/validation_animations.py`.

## Shape

```jsonc
"animations": [
  {
    "id": "anim-panel-in",
    "name": "show_panel",
    "targetWidgetId": "frame-panel",
    "preset": "slide",
    "trigger": "load",
    "durationMs": 300,
    "delayMs": 0,
    "easing": "easeOut",
    "repeatCount": 1,
    "parameters": { "direction": "left", "distance": 120 }
  }
]
```

| Field | Required | Notes |
|---|---|---|
| `id` | yes | Stable unique id (`duplicate_animation_id`). |
| `name` | yes | **ASCII** Python identifier, unique across animations (`invalid_animation_name`, `duplicate_animation_name`). Must not collide with generator reserved names, event handlers, or other generated symbols (`reserved_name_collision`, `animation_symbol_collision`). |
| `targetWidgetId` | yes | An existing widget id (`missing_animation_target`). |
| `preset` | yes | One of `slide`, `shake`, `bounce`, `pulse`, `color`, `fill`, `grow` (see below). The Inspector palette offers the first five; `fill`/`grow` are engine-supported and authored in JSON by hand. |
| `trigger` | no | Default `manual`. One of `load`, `click`, `hoverEnter`, `hoverLeave`, `focusIn`, `focusOut`, `manual` (`invalid_animation_trigger`). |
| `durationMs` | no | Default `300`. Number > 0, ≤ 600,000 (`invalid_animation_duration`). |
| `delayMs` | no | Default `0`. Number 0–86,400,000 (`invalid_animation_delay`). |
| `easing` | no | Default `easeOut`. One of `linear`, `easeIn`, `easeOut`, `easeInOut` (`invalid_animation_easing`). The schema enum also lists `backOut`/`elasticOut`/`bounceOut`, but the engine validator rejects them — do not use. |
| `repeatCount` | no | Default `1`. Integer 1–10,000 or the string `"infinite"` (`invalid_animation_repeat`). |
| `parameters` | preset-specific | See the preset table. Wrong values → `invalid_animation_parameter`. |

Maximum 500 animations per project (enforced by the designer's payload limit; the Python validator does not count them).

## Presets

| Preset | Parameters | Behavior |
|---|---|---|
| `slide` | `direction`: `left`/`right`/`up`/`down`, `distance`: 0–1,000,000 | Moves from the directional offset to the final position. |
| `shake` | `axis`: `x`/`y`, `distance`: 0–1,000,000, `cycles`: 1–10,000 | Decaying oscillation around the final position. |
| `bounce` | `direction`: `left`/`right`/`up`/`down`, `distance`: 0–1,000,000, `cycles`: 1–10,000 | Moves in the direction and returns. |
| `pulse` | `scale`: > 0, ≤ 1,000 | Grows around the widget center and returns to its size. |
| `color` | `property`: `bg`/`fg`, `to`: `#RGB` or `#RRGGBB` | Interpolates the color (`invalid_animation_color` on a bad hex value). |
| `fill` | `from`: number (optional, defaults to the widget's current value), `to`: number (required), both within ±1,000,000 | Animates a value widget's filled amount — the target **must** be a `Progressbar` or `Floodgauge` (`invalid_animation_value_target` otherwise). |
| `grow` | none | The widget grows from zero to its designed size, centered on the same spot (a spatial effect). |

### Target restrictions

- `slide`, `shake`, `bounce`, `pulse`, `grow` (the spatial presets) require a target that generated code lays out with `place()` (`invalid_animation_layout`). Rejected targets: `grid`- or `pack`-managed widgets, `Toplevel`, widgets inside `PanedWindow`/`TtkPanedWindow` panes, and real `Notebook` tabs (tabs are synthetic `ttk.Frame`s — `invalid_animation_notebook_tab`). A normal child placed inside a Notebook tab is fine.
- `color` requires a target that safely supports the chosen `bg`/`fg` option (`invalid_animation_color_target`). ttk themed widgets — including every ttkbootstrap widget (Button, Label, Entry, Frame, …) — are rejected. Classic Tk widgets (`Text`, `Canvas`, `Listbox`, …) work even in ttkbootstrap projects.
- `fill` requires a `Progressbar` or `Floodgauge` target (`invalid_animation_value_target`).

## Triggers

| Trigger | Start condition |
|---|---|
| `load` | Auto-starts during the generated window's initial idle processing. |
| `click` | Mouse click on the target widget. |
| `hoverEnter` / `hoverLeave` | Pointer enters / leaves the target. |
| `focusIn` / `focusOut` | Target gains / loses keyboard focus. |
| `manual` | No binding; call the generated API from your own code. |

Restarting an animation cancels its pending callback and replaces the playback. Stop an `infinite` animation with the generated stop API.

## Generated Python API

An animation named `show_panel` generates:

```python
start_show_panel()
stop_show_panel()
```

- Function export: the functions exist in `create_window()` and are also exposed as `root.start_show_panel` / `root.stop_show_panel`.
- Class / Split-file export: `App.start_show_panel()` / `App.stop_show_panel()` methods.

Inside event-handler code, call the same-named callable that the current export mode provides (bare names work — see events.md). Example of a `manual` animation started from a button:

```jsonc
{ "id": "button-show", "type": "Button", "name": "show_button", "parentId": null,
  "x": 24, "y": 120, "width": 96, "height": 32,
  "props": { "text": "Show panel" },
  "events": { "command": { "handlerName": "on_show", "code": "start_show_panel()" } } }
```

## Example (slide on load)

```jsonc
{
  "schemaVersion": 4,
  "name": "Animated",
  "canvasWidth": 320, "canvasHeight": 160,
  "toolkit": { "name": "tkinter", "theme": "default" },
  "widgets": [
    { "id": "frame-panel", "type": "Frame", "name": "panel_frame", "parentId": null,
      "x": 20, "y": 20, "width": 280, "height": 120,
      "props": { "bg": "#eef2f7" } }
  ],
  "animations": [
    { "id": "anim-panel-in", "name": "show_panel", "targetWidgetId": "frame-panel",
      "preset": "slide", "trigger": "load",
      "durationMs": 300, "delayMs": 0, "easing": "easeOut", "repeatCount": 1,
      "parameters": { "direction": "left", "distance": 120 } }
  ],
  "variables": [], "nonVisuals": [], "resources": [], "menuBar": null,
  "rootBg": "#ffffff", "rootResizable": true
}
```

Validate after authoring — the validator checks target layout, color support, parameters, and symbol collisions (see validation.md).
