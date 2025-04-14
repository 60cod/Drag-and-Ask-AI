import tkinter as tk
import logging
from services.text_capture_service import TextCaptureService
from services.event_handler_service import EventHandlerService
from services.clipboard_manager import ClipboardManager
from services.drag_detector import DragDetector
from services.api_key_manager import APIKeyManager
from ui.window_manager import AIButton, AIPopup
from ui.assistant_ui_manager import AssistantUIManager
from ai_service import AIService

class AIAssistant:
    def __init__(self):
        # 로거 설정
        self.logger = logging.getLogger(__name__)
        self.logger.info("프로그램 시작")
        
        # API 키 입력 받기
        api_key = APIKeyManager.get_api_key()
        if not api_key:
            self.logger.error("API 키를 찾을 수 없음")
            raise ValueError("OpenAI API 키가 설정되지 않았습니다.")
        
        # 메인 윈도우 설정
        self.root = tk.Tk()
        self.root.withdraw()
        
        # 서비스 초기화
        self.ai_service = AIService(api_key)
        self.clipboard = ClipboardManager(self.logger)
        self.text_capture = TextCaptureService(self.clipboard)
        
        # UI 매니저 초기화
        self.ui_manager = AssistantUIManager(self.root, self.logger)
        
        # 이벤트 핸들러 초기화
        self.event_handler = EventHandlerService(
            self.text_capture,
            self.ui_manager,
            self.ai_service
        )
        
        # UI 컴포넌트 생성
        self.ai_button = AIButton(self.root, self.event_handler.on_ai_button_click, self.logger)
        self.ai_popup = AIPopup(self.root, self.logger)
        
        # UI 매니저 설정
        self.ui_manager.setup(self.ai_button, self.ai_popup, self.event_handler)
        
        # 드래그 감지기 초기화
        self.drag_detector = DragDetector(
            self.logger,
            self.event_handler.on_drag_start,
            self.event_handler.on_drag_end,
            self.event_handler.on_click
        )
        
        self.logger.info("초기화 완료")
    
    def run(self):
        """프로그램 실행"""
        try:
            # 이벤트 루프 설정
            self.event_handler.setup_event_loop()
            
            # 마우스 이벤트 리스너 설정
            self.drag_detector.setup_listeners()
            
            self.logger.info("이벤트 리스너 설정 완료")
            self.root.mainloop()
        except Exception as e:
            self.logger.error(f"프로그램 실행 오류: {str(e)}")
        finally:
            self.event_handler.cleanup()

if __name__ == "__main__":
    assistant = AIAssistant()
    assistant.run()
