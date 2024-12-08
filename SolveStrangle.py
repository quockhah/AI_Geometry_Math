import math
import re
import Formula

class SolveTriangle:

    def __init__(self, **kwargs):
        # Khởi tạo các giá trị đã biết
        self.alpha = math.radians(kwargs.get('alpha')) if 'alpha' in kwargs else None
        self.beta = math.radians(kwargs.get('beta')) if 'beta' in kwargs else None
        self.delta = math.radians(kwargs.get('delta')) if 'delta' in kwargs else None
        self.a = kwargs.get('a')
        self.b = kwargs.get('b')
        self.c = kwargs.get('c')
        self.R = kwargs.get('R')
        self.S = kwargs.get('S')
        self.C = kwargs.get('C')
        self.p = kwargs.get('p')
        self.r = kwargs.get('r')
        self.hc = kwargs.get('hc')
        self.validTriangleData = [[self.alpha,self.b,self.c,self.a],[self.beta,self.a,self.c,self.b],[self.delta,self.b,self.a,self.c]]
        self.Value_to_find = []
        self.formula=[]
        self.element=[]
        self.element_add=[]
        self.yeu_tot=[]
        self.solution=[]
        for key, value in kwargs.items():
            
            if value is not None:
                self.element_add.append(key)

    def Check_formula(self, value):
        for dong in self.Value_to_find:
            if dong[1] == value and dong[0] not in self.formula: 
                self.formula.append(dong[0])
        self.formula.sort()

    def Choose_valid(self):
        """
            Chọn giá trị hợp lệ từ các thuộc tính và danh sách `validTriangleData`.

            Args:
                self: Tham chiếu đến đối tượng hiện tại, chứa các thuộc tính `alpha`, `beta`, `delta`, và danh sách `validTriangleData`.

            Returns:
                tuple or None: Một tuple từ danh sách `validTriangleData` khớp với giá trị hợp lệ, hoặc None nếu không tìm thấy.
        """
        isValue=None
        if self.alpha is not None:
            isValue=self.alpha
        elif self.beta is not None and isValue==None:
            isValue=self.beta
        elif self.delta is not None and isValue==None:
            isValue=self.delta
        for i in self.validTriangleData:
            if i[0]==isValue:
                result=i
        return result

    def Is_valid_triangle(self):
        """
            Kiểm tra xem các cạnh và góc được cung cấp có tạo thành một tam giác hợp lệ hay không.

            Args:
                self: Tham chiếu đến đối tượng hiện tại, chứa các thuộc tính `a`, `b`, `c` (các cạnh tam giác) 
                và phương thức `Choose_valid` để lấy dữ liệu cạnh và góc.

            Returns:
                bool: Trả về `True` nếu tam giác hợp lệ, thoả mãn định lý bất đẳng thức tam giác và công thức cosine.
                Nếu không hợp lệ, hàm sẽ in thông báo lỗi và thoát chương trình.
        """
        edges=[self.a,self.b,self.c]
        data=self.Choose_valid()
        corner=data[0]
        edge_1=data[1]
        edge_2=data[2]
        edge_3=data[3]
        result=False
        if self.a and self.b and self.c:
            if self.a + self.b > self.c and self.a + self.c > self.b and self.b + self.c > self.a:
                if round(math.pow(edge_3,2))==round(math.pow(edge_1,2)+math.pow(edge_2,2)-2*edge_1*edge_2*math.cos(corner)):
                    result= True
                else:
                     print("Các độ dài cạnh không được cung cấp hoặc không hợp lệ.")
            else:
                print("Các cạnh không thỏa mãn định lý bất đẳng thức tam giác.")
                result= False
        if result==False:
            print("Invalid triangle. Exiting program.")
            exit()

    def Parse_input(text):
        """
            Phân tích chuỗi để trích xuất các cặp key-value theo định dạng `key=value`.

            Args:
                text (str): Chuỗi đầu vào chứa các cặp key-value.

            Returns:
                dict: Một dictionary với key là chuỗi và value là số thực (float).
        """
        pattern = r'(\w+)\s*=\s*([\d.]+)(?!\?)'
        matches = re.findall(pattern, text) 
        data = {key: float(value) for key, value in matches}
        return data
    
    def Process_text(text):
        """
            Trích xuất biến đầu tiên có giá trị chưa xác định (`key=?`) từ một chuỗi.

            Args:
                text (str): Chuỗi đầu vào chứa các cặp key-value và biến chưa xác định.

            Returns:
                str hoặc None: Tên biến có giá trị chưa xác định hoặc None nếu không tìm thấy.
        """
        matches = re.findall(r'(\w+)=\?', text)
        data = matches[0] if matches else None
        return data
    
    def Solve_math(self):
        """
            Giải quyết các công thức toán học và cập nhật dữ liệu hợp lệ trong thuộc tính `validTriangleData`.

            Args:
                self: Tham chiếu đến đối tượng hiện tại, chứa các thuộc tính và phương thức cần thiết để tính toán.

            Returns:
                None: Hàm không trả về giá trị, nhưng cập nhật `self.validTriangleData` sau khi tính toán xong.
        """
        while True:
            changes = False
            changes = Formula.Formula_1(self, changes)
            changes = Formula.Formula_2(self, changes)
            changes = Formula.Formula_3(self, changes)
            changes = Formula.Formula_4(self, changes)
            changes = Formula.Formula_5(self, changes)
            changes = Formula.Formula_6(self, changes)
            changes = Formula.Formula_7(self, changes)
            changes = Formula.Formula_8(self, changes)

            if not changes:
                self.validTriangleData = [[self.alpha,self.b,self.c,self.a],[self.beta,self.a,self.c,self.b],[self.delta,self.b,self.a,self.c]]
                break

    def Solution(self):
        """
            Phân tích các công thức và thiết lập mối quan hệ giữa các phần tử dựa trên `Relationship_A`.

            Args:
                self: Tham chiếu đến đối tượng hiện tại, chứa các thuộc tính `formula`, `element_add`, `element`, và `yeu_tot`.

            Returns:
                None: Hàm không trả về giá trị, nhưng cập nhật các thuộc tính `element_add`, `element`, và `yeu_tot` dựa trên logic đã thực thi.
        """
        
        Relationship_A = [[1,'alpha', 'beta', 'delta'], [2,'beta','alpha','delta'], [3, 'delta', 'alpha', 'beta'], [4,'a','b','alpha','beta'], [5,'b','a', 'beta', 'alpha']
            ,[6,'c','a', 'delta', 'alpha'], [7,'a','c', 'delta', 'alpha'], [8,'b','c','beta','delta'], [9,'c','b','beta','detal'], [10,'alpha','a','beta','b']
            ,[11,'beta','b','delta','c'], [12,'delta','a', 'c', 'alpha'], [13,'alpha','a','delta','c'], [14,'beta','b', 'a', 'alpha'], [15,'delta','c','beta','b']
            ,[16,'p','a', 'b', 'c'], [17,'c','p','a','b'], [18,'b','p','a','c'], [19,'a','p','b', 'c'], [20,'S','p', 'c', 'b', 'a'], [21,'a','p', 'c', 'b', 'S']
            ,[22,'b','p', 'c', 'a', 'S'], [23,'c','p', 'b', 'a', 'S'], [24,'hc','S','c'], [25,'S','hc','c'], [26,'c','hc','S'], [27,'R','a','b','c','S']
            ,[28,'S','a','b','c','R'], [29,'c','a','b','S','R'], [30,'b','a','c','S','R'], [31,'a','b','c','S','R'], [32,'r','S','p'], [33,'S','r','p'], [34,'p','r','S']
            ,[35,'C','a','b','c'],[36,'C','p'],[37,'p','C']
            ]
        B=[]
        C=[]
        for item in self.formula:
            for row in Relationship_A:
                if item == row[0]:
                    B = row[1]      
                    C = row[2:]     
            for item_B in B:
                if item_B not in self.element_add:  
                    self.element_add.append(item_B)
            for item_C in C:
                if item_C not in self.element_add and item_C not in self.element:  
                    self.element.append(item_C)
                    self.yeu_tot.append(item_C)

    def Save_solution(self, value):
        """
            Lưu trữ và xử lý giải pháp bằng cách kiểm tra và cập nhật các công thức liên quan.

            Args:
                self: Tham chiếu đến đối tượng hiện tại, chứa các thuộc tính `formula` và `yeu_tot`, 
                cùng các phương thức `Check_formula` và `Solution`.
                value: Giá trị được sử dụng để kiểm tra các công thức thông qua phương thức `Check_formula`.

            Returns:
                None: Hàm không trả về giá trị, nhưng liên tục cập nhật danh sách `yeu_tot` cho đến khi không còn thay đổi.
        """
        prev_length = len(self.yeu_tot)
        while True:
            if not self.formula:  
                self.Check_formula(value) 
                self.Solution()
            else:
                for item in self.yeu_tot:
                    self.Check_formula(item)  
                    self.Solution()
            if len(self.yeu_tot) == prev_length:
                break
            prev_length = len(self.yeu_tot)


text = "a=5,c=3,alpha=90,S=?"
parsed_data = SolveTriangle.Parse_input(text)
parsed_data1 = SolveTriangle.Process_text(text)


Triangle = SolveTriangle(**parsed_data)
Triangle.Solve_math()

Triangle.Save_solution(parsed_data1)
#Triangle.Is_valid_triangle()
print(Triangle.yeu_tot)
print(Triangle.solution)
print(Triangle.formula)


# In kết quả
for item in Triangle.solution:
    if item[0] in Triangle.formula:
        print(item[1])  # In giá trị thứ 2