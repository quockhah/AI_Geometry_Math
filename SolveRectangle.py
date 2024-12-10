import math
from typing import Dict, List, Callable


class GeometryFormula:
    """
    Represents a geometry formula with its input, output, calculation, and explanation.

    Attributes:
        inputs (List[str]): List of input variables for the formula.
        output (str): Output variable of the formula.
        formula (Callable): Function to execute the formula.
        explanation (str): Explanation of how the formula works.
    """
    def __init__(self, inputs: List[str], output: str, formula: Callable, explanation: str):
        """
        Initialize a geometry formula.

        Args:
            inputs (List[str]): Input variables for the formula.
            output (str): Output variable of the formula.
            formula (Callable): Function to calculate the formula.
            explanation (str): Detailed explanation of the formula.
        """
        self.inputs = inputs
        self.output = output
        self.formula = formula
        self.explanation = explanation


class Rectangle:
    """
    Represents a rectangle and performs geometric calculations.

    Attributes:
        side_length_a (float): Length of the rectangle.
        side_width_b (float): Width of the rectangle.
        diagonal (float): Diagonal of the rectangle.
        area (float): Area of the rectangle.
        perimeter (float): Perimeter of the rectangle.
    """
    def __init__(self, semantic_data):
        """
        Initialize a rectangle with optional parameters.

        Keyword Args:
            length (float, optional): Length of the rectangle.
            width (float, optional): Width of the rectangle.
            diagonal (float, optional): Diagonal of the rectangle.
            area (float, optional): Area of the rectangle.
            perimeter (float, optional): Perimeter of the rectangle.
        """

        if semantic_data:
            # Trích xuất thông tin phân tích ngữ nghĩa
            analysis = semantic_data.get('semantic_analysis', {})
            shape = analysis.get('shape', None)
            known_factors = analysis.get('known_factors', {})
            self.requested_calculations = analysis.get('calculations', [])


            vietnamese_mapping = {
                    'chiều dài': 'side_length_a',
                    'chiều rộng':'side_width_b',
                    'đường chéo': 'diagonal',
                    'diện tích': 'area',
                    'chu vi': 'perimeter'
                }

            # Khởi tạo các giá trị mặc định
            self.side_length_a = None
            self.side_width_b=None
            self.diagonal = None
            self.area = None
            self.perimeter = None

                # Gán lại giá trị từ semantic data nếu tồn tại
            for key, value in known_factors.items():
                attribute = vietnamese_mapping.get(key)
                if attribute:
                    try:
                        # Loại bỏ đơn vị và chuyển đổi giá trị
                        setattr(self, attribute, float(value.replace("cm", "").replace("cm²", "").strip()))
                    except ValueError:
                        raise ValueError(f"Không thể phân tích giá trị cho {key}: {value}")
        else:
            return

        # Store solution steps and used formulas
        self.steps = []
        self.used_formulas = []

        # Define formula network
        self.formulas = [
            # Diện tích (Area)
            GeometryFormula(
                inputs=['side_length_a', 'side_width_b'],
                output='area',
                formula=lambda side_length_a, side_width_b: side_length_a * side_width_b,
                explanation="Tính diện tích hình chữ nhật: S = a * b (Biết chiều dài và chiều rộng)"
            ),
            GeometryFormula(
                inputs=['area','side_width_b'],
                output='side_length_a',
                formula=lambda area, side_width_b: area / side_width_b,
                explanation="Tính chiều dài từ diện tích và chiều rộng: a = S / b"
            ),
            GeometryFormula(
                inputs=['area','side_length_a'],
                output='side_width_b',
                formula=lambda area, side_length_a: area / side_length_a,
                explanation="Tính chiều rộng từ diện tích và chiều dài: b = S / a"
            ),

            # Chu vi (Perimeter)
            GeometryFormula(
                inputs=['side_length_a','side_width_b'],
                output='perimeter',
                formula=lambda side_length_a, side_width_b: 2 * (side_length_a + side_width_b),
                explanation="Tính chu vi hình chữ nhật: P = 2(a + b) (Biết chiều dài và chiều rộng)"
            ),
            GeometryFormula(
                inputs=['perimeter','side_width_b'],
                output='side_length_a',
                formula=lambda perimeter, side_width_b: (perimeter / 2) - side_width_b,
                explanation="Tính chiều dài từ chu vi và chiều rộng: a = (P / 2) - b"
            ),
            GeometryFormula(
                inputs=['perimeter','side_length_a'],
                output='side_width_b',
                formula=lambda perimeter, side_length_a: (perimeter / 2) - side_length_a,
                explanation="Tính chiều rộng từ chu vi và chiều dài: b = (P / 2) - a"
            ),

            # Đường chéo (Diagonal)
            GeometryFormula(
                inputs=['side_length_a', 'side_width_b'],
                output='diagonal',
                formula=lambda side_length_a, side_width_b: math.sqrt(side_length_a ** 2 + side_width_b ** 2),
                explanation="Tính độ dài đường chéo: d = √(a² + b²) (Biết chiều dài và chiều rộng)"
            ),
            GeometryFormula(
                inputs=['diagonal', 'side_length_a'],
                output='side_width_b',
                formula=lambda diagonal, side_length_a: math.sqrt(diagonal ** 2 - side_length_a ** 2),
                explanation="Tính chiều rộng từ đường chéo và chiều dài: b = √(d² - a²)"
            ),
            GeometryFormula(
                inputs=['diagonal', 'side_width_b'],
                output='side_length_a',
                formula=lambda diagonal, side_width_b: math.sqrt(diagonal ** 2 - side_width_b ** 2),
                explanation="Tính chiều dài từ đường chéo và chiều rộng: a = √(d² - b²)"
            ),

            # Complex formulas: Deriving side from multiple attributes
            GeometryFormula(
                inputs=['perimeter', 'diagonal'],
                output='side_length_a',
                formula=lambda perimeter, diagonal: math.sqrt(
                    ((perimeter / 2) ** 2 + (diagonal ** 2 / 4)) - (perimeter / 2)
                ),
                explanation="Tính chiều dài từ chu vi và đường chéo: a = √((P/2)² + (d²/4)) - (P/2)"
            ),
            GeometryFormula(
                inputs=['perimeter', 'diagonal'],
                output='side_width_b',
                formula=lambda perimeter, diagonal: math.sqrt(
                    ((perimeter / 2) ** 2 + (diagonal ** 2 / 4)) - (perimeter / 2)
                ),
                explanation="Tính chiều rộng từ chu vi và đường chéo: b = √((P/2)² + (d²/4)) - (P/2)"
            ),
            GeometryFormula(
                inputs=['diagonal', 'area'],
                output='side_length_a',
                formula=lambda diagonal, area: math.sqrt(
                    (diagonal ** 2 + math.sqrt(diagonal ** 4 - 4 * area ** 2)) / 2
                ),
                explanation="Tính chiều dài từ đường chéo và diện tích: a = √((d² + √(d⁴ - 4S²)) / 2)"
            ),
            GeometryFormula(
                inputs=['diagonal', 'area'],
                output='side_width_b',
                formula=lambda diagonal, area: math.sqrt(
                    (diagonal ** 2 - math.sqrt(diagonal ** 4 - 4 * area ** 2)) / 2
                ),
                explanation="Tính chiều rộng từ đường chéo và diện tích: b = √((d² - √(d⁴ - 4S²)) / 2)"
            )
        ]

        self.validate_inputs()

    def validate_inputs(self):
        """
        Validate geometric relationships between input values.
    
        Raises:
            ValueError: If input values do not satisfy geometric relationships.
        """
        # Validate diagonal using Pythagorean theorem
        if self.side_length_a and self.side_width_b and self.diagonal and not math.isclose(
            self.diagonal, 
            math.sqrt(self.side_length_a ** 2 + self.side_width_b ** 2), 
            rel_tol=1e-5
        ):
            raise ValueError("Giá trị đường chéo không phù hợp với chiều dài và chiều rộng theo công thức d = √(a² + b²)")

        # Validate perimeter calculation
        if self.side_length_a and self.side_width_b and self.perimeter and not math.isclose(
            self.perimeter, 
            2 * (self.side_length_a + self.side_width_b), 
            rel_tol=1e-5
        ):
            raise ValueError("Giá trị chu vi không phù hợp với chiều dài và chiều rộng theo công thức P = 2(a + b)")

        # Validate area calculation
        if self.side_length_a and self.side_width_b and self.area and not math.isclose(
            self.area, 
            self.side_length_a * self.side_width_b, 
            rel_tol=1e-5
        ):
            raise ValueError("Giá trị diện tích không phù hợp với chiều dài và chiều rộng theo công thức S = a * b")

    def solve(self) -> Dict[str, float]:
        """
        Automatically calculate unknown values based on input values.

        Returns:
            Dict[str, float]: Results of attributes (length, width, diagonal, area, perimeter).
        """
        while True:
            found_new = False

            for formula in self.formulas:
                # Check if all input variables are known
                if all(hasattr(self, inp) and getattr(self, inp) is not None for inp in formula.inputs):
                    # If output variable is not yet calculated
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
        Get final results with measurement units.

        Returns:
            Dict[str, str]: Formatted results with units.
        """
        unit = "cm"  # Can change unit if needed
        return {
            'length': f"{round(self.side_length_a, 2)} {unit}" if self.side_length_a is not None else None,
            'width': f"{round(self.side_width_b, 2)} {unit}" if self.side_width_b is not None else None,
            'diagonal': f"{round(self.diagonal, 2)} {unit}" if self.diagonal is not None else None,
            'area': f"{round(self.area, 2)} {unit}²" if self.area is not None else None,
            'perimeter': f"{round(self.perimeter, 2)} {unit}" if self.perimeter is not None else None
        }

    def get_solution_steps(self) -> str:
        """
        Return detailed solution steps.

        Returns:
            str: Detailed solution steps as a string.
        """
        solution = "Lời giải chi tiết:\n\n"
        for i, step in enumerate(self.steps, 1):
            solution += f"Bước {i}:\n"
            solution += f"Công thức: {step['formula']}\n"
            solution += "Thay số:\n"
            
            # Fix input variable names
            for var, val in step['inputs'].items():
                if var == "side_length_a":
                    var = "chiều dài"
                elif var == "side_width_b":
                    var = "chiều rộng"
                elif var == "area":
                    var = "diện tích"
                elif var == "perimeter":
                    var = "chu vi"
                elif var == "diagonal":
                    var = "đường chéo"
                
                solution += f"{var} = {val:.2f} cm\n"
            
            # Fix output variable names
            for var, val in step['output'].items():
                if var == "side_length_a":
                    var = "chiều dài"
                elif var == "side_width_b":
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
