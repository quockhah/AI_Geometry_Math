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


class HinhChuNhat:
    """
    Lớp đại diện cho hình chữ nhật và các tính toán liên quan.

    Attributes:
        length (float): Chiều dài của hình chữ nhật.
        width (float): Chiều rộng của hình chữ nhật.
        diagonal (float): Đường chéo của hình chữ nhật.
        area (float): Diện tích của hình chữ nhật.
        perimeter (float): Chu vi của hình chữ nhật.
    """
    def __init__(self, **kwargs):
        """
        Khởi tạo các thuộc tính của hình chữ nhật dựa trên đầu vào.

        Args:
            kwargs: Các giá trị đầu vào như chiều dài, chiều rộng, đường chéo, diện tích, chu vi, ...
        """
        self.length = kwargs.get('length', None)  # Chiều dài hình chữ nhật
        self.width = kwargs.get('width', None)  # Chiều rộng hình chữ nhật
        self.diagonal = kwargs.get('diagonal', None)  # Đường chéo
        self.area = kwargs.get('area', None)  # Diện tích
        self.perimeter = kwargs.get('perimeter', None)  # Chu vi

        # Lưu trữ các bước giải và công thức đã dùng
        self.steps = []
        self.used_formulas = []

        # Định nghĩa mạng công thức
        self.formulas = [
            GeometryFormula(
                inputs=['length', 'width'],
                output='area',
                formula=lambda length, width: length * width,
                explanation="Diện tích hình chữ nhật bằng chiều dài nhân chiều rộng: S = a * b"
            ),
            GeometryFormula(
                inputs=['area'],
                output='length',
                formula=lambda area, width: area / width,
                explanation="Chiều dài hình chữ nhật bằng diện tích chia cho chiều rộng: a = S / b"
            ),
            GeometryFormula(
                inputs=['area'],
                output='width',
                formula=lambda area, length: area / length,
                explanation="Chiều rộng hình chữ nhật bằng diện tích chia cho chiều dài: b = S / a"
            ),
            GeometryFormula(
                inputs=['length', 'width'],
                output='perimeter',
                formula=lambda length, width: 2 * (length + width),
                explanation="Chu vi hình chữ nhật bằng 2 lần tổng chiều dài và chiều rộng: P = 2(a + b)"
            ),
            GeometryFormula(
                inputs=['perimeter'],
                output='length',
                formula=lambda perimeter, width: (perimeter / 2) - width,
                explanation="Chiều dài hình chữ nhật bằng chu vi chia 2 trừ chiều rộng: a = (P / 2) - b"
            ),
            GeometryFormula(
                inputs=['perimeter'],
                output='width',
                formula=lambda perimeter, length: (perimeter / 2) - length,
                explanation="Chiều rộng hình chữ nhật bằng chu vi chia 2 trừ chiều dài: b = (P / 2) - a"
            ),
            GeometryFormula(
                inputs=['length', 'width'],
                output='diagonal',
                formula=lambda length, width: math.sqrt(length ** 2 + width ** 2),
                explanation="Đường chéo hình chữ nhật bằng căn bậc hai của tổng bình phương chiều dài và chiều rộng: d = √(a² + b²)"
            ),
            GeometryFormula(
                inputs=['diagonal', 'length'],
                output='width',
                formula=lambda diagonal, length: math.sqrt(diagonal ** 2 - length ** 2),
                explanation="Chiều rộng hình chữ nhật bằng căn bậc hai của đường chéo bình phương trừ chiều dài bình phương: b = √(d² - a²)"
            ),
            GeometryFormula(
                inputs=['diagonal', 'width'],
                output='length',
                formula=lambda diagonal, width: math.sqrt(diagonal ** 2 - width ** 2),
                explanation="Chiều dài hình chữ nhật bằng căn bậc hai của đường chéo bình phương trừ chiều rộng bình phương: a = √(d² - b²)"
            ),
        ]

        self.validate_inputs()

    def validate_inputs(self):
        """
        Kiểm tra các mối quan hệ hình học giữa các giá trị đầu vào.

        Raises:
            ValueError: Nếu các giá trị không thỏa mãn quan hệ hình học.
        """
        if self.length and self.width and self.diagonal and not math.isclose(self.diagonal, math.sqrt(self.length ** 2 + self.width ** 2), rel_tol=1e-5):
            raise ValueError("Giá trị diagonal không phù hợp với length và width theo công thức d = √(a² + b²)")
        if self.length and self.perimeter and not math.isclose(self.perimeter, 2 * (self.length + self.width), rel_tol=1e-5):
            raise ValueError("Giá trị perimeter không phù hợp với length và width theo công thức P = 2(a + b)")
        if self.length and self.area and not math.isclose(self.area, self.length * self.width, rel_tol=1e-5):
            raise ValueError("Giá trị area không phù hợp với length và width theo công thức S = a * b")

    def solve(self) -> Dict[str, float]:
        """
        Tự động tính toán các giá trị chưa biết dựa trên các giá trị đầu vào.

        Returns:
            Dict[str, float]: Kết quả của các thuộc tính (chiều dài, chiều rộng, đường chéo, diện tích, chu vi).
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
            'length': f"{round(self.length, 2)} {unit}" if self.length is not None else None,
            'width': f"{round(self.width, 2)} {unit}" if self.width is not None else None,
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
                if var == "length":
                    var = "chiều dài"
                elif var == "width":
                    var = "chiều rộng"
                elif var == "area":
                    var = "diện tích"
                elif var == "perimeter":
                    var = "chu vi"
                elif var == "diagonal":
                    var = "đường chéo"
                
                solution += f"{var} = {val:.2f} cm\n"
            
            # Sửa phần tên biến đầu ra
            for var, val in step['output'].items():
                if var == "length":
                    var = "chiều dài"
                elif var == "width":
                    var = "chiều rộng"
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
        print("Trường hợp 1: Dữ liệu không hợp lệ (diagonal = 13 không hợp lệ với length = 5 và width = 4)")
        rectangle_invalid = HinhChuNhat(length=5, width=4, diagonal=13)  # Giá trị diagonal không hợp lệ
        results_invalid = rectangle_invalid.solve()
        print("Kết quả hình chữ nhật (không hợp lệ):")
        print(results_invalid)
        print("\nLời giải hình chữ nhật (không hợp lệ):")
        print(rectangle_invalid.get_solution_steps())

    except ValueError as e:
        print("Lỗi:", e)

    try:
        # Trường hợp 2: Dữ liệu hợp lệ
        print("\nTrường hợp 2: Dữ liệu hợp lệ (length = 5, width = 4)")
        rectangle_valid = HinhChuNhat(length=5, width=4)  # Dữ liệu hợp lệ
        results_valid = rectangle_valid.solve()
        print("Kết quả hình chữ nhật (hợp lệ):")
        print(results_valid)
        print("\nLời giải hình chữ nhật (hợp lệ):")
        print(rectangle_valid.get_solution_steps())

    except ValueError as e:
        print("Lỗi:", e)
