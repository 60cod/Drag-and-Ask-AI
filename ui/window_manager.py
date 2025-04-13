import tkinter as tk
from tkinter import ttk

class AIButton:
    def __init__(self, root, on_click, logger):
        self.logger = logger
        self.window = tk.Toplevel(root)
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)
        self.window.configure(bg='white')
        
        # AI 버튼 생성 (테두리 없는 최소 크기)
        style = ttk.Style()
        style.configure('AI.TButton', padding=2)
        self.button = ttk.Button(
            self.window,
            text="AI",
            style='AI.TButton',
            command=on_click
        )
        self.button.pack(padx=0, pady=0)
        
        self.window.withdraw()
    
    def show(self, x, y):
        """버튼을 지정된 위치에 표시"""
        self.window.geometry(f"+{x}+{y}")
        self.window.deiconify()
        self.window.lift()
        self.window.update()
        self.logger.debug(f"AI 버튼 표시됨: 위치 ({x}, {y})")
    
    def hide(self):
        """버튼 숨기기"""
        self.window.withdraw()
    
    def is_visible(self):
        """버튼이 현재 표시되어 있는지 확인"""
        return self.window.winfo_ismapped()
    
    def get_position(self):
        """버튼의 현재 위치 반환"""
        return self.window.winfo_x(), self.window.winfo_y()
    
    def get_size(self):
        """버튼의 크기 반환"""
        return self.window.winfo_width(), self.window.winfo_height()

class AIPopup:
    def __init__(self, root, logger):
        self.logger = logger
        self.window = tk.Toplevel(root)
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)
        self.window.configure(bg='white')
        
        # 답변 창 테두리 설정
        self.frame = tk.Frame(
            self.window,
            bg='white',
            highlightbackground='#E5E5E5',  # 연한 회색 테두리
            highlightthickness=1
        )
        self.frame.pack(fill='both', expand=True)
        
        # 상단 프레임 (닫기 버튼용)
        self.top_frame = tk.Frame(self.frame, bg='white')
        self.top_frame.pack(fill='x', padx=8, pady=(2,0))
        
        # 닫기 버튼
        self.close_button = tk.Label(
            self.top_frame,
            text='×',
            bg='white',
            fg='black',
            font=('맑은 고딕', 12, 'bold'),
            cursor='hand2'
        )
        self.close_button.pack(side='right')
        
        # 답변 표시를 위한 스크롤 가능한 프레임
        self.scroll_frame = tk.Frame(self.frame, bg='white')
        self.scroll_frame.pack(fill='both', expand=True, padx=8, pady=(2,8))
        
        # 스크롤바 생성
        self.scrollbar = ttk.Scrollbar(self.scroll_frame)
        
        # 텍스트 위젯 생성 (스크롤 가능)
        self.answer_text = tk.Text(
            self.scroll_frame,
            wrap='word',
            font=('맑은 고딕', 9),
            bg='white',
            fg='black',
            relief='flat',
            cursor='arrow',  # 텍스트 커서 대신 기본 커서 사용
            padx=5,
            pady=1
        )
        self.answer_text.pack(side='left', fill='both', expand=True)
        
        # 스크롤바와 텍스트 위젯 연결
        self.answer_text.config(yscrollcommand=self._on_scroll)
        self.scrollbar.config(command=self.answer_text.yview)
        
        # 텍스트 위젯을 읽기 전용으로 설정
        self.answer_text.config(state='disabled')
        
        # 마우스 휠 이벤트 바인딩
        self.answer_text.bind('<MouseWheel>', self._on_mousewheel)
        self.answer_text.bind('<Button-4>', self._on_mousewheel)  # Linux
        self.answer_text.bind('<Button-5>', self._on_mousewheel)  # Linux
        
        self.window.withdraw()
    
    def _on_scroll(self, *args):
        """스크롤 이벤트 처리 및 스크롤바 표시/숨김"""
        self.scrollbar.set(*args)
        
        # 스크롤이 필요한지 확인
        if float(args[1]) < 1:  # 내용이 창보다 클 경우
            self.scrollbar.pack(side='right', fill='y')
        else:  # 내용이 창보다 작을 경우
            self.scrollbar.pack_forget()
    
    def _on_mousewheel(self, event):
        """마우스 휠 이벤트 처리"""
        if event.num == 5 or event.delta < 0:  # 아래로 스크롤
            self.answer_text.yview_scroll(1, 'units')
        elif event.num == 4 or event.delta > 0:  # 위로 스크롤
            self.answer_text.yview_scroll(-1, 'units')
        return 'break'  # 이벤트 전파 중단
    
    def set_close_callback(self, callback):
        """닫기 버튼 콜백 설정"""
        self.close_button.bind('<Button-1>', lambda e: callback())
    
    def show(self, x, y, text):
        """답변 창을 지정된 위치에 표시"""
        try:
            # 텍스트 업데이트
            self.answer_text.config(state='normal')
            self.answer_text.delete('1.0', tk.END)
            self.answer_text.insert('1.0', text)
            self.answer_text.config(state='disabled')
            
            # 스크롤을 맨 위로
            self.answer_text.yview_moveto(0)
            
            # 임시로 창을 표시하여 텍스트 높이 계산
            self.window.geometry("400x1000")  # 충분히 큰 높이로 설정
            self.window.update_idletasks()
            
            # 텍스트 높이 계산 (줄 수 * 줄 높이 + 여백)
            line_count = int(self.answer_text.index('end-1c').split('.')[0])
            line_height = self.answer_text.winfo_reqheight() / line_count if line_count > 0 else 20
            text_height = line_count * line_height + 200  # 상하 여백 포함
            
            # 최소 225px, 최대 400px로 제한
            # window_height = min(max(225, int(text_height)), 400)
            window_height = 250
            
            # 최종 창 크기 및 위치 설정
            self.window.geometry(f"400x{window_height}+{x}+{y}")
            self.window.deiconify()
            self.window.lift()
            self.window.update()
            self.logger.info(f"AI 답변 창 표시됨: 위치 ({x}, {y})")
        except Exception as e:
            self.logger.error(f"AI 답변 창 표시 오류: {str(e)}")
    
    def hide(self):
        """답변 창 숨기기"""
        self.window.withdraw()
        self.logger.debug("AI 답변 창 숨김")
    
    def is_visible(self):
        """답변 창이 현재 표시되어 있는지 확인"""
        return self.window.winfo_ismapped()
    
    def get_position(self):
        """답변 창의 현재 위치 반환"""
        return self.window.winfo_x(), self.window.winfo_y()
    
    def get_size(self):
        """답변 창의 크기 반환"""
        return self.window.winfo_width(), self.window.winfo_height() 