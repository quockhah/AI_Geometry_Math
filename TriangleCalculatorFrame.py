import tkinter as tk
from tkinter import messagebox
import math
from BaseCalculatorFrame import BaseCalculatorFrame



class TriangleCalculatorFrame(BaseCalculatorFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        tk.Label(self, 
                text="📐 Tính toán Hình Tam Giác",
                font=("Comic Sans MS", 20, "bold"),
                bg="#F0F8FF").pack(pady=10)
        
        # Draw triangle
        self.canvas.create_polygon(200, 50, 50, 250, 350, 250,
                                 outline="black", fill="white", width=2)
        self.canvas.create_text(200, 30, text="A", font=("Arial", 12, "bold"))
        self.canvas.create_text(30, 250, text="B", font=("Arial", 12, "bold"))
        self.canvas.create_text(370, 250, text="C", font=("Arial", 12, "bold"))
        
        # Input frame
        input_frame = tk.LabelFrame(self, text="Nhập số liệu",
                                  font=("Arial", 12, "bold"),
                                  bg="#F0F8FF")
        input_frame.pack(pady=20, padx=20)
        
        # Cạnh
        tk.Label(input_frame, text="Cạnh a:", font=("Arial", 11),
                bg="#F0F8FF").grid(row=0, column=0, padx=5, pady=5)
        self.side_a = tk.Entry(input_frame, font=("Arial", 11))
        self.side_a.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="Cạnh b:", font=("Arial", 11),
                bg="#F0F8FF").grid(row=1, column=0, padx=5, pady=5)
        self.side_b = tk.Entry(input_frame, font=("Arial", 11))
        self.side_b.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="Cạnh c:", font=("Arial", 11),
                bg="#F0F8FF").grid(row=2, column=0, padx=5, pady=5)
        self.side_c = tk.Entry(input_frame, font=("Arial", 11))
        self.side_c.grid(row=2, column=1, padx=5, pady=5)
        
        # Calculate button
        tk.Button(input_frame,
                 text="Tính toán",
                 command=self.calculate,
                 font=("Arial", 11),
                 bg="#4CAF50",
                 fg="white").grid(row=3, column=0, columnspan=2, pady=10)
        
        # Result frame
        self.result_frame = tk.LabelFrame(self, text="Kết quả",
                                        font=("Arial", 12, "bold"),
                                        bg="#F0F8FF")
        self.result_frame.pack(pady=20, padx=20, fill="x")
        
        self.result_text = tk.Text(self.result_frame, height=6,
                                 font=("Arial", 11), wrap=tk.WORD)
        self.result_text.pack(pady=10, padx=10, fill="x")
    
    def calculate(self):
        try:
            a = float(self.side_a.get())
            b = float(self.side_b.get())
            c = float(self.side_c.get())
            
            # Kiểm tra điều kiện tam giác
            if a + b <= c or b + c <= a or a + c <= b:
                raise ValueError("Ba cạnh không tạo thành tam giác!")
            
            # Tính nửa chu vi
            s = (a + b + c) / 2
            
            # Tính diện tích theo công thức Heron
            area = math.sqrt(s * (s - a) * (s - b) * (s - c))
            
            # Tính chu vi
            perimeter = a + b + c
            
            result = f"Diện tích: {area:.2f}\n"
            result += f"Chu vi: {perimeter:.2f}\n"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, result)
            
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))
    
    def switch_to_ai_solver(self):
        self.controller.show_geometry_solver("triangle")

class RectangleCalculatorFrame(BaseCalculatorFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        tk.Label(self, 
                text="▭ Tính toán Hình Chữ Nhật",
                font=("Comic Sans MS", 30, "bold"),
                bg="#F0F8FF").pack(pady=10)
        
        # Draw rectangle
        self.canvas.create_rectangle(50, 50, 350, 200, width=2)
        self.canvas.create_text(200,15, text="Chiều dài (d)",
                              font=("Arial", 10))
        self.canvas.create_text(30, 125, text="Chiều rộng (r)",
                              font=("Arial", 10))
        
        # Input frame
        input_frame = tk.LabelFrame(self, text="Nhập số liệu",
                                  font=("Arial", 12, "bold"),
                                  bg="#F0F8FF")
        input_frame.pack(pady=20, padx=20)
        
        tk.Label(input_frame, text="Chiều dài:",
                font=("Arial", 11), bg="#F0F8FF").grid(row=0, column=0, padx=5, pady=5)
        self.length_entry = tk.Entry(input_frame, font=("Arial", 11))
        self.length_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="Chiều rộng:",
                font=("Arial", 11), bg="#F0F8FF").grid(row=1, column=0, padx=5, pady=5)
        self.width_entry = tk.Entry(input_frame, font=("Arial", 11))
        self.width_entry.grid(row=1, column=1, padx=5, pady=5)
        
                # Calculate button
        tk.Button(input_frame,
                 text="Tính toán",
                 command=self.calculate,
                 font=("Arial", 11),
                 bg="#4CAF50",
                 fg="white").grid(row=3, column=0, columnspan=2, pady=10)
        
        # Result frame
        self.result_frame = tk.LabelFrame(self, text="Kết quả",
                                        font=("Arial", 12, "bold"),
                                        bg="#F0F8FF")
        self.result_frame.pack(pady=20, padx=20, fill="x")
        
        self.result_text = tk.Text(self.result_frame, height=6,
                                 font=("Arial", 11), wrap=tk.WORD)
        self.result_text.pack(pady=10, padx=10, fill="x")
    def calculate(self):
        try:
            length = float(self.length_entry.get())
            width = float(self.width_entry.get())
            area = length * width
            perimeter = 2 * (length + width)
            
            result = f"Diện tích: {area:.2f}\n"
            result += f"Chu vi: {perimeter:.2f}\n"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, result)
            
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ!")

    def switch_to_ai_solver(self):
        self.controller.show_geometry_solver("rectangle")

        
class SquareCalculatorFrame(BaseCalculatorFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        tk.Label(self, 
                text="🟥 Tính toán Hình Vuông",
                font=("Comic Sans MS", 20, "bold"),
                bg="#F0F8FF").pack(pady=10)
        
        # Draw square
        self.canvas.create_rectangle(100, 50, 300, 250, width=2)
        self.text_a = self.canvas.create_text(200, 30, text="a", font=("Arial", 12))
        
        # Input frame
        input_frame = tk.LabelFrame(self, text="Nhập số liệu",
                                  font=("Arial", 12, "bold"),
                                  bg="#F0F8FF")
        input_frame.pack(pady=20, padx=20)
        
        tk.Label(input_frame, text="Độ dài cạnh (a):",
                font=("Arial", 11), bg="#F0F8FF").grid(row=0, column=0, padx=5, pady=5)
        self.side_entry = tk.Entry(input_frame, font=("Arial", 11))
        self.side_entry.grid(row=0, column=1, padx=5, pady=5)
        self.side_entry.bind("<KeyRelease>", self.update_canvas)

        # Calculate button
        tk.Button(input_frame,
                 text="Tính toán",
                 command=self.calculate,
                 font=("Arial", 11),
                 bg="#4CAF50",
                 fg="white").grid(row=1, column=0, columnspan=2, pady=10)
        
        # Result frame
        self.result_frame = tk.LabelFrame(self, text="Kết quả",
                                        font=("Arial", 12, "bold"),
                                        bg="#F0F8FF")
        self.result_frame.pack(pady=20, padx=20, fill="x")
        
        self.result_text = tk.Text(self.result_frame, height=4,
                                 font=("Arial", 11), wrap=tk.WORD)
        self.result_text.pack(pady=10, padx=10, fill="x")
    def update_canvas(self, event): 
        try: 
            a = float(self.side_entry.get()) 
            self.canvas.itemconfig(self.text_a, fill="red") # Thay đổi màu văn bản thành đỏ khi nhập giá trị 
        except ValueError: 
            self.canvas.itemconfig(self.text_a, fill="black")
    def calculate(self):
        try:
            side = float(self.side_entry.get())
            area = side * side
            perimeter = 4 * side
            diagonal = side * math.sqrt(2)
            
            result = f"Diện tích: {area:.2f}\n"
            result += f"Chu vi: {perimeter:.2f}\n"
            result += f"Đường chéo: {diagonal:.2f}"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, result)
            
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ!")
    
    def switch_to_ai_solver(self):
        self.controller.show_geometry_solver("square")