# Non-visual components

Components without a visible widget on the canvas. Declared under `nonVisuals[]`. Twelve types: the classics **Timer, FileDialog, ColorChooser, MessageBox, BackgroundWorker, ThreadPool**, plus six ttkbootstrap-only dialogs **TtkMessagebox, Querybox, DatePickerDialog, ColorPickerDialog, ToastNotification, ToolTip** (the latter require `toolkit.name: "ttkbootstrap"`; see ttkbootstrap.md).

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
| `type` | yes | One of the twelve types below (`unsupported_widget_type` under the wrong toolkit for ttkbootstrap-only ones). |
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

### BackgroundWorker

Runs an event handler on a daemon background thread so the UI stays responsive, then
delivers the result to a UI-thread `completed` handler through an `after()` marshal loop.

```jsonc
{ "id": "worker-fetch", "type": "BackgroundWorker", "name": "fetch_worker",
  "events": {
    "doWork": { "handlerName": "fetch_data", "code": "value = int(fetch_entry.get()) * 2; return value" },
    "completed": { "handlerName": "on_fetch_done", "code": "print(result)" }
  } }
```

| Event | Handler signature | Notes |
|---|---|---|
| `doWork` | `def <name>()` | Runs on the background thread. `return` a value to hand it to `completed`. |
| `completed` | `def <name>(result)` | Runs on the UI thread. `result` is `{ok, value, error}` — check `result["ok"]` before using `result["value"]`. |

The component `name` also exposes helpers in event code: `run()`, `cancel()`, `cancelled()`, and `is_running()` for cooperative cancellation.

## ThreadPool

Runs handlers on a `concurrent.futures.ThreadPoolExecutor`.

```jsonc
{ "id": "pool-tasks", "type": "ThreadPool", "name": "task_pool",
  "props": { "maxWorkers": 4 },
  "events": {
    "taskCompleted": { "handlerName": "on_task_done", "code": "print(result)" }
  } }
```

| Item | Notes |
|---|---|
| `maxWorkers` prop | 1–64, default 4 (`invalid_pool_max_workers` outside the range). |
| `taskCompleted` event | `def <name>(result)` on the UI thread; `result` is `{ok, value, error}`. |
| Helpers | `submit(fn, *args)` to queue work and `shutdown()` from event code via the component `name`. |

# Common usage pattern

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


## BackgroundWorker

Runs event-handler code in a daemon background thread and delivers the outcome back to the UI thread through an `after()` poll loop. **Threads only** — Tkinter UIs must never be touched from the worker; mutate UI only inside `completed`.

| Aspect | Value |
|---|---|
| Events | `doWork` (label "Do Work (background)", no params — runs in the thread), `completed` (label "Completed", `result` param — runs on the UI thread) |
| `result` payload | Dict `{"ok": bool, "value": <doWork return value>, "error": <exception or None>}` |
| Methods | `worker_run()`, `worker_cancel()`, `worker_cancelled()`, `worker_is_running()` |
| Notes | Worker thread is a daemon; calling `run()` while already running raises `RuntimeError`; Cancellation is cooperative — poll `worker_cancelled()` inside `doWork`. |

## ThreadPool

Runs callables on a `concurrent.futures.ThreadPoolExecutor` and delivers each result to the UI thread.

| Aspect | Value |
|---|---|
| Props | `maxWorkers` (integer 1–64, default 4) |
| Events | `taskCompleted` (label "Task Completed", `result` param — same `{ok, value, error}` payload dict as BackgroundWorker; results of all submitted tasks arrive here) |
| Methods | `pool_submit(task)`, `pool_shutdown()` (`shutdown(wait=False)`), plus the raw `pool` executor attribute for advanced use |
| Notes | Best for I/O-bound work; CPU-bound tasks do not parallelize due to the GIL. The completion poll starts on the first `submit()` and runs for the app's lifetime. |

```jsonc
// run work without freezing the UI
{"id": "bw-1", "type": "BackgroundWorker", "name": "report_worker", "events": [
  {"event": "doWork", "handlerName": "fetch_report", "code": "data = load_slow_report()\nreturn data"},
  {"event": "completed", "handlerName": "on_report", "code": "status_label.config(text='loaded')}
]}
```
