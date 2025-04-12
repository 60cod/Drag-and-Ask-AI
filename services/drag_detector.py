import pyautogui
import keyboard
import mouse
import threading
import time
import asyncio
from typing import Callable

class DragDetector:
    def __init__(self, logger, on_drag_start: Callable, on_drag_end: Callable, on_click: Callable):
        self.logger = logger
        self.on_drag_start = on_drag_start
        self.on_drag_end = on_drag_end
        self.on_click = on_click
        
        # 마우스 위치 추적 변수
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.is_dragging = False
        self.has_moved = False
        
        # 마우스 이벤트 스레드 시작
        self.mouse_thread = threading.Thread(target=self._mouse_monitor)
        self.mouse_thread.daemon = True
        self.mouse_thread.start()
    
    def start_drag(self, *args):
        """드래그 시작 처리"""
        # Ctrl 키가 눌려있는지 확인
        if keyboard.is_pressed('ctrl'):
            current_x, current_y = pyautogui.position()
            self.drag_start_x = current_x
            self.drag_start_y = current_y
            self.is_dragging = True
            self.has_moved = False
            
            self.on_drag_start()
    
    def end_drag(self, *args):
        """드래그 종료 처리"""
        if not self.is_dragging:
            return

        if self.is_dragging and self.has_moved:
            current_x, current_y = pyautogui.position()
            self.on_drag_end(current_x, current_y)
        
        self.is_dragging = False
        self.has_moved = False
    
    def _mouse_monitor(self):
        """마우스 이동 모니터링"""
        while True:
            current_x, current_y = pyautogui.position()
            
            # 드래그 중일 때 이동 감지
            if self.is_dragging:
                if abs(current_x - self.drag_start_x) > 5 or abs(current_y - self.drag_start_y) > 5:
                    self.has_moved = True
            
            time.sleep(0.01)
    
    def setup_listeners(self):
        """마우스 이벤트 리스너 설정"""
        mouse.on_button(self.start_drag, buttons=('left',), types=('down',))
        mouse.on_button(self.end_drag, buttons=('left',), types=('up',))
        mouse.on_button(self.on_click, buttons=('left',), types=('down',)) 