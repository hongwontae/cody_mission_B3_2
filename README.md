# AI GitGen

Git diff를 기반으로 AI가 커밋 메시지와 Pull Request 설명을 자동으로 생성하는 Python CLI 프로그램입니다.

## 프로젝트 소개

개발자가 코드 변경 사항을 직접 분석하고 설명을 작성해야 하는 번거로움을 줄이기 위해 개발했습니다.

Gemini API를 활용하여 Git 변경 사항을 분석하고, 프롬프트 엔지니어링을 통해 일관된 형식의 결과물을 생성합니다.

## 주요 기능

- Git diff 기반 코드 변경 사항 분석
- Conventional Commits 형식의 커밋 메시지 생성
- Markdown 형식의 PR 설명 생성
- argparse 기반 CLI 명령어 처리
- 환경변수를 활용한 API Key 관리
- AI 응답 형식 검증
- HTTP 오류 및 Git 명령 실행 오류 처리
- 입력 및 출력 토큰 사용량 확인

## 기술 스택

- Python 3.12
- Git
- Google Gemini API
- Gemini 3.1 Flash-Lite
- requests
- subprocess
- argparse

## 설치 방법

```bash
git clone https://github.com/hongwontae/cody_mission_B3_2.git

cd cody_mission_B3_2

python3 -m venv .venv

source .venv/bin/activate

python -m pip install -r requirements.txt
```

## API Key 설정

Google AI Studio에서 Gemini API Key를 발급받습니다.

https://aistudio.google.com/apikey

발급받은 API Key를 환경변수로 설정합니다.

```bash
export FREE_OPEN_API_KEY="YOUR_API_KEY"
```

API Key는 소스 코드에 직접 작성하지 않습니다.

## 사용 방법

### 커밋 메시지 생성

```bash
git add <파일명>
python main.py commit
```

프로그램은 `git diff --cached`를 실행하여 스테이징된 변경 사항을 분석합니다.

출력 예시:

```text
fix: 음수 나이 입력 방지
```

### PR 설명 생성

```bash
python main.py pr
```

프로그램은 `git diff main...HEAD`를 실행하여 현재 브랜치의 커밋된 변경 사항을 분석합니다.

대상 브랜치를 변경할 수도 있습니다.

```bash
python main.py pr --base develop
```

### 도움말

```bash
python main.py --help
```

## 프로그램 동작 과정

1. argparse를 통해 명령줄 인자를 분석합니다.
2. subprocess를 통해 Git diff를 추출합니다.
3. 변경 사항이 존재하는지 확인합니다.
4. 실행 모드에 맞는 프롬프트를 구성합니다.
5. requests를 통해 Gemini API를 호출합니다.
6. JSON 응답에서 생성된 텍스트를 추출합니다.
7. 출력 형식을 검증하고 터미널에 출력합니다.

## 프롬프트 엔지니어링

다음 세 가지 프롬프트를 비교하는 실험을 진행했습니다.

- Prompt A: 단순 작업 지시
- Prompt B: 역할 및 제약 조건 지정
- Prompt C: 구체적인 규칙 및 Few-shot 예시 제공

실험 결과:

| 구분 | 입력 토큰 | 출력 토큰 | 전체 토큰 |
|---|---:|---:|---:|
| Prompt A | 69 | 67 | 136 |
| Prompt B | 156 | 9 | 165 |
| Prompt C | 345 | 7 | 352 |

구체적인 규칙과 예시를 제공했을 때 출력 형식 및 커밋 유형 판단이 개선되는 것을 관찰했습니다.

자세한 내용은 [프롬프트 비교 실험 보고서](docs/prompt-experiment.md)를 참고하세요.

## 예외 처리

- API Key 미설정
- 잘못된 CLI 명령어
- Git 명령 실행 실패
- 분석할 변경 사항 없음
- 지나치게 큰 Git diff
- API 인증 및 권한 오류
- API 사용 한도 초과
- 네트워크 응답 시간 초과
- AI 응답 데이터 및 출력 형식 오류

## 한계 및 주의 사항

- Git diff만으로 개발자의 모든 변경 의도를 파악할 수 없습니다.
- AI가 생성한 결과는 개발자의 검토가 필요합니다.
- 프로그램은 실제 커밋이나 PR을 자동으로 생성하지 않습니다.
- 외부 API로 Git diff를 전송하므로 민감한 정보가 포함된 코드는 주의해야 합니다.
- 무료 API 사용 한도 및 모델 제공 정책에 따라 이용이 제한될 수 있습니다.

## 관련 문서

- [프롬프트 비교 실험](docs/prompt-experiment.md)
- [트러블슈팅 보고서](docs/troubleshooting.md)
- [테스트 결과](docs/test-results.md)