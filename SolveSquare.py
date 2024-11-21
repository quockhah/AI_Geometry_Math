import math
from typing import Dict, List, Callable


class GeometryFormula:
    def __init__(self, inputs: List[str], output: str, formula: Callable, explanation: str):
        self.inputs = inputs
        self.output = output
        self.formula = formula
        self.explanation = explanation


class HinhVuong:
    def __init__(self, **kwargs):
        # Khởi tạo các giá trị đã biết
        self.a = kwargs.get('a')  # Cạnh hình vuông
        self.d = kwargs.get('d')  # Đường chéo
        self.S = kwargs.get('S')  # Diện tích
        self.P = kwargs.get('P')  # Chu vi
        self.r = kwargs.get('r')  # Bán kính đường tròn nội tiếp
        self.R = kwargs.get('R')  # Bán kính đường tròn ngoại tiếp

        # Lưu trữ các bước giải và công thức đã dùng
        self.steps = []
        self.used_formulas = []

        # Định nghĩa mạng công thức
        self.formulas = [
            GeometryFormula(
                inputs=['a'],
                output='S',
                formula=lambda a: a * a,
                explanation="Diện tích hình vuông bằng bình phương cạnh: S = a²"
            ),
            GeometryFormula(
                inputs=['S'],
                output='a',
                formula=lambda S: math.sqrt(S),
                explanation="Cạnh hình vuông bằng căn bậc hai của diện tích: a = √S"
            ),
            GeometryFormula(
                inputs=['a'],
                output='P',
                formula=lambda a: 4 * a,
                explanation="Chu vi hình vuông bằng 4 lần cạnh: P = 4a"
            ),
            GeometryFormula(
                inputs=['P'],
                output='a',
                formula=lambda P: P / 4,
                explanation="Cạnh hình vuông bằng chu vi chia 4: a = P/4"
            ),
            GeometryFormula(
                inputs=['a'],
                output='d',
                formula=lambda a: a * math.sqrt(2),
                explanation="Đường chéo hình vuông bằng cạnh nhân căn bậc hai của 2: d = a√2"
            ),
            GeometryFormula(
                inputs=['d'],
                output='a',
                formula=lambda d: d / math.sqrt(2),
                explanation="Cạnh hình vuông bằng đường chéo chia căn bậc hai của 2: a = d/√2"
            ),
        ]

        self.validate_inputs()

    def validate_inputs(self):
        # Kiểm tra các mối quan hệ hình học
        if self.a and self.d and not math.isclose(self.d, self.a * math.sqrt(2), rel_tol=1e-5):
            raise ValueError("Giá trị d không phù hợp với a theo công thức d = a√2")
        if self.a and self.P and not math.isclose(self.P, 4 * self.a, rel_tol=1e-5):
            raise ValueError("Giá trị P không phù hợp với a theo công thức P = 4a")
        if self.a and self.S and not math.isclose(self.S, self.a ** 2, rel_tol=1e-5):
            raise ValueError("Giá trị S không phù hợp với a theo công thức S = a²")

    def solve(self) -> Dict[str, float]:
        while True:
            found_new = False

            for formula in self.formulas:
                if all(hasattr(self, inp) and getattr(self, inp) is not None for inp in formula.inputs):
                    if not hasattr(self, formula.output) or getattr(self, formula.output) is None:
                        inputs = [getattr(self, inp) for inp in formula.inputs]
                        result = formula.formula(*inputs)
                        setattr(self, formula.output, result)

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

    def get_results(self) -> Dict[str, str]:
        unit = "cm"  # Bạn có thể thay đổi đơn vị nếu cần
        return {
            'a': f"{round(self.a, 2)} {unit}" if self.a is not None else None,
            'd': f"{round(self.d, 2)} {unit}" if self.d is not None else None,
            'S': f"{round(self.S, 2)} {unit}²" if self.S is not None else None,
            'P': f"{round(self.P, 2)} {unit}" if self.P is not None else None
        }

    def get_solution_steps(self) -> str:
        solution = "Lời giải chi tiết:\n\n"
        for i, step in enumerate(self.steps, 1):
            solution += f"Bước {i}:\n"
            solution += f"Công thức: {step['formula']}\n"
            solution += "Thay số:\n"
            for var, val in step['inputs'].items():
                solution += f"{var} = {val:.2f} cm\n"  # Thêm đơn vị
            for var, val in step['output'].items():
                solution += f"=> {var} = {val:.2f} cm\n"  # Thêm đơn vị
            solution += "\n"
        return solution


if __name__ == "__main__":
    try:
        # Trường hợp 1: Dữ liệu không hợp lệ
        print("Trường hợp 1: Dữ liệu không hợp lệ (d = 6 không hợp lệ với a = 5)")
        square_invalid = HinhVuong(a=5, d=6)  # Giá trị d không phù hợp
        results_invalid = square_invalid.solve()
        print("Kết quả hình vuông (không hợp lệ):")
        print(results_invalid)
        print("\nLời giải hình vuông (không hợp lệ):")
        print(square_invalid.get_solution_steps())

    except ValueError as e:
        print("Lỗi:", e)
    
    try:
        # Trường hợp 2: Dữ liệu hợp lệ
        print("\nTrường hợp 2: Dữ liệu hợp lệ (a = 5)")
        square_valid = HinhVuong(a=5)  # Dữ liệu hợp lệ với a = 5
        results_valid = square_valid.solve()
        print("Kết quả hình vuông (hợp lệ):")
        print(results_valid)
        print("\nLời giải hình vuông (hợp lệ):")
        print(square_valid.get_solution_steps())

    except ValueError as e:
        print("Lỗi:", e)
