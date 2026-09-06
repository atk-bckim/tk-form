# Layout

Tkinter offers three geometry managers (`place`, `grid`, `pack`). tkform supports **`place`** and **`grid`**, set per-widget via `layoutManager`.

## Per-widget selection

```jsonc
{ "id": "label-foo", "type": "Label", "name": "foo_label", "parentId": "frame-main",
  "x": 24, "y": 24, "width": 100, "height": 28,
  "layoutManager": "place",          // or "grid", or omit (= "place")
  "props": { "text": "Foo" } }
```

For `grid`, the relevant fields are `gridRow`, `gridCol`, `gridRowSpan`, `gridColSpan`, `gridSticky`, `gridPadX`, `gridPadY`, `gridIPadX`, `gridIPadY`:

```jsonc
{ "id": "label-foo", "type": "Label", "name": "foo_label", "parentId": "frame-main",
  "x": 0, "y": 0, "width": 100, "height": 28,        // x/y/w/h are design hints under grid
  "layoutManager": "grid",
  "gridRow": 0, "gridCol": 0, "gridRowSpan": 1, "gridColSpan": 2,
  "gridSticky": "ew", "gridPadX": 4, "gridPadY": 2,
  "props": { "text": "Foo" } }
```

`x`, `y`, `width`, `height` are still required by the schema for canvas display, but under `grid` they're just designer hints and have no effect on the generated layout.

## ⚠️ The mixed-layout rule (important)

**All children of the same parent MUST use the same `layoutManager`.** If you mix `place` and `grid` under one parent, the engine emits `mixed_layout_manager`:

> "A single Tkinter parent cannot mix grid and place managed children."

This is a hard Tkinter limitation — Tkinter itself deadlocks or misbehaves when you mix managers within one parent.

### Two exceptions

Children of these parent types are **exempt** from the rule (per `project_validation.py:114-134`):

| Parent type | Why exempt |
|---|---|
| `Toplevel` | Toplevel is a separate window; its children are managed independently of the root. |
| `PanedWindow` / `TtkPanedWindow` | Panes are added via `add()`, not via grid/place, so the manager on the child is ignored anyway. |

So this is fine:

```jsonc
// root window: place children
{ "id": "frame-root", "type": "Frame", "parentId": null, "layoutManager": "place", ... }

// Toplevel child: grid is OK even though siblings use place
{ "id": "toplevel-settings", "type": "Toplevel", "parentId": null,
  "props": { "title": "Settings" } }
{ "id": "label-foo", "type": "Label", "parentId": "toplevel-settings",
  "layoutManager": "grid", "gridRow": 0, "gridCol": 0, ... }
```

## Containers (valid `parentId` targets)

A widget's `parentId` must reference a widget of one of these types, else `invalid_parent_container`:

- `Frame`
- `LabelFrame`
- `Canvas`
- `PanedWindow`
- `TtkPanedWindow`
- `Notebook`
- `Toplevel`

`parentId: null` means the widget is a direct child of the root window.

## Nesting depth

Maximum widget nesting depth is **64** (`MAX_NESTING_DEPTH`). Exceeding it → `max_widget_nesting_depth_exceeded`. In practice you'll never hit this; it's a guard against cycles.

Cycles (A's parent is B, B's parent is A) → `parent_cycle`. Orphaned parent references (parentId points at a non-existent id) → `orphan_parent_reference`.

## Choosing place vs grid

| Use `place` when | Use `grid` when |
|---|---|
| You want pixel-exact positioning (designer-friendly) | You want a form that resizes cleanly |
| Drag-and-drop in the canvas matters | You have aligned label/input rows |
| Quick prototypes | Production forms with consistent layouts |

The designer defaults to `place`. For form-heavy UIs, switch the children of a Frame to `grid` together.
