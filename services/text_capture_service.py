import pyautogui
import keyboard
import time
import logging

class TextCaptureService:
    def __init__(self, clipboard_manager):
        self.logger = logging.getLogger(__name__)
        self.clipboard = clipboard_manager
        self.captured_text = None

    def capture_text(self):
        """드래그된 텍스트를 캡처"""
        try:
            # 현재 클립보드 내용 저장
            original_clipboard = self.clipboard.save_current_content()
            
            # 선택된 텍스트를 클립보드로 복사
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.2)  # 복사 완료 대기
            
            # 복사된 텍스트 저장
            self.captured_text = self.clipboard.get_text()
            
            # 원래 클립보드 내용 복원
            self.clipboard.restore()
            
            return self.captured_text if self.captured_text and self.captured_text.strip() else None
            
        except Exception as e:
            self.logger.error(f"텍스트 캡처 중 오류 발생: {str(e)}")
            self.clipboard.restore()
            return None

    def clear_captured_text(self):
        """캡처된 텍스트 초기화"""
        self.captured_text = None

    def get_captured_text(self):
        """캡처된 텍스트 반환"""
        return self.captured_text 