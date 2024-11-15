import math
import re


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
        self.validStrangleData = [[self.alpha,self.b,self.c],[self.beta,self.a,self.c],[self.delta,self.b,self.a]]
        self.mang = []
        self.soct=[]
        self.yt=[]
        self.ytbd=[]
        self.ytt=[]
        self.loigiai=[]
        for key, value in kwargs.items():
            
            if value is not None:
                self.ytbd.append(key)
        
    def round_even(value):
            if value is not None:
                return round(value)
            return None

    def ChooseValid(self):
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
        data=self.ChooseValid()
        edge=[i for i in edges if i not in data]
        corner=data[0]
        edge_1=data[1]
        edge_2=data[2]
        edge_3=edge[0]
        result=False
        if self.a and self.b and self.c:
            if self.a + self.b > self.c and self.a + self.c > self.b and self.b + self.c > self.a:
                # Kiểm tra xem tổng các góc có bằng 180 độ (π radians) không
                if round(math.pow(edge_3,2))==round(math.pow(edge_1,2)+math.pow(edge_2,2)-2*edge_1*edge_2*math.cos(corner)):
                    result= True
            else:
                print("Các cạnh không thỏa mãn định lý bất đẳng thức tam giác.")
                result= False
        print("Các độ dài cạnh không được cung cấp hoặc không hợp lệ.")
        if result==False:
            print("Invalid triangle. Exiting program.")
            exit()
    def giai(self):
        def round_even(value):
            if value is not None:
                return round(value)
            return None
        # Tiếp tục tính toán cho đến khi không còn giá trị nào có thể tính được
        while True:
            changes = False  # Biến kiểm tra xem có thay đổi gì không
            # Công thức 2: Tính góc còn thiếu nếu đã biết hai góc
            if self.beta and self.delta and not self.alpha:
                self.alpha = math.pi - self.beta - self.delta
                print("Tính góc alpha: alpha =", math.degrees(self.alpha))
                self.loigiai.append([1, f'\nTính góc alpha: \n180-{round_even(math.degrees(self.beta))}-{round_even(math.degrees(self.delta))}={round_even(math.degrees(self.alpha))}\n'])
                self.mang.append([1,":alpha"])
                changes = True
            if self.alpha and self.delta and not self.beta:
                self.beta = math.pi - self.alpha - self.delta
                self.loigiai.append([2, f'\nTính góc beta: \n180-{round_even(math.degrees(self.alpha))}-{round_even(math.degrees(self.delta))}={round_even(math.degrees(self.Beta))}\n'])
                self.mang.append([2,"beta"])
                changes = True
            if self.alpha and self.beta and not self.delta:
                self.delta = math.pi - self.alpha - self.beta
                self.loigiai.append([3, f'\nTính góc delta: \n180-{round_even(math.degrees(self.alpha))}-{round_even(math.degrees(self.beta))}={round_even(math.degrees(self.delta))}\n'])
                self.mang.append([3,"delta"])
                changes = True

            # Công thức 1: Định lý Sin để tính cạnh khi biết hai góc và một cạnh khác
            #alpha/beta/b     a=?
            if self.alpha and self.beta and self.b and not self.a:
                self.a = self.b * math.sin(self.alpha) / math.sin(self.beta)
                self.loigiai.append([4, f'Tính cạnh a:\n({self.b}*sin({round_even(math.degrees(self.alpha))}))/sin({round_even(math.degrees(self.beta))})={round_even(self.a)}\n'])
                self.mang.append([4,"a"])
                changes = True
            #alpha/beta/a     b=?
            if self.alpha and self.beta and self.a and not self.b:
                self.b = self.a * math.sin(self.beta) / math.sin(self.alpha)
                self.loigiai.append([5, f'Tính cạnh b:\n({round_even(self.a)}*sin({round_even(math.degrees(self.beta))}))/sin({round_even(math.degrees(self.alpha))})={round_even(self.b)}\n'])
                self.mang.append([5,"b"])
                changes = True
            #alpha/delta/a     
            if self.alpha and self.delta and self.a and not self.c:
                self.c = self.a * math.sin(self.delta) / math.sin(self.alpha)
                self.loigiai.append([6, f'Tính cạnh c: \n({round_even(self.a)}*sin({round_even(math.degrees(self.delta))}))/sin({round_even(math.degrees(self.alpha))})= {round_even(self.c)}\n'])
                self.mang.append([6,"c"])
                changes = True
            #alpha/delta/c     a=?
            if self.alpha and self.delta and self.c and not self.a:
                self.a = self.c * math.sin(self.alpha) / math.sin(self.delta)
                self.loigiai.append([7, f'Tính cạnh a:\n({round_even(self.c)}*sin({math.degrees(self.alpha)}))/sin({math.degrees(self.delta)})={round_even(self.a)}\n'])
                self.mang.append([7,"a"])
                changes = True
            #beta/delta/c      b=??  
            if self.beta and self.delta and self.c and not self.b:
                self.b = self.c * math.sin(self.beta) / math.sin(self.delta)
                self.loigiai.append([8, f'Tính cạnh b:\n({self.c}*sin({round_even(math.degrees(self.beta))}))/sin({round_even(math.degrees(self.delta))})={round_even(self.b)}\n'])
                print("Tính cạnh b bằng công thức sin: b =", self.b)
                self.mang.append([8,"b"])
                changes = True
            #beta/delta/b      c=?
            if self.beta and self.delta and self.b and not self.c:
                self.c = self.b * math.sin(self.delta) / math.sin(self.beta)
                self.loigiai.append([9, f'Tính cạnh c:\n({round_even(self.b)}*sin({round_even(math.degrees(self.delta))}))/sin({round_even(math.degrees(self.beta))})={round_even(self.c)}\n'])
                self.mang.append([9,"c"])
                changes = True
              # Trường hợp 1: Tính góc alpha nếu biết a, b và góc beta
            if self.a and self.b and self.beta and not self.alpha:
                self.alpha = math.asin(self.a * math.sin(self.beta) / self.b)
                print("Tính góc alpha bằng công thức sin: alpha =", math.degrees(self.alpha))
                self.mang.append([10,"alpha"])
                changes = True
        
                # Trường hợp 2: Tính góc beta nếu biết b, c và góc delta
            if self.b and self.c and self.delta and not self.beta:
                self.beta = math.asin(self.b * math.sin(self.delta) / self.c)
                print("Tính góc beta bằng công thức sin: beta =", math.degrees(self.beta))
                self.mang.append([11,"beta"])
                changes = True
            
            # Trường hợp 3: Tính góc delta nếu biết a, c và góc alpha
            
            if self.a and self.c and self.alpha and not self.delta:
                temp =math.sin(self.alpha)
                self.delta = math.asin(self.c * math.sin(self.alpha) / self.a)
                print("Tính góc delta bằng công thức sin: delta =", math.degrees(self.delta))
                self.loigiai.append([12, f'{math.degrees(self.delta)}'])
                self.mang.append([12,"delta"])
                changes = True

            # Trường hợp 4: Tính góc alpha nếu biết a, c và góc delta
            if self.a and self.c and self.delta and not self.alpha:
                self.alpha = math.asin(self.a * math.sin(self.delta) / self.c)
                print("Tính góc alpha bằng công thức sin: alpha =", math.degrees(self.alpha))
                self.mang.append([13,"alpha"])
                changes = True

            # Trường hợp 5: Tính góc beta nếu biết b, a và góc alpha
            if self.b and self.a and self.alpha and not self.beta:
                self.beta = math.asin(self.b * math.sin(self.alpha) / self.a)
                print("Tính góc beta bằng công thức sin: beta =", math.degrees(self.beta))
                self.loigiai.append([14,f'góc beta:\n{round_even(math.degrees(self.beta))}'])
                self.mang.append([14,"beta"])
                changes = True
            
            # Trường hợp 6: Tính góc delta nếu biết b, c và góc alpha
            if self.b and self.c and self.beta and not self.delta:
                self.delta = math.asin(self.c * math.sin(self.beta) / self.b)
                print("Tính góc delta bằng công thức sin: delta =", math.degrees(self.delta))
                self.mang.append([15,"delta"])
                changes = True

            

            # Công thức 3: Tính nửa chu vi p nếu đã biết tất cả các cạnh
            if self.a and self.b and self.c and not self.p:
                self.p = (self.a + self.b + self.c) / 2
                self.loigiai.append([16, f'Tính cạnh p: p = {round_even(self.p)}'])
                self.mang.append([16,"p"])
                changes = True

            # Nếu nửa chu vi p đã biết thì tính các yếu tố còn lại nếu chỉ thiếu 1 yếu tố trong công thức Heron
            if self.p and self.a and self.b and not self.c:
                self.c = 2 * self.p - self.a - self.b
                print("Tính cạnh c khi biết nửa chu vi: c =", self.c)
                self.mang.append([17,"c"])
                changes = True
            if self.p and self.a and self.c and not self.b:
                self.b = 2 * self.p - self.a - self.c
                print("Tính cạnh b khi biết nửa chu vi: b =", self.b)
                self.mang.append([18,"b"])
                changes = True
            if self.p and self.b and self.c and not self.a:
                self.a = 2 * self.p - self.b - self.c
                self.loigiai.append([19, f'Tính cạnh a:\n2*{self.p} - {self.b} - {self.c} = {self.a}'])
                self.mang.append([19,"a"])
                changes = True

            # Công thức 4: Tính diện tích S bằng công thức Heron (khi đã biết p và 3 cạnh)
            if self.p and self.a and self.b and self.c and not self.S:
                self.S = math.sqrt(self.p * (self.p - self.a) * (self.p - self.b) * (self.p - self.c))
                self.loigiai.append([20, f'Tính diện tích S bằng công thức Heron: S = {round_even(self.S)}'])
                self.mang.append([20,"S"])
                changes = True

            # Trường hợp tính cạnh a khi biết diện tích và các yếu tố còn lại
            if self.S and self.p and self.b and self.c and not self.a:
                a_solved = self.p - self.b - self.c
                self.a = math.sqrt(2 * self.S / a_solved)
                print("Tính cạnh a khi biết diện tích và các yếu tố còn lại: a =", self.a)
                self.mang.append([21,"a"])
                changes = True

            # Trường hợp tính cạnh b khi biết diện tích và các yếu tố còn lại
            if self.S and self.p and self.a and self.c and not self.b:
                b_solved = self.p - self.a - self.c
                self.b = math.sqrt(2 * self.S / b_solved)
                print("Tính cạnh b khi biết diện tích và các yếu tố còn lại: b =", self.b)
                self.mang.append([22,"b"])
                changes = True

            # Trường hợp tính cạnh c khi biết diện tích và các yếu tố còn lại
            if self.S and self.p and self.a and self.b and not self.c:
                c_solved = self.p - self.a - self.b
                self.c = math.sqrt(2 * self.S / c_solved)
                print("Tính cạnh c khi biết diện tích và các yếu tố còn lại: c =", self.c)
                self.mang.append([23,"c"])
                changes = True

            # Công thức 5: Tính chiều cao hc nếu biết diện tích S và cạnh c
            if self.S and self.c and not self.hc:
                self.hc = (2 * self.S) / self.c
                self.loigiai.append([24, f'Tính chiều cao hc: hc = {round_even(self.hc)}'])
                self.mang.append([24,"hc"])
                changes = True
            if self.hc and self.c and not self.S:
                self.S = (self.hc * self.c) / 2
                print("Tính diện tích S: S =", self.S)
                self.mang.append([25,"S"])
                changes = True

            if self.S and self.hc and not self.c:
                self.c = (2 * self.S) / self.hc
                print("Tính cạnh c: c =", self.c)
                self.mang.append([26,"c"])
                changes = True

            # Công thức 6: Tính bán kính đường tròn ngoại tiếp R nếu biết diện tích S và tất cả các cạnh
            if self.S and self.a and self.b and self.c and not self.R:
                self.R = (self.a * self.b * self.c) / (4 * self.S)
                print("Tính bán kính đường tròn ngoại tiếp R: R =", self.R)
                self.mang.append([27,"R"])
                changes = True
            if self.R and self.a and self.b and self.c and not self.S:
                self.S = (self.a * self.b * self.c) / (4 * self.R)
                print("Tính diện tích tam giác S: S =", self.S)
                self.mang.append([28,"S"])
                changes = True

            if self.S and self.R and self.a and self.b and not self.c:
                self.c = (4 * self.S * self.R) / (self.a * self.b)
                print("Tính cạnh c: c =", self.c)
                self.mang.append([29,"c"])
                changes = True

            if self.S and self.R and self.a and self.c and not self.b:
                self.b = (4 * self.S * self.R) / (self.a * self.c)
                print("Tính cạnh b: b =", self.b)
                self.mang.append([30,"b"])
                changes = True
            if self.S and self.R and self.b and self.c and not self.a:
                self.a = (4 * self.S * self.R) / (self.b * self.c)
                print("Tính cạnh a: a =", self.a)
                self.mang.append([31,"a"])
                changes = True

            # Công thức 7: Tính bán kính đường tròn nội tiếp r nếu biết p và S
            if self.S and self.p and not self.r:
                self.r = self.S / self.p
                print("Tính bán kính đường tròn nội tiếp r: r =", self.r)
                self.mang.append([32,"r"])
                changes = True
            if self.r and self.p and not self.S:
                self.S = self.r * self.p
                print("Tính diện tích tam giác S: S =", self.S)
                self.mang.append([33,"S"])
                changes = True

            if self.S and self.r and not self.p:
                self.p = self.S / self.r
                print("Tính nửa chu vi p: p =", self.p)
                self.mang.append([34,"p"])
                changes = True

            # Nếu không có thay đổi nào xảy ra, dừng vòng lặp
            if not changes:
                self.validStrangleData = [[self.alpha,self.b,self.c],[self.beta,self.a,self.c],[self.delta,self.b,self.a]]
                break
    def parse_input(text):
        pattern = r'(\w+)\s*=\s*([\d.]+)(?!\?)'
        matches = re.findall(pattern, text)
        
        data = {key: float(value) for key, value in matches}
    
        # Convert angles to radians if necessary
        return data
    def process_text(text):
        matches = re.findall(r'(\w+)=\?', text)
        a = matches[0] if matches else None
        return a
    def ket_qua(self, fields=None):
    # Trả về tất cả các giá trị đã tính, làm tròn các giá trị thành số chẵn nhất
        def round_even(value):
            if value is not None:
                return round(value)
            return None
        
        # Các giá trị cần tính toán
        results = {
            'alpha (độ)': round_even(math.degrees(self.alpha)) if self.alpha else None,
            'beta (độ)': round_even(math.degrees(self.beta)) if self.beta else None,
            'delta (độ)': round_even(math.degrees(self.delta)) if self.delta else None,
            'a': round_even(self.a) if self.a else None,
            'b': round_even(self.b) if self.b else None,
            'c': self.c if self.c else None,
            'nửa chu vi (p)': round_even(self.p) if self.p else None,
            'diện tích (S)': round_even(self.S) if self.S else None,
            'bán kính đường tròn ngoại tiếp (R)': round_even(self.R) if self.R else None,
            'bán kính đường tròn nội tiếp (r)': round_even(self.r) if self.r else None,
            'chiều cao với cạnh c (hc)': round_even(self.hc) if self.hc else None
        }
        
        # Nếu không có tham số `fields`, trả về tất cả các kết quả
        if fields is None:
            return results
        
        # Trả về chỉ các giá trị được yêu cầu
        return {key: value for key, value in results.items() if key in fields}
    
    def ktra(yeuto):
        if yeuto=="dientich":
            print("khang")
            
    def kt1(self, giatri):
        for dong in self.mang:
            if dong[1] == giatri and dong[0] not in self.soct:  # Check if the value is not already in `soct`
                self.soct.append(dong[0])
    def kt2(self):
        for dong in self.soct:
            if dong == 3:
                A = ["alpha", "beta"]
                if "delta" not in self.ytbd:  
                    self.ytbd.append("delta")
                for item in A:
                    if item not in self.ytbd and item not in self.yt:  
                        self.yt.append(item)
                        self.ytt.append(item)
            if dong == 5:
                A = ["a", "beta", "alpha"]
                if "b" not in self.ytbd:  
                    self.ytbd.append("b")
                for item in A:
                    if item not in self.ytbd and item not in self.yt:  
                        self.yt.append(item)
                        self.ytt.append(item)
            if dong == 6:
                A = ["a", "delta", "alpha"]
                if "c" not in self.ytbd:  
                    self.ytbd.append("c")
                for item in A:
                    if item not in self.ytbd and item not in self.yt:  
                        self.yt.append(item)
                        self.ytt.append(item)
            if dong == 12:
                A = ["a", "c", "alpha"]
                if "c" not in self.ytbd:  
                    self.ytbd.append("delta")
                for item in A:
                    if item not in self.ytbd and item not in self.yt:  
                        self.yt.append(item)
                        self.ytt.append(item)
            if dong == 14:
                A = ["b", "a", "alpha"]
                if "c" not in self.ytbd:  
                    self.ytbd.append("beta")
                for item in A:
                    if item not in self.ytbd and item not in self.yt:  
                        self.yt.append(item)
                        self.ytt.append(item)
            if dong == 16:
                A = ["p", "b", "c"]
                if "p" not in self.ytbd:  
                    self.ytbd.append("p")
                for item in A:
                    if item not in self.ytbd and item not in self.yt:  
                        self.yt.append(item)
                        self.ytt.append(item)
            if dong == 19:
                A = ["a", "b", "c"]
                if "p" not in self.ytbd:  
                    self.ytbd.append("p")
                for item in A:
                    if item not in self.ytbd and item not in self.yt:  
                        self.yt.append(item)
                        self.ytt.append(item)
            if dong == 20:
                A = ["p", "c", "b", "a"]
                if "S" not in self.ytbd:  
                    self.ytbd.append("S")
                for item in A:
                    if item not in self.ytbd and item not in self.yt:  
                        self.yt.append(item)
                        self.ytt.append(item)
    def tim(self, giatri):
        prev_length = len(self.ytt)
        while True:
            if not self.soct:  # Check if `soct` is empty
                self.kt1(giatri)  # Use self to call the method
                self.kt2()
            else:
                for item in self.ytt:
                    self.kt1(item)  # Use self to call the method
                    self.kt2()

            # Break the loop if no new items are added to `ytt`
            if len(self.ytt) == prev_length:
                break
            prev_length = len(self.ytt)

# Ví dụ sử dụng
# Khởi tạo các giá trị đã biết (góc nhập bằng độ, cạnh nếu có)

text = "b=3,a=5,alpha=90,S=?"
parsed_data = GiaiTamGiac.parse_input(text)
parsed_data1 = GiaiTamGiac.process_text(text)


tam_giac = GiaiTamGiac(**parsed_data)
tam_giac.giai()
tam_giac.is_valid_triangle()
ket_qua = tam_giac.ket_qua(fields=['alpha (độ)', 'a', 'diện tích (S)','beta (độ)','delta (độ)','c'])
#Display results
for key, value in ket_qua.items():
    print(f"{key}: {value}")
a="dientich"
GiaiTamGiac.ktra(a)
b = "S"
tam_giac.tim(parsed_data1)
#print("yt:", tam_giac.yt)
#print("ytt", tam_giac.ytt)
print("loigiai", tam_giac.loigiai)
#print("ytbd:", tam_giac.ytbd)
#print("soct",tam_giac.soct)
print("Mảng", tam_giac.mang)
soct_reversed = tam_giac.soct[::-1]

# Lấy các giá trị đầu tiên của các phần tử trong mảng loigiai
values_loigiai = [item[0] for item in tam_giac.loigiai]

# So sánh với mảng soct_reversed và in ra các giá trị trùng khớp
common_values = [value for value in values_loigiai if value in soct_reversed]

# In kết quả
for item in tam_giac.loigiai:
    if item[0] in tam_giac.soct:
        print(item[1])  # In giá trị thứ 2