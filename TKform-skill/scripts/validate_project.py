#!/usr/bin/env python3
"""Validate a tkform project file (.tkform.json) using a tkform engine.

Usage:
    python validate_project.py path/to/project.tkform.json
    python validate_project.py --engine-root /path/to/tkform/python path/to/project.tkform.json
    python validate_project.py --python /path/to/python --engine-root /path/to/tkform/python -

Exit code 0 if there are no error-severity diagnostics, 1 otherwise.
Output:
    - On success: "OK" (plus any warnings/errors counts as a heads-up).
    - On failure: one line per diagnostic: "severity · code · path · message".

Python executable resolution:
    1. --python
    2. TKFORM_ENGINE_PYTHON
    3. .vscode/settings.json: tkform.enginePythonPath
    4. .vscode/settings.json: tkform.pythonPath
    5. python3/python

Engine root resolution:
    1. --engine-root
    2. TKFORM_ENGINE_ROOT
    3. nearest python/tkform_engine or tkform_engine directory from the project/cwd
"""

import argparse
import json
import os
import re
import subprocess
import sys


ALLOWED_ENV_KEYS = set([
    "COMSPEC",
    "CONDA_PREFIX",
    "HOME",
    "HOMEDRIVE",
    "HOMEPATH",
    "LANG",
    "LC_ALL",
    "LC_CTYPE",
    "PATH",
    "PATHEXT",
    "PYENV_ROOT",
    "SYSTEMROOT",
    "TEMP",
    "TMP",
    "TMPDIR",
    "USERPROFILE",
    "VIRTUAL_ENV",
    "WINDIR",
])


def _parse_args(argv):
    parser = argparse.ArgumentParser(description="Validate a tkform project file with the tkform Python engine.")
    parser.add_argument("project", help="Path to a .tkform.json file, or '-' to read JSON from stdin.")
    parser.add_argument("--python", dest="python_executable", help="Python executable for running tkform_engine.cli.")
    parser.add_argument(
        "--engine-root",
        help="Directory containing tkform_engine, or the repository root containing python/tkform_engine.",
    )
    return parser.parse_args(argv[1:])


def _read_payload(path_arg):
    if path_arg == "-" or path_arg is None:
        raw = sys.stdin.read()
    else:
        with open(path_arg, "r", encoding="utf-8") as handle:
            raw = handle.read()
    return json.loads(raw or "{}")


def _resolve_python(args, project_path):
    workspace_root, settings = _load_workspace_settings(project_path)
    candidates = [
        args.python_executable,
        _env_python(),
        _setting(settings, "tkform.enginePythonPath"),
        _setting(settings, "tkform.pythonPath"),
    ]
    for candidate in candidates:
        value = _expand_path(candidate, workspace_root)
        if value:
            return value
    return "python" if sys.platform.startswith("win") else "python3"


def _resolve_engine_root(args, project_path):
    candidates = [
        args.engine_root,
        os.environ.get("TKFORM_ENGINE_ROOT"),
        _legacy_engine_root_env(),
    ]
    for candidate in candidates:
        root = _normalize_engine_root(_expand_path(candidate, None))
        if root:
            return root

    for start in _search_starts(project_path):
        current = start
        while current:
            root = _normalize_engine_root(current)
            if root:
                return root
            parent = os.path.dirname(current)
            if parent == current:
                break
            current = parent

    raise SystemExit(
        "Could not locate tkform_engine. Use --engine-root or set TKFORM_ENGINE_ROOT "
        "to the directory containing tkform_engine, or to the tkform repo root."
    )


def _env_python():
    value = os.environ.get("TKFORM_ENGINE_PYTHON")
    if value and os.path.isdir(os.path.expanduser(value)):
        return ""
    return value


def _legacy_engine_root_env():
    value = os.environ.get("TKFORM_ENGINE_PYTHON")
    if value and os.path.isdir(os.path.expanduser(value)):
        return value
    return ""


def _normalize_engine_root(value):
    if not value:
        return ""
    value = os.path.abspath(os.path.expanduser(value))
    if os.path.isdir(os.path.join(value, "tkform_engine")):
        return value
    python_root = os.path.join(value, "python")
    if os.path.isdir(os.path.join(python_root, "tkform_engine")):
        return python_root
    return ""


def _search_starts(project_path):
    starts = []
    if project_path and project_path != "-":
        starts.append(os.path.abspath(os.path.dirname(project_path)))
    starts.append(os.getcwd())
    # Local repo layout: <repo>/.agents/skills/tkform-author/scripts/validate_project.py.
    starts.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")))

    deduped = []
    for start in starts:
        if start not in deduped:
            deduped.append(start)
    return deduped


def _load_workspace_settings(project_path):
    for start in _search_starts(project_path):
        current = start
        while current:
            settings_path = os.path.join(current, ".vscode", "settings.json")
            if os.path.isfile(settings_path):
                return current, _read_jsonc_file(settings_path)
            parent = os.path.dirname(current)
            if parent == current:
                break
            current = parent
    return os.getcwd(), {}


def _read_jsonc_file(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            text = handle.read()
        text = _strip_json_comments(text)
        text = re.sub(r",\s*([}\]])", r"\1", text)
        parsed = json.loads(text or "{}")
        return parsed if isinstance(parsed, dict) else {}
    except Exception:
        return {}


def _strip_json_comments(text):
    result = []
    index = 0
    in_string = False
    escape = False
    while index < len(text):
        char = text[index]
        next_char = text[index + 1] if index + 1 < len(text) else ""
        if in_string:
            result.append(char)
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            index += 1
            continue
        if char == '"':
            in_string = True
            result.append(char)
            index += 1
            continue
        if char == "/" and next_char == "/":
            index += 2
            while index < len(text) and text[index] not in "\r\n":
                index += 1
            continue
        if char == "/" and next_char == "*":
            index += 2
            while index + 1 < len(text) and not (text[index] == "*" and text[index + 1] == "/"):
                index += 1
            index += 2
            continue
        result.append(char)
        index += 1
    return "".join(result)


def _setting(settings, key):
    value = settings.get(key) if isinstance(settings, dict) else None
    return value if isinstance(value, str) else ""


def _expand_path(value, workspace_root):
    if not isinstance(value, str):
        return ""
    value = value.strip()
    if not value:
        return ""
    if workspace_root:
        value = value.replace("${workspaceFolder}", workspace_root)
    return os.path.expandvars(os.path.expanduser(value))


def _python_env(base_env):
    env = {}
    for key, value in base_env.items():
        if value is None:
            continue
        if key in ALLOWED_ENV_KEYS or key == "Path" or key.startswith("LC_"):
            env[key] = value
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONNOUSERSITE"] = "1"
    env["PYTHONUTF8"] = "1"
    return env


def _run_engine(python, engine_root, payload):
    process = subprocess.Popen(
        [python, "-m", "tkform_engine.cli", "validate"],
        cwd=engine_root,
        env=_python_env(os.environ),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = process.communicate(json.dumps(payload).encode("utf-8"))
    stdout_text = stdout.decode("utf-8", "replace")
    stderr_text = stderr.decode("utf-8", "replace")
    if process.returncode != 0:
        raise SystemExit(stderr_text.strip() or stdout_text.strip() or "tkform engine process failed")
    try:
        response = json.loads(stdout_text or "{}")
    except Exception as exc:
        raise SystemExit("tkform engine returned invalid JSON: %s\n%s" % (exc, stdout_text))
    if not isinstance(response, dict) or not response.get("ok"):
        raise SystemExit(str(response.get("error") if isinstance(response, dict) else "tkform engine request failed"))
    result = response.get("result")
    return result if isinstance(result, dict) else {}


def _print_diagnostics(result):
    diagnostics = result.get("diagnostics")
    if not isinstance(diagnostics, list):
        diagnostics = []

    errors = [d for d in diagnostics if isinstance(d, dict) and d.get("severity") == "error"]
    warnings = [d for d in diagnostics if isinstance(d, dict) and d.get("severity") == "warning"]

    if not diagnostics:
        print("OK")
        return 0

    for diagnostic in diagnostics:
        if not isinstance(diagnostic, dict):
            continue
        severity = diagnostic.get("severity") or ""
        code = diagnostic.get("code") or ""
        location = diagnostic.get("path") or ""
        message = diagnostic.get("message") or ""
        widget_id = diagnostic.get("widget_id")
        widget_name = diagnostic.get("widget_name")
        suffix = ""
        if widget_name:
            suffix = " (widget: %s)" % widget_name
        elif widget_id:
            suffix = " (widget id: %s)" % widget_id
        print("%s · %s · %s · %s%s" % (severity, code, location, message, suffix))

    sys.stderr.write("\n%d error(s), %d warning(s)\n" % (len(errors), len(warnings)))
    return 1 if errors else 0


def main(argv):
    args = _parse_args(argv)
    payload = _read_payload(args.project)
    python = _resolve_python(args, args.project)
    engine_root = _resolve_engine_root(args, args.project)
    result = _run_engine(python, engine_root, payload)
    return _print_diagnostics(result)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
