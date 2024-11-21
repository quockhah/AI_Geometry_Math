import math
from typing import Dict, List, Callable

class GeometryFormula:
    def __init__(self, inputs: List[str], output: str, formula: Callable, explanation: str):
        self.inputs = inputs
        self.output = output
        self.formula = formula
        self.explanation = explanation

class HinhChuNhat:
    def __init__(self, **kwargs):
        # Khởi tạo các giá trị đã biết
        self.a = kwargs.get('a')  # Chiều dài
        self.b = kwargs.get('b')  # Chiều rộng
        self.d = kwargs.get('d')  # Đường chéo
        self.S = kwargs.get('S')  # Diện tích
        self.P = kwargs.get('P')  # Chu vi
        self.alpha = kwargs.get('alpha')  # Góc giữa đường chéo và cạnh (đơn vị độ)
        
        # Chuyển đổi góc từ độ sang radian nếu có
        if self.alpha is not None:
            self.alpha = math.radians(self.alpha)
        
        # Lưu trữ các bước giải và công thức đã dùng
        self.steps = []
        self.used_formulas = []
        
        # Định nghĩa mạng công thức
        self.formulas = [
            GeometryFormula(
                inputs=['a', 'b'],
                output='S',
                formula=lambda a, b: a * b,
                explanation="Diện tích hình chữ nhật bằng tích chiều dài và chiều rộng: S = a × b"
            ),
            GeometryFormula(
                inputs=['S', 'a'],
                output='b',
                formula=lambda S, a: S / a,
                explanation="Chiều rộng bằng diện tích chia chiều dài: b = S/a"
            ),
            GeometryFormula(
                inputs=['S', 'b'],
                output='a',
                formula=lambda S, b: S / b,
                explanation="Chiều dài bằng diện tích chia chiều rộng: a = S/b"
            ),
            GeometryFormula(
                inputs=['a', 'b'],
                output='P',
                formula=lambda a, b: 2 * (a + b),
                explanation="Chu vi hình chữ nhật bằng 2 lần tổng chiều dài và chiều rộng: P = 2(a + b)"
            ),
            GeometryFormula(
                inputs=['P', 'a'],
                output='b',
                formula=lambda P, a: (P - 2*a) / 2,
                explanation="Chiều rộng tính từ chu vi và chiều dài: b = (P - 2a)/2"
            ),
            GeometryFormula(
                inputs=['a', 'b'],
                output='d',
                formula=lambda a, b: math.sqrt(a**2 + b**2),
                explanation="Đường chéo tính theo định lý Pytago: d = √(a² + b²)"
            ),
            GeometryFormula(
                inputs=['a', 'b'],
                output='alpha',
                formula=lambda a, b: math.atan(b/a),
                explanation="Góc giữa đường chéo và cạnh dài: α = arctang(b/a)"
            ),
            GeometryFormula(
                inputs=['d', 'alpha'],
                output='a',
                formula=lambda d, alpha: d * math.cos(alpha),
                explanation="Chiều dài tính từ đường chéo và góc: a = d×cos(α)"
            ),
            GeometryFormula(
                inputs=['d', 'alpha'],
                output='b',
                formula=lambda d, alpha: d * math.sin(alpha),
                explanation="Chiều rộng tính từ đường chéo và góc: b = d×sin(α)"
            )
        ]

    def check_validity(self) -> bool:
        # Kiểm tra tính hợp lệ của các dữ liệu đầu vào
        if self.a is not None and self.b is not None:
            if self.a <= 0 or self.b <= 0:
                raise ValueError("Chiều dài và chiều rộng phải là số dương.")
            if self.d is not None and not math.isclose(self.d, math.sqrt(self.a**2 + self.b**2), abs_tol=1e-5):
                raise ValueError("Đường chéo không hợp lệ với chiều dài và chiều rộng.")
            if self.alpha is not None and (self.alpha < 0 or self.alpha > math.pi / 2):
                raise ValueError("Góc alpha phải nằm trong khoảng từ 0° đến 90°.")
        return True

    def solve(self) -> Dict[str, float]:
        if not self.check_validity():
            return {}

        while True:
            found_new = False
            
            # Duyệt qua tất cả công thức
            for formula in self.formulas:
                # Kiểm tra xem có đủ dữ liệu đầu vào cho công thức không
                if all(hasattr(self, inp) and getattr(self, inp) is not None for inp in formula.inputs):
                    # Kiểm tra xem kết quả đã được tính chưa
                    if not hasattr(self, formula.output) or getattr(self, formula.output) is None:
                        # Tính giá trị mới
                        inputs = [getattr(self, inp) for inp in formula.inputs]
                        result = formula.formula(*inputs)
                        setattr(self, formula.output, result)
                        
                        # Lưu bước giải
                        step = {
                            'formula': formula.explanation,
                            'inputs': {inp: getattr(self, inp) for inp in formula.inputs},
                            'output': {formula.output: result}
                        }
                        self.steps.append(step)
                        self.used_formulas.append(formula)
                        found_new = True
            
            if not found_new:
                break
        
        return self.get_results()

    def get_results(self) -> Dict[str, float]:
        results = {
            'a': f"{round(self.a, 2)} cm" if self.a is not None else None,
            'b': f"{round(self.b, 2)} cm" if self.b is not None else None,
            'd': f"{round(self.d, 2)} cm" if self.d is not None else None,
            'S': f"{round(self.S, 2)} cm²" if self.S is not None else None,
            'P': f"{round(self.P, 2)} cm" if self.P is not None else None,
            'alpha': f"{round(math.degrees(self.alpha), 2)}°" if self.alpha is not None else None
        }
        return results
    
    def get_solution_steps(self) -> str:
        solution = "Lời giải chi tiết:\n\n"
        for i, step in enumerate(self.steps, 1):
            solution += f"Bước {i}:\n"
            solution += f"Công thức: {step['formula']}\n"
            solution += "Thay số:\n"
            
            # Thay số cho các biến đầu vào
            for var, val in step['inputs'].items():
                if var == 'alpha':
                    solution += f"{var} = {math.degrees(val):.2f}°\n"
                else:
                    solution += f"{var} = {val:.2f} cm\n"
            
            # Thay số cho kết quả
            for var, val in step['output'].items():
                if var == 'alpha':
                    solution += f"=> {var} = {math.degrees(val):.2f}°\n"
                else:
                    solution += f"=> {var} = {val:.2f} cm\n"
            
            solution += "\n"
        
        return solution


# Ví dụ sử dụng:
if __name__ == "__main__":
    try:
        # Giải bài toán hình chữ nhật hợp lệ
        rectangle = HinhChuNhat(a=6, b=8)
        results = rectangle.solve()
        print("\nKết quả hình chữ nhật:")
        print(results)
        print("\nLời giải hình chữ nhật:")
        print(rectangle.get_solution_steps())

        # Giải bài toán với dữ liệu không hợp lệ
        invalid_rectangle = HinhChuNhat(a=6, b=8, d=20)  # Đường chéo không hợp lệ
        results_invalid = invalid_rectangle.solve()
        print("\nKết quả hình chữ nhật không hợp lệ:")
        print(results_invalid)
    
    except ValueError as e:
        print("Lỗi:", e)
