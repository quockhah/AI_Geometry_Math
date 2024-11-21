import math
from typing import Dict, List, Callable


class GeometryFormula:
    """
    Lớp đại diện cho một công thức hình học.

    Attributes:
        inputs (List[str]): Danh sách các biến đầu vào của công thức.
        output (str): Biến đầu ra của công thức.
        formula (Callable): Hàm thực thi công thức.
        explanation (str): Giải thích cách công thức hoạt động.
    """
    def __init__(self, inputs: List[str], output: str, formula: Callable, explanation: str):
        self.inputs = inputs
        self.output = output
        self.formula = formula
        self.explanation = explanation


class HinhVuong:
    """
    Lớp đại diện cho hình vuông và các tính toán liên quan.

    Attributes:
        side (float): Độ dài cạnh của hình vuông.
        diagonal (float): Đường chéo của hình vuông.
        area (float): Diện tích của hình vuông.
        perimeter (float): Chu vi của hình vuông.
        inscribed_radius (float): Bán kính đường tròn nội tiếp.
        circumscribed_radius (float): Bán kính đường tròn ngoại tiếp.
    """
    def __init__(self, **kwargs):
        """
        Khởi tạo các thuộc tính của hình vuông dựa trên đầu vào.

        Args:
            kwargs: Các giá trị đầu vào như cạnh, đường chéo, diện tích, chu vi, ...
        """
        self.side = kwargs.get('side', None)  # Cạnh hình vuông
        self.diagonal = kwargs.get('diagonal', None)  # Đường chéo
        self.area = kwargs.get('area', None)  # Diện tích
        self.perimeter = kwargs.get('perimeter', None)  # Chu vi
        self.inscribed_radius = kwargs.get('inscribed_radius', None)  # Bán kính đường tròn nội tiếp
        self.circumscribed_radius = kwargs.get('circumscribed_radius', None)  # Bán kính đường tròn ngoại tiếp

        # Lưu trữ các bước giải và công thức đã dùng
        self.steps = []
        self.used_formulas = []

        # Định nghĩa mạng công thức
        self.formulas = [
            GeometryFormula(
                inputs=['side'],
                output='area',
                formula=lambda side: side * side,
                explanation="Diện tích hình vuông bằng bình phương cạnh: S = a²"
            ),
            GeometryFormula(
                inputs=['area'],
                output='side',
                formula=lambda area: math.sqrt(area),
                explanation="Cạnh hình vuông bằng căn bậc hai của diện tích: a = √S"
            ),
            GeometryFormula(
                inputs=['side'],
                output='perimeter',
                formula=lambda side: 4 * side,
                explanation="Chu vi hình vuông bằng 4 lần cạnh: P = 4a"
            ),
            GeometryFormula(
                inputs=['perimeter'],
                output='side',
                formula=lambda perimeter: perimeter / 4,
                explanation="Cạnh hình vuông bằng chu vi chia 4: a = P/4"
            ),
            GeometryFormula(
                inputs=['side'],
                output='diagonal',
                formula=lambda side: side * math.sqrt(2),
                explanation="Đường chéo hình vuông bằng cạnh nhân căn bậc hai của 2: d = a√2"
            ),
            GeometryFormula(
                inputs=['diagonal'],
                output='side',
                formula=lambda diagonal: diagonal / math.sqrt(2),
                explanation="Cạnh hình vuông bằng đường chéo chia căn bậc hai của 2: a = d/√2"
            ),
        ]

        self.validate_inputs()

    def validate_inputs(self):
        """
        Kiểm tra các mối quan hệ hình học giữa các giá trị đầu vào.

        Raises:
            ValueError: Nếu các giá trị không thỏa mãn quan hệ hình học.
        """
        if self.side and self.diagonal and not math.isclose(self.diagonal, self.side * math.sqrt(2), rel_tol=1e-5):
            raise ValueError("Giá trị diagonal không phù hợp với side theo công thức d = a√2")
        if self.side and self.perimeter and not math.isclose(self.perimeter, 4 * self.side, rel_tol=1e-5):
            raise ValueError("Giá trị perimeter không phù hợp với side theo công thức P = 4a")
        if self.side and self.area and not math.isclose(self.area, self.side ** 2, rel_tol=1e-5):
            raise ValueError("Giá trị area không phù hợp với side theo công thức S = a²")

    def solve(self) -> Dict[str, float]:
        """
        Tự động tính toán các giá trị chưa biết dựa trên các giá trị đầu vào.

        Returns:
            Dict[str, float]: Kết quả của các thuộc tính (cạnh, đường chéo, diện tích, chu vi).
        """
        while True:
            found_new = False

            for formula in self.formulas:
                # Kiểm tra nếu tất cả các biến đầu vào đã biết
                if all(hasattr(self, inp) and getattr(self, inp) is not None for inp in formula.inputs):
                    # Nếu biến đầu ra chưa được tính
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
        """
        Lấy kết quả cuối cùng với đơn vị đo.

        Returns:
            Dict[str, str]: Kết quả định dạng với đơn vị.
        """
        unit = "cm"  # Có thể thay đổi đơn vị nếu cần
        return {
            'side': f"{round(self.side, 2)} {unit}" if self.side is not None else None,
            'diagonal': f"{round(self.diagonal, 2)} {unit}" if self.diagonal is not None else None,
            'area': f"{round(self.area, 2)} {unit}²" if self.area is not None else None,
            'perimeter': f"{round(self.perimeter, 2)} {unit}" if self.perimeter is not None else None
        }

    def get_solution_steps(self) -> str:
        """
        Trả về các bước giải chi tiết.

        Returns:
            str: Các bước giải chi tiết dưới dạng chuỗi.
        """
        solution = "Lời giải chi tiết:\n\n"
        for i, step in enumerate(self.steps, 1):
            solution += f"Bước {i}:\n"
            solution += f"Công thức: {step['formula']}\n"
            solution += "Thay số:\n"
            
            # Sửa phần tên biến đầu vào
            for var, val in step['inputs'].items():
                if var == "side":
                    var = "cạnh"
                elif var == "area":
                    var = "diện tích"
                elif var == "perimeter":
                    var = "chu vi"
                elif var == "diagonal":
                    var = "đường chéo"
                
                solution += f"{var} = {val:.2f} cm\n"
            
            # Sửa phần tên biến đầu ra
            for var, val in step['output'].items():
                if var == "side":
                    var = "cạnh"
                elif var == "area":
                    var = "diện tích"
                elif var == "perimeter":
                    var = "chu vi"
                elif var == "diagonal":
                    var = "đường chéo"
                
                solution += f"=> {var} = {val:.2f} cm\n"
            
            solution += "\n"
        
        return solution


if __name__ == "__main__":
    try:
        # Trường hợp 1: Dữ liệu không hợp lệ
        print("Trường hợp 1: Dữ liệu không hợp lệ (diagonal = 6 không hợp lệ với side = 5)")
        square_invalid = HinhVuong(side=5, diagonal=6)  # Giá trị diagonal không phù hợp
        results_invalid = square_invalid.solve()
        print("Kết quả hình vuông (không hợp lệ):")
        print(results_invalid)
        print("\nLời giải hình vuông (không hợp lệ):")
        print(square_invalid.get_solution_steps())

    except ValueError as e:
        print("Lỗi:", e)

    try:
        # Trường hợp 2: Dữ liệu hợp lệ
        print("\nTrường hợp 2: Dữ liệu hợp lệ (side = 5)")
        square_valid = HinhVuong(side=5)  # Dữ liệu hợp lệ với side = 5
        results_valid = square_valid.solve()
        print("Kết quả hình vuông (hợp lệ):")
        print(results_valid)
        print("\nLời giải hình vuông (hợp lệ):")
        print(square_valid.get_solution_steps())

    except ValueError as e:
        print("Lỗi:", e)
