# 🖱️Drag and Ask🧙✨

텍스트를 드래그하면 나타나는 AI 버튼을 통해 OpenAI API를 호출하여 답변을 받을 수 있는 Windows 프로그램입니다.

## 🔍주요 기능

- 텍스트 드래그 시 AI 버튼 표시
- OpenAI API를 통한 텍스트 분석 및 답변
- 스크롤 가능한 답변 창
- 로깅 기능 (선택적 활성화)

## ⚙️개발 환경 설정

1. Python 3.8 이상 설치

2. 가상 환경 생성 및 활성화:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
```

3. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

4. 환경 설정 파일 생성:
    - 프로젝트 루트의 `.envSample` 파일을 `.env`로 복사합니다.
    - `.envSample`는 기본 설정이 포함된 템플릿 파일입니다.
```bash
copy .envSample .env  # Windows
# 또는
cp .envSample .env    # Linux
```

5. `.env` 파일을 열어 OpenAI API 키 설정:
```ini
# OpenAI API 설정
OPENAI_API_KEY=your_api_key_here  # 실제 API 키로 변경

# 로깅 설정
ENABLE_LOGGING=true
ENABLE_CONSOLE_LOGGING=true
LOG_LEVEL=DEBUG
```

## 🪄프로그램 실행 방법

```bash
python main.py
```

## 사용 방법

1. 화면의 아무 곳에서나 Ctrl 키를 누른 상태로 텍스트를 드래그하면 AI 버튼이 나타납니다.
2. AI 버튼을 클릭하면 OpenAI API를 통해 답변을 받아볼 수 있습니다.
3. 답변 창의 "X" 버튼 또는 창 외부를 클릭하면 창이 닫힙니다.

## 환경 설정

`.env` 파일에서 다음 설정을 변경할 수 있습니다:
- 처음 실행 시: `.envSample` 파일을 `.env`로 복사하여 사용
- `.env` 파일은 개인 설정이 포함되므로 Git에서 제외됨
- `.envSample`는 기본 설정이 포함된 템플릿 파일

```ini
# OpenAI API 설정
OPENAI_API_KEY=your_api_key_here  # 실제 API 키로 변경 필요

# 로깅 설정
ENABLE_LOGGING=true        # 파일 로깅 활성화 여부 (true/false)
ENABLE_CONSOLE_LOGGING=true  # 콘솔 로깅 활성화 여부 (true/false)
LOG_LEVEL=DEBUG           # 로그 레벨 (DEBUG/INFO/WARNING/ERROR/CRITICAL)
```

## 프로그램 구조

```
ai-drag/
├── main.py              # 메인 프로그램
├── ai_service.py        # OpenAI API 서비스
├── requirements.txt    # 패키지 의존성
├── .envSample         # 환경 설정 템플릿
├── .gitignore         # Git 제외 설정
├── README.md          # 프로젝트 설명
├── logs/             # 로그 파일 디렉토리
├── ui/               # UI 관련 모듈
│   ├── window_manager.py    # 창 관리
├── services/         # 서비스 모듈
│   ├── clipboard_manager.py  # 클립보드 관리
│   └── drag_detector.py      # 드래그 감지
└── utils/           # 유틸리티 모듈
    └── logger.py          # 로깅 유틸리티
```

## 주의사항

1. Windows 64비트 운영체제에서만 실행 가능합니다.
2. OpenAI API 키가 필요하며, API 사용에 따른 비용이 발생할 수 있습니다.
3. 프로그램 실행 중에는 클립보드 내용이 일시적으로 변경될 수 있습니다.
4. `.env` 파일에는 개인 API 키가 포함되므로 공유하지 마세요.

## 문제 해결

로그 파일은 `logs` 디렉토리에 저장되며, 문제 발생 시 해당 로그를 확인하시면 도움이 됩니다.
로그 파일명 형식: `debug_YYYYMMDD_HHMMSS.log` 