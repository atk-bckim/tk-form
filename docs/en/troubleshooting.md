---
title: Troubleshooting and Feedback
document_type: User Guide
created: 2026-07-16
last_updated: 2026-07-16
version: v1.0
status: Published
tags: [tk-form, troubleshooting, support, feedback]
---

# Troubleshooting and Feedback

## Contents

- [Collect Useful Diagnostics](#collect-useful-diagnostics)
- [Common Problems](#common-problems)
- [Report an Issue](#report-an-issue)
- [Related Documents](#related-documents)
- [Change History](#change-history)

## Collect Useful Diagnostics

Open **View: Toggle Output** and choose **TK-Form** before reporting a problem. Then run **TK-Form: Copy Support Summary**. It produces a sanitized summary intended for a public issue and excludes project source and event code.

## Common Problems

| Problem | Likely cause | Recovery |
|---|---|---|
| Validate, Export, Preview, or Python Check is disabled | The workspace is not trusted. | Open a local folder you trust, then use VS Code workspace-trust controls to trust it. Editing remains available while untrusted. |
| Python Check or Preview says Tkinter is unavailable | The selected Python runtime does not include Tkinter. | Run `python3 -c "import tkinter; print(tkinter.TkVersion)"`, then choose a different absolute Python path or install Tkinter. |
| Python path must be absolute | A relative executable such as `python` or `python3` was set explicitly. | Use `python3 -c "import sys; print(sys.executable)"` and enter the full executable path, or leave the field blank to use the configured default. |
| A `.tkform.json` file will not open | The file is invalid JSON or was only partially edited outside the designer. | Open it as text, correct the JSON, and reopen it. Use **Open Example Project** to compare with a working project. |
| Export is blocked after validation | The engine found validation errors. | Run **Validate**, correct the reported widget, property, layout, event, or name issue, then export again. |
| Preview starts and exits immediately | Generated Python raised an exception or the process closed. | Inspect the TK-Form Output channel and reproduce with the same Python runtime. Compare with the Login example. |
| Custom changes disappeared after Export | A generated UI file was regenerated. | Keep custom logic in `app.py` with Split-file export; do not rely on edits inside `ui_<project>.py` or another regenerated file. |

## Report an Issue

Report bugs and feature requests through [GitHub Issues](https://github.com/atk-bckim/tk-form/issues). Include:

- A concise reproduction sequence.
- VS Code version and operating system.
- Python version and the runtime path shown by the designer or `tkform.pythonPath`.
- Whether the workspace is trusted.
- The relevant TK-Form Output lines and the result of **TK-Form: Copy Support Summary**.

Do not include project source or event code in an initial report. If a project file or generated Python is necessary, provide a minimized or redacted reproduction after it is requested.

For commercial licensing or purchasing inquiries, email `bckim7639@gmail.com`.

## Related Documents

| Document | Path | Relationship |
|---|---|---|
| Getting Started | [getting-started.md](./getting-started.md) | Resolves installation and Python setup problems. |
| Designer Workflow | [designer-workflow.md](./designer-workflow.md) | Explains Validate, Preview, and Export behavior. |
| Technical Scope | [technical-scope.md](./technical-scope.md) | Defines product limits and supported behavior. |

## Change History

| Version | Date | Changes |
|---|---|---|
| v1.0 | 2026-07-16 | Initial English troubleshooting and feedback guide. |
