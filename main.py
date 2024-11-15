import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk
from MainMenuFrame  import*
from GeometrySolverFrame import*

from TriangleCalculatorFrame import*

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Toán Ứng Dụng")
        self.root.geometry("950x670")
        
        self.container = tk.Frame(root)
        self.container.pack(side="top", fill="both", expand=True)
        
        self.frames = {}
        
        # Khởi tạo tất cả các frame cần thiết
        for F in (MainMenuFrame,SquareCalculatorFrame, GeometrySolverFrame,
                  TriangleCalculatorFrame, RectangleCalculatorFrame):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.show_frame(MainMenuFrame)
    
    def back_main(self, frame_class):
        frame_class.destroy()  # Đóng cửa sổ Toplevel
        self.root.deiconify()
        

    def show_frame(self, frame_class):
        """
        Hiển thị frame được chỉ định
        frame_class: Class của frame cần hiển thị (không phải string)
        """
        if frame_class in self.frames:
            frame = self.frames[frame_class]
            frame.tkraise()
        else:
            print(f"Error: Frame {frame_class} not found")
    
    def show_geometry_solver(self, shape_type):
        """
        Hiển thị frame giải toán với hình được chọn
        shape_type: Loại hình ('square', 'triangle', 'rectangle')
        """
        solver_window = tk.Toplevel(self.root)
        solver_window.title("Giải Toán Hình Học")
        solver_window.geometry("1200x750")  # Kích thước của cửa sổ mới

        solver_frame =  GeometrySolverFrame(solver_window, self)
        # Đặt lại giá trị loại hình
        solver_frame.shape_var.set(shape_type)
        solver_frame.on_shape_select()
            
        # Đặt frame vào cửa sổ mới
        solver_frame.grid(row=0, column=0, sticky="nsew")
        solver_window.grid_rowconfigure(0, weight=1)
        solver_window.grid_columnconfigure(0, weight=1)

        # Ẩn MainApplication (có thể xóa hoặc không cần gọi ở đây tùy thuộc vào yêu cầu)
        self.root.withdraw()  # Ẩn cửa sổ chính

    def show_triangle_solver(self, frame_class):
        calculator_window = tk.Toplevel(self.root)
        calculator_window.title("Giải Toán Tam Giác")
        calculator_window.geometry("1000x600") 
        calculator_frame =  TriangleCalculatorFrame(calculator_window, self)
        calculator_frame.grid(row=0, column=0, sticky="nsew")
        calculator_window.grid_rowconfigure(0, weight=1)
        calculator_window.grid_columnconfigure(0, weight=1)
        self.root.withdraw()

    def show_rectangle_solver(self,frame_class):
        calculator_window = tk.Toplevel(self.root)
        calculator_window.title("Hình chữ nhật")
        calculator_window.geometry("1000x600") 
        calculator_frame = RectangleCalculatorFrame(calculator_window, self)
        calculator_frame.grid(row=0, column=0, sticky="nsew")
        calculator_window.grid_rowconfigure(0, weight=1)
        calculator_window.grid_columnconfigure(0, weight=1)
        self.root.withdraw()
    def show_square_solver(self,frame_class):
        calculator_window = tk.Toplevel(self.root)
        calculator_window.title("Hình vuông")
        calculator_window.geometry("1000x600") 
        calculator_frame = SquareCalculatorFrame(calculator_window, self)
        calculator_frame.grid(row=0, column=0, sticky="nsew")
        calculator_window.grid_rowconfigure(0, weight=1)
        calculator_window.grid_columnconfigure(0, weight=1)
        self.root.withdraw()
    
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()