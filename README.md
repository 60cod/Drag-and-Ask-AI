[English](#english) | [한국어](#korean)

---

# 🖱️Drag and Ask🧙

<a name="english"></a>

This program lets you drag text to reveal an AI button, which, when clicked, instantly sends the text to the AI and displays the response in a small pop-up window. There's no need to switch between windows, offering quick and seamless communication with the AI. Its intuitive interface greatly boosts productivity. ✨

![demo](docs/images/usage_demo.gif)

### 💡Key Features

- AI button appears when text is dragged
- Text analysis and responses through OpenAI API
- Scrollable answer window
- Logging functionality (optional)

### ⚙️Development Environment Setup

1. Install Python 3.8 or higher

2. Create and activate virtual environment:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# or
source venv/bin/activate     #Linux/Mac
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create environment configuration file:
   - Copy `.envSample` file to `.env` in the project root.
   - `.envSample` is a template file containing default settings.
```bash
copy .envSample .env  # Windows
# or
cp .envSample .env    # Linux/Mac
```

5. Open `.env` file and set OpenAI API key:
```ini
# OpenAI API Settings
OPENAI_API_KEY=your_api_key_here  # Replace with your actual API key

# Logging Settings
ENABLE_LOGGING=false
ENABLE_CONSOLE_LOGGING=false
LOG_LEVEL=DEBUG
```

### 🪄Running the Program

```bash
python main.py
```

### How to Use

1. Hold Ctrl key and drag text anywhere on screen to display the AI button.
2. Click the AI button to get responses through OpenAI API.
3. Click the "X" button or outside the answer window to close it.

### Project Structure

```
ai-drag/
├── main.py              # Main program
├── ai_service.py        # OpenAI API service
├── requirements.txt    # Package dependencies
├── .envSample         # Environment settings template
├── .gitignore         # Git exclusion settings
├── README.md          # Project description
├── logs/             # Log files directory
├── ui/               # UI modules
│   ├── window_manager.py    # Window management
├── services/         # Service modules
│   ├── clipboard_manager.py  # Clipboard management
│   └── drag_detector.py      # Drag detection
└── utils/           # Utility modules
    └── logger.py          # Logging utility
```

### Precautions

1. Requires OpenAI API key, and API usage may incur costs.
2. Clipboard contents may be temporarily modified while the program is running.
3. Do not share your `.env` file as it contains your personal API key.

### Troubleshooting

Log files are stored in the `logs` directory and can be helpful when issues occur.
Log file format: `debug_YYYYMMDD_HHMMSS.log`

---

# 🖱️Drag and Ask🧙

<a name="korean"></a>

이 프로그램은 텍스트를 드래그하면 AI 버튼이 나타나고, 클릭하면 즉시 AI에게 질문하여 답변을 작은 창으로 화면에 바로 보여줍니다. 별도의 대화창을 열거나 전환할 필요 없이 빠르고 간편하게 AI와 소통할 수 있습니다. 직관적인 인터페이스로 작업 효율성을 크게 향상시킵니다.✨

![demo](docs/images/usage_demo.gif)

## 💡주요 기능

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
# or
source venv/bin/activate     #Linux/Mac
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
ENABLE_LOGGING=false
ENABLE_CONSOLE_LOGGING=false
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

1. OpenAI API 키가 필요하며, API 사용에 따른 비용이 발생할 수 있습니다.
2. 프로그램 실행 중에는 클립보드 내용이 일시적으로 변경될 수 있습니다.
3. `.env` 파일에는 개인 API 키가 포함되므로 공유하지 마세요.

## 문제 해결

로그 파일은 `logs` 디렉토리에 저장되며, 문제 발생 시 해당 로그를 확인하시면 도움이 됩니다.
로그 파일명 형식: `debug_YYYYMMDD_HHMMSS.log` 