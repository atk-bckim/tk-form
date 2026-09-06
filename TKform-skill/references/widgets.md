# Widgets

Every entry in `widgets[]` becomes a Tkinter widget in the generated Python. This file is the **authoritative allow-list of which `props` keys each widget type accepts**.

Source of truth: `python/tkform_engine/widget_spec.py` (`WIDGET_ALLOWED_PROPS`).

## Universal widget fields (outside `props`)

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | string | yes | Unique. Target of `parentId` / `bindings.command`. |
| `type` | enum (25) | yes | See table below. |
| `name` | Python identifier | yes | Becomes `self.<name>` in generated code. Unique across widgets. |
| `parentId` | string \| null | no | Must reference a container (see Containers). null = child of root window. |
| `x`, `y` | number | no | Position. Under `place`: **relative to the parent container's top-left** (or the root window if `parentId` is null) — standard Tkinter `place` semantics, NOT absolute-to-canvas. Under `grid`: design hint only, ignored at codegen. |
| `width`, `height` | integer ≥1 | no | **Layout** sizing in pixels under `place` (defaults 100 × 32). Note this is distinct from `props.width` / `props.height` (Tkinter's type-specific units — character columns for Entry, character columns × rows for Text, etc.). A widget can have both: e.g. `{ "width": 130, "height": 24, "props": { "width": 20 } }` means 130×24 px placed, with Entry content sized to 20 chars. |
| `props` | object | no | Tkinter options. Per-type allow-list below. |
| `events` | object \| array | no | See events.md. |
| `bindings` | object | no | Scroll wiring (see complex-widgets.md). |
| `layoutManager` | `"place"` \| `"grid"` | no | Default `place`. See layout.md. |
| `grid*` (Row/Col/RowSpan/ColSpan/Sticky/PadX/PadY/IPadX/IPadY) | number/string | no | Only meaningful under `grid`. |
| `locked`, `designer` | – | no | Designer-only; no effect on generated code. |

## Critical prop rules (read first)

1. **`props.command` must be a Python identifier reference** (e.g. `"self.on_click"` or `"on_click"`). Putting inline code like `"print(1)"` here is a validation error (`invalid_command_reference`). For inline code, use `events.command` instead. See events.md.
2. **`props.variable` / `props.textvariable`** must name a variable declared in `variables[]`. Engine emits `missing_variable_reference` otherwise. Exception: **Text** widgets cannot use `textvariable`/`variable` at all (`WIDGET_UNSUPPORTED_PROPS`).
3. **`props.image`** must reference a resource id in `resources[]`. Engine emits `missing_image_resource` otherwise.
4. **ttk widgets** (marked 🟦 below) **cannot use** `bg`, `fg`, `padx`, `pady`, `compound`, `underline`, `disabledforeground`, `highlightthickness`, `selectbackground`, `insertbackground`, `undo`, `wrap`, `tabs`, `spacing1/2/3`. They are silently dropped or rejected depending on the widget. The props ttk widgets *can* use are the non-tk-styling ones in their row of the table below (e.g. a Combobox accepts `values`, `value`, `state`, `width`; a Treeview accepts `columns`, `rows`, etc.). When in doubt, run the validator. If the user asks to color/style a ttk widget, tell them ttk widgets are themed via `tkTheme`, not direct bg/fg props.
5. **`bg` does not inherit.** `rootBg` colors only the root window; child widgets use Tkinter's default background unless you set `bg` on each non-ttk child explicitly. (ttk children get their background from the active `tkTheme`.) If the user wants a uniform background, set `bg` on every relevant non-ttk widget to match `rootBg`.
6. **`font` format.** Accepts a Tkinter font spec. Two string forms work: a space-separated string (`"TkDefaultFont 14 bold"`, `"Helvetica 10"`) — case-insensitive modifiers `bold`/`italic`/`underline`/`overstrike` may trail; or a Python-tuple literal string (`"(\"Helvetica\", 10, \"bold\")"`). Named fonts like `"TkDefaultFont"` are also valid. ttk widgets generally accept `font` (e.g. Combobox, Treeview headings) — the per-type table marks it where supported.
7. **Numeric-looking values must still be strings.** `values` on Combobox/OptionMenu/Spinbox, `items` on Listbox, `columns`/`columnWidths` on Treeview are all normalized to `string[]`. Pass numbers as strings (`["9600", "19200"]`, not `[9600, 19200]`) — the engine stringifies them anyway, but explicit strings avoid surprises and match the examples. The same applies to a Combobox's default `value`.

## The 25 widget types

🟦 = ttk widget (themed; cannot use bg/fg/padx/pady). 📦 = container (can be a `parentId`). 🔄 = scrollable (can be the target of a Scrollbar `bindings.command`).

| Type | Cat | Common use | Notable props |
|---|---|---|---|
| `Button` |  | Click action | `text`, `command` (ref only), `bg`, `fg`, `font`, `padx`, `pady`, `compound`, `underline`, `disabledforeground`, `image` |
| `Label` |  | Static text / image | `text`, `image`, `compound`, `anchor`, `bg`, `fg`, `font`, `wraplength`, `justify` |
| `Entry` | 🔄 | Single-line input | `textvariable`, `show` (e.g. `"*"`), `width`, `state`, `selectbackground`, `insertbackground`, `highlightthickness` |
| `Text` | 🔄 | Multi-line input | `initialText`, `width`, `height`, `wrap`, `undo`, `tabs`, `spacing1/2/3`, **no `textvariable`/`variable`** |
| `Checkbutton` |  | Boolean toggle | `text`, `variable`, `onvalue`/`offvalue` (via `value`), `bg`, `fg`, `command` (ref only) |
| `Radiobutton` |  | Mutually-exclusive choice | `text`, `variable`, `value`, `bg`, `fg`, `command` (ref only) |
| `Listbox` | 🔄 | Selectable item list | `items` (string[]), `selectmode` (`"browse"`/`"single"`/`"multiple"`/`"extended"`), `height`, `selectbackground`, `highlightthickness` |
| `Scale` |  | Numeric slider | `from_`, `to`, `orient` (`"horizontal"`/`"vertical"`), `length`, `variable`, `command` (ref only) |
| `Frame` | 📦 | Plain container | `bg`, `relief`, `bd`, `width`, `height`, `highlightthickness` |
| `LabelFrame` | 📦 | Labeled container | `text`, `bg`, `relief`, `bd`, `highlightthickness` |
| `Canvas` | 📦 | Drawing surface | `bg`, `scrollregion`, `highlightthickness`, `width`, `height` |
| `PanedWindow` | 📦 | Resizable panes (tk) | `orient`, `sashwidth`, `showhandle`, `bg`, `relief`, `bd` |
| `TtkPanedWindow` | 🟦📦 | Resizable panes (ttk) | `orient` only — very limited ttk styling |
| `OptionMenu` |  | Dropdown (tk) | `values` (string[]), `variable`, `command` (ref only), `text` |
| `Spinbox` |  | Numeric stepper | `from_`, `to`, `increment`, `textvariable`, `width`, `values`, `command` (ref only), `selectbackground`, `insertbackground` |
| `Scrollbar` |  | Scroller | `orient` (`"horizontal"`/`"vertical"`), plus `bindings.command` = target widget id (see complex-widgets.md) |
| `Separator` | 🟦 | Horizontal/vertical rule | `orient` only |
| `Notebook` | 🟦📦 | Tabbed container | Limited props; tabs are implied by children. `designer.activeTab` selects a tab in the editor. |
| `Toplevel` | 📦 | Secondary window | `title`, `bg`, `relief`, `bd`. Children of Toplevel are exempt from the mixed-layout rule (see layout.md). |
| `Progressbar` | 🟦 | Progress indicator | `orient`, `mode` (`"determinate"`/`"indeterminate"`), `length`, `maximum` |
| `Combobox` | 🟦 | Editable dropdown (ttk) | `values` (string[]), `value` (default), `state` (`"normal"`/`"readonly"`/`"disabled"`). Cross-check: `value` should be one of `values` (else `invalid_default_value` warning). Set `state: "readonly"` to make the dropdown non-editable (user can only pick from `values`). |
| `Treeview` | 🟦🔄📦 | Tabular data | `columns` (string[]), `columnWidths` (string[]), `rows` (`[{values: string[]}]`), `selectmode`, `height`. See complex-widgets.md. |
| `Sizegrip` | 🟦 | Bottom-right resize handle | (no meaningful props) |
| `Menubutton` |  | Button that opens a menu | `text`, `bg`, `fg`, `padx`, `pady`, `compound`, `underline` |
| `Message` |  | Wrapped multi-line text (tk) | `text`, `padx`, `pady`, `highlightthickness`, `bg`, `fg`, `font`, `anchor`, `width`, `aspect` |

## Common props accepted by almost every non-ttk widget

`text`, `command` (ref only), `bg`, `fg`, `font`, `relief`, `state`, `bd`, `anchor`, `wraplength`, `justify`, `cursor`, `takefocus`, `width`, `height`.

The full per-type union lives in `widget_spec.py:COMMON_PROPS` plus a small extension set per type. When in doubt, run `scripts/validate_project.py` — unsupported props surface as `unsupported_widget_prop`.

## Data-bearing props (normalized on load)

These props get special normalization in `projectSerialization.ts:174-196` — pass them as JSON arrays/strings as shown:

| Prop | Types | Accepted forms | Stored as |
|---|---|---|---|
| `values` | Combobox, OptionMenu, Spinbox | `["A","B"]` or `"A,B"` or `"A\nB"` | string[] |
| `items` | Listbox | same as above | string[] |
| `columns` | Treeview | same | string[] |
| `columnWidths` | Treeview | same; auto-aligned to `columns` length | string[] |
| `rows` | Treeview | `[{values:["a","b"]}, ...]` or `[["a","b"], ...]` | `{values: string[]}[]` |
| `initialText` | Text | string; default `""` if missing | string |

## Minimal example (the smallest useful widget set)

```jsonc
{
  "schemaVersion": 2,
  "name": "Demo",
  "canvasWidth": 320,
  "canvasHeight": 160,
  "widgets": [
    {
      "id": "label-hello",
      "type": "Label",
      "name": "hello_label",
      "parentId": null,
      "x": 24, "y": 24, "width": 200, "height": 28,
      "props": { "text": "Hello, world", "anchor": "w" }
    },
    {
      "id": "button-ok",
      "type": "Button",
      "name": "ok_button",
      "parentId": null,
      "x": 24, "y": 72, "width": 96, "height": 32,
      "props": { "text": "OK" },
      "events": { "command": "print('clicked')" }
    }
  ],
  "menuBar": null,
  "rootBg": "#ffffff",
  "rootResizable": true,
  "tkTheme": "default",
  "variables": [],
  "nonVisuals": [],
  "resources": []
}
```
