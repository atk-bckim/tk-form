---
title: 위젯 애니메이션
document_type: User Guide
created: 2026-07-19
last_updated: 2026-09-06
version: v1.2
status: Published
tags: [tk-form, animation, tkinter, preview, export]
---

# 위젯 애니메이션

## 목차

- [개요](#개요)
- [애니메이션 추가와 편집](#애니메이션-추가와-편집)
- [공통 설정](#공통-설정)
- [Preset 설정](#preset-설정)
- [Trigger와 수동 제어](#trigger와-수동-제어)
- [검증, Preview, Export](#검증-preview-export)
- [생성되는 Python API](#생성되는-python-api)
- [제한과 문제 해결](#제한과-문제-해결)
- [관련 문서](#관련-문서)
- [변경 이력](#변경-이력)

## 개요

TK-Form은 위젯에 선언형 애니메이션을 추가하고 Tkinter의 `after` 스케줄링으로 실행하는 기능을 제공합니다(v1.3.0에서 도입). 애니메이션은 프로젝트 파일의 `animations` 배열에 저장되며 Validate, Preview, Function/Class/Split-file Export에 동일하게 적용됩니다.

애니메이션을 만들기 전에 대상 위젯의 위치와 크기를 확정하세요. 공간 애니메이션은 생성된 Python에서 실제로 `place()`되는 위젯에 사용할 수 있습니다.

## 애니메이션 추가와 편집

1. 캔버스 또는 객체 트리에서 대상 위젯을 선택합니다.
2. Inspector의 **Animations** 영역에서 **Add Animation**을 선택합니다.
3. 고유한 Python 식별자 형식의 이름을 입력합니다. 예: `show_panel`.
4. Preset과 Trigger를 선택하고 시간·반복·preset별 값을 설정합니다.
5. **Save**를 선택한 뒤 **Validate**와 **Preview**로 결과를 확인합니다.

기존 항목은 **Edit**로 수정하고 **Remove**로 삭제합니다. 이름은 프로젝트 안에서 고유해야 하며 Python 예약어, TK-Form 생성기 예약 이름, 이벤트 handler 또는 다른 생성 심벌과 충돌할 수 없습니다.

## 공통 설정

| 설정 | 허용 값 | 설명 |
|---|---|---|
| Name | 고유한 Python 식별자 | `start_<name>()`, `stop_<name>()` API 이름에 사용됩니다. |
| Duration | 0보다 크고 최대 600,000 ms | 한 번 재생하는 시간입니다. |
| Delay | 0–86,400,000 ms | 재생을 시작하기 전 대기 시간입니다. |
| Easing | `linear`, `easeIn`, `easeOut`, `easeInOut` | 진행률 곡선입니다. |
| Repeat count | 1–10,000 | 전체 재생 횟수입니다. |
| Infinite repeat | 켜기/끄기 | 켜면 명시적으로 중지할 때까지 반복합니다. |

프로젝트당 애니메이션은 최대 500개입니다. 새 애니메이션의 기본값은 300 ms, 지연 0 ms, `easeOut`, 반복 1회입니다.

## Preset 설정

| Preset | 파라미터 | 동작 |
|---|---|---|
| `slide` | `direction`: left/right/up/down, `distance`: 0–1,000,000 | 지정 방향의 오프셋에서 원래 위치로 이동합니다. |
| `shake` | `axis`: x/y, `distance`: 0–1,000,000, `cycles`: 1–10,000 | 원래 위치를 중심으로 감쇠 진동합니다. |
| `bounce` | `direction`: left/right/up/down, `distance`: 0–1,000,000, `cycles`: 1–10,000 | 지정 방향으로 튀었다가 원래 위치로 돌아옵니다. |
| `pulse` | `scale`: 0보다 크고 최대 1,000 | 위젯 중심을 기준으로 확대했다가 원래 크기로 돌아옵니다. |
| `color` | `property`: bg/fg, `to`: `#RGB` 또는 `#RRGGBB` | 현재 색상에서 지정 색상으로 보간합니다. |

`slide`, `shake`, `bounce`, `pulse`는 `place()`로 배치되는 위젯만 지원합니다. `color`는 선택한 `bg` 또는 `fg` 속성을 안전하게 지원하는 클래식 Tk 위젯에서만 사용할 수 있습니다. ttk 테마 위젯(ttkbootstrap의 Button, Label, Entry, Frame 등)은 `bg`/`fg` 옵션이 없어 `color` preset이 검증에서 거부됩니다. ttkbootstrap 프로젝트에서도 `Text`, `Canvas`, `Listbox` 같은 클래식 Tk 위젯은 `color`를 사용할 수 있습니다.

## Trigger와 수동 제어

| Trigger | 실행 시점 |
|---|---|
| `load` | 생성된 창의 초기 idle 처리 시 자동 시작 |
| `click` | 대상 위젯의 마우스 클릭 |
| `hoverEnter` / `hoverLeave` | 포인터가 대상 위젯에 들어오거나 나갈 때 |
| `focusIn` / `focusOut` | 대상 위젯이 키보드 포커스를 얻거나 잃을 때 |
| `manual` | 자동 binding 없이 생성된 Python API를 호출할 때 |

같은 애니메이션을 다시 시작하면 진행 중인 예약 작업을 취소하고 새 재생으로 교체합니다. `infinite` 반복은 생성된 `stop_<name>()` API로 중지하세요.

## 검증, Preview, Export

1. **Validate**는 대상 ID, 이름, 레이아웃, preset 파라미터, 색상 지원, 생성 심벌 충돌을 확인합니다.
2. **Preview**는 선택한 Tkinter 런타임에서 실제 `after` callback과 위젯 배치를 실행합니다.
3. **Export**는 검증에 성공한 애니메이션 runtime과 start/stop API를 생성합니다.

Output Dock 또는 VS Code Problems에 오류가 표시되면 해당 애니메이션을 **Edit**해 값을 수정하세요. 대상 위젯이 삭제된 orphan 애니메이션에는 제거 Quick Fix가 제공될 수 있습니다.

## 생성되는 Python API

애니메이션 이름이 `show_panel`이면 다음 API가 생성됩니다.

```python
start_show_panel()
stop_show_panel()
```

- Function Export에서는 함수가 생성되고 `root.start_show_panel`, `root.stop_show_panel`로도 노출됩니다.
- Class Export에서는 `App.start_show_panel()`과 `App.stop_show_panel()` 메서드가 생성됩니다.
- Split-file Export에서는 생성된 UI 클래스가 같은 메서드를 제공하므로 `app.py`의 인스턴스에서 호출할 수 있습니다.

Event Editor handler 안에서는 해당 export 모드가 제공하는 동일 이름의 callable을 사용하세요. 재생 제어 코드는 재생성되는 `ui_<project>.py`가 아니라 보존되는 애플리케이션 파일에 두는 것을 권장합니다.

## 제한과 문제 해결

- 실제 `Notebook` 탭은 생성 시 Tk가 관리하는 합성 `ttk.Frame`이므로 애니메이션 대상이 될 수 없습니다. 탭 안에 `place()`로 배치한 일반 자식 위젯은 대상이 될 수 있습니다.
- `grid` 위젯, `Toplevel`, `PanedWindow`/`TtkPanedWindow`가 직접 관리하는 pane에는 공간 preset을 사용할 수 없습니다.
- 색상 preset이 거부되면 대상 위젯이 선택한 `bg`/`fg` 속성을 지원하는지 확인하세요.
- 잘못된 외부 프로젝트 값은 Inspector에 그대로 표시되며 수정하기 전에는 저장할 수 없습니다.
- Preview가 움직이지 않으면 먼저 **Validate**를 실행하고 Tkinter가 포함된 Python 런타임인지 확인하세요.
- 같은 이름의 위젯, Tk 변수, 리소스, 이벤트 handler 또는 자동 생성 메뉴 handler와 animation API 이름이 충돌하지 않도록 하세요.

## 관련 문서

| 문서 | 경로 | 관계 |
|---|---|---|
| 시작하기 | [getting-started.md](./getting-started.md) | v1.6.0 설치와 Python 준비를 설명합니다. |
| 디자이너 작업 흐름 | [designer-workflow.md](./designer-workflow.md) | Validate, Preview, Export 순서를 설명합니다. |
| ttkbootstrap 프로젝트 | [ttkbootstrap.md](./ttkbootstrap.md) | ttkbootstrap 프로젝트에서의 애니메이션 제한을 포함합니다. |
| 기술 범위 | [technical-scope.md](./technical-scope.md) | 프로젝트 형식, 지원 기능과 안전 한도를 정의합니다. |
| 문제 해결과 피드백 | [troubleshooting.md](./troubleshooting.md) | 런타임 및 진단 문제의 복구 방법을 제공합니다. |

## 변경 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| v1.2 | 2026-09-06 | v1.6.0 기준으로 ttk 테마 위젯의 color preset 거부 규칙과 ttkbootstrap 링크를 추가했습니다. |
| v1.1 | 2026-07-21 | 릴리스 참조를 v1.3.1로 갱신했습니다. |
| v1.0 | 2026-07-19 | TK-Form v1.3.0 위젯 애니메이션 안내를 작성했습니다. |
