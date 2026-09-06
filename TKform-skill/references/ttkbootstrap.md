# ttkbootstrap projects

A tkform project declares its UI toolkit in the top-level `toolkit` object. The default is standard Tkinter; `ttkbootstrap` (majorVersion 2) unlocks themed widgets, per-widget bootstyles, seven provider widgets, and six modern dialog components.

- Schema v4 expects `toolkit` on every project. Omitted legacy projects normalize to `tkinter`.
- The legacy `tkTheme` root field is superseded by `toolkit.theme` (old files migrate on save).

## The toolkit block

```jsonc
// tkinter (default)
"toolkit": { "name": "tkinter", "theme": "default" }        // themes: default, clam, alt, classic

// ttkbootstrap
"toolkit": { "name": "ttkbootstrap", "majorVersion": 2, "theme": "bootstrap-light" }
```

`majorVersion` is **required** and must be `2` — ttkbootstrap 3.x is unsupported (`unsupported_toolkit_major`). Unknown toolkit names fail with `unsupported_toolkit`.

ttkbootstrap themes (30): `bootstrap-light`, `bootstrap-dark`, `pydata-light`, `pydata-dark`, `nord-light`, `nord-dark`, `solarized-light`, `solarized-dark`, `catppuccin-light`, `catppuccin-dark`, `gruvbox-light`, `gruvbox-dark`, `dracula-light`, `dracula-dark`, `tokyo-night-light`, `tokyo-night-dark`, `one-light`, `one-dark`, `everforest-light`, `everforest-dark`, `vapor-light`, `vapor-dark`, `minty-light`, `minty-dark`, `pulse-light`, `pulse-dark`, `united-light`, `united-dark`, `sandstone-light`, `sandstone-dark`. Default: `bootstrap-light`.

## Runtime requirements

- Previewing/running ttkbootstrap output needs **Python 3.10+** (the generated code targets 3.10) and the `ttkbootstrap>=2,<3` package installed in the preview runtime. Plain tkinter projects only need Python 3.9+.
- Structural validation (the bundled validator script) does **not** require the package — you can author and validate without installing ttkbootstrap.

## What changes under ttkbootstrap

- **Provider widgets** become available: `DateEntry`, `LabeledScale`, `Meter`, `Floodgauge`, `Tableview`, `ScrolledText`, `ScrolledFrame` (see widgets.md, 🟧 rows). Using them under the tkinter toolkit fails validation.
- **Six more non-visual components** become available: `TtkMessagebox`, `Querybox`, `DatePickerDialog`, `ColorPickerDialog`, `ToastNotification`, `ToolTip` (see non-visuals.md).
- **Per-widget `toolkitProps`** unlock: `bootstyle`, and for some widgets `icon`, `iconSize` (8–128), `iconOnly`.
- **Backend-following props**: under ttkbootstrap, classic tk widgets (Text, Canvas, Listbox, PanedWindow, Message) keep their tk style props (`bg`, `fg`, `font`, …) because the generated code instantiates the classic classes. ttk widgets follow ttk rules (no bg/fg).

## toolkitProps

Both provider bags may be present on one widget; only the active toolkit's is used (the other is preserved for round-trips):

```jsonc
{
  "id": "meter-usage", "type": "Meter", "name": "usage_meter", "parentId": null,
  "x": 24, "y": 84, "width": 200, "height": 200,
  "props": { "amountused": 65, "amounttotal": 100, "metersize": 200, "meterthickness": 10, "metertype": "full", "showtext": true, "interactive": false },
  "toolkitProps": { "tkinter": {}, "ttkbootstrap": { "bootstyle": "success" } }
}
```

### bootstyle grammar

`bootstyle` combines a color (and optionally a variant/surface) into one string, e.g. `"success"`, `"outline"`, `"info-round"`:

- **Colors**: `primary`, `secondary`, `success`, `info`, `warning`, `danger`, `light`, `dark`, `neutral`.
- **Surfaces** (with `@` prefix): `@chrome`, `@card`, `@primary`, `@secondary`, `@success`, `@info`, `@warning`, `@danger`, `@light`, `@dark`.
- **Per-widget variants**: Button `outline`/`link`/`ghost`; Menubutton `outline`/`ghost`; Checkbutton `round`/`square`; Progressbar `striped`/`thin`; Scrollbar `round`/`thin`. Checkbutton also accepts base types `toggle`/`toolbutton`; Button accepts base type `toolbutton`.

Invalid tokens fail validation: `invalid_bootstyle_token`, `invalid_bootstyle_variant`, `invalid_bootstrap_icon` (unknown icon name), `invalid_icon_size` (outside 8–128). If you are not sure a token is valid, run the validator.

### Icons

Buttons and similar catalog-gated widgets accept `icon` (a Bootstrap Icons name, e.g. `"save"`), `iconSize` (8–128 px), and `iconOnly` (boolean) inside `toolkitProps.ttkbootstrap`. No icon font is bundled with exported projects — the generated code references the icon names via ttkbootstrap's icon support.

## Provider widget quick reference

| Widget | Key props | Binds to Tk variable |
|---|---|---|
| `DateEntry` | `dateformat`, `firstweekday` (0–6), `startdate` (ISO), `textvariable` | `textvariable` |
| `LabeledScale` | `from_` < `to`, `compound` (`top`/`bottom`) | `variable` |
| `Meter` | `amountused` ≥ 0, `amounttotal` > 0, `metertype` (`full`/`semi`), `metersize`, `meterthickness`, `showtext`, `interactive`, `subtext` | `variable` (amount used) |
| `Floodgauge` | `value`, `maximum`, `orient`, `mode`, `text`, `mask` | `variable` + `textvariable` |
| `Tableview` | `columns`, `columnWidths`, `rows`, `paginated`, `pagesize`, `searchable`, `height`, `selectmode` | — |
| `ScrolledText` | `initialText`, `wrap`, `autohide`, `vbar`, `hbar`, `undo`, `state` | — (no `textvariable`) |
| `ScrolledFrame` | `autohide`, `padding` — it is a **container** (can be a `parentId`) | — |

Ranges and enum values are validated (`invalid_dateentry_*`, `invalid_labeledscale_compound`, `invalid_scale_range`, `invalid_meter_*`, `invalid_floodgauge_*`, `invalid_tableview_*`, `invalid_scrolledtext_*`, `invalid_scrolledframe_padding`).

## Animations under ttkbootstrap

All five animation presets work, with one restriction: the `color` preset only animates classic Tk `bg`/`fg` and is **rejected on ttk themed widgets** (Button, Label, Entry, Frame, …). Classic Tk widgets in a ttkbootstrap project (Text, Canvas, Listbox) remain valid `color` targets. See animations.md.

## Choosing the toolkit

| Use tkinter when | Use ttkbootstrap when |
|---|---|
| Zero extra runtime dependencies matter | A modern themed look matters more than dependency weight |
| You need pixel-level `bg`/`fg` control on buttons/labels | You want bootstyle theming, provider widgets, and modern dialogs |
| Target runtime Python version may be < 3.10 | Preview runtime is guaranteed Python 3.10+ |
