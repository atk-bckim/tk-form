# TK-Form — Visual Tkinter GUI Designer for VS Code

Design Tkinter interfaces with **drag & drop** in VS Code, preview the real Tkinter window, and export **clean, runnable Python code** — no coordinate math, no hand-written layout code.

[![Latest release](https://img.shields.io/github/v/release/atk-bckim/tk-form)](https://github.com/atk-bckim/tk-form/releases)
[![VS Code](https://img.shields.io/badge/VS%20Code-1.94%2B-007ACC?logo=visualstudiocode&logoColor=white)](https://code.visualstudio.com/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Fuel my next token](https://img.shields.io/badge/Fuel%20my%20next%20token-Ko--fi-72a4f2?style=flat-square&logo=kofi&logoColor=white)](https://ko-fi.com/bckim)
[![Sponsor on GitHub](https://img.shields.io/badge/Sponsor-GitHub%20Sponsors-30363d?style=flat-square&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/atk-bckim)

<!-- TODO(demo-gif): upload the demo animation to atk-bckim/asset at tkform/marketplace/demo.gif, then uncomment:
![TK-Form demo: drag widgets onto the canvas, tweak properties, preview the real Tkinter window, and export Python](https://raw.githubusercontent.com/atk-bckim/asset/main/tkform/marketplace/demo.gif)
Storyboard: 0-2s drag a Button and an Entry from the palette onto the canvas · 2-4s edit a label and event code in the Inspector · 4-6s run Preview showing the real Tkinter window · 6-8s run Export and scroll the generated Python. Keep it under 10s, 800px wide.
-->

TK-Form brings a WinForms-style visual workflow to Tkinter: place widgets on a canvas, edit properties and events in an inspector, run the **real Tkinter preview**, and export a working Python starting point — all without leaving VS Code.

## Why TK-Form?

Hand-writing Tkinter layout means guessing pixel coordinates, fighting `pack()` and `grid()` options, and running the app over and over just to move a button. TK-Form replaces that loop with a visual designer backed by a readable `.tkform.json` project file and a validation engine, so the thing you see on the canvas is one click away from the thing your users will run.

## Key Features

- **Visual drag & drop designer** — place, resize, align, snap, and zoom widgets on a canvas with multi-select and a widget tree.
- **Real Tkinter preview** — run the actual interface in a local Python runtime, not a mock-up.
- **Validation before export** — cross-references, prop allow-lists, layout rules, name collisions, and event-handler syntax are checked before code generation.
- **Three export modes** — a single-file `create_window()` script, an `App(tk.Tk)` class, or a split `ui_<project>.py` + `app.py` pair.
- **`place`, `grid`, and `pack` layouts** — including grid row/column stretch weights and pack fill/expand options.
- **ttkbootstrap 2.x support** — 30 themes, per-widget `bootstyle`, seven provider widgets (Meter, Tableview, DateEntry, …), and themed dialogs, toast, and tooltips.
- **Widget animations** — seven presets (`slide`, `shake`, `bounce`, `pulse`, `color`, `fill`, `grow`) with triggers, easing curves, and generated `start_*()`/`stop_*()` APIs.
- **Event Editor with autocompletion** — inline Python handlers with in-scope suggestions for widgets, Tk variables, and generated APIs.
- **AI-friendly** — a readable JSON project format plus a ready-made AI skill for Codex, Copilot, Cursor, and other coding agents.

## Supported Widgets

Classic Tk: `Button`, `Label`, `Entry`, `Text`, `Checkbutton`, `Radiobutton`, `Listbox`, `Scale`, `OptionMenu`, `Spinbox`, `Scrollbar`, `Menubutton`, `Message` · Containers: `Frame`, `LabelFrame`, `Canvas`, `PanedWindow`, `Notebook`, `Toplevel` · ttk: `Progressbar`, `Combobox`, `Treeview`, `Sizegrip`, `Separator`, `TtkPanedWindow` · ttkbootstrap providers: `DateEntry`, `LabeledScale`, `Meter`, `Floodgauge`, `Tableview`, `ScrolledText`, `ScrolledFrame`.

Non-visual components: `Timer`, `FileDialog`, `ColorChooser`, `MessageBox`, plus ttkbootstrap `TtkMessagebox`, `Querybox`, `DatePickerDialog`, `ColorPickerDialog`, `ToastNotification`, and `ToolTip`. See the full [technical scope](./docs/en/technical-scope.md).

## Installation

### Visual Studio Code Marketplace

```bash
code --install-extension Byeong-cheolKim.tk-form
```

### VSIX from GitHub Releases

1. Download `tk-form-<version>.vsix` from [Releases](https://github.com/atk-bckim/tk-form/releases).
2. In VS Code, open the Extensions view and choose **Install from VSIX...** from the `...` menu.

VSIX-installed extensions may not auto-update — check the [Releases](https://github.com/atk-bckim/tk-form/releases) page for new versions.

## Quick Start

1. Open a trusted local folder, then run **TK-Form: Open Example Project** and pick an example (six included — from a minimal login form to ttkbootstrap widget showcases).
2. Edit the design on the canvas, then run **Check Python → Validate → Preview** to see the real Tkinter window.
3. Run **Export Python** and save the generated `.py` file — a runnable starting point you can extend.

## Documentation

User documentation is available in three languages:

- [한국어 문서](./docs/ko/index.md)
- [English documentation](./docs/en/index.md)
- [简体中文文档](./docs/zh/index.md)

Highlights: [Widget Animations](./docs/en/animations.md) · [ttkbootstrap Projects](./docs/en/ttkbootstrap.md) · [Technical Scope](./docs/en/technical-scope.md) · [Troubleshooting](./docs/en/troubleshooting.md)

## AI Skill

The [`TKform-skill`](./TKform-skill/) folder ships the **tkform-author** skill for AI coding agents (Codex, Copilot, Cursor, Claude, ZCode, etc.). It teaches an agent how to author and edit `.tkform.json` project files instead of guessing the Tkinter JSON structure, bundles the same JSON Schema as the extension, and includes a validator script backed by the extension's Python engine.

Point your agent at the folder to register the skill:

```text
https://github.com/atk-bckim/tk-form/tree/main/TKform-skill
```

See [`TKform-skill/SKILL.md`](./TKform-skill/SKILL.md) for the full guide.

## Feedback and Support

Report bugs and suggest features through [Issues](https://github.com/atk-bckim/tk-form/issues). Please include reproduction steps, your VS Code, operating-system, and Python versions, plus the output from `TK-Form: Copy Support Summary`. Do not include project source or event code in an initial report.

For commercial licensing or purchasing inquiries, contact `bckim7639@gmail.com`. Personal use is free; commercial/enterprise use requires a paid license.

Sponsorship: [Ko-fi](https://ko-fi.com/bckim) · [GitHub Sponsors](https://github.com/sponsors/atk-bckim)
