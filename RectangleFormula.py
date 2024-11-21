import math

class Rectangle:
    def __init__(self, **kwargs):
        """
        Khởi tạo các giá trị cho hình chữ nhật.
        :param kwargs: Các tham số đầu vào gồm chiều dài, chiều rộng, diện tích, chu vi, và đường chéo.
        """
        self.length = kwargs.get('length', None)  # Chiều dài
        self.width = kwargs.get('width', None)  # Chiều rộng
        self.area = kwargs.get('area', None)  # Diện tích
        self.perimeter = kwargs.get('perimeter', None)  # Chu vi
        self.diagonal = kwargs.get('diagonal', None)  # Đường chéo
        self.solution_steps = []  # Danh sách các bước giải
        self.calculated_values = []  # Các giá trị đã tính
        self.steps = 0  # Biến đếm số bước

    def Formula_1(self, changes):
        """
        Tính diện tích, chu vi, và đường chéo nếu chưa có.
        :param changes: Biến kiểm tra xem có sự thay đổi nào trong quá trình tính toán không.
        :return: Trả về True nếu có sự thay đổi, ngược lại False.
        """
        if self.length and self.width and not self.area:
            self.area = self.length * self.width  # Tính diện tích
            self.solution_steps.append([self.steps + 1, f"Tính diện tích: {self.length} * {self.width} = {self.area}"])
            self.calculated_values.append([self.steps + 1, "area"])
            changes = True
            self.steps += 1

        if self.length and self.width and not self.perimeter:
            self.perimeter = 2 * (self.length + self.width)  # Tính chu vi
            self.solution_steps.append([self.steps + 1, f"Tính chu vi: 2 * ({self.length} + {self.width}) = {self.perimeter}"])
            self.calculated_values.append([self.steps + 1, "perimeter"])
            changes = True
            self.steps += 1

        if self.length and self.width and not self.diagonal:
            self.diagonal = math.sqrt(self.length**2 + self.width**2)  # Tính đường chéo
            self.diagonal = round(self.diagonal, 2)  # Làm tròn đến 2 chữ số thập phân
            self.solution_steps.append([self.steps + 1, f"Tính đường chéo: √({self.length}² + {self.width}²) = {self.diagonal}"])
            self.calculated_values.append([self.steps + 1, "diagonal"])
            changes = True
            self.steps += 1

        return changes

    def Formula_2(self, changes):
        """
        Tính chiều dài hoặc chiều rộng từ diện tích, chu vi, hoặc đường chéo nếu chưa có.
        :param changes: Biến kiểm tra xem có sự thay đổi nào trong quá trình tính toán không.
        :return: Trả về True nếu có sự thay đổi, ngược lại False.
        """
        if self.area and self.width and not self.length:
            self.length = self.area / self.width  # Tính chiều dài từ diện tích
            self.solution_steps.append([self.steps + 1, f"Tính chiều dài: {self.area} / {self.width} = {self.length}"])
            self.calculated_values.append([self.steps + 1, "length"])
            changes = True
            self.steps += 1

        if self.area and self.length and not self.width:
            self.width = self.area / self.length  # Tính chiều rộng từ diện tích
            self.solution_steps.append([self.steps + 1, f"Tính chiều rộng: {self.area} / {self.length} = {self.width}"])
            self.calculated_values.append([self.steps + 1, "width"])
            changes = True
            self.steps += 1

        if self.perimeter and self.width and not self.length:
            self.length = (self.perimeter / 2) - self.width  # Tính chiều dài từ chu vi
            self.solution_steps.append([self.steps + 1, f"Tính chiều dài: ({self.perimeter} / 2) - {self.width} = {self.length}"])
            self.calculated_values.append([self.steps + 1, "length"])
            changes = True
            self.steps += 1

        if self.perimeter and self.length and not self.width:
            self.width = (self.perimeter / 2) - self.length  # Tính chiều rộng từ chu vi
            self.solution_steps.append([self.steps + 1, f"Tính chiều rộng: ({self.perimeter} / 2) - {self.length} = {self.width}"])
            self.calculated_values.append([self.steps + 1, "width"])
            changes = True
            self.steps += 1

        if self.diagonal and self.length and not self.width:
            self.width = math.sqrt(self.diagonal**2 - self.length**2)  # Tính chiều rộng từ đường chéo
            self.solution_steps.append([self.steps + 1, f"Tính chiều rộng: √({self.diagonal}² - {self.length}²) = {self.width}"])
            self.calculated_values.append([self.steps + 1, "width"])
            changes = True
            self.steps += 1

        if self.diagonal and self.width and not self.length:
            self.length = math.sqrt(self.diagonal**2 - self.width**2)  # Tính chiều dài từ đường chéo
            self.solution_steps.append([self.steps + 1, f"Tính chiều dài: √({self.diagonal}² - {self.width}²) = {self.length}"])
            self.calculated_values.append([self.steps + 1, "length"])
            changes = True
            self.steps += 1

        return changes

    def Formula_3(self, changes):
        """
        Tính chu vi hoặc diện tích từ chiều dài và chiều rộng nếu chưa có.
        :param changes: Biến kiểm tra xem có sự thay đổi nào trong quá trình tính toán không.
        :return: Trả về True nếu có sự thay đổi, ngược lại False.
        """
        if self.length and self.width and not self.area:
            self.area = self.length * self.width  # Diện tích từ chiều dài và chiều rộng
            self.solution_steps.append([self.steps + 1, f"Tính diện tích: {self.length} * {self.width} = {self.area}"])
            self.calculated_values.append([self.steps + 1, "area"])
            changes = True
            self.steps += 1

        if self.length and self.width and not self.perimeter:
            self.perimeter = 2 * (self.length + self.width)  # Chu vi từ chiều dài và chiều rộng
            self.solution_steps.append([self.steps + 1, f"Tính chu vi: 2 * ({self.length} + {self.width}) = {self.perimeter}"])
            self.calculated_values.append([self.steps + 1, "perimeter"])
            changes = True
            self.steps += 1

        return changes

    def Formula_4(self, changes):
        """
        Tính diện tích nếu chưa có.
        :param changes: Biến kiểm tra xem có sự thay đổi nào trong quá trình tính toán không.
        :return: Trả về True nếu có sự thay đổi, ngược lại False.
        """
        if self.length and self.width and not self.area:
            self.area = self.length * self.width  # Diện tích từ chiều dài và chiều rộng
            self.solution_steps.append([self.steps + 1, f"Tính diện tích: {self.length} * {self.width} = {self.area}"])
            self.calculated_values.append([self.steps + 1, "area"])
            changes = True
            self.steps += 1

        if self.length and self.diagonal and not self.area:
            self.area = self.length * self.width  # Diện tích từ chiều dài và chiều rộng
            self.solution_steps.append([self.steps + 1, f"Tính diện tích: {self.length} * {self.width} = {self.area}"])
            self.calculated_values.append([self.steps + 1, "area"])
            changes = True
            self.steps += 1

        return changes

    def solve(self):
        """
        Tính toán tất cả các giá trị cần thiết cho hình chữ nhật.
        :return: Kết quả cuối cùng sau khi tính toán xong.
        """
        changes = True
        while changes:
            changes = False
            changes = self.Formula_1(changes)
            changes = self.Formula_2(changes)
            changes = self.Formula_3(changes)
            changes = self.Formula_4(changes)

        return self.get_results()

    def get_results(self):
        """
        Trả về kết quả cuối cùng.
        :return: Từ điển chứa các giá trị chiều dài, chiều rộng, diện tích, chu vi và đường chéo.
        """
        return {
            'length': f"{self.length} cm" if self.length else None,
            'width': f"{self.width} cm" if self.width else None,
            'area': f"{self.area} cm²" if self.area else None,
            'perimeter': f"{self.perimeter} cm" if self.perimeter else None,
            'diagonal': f"{self.diagonal} cm" if self.diagonal else None
        }

    def get_solution_steps(self):
        """
        Trả về các bước giải chi tiết.
        :return: Chuỗi mô tả các bước giải chi tiết.
        """
        solution = "Các bước giải chi tiết:\n\n"
        for step in self.solution_steps:
            solution += f"Bước {step[0]}: {step[1]}\n"
        return solution


# Ví dụ sử dụng:
rectangle = Rectangle(length=6, width=4)
rectangle.solve()
print(rectangle.get_results())
print(rectangle.get_solution_steps())
