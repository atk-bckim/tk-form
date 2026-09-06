# Events & handlers

Events are how you attach Python code to user actions (clicks, key presses, etc.). They live under `events` on a widget, a menu item, or a non-visual component.

## The two accepted forms

Both forms are normalized to the same internal `EventHandler[]`. **Pick one form per `events` value** and use it consistently.

### Map form (terse, recommended for simple cases)

```jsonc
"events": {
  "command": "print('clicked')"
}
```

Value can be a string (inline code) or an object (with a named handler):

```jsonc
"events": {
  "command": { "handlerName": "on_save", "code": "print('saved')" },
  "<Leave>": { "handlerName": "on_hover_out", "code": "print('leave')" }
}
```

### Array form (explicit, recommended when you need ids / `enabled` toggles)

```jsonc
"events": [
  {
    "id": "event-save",
    "event": "command",
    "kind": "command",
    "handlerName": "on_save_settings",
    "code": "print(\"settings saved\")",
    "enabled": true
  },
  {
    "id": "event-leave",
    "event": "<Leave>",
    "kind": "bind",
    "handlerName": "save_button_leave",
    "code": "print(\"hover leave\")",
    "enabled": true
  }
]
```

Field reference (array form):
| Field | Required | Notes |
|---|---|---|
| `id` | no | Stable unique id. Auto-generated if missing. |
| `event` | yes | Event name — see table below. |
| `kind` | derived | `"command"` if `event` is `"command"`, else `"bind"`. You can omit it. |
| `handlerName` | no | Python method name. Must be a valid identifier and unique across ALL enabled handlers project-wide. If omitted, an anonymous handler is generated. |
| `code` | no (but recommended) | Python body. Must compile (`def h(event=None): <code>`). Empty code on an enabled handler = `empty_event_handler`. |
| `enabled` | no | Default `true`. Disabled handlers are skipped at codegen. |

## Event name conventions

| `event` value | `kind` (derived) | Meaning | Works on |
|---|---|---|---|
| `"command"` | command | The widget's primary action (Button click, Scale move, etc.) | Button, Checkbutton, Radiobutton, Scale, Spinbox, Listbox, OptionMenu, Combobox (via `<<ComboboxSelected>>`), Menu item, Timer |
| `"<Button-1>"` | bind | Left mouse click | any widget |
| `"<Button-3>"` | bind | Right mouse click | any widget |
| `"<Leave>"` / `"<Enter>"` | bind | Mouse exits / enters widget | any widget |
| `"<Key>"`, `"<Key-Return>"`, `"<Control-s>"` | bind | Keyboard | any focusable widget |
| `"<Double-Button-1>"` | bind | Double click | any widget (commonly Listbox/Treeview) |
| `"<Map>"` / `"<Unmap>"` | bind | Widget shown/hidden | any widget |

Full Tk bind syntax applies (e.g. `"<Control-Shift-s>"`, `"<KeyPress>"`).

## ⚠️ The big trap: `props.command` vs `events.command`

Two different things, both called "command":

| Location | What it accepts | When to use |
|---|---|---|
| **`props.command`** | A Python identifier reference (e.g. `"self.on_click"`, `"on_click"`). **Cannot be inline code.** | Rarely — only when wiring to an externally defined function. |
| **`events.command`** | Inline Python code (e.g. `"print('x')"`) OR a `{handlerName, code}` object. | The normal way to attach behavior. |

```jsonc
// ❌ WRONG — invalid_command_reference error
{ "type": "Button", "props": { "command": "print('clicked')" } }

// ✅ RIGHT — inline code via events
{ "type": "Button", "props": { "text": "OK" }, "events": { "command": "print('clicked')" } }

// ✅ ALSO RIGHT — identifier reference via props (rare; pairs with events elsewhere)
{ "type": "Button", "props": { "command": "self.on_click" } }
```

If a widget has **both** `props.command` and an enabled `events.command`, the events one wins and a `command_event_overrides_prop` warning is emitted. Just use `events.command`.

## Handler-name uniqueness

`handlerName` must be unique **across the entire project** (all widgets, menu items, non-visuals) among enabled handlers. Two handlers with the same name → `duplicate_handler_name` error.

If you don't need a stable method name, omit `handlerName` and let codegen produce an anonymous handler.

## Code can reference widgets and Tk variables by bare name

Inside `code`, **both widgets and Tk variables are in scope as plain Python names** (no `self.` prefix needed). The codegen guarantees this in every export mode:

- **Function export**: widgets and variables are local variables in `create_window()`, and your handler is a nested function that closes over them.
- **Class export**: the handler is a method, but the codegen prepends alias lines (`send_entry = self.send_entry`, `filter_var = self.filter_var`, ...) at the top of the method body, so the rest of your code can use bare names too.

So you can reference any widget by its `name`, and any declared Tk variable by its `name`, directly:

```jsonc
"events": {
  "command": {
    "handlerName": "on_send",
    "code": "print('send', send_entry.get()); log_text.delete('1.0', 'end')"
  }
}
```

Here `send_entry` / `log_text` are widget `name`s, and `filter_var` (if used) would be a Tk variable `name`. All three work as bare Python identifiers.

Caveat: the validator only `compile()`s the handler body — it cannot verify that a bare name actually exists. A typo like `send_entri.get()` will pass validation and only fail at runtime. So match names exactly against `widgets[].name` and `variables[].name`.

## Validation of code

Every enabled handler's `code` is compiled with `def <handlerName>(event=None): <body>` (`project_validation.py:447-462`). Syntax errors → `invalid_handler_code`. The handler always receives an `event` argument (which is `None` for `"command"` handlers).

## Non-visual events

Timer / FileDialog / ColorChooser / MessageBox accept the same `events` shape. See non-visuals.md.
