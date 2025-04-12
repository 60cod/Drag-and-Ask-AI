import win32clipboard
import win32con
import logging

class ClipboardManager:
    def __init__(self, logger):
        self.logger = logger
        self.original_content = None

    def save_current_content(self):
        """현재 클립보드 내용을 저장"""
        try:
            win32clipboard.OpenClipboard()
            if win32clipboard.IsClipboardFormatAvailable(win32con.CF_UNICODETEXT):
                self.original_content = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
        except Exception as e:
            self.logger.error(f"클립보드 저장 오류: {str(e)}")

    def get_text(self):
        """클립보드에서 텍스트 가져오기"""
        try:
            win32clipboard.OpenClipboard()
            text = ""
            if win32clipboard.IsClipboardFormatAvailable(win32con.CF_UNICODETEXT):
                text = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
            return text
        except Exception as e:
            self.logger.error(f"클립보드 읽기 오류: {str(e)}")
            return ""

    def restore(self):
        """클립보드 내용을 원래대로 복원"""
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            if self.original_content:
                win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, self.original_content)
                self.original_content = None
            win32clipboard.CloseClipboard()
            self.logger.debug("클립보드 내용 복원됨")
        except Exception as e:
            self.logger.error(f"클립보드 복원 오류: {str(e)}") 