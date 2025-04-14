import keyboard
import pyautogui
import logging
import asyncio
from threading import Thread

class EventHandlerService:
    def __init__(self, text_capture_service, ui_manager, ai_service):
        self.logger = logging.getLogger(__name__)
        self.text_capture = text_capture_service
        self.ui_manager = ui_manager
        self.ai_service = ai_service
        self.current_api_call = None
        self.loop = None

    def setup_event_loop(self):
        """이벤트 루프 설정"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        # 이벤트 루프 실행을 위한 스레드 시작
        loop_thread = Thread(target=self._run_event_loop, daemon=True)
        loop_thread.start()

    def _run_event_loop(self):
        """이벤트 루프 실행"""
        self.loop.run_forever()

    def on_drag_start(self):
        """드래그 시작 처리"""
        if self.ui_manager.is_any_window_visible():
            return
        self.ui_manager.hide_all()

    def on_drag_end(self, x, y):
        """드래그 종료 처리"""
        try:
            if keyboard.is_pressed('ctrl'):
                captured_text = self.text_capture.capture_text()
                if captured_text:
                    self.ui_manager.show_ai_button(x, y)
                else:
                    self.logger.debug("드래그된 텍스트가 없음")
            else:
                self.logger.debug("Ctrl 키가 눌리지 않은 상태")
        except Exception as e:
            self.logger.error(f"드래그 종료 처리 중 오류 발생: {str(e)}")

    def on_click(self, *args):
        """클릭 이벤트 처리"""
        if not self.ui_manager.is_any_window_visible():
            return

        x, y = pyautogui.position()
        self.ui_manager.handle_click(x, y)

    async def _get_ai_response(self, text, button_x, button_y):
        """AI 응답 요청 및 처리"""
        try:
            response = await self.ai_service.get_response(text)
            self.ui_manager.show_response(button_x, button_y, response)
        except Exception as error:
            error_msg = str(error)
            self.logger.error(f"API 호출 중 오류 발생: {error_msg}")
            self.ui_manager.show_error(button_x, button_y)
        finally:
            self.current_api_call = None
            self.text_capture.clear_captured_text()

    def on_ai_button_click(self):
        """AI 버튼 클릭 처리"""
        self.logger.info("AI 버튼 클릭됨")
        try:
            captured_text = self.text_capture.get_captured_text()
            if captured_text and captured_text.strip():
                button_x, button_y = self.ui_manager.get_ai_button_position()
                self.logger.debug(f"버튼 위치: ({button_x}, {button_y})")
                
                self.ui_manager.hide_ai_button()
                self.ui_manager.show_loading(button_x, button_y)
                
                self.current_api_call = asyncio.run_coroutine_threadsafe(
                    self._get_ai_response(captured_text, button_x, button_y),
                    self.loop
                )
            else:
                self.logger.warning("저장된 드래그 텍스트 없음")
        except Exception as e:
            self.logger.error(f"AI 버튼 클릭 처리 오류: {str(e)}")
            self.text_capture.clear_captured_text()

    def cancel_current_api_call(self):
        """현재 진행 중인 API 호출 취소"""
        if self.current_api_call:
            self.current_api_call.cancel()
            self.current_api_call = None
            self.logger.debug("API 호출 중단됨")

    def cleanup(self):
        """리소스 정리"""
        if self.loop:
            self.loop.stop()
            self.loop.close() 