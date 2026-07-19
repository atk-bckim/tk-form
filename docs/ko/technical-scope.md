---
title: 기술 범위
document_type: Reference
created: 2026-07-16
last_updated: 2026-07-19
version: v1.1
status: Published
tags: [tk-form, architecture, tkinter, scope]
---

# 기술 범위

## 목차

- [릴리스 범위](#릴리스-범위)
- [아키텍처와 데이터 흐름](#아키텍처와-데이터-흐름)
- [프로젝트 모델](#프로젝트-모델)
- [지원되는 설계 기능](#지원되는-설계-기능)
- [지원 위젯 종류](#지원-위젯-종류)
- [검증과 안전 한도](#검증과-안전-한도)
- [현재 경계](#현재-경계)
- [관련 문서](#관련-문서)
- [변경 이력](#변경-이력)

## 릴리스 범위

이 문서는 공개 **TK-Form v1.3.0** VSIX 릴리스를 설명합니다. TK-Form은 실용적인 Tkinter 애플리케이션을 위한 시각적 저작·코드 생성 도구이며, 범용 IDE나 손으로 작성한 Python을 양방향으로 편집하는 도구는 아닙니다.

## 아키텍처와 데이터 흐름

| 계층 | 현재 구현 |
|---|---|
| VS Code 통합 | TypeScript 확장 호스트, `*.tkform.json` 사용자 지정 편집기, 확장 명령, 작업 영역 신뢰 적용, 출력, Preview 프로세스 관리, Export 파일 접근 |
| 디자이너 웹뷰 | React, Vite, Tailwind CSS, Zustand 상태 관리, `dnd-kit` 상호작용 지원, CodeMirror Python 편집 지원 |
| 프로젝트 형식 | `*.tkform.json`용 JSON Schema draft-07, 새 파일은 schema version 3 사용 |
| Python 엔진 | Python 표준 라이브러리와 Tkinter/ttk를 사용하는 번들 `tkform_engine` 패키지. 검증, Python 생성, Preview 담당 |

일반적인 데이터 흐름은 다음과 같습니다.

```text
*.tkform.json → TK-Form 사용자 지정 편집기 → 확장 호스트 → 번들 Python 엔진
                                                   ├─ 진단과 출력
                                                   ├─ Preview 프로세스
                                                   └─ 생성된 Python 파일
```

디자이너는 불러온 프로젝트를 schema version 3으로 정규화합니다. version 1·2 파일은 열 수 있으며 저장할 때 마이그레이션됩니다.

## 프로젝트 모델

프로젝트는 루트 창, 위젯, 메뉴, Tk 변수, 이미지 리소스, 비시각 컴포넌트, 애니메이션을 설명합니다. 위젯 ID는 내부에서 안정적으로 참조되며, 위젯과 애니메이션 이름은 유효하고 고유한 Python 식별자여야 하고 생성된 Python의 이름으로 사용됩니다.

모델이 지원하는 항목은 다음과 같습니다.

- 루트 창의 크기, 배경, 크기 조정 가능 여부, ttk 테마
- `place`, `grid` 레이아웃 매니저. 같은 부모의 자식은 하나의 매니저를 사용해야 하며 `Toplevel`, `PanedWindow`, `TtkPanedWindow` 아래는 예외입니다.
- `command` 핸들러와 `<Button-1>`, `<Key>` 등의 Tk 바인딩 시퀀스를 위한 Event Editor
- 메뉴 계층, 메뉴 명령, 단축키 바인딩
- `StringVar`, `IntVar`, `DoubleVar`, `BooleanVar` 선언
- 위젯 ID로 참조하는 Base64 이미지 리소스
- `Timer`, `FileDialog`, `ColorChooser`, `MessageBox` 비시각 컴포넌트
- `slide`, `shake`, `bounce`, `pulse`, `color` preset과 load/click/hover/focus/manual trigger를 사용하는 위젯 애니메이션
- `bindings.command`를 사용하는 표준 Scrollbar 바인딩. 이전 호환을 위해 `xscrollcommand`, `yscrollcommand`도 허용

Scrollbar의 가로 대상은 `Text`, `Listbox`, `Entry`, `Treeview`, `Canvas`이고, 세로 대상은 `Text`, `Listbox`, `Treeview`, `Canvas`입니다.

## 지원되는 설계 기능

시각 편집기는 캔버스 배치, 드래그와 크기 조정, 정렬, 스냅, 확대/축소, 다중 선택, 객체 트리, 속성 편집, 메뉴, 변수, 리소스, 비시각 컴포넌트, 애니메이션을 지원합니다. 프로젝트 검증기는 코드 생성 전에 교차 참조, 중복·예약 이름, 속성 호환성, 레이아웃 일관성, 바인딩, 애니메이션 파라미터와 생성 심벌, 페이로드 한도, 이벤트 핸들러 문법을 확인합니다.

레거시 위젯 `props.command` 필드는 Python 함수 참조만 허용합니다. 인라인 Python 로직은 Event Editor에 작성하세요. 둘 다 있을 때는 Event Editor의 command가 우선합니다.

## 지원 위젯 종류

| 분류 | 위젯 종류 |
|---|---|
| 일반 컨트롤 | `Button`, `Label`, `Entry`, `Text`, `Checkbutton`, `Radiobutton`, `Listbox`, `Scale`, `OptionMenu`, `Spinbox`, `Scrollbar`, `Menubutton`, `Message` |
| 컨테이너와 레이아웃 | `Frame`, `LabelFrame`, `Canvas`, `PanedWindow`, `TtkPanedWindow`, `Notebook`, `Toplevel` |
| ttk 추가 위젯 | `Progressbar`, `Combobox`, `Treeview`, `Sizegrip`, `Separator` |

`Notebook`, `Progressbar`, `Combobox`, `Treeview`, `Sizegrip`, `Separator`, `TtkPanedWindow`은 ttk 생성자를 사용합니다. 지원 속성은 클래식 Tk 위젯과 다르며, 예를 들어 `bg`, `fg`, `padx`, `pady` 같은 클래식 시각 속성은 같은 방식으로 지원되지 않습니다.

## 검증과 안전 한도

| 한도 | 최대값 |
|---|---:|
| 프로젝트 페이로드 | 8 MiB |
| 이미지 업로드 | 이미지당 5 MiB |
| 위젯 | 2,000개 |
| 리소스 | 200개 |
| Tk 변수 | 500개 |
| 비시각 컴포넌트 | 500개 |
| 애니메이션 | 500개 |
| 위젯·메뉴 중첩 | 64단계 |

Python을 실행하는 작업에는 신뢰된 로컬 작업 영역이 필요합니다. 명시적인 Export 대상은 절대 경로여야 하며 신뢰된 작업 영역 폴더 안에 있어야 합니다. Preview에는 Tkinter가 있는 로컬 Python 런타임이 필요합니다.

## 현재 경계

- 생성된 Python은 시작점입니다. TK-Form은 재생성하는 파일 안의 수동 편집을 보존하지 않으며 손으로 작성한 Python과 양방향 동기화를 제공하지 않습니다.
- 캔버스는 Tk 레이아웃을 근사합니다. 캔버스 결과를 최종 런타임 레이아웃으로 간주하기 전에 Validate와 Preview를 실행하세요.
- Split-file Export는 기존 `app.py`를 보호하지만 이후 Export에서 `ui_<project>.py`를 다시 작성합니다.
- 레거시 `command` 속성에는 인라인 Python 코드를 넣을 수 없습니다. Event Editor를 사용하세요.
- `Text`는 `textvariable`을 지원하지 않습니다.
- `Entry`는 가로 Scrollbar 바인딩만 지원합니다.
- 공간 애니메이션은 생성 Python에서 실제로 `place()`되는 위젯만 지원합니다. 실제 `Notebook` 탭, `grid` 위젯, `Toplevel`, pane으로 관리되는 위젯은 대상이 될 수 없습니다.
- 색상 애니메이션은 대상 위젯이 안전하게 지원하는 `bg` 또는 `fg` 속성에만 적용됩니다.
- 제품은 실용적이고 자주 사용하는 단일 창 폼과 내부 도구에 초점을 둡니다. 자동 라이선스, 인앱 계정 관리, 광범위한 엔터프라이즈 셀프서비스는 포함하지 않습니다.

## 관련 문서

| 문서 | 경로 | 관계 |
|---|---|---|
| 시작하기 | [getting-started.md](./getting-started.md) | 릴리스를 설치하고 런타임을 준비합니다. |
| 디자이너 작업 흐름 | [designer-workflow.md](./designer-workflow.md) | 설계, Preview, Export에서 이 기능을 적용합니다. |
| 위젯 애니메이션 | [animations.md](./animations.md) | preset, trigger, 생성 API와 대상 제한을 설명합니다. |
| 문제 해결과 피드백 | [troubleshooting.md](./troubleshooting.md) | 한도와 검증 실패를 진단하는 데 도움이 됩니다. |

## 변경 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| v1.1 | 2026-07-19 | v1.3.0 schema v3 애니메이션 기능과 한계를 반영했습니다. |
| v1.0 | 2026-07-16 | 공개 문서 저장소용 한국어 기술 범위 참고 문서를 처음 작성했습니다. |
