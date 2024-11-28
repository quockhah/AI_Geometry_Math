import math

def Formula_1(self, changes):
    """
        Tính toán giá trị các góc tam giác (alpha, beta, delta) dựa trên hai góc đã biết.

        Args:
            self: Tham chiếu đến đối tượng hiện tại, chứa các thuộc tính `alpha`, `beta`, `delta`, 
            `solution`, và `Value_to_find`.
            changes (bool): Biến cờ để theo dõi liệu có sự thay đổi nào được thực hiện trong quá trình tính toán.

        Returns:
            bool: Trả về `True` nếu có thay đổi được thực hiện, ngược lại trả về `False`.
    """
    if self.beta and self.delta and not self.alpha:
        self.alpha = math.pi - self.beta - self.delta
        print("Tính góc alpha: alpha =", math.degrees(self.alpha))
        self.solution.append([1, f'\nTính góc alpha: \n180-{round(math.degrees(self.beta))}-{round(math.degrees(self.delta))}={round(math.degrees(self.alpha))}'])
        self.Value_to_find.append([1, ":alpha"])
        changes = True
    if self.alpha and self.delta and not self.beta:
        self.beta = math.pi - self.alpha - self.delta
        self.solution.append([2, f'\nTính góc beta: \n180-{round(math.degrees(self.alpha))}-{round(math.degrees(self.delta))}={round(math.degrees(self.beta))}'])
        self.Value_to_find.append([2, "beta"])
        changes = True
    if self.alpha and self.beta and not self.delta:
        self.delta = math.pi - self.alpha - self.beta
        self.solution.append([3, f'\nTính góc delta: \n180-{round(math.degrees(self.alpha))}-{round(math.degrees(self.beta))}={round(math.degrees(self.delta))}'])
        self.Value_to_find.append([3, "delta"])
        changes = True
    return changes

def Formula_2(self, changes):
    """
        Tính toán cạnh hoặc góc tam giác sử dụng định lý sin dựa trên các thông tin đã biết.

        Args:
            self: Tham chiếu đến đối tượng hiện tại, chứa các thuộc tính như `alpha`, `beta`, `delta`, 
            `a`, `b`, `c`, `solution`, và `Value_to_find`.
            changes (bool): Biến cờ để theo dõi liệu có sự thay đổi nào được thực hiện trong quá trình tính toán.

        Returns:
            bool: Trả về `True` nếu có thay đổi được thực hiện, ngược lại trả về `False`.
    """
    if self.alpha and self.beta and self.b and not self.a:
        self.a = self.b * math.sin(self.alpha) / math.sin(self.beta)
        self.solution.append([4, f'\nTính cạnh a:\n({self.b}*sin({round(math.degrees(self.alpha))}))/sin({round(math.degrees(self.beta))})={round(self.a)}'])
        self.Value_to_find.append([4, "a"])
        changes = True

    if self.alpha and self.beta and self.a and not self.b:
        self.b = self.a * math.sin(self.beta) / math.sin(self.alpha)
        self.solution.append([5, f'\nTính cạnh b:\n({round(self.a)}*sin({round(math.degrees(self.beta))}))/sin({round(math.degrees(self.alpha))})={round(self.b)}'])
        self.Value_to_find.append([5, "b"])
        changes = True

    if self.alpha and self.delta and self.a and not self.c:
        self.c = self.a * math.sin(self.delta) / math.sin(self.alpha)
        self.solution.append([6, f'\nTính cạnh c: \n({round(self.a)}*sin({round(math.degrees(self.delta))}))/sin({round(math.degrees(self.alpha))})= {round(self.c)}'])
        self.Value_to_find.append([6, "c"])
        changes = True

    if self.alpha and self.delta and self.c and not self.a:
        self.a = self.c * math.sin(self.alpha) / math.sin(self.delta)
        self.solution.append([7, f'\nTính cạnh a:\n({round(self.c)}*sin({math.degrees(self.alpha)}))/sin({math.degrees(self.delta)})={round(self.a)}'])
        self.Value_to_find.append([7, "a"])
        changes = True

    if self.beta and self.delta and self.c and not self.b:
        self.b = self.c * math.sin(self.beta) / math.sin(self.delta)
        self.solution.append([8, f'\nTính cạnh b:\n({self.c}*sin({round(math.degrees(self.beta))}))/sin({round(math.degrees(self.delta))})={round(self.b)}'])
        print("Tính cạnh b bằng công thức sin: b =", self.b)
        self.Value_to_find.append([8, "b"])
        changes = True

    if self.beta and self.delta and self.b and not self.c:
        self.c = self.b * math.sin(self.delta) / math.sin(self.beta)
        self.solution.append([9, f'\nTính cạnh c:\n({round(self.b)}*sin({round(math.degrees(self.delta))}))/sin({round(math.degrees(self.beta))})={round(self.c)}'])
        self.Value_to_find.append([9, "c"])
        changes = True

    if self.a and self.b and self.beta and not self.alpha:
        self.alpha = math.asin(max(-1, min(1, self.a * math.sin(self.beta) / self.b)))
        self.solution.append([10, f'\nTính góc alpha:\nsin^(-1)({round(self.a)}*sin({round(math.degrees(self.beta))}))/{round(self.b)}={round(math.degrees(self.alpha))}'])
        self.Value_to_find.append([10, "alpha"])
        changes = True

    if self.b and self.c and self.delta and not self.beta:
        self.beta = math.asin(max(-1, min(1, self.b * math.sin(self.delta) / self.c)))
        self.solution.append([11, f'\nTính góc beta:\nsin^(-1)({round(self.b)}*sin({round(math.degrees(self.delta))}))/{round(self.c)}={round(math.degrees(self.beta))}'])
        self.Value_to_find.append([11, "beta"])
        changes = True

    if self.a and self.c and self.alpha and not self.delta:
        self.delta = math.asin(max(-1, min(1, self.c * math.sin(self.alpha) / self.a)))
        self.solution.append([12, f'\nTính góc delta:\nsin^(-1)({round(self.c)}*sin({round(math.degrees(self.alpha))}))/{round(self.a)}={round(math.degrees(self.delta))}'])
        self.Value_to_find.append([12, "delta"])
        changes = True

    if self.a and self.c and self.delta and not self.alpha:
        self.alpha = math.asin(max(-1, min(1, self.a * math.sin(self.delta) / self.c)))
        self.solution.append([13, f'\nTính góc alpha:\nsin^(-1)({round(self.a)}*sin({round(math.degrees(self.delta))}))/{round(self.c)}=={round(math.degrees(self.alpha))}'])
        self.Value_to_find.append([13, "alpha"])
        changes = True

    if self.b and self.a and self.alpha and not self.beta:
        self.beta = math.asin(max(-1, min(1, self.b * math.sin(self.alpha) / self.a)))
        self.solution.append([14, f'\nTính góc beta:\nsin^(-1)({round(self.b)}*sin({round(math.degrees(self.alpha))}))/{round(self.a)}={round(math.degrees(self.beta))}'])
        self.Value_to_find.append([14, "beta"])
        changes = True

    if self.b and self.c and self.beta and not self.delta:
        self.delta = math.asin(max(-1, min(1, self.c * math.sin(self.beta) / self.b)))
        self.solution.append([15, f'\nTính góc delta:\nsin^(-1)({round(self.c)}*sin({round(math.degrees(self.beta))}))/{round(self.b)}={round(math.degrees(self.delta))}'])
        self.Value_to_find.append([15, "delta"])
        changes = True
    
    return changes

def Formula_3(self, changes):
    """
        Tính toán các cạnh và nửa chu vi (p) của tam giác dựa trên các thông tin đã biết.

        Args:
            self: Tham chiếu đến đối tượng hiện tại, chứa các thuộc tính như `a`, `b`, `c`, `p`, 
            `solution`, và `Value_to_find`.
            changes (bool): Biến cờ để theo dõi liệu có sự thay đổi nào được thực hiện trong quá trình tính toán.

        Returns:
            bool: Trả về `True` nếu có thay đổi được thực hiện, ngược lại trả về `False`.
    """
    if self.a and self.b and self.c and not self.p:
        self.p = (self.a + self.b + self.c) / 2  
        self.solution.append([16, f'\nTính cạnh p:\n({round(self.a)} + {round(self.b)} + {round(self.c)})/2 = {round(self.p)}'])
        self.Value_to_find.append([16, "p"]) 
        changes = True

    if self.p and self.a and self.b and not self.c:
        self.c = 2 * self.p - self.a - self.b 
        self.solution.append([17, f'\nTính cạnh c:\n2*{round(self.p)} - {round(self.a)} - {round(self.b)} = {round(self.c)}'])  
        self.Value_to_find.append([17, "c"])  
        changes = True

    if self.p and self.a and self.c and not self.b:
        self.b = 2 * self.p - self.a - self.c  
        self.solution.append([18, f'\nTính cạnh b:\n2*{round(self.p)} - {round(self.a)} - {round(self.c)} = {round(self.b)}'])  
        self.Value_to_find.append([18, "b"])
        changes = True

    if self.p and self.b and self.c and not self.a:
        self.a = 2 * self.p - self.b - self.c
        self.solution.append([19, f'\nTính cạnh a:\n2*{round(self.p)} - {round(self.b)} - {round(self.c)} = {round(self.a)}'])  
        self.Value_to_find.append([19, "a"])
        changes = True

    return changes

def Formula_4(self, changes):
    """
        Tính diện tích tam giác (S) bằng công thức Heron hoặc tính một cạnh (a, b, c) nếu diện tích đã biết.

        Args:
            self: Tham chiếu đến đối tượng hiện tại, chứa các thuộc tính như `a`, `b`, `c`, `S`, `p`, `solution`, và `Value_to_find`.
            changes (bool): Biến cờ để theo dõi liệu có sự thay đổi nào được thực hiện trong quá trình tính toán.

        Returns:
            bool: Trả về `True` nếu có thay đổi được thực hiện, ngược lại trả về `False`.
    """
    if self.p and self.a and self.b and self.c and not self.S:
        self.S = math.sqrt(self.p * (self.p - self.a) * (self.p - self.b) * (self.p - self.c))
        self.solution.append([20, f'\nTính diện tích S bằng công thức Heron:\nsqrt({round(self.p)}*({round(self.p)}-{round(self.a)})*({round(self.p)}-{round(self.b)})*({round(self.p)}-{round(self.c)}))={round(self.S)}'])
        self.Value_to_find.append([20, "S"])
        changes = True

    if self.S and self.p and self.b and self.c and not self.a:
        a_solved = self.p - self.b - self.c
        self.a = math.sqrt(2 * self.S / a_solved)
        self.solution.append([21, f'\nTính cạnh a:\nsqrt((2*{round(self.S)}/({round(self.p)}-{round(self.b)}-{round(self.c)}))={round(self.a)}'])
        self.Value_to_find.append([21, "a"])
        changes = True

    if self.S and self.p and self.a and self.c and not self.b:
        b_solved = self.p - self.a - self.c
        self.b = math.sqrt(2 * self.S / b_solved)
        self.solution.append([22, f'\nTính cạnh b:\nsqrt((2*{round(self.S)}/({round(self.p)}-{round(self.a)}-{round(self.c)}))={round(self.b)}'])
        self.Value_to_find.append([22, "b"])
        changes = True

    if self.S and self.p and self.a and self.b and not self.c:
        c_solved = self.p - self.a - self.b
        self.c = math.sqrt(2 * self.S / c_solved)
        self.solution.append([23, f'\nTính cạnh a:\nsqrt((2*{round(self.S)}/({round(self.p)}-{round(self.a)}-{round(self.b)}))={round(self.c)}'])
        self.Value_to_find.append([23, "c"])
        changes = True

    return changes
def Formula_5(self, changes):
    """
        Tính toán chiều cao (hc), diện tích (S), hoặc cạnh (c) của tam giác dựa trên các giá trị có sẵn.

        Args:
            self: Tham chiếu đến đối tượng hiện tại, chứa các thuộc tính như `S`, `c`, `hc`, `solution`, và `Value_to_find`.
            changes (bool): Biến cờ để theo dõi liệu có sự thay đổi nào được thực hiện trong quá trình tính toán.

        Returns:
            bool: Trả về `True` nếu có thay đổi được thực hiện, ngược lại trả về `False`.

    """
    if self.S and self.c and not self.hc:
        self.hc = (2 * self.S) / self.c
        self.solution.append([24, f'\nTính chiều cao hc:\n(2*{round(self.S)}/{round(self.c)}) = {round(self.hc)}'])
        self.Value_to_find.append([24, "hc"])
        changes = True

    if self.hc and self.c and not self.S:
        self.S = (self.hc * self.c) / 2
        self.solution.append([25, f'\nTính diện tích S:\n({round(self.hc)}*{round(self.c)})/2 = {round(self.S)}'])
        self.Value_to_find.append([25, "S"])
        changes = True

    if self.S and self.hc and not self.c:
        self.c = (2 * self.S) / self.hc
        self.solution.append([26, f'\nTính cạnh c:\n(2*{round(self.S)}/{round(self.hc)}) = {round(self.c)}'])
        self.Value_to_find.append([26, "c"])
        changes = True

    return changes
def Formula_6(self, changes):
    """
        Tính bán kính đường tròn ngoại tiếp (R), diện tích tam giác (S), hoặc các cạnh (a, b, c) của tam giác 
        dựa trên các giá trị có sẵn.

        Args:
            self: Tham chiếu đến đối tượng hiện tại, chứa các thuộc tính như `S`, `a`, `b`, `c`, `R`, `solution`, và `Value_to_find`.
            changes (bool): Biến cờ để theo dõi liệu có sự thay đổi nào được thực hiện trong quá trình tính toán.

        Returns:
            bool: Trả về `True` nếu có thay đổi được thực hiện, ngược lại trả về `False`.

    """
    if self.S and self.a and self.b and self.c and not self.R:
        self.R = (self.a * self.b * self.c) / (4 * self.S)
        self.solution.append([27,f'\nTính bán kính đường tròn ngoại tiếp R:\n({round(self.a)}*{round(self.b)}*{round(self.c)})/(4*{round(self.S)}) = {round(self.R)}'])
        self.Value_to_find.append([27, "R"])
        changes = True

    if self.R and self.a and self.b and self.c and not self.S:
        self.S = (self.a * self.b * self.c) / (4 * self.R)
        self.solution.append([28,f'\nTính diện tích tam giác S:\n({round(self.a)}*{round(self.b)}*{round(self.c)})/(4*{round(self.R)})={round(self.S)}'])
        self.Value_to_find.append([28, "S"])
        changes = True

    if self.S and self.R and self.a and self.b and not self.c:
        self.c = (4 * self.S * self.R) / (self.a * self.b)
        self.solution.append([29,f'\nTính cạnh c:\n(4*{round(self.S)}*{round(self.R)})/({round(self.a)}*{round(self.b)})={round(self.c)}'])
        self.Value_to_find.append([29, "c"])
        changes = True

    if self.S and self.R and self.a and self.c and not self.b:
        self.b = (4 * self.S * self.R) / (self.a * self.c)
        self.solution.append([30,f'\nTính cạnh b:\n(4*{round(self.S)}*{round(self.R)})/({round(self.a)}*{round(self.c)})={round(self.b)}'])
        self.Value_to_find.append([30, "b"])
        changes = True

    if self.S and self.R and self.b and self.c and not self.a:
        self.a = (4 * self.S * self.R) / (self.b * self.c)
        self.solution.append([31,f'\nTính cạnh a:\n(4*{round(self.S)}*{round(self.R)})/({round(self.b)}*{round(self.c)})={round(self.a)}'])
        self.Value_to_find.append([31, "a"])
        changes = True
    
    return changes
def Formula_7(self, changes):
    """
        Tính bán kính (r), diện tích (S) và nữa chu vi (p) của hình tròn hoặc tam giác
        dựa trên các giá trị đã có sẵn.

        Args:
            self: Tham chiếu đến đối tượng hiện tại, chứa các thuộc tính như `S`, `p`, `r`, `solution`, và `Value_to_find`.
            changes (bool): Biến cờ để theo dõi liệu có sự thay đổi nào được thực hiện trong quá trình tính toán.

        Returns:
            bool: Trả về `True` nếu có thay đổi được thực hiện, ngược lại trả về `False`.
    """
    if self.S and self.p and not self.r:
        self.r = self.S / self.p
        self.solution.append([32,f'\nTính bán kính r:\n{round(self.S)}/{round(self.p)}={round(self.r)}'])
        self.Value_to_find.append([32, "r"])
        changes = True

    if self.r and self.p and not self.S:
        self.S = self.r * self.p
        self.solution.append([33,f'\nTính diện S:\n{round(self.r)}/{round(self.p)}={round(self.S)}'])
        self.Value_to_find.append([33, "S"])
        changes = True

    if self.S and self.r and not self.p:
        self.p = self.S / self.r
        self.solution.append([34,f'\nTính nữa chu vi p:\n{round(self.S)}/{round(self.r)}={round(self.p)}'])
        self.Value_to_find.append([34, "p"])
        changes = True

    return changes
def Formula_8(self, changes):
    """
        Tính chu vi (C) hoặc nữa chu vi (p) của tam giác dựa trên các giá trị đã biết.

        Args:
            self (object): Đối tượng của lớp, chứa các thuộc tính như a, b, c, p, C.
            changes (bool): Biến đánh dấu xem có thay đổi giá trị nào trong quá trình tính toán hay không.

        return:
            bool: Trả về `True` nếu có thay đổi giá trị nào, `False` nếu không có thay đổi.
    """
    if self.a and self.b and self.c and not self.C:
        self.C=self.a+self.b+self.c
        self.solution.append([35,f'\nTính chu vi C:\n{round(self.a)}+{round(self.b)}+{round(self.c)}={round(self.C)}'])
        self.Value_to_find.append([35, "C"])
        changes = True

    if self.p and not self.C:
        self.C=self.p * 2
        self.solution.append([36,f'\nTính chu vi C:\n{round(self.p)}*2={round(self.C)}'])
        self.Value_to_find.append([36, "C"])
        changes = True

    if self.C and not self.p:
        self.p=self.C * 2
        self.solution.append([37,f'\nTính nữa chu vi p:\n{round(self.p)}*2={round(self.p)}'])
        self.Value_to_find.append([37, "p"])
        changes = True

    return changes





