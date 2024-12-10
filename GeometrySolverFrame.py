import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from MainMenuFrame import *
import json
import os
from datetime import datetime
import re
from SolveSquare import *
from SolveRectangle import *
class GeometrySolverFrame(tk.Frame):
    def __init__(self, parent, controller):
        """_summary_

        Arguments:
            parent -- _description_ --khung cha.
            controller -- _description_ --controller -- đối tượng điều khiển để chuyển đổi giữa các màn hình.
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#F0F8FF")
        self.COLOR_MAP = {
            "đỏ": "red", 
            "xanh": "blue", 
            "xanh lá": "green", 
            "vàng": "yellow", 
            "cam": "orange", 
            "tím": "purple", 
            "hồng": "pink",
            "nâu": "brown",
            "trắng": "white",
            "đen": "black"
        }

        back_button = tk.Button(self,text="↩ Quay lại Menu chính",font=("Arial", 12),
                                command=lambda: controller.back_main(parent),bg="#FF99CC",fg="white")
        back_button.pack(pady=10, padx=10, anchor="nw")

        self.main_frame = tk.Frame(self, bg="#F0F8FF")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.left_panel = tk.Frame(self.main_frame, bg="#F0F8FF")
        self.left_panel.pack(side="left", fill="both", expand=True, padx=10)

        self.right_panel = tk.Frame(self.main_frame, bg="#F0F8FF")
        self.right_panel.pack(side="right", fill="both", expand=False, padx=10)

        self.setup_shape_selector()
        self.setup_problem_input()
        self.setup_visualization()
        self.setup_calculation_display()
        self.setup_note()

    #Tạo giao diện để người dùng chọn loại hình học (ví dụ: hình vuông, hình tam giác, hình chữ nhật).
    def setup_shape_selector(self):

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

    #Tạo giao diện để người dùng nhập bài toán
    def setup_problem_input(self):

        input_frame = tk.LabelFrame(self.left_panel, text="Nhập Bài Toán",font=("Arial", 12, "bold"), bg="#F0F8FF")
        input_frame.pack(fill="x", pady=10)
        self.problem_text = scrolledtext.ScrolledText(input_frame,height=8, width=75,font=("Arial", 11))
        self.problem_text.pack(pady=10, padx=10)

        analyze_btn = tk.Button(input_frame, text="Giải bài toán",command=self.save_problem_to_json,font=("Arial", 11, "bold"),bg="#4CAF50", fg="white")
        analyze_btn.pack(pady=10)

    #Lưu nội dung bài toán vào tệp JSON để xử lý và hiển thị lại khi cần
    def save_problem_to_json(self):

        problem_text = self.problem_text.get("1.0", "end-1c").strip()
        shape = self.shape_var.get()

        if not problem_text:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập bài toán!")
            return

        semantic_data = self.parse_problem_semantics(problem_text, shape)
        if semantic_data is None:
            return
        self.draw_shape(shape, problem_text)

        problem_data = {
            "problem_text": problem_text,
            "shape": shape,
            "semantic_analysis": semantic_data,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        os.makedirs("problem_data", exist_ok=True)

        filename = f"problem_data/problem_data.json"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(problem_data, f, ensure_ascii=False, indent=4)
            
            self.current_problem_file = filename
            
            
            self.calc_text.delete('1.0', tk.END)
            self.calc_text.insert(tk.END, "Phân tích:\n")
            semantic_analysis = problem_data.get("semantic_analysis", {})
            known_factors = semantic_analysis.get("known_factors", {})
            calculations = semantic_analysis.get("calculations", [])
            shape_cal=problem_data.get('shape')

            known_factors_str = ", ".join(f"{key}={value}" for key, value in known_factors.items())
            calculations_str = ", ".join(calculations)
            solution=None

            if shape_cal=="square":
                square=Square(problem_data)
                square.solve()
                solution=square.get_solution_steps()
            elif shape_cal=="rectangle":
                rectangle=Rectangle(problem_data)
                rectangle.solve()
                solution=rectangle.get_solution_steps()
            self.calc_text.insert(tk.END, f"Các yếu tố đã biết: {known_factors_str}\n")
            self.calc_text.insert(tk.END, f"Yêu cầu: tính {calculations_str}\n")
            self.calc_text.insert(tk.END, f"Giải \n: {solution}")

     
            self.load_and_update_visualization()
        except TypeError as e:
            messagebox.showerror("Lỗi", f"Không đủ dữ liệu để tính toán")
        except Exception as e:
            messagebox.showerror("Lỗi", f"{e}")

    def validate_shape_in_text(self,text,shape):
        shapes = [("Hình Chữ Nhật", "rectangle"),
                  ("Hình Tam Giác", "triangle"),
                  ("Hình Vuông", "square")]
        for vietnamese, english in shapes:
            if vietnamese.lower() in text.lower():
                shape_in_text= english  # Trả về loại hình bằng tiếng Anh
        res=None
        if shape_in_text==shape:
            return True
        else: return False

    #Hàm này sẽ phân tích ngữ nghĩa bài toán để trích xuất thông tin cần thiết.
    def parse_problem_semantics(self, problem_text, shape):
        """
        Analyze the semantics of a geometry problem to extract essential information.

        Arguments:
            problem_text -- The content of the problem, provided as a string.
            shape -- The type of geometric shape (e.g., square, triangle, rectangle).

        Returns:
            semantic_data -- A dictionary containing extracted semantic information, including:
                - Related entities.
                - Dimensional information.
                - Color instructions (if applicable).
                - Given values (e.g., numbers with units).
        """
        def data_preprocessing(text):
            text = re.sub(r'\b(bằng)\b', '=', text.lower(), flags=re.IGNORECASE)
            text = re.sub(r'\b(là)\b', '=', text.lower(), flags=re.IGNORECASE)
            text = re.sub(r'\s+', ' ', text).strip()
            return text
        
        # Hàm trích xuất các thông tin đã biết
        def extract_given_info(text, shape):
            known_factors = {}
            patterns = {}
            # Mẫu nhận diện theo từng loại hình học
            if shape == "square":
                patterns = {
                    "side": r"cạnh\s*=\s*([a-zA-Z0-9=+\-*/]+\s*(cm|m|mm|km)?)",
                    "chu vi": r"chu vi\s*=\s*([a-zA-Z0-9=+\-*/]+\s*(cm|m|mm|km)?)",
                    "diện tích": r"diện tích\s*=\s*([a-zA-Z0-9=+\-*/]+\s*(cm²|m²|mm²|km²)?)",
                    "đường chéo": r"đường chéo\s*=\s*([a-zA-Z0-9=+\-*/]+\s*(cm|m|mm|km)?)"
                }
            elif shape == "triangle":
                patterns = {
                    "a": r"cạnh a\s*=\s*([a-zA-Z0-9+\-*/]+\s*(cm|m|mm|km)?)",
                    "b": r"cạnh b\s*=\s*([a-zA-Z0-9+\-*/]+\s*(cm|m|mm|km)?)",
                    "c": r"cạnh c\s*=\s*([a-zA-Z0-9+\-*/]+\s*(cm|m|mm|km)?)",
                    "chu vi": r"chu vi\s*=\s*([a-zA-Z0-9=+\-*/]+\s*(cm|m|mm|km)?)",
                    "diện tích": r"diện tích\s*=\s*([a-zA-Z0-9=+\-*/]+\s*(cm²|m²|mm²|km²)?)",
                    "đường cao": r"đường cao\s*=\s*([a-zA-Z0-9=+\-*/]+\s*(cm|m|mm|km)?)"
                }
            elif shape == "rectangle":
                patterns = {
                    "chiều dài": r"chiều dài\s*=\s*([a-zA-Z0-9=+\-*/]+\s*(cm|m|mm|km)?)",
                    "chiều rộng": r"chiều rộng\s*=\s*([a-zA-Z0-9=+\-*/]+\s*(cm|m|mm|km)?)",
                    "chu vi": r"chu vi\s*=\s*([a-zA-Z0-9=+\-*/]+\s*(cm|m|mm|km)?)",
                    "diện tích": r"diện tích\s*=\s*([a-zA-Z0-9=+\-*/]+\s*(cm²|m²|mm²|km²)?)",
                    "đường chéo": r"đường chéo\s*=\s*([a-zA-Z0-9=+\-*/]+\s*(cm|m|mm|km)?)"
                }
            # Áp dụng các biểu thức regex
            for key, pattern in patterns.items():
                match = re.search(pattern, text)
                if match:
                    known_factors[key] = match.group(1)
            return known_factors

        # Hàm trích xuất các yêu cầu cần tính
        def extract_calculations(text):
            calculations = []
            if shape == "square":
                keywords = ["cạnh", "chu vi", "diện tích", "đường chéo"]
            elif shape == "triangle":
                keywords = ["cạnh a", "cạnh b", "cạnh c", "chu vi", "diện tích", "đường cao"]
            elif shape == "rectangle":
                keywords = ["chiều dài", "chiều rộng", "chu vi", "diện tích", "đường chéo"]
            for keyword in keywords:
                if keyword in text:
                    calculations.append(keyword)
            return calculations

        semantic_data = {}
        problem_text=data_preprocessing(problem_text)

        numbers = re.findall(r'\d+(?:\.\d+)?', problem_text)
        
        is_shape=self.validate_shape_in_text(problem_text,shape)
        if is_shape==False:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập bài toán đúng với hình đã chọn")
            return
        # color_instructions = self.extract_color_instructions(problem_text)
        # semantic_data["color_instructions"] = color_instructions

        if shape == "triangle" or shape == "rectangle" or shape == "square":
            given_part = ""
            calculate_part = ""

            if "cho" in problem_text:
                given_part = problem_text.split("cho", 1)[1].strip()
                if "tính" in given_part:
                    given_part, calculate_part = given_part.split("tính", 1)

            
            

           
            

            # Xử lý thông tin
            known_factors = extract_given_info(given_part,shape)
            calculations = extract_calculations(calculate_part)
            semantic_data["shape"]=shape
            semantic_data["known_factors"]= known_factors
            semantic_data["calculations"]= calculations


        return semantic_data
    
    def extract_color_instructions(self, problem_text):
        """_summary_

        Arguments:
            problem_text -- _description_ -- nội dung bài toán.

        Returns:
            _description_ -- từ điển chứa các yếu tố hình học và màu sắc tương ứng.
        """
        color_instructions = {}
        
        shape_elements = {
            "triangle": {
                "cạnh a": ["side_a", "a"],
                "cạnh b": ["side_b", "b"],
                "cạnh c": ["side_c", "c"],
                "góc α": ["angle_alpha"],
                "góc β": ["angle_beta"],
                "góc γ": ["angle_gamma"]
            },
            "rectangle": {
                "chiều dài": ["length", "d"],
                "chiều rộng": ["width", "r"]
            },
            "square": {
                "cạnh": ["side", "a"]
            }
        }

        for color_word, color_value in self.COLOR_MAP.items():
            if color_word in problem_text:
                for  elements in shape_elements.items():
                    for element, keys in elements.items():
                        if element in problem_text:
                            for key in keys:
                                color_instructions[key] = color_value

        return color_instructions

    def extract_dimensions(self, problem_text, dimension_keywords):
        """_summary_
        Trích xuất kích thước từ bài toán dựa trên các từ khóa (chiều dài, chiều rộng, cạnh, v.v.).
        Arguments:
            problem_text -- _description_  --nội dung bài toán.
            dimension_keywords -- _description_ -- danh sách các từ khóa để tìm kích thước.

        Returns:
            _description_ -- từ điển chứa thông tin kích thước và giá trị tương ứng.
        """ 
        dimensions = {}
        for keyword in dimension_keywords:
            pattern = fr'{keyword}\s*=\s*(\d+\.?\d*)'
            match = re.search(pattern, problem_text)
            if match:
                dimensions[keyword] = float(match.group(1))
        return dimensions
    
    # Hàm tải dữ liệu bài toán từ JSON và cập nhật giao diện minh họa
    def load_and_update_visualization(self):

        if not self.current_problem_file:
            return

        try:
            with open(self.current_problem_file, 'r', encoding='utf-8') as f:
                problem_data = json.load(f)

            shape = problem_data.get('shape')
            problem_text = problem_data.get('problem_text')
            if shape:
                self.shape_var.set(shape)
                self.draw_shape(shape, problem_text)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file: {e}") 

    # Hàm thiết lập giao diện minh họa hình học
    def setup_visualization(self):

        visual_frame = tk.LabelFrame(self.right_panel, text="Hình ảnh minh họa",
                                     font=("Arial", 12, "bold"), bg="#F0F8FF")
        visual_frame.pack(fill="both", expand=True, pady=10)

        self.canvas = tk.Canvas(visual_frame, width=400, height=300,
                                bg="white", highlightthickness=1)
        self.canvas.pack(pady=10, padx=10)

    # Hàm thiết lập giao diện hiển thị các bước giải
    def setup_calculation_display(self):
        calc_frame = tk.LabelFrame(self.left_panel, text="Các bước giải",
                                   font=("Arial", 12, "bold"), bg="#F0F8FF")
        calc_frame.pack(fill="both", expand=True, pady=10)

        self.calc_text = scrolledtext.ScrolledText(calc_frame, height=10,
                                                   font=("Arial", 11))
        self.calc_text.pack(pady=10, padx=10, fill="both", expand=True)

    # Hàm thiết lập giao diện ghi chú
    def setup_note(self):
        #Tạo khung chứa ghi chú về các yếu tố của hình học (như công thức, khái niệm, v.v.).
        chat_frame = tk.LabelFrame(self.right_panel, text="Chú thích",
                                font=("Arial", 12, "bold"), bg="#F0F8FF")
        chat_frame.pack(fill="both", expand=True, pady=10)
        self.chat_display = scrolledtext.ScrolledText(chat_frame, height=8,
                                                    font=("Arial", 11))
        self.chat_display.pack(pady=5, padx=10, fill="both", expand=True)

    #hiển thị từng ghi chú khi người dùng chọn 1 hình học
    def on_shape_select(self):
        """ Cập nhật giao diện và hiển thị ghi chú tương ứng khi người dùng chọn loại hình học."""
        shape = self.shape_var.get()
        self.draw_shape(shape)
        self.chat_display.config(state=tk.NORMAL)  
        self.chat_display.delete("1.0", tk.END) 
        # Hiển thị chú thích liên quan đến hình 
        if shape == "rectangle":
            self.chat_display.insert(tk.END, 
                                        "- Chiều dài: a\n"
                                        "- Chiều rộng: b\n"
                                        "- Diện tích: S\n"
                                        "- Chu vi: P\n"
                                        "- Đường chéo: d\n"
                                        "- Công thức tính diện tích (area):\n" 
                                        " 1. Tính diện tích từ chiều dài và chiều rộng: S = a × b\n"
                                        " 2. Tính chiều dài từ diện tích và chiều rộng: a = S / b\n"
                                        " 3. Tính chiều rộng từ diện tích và chiều dài: b = S / a\n"
                                        "- Công thức tính chu vi (perimeter):\n" 
                                        " 1. Tính chu vi từ chiều dài và chiều rộng: P = 2(a + b)\n" 
                                        " 2. Tính chiều dài từ chu vi và chiều rộng: a = P / 2 - b\n" 
                                        " 3. Tính chiều rộng từ chu vi và chiều dài: b = P / 2 - a\n"
                                        "- Công thức tính đường chéo (diagonal):\n" 
                                        " 1. Tính đường chéo từ chiều dài và chiều rộng: d = √(a² + b²)\n"
                                        " 2. Tính chiều rộng từ đường chéo và chiều dài: b = √(d² - a²)\n" 
                                        " 3. Tính chiều dài từ đường chéo và chiều rộng: a = √(d² - b²)\n" 
                                        "- Công thức phức hợp:\n" 
                                        " 1. Tính chiều dài từ chu vi và đường chéo: a = √[(P / 2)² + (d / 4)²] - P / 2\n" 
                                        " 2. Tính chiều rộng từ chu vi và đường chéo: b = √[(P / 2)² + (d / 4)²] - P / 2\n" 
                                        " 3. Tính chiều dài từ đường chéo và diện tích: a = √[d² + (d / 4)² - 4S] / 2\n" 
                                        " 4. Tính chiều rộng từ đường chéo và diện tích: b = √[d² - (d / 4)² - 4S] / 2\n")
        elif shape == "triangle":
            self.chat_display.insert(tk.END, 
                                    "1. Góc alpha: α\n"
                                    "2. Góc beta : β \n"
                                    "3. Góc delta : δ\n"
                                    "4. cạnh : a, b, c \n"
                                    "5. Diện tích: S \n"
                                    "6. Nửa chu vi: p \n"
                                    "7. Bán kính đường tròn ngoại tiếp : R\n"
                                    "8. Bán kính đường tròn nội tiếp  : r\n"
                                    "9. Chiều cao: Hc\n")
        elif shape == "square":
            self.chat_display.insert(tk.END,
                                    "- Độ dài cạnh: a\n"
                                    "- Diện tích: S\n"
                                    "- Chu vi: P\n"
                                    "- đường chéo: d\n"
                                    "1. Tính cạnh từ diện tích: a = √S\n"
                                    "2. Tính cạnh từ chu vi: a = P / 4\n"
                                    "3. Tính cạnh từ đường chéo: a = d / √2\n"
                                    "4. Tính diện tích: S = a²\n"
                                    "5. Tính chu vi: P = 4a\n"
                                    "6. Tính đường chéo: d = a√2\n")
                                    
            self.chat_display.config(state=tk.DISABLED)

    def draw_shape(self, shape, problem_text=None):
        """_summary_

        Arguments:
            shape -- _description_ --loại hình học cần vẽ (hình vuông, hình chữ nhật, tam giác).

        Keyword Arguments:
            problem_text -- _description_ (default: {None}) -- nội dung bài toán để xác định thông tin bổ sung (màu sắc, chú thích).
        """
        self.canvas.delete("all")
        default_line_color = "black"
        default_fill_color = "#080FE6"
        default_rectangle_color = "#90EE90"
        default_square_color = "#FFECA1"
        default_triangle_color = "#DFE648"
        problem_text = problem_text.lower() if problem_text else ""
        if shape == "square":
            canvas_width = int(self.canvas["width"])
            canvas_height = int(self.canvas["height"])
            square_size = 200

            x1 = (canvas_width - square_size) // 2
            y1 = (canvas_height - square_size) // 2
            x2 = x1 + square_size
            y2 = y1 + square_size
            self.canvas.create_rectangle(x1, y1, x2, y2, width=2, outline=default_line_color, fill=default_square_color)

            side_a_color = "red" if "cạnh a" in problem_text.lower() or "a =" in problem_text.lower() or "cạnh" in problem_text.lower() else default_line_color
            side_d_color = "red" if "đường chéo" in problem_text.lower() or "d =" in problem_text.lower() else default_line_color
            side_S_color = "red" if "diện tích" in problem_text.lower() or "s =" in problem_text.lower() else default_line_color
            side_P_color = "red" if "chu vi" in problem_text.lower() or "p =" in problem_text.lower() else default_line_color
            side_AC_color = "red" if "đường chéo ac" in problem_text.lower() or "đường chéo ac =" in problem_text.lower() else default_line_color
            side_BD_color = "red" if "đường chéo bd" in problem_text.lower() or "đường chéo bd =" in problem_text.lower() else default_line_color

            self.canvas.create_text((x1 + x2) // 2, y1 - 10, text="a", font=("Arial", 12), fill=side_a_color, tags="side_a_label")
            self.canvas.create_text(x1 - 10, y1 - 10, text="A", font=("Arial", 12), fill="black")
            self.canvas.create_text(x2 + 10, y1 - 10, text="B", font=("Arial", 12), fill="black")
            self.canvas.create_text(x2 + 10, y2 + 10, text="C", font=("Arial", 12), fill="black")
            self.canvas.create_text(x1 - 10, y2 + 10, text="D", font=("Arial", 12), fill="black")
            self.canvas.create_line(x1, y1, x2, y2, fill=side_AC_color, dash=(4, 2))
            self.canvas.create_line(x1, y2, x2, y1, fill=side_BD_color, dash=(4, 2))

            xd = (x1 + x2) // 2
            yd = (y1 + y2) // 2 + 20
            side_diag_color = "red" if side_d_color == "red" or side_AC_color == "red" or side_BD_color == "red" else default_line_color
            self.canvas.create_text(xd, yd, text="d", font=("Arial", 12), fill=side_diag_color, tags="side_a_label")

            self.canvas.create_text(x1 - 50, y1 + 20, text="S= ?", font=("Helvetica bold", 12), fill=side_S_color,tags="side_a_label")  # Diện tích
            self.canvas.create_text(x1 - 50, y1 + 40, text="P= ?", font=("Helvetica bold", 12), fill=side_P_color, tags="side_a_label")  # Chu vi
        elif shape == "triangle":
            self.canvas.create_polygon(200, 50, 50, 250, 350, 250, outline=default_line_color, fill=default_triangle_color, width=2)
            side_a_color = "red" if "cạnh a" in problem_text or "a="  in problem_text else default_line_color
            side_b_color = "red" if "cạnh b" in problem_text or "b=" in problem_text or "b" in problem_text else default_line_color
            side_c_color = "red" if "cạnh c" in problem_text or "c=" in problem_text else default_line_color
            side_Hc_color = "red" if "chiều cao" in problem_text or "hc="  in problem_text else default_line_color
            angle_alpha_color = "red" if "góc alpha" in problem_text else default_fill_color
            angle_beta_color = "red" if "góc beta" in problem_text else default_fill_color
            angle_delta_color = "red" if "góc delta" in problem_text else default_fill_color

            self.canvas.create_text(120, 140, text="a", font=("Arial", 12, "bold"), fill=side_a_color)
            self.canvas.create_text(280, 140, text="b", font=("Arial", 12, "bold"), fill=side_b_color)
            self.canvas.create_text(200, 270, text="c", font=("Arial", 12, "bold"), fill=side_c_color)
            self.canvas.create_text(185, 240, text="Hc", font=("Arial", 12, "bold"), fill=side_Hc_color)
            self.canvas.create_text(193, 73, text="α", font=("Arial", 16, "bold"), fill=angle_alpha_color)
            self.canvas.create_text(80, 240, text="β", font=("Arial", 16, "bold"), fill=angle_beta_color)
            self.canvas.create_text(320, 245, text="δ", font=("Arial", 16, "bold"), fill=angle_delta_color)
            
            self.canvas.create_text(200, 30, text="A", font=("Arial", 12, "bold"), fill=default_line_color)
            self.canvas.create_text(30, 250, text="B", font=("Arial", 12, "bold"), fill=default_line_color)
            self.canvas.create_text(370, 250,text="C", font=("Arial", 12, "bold"), fill=default_line_color)
            self.canvas.create_line(200, 50, 200, 250, fill=default_line_color)  
            self.canvas.create_line(50, 250, 280, 140, fill=default_line_color)  
            self.canvas.create_line(350, 250, 120, 140, fill=default_line_color) 
           
        elif shape == "rectangle":
            self.canvas.create_rectangle(50, 50, 350, 200, width=2, outline=default_line_color, fill=default_rectangle_color)

            diagonal_AC_color = "red" if "đường chéo ac" in problem_text.lower() or "đường chéo ac =" in problem_text.lower() else default_line_color
            diagonal_BD_color = "red" if "đường chéo bd" in problem_text.lower() or "đường chéo bd =" in problem_text.lower() else default_line_color
            diagonal_color = "red" if "đường chéo" in problem_text.lower() or "d =" in problem_text.lower() else default_line_color
            length_color = "red" if "chiều dài" in problem_text.lower() or "a = " in problem_text.lower() else default_line_color
            width_color = "red" if "chiều rộng" in problem_text.lower() or "b=" in problem_text.lower() else default_line_color
            area_color = "red" if "diện tích" in problem_text.lower() or "s" in problem_text.lower() else default_line_color
            perimeter_color = "red" if "chu vi" in problem_text.lower() or "p" in problem_text.lower() else default_line_color

            self.canvas.create_text(200, 30, text="a", font=("Helvetica", 10, "bold"), fill=length_color)
            self.canvas.create_text(30, 125, text="b", font=("Helvetica", 10, "bold"), fill=width_color)
            self.canvas.create_text(45, 45, text="A", font=("Helvetica", 10, "bold"), fill="black")
            self.canvas.create_text(355, 45, text="B", font=("Helvetica", 10, "bold"), fill="black")
            self.canvas.create_text(355, 205, text="C", font=("Helvetica", 10, "bold"), fill="black")
            self.canvas.create_text(45, 205, text="D", font=("Helvetica", 10, "bold"), fill="black")

            self.canvas.create_line(50, 50, 350, 200, fill=diagonal_AC_color, dash=(4, 2))
            self.canvas.create_line(50, 200, 350, 50, fill=diagonal_BD_color, dash=(4, 2))

            xd = (50 + 350) // 2
            yd = (50 + 200) // 2

            # Đổi màu văn bản "d" cho cả hai đường chéo
            side_diag_color = "red" if diagonal_AC_color == "red" or diagonal_BD_color == "red" or diagonal_color == "red" else default_line_color
            self.canvas.create_text(xd, yd +20 , text="d", font=("Arial", 12), fill=side_diag_color, tags="side_a_label")

            self.canvas.create_text(200, 220, text="S=?", font=("Helvetica", 12, "bold"), fill=area_color)
            self.canvas.create_text(200, 240, text="P=?", font=("Helvetica", 12, "bold"), fill=perimeter_color)
