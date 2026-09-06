---
title: Getting Started
document_type: User Guide
created: 2026-07-16
last_updated: 2026-09-06
version: v1.3
status: Published
tags: [tk-form, vscode, tkinter, installation]
---

# Getting Started

## Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Install the VSIX](#install-the-vsix)
- [Create a First Project](#create-a-first-project)
- [Check Python and Tkinter](#check-python-and-tkinter)
- [Related Documents](#related-documents)
- [Change History](#change-history)

## Overview

TK-Form is a VS Code extension for visually designing Tkinter interfaces. This guide applies to the public **v1.6.0** VSIX release and starts with an example project so you can confirm your local Python runtime before designing your own interface.

## Requirements

- VS Code **1.94 or later**.
- A local Python runtime that includes Tkinter for validation, Preview, and Export. The validation and code-generation engine requires **Python 3.9+**, and ttkbootstrap project previews require **Python 3.10+**.
- For ttkbootstrap previews, the selected runtime needs the `ttkbootstrap>=2,<3` package (an optional dependency that ships outside the extension).
- A local workspace that you trust before using Python-backed actions.

Opening, editing, and saving `.tkform.json` files remains available in an untrusted workspace. Validation, code generation, Export, Preview, and Python-runtime inspection are disabled there because they execute local Python.

## Install the VSIX

1. Download `tk-form-1.6.0.vsix` from the [v1.6.0 release](https://github.com/atk-bckim/tk-form/releases/tag/v1.6.0), or choose another release that matches your needs.
2. In VS Code, open the Extensions view.
3. Select **Install from VSIX...** from the `...` menu and choose the downloaded file.

You can also use the command line:

```bash
code --install-extension tk-form-1.6.0.vsix
```

VSIX-installed extensions may not auto-update by default. Check the [Releases](https://github.com/atk-bckim/tk-form/releases) page when you want to update.

## Create a First Project

1. Open a local folder in VS Code and mark it as trusted.
2. Run **TK-Form: Open Example Project** from the Command Palette.
3. Choose an example. Alongside **Login**, **Settings Panel**, and **Data Browser**, the ttkbootstrap examples **Ttkbootstrap Login**, **Ttkbootstrap Widgets**, and **Ttkbootstrap Dialogs** are available. The ttkbootstrap examples need the ttkbootstrap package and Python 3.10+ to preview.
4. Save the generated `.tkform.json` file and allow the TK-Form custom editor to open it.
5. Open the designer's **Python** panel and either select an absolute Python executable or use the configured default.
6. Run **Check Python**, then select **Validate**, **Preview**, and **Export** in that order.

To begin with a blank design instead, run **TK-Form: New Project**. Opening an existing `.tkform.json` file launches the TK-Form custom editor automatically.

## Check Python and Tkinter

Preview needs a Python runtime with Tkinter. Check the runtime from a terminal:

```bash
python3 -c "import tkinter; print(tkinter.TkVersion)"
```

If this command fails, select another absolute Python executable in the designer's **Python** panel or install a Python distribution that includes Tkinter. If the reported version is below 3.9, the validation and code-generation engine does not meet its requirements, and ttkbootstrap projects should preview on a 3.10+ runtime.

## Related Documents

| Document | Path | Relationship |
|---|---|---|
| Designer Workflow | [designer-workflow.md](./designer-workflow.md) | Explains the day-to-day design and export flow. |
| ttkbootstrap Projects | [ttkbootstrap.md](./ttkbootstrap.md) | Covers ttkbootstrap themes, widgets, and runtime requirements. |
| Widget Animations | [animations.md](./animations.md) | Covers the current presets, triggers, and generated Python APIs. |
| Technical Scope | [technical-scope.md](./technical-scope.md) | Lists supported features and operating limits. |
| Troubleshooting and Feedback | [troubleshooting.md](./troubleshooting.md) | Covers common setup failures and issue reports. |

## Change History

| Version | Date | Changes |
|---|---|---|
| v1.3 | 2026-09-06 | Updated the current release and installation artifact for v1.6.0 and added the Python runtime requirements and ttkbootstrap examples. |
| v1.2 | 2026-07-21 | Updated the current release and installation artifact for v1.3.1. |
| v1.1 | 2026-07-19 | Updated the install artifact and links for the v1.3.0 animation release. |
| v1.0 | 2026-07-16 | Initial English guide for the public documentation repository. |
