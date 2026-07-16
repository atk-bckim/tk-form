---
title: 문제 해결과 피드백
document_type: User Guide
created: 2026-07-16
last_updated: 2026-07-16
version: v1.0
status: Published
tags: [tk-form, troubleshooting, support, feedback]
---

# 문제 해결과 피드백

## 목차

- [유용한 진단 정보 수집](#유용한-진단-정보-수집)
- [자주 발생하는 문제](#자주-발생하는-문제)
- [이슈 작성](#이슈-작성)
- [관련 문서](#관련-문서)
- [변경 이력](#변경-이력)

## 유용한 진단 정보 수집

문제를 제보하기 전에 **View: Toggle Output**을 열고 **TK-Form**을 선택하세요. 그다음 **TK-Form: Copy Support Summary**를 실행합니다. 이 명령은 공개 이슈에 적합하도록 프로젝트 소스와 이벤트 코드를 제외한 진단 요약을 만듭니다.

## 자주 발생하는 문제

| 문제 | 예상 원인 | 해결 방법 |
|---|---|---|
| Validate, Export, Preview, Python Check가 비활성화됨 | 작업 영역이 신뢰되지 않았습니다. | 신뢰할 수 있는 로컬 폴더를 열고 VS Code 작업 영역 신뢰 설정에서 신뢰합니다. 신뢰되지 않아도 편집은 가능합니다. |
| Python Check 또는 Preview에서 Tkinter를 찾을 수 없음 | 선택한 Python 런타임에 Tkinter가 없습니다. | `python3 -c "import tkinter; print(tkinter.TkVersion)"`를 실행하고, 다른 절대 Python 경로를 선택하거나 Tkinter를 설치합니다. |
| Python 경로가 절대 경로여야 함 | `python`, `python3`처럼 상대 실행 파일을 명시했습니다. | `python3 -c "import sys; print(sys.executable)"`로 전체 실행 경로를 확인해 입력하거나, 구성된 기본값을 쓰도록 필드를 비웁니다. |
| `.tkform.json` 파일이 열리지 않음 | JSON이 유효하지 않거나 디자이너 밖에서 부분 편집되었습니다. | 텍스트로 열어 JSON을 수정한 뒤 다시 엽니다. **Open Example Project**의 정상 프로젝트와 비교합니다. |
| 검증 후 Export가 막힘 | 엔진이 검증 오류를 발견했습니다. | **Validate**를 실행하고 위젯, 속성, 레이아웃, 이벤트, 이름 관련 오류를 수정한 뒤 다시 Export합니다. |
| Preview가 즉시 종료됨 | 생성된 Python 예외 또는 프로세스 종료가 발생했습니다. | TK-Form Output 채널을 확인하고 같은 Python 런타임으로 재현합니다. Login 예제와 비교합니다. |
| Export 후 사용자 변경이 사라짐 | 생성 UI 파일이 다시 생성되었습니다. | Split-file Export에서 사용자 로직은 `app.py`에 둡니다. `ui_<project>.py`나 다른 재생성 파일의 편집에 의존하지 마세요. |

## 이슈 작성

버그와 기능 요청은 [GitHub Issues](https://github.com/atk-bckim/tk-form/issues)에 남겨 주세요. 다음을 포함하면 도움이 됩니다.

- 간결한 재현 순서
- VS Code 버전과 운영체제
- 디자이너 또는 `tkform.pythonPath`에 표시된 Python 버전과 런타임 경로
- 작업 영역 신뢰 여부
- 관련 TK-Form Output 줄과 **TK-Form: Copy Support Summary** 결과

최초 이슈에는 프로젝트 소스나 이벤트 코드를 포함하지 마세요. 프로젝트 파일이나 생성된 Python이 필요하면 요청 후 최소화하거나 민감한 정보를 가린 재현 예제를 제공해 주세요.

상업용 라이선스나 구매 문의는 `bckim7639@gmail.com`으로 보내 주세요.

## 관련 문서

| 문서 | 경로 | 관계 |
|---|---|---|
| 시작하기 | [getting-started.md](./getting-started.md) | 설치와 Python 설정 문제를 해결합니다. |
| 디자이너 작업 흐름 | [designer-workflow.md](./designer-workflow.md) | Validate, Preview, Export 동작을 설명합니다. |
| 기술 범위 | [technical-scope.md](./technical-scope.md) | 제품 한도와 지원 동작을 정의합니다. |

## 변경 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| v1.0 | 2026-07-16 | 한국어 문제 해결과 피드백 안내를 처음 작성했습니다. |
