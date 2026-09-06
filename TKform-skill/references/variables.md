# Tk variables

Tk variables (`StringVar`, `IntVar`, `DoubleVar`, `BooleanVar`) are how Tkinter keeps widget state observable. Declare them in `variables[]` and reference them by `name` from widget props or event code.

## Shape

```jsonc
"variables": [
  { "id": "var-username", "name": "username_var", "varType": "StringVar", "defaultValue": "admin" },
  { "id": "var-notifications", "name": "notifications_var", "varType": "BooleanVar", "defaultValue": "1" },
  { "id": "var-volume", "name": "volume_var", "varType": "IntVar", "defaultValue": "50" },
  { "id": "var-price", "name": "price_var", "varType": "DoubleVar", "defaultValue": "9.99" }
]
```

| Field | Required | Notes |
|---|---|---|
| `id` | yes | Stable unique id. |
| `name` | yes | Python identifier. Must be unique across `variables[]` (`duplicate_variable_name`). Referenced verbatim from widget props. |
| `varType` | yes | One of `StringVar`, `IntVar`, `DoubleVar`, `BooleanVar`. |
| `defaultValue` | no | String; engine casts to the type. For `BooleanVar` use `"1"`/`"0"` or `"True"`/`"False"`. Defaults to `""`. |

## Referencing from widgets

Two prop keys are tracked as variable references (`widget_spec.py:REFERENCE_PROPS`):

| Prop | Used by | Effect |
|---|---|---|
| `textvariable` | Entry, Spinbox, OptionMenu | Two-way bind: typing in the widget updates the variable and vice versa. (**Not** Text — see below.) |
| `variable` | Checkbutton, Radiobutton, Scale, Listbox | Two-way bind of the value/selection. |

### Example (settings panel pattern)

```jsonc
"variables": [
  { "id": "var-username", "name": "username_var", "varType": "StringVar", "defaultValue": "admin" },
  { "id": "var-notifications", "name": "notifications_var", "varType": "BooleanVar", "defaultValue": "1" }
],
"widgets": [
  { "id": "entry-user", "type": "Entry", "name": "username_entry", "parentId": "frame-main",
    "props": { "textvariable": "username_var" } },
  { "id": "check-notifications", "type": "Checkbutton", "name": "notifications_check", "parentId": "frame-main",
    "props": { "text": "Enable notifications", "variable": "notifications_var" } }
]
```

## ⚠️ Reference integrity rule

If `widget.props.variable` or `widget.props.textvariable` names a variable NOT declared in `variables[]`, the engine emits `missing_variable_reference`. Always declare the variable before/alongside referencing it.

For **Checkbutton**/**Radiobutton**, `variable` should point to the same Tk variable across the radio group (multiple Radiobuttons sharing a `StringVar`/`IntVar` give the mutual-exclusion behavior).

## ⚠️ Text widget cannot use variables

`Text` is listed in `REFERENCE_PROPS` consumers in some Tk tutorials, but the tkform engine explicitly forbids it (`widget_spec.py:179-181`):

```jsonc
// ❌ WRONG — Text cannot use textvariable
{ "type": "Text", "props": { "textvariable": "my_var" } }
```

Use `initialText` for the starting content of a Text widget, and read/write its content via `.get("1.0", "end-1c")` / `.delete()` / `.insert()` in event handlers.

## Reading/writing in event code

Inside `events.code`, variables are in scope as **bare Python names** (the codegen handles the `self.` prefix for you in class export, or makes them locals in function export — see events.md for the full reference convention that also covers widgets):

```jsonc
"events": {
  "command": {
    "handlerName": "on_refresh",
    "code": "value = filter_var.get(); print('refresh', value); filter_var.set('')"
  }
}
```

(The engine generates the variable as `self.filter_var = StringVar(...)` in class export or a local in function export, then aliases it as a bare name at the top of each handler — so `filter_var.get()` / `.set(x)` works directly without a `self.` prefix. See events.md for the full story.)

## Menu radiobutton variables

Menu items of `kind: "radiobutton"` also reference a Tk variable via `variable` + `value` — the variable MUST be declared here too. See menus.md.
