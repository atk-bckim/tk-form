# Complex widgets & containers

Containers (can be a `parentId`): **Frame, LabelFrame, Canvas, PanedWindow, TtkPanedWindow, Notebook, Toplevel**.

`parentId` must point to one of these (else `invalid_parent_container`). A widget with `parentId: null` becomes a direct child of the root window.

## Treeview

Tabular widget (ttk). Columns + rows are declared declaratively and emitted as initial data.

```jsonc
{
  "id": "tree-customers",
  "type": "Treeview",
  "name": "customer_tree",
  "parentId": "frame-main",
  "x": 24, "y": 110, "width": 410, "height": 232,
  "props": {
    "columns": ["name", "plan", "status"],
    "columnWidths": ["140", "100", "120"],
    "rows": [
      { "values": ["Kim", "Pro", "Active"] },
      { "values": ["Lee", "Team", "Trial"] }
    ],
    "selectmode": "browse",
    "height": 10
  }
}
```

Rules:
- `columnWidths` length should match `columns` length; on load it is auto-padded/truncated to match.
- Each row's `values` length should match `columns` length, else `treeview_row_column_mismatch` (warning) and `empty_treeview_row` if a row is empty.
- Treeview is scrollable: a Scrollbar can target it via `bindings.command`.
- The first implicit column ("#0") is the tree column; the names in `columns` are the data columns.

## Notebook

Tabbed container (ttk). Tabs are implied by **child widgets** whose `parentId` is the Notebook. There is no explicit `tabs` array.

```jsonc
{ "id": "notebook-main", "type": "Notebook", "name": "main_tabs", "parentId": "frame-root", "x": 0, "y": 0, "width": 400, "height": 300, "props": {} }
```

Children:
```jsonc
{ "id": "frame-tab1", "type": "Frame", "name": "tab1_frame", "parentId": "notebook-main", "x": 0, "y": 0, "width": 380, "height": 260, "props": { "bg": "#fff" } }
```

Designer-only fields under `designer`:
- `tabIndex` — per-child, the tab order index.
- `activeTab` — on the Notebook itself, which tab is selected in the editor.

Tab labels come from the child widget's `text`-ish prop (Frame has no text, so the designer infers from `name`); in exported code, `notebook.add(child, text=...)` is emitted.

## PanedWindow / TtkPanedWindow

Two-pane or multi-pane resizable container.

```jsonc
{ "id": "paned-main", "type": "PanedWindow", "name": "main_pane", "parentId": null, "x": 0, "y": 0, "width": 400, "height": 300, "props": { "orient": "horizontal", "sashwidth": 4, "showhandle": true } }
```

- `orient` — `"horizontal"` (side-by-side) or `"vertical"` (stacked).
- Children are added as panes; **children of PanedWindow / TtkPanedWindow are exempt from the mixed-layout rule** (see layout.md).
- Use `PanedWindow` (tk) when you need `bg`/`sashwidth`/`showhandle`. Use `TtkPanedWindow` (ttk) when you want a themed look — but then those tk props are unavailable.

## Canvas

Free-form drawing surface (tk). Children of Canvas are managed widgets, but most Canvas usage is programmatic drawing in event handlers (e.g. `canvas.create_line(...)` referenced by the Canvas's `name`).

```jsonc
{ "id": "canvas-draw", "type": "Canvas", "name": "draw_canvas", "parentId": null, "x": 0, "y": 0, "width": 400, "height": 300, "props": { "bg": "#ffffff", "scrollregion": "0 0 800 600" } }
```

- `scrollregion` — `"x0 y0 x1 y1"` for scrollable canvases.
- Pair with a Scrollbar via `bindings.command` for scrolling.

## Toplevel

Secondary window. Children of Toplevel are exempt from the mixed-layout rule (they often use `grid` while the root uses `place`).

```jsonc
{ "id": "toplevel-about", "type": "Toplevel", "name": "about_window", "parentId": null, "x": 100, "y": 100, "width": 300, "height": 200, "props": { "title": "About" } }
```

- `title` — window title bar text.
- Common pattern: a Toplevel is created hidden (`withdraw()`) and shown/hidden from event handlers (`about_window.deiconify()` / `about_window.withdraw()`).

## Scrollbar (scroll wiring)

A Scrollbar drives another widget's scrolling. The wiring is **declarative via `bindings`**, not via code.

```jsonc
{
  "id": "scroll-log",
  "type": "Scrollbar",
  "name": "activity_scrollbar",
  "parentId": "frame-main",
  "x": 632, "y": 110, "width": 18, "height": 232,
  "props": { "orient": "vertical" },
  "bindings": { "command": "text-log" }
}
```

Rules (`project_validation.py:215-230`):
- `bindings.command` must reference an existing widget id.
- The target must be a scrollable type: **Text, Listbox, Entry, Treeview**.
- A Scrollbar bound to an **Entry** must have `orient: "horizontal"` (`invalid_scrollbar_entry_orientation`).
- For the reverse direction (widget → scrollbar), `bindings.xscrollcommand` / `bindings.yscrollcommand` on the *scrolled* widget can point back at a Scrollbar id — but in practice the engine emits the wiring from the Scrollbar side alone.

### Scroll wiring example (Text + vertical Scrollbar)

```jsonc
{ "id": "text-log", "type": "Text", "name": "activity_log", "parentId": "frame-main",
  "x": 468, "y": 110, "width": 164, "height": 232,
  "props": { "initialText": "Select a customer to inspect activity." } },
{ "id": "scroll-log", "type": "Scrollbar", "name": "activity_scrollbar", "parentId": "frame-main",
  "x": 632, "y": 110, "width": 18, "height": 232,
  "props": { "orient": "vertical" },
  "bindings": { "command": "text-log" } }
```

This is the canonical pattern from `examples/data-browser.tkform.json`.
