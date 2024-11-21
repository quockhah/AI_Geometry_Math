import math

class Square:
    def __init__(self, **kwargs):
        """
        Khởi tạo hình vuông với các giá trị cạnh, diện tích, chu vi và đường chéo tùy chọn.
        : Các tham số tùy chọn cho cạnh, diện tích, chu vi và đường chéo.
        """
        self.side = kwargs.get('side', None)  # Cạnh của hình vuông
        self.area = kwargs.get('area', None)  # Diện tích
        self.perimeter = kwargs.get('perimeter', None)  # Chu vi
        self.diagonal = kwargs.get('diagonal', None)  # Đường chéo
        self.solution_steps = []  # Danh sách các bước giải
        self.calculated_values = []  # Danh sách các giá trị đã tính
        self.steps = 0  # Bộ đếm số bước

    def Formula_1(self, changes):
        """Tính diện tích, chu vi và đường chéo nếu chưa có."""
        if self.side and not self.area:
            self.area = round(self.side ** 2, 2)  # Diện tích
            self.solution_steps.append([self.steps + 1, f"Tính diện tích: {self.side}² = {self.area}"])
            self.calculated_values.append([self.steps + 1, "area"])
            changes = True
            self.steps += 1

        if self.area and self.side and not self.perimeter:
            self.perimeter = round(4 * self.side, 2)  # Chu vi
            self.solution_steps.append([self.steps + 1, f"Tính chu vi: 4 * {self.side} = {self.perimeter}"])
            self.calculated_values.append([self.steps + 1, "perimeter"])
            changes = True
            self.steps += 1

        if self.side and not self.diagonal:
            self.diagonal = round(self.side * math.sqrt(2), 2)  # Đường chéo
            self.solution_steps.append([self.steps + 1, f"Tính đường chéo: {self.side} * √2 = {self.diagonal}"])
            self.calculated_values.append([self.steps + 1, "diagonal"])
            changes = True
            self.steps += 1

        return changes

    def Formula_2(self, changes):
        """Tính cạnh từ diện tích, chu vi hoặc đường chéo nếu chưa có."""
        if self.area and not self.side:
            self.side = round(math.sqrt(self.area), 2)  # Tính cạnh từ diện tích
            self.solution_steps.append([self.steps + 1, f"Tính cạnh: √{self.area} = {self.side}"])
            self.calculated_values.append([self.steps + 1, "side"])
            changes = True
            self.steps += 1

        if self.perimeter and not self.side:
            self.side = round(self.perimeter / 4, 2)  # Tính cạnh từ chu vi
            self.solution_steps.append([self.steps + 1, f"Tính cạnh: {self.perimeter} / 4 = {self.side}"])
            self.calculated_values.append([self.steps + 1, "side"])
            changes = True
            self.steps += 1

        if self.diagonal and not self.side:
            self.side = round(self.diagonal / math.sqrt(2), 2)  # Tính cạnh từ đường chéo
            self.solution_steps.append([self.steps + 1, f"Tính cạnh: {self.diagonal} / √2 = {self.side}"])
            self.calculated_values.append([self.steps + 1, "side"])
            changes = True
            self.steps += 1

        return changes

    def Formula_3(self, changes):
        """Tính chu vi hoặc diện tích từ cạnh nếu chưa có."""
        if self.side and self.area and not self.perimeter:
            self.perimeter = round(4 * self.side, 2)  # Chu vi từ cạnh
            self.solution_steps.append([self.steps + 1, f"Tính chu vi: 4 * {self.side} = {self.perimeter}"])
            self.calculated_values.append([self.steps + 1, "perimeter"])
            changes = True
            self.steps += 1

        if self.side and self.perimeter and not self.area:
            self.area = round(self.side ** 2, 2)  # Diện tích từ cạnh
            self.solution_steps.append([self.steps + 1, f"Tính diện tích: {self.side}² = {self.area}"])
            self.calculated_values.append([self.steps + 1, "area"])
            changes = True
            self.steps += 1

        return changes

    def Formula_4(self, changes):
        """Tính diện tích nếu chưa có."""
        if self.side and self.perimeter and not self.area:
            self.area = round(self.side ** 2, 2)  # Diện tích từ cạnh
            self.solution_steps.append([self.steps + 1, f"Tính diện tích: {self.side}² = {self.area}"])
            self.calculated_values.append([self.steps + 1, "area"])
            changes = True
            self.steps += 1

        if self.side and self.diagonal and not self.area:
            self.area = round(self.side ** 2, 2)  # Diện tích từ cạnh
            self.solution_steps.append([self.steps + 1, f"Tính diện tích: {self.side}² = {self.area}"])
            self.calculated_values.append([self.steps + 1, "area"])
            changes = True
            self.steps += 1

        return changes

    def solve(self):
        """Thực hiện tính toán cho tất cả các thuộc tính hình vuông còn thiếu."""
        changes = True
        while changes:
            changes = False
            changes = self.Formula_1(changes)
            changes = self.Formula_2(changes)
            changes = self.Formula_3(changes)
            changes = self.Formula_4(changes)

        return self.get_results()

    def get_results(self):
        """Trả về kết quả cuối cùng."""
        return {
            'side': f"{self.side} cm" if self.side else None,
            'area': f"{self.area} cm²" if self.area else None,
            'perimeter': f"{self.perimeter} cm" if self.perimeter else None,
            'diagonal': f"{self.diagonal} cm" if self.diagonal else None
        }

    def get_solution_steps(self):
        """Trả về các bước giải chi tiết."""
        solution = "Các bước giải chi tiết:\n\n"
        for step in self.solution_steps:
            solution += f"Bước {step[0]}: {step[1]}\n"
        return solution


# Ví dụ sử dụng:
square = Square(side=5)
square.solve()
print(square.get_results())
print(square.get_solution_steps())
