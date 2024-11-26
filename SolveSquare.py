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


class Square:
    """
    Represents a square and performs geometric calculations.

    Attributes:
        side_length_a (float): Length of the square's side.
        diagonal (float): Diagonal of the square.
        area (float): Area of the square.
        perimeter (float): Perimeter of the square.
    """
    def __init__(self, **kwargs):
        """
        Initialize a square with optional parameters.

        Keyword Args:
            side (float, optional): Length of the square's side.
            diagonal (float, optional): Diagonal of the square.
            area (float, optional): Area of the square.
            perimeter (float, optional): Perimeter of the square.
        """
        self.side_length_a = kwargs.get('side', None)  # Square side length
        self.diagonal = kwargs.get('diagonal', None)  # Diagonal
        self.area = kwargs.get('area', None)  # Area
        self.perimeter = kwargs.get('perimeter', None)  # Perimeter

        # Store solution steps and used formulas
        self.steps = []
        self.used_formulas = []

        # Define formula network
        self.formulas = [
            # Side length from various inputs
            GeometryFormula(
                inputs=['area'],
                output='side_length_a',
                formula=lambda area: math.sqrt(area),
                explanation="Tính độ dài cạnh từ diện tích: a = √S"
            ),
            GeometryFormula(
                inputs=['perimeter'],
                output='side_length_a',
                formula=lambda perimeter: perimeter / 4,
                explanation="Tính độ dài cạnh từ chu vi: a = P / 4"
            ),
            GeometryFormula(
                inputs=['diagonal'],
                output='side_length_a',
                formula=lambda diagonal: diagonal / math.sqrt(2),
                explanation="Tính độ dài cạnh từ đường chéo: a = d / √2"
            ),

            # Area calculations
            GeometryFormula(
                inputs=['side_length_a'],
                output='area',
                formula=lambda side_length_a: side_length_a ** 2,
                explanation="Tính diện tích hình vuông: S = a²"
            ),

            # Perimeter calculations
            GeometryFormula(
                inputs=['side_length_a'],
                output='perimeter',
                formula=lambda side_length_a: 4 * side_length_a,
                explanation="Tính chu vi hình vuông: P = 4a"
            ),

            # Diagonal calculations
            GeometryFormula(
                inputs=['side_length_a'],
                output='diagonal',
                formula=lambda side_length_a: side_length_a * math.sqrt(2),
                explanation="Tính đường chéo hình vuông: d = a√2"
            ),

            # Complex formulas: Deriving side from multiple attributes
            GeometryFormula(
                inputs=['diagonal', 'area'],
                output='side_length_a',
                formula=lambda diagonal, area: math.sqrt(
                    (diagonal ** 2 + math.sqrt(diagonal ** 4 - 4 * area ** 2)) / 2
                ),
                explanation="Tính độ dài cạnh từ đường chéo và diện tích"
            ),
            GeometryFormula(
                inputs=['diagonal', 'perimeter'],
                output='side_length_a',
                formula=lambda diagonal, perimeter: math.sqrt(
                    ((perimeter / 4) ** 2 + (diagonal ** 2 / 4)) - (perimeter / 4)
                ),
                explanation="Tính độ dài cạnh từ đường chéo và chu vi"
            )
        ]

        self.validate_inputs()

    def validate_inputs(self):
        """
        Validate geometric relationships between input values.

        Raises:
            ValueError: If input values do not satisfy geometric relationships.
        """
        # Diagonal validation
        if self.side_length_a and self.diagonal and not math.isclose(
            self.diagonal, 
            self.side_length_a * math.sqrt(2), 
            rel_tol=1e-5
        ):
            raise ValueError("Giá trị đường chéo không phù hợp với độ dài cạnh theo công thức d = a√2")

        # Area validation
        if self.side_length_a and self.area and not math.isclose(
            self.area, 
            self.side_length_a ** 2, 
            rel_tol=1e-5
        ):
            raise ValueError("Giá trị diện tích không phù hợp với độ dài cạnh theo công thức S = a²")

        # Perimeter validation
        if self.side_length_a and self.perimeter and not math.isclose(
            self.perimeter, 
            4 * self.side_length_a, 
            rel_tol=1e-5
        ):
            raise ValueError("Giá trị chu vi không phù hợp với độ dài cạnh theo công thức P = 4a")

    def solve(self) -> Dict[str, float]:
        """
        Automatically calculate unknown values based on input values.

        Returns:
            Dict[str, float]: Results of attributes (side, diagonal, area, perimeter).
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
            'side': f"{round(self.side_length_a, 2)} {unit}" if self.side_length_a is not None else None,
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
                    var = "độ dài cạnh"
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
                    var = "độ dài cạnh"
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
    # Test cases
    try:
        # Case 1: Invalid data
        print("Trường hợp 1: Dữ liệu không hợp lệ (đường chéo = 13 không hợp lệ với độ dài cạnh = 5)")
        square_invalid = Square(side=5, diagonal=13)  # Invalid diagonal value
        results_invalid = square_invalid.solve()
        print("Kết quả hình vuông (không hợp lệ):")
        print(results_invalid)
        print("\nLời giải hình vuông (không hợp lệ):")
        print(square_invalid.get_solution_steps())

    except ValueError as e:
        print("Lỗi:", e)

    try:
        # Case 2: Valid data
        print("\nTrường hợp 2: Dữ liệu hợp lệ (độ dài cạnh = 5)")
        square_valid = Square(side=5)  # Valid Data
        results_valid = square_valid.solve()
        print("Kết quả hình vuông (hợp lệ):")
        print(results_valid)
        print("\nLời giải hình vuông (hợp lệ):")
        print(square_valid.get_solution_steps())

    except ValueError as e:
        print("Lỗi:", e)