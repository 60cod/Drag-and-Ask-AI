import pyautogui
import keyboard
import mouse
import tkinter as tk
from tkinter import ttk
import threading
import time
import os
from dotenv import load_dotenv
import logging
from datetime import datetime
import sys
import win32clipboard
import win32con
import asyncio
from ai_service import AIService
from utils.logger import setup_logger
from services.clipboard_manager import ClipboardManager
from services.drag_detector import DragDetector
from ui.window_manager import AIButton, AIPopup

class AIAssistant:
    def __init__(self):
        # 로거 설정
        self.logger = setup_logger('AIAssistant')
        self.logger.info("프로그램 시작")
        
        # .env 파일에서 API 키 로드
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            self.logger.error("API 키를 찾을 수 없음")
            raise ValueError("OpenAI API 키가 설정되지 않았습니다. .env 파일을 확인해주세요.")
        
        # 이벤트 루프 설정
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        # 메인 윈도우 설정
        self.root = tk.Tk()
        self.root.withdraw()
        
        # 서비스 초기화
        self.ai_service = AIService(api_key)
        self.clipboard = ClipboardManager(self.logger)
        
        # UI 컴포넌트 초기화
        self.ai_button = AIButton(self.root, self.on_ai_button_click, self.logger)
        self.ai_popup = AIPopup(self.root, self.logger)
        self.ai_popup.set_close_callback(self.hide_popup)
        
        # 현재 진행 중인 API 호출
        self.current_api_call = None
        
        # 드래그 감지기 초기화
        self.drag_detector = DragDetector(
            self.logger,
            self.on_drag_start,
            self.on_drag_end,
            self.on_click
        )
        
        self.logger.info("초기화 완료")
    
    def on_drag_start(self):
        """드래그 시작 시 처리"""
        if self.ai_button.is_visible() or self.ai_popup.is_visible():
            return
        
        self.clipboard.save_current_content()
        self.ai_button.hide()
        self.ai_popup.hide()
    
    def on_drag_end(self, x, y):
        """드래그 종료 시 처리"""
        try:
            # 선택된 텍스트를 클립보드에 저장
            keyboard.send('ctrl+c')
            time.sleep(0.1)  # 복사가 완료될 때까지 잠시 대기
            
            # 드래그가 끝난 위치에 버튼 표시
            self.ai_button.show(x + 10, y + 10)
        except Exception as e:
            self.logger.error(f"드래그 종료 처리 오류: {str(e)}")
    
    def on_click(self, *args):
        """클릭 이벤트 처리"""
        if not (self.ai_button.is_visible() or self.ai_popup.is_visible()):
            return
        
        x, y = pyautogui.position()
        
        # 답변 창이 표시되어 있을 때
        if self.ai_popup.is_visible():
            popup_x, popup_y = self.ai_popup.get_position()
            popup_width, popup_height = self.ai_popup.get_size()
            
            # 클릭이 답변 창 영역 밖이면 창 닫기
            if not (popup_x <= x <= popup_x + popup_width and popup_y <= y <= popup_y + popup_height):
                self.hide_popup()
                self.logger.debug("AI 답변 창 숨김 (창 영역 밖 클릭)")
        
        # AI 버튼이 표시되어 있을 때
        elif self.ai_button.is_visible():
            btn_x, btn_y = self.ai_button.get_position()
            btn_width, btn_height = self.ai_button.get_size()
            
            # 클릭이 버튼 영역 밖이면 버튼 숨기기
            if not (btn_x <= x <= btn_x + btn_width and btn_y <= y <= btn_y + btn_height):
                self.ai_button.hide()
                self.clipboard.restore()  # 클립보드 원복
                self.logger.debug("AI 버튼 숨김 (버튼 영역 밖 클릭)")
    
    def on_ai_button_click(self):
        """AI 버튼 클릭 처리"""
        self.logger.info("AI 버튼 클릭됨")
        try:
            selected_text = self.clipboard.get_text()
            
            if selected_text.strip():
                # 버튼의 현재 위치 저장
                button_x, button_y = self.ai_button.get_position()
                self.logger.debug(f"버튼 위치: ({button_x}, {button_y})")
                
                # 버튼 숨기기
                self.ai_button.hide()
                
                # 클립보드 원복
                self.clipboard.restore()
                
                # 답변창에 로딩 메시지 표시
                self.ai_popup.show(button_x, button_y, "AI가 응답을 생성하는 중입니다...")
                
                # API 호출 및 응답 처리
                async def get_ai_response():
                    try:
                        response = await self.ai_service.get_response(selected_text)
                        # GUI 업데이트는 메인 스레드에서 실행
                        self.root.after(0, lambda: self.ai_popup.show(button_x, button_y, response))
                    except Exception as error:
                        error_msg = str(error)
                        self.logger.error(f"API 호출 중 오류 발생: {error_msg}")
                        # GUI 업데이트는 메인 스레드에서 실행
                        self.root.after(0, lambda: self.ai_popup.show(
                            button_x, 
                            button_y, 
                            "OpenAI API 호출 중 오류가 발생했습니다.\n잠시 후 다시 시도해주세요."
                        ))
                    finally:
                        self.current_api_call = None
                
                # 비동기 API 호출 실행
                self.current_api_call = asyncio.run_coroutine_threadsafe(get_ai_response(), self.loop)
            else:
                self.logger.warning("선택된 텍스트 없음")
                self.clipboard.restore()
        except Exception as e:
            self.logger.error(f"AI 버튼 클릭 처리 오류: {str(e)}")
            self.clipboard.restore()
    
    def hide_popup(self):
        """답변 창 숨기기"""
        # 현재 진행 중인 API 호출이 있다면 중단
        if self.current_api_call:
            self.current_api_call.cancel()
            self.current_api_call = None
            self.logger.debug("API 호출 중단됨")
        
        self.ai_popup.hide()
    
    def run(self):
        """프로그램 실행"""
        try:
            # 이벤트 루프 실행을 위한 스레드 시작
            def run_event_loop():
                self.loop.run_forever()
            
            loop_thread = threading.Thread(target=run_event_loop, daemon=True)
            loop_thread.start()
            
            # 마우스 이벤트 리스너 설정
            self.drag_detector.setup_listeners()
            
            self.logger.info("이벤트 리스너 설정 완료")
            self.root.mainloop()
        except Exception as e:
            self.logger.error(f"프로그램 실행 오류: {str(e)}")
        finally:
            self.loop.stop()
            self.loop.close()

if __name__ == "__main__":
    assistant = AIAssistant()
    assistant.run()
