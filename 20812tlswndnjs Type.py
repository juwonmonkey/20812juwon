import tkinter as tk
from tkinter import filedialog, messagebox
import time

class TypingPracticeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("20812 신주원 타자연습")
        self.root.geometry("600x400")
        
        self.text_to_type = ""
        self.start_time = None
        
        self.file_button = tk.Button(root, text="파일 열기", command=self.load_text_file)
        self.file_button.pack(pady=10)
        
        self.text_label = tk.Label(root, text="파일을 불러오세요", wraplength=580, font=("Arial", 14), justify="center")
        self.text_label.pack(pady=20)
        
        self.input_text = tk.Text(root, height=5, width=60, state="disabled", wrap="word")
        self.input_text.pack(pady=10)
        self.input_text.bind("<KeyRelease>", self.check_typing)
        
        self.result_label = tk.Label(root, text="", font=("Arial", 12), fg="green")
        self.result_label.pack(pady=20)

    def load_text_file(self):
        """메모장 파일로 문장 설정"""
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not file_path:
            return
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                self.text_to_type = file.read().strip()
                self.text_label.config(text=self.text_to_type)
                self.input_text.config(state="normal")
                self.input_text.delete("1.0", tk.END)
                self.start_time = None
                self.result_label.config(text="")
        except Exception as e:
            messagebox.showerror("오류", f"파일을 열 수 없습니다: {e}")

    def check_typing(self, event):
        """사용자 입력을 확인하고 결과를 계산"""
        if not self.text_to_type or not self.start_time:
            self.start_time = time.time()
        
        user_input = self.input_text.get("1.0", tk.END).strip()
        
        if user_input == self.text_to_type:
            self.input_text.config(state="disabled")
            elapsed_time = time.time() - self.start_time
            words_per_minute = len(self.text_to_type.split()) / (elapsed_time / 60)
            accuracy = sum(1 for a, b in zip(user_input, self.text_to_type) if a == b) / len(self.text_to_type) * 100
            
            self.result_label.config(
                text=f"완료! 시간: {elapsed_time:.2f}초, 속도: {words_per_minute:.2f} WPM, 정확도: {accuracy:.2f}%"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = TypingPracticeApp(root)
    root.mainloop()
