import tkinter as tk
from tkinter import messagebox
from GeometrySolverFrame import GeometrySolverFrame
class MainMenuFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#FFE5E5")
        
        # Header
        header_frame = tk.Frame(self, bg="#FFB6C1", height=80)
        header_frame.pack(fill="x", pady=10)
        
        tk.Label(header_frame, 
                text="🌟 Vui Học Hình Học 🌟",
                font=("Comic Sans MS", 24, "bold"),
                bg="#FFB6C1",
                fg="#444444").pack(pady=15)
        
        # Main content area
        content_frame = tk.Frame(self, bg="#FFE5E5")
        content_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Buttons frame
        buttons_frame = tk.Frame(content_frame, bg="#FFE5E5")
        buttons_frame.pack(pady=20)


        shapes = [
            ("🟥 Hình Vuông", "square"),
            ("📐 Hình Tam Giác", "triangle"),
            ("▉ Hình Chữ Nhật", "rectangle")
        ]
        
        for text, shape_type in shapes:
            btn = tk.Button(buttons_frame,
                          text=text,
                          font=("Comic Sans MS", 14),
                          command=lambda s=shape_type: controller.show_geometry_solver(s),
                          bg="#FF99CC",
                          fg="white",
                          width=15,
                          height=2)
            btn.pack(pady=15, padx=20)
        
        # Score display
        self.score_label = tk.Label(content_frame,
                                  text="⭐ Điểm: 0",
                                  font=("Comic Sans MS", 16),
                                  bg="#FFE5E5")
        self.score_label.pack(pady=10)
        
        # Help button
        help_btn = tk.Button(self,
                           text="❓ Trợ giúp",
                           font=("Comic Sans MS", 12),
                           command=self.show_help,
                           bg="#87CEEB")
        help_btn.pack(pady=5)
    
    def show_help(self):
        help_text = """
        🌟 Hướng dẫn sử dụng 🌟
        
        1. Chọn một hình học bạn muốn học
        2. Nhập bài toán và chọn yêu cầu cần tìm
        3. Nhấn "Phân tích bài toán" để xem lời giải
        4. Sử dụng nút "Quay lại" để trở về menu chính """
        messagebox.showinfo("Hướng dẫn 📖", help_text)