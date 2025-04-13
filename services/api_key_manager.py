import tkinter as tk
from tkinter import ttk, messagebox
import os
from dotenv import load_dotenv

class APIKeyManager:
    @staticmethod
    def get_api_key():
        root = tk.Tk()
        root.title("OpenAI API 키 입력")
        root.geometry("600x190")
        
        # 메인 프레임 생성 (여백을 위해)
        main_frame = ttk.Frame(root, padding="20 10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        label = ttk.Label(main_frame, text="OpenAI API 키를 입력해주세요:")
        label.pack(pady=10)
        
        # 입력창을 담을 프레임
        entry_frame = ttk.Frame(main_frame)
        entry_frame.pack(fill=tk.X, padx=20, pady=10)
        
        api_key_var = tk.StringVar(value='')
        entry = ttk.Entry(entry_frame, textvariable=api_key_var, width=40)
        entry.pack(fill=tk.X)
        
        result_key = None
        
        def save_api_key():
            nonlocal result_key
            api_key = api_key_var.get().strip()
            if api_key:
                try:
                    # .env 파일이 없으면 생성
                    if not os.path.exists('.env'):
                        with open('.env', 'w', encoding='utf-8') as f:
                            f.write('OPENAI_API_KEY=\n')
                    
                    # .env 파일 읽기
                    with open('.env', 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    # API 키 라인 찾아서 수정 또는 추가
                    key_found = False
                    new_lines = []
                    for line in lines:
                        if line.strip().startswith('OPENAI_API_KEY='):
                            new_lines.append(f'OPENAI_API_KEY={api_key}\n')
                            key_found = True
                        else:
                            new_lines.append(line)
                    
                    if not key_found:
                        new_lines.append(f'OPENAI_API_KEY={api_key}\n')
                    
                    # 수정된 내용 저장
                    with open('.env', 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)
                    
                    # 환경 변수 업데이트
                    os.environ['OPENAI_API_KEY'] = api_key
                    result_key = api_key
                    
                    # 성공 메시지를 표시하고 자동으로 닫히도록 설정
                    success_window = tk.Toplevel(root)
                    success_window.withdraw()
                    success_window.after(1500, success_window.destroy)
                    messagebox.showinfo("성공", "OpenAI API 키가 정상적으로 저장되었습니다.", parent=success_window)
                    root.destroy()
                except Exception as e:
                    tk.messagebox.showerror("오류", f"API 키 저장 중 오류가 발생했습니다: {str(e)}")
                    clear_api_key()
                    root.destroy()
            else:
                tk.messagebox.showerror("오류", "API 키를 입력해주세요.")
        
        def clear_api_key():
            try:
                if os.path.exists('.env'):
                    with open('.env', 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    # API 키 라인 찾아서 초기화
                    new_lines = []
                    for line in lines:
                        if line.strip().startswith('OPENAI_API_KEY='):
                            new_lines.append('OPENAI_API_KEY=\n')
                        else:
                            new_lines.append(line)
                    
                    with open('.env', 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)
                    
                    # 환경 변수도 초기화
                    if 'OPENAI_API_KEY' in os.environ:
                        del os.environ['OPENAI_API_KEY']
            except Exception as e:
                print(f"API 키 초기화 중 오류 발생: {str(e)}")
        
        def on_closing():
            nonlocal result_key
            if not result_key:
                clear_api_key()
                tk.messagebox.showerror("오류", "OpenAI API 키가 설정되지 않았습니다.")
            root.destroy()
            
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # 저장 버튼을 담을 프레임
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, padx=220, pady=10)
        
        style = ttk.Style()
        style.configure('Tall.TButton', padding=6)  # 버튼 높이 증가
        
        save_button = ttk.Button(button_frame, text="저장", command=save_api_key, style='Tall.TButton')
        save_button.pack(fill=tk.X)
        
        # 창을 화면 중앙에 위치
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')
        
        root.mainloop()
        
        # 입력창이 닫힌 후 환경 변수 다시 확인
        load_dotenv()
        return os.getenv('OPENAI_API_KEY') 