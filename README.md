# TK-Form for VS Code

This repository provides public TK-Form distribution, user documentation, and community feedback. It intentionally contains no source code or development history—only verified VSIX releases and user-facing documentation.

[![Fuel my next token](https://img.shields.io/badge/Fuel%20my%20next%20token-Ko--fi-72a4f2?style=for-the-badge&logo=kofi&logoColor=white)](https://ko-fi.com/bckim)
[![Sponsor on GitHub](https://img.shields.io/badge/Sponsor-GitHub%20Sponsors-30363d?style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/atk-bckim)

## Install

1. Download the required `.vsix` file from [Releases](https://github.com/atk-bckim/tk-form/releases).
2. In VS Code, open the Extensions view and select **Install from VSIX...** from the `...` menu.
3. Select the downloaded `.vsix` file.

You can also install it from the command line:

```bash
code --install-extension tk-form-<version>.vsix
```

## Documentation

Choose a language in the [documentation index](./docs/index.md):

- [한국어](./docs/ko/index.md)
- [English](./docs/en/index.md)
- [简体中文](./docs/zh/index.md)

TK-Form v1.6.0 documentation:

- [위젯 애니메이션](./docs/ko/animations.md) / [Widget Animations](./docs/en/animations.md) / [部件动画](./docs/zh/animations.md)
- [ttkbootstrap 프로젝트](./docs/ko/ttkbootstrap.md) / [ttkbootstrap Projects](./docs/en/ttkbootstrap.md) / [ttkbootstrap 项目](./docs/zh/ttkbootstrap.md)

## AI Skill

The [`TKform-skill`](./TKform-skill/) folder ships the **tkform-author** skill for AI coding agents (Codex, Copilot, Cursor, Claude, ZCode, etc.). It teaches an agent how to author and edit `.tkform.json` — the project format of the TK-Form designer — instead of guessing the Tkinter JSON structure from scratch. The skill is refreshed for **TK-Form v1.6.0** (schema version 4).

What is inside:

| Part | Purpose |
|---|---|
| `SKILL.md` | Routing hub: mental model, authoring traps, and the standard validate-and-fix workflow |
| `references/` (11 guides) | Focused, load-on-demand docs: widgets and per-type prop allow-lists, events, Tk variables, `place`/`grid`/`pack` layout, menus, non-visual components, animations, ttkbootstrap toolkits, image resources, diagnostics |
| `references/tkform.schema.json` | The same JSON Schema the extension registers for `*.tkform.json` |
| `scripts/validate_project.py` | A validator that runs the extension's bundled Python engine — the same checks the designer's **Validate** command performs |

### Install

Point your AI agent at the folder:

```text
https://github.com/atk-bckim/tk-form/tree/main/TKform-skill
```

Most agents register the skill by cloning or copying the folder into their skills directory (for example `.agents/skills/tkform-author/`). Inside VS Code, the designer's **AI Skill** toolbar button opens the same setup guide.

### Validate a project

```bash
python TKform-skill/scripts/validate_project.py path/to/project.tkform.json
```

Run it with a local Python 3.9+ runtime. When invoked outside the tkform repository, pass the engine location with `--engine-root` — details are in [`TKform-skill/SKILL.md`](./TKform-skill/SKILL.md). A mirror of this skill also lives in the [atk-bckim/bckim-skills](https://github.com/atk-bckim/bckim-skills/tree/main/TKform-skill) repository.

## Feedback and Support

Report bugs and suggest features through [Issues](https://github.com/atk-bckim/tk-form/issues). Please include reproduction steps, your VS Code, operating-system, and Python versions, plus the output from `TK-Form: Copy Support Summary`.

Do not include project source or event code in an initial report. If needed, we may request a minimized or redacted reproduction.

For commercial licensing or purchasing inquiries, contact `bckim7639@gmail.com`.

## Releases

Each release includes an installable VSIX file and release notes. Extensions installed from a VSIX may have automatic updates disabled by default, unlike Marketplace installations, so check this repository for new releases.
