# Non-visual components

Components without a visible widget on the canvas. Declared under `nonVisuals[]`. Ten types: the four classics **Timer, FileDialog, ColorChooser, MessageBox**, plus six ttkbootstrap-only dialogs **TtkMessagebox, Querybox, DatePickerDialog, ColorPickerDialog, ToastNotification, ToolTip** (require `toolkit.name: "ttkbootstrap"`; see ttkbootstrap.md).

## Shape

```jsonc
"nonVisuals": [
  {
    "id": "timer-poll",
    "type": "Timer",
    "name": "poll_timer",
    "props": { "interval": 1000 },
    "events": { "command": { "handlerName": "on_tick", "code": "print('tick')" } }
  }
]
```

| Field | Required | Notes |
|---|---|---|
| `id` | yes | Stable unique id (`duplicate_component_id` if repeated). |
| `type` | yes | One of the ten types above (`unsupported_widget_type` under the wrong toolkit for ttkbootstrap-only ones). |
| `name` | yes | ASCII Python identifier; becomes `self.<name>`. Must be unique across non-visuals (`invalid_component_name` if not a valid identifier). |
| `props` | no | Type-specific config (see below). |
| `events` | no | Same shape as widget events (see events.md). |

## Timer

Periodic callback.

```jsonc
{
  "id": "timer-poll",
  "type": "Timer",
  "name": "poll_timer",
  "props": { "interval": 1000 },
  "events": { "command": { "handlerName": "on_poll", "code": "print('polling')" } }
}
```

| Prop | Type | Notes |
|---|---|---|
| `interval` | number | Milliseconds between ticks. Required for the timer to do anything useful. |

The `events.command` fires on each tick. In generated code, the timer is started automatically when the UI is built (or controlled from event code via `self.poll_timer.start()` / `.stop()` — exact API matches the generated class).

## FileDialog

File picker. Triggered from event code (not auto-shown).

```jsonc
{
  "id": "fd-open",
  "type": "FileDialog",
  "name": "open_dialog",
  "props": {
    "mode": "open",
    "title": "Open File",
    "filetypes": "[('Text files', '*.txt'), ('All files', '*.*')]"
  }
}
```

| Prop | Type | Notes |
|---|---|---|
| `mode` | `"open"` \| `"save"` \| `"directory"` | Which dialog to show. |
| `title` | string | Window title. |
| `filetypes` | **string** | ⚠️ Special parsing — see below. |
| `initialdir` | string | Starting directory. |
| `initialfile` | string | Default filename (save mode). |

### ⚠️ `filetypes` parsing rule

`filetypes` is passed as a **JSON string**, but its content must parse as a Python literal list of string pairs:

```jsonc
// ✅ RIGHT
"filetypes": "[('Text files', '*.txt'), ('All files', '*.*')]"

// ❌ WRONG — invalid_filedialog_filetypes error
"filetypes": "Text files|*.txt"
```

The engine uses `ast.literal_eval` (via `safe_literals.parse_filedialog_filetypes`), so the value must be a syntactically valid Python list of 2-tuples of strings. Empty string means "no filter".

## ColorChooser

Color picker.

```jsonc
{
  "id": "cc-fg",
  "type": "ColorChooser",
  "name": "fg_color_dialog",
  "props": { "title": "Pick foreground color", "initialcolor": "#000000" }
}
```

| Prop | Type | Notes |
|---|---|---|
| `title` | string | Window title. |
| `initialcolor` | string | Initial color (e.g. `"#ff0000"` or `"red"`). |

Invoked from event code.

## MessageBox

Modal alert / confirmation.

```jsonc
{
  "id": "mb-confirm-delete",
  "type": "MessageBox",
  "name": "confirm_delete_box",
  "props": {
    "kind": "askyesno",
    "title": "Confirm delete",
    "message": "Delete this item?",
    "icon": "warning"
  }
}
```

| Prop | Type | Notes |
|---|---|---|
| `kind` | string | One of `showinfo`, `showwarning`, `showerror`, `askquestion`, `askokcancel`, `askyesno`, `askyesnocancel`, `askretrycancel`. |
| `title` | string | Window title. |
| `message` | string | Body text. |
| `icon` | string | One of `info`, `warning`, `error`, `question`. |
| `default` | string | Which button is default (`yes`, `no`, `ok`, `cancel`, `retry`, `abort`, `ignore`). |
| `parent` | string | Widget id to parent the dialog to (optional). |

For `ask*` kinds, the return value flows back into the calling code (e.g. `if confirm_delete_box.show(): ...` — exact API matches the generated class).

## ttkbootstrap-only dialogs

These six types require `toolkit.name: "ttkbootstrap"` (majorVersion 2). See `examples/ttkbootstrap-dialogs.tkform.json` for a working set.

### TtkMessagebox

```jsonc
{ "id": "mb-overwrite", "type": "TtkMessagebox", "name": "overwrite_box",
  "props": { "mbType": "yesno", "title": "Confirm", "message": "Overwrite the file?", "alert": false } }
```

| Prop | Type | Notes |
|---|---|---|
| `mbType` | one of `info`, `warning`, `error`, `question`, `ok`, `okcancel`, `yesno`, `yesnocancel`, `retrycancel` | Dialog shape (`invalid_ttkmessagebox_type` otherwise). Default `info`. |
| `title` | string | Window title. |
| `message` | string | Body text. |
| `alert` | boolean | Plays an alert bell. |
| `variable` | string | Optional declared **StringVar** that receives the chosen button value. |

### Querybox

Asks the user for a value.

```jsonc
{ "id": "qb-name", "type": "Querybox", "name": "name_query",
  "props": { "queryType": "string", "title": "Query", "prompt": "Name", "variable": "name_var" } }
```

| Prop | Type | Notes |
|---|---|---|
| `queryType` | one of `string`, `integer`, `float`, `date` | Input kind (`invalid_querybox_type` otherwise). Default `string`. |
| `title`, `prompt` | string | Dialog texts. |
| `initialvalue` / `minvalue` / `maxvalue` | number | Only for `integer`/`float` (parsed per type). |
| `variable` | string | Optional declared Tk variable that receives the result — `StringVar` for `string`/`date`, `IntVar` for `integer`, `DoubleVar` for `float` (`missing_variable_reference` if undeclared, type mismatch is diagnosed too). |

### DatePickerDialog

```jsonc
{ "id": "dp-day", "type": "DatePickerDialog", "name": "day_picker",
  "props": { "title": "Day", "firstweekday": 6, "startdate": "", "variable": "chosen_day_var" } }
```

| Prop | Type | Notes |
|---|---|---|
| `title` | string | Window title. |
| `firstweekday` | number 0–6 | First day of week. Default 6 (Sunday). |
| `startdate` | string | ISO `YYYY-MM-DD` initial date (empty = today). |
| `variable` | string | Optional declared **StringVar** receiving the picked date. |

### ColorPickerDialog

```jsonc
{ "id": "cp-color", "type": "ColorPickerDialog", "name": "color_picker",
  "props": { "title": "Color", "initialcolor": "#0d6efd", "variable": "picked_color_var" } }
```

| Prop | Type | Notes |
|---|---|---|
| `title` | string | Window title. |
| `initialcolor` | string | `#RGB`/`#RRGGBB` hex color. |
| `variable` | string | Optional declared **StringVar** receiving the chosen hex color. |

### ToastNotification

Timed notification at the window edge.

```jsonc
{ "id": "toast-saved", "type": "ToastNotification", "name": "saved_toast",
  "props": { "title": "Saved", "message": "Record stored.", "duration": 3000, "bootstyle": "success", "position": "se" } }
```

| Prop | Type | Notes |
|---|---|---|
| `title`, `message` | string | Toast texts. |
| `duration` | number | Milliseconds before it closes. Default 3000. |
| `bootstyle` | string | Catalog color token (e.g. `success`). Default `info`. |
| `position` | one of `ne`, `nw`, `se`, `sw` | Screen corner. Default `se`. |

### ToolTip

Attaches a tooltip to a widget.

```jsonc
{ "id": "tip-save", "type": "ToolTip", "name": "save_tooltip",
  "props": { "targetWidgetId": "btn-save", "text": "Save the form", "bootstyle": "info", "wraplength": 300 } }
```

| Prop | Type | Notes |
|---|---|---|
| `targetWidgetId` | string | Id of the widget the tooltip attaches to (must exist). |
| `text` | string | Tooltip content. |
| `bootstyle` | string | Catalog color token (non-catalog tokens get a warning). Default `info`. |
| `wraplength` | number | Wrap width in pixels. |

## Result variables (dialog → Tk variable)

`TtkMessagebox`, `Querybox`, `DatePickerDialog`, and `ColorPickerDialog` accept a `variable` prop naming a **declared** Tk variable; the generated code writes the dialog result into it. The variable's `varType` must match the result type (`StringVar` for messagebox/datepicker/colorpicker, and per-`queryType` for Querybox). An undeclared variable → `missing_variable_reference`.

## Common usage pattern

Non-visuals are usually invoked from a Button's event handler:

```jsonc
{
  "id": "button-open",
  "type": "Button",
  "name": "open_button",
  "props": { "text": "Open..." },
  "events": {
    "command": { "handlerName": "on_open", "code": "path = open_dialog.show(); print('chose', path)" }
  }
}
```

So a typical pattern is: declare the non-visual once in `nonVisuals[]`, reference it by `name` from event code elsewhere.
