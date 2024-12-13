import math
from typing import Dict, List, Callable
from SolveSquare import *
class Triangle:
    """
    Represents a Triangle and performs geometric calculations.

    Attributes:
        side_length_a (float): Length of side a.
        side_length_b (float): Length of side b.
        side_length_c (float): Length of side c.
        alpha (float): Angle between side b and side c (in radians).
        beta (float): Angle between side a and side c (in radians).
        delta (float): Angle between side a and side b (in radians).
        area (float): Area of the triangle.
        perimeter (float): Perimeter of the triangle.
        height_a (float): Height corresponding to side a.
        height_b (float): Height corresponding to side b.
        height_c (float): Height corresponding to side c.
        inradius (float): Inradius of the triangle.
        circumradius (float): Circumradius of the triangle.
    """
    
    def __init__(self, semantic_data):
        """
        Initialize a Triangle with optional parameters.

        Keyword Args:
            side_a (float, optional): Length of side a.
            side_b (float, optional): Length of side b.
            side_c (float, optional): Length of side c.
            alpha (float, optional): Angle between side b and side c (in degrees).
            beta (float, optional): Angle between side a and side c (in degrees).
            delta (float, optional): Angle between side a and side b (in degrees).
            area (float, optional): Area of the triangle.
            perimeter (float, optional): Perimeter of the triangle.
            height_a (float, optional): Height corresponding to side a.
            height_b (float, optional): Height corresponding to side b.
            height_c (float, optional): Height corresponding to side c.
            inradius (float, optional): Inradius of the triangle.
            circumradius (float, optional): Circumradius of the triangle.
        """
        if semantic_data:
            analysis = semantic_data.get('semantic_analysis', {})
            shape = analysis.get('shape', None)
            known_factors = analysis.get('known_factors', {})
            self.requested_calculations = analysis.get('calculations', [])
            vietnamese_mapping = {
                    'cạnh a': 'side_length_a',
                    'cạnh b': 'side_length_b',
                    'cạnh c':'side_length_c',
                    'alpha': 'alpha',
                    'beta': 'beta',
                    'delta': 'delta',
                    'diện tích': 'area',
                    'chu vi': 'perimeter',
                    'đường cao a': 'height_a',
                    'đường cao b': 'height_b',
                    'đường cao c': 'height_c',
                    'bán kính đường tròn ngoại tiếp ': 'circumradius',
                    'bán kinh đường tròn nội tiếp': 'inradius',
                    'nửa chu vi': 'semi_perimeter',
                }
            self.side_length_a = None
            self.side_length_b = None
            self.side_length_c = None
            
            # Angles alpha, beta, delta (convert to radians if available)
            self.alpha = None
            self.beta = None
            self.delta = None
            
            # area abd perimeter
            self.area = None
            self.perimeter = None
            
            # Height
            self.height_a = None
            self.height_b = None
            self.height_c = None
            
            # inradius and circumradiu
            self.inradius = None
            self.circumradius = None
            
            # semi_perimeter
            self.semi_perimeter = None

            for key, value in known_factors.items():
                attribute = vietnamese_mapping.get(key)
                if attribute:
                    try:
                        # Loại bỏ đơn vị và chuyển đổi giá trị
                        setattr(self, attribute, float(value.replace("cm", "").replace("cm²", "").strip()))
                    except ValueError:
                        raise ValueError(f"Không thể phân tích giá trị cho {key}: {value}")

            if self.alpha!=None:
                self.alpha = math.radians(self.alpha)
            if self.beta!=None:  
                self.beta = math.radians(self.beta)
            if self.delta!=None:
                self.delta = math.radians(self.delta)

        else:
            return

        # Store solution steps and used formulas
        self.steps = []
        self.used_formulas = []

        # Define formula network
        self.formulas = [
            # 1. Tính chu vi và diện tích tam giác 
            #    Calculate the perimeter and area of ​​a triangle
            GeometryFormula(
                inputs=['side_length_a', 'side_length_b', 'side_length_c'],
                output='perimeter',
                formula=lambda a, b, c: a + b + c,
                explanation="Tính chu vi tam giác: P = a + b + c"
            ),
            GeometryFormula(
                inputs=['side_length_a', 'side_length_b', 'side_length_c'],
                output='semi_perimeter',
                formula=lambda a, b, c: (a + b + c) / 2,
                explanation="Tính nửa chu vi: s = (a + b + c) / 2"
            ),
            GeometryFormula(
                inputs=['side_length_a', 'side_length_b', 'side_length_c'],
                output='area',
                formula=lambda a, b, c: math.sqrt(
                    self.semi_perimeter * (self.semi_perimeter - a) *
                    (self.semi_perimeter - b) * (self.semi_perimeter - c)
                ) if self.semi_perimeter is not None else 0,  # Trả về 0 nếu bán chu vi chưa có giá trị
                explanation="Tính diện tích tam giác theo công thức Heron"
            ),
            # 2. Tính chiều cao từ các cạnh
            #    Calculate height from sides
            GeometryFormula(
                inputs=['side_length_a', 'area'],
                output='height_a',
                formula=lambda a, area: (2 * area) / a,
                explanation="Tính chiều cao ứng với cạnh a: h_a = 2S / a"
            ),
            GeometryFormula(
                inputs=['side_length_b', 'area'],
                output='height_b',
                formula=lambda b, area: (2 * area) / b,
                explanation="Tính chiều cao ứng với cạnh b: h_b = 2S / b"
            ),
            GeometryFormula(
                inputs=['side_length_c', 'area'],
                output='height_c',
                formula=lambda c, area: (2 * area) / c,
                explanation="Tính chiều cao ứng với cạnh c: h_c = 2S / c"
            ),
            # 3. Bán kính ngoại tiếp (Circumradius) và nội tiếp (Inradius)
            GeometryFormula(
                inputs=['side_length_a', 'side_length_b', 'side_length_c', 'area'],
                output='circumradius',
                formula=lambda a, b, c, area: (a * b * c) / (4 * area),
                explanation="Tính bán kính ngoại tiếp: R = (a * b * c) / (4S)"
            ),
            GeometryFormula(
                inputs=['side_length_a', 'side_length_b', 'side_length_c', 'area'],
                output='inradius',
                formula=lambda a, b, c, area: area / self.semi_perimeter,
                explanation="Tính bán kính nội tiếp: r = S / s"
            ),
            # 4. Tính các góc trong tam giác bằng định lý cosin
            #    Calculate angles in a triangle using the cosine theorem
            GeometryFormula(
                inputs=['side_length_a', 'side_length_b', 'side_length_c'],
                output='alpha',
                formula=lambda a, b, c: math.acos((b**2 + c**2 - a**2) / (2 * b * c)),
                explanation="Tính góc alpha: cos(α) = (b² + c² - a²) / (2bc)"
            ),
            GeometryFormula(
                inputs=['side_length_a', 'side_length_b', 'side_length_c'],
                output='beta',
                formula=lambda a, b, c: math.acos((a**2 + c**2 - b**2) / (2 * a * c)),
                explanation="Tính góc beta: cos(β) = (a² + c² - b²) / (2ac)"
            ),
            GeometryFormula(
                inputs=['side_length_a', 'side_length_b', 'side_length_c'],
                output='delta',
                formula=lambda a, b, c: math.acos((a**2 + b**2 - c**2) / (2 * a * b)),
                explanation="Tính góc delta: cos(δ) = (a² + b² - c²) / (2ab)"
            ),
            # # 5. Các công thức đặc biệt cho Tam giác Vuông
            # #    Special Formulas for Right Triangles
            # GeometryFormula(
            #     inputs=['side_length_a', 'side_length_b','alpha'],
            #     output='c',
            #     formula=lambda a, b,alpha: math.sqrt(a**2 + b**2) if alpha==90 else None,
            #     explanation="Tính cạnh huyền trong tam giác vuông: c = √(a² + b²)"
            # ),
            # GeometryFormula(
            #     inputs=['side_length_a', 'side_length_b', 'side_length_c'],
            #     output='is_right_triangle',
            #     formula=lambda a, b, c: math.isclose(a**2 + b**2, c**2),
            #     explanation="Kiểm tra tam giác vuông: a² + b² = c²"
            # ),
            # # 6. Tam giác vuông cân
            # #    Isosceles right triangle
            # GeometryFormula(
            #     inputs=['side_length_a'],
            #     output='area',
            #     formula=lambda a: 0.5 * a**2,
            #     explanation="Diện tích tam giác vuông cân: S = 1/2 * a²"
            # ),
            # GeometryFormula(
            #     inputs=['side_length_a'],
            #     output='circumradius',
            #     formula=lambda a: a / math.sqrt(2),
            #     explanation="Bán kính ngoại tiếp tam giác vuông cân: R = a / √2"
            # ),
            # GeometryFormula(
            #     inputs=['side_length_a'],
            #     output='inradius',
            #     formula=lambda a: a / 2,
            #     explanation="Bán kính nội tiếp tam giác vuông cân: r = a / 2"
            # ),
            # 7. Tam giác đều
            # GeometryFormula(
            #     inputs=['side_length_a'],
            #     output='area',
            #     formula=lambda a: (math.sqrt(3) / 4) * a**2,
            #     explanation="Diện tích tam giác đều: S = (√3 / 4) * a²"
            # ),
            # GeometryFormula(
            #     inputs=['side_length_a'],
            #     output='height',
            #     formula=lambda a: (math.sqrt(3) / 2) * a,
            #     explanation="Chiều cao tam giác đều: h = (√3 / 2) * a"
            # ),
            # GeometryFormula(
            #     inputs=['side_length_a'],
            #     output='circumradius',
            #     formula=lambda a: a / math.sqrt(3),
            #     explanation="Bán kính ngoại tiếp tam giác đều: R = a / √3"
            # ),
            # GeometryFormula(
            #     inputs=['side_length_a'],
            #     output='inradius',
            #     formula=lambda a: a / (2 * math.sqrt(3)),
            #     explanation="Bán kính nội tiếp tam giác đều: r = a / (2√3)"
            # ),
            # # 8. Các công thức bổ sung cho tam giác vuông trong hình học học
            # #    Additional formulas for right triangles in geometry
            # GeometryFormula(
            #     inputs=['side_length_a', 'side_length_b', 'area'],
            #     output='angle',
            #     formula=lambda a, b, area: math.acos((2 * area) / (a * b)),
            #     explanation="Tính góc giữa hai cạnh trong tam giác vuông từ diện tích"
            # ),
            # GeometryFormula(
            #     inputs=['side_length_a', 'side_length_b', 'height_a'],
            #     output='area_from_height',
            #     formula=lambda a, b, h: 0.5 * a * h,
            #     explanation="Tính diện tích từ chiều cao và cạnh trong tam giác vuông"
            # ),
            # 9. Tính bán kính nội tiếp và ngoại tiếp từ các công thức đặc biệt
            #    Calculate inscribed and circumscribed radius from special formulas
            GeometryFormula(
                inputs=['side_length_a', 'side_length_b', 'side_length_c', 'semi_perimeter'],
                output='circumradius',
                formula=lambda a, b, c, s: (a * b * c) / (4 * math.sqrt(s * (s - a) * (s - b) * (s - c))),
                explanation="Bán kính ngoại tiếp từ bán kính nửa chu vi"
            ),
        ]

        self.validate_inputs()

    def validate_inputs(self):
        """
        Validates the input values based on the geometric relationships between them.

        This method checks the following conditions:
        - Whether the sides of the triangle satisfy the triangle inequality.
        - Whether the area matches the sides of the triangle using Heron's formula.
        - Whether the circumradius matches the sides and area of the triangle.
        - Whether the inradius matches the sides and area of the triangle.

        If any of these conditions are not satisfied, a `ValueError` will be raised with an appropriate message.

        Raises:
            ValueError: If one or more input values are invalid or do not satisfy the geometric relationships.
        """     
        # Check the sides of the triangle
        if self.side_length_a and self.side_length_b and self.side_length_c:
            a = self.side_length_a
            b = self.side_length_b
            c = self.side_length_c
            # Check triangle condition
            if not (a + b > c and a + c > b and b + c > a):
                raise ValueError(f"Các cạnh a={a}, b={b}, c={c} không thỏa mãn bất đẳng thức tam giác.")
        
        # Check the area of ​​a triangle with its sides
        if self.side_length_a and self.side_length_b and self.side_length_c and self.area:
            semi_perimeter = (self.side_length_a + self.side_length_b + self.side_length_c) / 2
            expected_area = math.sqrt(
                semi_perimeter * (semi_perimeter - self.side_length_a) *
                (semi_perimeter - self.side_length_b) * (semi_perimeter - self.side_length_c)
            )
            if not math.isclose(self.area, expected_area, rel_tol=1e-5):
                raise ValueError(f"Giá trị diện tích không phù hợp với các cạnh a={self.side_length_a}, b={self.side_length_b}, c={self.side_length_c}")

        # Check the circumradius from the edges
        if self.side_length_a and self.side_length_b and self.side_length_c and self.circumradius:
            expected_circumradius = (self.side_length_a * self.side_length_b * self.side_length_c) / \
                (4 * self.area)
            if not math.isclose(self.circumradius, expected_circumradius, rel_tol=1e-5):
                raise ValueError(f"Bán kính ngoại tiếp không phù hợp với các cạnh a={self.side_length_a}, b={self.side_length_b}, c={self.side_length_c} và diện tích {self.area}")

        # Check inradius from edges
        if self.side_length_a and self.side_length_b and self.side_length_c and self.inradius:
            semi_perimeter = (self.side_length_a + self.side_length_b + self.side_length_c) / 2
            expected_inradius = self.area / semi_perimeter
            if not math.isclose(self.inradius, expected_inradius, rel_tol=1e-5):
                raise ValueError(f"Bán kính nội tiếp không phù hợp với các cạnh a={self.side_length_a}, b={self.side_length_b}, c={self.side_length_c} và diện tích {self.area}")


    def solve(self) -> Dict[str, float]:
        """
        Automatically calculates missing values based on the provided inputs.

        This method goes through a list of formulas and checks if all the required inputs are available.
        When all inputs for a formula are found, it calculates the result, stores it, and logs the calculation step.
        The process continues until no more new values can be calculated.

        It also ensures that the semi-perimeter is calculated before being used in any formula that requires it.

        Returns:
            Dict[str, float]: A dictionary containing the results of the calculated values, 
            such as side lengths, diagonals, area, and perimeter.
        """
        while True:
            found_new = False  

           # Iterate through all the formulas in the list
            for formula in self.formulas:
                # Check if all formula inputs have values
                if all(hasattr(self, inp) and getattr(self, inp) is not None for inp in formula.inputs):
                    # If the output value has not been calculated
                    if not hasattr(self, formula.output) or getattr(self, formula.output) is None:
                       # Check if the semi-perimeter has a valid value

                        
                        # Get the values ​​of the inputs
                        inputs = [getattr(self, inp) for inp in formula.inputs]
                        # Calculate the result
                        result = formula.formula(*inputs)
                        # Save the result to the object
                        setattr(self, formula.output, result)

                        # Save information about this calculation step
                        step = {
                            'formula': formula.explanation,
                            'inputs': {inp: getattr(self, inp) for inp in formula.inputs},
                            'output': {formula.output: result}
                        }
                        self.steps.append(step)  # Add step to steps list
                        self.used_formulas.append(formula)  # Add formula to list of used formulas
                        found_new = True  # Mark as found new value

            # If there are no more formulas that can calculate a new value, exit the loop.p
            if not found_new:
                break

        # Trả về kết quả cuối cùng
        return self.get_results()


    def get_results(self) -> Dict[str, str]:
        """
        Get final results with measurement units for all possible formulas and cases.

        Returns:
            Dict[str, str]: Formatted results with units for all calculated values.
        """
        unit = "cm"  # Can change if needed
        results = {}

        #Iterate through the formulas and get the corresponding result values
        if hasattr(self, 'side_length_a') and self.side_length_a is not None:
            results['side_length_a'] = f"{round(self.side_length_a, 2)} {unit}"
        
        if hasattr(self, 'side_length_b') and self.side_length_b is not None:
            results['side_length_b'] = f"{round(self.side_length_b, 2)} {unit}"
        
        if hasattr(self, 'side_length_c') and self.side_length_c is not None:
            results['side_length_c'] = f"{round(self.side_length_c, 2)} {unit}"
        
        if hasattr(self, 'diagonal') and self.diagonal is not None:
            results['diagonal'] = f"{round(self.diagonal, 2)} {unit}"

        if hasattr(self, 'area') and self.area is not None:
            results['area'] = f"{round(self.area, 2)} {unit}²"

        if hasattr(self, 'perimeter') and self.perimeter is not None:
            results['perimeter'] = f"{round(self.perimeter, 2)} {unit}"
        
        if hasattr(self, 'circumradius') and self.circumradius is not None:
            results['circumradius'] = f"{round(self.circumradius, 2)} {unit}"
        
        if hasattr(self, 'inradius') and self.inradius is not None:
            results['inradius'] = f"{round(self.inradius, 2)} {unit}"
        
        if hasattr(self, 'height_a') and self.height_a is not None:
            results['height_a'] = f"{round(self.height_a, 2)} {unit}"

        if hasattr(self, 'height_b') and self.height_b is not None:
            results['height_b'] = f"{round(self.height_b, 2)} {unit}"

        if hasattr(self, 'height_c') and self.height_c is not None:
            results['height_c'] = f"{round(self.height_c, 2)} {unit}"
        
        if hasattr(self, 'alpha') and self.alpha is not None:
            results['alpha'] = f"{round(math.degrees(self.alpha), 2)}°"  # Convert radian to degree

        if hasattr(self, 'beta') and self.beta is not None:
            results['beta'] = f"{round(math.degrees(self.beta), 2)}°"    # Convert radian to degree

        if hasattr(self, 'delta') and self.delta is not None:
            results['delta'] = f"{round(math.degrees(self.delta), 2)}°"  # Convert radian to degree

        if hasattr(self, 'is_right_triangle') and self.is_right_triangle is not None:
            results['is_right_triangle'] = "Yes" if self.is_right_triangle else "No"

         # Return the result as a dictionary
        return results


    def get_solution_steps(self) -> str:
        """
        Return detailed solution steps for a triangle.

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
                    var = "độ dài cạnh a"
                elif var == "side_length_b":
                    var = "độ dài cạnh b"
                elif var == "side_length_c":
                    var = "độ dài cạnh c"
                elif var == "semi_perimeter":
                    var = "nửa chu vi"
                elif var == "area":
                    var = "diện tích"
                elif var == "perimeter":
                    var = "chu vi"
                elif var == "circumradius":
                    var = "bán kính ngoại tiếp"
                elif var == "inradius":
                    var = "bán kính nội tiếp"
                elif var == "height_a":
                    var = "chiều cao a"
                elif var == "height_b":
                    var = "chiều cao b"
                elif var == "height_c":
                    var = "chiều cao c"
                elif var == "alpha":
                    var = "góc α"
                elif var == "beta":
                    var = "góc β"
                elif var == "delta":
                    var = "góc delta"
                
                solution += f"{var} = {val:.2f} cm\n"
            
            # Fix output variable names
            for var, val in step['output'].items():
                if var == "side_length_a":
                    var = "độ dài cạnh a"
                elif var == "side_length_b":
                    var = "độ dài cạnh b"
                elif var == "side_length_c":
                    var = "độ dài cạnh c"
                elif var == "semi_perimeter":
                    var = "nửa chu vi"
                elif var == "area":
                    var = "diện tích"
                elif var == "perimeter":
                    var = "chu vi"
                elif var == "circumradius":
                    var = "bán kính ngoại tiếp"
                elif var == "inradius":
                    var = "bán kính nội tiếp"
                elif var == "height_a":
                    var = "chiều cao a"
                elif var == "height_b":
                    var = "chiều cao b"
                elif var == "height_c":
                    var = "chiều cao c"
                elif var == "alpha":
                    var = "góc α"
                elif var == "beta":
                    var = "góc β"
                elif var == "gamma":
                    var = "góc γ"
                
                solution += f"=> {var} = {val:.2f} cm\n"
            
            solution += "\n"
        
        return solution