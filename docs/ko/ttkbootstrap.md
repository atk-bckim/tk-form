---
title: ttkbootstrap 프로젝트
document_type: User Guide
created: 2026-09-06
last_updated: 2026-09-06
version: v1.0
status: Published
tags: [tk-form, ttkbootstrap, theme, widgets, dialogs]
---

# ttkbootstrap 프로젝트

## 목차

- [개요](#개요)
- [프로젝트를 ttkbootstrap으로 설정](#프로젝트를-ttkbootstrap으로-설정)
- [테마와 bootstyle](#테마와-bootstyle)
- [provider 위젯](#provider-위젯)
- [다이얼로그, 토스트, 툴팁](#다이얼로그-토스트-툴팁)
- [런타임 요구 사항](#런타임-요구-사항)
- [캔버스 근사와 제한](#캔버스-근사와-제한)
- [관련 문서](#관련-문서)
- [변경 이력](#변경-이력)

## 개요

TK-Form v1.3.3부터 프로젝트마다 UI 툴킷으로 **ttkbootstrap 2.x**를 선택할 수 있습니다. ttkbootstrap 프로젝트는 부트스트랩 스타일의 테마와 bootstyle 속성, 추가 provider 위젯, 모던한 다이얼로그·토스트·툴팁 컴포넌트를 제공하며, Function/Class/Split-file 모두 ttkbootstrap 기반 Python 코드로 Export합니다.

ttkbootstrap은 확장에 번들되지 않은 **선택 의존성**입니다. 디자인과 Export에는 확장만 있으면 되지만, Preview와 실행에는 선택한 Python 런타임에 ttkbootstrap 패키지가 설치되어 있어야 합니다.

## 프로젝트를 ttkbootstrap으로 설정

1. **TK-Form: New Project**로 빈 프로젝트를 만들거나 **TK-Form: Open Example Project**에서 **Ttkbootstrap Login**, **Ttkbootstrap Widgets**, **Ttkbootstrap Dialogs** 예제를 엽니다.
2. 디자이너의 툴킷 설정에서 프로젝트 UI 툴킷을 `ttkbootstrap`(majorVersion 2)으로 지정합니다.
3. 위젯을 배치하고 [테마와 bootstyle](#테마와-bootstyle)을 편집한 뒤 Validate → Preview → Export 순서로 진행합니다.

툴킷은 프로젝트 단위 속성입니다. 일반 Tkinter 프로젝트와 ttkbootstrap 프로젝트의 편집 워크플로는 같지만, 사용할 수 있는 속성과 컴포넌트가 달라집니다.

## 테마와 bootstyle

- **테마**는 프로젝트 속성입니다. 프로젝트에 하나의 ttkbootstrap 테마를 지정하면 생성된 Python이 해당 테마로 창을 초기화합니다.
- **bootstyle**은 위젯별 속성입니다. 버튼, 라벨, 입력창 등 ttkbootstrap이 지원하는 위젯에 색상·스타일 변형을 지정하면 Inspector에서 편집하고 생성 코드에 반영됩니다.
- ttkbootstrap 프로젝트에서 Inspector는 위젯마다 실제 백엔드 모듈을 따라갑니다. ttk 스타일 속성을 지원하는 위젯은 ttk 속성을, 클래식 tk로 폴백하는 `Text`, `Canvas`, `Listbox`, `PanedWindow`, `Message` 같은 위젯은 tk 스타일 속성을 노출합니다.

## provider 위젯

ttkbootstrap 프로젝트에서는 다음 provider 위젯을 사용할 수 있습니다.

| 위젯 | 용도 |
|---|---|
| `DateEntry` | 날짜 선택 입력창 |
| `LabeledScale` | 라벨이 붙은 슬라이더 |
| `Meter` | 게이지형 값 표시 |
| `Floodgauge` | 진행 상태를 채우는 게이지 |
| `Tableview` | 표 형태 데이터 뷰 |
| `ScrolledText` | 스크롤이 통합된 텍스트 영역 |
| `ScrolledFrame` | 스크롤이 통합된 프레임 |

provider 위젯은 ttkbootstrap 프로젝트에서만 사용할 수 있으며, 일반 Tkinter 프로젝트에서는 팔레트에 나타나지 않습니다.

## 다이얼로그, 토스트, 툴팁

ttkbootstrap 프로젝트에서는 비시각 컴포넌트로 다음을 사용할 수 있습니다.

| 컴포넌트 | 용도 |
|---|---|
| `TtkMessagebox` | ttkbootstrap 스타일 메시지 상자 |
| `Querybox` | 사용자 입력을 묻는 대화상자 |
| `DatePickerDialog` | 날짜 선택 대화상자 |
| `ColorPickerDialog` | 색상 선택 대화상자 |
| `ToastNotification` | 화면 가장자리에 사라지는 알림 |
| `ToolTip` | 위젯에 붙이는 툴팁 |

현재 범위에는 `FontDialog`와 `Querybox.get_font`가 포함되지 않고, 생성된 프로젝트에 아이콘 폰트가 번들되지도 않습니다.

## 런타임 요구 사항

- Preview 런타임은 **Python 3.10 이상**이어야 합니다(일반 Tkinter 프로젝트의 검증·코드 생성 엔진 기준은 3.9 이상).
- Preview 런타임에 `ttkbootstrap>=2,<3`을 설치합니다. 예: `pip install "ttkbootstrap>=2,<3"`
- **ttkbootstrap 3.x는 지원하지 않습니다.** 생성 코드는 Python 3.10을 대상으로 작성됩니다.

## 캔버스 근사와 제한

- 캔버스의 ttkbootstrap 색상과 bootstyle은 CSS 근사입니다. 최종 외관은 Preview 창이 기준입니다.
- 위젯 아이콘은 캔버스에서 문자 플레이스홀더로 렌더링되며, 실제 아이콘은 Preview에서 나타납니다.
- provider 위젯(`Meter`, `Floodgauge`, `Tableview`, `DateEntry`, `LabeledScale`, `ScrolledText`, `ScrolledFrame`)은 캔버스에서 스케치 프리뷰로 렌더링됩니다.
- 애니메이션은 캔버스에서 재생되지 않습니다.
- `color` 애니메이션 preset은 ttk 테마 위젯(ttkbootstrap의 Button, Label, Entry, Frame 등)에서 거부됩니다. `Text`, `Canvas`, `Listbox` 같은 클래식 Tk 위젯은 ttkbootstrap 프로젝트에서도 `color`를 사용할 수 있습니다.

## 관련 문서

| 문서 | 경로 | 관계 |
|---|---|---|
| 시작하기 | [getting-started.md](./getting-started.md) | 설치와 Python 런타임 준비를 설명합니다. |
| 디자이너 작업 흐름 | [designer-workflow.md](./designer-workflow.md) | 공통 편집·검증·Export 흐름을 설명합니다. |
| 위젯 애니메이션 | [animations.md](./animations.md) | ttkbootstrap 프로젝트에서의 애니메이션 제한을 포함합니다. |
| 기술 범위 | [technical-scope.md](./technical-scope.md) | 지원 위젯과 운영 한도를 정의합니다. |
| 문제 해결과 피드백 | [troubleshooting.md](./troubleshooting.md) | ttkbootstrap 런타임 문제의 복구 방법을 제공합니다. |

## 변경 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| v1.0 | 2026-09-06 | TK-Form v1.6.0 기준 ttkbootstrap 프로젝트 안내를 처음 작성했습니다. |
