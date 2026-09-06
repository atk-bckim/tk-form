---
title: 디자이너 작업 흐름
document_type: User Guide
created: 2026-07-16
last_updated: 2026-09-06
version: v1.3
status: Published
tags: [tk-form, workflow, export, preview]
---

# 디자이너 작업 흐름

## 목차

- [디자인 화면](#디자인-화면)
- [핵심 작업 흐름](#핵심-작업-흐름)
- [레이아웃 매니저](#레이아웃-매니저)
- [Export 모드](#export-모드)
- [Python 런타임 구성](#python-런타임-구성)
- [작업 영역 신뢰와 파일 안전성](#작업-영역-신뢰와-파일-안전성)
- [관련 문서](#관련-문서)
- [변경 이력](#변경-이력)

## 디자인 화면

`*.tkform.json` 사용자 지정 편집기는 Tkinter·ttk 위젯을 배치하는 캔버스, 속성 검사기, 객체 트리, 메뉴·Tk 변수·이미지 리소스·비시각 컴포넌트 제어 영역을 제공합니다. 드래그, 크기 조정, 정렬, 스냅, 확대/축소, 다중 선택, 속성 및 이벤트 코드 편집을 사용할 수 있습니다.

프로젝트마다 UI 툴킷을 선택합니다. 기본은 표준 Tkinter이고, 프로젝트를 **ttkbootstrap**으로 설정하면 테마와 위젯별 bootstyle을 편집할 수 있습니다. 자세한 내용은 [ttkbootstrap 프로젝트](./ttkbootstrap.md)를 참고하세요.

반응형 아이콘 중심 명령 모음은 자주 쓰는 작업을 계속 보여 주고, 보조 작업은 오버플로 메뉴로 묶습니다. 접근 가능한 툴팁은 각 작업을 설명합니다. Inspector 섹션은 키보드 탐색 가능한 아이콘 탭이며, 진단 배지와 위젯 애니메이션용 **Motion** 탭을 제공합니다.

Event Editor의 Python 코드 편집기는 자동완성을 제공합니다. 현재 handler 범위의 이름(위젯, Tk 변수, 비시각 컴포넌트, `event`·`value`·`result`·`self` 같은 handler 매개변수)은 입력하는 즉시 제안되고, 점(`.`) 뒤에는 위젯 타입에 맞는 Tk/ttk 메서드와 속성이 제안됩니다. `Ctrl+Space`로 언제든 목록을 열 수 있고, 편집기 위쪽 한 줄짜리 **In scope** 힌트에 현재 handler에서 사용할 수 있는 이름이 표시됩니다.

번들 예제는 **Login**, **Settings Panel**, **Data Browser**와 ttkbootstrap 예제인 **Ttkbootstrap Login**, **Ttkbootstrap Widgets**, **Ttkbootstrap Dialogs**입니다. 수정하지 말아야 하는 고정 템플릿이 아니라 동작하는 참고 디자인으로 활용하세요.

## 핵심 작업 흐름

1. **Design** — 위젯을 배치하고, 부모 컨테이너·레이아웃·속성을 지정하며 필요할 때 이벤트 로직을 추가합니다.
2. **Validate** — **TK-Form: Validate Project**를 실행하여 프로젝트 구조, 위젯 속성, 레이아웃 규칙, 이름, 바인딩, 이벤트 핸들러 문법을 확인합니다.
3. **Preview** — **TK-Form: Preview Project**를 실행하여 선택한 로컬 Python 런타임으로 인터페이스를 생성하고 엽니다. 실행 중인 미리보기는 **TK-Form: Stop Preview**로 종료합니다.
4. **Export** — **TK-Form: Export Python**을 실행하고 신뢰된 작업 영역 안의 저장 위치를 선택합니다.

캔버스는 Tk 레이아웃의 근사이며, 특히 ttkbootstrap 테마와 `pack` 배치에서 차이가 날 수 있습니다. 디자이너에도 "캔버스 근사 — Preview가 최종" 상태 안내가 표시됩니다. 최종 크기와 배치는 항상 Validate와 Preview로 확인하세요.

**TK-Form: Open Output**에서 검증, Preview, Export 메시지를 확인할 수 있습니다. **TK-Form: Copy Support Summary**는 프로젝트 소스나 이벤트 코드 없이 정리된 진단 요약을 복사합니다.

## 레이아웃 매니저

`place`, `grid`, `pack` 세 가지 레이아웃 매니저를 지원합니다.

| 매니저 | 지정 방식 | 적합한 용도 |
|---|---|---|
| `place` | 위젯별 x/y 좌표와 크기 | 픽셀 단위의 고정 배치 |
| `grid` | 행·열 그리드 셀 | 표 형태의 대화상자와 폼 |
| `pack` | side/fill/expand/padx/pady/anchor | 도구 모음처럼 한 방향으로 쌓는 유동 레이아웃 |

`pack`은 위젯별 `packSide`(`top`/`bottom`/`left`/`right`), `packFill`, `packExpand`, `packPadX`, `packPadY`, `packAnchor`를 Layout 탭에서 편집합니다. 캔버스는 pack을 유연한 행·열(flex)로 근사하므로 Preview가 최종 렌더링입니다. pack의 쌓이는 순서는 형제 순서를 따르므로, pack으로 배치된 자식에는 z-order 동작이 제공되지 않습니다.

같은 부모의 자식은 하나의 매니저를 사용해야 합니다. 단, `Toplevel`, `PanedWindow`, `TtkPanedWindow` 아래에서는 매니저를 섞을 수 있습니다. 매니저를 섞어 쓰면 검증에서 알려 줍니다.

## Export 모드

| 모드 | 결과물 | 용도 |
|---|---|---|
| Function | `create_window()`가 있는 단일 파일 스크립트 | 작고 직접적인 애플리케이션 시작점. 이름을 지정한 위젯은 `root._tkform_widgets`로 접근합니다. |
| Class | 단일 파일의 `App(tk.Tk)` 클래스 | 클래스 기반 UI. 이름을 지정한 위젯과 Tk 변수는 `self.<name>` 속성이 됩니다. |
| Split-file | 재생성되는 `ui_<project>.py`와 별도 `app.py` 시작점 | 재생성 UI 파일 밖에 사용자 애플리케이션 로직을 둡니다. `app.py`는 없을 때만 생성합니다. |

생성된 UI 코드는 편집 가능한 시작점이며 양방향 동기화 시스템이 아닙니다. 다시 내보내면 생성 파일이 교체될 수 있습니다. 특히 Split-file 모드에서는 사용자 로직을 생성 UI 파일 밖에 두세요.

## Python 런타임 구성

디자이너의 **Python** 패널에서 Preview 인터프리터를 설정하거나 다음 VS Code 설정을 사용할 수 있습니다.

| 설정 | 용도 |
|---|---|
| `tkform.pythonPath` | Preview에 사용할 절대 Python 실행 경로 |
| `tkform.enginePythonPath` | 검증과 코드 생성에 사용할 선택적 Python 실행 경로 |
| `tkform.previewInheritPythonPath` | 활성화하면 프로젝트 폴더를 앞에 두고 기존 `PYTHONPATH`를 상속합니다. 기본값은 비활성화입니다. |

Preview의 우선순위는 디자이너 패널, `tkform.pythonPath`, `TKFORM_PREVIEW_PYTHON`, 엔진 런타임 순서입니다. 검증과 코드 생성은 `TKFORM_ENGINE_PYTHON`, `tkform.enginePythonPath`, macOS/Linux의 `python3` 또는 Windows의 `python` 순서로 선택합니다.

## 작업 영역 신뢰와 파일 안전성

Python을 실행하는 작업에는 신뢰된 로컬 작업 영역이 필요합니다. 명시적으로 지정하는 Export 대상은 절대 경로여야 하며 신뢰된 작업 영역 폴더 안에 있어야 합니다. 이는 신뢰되지 않거나 무관한 위치에서 Python 실행과 파일 내보내기가 동작하지 않도록 합니다.

## 관련 문서

| 문서 | 경로 | 관계 |
|---|---|---|
| 시작하기 | [getting-started.md](./getting-started.md) | 설치와 최초 실행 구성을 다룹니다. |
| ttkbootstrap 프로젝트 | [ttkbootstrap.md](./ttkbootstrap.md) | ttkbootstrap 테마, bootstyle, provider 위젯을 다룹니다. |
| 위젯 애니메이션 | [animations.md](./animations.md) | Inspector에서 애니메이션을 구성하고 Preview·Export하는 방법을 다룹니다. |
| 기술 범위 | [technical-scope.md](./technical-scope.md) | 지원 위젯, 데이터 모델 기능, 한계를 정의합니다. |
| 문제 해결과 피드백 | [troubleshooting.md](./troubleshooting.md) | 작업 흐름이 실패할 때의 복구 방법을 제공합니다. |

## 변경 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| v1.3 | 2026-09-06 | v1.6.0 기준으로 pack 레이아웃, Event Editor 자동완성, 캔버스 근사 안내, ttkbootstrap 링크를 추가했습니다. |
| v1.2 | 2026-07-21 | v1.3.1의 반응형 명령 모음과 키보드 탐색 Inspector 탭을 문서화했습니다. |
| v1.1 | 2026-07-19 | v1.3.0 위젯 애니메이션 안내 링크를 추가했습니다. |
| v1.0 | 2026-07-16 | 공개 문서 저장소용 한국어 작업 흐름 안내를 처음 작성했습니다. |
