---
title: TK-Form 사용자 매뉴얼
document_type: User Manual
created: 2026-07-16
last_updated: 2026-07-16
version: v1.0
status: Published
tags: [tk-form, vscode, tkinter]
---

# TK-Form 사용자 매뉴얼

## 목차

- [개요](#개요)
- [요구 사항](#요구-사항)
- [빠른 시작](#빠른-시작)
- [기본 작업 흐름](#기본-작업-흐름)
- [Export 모드](#export-모드)
- [Python 런타임](#python-런타임)
- [주요 명령](#주요-명령)
- [문제 해결과 피드백](#문제-해결과-피드백)
- [관련 문서](#관련-문서)
- [변경 이력](#변경-이력)

## 개요

TK-Form은 VS Code 안에서 Tkinter 인터페이스를 시각적으로 설계하고, 검증·실행 미리보기·Python 내보내기를 수행하는 확장입니다. 프로젝트는 읽을 수 있는 `.tkform.json` 파일로 저장됩니다.

## 요구 사항

- VS Code 1.94 이상
- Preview용 Tkinter 포함 Python 런타임
- Python을 실행하는 기능을 사용할 때 신뢰할 수 있는 로컬 작업 영역

`.tkform.json`의 열기·편집·저장은 신뢰되지 않은 작업 영역에서도 가능하지만, Validate·Export·Preview·Python 런타임 확인은 로컬 Python을 실행하므로 신뢰된 작업 영역에서만 사용할 수 있습니다.

## 빠른 시작

1. 로컬 폴더를 VS Code에서 열고 작업 영역을 신뢰합니다.
2. 명령 팔레트에서 `TK-Form: Open Example Project`를 실행합니다.
3. `Login` 예제를 선택하고 생성된 `.tkform.json` 파일을 저장합니다.
4. 디자이너 도구 모음의 `Python` 패널에서 Python 실행 파일을 지정하거나 기본 런타임을 사용합니다.
5. `Check Python`으로 런타임을 확인한 뒤 `Validate`, `Preview`, `Export` 순서로 진행합니다.

새 프로젝트는 `TK-Form: New Project`로 만들 수 있습니다. 기존 `.tkform.json` 파일을 열면 시각적 편집기가 자동으로 실행됩니다.

## 기본 작업 흐름

1. **Design** — 캔버스에서 위젯을 배치하고 크기·속성·이벤트를 편집합니다.
2. **Validate** — 프로젝트 구조, 레이아웃, 옵션, 생성 코드 관련 문제를 확인합니다.
3. **Preview** — 선택한 로컬 Python으로 실제 Tkinter 창을 실행합니다.
4. **Export** — 프로젝트에 맞는 Python 시작 코드를 저장합니다.

## Export 모드

- **Function**: 단일 파일 스크립트를 생성합니다. 이름을 지정한 위젯은 `root._tkform_widgets`로 접근할 수 있습니다.
- **Class**: `App(tk.Tk)` 클래스를 생성합니다. 이름을 지정한 위젯은 `self.<widget_name>` 속성으로 접근할 수 있습니다.
- **Split-file**: `ui_<project>.py`는 재생성하고 사용자 시작점은 별도로 유지합니다. `app.py`는 없을 때만 생성됩니다.

생성된 UI 파일은 재생성 시 교체될 수 있습니다. 사용자 로직은 Split-file 모드의 `app.py`처럼 생성 대상 밖의 파일에 두는 것을 권합니다.

## Python 런타임

대부분의 경우 디자이너의 `Python` 패널에서 런타임을 선택하면 됩니다. 다음 설정도 사용할 수 있습니다.

- `tkform.pythonPath`: Preview에 사용할 절대 Python 경로
- `tkform.enginePythonPath`: 검증·코드 생성용 선택적 Python 경로
- `tkform.previewInheritPythonPath`: 프로젝트 폴더와 기존 `PYTHONPATH` 상속 여부

Tkinter 사용 가능 여부는 터미널에서 확인할 수 있습니다.

```bash
python3 -c "import tkinter; print(tkinter.TkVersion)"
```

## 주요 명령

- `TK-Form: New Project`
- `TK-Form: Open Project`
- `TK-Form: Open Example Project`
- `TK-Form: Validate Project`
- `TK-Form: Preview Project`
- `TK-Form: Stop Preview`
- `TK-Form: Export Python`
- `TK-Form: Open Output`
- `TK-Form: Check Python Runtime`
- `TK-Form: Copy Support Summary`

## 문제 해결과 피드백

문제가 발생하면 먼저 `View: Toggle Output`에서 `TK-Form` 출력을 확인하세요. 버그 제보 시에는 재현 절차, VS Code·운영체제·Python 버전, 작업 영역 신뢰 여부, `TK-Form: Copy Support Summary` 결과를 [Issues](https://github.com/atk-bckim/tk-form/issues)에 남겨 주세요.

민감한 프로젝트 소스나 이벤트 코드는 처음부터 첨부하지 마세요. 필요한 경우 최소 재현 예제 또는 정보를 가린 파일을 요청드릴 수 있습니다.

## 관련 문서

| 문서 | 경로 | 관계 |
|---|---|---|
| TK-Form for VS Code | [README.md](./README.md) | VSIX 설치와 피드백 창구 안내 |

## 변경 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| v1.0 | 2026-07-16 | 공개 배포·피드백 레포용 최초 매뉴얼 |
