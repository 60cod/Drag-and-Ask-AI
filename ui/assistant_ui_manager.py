import tkinter as tk
import logging

class AssistantUIManager:
    def __init__(self, root, logger):
        self.root = root
        self.logger = logger
        self.ai_button = None
        self.ai_popup = None
        self.event_handler = None

    def setup(self, ai_button, ai_popup, event_handler):
        """UI 컴포넌트 초기화"""
        self.ai_button = ai_button
        self.ai_popup = ai_popup
        self.event_handler = event_handler
        self.ai_popup.set_close_callback(self.hide_popup)

    def is_any_window_visible(self):
        """UI 창이 표시되어 있는지 확인"""
        return self.ai_button.is_visible() or self.ai_popup.is_visible()

    def hide_all(self):
        """모든 UI 창 숨기기"""
        self.ai_button.hide()
        self.ai_popup.hide()

    def show_ai_button(self, x, y):
        """AI 버튼 표시"""
        try:
            self.ai_button.show(x + 10, y + 10)
        except Exception as e:
            self.logger.error(f"AI 버튼 표시 중 오류 발생: {str(e)}")

    def hide_ai_button(self):
        """AI 버튼 숨기기"""
        self.ai_button.hide()

    def show_loading(self, x, y):
        """로딩 메시지 표시"""
        self.ai_popup.show(x, y, "AI가 응답을 생성하는 중입니다...")

    def show_response(self, x, y, response):
        """AI 응답 표시"""
        self.root.after(0, lambda: self.ai_popup.show(x, y, response))

    def show_error(self, x, y):
        """에러 메시지 표시"""
        self.root.after(0, lambda: self.ai_popup.show(
            x, y, "OpenAI API 호출 중 오류가 발생했습니다.\n잠시 후 다시 시도해주세요."
        ))

    def hide_popup(self):
        """팝업 창 숨기기"""
        self.event_handler.cancel_current_api_call()
        self.ai_popup.hide()

    def handle_click(self, x, y):
        """클릭 이벤트 처리"""
        if self.ai_popup.is_visible():
            self._handle_popup_click(x, y)
        elif self.ai_button.is_visible():
            self._handle_button_click(x, y)

    def _handle_popup_click(self, x, y):
        """팝업 창 클릭 처리"""
        popup_x, popup_y = self.ai_popup.get_position()
        popup_width, popup_height = self.ai_popup.get_size()
        
        if not (popup_x <= x <= popup_x + popup_width and 
                popup_y <= y <= popup_y + popup_height):
            self.hide_popup()
            self.logger.debug("AI 답변 창 숨김 (창 영역 밖 클릭)")

    def _handle_button_click(self, x, y):
        """버튼 클릭 처리"""
        btn_x, btn_y = self.ai_button.get_position()
        btn_width, btn_height = self.ai_button.get_size()
        
        if not (btn_x <= x <= btn_x + btn_width and 
                btn_y <= y <= btn_y + btn_height):
            self.ai_button.hide()
            self.logger.debug("AI 버튼 숨김 (버튼 영역 밖 클릭)")

    def get_ai_button_position(self):
        """AI 버튼 위치 반환"""
        return self.ai_button.get_position() 