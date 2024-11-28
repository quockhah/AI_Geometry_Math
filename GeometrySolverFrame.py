import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import openai
from MainMenuFrame import *
import json
import os
from datetime import datetime
import re
class GeometrySolverFrame(tk.Frame):
    def __init__(self, parent, controller):
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

    def setup_problem_input(self):
        input_frame = tk.LabelFrame(self.left_panel, text="Nhập Bài Toán",font=("Arial", 12, "bold"), bg="#F0F8FF")
        input_frame.pack(fill="x", pady=10)
        self.problem_text = scrolledtext.ScrolledText(input_frame,height=8, width=75,font=("Arial", 11))
        self.problem_text.pack(pady=10, padx=10)

        analyze_btn = tk.Button(input_frame, text="Giải bài toán",command=self.save_problem_to_json,font=("Arial", 11, "bold"),bg="#4CAF50", fg="white")
        analyze_btn.pack(pady=10)
    
    
    def save_problem_to_json(self):
       
        problem_text = self.problem_text.get("1.0", "end-1c").strip()
        shape = self.shape_var.get()

        if not problem_text:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập bài toán!")
            return

        semantic_data = self.parse_problem_semantics(problem_text, shape)

        self.draw_shape(shape, problem_text)

        problem_data = {
            "problem_text": problem_text,
            "shape": shape,
            "semantic_analysis": semantic_data,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        os.makedirs("problem_data", exist_ok=True)

        filename = f"problem_data/data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(problem_data, f, ensure_ascii=False, indent=4)
            
            self.current_problem_file = filename
            
            messagebox.showinfo("Thành công", f"Đã lưu bài toán vào {filename}")
            
            self.calc_text.delete('1.0', tk.END)
            self.calc_text.insert(tk.END, "Phân tích ngữ nghĩa:\n")
            for key, value in semantic_data.items():
                self.calc_text.insert(tk.END, f"{key}: {value}\n")
            
            self.load_and_update_visualization()
        
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu bài toán: {e}")
    def parse_problem_semantics(self, problem_text, shape):
        semantic_data = {
            "entities": [],
            "dimensions": {},
            "color_instructions": {},
            "given_values": {}
        }

        problem_text = problem_text.lower()

        numbers = re.findall(r'\d+(?:\.\d+)?', problem_text)
        
        units = re.findall(r'(cm|m|km|mm)', problem_text)
        color_instructions = self.extract_color_instructions(problem_text)
        semantic_data["color_instructions"] = color_instructions

        if shape == "rectangle":
            semantic_data["entities"] = ["hình chữ nhật", "chiều dài", "chiều rộng"]
            dimensions = self.extract_dimensions(problem_text, ["dài", "rộng"])
            semantic_data["dimensions"] = dimensions

        elif shape == "triangle":
            semantic_data["entities"] = ["hình tam giác", "cạnh a", "cạnh b", "cạnh c"]
            dimensions = self.extract_dimensions(problem_text, ["a", "b", "c"])
            semantic_data["dimensions"] = dimensions

        elif shape == "square":
            semantic_data["entities"] = ["hình vuông", "cạnh"]
            dimensions = self.extract_dimensions(problem_text, ["a"])
            semantic_data["dimensions"] = dimensions

        semantic_data["given_values"]["numbers"] = numbers
        semantic_data["given_values"]["units"] = units

        return semantic_data
    def extract_color_instructions(self, problem_text):
        """Extract color instructions from problem text"""
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
                for shape_type, elements in shape_elements.items():
                    for element, keys in elements.items():
                        if element in problem_text:
                            for key in keys:
                                color_instructions[key] = color_value

        return color_instructions

    def extract_dimensions(self, problem_text, dimension_keywords):
        """Extract dimensions based on keywords"""
        dimensions = {}
        for keyword in dimension_keywords:
            pattern = fr'{keyword}\s*=\s*(\d+\.?\d*)'
            match = re.search(pattern, problem_text)
            if match:
                dimensions[keyword] = float(match.group(1))
        return dimensions
    def load_and_update_visualization(self):
        """Load problem from JSON and update visualization"""
        if not self.current_problem_file:
            return

        try:
            with open(self.current_problem_file, 'r', encoding='utf-8') as f:
                problem_data = json.load(f)

            shape = problem_data.get('shape')
            if shape:
                self.shape_var.set(shape)
                self.draw_shape(shape, problem_data)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file: {e}")
    def draw_shape(self, shape, problem_data=None):
        """Draw shape with optional color modifications"""
        self.canvas.delete("all")


        default_line_color = "black"
        default_fill_color = "#90EE90"

       
        color_instructions = problem_data['semantic_analysis']['color_instructions'] if problem_data else {}

        if shape == "triangle":
          
            side_colors = {
                "a": color_instructions.get("side_a", default_line_color),
                "b": color_instructions.get("side_b", default_line_color),
                "c": color_instructions.get("side_c", default_line_color)
            }
            
            angle_colors = {
                "α": color_instructions.get("angle_alpha", default_line_color),
                "β": color_instructions.get("angle_beta", default_line_color),
                "δ": color_instructions.get("angle_delta", default_line_color)
            }

            self.canvas.create_polygon(
                200, 50, 50, 250, 350, 250, 
                outline=default_line_color, 
                fill=default_fill_color, 
                width=2
            )

            self.canvas.create_text(
                200, 30, text="α", 
                font=("Arial", 12, "bold"), 
                fill=angle_colors["α"]
            )

    def setup_visualization(self):
        visual_frame = tk.LabelFrame(self.right_panel, text="Hình ảnh minh họa",
                                     font=("Arial", 12, "bold"), bg="#F0F8FF")
        visual_frame.pack(fill="both", expand=True, pady=10)

        self.canvas = tk.Canvas(visual_frame, width=400, height=300,
                                bg="white", highlightthickness=1)
        self.canvas.pack(pady=10, padx=10)

    def setup_calculation_display(self):
        calc_frame = tk.LabelFrame(self.left_panel, text="Các bước giải",
                                   font=("Arial", 12, "bold"), bg="#F0F8FF")
        calc_frame.pack(fill="both", expand=True, pady=10)

        self.calc_text = scrolledtext.ScrolledText(calc_frame, height=10,
                                                   font=("Arial", 11))
        self.calc_text.pack(pady=10, padx=10, fill="both", expand=True)

    def setup_note(self):
        
        chat_frame = tk.LabelFrame(self.right_panel, text="Chú thích",
                                font=("Arial", 12, "bold"), bg="#F0F8FF")
        chat_frame.pack(fill="both", expand=True, pady=10)
        self.chat_display = scrolledtext.ScrolledText(chat_frame, height=8,
                                                    font=("Arial", 11))
        self.chat_display.pack(pady=5, padx=10, fill="both", expand=True)


    def on_shape_select(self):
        shape = self.shape_var.get()
        self.draw_shape(shape)
        self.chat_display.config(state=tk.NORMAL)  
        self.chat_display.delete("1.0", tk.END)  
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
        """Draw shape with potential color modifications for specific elements"""
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
            side_a_color = "red" if "cạnh a" in problem_text or "a =" in problem_text or "cạnh" in problem_text else default_line_color
            side_d_color = "red" if "đường chéo" in problem_text or "d =" in problem_text else default_line_color
            side_S_color = "red" if "diện tích" in problem_text or "S =" in problem_text else default_line_color
            side_P_color = "red" if "chu vi" in problem_text or "P =" in problem_text else default_line_color
            self.canvas.create_text((x1 + x2) // 2, y1 - 10, text="a", font=("Arial", 12), fill=side_a_color,tags="side_a_label") 
            self.canvas.create_text(x1 - 10, y1 - 10, text="A", font=("Arial", 12), fill="black") 
            self.canvas.create_text(x2 + 10, y1 - 10, text="B", font=("Arial", 12), fill="black") 
            self.canvas.create_text(x2 + 10, y2 + 10, text="C", font=("Arial", 12), fill="black") 
            self.canvas.create_text(x1 - 10, y2 + 10, text="D", font=("Arial", 12), fill="black")
            self.canvas.create_line(x1, y1, x2, y2, fill=side_d_color, dash=(4, 2)) 
            self.canvas.create_line(x1, y2, x2, y1, fill=side_d_color, dash=(4, 2))
            xd = (x1 + x2) // 2 
            yd = (y1 + y2) // 2 + 20 
            self.canvas.create_text(xd, yd, text="d", font=("Arial", 12), fill=side_d_color, tags="side_a_label")
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
            angle_gamma_color = "red" if "góc delta" in problem_text else default_fill_color

            self.canvas.create_text(120, 140, text="a", font=("Arial", 12, "bold"), fill=side_a_color)
            self.canvas.create_text(280, 140, text="b", font=("Arial", 12, "bold"), fill=side_b_color)
            self.canvas.create_text(200, 270, text="c", font=("Arial", 12, "bold"), fill=side_c_color)
            self.canvas.create_text(185, 240, text="Hc", font=("Arial", 12, "bold"), fill=side_Hc_color)
            self.canvas.create_text(193, 73, text="α", font=("Arial", 16, "bold"), fill=angle_alpha_color)
            self.canvas.create_text(80, 240, text="β", font=("Arial", 16, "bold"), fill=angle_beta_color)
            self.canvas.create_text(320, 245, text="δ", font=("Arial", 16, "bold"), fill=angle_gamma_color)
            
            self.canvas.create_text(200, 30, text="A", font=("Arial", 12, "bold"), fill=default_line_color)
            self.canvas.create_text(30, 250, text="B", font=("Arial", 12, "bold"), fill=default_line_color)
            self.canvas.create_text(370, 250,text="C", font=("Arial", 12, "bold"), fill=default_line_color)
            self.canvas.create_line(200, 50, 200, 250, fill=default_line_color)  
            self.canvas.create_line(50, 250, 280, 140, fill=default_line_color)  
            self.canvas.create_line(350, 250, 120, 140, fill=default_line_color) 
           
        elif shape == "rectangle":
            self.canvas.create_rectangle(50, 50, 350, 200, width=2, outline=default_line_color, fill=default_rectangle_color)

            length_color = "red" if "chiều dài" in problem_text or "a" in problem_text else default_line_color
            width_color = "red" if "chiều rộng" in problem_text or "b" in problem_text else default_line_color
            diagonal_color = "red" if "đường chéo" in problem_text or "d =" in problem_text else default_line_color
            area_color = "red" if "diện tích" in problem_text or "S" in problem_text else default_line_color
            perimeter_color = "red" if "chu vi" in problem_text or "P" in problem_text else default_line_color
            self.canvas.create_text(200, 30, text="a", font=("Helvetica", 10, "bold"), fill=length_color)
            self.canvas.create_text(30, 125, text="b", font=("Helvetica", 10, "bold"), fill=width_color)
            self.canvas.create_text(45, 45, text="A", font=("Helvetica", 10, "bold"), fill="black") 
            self.canvas.create_text(355, 45, text="B", font=("Helvetica", 10, "bold"), fill="black") 
            self.canvas.create_text(355, 205, text="C", font=("Helvetica", 10, "bold"), fill="black") 
            self.canvas.create_text(45, 205, text="D", font=("Helvetica", 10, "bold"), fill="black")

            self.canvas.create_line(50, 50, 350, 200, fill=diagonal_color, dash=(4, 2))  
            self.canvas.create_line(50, 200, 350, 50, fill=diagonal_color, dash=(4, 2))  
            xd = (50 + 350) // 2 
            yd = (50 + 200) // 2  
            self.canvas.create_text(xd, yd + 20, text="d", font=("Helvetica", 10, "bold"), fill=diagonal_color)
            self.canvas.create_text(200, 220, text="S=?", font=("Helvetica", 12, "bold"), fill=area_color)  
            self.canvas.create_text(200, 240, text="P=?", font=("Helvetica", 12, "bold"), fill=perimeter_color)