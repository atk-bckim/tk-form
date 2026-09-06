# Non-visual components

Components without a visible widget on the canvas. Declared under `nonVisuals[]`. Four types: **Timer, FileDialog, ColorChooser, MessageBox**.

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
| `id` | yes | Stable unique id. |
| `type` | yes | One of `Timer`, `FileDialog`, `ColorChooser`, `MessageBox`. |
| `name` | yes | Python identifier; becomes `self.<name>`. Must be unique across non-visuals (`invalid_component_name` if not a valid identifier). |
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
