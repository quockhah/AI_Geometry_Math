import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from MainMenuFrame import*
class BaseCalculatorFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#F0F8FF")
        
        # Header frame
        header_frame = tk.Frame(self, bg="#F0F8FF")
        header_frame.pack(fill="x", pady=10)
        
        # Back button
        back_btn = tk.Button(header_frame,
                           text="↩ Quay lại",
                           command=lambda: controller.show_frame(MainMenuFrame),
                           font=("Arial", 12),
                           bg="#FF99CC",
                           fg="white")
        back_btn.pack(side="left", padx=10)
        
        # AI Solver button
        ai_btn = tk.Button(header_frame,
                          text="🤖 Sử dụng AI Solver",
                          command=lambda: self.switch_to_ai_solver(),
                          font=("Arial", 12),
                          bg="#4CAF50",
                          fg="white")
        ai_btn.pack(side="right", padx=10)
        
        # Canvas frame for visualization
        self.canvas_frame = tk.Frame(self, bg="white")
        self.canvas_frame.pack(pady=20)
        
        self.canvas = tk.Canvas(self.canvas_frame, width=400, height=300,
                              bg="white")
        self.canvas.pack()
    
    def switch_to_ai_solver(self):
        pass