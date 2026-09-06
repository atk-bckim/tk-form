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

## Limits (schema/project-limits.json, loaded by `project_limits.py`)

| Limit | Value | Diagnostic code if exceeded |
|---|---|---|
| Total payload size | 8 MB | `project_payload_too_large` |
| Single image (decoded) | 5 MB | `image_upload_too_large` |
| Widgets count | 2000 | `project_widget_limit_exceeded` |
| Resources count | 200 | `project_resource_limit_exceeded` |
| Variables count | 500 | `project_variable_limit_exceeded` |
| Non-visuals count | 500 | `project_non_visual_limit_exceeded` |
| Nesting depth (widgets or menus) | 64 | `max_widget_nesting_depth_exceeded` / `max_menu_nesting_depth_exceeded` |
| Animations count | 500 | Designer-side limit (not enforced by the Python validator) |
| Animation duration / delay / repeat | 600,000 ms / 86,400,000 ms / 10,000 or `infinite` | `invalid_animation_duration` / `invalid_animation_delay` / `invalid_animation_repeat` |

## Diagnostic codes (grouped)

### Identity / naming
| Code | Severity | Meaning |
|---|---|---|
| `duplicate_widget_id` | error | Two widgets share an `id`. |
| `duplicate_widget_name` | error | Two widgets share a `name`. |
| `invalid_widget_name` | error | `name` is not a valid ASCII Python identifier (or is a keyword). |
| `invalid_variable_name` | error | A Tk variable's `name` is invalid. |
| `duplicate_variable_name` | error | Two Tk variables share a `name`. |
| `invalid_variable_type` | error | `varType` not in the four allowed types. |
| `invalid_component_name` | error | Non-visual component `name` is invalid. |
| `invalid_resource_name` | error | Resource `name` can't become a Python identifier. |
| `invalid_handler_name` | error | Handler `handlerName` is not a valid identifier. Unicode letters are allowed per PEP 3131 (NFKC-stable, non-keyword); widget/variable/animation/component names stay ASCII. |
| `invalid_animation_id` / `invalid_animation_name` | error | Animation `id` empty or `name` not a valid ASCII identifier. |
| `duplicate_animation_id` / `duplicate_animation_name` | error | Two animations share an `id` or `name`. |

### Toolkit (ttkbootstrap)
| Code | Severity | Meaning |
|---|---|---|
| `unsupported_toolkit` | error | `toolkit.name` is not `tkinter` or `ttkbootstrap`. |
| `unsupported_toolkit_major` | error | ttkbootstrap `majorVersion` missing or not 2 (3.x unsupported). |
| `unsupported_toolkit_widget` | error | A ttkbootstrap-only widget/component used under the tkinter toolkit. |
| `unsupported_toolkit_prop` | error | A `toolkitProps` key not allowed for this widget/toolkit. |
| `invalid_bootstyle_token` / `invalid_bootstyle_variant` | error/warning | `toolkitProps.ttkbootstrap.bootstyle` isn't a valid color/variant token (see ttkbootstrap.md). |
| `invalid_bootstrap_icon` / `invalid_icon_size` | error/warning | Unknown Bootstrap icon name, or `iconSize` outside 8–128. |

### Widget types & props
| Code | Severity | Meaning |
|---|---|---|
| `unsupported_widget_type` | error | `type` not in the 32 supported types (or a ttkbootstrap-only type under the tkinter toolkit). |
| `unsupported_widget_prop` | error | A prop key isn't allowed for this widget type (see widgets.md). |

### Parenting & layout
| Code | Severity | Meaning |
|---|---|---|
| `orphan_parent_reference` | error | `parentId` points at a non-existent widget. |
| `invalid_parent_container` | error | `parentId` points at a non-container type. |
| `parent_cycle` | error | A widget's parent chain loops back. |
| `max_widget_nesting_depth_exceeded` | error | Widget nesting > 64. |
| `mixed_layout_manager` | error | Siblings under one parent mix two different layout managers among `place`/`grid`/`pack` (except Toplevel/PanedWindow children — see layout.md). |

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

### Animations
| Code | Severity | Meaning |
|---|---|---|
| `missing_animation_target` | error | `targetWidgetId` references a non-existent widget. |
| `invalid_animation_notebook_tab` | error | Target is a synthetic Notebook tab frame. |
| `invalid_animation_preset` | error | Preset not in the seven supported values. |
| `invalid_animation_value_target` | error | `fill` target is not a `Progressbar`/`Floodgauge`. |
| `invalid_animation_trigger` / `invalid_animation_easing` | error | Trigger not in the 7; easing not in `linear`/`easeIn`/`easeOut`/`easeInOut`. |
| `invalid_animation_duration` / `invalid_animation_delay` / `invalid_animation_repeat` | error | Out of range (see Limits). |
| `invalid_animation_layout` | error | Spatial preset on a non-`place()` target (grid/pack/Toplevel/pane). |
| `invalid_animation_parameter` | error | Preset parameter out of range or wrong enum. |
| `invalid_animation_color` / `invalid_animation_color_target` | error | Bad `#hex`, or target doesn't support animated `bg`/`fg` (ttk themed widgets rejected). |
| `reserved_name_collision` / `animation_symbol_collision` | error | Animation name collides with reserved/generated symbols (e.g. an event handler). |

### ttkbootstrap providers & dialogs
| Code | Severity | Meaning |
|---|---|---|
| `invalid_dateentry_startdate` / `invalid_dateentry_weekday` / `invalid_dateentry_format` | error | `startdate` not ISO `YYYY-MM-DD`, `firstweekday` outside 0–6, empty `dateformat`. |
| `invalid_labeledscale_compound` / `invalid_scale_range` | error | `compound` not `top`/`bottom`; `from_` not less than `to`. |
| `invalid_meter_total` / `invalid_meter_used` / `invalid_meter_type` / `invalid_meter_size` / `invalid_meter_thickness` | error | `amounttotal` ≤ 0, `amountused` < 0, `metertype` not `full`/`semi`, `metersize`/`meterthickness` < 1. |
| `meter_used_exceeds_total` | warning | `amountused` exceeds `amounttotal`. |
| `invalid_floodgauge_maximum` / `invalid_floodgauge_mask` | error | Floodgauge `maximum`/`mask` invalid. |
| `invalid_tableview_columns` / `invalid_tableview_column_width` / `invalid_tableview_pagesize` | error | Tableview column/page settings invalid. |
| `invalid_scrolledtext_wrap` / `invalid_scrolledtext_bars` / `invalid_scrolledframe_padding` | error | ScrolledText/ScrolledFrame options invalid. |
| `invalid_ttkmessagebox_type` / `invalid_querybox_type` | error | `mbType`/`queryType` not in the allowed sets (see non-visuals.md). |

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
| `DateEntry`/`Meter`/etc. in a tkinter project | `unsupported_toolkit_widget` | Switch the project `toolkit` to ttkbootstrap (see ttkbootstrap.md). |
| `preset: "fill"` or `"grow"` animation | `invalid_animation_preset` | Use `slide`/`shake`/`bounce`/`pulse`/`color`. |
| `slide` animation on a grid/pack child | `invalid_animation_layout` | Lay the target out with `place`, or animate a different widget. |
| `color` animation on a ttkbootstrap Button | `invalid_animation_color_target` | Animate a classic Tk widget (Text/Canvas/Listbox) instead. |
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
