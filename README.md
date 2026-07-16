# TK-Form for VS Code

TK-Form의 공개 배포, 사용자 매뉴얼, 그리고 커뮤니티 피드백을 위한 저장소입니다.

소스 코드와 개발 이력은 이 저장소에 포함하지 않습니다. 여기서는 검증된 VSIX 릴리스와 사용자 문서만 제공합니다.

## 설치

1. [Releases](https://github.com/atk-bckim/tk-form/releases)에서 원하는 버전의 `.vsix` 파일을 다운로드합니다.
2. VS Code에서 Extensions 뷰를 열고 `...` 메뉴에서 **Install from VSIX...**를 선택합니다.
3. 다운로드한 `.vsix` 파일을 선택합니다.

명령줄에서는 다음처럼 설치할 수 있습니다.

```bash
code --install-extension tk-form-<version>.vsix
```

## 사용자 매뉴얼

설치, 첫 프로젝트 생성, Preview, Export 방법은 [MANUAL.md](./MANUAL.md)를 참고하세요.

## 피드백과 지원

버그 제보와 기능 제안은 [Issues](https://github.com/atk-bckim/tk-form/issues)에 남겨 주세요. 재현 절차, VS Code·운영체제·Python 버전, 그리고 `TK-Form: Copy Support Summary` 결과를 포함하면 확인에 도움이 됩니다.

프로젝트 소스나 이벤트 코드는 첫 제보에 포함하지 말아 주세요. 필요한 경우 최소화하거나 민감한 정보를 가린 재현 파일을 요청드릴 수 있습니다.

상업용 라이선스와 구매 문의는 `bckim7639@gmail.com`으로 보내 주세요.

## 릴리스

각 릴리스에는 설치 가능한 VSIX 파일과 변경 사항이 포함됩니다. VSIX로 설치한 확장은 Marketplace 설치본과 달리 자동 업데이트가 기본적으로 비활성화될 수 있으므로, 새 릴리스를 주기적으로 확인해 주세요.
