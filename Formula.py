import math

def Formula_1(self, changes):
    if self.beta and self.delta and not self.alpha:
        self.alpha = math.pi - self.beta - self.delta
        print("Tính góc alpha: alpha =", math.degrees(self.alpha))
        self.loigiai.append([1, f'\nTính góc alpha: \n180-{round(math.degrees(self.beta))}-{round(math.degrees(self.delta))}={round(math.degrees(self.alpha))}'])
        self.Gia_tri_tinh.append([1, ":alpha"])
        changes = True
    if self.alpha and self.delta and not self.beta:
        self.beta = math.pi - self.alpha - self.delta
        self.loigiai.append([2, f'\nTính góc beta: \n180-{round(math.degrees(self.alpha))}-{round(math.degrees(self.delta))}={round(math.degrees(self.beta))}'])
        self.Gia_tri_tinh.append([2, "beta"])
        changes = True
    if self.alpha and self.beta and not self.delta:
        self.delta = math.pi - self.alpha - self.beta
        self.loigiai.append([3, f'\nTính góc delta: \n180-{round(math.degrees(self.alpha))}-{round(math.degrees(self.beta))}={round(math.degrees(self.delta))}'])
        self.Gia_tri_tinh.append([3, "delta"])
        changes = True
    return changes

def Formula_2(self, changes):
    if self.alpha and self.beta and self.b and not self.a:
        self.a = self.b * math.sin(self.alpha) / math.sin(self.beta)
        self.loigiai.append([4, f'\nTính cạnh a:\n({self.b}*sin({round(math.degrees(self.alpha))}))/sin({round(math.degrees(self.beta))})={round(self.a)}\n'])
        self.Gia_tri_tinh.append([4, "a"])
        changes = True

    if self.alpha and self.beta and self.a and not self.b:
        self.b = self.a * math.sin(self.beta) / math.sin(self.alpha)
        self.loigiai.append([5, f'\nTính cạnh b:\n({round(self.a)}*sin({round(math.degrees(self.beta))}))/sin({round(math.degrees(self.alpha))})={round(self.b)}\n'])
        self.Gia_tri_tinh.append([5, "b"])
        changes = True

    if self.alpha and self.delta and self.a and not self.c:
        self.c = self.a * math.sin(self.delta) / math.sin(self.alpha)
        self.loigiai.append([6, f'\nTính cạnh c: \n({round(self.a)}*sin({round(math.degrees(self.delta))}))/sin({round(math.degrees(self.alpha))})= {round(self.c)}\n'])
        self.Gia_tri_tinh.append([6, "c"])
        changes = True

    if self.alpha and self.delta and self.c and not self.a:
        self.a = self.c * math.sin(self.alpha) / math.sin(self.delta)
        self.loigiai.append([7, f'\nTính cạnh a:\n({round(self.c)}*sin({math.degrees(self.alpha)}))/sin({math.degrees(self.delta)})={round(self.a)}\n'])
        self.Gia_tri_tinh.append([7, "a"])
        changes = True

    if self.beta and self.delta and self.c and not self.b:
        self.b = self.c * math.sin(self.beta) / math.sin(self.delta)
        self.loigiai.append([8, f'\nTính cạnh b:\n({self.c}*sin({round(math.degrees(self.beta))}))/sin({round(math.degrees(self.delta))})={round(self.b)}\n'])
        print("Tính cạnh b bằng công thức sin: b =", self.b)
        self.Gia_tri_tinh.append([8, "b"])
        changes = True

    if self.beta and self.delta and self.b and not self.c:
        self.c = self.b * math.sin(self.delta) / math.sin(self.beta)
        self.loigiai.append([9, f'\nTính cạnh c:\n({round(self.b)}*sin({round(math.degrees(self.delta))}))/sin({round(math.degrees(self.beta))})={round(self.c)}\n'])
        self.Gia_tri_tinh.append([9, "c"])
        changes = True

    if self.a and self.b and self.beta and not self.alpha:
        self.alpha = math.asin(max(-1, min(1, self.a * math.sin(self.beta) / self.b)))
        self.loigiai.append([10, f'\nTính góc alpha:\nsin^(-1)({round(self.a)}*sin({round(math.degrees(self.beta))}))/{round(self.b)}\n'])
        self.Gia_tri_tinh.append([10, "alpha"])
        changes = True

    if self.b and self.c and self.delta and not self.beta:
        self.beta = math.asin(max(-1, min(1, self.b * math.sin(self.delta) / self.c)))
        self.loigiai.append([11, f'\nTính góc beta:\nsin^(-1)({round(self.b)}*sin({round(math.degrees(self.delta))}))/{round(self.c)}\n'])
        self.Gia_tri_tinh.append([11, "beta"])
        changes = True

    if self.a and self.c and self.alpha and not self.delta:
        self.delta = math.asin(max(-1, min(1, self.c * math.sin(self.alpha) / self.a)))
        self.loigiai.append([12, f'\nTính góc delta:\nsin^(-1)({round(self.c)}*sin({round(math.degrees(self.alpha))}))/{round(self.a)}\n'])
        self.Gia_tri_tinh.append([12, "delta"])
        changes = True

    if self.a and self.c and self.delta and not self.alpha:
        self.alpha = math.asin(max(-1, min(1, self.a * math.sin(self.delta) / self.c)))
        self.loigiai.append([13, f'\nTính góc alpha:\nsin^(-1)({round(self.a)}*sin({round(math.degrees(self.delta))}))/{round(self.c)}\n'])
        self.Gia_tri_tinh.append([13, "alpha"])
        changes = True

    if self.b and self.a and self.alpha and not self.beta:
        self.beta = math.asin(max(-1, min(1, self.b * math.sin(self.alpha) / self.a)))
        self.loigiai.append([14, f'\nTính góc beta:\nsin^(-1)({round(self.b)}*sin({round(math.degrees(self.alpha))}))/{round(self.a)}\n'])
        self.Gia_tri_tinh.append([14, "beta"])
        changes = True

    if self.b and self.c and self.beta and not self.delta:
        self.delta = math.asin(max(-1, min(1, self.c * math.sin(self.beta) / self.b)))
        self.loigiai.append([15, f'\nTính góc delta:\nsin^(-1)({round(self.c)}*sin({round(math.degrees(self.beta))}))/{round(self.b)}\n'])
        self.Gia_tri_tinh.append([15, "delta"])
        changes = True

def Formula_3(self, changes):
    if self.a and self.b and self.c and not self.p:
        self.p = (self.a + self.b + self.c) / 2  
        self.loigiai.append([16, f'\nTính cạnh p:\n({round(self.a)} + {round(self.b)} + {round(self.c)})/2 = {round(self.p)}'])
        self.Gia_tri_tinh.append([16, "p"]) 
        changes = True

    if self.p and self.a and self.b and not self.c:
        self.c = 2 * self.p - self.a - self.b 
        self.loigiai.append([17, f'\nTính cạnh c:\n2*{round(self.p)} - {round(self.a)} - {round(self.b)} = {round(self.c)}'])  
        self.Gia_tri_tinh.append([17, "c"])  
        changes = True

    if self.p and self.a and self.c and not self.b:
        self.b = 2 * self.p - self.a - self.c  
        self.loigiai.append([18, f'\nTính cạnh b:\n2*{round(self.p)} - {round(self.a)} - {round(self.c)} = {round(self.b)}'])  
        self.Gia_tri_tinh.append([18, "b"])
        changes = True

    if self.p and self.b and self.c and not self.a:
        self.a = 2 * self.p - self.b - self.c
        self.loigiai.append([19, f'\nTính cạnh a:\n2*{round(self.p)} - {round(self.b)} - {round(self.c)} = {round(self.a)}'])  
        self.Gia_tri_tinh.append([19, "a"])
        changes = True
    return changes

def Formula_4(self, changes):
    if self.p and self.a and self.b and self.c and not self.S:
        self.S = math.sqrt(self.p * (self.p - self.a) * (self.p - self.b) * (self.p - self.c))
        self.loigiai.append([20, f'\nTính diện tích S bằng công thức Heron:\nsqrt({round(self.p)}*({round(self.p)}-{round(self.a)})*({round(self.p)}-{round(self.b)})*({round(self.p)}-{round(self.c)}))={round(self.S)}'])
        self.Gia_tri_tinh.append([20, "S"])
        changes = True

    if self.S and self.p and self.b and self.c and not self.a:
        a_solved = self.p - self.b - self.c
        self.a = math.sqrt(2 * self.S / a_solved)
        self.loigiai.append([21, f'\nTính cạnh a:\nsqrt((2*{round(self.S)}/({round(self.p)}-{round(self.b)}-{round(self.c)}))={round(self.a)}'])
        self.Gia_tri_tinh.append([21, "a"])
        changes = True

    if self.S and self.p and self.a and self.c and not self.b:
        b_solved = self.p - self.a - self.c
        self.b = math.sqrt(2 * self.S / b_solved)
        self.loigiai.append([22, f'\nTính cạnh b:\nsqrt((2*{round(self.S)}/({round(self.p)}-{round(self.a)}-{round(self.c)}))={round(self.b)}'])
        self.Gia_tri_tinh.append([22, "b"])
        changes = True

    if self.S and self.p and self.a and self.b and not self.c:
        c_solved = self.p - self.a - self.b
        self.c = math.sqrt(2 * self.S / c_solved)
        self.loigiai.append([23, f'\nTính cạnh a:\nsqrt((2*{round(self.S)}/({round(self.p)}-{round(self.a)}-{round(self.b)}))={round(self.c)}'])
        self.Gia_tri_tinh.append([23, "c"])
        changes = True

    return changes
def Formula_5(self, changes):
    if self.S and self.c and not self.hc:
        self.hc = (2 * self.S) / self.c
        self.loigiai.append([24, f'\nTính chiều cao hc:\n(2*{round(self.S)}/{round(self.c)}) = {round(self.hc)}'])
        self.Gia_tri_tinh.append([24, "hc"])
        changes = True

    if self.hc and self.c and not self.S:
        self.S = (self.hc * self.c) / 2
        self.loigiai.append([25, f'\nTính diện tích S:\n({round(self.hc)}*{round(self.c)})/2 = {round(self.S)}'])
        self.Gia_tri_tinh.append([25, "S"])
        changes = True

    if self.S and self.hc and not self.c:
        self.c = (2 * self.S) / self.hc
        self.loigiai.append([26, f'\nTính cạnh c:\n(2*{round(self.S)}/{round(self.hc)}) = {round(self.c)}'])
        self.Gia_tri_tinh.append([26, "c"])
        changes = True
    return changes
def Formula_6(self, changes):
    if self.S and self.a and self.b and self.c and not self.R:
        self.R = (self.a * self.b * self.c) / (4 * self.S)
        self.loigiai.append([27,f'\nTính bán kính đường tròn ngoại tiếp R:\n({round(self.a)}*{round(self.b)}*{round(self.c)})/(4*{round(self.S)}) = {round(self.R)}'])
        self.Gia_tri_tinh.append([27, "R"])
        changes = True

    if self.R and self.a and self.b and self.c and not self.S:
        self.S = (self.a * self.b * self.c) / (4 * self.R)
        self.loigiai.append([28,f'\nTính diện tích tam giác S:\n({round(self.a)}*{round(self.b)}*{round(self.c)})/(4*{round(self.R)})={round(self.S)}'])
        self.Gia_tri_tinh.append([28, "S"])
        changes = True

    if self.S and self.R and self.a and self.b and not self.c:
        self.c = (4 * self.S * self.R) / (self.a * self.b)
        self.loigiai.append([29,f'\nTính cạnh c:\n(4*{round(self.S)}*{round(self.R)})/({round(self.a)}*{round(self.b)})={round(self.c)}'])
        self.Gia_tri_tinh.append([29, "c"])
        changes = True

    if self.S and self.R and self.a and self.c and not self.b:
        self.b = (4 * self.S * self.R) / (self.a * self.c)
        self.loigiai.append([30,f'\nTính cạnh b:\n(4*{round(self.S)}*{round(self.R)})/({round(self.a)}*{round(self.c)})={round(self.b)}'])
        self.Gia_tri_tinh.append([30, "b"])
        changes = True

    if self.S and self.R and self.b and self.c and not self.a:
        self.a = (4 * self.S * self.R) / (self.b * self.c)
        self.loigiai.append([31,f'\nTính cạnh a:\n(4*{round(self.S)}*{round(self.R)})/({round(self.b)}*{round(self.c)})={round(self.a)}'])
        self.Gia_tri_tinh.append([31, "a"])
        changes = True
def Formula_7(self, changes):
    if self.S and self.p and not self.r:
        self.r = self.S / self.p
        self.loigiai.append([32,f'\nTính bán kính r:\n{round(self.S)}/{round(self.p)}={round(self.r)}'])
        self.Gia_tri_tinh.append([32, "r"])
        changes = True

    if self.r and self.p and not self.S:
        self.S = self.r * self.p
        self.loigiai.append([33,f'\nTính diện S:\n{round(self.r)}/{round(self.p)}={round(self.S)}'])
        self.Gia_tri_tinh.append([33, "S"])
        changes = True

    if self.S and self.r and not self.p:
        self.p = self.S / self.r
        self.loigiai.append([34,f'\nTính nữa chu vi p:\n{round(self.S)}/{round(self.r)}={round(self.p)}'])
        self.Gia_tri_tinh.append([34, "p"])
        changes = True



