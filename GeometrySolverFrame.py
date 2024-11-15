import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import openai
from MainMenuFrame import *
class GeometrySolverFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#F0F8FF")
        
        # Nút quay lại menu chính
        back_button = tk.Button(self,
                              text="↩ Quay lại Menu chính",
                              font=("Arial", 12),
                              command=lambda: controller.back_main(parent),
                              bg="#FF99CC",
                              fg="white")
        back_button.pack(pady=10, padx=10, anchor="nw")
        
        # Main frame
        self.main_frame = tk.Frame(self, bg="#F0F8FF")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Left panel (60% width)
        self.left_panel = tk.Frame(self.main_frame, bg="#F0F8FF")
        self.left_panel.pack(side="left", fill="both", expand=True, padx=10)
        
        # Right panel (40% width)
        self.right_panel = tk.Frame(self.main_frame, bg="#F0F8FF")
        self.right_panel.pack(side="right", fill="both", expand=False, padx=10)
        
        self.setup_shape_selector()
        self.setup_problem_input()
        self.setup_visualization()
        self.setup_calculation_display()
        self.setup_chatbot()

    def setup_shape_selector(self):
        # Shape selection frame
        shape_frame = tk.LabelFrame(self.left_panel, text="Chọn Hình", 
                                  font=("Arial", 12, "bold"), bg="#F0F8FF")
        shape_frame.pack(fill="x", pady=10)
        
        shapes = [("Hình Chữ Nhật", "rectangle"), 
                 ("Hình Tam Giác", "triangle"), 
                 ("Hình Vuông", "square")]
        
        self.shape_var = tk.StringVar()
        for text, value in shapes:
            rb = tk.Radiobutton(shape_frame, text=text, value=value,
                              variable=self.shape_var, font=("Arial", 11),
                              command=self.on_shape_select, bg="#F0F8FF")
            rb.pack(side="left", padx=20, pady=5)
            
    def setup_problem_input(self):
        # Frame nhập bài toán
        input_frame = tk.LabelFrame(self.left_panel, text="Nhập Bài Toán", 
                                  font=("Arial", 12, "bold"), bg="#F0F8FF")
        input_frame.pack(fill="x", pady=10)
        
        # Text area nhập đề bài
        self.problem_text = scrolledtext.ScrolledText(input_frame, 
                                                    height=4, width=50, 
                                                    font=("Arial", 11))
        self.problem_text.pack(pady=10, padx=10)
        
        # Frame chứa các nút yêu cầu tìm
        find_frame = tk.Frame(input_frame, bg="#F0F8FF")
        find_frame.pack(fill="x", pady=5)
        
        self.find_vars = {}
        self.setup_find_buttons(find_frame)
        
        # Nút phân tích
        analyze_btn = tk.Button(input_frame, text="Phân tích bài toán",
                              command=self.analyze_problem,
                              font=("Arial", 11, "bold"),
                              bg="#4CAF50", fg="white")
        analyze_btn.pack(pady=10)
        
    def setup_find_buttons(self, parent):
        # Dictionary lưu trữ các nút theo hình
        self.find_buttons = {
            "rectangle": [
                ("Diện tích", "area"),
                ("Chu vi", "perimeter"),
                ("Chiều dài", "length"),
                ("Chiều rộng", "width"),
                ("Đường chéo", "diagonal")
            ],
            "triangle": [
                ("Diện tích", "area"),
                ("Chu vi", "perimeter"),
                ("Độ dài các cạnh", "sides"),
                ("Các góc", "angles"),
                ("Đường cao", "height"),
                ("Trung tuyến", "median"),
                ("Trọng tâm", "centroid")
            ],
            "square": [
                ("Diện tích", "area"),
                ("Chu vi", "perimeter"),
                ("Độ dài cạnh", "side"),
                ("Đường chéo", "diagonal")
            ]
        }
        
        # Ẩn tất cả buttons ban đầu
        self.current_find_frame = tk.Frame(parent, bg="#F0F8FF")
        self.current_find_frame.pack(fill="x")
        
    def setup_visualization(self):
        # Frame hiển thị hình
        visual_frame = tk.LabelFrame(self.right_panel, text="Hình ảnh minh họa",
                                   font=("Arial", 12, "bold"), bg="#F0F8FF")
        visual_frame.pack(fill="both", expand=True, pady=10)
        
        # Canvas để vẽ hình
        self.canvas = tk.Canvas(visual_frame, width=400, height=300,
                              bg="white", highlightthickness=1)
        self.canvas.pack(pady=10, padx=10)
        
    def setup_calculation_display(self):
        # Frame hiển thị các bước tính
        calc_frame = tk.LabelFrame(self.left_panel, text="Các bước giải",
                                 font=("Arial", 12, "bold"), bg="#F0F8FF")
        calc_frame.pack(fill="both", expand=True, pady=10)
        
        self.calc_text = scrolledtext.ScrolledText(calc_frame, height=10,
                                                 font=("Arial", 11))
        self.calc_text.pack(pady=10, padx=10, fill="both", expand=True)
        
    def setup_chatbot(self):
        # Frame chatbot
        chat_frame = tk.LabelFrame(self.right_panel, text="AI Assistant",
                                 font=("Arial", 12, "bold"), bg="#F0F8FF")
        chat_frame.pack(fill="both", expand=True, pady=10)
        
        # Hiển thị chat
        self.chat_display = scrolledtext.ScrolledText(chat_frame, height=8,
                                                    font=("Arial", 11))
        self.chat_display.pack(pady=5, padx=10, fill="both", expand=True)
        
        # Frame nhập câu hỏi
        input_frame = tk.Frame(chat_frame, bg="#F0F8FF")
        input_frame.pack(fill="x", padx=10, pady=5)
        
        self.chat_entry = tk.Entry(input_frame, font=("Arial", 11))
        self.chat_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        send_btn = tk.Button(input_frame, text="Gửi",
                           command=self.send_question,
                           font=("Arial", 11))
        send_btn.pack(side="right")
        
    def on_shape_select(self):
        # Xóa các nút find cũ
        for widget in self.current_find_frame.winfo_children():
            widget.destroy()
            
        shape = self.shape_var.get()
        if shape in self.find_buttons:
            for text, value in self.find_buttons[shape]:
                var = tk.BooleanVar()
                self.find_vars[value] = var
                cb = tk.Checkbutton(self.current_find_frame, text=text,
                                  variable=var, font=("Arial", 11),
                                  bg="#F0F8FF")
                cb.pack(side="left", padx=10)
                
        self.draw_shape(shape)
        
    def draw_shape(self, shape):
        self.canvas.delete("all")
        if shape == "rectangle":
            self.canvas.create_rectangle(50, 50, 350, 200, width=2)
            # Thêm nhãn kích thước
            self.canvas.create_text(200, 30, text="Chiều dài (d)",
                                  font=("Arial", 10))
            self.canvas.create_text(30, 125, text="Chiều rộng (r)",
                                  font=("Arial", 10))
        elif shape == "triangle":
            self.canvas.create_polygon(200, 50, 50, 250, 350, 250,
                                     outline="black", fill="", width=2)
            # Thêm nhãn góc và cạnh
            self.canvas.create_text(200, 30, text="A",
                                  font=("Arial", 12, "bold"))
            self.canvas.create_text(30, 250, text="B",
                                  font=("Arial", 12, "bold"))
            self.canvas.create_text(370, 250, text="C",
                                  font=("Arial", 12, "bold"))
        elif shape == "square":
            self.canvas.create_rectangle(100, 50, 300, 250, width=2)
            self.canvas.create_text(200, 30, text="a", font=("Arial", 12))
            
    def analyze_problem(self):
        problem_text = self.problem_text.get("1.0", "end-1c")
        shape = self.shape_var.get()
        find_items = [k for k, v in self.find_vars.items() if v.get()]
        
        # Tạo prompt cho GPT
        prompt = self.create_ai_prompt(problem_text, shape, find_items)
        
        try:
            # Gọi OpenAI API
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=500,
                temperature=0.7
            )
            
            # Xử lý kết quả
            solution = response.choices[0].text.strip()
            self.display_solution(solution)
            
        except Exception as e:
            messagebox.showerror("Lỗi",
                               "Có lỗi xảy ra khi phân tích bài toán: " + str(e))
            
    def create_ai_prompt(self, problem, shape, find_items):
        prompt = f"""Hãy giải bài toán hình học sau:
        Hình: {shape}
        Đề bài: {problem}
        Yêu cầu tìm: {', '.join(find_items)}
        
        Hãy giải theo các bước sau:
        1. Phân tích đề bài
        2. Liệt kê dữ kiện đã cho
        3. Xác định công thức cần dùng
        4. Giải từng bước
        5. Kết luận
        
        Trình bày chi tiết từng bước và giải thích rõ ràng."""
        
        return prompt
        
    def display_solution(self, solution):
        # Xóa nội dung cũ
        self.calc_text.delete("1.0", "end")
        
        # Hiển thị lời giải mới
        self.calc_text.insert("1.0", solution)
        
        # Tự động cuộn xuống đầu
        self.calc_text.see("1.0")
        
    def send_question(self):
        question = self.chat_entry.get()
        if question.strip():
            # Hiển thị câu hỏi
            self.chat_display.insert("end", f"Bạn: {question}\n")
            
            try:
                # Tạo prompt cho câu hỏi
                prompt = f"""Học sinh hỏi về bài toán hình học: {question}
                Hãy giải thích ngắn gọn, dễ hiểu và thân thiện."""
                
                # Gọi OpenAI API
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=prompt,
                    max_tokens=200,
                    temperature=0.7
                )
                
                # Hiển thị câu trả lời
                answer = response.choices[0].text.strip()
                self.chat_display.insert("end", f"AI: {answer}\n\n")
                
                # Cuộn xuống cuối
                self.chat_display.see("end")
                
            except Exception as e:
                self.chat_display.insert("end",
                                       "AI: Xin lỗi, tôi không thể trả lời " +
                                       "lúc này. Vui lòng thử lại sau.\n\n")
                
            # Xóa nội dung đã nhập
            self.chat_entry.delete(0, "end")
    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()
    