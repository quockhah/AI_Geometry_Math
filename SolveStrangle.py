import math
import re
import Formula

class GiaiTamGiac:

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
        self.p = kwargs.get('p')
        self.r = kwargs.get('r')
        self.hc = kwargs.get('hc')
        self.validStrangleData = [[self.alpha,self.b,self.c,self.a],[self.beta,self.a,self.c,self.b],[self.delta,self.b,self.a,self.c]]
        self.Gia_tri_tinh = []
        self.cong_thuc=[]
        self.yeu_to=[]
        self.yeu_to_them=[]
        self.yeu_to_bd=[]
        self.yeu_tot=[]
        self.loigiai=[]
        for key, value in kwargs.items():
            
            if value is not None:
                self.yeu_to_them.append(key)
                self.yeu_to_bd.append(key)



    def choose_valid(self):
        isValue=None
        if self.alpha is not None:
            isValue=self.alpha
        elif self.beta is not None and isValue==None:
            isValue=self.beta
        elif self.delta is not None and isValue==None:
            isValue=self.delta
        for i in self.validStrangleData:
            if i[0]==isValue:
                result=i
        return result

    def is_valid_triangle(self):
        # Kiểm tra định lý bất đẳng thức tam giác
        edges=[self.a,self.b,self.c]
        data=self.choose_valid()
        corner=data[0]
        edge_1=data[1]
        edge_2=data[2]
        edge_3=data[3]
        result=False
        if self.a and self.b and self.c:
            if self.a + self.b > self.c and self.a + self.c > self.b and self.b + self.c > self.a:
                # Kiểm tra xem tổng các góc có bằng 180 độ (π radians) không
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
    
    def giai(self):
        # Tiếp tục tính toán cho đến khi không còn giá trị nào có thể tính được
        while True:
            changes = False
            changes = Formula.Formula_1(self, changes)
            changes = Formula.Formula_2(self, changes)
            changes = Formula.Formula_3(self, changes)
            changes = Formula.Formula_4(self, changes)
            changes = Formula.Formula_5(self, changes)
            changes = Formula.Formula_6(self, changes)
            changes = Formula.Formula_7(self, changes)
            if not changes:
                self.validStrangleData = [[self.alpha,self.b,self.c,self.a],[self.beta,self.a,self.c,self.b],[self.delta,self.b,self.a,self.c]]
                break
    def parse_input(text):
        pattern = r'(\w+)\s*=\s*([\d.]+)(?!\?)'
        matches = re.findall(pattern, text)
        
        data = {key: float(value) for key, value in matches}
    
        # Convert angles to radians if necessary
        return data
    def process_text(text):
        matches = re.findall(r'(\w+)=\?', text)
        data = matches[0] if matches else None
        return data
            
    def kt1(self, giatri):
        for dong in self.Gia_tri_tinh:
            if dong[1] == giatri and dong[0] not in self.cong_thuc: 
                self.cong_thuc.append(dong[0])
        self.cong_thuc.sort()
    def LoiGiai(self):
        A = [[1,'alpha', 'beta', 'delta'], [2,'beta','alpha','delta'], [3, 'delta', 'alpha', 'beta'], [4,'a','b','alpha','beta'], [5,'b','a', 'beta', 'alpha']
            ,[6,'c','a', 'delta', 'alpha'], [7,'a','c', 'delta', 'alpha'], [8,'b','c','beta','delta'], [9,'c','b','beta','detal'], [10,'alpha','a','beta','b']
            ,[11,'beta','b','delta','c'], [12,'delta','a', 'c', 'alpha'], [13,'alpha','a','delta','c'], [14,'beta','b', 'a', 'alpha'], [15,'delta','c','beta','b']
            ,[16,'p','a', 'b', 'c'], [17,'c','p','a','b'], [18,'b','p','a','c'], [19,'a','p','b', 'c'], [20,'S','p', 'c', 'b', 'a'], [21,'a','p', 'c', 'b', 'S']
            ,[22,'b','p', 'c', 'a', 'S'], [23,'c','p', 'b', 'a', 'S'], [24,'hc','S','c'], [25,'S','hc','c'], [26,'c','hc','S'], [27,'R','a','b','c','S']
            ,[28,'S','a','b','c','R'], [29,'c','a','b','S','R'], [30,'b','a','c','S','R'], [31,'a','b','c','S','R'], [32,'r','S','p'], [33,'S','r','p'], [34,'p','r','S']
            ]
        B=[]
        C=[]
        for item in self.cong_thuc:
            for row in A:
                if item == row[0]:
                    B = row[1]      
                    C = row[2:]     
            for item_B in B:
                if item_B not in self.yeu_to_them:  
                    self.yeu_to_them.append(item_B)
            for item_C in C:
                if item_C not in self.yeu_to_them and item_C not in self.yeu_to:  
                    self.yeu_to.append(item_C)
                    self.yeu_tot.append(item_C)

    def tim(self, giatri):
        prev_length = len(self.yeu_tot)
        while True:
            if not self.cong_thuc:  
                self.kt1(giatri) 
                self.LoiGiai()
            else:
                for item in self.yeu_tot:
                    self.kt1(item)  
                    self.LoiGiai()
            if len(self.yeu_tot) == prev_length:
                break
            prev_length = len(self.yeu_tot)



text = "a=5,b=4,c=3,alpha=90,r=?"
parsed_data = GiaiTamGiac.parse_input(text)
parsed_data1 = GiaiTamGiac.process_text(text)


tam_giac = GiaiTamGiac(**parsed_data)
tam_giac.giai()
tam_giac.is_valid_triangle()
tam_giac.tim(parsed_data1)


# In kết quả
for item in tam_giac.loigiai:
    if item[0] in tam_giac.cong_thuc:
        print(item[1])  # In giá trị thứ 2