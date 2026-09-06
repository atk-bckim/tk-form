# Validation

The engine validator (`python/tkform_engine/project_validation.py`) is the single source of truth for what is a valid tkform project. **Always run it after authoring** — the bundled JSON Schema (`references/tkform.schema.json`, same content as the extension's `schema/tkform.schema.json`) only checks structural shape; cross-references, code compilation, and the rules below need the engine.

## How to validate

```bash
python .agents/skills/tkform-author/scripts/validate_project.py path/to/project.tkform.json
# or via stdin:
python .agents/skills/tkform-author/scripts/validate_project.py - < path/to/project.tkform.json
```

When this skill is installed outside the tkform repo, pass the engine location or set it in the environment:

```bash
python path/to/tkform-author/scripts/validate_project.py --engine-root /path/to/tkform/python path/to/project.tkform.json
TKFORM_ENGINE_ROOT=/path/to/tkform/python python path/to/tkform-author/scripts/validate_project.py path/to/project.tkform.json
```

Python executable resolution order is `--python`, `TKFORM_ENGINE_PYTHON`, workspace `tkform.enginePythonPath`, workspace `tkform.pythonPath`, then `python3`/`python`. Engine root resolution order is `--engine-root`, `TKFORM_ENGINE_ROOT`, then nearest `python/tkform_engine` or `tkform_engine` directory from the project path/current directory.

Exit code 0 = no errors, 1 = at least one error-severity diagnostic. Output is one line per diagnostic:

```
error · missing_variable_reference · widgets[3].props.textvariable · Widget 'username_entry' references missing Tk variable 'username_var'. (widget: username_entry)
warning · invalid_default_value · widgets[1].props.value · Widget 'theme_combo' default value 'Dark' is not in its option list.
```

The script uses the same engine the VS Code extension uses, so what you see here matches what the user sees in the designer's Problems panel.

## Limits (project_limits.py)

| Limit | Value | Diagnostic code if exceeded |
|---|---|---|
| Total payload size | 8 MB | `project_payload_too_large` |
| Single image (decoded) | 5 MB | `image_upload_too_large` |
| Widgets count | 2000 | `project_widget_limit_exceeded` |
| Resources count | 200 | `project_resource_limit_exceeded` |
| Variables count | 500 | `project_variable_limit_exceeded` |
| Non-visuals count | 500 | `project_non_visual_limit_exceeded` |
| Nesting depth (widgets or menus) | 64 | `max_widget_nesting_depth_exceeded` / `max_menu_nesting_depth_exceeded` |

## Diagnostic codes (grouped)

### Identity / naming
| Code | Severity | Meaning |
|---|---|---|
| `duplicate_widget_id` | error | Two widgets share an `id`. |
| `duplicate_widget_name` | error | Two widgets share a `name`. |
| `invalid_widget_name` | error | `name` is not a valid Python identifier (or is a keyword). |
| `invalid_variable_name` | error | A Tk variable's `name` is invalid. |
| `duplicate_variable_name` | error | Two Tk variables share a `name`. |
| `invalid_variable_type` | error | `varType` not in the four allowed types. |
| `invalid_component_name` | error | Non-visual component `name` is invalid. |
| `invalid_resource_name` | error | Resource `name` can't become a Python identifier. |
| `invalid_handler_name` | error | Handler `handlerName` is not a valid identifier. |

### Widget types & props
| Code | Severity | Meaning |
|---|---|---|
| `unsupported_widget_type` | error | `type` not in the 25 supported types. |
| `unsupported_widget_prop` | error | A prop key isn't allowed for this widget type (see widgets.md). |

### Parenting & layout
| Code | Severity | Meaning |
|---|---|---|
| `orphan_parent_reference` | error | `parentId` points at a non-existent widget. |
| `invalid_parent_container` | error | `parentId` points at a non-container type. |
| `parent_cycle` | error | A widget's parent chain loops back. |
| `max_widget_nesting_depth_exceeded` | error | Widget nesting > 64. |
| `mixed_layout_manager` | error | Siblings under one parent mix `place` and `grid` (except Toplevel/PanedWindow children — see layout.md). |

### Variables & references
| Code | Severity | Meaning |
|---|---|---|
| `missing_variable_reference` | error | `props.variable` / `props.textvariable` names an undeclared variable. |
| `missing_menu_variable_reference` | error | Menu radiobutton/checkbutton `variable` is undeclared. |
| `invalid_menu_variable_reference` | error | Menu variable name isn't a valid identifier. |

### Bindings / scroll
| Code | Severity | Meaning |
|---|---|---|
| `missing_scrollbar_binding_target` | error | `bindings.command` references a non-existent widget. |
| `invalid_scrollbar_binding_target` | error | Scrollbar targets a non-scrollable widget. |
| `invalid_scrollbar_entry_orientation` | error | Scrollbar on Entry must be `orient: "horizontal"`. |

### Code / command
| Code | Severity | Meaning |
|---|---|---|
| `invalid_command_reference` | error | `props.command` is not a Python identifier reference. **Use `events.command` for inline code.** |
| `invalid_handler_code` | error | Handler `code` failed Python `compile()`. |
| `empty_event_handler` | error | An enabled handler has empty `code`. |
| `duplicate_handler_name` | error | Same `handlerName` used by multiple enabled handlers. |
| `command_event_overrides_prop` | warning | Widget has both `props.command` and an enabled `events.command` — events wins. |

### Menus
| Code | Severity | Meaning |
|---|---|---|
| `menu_item_cycle` | error | Menu `children` chain loops. |
| `max_menu_nesting_depth_exceeded` | error | Menu nesting > 64. |

### Data widgets
| Code | Severity | Meaning |
|---|---|---|
| `invalid_default_value` | warning | Combobox/OptionMenu `value` is not in `values`. |
| `empty_listbox_item` | warning | A Listbox `items` entry is empty. |
| `empty_treeview_row` | warning | A Treeview row has no values. |
| `treeview_row_column_mismatch` | warning | Treeview row `values` length ≠ `columns` length. |

### Resources / non-visuals
| Code | Severity | Meaning |
|---|---|---|
| `missing_image_resource` | error | `props.image` references an undeclared resource. |
| `invalid_image_data` | error | `dataUrl` is not valid base64. |
| `image_upload_too_large` | error | Decoded image > 5 MB. |
| `invalid_filedialog_filetypes` | error | FileDialog `filetypes` isn't a Python-literal list of 2-tuples (see non-visuals.md). |

## Common authoring mistakes → fix

| Mistake | Diagnostic | Fix |
|---|---|---|
| Inline code in `props.command` | `invalid_command_reference` | Move to `events.command`. |
| ttk widget with `bg`/`fg` | (silently dropped or `unsupported_widget_prop`) | Remove the prop; ttk is themed, not colored. |
| `textvariable` on a Text widget | `unsupported_widget_prop` | Use `initialText` instead. |
| Vertical Scrollbar on Entry | `invalid_scrollbar_entry_orientation` | Set `orient: "horizontal"`. |
| Reference a Tk variable without declaring it | `missing_variable_reference` | Add it to `variables[]`. |
| Two buttons with `handlerName: "on_click"` | `duplicate_handler_name` | Rename one or omit `handlerName`. |
| Same `id` on two widgets | `duplicate_widget_id` | Make ids unique. |
| `parentId` pointing at a Button | `invalid_parent_container` | Use a Frame/LabelFrame/etc. |

## What the JSON Schema catches vs the engine

The bundled `references/tkform.schema.json` file gives editor autocomplete/schema context and basic shape checks. It mirrors the extension's `schema/tkform.schema.json`, which VS Code registers through `package.json` jsonValidation. It does **not** replace engine validation:

| Check | Schema | Engine |
|---|---|---|
| Field types, required fields, enums | ✅ | ✅ |
| Identifier regex | ✅ | ✅ |
| Per-widget-type prop allow-lists | ❌ | ✅ |
| Cross-references (variables/parents/images) | ❌ | ✅ |
| Duplicate id/name within arrays | ❌ | ✅ |
| Python code compilation | ❌ | ✅ |
| Layout mixing exceptions | ❌ | ✅ |

So: **always run the engine validator before declaring a file done.**
