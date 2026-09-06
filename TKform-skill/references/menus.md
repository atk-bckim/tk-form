# Menus

Top-level menu bar attached to the root window. Lives under `menuBar` (null if no menu bar).

## Shape

```jsonc
"menuBar": {
  "menus": [
    {
      "id": "menu-file",
      "label": "File",
      "items": [
        {
          "id": "item-refresh",
          "kind": "command",
          "label": "Refresh",
          "accelerator": "Ctrl+R",
          "acceleratorBinding": "<Control-r>",
          "events": {
            "command": { "handlerName": "on_menu_refresh", "code": "print('menu refresh')" }
          }
        },
        { "id": "item-sep1", "kind": "separator" },
        {
          "id": "item-exit",
          "kind": "command",
          "label": "Exit",
          "events": { "command": { "handlerName": "on_exit", "code": "root.destroy()" } }
        }
      ]
    },
    {
      "id": "menu-view",
      "label": "View",
      "items": [
        {
          "id": "item-theme-light",
          "kind": "radiobutton",
          "label": "Light",
          "variable": "theme_var",
          "value": "light"
        },
        {
          "id": "item-theme-dark",
          "kind": "radiobutton",
          "label": "Dark",
          "variable": "theme_var",
          "value": "dark"
        },
        { "id": "item-toolbar", "kind": "checkbutton", "label": "Show toolbar", "variable": "toolbar_var" }
      ]
    },
    {
      "id": "menu-recent",
      "label": "Recent",
      "items": [
        {
          "id": "item-recent",
          "kind": "cascade",
          "label": "Open Recent",
          "children": [
            { "id": "item-file1", "kind": "command", "label": "readme.md", "events": { "command": "print('open')" } }
          ]
        }
      ]
    }
  ]
}
```

## Structure

`menuBar.menus[]` → top-level menus (left to right on the bar).
`menu.items[]` → items in display order.
`menuItem.children[]` → submenu (only meaningful for `kind: "cascade"`).

## Item kinds

| `kind` | Behavior | Required fields |
|---|---|---|
| `command` | Clickable item that fires `events.command` | `label`, `events.command` (or external `acceleratorBinding`) |
| `separator` | Horizontal rule (no label, no action) | (none) — `separator: true` is shorthand |
| `checkbutton` | Toggle with checkmark; binds to a Tk `BooleanVar` | `label`, `variable` (must be declared) |
| `radiobutton` | Mutually-exclusive choice; binds to a shared Tk variable | `label`, `variable` (declared), `value` |
| `cascade` | Submenu parent | `label`, `children[]` (non-empty) |

## Fields

| Field | Applies to | Notes |
|---|---|---|
| `id` | all | Stable unique id. |
| `label` | non-separator | Display text. |
| `kind` | all | One of the five above. Default `command`. |
| `separator` | all | `true` forces `kind: "separator"`. |
| `accelerator` | command/check/radio/cascade | Display-only hint (e.g. `"Ctrl+R"`). |
| `acceleratorBinding` | command/check/radio/cascade | The actual Tk bind sequence (e.g. `"<Control-r>"`) bound on root, so the shortcut works even without opening the menu. |
| `variable` | checkbutton, radiobutton | Tk variable name. Must be declared in `variables[]` (`missing_menu_variable_reference` if not). |
| `value` | radiobutton | The value this choice assigns to `variable`. |
| `events` | command | Handler for `command` event (see events.md). |
| `children` | cascade | Recursive `MenuItemData[]`. Subject to `MAX_NESTING_DEPTH` (64) and cycle detection. |

## Variable references

For `radiobutton` and `checkbutton` items, `variable` must:
1. Be a valid Python identifier.
2. Be declared in `variables[]` at the project level.

Radiobuttons that should be mutually exclusive must share the same `variable` (and have distinct `value`s).

## Validation

- `menu_item_cycle` — `children` chain that loops back on itself.
- `max_menu_nesting_depth_exceeded` — submenu nesting > 64.
- `missing_menu_variable_reference` — `variable` not declared.
- `invalid_menu_variable_reference` — `variable` not a valid identifier.

## acceleratorBinding note

`acceleratorBinding` is bound on the **root window** with `root.bind("<Control-r>", ...)`. The handler is the same one attached to the menu item's `events.command`. If you set `acceleratorBinding` but no `events.command`, the binding will do nothing.

## Minimal example (File menu with one command)

```jsonc
"menuBar": {
  "menus": [
    {
      "id": "menu-file",
      "label": "File",
      "items": [
        {
          "id": "item-open",
          "kind": "command",
          "label": "Open",
          "events": { "command": "print('open')" }
        }
      ]
    }
  ]
}
```
