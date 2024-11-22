import tkinter as tk
from tkinter import filedialog, messagebox

class SimpleNotepad:
    def __init__(self, root):
        self.root = root
        self.root.title("20812 신주원 memo")
        self.root.geometry("800x600")

        self.text_area = tk.Text(self.root, wrap="word", font=("consolas", 12))
        self.text_area.pack(expand=True, fill="both")

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.menu_bar = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="새 파일", command=self.new_file)
        self.menu_bar.add_cascade(label="열기", command=self.open_file)
        self.menu_bar.add_cascade(label="저장", command=self.save_file)
        self.menu_bar.add_cascade(label="다른 이름으로 저장", command=self.save_as_file)
        self.menu_bar.add_separator()
        self.menu_bar.add_cascade(label="종료", command=self.root.quit)
		self.current_file = None

    def new_file(self):
        """새 파일 만들기"""
        if self.confirm_unsaved_changes():
            self.text_area.delete("1.0", tk.END)
            self.current_file = None
            self.root.title("메모장 - 새 파일")

    def open_file(self):
        """파일 열기"""
        if not self.confirm_unsaved_changes():
            return

        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", content)
                self.current_file = file_path
                self.root.title(f"메모장 - {file_path}")
            except Exception as e:
                messagebox.showerror("오류", f"파일을 열 수 없습니다:\n{e}")

    def save_file(self):
        """현재 파일 저장"""
        if self.current_file:
            try:
                with open(self.current_file, "w", encoding="utf-8") as file:
                    file.write(self.text_area.get("1.0", tk.END).strip())
                messagebox.showinfo("저장 완료", "저장 완료")
            except Exception as e:
                messagebox.showerror("오류", f"오류\n{e}")
        else:
            self.save_as_file()

    def save_as_file(self):
        """다른 이름으로 저장"""
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.text_area.get("1.0", tk.END).strip())
                self.current_file = file_path
                self.root.title(f"메모장 - {file_path}")
                messagebox.showinfo("저장 완료", "저장 완료")
            except Exception as e:
                messagebox.showerror("오류", f"오류\n{e}")

    def confirm_unsaved_changes(self):
        """저장 아직 안함"""
        content = self.text_area.get("1.0", tk.END).strip()
        if content and (self.current_file is None or self.read_file(self.current_file) != content):
            response = messagebox.askyesnocancel("저장", "저장?")
            if response:  # Yes
                self.save_file()
            return response is not None  # Yes or No
        return True  # No changes or Cancel

    @staticmethod
    def read_file(file_path):
        """파일 불러오기"""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read().strip()
        except Exception:
            return ""

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleNotepad(root)
    root.mainloop()