---
title: 시작하기
document_type: User Guide
created: 2026-07-16
last_updated: 2026-07-21
version: v1.2
status: Published
tags: [tk-form, vscode, tkinter, installation]
---

# 시작하기

## 목차

- [개요](#개요)
- [요구 사항](#요구-사항)
- [VSIX 설치](#vsix-설치)
- [첫 프로젝트 만들기](#첫-프로젝트-만들기)
- [Python과 Tkinter 확인](#python과-tkinter-확인)
- [관련 문서](#관련-문서)
- [변경 이력](#변경-이력)

## 개요

TK-Form은 Tkinter 인터페이스를 시각적으로 설계하는 VS Code 확장입니다. 이 안내는 공개 **v1.3.1** VSIX 릴리스를 기준으로 하며, 예제 프로젝트에서 로컬 Python 런타임을 먼저 확인한 뒤 자체 인터페이스를 설계하도록 안내합니다.

## 요구 사항

- VS Code **1.94 이상**
- 검증, Preview, Export에 사용할 Tkinter 포함 로컬 Python 런타임
- Python을 실행하는 기능을 사용하기 전에 신뢰로 설정한 로컬 작업 영역

신뢰되지 않은 작업 영역에서도 `.tkform.json` 파일을 열고, 편집하고, 저장할 수 있습니다. 하지만 Validate, 코드 생성, Export, Preview, Python 런타임 확인은 로컬 Python을 실행하므로 비활성화됩니다.

## VSIX 설치

1. [v1.3.1 릴리스](https://github.com/atk-bckim/tk-form/releases/tag/v1.3.1)에서 `tk-form-1.3.1.vsix`를 내려받거나, 필요한 다른 릴리스를 선택합니다.
2. VS Code에서 Extensions 뷰를 엽니다.
3. `...` 메뉴의 **Install from VSIX...**를 선택하고 내려받은 파일을 선택합니다.

명령줄에서도 설치할 수 있습니다.

```bash
code --install-extension tk-form-1.3.1.vsix
```

VSIX로 설치한 확장은 기본적으로 자동 업데이트되지 않을 수 있습니다. 업데이트가 필요할 때는 [Releases](https://github.com/atk-bckim/tk-form/releases) 페이지를 확인하세요.

## 첫 프로젝트 만들기

1. VS Code에서 로컬 폴더를 열고 작업 영역을 신뢰로 설정합니다.
2. 명령 팔레트에서 **TK-Form: Open Example Project**를 실행합니다.
3. **Login**을 선택하고 생성된 `.tkform.json` 파일을 저장합니다. 이후 TK-Form 사용자 지정 편집기가 열립니다.
4. 디자이너의 **Python** 패널에서 절대 Python 실행 경로를 지정하거나 구성된 기본값을 사용합니다.
5. **Check Python**을 실행한 뒤 **Validate**, **Preview**, **Export** 순서로 진행합니다.

빈 디자인에서 시작하려면 **TK-Form: New Project**를 실행하세요. 기존 `.tkform.json` 파일을 열면 TK-Form 사용자 지정 편집기가 자동으로 실행됩니다.

## Python과 Tkinter 확인

Preview에는 Tkinter가 포함된 Python 런타임이 필요합니다. 터미널에서 다음 명령으로 확인할 수 있습니다.

```bash
python3 -c "import tkinter; print(tkinter.TkVersion)"
```

명령이 실패하면 디자이너의 **Python** 패널에서 다른 절대 Python 실행 경로를 선택하거나 Tkinter가 포함된 Python 배포판을 설치하세요.

## 관련 문서

| 문서 | 경로 | 관계 |
|---|---|---|
| 디자이너 작업 흐름 | [designer-workflow.md](./designer-workflow.md) | 일상적인 설계와 내보내기 흐름을 설명합니다. |
| 위젯 애니메이션 | [animations.md](./animations.md) | 현재 preset, trigger와 생성 Python API를 설명합니다. |
| 기술 범위 | [technical-scope.md](./technical-scope.md) | 지원 기능과 운영 한도를 설명합니다. |
| 문제 해결과 피드백 | [troubleshooting.md](./troubleshooting.md) | 설정 문제와 이슈 작성 방법을 다룹니다. |

## 변경 이력

| 버전 | 날짜 | 변경 사항 |
|---|---|---|
| v1.2 | 2026-07-21 | 현재 릴리스와 설치 파일을 v1.3.1로 갱신했습니다. |
| v1.1 | 2026-07-19 | v1.3.0 설치 파일과 애니메이션 안내 링크로 갱신했습니다. |
| v1.0 | 2026-07-16 | 공개 문서 저장소용 한국어 시작 안내를 처음 작성했습니다. |
